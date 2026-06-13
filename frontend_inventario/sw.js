/* Service worker — cache do app shell (offline-first).
   Estratégia: cache-first pro shell; rede nunca é exigida pra coletar. */
const CACHE = "drenagem-v1";
const SHELL = [
  "./", "./index.html", "./app.js", "./catalogo.js", "./manifest.json",
];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  // chamadas ao backend (/sync etc.) sempre vão à rede — nunca cacheia dados
  if (url.pathname.startsWith("/sync") || url.pathname.startsWith("/dispositivos")
      || url.pathname.startsWith("/export") || url.pathname.startsWith("/catalogo")) {
    return; // deixa passar direto pra rede
  }
  // app shell: cache-first
  e.respondWith(
    caches.match(e.request).then(hit => hit || fetch(e.request).then(resp => {
      if (resp.ok && e.request.method === "GET") {
        const cp = resp.clone(); caches.open(CACHE).then(c => c.put(e.request, cp));
      }
      return resp;
    }).catch(() => caches.match("./index.html")))
  );
});
