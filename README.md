# Inventário de Drenagem Rodoviária

App de campo **offline-first** para inventário de drenagem superficial, profunda e
transversal (bueiros) em rodovias. Coleta no celular sem sinal e sincroniza depois.

## Arquitetura

```
catálogo (fonte única da verdade)
        │  define tipos + atributos por tipo
        ├──────────────► backend valida  (catalogo_dispositivos.py)
        └──────────────► PWA gera o form  (catalogo.js)

PWA (campo, offline)  ──/sync──►  FastAPI  ──►  Postgres/SQLite
   IndexedDB                       last-write-wins        export GeoJSON
```

O **catálogo** (`backend/catalogo_dispositivos.py`) é o coração: define cada tipo de
dispositivo (DNIT) e seus atributos. Ele valida no servidor *e* gera o formulário
dinâmico no PWA. Adicionar um tipo novo = editar o catálogo e rodar `python catalogo_dispositivos.py`
(regenera `pwa/catalogo.js`). Nenhum form precisa ser mexido à mão.

### Tipos cobertos
- **Superficial:** canaleta, sarjeta, valeta de proteção, meio-fio, descida d'água
  (rápida / **degraus = escada hidráulica**), dissipador de energia, caixa coletora, saída d'água
- **Profunda:** dreno longitudinal, espinha-de-peixe, DHP, colchão drenante
- **Transversal:** bueiro tubular (BSTC/BDTC/BTTC), bueiro celular, ala/boca

Atributos específicos por tipo (Ø, seção, nº de degraus, nº de linhas, obstrução %, etc.)
ficam em JSONB validado — sem colunas nulas.

## Rodar

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload          # http://localhost:8000/docs
```
Trocar pra Postgres: `export DATABASE_URL=postgresql://user:senha@host/db`

### PWA
Precisa ser servido por HTTP (GPS e service worker exigem origem segura/localhost):
```bash
cd pwa
python -m http.server 5500         # abra http://localhost:5500
```
No celular: acesse pela rede local ou faça deploy (Render/Netlify). "Adicionar à
tela inicial" instala como app. Primeira sincronização pede a URL do backend.

## Sincronização (offline-first)
- Cada registro recebe **UUID no cliente** → cria offline sem colisão.
- `POST /sync` manda pendentes + `last_sync`; conflito resolvido por `updated_at`
  (**last-write-wins**); resposta traz mudanças do servidor (outros aparelhos).
- Soft-delete (`deleted`) propaga remoções.

## Testes
```bash
# backend (CRUD, validação, sync com conflito, GeoJSON)
cd backend && python -c "import main"   # + ver bloco de teste no histórico

# PWA (DOM headless: form dinâmico, condicional, validação, GPS, persistência)
cd pwa && npm install jsdom fake-indexeddb && node test_pwa.mjs
```

## Próximos passos sugeridos
1. **Upload de fotos** — hoje a foto fica local (sync manda só a referência).
   Adicionar `POST /fotos` multipart + storage (S3/R2) e enviar no sync.
2. **Mapa de coleta** — Leaflet offline com os pontos já coletados sobre a malha.
3. **Snap à malha GPS** — reaproveitar seu `malha_gps.py` pra validar km×coordenada
   no momento da coleta (KDTree).
4. **Auth** — token por inspetor/concessionária antes do `/sync`.
5. **Export KMZ** — direção colorida por estado de conservação (como no Lote 21).
