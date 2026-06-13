"""
API de inventário de drenagem — FastAPI + SQLModel.

Rodar local:
    pip install fastapi "uvicorn[standard]" sqlmodel
    uvicorn main:app --reload

Trocar pra Postgres: basta mudar DATABASE_URL.
"""
from __future__ import annotations
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from pathlib import Path
import json
import os
import shutil
import uuid

from fastapi import FastAPI, File, Form, HTTPException, Depends, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, Session, create_engine, select

from models import Dispositivo, DispositivoSync, SyncRequest, SyncResponse, agora

FOTOS_DIR = Path(os.getenv("FOTOS_DIR", "/data/fotos_inventario"))


def _utc(dt: datetime) -> datetime:
    """SQLite descarta tzinfo; tratamos datetime naive como UTC."""
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
from catalogo_dispositivos import (
    catalogo_dict, ESTADOS_CONSERVACAO, valida_atributos, _POR_TIPO,
)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./coleta.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}
                       if DATABASE_URL.startswith("sqlite") else {})


def get_session():
    with Session(engine) as s:
        yield s


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    FOTOS_DIR.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(title="Inventário de Drenagem", version="0.1", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# CATÁLOGO  (o PWA pode puxar daqui pra atualizar tipos sem novo deploy)
# ---------------------------------------------------------------------------
@app.get("/catalogo")
def get_catalogo():
    return {"estados_conservacao": ESTADOS_CONSERVACAO, "dispositivos": catalogo_dict()}


# ---------------------------------------------------------------------------
# CRUD  (uso de escritório / web online)
# ---------------------------------------------------------------------------
def _valida(d: DispositivoSync | Dispositivo):
    if d.tipo not in _POR_TIPO:
        raise HTTPException(422, f"tipo desconhecido: {d.tipo}")
    erros = valida_atributos(d.tipo, d.atributos or {})
    if erros:
        raise HTTPException(422, {"atributos": erros})


@app.get("/dispositivos", response_model=list[Dispositivo])
def listar(
    rodovia: str | None = None,
    categoria: str | None = None,
    incluir_apagados: bool = False,
    s: Session = Depends(get_session),
):
    q = select(Dispositivo)
    if not incluir_apagados:
        q = q.where(Dispositivo.deleted == False)  # noqa: E712
    if rodovia:
        q = q.where(Dispositivo.rodovia == rodovia)
    if categoria:
        q = q.where(Dispositivo.categoria == categoria)
    return s.exec(q.order_by(Dispositivo.rodovia, Dispositivo.km_ini)).all()


@app.post("/dispositivos", response_model=Dispositivo)
def criar(d: DispositivoSync, s: Session = Depends(get_session)):
    _valida(d)
    obj = Dispositivo(**d.model_dump())
    obj.updated_at = agora()
    s.add(obj)
    s.commit()
    s.refresh(obj)
    return obj


@app.get("/dispositivos/{id}", response_model=Dispositivo)
def obter(id: str, s: Session = Depends(get_session)):
    obj = s.get(Dispositivo, id)
    if not obj:
        raise HTTPException(404, "não encontrado")
    return obj


# ---------------------------------------------------------------------------
# SYNC  (coração do offline-first)
# ---------------------------------------------------------------------------
@app.post("/sync", response_model=SyncResponse)
def sync(req: SyncRequest, s: Session = Depends(get_session)):
    """
    1) PUSH: grava registros do cliente. Resolve conflito por updated_at
       (last-write-wins) — só sobrescreve se o do cliente for mais novo.
    2) PULL: devolve tudo que mudou no servidor desde last_sync.
    """
    aplicados = ignorados = 0
    chegada = agora()

    for r in req.registros:
        if r.tipo in _POR_TIPO:
            erros = valida_atributos(r.tipo, r.atributos or {})
            if erros:
                ignorados += 1
                continue
        existente = s.get(Dispositivo, r.id)
        if existente is None:
            obj = Dispositivo(**r.model_dump())
            s.add(obj)
            aplicados += 1
        else:
            # last-write-wins: cliente só vence se for estritamente mais novo
            if _utc(r.updated_at) > _utc(existente.updated_at):
                for k, v in r.model_dump().items():
                    setattr(existente, k, v)
                s.add(existente)
                aplicados += 1
            else:
                ignorados += 1
    s.commit()

    # PULL — devolve mudanças do servidor (inclui o que outros aparelhos enviaram)
    q = select(Dispositivo)
    if req.last_sync is not None:
        q = q.where(Dispositivo.updated_at > req.last_sync)
    mudancas = s.exec(q).all()

    return SyncResponse(
        server_time=chegada,
        aplicados=aplicados,
        ignorados=ignorados,
        registros=mudancas,
    )


# ---------------------------------------------------------------------------
# EXPORT GeoJSON  (integra com seu tooling ARTESP/KMZ)
# ---------------------------------------------------------------------------
@app.get("/export/geojson")
def export_geojson(rodovia: str | None = None, s: Session = Depends(get_session)):
    q = select(Dispositivo).where(Dispositivo.deleted == False)  # noqa: E712
    if rodovia:
        q = q.where(Dispositivo.rodovia == rodovia)
    feats = []
    for d in s.exec(q).all():
        # LineString se tiver entrada e saída; senão Point
        if d.lat_fim is not None and d.lon_fim is not None:
            geom = {"type": "LineString",
                    "coordinates": [[d.lon_ini, d.lat_ini], [d.lon_fim, d.lat_fim]]}
        elif d.lat_ini is not None:
            geom = {"type": "Point", "coordinates": [d.lon_ini, d.lat_ini]}
        else:
            geom = None
        feats.append({
            "type": "Feature",
            "geometry": geom,
            "properties": {
                "id": d.id, "rodovia": d.rodovia, "km_ini": d.km_ini, "km_fim": d.km_fim,
                "sentido": d.sentido, "lado": d.lado, "categoria": d.categoria,
                "tipo": d.tipo, "estado": d.estado_conservacao,
                "extensao_m": d.extensao_m, **(d.atributos or {}),
            },
        })
    return JSONResponse({"type": "FeatureCollection", "features": feats})


# ---------------------------------------------------------------------------
# SINCRONIZAÇÃO DE CAMPO  (multipart: metadados JSON + foto binária)
# ---------------------------------------------------------------------------
@app.post("/api/inventario/sincronizar")
async def sincronizar_inventario(
    metadados: str = Form(..., description="JSON completo do registro do dispositivo"),
    foto: UploadFile | None = File(None),
):
    """
    Recebe o registro de um dispositivo (JSON no campo 'metadados') e,
    opcionalmente, um arquivo de foto. Salva a foto em /data/fotos_inventario/
    e retorna a confirmação com o caminho gravado.
    """
    try:
        meta: dict = json.loads(metadados)
    except json.JSONDecodeError as exc:
        raise HTTPException(422, f"'metadados' não é JSON válido: {exc}")

    dispositivo_id: str = meta.get("id") or str(uuid.uuid4())
    foto_salva: str | None = None

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


@app.get("/health")
def health():
    return {"ok": True, "time": agora().isoformat()}


# ---------------------------------------------------------------------------
# ARQUIVOS ESTÁTICOS — montado por último para não interceptar rotas de API
# html=True → serve index.html para qualquer path desconhecido (SPA fallback)
# ---------------------------------------------------------------------------
app.mount("/inventario", StaticFiles(directory="frontend_inventario", html=True), name="inventario")
