from __future__ import annotations

import base64
import json
import logging
import os
import re
import threading
import urllib.parse
import urllib.request
from email import policy
from email.parser import BytesParser
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

from O365 import Account
from O365.utils import BaseTokenBackend
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


_USERS_LOCK = threading.Lock()
logger = logging.getLogger(__name__)

# Escopos OAuth explícitos do Microsoft Graph para Outlook (delegated).
DEFAULT_SCOPES = [
    "https://graph.microsoft.com/Mail.ReadWrite",
    "offline_access",
]
DEFAULT_ARTESP_EMAIL = "artesp.nc@conservacao.br"
RESERVED_O365_SCOPES = {"openid", "profile", "offline_access"}


@dataclass(frozen=True)
class OutlookOAuthConfig:
    client_id: str
    client_secret: str
    tenant_id: str
    redirect_uri: str
    scopes: tuple[str, ...] = tuple(DEFAULT_SCOPES)

    @staticmethod
    def from_env() -> "OutlookOAuthConfig":
        # Garante leitura do .env em ambiente local mesmo quando o cwd do processo varia.
        here = Path(__file__).resolve()
        repo_root = here.parent.parent
        load_dotenv(repo_root / ".env", override=False)
        load_dotenv(here.parent / ".env", override=False)
        load_dotenv(override=False)
        client_id = (
            os.getenv("CLIENT_ID")
            or os.getenv("O365_CLIENT_ID")
            or os.getenv("ARTESP_CLIENT_ID")
            or ""
        ).strip()
        client_secret = (
            os.getenv("CLIENT_SECRET")
            or os.getenv("O365_CLIENT_SECRET")
            or os.getenv("ARTESP_CLIENT_SECRET")
            or ""
        ).strip()
        tenant_id = (
            os.getenv("TENANT_ID")
            or os.getenv("O365_TENANT_ID")
            or os.getenv("ARTESP_TENANT_ID")
            or os.getenv("AZURE_TENANT_ID")
            or ""
        ).strip()
        redirect_uri = (
            os.getenv("REDIRECT_URI")
            or os.getenv("O365_REDIRECT_URI")
            or os.getenv("ARTESP_REDIRECT_URI")
            or ""
        ).strip()
        scopes_raw = (
            os.getenv("OUTLOOK_SCOPES")
            or os.getenv("O365_SCOPES")
            or os.getenv("ARTESP_OUTLOOK_SCOPES")
            or ""
        ).strip()
        if not client_id:
            raise RuntimeError("CLIENT_ID não configurado no ambiente.")
        if not client_secret:
            raise RuntimeError("CLIENT_SECRET não configurado no ambiente.")
        if not tenant_id:
            tenant_id = "common"
        if not redirect_uri:
            raise RuntimeError("REDIRECT_URI não configurado no ambiente.")
        scopes = tuple(
            [s.strip() for s in scopes_raw.split(",") if s.strip()]
            if scopes_raw
            else DEFAULT_SCOPES
        )
        return OutlookOAuthConfig(
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id,
            redirect_uri=redirect_uri,
            scopes=scopes,
        )


class OAuthDbStore:
    """
    Persistência de token/flow OAuth no banco (Render Postgres via DATABASE_URL).
    Não grava token em arquivo local.
    """

    def __init__(self, database_url: str | None = None):
        self.database_url = (database_url or os.getenv("DATABASE_URL") or "").strip()
        if not self.database_url:
            raise RuntimeError("DATABASE_URL não configurado. Necessário para persistir token OAuth.")
        self._is_sqlite = self.database_url.lower().startswith("sqlite")
        if self._is_sqlite:
            self.database_url = self._normalizar_sqlite_url(self.database_url)
            self._garantir_pasta_sqlite(self.database_url)
        if self._is_sqlite:
            self.engine = create_engine(
                self.database_url,
                connect_args={"check_same_thread": False},
            )
        else:
            self.engine = create_engine(self.database_url)
        try:
            self._ensure_schema()
        except SQLAlchemyError as e:
            if self._is_sqlite:
                raise RuntimeError(
                    "DATABASE_URL sqlite inválido ou arquivo de banco indisponível para OAuth Outlook. "
                    "Verifique caminho, permissões e formato (ex.: sqlite:///./local_test.db). "
                    f"Detalhe técnico: {e}"
                ) from e
            raise RuntimeError(
                "DATABASE_URL inválido ou banco indisponível para OAuth Outlook. "
                "Verifique host, porta, usuário, senha e conectividade."
            ) from e

    @staticmethod
    def _normalizar_sqlite_url(database_url: str) -> str:
        url = (database_url or "").strip()
        if not url.lower().startswith("sqlite:///"):
            raise RuntimeError(
                "DATABASE_URL sqlite inválido. Use formato sqlite:///./local_test.db "
                "ou sqlite:////caminho/absoluto/local_test.db"
            )
        path_part = url[len("sqlite:///"):]
        if not path_part:
            raise RuntimeError("DATABASE_URL sqlite inválido: caminho do arquivo não informado.")
        if path_part == ":memory:":
            return "sqlite:///:memory:"
        # Normaliza barras para evitar interpretação UNC inválida no Windows.
        path_part = path_part.replace("\\", "/")
        # Caso comum de absoluto Windows vindo como /C:/...
        if len(path_part) >= 3 and path_part[0] == "/" and path_part[2] == ":":
            path_part = path_part[1:]
        # Caminho absoluto (Windows drive ou Unix-style).
        if Path(path_part).is_absolute():
            abs_posix = Path(path_part).resolve().as_posix()
            return f"sqlite:///{abs_posix}"
        # Caminho relativo: ancora na raiz do repositório, não no cwd do processo.
        repo_root = Path(__file__).resolve().parent.parent
        abs_path = (repo_root / path_part).resolve()
        abs_posix = abs_path.as_posix()
        return f"sqlite:///{abs_posix}"

    @staticmethod
    def _garantir_pasta_sqlite(sqlite_url: str) -> None:
        path_part = sqlite_url[len("sqlite:///"):]
        if path_part == ":memory:":
            return
        db_path = Path(path_part)
        db_path.parent.mkdir(parents=True, exist_ok=True)

    def _ensure_schema(self) -> None:
        if self._is_sqlite:
            ddl = """
                CREATE TABLE IF NOT EXISTS oauth_outlook_tokens (
                    user_id TEXT PRIMARY KEY,
                    token_json TEXT NULL,
                    oauth_flow_json TEXT NULL,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """
        else:
            ddl = """
                CREATE TABLE IF NOT EXISTS oauth_outlook_tokens (
                    user_id TEXT PRIMARY KEY,
                    token_json TEXT NULL,
                    oauth_flow_json TEXT NULL,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """
        with self.engine.begin() as conn:
            conn.execute(text(ddl))

    def _now_expr(self) -> str:
        return "CURRENT_TIMESTAMP" if self._is_sqlite else "NOW()"

    def _upsert_sql(self) -> str:
        now_expr = self._now_expr()
        return f"""
            INSERT INTO oauth_outlook_tokens (user_id, token_json, oauth_flow_json, updated_at)
            VALUES (:user_id, :token_json, :oauth_flow_json, {now_expr})
            ON CONFLICT (user_id) DO UPDATE
            SET token_json = COALESCE(excluded.token_json, oauth_outlook_tokens.token_json),
                oauth_flow_json = COALESCE(excluded.oauth_flow_json, oauth_outlook_tokens.oauth_flow_json),
                updated_at = {now_expr}
        """

    def _clear_flow_sql(self) -> str:
        now_expr = self._now_expr()
        return f"""
            UPDATE oauth_outlook_tokens
            SET oauth_flow_json = NULL, updated_at = {now_expr}
            WHERE user_id = :user_id
        """

    def get_record(self, user_id: str) -> dict[str, Any]:
        uid = (user_id or "").strip().lower()
        if not uid:
            return {}
        with self.engine.connect() as conn:
            row = conn.execute(
                text(
                    "SELECT token_json, oauth_flow_json FROM oauth_outlook_tokens WHERE user_id = :user_id"
                ),
                {"user_id": uid},
            ).mappings().first()
        if not row:
            return {}
        token_json = row.get("token_json")
        flow_json = row.get("oauth_flow_json")
        out: dict[str, Any] = {}
        if token_json:
            try:
                out["o365_token"] = json.loads(token_json)
            except json.JSONDecodeError:
                out["o365_token"] = None
        if flow_json:
            try:
                out["o365_oauth_flow"] = json.loads(flow_json)
            except json.JSONDecodeError:
                out["o365_oauth_flow"] = None
        return out

    def upsert_record(self, user_id: str, token: Any = None, flow: Any = None) -> None:
        uid = (user_id or "").strip().lower()
        if not uid:
            raise ValueError("user_id inválido")
        token_json = (
            token if isinstance(token, str) else self._json_dumps_safe(token)
        ) if token is not None else None
        flow_json = (
            flow if isinstance(flow, str) else self._json_dumps_safe(flow)
        ) if flow is not None else None
        with self.engine.begin() as conn:
            conn.execute(
                text(self._upsert_sql()),
                {"user_id": uid, "token_json": token_json, "oauth_flow_json": flow_json},
            )

    def save_token(self, user_id: str, token: Any) -> None:
        """Persistência explícita do token OAuth no banco."""
        self.upsert_record(user_id=user_id, token=token)

    @staticmethod
    def _json_dumps_safe(obj: Any) -> str:
        def _default(v: Any) -> Any:
            if isinstance(v, (datetime, date)):
                return v.isoformat()
            return str(v)
        return json.dumps(obj, ensure_ascii=False, default=_default)

    def clear_flow(self, user_id: str) -> None:
        uid = (user_id or "").strip().lower()
        with self.engine.begin() as conn:
            conn.execute(text(self._clear_flow_sql()), {"user_id": uid})


class DbTokenBackend(BaseTokenBackend):
    def __init__(self, store: OAuthDbStore, user_id: str, token_field: str = "o365_token"):
        super().__init__()
        self.store = store
        self.user_id = (user_id or "").strip().lower()
        self.token_field = token_field
        self.token = None

    def load_token(self) -> bool:
        user = self.store.get_record(self.user_id)
        token = user.get(self.token_field)
        if not token:
            self._cache = {}
            self.token = None
            return False
        if isinstance(token, str):
            cache = self.deserialize(token)
        elif isinstance(token, dict):
            cache = token
        else:
            cache = self.deserialize(str(token))
        self._cache = cache or {}
        self.token = self._cache
        return self.has_data

    def save_token(self, force: bool = False):
        if not self._has_state_changed and not force:
            return True
        serialized_cache = self.serialize()
        self.store.upsert_record(self.user_id, token=serialized_cache)
        return True

    def delete_token(self):
        self.store.upsert_record(self.user_id, token={})
        self._cache = {}
        self.token = None
        return True

    def check_token(self):
        self.load_token()
        return self.has_data


def _create_account(config: OutlookOAuthConfig, token_backend: DbTokenBackend) -> Account:
    credentials = (config.client_id, config.client_secret)
    # Suporta single-tenant (GUID) e multitenant (common/organizations/consumers).
    return Account(
        credentials=credentials,
        tenant_id=config.tenant_id,
        auth_flow_type="authorization",
        token_backend=token_backend,
    )


def _token_dict_parece_valido(token: Any) -> bool:
    return isinstance(token, dict) and any(k in token for k in ("access_token", "refresh_token"))


def _extrair_token_reflexivo(*objs: Any) -> dict[str, Any] | None:
    """
    Tenta extrair token OAuth de objetos internos da lib O365.
    """
    # 1) getters usuais
    for obj in objs:
        if obj is None:
            continue
        for nome in ("get_token", "load_token"):
            fn = getattr(obj, nome, None)
            if callable(fn):
                try:
                    tok = fn()
                    if _token_dict_parece_valido(tok):
                        return tok
                except Exception:
                    pass
        tok = getattr(obj, "token", None)
        if _token_dict_parece_valido(tok):
            return tok

    # 2) varredura rasa de __dict__ procurando dict com access/refresh token
    visitados: set[int] = set()
    fila = [o for o in objs if o is not None]
    depth = 0
    while fila and depth < 3:
        prox: list[Any] = []
        for cur in fila:
            oid = id(cur)
            if oid in visitados:
                continue
            visitados.add(oid)
            if _token_dict_parece_valido(cur):
                return cur  # type: ignore[return-value]
            d = getattr(cur, "__dict__", None)
            if not isinstance(d, dict):
                continue
            for v in d.values():
                if _token_dict_parece_valido(v):
                    return v
                if hasattr(v, "__dict__"):
                    prox.append(v)
        fila = prox
        depth += 1
    return None


def _extrair_email_callback_oauth(requested_url: str) -> str:
    """Extrai e-mail do callback OAuth (client_info/preferred_username)."""
    try:
        q = urllib.parse.parse_qs(urllib.parse.urlparse(requested_url).query or "")
        client_info = (q.get("client_info", [""])[0] or "").strip()
        if not client_info:
            return ""
        pad = "=" * ((4 - (len(client_info) % 4)) % 4)
        raw = base64.urlsafe_b64decode((client_info + pad).encode("ascii"))
        obj = json.loads(raw.decode("utf-8", errors="ignore"))
        email = (
            str(obj.get("preferred_username") or obj.get("upn") or "").strip().lower()
        )
        return email
    except Exception:
        return ""


def iniciar_oauth_usuario(
    user_id: str,
    config: OutlookOAuthConfig,
    redirect_uri: str | None = None,
) -> dict[str, Any]:
    store = OAuthDbStore()
    token_backend = DbTokenBackend(store, user_id)
    account = _create_account(config, token_backend)
    callback_uri = (redirect_uri or "").strip() or config.redirect_uri
    requested_scopes = [
        s for s in config.scopes if (s or "").strip().lower() not in RESERVED_O365_SCOPES
    ]
    if not requested_scopes:
        requested_scopes = ["https://graph.microsoft.com/Mail.ReadWrite"]
    url, flow = account.con.get_authorization_url(
        requested_scopes=requested_scopes,
        redirect_uri=callback_uri,
    )
    store.upsert_record(user_id, flow=flow)
    return {"authorization_url": url}


def concluir_oauth_usuario(
    user_id: str,
    config: OutlookOAuthConfig,
    requested_url: str,
) -> bool:
    store = OAuthDbStore()
    user = store.get_record(user_id)
    flow = user.get("o365_oauth_flow")
    if not flow:
        raise RuntimeError("Fluxo OAuth não encontrado para o usuário.")
    token_backend = DbTokenBackend(store, user_id)
    account = _create_account(config, token_backend)
    # 1) Captura code/state no requested_url e 2) troca por token real.
    try:
        request_token_result = account.con.request_token(requested_url, flow=flow)
        ok = bool(request_token_result)
        logger.info("OAuth callback: request_token_result=%s user_id=%s", ok, user_id)
        if not ok:
            q = urllib.parse.parse_qs(urllib.parse.urlparse(requested_url).query or "")
            err = (q.get("error", [""])[0] or "").strip()
            err_desc = (q.get("error_description", [""])[0] or "").strip()
            detalhe = err_desc or err or f"request_token=False sem detalhe do provedor. retorno={request_token_result!r}"
            raise RuntimeError(f"Falha na troca do código OAuth por token: {detalhe}")

        # 3) Persistência oficial do cache OAuth no backend customizado.
        account.con.token_backend.save_token(force=True)
        token_cache_serialized = account.con.token_backend.serialize()
        if not token_cache_serialized:
            logger.error("OAuth callback: cache OAuth vazio após request_token user_id=%s", user_id)
            raise RuntimeError("OAuth concluído sem token persistível. Revogue e autentique novamente.")

        # 4) Identifica usuário da conta Microsoft (quando disponível).
        user_email = (user_id or "").strip().lower()
        email_callback = _extrair_email_callback_oauth(requested_url)
        if email_callback:
            user_email = email_callback
        try:
            u = account.get_current_user()
            mail = (getattr(u, "mail", None) or getattr(u, "user_principal_name", None) or "").strip().lower()
            if mail:
                user_email = mail
        except Exception:
            pass

        # 5) FORÇA persistência no SQLite/DB.
        try:
            store.save_token(user_email, token_cache_serialized)
            logger.info("OAuth callback: token persistido para user_email=%s", user_email)
            # Mantém compatibilidade com o usuário logado na aplicação.
            if user_email != (user_id or "").strip().lower():
                store.save_token(user_id, token_cache_serialized)
                logger.info("OAuth callback: token espelhado para user_id_sessao=%s", user_id)
        except Exception as db_err:
            logger.exception("OAuth callback: erro de persistência do token")
            raise RuntimeError(f"Erro ao persistir token OAuth: {db_err}") from db_err

        # Confirma persistência (has_token=1) antes de concluir.
        rec = store.get_record(user_email) or store.get_record(user_id)
        if not rec.get("o365_token"):
            raise RuntimeError("OAuth concluído sem token persistível. Revogue e autentique novamente.")

        store.clear_flow(user_id)
        if user_email != (user_id or "").strip().lower():
            store.clear_flow(user_email)
        return True
    except RuntimeError:
        raise
    except Exception as e:
        logger.exception("OAuth callback: erro fatal")
        raise RuntimeError(f"Erro fatal no callback OAuth: {e}") from e


def _graph_headers() -> dict[str, str]:
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "ConsistencyLevel": "eventual",
    }


def _find_message_by_nc_id(con, nc_id: str) -> dict[str, Any] | None:
    nc_id = (nc_id or "").strip()
    if not nc_id:
        return None
    q = urllib.parse.quote(f'"subject:{nc_id}"')
    url = f"https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages?$search={q}&$top=1"
    resp = con.get(url, headers=_graph_headers(), timeout=20)
    resp.raise_for_status()
    data = resp.json()
    values = data.get("value", [])
    return values[0] if values else None


def _download_bytes(url: str, timeout_s: int = 20) -> bytes:
    raw = str(url or "").strip()
    if not raw:
        raise ValueError("URL/caminho de imagem vazio.")
    p = Path(raw)
    if p.is_file():
        return p.read_bytes()
    if raw.lower().startswith("file://"):
        file_path = urllib.request.url2pathname(raw[7:])
        p2 = Path(file_path)
        if p2.is_file():
            return p2.read_bytes()
    with urllib.request.urlopen(raw, timeout=timeout_s) as r:
        return r.read()


def _guess_mime(url: str) -> str:
    u = url.lower()
    if u.endswith(".png"):
        return "image/png"
    if u.endswith(".gif"):
        return "image/gif"
    if u.endswith(".webp"):
        return "image/webp"
    return "image/jpeg"


def _parse_eml_payload(eml_path: str) -> dict[str, Any]:
    path = Path(str(eml_path or "").strip())
    if not path.is_file():
        raise FileNotFoundError(f".eml não encontrado: {path}")
    msg = BytesParser(policy=policy.default).parsebytes(path.read_bytes())
    subject = str(msg.get("subject") or "").strip()
    html = ""
    inlines: list[dict[str, Any]] = []
    seq = 0
    for part in msg.walk():
        if part.is_multipart():
            continue
        ctype = (part.get_content_type() or "").lower()
        if ctype == "text/html" and not html:
            try:
                html = part.get_content() or ""
            except Exception:
                html = ""
            continue
        if not ctype.startswith("image/"):
            continue
        raw = part.get_payload(decode=True)
        if not raw:
            continue
        cid_raw = str(part.get("Content-ID") or "").strip()
        cid = cid_raw.strip("<>").strip()
        if not cid:
            seq += 1
            cid = f"emlimg{seq:03d}"
        inlines.append(
            {
                "cid": cid,
                "name": part.get_filename() or f"{cid}.jpg",
                "content_type": ctype or "image/jpeg",
                "content_bytes": raw,
            }
        )
    return {"subject": subject, "html": html, "inline_images": inlines}


def _normalizar_html_cids(html: str, cids: list[str]) -> str:
    out = str(html or "")
    if not out or not cids:
        return out
    mapa = {c.lower(): c for c in cids}
    refs = re.findall(r"cid:([^'\" >]+)", out, flags=re.IGNORECASE)
    for ref in refs:
        k = str(ref or "").strip().strip("<>").lower()
        alvo = mapa.get(k)
        if not alvo:
            continue
        out = re.sub(
            rf"cid:\s*{re.escape(ref)}",
            f"cid:{alvo}",
            out,
            flags=re.IGNORECASE,
        )
    return out


def _montar_html_superacao(dados: dict[str, Any], cids: list[str]) -> str:
    resumo = str(dados.get("linha_resumo") or "").strip()
    imgs = "".join(
        f"<p style='margin:10px 0;'><img src='cid:{cid}' style='max-width:720px;width:100%;height:auto;border:0;' /></p>"
        for cid in cids
    )
    return (
        "<div style='font-family:Calibri,Arial,sans-serif;font-size:11pt;color:#000;'>"
        "<p>Prezados,</p>"
        "<p>Seguem registros fotográficos das superações de não conformidade, dentro do prazo regulamentado.</p>"
        + (f"<p>{resumo}</p>" if resumo else "")
        + imgs
        + "</div>"
    )


def gerar_rascunho_nc(
    *,
    user_id: str,
    oauth_config: OutlookOAuthConfig,
    dados_csv: dict[str, Any],
    email_artesp: str = DEFAULT_ARTESP_EMAIL,
) -> dict[str, Any]:
    """
    Gera rascunho de e-mail NC:
    - Reply ao e-mail encontrado por ID NC no assunto da inbox
    - Se não encontrar, cria novo draft para ARTESP
    - Corpo em HTML com imagens inline (ou HTML do .eml do job, quando existir)
    """
    store = OAuthDbStore()
    token_backend = DbTokenBackend(store, user_id)
    account = _create_account(oauth_config, token_backend)

    if not account.is_authenticated:
        raise RuntimeError("Usuário não autenticado no Outlook. Execute o OAuth antes.")

    con = account.con
    nc_id = str(dados_csv.get("id_nc") or "").strip()
    if not nc_id:
        raise ValueError("dados_csv.id_nc é obrigatório")

    fotos_links = dados_csv.get("links_fotos") or dados_csv.get("fotos") or []
    if isinstance(fotos_links, str):
        fotos_links = [x.strip() for x in fotos_links.split(";") if x.strip()]
    eml_path = str(dados_csv.get("eml_path") or "").strip()
    eml_payload: dict[str, Any] | None = None
    if eml_path:
        eml_payload = _parse_eml_payload(eml_path)

    encontrado = _find_message_by_nc_id(con, nc_id)
    if encontrado:
        draft = None
        modo = "reply_all"
        for acao in ("createReplyAll", "createReply"):
            r = con.post(
                f"https://graph.microsoft.com/v1.0/me/messages/{encontrado['id']}/{acao}",
                headers=_graph_headers(),
                timeout=20,
            )
            if r.status_code >= 400:
                continue
            draft = r.json()
            modo = "reply_all" if acao == "createReplyAll" else "reply"
            break
        if not draft:
            raise RuntimeError(
                "Falha ao criar rascunho de resposta no e-mail recebido (ReplyAll/Reply)."
            )
    else:
        assunto = str(dados_csv.get("assunto") or "").strip() or f"RES: Superação NC {nc_id}"
        r = con.post(
            "https://graph.microsoft.com/v1.0/me/messages",
            headers=_graph_headers(),
            data={
                "subject": assunto,
                "toRecipients": [{"emailAddress": {"address": email_artesp}}],
            },
            timeout=20,
        )
        r.raise_for_status()
        draft = r.json()
        modo = "novo"

    draft_id = draft["id"]
    cids: list[str] = []
    inline_eml = (eml_payload or {}).get("inline_images") or []
    for img in inline_eml:
        cid = str(img.get("cid") or "").strip()
        raw = img.get("content_bytes") or b""
        if not cid or not raw:
            continue
        cids.append(cid)
        a = con.post(
            f"https://graph.microsoft.com/v1.0/me/messages/{draft_id}/attachments",
            headers=_graph_headers(),
            data={
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": str(img.get("name") or f"{cid}.jpg"),
                "contentType": str(img.get("content_type") or "image/jpeg"),
                "isInline": True,
                "contentId": cid,
                "contentBytes": base64.b64encode(raw).decode("ascii"),
            },
            timeout=30,
        )
        a.raise_for_status()

    # Reforço: mesmo com .eml, adiciona também fotos do job como fallback.
    base_seq = len(cids)
    for i, link in enumerate(fotos_links, start=1):
        raw = _download_bytes(link)
        cid = f"ncimg{base_seq + i:03d}"
        cids.append(cid)
        a = con.post(
            f"https://graph.microsoft.com/v1.0/me/messages/{draft_id}/attachments",
            headers=_graph_headers(),
            data={
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": f"foto_{base_seq + i:03d}.jpg",
                "contentType": _guess_mime(link),
                "isInline": True,
                "contentId": cid,
                "contentBytes": base64.b64encode(raw).decode("ascii"),
            },
            timeout=30,
        )
        a.raise_for_status()

    assunto_final = (
        str((eml_payload or {}).get("subject") or "").strip()
        or str(dados_csv.get("assunto") or "").strip()
        or f"RES: Superação NC {nc_id}"
    )
    html = str((eml_payload or {}).get("html") or "").strip()
    if not html:
        html = _montar_html_superacao(dados_csv, cids)
    else:
        html = _normalizar_html_cids(html, cids)
        tem_img_inline = bool(
            re.search(r"<img[^>]+src\s*=\s*[\"']?\s*cid:", html, flags=re.IGNORECASE)
        )
        if cids and not tem_img_inline:
            html += "".join(
                f"<p style='margin:10px 0;'><img src='cid:{cid}' style='max-width:720px;width:100%;height:auto;border:0;' /></p>"
                for cid in cids
            )
    if cids and not re.search(r"<img[^>]+src\s*=\s*[\"']?\s*cid:", html, flags=re.IGNORECASE):
        html += "".join(
            f"<p style='margin:10px 0;'><img src='cid:{cid}' style='max-width:720px;width:100%;height:auto;border:0;' /></p>"
            for cid in cids
        )
    p = con.patch(
        f"https://graph.microsoft.com/v1.0/me/messages/{draft_id}",
        headers=_graph_headers(),
        data={"subject": assunto_final, "body": {"contentType": "HTML", "content": html}},
        timeout=20,
    )
    p.raise_for_status()
    # Validação final: confirma no Graph que o item existe e está em rascunhos.
    chk = con.get(
        f"https://graph.microsoft.com/v1.0/me/messages/{draft_id}?$select=id,isDraft,subject,webLink,parentFolderId",
        headers=_graph_headers(),
        timeout=20,
    )
    chk.raise_for_status()
    meta = chk.json() or {}
    is_draft = bool(meta.get("isDraft"))
    if not is_draft:
        raise RuntimeError(f"Mensagem criada mas não está como rascunho (id={draft_id}).")

    return {
        "status": "ok",
        "modo": modo,
        "draft_id": draft_id,
        "is_draft": is_draft,
        "subject": meta.get("subject"),
        "web_link": meta.get("webLink"),
        "parent_folder_id": meta.get("parentFolderId"),
    }


def salvar_rascunho_outlook(dados_nc: dict[str, Any]) -> dict[str, Any]:
    """
    Cria rascunho de reply encadeado pelo código da constatação no assunto.
    Espera em dados_nc:
      - user_id (obrigatório)
      - codigo_constatacao ou id_nc (obrigatório)
      - rodovia, km, links_fotos (opcionais)
    """
    user_id = str(dados_nc.get("user_id") or "").strip().lower()
    codigo = str(dados_nc.get("codigo_constatacao") or dados_nc.get("id_nc") or "").strip()
    if not user_id:
        raise ValueError("dados_nc.user_id é obrigatório")
    if not codigo:
        raise ValueError("dados_nc.codigo_constatacao (ou id_nc) é obrigatório")
    cfg = OutlookOAuthConfig.from_env()
    payload = dict(dados_nc)
    payload["id_nc"] = codigo
    return gerar_rascunho_nc(
        user_id=user_id,
        oauth_config=cfg,
        dados_csv=payload,
        email_artesp=str(dados_nc.get("email_artesp") or DEFAULT_ARTESP_EMAIL),
    )


def outlook_esta_autenticado(user_id: str) -> bool:
    """
    Verifica se o usuário já possui token Outlook válido no backend de banco.
    """
    uid = (user_id or "").strip().lower()
    if not uid:
        return False
    cfg = OutlookOAuthConfig.from_env()
    store = OAuthDbStore()
    token_backend = DbTokenBackend(store, uid)
    account = _create_account(cfg, token_backend)
    return bool(account.is_authenticated)
