/* === YUNNAN GUIDE — SCRIPT.JS === */
(function () {
  'use strict';

  /* ========================================
     DOM REFS
     ======================================== */
  var searchBtn = document.getElementById('search-btn');
  var searchOverlay = document.getElementById('search-overlay');
  var searchInput = document.getElementById('search-input');
  var searchResults = document.getElementById('search-results');
  var themeBtn = document.getElementById('theme-btn');
  var qrFab = document.getElementById('qr-fab');
  var qrSheet = document.getElementById('qr-sheet');
  var qrClose = document.getElementById('qr-close');
  var progressBar = document.getElementById('progress-bar');
  var hero = document.getElementById('hero');
  var expandAllBtn = document.getElementById('expand-all-btn');
  var collapseAllBtn = document.getElementById('collapse-all-btn');

  /* ========================================
     TAB NAVIGATION
     ======================================== */
  var tabBtns = document.querySelectorAll('.tab-btn');
  var tabPanels = document.querySelectorAll('.tab-panel');
  var leafletMap = null;
  var currentTab = 'tab-map';
  document.body.classList.add('map-tab-active');

  function switchTab(tabId) {
    if (tabId === currentTab) return;
    currentTab = tabId;

    // Update panels
    tabPanels.forEach(function (p) { p.classList.remove('active'); });
    document.getElementById(tabId).classList.add('active');

    // Update buttons
    tabBtns.forEach(function (b) {
      var isActive = b.getAttribute('data-tab') === tabId;
      b.classList.toggle('active', isActive);
      b.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });

    // Hero: compact on non-map tabs, hidden on map
    if (hero) {
      if (tabId === 'tab-map') {
        hero.style.display = 'none';
      } else {
        hero.style.display = '';
        hero.classList.add('compact');
      }
    }

    // Hide quick-reference FAB on map for cleaner view
    document.body.classList.toggle('map-tab-active', tabId === 'tab-map');

    // Resize map when switching to map tab
    if (tabId === 'tab-map' && leafletMap) {
      setTimeout(function () { leafletMap.invalidateSize(); }, 150);
    }

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'instant' });
  }

  tabBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      switchTab(this.getAttribute('data-tab'));
    });
  });

  /* ========================================
     LEAFLET MAP INITIALIZATION
     ======================================== */
  function initMap() {
    if (typeof L === 'undefined') return;

    leafletMap = L.map('yunnan-map', {
      scrollWheelZoom: false,
      zoomControl: true,
      attributionControl: true
    }).setView([26.5, 100.15], 8);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap',
      maxZoom: 17
    }).addTo(leafletMap);

    var locations = [
      {name:"Dayan Old Town (大研古城)", lat:26.8724, lng:100.226, day:"D1–D4", desc:"UNESCO World Heritage Naxi old town. 354 stone bridges, 3-tier water system, Sifang Square market center.", icon:"🏘️", img:"images/280561044762.jpg", imgAlt:"Dayan Old Town canal at dusk"},
      {name:"Black Dragon Pool (黑龍潭)", lat:26.885, lng:100.228, day:"D2", desc:"Spring-fed pool with iconic Jade Dragon reflection. Dongba Culture Museum inside the park.", icon:"💧", img:"images/960px-Lijiang_Yunnan_Black-Dragon-Pool-01.jpg", imgAlt:"Black Dragon Pool with Jade Dragon Snow Mountain"},
      {name:"Baisha Old Town (白沙古鎮)", lat:26.9085, lng:100.169, day:"D2", desc:"Original Naxi capital. Baisha Murals — Buddhist/Taoist/Dongba fusion art from 14th-16th century.", icon:"🎨", img:"images/960px-Baisha_Old_Town_(21183444262).jpg", imgAlt:"Baisha Old Town with mountain backdrop"},
      {name:"Jade Dragon Snow Mountain (玉龍雪山)", lat:27.1167, lng:100.1833, day:"D3", desc:"Sacred Naxi mountain, 5,596m. Never summited (religious prohibition). Blue Moon Valley, Impressions Lijiang show.", icon:"🏔️", img:"images/31dbed614317.jpg", imgAlt:"Jade Dragon Snow Mountain from Lijiang"},
      {name:"Blue Moon Valley (藍月谷)", lat:27.091, lng:100.192, day:"D3", desc:"Glacial meltwater lakes — turquoise to electric blue from suspended glacial flour.", icon:"💎", img:"images/960px-20140511_Lijiang_Impression_Show.jpg", imgAlt:"Blue Moon Valley glacial lakes"},
      {name:"Yuhu Village (玉湖村)", lat:27.04, lng:100.185, day:"D3", desc:"Joseph Rock's base for 27 years. Naxi home visits — connecting to families who hosted one of Asia's great ethnographers.", icon:"🏡", img:"images/960px-Lijiang_Oct_2007_232.jpg", imgAlt:"Yuhu Village"},
      {name:"Lashi Lake (拉市海)", lat:26.858, lng:100.115, day:"D4", desc:"Tea Horse Road origin. Horseback trails on original caravan routes. Migratory bird wetland — bar-headed geese fly over the Himalayas.", icon:"🐎", img:"images/lashi_lake.jpg", imgAlt:"Lashi Lake"},
      {name:"Shuhe Old Town (束河古鎮)", lat:26.903, lng:100.207, day:"D4", desc:"Older than Dayan. Historic leather crafting hub for Tea Horse Road caravans. UNESCO-listed.", icon:"🏘️", img:"images/960px-Qinglong_Qiao,_Lijiang_Shi.jpg", imgAlt:"Shuhe Old Town"},
      {name:"Tiger Leaping Gorge (虎跳峽)", lat:27.185, lng:100.11, day:"D5", desc:"One of the deepest gorges on Earth — 3,900m from river to summit. The Jinsha River (upper Yangtze) at its most dramatic.", icon:"🐅", img:"images/960px-Yunnan_China_Tiger-Leaping-Gorge-06.jpg", imgAlt:"Tiger Leaping Gorge"},
      {name:"Shaxi / Sideng Square (沙溪)", lat:26.315, lng:99.925, day:"D5–D6", desc:"Only surviving Tea Horse Road market town with original market square intact. UNESCO restored. Xingjiao Temple.", icon:"🏛️", img:"images/shaxi_old_town.jpg", imgAlt:"Shaxi old town"},
      {name:"Dali Old Town (大理古城)", lat:25.694, lng:100.154, day:"D6–D7", desc:"Former Nanzhao/Dali Kingdom territory. Defeated Tang Dynasty armies. Catholic church with Bai-European fusion architecture.", icon:"⛩️", img:"images/960px-Dali_Yunnan_China_Chongsheng-Temple-03.jpg", imgAlt:"Three Pagodas, Dali"},
      {name:"Three Pagodas (崇圣寺三塔)", lat:25.728, lng:100.1425, day:"D6", desc:"Main pagoda 69m tall, built 823-840 AD during Nanzhao. Visible legacy of Nanzhao/Dali Kingdom Buddhist culture.", icon:"🗼", img:"images/960px-Three_Pagodas,_Dali,_China_-_panoramio.jpg", imgAlt:"Three Pagodas of Chongsheng Temple"},
      {name:"Xizhou Village (喜洲)", lat:25.853, lng:100.12, day:"D7", desc:"Best-preserved Bai village architecture. Spectacular screen walls (照壁). Yan Family Compound. Tie-dye workshop nearby.", icon:"🏘️", img:"images/xizhou_village.jpg", imgAlt:"Xizhou Village"},
      {name:"Erhai Lake / Longkan Wharf (洱海)", lat:25.78, lng:100.2, day:"D7", desc:"250 km² lake at 1,974m. Historical Bai water highway. Cycling route with Cangshan mountain views.", icon:"🚲", img:"images/960px-Tree_in_front_of_Erhai_Lake.jpg", imgAlt:"Erhai Lake with Cangshan Mountains"}
    ];

    var dayColors = {
      'D1–D4': '#c2583a', 'D2': '#c2583a', 'D3': '#4a7c6f', 'D4': '#4a7c6f',
      'D5': '#2c3e6b', 'D5–D6': '#2c3e6b', 'D6': '#5a6fa0', 'D6–D7': '#5a6fa0', 'D7': '#c9a84c'
    };

    var dayLabels = {
      'D1–D4': 'D1', 'D2': 'D2', 'D3': 'D3', 'D4': 'D4',
      'D5': 'D5', 'D5–D6': 'D5', 'D6': 'D6', 'D6–D7': 'D6', 'D7': 'D7'
    };

    // Offset overlapping markers slightly for visibility
    var seen = {};
    locations.forEach(function (loc) {
      var key = loc.lat.toFixed(2) + ',' + loc.lng.toFixed(2);
      if (!seen[key]) { seen[key] = 0; }
      var offset = seen[key];
      seen[key]++;
      if (offset > 0) {
        // Spiral offset for dense clusters
        var angle = offset * 1.2;
        loc.lat += Math.cos(angle) * 0.008 * offset;
        loc.lng += Math.sin(angle) * 0.008 * offset;
      }
    });

    var markers = [];
    locations.forEach(function (loc, idx) {
      var color = dayColors[loc.day] || '#c2583a';
      var label = dayLabels[loc.day] || 'D' + (idx + 1);
      var num = idx + 1;
      var divIcon = L.divIcon({
        className: 'yn-marker',
        html: '<div style="background:' + color + ';color:#fff;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;box-shadow:0 2px 8px rgba(0,0,0,0.35);border:2.5px solid #fff;letter-spacing:-0.5px">' + num + '</div>',
        iconSize: [36, 36],
        iconAnchor: [18, 18],
        popupAnchor: [0, -20]
      });

      var popupHtml = '<div style="font-family:Inter,sans-serif;max-width:260px">';
      if (loc.img) {
        popupHtml += '<img src="' + loc.img + '" alt="' + loc.imgAlt + '" loading="lazy" style="width:100%;border-radius:6px;margin-bottom:8px;height:140px;object-fit:cover">';
      }
      popupHtml += '<strong style="font-size:0.95rem">' + loc.icon + ' ' + loc.name + '</strong><br>';
      popupHtml += '<span style="display:inline-block;margin:4px 0;padding:2px 8px;border-radius:10px;background:' + color + ';color:#fff;font-size:0.7rem;font-weight:600">' + loc.day + '</span><br>';
      popupHtml += '<span style="font-size:0.82rem;color:#5a5650;line-height:1.4">' + loc.desc + '</span></div>';

      var m = L.marker([loc.lat, loc.lng], { icon: divIcon }).addTo(leafletMap);
      m.bindPopup(popupHtml, { closeButton: false, maxWidth: 280 });
      markers.push(m);
    });

    // Route polylines (colored by day phase)
    var routeSegments = [
      [[26.8724,100.226], [26.885,100.228], '#c2583a'],
      [[26.885,100.228], [26.9085,100.169], '#c2583a'],
      [[26.8724,100.226], [27.1167,100.1833], '#4a7c6f'],
      [[27.1167,100.1833], [27.091,100.192], '#4a7c6f'],
      [[27.091,100.192], [27.04,100.185], '#4a7c6f'],
      [[26.8724,100.226], [26.858,100.115], '#4a7c6f'],
      [[26.858,100.115], [26.903,100.207], '#4a7c6f'],
      [[26.903,100.207], [27.185,100.11], '#2c3e6b'],
      [[27.185,100.11], [26.315,99.925], '#2c3e6b'],
      [[26.315,99.925], [25.694,100.154], '#2c3e6b'],
      [[25.694,100.154], [25.728,100.1425], '#c9a84c'],
      [[25.728,100.1425], [25.853,100.12], '#c9a84c'],
      [[25.853,100.12], [25.78,100.2], '#c9a84c']
    ];

    routeSegments.forEach(function (seg) {
      L.polyline([seg[0], seg[1]], {
        color: seg[2], weight: 3, opacity: 0.6, dashArray: '8 6'
      }).addTo(leafletMap);
    });

    // Day legend
    var legend = L.control({ position: 'bottomleft' });
    legend.onAdd = function () {
      var div = L.DomUtil.create('div', 'map-legend');
      div.innerHTML = '<div style="background:rgba(255,255,255,0.92);padding:8px 10px;border-radius:8px;font-family:Inter,sans-serif;font-size:0.72rem;box-shadow:0 2px 6px rgba(0,0,0,0.15);line-height:1.6">' +
        '<div style="font-weight:700;margin-bottom:4px;font-size:0.75rem">Route by Day</div>' +
        '<div><span style="display:inline-block;width:12px;height:3px;background:#c2583a;border-radius:2px;vertical-align:middle;margin-right:5px"></span> D1–D2 Lijiang</div>' +
        '<div><span style="display:inline-block;width:12px;height:3px;background:#4a7c6f;border-radius:2px;vertical-align:middle;margin-right:5px"></span> D3–D4 Mountain & Lake</div>' +
        '<div><span style="display:inline-block;width:12px;height:3px;background:#2c3e6b;border-radius:2px;vertical-align:middle;margin-right:5px"></span> D5 Gorge → Shaxi</div>' +
        '<div><span style="display:inline-block;width:12px;height:3px;background:#c9a84c;border-radius:2px;vertical-align:middle;margin-right:5px"></span> D6–D7 Dali</div>' +
        '</div>';
      return div;
    };
    legend.addTo(leafletMap);

    // Numbered marker legend
    var markerLegend = L.control({ position: 'topright' });
    markerLegend.onAdd = function () {
      var div = L.DomUtil.create('div', 'marker-legend');
      var html = '<div style="background:rgba(255,255,255,0.92);padding:8px 10px;border-radius:8px;font-family:Inter,sans-serif;font-size:0.68rem;box-shadow:0 2px 6px rgba(0,0,0,0.15);line-height:1.5;max-height:50vh;overflow-y:auto">';
      html += '<div style="font-weight:700;margin-bottom:4px;font-size:0.72rem">Stops</div>';
      locations.forEach(function (loc, idx) {
        var color = dayColors[loc.day] || '#c2583a';
        var shortName = loc.name.split('(')[0].trim();
        html += '<div style="white-space:nowrap"><span style="display:inline-block;width:18px;height:18px;border-radius:50%;background:' + color + ';color:#fff;text-align:center;line-height:18px;font-size:0.6rem;font-weight:700;margin-right:4px;vertical-align:middle">' + (idx + 1) + '</span>' + shortName + '</div>';
      });
      html += '</div>';
      div.innerHTML = html;
      return div;
    };
    markerLegend.addTo(leafletMap);

    // Fit bounds
    var group = L.featureGroup(markers);
    leafletMap.fitBounds(group.getBounds().pad(0.12));
  }

  // Initialize map
  initMap();

  /* ========================================
     DARK MODE
     ======================================== */
  function setTheme(dark) {
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
    themeBtn.textContent = dark ? '☀️' : '🌙';
    try { localStorage.setItem('yn-theme', dark ? 'dark' : 'light'); } catch (e) {}
  }

  themeBtn.addEventListener('click', function () {
    var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    setTheme(!isDark);
  });

  // Restore preference
  try {
    var saved = localStorage.getItem('yn-theme');
    if (saved === 'dark') setTheme(true);
    else if (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches) setTheme(true);
  } catch (e) {}

  /* ========================================
     SEARCH
     ======================================== */
  var searchIndex = [];
  document.querySelectorAll('[data-search]').forEach(function (el) {
    searchIndex.push({
      text: el.textContent,
      section: el.getAttribute('data-search'),
      el: el
    });
  });

  searchBtn.addEventListener('click', function () {
    searchOverlay.classList.add('open');
    setTimeout(function () { searchInput.focus(); }, 100);
  });

  searchOverlay.addEventListener('click', function (e) {
    if (e.target === searchOverlay) {
      searchOverlay.classList.remove('open');
      searchInput.value = '';
      searchResults.innerHTML = '';
    }
  });

  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      searchOverlay.classList.add('open');
      setTimeout(function () { searchInput.focus(); }, 100);
    }
    if (e.key === 'Escape' && searchOverlay.classList.contains('open')) {
      searchOverlay.classList.remove('open');
      searchInput.value = '';
      searchResults.innerHTML = '';
    }
  });

  searchInput.addEventListener('input', function () {
    var q = this.value.trim().toLowerCase();
    if (q.length < 2) { searchResults.innerHTML = ''; return; }

    var hits = [];
    searchIndex.forEach(function (item) {
      var idx = item.text.toLowerCase().indexOf(q);
      if (idx !== -1) {
        var start = Math.max(0, idx - 40);
        var end = Math.min(item.text.length, idx + q.length + 40);
        var snippet = (start > 0 ? '…' : '') +
          item.text.substring(start, idx) +
          '<mark>' + item.text.substring(idx, idx + q.length) + '</mark>' +
          item.text.substring(idx + q.length, end) +
          (end < item.text.length ? '…' : '');
        hits.push({ section: item.section, snippet: snippet, el: item.el });
      }
    });

    if (hits.length === 0) {
      searchResults.innerHTML = '<div class="search-empty">No results found</div>';
      return;
    }

    searchResults.innerHTML = hits.slice(0, 15).map(function (h) {
      return '<div class="search-result" tabindex="0"><div class="search-result-section">' +
        h.section + '</div><div>' + h.snippet + '</div></div>';
    }).join('');

    searchResults.querySelectorAll('.search-result').forEach(function (r, i) {
      r.addEventListener('click', function () {
        var hit = hits[i];

        // Determine which tab this content is in
        var tabPanel = hit.el.closest('.tab-panel');
        if (tabPanel && tabPanel.id !== currentTab) {
          switchTab(tabPanel.id);
        }

        // Expand section/day card if collapsed
        var parentSection = hit.el.closest('.section.collapsed');
        if (parentSection) {
          parentSection.classList.remove('collapsed');
        }
        var parentCard = hit.el.closest('.day-card.collapsed');
        if (parentCard) {
          parentCard.classList.remove('collapsed');
        }

        // Expand collapsible if needed
        var parentCollapsible = hit.el.closest('.collapsible-content');
        if (parentCollapsible && parentCollapsible.style.maxHeight === '0px') {
          var toggle = parentCollapsible.previousElementSibling;
          if (toggle && toggle.classList.contains('collapsible-toggle')) {
            toggle.click();
          }
        }

        // Scroll to element
        setTimeout(function () {
          hit.el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);

        searchOverlay.classList.remove('open');
        searchInput.value = '';
        searchResults.innerHTML = '';
      });
    });
  });

  /* ========================================
     COLLAPSIBLES (within day cards)
     ======================================== */
  document.querySelectorAll('.collapsible-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      this.classList.toggle('open');
      var content = this.nextElementSibling;
      if (this.classList.contains('open')) {
        content.style.maxHeight = content.scrollHeight + 'px';
      } else {
        content.style.maxHeight = '0px';
      }
    });
  });

  /* ========================================
     CONVERSATION STARTER ACCORDIONS
     ======================================== */
  document.querySelectorAll('.convo-question').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var answer = this.nextElementSibling;
      var isOpen = answer.style.maxHeight && answer.style.maxHeight !== '0px';
      answer.style.maxHeight = isOpen ? '0px' : answer.scrollHeight + 'px';
    });
  });

  /* ========================================
     QUICK REFERENCE SHEET
     ======================================== */
  if (qrFab && qrSheet) {
    qrFab.addEventListener('click', function () { qrSheet.classList.toggle('open'); });
  }
  if (qrClose) {
    qrClose.addEventListener('click', function () { qrSheet.classList.remove('open'); });
  }
  document.querySelectorAll('.qr-tab').forEach(function (tab) {
    tab.addEventListener('click', function () {
      document.querySelectorAll('.qr-tab').forEach(function (t) { t.classList.remove('active'); });
      document.querySelectorAll('.qr-panel').forEach(function (p) { p.classList.remove('active'); });
      this.classList.add('active');
      var panel = document.getElementById(this.getAttribute('data-panel'));
      if (panel) panel.classList.add('active');
    });
  });

  /* ========================================
     DAY CARD TOGGLE
     ======================================== */
  document.querySelectorAll('.day-card-header').forEach(function (header) {
    header.addEventListener('click', function () {
      this.closest('.day-card').classList.toggle('collapsed');
    });
  });

  /* ========================================
     SECTION TOGGLE (Info tab)
     ======================================== */
  document.querySelectorAll('.section-header').forEach(function (header) {
    header.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') return;
      var section = this.closest('.section');
      if (section && section.querySelector('.section-body')) {
        section.classList.toggle('collapsed');
      }
    });
  });

  /* ========================================
     EXPAND / COLLAPSE ALL (Itinerary)
     ======================================== */
  if (expandAllBtn) {
    expandAllBtn.addEventListener('click', function () {
      document.querySelectorAll('#tab-itinerary .day-card').forEach(function (c) {
        c.classList.remove('collapsed');
      });
    });
  }
  if (collapseAllBtn) {
    collapseAllBtn.addEventListener('click', function () {
      document.querySelectorAll('#tab-itinerary .day-card').forEach(function (c) {
        c.classList.add('collapsed');
      });
    });
  }

  /* ========================================
     DAY PILL NAVIGATION
     ======================================== */
  document.querySelectorAll('.day-pill').forEach(function (pill) {
    pill.addEventListener('click', function (e) {
      e.preventDefault();
      var dayId = this.getAttribute('data-day') || this.getAttribute('href').substring(1);
      var target = document.getElementById(dayId);
      if (!target) return;

      // Ensure we're on itinerary tab
      if (currentTab !== 'tab-itinerary') {
        switchTab('tab-itinerary');
      }

      // Expand the target day card
      target.classList.remove('collapsed');

      // Scroll to it
      setTimeout(function () {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);

      // Update active pill
      document.querySelectorAll('.day-pill').forEach(function (p) { p.classList.remove('active'); });
      this.classList.add('active');
    });
  });

  /* ========================================
     SCROLL PROGRESS BAR
     ======================================== */
  function updateProgress() {
    var scrollTop = window.scrollY;
    var docHeight = document.documentElement.scrollHeight - window.innerHeight;
    var pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    if (progressBar) progressBar.style.width = pct + '%';
  }

  /* ========================================
     ACTIVE DAY TRACKING ON SCROLL
     ======================================== */
  function updateActiveDayPill() {
    if (currentTab !== 'tab-itinerary') return;

    var scrollY = window.scrollY + 150;
    var currentDay = '';
    document.querySelectorAll('.day-card').forEach(function (card) {
      if (card.offsetTop <= scrollY) {
        currentDay = card.id;
      }
    });

    document.querySelectorAll('.day-pill').forEach(function (pill) {
      var pillDay = pill.getAttribute('data-day') || pill.getAttribute('href').substring(1);
      pill.classList.toggle('active', pillDay === currentDay);
    });
  }

  /* ========================================
     SCROLL HANDLER (throttled)
     ======================================== */
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (!ticking) {
      requestAnimationFrame(function () {
        updateProgress();
        updateActiveDayPill();
        ticking = false;
      });
      ticking = true;
    }
  });
  updateProgress();

  /* ========================================
     NAV BRAND → Home / Map
     ======================================== */
  var navBrand = document.getElementById('nav-brand');
  if (navBrand) {
    navBrand.addEventListener('click', function (e) {
      e.preventDefault();
      switchTab('tab-map');
      if (hero) {
        hero.style.display = '';
        hero.classList.remove('compact');
      }
    });
  }

  /* ========================================
     SERVICE WORKER
     ======================================== */
  if ('serviceWorker' in navigator) {
    // Force clear old caches, then re-register
    caches.keys().then(function(names) {
      names.forEach(function(name) { caches.delete(name); });
    });
    navigator.serviceWorker.getRegistrations().then(function(regs) {
      regs.forEach(function(reg) { reg.unregister(); });
    }).then(function() {
      navigator.serviceWorker.register('sw.js').catch(function () {});
    });
  }

})();
