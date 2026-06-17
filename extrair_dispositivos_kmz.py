"""
Extrai de lote_13_colinas.kmz:
  - Todos os Dispositivos (SPD_XXX/YYY)
  - Cada Ramo (A, B, C…) com extensão, coordenadas do ponto central
    e coordenadas de início/fim da linha
  - Sentido da pista principal que o ramo serve (NORTE/SUL/LESTE/OESTE)

Saída: dispositivos_ramos.xlsx  (mesma pasta do KMZ)
"""

import re
import zipfile
import xml.etree.ElementTree as ET
from math import radians, sin, cos, sqrt, atan2, degrees
from pathlib import Path

import pandas as pd

KMZ = Path(
    r"C:\Users\oseia\OneDrive\Ambiente de Trabalho"
    r"\RELATÓRIOS ARTESP\VIA_COLINAS Lote 13\Arquivos\lote_13_colinas.kmz"
)
OUT = KMZ.with_name("dispositivos_ramos.xlsx")
NS  = "http://www.opengis.net/kml/2.2"


# ── Helpers gerais ───────────────────────────────────────────────────────────

def haversine_km(lon1, lat1, lon2, lat2):
    """Distância geodésica em km entre dois pontos WGS-84."""
    R = 6371.0
    φ1, φ2 = radians(lat1), radians(lat2)
    dφ = radians(lat2 - lat1)
    dλ = radians(lon2 - lon1)
    a = sin(dφ / 2) ** 2 + cos(φ1) * cos(φ2) * sin(dλ / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def extensao_linha_km(coords_str: str) -> float:
    """Comprimento geodésico de uma LineString KML (soma dos segmentos)."""
    pontos = []
    for token in coords_str.split():
        parts = token.split(",")
        if len(parts) >= 2:
            try:
                pontos.append((float(parts[0]), float(parts[1])))
            except ValueError:
                pass
    total = 0.0
    for i in range(1, len(pontos)):
        total += haversine_km(*pontos[i - 1], *pontos[i])
    return round(total, 3)


def parse_coords_pt(coords_str: str):
    """Retorna (lat, lon) de um ponto KML."""
    parts = coords_str.strip().split(",")
    if len(parts) >= 2:
        return round(float(parts[1]), 7), round(float(parts[0]), 7)
    return None, None


def parse_coords_linha(coords_str: str):
    """Retorna (lat_ini, lon_ini, lat_fim, lon_fim) de uma LineString KML."""
    pontos = []
    for token in coords_str.split():
        parts = token.split(",")
        if len(parts) >= 2:
            try:
                pontos.append((float(parts[1]), float(parts[0])))  # lat, lon
            except ValueError:
                pass
    if not pontos:
        return None, None, None, None
    lat_i, lon_i = round(pontos[0][0], 7),  round(pontos[0][1], 7)
    lat_f, lon_f = round(pontos[-1][0], 7), round(pontos[-1][1], 7)
    return lat_i, lon_i, lat_f, lon_f


def parse_description(desc: str):
    """Extrai rodovia, km_texto, ramo e extensão da description do Point."""
    rodovia  = ""
    km_texto = ""
    ramo     = ""
    ext_km   = None

    linhas = [l.strip() for l in desc.strip().splitlines() if l.strip()]
    for linha in linhas:
        m = re.search(r"km\s+([\d+,\.]+)", linha, re.IGNORECASE)
        if m and not km_texto:
            km_texto = m.group(1).replace(",", "+")
        m = re.match(r"(SP_\d+)", linha)
        if m:
            rodovia = m.group(1)
        m = re.match(r"Ramo\s+(\w+)\s*=\s*([\d,\.]+)\s*km", linha, re.IGNORECASE)
        if m:
            ramo = f"Ramo {m.group(1).upper()}"
            try:
                raw = m.group(2)
                if "," in raw:
                    # "0,174" ou "1.234,5" → remove pontos (milhar), vírgula = decimal
                    val = raw.replace(".", "").replace(",", ".")
                else:
                    # "0.289" → ponto já é decimal
                    val = raw
                ext_km = float(val)
            except ValueError:
                ext_km = None

    return rodovia, km_texto, ramo, ext_km


# ── Sentido da pista ─────────────────────────────────────────────────────────

def _ls_pts(coords_str: str):
    """Parse coordenadas KML → lista de (lon, lat)."""
    pts = []
    for token in coords_str.split():
        parts = token.split(",")
        if len(parts) >= 2:
            try:
                pts.append((float(parts[0]), float(parts[1])))
            except ValueError:
                pass
    return pts


def _bearing(p1, p2) -> float:
    """Rumo de p1→p2 em graus a partir do Norte (0–360)."""
    dlon = p2[0] - p1[0]
    dlat = p2[1] - p1[1]
    return degrees(atan2(dlon, dlat)) % 360


def _cardinal(b: float) -> str:
    if b <= 45 or b > 315:
        return "NORTE"
    elif b <= 135:
        return "LESTE"
    elif b <= 225:
        return "SUL"
    else:
        return "OESTE"


_OPOSTO = {"NORTE": "SUL", "SUL": "NORTE", "LESTE": "OESTE", "OESTE": "LESTE"}


def _dist_seg(px, py, x1, y1, x2, y2) -> float:
    """Distância euclidiana de (px,py) ao segmento (x1,y1)-(x2,y2)."""
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5
    t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
    return ((px - x1 - t * dx) ** 2 + (py - y1 - t * dy) ** 2) ** 0.5


def _dist_ls(px, py, pts) -> float:
    """Distância mínima de (px,py) a uma LineString."""
    if len(pts) < 2:
        return float("inf")
    return min(
        _dist_seg(px, py, pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1])
        for i in range(1, len(pts))
    )


def _seg_mais_proximo(px, py, pts) -> int:
    """Índice i do segmento (pts[i-1], pts[i]) mais próximo de (px,py)."""
    best_i, best_d = 1, float("inf")
    for i in range(1, len(pts)):
        d = _dist_seg(px, py, pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1])
        if d < best_d:
            best_d, best_i = d, i
    return best_i


def load_road_data(root) -> dict:
    """
    Carrega as LineStrings das rodovias principais do folder Traçado.

    Retorna dict  rodovia → info, onde info é:
      {'tipo': 'cross_product', 'pts': [...], 'RIGHT': 'NORTE', 'LEFT': 'SUL'}
      {'tipo': 'nearest_ls',   'pistas': {'NORTE': [...], 'SUL': [...]}}
    """
    tracado = None
    for f in root.iter(f"{{{NS}}}Folder"):
        n = f.findtext(f"{{{NS}}}name", "").strip()
        if "Tra" in n and "ado" in n:
            tracado = f
            break
    if tracado is None:
        return {}

    road_data = {}
    for sp_folder in tracado:
        if sp_folder.tag != f"{{{NS}}}Folder":
            continue
        sp_name = sp_folder.findtext(f"{{{NS}}}name", "").strip()

        # Apenas Placemarks diretos (não subpastas) com LineString
        pms = []
        for child in sp_folder:
            if child.tag != f"{{{NS}}}Placemark":
                continue
            ls_el = child.find(f".//{{{NS}}}LineString/{{{NS}}}coordinates")
            if ls_el is None or not (ls_el.text or "").strip():
                continue
            pts = _ls_pts(ls_el.text)
            pm_name = child.findtext(f"{{{NS}}}name", "").strip()
            if len(pts) >= 2:
                pms.append((pm_name, pts))

        if not pms:
            continue

        if len(pms) == 1:
            # Eixo único → produto vetorial para determinar o lado
            _, pts = pms[0]
            b   = _bearing(pts[0], pts[-1])
            fwd = _cardinal(b)
            road_data[sp_name] = {
                "tipo":  "cross_product",
                "pts":   pts,
                "RIGHT": fwd,           # lado direito do sentido do eixo
                "LEFT":  _OPOSTO[fwd],  # lado esquerdo
            }
        else:
            # Múltiplas pistas → pista mais próxima
            pistas: dict[str, list] = {}
            for pm_name, pts in pms:
                b     = _bearing(pts[0], pts[-1])
                label = _cardinal(b)
                # Em caso de colisão de rótulo, mantém o primeiro (mais longo)
                if label not in pistas or len(pts) > len(pistas[label]):
                    pistas[label] = pts
            if pistas:
                road_data[sp_name] = {"tipo": "nearest_ls", "pistas": pistas}

    return road_data


def calc_sentido(lon_p, lat_p, rodovia: str, road_data: dict) -> str:
    """
    Retorna o sentido da pista (NORTE/SUL/LESTE/OESTE) para o ponto (lon_p, lat_p).

    Para eixo único: usa produto vetorial em relação ao segmento mais próximo.
    Para múltiplas pistas: usa a pista (LineString) mais próxima.
    """
    if lon_p is None or lat_p is None or rodovia not in road_data:
        return ""
    info = road_data[rodovia]

    if info["tipo"] == "cross_product":
        pts = info["pts"]
        si  = _seg_mais_proximo(lon_p, lat_p, pts)
        x1, y1 = pts[si - 1]
        x2, y2 = pts[si]
        # Produto vetorial 2D: (p2-p1) × (P-p1)
        # positivo → P à ESQUERDA do sentido p1→p2
        cross = (x2 - x1) * (lat_p - y1) - (y2 - y1) * (lon_p - x1)
        return info["RIGHT"] if cross < 0 else info["LEFT"]

    elif info["tipo"] == "nearest_ls":
        best_label, best_d = "", float("inf")
        for label, pts in info["pistas"].items():
            d = _dist_ls(lon_p, lat_p, pts)
            if d < best_d:
                best_d, best_label = d, label
        return best_label

    return ""


def ponto_para_sentido(
    lon_i, lat_i, lon_f, lat_f, lon_pt, lat_pt,
    rodovia: str, road_data: dict,
) -> str:
    """
    Escolhe o endpoint do ramo mais próximo da rodovia e calcula o sentido.
    Fallback para o ponto central (lon_pt, lat_pt) se não houver LineString.
    """
    info = road_data.get(rodovia)
    if not info:
        return ""

    def _dist_any(lon, lat):
        if info["tipo"] == "cross_product":
            return _dist_ls(lon, lat, info["pts"])
        return min(_dist_ls(lon, lat, pts) for pts in info["pistas"].values())

    candidates = []
    if lon_i is not None and lat_i is not None:
        candidates.append((lon_i, lat_i))
    if lon_f is not None and lat_f is not None:
        candidates.append((lon_f, lat_f))

    if not candidates:
        # Sem LineString: usa ponto central
        return calc_sentido(lon_pt, lat_pt, rodovia, road_data)
    if len(candidates) == 1:
        lon_p, lat_p = candidates[0]
    else:
        d0 = _dist_any(*candidates[0])
        d1 = _dist_any(*candidates[1])
        lon_p, lat_p = candidates[0] if d0 <= d1 else candidates[1]

    return calc_sentido(lon_p, lat_p, rodovia, road_data)


# ── Leitura do KMZ ──────────────────────────────────────────────────────────

with zipfile.ZipFile(KMZ) as z:
    kml_bytes = z.read("doc.kml")

root = ET.fromstring(kml_bytes.decode("utf-8", errors="ignore"))

# Carregar dados das rodovias principais
road_data = load_road_data(root)
print("Rodovias carregadas:")
for rod, info in road_data.items():
    if info["tipo"] == "cross_product":
        pts = info["pts"]
        print(f"  {rod}: eixo único ({len(pts)} pts)  "
              f"RIGHT={info['RIGHT']}  LEFT={info['LEFT']}")
    else:
        pistas_str = ", ".join(f"{k}({len(v)}pts)" for k, v in info["pistas"].items())
        print(f"  {rod}: {len(info['pistas'])} pistas  [{pistas_str}]")

# Localizar pasta "Dispositivos"
disp_folder = None
for f in root.iter(f"{{{NS}}}Folder"):
    if f.findtext(f"{{{NS}}}name", "").strip() == "Dispositivos":
        disp_folder = f
        break

if disp_folder is None:
    raise RuntimeError("Pasta 'Dispositivos' não encontrada no KMZ.")

# ── Extração ────────────────────────────────────────────────────────────────

rows = []

# Nível: Dispositivos → SP_XXX → SPD_XXX/YYY
for rodovia_folder in disp_folder:
    if rodovia_folder.tag != f"{{{NS}}}Folder":
        continue
    rodovia_nome = rodovia_folder.findtext(f"{{{NS}}}name", "").strip()

    for spd_folder in rodovia_folder:
        if spd_folder.tag != f"{{{NS}}}Folder":
            continue
        spd_nome = spd_folder.findtext(f"{{{NS}}}name", "").strip()

        linhas_por_ramo = {}  # nome_ramo → coords_str da linha
        pontos_por_ramo = {}  # nome_ramo → (desc, coords_str do ponto)

        for pm in spd_folder.iter(f"{{{NS}}}Placemark"):
            pm_nome = pm.findtext(f"{{{NS}}}name", "").strip().upper()
            desc    = pm.findtext(f"{{{NS}}}description", "")

            ls = pm.find(f".//{{{NS}}}LineString")
            pt = pm.find(f".//{{{NS}}}Point")

            if ls is not None:
                coords = ls.findtext(f"{{{NS}}}coordinates", "")
                linhas_por_ramo[pm_nome] = coords

            elif pt is not None:
                coords = pt.findtext(f"{{{NS}}}coordinates", "")
                pontos_por_ramo[pm_nome] = (desc, coords)

        todos_ramos = set(linhas_por_ramo) | set(pontos_por_ramo)
        for ramo_key in sorted(todos_ramos):
            desc, pt_coords = pontos_por_ramo.get(ramo_key, ("", ""))
            ls_coords       = linhas_por_ramo.get(ramo_key, "")

            rodovia_desc, km_texto, ramo_desc, ext_desc = parse_description(desc)

            # Extensão: prefere a da description; fallback: calcula da linha
            if ext_desc is not None:
                ext_km = ext_desc
            elif ls_coords:
                ext_km = extensao_linha_km(ls_coords)
            else:
                ext_km = None

            # Ponto central
            lat_pt, lon_pt = parse_coords_pt(pt_coords) if pt_coords else (None, None)

            # Início / Fim da linha
            lat_i, lon_i, lat_f, lon_f = (
                parse_coords_linha(ls_coords) if ls_coords else (None, None, None, None)
            )

            # Rodovia efetiva (da description ou do folder)
            rodovia_ef = rodovia_desc or rodovia_nome

            # Sentido da pista
            sentido = ponto_para_sentido(
                lon_i, lat_i, lon_f, lat_f, lon_pt, lat_pt,
                rodovia_ef, road_data,
            )

            rows.append({
                "Dispositivo":    spd_nome,
                "Rodovia":        rodovia_ef,
                "km":             km_texto,
                "Ramo":           ramo_desc or ramo_key.title(),
                "Extensão (km)":  ext_km,
                "Sentido Pista":  sentido,
                "Lat (ponto)":    lat_pt,
                "Lon (ponto)":    lon_pt,
                "Lat início":     lat_i,
                "Lon início":     lon_i,
                "Lat fim":        lat_f,
                "Lon fim":        lon_f,
            })

# ── Saída ───────────────────────────────────────────────────────────────────

df = pd.DataFrame(rows)
df.to_excel(OUT, index=False, sheet_name="Dispositivos_Ramos")

print(f"\nExtraídos {len(df)} ramos de {df['Dispositivo'].nunique()} dispositivos.")
print(f"Salvo em: {OUT}")
print(df[["Dispositivo", "km", "Ramo", "Extensão (km)", "Sentido Pista"]].to_string(index=False))
