// Self-destroying service worker to instantly clear old localhost routing layouts
self.addEventListener('install', event => {
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    self.registration.unregister()
      .then(() => self.clients.matchAll())
      .then(clients => {
        clients.forEach(client => {
          if (client.navigate) {
            client.navigate(client.url);
          }
        });
      })
  );
});

self.addEventListener('fetch', event => {
  // Pass through all requests directly to the network without checking any cache
  event.respondWith(fetch(event.request));
});