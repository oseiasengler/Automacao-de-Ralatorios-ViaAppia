"""
Router do PWA Inventário de Drenagem (integrado ao GeradorARTESP).
Rotas montadas sem prefixo para compatibilidade com o app.js existente.
"""
from __future__ import annotations

import json
import logging
import os
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, Session, create_engine, select

# Importações do núcleo do inventário (raiz do repositório = /app no container)
try:
    from models import Dispositivo, DispositivoSync, SyncRequest, SyncResponse, agora
    from catalogo_dispositivos import (
        catalogo_dict, ESTADOS_CONSERVACAO, valida_atributos, _POR_TIPO,
    )
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from models import Dispositivo, DispositivoSync, SyncRequest, SyncResponse, agora
    from catalogo_dispositivos import (
        catalogo_dict, ESTADOS_CONSERVACAO, valida_atributos, _POR_TIPO,
    )

# ── Banco de dados do inventário (independente do GeradorARTESP) ─────────────
_DB_URL = os.getenv(
    "INVENTARIO_DATABASE_URL",
    os.getenv("DATABASE_URL", "sqlite:///./coleta.db"),
)
_engine = create_engine(
    _DB_URL,
    connect_args={"check_same_thread": False} if _DB_URL.startswith("sqlite") else {},
)

FOTOS_DIR = Path(os.getenv("FOTOS_DIR", "/data/fotos_inventario"))


def setup_inventario() -> None:
    """Cria tabelas e garante existência de diretórios. Chamado no startup."""
    SQLModel.metadata.create_all(_engine)
    FOTOS_DIR.mkdir(parents=True, exist_ok=True)
    logging.info("Inventário: banco e diretório de fotos prontos.")


def _get_session():
    with Session(_engine) as s:
        yield s


def _utc(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)


# ── Router ────────────────────────────────────────────────────────────────────
router = APIRouter(tags=["Inventário de Drenagem"])


# Catálogo — o PWA puxa daqui para gerar formulários dinâmicos
@router.get("/catalogo")
def get_catalogo():
    return {"estados_conservacao": ESTADOS_CONSERVACAO, "dispositivos": catalogo_dict()}


# CRUD
def _valida(d):
    if d.tipo not in _POR_TIPO:
        raise HTTPException(422, f"tipo desconhecido: {d.tipo}")
    erros = valida_atributos(d.tipo, d.atributos or {})
    if erros:
        raise HTTPException(422, {"atributos": erros})


@router.get("/dispositivos", response_model=list[Dispositivo])
def listar(
    rodovia: Optional[str] = None,
    categoria: Optional[str] = None,
    incluir_apagados: bool = False,
    s: Session = Depends(_get_session),
):
    q = select(Dispositivo)
    if not incluir_apagados:
        q = q.where(Dispositivo.deleted == False)  # noqa: E712
    if rodovia:
        q = q.where(Dispositivo.rodovia == rodovia)
    if categoria:
        q = q.where(Dispositivo.categoria == categoria)
    return s.exec(q.order_by(Dispositivo.rodovia, Dispositivo.km_ini)).all()


@router.post("/dispositivos", response_model=Dispositivo)
def criar(d: DispositivoSync, s: Session = Depends(_get_session)):
    _valida(d)
    obj = Dispositivo(**d.model_dump())
    obj.updated_at = agora()
    s.add(obj)
    s.commit()
    s.refresh(obj)
    return obj


@router.get("/dispositivos/{id}", response_model=Dispositivo)
def obter(id: str, s: Session = Depends(_get_session)):
    obj = s.get(Dispositivo, id)
    if not obj:
        raise HTTPException(404, "não encontrado")
    return obj


# Sync offline-first (coração do PWA)
@router.post("/sync", response_model=SyncResponse)
def sync(req: SyncRequest, s: Session = Depends(_get_session)):
    aplicados = ignorados = 0
    chegada = agora()
    for r in req.registros:
        if r.tipo in _POR_TIPO:
            if valida_atributos(r.tipo, r.atributos or {}):
                ignorados += 1
                continue
        existente = s.get(Dispositivo, r.id)
        if existente is None:
            s.add(Dispositivo(**r.model_dump()))
            aplicados += 1
        else:
            if _utc(r.updated_at) > _utc(existente.updated_at):
                for k, v in r.model_dump().items():
                    setattr(existente, k, v)
                s.add(existente)
                aplicados += 1
            else:
                ignorados += 1
    s.commit()
    q = select(Dispositivo)
    if req.last_sync is not None:
        q = q.where(Dispositivo.updated_at > req.last_sync)
    return SyncResponse(
        server_time=chegada,
        aplicados=aplicados,
        ignorados=ignorados,
        registros=s.exec(q).all(),
    )


# Export GeoJSON
@router.get("/export/geojson")
def export_geojson(rodovia: Optional[str] = None, s: Session = Depends(_get_session)):
    q = select(Dispositivo).where(Dispositivo.deleted == False)  # noqa: E712
    if rodovia:
        q = q.where(Dispositivo.rodovia == rodovia)
    feats = []
    for d in s.exec(q).all():
        if d.lat_fim is not None and d.lon_fim is not None:
            geom = {"type": "LineString", "coordinates": [[d.lon_ini, d.lat_ini], [d.lon_fim, d.lat_fim]]}
        elif d.lat_ini is not None:
            geom = {"type": "Point", "coordinates": [d.lon_ini, d.lat_ini]}
        else:
            geom = None
        feats.append({
            "type": "Feature", "geometry": geom,
            "properties": {
                "id": d.id, "rodovia": d.rodovia, "km_ini": d.km_ini, "km_fim": d.km_fim,
                "sentido": d.sentido, "lado": d.lado, "categoria": d.categoria,
                "tipo": d.tipo, "estado": d.estado_conservacao,
                "extensao_m": d.extensao_m, **(d.atributos or {}),
            },
        })
    return JSONResponse({"type": "FeatureCollection", "features": feats})


# Sincronização com foto (multipart)
@router.post("/api/inventario/sincronizar")
async def sincronizar_inventario(
    metadados: str = Form(..., description="JSON completo do registro do dispositivo"),
    foto: Optional[UploadFile] = File(None),
):
    try:
        meta: dict = json.loads(metadados)
    except json.JSONDecodeError as exc:
        raise HTTPException(422, f"'metadados' não é JSON válido: {exc}")

    dispositivo_id: str = meta.get("id") or str(uuid.uuid4())
    foto_salva: Optional[str] = None

    if foto and foto.filename:
        ext = Path(foto.filename).suffix.lower() or ".jpg"
        nome = f"{dispositivo_id}_{uuid.uuid4().hex[:8]}{ext}"
        pasta = FOTOS_DIR / dispositivo_id
        pasta.mkdir(parents=True, exist_ok=True)
        caminho = pasta / nome
        with caminho.open("wb") as f:
            shutil.copyfileobj(foto.file, f)
        foto_salva = str(caminho)

    return {
        "ok": True,
        "dispositivo_id": dispositivo_id,
        "foto_salva": foto_salva,
        "campos_recebidos": list(meta.keys()),
    }
