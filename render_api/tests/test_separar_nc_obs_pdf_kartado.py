"""Mapa código ↔ observação do PDF para coluna «Descrição» (W) Kartado."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

_REPO = Path(__file__).resolve().parents[2]
_NC_ARTESP = _REPO / "nc_artesp"
if str(_NC_ARTESP) not in sys.path:
    sys.path.insert(0, str(_NC_ARTESP))

from modulos.separar_nc import (  # noqa: E402
    _mapa_observacoes_desde_ncs_pdf,
    _observacao_pdf_para_codigo_mae,
)


def test_mapa_obs_pdf_varias_chaves_por_codigo():
    ncs = [
        SimpleNamespace(codigo="31-9999", observacao="  Texto obs  "),
        SimpleNamespace(codigo="8888", observacao="Só dígitos"),
    ]
    m = _mapa_observacoes_desde_ncs_pdf(ncs)
    assert m.get("31-9999") == "Texto obs"
    assert m.get("9999") == "Texto obs"
    assert m.get("8888") == "Só dígitos"


def test_lookup_obs_pdf_codigo_mae_com_prefixo():
    m = _mapa_observacoes_desde_ncs_pdf(
        [SimpleNamespace(codigo="6033", observacao="Obs do PDF")]
    )
    assert _observacao_pdf_para_codigo_mae(m, "26-6033") == "Obs do PDF"
    assert _observacao_pdf_para_codigo_mae(m, "6033") == "Obs do PDF"
    assert _observacao_pdf_para_codigo_mae(m, "9999") == ""


def test_sem_observacao_nao_entra_no_mapa():
    m = _mapa_observacoes_desde_ncs_pdf(
        [
            SimpleNamespace(codigo="1", observacao=""),
            SimpleNamespace(codigo="", observacao="x"),
        ]
    )
    assert m == {}


def test_lookup_obs_pdf_codigo_excel_como_numero_float():
    m = _mapa_observacoes_desde_ncs_pdf(
        [SimpleNamespace(codigo="6033", observacao="Obs do PDF")]
    )
    assert _observacao_pdf_para_codigo_mae(m, "6033.0") == "Obs do PDF"
    assert _observacao_pdf_para_codigo_mae(m, 6033.0) == "Obs do PDF"
