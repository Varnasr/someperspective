// Self-destruct: clear all caches and unregister.
// The aggressive shell-caching SW from v3.0.0 cached broken HTML;
// this replacement wipes the slate clean on next visit.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.map(k => caches.delete(k))))
      .then(() => self.clients.claim())
      .then(() => self.registration.unregister())
  );
});
