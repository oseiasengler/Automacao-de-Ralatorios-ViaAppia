"""Cabeçalho coluna AA «Observações» (Kartado) — separado de ObsGestor."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_NC_ARTESP = _REPO / "nc_artesp"
if str(_NC_ARTESP) not in sys.path:
    sys.path.insert(0, str(_NC_ARTESP))

from modulos.separar_nc import (  # noqa: E402
    _KARTADO_CANON_OBSERVACOES_K,
    _kartado_cols_tpl_unificar_cabecalho_observacoes,
    _kartado_hdr_tem_coluna_observacoes,
    _kartado_primeira_coluna_observacoes_por_hdr,
    _norm_header,
)


def test_primeira_col_observacoes_sinonimo_observacao_singular():
    hdr = {_norm_header("Observação"): 12}
    assert _kartado_primeira_coluna_observacoes_por_hdr(hdr) == 12
    assert _kartado_hdr_tem_coluna_observacoes(hdr)


def test_obsgestor_nao_e_coluna_aa_observacoes():
    hdr = {_norm_header("ObsGestor"): 5, _norm_header("Obs gestor"): 6}
    assert _kartado_primeira_coluna_observacoes_por_hdr(hdr) is None
    assert not _kartado_hdr_tem_coluna_observacoes(hdr)


def test_com_observacoes_e_obsgestor_so_pega_observacoes():
    hdr = {_norm_header("ObsGestor"): 5, _norm_header("Observações"): 27}
    assert _kartado_primeira_coluna_observacoes_por_hdr(hdr) == 27


def test_unificar_cols_tpl_observacoes_nao_remove_obsgestor():
    hdr = {_norm_header("ObsGestor"): 9, _norm_header("Observações"): 11, "rodovia": 3}
    _kartado_cols_tpl_unificar_cabecalho_observacoes(hdr)
    assert hdr.get(_norm_header("ObsGestor")) == 9
    assert hdr[_KARTADO_CANON_OBSERVACOES_K] == 11
    assert hdr["rodovia"] == 3
