var CACHE = 'yunnan-v1';
var URLS = ['./', './index.html', './style.css', './script.js'];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(URLS); }));
  self.skipWaiting();
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (names) {
      return Promise.all(names.filter(function (n) { return n !== CACHE; }).map(function (n) { return caches.delete(n); }));
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', function (e) {
  if (e.request.url.indexOf('fonts.googleapis.com') !== -1 || e.request.url.indexOf('fonts.gstatic.com') !== -1) {
    e.respondWith(caches.open(CACHE).then(function (c) {
      return c.match(e.request).then(function (r) {
        return r || fetch(e.request).then(function (resp) { c.put(e.request, resp.clone()); return resp; });
      });
    }));
    return;
  }
  e.respondWith(
    caches.match(e.request).then(function (r) { return r || fetch(e.request); })
  );
});
