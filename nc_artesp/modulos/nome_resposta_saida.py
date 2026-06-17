"""Pendentes: stem ``prazo - código - data const. - só Atividade da mãe`` (sem coluna «Tipo de Atividade» / O no nome)."""

import re
from datetime import date, datetime, timedelta

from config import ART03_ATIVIDADE_PARA_SERVICO_KARTADO, PRAZO_DIAS_APOS_ENVIO, SERVICO_NC
from utils.helpers import parse_data

_CHARS_INV_FICHEIRO = re.compile(r'[\\/:*?"<>|\x00-\x1f]')
STEM_RELATORIO_PENDENTES_MAX = 110
_UNICODE_SPACE_PARA_NORMAL = (
    "\u00a0",  # NBSP (Excel)
    "\u202f",  # narrow no-break space
    "\u2007",  # figure space
    "\u2009",  # thin space
    "\u200a",  # hair space
    "\u3000",  # ideographic space
)


def _normalizar_separadores_classe_kartado(s: str) -> str:
    t = (s or "").strip()
    for ch in _UNICODE_SPACE_PARA_NORMAL:
        t = t.replace(ch, " ")
    t = re.sub(r"[\u2010\u2011\u2012\u2013\u2014\u2212]", "-", t)
    t = re.sub(r" +", " ", t).strip()
    return t


def _prefixos_primerio_segmento_classe_kartado() -> frozenset[str]:
    out: set[str] = set()
    for v in ART03_ATIVIDADE_PARA_SERVICO_KARTADO.values():
        if not isinstance(v, str):
            continue
        nv = _normalizar_separadores_classe_kartado(v)
        if "-" not in nv:
            continue
        pre, _, resto = nv.partition(" - ")
        if not resto:
            continue
        pre = pre.strip()
        if not pre:
            continue
        cf = pre.casefold()
        out.add(cf)
        if len(pre) > 1 and pre.endswith("."):
            out.add(pre[:-1].strip().casefold())
    return frozenset(out)


_PREFIXOS_CLASSE_KARTADO_STEM = _prefixos_primerio_segmento_classe_kartado()


def _sem_prefixo_classe_kartado_nome_pendentes(s: str) -> str:
    """Valores ART03 usam «Sigla - …» (ex.: FD, VD, Pav., Dren.); no stem Pendentes fica o restante após o primeiro hífen."""
    t0 = (s or "").strip()
    if not t0:
        return t0
    t = _normalizar_separadores_classe_kartado(t0)
    if "-" not in t:
        return t0
    parts = re.split(r"\s*-\s*", t, maxsplit=1)
    if len(parts) < 2:
        return t0
    pre, rest = parts[0].strip(), parts[1].strip()
    chave = pre.casefold()
    if chave and chave in _PREFIXOS_CLASSE_KARTADO_STEM:
        u = rest.strip()
        return u if u else t0
    return t0


def _sanitizar_stem_pendentes(s: str, max_len: int = 200) -> str:
    s = _CHARS_INV_FICHEIRO.sub(" ", (s or "").strip())
    s = s.replace("_", " ")
    s = re.sub(r" +", " ", s)
    s = s[:max_len].strip()
    return s if s else "Resposta NC"


def _texto_atividade_stem_valido(s: str) -> bool:
    t = (s or "").strip()
    if len(t) < 5:
        return False
    tl = t.casefold()
    if tl in (
        "artesp",
        "kartado",
        "origem",
        "soluciona",
        "pendente",
        "sim",
        "nao",
        "não",
        "s/n",
    ):
        return False
    return True


def _texto_atividade_exibicao_pendentes(nc: dict) -> str:
    """Texto de atividade para células/linhas (Excel resposta, Kria, relatório): não aplica o filtro curto do stem sobre ``atividade``/``mae_atividade_q``."""
    for chave in ("atividade", "mae_atividade_q"):
        ativ = str(nc.get(chave) or "").strip()
        if ativ:
            raw = _sem_prefixo_classe_kartado_nome_pendentes(ativ)
            out = _sanitizar_stem_pendentes(raw, 200)
            if out and out != "Resposta NC":
                return out
            if (raw or "").strip():
                return (raw or "")[:200]
            return ativ[:200]
    return _segmento_atividade_nome_pendentes(nc)


def _segmento_atividade_nome_pendentes(nc: dict) -> str:
    """Mesma linha de texto que o .eml (``atividade``), depois ``mae_atividade_q`` / ``tipo_nc``; remove prefixos de classe Kartado só quando reconhecidos."""
    for chave in ("atividade", "mae_atividade_q"):
        ativ = str(nc.get(chave) or "").strip()
        if ativ and _texto_atividade_stem_valido(ativ):
            raw = _sem_prefixo_classe_kartado_nome_pendentes(ativ)
            return _sanitizar_stem_pendentes(raw, 200) or "Conservação Rotina"
    tipo_raw = str(nc.get("tipo_nc") or "").strip()
    if tipo_raw and _texto_atividade_stem_valido(tipo_raw):
        raw = _sem_prefixo_classe_kartado_nome_pendentes(tipo_raw)
        return _sanitizar_stem_pendentes(raw, 200) or "Conservação Rotina"
    if tipo_raw in SERVICO_NC:
        t = SERVICO_NC[tipo_raw]
        if isinstance(t, tuple) and len(t) >= 2 and str(t[1]).strip():
            cat = _sem_prefixo_classe_kartado_nome_pendentes(str(t[1]).strip())
        else:
            cat = "Conservação Rotina"
    else:
        cat = "Conservação Rotina"
    if not cat:
        cat = "Conservação Rotina"
    return _sanitizar_stem_pendentes(cat, 80) or "Conservação Rotina"


def _data_prazo_para_nome(nc: dict) -> datetime | None:
    dr = nc.get("data_reparo")
    dc = nc.get("data_con")
    dt_p = parse_data(dr) if dr is not None else None
    if dt_p is None and dc is not None:
        dt_c = parse_data(dc)
        if dt_c:
            dt_p = dt_c + timedelta(days=PRAZO_DIAS_APOS_ENVIO)
    if dt_p is None:
        return None
    if isinstance(dt_p, date) and not isinstance(dt_p, datetime):
        return datetime(dt_p.year, dt_p.month, dt_p.day)
    return dt_p.replace(microsecond=0)


def _stem_relatorio_pendentes(nc: dict) -> str:
    dt_p = _data_prazo_para_nome(nc)
    prazo_yyyymmdd = dt_p.strftime("%Y%m%d") if dt_p else "00000000"

    cod = str(nc.get("codigo") or "").strip() or "sem_codigo"

    dc = nc.get("data_con")
    dt_c = parse_data(dc) if dc is not None else None
    if dt_c is None:
        const_str = "00-00-0000"
    else:
        if isinstance(dt_c, date) and not isinstance(dt_c, datetime):
            const_str = dt_c.strftime("%d-%m-%Y")
        else:
            const_str = dt_c.strftime("%d-%m-%Y")

    seg_ativ = _segmento_atividade_nome_pendentes(nc)

    rod = (
        str(nc.get("rod_tag") or "").strip()
        or re.sub(r"\s+", "", str(nc.get("rod_raw") or "").strip())
        or str(nc.get("rodovia") or "").strip()
    )
    parts = [prazo_yyyymmdd, cod]
    if rod:
        parts.append(rod)
    parts += [const_str, seg_ativ]
    raw = " - ".join(parts)
    return _sanitizar_stem_pendentes(raw, STEM_RELATORIO_PENDENTES_MAX)


def linha_assunto_resposta_artesp_para_nc(nc: dict, titulo_relatorio: str = "") -> str:
    return _stem_relatorio_pendentes(nc)


def nome_ficheiro_resposta_artesp_xlsx(nc: dict, titulo_relatorio: str = "") -> str:
    stem = _stem_relatorio_pendentes(nc)
    if not stem.lower().endswith(".xlsx"):
        stem = f"{stem}.xlsx"
    return stem
