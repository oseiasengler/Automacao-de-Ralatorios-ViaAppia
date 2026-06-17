"""
Insere uma linha por ramo do dispositivos_ramos.xlsx na posição correta
da malha Eixo Lote 13.xlsx, mantendo a ordem por km.

Colunas originais da malha : Rodovia, Km, Sentido, Latitude, Longitude
Colunas extras (só ramos)  : Dispositivo, Ramo, Extensão_km,
                             Lat_inicio, Lon_inicio, Lat_fim, Lon_fim
"""

import pandas as pd
import numpy as np
from pathlib import Path

MALHA = r"C:\GeradorARTESP\assets\malha\Eixo Lote 13.xlsx"
DISP  = (
    r"C:\Users\oseia\OneDrive\Ambiente de Trabalho"
    r"\RELATÓRIOS ARTESP\VIA_COLINAS Lote 13\Arquivos\dispositivos_ramos.xlsx"
)
OUT = Path(MALHA).parent / "Eixo Lote 13 com Dispositivos_final.xlsx"

# ── Sentidos confirmados manualmente via descrição do KMZ ────────────────────
# chave: (Dispositivo, Ramo)  →  sentido ("Norte"/"Sul"/"Leste"/"Oeste")
SENTIDO_OVERRIDE = {
    # SPD_006/102 – SPI_102/300 km 6+620
    ("SPD_006/102", "Ramo A"): "Oeste",
    ("SPD_006/102", "Ramo B"): "Leste",
    ("SPD_006/102", "Ramo C"): "Leste",
    ("SPD_006/102", "Ramo D"): "Oeste",
    ("SPD_006/102", "Ramo E"): "Oeste",
    ("SPD_006/102", "Ramo F"): "Oeste",
    ("SPD_006/102", "Ramo G"): "Leste",
    ("SPD_006/102", "Ramo H"): "Leste",
    # SPD_035/075 – km 35+500 (Ramo B: KMZ=Norte, geométrico=Sul incorreto)
    ("SPD_035/075", "Ramo B"): "Norte",
    # SPD_043/075 – km 43+850 (Ramo D: KMZ=Norte, geométrico=Sul incorreto)
    ("SPD_043/075", "Ramo D"): "Norte",
}

# Para ramos com nome duplicado no mesmo dispositivo, usa extensão como chave
# chave: (Dispositivo, Ramo, round(Extensão_km, 3))
SENTIDO_OVERRIDE_EXT = {
    # SPD_007/102 – SPI_102/300 km 7+868
    ("SPD_007/102", "Ramo A", 0.567): "Leste",
    ("SPD_007/102", "Ramo A", 0.505): "Oeste",
    ("SPD_007/102", "Ramo A", 0.470): "Oeste",
    ("SPD_007/102", "Ramo D", 0.493): "Leste",
    # SPD_038/075 – km 38+850 (dois "Ramo D"; 0.486 é Norte, 0.040 é Norte geométrico)
    ("SPD_038/075", "Ramo D", 0.486): "Norte",
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def km_para_m(k):
    k = str(k).strip()
    if "+" in k:
        p = k.split("+")
        return int(p[0]) * 1000 + int(p[1])
    try:
        return int(k)
    except ValueError:
        return np.nan


def norm_rod(r):
    r = str(r).strip()
    if r in ("SP_102", "SPI_102/300"):
        return "SPI102300"
    if r.startswith("SP_"):
        return "SP" + r[3:].zfill(7)
    return r


def norm_sent(s):
    return {"NORTE": "Norte", "SUL": "Sul",
            "LESTE": "Leste", "OESTE": "Oeste"}.get(str(s).strip().upper(), "")


# ── Carregar malha ───────────────────────────────────────────────────────────
print("Carregando malha...")
malha = pd.read_excel(MALHA, header=0)
malha.columns = ["Rodovia", "Km", "Sentido", "Latitude", "Longitude"]
malha["Km_m"]        = malha["Km"].apply(km_para_m)
malha["_tipo"]       = "Malha"
malha["Dispositivo"] = np.nan
malha["Ramo"]        = np.nan
malha["Extensão_km"] = np.nan
malha["Lat_inicio"]  = np.nan
malha["Lon_inicio"]  = np.nan
malha["Lat_fim"]     = np.nan
malha["Lon_fim"]     = np.nan

# Preservar a ordem de blocos (Rodovia × Sentido) do arquivo original
ordem_grupos = (
    malha.drop_duplicates(subset=["Rodovia", "Sentido"], keep="first")
    [["Rodovia", "Sentido"]]
    .reset_index(drop=True)
)
ordem_grupos["_grupo_ord"] = range(len(ordem_grupos))
malha = malha.merge(ordem_grupos, on=["Rodovia", "Sentido"], how="left")

# ── Carregar dispositivos ────────────────────────────────────────────────────
print("Carregando dispositivos...")
disp = pd.read_excel(DISP)

# ── Construir linhas a inserir ───────────────────────────────────────────────
novas     = []
sem_match = []

for _, row in disp.iterrows():
    disp_nome = str(row["Dispositivo"])
    ramo_nome = str(row["Ramo"])
    rod_mal   = norm_rod(row["Rodovia"])
    km_str    = str(row["km"]).strip() if pd.notna(row["km"]) else ""
    km_num    = km_para_m(km_str) if km_str else np.nan

    # Sentido: override simples → override por extensão → coluna geométrica
    sent_raw = SENTIDO_OVERRIDE.get((disp_nome, ramo_nome), "")
    if not sent_raw:
        try:
            ext_val = round(float(row.get("Extensão (km)") or 0), 3)
        except (TypeError, ValueError):
            ext_val = 0.0
        sent_raw = SENTIDO_OVERRIDE_EXT.get((disp_nome, ramo_nome, ext_val), "")
    if not sent_raw:
        sent_raw = norm_sent(row.get("Sentido Pista", ""))

    if not sent_raw or pd.isna(km_num):
        sem_match.append(f"{disp_nome} / {ramo_nome}  (sem sentido ou km)")
        continue

    grupo = ordem_grupos[
        (ordem_grupos["Rodovia"] == rod_mal) & (ordem_grupos["Sentido"] == sent_raw)
    ]
    if grupo.empty:
        sem_match.append(
            f"{disp_nome} / {ramo_nome}  ({rod_mal}/{sent_raw} ausente na malha)"
        )
        continue

    lat = row.get("Lat (ponto)") if pd.notna(row.get("Lat (ponto)")) else row.get("Lat início")
    lon = row.get("Lon (ponto)") if pd.notna(row.get("Lon (ponto)")) else row.get("Lon início")

    novas.append({
        "Rodovia":     rod_mal,
        "Km":          km_str,
        "Sentido":     sent_raw,
        "Latitude":    lat,
        "Longitude":   lon,
        "Km_m":        km_num,
        "_tipo":       "Dispositivo",
        "Dispositivo": disp_nome,
        "Ramo":        ramo_nome,
        "Extensão_km": row.get("Extensão (km)"),
        "Lat_inicio":  row.get("Lat início"),
        "Lon_inicio":  row.get("Lon início"),
        "Lat_fim":     row.get("Lat fim"),
        "Lon_fim":     row.get("Lon fim"),
        "_grupo_ord":  int(grupo["_grupo_ord"].iloc[0]),
    })

df_novas = pd.DataFrame(novas)
print(f"Ramos a inserir: {len(df_novas)}  |  sem match: {len(sem_match)}")

# ── Combinar e reordenar ─────────────────────────────────────────────────────
combinado = pd.concat([malha, df_novas], ignore_index=True)
combinado["_tipo_ord"] = combinado["_tipo"].map({"Malha": 0, "Dispositivo": 1})
combinado = combinado.sort_values(
    ["_grupo_ord", "Km_m", "_tipo_ord"], kind="stable"
).reset_index(drop=True)

# ── Exportar ─────────────────────────────────────────────────────────────────
colunas_saida = [
    "Rodovia", "Km", "Sentido", "Latitude", "Longitude",
    "Dispositivo", "Ramo", "Extensão_km",
    "Lat_inicio", "Lon_inicio", "Lat_fim", "Lon_fim",
]
df_out = combinado[colunas_saida].copy()

malha_rows = df_out["Dispositivo"].isna().sum()
disp_rows  = df_out["Dispositivo"].notna().sum()
print(f"Linhas malha: {malha_rows}  |  Ramos inseridos: {disp_rows}  |  Total: {len(df_out)}")

print("Salvando...")
with pd.ExcelWriter(OUT, engine="openpyxl") as writer:
    df_out.to_excel(writer, index=False, sheet_name="Malha+Dispositivos")
print(f"Salvo em: {OUT}")

# Verificar amostra SPD_035/075
print()
print("Amostra SPD_035/075 km 35+500:")
s = combinado[combinado["Dispositivo"] == "SPD_035/075"][
    ["Km", "Sentido", "Ramo", "Extensão_km"]
]
print(s.to_string(index=False))

if sem_match:
    print(f"\nNao inseridos ({len(sem_match)}):")
    for msg in sem_match:
        print(f"  {msg}")
