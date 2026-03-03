var CACHE = 'yunnan-v4';
var URLS = [
  './',
  './index.html',
  './style.css',
  './script.js',
  './manifest.json',
  './images/280561044762.jpg',
  './images/31dbed614317.jpg',
  './images/7ed65f42ccf1.jpg',
  './images/960px-20140511_Lijiang_Impression_Show.jpg',
  './images/960px-Baisha_Old_Town_(21183444262).jpg',
  './images/960px-Dali_City_Birdseye.JPG',
  './images/960px-Dali_Yunnan_China_Chongsheng-Temple-03.jpg',
  './images/960px-Dali_Yunnan_China_West-gate-of-old-town-Dali-01.jpg',
  './images/960px-Lijiang_Oct_2007_232.jpg',
  './images/960px-Lijiang_Yunnan_Black-Dragon-Pool-01.jpg',
  './images/960px-Lijiang_banner_Shuhe_old_town.png',
  './images/960px-Qinglong_Qiao,_Lijiang_Shi.jpg',
  './images/960px-Shaxi_banner_Xingjiao_Temple.JPG',
  './images/960px-Three_Pagodas,_Dali,_China_-_panoramio.jpg',
  './images/960px-Tree_in_front_of_Erhai_Lake.jpg',
  './images/960px-Yunnan_China_Tiger-Leaping-Gorge-04.jpg',
  './images/960px-Yunnan_China_Tiger-Leaping-Gorge-06.jpg',
  './images/baisha_murals.jpg',
  './images/lashi_lake.jpg',
  './images/mu_fu.jpg',
  './images/shaxi_old_town.jpg',
  './images/xizhou_village.jpg',
  './images/yuhu_village.jpg'
];

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
  // Cache-first for fonts
  if (e.request.url.indexOf('fonts.googleapis.com') !== -1 || e.request.url.indexOf('fonts.gstatic.com') !== -1) {
    e.respondWith(caches.open(CACHE).then(function (c) {
      return c.match(e.request).then(function (r) {
        return r || fetch(e.request).then(function (resp) { c.put(e.request, resp.clone()); return resp; });
      });
    }));
    return;
  }
  // Cache-first for Leaflet tiles
  if (e.request.url.indexOf('tile.openstreetmap.org') !== -1) {
    e.respondWith(caches.open(CACHE).then(function (c) {
      return c.match(e.request).then(function (r) {
        return r || fetch(e.request).then(function (resp) {
          if (resp.ok) c.put(e.request, resp.clone());
          return resp;
        }).catch(function () { return r; });
      });
    }));
    return;
  }
  // Default: cache-first
  e.respondWith(
    caches.match(e.request).then(function (r) { return r || fetch(e.request); })
  );
});
