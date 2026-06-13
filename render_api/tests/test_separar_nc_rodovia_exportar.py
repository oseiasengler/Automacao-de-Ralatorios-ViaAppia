"""Rodovia no Exportar/Kartado: alias SPI unificado."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_NC_ARTESP = _REPO / "nc_artesp"
if str(_NC_ARTESP) not in sys.path:
    sys.path.insert(0, str(_NC_ARTESP))

from modulos.separar_nc import _rodovia_fmt_eaf_para_kartado  # noqa: E402


def test_spi_aliases_mesmo_texto_rodovia():
    a = _rodovia_fmt_eaf_para_kartado("SPI")
    b = _rodovia_fmt_eaf_para_kartado("SPI 102/300")
    c = _rodovia_fmt_eaf_para_kartado("SPI102/300")
    assert a == b == c
    assert "SPI" in a


def test_spi_formato_exibicao_kartado():
    """SPI 102-300 e variantes devem exibir como SPI-102/300 no relatório Kartado."""
    for entrada in ("SPI 102-300", "SPI 102/300", "SPI102/300", "SPI"):
        resultado = _rodovia_fmt_eaf_para_kartado(entrada)
        assert resultado == "SPI-102/300", f"Entrada {entrada!r} → {resultado!r}"
