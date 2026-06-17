"""
nc_artesp/config.py
────────────────────────────────────────────────────────────────────────────
Configurações do pipeline NC ARTESP.
Os caminhos de pasta são usados apenas no modo desktop; no modo web (API)
os parâmetros das funções sobrepõem estes defaults.
Valores sobrepõíveis via variáveis de ambiente ARTESP_*.
"""

from __future__ import annotations

import logging
import os
import re
import unicodedata
from pathlib import Path

_logger_cfg = logging.getLogger(__name__)

KARTADO_SERVICOS_MERGE_AVISOS: list[dict[str, str]] = []


def _kartado_merge_ui(level: str, text: str) -> None:
    if (level or "").lower() != "warning":
        return
    KARTADO_SERVICOS_MERGE_AVISOS.append({"level": level, "text": text})


def _normalizar_entrada_servico_kartado(bruto: str, etiqueta: str) -> tuple[str | None, str]:
    """
    Devolve (texto_canónico, "") ou (None, motivo).
    Só corrige casos óbvios de colagem truncada; caso duvidoso → não usar.
    """
    s = " ".join((bruto or "").strip().split())
    if not s:
        return None, "texto vazio"
    antes = s
    for pref in ("OAE", "SH", "ROTINA"):
        if s.startswith(pref):
            tail = s[len(pref) :]
            if re.match(r"^\s*-\S", tail):
                novo_tail = re.sub(r"^(\s*)-(\S)", r"\1- \2", tail, count=1)
                if novo_tail != tail:
                    _logger_cfg.info(
                        "Kartado %s: espaço após hifen corrigido (%s): %r → %r",
                        etiqueta,
                        pref,
                        antes,
                        pref + novo_tail,
                    )
                    _kartado_merge_ui(
                        "info",
                        f"Kartado {etiqueta}: espaço após hífen corrigido ({pref}): {antes!r} → {(pref + novo_tail)!r}",
                    )
                    s = pref + novo_tail
                    antes = s
            break
    if "\x00" in s or len(s) > 500:
        return None, "formato inválido ou texto excessivamente longo"
    return s, ""


def _merge_identity_servicos_kartado(
    destino: dict[str, str],
    candidatos: tuple[str, ...],
    *,
    etiqueta: str,
) -> tuple[str, ...]:
    """
    Regista identity ``serviço → serviço`` em ``destino`` (mesma regra que FD).
    Ignora duplicados no lote; não sobrescreve chave existente com valor diferente (log warning).
    """
    registados: list[str] = []
    visto: set[str] = set()
    for bruto in candidatos:
        s, motivo = _normalizar_entrada_servico_kartado(bruto, etiqueta)
        if s is None:
            _logger_cfg.warning("Kartado %s: entrada ignorada (%s): %r", etiqueta, motivo, bruto)
            _kartado_merge_ui(
                "warning",
                f"Kartado {etiqueta}: entrada ignorada ({motivo}): {bruto!r}",
            )
            continue
        if s in visto:
            continue
        visto.add(s)
        if s in destino:
            if destino[s] == s:
                continue
            _logger_cfg.warning(
                "Kartado %s: não registrei %r — chave já existe no projeto com valor diferente (%r).",
                etiqueta,
                s,
                destino[s],
            )
            _kartado_merge_ui(
                "warning",
                f"Kartado {etiqueta}: não registrei {s!r} — chave já existe no projeto com valor diferente ({destino[s]!r}).",
            )
            continue
        destino.setdefault(s, s)
        registados.append(s)
    return tuple(registados)


def _env_str(key: str, default: str) -> str:
    return (os.environ.get(key) or "").strip() or default

def _env_int(key: str, default: int) -> int:
    try:
        v = (os.environ.get(key) or "").strip()
        return int(v) if v else default
    except ValueError:
        return default


def _env_float(key: str, default: float) -> float:
    try:
        v = (os.environ.get(key) or "").strip().replace(",", ".")
        return float(v) if v else default
    except ValueError:
        return default


def _env_bool(key: str, default: bool) -> bool:
    v = (os.environ.get(key) or "").strip().lower()
    if v in ("1", "true", "yes", "on"):
        return True
    if v in ("0", "false", "no", "off"):
        return False
    return default

_BASE = Path(_env_str("ARTESP_NC_BASE", r"C:\AUTOMAÇÃO_MACROS\Macros Kcor Ellen\artesp_nc_v2.0"))

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 01 — SEPARAR NC
# ═══════════════════════════════════════════════════════════════════════════

M01_EXPORTAR           = _BASE / "Exportar"
M01_ARQUIVOS_ANTERIORES = _BASE / "Arquivos Anteriores"   # destino após processamento completo
M01_LINHA_INICIO        = _env_int("ARTESP_M01_LINHA_INICIO", 5)   # 5 = igual à macro (cabeçalho nas linhas 1–4)
M01_LOTE                = _env_str("ARTESP_LOTE", "LOTE 13")
# Concessionária (col G da EAF / relatório): lote → nome; ex.: Lote 13 → "Lote 13 Rodovias das Colinas"
_LOTE_CONCESSIONARIA = {
    "13": "Rodovias das Colinas",
    "21": "Rodovias do Tietê",
    "26": "SP Serra",
    "50": "CONSOL",
}
LOTES_MENU_ANALISE = [
    ("13", "Lote 13 — Rodovias das Colinas"),
    ("21", "Lote 21 — Rodovias do Tietê"),
    ("26", "Lote 26 — SP Serra"),
    ("50", "Lote 50 — Nascentes das Gerais (Artemig MG)"),
]
# Regra de negócio Kartado: funcionalidades/regras Kartado do ARTESP aplicam-se aos lotes 13/21/26.
LOTES_KARTADO_ARTESP: tuple[str, ...] = ("13", "21", "26")
_env_concessionaria    = (os.environ.get("ARTESP_CONCESSIONARIA_NOME") or "").strip()
_lote_num              = re.search(r"\d+", M01_LOTE)
CONCESSIONARIA_NOME     = _env_concessionaria or _LOTE_CONCESSIONARIA.get((_lote_num.group(0) if _lote_num else ""), "")
# Template EAF: env ou nc_artesp/assets/templates/Template_EAF.xlsx
_template_eaf_env = _env_str("ARTESP_TEMPLATE_EAF", "")
_nc_root = Path(__file__).resolve().parent  # nc_artesp/
_tpl = _nc_root / "assets" / "templates"
if _template_eaf_env:
    M01_TEMPLATE_EAF = Path(_template_eaf_env)
else:
    _candidatos_eaf = [
        _tpl / "Template_EAF.xlsx",
        _tpl / "Template_EAF.xls",
    ]
    M01_TEMPLATE_EAF = next((p for p in _candidatos_eaf if p.is_file()), _candidatos_eaf[0])
# Template do relatório XLSX (Análise PDF): nc_artesp/assets/templates/Template_EAF.xlsx (ou env).
_template_relatorio_env = _env_str("ARTESP_TEMPLATE_RELATORIO", "").strip().strip('"').strip("'")
TEMPLATE_RELATORIO_XLSX = (
    Path(_template_relatorio_env)
    if _template_relatorio_env
    else _tpl / "Template_EAF.xlsx"
)
NOMES_TEMPLATE_RELATORIO = (
    "Template_Relatório de Fiscalização de Conservação de Rotina - Não Conformidades.xls",
    "Template_Relatório de Fiscalização de Conservação de Rotina - Não Conformidades.xlsx",
    "Relatório de Fiscalização de Conservação de Rotina - Não Conformidades.xlsx",
)
# Data do reparo = data do envio + N dias quando não informada
PRAZO_DIAS_APOS_ENVIO   = _env_int("ARTESP_PRAZO_DIAS_APOS_ENVIO", 10)

# ── M01: Separar NC (exportação por grupo / por NC) ──
# Padrão False (Kartado): template único consolidado (Template - Geral - 4 e 5 - Final.xlsx ou Template - geral.xlsx),
#   todas as NCs num .xlsx; coluna «Classe» via ART03 / SERVICO_NC (mapas abaixo).
# True (ARTESP_M01_COPIA_PLANILHA_MAE=1): macro Art_011 — Template_EAF.xlsx + linhas da mãe.
# API (FastAPI): por omissão força cópia mãe via ``m01_kartado=false`` nos endpoints; use m01_kartado=true para Kartado.
M01_COPIA_PLANILHA_MAE = _env_bool("ARTESP_M01_COPIA_PLANILHA_MAE", False)

# Texto coluna Q da planilha-mãe EAF → token no nome do ficheiro exportado (Art_011).
# Sincronizado com os ElseIf ``serv`` da macro; lookup: ``m01_servico_abrev_art011_lookup`` (exacto + espaços + NFC).
# Referência: nc_artesp/Macros/01 - Art_011_EAF_Separar_Mod_Exc_NC.bas
M01_SERVICO_ABREV_ART011: dict[str, str] = {
    "Pichação ao longo da rodovia": "PICHAÇÃO",
    "Substituição de pano rol. Medianamente comprometido": "PAVIMENTO",
    "Reparo definitivo com recorte": "REPARO RECORTE",
    "Remoção de lixo doméstico das instalações": "LIXO INST",
    "Reparo de elemento de drenagem - manutenção": "REPARO DE DRENAGEM",
    "Despraguejamento": "DESPRAGUEJAMENTO",
    "Aceiros": "ACEIRO",
    "Selagem de trincas": "SELAGEM TRINCA",
    "Limpeza e varredura de áreas pavimentadas": "LIMPEZA DE PAVIMENTO",
    "Remoção de lixo e entulho da faixa de domínio": "REMOÇÃO LIXO_ENTULHO",
    "Defensa metálica (manutenção ou substituição)": "REPARO DE DEFENSA",
    "Depressão ou recalque de pequena extensão": "PAVIMENTO - DEPRESSÃO",
    "Buraco ou panela": "PANELA",
    "Panela ou buraco na faixa rolamento": "PANELA",
    "Reparo e reposição de cerca": "REPARO CERCA",
    "Manutenção árvores e arbustos": "MANUTENÇÃO ÁRVORES",
    "Drenagem fora de  plataforma limpeza geral": "LIMP DRENAGEM FORA PLAT",
    "Drenagem fora de plataforma limpeza geral": "LIMP DRENAGEM FORA PLAT",
    "Remoção de árvores ou galhos que não tem risco": "REMOÇÃO DE GALHOS",
    "Drenagem plataforma limpeza geral": "LIMP DRENAGEM PLAT",
    "Recomposição de erosão em corte / aterro": "EROSÃO",
    "Substituição de junta de dilatação": "JUNTA DILATAÇÃO",
    "Juntas e trincas: Limpeza e Resselagem": "JUNTA DILATAÇÃO - LIMPEZA",
    "Depressão em encontro de obra de arte": "DEPRESSÃO OAE",
    "Recuperação do revestimento vegetal": "PLANTIO DE GRAMA",
    "Remoção de massa verde": "MASSA VERDE",
    "Drenagem profunda limpeza geral": "LIMP DE DRENAGEM PROF",
    "Pavimentação/ Passeio/ Alambrado": "PRÉDIO E PÁTIO - OUTROS",
    "Poda manual ou mecanizada": "PODA DO REVESTIMENTO",
    "Bueiros limpeza geral": "BUEIROS - LIMPEZA",
    "Bordos e lajes quebrados reparo definitivo com recorte": "PAVIMENTO RIGIDO",
    "Correção de degrau entre pista e acostam. não pavimentado": "DEGRAU PISTA_ACOSTAMENTO",
    "Correção de degrau entre a pista e acostamento": "DEGRAU PISTA_ACOSTAMENTO",
    "Desobstrução de elemento de drenagem": "DESOBSTRUÇÃO DE DRENAGEM",
    "Conformação lateral": "CONFORMAÇÃO LATERAL",
    "Pichações e vandalismo": "PICHAÇÃO",
    "Hidráulica/ Esgoto/ Drenagem": "HIDR_ESG_DREN",
    "Barreira rígida manutenção e ou reparo": "BARREIRA RIGIDA",
    "Reconformação de vias secundárias": "CONFORM. LATERAL",
    "Louças/ Metais": "PREDIO - LOUÇAS_METAIS",
}


def m01_servico_abrev_art011_lookup(tipo_col_q: str) -> str | None:
    """
    Texto da coluna Q (tipo de NC / serviço na mãe EAF) → abreviatura do nome do ficheiro Exportar (VBA Art_011).
    Ordem: igualdade exacta; espaços colapsados; NFC Unicode; por último comparação casefold às chaves.
    """
    raw = (tipo_col_q or "").strip()
    if not raw:
        return None
    d = M01_SERVICO_ABREV_ART011
    if raw in d:
        return d[raw]
    norm_ws = " ".join(raw.split())
    if norm_ws in d:
        return d[norm_ws]
    nfc = unicodedata.normalize("NFC", norm_ws)
    if nfc in d:
        return d[nfc]
    nfc_cf = nfc.casefold()
    for k, v in d.items():
        if unicodedata.normalize("NFC", " ".join(str(k).split())).casefold() == nfc_cf:
            return v
    return None


M01_DICAS_PALAVRA_TEMPLATE_KARTADO: list[tuple[str, str]] = [
    ("panela", "Panela_Buraco"),
    ("buraco", "Panela_Buraco"),
    ("capina", "Capina"),
    ("dren", "Dren."),
    ("defensa", "Defensa"),
    ("eros", "Eros"),
    ("alambrado", "Alambrado"),
]

# M01 modo Kartado (templates por atividade): texto da coluna Q da EAF (tipo de NC / atividade)
# → nome do ficheiro .xlsx do Kartado (ex. «Pav. - Panela_Buraco.xlsx»), alinhado à macro Art_03_KTD / planilhas padrão.
# O valor (antes de «.xlsx») é também o texto da coluna «Classe» no export M01 Kartado quando há match;
# sem match, M01 usa SERVICO_NC. Chave = texto da coluna Q da mãe EAF.
#
# Lista canónica FD (stems dos templates em nc_artesp/assets/templates/): relatórios Kartado, UI/API e lookup quando
# col Q já traz o serviço no formato «FD - …». Ver também ART03_ATIVIDADE_PARA_SERVICO_KARTADO (merge via setdefault).
KARTADO_RELATORIO_SERVICOS_FD: tuple[str, ...] = (
    "FD - Animais Mortos - Remoção",
    "FD - Call Box - Guarda Corpo Danificado",
    "FD - Call Box - Guarda Corpo Limpeza/Pintura",
    "FD - Call Box - Limpeza Passeio",
    "FD - Call Box - Limpeza Totem",
    "FD - Call Box - Outros",
    "FD - Cargas - Limpeza",
    "FD - Conformação Lateral",
    "FD - Conformação Talude",
    "FD - Controle Fitossanitário",
    "FD - Deslizamento Talude",
    "FD - Despraguejamento (Prédio/Pátio)",
    "FD - Empoçamento - Conformação",
    "FD - Erosão",
    "FD - Lixo/Entulho",
    "FD - Monumentos - Limpeza/Pintura",
    "FD - Monumentos - Reparo",
    "FD - Parada ônibus - Limpeza/Pintura",
    "FD - Parada ônibus - Reparo",
    "FD - Passeio - Limpeza",
    "FD - Passeio - Reparo",
    "FD - Pichação",
    "FD - Prédio e Pátio",
    "FD - Utilidades Públicas - Limpeza/Reparo",
)

_KARTADO_RELATORIO_SERVICOS_EXTRA_LINHAS = ""

KARTADO_RELATORIO_SERVICOS_EXTRA_RAW: tuple[str, ...] = tuple(
    ln.strip()
    for ln in _KARTADO_RELATORIO_SERVICOS_EXTRA_LINHAS.splitlines()
    if ln.strip()
)


def _kartado_barra_em_valor_classe(v: str) -> str:
    s = str(v or "")
    if s.lower().endswith(".xlsx"):
        return s
    return s.replace("_", "/")


def _kartado_art03_aplicar_barra_nos_valores(d: dict[str, str]) -> None:
    for _k in list(d.keys()):
        _v = d[_k]
        if not isinstance(_v, str):
            continue
        _nv = _kartado_barra_em_valor_classe(_v)
        if _nv != _v:
            d[_k] = _nv


def _kartado_art03_espelhar_chaves_com_barra(d: dict[str, str]) -> None:
    for _k in list(d.keys()):
        if not isinstance(_k, str) or "_" not in _k:
            continue
        _nk = _kartado_barra_em_valor_classe(_k)
        if _nk == _k or _nk in d:
            continue
        d[_nk] = d[_k]


def _kartado_art03_registar_identidade_e_legado_sub(d: dict[str, str]) -> None:
    for _vv in {_v for _v in d.values() if isinstance(_v, str)}:
        if _vv.lower().endswith(".xlsx"):
            continue
        d.setdefault(_vv, _vv)
        if "/" in _vv:
            leg = _vv.replace("/", "_")
            if leg != _vv:
                d.setdefault(leg, _vv)


ART03_ATIVIDADE_PARA_SERVICO_KARTADO: dict[str, str] = {
    # Chaves = texto da coluna «Atividade» na mãe EAF (detetada pelo cabeçalho — típico N ou Q).
    # Valores → coluna «Classe» só no .xlsx consolidado Kartado (M01, template Geral); não usar noutros fluxos (Kcor, Pendentes).
    "Reparo e reposição de alambrado": "CTA - Alambrado - Danificado",
    "Reparo e reposição de cerca": "CTA - Cerca - Danificada",
    "Elemento antiofuscante(substituição ou reposição)": "CTA - Tela Antiofuscante - Danificada",
    "Barreira rígida manutenção e ou reparo": "DC - Barreira Rígida - Danificada",
    "Barreira rígida danificada": "DC - Barreira Rígida - Danificada",
    "Reparo e substituição": "DC - Defensa Metálica/Terminais - Danificada",
    "Defensa metálica": "DC - Defensa Metálica/Terminais - Danificada",
    "Defensa metálica (manutenção ou substituição)": "DC - Defensa Metálica/Terminais - Danificada",
    "Defensa metálica danificada": "DC - Defensa Metálica/Terminais - Danificada",
    "Bueiros limpeza geral": "Dren. - Caixas - Limpeza",
    "Drenagem profunda limpeza geral": "Dren. - Linha de Tubo - Limpeza",
    "Desobstrução de elemento de drenagem": "Dren. - Montante/Jusante - Limpeza",
    "Drenagem fora de plataforma limpeza geral": "Dren. - Montante/Jusante - Limpeza",
    "Drenagem fora de  plataforma limpeza geral": "Dren. - Montante/Jusante - Limpeza",
    "Drenagem plataforma limpeza geral": "Dren. - Superficial - Limpeza",
    "Drenagem limpeza geral": "Dren. - Superficial - Limpeza",
    "Reparo de elemento de drenagem - manutenção": "Dren. - Superficial - Reparo",
    "Reparo de elemento de drenagem em risco a rodovia": "Dren. - Superficial - Reparo",
    "Reparo de elemento de drenagem  (manutenção)": "Dren. - Superficial - Reparo",
    "Conformação lateral": "FD - Conformação Lateral",
    "Despraguejamento": "FD - Controle Fitossanitário",
    "Recomposição de erosão em corte / aterro": "FD - Erosão",
    "Remoção material e limpeza plataforma": "FD - Erosão",
    "Remoção de lixo e entulho da faixa de domínio": "FD - Lixo/Entulho",
    "Remoção de lixo doméstico das instalações": "FD - Lixo/Entulho",
    "Pichações e vandalismo": "FD - Pichação",
    "Pichação ao longo da rodovia": "FD - Pichação",
    "Hidráulica/ Esgoto/ Drenagem": "FD - Prédio e Pátio",
    "Pintura / Revestimento": "FD - Prédio e Pátio",
    "Pintura  Revestimento": "FD - Prédio e Pátio",
    "Conservação preventiva e corretiva": "FD - Prédio e Pátio",
    "Verificação e conservação": "FD - Prédio e Pátio",
    "Substituição, reparo ou limpeza": "FD - Prédio e Pátio",
    "Caixilhos  Esquadrias": "FD - Prédio e Pátio",
    "Paredes / Piso": "FD - Prédio e Pátio",
    "Paredes _ Piso": "FD - Prédio e Pátio",
    "Ponto de onibus": "FD - Parada ônibus - Reparo",
    "Pontos de onibus": "FD - Parada ônibus - Reparo",
    "Ponto de ônibus": "FD - Parada ônibus - Reparo",
    "Pontos de ônibus": "FD - Parada ônibus - Reparo",
    "Paradas de ônibus, monumentos e utilidades publicas": "FD - Parada ônibus - Reparo",
    "Paradas de ônibus, monumentos e utilidades públicas": "FD - Parada ônibus - Reparo",
    "Paradas de onibus, monumentos e utilidades publicas": "FD - Parada ônibus - Reparo",
    "Pavimentação/ Passeio/ Alambrado": "FD - Prédio e Pátio",
    "Limpeza ou pintura de superfície exposta ao trafego": "FD - Utilidades Públicas - Limpeza/Reparo",
    "Substituição de aparelho de apoio": "OAE - Estrutura - Danos",
    "Guarda-corpo danificado": "OAE - Guarda corpos e Balaústres - Danificado",
    "Substituição de junta de dilatação": "OAE - Junta de Dilatação",
    "Juntas e trincas: Limpeza e Resselagem": "OAE - Limpeza",
    "Limpeza ou pintura de superficie exposta ao tráfego": "OAE - Limpeza",
    "Depressão em encontro de obra de arte": "Pav. - Depressão encontro OAE",
    "Correção de degrau entre pista e acostam. não pavimentado": "Pav. - Degrau",
    "Correção de degrau entre a pista e acostamento": "Pav. - Degrau",
    "Depressão ou recalque de pequena extensão": "Pav. - Depressão ou Recalque",
    "Limpeza de áreas pavimentadas": "Pav. - Limpeza",
    "Limpeza e varredura de áreas pavimentadas": "Pav. - Limpeza",
    "Panela ou buraco na faixa rolamento": "Pav. - Panela/Buraco",
    "Buraco ou panela": "Pav. - Panela/Buraco",
    "Reparo definitivo com recorte": "Pav. - Reparo com recorte",
    "Bordos e lajes quebrados reparo definitivo com recorte": "Pav. - Reparo de Bordos e Lajes",
    "Substituição de pano rol. comprometido": "Pav. - Substituição de Pano de Rolamento",
    "Substituição de pano rol. Medianamente comprometido": "Pav. - Substituição de Pano de Rolamento",
    "Selagem de trincas": "Pav. - Trincas",
    "Aceiros": "VD - Vegetação - Aceiro",
    "Capina": "VD - Vegetação - Capina Vegetação",
    "Poda manual ou mecanizada": "VD - Vegetação - Poda do Revestimento Vegetal",
    "Recuperação do revestimento vegetal": "VD - Vegetação - Recuperação do Revestimento (Plantio)",
    "Remoção de massa verde": "VD - Vegetação - Remoção de Massa Seca",
    "Corte e poda de árvores e arbustos em risco": "VD - Árvores e Arbustos - Manutenção/Poda Galhos",
    "Manutenção árvores e arbustos": "VD - Árvores e Arbustos - Manutenção/Poda Galhos",
    "Remoção de árvores ou galhos que não tem risco": "VD - Árvores e Arbustos - Remoção de Galhos",
}

# Aliases diretos da planilha-mãe (tipos de apontamento) -> classes FD aceitas no consolidado Kartado.
ART03_ATIVIDADE_PARA_SERVICO_KARTADO.update({
    "Call Box - Guarda Corpo Limpeza_Pintura": "FD - Call Box - Guarda Corpo Limpeza/Pintura",
    "Call Box - Limpeza Passeio": "FD - Call Box - Limpeza Passeio",
    "Call Box - Limpeza Totem": "FD - Call Box - Limpeza Totem",
    "Call Box - Outros": "FD - Call Box - Outros",
    "Cargas - Limpeza": "FD - Cargas - Limpeza",
    "Conformaçao Lateral": "FD - Conformacao Lateral",
    "Conformação Lateral": "FD - Conformacao Lateral",
    "Conformacao Talude": "FD - Conformacao Talude",
    "Conformação Talude": "FD - Conformacao Talude",
    "Controle Fitossanitario": "FD - Controle Fitossanitario",
    "Controle Fitossanitário": "FD - Controle Fitossanitario",
    "Deslizamento Talude": "FD - Deslizamento Talude",
    "Despraguejamento (Predio_Patio)": "FD - Despraguejamento (Prédio/Pátio)",
    "Despraguejamento (Prédio_Pátio)": "FD - Despraguejamento (Prédio/Pátio)",
    "Empoçamento - Conformação": "FD - Empocamento - Conformacao",
    "Empocamento - Conformacao": "FD - Empocamento - Conformacao",
    "Erosão": "FD - Erosao",
    "Erosao": "FD - Erosao",
    "Lixo_Entulho": "FD - Lixo/Entulho",
    "Lixo/Entulho": "FD - Lixo/Entulho",
    "Monumentos - Limpeza_Pintura": "FD - Monumentos - Limpeza/Pintura",
    "Monumentos - Reparo": "FD - Monumentos - Reparo",
    "Parada onibus - Limpeza_Pintura": "FD - Parada onibus - Limpeza/Pintura",
    "Parada ônibus - Limpeza_Pintura": "FD - Parada onibus - Limpeza/Pintura",
    "Parada onibus - Reparo": "FD - Parada onibus - Reparo",
    "Parada ônibus - Reparo": "FD - Parada onibus - Reparo",
    "Passeio - Limpeza": "FD - Passeio - Limpeza",
    "Passeio - Reparo": "FD - Passeio - Reparo",
    "Pichação": "FD - Pichaao",
    "Pichacao": "FD - Pichaao",
    "Pichaao": "FD - Pichaao",
    "Predio e Patio": "FD - Predio e Patio",
    "Prédio e Pátio": "FD - Predio e Patio",
    "Utilidades Publicas - Limpeza_Reparo": "FD - Utilidades Publicas - Limpeza/Reparo",
    "Utilidades Públicas - Limpeza_Reparo": "FD - Utilidades Publicas - Limpeza/Reparo",
    "Animais Mortos - Remocao": "FD - Animais Mortos - Remocao",
    "Animais Mortos - Remoção": "FD - Animais Mortos - Remocao",
})

for _kart_fd_srv in KARTADO_RELATORIO_SERVICOS_FD:
    ART03_ATIVIDADE_PARA_SERVICO_KARTADO.setdefault(_kart_fd_srv, _kart_fd_srv)

_kartado_art03_aplicar_barra_nos_valores(ART03_ATIVIDADE_PARA_SERVICO_KARTADO)
_kartado_art03_espelhar_chaves_com_barra(ART03_ATIVIDADE_PARA_SERVICO_KARTADO)

_KARTADO_EXTRA_REGISTRADOS = _merge_identity_servicos_kartado(
    ART03_ATIVIDADE_PARA_SERVICO_KARTADO,
    KARTADO_RELATORIO_SERVICOS_EXTRA_RAW,
    etiqueta="relatorio_extra",
)

_kartado_art03_aplicar_barra_nos_valores(ART03_ATIVIDADE_PARA_SERVICO_KARTADO)
_kartado_art03_espelhar_chaves_com_barra(ART03_ATIVIDADE_PARA_SERVICO_KARTADO)
_kartado_art03_registar_identidade_e_legado_sub(ART03_ATIVIDADE_PARA_SERVICO_KARTADO)

KARTADO_RELATORIO_SERVICOS_TODOS: tuple[str, ...] = tuple(
    dict.fromkeys(
        (
            *(_kartado_barra_em_valor_classe(s) for s in KARTADO_RELATORIO_SERVICOS_FD),
            *(_kartado_barra_em_valor_classe(s) for s in _KARTADO_EXTRA_REGISTRADOS),
        )
    )
)


def _kartado_stem_ficheiro_template_xlsx(valor_classe: str) -> str:
    """Stem do .xlsx no disco: «/» (e «\\») substituídos por «_» (Windows); classe canónica pode usar «/»."""
    s = (valor_classe or "").strip()
    if s.lower().endswith(".xlsx"):
        s = s[:-5]
    stem = s.replace("/", "_").replace("\\", "_")
    return f"{stem}.xlsx"


# Mesmo mapeamento Art_03 → nome de ficheiro (.xlsx em nc_artesp/assets/templates/ ou fotos_campo/assets/templates/).
M01_MAPA_ATIVIDADE_TEMPLATE_KARTADO = {
    k: (v if str(v).lower().endswith(".xlsx") else _kartado_stem_ficheiro_template_xlsx(v))
    for k, v in ART03_ATIVIDADE_PARA_SERVICO_KARTADO.items()
}

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 02 — GERAR MODELO FOTO (macro Art_022)
# Saída Kria:  Arquivos/Arquivo Foto - Conserva/  |  Nome: yyyymmdd-hhmm - {Artesp}.xlsx
# Saída Resposta: _Respostas/_Relatório EAF - NC/Pendentes/  |  Nome: yyyymmdd - hhmmss - {rodovia} - dd-mm-yyyy - {nc}.xlsx
# ═══════════════════════════════════════════════════════════════════════════

M02_FOTOS_NC     = _BASE / "Imagens Provisórias"
M02_FOTOS_PDF    = _BASE / "Imagens Provisórias - PDF"
M02_SALVAR_FOTO  = _BASE / "Arquivos" / "Arquivo Foto - Conserva"
# Modelos M02: somente em nc_artesp/assets/templates/ (igual às macros)
M02_MODELO_KRIA  = _nc_root / "assets" / "templates" / "Modelo Abertura Evento Kria Conserva Rotina.xlsx"
M02_MODELO_RESP  = _nc_root / "assets" / "templates" / "Modelo.xlsx"
M02_PENDENTES    = _BASE / "_Respostas" / "_Relatório EAF - NC" / "Pendentes"
# Cabeçalhos exactos (linha 1) nas exportações Kartado: M01 grava texto da mãe (Q e O); M02 lê só para o nome do ficheiro Resposta Pendentes — não reutilizar «Classe»/consolidado.
RESPOSTA_PENDENTES_HEADER_MAE_ATIVIDADE_Q = "Atividade (mãe EAF)"
RESPOSTA_PENDENTES_HEADER_MAE_TIPO_ATIV_O = "Tipo atividade (mãe EAF)"
# PDF de origem para step 1.5 (opcional — pode ser None)
M02_PDF_ARQUIVO  = _env_str("ARTESP_M02_PDF_ARQUIVO", "")   # caminho fixo de PDF (single mode)
M02_PDF_ORIGEM   = _env_str("ARTESP_M02_PDF_ORIGEM",  "")

# nc (N).jpg: 800×500 px, 222×319 DPI. Tamanho efetivo no Excel é o do merge do template.
M02_FOTO_W     = _env_int("ARTESP_M02_FOTO_W",     800)
M02_FOTO_H     = _env_int("ARTESP_M02_FOTO_H",     500)
M02_FOTO_DPI_X = _env_int("ARTESP_M02_FOTO_DPI_X", 222)
M02_FOTO_DPI_Y = _env_int("ARTESP_M02_FOTO_DPI_Y", 319)
# PDF (N).jpg / quadro Resposta no Modelo.xlsx ≈ 16,77×7 cm → px a 96 DPI (alinhado ao merge)
M02_FOTO_PDF_W = _env_int("ARTESP_M02_FOTO_PDF_W", 960)
M02_FOTO_PDF_H = _env_int("ARTESP_M02_FOTO_PDF_H", 401)
# PyMuPDF antes do redimensionamento (Extrair PDF — ARTESP e Artemig lote 50)
M02_EXTRACAO_RENDER_DPI = _env_int("ARTESP_M02_EXTRACAO_RENDER_DPI", 300)
# PDF (COD).jpg: False = um só pixmap largura total do clip detectado (comportamento estável).
# True = cabeçalho largura total + faixa foto estreita (experimental).
M02_RECORTE_PREVIEW_COMPOSITO = _env_bool("ARTESP_M02_RECORTE_PREVIEW_COMPOSITO", False)
# Altura da faixa «full width» medida desde **clip.y0** (não desde o topo da página).
M02_RECORTE_COMPOSITO_ALTURA_CAB_PT = _env_int(
    "ARTESP_M02_RECORTE_COMPOSITO_ALTURA_CAB_PT", 150
)
M02_RECORTE_COMPOSITO_FOTO_LARGURA_FRACAO = _env_float(
    "ARTESP_M02_RECORTE_COMPOSITO_FOTO_LARGURA_FRACAO", 0.60
)
# Opcional: força vertical na pré-visualização PDF (COD).jpg (0 em ambos = usa bloco detectado).
M02_RECORTE_PDF_PREVIEW_Y0_PT = _env_int("ARTESP_M02_RECORTE_PDF_PREVIEW_Y0_PT", 0)
M02_RECORTE_PDF_PREVIEW_Y1_PT = _env_int("ARTESP_M02_RECORTE_PDF_PREVIEW_Y1_PT", 0)
# PDF (COD).jpg: após render, cortar colunas quase brancas à esquerda/direita (pixels).
M02_RECORTE_TRIM_BRANCO_PDF_PREVIEW = _env_bool(
    "ARTESP_M02_RECORTE_TRIM_BRANCO_PDF_PREVIEW", True
)
M02_RECORTE_TRIM_BRANCO_LIMIAR = _env_int("ARTESP_M02_RECORTE_TRIM_BRANCO_LIMIAR", 248)
M02_RECORTE_TRIM_BRANCO_PAD_PX = _env_int("ARTESP_M02_RECORTE_TRIM_BRANCO_PAD_PX", 4)

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 03 — INSERIR NC CONSERVAÇÃO (macro Art_03)
# Saída: Arquivos/Conservação/  |  Nome: yyyymmdd-hhmm - {cco}.xlsx
# ═══════════════════════════════════════════════════════════════════════════

M03_ENTRADA      = _BASE / "Arquivos" / "Arquivo Foto - Conserva"
M03_IMAGENS      = _BASE / "Imagens" / "Conservação"
# Modelo Kcor-Kria: somente em nc_artesp/assets/templates/
M03_MODELO_KCOR  = _nc_root / "assets" / "templates" / "_Planilha Modelo Kcor-Kria.xlsx"
M03_SAIDA        = _BASE / "Arquivos" / "Conservação"
M03_LINHA_INICIO = _env_int("ARTESP_M03_LINHA_INICIO", 9)   # âncora y (linha do km)
M03_BLOCO        = _env_int("ARTESP_M03_BLOCO", 5)           # linhas por bloco NC

# Planilha «Exportar» rotina (ZIP final entrega/Exportar/Exportar.xlsx)
_env_tpl_exportar_rotina = _env_str("ARTESP_TEMPLATE_EXPORTAR_ROTINA", "").strip().strip('"').strip("'")
TEMPLATE_EXPORTAR_ROTINA = (
    Path(_env_tpl_exportar_rotina)
    if _env_tpl_exportar_rotina
    else (_nc_root / "assets" / "templates" / "Exportar.xlsx")
)

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 04 — JUNTAR ARQUIVOS (macro Art_04)
# Saída: Arquivos/Conservação/Acumulado/  |  Nome: yyyymmdd - hhmmss - Eventos Acumulado Artesp para Exportar Kria.xlsx
# Template padrão (macro): Acumulado/Padrão/Eventos Acumulado Artesp para Exportar Kria.xlsx
# ═══════════════════════════════════════════════════════════════════════════
# O que alimenta o acumulado: os .xlsx em Arquivos/Conservação (saída do M03).

M04_ENTRADA    = _BASE / "Arquivos" / "Conservação"   # pasta com os Kcor-Kria individuais (M03)
M04_ACUMULADO  = _BASE / "Acumulado" / "Kcor_Acumulado.xlsx"  # arquivo acumulado (rede)
M04_SAIDA      = _BASE / "Arquivos" / "Conservação" / "Acumulado"  # igual à macro
M04_NOME_SAIDA = "Eventos Acumulado Artesp para Exportar Kria.xlsx"  # nome exato do relatório (macro)
# Planilha-base vazia do acumulado (layout Kcor-Kria): ficheiro dedicado em templates/
M04_TEMPLATE_ACUMULADO = _nc_root / "assets" / "templates" / "Acumulado.xlsx"
M04_MODELO_ACUMULADO = _nc_root / "assets" / "templates" / "Eventos Acumulado Artesp para Exportar Kria.xlsx"  # fallback macro


def resolver_template_acumulado_kcor_kria() -> Path | None:
    """
    Planilha-base do acumulado no layout Kcor-Kria (A1 = NumItem), independente do Kartado.
    Ordem: env ARTESP_M04_TEMPLATE_ACUMULADO_KCOR_KRIA → Acumulado.xlsx → M03_MODELO_KCOR
    → Eventos Acumulado… → ficheiros *Kcor*Kria* em assets/templates/ (case-insensitive no Linux).
    """
    try:
        from nc_artesp.utils.helpers import resolver_path_ficheiro_ci
    except ImportError:
        from utils.helpers import resolver_path_ficheiro_ci

    def _ok(c: Path) -> Path | None:
        r = resolver_path_ficheiro_ci(c)
        return r if r.is_file() else None

    envp = _env_str("ARTESP_M04_TEMPLATE_ACUMULADO_KCOR_KRIA", "").strip().strip('"').strip("'")
    if envp:
        return _ok(Path(envp))
    for cand in (M04_TEMPLATE_ACUMULADO, M03_MODELO_KCOR, M04_MODELO_ACUMULADO):
        hit = _ok(cand)
        if hit is not None:
            return hit
    td = _nc_root / "assets" / "templates"
    if td.is_dir():
        kcor_kria: list[Path] = []
        try:
            for c in td.iterdir():
                if not c.is_file() or c.name.startswith("~"):
                    continue
                if not c.suffix.casefold().startswith(".xls"):
                    continue
                n = c.name.casefold()
                if "kcor" in n and "kria" in n:
                    kcor_kria.append(c)
        except OSError:
            pass
        for c in sorted(kcor_kria, key=lambda x: x.name.casefold()):
            hit = _ok(c)
            if hit is not None:
                return hit
    return None


CABECALHO_KCOR_KRIA = [
    "NumItem", "Origem", "Motivo", "Classificação", "Tipo",
    "Rodovia", "KMi", "KMf", "Sentido", "Local",
    "Gestor", "Executor", "Data Solicitação", "Data Suspensão",
    "DtInicio_Prog", "DtFim_Prog", "DtInicio_Exec", "DtFim_Exec",
    "Prazo", "ObsGestor", "Observações", "Diretório", "Arquivos",
    "Indicador", "Unidade",
]
NUM_COLUNAS_KCOR_KRIA = 25  # A–Y

# Coluna V «Diretório» no Kcor-Kria: texto de rede das macros (Art_03 / Kria2), não o Path local
# (M03_IMAGENS / M07_IMAGENS) da máquina que gera o Excel (API, Render, PC do técnico).
_KCOR_V_DIR_CONS = r"L:\ENGENHARIA\CONSERVA\06 - Abertura Externa Evento Kria\Imagens\Conservação"
_KCOR_V_DIR_MA = r"L:\ENGENHARIA\CONSERVA\06 - Abertura Externa Evento Kria\Imagens\Meio Ambiente"
KCOR_KRIA_DIRETORIO_TEXTO_CONSERVACAO = _env_str(
    "ARTESP_KCOR_DIRETORIO_TEXTO_CONSERVACAO", _KCOR_V_DIR_CONS
).rstrip("\\/")
KCOR_KRIA_DIRETORIO_TEXTO_MEIO_AMBIENTE = _env_str(
    "ARTESP_KCOR_DIRETORIO_TEXTO_MEIO_AMBIENTE", _KCOR_V_DIR_MA
).rstrip("\\/")

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 05 — INSERIR NÚMERO KRIA
# ═══════════════════════════════════════════════════════════════════════════

M05_COL_NUMERO = _env_str("ARTESP_M05_COL_NUMERO", "Y")
M05_SUFIXO     = _env_str("ARTESP_M05_SUFIXO",     "26")

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 06 — EXPORTAR CALENDÁRIO
# ═══════════════════════════════════════════════════════════════════════════

M06_PASTA_OUTLOOK = _BASE / "Calendario"

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 07 — INSERIR NC MEIO AMBIENTE (macro Kria2_Inserir_NC_MA_Salvar_Img)
# Saída: Arquivos/Meio Ambiente/  |  Nome: yyyymmdd-hhmm - {cco}.xlsx
# ═══════════════════════════════════════════════════════════════════════════

M07_ENTRADA      = _BASE / "Arquivos" / "Arquivo Foto - MA"
M07_IMAGENS      = _BASE / "Imagens" / "Meio Ambiente"
M07_SAIDA        = _BASE / "Arquivos" / "Meio Ambiente"
M07_MODELO_KCOR  = _nc_root / "assets" / "templates" / "_Planilha Modelo Kcor-Kria.xlsx"  # mesmo modelo do M03

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULOS 1–4 EXCLUSIVOS MEIO AMBIENTE (equivalentes M01, M02, M03, M04 para MA)
# M01 MA: EAF desde PDF + Separar NC → Exportar MA
# M02 MA: Gerar Modelo Foto (Kria + Resposta) desde Exportar MA
# M03 MA: = M07 (Inserir NC / Kcor-Kria Meio Ambiente)
# M04 MA: Juntar Kcor-Kria MA → Acumulado MA
# ═══════════════════════════════════════════════════════════════════════════

M01_MA_EAF          = _BASE / "Arquivos" / "Meio Ambiente" / "EAF MA"           # planilha-mãe EAF MA
M01_MA_EXPORTAR     = _BASE / "Arquivos" / "Meio Ambiente" / "Exportar MA"       # saída Separar NC (EAF individuais)
M02_MA_KRIA         = _BASE / "Arquivos" / "Meio Ambiente" / "Arquivo Foto MA"  # saída Kria M02
M02_MA_PENDENTES    = _BASE / "Arquivos" / "Meio Ambiente" / "Pendentes MA"      # saída Resposta M02
M04_MA_ENTRADA     = _BASE / "Arquivos" / "Meio Ambiente"                        # Kcor-Kria individuais (saída M03 MA)
M04_MA_ACUMULADO   = _BASE / "Acumulado" / "Kcor_Acumulado_MA.xlsx"             # acumulado MA (rede)
M04_MA_SAIDA       = _BASE / "Arquivos" / "Meio Ambiente" / "Acumulado"          # pasta do relatório acumulado MA
M04_MA_NOME_SAIDA  = "Eventos Acumulado Artesp MA - Exportar Kria.xlsx"         # nome do relatório acumulado MA

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 08 — SALVAR IMAGEM
# ═══════════════════════════════════════════════════════════════════════════

M08_IMAGENS_SRC   = _BASE / "Imagens" / "Conservação"
M08_DESTINO       = Path(r"D:\Apontamentos NC Artesp - Imagens Classificadas")
M08_EXPORTAR      = M08_DESTINO / "_Exportar"
M08_TIPOS_EXPORTAR = ("Pav. - Depressao", "Pav. - Pano de Rolamento")
M08_TIPO_NOME_PASTA: dict[str, str] = {}   # preenchido abaixo

# ═══════════════════════════════════════════════════════════════════════════
# E-MAIL
# ═══════════════════════════════════════════════════════════════════════════

M02_FOTOS_PDF_NC  = M02_FOTOS_PDF   # alias usado por nc_criar_email
NC_EMAIL_CC: list[str] = []         # destinatários em cópia (configurar por env se necessário)
NC_EMAIL_PREVIEW_EXCEL_VISIBLE = _env_bool("ARTESP_NC_EMAIL_PREVIEW_EXCEL_VISIBLE", False)

# ═══════════════════════════════════════════════════════════════════════════
# RODOVIAS — pipeline ARTESP (lotes 13 / 21 / 26 + env ARTESP_LOTE).
# Artemig (lote 50 / MG) é pacote e regras próprios em ``nc_artemig`` — não misturar aqui.
# O Excel Kartado em ``Kartado/*.xlsx`` (ARTESP_RODOVIAS_KARTADO_XLSX) só acrescenta aliases SP/SPI/SPA.
# ═══════════════════════════════════════════════════════════════════════════

_ROD_SPI102_INTER = {
    "tag": "SPI102/300",
    "nome": "Interligação SP-102/SP-300",
    "sentidos": ["Norte", "Sul"],
}

_RODOVIAS_CORE: dict[str, dict] = {
    "SP 021": {"tag": "SP021",       "nome": "Rod. SP 021 (SP Serra — Lote 26)",     "sentidos": []},
    "SP 075": {"tag": "SP075",       "nome": "Rod. Senador José Ermírio de Moraes",  "sentidos": ["Norte", "Sul"]},
    "SP 127": {"tag": "SP127",       "nome": "Rod. João Mellão",                     "sentidos": ["Norte", "Sul"]},
    "SP 280": {"tag": "SP280",       "nome": "Rod. Castello Branco",                 "sentidos": ["Leste", "Oeste"]},
    "SP 300": {"tag": "SP300",       "nome": "Rod. Marechal Rondon",                 "sentidos": ["Leste", "Oeste"]},
    "SP 102": _ROD_SPI102_INTER,
    "SPI 102/300": _ROD_SPI102_INTER,
    "SPI102/300": _ROD_SPI102_INTER,
    "SPI 102-300": _ROD_SPI102_INTER,
    "CP 147": {"tag": "FORA",        "nome": "Rod. Fora do Lote",                    "sentidos": []},
    "CP 308": {"tag": "FORA",        "nome": "Rod. Fora do Lote",                    "sentidos": []},
}


def _resolver_xlsx_parametrizacao_kartado_rodoivas() -> Path | None:
    env_path = _env_str("ARTESP_RODOVIAS_KARTADO_XLSX", "").strip()
    if env_path:
        p = Path(env_path)
        return p if p.is_file() else None
    kd = Path(__file__).resolve().parent.parent / "Kartado"
    if not kd.is_dir():
        return None
    cand = [p for p in sorted(kd.glob("*.xlsx")) if "rodovia" in p.name.lower()]
    return cand[0] if cand else None


def _fusao_rodoivas_core_com_kartado_xlsx(core: dict[str, dict]) -> dict[str, dict]:
    out = dict(core)
    path_xlsx = _resolver_xlsx_parametrizacao_kartado_rodoivas()
    if path_xlsx is None:
        return out
    try:
        try:
            from nc_artesp.utils.rodovias_kartado_param import carregar_rodoivas_extra_kartado_xlsx
        except ImportError:
            from utils.rodovias_kartado_param import carregar_rodoivas_extra_kartado_xlsx
        extra = carregar_rodoivas_extra_kartado_xlsx(path_xlsx)
        for k, v in extra.items():
            if k not in out:
                out[k] = v
    except Exception:
        pass
    return out


RODOVIAS: dict[str, dict] = _fusao_rodoivas_core_com_kartado_xlsx(_RODOVIAS_CORE)

# Mapa tag → nome curto para nome de arquivo (M01)
RODOVIA_NOME_SEPARAR: dict[str, str] = {
    "SP021":      "SP-021",
    "SP075":      "SP-075",
    "SP127":      "SP-127",
    "SP280":      "SP-280",
    "SP300":      "SP-300",
    "SPI102/300": "SPI-102/300",
    "FORA":       "Fora",
}

# ═══════════════════════════════════════════════════════════════════════════
# TIPOS DE SERVIÇO — abreviações para nome de arquivo
# ═══════════════════════════════════════════════════════════════════════════

SERVICO_ABREV: dict[str, str] = {
    # Pavimentação
    "Depressão ou recalque de pequena extensão":          "Pav - Depressao",
    "Afundamento de trilha de roda":                      "Pav - Afundamento",
    "Remendo profundo ou superficial":                    "Pav - Remendo",
    "Desgaste ou desagregação do revestimento":           "Pav - Desgaste",
    "Buraco ou panela":                                   "Pav - Panela",
    "Trincas":                                            "Pav - Trincas",
    "Irregularidade transversal":                         "Pav - Irregularidade",
    "Pavimentação/ Passeio/ Alambrado":                   "Pred - Pav Passeio Alam",
    # Defesas e dispositivos viários
    "Defensa metálica (manutenção ou substituição)":      "Reparo Defensa",
    "Placas (implantação ou substituição)":               "Sinal Vertical",
    "Pintura de solo":                                    "Sinal Horizontal",
    "Dispositivo de segurança":                           "Disp Seguranca",
    # Drenagem
    "Desobstrução de elemento de drenagem":               "Desobstrucao Drenagem",
    "Hidráulica/ Esgoto/ Drenagem":                       "Hidr Esg Dren",
    # Vegetação e Limpeza
    "Roçada":                                             "Rocada",
    "Capina":                                             "Capina",
    "Remoção de lixo e entulho da faixa de domínio":      "Limpeza FD",
    # Erosão e Taludes
    "Recomposição de erosão em corte / aterro":           "Eros Corte Aterro",
    "Escorregamento de taludes":                          "Taludes",
    "Deslizamento":                                       "Deslizamento",
    # Estruturas e OAE
    "Recuperação de OAE":                                 "Recup OAE",
    "Manutenção de OAE":                                  "Manut OAE",
    "Dispositivo com OAE":                                "Disp OAE",
    # Iluminação e Obras
    "Iluminação":                                         "Iluminacao",
    "Obras de Arte Especiais":                            "OAE",
    "Duplicação":                                         "Duplicacao",
    "Faixa Adicional":                                    "Faixa Adicional",
}

# ═══════════════════════════════════════════════════════════════════════════
# MAPA SERVIÇO → CLASSIFICAÇÃO KCOR
# ═══════════════════════════════════════════════════════════════════════════

# SERVICO_NC: serviço → (tipo_nc, classificação, executor)
# Usado pelo inserir_nc_kria.py (M03/M07)
SERVICO_NC: dict[str, tuple] = {
    k: ("Conservação Rotina", "Conservação Rotina", "Soluciona - Conserva")
    for k in SERVICO_ABREV
}
SERVICO_NC.update({
    "Recuperação de OAE": ("Obras",              "Obras",  "Soluciona - Obras"),
    "Manutenção de OAE":  ("Obras",              "Obras",  "Soluciona - Obras"),
    "Duplicação":         ("Obras",              "Obras",  "Soluciona - Obras"),
    "Faixa Adicional":    ("Obras",              "Obras",  "Soluciona - Obras"),
})

# ═══════════════════════════════════════════════════════════════════════════
# TIPO → PASTA DE DESTINO (M08)
# ═══════════════════════════════════════════════════════════════════════════

for _tipo, _abrev in SERVICO_ABREV.items():
    M08_TIPO_NOME_PASTA[_abrev] = _abrev

# ═══════════════════════════════════════════════════════════════════════════
# MAPA EAF — Grupos de fiscalização por trecho km (equipes por rodovia + km ini/fim)
#
# grupo   : número do grupo (coluna P da EAF)
# empresa : nome EAF (NEP, Autoroutes, EBP 22)
# trechos : lista de { rodovia, km_ini, km_fim } — cada equipe é responsável por esses trechos
# email   : (opcional) e-mail do responsável pelo apontamento desse grupo — preencher conforme
#           a imagem/planilha de contatos (e-mail de cada responsável e seu grupo EAF)
#
# Responsável Técnico por empresa (nome EAF). Chave = nome da empresa (igual a MAPA_EAF).
# Valores = nomes dos fiscais que aparecem nos PDFs, separados por ";" ou ",".
# Só zera grupo/empresa se o nome do fiscal estiver cadastrado em OUTRA EAF (conflito).
# Nome desconhecido (não está em nenhuma lista) mantém a empresa definida pelo trecho.
MAPA_RESPONSAVEL_TECNICO: dict[str, str] = {
    # Valores podem conter múltiplos responsáveis separados por ';' ou ','.
    # Isso permite validar o responsável técnico de forma correta mesmo quando
    # o PDF/Excel traz nomes individuais diferentes para a mesma EAF/grupo.
    "NEP": "Gabriel Miranda de Souza; Leticia Ferreira de Souza",
    "Autoroutes": "Ricardo Antonio Pacheco Machado Jr; Ricardo Walter",
    "EBP 22": "Rogerio Aguiar; Percival Gonçalves de Magalhães",
}

# EAF aceitas no relatório. Vazio = todas as empresas do MAPA_EAF aparecem.
# Preenchido = só as listadas (ex.: ("Autoroutes",) ou ("NEP", "Autoroutes", "EBP 22")).
# Se uma NC tiver empresa fora desta lista, grupo e empresa são zerados (trava lista branca).
EAF_PERMITIDAS: tuple[str, ...] = ()

# Lote 13 — Colinas (concessionária: Rodovias das Colinas). EAFs = fiscalizadoras por trecho.
# Trechos por EAF; rodovia + km definem a empresa no relatório. Conferir KMs conforme os PDFs.
# ═══════════════════════════════════════════════════════════════════════════

MAPA_EAF: list[dict] = [
    {
        "grupo": 1,
        "empresa": "NEP",
        "email": "",  # preencher com o e-mail do responsável do grupo 1 (ex.: responsavel.nep@empresa.com)
        "trechos": [
            {"rodovia": "SP 075", "km_ini": 43.000, "km_fim": 77.600},
        ],
    },
    {
        "grupo": 2,
        "empresa": "Autoroutes",
        "email": "",  # preencher com o e-mail do responsável do grupo 2
        "trechos": [
            {"rodovia": "SP 075",      "km_ini": 15.000, "km_fim":  43.000},
            {"rodovia": "SP 127",      "km_ini": 60.000, "km_fim": 105.900},
            {"rodovia": "SP 280",      "km_ini": 79.380, "km_fim": 129.600},
            {"rodovia": "SP 300",      "km_ini": 64.600, "km_fim": 103.000},
            {"rodovia": "SP 300",      "km_ini": 108.900, "km_fim": 158.650},
            {"rodovia": "SPI 102-300", "km_ini":  0.000, "km_fim":   7.900},
        ],
    },
    {
        "grupo": 11,
        "empresa": "EBP 22",
        "email": "",  # preencher com o e-mail do responsável do grupo 11
        "trechos": [
            {"rodovia": "SP 127", "km_ini":  0.000, "km_fim": 32.026},
            {"rodovia": "SP 127", "km_ini": 39.900, "km_fim": 60.000},
        ],
    },
]

# Por lote (13, 21, 26): EAFs e responsáveis podem ser outros. Lote 13 = mapa acima (já em uso).
# Preencher "21" e "26" quando houver dados (planilhas Excel de cada trecho). Fallback = Lote 13.
# Lote 21 — Rodovias do Tietê (trechos fiscalizados). SP 300: Autoroutes G2 (158+650–240+999) e MMG (241+000–336+500).
def _trechos_lote21_nep() -> list:
    r = []
    for rod in (
        "SP 101",
        "SP 113",
        "SP 308",
        "SPA 022/101",
        "SPA 026/101",
        "SPA 032/101",
        "SPA 043/101",
        "SPA 051/101",
        "SPA 139/308",
        "SPA 155/308",
        "SPI 162/308",
        "CPR 010/308",
        "CPR 152/101",
        "ESF 020/101",
        "HRT 050/101",
        "IDT 085/101",
        "MOR 040/101",
        "MOR 137/101",
        "MOR 293/101",
        "PFZ 080/101",
        "PIR 030/308",
        "RFR 154/101",
        "RPD 015/308",
        "RPD 020/308",
    ):
        r.append({"rodovia": rod, "km_ini": 0.0, "km_fim": 9999.0})
    return r


def _trechos_lote21_autoroutes_g2() -> list:
    r = [
        {"rodovia": "SP 300", "km_ini": 158.650, "km_fim": 240.999},
    ]
    for rod in (
        "SPA 159/300",
        "SPA 172/300",
        "SPA 176/300",
        "SPA 193/300",
        "SPA 196/300",
        "SPI 181/300",
        "AHB 146/300",
        "CHS 326/300",
        "CHS 387/300",
        "LRP 321/300",
        "TIT 366/113",
    ):
        r.append({"rodovia": rod, "km_ini": 0.0, "km_fim": 9999.0})
    return r


def _trechos_lote21_mmg() -> list:
    r = [
        {"rodovia": "SP 209", "km_ini": 0.0, "km_fim": 9999.0},
        {"rodovia": "SP 300", "km_ini": 241.000, "km_fim": 336.500},
    ]
    for rod in (
        "SPA 007/209",
        "SPA 231/300",
        "SPA 251/300",
        "SPA 270/300",
        "SPA 283/300",
        "SPA 241/300",
        "BRE 005/300",
        "BRE 232/300",
        "BTC 055/300",
        "BTC 260/209",
        "BTC 353/300",
        "BTC 040/209",
        "ITN 313/209",
        "LEP 030/300",
        "LEP 119/300",
        "LEP 148/300",
        "LEP 321/300",
        "LEP 347/300",
        "LEP 357/300",
        "LEP 363/300",
        "LEP 374/300",
        "MTB 070/300",
        "MTB 148/300",
        "MTB 195/300",
        "PRD 010/300",
        "SMN 040/300",
        "SMN 373/300",
    ):
        r.append({"rodovia": rod, "km_ini": 0.0, "km_fim": 9999.0})
    return r


MAPA_EAF_POR_LOTE: dict[str, list] = {
    "13": MAPA_EAF,
    "21": [
        {
            "grupo": 2,
            "empresa": "NEP",
            "email": "",
            "trechos": _trechos_lote21_nep(),
        },
        {
            "grupo": 3,
            "empresa": "Autoroutes G2",
            "email": "",
            "trechos": _trechos_lote21_autoroutes_g2(),
        },
        {
            "grupo": 3,
            "empresa": "MMG",
            "email": "",
            "trechos": _trechos_lote21_mmg(),
        },
    ],
    "26": [],  # preencher trechos/EAFs do Lote 26 quando houver
}
MAPA_RESPONSAVEL_TECNICO_POR_LOTE: dict[str, dict] = {
    "13": MAPA_RESPONSAVEL_TECNICO,
    "21": {
        "NEP": "Vinicius Francalassi Nalesso",
        "Autoroutes G2": "Ricardo Antonio Pacheco Machado Jr",
        "MMG": "Guilherme Macedo",
    },
    "26": {},
}


def get_mapa_eaf(lote: str) -> list:
    num = (lote or "").strip()
    if not num:
        return MAPA_EAF
    if num == "50":
        try:
            from nc_artemig import config as cfg_artemig
            return cfg_artemig.MAPA_EAF_POR_LOTE.get("50") or []
        except ImportError:
            return []
    return MAPA_EAF_POR_LOTE.get(num) or MAPA_EAF


def get_mapa_responsavel_tecnico(lote: str) -> dict:
    num = (lote or "").strip()
    if not num:
        return MAPA_RESPONSAVEL_TECNICO
    if num == "50":
        try:
            from nc_artemig import config as cfg_artemig
            return cfg_artemig.MAPA_RESPONSAVEL_TECNICO_POR_LOTE.get("50") or {}
        except ImportError:
            return {}
    return MAPA_RESPONSAVEL_TECNICO_POR_LOTE.get(num) or MAPA_RESPONSAVEL_TECNICO


def lote_eh_kartado_artesp(lote: str) -> bool:
    return (lote or "").strip() in LOTES_KARTADO_ARTESP
