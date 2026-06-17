"""
Lê os 42 Data_ de "Zebrados norte", separa as 10 melhores leituras
por tipo (Zebrado / Canalização) usando o campo Seccionado do LOG.txt,
e gera um Excel com duas abas.

Seccionado = 0  →  Zebrado
Seccionado = 1  →  Canalização
"""

import re
from pathlib import Path

import pandas as pd

BASE = Path(r"X:\SP075\Zebrados norte")
OUT  = BASE / "leituras_top10.xlsx"

# Índices das colunas no LOG.txt (0-based, ordem do cabeçalho)
IDX = {
    "Lat":        1,   # Lat Inicial
    "Lon":        2,   # Lon Inicial
    "FotoIni":    4,   # Foto ID Inicio
    "RL":         5,
    "RL_DP":      6,
    "Largura":   12,
    "Marco":     14,
    "Seccionado":19,
}

COLUNAS_SAIDA = {
    "Data":       "Data",
    "Item":       "Item",
    "RL":         "RL (mcd.lx-1.m-2)",
    "RL_DP":      "RL Desvio Padrao",
    "Lat":        "Latitude",
    "Lon":        "Longitude",
    "Marco":      "Marco km",
    "Largura":    "Largura",
    "FotoIni":    "Foto ID",
}


def ler_observation(dat: Path) -> str:
    try:
        raw = dat.read_bytes().decode("latin-1", errors="ignore")
        m = re.search(r'Observation = "([^"]*)"', raw)
        return m.group(1).strip() if m else ""
    except Exception:
        return ""


def ler_log(log: Path) -> pd.DataFrame:
    df = pd.read_csv(log, sep="\t", header=0, decimal=",", encoding="latin-1")
    cols = df.columns.tolist()
    rename = {cols[i]: nome for nome, i in IDX.items()}
    df = df.rename(columns=rename)
    df[list(IDX.keys())] = df[list(IDX.keys())].apply(pd.to_numeric, errors="coerce")
    return df


linhas_zeb = []
linhas_can = []

dirs = sorted(
    [d for d in BASE.iterdir() if d.is_dir() and d.name.startswith("Data_")],
    key=lambda p: int(p.name.split("_")[1]),
)

for d in dirs:
    item = ler_observation(d / "SOURCE" / "Data.dat")

    try:
        df = ler_log(d / "LOG" / "LOG.txt")
    except Exception as e:
        print(f"[ERRO] {d.name}: {e}")
        continue

    validos = df[df["RL"] > 0].copy()
    validos["RL"]    = validos["RL"].round().astype(int)
    validos["RL_DP"] = validos["RL_DP"].round().astype(int)
    validos["Data"] = d.name
    validos["Item"] = item

    cols = list(COLUNAS_SAIDA.keys())

    zeb = validos[validos["Seccionado"] == 0].nlargest(10, "RL")[cols]
    can = validos[validos["Seccionado"] == 1].nlargest(10, "RL")[cols]

    linhas_zeb.append(zeb)
    linhas_can.append(can)

    print(
        f"{d.name}  item={item or '(vazio)':20s}  "
        f"zeb={len(zeb):2d}  can={len(can):2d}"
    )

df_zeb = pd.concat(linhas_zeb, ignore_index=True).rename(columns=COLUNAS_SAIDA)
df_can = pd.concat(linhas_can, ignore_index=True).rename(columns=COLUNAS_SAIDA)

with pd.ExcelWriter(OUT, engine="openpyxl") as writer:
    df_zeb.to_excel(writer, sheet_name="Zebrados",    index=False)
    df_can.to_excel(writer, sheet_name="Canalizacao", index=False)

print(f"\nSalvo em: {OUT}")
print(f"Zebrados:    {len(df_zeb)} linhas")
print(f"Canalizacao: {len(df_can)} linhas")
