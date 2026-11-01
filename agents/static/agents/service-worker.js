
const CACHE_NAME = "mwalimu-ai-v3";

const FICHIERS = [
    "/",
    "/chat/",
    "/static/agents/style.css",
    "/static/agents/manifest.json"
];

// Installer le Service Worker
self.addEventListener("install", event => {

    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll(FICHIERS);
        })
    );

    self.skipWaiting();
});

// Activer la nouvelle version
self.addEventListener("activate", event => {

    event.waitUntil(
        caches.keys().then(noms => {
            return Promise.all(
                noms
                    .filter(nom => nom !== CACHE_NAME)
                    .map(nom => caches.delete(nom))
            );
        })
    );

    self.clients.claim();
});

// Gérer les requêtes
self.addEventListener("fetch", event => {

    if (event.request.method !== "GET") {
        return;
    }

    const url = new URL(event.request.url);

    // Pour les pages HTML : réseau d'abord, cache ensuite
    if (event.request.mode === "navigate") {

        event.respondWith(
            fetch(event.request)
                .then(response => {
                    return response;
                })
                .catch(() => {
                    return caches.match(event.request);
                })
        );

    } else {

        // Pour les fichiers statiques : cache d'abord
        event.respondWith(
            caches.match(event.request).then(response => {
                return response || fetch(event.request);
            })
        );

    }

});
