"""Nome ficheiro Exportar: mapeamento coluna Q → abreviatura Art_011 (VBA)."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_NC_ARTESP = _REPO / "nc_artesp"
if str(_NC_ARTESP) not in sys.path:
    sys.path.insert(0, str(_NC_ARTESP))

from config import m01_servico_abrev_art011_lookup  # noqa: E402


def test_lookup_strings_macro_vba():
    assert m01_servico_abrev_art011_lookup("Pichações e vandalismo") == "PICHAÇÃO"
    assert m01_servico_abrev_art011_lookup("Pichação ao longo da rodovia") == "PICHAÇÃO"
    assert (
        m01_servico_abrev_art011_lookup("Remoção de lixo e entulho da faixa de domínio")
        == "REMOÇÃO LIXO_ENTULHO"
    )
    assert m01_servico_abrev_art011_lookup("Panela ou buraco na faixa rolamento") == "PANELA"
    assert m01_servico_abrev_art011_lookup("Louças/ Metais") == "PREDIO - LOUÇAS_METAIS"


def test_lookup_normaliza_espacos_extras():
    assert (
        m01_servico_abrev_art011_lookup("Drenagem  fora de   plataforma limpeza geral")
        == "LIMP DRENAGEM FORA PLAT"
    )


def test_lookup_desconhecido_devolve_none():
    assert m01_servico_abrev_art011_lookup("Serviço inventado XYZ 123") is None
    assert m01_servico_abrev_art011_lookup("") is None
