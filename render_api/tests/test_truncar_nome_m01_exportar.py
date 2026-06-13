"""truncar_nome_preservando_sufixo_prazo_m01 — nomes Exportar Art_011."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_NC_ARTESP = _REPO / "nc_artesp"
if str(_NC_ARTESP) not in sys.path:
    sys.path.insert(0, str(_NC_ARTESP))

from utils.helpers import truncar_nome_preservando_sufixo_prazo_m01  # noqa: E402


def test_m01_nome_curto_intacto():
    nome = (
        "20260513 - CONSTATAÇÕES NC LOTE 13 (SP 127 - Conservação) - Prazo - 20-05-2026.xlsx"
    )
    assert truncar_nome_preservando_sufixo_prazo_m01(nome, 150) == nome


def test_m01_preserva_prazo_e_encurta_servico():
    serv_longo = "Corte e poda de árvores e arbustos em risco na faixa de domínio"
    nome = (
        f"20260513 - CONSTATAÇÕES NC LOTE 13 (SP 127 - {serv_longo}) - Prazo - 20-05-2026.xlsx"
    )
    out = truncar_nome_preservando_sufixo_prazo_m01(nome, 100)
    assert len(out) <= 100
    assert out.endswith(" - Prazo - 20-05-2026.xlsx")
    assert "20260513 - CONSTATAÇÕES NC LOTE 13 (SP 127 - " in out
    assert "Praze" not in out
    assert " - Prazo - " in out


def test_limite_80_nao_corta_prazo_no_meio():
    nome = (
        "20260513 - CONSTATAÇÕES NC LOTE 13 (SP 127 - Conservação) - Prazo - 20-05-2026.xlsx"
    )
    out = truncar_nome_preservando_sufixo_prazo_m01(nome, 80)
    assert " - Prazo - 20-05-2026" in out
    assert "Conserv" in out or "Conserva" in out
