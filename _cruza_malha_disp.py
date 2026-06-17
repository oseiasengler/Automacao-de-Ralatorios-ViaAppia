"""
Cruza dispositivos_ramos.xlsx com Eixo Lote 13.xlsx
para encontrar as linhas corretas de inserção.
"""
import pandas as pd
import numpy as np
from pathlib import Path

MALHA = r"C:\GeradorARTESP\assets\malha\Eixo Lote 13.xlsx"
DISP  = (
    r"C:\Users\oseia\OneDrive\Ambiente de Trabalho"
    r"\RELATÓRIOS ARTESP\VIA_COLINAS Lote 13\Arquivos\dispositivos_ramos.xlsx"
)

# ── Carregar malha ───────────────────────────────────────────────────────────
malha = pd.read_excel(MALHA, header=0)
malha.columns = ["Rodovia", "Km", "Sentido", "Latitude", "Longitude"]

# Converter km da malha para metro numérico (ex: "15+400" → 15400)
def km_para_m(k):
    k = str(k).strip()
    if "+" in k:
        partes = k.split("+")
        return int(partes[0]) * 1000 + int(partes[1])
    return int(k)

malha["Km_m"] = malha["Km"].apply(km_para_m)

# ── Carregar dispositivos ────────────────────────────────────────────────────
disp = pd.read_excel(DISP)

# Normalizar rodovia: SP_075 → SP0000075 / SP_127 → SP0000127 etc.
def norm_rod(r):
    r = str(r).strip()
    if r.startswith("SP_"):
        num = r[3:]
        return "SP" + num.zfill(7)
    return r

# Normalizar sentido: NORTE → Norte, SUL → Sul etc.
def norm_sent(s):
    return str(s).strip().capitalize()

disp["Rod_mal"] = disp["Rodovia"].apply(norm_rod)
disp["Sent_mal"] = disp["Sentido Pista"].apply(norm_sent)

# km numérico
disp["Km_m"] = disp["km"].apply(lambda k: km_para_m(k) if pd.notna(k) and str(k).strip() else np.nan)

# ── Por dispositivo único, encontrar linha mais próxima na malha ─────────────
# Agrupa por Dispositivo + Sentido (um dispositivo pode ter ramos NORTE e SUL)
chaves = (
    disp.dropna(subset=["Km_m"])
    .groupby(["Dispositivo", "Rod_mal", "Sent_mal", "km", "Km_m"])
    .size()
    .reset_index(name="n_ramos")
)

resultado = []
for _, row in chaves.iterrows():
    rod = row["Rod_mal"]
    sent = row["Sent_mal"]
    km_num = row["Km_m"]

    sub_malha = malha[(malha["Rodovia"] == rod) & (malha["Sentido"] == sent)]
    if sub_malha.empty:
        # Tentar sem sentido (SP_102 não está no road_data)
        sub_malha = malha[malha["Rodovia"] == rod]

    if sub_malha.empty:
        idx_malha = None
        km_malha  = None
        delta_m   = None
        lat_mal   = None
        lon_mal   = None
    else:
        diffs = (sub_malha["Km_m"] - km_num).abs()
        pos   = diffs.idxmin()
        idx_malha = int(pos)
        km_malha  = malha.loc[pos, "Km"]
        delta_m   = int(diffs.loc[pos])
        lat_mal   = malha.loc[pos, "Latitude"]
        lon_mal   = malha.loc[pos, "Longitude"]

    resultado.append({
        "Dispositivo":   row["Dispositivo"],
        "Rodovia":       row["Rod_mal"],
        "km_disp":       row["km"],
        "Sentido":       sent,
        "n_ramos":       row["n_ramos"],
        "linha_malha":   idx_malha,   # índice 0-based da linha no DataFrame (linha Excel = +2)
        "km_malha":      km_malha,
        "delta_m":       delta_m,
        "Lat_malha":     lat_mal,
        "Lon_malha":     lon_mal,
    })

df_res = pd.DataFrame(resultado)
df_res["linha_excel"] = df_res["linha_malha"].apply(
    lambda x: int(x) + 2 if pd.notna(x) else None   # +1 header +1 base-1→base-1
)

print(df_res.to_string(index=False))
print(f"\nTotal dispositivo×sentido mapeados: {len(df_res)}")
print(f"Não encontrados: {df_res['linha_malha'].isna().sum()}")
print(f"Match exato (delta=0): {(df_res['delta_m']==0).sum()}")
print(f"Match com delta 1-10m: {((df_res['delta_m']>0)&(df_res['delta_m']<=10)).sum()}")
print(f"Match com delta >10m:  {(df_res['delta_m']>10).sum()}")

# Salvar resultado
OUT = Path(MALHA).parent / "mapeamento_dispositivos_malha.xlsx"
df_res.to_excel(OUT, index=False)
print(f"\nSalvo em: {OUT}")
