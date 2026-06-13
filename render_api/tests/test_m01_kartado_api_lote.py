"""Gates M01 Kartado na API ARTESP (lotes 13/21/26)."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from render_api.nc_router import (  # noqa: E402
    _lote_num_texto,
    _m01_kartado_ativo_para_lote,
)


def test_lote_num_detecta_artesp_em_rotulos():
    assert _lote_num_texto("Lote 21 — Rodovias do Tietê") == "21"
    assert _lote_num_texto("ARTESP 13") == "13"
    assert _lote_num_texto("26") == "26"


def test_lote_num_fallback_primeiro_grupo_digitos():
    assert _lote_num_texto("Lote 50 — MG") == "50"


def test_m01_kartado_false_sem_flag():
    assert _m01_kartado_ativo_para_lote(False, "21") is False


def test_m01_kartado_lote_50_nunca():
    assert _m01_kartado_ativo_para_lote(True, "50") is False


def test_m01_kartado_lotes_artesp():
    assert _m01_kartado_ativo_para_lote(True, "13") is True
    assert _m01_kartado_ativo_para_lote(True, "21") is True
    assert _m01_kartado_ativo_para_lote(True, "Lote 26") is True


def test_m01_kartado_lote_fora_artesp():
    assert _m01_kartado_ativo_para_lote(True, "99") is False


def test_m01_kartado_fallback_m01_lote_env(monkeypatch):
    import nc_artesp.config as cfg

    monkeypatch.setattr(cfg, "M01_LOTE", "Lote 13", raising=False)
    assert _m01_kartado_ativo_para_lote(True, "") is True
