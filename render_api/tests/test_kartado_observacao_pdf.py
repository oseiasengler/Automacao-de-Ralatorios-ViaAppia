"""Regras de roteamento Observação PDF → colunas AA / X / Y Kartado."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_NC_ARTESP = _REPO / "nc_artesp"
if str(_NC_ARTESP) not in sys.path:
    sys.path.insert(0, str(_NC_ARTESP))

from utils.kartado_observacao_pdf import (  # noqa: E402
    normalizar_observacao_extraida_pdf,
    rotear_observacao_pdf_para_kartado,
    texto_observacoes_aa_para_excel,
)


def test_texto_livre_sem_lexico_vai_para_observacoes_aa():
    r = rotear_observacao_pdf_para_kartado(
        "Grande quantidade de galhos e massa seca rente a cerca., Drenagem fora de plataforma."
    )
    assert r.localizacao_pista_x == ""
    assert r.localizacao_tipo_y == ""
    assert "galhos" in r.texto_livre_observacoes.casefold()
    assert "drenagem" in r.texto_livre_observacoes.casefold()


def test_faixa_refugio_viaduto_distribui_x_y_e_livre():
    r = rotear_observacao_pdf_para_kartado(
        "Afundamento do passeio. Refúgio. Faixa 03. Viaduto com trinca."
    )
    assert "Refúgio" in r.localizacao_pista_x
    assert "Faixa 03" in r.localizacao_pista_x
    assert "Viaduto" in r.localizacao_tipo_y
    liv = r.texto_livre_observacoes.casefold()
    assert "afundamento" in liv and "trinca" in liv


def test_pista_principal_empate_favorece_coluna_y():
    r = rotear_observacao_pdf_para_kartado("Pista Principal")
    assert "Pista Principal" in r.localizacao_tipo_y
    assert r.localizacao_pista_x == ""


def test_fora_de_plataforma_em_contexto_drenagem_fica_texto_livre():
    r = rotear_observacao_pdf_para_kartado("Drenagem fora de plataforma")
    assert r.localizacao_pista_x == ""
    liv = r.texto_livre_observacoes.casefold()
    assert "drenagem" in liv and "fora de plataforma" in liv


def test_fora_de_plataforma_catalogo_quando_termo_isolado():
    r = rotear_observacao_pdf_para_kartado("Situação: Fora de Plataforma, erosão.")
    assert "Fora de Plataforma" in r.localizacao_pista_x
    liv_e = r.texto_livre_observacoes.casefold()
    assert "erosão" in liv_e or "erosao" in liv_e


def test_predio_patio_alias():
    r = rotear_observacao_pdf_para_kartado("Danos no Predio/Patio lateral")
    assert "Prédio/Pátio" in r.localizacao_pista_x
    liv = r.texto_livre_observacoes.casefold()
    assert "danos" in liv and "lateral" in liv


def test_aa_sem_só_delimitadores_apos_roteamento_xy():
    r = rotear_observacao_pdf_para_kartado("Viaduto Refúgio")
    assert r.texto_livre_observacoes == ""
    assert "Viaduto" in r.localizacao_tipo_y
    assert "Refúgio" in r.localizacao_pista_x


def test_texto_observacoes_aa_para_excel_rejeita_so_pontuacao():
    assert texto_observacoes_aa_para_excel(": | :") == ""
    assert texto_observacoes_aa_para_excel("  .  ") == ""


def test_normalizar_observacao():
    s = normalizar_observacao_extraida_pdf("  a\n\nb  \tc  ")
    assert s == "a b c"


def test_alca_desaceleracao_sem_acento_primeira_palavra_vai_y():
    r = rotear_observacao_pdf_para_kartado("Danos na Alca Desaceleracao.")
    assert "Alça Desaceleração" in r.localizacao_tipo_y
    assert "danos" in r.texto_livre_observacoes.casefold()


def test_alca_aceleracao_pdf_vai_y():
    r = rotear_observacao_pdf_para_kartado("Ponto na Alca Aceleracao.")
    assert "Alça Aceleração" in r.localizacao_tipo_y


def test_mureta_tampa_esgoto_bambu_sem_lexico_fica_aa():
    r = rotear_observacao_pdf_para_kartado(
        "Mureta danificada. próximo a tampa de esgoto. "
        "Bambu com projeção sobre a faixa de rolamento, apresentando risco de queda."
    )
    assert r.localizacao_pista_x == ""
    assert r.localizacao_tipo_y == ""
    liv = r.texto_livre_observacoes.casefold()
    assert "mureta" in liv and "esgoto" in liv and "bambu" in liv and "queda" in liv
