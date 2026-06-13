"""Nome ficheiro Pendentes: sem prefixo de classe Kartado («FD -», «VD -», «Pav. -», …) no stem."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_NC_ARTESP = _REPO / "nc_artesp"
if str(_NC_ARTESP) not in sys.path:
    sys.path.insert(0, str(_NC_ARTESP))

from modulos.nome_resposta_saida import (  # noqa: E402
    _segmento_atividade_nome_pendentes,
    _texto_atividade_exibicao_pendentes,
    nome_ficheiro_resposta_artesp_xlsx,
)


def test_segmento_mae_atividade_sem_fd():
    nc = {
        "mae_atividade_q": "FD - Prédio e Pátio",
        "tipo_nc": "qualquer",
        "codigo": "924902",
        "data_con": date(2026, 5, 13),
        "data_reparo": date(2026, 5, 13),
    }
    assert _segmento_atividade_nome_pendentes(nc) == "Prédio e Pátio"


def test_segmento_pav_limpeza_com_nbsp():
    nc = {
        "mae_atividade_q": "Pav.\u00a0-\u00a0Limpeza",
        "tipo_nc": "x",
        "codigo": "924873",
        "data_con": date(2026, 5, 13),
        "data_reparo": date(2026, 5, 20),
    }
    assert _segmento_atividade_nome_pendentes(nc) == "Limpeza"


def test_segmento_vd_com_nbsp_entre_partes():
    nc = {
        "mae_atividade_q": "VD\u00a0-\u00a0Vegetação\u00a0-\u00a0Remoção de Massa Seca",
        "tipo_nc": "x",
        "codigo": "924908",
        "data_con": date(2026, 5, 13),
        "data_reparo": date(2026, 5, 20),
    }
    seg = _segmento_atividade_nome_pendentes(nc)
    assert not seg.startswith("VD")
    assert "Massa" in seg or "massa" in seg.casefold()


def test_segmento_pav_limpeza_sem_sigla():
    nc = {
        "mae_atividade_q": "Pav. - Limpeza",
        "tipo_nc": "x",
        "codigo": "924873",
        "data_con": date(2026, 5, 13),
        "data_reparo": date(2026, 5, 20),
    }
    assert _segmento_atividade_nome_pendentes(nc) == "Limpeza"


def test_segmento_vd_arvores_via_art03():
    nc = {
        "mae_atividade_q": "",
        "tipo_nc": "Remoção de árvores ou galhos que não tem risco",
        "codigo": "924874",
        "data_con": date(2026, 5, 13),
        "data_reparo": date(2026, 5, 20),
    }
    seg = _segmento_atividade_nome_pendentes(nc)
    assert not seg.startswith("VD")
    assert "Galhos" in seg or "galhos" in seg.casefold()


def test_segmento_dc_defensa_varios_hifens():
    nc = {
        "mae_atividade_q": "DC - Defensa Metálica/Terminais - Danificada",
        "tipo_nc": "x",
        "codigo": "924886",
        "data_con": date(2026, 5, 13),
        "data_reparo": date(2026, 5, 20),
    }
    seg = _segmento_atividade_nome_pendentes(nc)
    assert not seg.startswith("DC")
    assert "Danificada" in seg


def test_nome_xlsx_sem_fd_no_final():
    nc = {
        "mae_atividade_q": "FD - Prédio e Pátio",
        "tipo_nc": "x",
        "codigo": "924902",
        "data_con": date(2026, 5, 13),
        "data_reparo": date(2026, 5, 13),
    }
    nome = nome_ficheiro_resposta_artesp_xlsx(nc)
    assert "FD" not in nome
    assert "Prédio e Pátio" in nome


def test_rodovia_incluida_no_stem_via_rod_tag():
    nc = {
        "mae_atividade_q": "Pav. - Limpeza e varredura de áreas pavimentadas",
        "tipo_nc": "x",
        "codigo": "144836",
        "rod_tag": "SP127",
        "rod_raw": "SP 127",
        "data_con": date(2026, 5, 18),
        "data_reparo": date(2026, 5, 25),
    }
    nome = nome_ficheiro_resposta_artesp_xlsx(nc)
    assert "SP127" in nome
    assert "144836" in nome
    assert "18-05-2026" in nome


def test_rodovia_fallback_rod_raw():
    nc = {
        "mae_atividade_q": "Pav. - Limpeza e varredura",
        "tipo_nc": "x",
        "codigo": "144836",
        "rod_raw": "SP 127",
        "data_con": date(2026, 5, 18),
        "data_reparo": date(2026, 5, 25),
    }
    nome = nome_ficheiro_resposta_artesp_xlsx(nc)
    assert "SP127" in nome


def test_sem_rodovia_nao_afeta_stem():
    nc = {
        "mae_atividade_q": "Pav. - Limpeza e varredura",
        "tipo_nc": "x",
        "codigo": "144836",
        "data_con": date(2026, 5, 18),
        "data_reparo": date(2026, 5, 25),
    }
    nome = nome_ficheiro_resposta_artesp_xlsx(nc)
    assert "144836" in nome
    assert "18-05-2026" in nome


def test_atividade_sem_prefixo_inalterada():
    nc = {
        "mae_atividade_q": "Limpeza e varredura",
        "tipo_nc": "y",
        "codigo": "1",
        "data_con": date(2026, 5, 13),
        "data_reparo": date(2026, 5, 13),
    }
    assert "Limpeza e varredura" in _segmento_atividade_nome_pendentes(nc)


def test_segmento_fallback_tipo_nc_sem_mapear_art03():
    """Sem mae_atividade_q: usa texto literal de tipo_nc (ART03/FD só no consolidado Kartado)."""
    nc = {
        "mae_atividade_q": "",
        "tipo_nc": "Prédio e Pátio",
        "codigo": "924902",
        "data_con": date(2026, 5, 13),
        "data_reparo": date(2026, 5, 13),
    }
    assert _segmento_atividade_nome_pendentes(nc) == "Prédio e Pátio"


def test_segmento_prioriza_atividade_como_eml():
    nc = {
        "atividade": "Cobertura forro",
        "mae_atividade_q": "",
        "tipo_nc": "FD - Prédio e Pátio",
        "codigo": "1",
        "data_con": date(2026, 5, 13),
        "data_reparo": date(2026, 5, 13),
    }
    assert _segmento_atividade_nome_pendentes(nc) == "Cobertura forro"


def test_exibicao_atividade_curta_nao_cai_em_tipo_nc():
    nc = {
        "atividade": "Cov",
        "mae_atividade_q": "",
        "tipo_nc": "FD - Prédio e Pátio",
        "codigo": "1",
        "data_con": date(2026, 5, 13),
        "data_reparo": date(2026, 5, 13),
    }
    assert _texto_atividade_exibicao_pendentes(nc) == "Cov"
    assert _segmento_atividade_nome_pendentes(nc) != "Cov"
