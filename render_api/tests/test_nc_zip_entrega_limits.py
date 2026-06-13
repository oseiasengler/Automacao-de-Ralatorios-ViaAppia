"""ZIP NC entrega: profundidade de pastas e limite de caminho interno (Windows 0x80010135)."""

from __future__ import annotations

from render_api.nc_router import (  # noqa: E402
    DIR_PENDENTES_ENTREGA,
    NC_ENTREGA_ZIP_PROFUNDIDADE_RESPOSTAS,
    _NC_KARTADO_ZIP_INTERNO_XLSX,
    _NC_ZIP_MAX_ARC_TOTAL,
    _NC_ZIP_MAX_COMPONENTE,
    _nc_arcnome_zip_para_extracao_windows,
)


def test_kartado_zip_interno_xlsx_nome_curto():
    assert _NC_KARTADO_ZIP_INTERNO_XLSX == "Kartado Consolidado.xlsx"
    assert len(_NC_KARTADO_ZIP_INTERNO_XLSX) <= _NC_ZIP_MAX_COMPONENTE


def _profundidade(arc: str) -> int:
    p = (arc or "").replace("\\", "/").strip("/")
    return len([x for x in p.split("/") if x])


def test_profundidade_padrao_respostas_constante():
    assert NC_ENTREGA_ZIP_PROFUNDIDADE_RESPOSTAS == 2


def test_arcnome_respostas_pendentes_limite_total():
    long_name = ("20260514 - 924705 - 13-05-2026 - Corte e poda de árvores e arbustos em risco " * 4).strip() + ".xlsx"
    arc_in = f"{DIR_PENDENTES_ENTREGA}/" + long_name
    usados: set[str] = set()
    arc_out = _nc_arcnome_zip_para_extracao_windows(arc_in, usados=usados)
    assert len(arc_out) <= _NC_ZIP_MAX_ARC_TOTAL
    assert _profundidade(arc_out) <= 2
    assert not arc_out.startswith("i/") and "/i/" not in f"/{arc_out}/"


def test_arcnome_componente_truncado():
    usados: set[str] = set()
    arc = _nc_arcnome_zip_para_extracao_windows(
        "Kartado/" + ("x" * 200) + ".xlsx",
        usados=usados,
    )
    leaf = arc.split("/")[-1]
    assert len(leaf) <= _NC_ZIP_MAX_COMPONENTE


def test_arcnome_exportar_preserva_nome_m01():
    nome = (
        "20260513 - CONSTATAÇÕES NC LOTE 13 (SP 127 - Conservação) - Prazo - 20-05-2026.xlsx"
    )
    usados: set[str] = set()
    arc = _nc_arcnome_zip_para_extracao_windows(f"exportar/{nome}", usados=usados)
    assert arc == f"exportar/{nome}"
    assert len(arc) <= _NC_ZIP_MAX_ARC_TOTAL


def test_arcnome_respostas_preserva_nomes_pasta():
    nome = "20260513 - CONSTATAÇÕES NC LOTE 13 (SP 127 - Limpeza) - Prazo - 20-05-2026.xlsx"
    usados: set[str] = set()
    arc = _nc_arcnome_zip_para_extracao_windows(
        f"{DIR_PENDENTES_ENTREGA}/{nome}",
        usados=usados,
    )
    assert arc.startswith(f"{DIR_PENDENTES_ENTREGA}/")
    assert nome in arc
