/* === YUNNAN GUIDE — SCRIPT.JS === */
(function () {
  'use strict';

  /* --- DOM REFS --- */
  const menuBtn = document.getElementById('menu-btn');
  const menuOverlay = document.getElementById('menu-overlay');
  const searchBtn = document.getElementById('search-btn');
  const searchOverlay = document.getElementById('search-overlay');
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');
  const themeBtn = document.getElementById('theme-btn');
  const qrFab = document.getElementById('qr-fab');
  const qrSheet = document.getElementById('qr-sheet');
  const qrClose = document.getElementById('qr-close');
  const progressBar = document.getElementById('progress-bar');
  const dayStrip = document.getElementById('day-strip');

  /* --- MOBILE MENU --- */
  menuBtn.addEventListener('click', function () {
    menuOverlay.classList.toggle('open');
    menuBtn.textContent = menuOverlay.classList.contains('open') ? '✕' : '☰';
  });
  menuOverlay.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () {
      menuOverlay.classList.remove('open');
      menuBtn.textContent = '☰';
    });
  });

  /* --- DARK MODE --- */
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

  /* --- SEARCH --- */
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
        var snippet = (start > 0 ? '...' : '') +
          item.text.substring(start, idx) +
          '<mark>' + item.text.substring(idx, idx + q.length) + '</mark>' +
          item.text.substring(idx + q.length, end) +
          (end < item.text.length ? '...' : '');
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
        hits[i].el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Expand if collapsed
        var parent = hits[i].el.closest('.collapsible-content');
        if (parent && parent.style.maxHeight === '0px') {
          var toggle = parent.previousElementSibling;
          if (toggle && toggle.classList.contains('collapsible-toggle')) toggle.click();
        }
        searchOverlay.classList.remove('open');
        searchInput.value = '';
        searchResults.innerHTML = '';
      });
    });
  });

  /* --- COLLAPSIBLES --- */
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

  /* --- CONVERSATION STARTER ACCORDIONS --- */
  document.querySelectorAll('.convo-question').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var answer = this.nextElementSibling;
      var isOpen = answer.style.maxHeight && answer.style.maxHeight !== '0px';
      if (isOpen) {
        answer.style.maxHeight = '0px';
      } else {
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    });
  });

  /* --- QUICK REFERENCE SHEET --- */
  qrFab.addEventListener('click', function () { qrSheet.classList.toggle('open'); });
  qrClose.addEventListener('click', function () { qrSheet.classList.remove('open'); });
  document.querySelectorAll('.qr-tab').forEach(function (tab) {
    tab.addEventListener('click', function () {
      document.querySelectorAll('.qr-tab').forEach(function (t) { t.classList.remove('active'); });
      document.querySelectorAll('.qr-panel').forEach(function (p) { p.classList.remove('active'); });
      this.classList.add('active');
      document.getElementById(this.dataset.panel).classList.add('active');
    });
  });

  /* --- SCROLL PROGRESS --- */
  function updateProgress() {
    var scrollTop = window.scrollY;
    var docHeight = document.documentElement.scrollHeight - window.innerHeight;
    var pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    progressBar.style.width = pct + '%';
  }

  /* --- ACTIVE SECTION TRACKING --- */
  var navSections = [];
  document.querySelectorAll('[data-nav-id]').forEach(function (el) {
    navSections.push({ id: el.getAttribute('data-nav-id'), el: el });
  });
  var dayPills = document.querySelectorAll('.day-pill');
  var tocLinks = document.querySelectorAll('.toc-sidebar a');

  function updateActiveSection() {
    var scrollY = window.scrollY + 120;
    var current = '';
    navSections.forEach(function (s) {
      if (s.el.offsetTop <= scrollY) current = s.id;
    });
    dayPills.forEach(function (p) {
      p.classList.toggle('active', p.getAttribute('href') === '#' + current);
    });
    tocLinks.forEach(function (a) {
      a.classList.toggle('active', a.getAttribute('href') === '#' + current);
    });
  }

  /* --- DAY STRIP VISIBILITY --- */
  var daysSection = document.getElementById('days');
  function updateDayStrip() {
    if (!daysSection) return;
    var rect = daysSection.getBoundingClientRect();
    var show = rect.top < 100 && rect.bottom > 100;
    dayStrip.classList.toggle('show', show);
  }

  /* --- SCROLL HANDLER --- */
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (!ticking) {
      requestAnimationFrame(function () {
        updateProgress();
        updateActiveSection();
        updateDayStrip();
        ticking = false;
      });
      ticking = true;
    }
  });
  updateProgress();

  /* --- SERVICE WORKER REGISTRATION --- */
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js').catch(function () {});
  }
})();
