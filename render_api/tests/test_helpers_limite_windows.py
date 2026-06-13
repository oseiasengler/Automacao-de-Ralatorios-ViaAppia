"""caminho_dentro_limite_windows — caminhos curtos para Shell / Explorador."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_NC_ARTESP = _REPO / "nc_artesp"
if str(_NC_ARTESP) not in sys.path:
    sys.path.insert(0, str(_NC_ARTESP))

from utils.helpers import caminho_dentro_limite_windows  # noqa: E402


def test_caminho_dentro_trunca_stem_quando_pasta_longa(tmp_path):
    pasta = tmp_path / ("p" * 120)
    nome = "a" * 80 + ".eml"
    out = caminho_dentro_limite_windows(pasta / nome, max_len=220)
    assert len(str(out)) <= 220
    assert out.suffix == ".eml"


def test_caminho_dentro_trunca_quando_stem_longo_e_pasta_curta(tmp_path):
    pasta = tmp_path / "sub"
    nome = "n" * 200 + ".eml"
    out = caminho_dentro_limite_windows(pasta / nome, max_len=248)
    assert len(str(out)) <= 248
    assert out.suffix == ".eml"
    assert len(out.stem) < 200
