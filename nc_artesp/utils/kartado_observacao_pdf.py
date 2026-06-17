"""
Regras de extração do campo «Observação» do PDF e de inserção no Excel Kartado consolidado
(Template - Geral - 4 e 5 - Final.xlsx):

**Coluna Y** («Localização Tipo») — só estes léxicos (e aliases ortográficos no PDF):
Alça Desaceleração, Pista Principal, Alça Aceleração, Alça Interna Dispositivo, Rotatória,
Viaduto, Ponte, Passarela, Túnel, Pista AVI, Pista Manual, Canteiro Central, Canteiro Lateral, Outros.

**Coluna X** («Localização Pista») — só estes léxicos (e aliases):
Refúgio, Faixa 01–05, Acostamento, Pista Principal, Marginal, Trevo, Acesso Terceiro,
Fora de Plataforma, Pedágio, Balança, Prédio/Pátio.

**Coluna AA** («Observações») — texto livre do PDF **e** qualquer troço que **não** seja
reconhecido como léxico X ou Y (após retirar os intervalos classificados para X/Y).
Exemplos que ficam na AA: galhos/massa seca, drenagem fora de plataforma (quando não for
só o rótulo «Fora de Plataforma» de pista), afundamento do passeio, próximo a tampa de esgoto,
mureta danificada, bambu com projeção / risco de queda, etc.

**Exceção:** «Fora de Plataforma» (pista) não conta se o token imediatamente anterior for
drenagem/água/esgoto/lixo/entulho (evita falso positivo em «Drenagem fora de plataforma»).

Deteção: frase com limite de palavra; padrões mais longos primeiro; empate Tipo vs Pista
de igual comprimento favorece **Y**.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

_COL_PISTA = "pista"
_COL_TIPO = "tipo"


def _sem_acentos(s: str) -> str:
    t = unicodedata.normalize("NFD", s or "")
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def _frase_regex(phrase: str) -> str:
    s = (phrase or "").strip()
    if not s:
        return ""
    partes = [p for p in re.split(r"\s+", s) if p]
    if not partes:
        return ""
    esc = [re.escape(p) for p in partes]
    nucleo = r"\s+".join(esc)
    return r"(?<![\w/])" + nucleo + r"(?![\w/])"


def _compilar_regras(
    col: str,
    pares: list[tuple[str, tuple[str, ...]]],
) -> list[tuple[str, str, re.Pattern[str]]]:
    out: list[tuple[str, str, re.Pattern[str]]] = []
    for canon, aliases in pares:
        alts = (canon,) + aliases
        vistos_rx: set[str] = set()
        pats: list[str] = []
        for a in alts:
            if not (a or "").strip():
                continue
            rx = _frase_regex(a)
            if not rx or rx in vistos_rx:
                continue
            vistos_rx.add(rx)
            pats.append(rx)
        if not pats:
            continue
        flags = re.IGNORECASE | re.UNICODE
        out.append((col, canon, re.compile("(?:" + "|".join(pats) + ")", flags)))
    return out


_LOCALIZACAO_TIPO: list[tuple[str, tuple[str, ...]]] = [
    (
        "Alça Desaceleração",
        (
            "Alca Desaceleração",
            "Alça Desaceleracao",
            "Alca Desaceleracao",
        ),
    ),
    ("Pista Principal", ()),
    (
        "Alça Aceleração",
        (
            "Alça Aceleracao",
            "Alca Aceleração",
            "Alca Aceleracao",
        ),
    ),
    ("Alça Interna Dispositivo", ("Alca Interna Dispositivo",)),
    ("Rotatória", ("Rotatoria",)),
    ("Viaduto", ()),
    ("Ponte", ()),
    ("Passarela", ()),
    ("Túnel", ("Tunel",)),
    ("Pista AVI", ()),
    ("Pista Manual", ()),
    ("Canteiro Central", ()),
    ("Canteiro Lateral", ()),
    ("Outros", ()),
]

_LOCALIZACAO_PISTA: list[tuple[str, tuple[str, ...]]] = [
    ("Refúgio", ("Refugio",)),
    ("Faixa 01", ("Faixa 1",)),
    ("Faixa 02", ("Faixa 2",)),
    ("Faixa 03", ("Faixa 3",)),
    ("Faixa 04", ("Faixa 4",)),
    ("Faixa 05", ("Faixa 5",)),
    ("Acostamento", ()),
    ("Pista Principal", ()),
    ("Marginal", ()),
    ("Trevo", ()),
    ("Acesso Terceiro", ()),
    ("Fora de Plataforma", ("Fora de plataforma",)),
    ("Pedágio", ("Pedagio",)),
    ("Balança", ("Balanca",)),
    (
        "Prédio/Pátio",
        (
            "Prédio/Patio",
            "Predio/Patio",
            "Prédio / Pátio",
            "Predio/Pátio",
        ),
    ),
]


def _regras_ordenadas() -> list[tuple[str, str, re.Pattern[str], int, int]]:
    tipo = _compilar_regras(_COL_TIPO, _LOCALIZACAO_TIPO)
    pista = _compilar_regras(_COL_PISTA, _LOCALIZACAO_PISTA)
    todas: list[tuple[str, str, re.Pattern[str], int, int]] = []
    for col, canon, pat in tipo:
        todas.append((col, canon, pat, len(pat.pattern), 0))
    for col, canon, pat in pista:
        todas.append((col, canon, pat, len(pat.pattern), 1))
    todas.sort(key=lambda x: (-x[3], x[4]))
    return todas


_REGRAS_CACHE: list[tuple[str, str, re.Pattern[str], int, int]] | None = None


def _regras() -> list[tuple[str, str, re.Pattern[str], int, int]]:
    global _REGRAS_CACHE
    if _REGRAS_CACHE is None:
        _REGRAS_CACHE = _regras_ordenadas()
    return _REGRAS_CACHE


def _sobrepoem(a0: int, a1: int, b0: int, b1: int) -> bool:
    return not (a1 <= b0 or b1 <= a0)


_FORA_PLATA_PRECEDENTES_INVALIDOS = frozenset(
    {
        "drenagem",
        "água",
        "agua",
        "escoamento",
        "escoamentos",
        "esgoto",
        "efluente",
        "lixo",
        "entulho",
    }
)


def _fora_de_plataforma_valido(bruto: str, start: int) -> bool:
    if start <= 0:
        return True
    prefix = bruto[:start].rstrip()
    toks = re.findall(r"[\wÀ-ÿ]+", prefix, re.I)
    if not toks:
        return True
    return toks[-1].casefold() not in _FORA_PLATA_PRECEDENTES_INVALIDOS


@dataclass(frozen=True)
class RotagemObservacaoKartado:
    texto_livre_observacoes: str
    localizacao_pista_x: str
    localizacao_tipo_y: str


def _texto_para_observacoes_aa_por_spans(
    bruto: str, ocupados: list[tuple[int, int, str, str]]
) -> str:
    if not ocupados:
        return re.sub(r"\s+", " ", (bruto or "").strip()).strip()
    spans = sorted((s, e) for s, e, _, _ in ocupados)
    partes: list[str] = []
    cur = 0
    for s, e in spans:
        s = max(int(s), cur)
        if cur < s:
            chunk = bruto[cur:s]
            if chunk.strip():
                partes.append(chunk.strip())
        cur = max(cur, int(e))
    if cur < len(bruto):
        tail = bruto[cur:]
        if tail.strip():
            partes.append(tail.strip())
    liv = " ".join(partes)
    liv = re.sub(r"\s+", " ", liv).strip().strip(",;.")
    return liv


def texto_observacoes_aa_para_excel(s: str) -> str:
    """Vazio se o texto for só separadores (evita «: | :» na coluna AA do consolidado)."""
    t = re.sub(r"\s+", " ", (s or "").strip()).strip().strip(",;.")
    if not t or re.fullmatch(r"[\s:;|,.:-]+", t):
        return ""
    return t


def rotear_observacao_pdf_para_kartado(obs: str) -> RotagemObservacaoKartado:
    """Léxicos Y e X no texto; o restante (incl. exemplos de texto livre do PDF) → ``texto_livre_observacoes`` / coluna AA."""
    bruto = (obs or "").strip()
    if not bruto:
        return RotagemObservacaoKartado("", "", "")

    ocupados: list[tuple[int, int, str, str]] = []
    for col, canon, pat, _, _ in _regras():
        for m in pat.finditer(bruto):
            s, e = m.start(), m.end()
            if canon == "Fora de Plataforma" and not _fora_de_plataforma_valido(bruto, s):
                continue
            if any(_sobrepoem(s, e, a, b) for a, b, _, _ in ocupados):
                continue
            ocupados.append((s, e, col, canon))

    ocupados.sort(key=lambda x: x[0])
    livre = texto_observacoes_aa_para_excel(_texto_para_observacoes_aa_por_spans(bruto, ocupados))

    pist = [c for _, _, col, c in ocupados if col == _COL_PISTA]
    tipos = [c for _, _, col, c in ocupados if col == _COL_TIPO]

    def _join_unicos(seq: list[str]) -> str:
        vistos: set[str] = set()
        out: list[str] = []
        for x in seq:
            k = x.casefold()
            if k in vistos:
                continue
            vistos.add(k)
            out.append(x)
        return " | ".join(out)

    return RotagemObservacaoKartado(
        texto_livre_observacoes=livre[:32000],
        localizacao_pista_x=_join_unicos(pist)[:500],
        localizacao_tipo_y=_join_unicos(tipos)[:500],
    )


def normalizar_observacao_extraida_pdf(s: str) -> str:
    """Pós-processamento do texto bruto do campo Observação no PDF (uma linha lógica)."""
    t = (s or "").replace("\r\n", "\n").replace("\r", "\n")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n+", " ", t)
    return t.strip()
