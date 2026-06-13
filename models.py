"""
Modelos de dados — núcleo comum + atributos específicos (JSON).

Campos de sincronização (offline-first):
  - id: UUID gerado no CLIENTE (permite criar offline sem colisão)
  - updated_at: timestamp UTC — resolve conflito por last-write-wins
  - deleted: soft-delete (registro apagado offline precisa propagar no sync)
"""
from __future__ import annotations
from datetime import datetime, date, timezone
from typing import Optional, Any
from sqlmodel import SQLModel, Field, Column, JSON
import uuid


def agora() -> datetime:
    return datetime.now(timezone.utc)


class DispositivoBase(SQLModel):
    # ---- localização ----
    rodovia: str = Field(index=True)              # ex.: SP-280
    km_ini: float = Field(index=True)
    km_fim: Optional[float] = None                # None = dispositivo pontual
    sentido: str = "Norte"                          # Norte|Sul|Leste|Oeste|Interna|Externa
    lado: str = "Lado Direito"                      # Lado Direito|Lado Esquerdo|Canteiro Lateral|Canteiro Central|Dispositivo|Alça
    estaca: Optional[str] = None                   # km/estaca manual (ex.: "1250+10")
    lat_ini: Optional[float] = None
    lon_ini: Optional[float] = None
    lat_fim: Optional[float] = None
    lon_fim: Optional[float] = None
    precisao_gps_m: Optional[float] = None         # acurácia reportada pelo GPS

    # ---- classificação ----
    categoria: str = Field(index=True)             # superficial|profunda|transversal
    tipo: str = Field(index=True)                  # chave do catálogo
    extensao_m: Optional[float] = None

    # ---- atributos específicos do tipo (validados pelo catálogo) ----
    atributos: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    # ---- coleta ----
    direcao_coleta: str = "Direta"                 # Direta|Reversa (canaletas coletadas contra o fluxo)

    # ---- rede hidráulica ----
    id_rede: Optional[str] = None                  # código da travessia (ex: TR-KM024-01)
    conectado_a: Optional[str] = None              # UUID do dispositivo a montante

    # ---- inspeção ----
    estado_conservacao: Optional[str] = None       # bom|regular|ruim|critico
    data_inspecao: Optional[date] = None
    inspetor: Optional[str] = None
    observacoes: Optional[str] = None
    fotos: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    ncs: list[str] = Field(default_factory=list, sa_column=Column(JSON))


class Dispositivo(DispositivoBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    updated_at: datetime = Field(default_factory=agora, index=True)
    deleted: bool = Field(default=False, index=True)


class DispositivoSync(DispositivoBase):
    """Payload de entrada do cliente — traz o id e updated_at gerados offline."""
    id: str
    updated_at: datetime
    deleted: bool = False


class SyncRequest(SQLModel):
    last_sync: Optional[datetime] = None           # None = primeira sincronização
    registros: list[DispositivoSync] = []


class SyncResponse(SQLModel):
    server_time: datetime
    aplicados: int                                 # quantos do cliente foram gravados
    ignorados: int                                 # perderam no last-write-wins
    registros: list[Dispositivo]                   # mudanças do servidor desde last_sync
