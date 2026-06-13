"""Regression: «Classe» Kartado apenas com valores canónicos; cruzamento M/N/O."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_NC_ARTESP = _REPO / "nc_artesp"
if str(_NC_ARTESP) not in sys.path:
    sys.path.insert(0, str(_NC_ARTESP))

from modulos.separar_nc import (  # noqa: E402
    _CLASSES_KARTADO_PERMITIDAS,
    _partir_celula_grupo_atividade_mae_combinada,
    _resolver_classe_kartado_inteligente_mno,
)


def test_resolver_classe_via_texto_col_n_art03():
    r = _resolver_classe_kartado_inteligente_mno(
        texto_m="",
        texto_n="Pichações e vandalismo",
        texto_o="",
        tipo_txt_detetado="",
    )
    assert r == "FD - Pichação"
    assert r in _CLASSES_KARTADO_PERMITIDAS


def test_resolver_classe_via_tipo_txt_detetado():
    r = _resolver_classe_kartado_inteligente_mno(
        texto_m="",
        texto_n="",
        texto_o="",
        tipo_txt_detetado="Remoção de lixo e entulho da faixa de domínio",
    )
    assert r == "FD - Lixo/Entulho"


def test_resolver_classe_composto_m_n():
    r = _resolver_classe_kartado_inteligente_mno(
        texto_m="x",
        texto_n="Despraguejamento",
        texto_o="",
        tipo_txt_detetado="",
    )
    assert r == "FD - Controle Fitossanitário"


def test_resolver_classe_apenas_kartado_canonico():
    r = _resolver_classe_kartado_inteligente_mno(
        texto_m="",
        texto_n="",
        texto_o="FD - Call Box - Limpeza Totem",
        tipo_txt_detetado="",
    )
    assert r == "FD - Call Box - Limpeza Totem"


def test_resolver_sem_match_usa_fallback_permitido():
    r = _resolver_classe_kartado_inteligente_mno(
        texto_m="@@@",
        texto_n="###",
        texto_o="$$$",
        tipo_txt_detetado="%%%",
    )
    assert r in _CLASSES_KARTADO_PERMITIDAS
    assert r.startswith("FD -")


def test_partir_celula_grupo_atividade_mae_combinada():
    texto = "Grupo de atividade; Prédios e Pátios - Atividade - Cobertura / Forro"
    g, a = _partir_celula_grupo_atividade_mae_combinada(texto)
    assert g == "Prédios e Pátios"
    assert a == "Cobertura / Forro"


def test_resolver_grupo_atividade_predios_cobertura_nao_eh_lixo_entulho():
    texto = "Grupo de atividade; Prédios e Pátios - Atividade - Cobertura / Forro"
    g, a = _partir_celula_grupo_atividade_mae_combinada(texto)
    r = _resolver_classe_kartado_inteligente_mno(
        texto_m=g,
        texto_n=a,
        texto_o="",
        tipo_txt_detetado="",
    )
    assert r in ("FD - Prédio e Pátio", "FD - Predio e Patio")
    assert "Lixo" not in r and "Entulho" not in r


def test_resolver_alias_fd_call_box_totem():
    r = _resolver_classe_kartado_inteligente_mno(
        texto_m="",
        texto_n="Call Box - Limpeza Totem",
        texto_o="",
        tipo_txt_detetado="",
    )
    assert r == "FD - Call Box - Limpeza Totem"
    r = _resolver_classe_kartado_inteligente_mno(
        texto_m="",
        texto_n="Predio e Patio",
        texto_o="",
        tipo_txt_detetado="",
    )
    assert r == "FD - Predio e Patio"


def test_resolver_regra_artesp_apontamento_sem_prefixo_fd():
    r = _resolver_classe_kartado_inteligente_mno(
        texto_m="",
        texto_n="Call Box Outros",
        texto_o="",
        tipo_txt_detetado="",
    )
    assert r == "FD - Call Box - Outros"


def test_resolver_prefixo_catalogo_utilidades_limpeza_para_parada_onibus():
    r = _resolver_classe_kartado_inteligente_mno(
        texto_m="",
        texto_n="XX - b.9.1 - Utilidades Publicas - Limpeza",
        texto_o="",
        tipo_txt_detetado="",
    )
    assert r == "FD - Parada onibus - Limpeza/Pintura"


def test_resolver_prefixo_catalogo_parada_onibus_limpeza():
    r = _resolver_classe_kartado_inteligente_mno(
        texto_m="",
        texto_n="XX - b.7.1 - Parada de Onibus - Limpeza",
        texto_o="",
        tipo_txt_detetado="",
    )
    assert r == "FD - Parada onibus - Limpeza/Pintura"


def test_resolver_ponto_onibus_com_macro_composta_em_m_prioriza_n():
    """M com grupo macro composto não deve ganhar ao «Ponto de onibus» em N (fuzzy monumentos/utilidades)."""
    r = _resolver_classe_kartado_inteligente_mno(
        texto_m="Paradas de ônibus, monumentos e utilidades publicas",
        texto_n="Ponto de onibus",
        texto_o="",
        tipo_txt_detetado="",
    )
    assert r == "FD - Parada ônibus - Reparo"


def test_resolver_alias_macro_paradas_onibus_monumentos_utilidades():
    r = _resolver_classe_kartado_inteligente_mno(
        texto_m="Paradas de ônibus, monumentos e utilidades publicas",
        texto_n="",
        texto_o="",
        tipo_txt_detetado="",
    )
    assert r == "FD - Parada ônibus - Reparo"
