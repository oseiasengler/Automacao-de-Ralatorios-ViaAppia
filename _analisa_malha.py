import pandas as pd

f = r"C:\GeradorARTESP\assets\malha\Eixo Lote 13.xlsx"
df = pd.read_excel(f, sheet_name="Planilha1", header=0)
df.columns = ["Rodovia", "Km", "Sentido", "Latitude", "Longitude"]

print("Rodovias:", sorted(df["Rodovia"].unique()))
print("Sentidos:", sorted(df["Sentido"].unique()))
print("Total linhas:", len(df))
print()

for rod in sorted(df["Rodovia"].unique()):
    sub = df[df["Rodovia"] == rod]
    kms = sub["Km"].tolist()
    sentidos = sorted(sub["Sentido"].unique())
    print(f"{rod}: {len(sub)} pts  km=[{kms[0]}..{kms[-1]}]  sentidos={sentidos}")

print()
print("Primeiras 10 linhas:")
print(df.head(10).to_string())

# Verificar formato do km nos dispositivos
disp = pd.read_excel(
    r"C:\Users\oseia\OneDrive\Ambiente de Trabalho"
    r"\RELATÓRIOS ARTESP\VIA_COLINAS Lote 13\Arquivos\dispositivos_ramos.xlsx"
)
print()
print("Dispositivos - primeiras linhas:")
print(disp[["Dispositivo","Rodovia","km","Ramo","Sentido Pista"]].head(20).to_string())
print()
print("KMs únicos dos dispositivos (SP_075):")
sub_disp = disp[disp["Rodovia"]=="SP_075"][["Dispositivo","km","Sentido Pista"]].drop_duplicates("Dispositivo")
print(sub_disp.to_string())
