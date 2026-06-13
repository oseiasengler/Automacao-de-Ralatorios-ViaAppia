"""parse_data — serial Excel em texto (células data_only como número)."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_NC_ARTESP = _REPO / "nc_artesp"
if str(_NC_ARTESP) not in sys.path:
    sys.path.insert(0, str(_NC_ARTESP))

from utils.helpers import parse_data  # noqa: E402


def test_parse_data_aceita_serial_excel_como_string():
    dt = parse_data("45000")
    assert dt is not None
    assert dt.year >= 2022


def test_parse_data_aceita_serial_excel_float_string():
    dt = parse_data("45000.0")
    assert dt is not None
    assert dt.year >= 2022
