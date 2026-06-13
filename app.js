/* global CATALOGO */
/* ============================================================
   Inventário de Drenagem — app de campo offline-first
   Armazena local em IndexedDB; sincroniza em lote com /sync.
   ============================================================ */
"use strict";

const CAT = window.CATALOGO;
const DB_NAME = "drenagem", DB_VER = 1;
const ESTADOS     = CAT.estados_conservacao;
const TIPOS       = CAT.dispositivos;
const GRUPOS_META = CAT.grupos_meta;
const tipoPorChave = Object.fromEntries(TIPOS.map(t => [t.tipo, t]));

let travessia = null; // ID da travessia ativa (persiste entre resets de form)

let db, estado = {
  id: null, grupo: null, sentido: "Norte", lado: "Lado Direito", estadoConserv: null,
  gps1: null, gps2: null, fotos: [],
  id_rede: null, conectado_a: null,
  direcao_coleta: "Direta"
};

function parseKm(str) {
  const s = String(str).trim();
  const m = s.match(/^(\d+)\+(\d{1,3})$/);
  if (m) return Number(m[1]) + Number(m[2]) / 1000;
  return Number(s.replace(",", "."));
}

function formatKm(num) {
  const km = Math.floor(num);
  const metros = Math.round((num - km) * 1000);
  return `${km}+${String(metros).padStart(3, "0")}`;
}

/* ---------- travessia & conectividade ---------- */
function distM(lat1, lon1, lat2, lon2) {
  const R = 6371000, r = Math.PI / 180;
  const dLat = (lat2 - lat1) * r, dLon = (lon2 - lon1) * r;
  const a = Math.sin(dLat / 2) ** 2 + Math.cos(lat1 * r) * Math.cos(lat2 * r) * Math.sin(dLon / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

function gerarIdTravessia() {
  const kmStr = $("#km_ini").value.trim();
  const km = kmStr ? Math.floor(parseKm(kmStr)) : 0;
  const seq = String(Math.floor(Math.random() * 98) + 1).padStart(2, "0");
  return `TR-KM${String(km).padStart(3, "0")}-${seq}`;
}

function iniciarTravessia() {
  travessia = gerarIdTravessia();
  estado.id_rede = travessia;
  $("#travessiaLabel").textContent = travessia;
  $("#cardTravInativo").classList.add("hidden");
  $("#cardTravAtivo").classList.remove("hidden");
  atualizaConectividadeUI();
}

function finalizarTravessia() {
  travessia = null;
  estado.id_rede = null;
  $("#cardTravAtivo").classList.add("hidden");
  $("#cardTravInativo").classList.remove("hidden");
  atualizaConectividadeUI();
}

function atualizaConectividadeUI() {
  $("#idRedeDisplay").textContent = estado.id_rede || "—";
  if (!estado.conectado_a) { $("#conectadoDisplay").textContent = "não vinculado"; return; }
  idbGet("registros", estado.conectado_a).then(r => {
    if (r) {
      const t = tipoPorChave[r.tipo];
      $("#conectadoDisplay").textContent = `${t ? t.rotulo : r.tipo} · km ${formatKm(r.km_ini)} · ${r.lado}`;
    } else {
      $("#conectadoDisplay").textContent = "não vinculado";
    }
  });
}

async function vincularAnterior() {
  const lista = $("#vincularLista");
  lista.classList.remove("hidden");
  lista.innerHTML = "<small style='color:var(--muted)'>Buscando...</small>";

  const todos = await idbAll("registros");
  let candidatos = todos
    .filter(r => !r.deleted && r.id !== estado.id)
    .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));

  if (estado.gps1) {
    const { lat, lon } = estado.gps1;
    const proximos = candidatos.filter(r => r.lat_ini != null && distM(lat, lon, r.lat_ini, r.lon_ini) <= 300);
    candidatos = proximos.length ? proximos.slice(0, 8) : candidatos.slice(0, 8);
  } else {
    candidatos = candidatos.slice(0, 8);
  }

  if (!candidatos.length) {
    lista.innerHTML = "<small style='color:var(--muted)'>Nenhum ativo encontrado.</small>";
    return;
  }

  lista.innerHTML = candidatos.map(r => {
    const t = tipoPorChave[r.tipo];
    const label = t ? t.rotulo : r.tipo;
    const mins = Math.round((Date.now() - new Date(r.updated_at)) / 60000);
    const tempo = mins < 60 ? `há ${mins} min` : `há ${Math.round(mins / 60)}h`;
    return `<button class="vincular-item" data-id="${r.id}" data-label="${label} · ${r.lado}">
      <b>${label}</b> · km ${formatKm(r.km_ini)} · ${r.lado}<br>
      <small>${tempo} · ${r.sentido}</small>
    </button>`;
  }).join("");

  lista.querySelectorAll(".vincular-item").forEach(btn => {
    btn.onclick = () => selecionarVinculo(btn.dataset.id, btn.dataset.label);
  });
}

function selecionarVinculo(id, label) {
  estado.conectado_a = id;
  $("#conectadoDisplay").textContent = label;
  $("#vincularLista").classList.add("hidden");
}

/* ---------- IndexedDB ---------- */
function openDB() {
  return new Promise((res, rej) => {
    const r = indexedDB.open(DB_NAME, DB_VER);
    r.onupgradeneeded = e => {
      const d = e.target.result;
      if (!d.objectStoreNames.contains("registros"))
        d.createObjectStore("registros", { keyPath: "id" });
      if (!d.objectStoreNames.contains("config"))
        d.createObjectStore("config", { keyPath: "k" });
    };
    r.onsuccess = e => res(e.target.result);
    r.onerror = e => rej(e.target.error);
  });
}
function tx(store, mode = "readonly") { return db.transaction(store, mode).objectStore(store); }
function idbPut(store, v) { return new Promise((res, rej) => { const r = tx(store, "readwrite").put(v); r.onsuccess = res; r.onerror = () => rej(r.error); }); }
function idbGet(store, k) { return new Promise((res, rej) => { const r = tx(store).get(k); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); }); }
function idbAll(store) { return new Promise((res, rej) => { const r = tx(store).getAll(); r.onsuccess = () => res(r.result || []); r.onerror = () => rej(r.error); }); }
function idbDel(store, k) { return new Promise((res, rej) => { const r = tx(store, "readwrite").delete(k); r.onsuccess = res; r.onerror = () => rej(r.error); }); }

/* ---------- util ---------- */
const $ = s => document.querySelector(s);
const uuid = () => (crypto.randomUUID ? crypto.randomUUID()
  : "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, c => {
    const r = Math.random() * 16 | 0; return (c === "x" ? r : (r & 3 | 8)).toString(16);
  }));
function toast(msg) { const t = $("#toast"); t.textContent = msg; t.classList.add("show"); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove("show"), 2600); }
function seg(container, opcoes, atual, onPick, rotulos) {
  container.innerHTML = "";
  opcoes.forEach(v => {
    const b = document.createElement("button"); b.type = "button";
    b.textContent = rotulos ? rotulos[v] : v; b.dataset.v = v;
    if (v === atual) b.classList.add("sel");
    b.onclick = () => { [...container.children].forEach(c => c.classList.remove("sel")); b.classList.add("sel"); onPick(v); };
    container.appendChild(b);
  });
}

/* ---------- grupos (tela inicial) ---------- */
function renderGrupos() {
  $("#gruposGrid").innerHTML = Object.entries(GRUPOS_META).map(([k, g]) => {
    const n = TIPOS.filter(t => t.grupo === k).length;
    return `<div class="grupo-card" onclick="onGrupo('${k}')" tabindex="0"
              onkeydown="if(event.key==='Enter')onGrupo('${k}')">
      <div class="icone">${g.icone}</div>
      <div class="label">${g.rotulo}</div>
      <div class="qtd">${n} tipos</div>
    </div>`;
  }).join("");
}

function onGrupo(grupoKey) {
  estado.grupo = grupoKey;
  initForm();
  setTab("form");
}

/* helper: dado uma categoria, devolve o grupo correspondente */
function grupoDeCategoria(cat) {
  const t = TIPOS.find(t => t.categoria === cat);
  return t?.grupo ?? cat;
}

/* ---------- montagem do form ---------- */
function initForm() {
  const lista = estado.grupo
    ? TIPOS.filter(t => t.grupo === estado.grupo)
    : TIPOS;
  $("#tipo").innerHTML = lista.map(t => `<option value="${t.tipo}">${t.rotulo}</option>`).join("");
  $("#selSentido").value = estado.sentido;
  $("#selSentido").onchange = e => estado.sentido = e.target.value;
  $("#selLado").value = estado.lado;
  $("#selLado").onchange = e => estado.lado = e.target.value;
  seg($("#segEstado"), ESTADOS, estado.estadoConserv, v => estado.estadoConserv = v);
  $("#data_inspecao").value = new Date().toISOString().slice(0, 10);
  atualizaConectividadeUI();
  // atualiza breadcrumb
  const gm = estado.grupo ? GRUPOS_META[estado.grupo] : null;
  $("#breadcrumbGrupo").textContent = gm ? `${gm.icone} ${gm.rotulo}` : "";
  onTipo();
}
function onTipo() {
  const t = tipoPorChave[$("#tipo").value];
  const linear = t.geometria === "linear";
  $("#wrapKmFim").classList.toggle("hidden", !linear);
  $("#wrapGps2").classList.toggle("hidden", !linear);
  $("#lblGps").textContent = linear ? "Coordenada (entrada)" : "Coordenada";

  const isCanaleta = t.tipo === "canaleta";
  $("#wrapDirecaoColeta").classList.toggle("hidden", !isCanaleta);
  if (isCanaleta) {
    $("#selDirecaoColeta").value = estado.direcao_coleta;
    $("#selDirecaoColeta").onchange = e => estado.direcao_coleta = e.target.value;
  }

  renderAtributos(t);
}
function renderAtributos(t) {
  const box = $("#atributos"); box.innerHTML = "";
  $("#tituloAtributos").textContent = "Especificações — " + t.rotulo;
  t.atributos.forEach(c => {
    const wrap = document.createElement("div");
    wrap.className = "field"; wrap.dataset.nome = c.nome;
    if (c.depende_de) { wrap.dataset.dependeDe = c.depende_de; wrap.dataset.dependeValor = c.depende_valor; }
    const lab = document.createElement("label");
    lab.textContent = c.rotulo + (c.unidade ? ` (${c.unidade})` : "");
    if (c.obrigatorio) lab.className = "req";
    wrap.appendChild(lab);

    let el;
    if (c.tipo === "enum") {
      el = document.createElement("select");
      el.innerHTML = `<option value="">—</option>` + c.opcoes.map(o => `<option value="${o}">${o}</option>`).join("");
    } else if (c.tipo === "bool") {
      el = document.createElement("select");
      el.innerHTML = `<option value="">—</option><option value="true">Sim</option><option value="false">Não</option>`;
    } else if (c.tipo === "numero") {
      el = document.createElement("input"); el.type = "number"; el.inputMode = "decimal"; el.step = "any";
    } else {
      el = document.createElement("input"); el.type = "text";
    }
    el.id = "attr_" + c.nome; el.dataset.tipo = c.tipo;
    if (c.depende_de) el.addEventListener; // placeholder
    wrap.appendChild(el);
    if (c.ajuda) { const h = document.createElement("div"); h.className = "hint"; h.textContent = c.ajuda; wrap.appendChild(h); }
    box.appendChild(wrap);

    // reavalia campos condicionais quando o campo-pai muda
    el.addEventListener("change", () => aplicaCondicionais(t));
  });
  aplicaCondicionais(t);
}
function aplicaCondicionais(t) {
  t.atributos.forEach(c => {
    if (!c.depende_de) return;
    const pai = $("#attr_" + c.depende_de);
    const wrap = document.querySelector(`#atributos .field[data-nome="${c.nome}"]`);
    if (!pai || !wrap) return;
    wrap.classList.toggle("hidden", String(pai.value) !== c.depende_valor);
  });
}

/* ---------- GPS ---------- */
function capturaGps(n) {
  if (!navigator.geolocation) return toast("GPS indisponível");
  const alvo = $("#gps" + n);
  alvo.innerHTML = "<small>capturando…</small>—";
  navigator.geolocation.getCurrentPosition(p => {
    const { latitude: la, longitude: lo, accuracy: ac } = p.coords;
    const obj = { lat: +la.toFixed(6), lon: +lo.toFixed(6), acc: Math.round(ac) };
    estado["gps" + n] = obj;
    const cls = ac <= 10 ? "acc-ok" : "acc-bad";
    alvo.innerHTML = `<small>±<span class="${cls}">${obj.acc} m</span> de acurácia</small>${obj.lat}, ${obj.lon}`;
  }, err => { alvo.innerHTML = "<small>falhou</small>—"; toast("GPS: " + err.message); },
    { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 });
}

/* ---------- EXIF GPS — parser puro, sem dependências externas ----------
   Estrutura JPEG: SOI(FFD8) → segmentos FF xx [len_be 2B] [dados].
   APP1 (FFE1) contém "Exif\0\0" seguido do bloco TIFF com IFD0 e GPS IFD.
   GPS IFD pointer está na tag 0x8825 do IFD0.
   Tags GPS relevantes: 0x01 LatRef, 0x02 Lat, 0x03 LonRef, 0x04 Lon (RATIONAL×3).
   ----------------------------------------------------------------------- */
function _readBuf(file) {
  return new Promise((res, rej) => {
    const r = new FileReader(); r.onload = () => res(r.result); r.onerror = () => rej(r.error);
    r.readAsArrayBuffer(file);
  });
}
function parseExifGps(buf) {
  try {
    const dv = new DataView(buf);
    if (dv.byteLength < 4 || dv.getUint16(0) !== 0xFFD8) return null;   // não é JPEG
    let off = 2;
    while (off + 4 <= dv.byteLength) {
      const marker = dv.getUint16(off);
      if (marker === 0xFFDA) break;                                        // SOS: chegou ao stream de pixels
      const segLen = dv.getUint16(off + 2);
      if (marker === 0xFFE1 && segLen >= 8 &&
          dv.getUint32(off + 4) === 0x45786966 &&                          // "Exif"
          dv.getUint16(off + 8) === 0x0000) {                              // \0\0
        return _tiffGps(dv, off + 10);                                     // início do bloco TIFF
      }
      off += 2 + segLen;
    }
  } catch (_) { /* buffer truncado ou corrompido — ignora silenciosamente */ }
  return null;
}
function _tiffGps(dv, t) {
  const le  = dv.getUint16(t) === 0x4949;                  // II = little-endian, MM = big-endian
  const u16 = o => dv.getUint16(t + o, le);
  const u32 = o => dv.getUint32(t + o, le);
  if (u16(2) !== 42) return null;                           // magic TIFF

  // IFD0 → procura ponteiro para GPS IFD (tag 0x8825)
  const ifd0 = u32(4);
  let gpsBase = null;
  const n0 = u16(ifd0);
  for (let i = 0; i < n0; i++) {
    const e = ifd0 + 2 + i * 12;
    if (u16(e) === 0x8825) { gpsBase = u32(e + 8); break; }
  }
  if (gpsBase === null) return null;

  // GPS IFD: lê tags de referência (ASCII inline) e coordenadas (RATIONAL×3)
  const gps = {};
  const ng = u16(gpsBase);
  for (let i = 0; i < ng; i++) {
    const e = gpsBase + 2 + i * 12;
    const tag = u16(e), type = u16(e + 2), vo = e + 8;
    if ((tag === 0x01 || tag === 0x03) && type === 2)
      gps[tag] = String.fromCharCode(dv.getUint8(t + vo));  // N/S ou E/W — 2 bytes, cabe inline
    else if ((tag === 0x02 || tag === 0x04) && type === 5) {
      const base = u32(vo);                                  // offset dos 3 racionais a partir de t
      gps[tag] = [0, 1, 2].map(j => {
        const den = u32(base + j * 8 + 4);
        return den ? u32(base + j * 8) / den : 0;           // grau | minuto | segundo
      });
    }
  }

  if (!gps[0x02] || !gps[0x04]) return null;
  const dec = ([d, m, s]) => d + m / 60 + s / 3600;
  let lat = dec(gps[0x02]), lon = dec(gps[0x04]);
  if (gps[0x01] === "S") lat = -lat;
  if (gps[0x03] === "W") lon = -lon;
  return (isFinite(lat) && isFinite(lon) && !(lat === 0 && lon === 0))
    ? { lat: +lat.toFixed(6), lon: +lon.toFixed(6) } : null;
}

/* ---------- fotos (downscale local + EXIF GPS) ---------- */
async function addFoto(input) {
  const file = input.files[0]; if (!file) return;
  input.value = "";

  // lê ArrayBuffer (EXIF) e DataURL (canvas) em paralelo — um único acesso ao ficheiro
  const [buf, dataUrl] = await Promise.all([
    _readBuf(file).catch(() => null),
    new Promise(res => {
      const fr = new FileReader();
      fr.onload = () => {
        const img = new Image();
        img.onload = () => {
          const max = 1280, sc = Math.min(1, max / Math.max(img.width, img.height));
          const cv = document.createElement("canvas");
          cv.width = img.width * sc; cv.height = img.height * sc;
          cv.getContext("2d").drawImage(img, 0, 0, cv.width, cv.height);
          res(cv.toDataURL("image/jpeg", 0.7));
        };
        img.src = fr.result;
      };
      fr.readAsDataURL(file);
    }),
  ]);

  const ref = `${(estado.id || "novo")}_${estado.fotos.length + 1}.jpg`;
  estado.fotos.push({ ref, dataUrl });
  renderFotos();

  // preenche GPS1 automaticamente apenas se ainda não foi capturado (não sobrescreve)
  if (buf) {
    const gps = parseExifGps(buf);
    if (gps && !estado.gps1) {
      estado.gps1 = { lat: gps.lat, lon: gps.lon, acc: null };
      $("#gps1").innerHTML = `<small>GPS da foto <span class="acc-ok">EXIF</span></small>${gps.lat}, ${gps.lon}`;
      toast("Coordenada lida do EXIF ✓");
    }
  }
}
function renderFotos() {
  const box = $("#fotos");
  [...box.querySelectorAll("img")].forEach(i => i.remove());
  estado.fotos.forEach((f, i) => {
    const im = document.createElement("img"); im.src = f.dataUrl;
    im.onclick = () => { if (confirm("Remover foto?")) { estado.fotos.splice(i, 1); renderFotos(); } };
    box.insertBefore(im, box.firstChild);
  });
}

/* ---------- salvar ---------- */
function lerAtributos(t) {
  const out = {}; const erros = [];
  t.atributos.forEach(c => {
    const wrap = document.querySelector(`#atributos .field[data-nome="${c.nome}"]`);
    if (wrap && wrap.classList.contains("hidden")) return;          // condicional oculto: ignora
    const el = $("#attr_" + c.nome); if (!el) return;
    let v = el.value;
    if (v === "" || v == null) { if (c.obrigatorio) erros.push(c.rotulo); return; }
    if (c.tipo === "numero") v = Number(v);
    else if (c.tipo === "bool") v = (v === "true");
    out[c.nome] = v;
  });
  return { out, erros };
}
async function salvar() {
  const t = tipoPorChave[$("#tipo").value];
  const rodovia = $("#rodovia").value.trim();
  const kmIni = $("#km_ini").value;
  const erros = [];
  if (!rodovia) erros.push("Rodovia");
  if (kmIni === "") erros.push("km inicial");
  const { out: atributos, erros: errAttr } = lerAtributos(t);
  erros.push(...errAttr);
  if (erros.length) return toast("Faltando: " + erros.join(", "));

  const linear = t.geometria === "linear";
  const reg = {
    id: estado.id || uuid(),
    rodovia, km_ini: parseKm(kmIni),
    km_fim: (linear && $("#km_fim").value !== "") ? parseKm($("#km_fim").value) : null,
    sentido: estado.sentido, lado: estado.lado,
    direcao_coleta: estado.direcao_coleta,
    id_rede: estado.id_rede, conectado_a: estado.conectado_a,
    estaca: $("#estaca").value.trim() || null,
    lat_ini: estado.gps1?.lat ?? null, lon_ini: estado.gps1?.lon ?? null,
    lat_fim: linear ? (estado.gps2?.lat ?? null) : null,
    lon_fim: linear ? (estado.gps2?.lon ?? null) : null,
    precisao_gps_m: estado.gps1?.acc ?? null,
    categoria: t.categoria, tipo: t.tipo,
    extensao_m: null,
    atributos,
    estado_conservacao: estado.estadoConserv,
    data_inspecao: $("#data_inspecao").value || null,
    inspetor: $("#inspetor").value.trim() || null,
    observacoes: $("#observacoes").value.trim() || null,
    fotos: estado.fotos,                          // {ref,dataUrl} local
    ncs: [],
    updated_at: new Date().toISOString(),
    _sync: "pendente",
  };
  await idbPut("registros", reg);
  toast(estado.id ? "Atualizado ✓" : "Salvo offline ✓");
  await atualizaBadge();
  limparForm();   // também chama setTab("grupos")
}

function limparForm() {
  estado = { id: null, grupo: null, sentido: "Norte", lado: "Lado Direito", estadoConserv: null, gps1: null, gps2: null, fotos: [], id_rede: travessia, conectado_a: null, direcao_coleta: travessia ? estado.direcao_coleta : "Direta" };
  $("#rodovia").value = ""; $("#km_ini").value = ""; $("#km_fim").value = "";
  $("#estaca").value = ""; $("#inspetor").value = ""; $("#observacoes").value = "";
  $("#gps1").innerHTML = "<small>sem captura</small>—";
  $("#gps2").innerHTML = "<small>sem captura</small>—";
  $("#btnSalvar").textContent = "Salvar offline";
  $("#btnDel")?.remove();
  setTab("grupos");
}

/* ---------- lista / edição ---------- */
const ICONE = { superficial: "▽", profunda: "⤓", transversal: "⊟" };
async function renderLista() {
  const regs = (await idbAll("registros")).sort((a, b) => b.updated_at.localeCompare(a.updated_at));
  const w = $("#listaWrap");
  if (!regs.length) { w.innerHTML = `<div class="empty"><div class="big">▽</div>Nenhum dispositivo coletado ainda.<br>Vá em <b>Novo</b> e comece o inventário.</div>`; return; }
  w.innerHTML = regs.map(r => {
    const t = tipoPorChave[r.tipo];
    const km = r.km_fim != null ? `km ${formatKm(r.km_ini)}–${formatKm(r.km_fim)}` : `km ${formatKm(r.km_ini)}`;
    const cls = r._sync === "sincronizado" ? "sync" : "pend";
    return `<div class="item" onclick="editar('${r.id}')">
      <div class="ico">${ICONE[r.categoria] || "•"}</div>
      <div class="meta"><b>${t ? t.rotulo : r.tipo}</b>
        <span>${r.rodovia} · ${km} · ${r.lado}${r.estado_conservacao ? " · " + r.estado_conservacao : ""}</span></div>
      <span class="pill ${cls}">${r._sync === "sincronizado" ? "sync" : "pendente"}</span>
    </div>`;
  }).join("");
}
async function editar(id) {
  const r = await idbGet("registros", id); if (!r) return;
  estado = { id: r.id, grupo: grupoDeCategoria(r.categoria),
    sentido: r.sentido, lado: r.lado, estadoConserv: r.estado_conservacao,
    id_rede: r.id_rede ?? null, conectado_a: r.conectado_a ?? null,
    direcao_coleta: r.direcao_coleta ?? "Direta",
    gps1: r.lat_ini != null ? { lat: r.lat_ini, lon: r.lon_ini, acc: r.precisao_gps_m } : null,
    gps2: r.lat_fim != null ? { lat: r.lat_fim, lon: r.lon_fim, acc: null } : null,
    fotos: r.fotos || [] };
  setTab("form");
  initForm();   // popula #tipo com os tipos do grupo
  $("#tipo").value = r.tipo; onTipo();
  $("#rodovia").value = r.rodovia; $("#km_ini").value = r.km_ini != null ? formatKm(r.km_ini) : "";
  $("#km_fim").value = r.km_fim != null ? formatKm(r.km_fim) : ""; $("#estaca").value = r.estaca ?? "";
  $("#inspetor").value = r.inspetor ?? ""; $("#observacoes").value = r.observacoes ?? "";
  $("#data_inspecao").value = r.data_inspecao ?? "";
  initSegFromState();
  Object.entries(r.atributos || {}).forEach(([k, v]) => { const el = $("#attr_" + k); if (el) el.value = (typeof v === "boolean") ? String(v) : v; });
  aplicaCondicionais(tipoPorChave[r.tipo]);
  if (estado.gps1) $("#gps1").innerHTML = `<small>±${estado.gps1.acc ?? "?"} m</small>${estado.gps1.lat}, ${estado.gps1.lon}`;
  if (estado.gps2) $("#gps2").innerHTML = `<small>saída</small>${estado.gps2.lat}, ${estado.gps2.lon}`;
  renderFotos();
  $("#btnSalvar").textContent = "Atualizar";
  // botão apagar via observação longa
  if (!$("#btnDel")) { const b = document.createElement("button"); b.id = "btnDel"; b.className = "btn ghost"; b.textContent = "🗑"; b.onclick = () => apagar(r.id); $("#barForm").insertBefore(b, $("#btnSalvar")); }
}
function initSegFromState() {
  $("#selSentido").value = estado.sentido;
  $("#selSentido").onchange = e => estado.sentido = e.target.value;
  $("#selLado").value = estado.lado;
  $("#selLado").onchange = e => estado.lado = e.target.value;
  seg($("#segEstado"), ESTADOS, estado.estadoConserv, v => estado.estadoConserv = v);
}
async function apagar(id) {
  if (!confirm("Apagar este dispositivo?")) return;
  await idbDel("registros", id); toast("Apagado"); $("#btnDel")?.remove();
  limparForm(); setTab("lista"); renderLista(); atualizaBadge();
}

/* ---------- sync ---------- */
async function getBackend() {
  const c = await idbGet("config", "backend");
  return c?.v || "";
}
async function sincronizar() {
  let url = await getBackend();
  if (!url) {
    url = prompt("URL do backend (ex.: https://api.suarodovia.com.br):", "http://localhost:8000");
    if (!url) return;
    await idbPut("config", { k: "backend", v: url.replace(/\/$/, "") });
    url = url.replace(/\/$/, "");
  }
  if (!navigator.onLine) return toast("Sem conexão — tente quando tiver rede");

  const cfgSync = await idbGet("config", "last_sync");
  const last_sync = cfgSync?.v || null;
  const todos = await idbAll("registros");
  const pendentes = todos.filter(r => r._sync !== "sincronizado");

  // payload: tira o binário das fotos (envia só refs nesta versão)
  const registros = pendentes.map(r => ({ ...r, fotos: (r.fotos || []).map(f => f.ref || f), _sync: undefined }));

  $("#btnSync").disabled = true; $("#btnSync").textContent = "Sincronizando…";
  try {
    const resp = await fetch(url + "/sync", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ last_sync, registros }),
    });
    if (!resp.ok) throw new Error("HTTP " + resp.status);
    const j = await resp.json();

    // marca enviados como sincronizados (mantém fotos locais)
    for (const r of pendentes) { r._sync = "sincronizado"; await idbPut("registros", r); }

    // aplica mudanças vindas do servidor (outros aparelhos)
    for (const sv of (j.registros || [])) {
      const local = await idbGet("registros", sv.id);
      if (sv.deleted) { await idbDel("registros", sv.id); continue; }
      const fotosLocais = local?.fotos || [];
      await idbPut("registros", { ...sv, fotos: fotosLocais, _sync: "sincronizado" });
    }
    await idbPut("config", { k: "last_sync", v: j.server_time });
    toast(`Sync ✓  enviados ${j.aplicados} · recebidos ${(j.registros || []).length}`);
    renderLista(); atualizaBadge();
  } catch (e) {
    toast("Falha no sync: " + e.message);
  } finally {
    $("#btnSync").disabled = false; $("#btnSync").textContent = "Sincronizar";
  }
}

/* ---------- export GeoJSON local ---------- */
async function exportGeoJSON() {
  const regs = (await idbAll("registros")).filter(r => r.lat_ini != null);
  if (!regs.length) return toast("Nada georreferenciado pra exportar");
  const feats = regs.map(r => {
    const geom = (r.lat_fim != null)
      ? { type: "LineString", coordinates: [[r.lon_ini, r.lat_ini], [r.lon_fim, r.lat_fim]] }
      : { type: "Point", coordinates: [r.lon_ini, r.lat_ini] };
    return { type: "Feature", geometry: geom, properties: {
      id: r.id, rodovia: r.rodovia, km_ini: r.km_ini, km_fim: r.km_fim, lado: r.lado,
      categoria: r.categoria, tipo: r.tipo, estado: r.estado_conservacao, ...r.atributos } };
  });
  const fc = { type: "FeatureCollection", features: feats };
  const blob = new Blob([JSON.stringify(fc, null, 2)], { type: "application/geo+json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `drenagem_${new Date().toISOString().slice(0, 10)}.geojson`;
  a.click(); URL.revokeObjectURL(a.href);
  toast(`Exportado ${feats.length} feições`);
}

/* ---------- navegação / status ---------- */
function setTab(tab) {
  document.querySelectorAll("nav.tabs button").forEach(b => b.classList.toggle("sel", b.dataset.tab === tab));
  $("#tab-grupos").classList.toggle("hidden", tab !== "grupos");
  $("#tab-form").classList.toggle("hidden", tab !== "form");
  $("#tab-lista").classList.toggle("hidden", tab !== "lista");
  $("#barForm").classList.toggle("hidden", tab !== "form");
  $("#barLista").classList.toggle("hidden", tab !== "lista");
  if (tab === "grupos") { renderGrupos(); $("#btnDel")?.remove(); }
  if (tab === "lista") renderLista();
  if (tab === "form" && !estado.id) $("#btnDel")?.remove();
}
async function atualizaBadge() {
  const regs = await idbAll("registros");
  const n = regs.filter(r => r._sync !== "sincronizado").length;
  const b = $("#pend"); b.textContent = n; b.classList.toggle("zero", n === 0);
}
function netStatus() {
  const on = navigator.onLine;
  $("#netDot").classList.toggle("on", on);
  $("#netTxt").textContent = on ? "online" : "offline";
}

/* ---------- boot ---------- */
(async function () {
  db = await openDB();
  setTab("grupos");   // começa no picker de grupos, não no form vazio
  netStatus();
  await atualizaBadge();
  window.addEventListener("online", netStatus);
  window.addEventListener("offline", netStatus);
  if ("serviceWorker" in navigator) {
    try { await navigator.serviceWorker.register("sw.js"); } catch (e) { /* file:// não suporta SW */ }
  }
})();
