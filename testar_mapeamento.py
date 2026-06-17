import re, unicodedata

def _norm(s):
    t = unicodedata.normalize("NFKC", (s or "").strip())
    return " ".join(t.lower().split())

def mapear(pat):
    pl = _norm(re.sub(r"\s+", " ", (pat or "").strip()))
    kcor = None
    def _set(v): nonlocal kcor; kcor = v

    # Regras originais
    if len(pl) >= 6 and pl[:6] == "trilha":         _set("Afundamento nas trilhas de rodas")
    if len(pl) >= 9 and pl[:9] == "alambrado":      _set("Alambrado")
    if pl == _norm("Dispositivo de segurança (alambrado)"): _set("Alambrado")
    if pl.startswith("guarda corpo"):                _set("Barreira rígida")
    if pl == _norm("Inexistência de elementos refletivos"): _set("Barreira rígida")
    if len(pl) >= 7 and pl[:7] == "buracos":        _set("Buracos e panelas - Emergencial")
    if len(pl) >= 7 and pl[-7:] == "caiação":       _set("Caiação")
    if len(pl) >= 5 and pl[:5] == "cerca":          _set("Cerca")
    if len(pl) >= 6 and pl[:6] == "erosão":         _set("Conservação de terraplenos e contenções")
    if len(pl) >= 7 and pl[:7] == "defensa":        _set("Defensa metálica")
    if len(pl) >= 11 and pl[:11] == "deformações":  _set("Deformação permanente")
    if len(pl) >= 6 and pl[:6] == "degrau":
        if "acostamento" in pl:                      _set("Degraus em acostamentos no maximo 5cm")
        else:                                         _set("Degraus")
    if len(pl) >= 20 and pl[:20] == "sinalização vertical":  _set("Demais placas")
    if len(pl) >= 13 and pl[:13] == "demais placas":          _set("Demais placas")
    if pl == _norm("Vandalismo demais placas"):               _set("Demais placas")
    if len(pl) >= 6 and pl[-6:] == "perigo":        _set("Demais placas")
    if len(pl) >= 8 and pl[-8:] == "vertical":      _set("Demais placas")
    if len(pl) >= 10 and pl[:10] == "iluminação":   _set("Dispositivos de Iluminação")
    if len(pl) >= 20 and pl[:20] == "drenagem subterrânea":  _set("Drenagem Subterrânea")
    if len(pl) >= 20 and pl[:20] == "drenagem superficial":  _set("Drenagem Superficial")
    if len(pl) >= 6 and pl[:6] == "grelha":         _set("Drenagem Superficial")
    if len(pl) >= 7 and pl[:7] == "entulho":        _set("Entulho")
    if len(pl) >= 32 and pl[:32] == "vandalismo placas de advertência": _set("Placas - Regulam. / Advertência")
    if len(pl) >= 21 and pl[:21] == "placas de advertência":            _set("Placas - Regulam. / Advertência")
    if len(pl) >= 10 and pl[-10:] == "horizontal":  _set("Sinalização horizontal")
    if len(pl) >= 22 and pl[:22] == "sinalização horizontal": _set("Sinalização horizontal")
    if len(pl) >= 7 and pl[-7:] == "tachões":       _set("Tachas e tachões")
    if len(pl) >= 9 and pl[:9] == "vegetação":      _set("Vegetação")
    # Novas regras — parametrização ArteM IG confirmada
    if pl.startswith("afundamento"):                 _set("Afundamento nas trilhas de rodas")
    if pl.startswith("detrito"):                     _set("Entulho")
    if pl.startswith("inexistência de cerca"):       _set("Cerca")
    if pl.startswith("inexistência de defensa"):     _set("Defensa metálica")
    if pl.startswith("inexistência de ilumina"):     _set("Dispositivos de Iluminação")
    if pl.startswith("inexistência de sinalização h"): _set("Sinalização horizontal")
    if pl.startswith("repintura"):                   _set("Sinalização horizontal")
    if pl.startswith("tacha"):                       _set("Tachas e tachões")
    if pl.startswith("talude"):                      _set("Conservação de terraplenos e contenções")
    if pl.startswith("altura"):                      _set("Vegetação")
    if pl.startswith("inexistência de marco"):       _set("Demais placas")
    if pl.startswith("dispositivos aux"):            _set("Demais placas")
    if pl.startswith("abrigo"):                      _set("Abrigo de passageiros")
    return kcor or ""

casos = [
    ("Abrigo de passageiros danificado",                       "Abrigo de passageiros"),
    ("Afundamento da trilha de roda",                          "Afundamento nas trilhas de rodas"),
    ("Afundamento na trilha de roda",                          "Afundamento nas trilhas de rodas"),
    ("Alambrado danificado",                                   "Alambrado"),
    ("Altura de árvore fora padrão",                           "Vegetação"),
    ("Buracos e/ou panelas na pista de rolamento",             "Buracos e panelas - Emergencial"),
    ("Buracos e/ou panelas no acostamento",                    "Buracos e panelas - Emergencial"),
    ("Cerca de vedação danificada",                            "Cerca"),
    ("Defensa metálica danificada",                            "Defensa metálica"),
    ("Deformações permanentes",                                "Deformação permanente"),
    ("Degrau na pista de rolamento",                           "Degraus"),
    ("Degrau pista de rolamento",                              "Degraus"),
    ("Degrau pista/acostamento",                               "Degraus em acostamentos no maximo 5cm"),
    ("Degrau pista/pista",                                     "Degraus"),
    ("Demais placas danificada",                               "Demais placas"),
    ("Detritos na faixa de domínio",                           "Entulho"),
    ("Detritos na pista",                                      "Entulho"),
    ("Detritos no acostamento",                                "Entulho"),
    ("Dispositivos auxilares (MP/Delineador)",                 "Demais placas"),
    ("Dispositivos auxilares danificados/inexistentes",        "Demais placas"),
    ("Drenagem subterrânea obstruída",                         "Drenagem Subterrânea"),
    ("Drenagem subterrânea obstruída/danificada",              "Drenagem Subterrânea"),
    ("Drenagem superficial danificada",                        "Drenagem Superficial"),
    ("Drenagem superficial obstruída",                         "Drenagem Superficial"),
    ("Drenagem superficial obstruída/danificada",              "Drenagem Superficial"),
    ("Entulho na faixa de domínio",                            "Entulho"),
    ("Entulho na pista",                                       "Entulho"),
    ("Entulho no acostamento",                                 "Entulho"),
    ("Erosão em talude de aterro",                             "Conservação de terraplenos e contenções"),
    ("Erosão em talude de corte",                              "Conservação de terraplenos e contenções"),
    ("Erosão na faixa de domínio",                             "Conservação de terraplenos e contenções"),
    ("Erosão na pista de rolamento",                           "Conservação de terraplenos e contenções"),
    ("Grelha de proteção danificada",                          "Drenagem Superficial"),
    ("Guarda corpo danificado",                                "Barreira rígida"),
    ("Iluminação e instalação elétrica danificada",            "Dispositivos de Iluminação"),
    ("Inexistência de cerca de vedação",                       "Cerca"),
    ("Inexistência de defensa metálica",                       "Defensa metálica"),
    ("Inexistência de elementos refletivos",                   "Barreira rígida"),
    ("Inexistência de iluminação e instalação elétrica",       "Dispositivos de Iluminação"),
    ("Inexistência de marcador de perigo",                     "Demais placas"),
    ("Inexistência de marco quilométrico",                     "Demais placas"),
    ("Inexistência de sinalização horizontal",                 "Sinalização horizontal"),
    ("Inexistência de sinalização vertical",                   "Demais placas"),
    ("Inexistência de tachas e tachões",                       "Tachas e tachões"),
    ("Má condição da caiação",                                 "Caiação"),
    ("Placas de advertência / regulamentação danificada",      "Placas - Regulam. / Advertência"),
    ("Repintura de sinalização horizontal",                    "Sinalização horizontal"),
    ("Sinalização horizontal danificada",                      "Sinalização horizontal"),
    ("Sinalização vertical danificada",                        "Demais placas"),
    ("Tachas e tachões danificados",                           "Tachas e tachões"),
    ("Talude sem revestimento",                                "Conservação de terraplenos e contenções"),
    ("Trilha de roda",                                         "Afundamento nas trilhas de rodas"),
    ("Vandalismo demais placas",                               "Demais placas"),
    ("Vandalismo placas de advertência / regulamentação",      "Placas - Regulam. / Advertência"),
    ("Vegetação fora padrão",                                  "Vegetação"),
]

ok = err = 0
for pat, esperado in casos:
    resultado = mapear(pat)
    if resultado == esperado:
        ok += 1
    else:
        err += 1
        print(f"  ERRO: {pat!r}")
        print(f"         esperado : {esperado!r}")
        print(f"         obtido   : {resultado!r}")

print(f"\nResultado: {ok}/{len(casos)} corretos  |  {err} erros")
