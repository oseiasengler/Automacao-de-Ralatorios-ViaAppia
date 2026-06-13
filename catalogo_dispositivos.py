"""
Catálogo unificado de activos de concessões rodoviárias — fonte única da verdade.

Define a taxonomia e o schema de atributos específicos de cada tipo.
Este módulo dirige:
  - a validação no backend (valida_atributos)
  - o formulário dinâmico no PWA (export_catalogo_js / catalogo.json)

Padrão de dados: núcleo comum (em models.py) + atributos específicos (JSONB),
validados aqui pelo tipo do dispositivo.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any
import json


class Grupo(str, Enum):
    SEGURANCA    = "seguranca"
    DRENAGEM     = "drenagem"
    OAE          = "oae"
    ITS          = "its"
    EDIFICACOES  = "edificacoes"
    FAIXA        = "faixa_dominio"


class Categoria(str, Enum):
    # drenagem (sub-categorias históricas mantidas)
    SUPERFICIAL  = "superficial"
    PROFUNDA     = "profunda"
    TRANSVERSAL  = "transversal"
    # novos grupos (categoria == grupo para tipos não-drenagem)
    SEGURANCA    = "seguranca"
    OAE          = "oae"
    ITS          = "its"
    EDIFICACOES  = "edificacoes"
    FAIXA        = "faixa_dominio"


class Geometria(str, Enum):
    LINEAR  = "linear"
    PONTUAL = "pontual"


class TipoCampo(str, Enum):
    NUMERO = "numero"
    TEXTO  = "texto"
    ENUM   = "enum"
    BOOL   = "bool"


@dataclass
class Campo:
    nome: str
    rotulo: str
    tipo: TipoCampo
    obrigatorio: bool = False
    unidade: str | None = None
    opcoes: list[str] = field(default_factory=list)
    minimo: float | None = None
    maximo: float | None = None
    ajuda: str | None = None
    depende_de: str | None = None
    depende_valor: str | None = None


@dataclass
class TipoDispositivo:
    tipo: str
    rotulo: str
    categoria: Categoria
    geometria: Geometria
    grupo: Grupo
    atributos: list[Campo] = field(default_factory=list)


# ---------------------------------------------------------------------------
# METADADOS DOS GRUPOS (exportados para o PWA)
# ---------------------------------------------------------------------------
GRUPOS_META: dict[str, dict[str, str]] = {
    "seguranca":     {"rotulo": "Segurança e Sinalização",    "icone": "🛡️"},
    "drenagem":      {"rotulo": "Sistema de Drenagem",         "icone": "💧"},
    "oae":           {"rotulo": "Obras de Arte Especiais",     "icone": "🌉"},
    "its":           {"rotulo": "Sistemas e Tecnologia (ITS)", "icone": "📡"},
    "edificacoes":   {"rotulo": "Edificações e Serviços",      "icone": "🏢"},
    "faixa_dominio": {"rotulo": "Faixa de Domínio e Apoio",   "icone": "🌱"},
}


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def _c(nome: str, rotulo: str, tipo: TipoCampo, **kw: Any) -> Campo:
    return Campo(nome=nome, rotulo=rotulo, tipo=tipo, **kw)


# Listas de opções reutilizadas — drenagem
MAT_REVEST = ["concreto", "grama", "solo", "pead", "alvenaria", "pedra_argamassada"]
MAT_TUBO   = ["concreto", "pead", "pvc", "metalico"]
SECOES     = ["triangular", "trapezoidal", "retangular", "meia_cana"]

# OAE: schema completo partilhado por todos os tipos de obra de arte especial
OAE_ATRIBUTOS: list[Campo] = [
    _c("tipo_oae", "Tipo de OAE", TipoCampo.ENUM,
       opcoes=["ponte", "viaduto", "passarela",
               "passagem_superior", "passagem_inferior",
               "passagem_gado", "galeria"],
       ajuda="Discriminador do tipo de obra de arte"),
    _c("qtd_vaos", "Qtd. de vãos", TipoCampo.NUMERO, minimo=1),
    _c("comprimento_m", "Comprimento total", TipoCampo.NUMERO, unidade="m", minimo=0),
    _c("largura_m", "Largura", TipoCampo.NUMERO, unidade="m", minimo=0),
    _c("vao_livre_m", "Vão livre", TipoCampo.NUMERO, unidade="m", minimo=0),
    _c("gabarito_vertical_m", "Gabarito vertical", TipoCampo.NUMERO, unidade="m", minimo=0),
    _c("gabarito_horizontal_m", "Gabarito horizontal", TipoCampo.NUMERO, unidade="m", minimo=0),
    _c("tabuleiro_tipo", "Tipo de tabuleiro", TipoCampo.TEXTO),
    _c("tipologia_vaos", "Tipologia dos vãos", TipoCampo.TEXTO),
    _c("inclinacao_rampas", "Inclinação das rampas", TipoCampo.TEXTO),
    _c("telamento", "Telamento?", TipoCampo.BOOL),
    _c("iluminacao", "Iluminação?", TipoCampo.BOOL),
    _c("dispositivo_contencao", "Dispositivo de contenção", TipoCampo.TEXTO),
    _c("trem_tipo", "Trem tipo", TipoCampo.TEXTO),
    _c("status_oae", "Status da OAE", TipoCampo.ENUM,
       opcoes=["em_operacao", "interditado", "em_obras", "demolido"]),
    _c("data_implantacao", "Data de implantação", TipoCampo.TEXTO),
    _c("municipio", "Município", TipoCampo.TEXTO),
    _c("calcamento", "Calçamento", TipoCampo.TEXTO),
    _c("escada", "Escada de acesso?", TipoCampo.BOOL),
]

# ITS: campos comuns a equipamentos tecnológicos
ITS_ATRIBUTOS_BASE: list[Campo] = [
    _c("registro_artesp", "Registro ARTESP", TipoCampo.TEXTO),
    _c("grupo_componente", "Grupo componente", TipoCampo.TEXTO),
    _c("tipo_componente", "Tipo componente", TipoCampo.TEXTO),
    _c("marca", "Marca", TipoCampo.TEXTO),
    _c("modelo", "Modelo", TipoCampo.TEXTO),
]


# ---------------------------------------------------------------------------
# CATÁLOGO
# ---------------------------------------------------------------------------
CATALOGO: list[TipoDispositivo] = [

    # ══════════════════════════════════════════════════════════════════════
    # SEGURANÇA E SINALIZAÇÃO
    # ══════════════════════════════════════════════════════════════════════
    TipoDispositivo(
        "alambrado", "Alambrado", Categoria.SEGURANCA, Geometria.LINEAR, Grupo.SEGURANCA,
        [
            _c("tipo_poste", "Tipo de poste", TipoCampo.ENUM,
               opcoes=["concreto", "metalico", "madeira", "misto"]),
            _c("espacamento_poste_m", "Espaçamento entre postes", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("altura_poste_m", "Altura do poste", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("tipo_tela", "Tipo de tela", TipoCampo.ENUM,
               opcoes=["hexagonal", "soldada", "rolo_simples", "outro"]),
            _c("altura_tela_m", "Altura da tela", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("abertura_tela_cm", "Abertura da tela", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("extensao_m", "Extensão do tramo", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("qtd_postes", "Qtd. postes no tramo", TipoCampo.NUMERO, minimo=0),
        ],
    ),
    TipoDispositivo(
        "balizador", "Balizadores", Categoria.SEGURANCA, Geometria.LINEAR, Grupo.SEGURANCA,
        [
            _c("tipo_balizador", "Tipo de balizador", TipoCampo.ENUM,
               opcoes=["cilindrico", "plastico_flexivel", "borracha", "concreto", "outro"]),
            _c("refletivo", "Refletivo?", TipoCampo.BOOL),
            _c("tamanho_refletivo", "Tamanho do refletivo", TipoCampo.TEXTO),
            _c("largura_cm", "Largura", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("altura_cm", "Altura além do solo", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("cadencia_m", "Cadência (espaçamento)", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("extensao_m", "Extensão do tramo", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("qtd_balizadores", "Qtd. balizadores", TipoCampo.NUMERO, minimo=0),
        ],
    ),
    TipoDispositivo(
        "barreira_concreto", "Barreira de Concreto", Categoria.SEGURANCA, Geometria.LINEAR, Grupo.SEGURANCA,
        [
            _c("tipo_barreira", "Tipo de barreira", TipoCampo.ENUM,
               opcoes=["new_jersey", "f_shape", "blocos_interligados", "outro"]),
            _c("com_armadura", "Com armadura?", TipoCampo.BOOL),
            _c("tipo_entrada", "Tipo de entrada", TipoCampo.TEXTO),
            _c("tipo_saida", "Tipo de saída", TipoCampo.TEXTO),
            _c("comprimento_m", "Comprimento", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("altura_total_cm", "Altura total", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("altura_alma_cm", "Altura da alma", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("altura_espelho_cm", "Altura do espelho", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("largura_base_cm", "Largura da base", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("largura_topo_cm", "Largura do topo", TipoCampo.NUMERO, unidade="cm", minimo=0),
        ],
    ),
    TipoDispositivo(
        "cerca", "Cerca", Categoria.SEGURANCA, Geometria.LINEAR, Grupo.SEGURANCA,
        [
            _c("tipo_mourao", "Tipo de mourão", TipoCampo.ENUM,
               opcoes=["concreto", "metalico", "madeira", "misto"]),
            _c("espacamento_mourao_m", "Espaçamento entre mourões", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("altura_mourao_m", "Altura do mourão", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("tipo_arame", "Tipo de arame", TipoCampo.ENUM,
               opcoes=["liso", "farpado", "tela", "misto"]),
            _c("qtd_fios", "Quantidade de fios", TipoCampo.NUMERO, minimo=0),
            _c("extensao_m", "Extensão do tramo", TipoCampo.NUMERO, unidade="m", minimo=0),
        ],
    ),
    TipoDispositivo(
        "defensa_metalica", "Defensa Metálica", Categoria.SEGURANCA, Geometria.LINEAR, Grupo.SEGURANCA,
        [
            _c("tipo_defensa", "Tipo de defensa", TipoCampo.ENUM,
               opcoes=["simples", "dupla", "rigida", "semirigida", "flexivel"]),
            _c("marca", "Marca", TipoCampo.TEXTO),
            _c("modelo", "Modelo", TipoCampo.TEXTO),
            _c("tipo_entrada", "Tipo de entrada", TipoCampo.TEXTO),
            _c("tipo_saida", "Tipo de saída", TipoCampo.TEXTO),
            _c("altura_mm", "Altura/Espessura", TipoCampo.NUMERO, unidade="mm", minimo=0),
            _c("espaco_postes_m", "Espaço entre postes", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("comprimento_m", "Comprimento do tramo", TipoCampo.NUMERO, unidade="m", minimo=0),
        ],
    ),
    TipoDispositivo(
        "sinalizacao_marcas", "Sinalização Horiz. — Marcas Viárias", Categoria.SEGURANCA, Geometria.LINEAR, Grupo.SEGURANCA,
        [
            _c("tipo_marca", "Tipo de marca", TipoCampo.ENUM,
               opcoes=["linha_simples", "linha_dupla", "linha_contínua",
                       "linha_tracejada", "chevron", "outra"]),
            _c("cor", "Cor", TipoCampo.ENUM, opcoes=["amarela", "branca", "vermelha"]),
            _c("material", "Material", TipoCampo.ENUM,
               opcoes=["tinta", "termoplastico", "plastico_frio", "epoxy"]),
            _c("largura_cm", "Largura", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("extensao_m", "Extensão", TipoCampo.NUMERO, unidade="m", minimo=0),
        ],
    ),
    TipoDispositivo(
        "sinalizacao_zebrado", "Sinalização Horiz. — Zebrado", Categoria.SEGURANCA, Geometria.PONTUAL, Grupo.SEGURANCA,
        [
            _c("tipo_zebrado", "Tipo", TipoCampo.ENUM,
               opcoes=["faixa_pedestres", "cruzamento_bicicleta", "zebrado_bloqueio", "outro"]),
            _c("material", "Material", TipoCampo.ENUM,
               opcoes=["tinta", "termoplastico", "plastico_frio", "epoxy"]),
            _c("area_m2", "Área", TipoCampo.NUMERO, unidade="m²", minimo=0),
        ],
    ),
    TipoDispositivo(
        "sinalizacao_tacha", "Sinalização Horiz. — Tacha Longitudinal", Categoria.SEGURANCA, Geometria.LINEAR, Grupo.SEGURANCA,
        [
            _c("tipo_tacha", "Tipo de tacha", TipoCampo.ENUM,
               opcoes=["refletiva", "nao_refletiva", "led", "outro"]),
            _c("cor", "Cor", TipoCampo.ENUM, opcoes=["amarela", "branca", "vermelha"]),
            _c("espacamento_m", "Espaçamento", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("extensao_m", "Extensão do tramo", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("qtd_tachas", "Qtd. tachas", TipoCampo.NUMERO, minimo=0),
        ],
    ),
    TipoDispositivo(
        "sinalizacao_vertical", "Sinalização Vertical", Categoria.SEGURANCA, Geometria.PONTUAL, Grupo.SEGURANCA,
        [
            _c("codigo_nbr", "Código NBR", TipoCampo.TEXTO,
               ajuda="Ex: R-1, A-1b, IE-1"),
            _c("tipo_placa", "Tipo de placa", TipoCampo.ENUM,
               opcoes=["regulamentacao", "advertencia", "indicacao",
                       "educativa", "obra", "outra"]),
            _c("dimensao_cm", "Dimensão (diâm./lado)", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("material_placa", "Material", TipoCampo.ENUM,
               opcoes=["aco_galvanizado", "aluminio", "polietileno", "outro"]),
            _c("tipo_suporte", "Tipo de suporte", TipoCampo.ENUM,
               opcoes=["coluna_simples", "coluna_dupla", "portico", "semipórtico",
                       "muro", "parede", "outro"]),
            _c("altura_suporte_m", "Altura do suporte", TipoCampo.NUMERO, unidade="m", minimo=0),
        ],
    ),
    TipoDispositivo(
        "transicao", "Transição", Categoria.SEGURANCA, Geometria.PONTUAL, Grupo.SEGURANCA,
        [
            _c("tipo_entrada", "Tipo de dispositivo de entrada", TipoCampo.TEXTO),
            _c("tipo_saida", "Tipo de dispositivo de saída", TipoCampo.TEXTO),
            _c("comprimento_m", "Comprimento", TipoCampo.NUMERO, unidade="m", minimo=0),
        ],
    ),

    # ══════════════════════════════════════════════════════════════════════
    # DRENAGEM SUPERFICIAL
    # ══════════════════════════════════════════════════════════════════════
    TipoDispositivo(
        "canaleta", "Canaleta", Categoria.SUPERFICIAL, Geometria.LINEAR, Grupo.DRENAGEM,
        [
            _c("secao", "Seção", TipoCampo.ENUM, obrigatorio=True, opcoes=SECOES),
            _c("material", "Material", TipoCampo.ENUM, obrigatorio=True, opcoes=MAT_REVEST),
            _c("largura_cm", "Largura", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("altura_cm", "Altura", TipoCampo.NUMERO, unidade="cm", minimo=0),
        ],
    ),
    TipoDispositivo(
        "sarjeta", "Sarjeta", Categoria.SUPERFICIAL, Geometria.LINEAR, Grupo.DRENAGEM,
        [
            _c("posicao", "Posição", TipoCampo.ENUM, obrigatorio=True,
               opcoes=["corte", "aterro", "canteiro_central"]),
            _c("secao", "Seção", TipoCampo.ENUM, opcoes=SECOES),
            _c("material", "Material", TipoCampo.ENUM, opcoes=MAT_REVEST),
            _c("largura_cm", "Largura", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("altura_cm", "Altura", TipoCampo.NUMERO, unidade="cm", minimo=0),
        ],
    ),
    TipoDispositivo(
        "valeta_protecao", "Valeta de proteção", Categoria.SUPERFICIAL, Geometria.LINEAR, Grupo.DRENAGEM,
        [
            _c("posicao", "Posição", TipoCampo.ENUM, obrigatorio=True,
               opcoes=["crista_corte", "pe_aterro", "banqueta"]),
            _c("secao", "Seção", TipoCampo.ENUM, opcoes=SECOES),
            _c("material", "Material", TipoCampo.ENUM, opcoes=MAT_REVEST),
            _c("largura_cm", "Largura", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("profundidade_cm", "Profundidade", TipoCampo.NUMERO, unidade="cm", minimo=0),
        ],
    ),
    TipoDispositivo(
        "meio_fio", "Meio-fio", Categoria.SUPERFICIAL, Geometria.LINEAR, Grupo.DRENAGEM,
        [
            _c("tipo_mf", "Tipo", TipoCampo.ENUM, opcoes=["simples", "conjugado_sarjeta"]),
            _c("material", "Material", TipoCampo.ENUM, opcoes=["concreto", "pre_moldado"]),
            _c("altura_cm", "Altura", TipoCampo.NUMERO, unidade="cm", minimo=0),
        ],
    ),
    TipoDispositivo(
        "descida_dagua", "Descida d'água / Escada hidráulica", Categoria.SUPERFICIAL, Geometria.LINEAR, Grupo.DRENAGEM,
        [
            _c("tipo_descida", "Tipo", TipoCampo.ENUM, obrigatorio=True,
               opcoes=["rapida", "degraus"],
               ajuda="'degraus' = escada hidráulica"),
            _c("material", "Material", TipoCampo.ENUM, opcoes=["concreto", "pre_moldado", "alvenaria"]),
            _c("largura_cm", "Largura", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("n_degraus", "Nº de degraus", TipoCampo.NUMERO, minimo=1, obrigatorio=True,
               depende_de="tipo_descida", depende_valor="degraus"),
            _c("altura_espelho_cm", "Altura do espelho", TipoCampo.NUMERO, unidade="cm", minimo=0,
               depende_de="tipo_descida", depende_valor="degraus"),
            _c("tem_dissipador_saida", "Dissipador na saída?", TipoCampo.BOOL),
        ],
    ),
    TipoDispositivo(
        "dissipador_energia", "Dissipador de energia", Categoria.SUPERFICIAL, Geometria.PONTUAL, Grupo.DRENAGEM,
        [
            _c("tipo_dissipador", "Tipo", TipoCampo.ENUM, obrigatorio=True,
               opcoes=["bacia", "enrocamento", "blocos", "escalonado"]),
            _c("comprimento_cm", "Comprimento", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("largura_cm", "Largura", TipoCampo.NUMERO, unidade="cm", minimo=0),
        ],
    ),
    TipoDispositivo(
        "caixa_coletora", "Caixa coletora / ligação", Categoria.SUPERFICIAL, Geometria.PONTUAL, Grupo.DRENAGEM,
        [
            _c("funcao", "Função", TipoCampo.ENUM,
               opcoes=["coletora", "ligacao", "passagem"]),
            _c("largura_cm", "Largura", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("comprimento_cm", "Comprimento", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("profundidade_cm", "Profundidade", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("tem_grelha", "Tem grelha?", TipoCampo.BOOL),
        ],
    ),
    TipoDispositivo(
        "saida_dagua", "Saída/entrada d'água", Categoria.SUPERFICIAL, Geometria.PONTUAL, Grupo.DRENAGEM,
        [
            _c("funcao", "Função", TipoCampo.ENUM, opcoes=["saida", "entrada"]),
            _c("material", "Material", TipoCampo.ENUM, opcoes=["concreto", "alvenaria"]),
            _c("largura_cm", "Largura", TipoCampo.NUMERO, unidade="cm", minimo=0),
        ],
    ),

    # ══════════════════════════════════════════════════════════════════════
    # DRENAGEM PROFUNDA
    # ══════════════════════════════════════════════════════════════════════
    TipoDispositivo(
        "dreno_longitudinal", "Dreno longitudinal", Categoria.PROFUNDA, Geometria.LINEAR, Grupo.DRENAGEM,
        [
            _c("classe", "Classe", TipoCampo.ENUM, opcoes=["profundo", "raso_pavimento"]),
            _c("diametro_tubo_mm", "Ø tubo", TipoCampo.NUMERO, unidade="mm", minimo=0),
            _c("material_tubo", "Material do tubo", TipoCampo.ENUM, opcoes=MAT_TUBO),
            _c("profundidade_cm", "Profundidade", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("material_filtrante", "Material filtrante", TipoCampo.ENUM,
               opcoes=["brita", "areia", "geotextil", "misto"]),
        ],
    ),
    TipoDispositivo(
        "espinha_peixe", "Dreno espinha-de-peixe", Categoria.PROFUNDA, Geometria.LINEAR, Grupo.DRENAGEM,
        [
            _c("diametro_tubo_mm", "Ø tubo", TipoCampo.NUMERO, unidade="mm", minimo=0),
            _c("profundidade_cm", "Profundidade", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("espacamento_m", "Espaçamento entre ramos", TipoCampo.NUMERO, unidade="m", minimo=0),
        ],
    ),
    TipoDispositivo(
        "dhp", "Dreno sub-horizontal (DHP)", Categoria.PROFUNDA, Geometria.PONTUAL, Grupo.DRENAGEM,
        [
            _c("diametro_mm", "Ø", TipoCampo.NUMERO, unidade="mm", minimo=0),
            _c("comprimento_m", "Comprimento", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("inclinacao_graus", "Inclinação", TipoCampo.NUMERO, unidade="°"),
        ],
    ),
    TipoDispositivo(
        "colchao_drenante", "Colchão drenante", Categoria.PROFUNDA, Geometria.LINEAR, Grupo.DRENAGEM,
        [
            _c("espessura_cm", "Espessura", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("material", "Material", TipoCampo.ENUM, opcoes=["brita", "areia", "misto"]),
        ],
    ),

    # ══════════════════════════════════════════════════════════════════════
    # DRENAGEM TRANSVERSAL (bueiros)
    # ══════════════════════════════════════════════════════════════════════
    TipoDispositivo(
        "bueiro_tubular", "Bueiro tubular (BSTC/BDTC/BTTC)", Categoria.TRANSVERSAL, Geometria.PONTUAL, Grupo.DRENAGEM,
        [
            _c("n_linhas", "Nº de linhas", TipoCampo.ENUM, obrigatorio=True,
               opcoes=["1", "2", "3"], ajuda="1=simples, 2=duplo, 3=triplo"),
            _c("diametro_mm", "Ø", TipoCampo.NUMERO, obrigatorio=True, unidade="mm", minimo=0),
            _c("material", "Material", TipoCampo.ENUM, opcoes=["concreto", "metalico", "pead"]),
            _c("tem_ala", "Tem ala (asa)?", TipoCampo.BOOL),
            _c("tem_dissipador_saida", "Dissipador na saída?", TipoCampo.BOOL),
            _c("obstrucao_pct", "Obstrução da seção", TipoCampo.NUMERO, unidade="%", minimo=0, maximo=100),
        ],
    ),
    TipoDispositivo(
        "bueiro_celular", "Bueiro celular (BSCC/BDCC)", Categoria.TRANSVERSAL, Geometria.PONTUAL, Grupo.DRENAGEM,
        [
            _c("n_celulas", "Nº de células", TipoCampo.ENUM, opcoes=["1", "2", "3"]),
            _c("largura_cm", "Largura", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("altura_cm", "Altura", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("material", "Material", TipoCampo.ENUM, opcoes=["concreto"]),
            _c("tem_ala", "Tem ala (asa)?", TipoCampo.BOOL),
            _c("obstrucao_pct", "Obstrução da seção", TipoCampo.NUMERO, unidade="%", minimo=0, maximo=100),
        ],
    ),
    TipoDispositivo(
        "ala", "Ala / boca (componente)", Categoria.TRANSVERSAL, Geometria.PONTUAL, Grupo.DRENAGEM,
        [
            _c("posicao", "Posição", TipoCampo.ENUM, opcoes=["montante", "jusante"]),
            _c("material", "Material", TipoCampo.ENUM,
               opcoes=["concreto", "alvenaria", "pedra_argamassada"]),
            _c("altura_cm", "Altura", TipoCampo.NUMERO, unidade="cm", minimo=0),
        ],
    ),

    # ══════════════════════════════════════════════════════════════════════
    # OBRAS DE ARTE ESPECIAIS — 1 tipo com discriminador tipo_oae
    # ══════════════════════════════════════════════════════════════════════
    TipoDispositivo(
        "oae", "Obra de Arte Especial", Categoria.OAE, Geometria.PONTUAL, Grupo.OAE,
        OAE_ATRIBUTOS,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # SISTEMAS E TECNOLOGIA (ITS)
    # ══════════════════════════════════════════════════════════════════════
    TipoDispositivo(
        "call_box", "Call Box", Categoria.ITS, Geometria.PONTUAL, Grupo.ITS,
        ITS_ATRIBUTOS_BASE,
    ),
    TipoDispositivo(
        "estacao_meteorologica", "Estação Meteorológica", Categoria.ITS, Geometria.PONTUAL, Grupo.ITS,
        ITS_ATRIBUTOS_BASE,
    ),
    TipoDispositivo(
        "radar_velocidade", "Medidor de Velocidade (Radar)", Categoria.ITS, Geometria.PONTUAL, Grupo.ITS,
        ITS_ATRIBUTOS_BASE,
    ),
    TipoDispositivo(
        "pmv", "PMV (Painel Mensagem Variável)", Categoria.ITS, Geometria.PONTUAL, Grupo.ITS,
        [
            _c("tipo_pmv", "Tipo de PMV", TipoCampo.ENUM,
               opcoes=["led", "eletronico", "fibra_optica", "outro"]),
        ] + ITS_ATRIBUTOS_BASE,
    ),
    TipoDispositivo(
        "sat", "SAT (Sensor Automático de Tráfego)", Categoria.ITS, Geometria.PONTUAL, Grupo.ITS,
        ITS_ATRIBUTOS_BASE,
    ),
    TipoDispositivo(
        "scftv", "SCFTV (Circuito Fechado de Televisão)", Categoria.ITS, Geometria.PONTUAL, Grupo.ITS,
        ITS_ATRIBUTOS_BASE,
    ),
    TipoDispositivo(
        "portico", "Semi-Pórtico / Pórtico / Braço", Categoria.ITS, Geometria.PONTUAL, Grupo.ITS,
        [
            _c("tipo_portico", "Tipo", TipoCampo.ENUM,
               opcoes=["portico", "semi_portico", "braco"]),
            _c("material", "Material", TipoCampo.ENUM,
               opcoes=["aco", "aluminio", "concreto", "misto"]),
            _c("vao_m", "Vão", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("altura_m", "Altura", TipoCampo.NUMERO, unidade="m", minimo=0),
        ],
    ),

    # ══════════════════════════════════════════════════════════════════════
    # EDIFICAÇÕES E SERVIÇOS
    # ══════════════════════════════════════════════════════════════════════
    TipoDispositivo(
        "acesso_rodoviario", "Acesso Rodoviário", Categoria.EDIFICACOES, Geometria.PONTUAL, Grupo.EDIFICACOES,
        [
            _c("caracteristica", "Característica", TipoCampo.TEXTO),
            _c("situacao_pavimento", "Situação pavimento", TipoCampo.ENUM,
               opcoes=["bom", "regular", "ruim", "critico"]),
            _c("situacao_sinalizacao", "Situação sinalização", TipoCampo.ENUM,
               opcoes=["bom", "regular", "ruim", "critico"]),
            _c("situacao_drenagem", "Situação drenagem", TipoCampo.ENUM,
               opcoes=["bom", "regular", "ruim", "critico"]),
            _c("situacao_fx_aceleracao", "Situação faixa acel./desacel.", TipoCampo.ENUM,
               opcoes=["bom", "regular", "ruim", "critico"]),
        ],
    ),
    TipoDispositivo(
        "balanca", "Balança", Categoria.EDIFICACOES, Geometria.PONTUAL, Grupo.EDIFICACOES,
        [
            _c("tp_balanca", "Tipo de balança", TipoCampo.ENUM,
               opcoes=["seletiva", "precisao_fixa", "dinamica", "outro"]),
            _c("marca", "Marca", TipoCampo.TEXTO),
            _c("modelo", "Modelo", TipoCampo.TEXTO),
            _c("registro_artesp", "Registro ARTESP", TipoCampo.TEXTO),
            _c("data_ultima_aferacao", "Data última aferição", TipoCampo.TEXTO),
            _c("numero_certificado", "Nº certificado aferição", TipoCampo.TEXTO),
        ],
    ),
    TipoDispositivo(
        "base_operacional", "Base Operacional", Categoria.EDIFICACOES, Geometria.PONTUAL, Grupo.EDIFICACOES,
        [
            _c("registro_artesp", "Registro ARTESP", TipoCampo.TEXTO),
            _c("atende_usuario", "Atende usuário?", TipoCampo.BOOL),
            _c("endereco", "Endereço", TipoCampo.TEXTO),
        ],
    ),
    TipoDispositivo(
        "base_pmrv", "Base PMRV", Categoria.EDIFICACOES, Geometria.PONTUAL, Grupo.EDIFICACOES,
        [
            _c("registro_artesp", "Registro ARTESP", TipoCampo.TEXTO),
            _c("codigo_base", "Código da base", TipoCampo.TEXTO),
            _c("atende_usuario", "Atende usuário?", TipoCampo.BOOL),
            _c("endereco", "Endereço", TipoCampo.TEXTO),
        ],
    ),
    TipoDispositivo(
        "base_sau", "Base SAU (Serviço de Atendimento ao Usuário)", Categoria.EDIFICACOES, Geometria.PONTUAL, Grupo.EDIFICACOES,
        [
            _c("registro_artesp", "Registro ARTESP", TipoCampo.TEXTO),
            _c("tipo_sau", "Tipo SAU", TipoCampo.TEXTO),
        ],
    ),
    TipoDispositivo(
        "cco", "CCO (Centro de Controle Operacional)", Categoria.EDIFICACOES, Geometria.PONTUAL, Grupo.EDIFICACOES,
        [
            _c("registro_artesp", "Registro ARTESP", TipoCampo.TEXTO),
            _c("atende_usuario", "Atende usuário?", TipoCampo.BOOL),
            _c("endereco", "Endereço", TipoCampo.TEXTO),
        ],
    ),
    TipoDispositivo(
        "patio_apreensao", "Pátio de Apreensão de Animais", Categoria.EDIFICACOES, Geometria.PONTUAL, Grupo.EDIFICACOES,
        [
            _c("capacidade_animais", "Capacidade (animais)", TipoCampo.NUMERO, minimo=0),
            _c("tipo_instalacao", "Tipo de instalação", TipoCampo.TEXTO),
        ],
    ),
    TipoDispositivo(
        "pgf", "PGF (Posto Geral de Fiscalização)", Categoria.EDIFICACOES, Geometria.PONTUAL, Grupo.EDIFICACOES,
        [
            _c("registro_artesp", "Registro ARTESP", TipoCampo.TEXTO),
            _c("sistema_pesagem_fixa", "Sistema de pesagem fixa?", TipoCampo.BOOL),
            _c("balanca_seletiva", "Balança seletiva?", TipoCampo.BOOL),
            _c("balanca_precisao_fixa", "Balança de precisão fixa?", TipoCampo.BOOL),
            _c("detector_veiculos", "Detector de veículos?", TipoCampo.BOOL),
            _c("registro_imagem", "Registro de imagem?", TipoCampo.BOOL),
        ],
    ),
    TipoDispositivo(
        "posto_pesagem", "Posto de Pesagem", Categoria.EDIFICACOES, Geometria.PONTUAL, Grupo.EDIFICACOES,
        [
            _c("registro_artesp", "Registro ARTESP", TipoCampo.TEXTO),
            _c("marca", "Marca", TipoCampo.TEXTO),
            _c("modelo", "Modelo", TipoCampo.TEXTO),
            _c("tipo_balanca", "Tipo de balança", TipoCampo.TEXTO),
        ],
    ),
    TipoDispositivo(
        "praca_pedagio", "Praça de Pedágio", Categoria.EDIFICACOES, Geometria.PONTUAL, Grupo.EDIFICACOES,
        [
            _c("registro_artesp", "Registro ARTESP", TipoCampo.TEXTO),
            _c("tipo_pedagio", "Tipo de praça", TipoCampo.ENUM,
               opcoes=["principal", "secundaria", "cancela", "free_flow"]),
            _c("num_faixas", "Nº de faixas", TipoCampo.NUMERO, minimo=1),
            _c("tipo_cobranca", "Tipo de cobrança", TipoCampo.ENUM,
               opcoes=["manual", "automatico", "misto", "free_flow"]),
        ],
    ),
    TipoDispositivo(
        "posto_combustivel", "Posto de Combustível", Categoria.EDIFICACOES, Geometria.PONTUAL, Grupo.EDIFICACOES,
        [
            _c("tipo_instalacao", "Tipo de instalação", TipoCampo.ENUM,
               opcoes=["concessao", "parceria", "proprio", "outro"]),
            _c("bandeira", "Bandeira", TipoCampo.TEXTO),
        ],
    ),
    TipoDispositivo(
        "monumentos", "Monumentos / Marcos", Categoria.EDIFICACOES, Geometria.PONTUAL, Grupo.EDIFICACOES,
        [
            _c("tipo_monumento", "Tipo", TipoCampo.ENUM,
               opcoes=["marco_km", "marco_hectometrico", "placa_historica",
                       "monumento", "outro"]),
            _c("localidade", "Localidade", TipoCampo.TEXTO),
        ],
    ),
    TipoDispositivo(
        "pontos_fiscalizacao", "Pontos Homologados de Fiscalização", Categoria.EDIFICACOES, Geometria.PONTUAL, Grupo.EDIFICACOES,
        [
            _c("tipo_ponto", "Tipo de ponto", TipoCampo.TEXTO),
            _c("descricao", "Descrição", TipoCampo.TEXTO),
        ],
    ),

    # ══════════════════════════════════════════════════════════════════════
    # FAIXA DE DOMÍNIO E APOIO
    # ══════════════════════════════════════════════════════════════════════
    TipoDispositivo(
        "arvore", "Árvore", Categoria.FAIXA, Geometria.PONTUAL, Grupo.FAIXA,
        [
            _c("especie", "Espécie", TipoCampo.TEXTO),
            _c("dap_cm", "DAP (diâm. altura do peito)", TipoCampo.NUMERO, unidade="cm", minimo=0),
            _c("altura_m", "Altura estimada", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("estado_fitossanitario", "Estado fitossanitário", TipoCampo.ENUM,
               opcoes=["otimo", "bom", "regular", "ruim", "morta"]),
            _c("posicao_faixa", "Posição na faixa", TipoCampo.ENUM,
               opcoes=["canteiro_central", "acostamento", "talude", "outro"]),
        ],
    ),
    TipoDispositivo(
        "canteiro_gramado", "Canteiro Gramado", Categoria.FAIXA, Geometria.LINEAR, Grupo.FAIXA,
        [
            _c("tipo_vegetacao", "Tipo de vegetação", TipoCampo.ENUM,
               opcoes=["graminea", "arbustiva", "arborea", "mista"]),
            _c("tipo_rocada", "Tipo de roçada", TipoCampo.ENUM,
               opcoes=["mecanica", "manual", "quimica", "mista"]),
            _c("tipo_terreno", "Tipo de terreno", TipoCampo.ENUM,
               opcoes=["plano", "ondulado", "acidentado"]),
            _c("largura_m", "Largura", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("comprimento_m", "Comprimento", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("area_m2", "Área", TipoCampo.NUMERO, unidade="m²", minimo=0),
        ],
    ),
    TipoDispositivo(
        "passeio", "Passeio", Categoria.FAIXA, Geometria.LINEAR, Grupo.FAIXA,
        [
            _c("material", "Material", TipoCampo.ENUM,
               opcoes=["concreto", "asfalto", "piso_intertravado", "terra", "outro"]),
            _c("largura_m", "Largura", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("extensao_m", "Extensão", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("acessivel", "Acessível (PCD)?", TipoCampo.BOOL),
        ],
    ),
    TipoDispositivo(
        "ponto_onibus", "Ponto de Ônibus", Categoria.FAIXA, Geometria.PONTUAL, Grupo.FAIXA,
        [
            _c("tipo_abrigo", "Tipo de abrigo", TipoCampo.ENUM,
               opcoes=["coberto", "descoberto", "banco_simples"]),
            _c("cobertura", "Tem cobertura?", TipoCampo.BOOL),
            _c("assento", "Tem assento?", TipoCampo.BOOL),
            _c("iluminacao", "Tem iluminação?", TipoCampo.BOOL),
            _c("acessivel", "Acessível (PCD)?", TipoCampo.BOOL),
        ],
    ),
    TipoDispositivo(
        "refilamento", "Refilamento", Categoria.FAIXA, Geometria.LINEAR, Grupo.FAIXA,
        [
            _c("tipo_refilamento", "Tipo", TipoCampo.ENUM,
               opcoes=["manual", "mecanico"]),
            _c("largura_m", "Largura refilada", TipoCampo.NUMERO, unidade="m", minimo=0),
            _c("extensao_m", "Extensão", TipoCampo.NUMERO, unidade="m", minimo=0),
        ],
    ),
    TipoDispositivo(
        "terminal", "Terminal Rodoviário / Retorno", Categoria.FAIXA, Geometria.PONTUAL, Grupo.FAIXA,
        [
            _c("tipo_terminal", "Tipo", TipoCampo.ENUM,
               opcoes=["retorno", "terminal_onibus", "parada_emergencia", "outro"]),
            _c("area_m2", "Área", TipoCampo.NUMERO, unidade="m²", minimo=0),
        ],
    ),
    TipoDispositivo(
        "veiculo_operacional", "Veículo Operacional", Categoria.FAIXA, Geometria.PONTUAL, Grupo.FAIXA,
        [
            _c("tipo_veiculo", "Tipo", TipoCampo.ENUM,
               opcoes=["utilitario", "caminhao", "moto", "ambulancia",
                       "guincho", "patrol", "outro"]),
            _c("placa", "Placa", TipoCampo.TEXTO),
            _c("ano", "Ano", TipoCampo.NUMERO, minimo=1980, maximo=2100),
            _c("marca", "Marca", TipoCampo.TEXTO),
            _c("modelo", "Modelo", TipoCampo.TEXTO),
            _c("km_atual", "KM atual", TipoCampo.NUMERO, unidade="km", minimo=0),
        ],
    ),
]


# Estado de conservação (núcleo comum a todos — padrão de fiscalização)
ESTADOS_CONSERVACAO = ["bom", "regular", "ruim", "critico"]

_POR_TIPO: dict[str, TipoDispositivo] = {d.tipo: d for d in CATALOGO}


# ---------------------------------------------------------------------------
# VALIDAÇÃO
# ---------------------------------------------------------------------------
def valida_atributos(tipo: str, atributos: dict[str, Any]) -> list[str]:
    """Retorna lista de erros (vazia = válido)."""
    disp = _POR_TIPO.get(tipo)
    if disp is None:
        return [f"tipo desconhecido: {tipo}"]

    erros: list[str] = []
    campos = {c.nome: c for c in disp.atributos}

    for c in disp.atributos:
        if c.depende_de:
            if str(atributos.get(c.depende_de)) != c.depende_valor:
                continue
        val = atributos.get(c.nome)
        if c.obrigatorio and (val is None or val == ""):
            erros.append(f"{c.nome}: obrigatório")
            continue
        if val is None or val == "":
            continue
        if c.tipo == TipoCampo.NUMERO:
            try:
                n = float(val)
            except (TypeError, ValueError):
                erros.append(f"{c.nome}: deve ser número")
                continue
            if c.minimo is not None and n < c.minimo:
                erros.append(f"{c.nome}: mínimo {c.minimo}")
            if c.maximo is not None and n > c.maximo:
                erros.append(f"{c.nome}: máximo {c.maximo}")
        elif c.tipo == TipoCampo.ENUM and val not in c.opcoes:
            erros.append(f"{c.nome}: valor inválido '{val}'")

    for k in atributos:
        if k not in campos:
            erros.append(f"{k}: atributo não pertence ao tipo {tipo}")
    return erros


# ---------------------------------------------------------------------------
# EXPORT (alimenta o PWA)
# ---------------------------------------------------------------------------
def catalogo_dict() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for d in CATALOGO:
        item = asdict(d)
        item["categoria"] = d.categoria.value
        item["geometria"] = d.geometria.value
        item["grupo"]     = d.grupo.value
        for a in item["atributos"]:
            a["tipo"] = a["tipo"].value if hasattr(a["tipo"], "value") else a["tipo"]
        out.append(item)
    return out


def export_json(caminho: str = "catalogo.json") -> None:
    payload: dict[str, Any] = {
        "estados_conservacao": ESTADOS_CONSERVACAO,
        "grupos_meta":         GRUPOS_META,
        "dispositivos":        catalogo_dict(),
    }
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def export_js(caminho: str = "catalogo.js") -> None:
    """Gera o catálogo como módulo JS pro PWA embutir (offline, sem fetch)."""
    payload: dict[str, Any] = {
        "estados_conservacao": ESTADOS_CONSERVACAO,
        "grupos_meta":         GRUPOS_META,
        "dispositivos":        catalogo_dict(),
    }
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("// GERADO POR catalogo_dispositivos.py — não editar à mão\n")
        f.write("window.CATALOGO = ")
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write(";\n")


if __name__ == "__main__":
    import os, sys
    # suporta execução a partir da raiz do projecto ou de dentro de APP_Inventarios
    base = os.path.dirname(os.path.abspath(__file__))
    export_json(os.path.join(base, "catalogo.json"))
    export_js(os.path.join(base, "catalogo.js"))
    print(f"{len(CATALOGO)} tipos exportados em {base}/catalogo.js")
