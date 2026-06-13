// GERADO POR catalogo_dispositivos.py — não editar à mão
window.CATALOGO = {
  "estados_conservacao": [
    "bom",
    "regular",
    "ruim",
    "critico"
  ],
  "grupos_meta": {
    "seguranca": {
      "rotulo": "Segurança e Sinalização",
      "icone": "🛡️"
    },
    "drenagem": {
      "rotulo": "Sistema de Drenagem",
      "icone": "💧"
    },
    "oae": {
      "rotulo": "Obras de Arte Especiais",
      "icone": "🌉"
    },
    "its": {
      "rotulo": "Sistemas e Tecnologia (ITS)",
      "icone": "📡"
    },
    "edificacoes": {
      "rotulo": "Edificações e Serviços",
      "icone": "🏢"
    },
    "faixa_dominio": {
      "rotulo": "Faixa de Domínio e Apoio",
      "icone": "🌱"
    }
  },
  "dispositivos": [
    {
      "tipo": "alambrado",
      "rotulo": "Alambrado",
      "categoria": "seguranca",
      "geometria": "linear",
      "grupo": "seguranca",
      "atributos": [
        {
          "nome": "tipo_poste",
          "rotulo": "Tipo de poste",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "concreto",
            "metalico",
            "madeira",
            "misto"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "espacamento_poste_m",
          "rotulo": "Espaçamento entre postes",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "altura_poste_m",
          "rotulo": "Altura do poste",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_tela",
          "rotulo": "Tipo de tela",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "hexagonal",
            "soldada",
            "rolo_simples",
            "outro"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "altura_tela_m",
          "rotulo": "Altura da tela",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "abertura_tela_cm",
          "rotulo": "Abertura da tela",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "extensao_m",
          "rotulo": "Extensão do tramo",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "qtd_postes",
          "rotulo": "Qtd. postes no tramo",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "balizador",
      "rotulo": "Balizadores",
      "categoria": "seguranca",
      "geometria": "linear",
      "grupo": "seguranca",
      "atributos": [
        {
          "nome": "tipo_balizador",
          "rotulo": "Tipo de balizador",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "cilindrico",
            "plastico_flexivel",
            "borracha",
            "concreto",
            "outro"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "refletivo",
          "rotulo": "Refletivo?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tamanho_refletivo",
          "rotulo": "Tamanho do refletivo",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "largura_cm",
          "rotulo": "Largura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "altura_cm",
          "rotulo": "Altura além do solo",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "cadencia_m",
          "rotulo": "Cadência (espaçamento)",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "extensao_m",
          "rotulo": "Extensão do tramo",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "qtd_balizadores",
          "rotulo": "Qtd. balizadores",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "barreira_concreto",
      "rotulo": "Barreira de Concreto",
      "categoria": "seguranca",
      "geometria": "linear",
      "grupo": "seguranca",
      "atributos": [
        {
          "nome": "tipo_barreira",
          "rotulo": "Tipo de barreira",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "new_jersey",
            "f_shape",
            "blocos_interligados",
            "outro"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "com_armadura",
          "rotulo": "Com armadura?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_entrada",
          "rotulo": "Tipo de entrada",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_saida",
          "rotulo": "Tipo de saída",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "comprimento_m",
          "rotulo": "Comprimento",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "altura_total_cm",
          "rotulo": "Altura total",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "altura_alma_cm",
          "rotulo": "Altura da alma",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "altura_espelho_cm",
          "rotulo": "Altura do espelho",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "largura_base_cm",
          "rotulo": "Largura da base",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "largura_topo_cm",
          "rotulo": "Largura do topo",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "cerca",
      "rotulo": "Cerca",
      "categoria": "seguranca",
      "geometria": "linear",
      "grupo": "seguranca",
      "atributos": [
        {
          "nome": "tipo_mourao",
          "rotulo": "Tipo de mourão",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "concreto",
            "metalico",
            "madeira",
            "misto"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "espacamento_mourao_m",
          "rotulo": "Espaçamento entre mourões",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "altura_mourao_m",
          "rotulo": "Altura do mourão",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_arame",
          "rotulo": "Tipo de arame",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "liso",
            "farpado",
            "tela",
            "misto"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "qtd_fios",
          "rotulo": "Quantidade de fios",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "extensao_m",
          "rotulo": "Extensão do tramo",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "defensa_metalica",
      "rotulo": "Defensa Metálica",
      "categoria": "seguranca",
      "geometria": "linear",
      "grupo": "seguranca",
      "atributos": [
        {
          "nome": "tipo_defensa",
          "rotulo": "Tipo de defensa",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "simples",
            "dupla",
            "rigida",
            "semirigida",
            "flexivel"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "marca",
          "rotulo": "Marca",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "modelo",
          "rotulo": "Modelo",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_entrada",
          "rotulo": "Tipo de entrada",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_saida",
          "rotulo": "Tipo de saída",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "altura_mm",
          "rotulo": "Altura/Espessura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "mm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "espaco_postes_m",
          "rotulo": "Espaço entre postes",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "comprimento_m",
          "rotulo": "Comprimento do tramo",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "sinalizacao_marcas",
      "rotulo": "Sinalização Horiz. — Marcas Viárias",
      "categoria": "seguranca",
      "geometria": "linear",
      "grupo": "seguranca",
      "atributos": [
        {
          "nome": "tipo_marca",
          "rotulo": "Tipo de marca",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "linha_simples",
            "linha_dupla",
            "linha_contínua",
            "linha_tracejada",
            "chevron",
            "outra"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "cor",
          "rotulo": "Cor",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "amarela",
            "branca",
            "vermelha"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "material",
          "rotulo": "Material",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "tinta",
            "termoplastico",
            "plastico_frio",
            "epoxy"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "largura_cm",
          "rotulo": "Largura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "extensao_m",
          "rotulo": "Extensão",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "sinalizacao_zebrado",
      "rotulo": "Sinalização Horiz. — Zebrado",
      "categoria": "seguranca",
      "geometria": "pontual",
      "grupo": "seguranca",
      "atributos": [
        {
          "nome": "tipo_zebrado",
          "rotulo": "Tipo",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "faixa_pedestres",
            "cruzamento_bicicleta",
            "zebrado_bloqueio",
            "outro"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "material",
          "rotulo": "Material",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "tinta",
            "termoplastico",
            "plastico_frio",
            "epoxy"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "area_m2",
          "rotulo": "Área",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m²",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "sinalizacao_tacha",
      "rotulo": "Sinalização Horiz. — Tacha Longitudinal",
      "categoria": "seguranca",
      "geometria": "linear",
      "grupo": "seguranca",
      "atributos": [
        {
          "nome": "tipo_tacha",
          "rotulo": "Tipo de tacha",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "refletiva",
            "nao_refletiva",
            "led",
            "outro"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "cor",
          "rotulo": "Cor",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "amarela",
            "branca",
            "vermelha"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "espacamento_m",
          "rotulo": "Espaçamento",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "extensao_m",
          "rotulo": "Extensão do tramo",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "qtd_tachas",
          "rotulo": "Qtd. tachas",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "sinalizacao_vertical",
      "rotulo": "Sinalização Vertical",
      "categoria": "seguranca",
      "geometria": "pontual",
      "grupo": "seguranca",
      "atributos": [
        {
          "nome": "codigo_nbr",
          "rotulo": "Código NBR",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": "Ex: R-1, A-1b, IE-1",
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_placa",
          "rotulo": "Tipo de placa",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "regulamentacao",
            "advertencia",
            "indicacao",
            "educativa",
            "obra",
            "outra"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "dimensao_cm",
          "rotulo": "Dimensão (diâm./lado)",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "material_placa",
          "rotulo": "Material",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "aco_galvanizado",
            "aluminio",
            "polietileno",
            "outro"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_suporte",
          "rotulo": "Tipo de suporte",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "coluna_simples",
            "coluna_dupla",
            "portico",
            "semipórtico",
            "muro",
            "parede",
            "outro"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "altura_suporte_m",
          "rotulo": "Altura do suporte",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "transicao",
      "rotulo": "Transição",
      "categoria": "seguranca",
      "geometria": "pontual",
      "grupo": "seguranca",
      "atributos": [
        {
          "nome": "tipo_entrada",
          "rotulo": "Tipo de dispositivo de entrada",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_saida",
          "rotulo": "Tipo de dispositivo de saída",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "comprimento_m",
          "rotulo": "Comprimento",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "canaleta",
      "rotulo": "Canaleta",
      "categoria": "superficial",
      "geometria": "linear",
      "grupo": "drenagem",
      "atributos": [
        {
          "nome": "secao",
          "rotulo": "Seção",
          "tipo": "enum",
          "obrigatorio": true,
          "unidade": null,
          "opcoes": [
            "triangular",
            "trapezoidal",
            "retangular",
            "meia_cana"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "material",
          "rotulo": "Material",
          "tipo": "enum",
          "obrigatorio": true,
          "unidade": null,
          "opcoes": [
            "concreto",
            "grama",
            "solo",
            "pead",
            "alvenaria",
            "pedra_argamassada"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "largura_cm",
          "rotulo": "Largura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "altura_cm",
          "rotulo": "Altura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "sarjeta",
      "rotulo": "Sarjeta",
      "categoria": "superficial",
      "geometria": "linear",
      "grupo": "drenagem",
      "atributos": [
        {
          "nome": "posicao",
          "rotulo": "Posição",
          "tipo": "enum",
          "obrigatorio": true,
          "unidade": null,
          "opcoes": [
            "corte",
            "aterro",
            "canteiro_central"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "secao",
          "rotulo": "Seção",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "triangular",
            "trapezoidal",
            "retangular",
            "meia_cana"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "material",
          "rotulo": "Material",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "concreto",
            "grama",
            "solo",
            "pead",
            "alvenaria",
            "pedra_argamassada"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "largura_cm",
          "rotulo": "Largura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "altura_cm",
          "rotulo": "Altura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "valeta_protecao",
      "rotulo": "Valeta de proteção",
      "categoria": "superficial",
      "geometria": "linear",
      "grupo": "drenagem",
      "atributos": [
        {
          "nome": "posicao",
          "rotulo": "Posição",
          "tipo": "enum",
          "obrigatorio": true,
          "unidade": null,
          "opcoes": [
            "crista_corte",
            "pe_aterro",
            "banqueta"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "secao",
          "rotulo": "Seção",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "triangular",
            "trapezoidal",
            "retangular",
            "meia_cana"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "material",
          "rotulo": "Material",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "concreto",
            "grama",
            "solo",
            "pead",
            "alvenaria",
            "pedra_argamassada"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "largura_cm",
          "rotulo": "Largura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "profundidade_cm",
          "rotulo": "Profundidade",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "meio_fio",
      "rotulo": "Meio-fio",
      "categoria": "superficial",
      "geometria": "linear",
      "grupo": "drenagem",
      "atributos": [
        {
          "nome": "tipo_mf",
          "rotulo": "Tipo",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "simples",
            "conjugado_sarjeta"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "material",
          "rotulo": "Material",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "concreto",
            "pre_moldado"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "altura_cm",
          "rotulo": "Altura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "descida_dagua",
      "rotulo": "Descida d'água / Escada hidráulica",
      "categoria": "superficial",
      "geometria": "linear",
      "grupo": "drenagem",
      "atributos": [
        {
          "nome": "tipo_descida",
          "rotulo": "Tipo",
          "tipo": "enum",
          "obrigatorio": true,
          "unidade": null,
          "opcoes": [
            "rapida",
            "degraus"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": "'degraus' = escada hidráulica",
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "material",
          "rotulo": "Material",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "concreto",
            "pre_moldado",
            "alvenaria"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "largura_cm",
          "rotulo": "Largura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "n_degraus",
          "rotulo": "Nº de degraus",
          "tipo": "numero",
          "obrigatorio": true,
          "unidade": null,
          "opcoes": [],
          "minimo": 1,
          "maximo": null,
          "ajuda": null,
          "depende_de": "tipo_descida",
          "depende_valor": "degraus"
        },
        {
          "nome": "altura_espelho_cm",
          "rotulo": "Altura do espelho",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": "tipo_descida",
          "depende_valor": "degraus"
        },
        {
          "nome": "tem_dissipador_saida",
          "rotulo": "Dissipador na saída?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "dissipador_energia",
      "rotulo": "Dissipador de energia",
      "categoria": "superficial",
      "geometria": "pontual",
      "grupo": "drenagem",
      "atributos": [
        {
          "nome": "tipo_dissipador",
          "rotulo": "Tipo",
          "tipo": "enum",
          "obrigatorio": true,
          "unidade": null,
          "opcoes": [
            "bacia",
            "enrocamento",
            "blocos",
            "escalonado"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "comprimento_cm",
          "rotulo": "Comprimento",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "largura_cm",
          "rotulo": "Largura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "caixa_coletora",
      "rotulo": "Caixa coletora / ligação",
      "categoria": "superficial",
      "geometria": "pontual",
      "grupo": "drenagem",
      "atributos": [
        {
          "nome": "funcao",
          "rotulo": "Função",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "coletora",
            "ligacao",
            "passagem"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "largura_cm",
          "rotulo": "Largura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "comprimento_cm",
          "rotulo": "Comprimento",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "profundidade_cm",
          "rotulo": "Profundidade",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tem_grelha",
          "rotulo": "Tem grelha?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "saida_dagua",
      "rotulo": "Saída/entrada d'água",
      "categoria": "superficial",
      "geometria": "pontual",
      "grupo": "drenagem",
      "atributos": [
        {
          "nome": "funcao",
          "rotulo": "Função",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "saida",
            "entrada"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "material",
          "rotulo": "Material",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "concreto",
            "alvenaria"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "largura_cm",
          "rotulo": "Largura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "dreno_longitudinal",
      "rotulo": "Dreno longitudinal",
      "categoria": "profunda",
      "geometria": "linear",
      "grupo": "drenagem",
      "atributos": [
        {
          "nome": "classe",
          "rotulo": "Classe",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "profundo",
            "raso_pavimento"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "diametro_tubo_mm",
          "rotulo": "Ø tubo",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "mm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "material_tubo",
          "rotulo": "Material do tubo",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "concreto",
            "pead",
            "pvc",
            "metalico"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "profundidade_cm",
          "rotulo": "Profundidade",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "material_filtrante",
          "rotulo": "Material filtrante",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "brita",
            "areia",
            "geotextil",
            "misto"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "espinha_peixe",
      "rotulo": "Dreno espinha-de-peixe",
      "categoria": "profunda",
      "geometria": "linear",
      "grupo": "drenagem",
      "atributos": [
        {
          "nome": "diametro_tubo_mm",
          "rotulo": "Ø tubo",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "mm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "profundidade_cm",
          "rotulo": "Profundidade",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "espacamento_m",
          "rotulo": "Espaçamento entre ramos",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "dhp",
      "rotulo": "Dreno sub-horizontal (DHP)",
      "categoria": "profunda",
      "geometria": "pontual",
      "grupo": "drenagem",
      "atributos": [
        {
          "nome": "diametro_mm",
          "rotulo": "Ø",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "mm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "comprimento_m",
          "rotulo": "Comprimento",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "inclinacao_graus",
          "rotulo": "Inclinação",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "°",
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "colchao_drenante",
      "rotulo": "Colchão drenante",
      "categoria": "profunda",
      "geometria": "linear",
      "grupo": "drenagem",
      "atributos": [
        {
          "nome": "espessura_cm",
          "rotulo": "Espessura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "material",
          "rotulo": "Material",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "brita",
            "areia",
            "misto"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "bueiro_tubular",
      "rotulo": "Bueiro tubular (BSTC/BDTC/BTTC)",
      "categoria": "transversal",
      "geometria": "pontual",
      "grupo": "drenagem",
      "atributos": [
        {
          "nome": "n_linhas",
          "rotulo": "Nº de linhas",
          "tipo": "enum",
          "obrigatorio": true,
          "unidade": null,
          "opcoes": [
            "1",
            "2",
            "3"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": "1=simples, 2=duplo, 3=triplo",
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "diametro_mm",
          "rotulo": "Ø",
          "tipo": "numero",
          "obrigatorio": true,
          "unidade": "mm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "material",
          "rotulo": "Material",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "concreto",
            "metalico",
            "pead"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tem_ala",
          "rotulo": "Tem ala (asa)?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tem_dissipador_saida",
          "rotulo": "Dissipador na saída?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "obstrucao_pct",
          "rotulo": "Obstrução da seção",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "%",
          "opcoes": [],
          "minimo": 0,
          "maximo": 100,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "bueiro_celular",
      "rotulo": "Bueiro celular (BSCC/BDCC)",
      "categoria": "transversal",
      "geometria": "pontual",
      "grupo": "drenagem",
      "atributos": [
        {
          "nome": "n_celulas",
          "rotulo": "Nº de células",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "1",
            "2",
            "3"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "largura_cm",
          "rotulo": "Largura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "altura_cm",
          "rotulo": "Altura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "material",
          "rotulo": "Material",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "concreto"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tem_ala",
          "rotulo": "Tem ala (asa)?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "obstrucao_pct",
          "rotulo": "Obstrução da seção",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "%",
          "opcoes": [],
          "minimo": 0,
          "maximo": 100,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "ala",
      "rotulo": "Ala / boca (componente)",
      "categoria": "transversal",
      "geometria": "pontual",
      "grupo": "drenagem",
      "atributos": [
        {
          "nome": "posicao",
          "rotulo": "Posição",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "montante",
            "jusante"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "material",
          "rotulo": "Material",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "concreto",
            "alvenaria",
            "pedra_argamassada"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "altura_cm",
          "rotulo": "Altura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "oae",
      "rotulo": "Obra de Arte Especial",
      "categoria": "oae",
      "geometria": "pontual",
      "grupo": "oae",
      "atributos": [
        {
          "nome": "tipo_oae",
          "rotulo": "Tipo de OAE",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "ponte",
            "viaduto",
            "passarela",
            "passagem_superior",
            "passagem_inferior",
            "passagem_gado",
            "galeria"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": "Discriminador do tipo de obra de arte",
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "qtd_vaos",
          "rotulo": "Qtd. de vãos",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": 1,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "comprimento_m",
          "rotulo": "Comprimento total",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "largura_m",
          "rotulo": "Largura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "vao_livre_m",
          "rotulo": "Vão livre",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "gabarito_vertical_m",
          "rotulo": "Gabarito vertical",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "gabarito_horizontal_m",
          "rotulo": "Gabarito horizontal",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tabuleiro_tipo",
          "rotulo": "Tipo de tabuleiro",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipologia_vaos",
          "rotulo": "Tipologia dos vãos",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "inclinacao_rampas",
          "rotulo": "Inclinação das rampas",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "telamento",
          "rotulo": "Telamento?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "iluminacao",
          "rotulo": "Iluminação?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "dispositivo_contencao",
          "rotulo": "Dispositivo de contenção",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "trem_tipo",
          "rotulo": "Trem tipo",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "status_oae",
          "rotulo": "Status da OAE",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "em_operacao",
            "interditado",
            "em_obras",
            "demolido"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "data_implantacao",
          "rotulo": "Data de implantação",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "municipio",
          "rotulo": "Município",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "calcamento",
          "rotulo": "Calçamento",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "escada",
          "rotulo": "Escada de acesso?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "call_box",
      "rotulo": "Call Box",
      "categoria": "its",
      "geometria": "pontual",
      "grupo": "its",
      "atributos": [
        {
          "nome": "registro_artesp",
          "rotulo": "Registro ARTESP",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "grupo_componente",
          "rotulo": "Grupo componente",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_componente",
          "rotulo": "Tipo componente",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "marca",
          "rotulo": "Marca",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "modelo",
          "rotulo": "Modelo",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "estacao_meteorologica",
      "rotulo": "Estação Meteorológica",
      "categoria": "its",
      "geometria": "pontual",
      "grupo": "its",
      "atributos": [
        {
          "nome": "registro_artesp",
          "rotulo": "Registro ARTESP",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "grupo_componente",
          "rotulo": "Grupo componente",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_componente",
          "rotulo": "Tipo componente",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "marca",
          "rotulo": "Marca",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "modelo",
          "rotulo": "Modelo",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "radar_velocidade",
      "rotulo": "Medidor de Velocidade (Radar)",
      "categoria": "its",
      "geometria": "pontual",
      "grupo": "its",
      "atributos": [
        {
          "nome": "registro_artesp",
          "rotulo": "Registro ARTESP",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "grupo_componente",
          "rotulo": "Grupo componente",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_componente",
          "rotulo": "Tipo componente",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "marca",
          "rotulo": "Marca",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "modelo",
          "rotulo": "Modelo",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "pmv",
      "rotulo": "PMV (Painel Mensagem Variável)",
      "categoria": "its",
      "geometria": "pontual",
      "grupo": "its",
      "atributos": [
        {
          "nome": "tipo_pmv",
          "rotulo": "Tipo de PMV",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "led",
            "eletronico",
            "fibra_optica",
            "outro"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "registro_artesp",
          "rotulo": "Registro ARTESP",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "grupo_componente",
          "rotulo": "Grupo componente",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_componente",
          "rotulo": "Tipo componente",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "marca",
          "rotulo": "Marca",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "modelo",
          "rotulo": "Modelo",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "sat",
      "rotulo": "SAT (Sensor Automático de Tráfego)",
      "categoria": "its",
      "geometria": "pontual",
      "grupo": "its",
      "atributos": [
        {
          "nome": "registro_artesp",
          "rotulo": "Registro ARTESP",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "grupo_componente",
          "rotulo": "Grupo componente",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_componente",
          "rotulo": "Tipo componente",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "marca",
          "rotulo": "Marca",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "modelo",
          "rotulo": "Modelo",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "scftv",
      "rotulo": "SCFTV (Circuito Fechado de Televisão)",
      "categoria": "its",
      "geometria": "pontual",
      "grupo": "its",
      "atributos": [
        {
          "nome": "registro_artesp",
          "rotulo": "Registro ARTESP",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "grupo_componente",
          "rotulo": "Grupo componente",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_componente",
          "rotulo": "Tipo componente",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "marca",
          "rotulo": "Marca",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "modelo",
          "rotulo": "Modelo",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "portico",
      "rotulo": "Semi-Pórtico / Pórtico / Braço",
      "categoria": "its",
      "geometria": "pontual",
      "grupo": "its",
      "atributos": [
        {
          "nome": "tipo_portico",
          "rotulo": "Tipo",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "portico",
            "semi_portico",
            "braco"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "material",
          "rotulo": "Material",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "aco",
            "aluminio",
            "concreto",
            "misto"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "vao_m",
          "rotulo": "Vão",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "altura_m",
          "rotulo": "Altura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "acesso_rodoviario",
      "rotulo": "Acesso Rodoviário",
      "categoria": "edificacoes",
      "geometria": "pontual",
      "grupo": "edificacoes",
      "atributos": [
        {
          "nome": "caracteristica",
          "rotulo": "Característica",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "situacao_pavimento",
          "rotulo": "Situação pavimento",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "bom",
            "regular",
            "ruim",
            "critico"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "situacao_sinalizacao",
          "rotulo": "Situação sinalização",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "bom",
            "regular",
            "ruim",
            "critico"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "situacao_drenagem",
          "rotulo": "Situação drenagem",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "bom",
            "regular",
            "ruim",
            "critico"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "situacao_fx_aceleracao",
          "rotulo": "Situação faixa acel./desacel.",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "bom",
            "regular",
            "ruim",
            "critico"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "balanca",
      "rotulo": "Balança",
      "categoria": "edificacoes",
      "geometria": "pontual",
      "grupo": "edificacoes",
      "atributos": [
        {
          "nome": "tp_balanca",
          "rotulo": "Tipo de balança",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "seletiva",
            "precisao_fixa",
            "dinamica",
            "outro"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "marca",
          "rotulo": "Marca",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "modelo",
          "rotulo": "Modelo",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "registro_artesp",
          "rotulo": "Registro ARTESP",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "data_ultima_aferacao",
          "rotulo": "Data última aferição",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "numero_certificado",
          "rotulo": "Nº certificado aferição",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "base_operacional",
      "rotulo": "Base Operacional",
      "categoria": "edificacoes",
      "geometria": "pontual",
      "grupo": "edificacoes",
      "atributos": [
        {
          "nome": "registro_artesp",
          "rotulo": "Registro ARTESP",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "atende_usuario",
          "rotulo": "Atende usuário?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "endereco",
          "rotulo": "Endereço",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "base_pmrv",
      "rotulo": "Base PMRV",
      "categoria": "edificacoes",
      "geometria": "pontual",
      "grupo": "edificacoes",
      "atributos": [
        {
          "nome": "registro_artesp",
          "rotulo": "Registro ARTESP",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "codigo_base",
          "rotulo": "Código da base",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "atende_usuario",
          "rotulo": "Atende usuário?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "endereco",
          "rotulo": "Endereço",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "base_sau",
      "rotulo": "Base SAU (Serviço de Atendimento ao Usuário)",
      "categoria": "edificacoes",
      "geometria": "pontual",
      "grupo": "edificacoes",
      "atributos": [
        {
          "nome": "registro_artesp",
          "rotulo": "Registro ARTESP",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_sau",
          "rotulo": "Tipo SAU",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "cco",
      "rotulo": "CCO (Centro de Controle Operacional)",
      "categoria": "edificacoes",
      "geometria": "pontual",
      "grupo": "edificacoes",
      "atributos": [
        {
          "nome": "registro_artesp",
          "rotulo": "Registro ARTESP",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "atende_usuario",
          "rotulo": "Atende usuário?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "endereco",
          "rotulo": "Endereço",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "patio_apreensao",
      "rotulo": "Pátio de Apreensão de Animais",
      "categoria": "edificacoes",
      "geometria": "pontual",
      "grupo": "edificacoes",
      "atributos": [
        {
          "nome": "capacidade_animais",
          "rotulo": "Capacidade (animais)",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_instalacao",
          "rotulo": "Tipo de instalação",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "pgf",
      "rotulo": "PGF (Posto Geral de Fiscalização)",
      "categoria": "edificacoes",
      "geometria": "pontual",
      "grupo": "edificacoes",
      "atributos": [
        {
          "nome": "registro_artesp",
          "rotulo": "Registro ARTESP",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "sistema_pesagem_fixa",
          "rotulo": "Sistema de pesagem fixa?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "balanca_seletiva",
          "rotulo": "Balança seletiva?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "balanca_precisao_fixa",
          "rotulo": "Balança de precisão fixa?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "detector_veiculos",
          "rotulo": "Detector de veículos?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "registro_imagem",
          "rotulo": "Registro de imagem?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "posto_pesagem",
      "rotulo": "Posto de Pesagem",
      "categoria": "edificacoes",
      "geometria": "pontual",
      "grupo": "edificacoes",
      "atributos": [
        {
          "nome": "registro_artesp",
          "rotulo": "Registro ARTESP",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "marca",
          "rotulo": "Marca",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "modelo",
          "rotulo": "Modelo",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_balanca",
          "rotulo": "Tipo de balança",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "praca_pedagio",
      "rotulo": "Praça de Pedágio",
      "categoria": "edificacoes",
      "geometria": "pontual",
      "grupo": "edificacoes",
      "atributos": [
        {
          "nome": "registro_artesp",
          "rotulo": "Registro ARTESP",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_pedagio",
          "rotulo": "Tipo de praça",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "principal",
            "secundaria",
            "cancela",
            "free_flow"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "num_faixas",
          "rotulo": "Nº de faixas",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": 1,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_cobranca",
          "rotulo": "Tipo de cobrança",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "manual",
            "automatico",
            "misto",
            "free_flow"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "posto_combustivel",
      "rotulo": "Posto de Combustível",
      "categoria": "edificacoes",
      "geometria": "pontual",
      "grupo": "edificacoes",
      "atributos": [
        {
          "nome": "tipo_instalacao",
          "rotulo": "Tipo de instalação",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "concessao",
            "parceria",
            "proprio",
            "outro"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "bandeira",
          "rotulo": "Bandeira",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "monumentos",
      "rotulo": "Monumentos / Marcos",
      "categoria": "edificacoes",
      "geometria": "pontual",
      "grupo": "edificacoes",
      "atributos": [
        {
          "nome": "tipo_monumento",
          "rotulo": "Tipo",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "marco_km",
            "marco_hectometrico",
            "placa_historica",
            "monumento",
            "outro"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "localidade",
          "rotulo": "Localidade",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "pontos_fiscalizacao",
      "rotulo": "Pontos Homologados de Fiscalização",
      "categoria": "edificacoes",
      "geometria": "pontual",
      "grupo": "edificacoes",
      "atributos": [
        {
          "nome": "tipo_ponto",
          "rotulo": "Tipo de ponto",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "descricao",
          "rotulo": "Descrição",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "arvore",
      "rotulo": "Árvore",
      "categoria": "faixa_dominio",
      "geometria": "pontual",
      "grupo": "faixa_dominio",
      "atributos": [
        {
          "nome": "especie",
          "rotulo": "Espécie",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "dap_cm",
          "rotulo": "DAP (diâm. altura do peito)",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "cm",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "altura_m",
          "rotulo": "Altura estimada",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "estado_fitossanitario",
          "rotulo": "Estado fitossanitário",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "otimo",
            "bom",
            "regular",
            "ruim",
            "morta"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "posicao_faixa",
          "rotulo": "Posição na faixa",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "canteiro_central",
            "acostamento",
            "talude",
            "outro"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "canteiro_gramado",
      "rotulo": "Canteiro Gramado",
      "categoria": "faixa_dominio",
      "geometria": "linear",
      "grupo": "faixa_dominio",
      "atributos": [
        {
          "nome": "tipo_vegetacao",
          "rotulo": "Tipo de vegetação",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "graminea",
            "arbustiva",
            "arborea",
            "mista"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_rocada",
          "rotulo": "Tipo de roçada",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "mecanica",
            "manual",
            "quimica",
            "mista"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "tipo_terreno",
          "rotulo": "Tipo de terreno",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "plano",
            "ondulado",
            "acidentado"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "largura_m",
          "rotulo": "Largura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "comprimento_m",
          "rotulo": "Comprimento",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "area_m2",
          "rotulo": "Área",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m²",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "passeio",
      "rotulo": "Passeio",
      "categoria": "faixa_dominio",
      "geometria": "linear",
      "grupo": "faixa_dominio",
      "atributos": [
        {
          "nome": "material",
          "rotulo": "Material",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "concreto",
            "asfalto",
            "piso_intertravado",
            "terra",
            "outro"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "largura_m",
          "rotulo": "Largura",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "extensao_m",
          "rotulo": "Extensão",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "acessivel",
          "rotulo": "Acessível (PCD)?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "ponto_onibus",
      "rotulo": "Ponto de Ônibus",
      "categoria": "faixa_dominio",
      "geometria": "pontual",
      "grupo": "faixa_dominio",
      "atributos": [
        {
          "nome": "tipo_abrigo",
          "rotulo": "Tipo de abrigo",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "coberto",
            "descoberto",
            "banco_simples"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "cobertura",
          "rotulo": "Tem cobertura?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "assento",
          "rotulo": "Tem assento?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "iluminacao",
          "rotulo": "Tem iluminação?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "acessivel",
          "rotulo": "Acessível (PCD)?",
          "tipo": "bool",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "refilamento",
      "rotulo": "Refilamento",
      "categoria": "faixa_dominio",
      "geometria": "linear",
      "grupo": "faixa_dominio",
      "atributos": [
        {
          "nome": "tipo_refilamento",
          "rotulo": "Tipo",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "manual",
            "mecanico"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "largura_m",
          "rotulo": "Largura refilada",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "extensao_m",
          "rotulo": "Extensão",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "terminal",
      "rotulo": "Terminal Rodoviário / Retorno",
      "categoria": "faixa_dominio",
      "geometria": "pontual",
      "grupo": "faixa_dominio",
      "atributos": [
        {
          "nome": "tipo_terminal",
          "rotulo": "Tipo",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "retorno",
            "terminal_onibus",
            "parada_emergencia",
            "outro"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "area_m2",
          "rotulo": "Área",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "m²",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    },
    {
      "tipo": "veiculo_operacional",
      "rotulo": "Veículo Operacional",
      "categoria": "faixa_dominio",
      "geometria": "pontual",
      "grupo": "faixa_dominio",
      "atributos": [
        {
          "nome": "tipo_veiculo",
          "rotulo": "Tipo",
          "tipo": "enum",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [
            "utilitario",
            "caminhao",
            "moto",
            "ambulancia",
            "guincho",
            "patrol",
            "outro"
          ],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "placa",
          "rotulo": "Placa",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "ano",
          "rotulo": "Ano",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": 1980,
          "maximo": 2100,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "marca",
          "rotulo": "Marca",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "modelo",
          "rotulo": "Modelo",
          "tipo": "texto",
          "obrigatorio": false,
          "unidade": null,
          "opcoes": [],
          "minimo": null,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        },
        {
          "nome": "km_atual",
          "rotulo": "KM atual",
          "tipo": "numero",
          "obrigatorio": false,
          "unidade": "km",
          "opcoes": [],
          "minimo": 0,
          "maximo": null,
          "ajuda": null,
          "depende_de": null,
          "depende_valor": null
        }
      ]
    }
  ]
};
