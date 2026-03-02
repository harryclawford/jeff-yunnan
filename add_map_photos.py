#!/usr/bin/env python3
"""Add interactive Leaflet map and Wikimedia photos to the Yunnan guide."""

import re

# Read current index.html
with open('index.html', 'r') as f:
    html = f.read()

# === MAP DATA ===
# All key locations with coords, descriptions, day associations
map_locations = [
    {"name": "Dayan Old Town (大研古城)", "lat": 26.8724, "lng": 100.2257, "day": "D1-D2", "desc": "UNESCO World Heritage Naxi old town. 354 stone bridges, three-tier water system.", "icon": "🏘️"},
    {"name": "Black Dragon Pool (黑龍潭)", "lat": 26.8874, "lng": 100.2270, "day": "D2", "desc": "Spring-fed pool with iconic Jade Dragon Snow Mountain reflections. Home to Dongba Culture Museum.", "icon": "💧"},
    {"name": "Baisha Old Town (白沙古镇)", "lat": 26.9195, "lng": 100.2095, "day": "D2", "desc": "Original Naxi capital. Famous Baisha Murals — Buddhist/Taoist/Dongba fusion art from 14th-16th century.", "icon": "🎨"},
    {"name": "Jade Dragon Snow Mountain (玉龍雪山)", "lat": 27.1215, "lng": 100.1865, "day": "D3", "desc": "Sacred Naxi peak at 5,596m. Never summited — religious prohibition. Cable car to 4,506m.", "icon": "🏔️"},
    {"name": "Blue Moon Valley (藍月谷)", "lat": 27.0858, "lng": 100.2074, "day": "D3", "desc": "Glacial meltwater lakes in turquoise, jade green, and electric blue. Rayleigh scattering from glacial flour.", "icon": "💎"},
    {"name": "Yuhu Village (玉湖村)", "lat": 27.0036, "lng": 100.1894, "day": "D3", "desc": "Joseph Rock's base for 27 years. Naxi home visits. Tolkien reportedly drew Middle Earth inspiration from Rock's photos.", "icon": "🏡"},
    {"name": "Lashi Lake (拉市海)", "lat": 26.8400, "lng": 100.0800, "day": "D4", "desc": "Tea Horse Road origin point. Horseback trails on original caravan routes. Migratory bird wetland.", "icon": "🐎"},
    {"name": "Shuhe Old Town (束河古镇)", "lat": 26.9065, "lng": 100.2550, "day": "D4", "desc": "Older than Dayan. Historic leather crafting hub for Tea Horse Road caravans. UNESCO listed.", "icon": "🏘️"},
    {"name": "Tiger Leaping Gorge (虎跳峡)", "lat": 27.1844, "lng": 100.1147, "day": "D5", "desc": "One of Earth's deepest gorges — 3,900m from river to summit. The Jinsha (upper Yangtze) at its most dramatic.", "icon": "🐅"},
    {"name": "Shaxi / Sideng Square (沙溪)", "lat": 26.2916, "lng": 99.8958, "day": "D5-D6", "desc": "Only intact Tea Horse Road market square. UNESCO restored. Xingjiao Temple shows Tibetan Buddhist influence.", "icon": "🏛️"},
    {"name": "Dali Old Town (大理古城)", "lat": 25.6986, "lng": 100.1625, "day": "D6", "desc": "Former Nanzhao/Dali Kingdom territory. Ming-dynasty layout. Catholic church with Bai-European fusion architecture.", "icon": "⛩️"},
    {"name": "Three Pagodas (崇圣寺三塔)", "lat": 25.7278, "lng": 100.1425, "day": "D6", "desc": "Main pagoda 69m tall, built 823-840 AD during Nanzhao. Serious state investment in Buddhist architecture.", "icon": "🗼"},
    {"name": "Xizhou Village (喜洲)", "lat": 25.8175, "lng": 100.1278, "day": "D7", "desc": "Best-preserved Bai architecture. Spectacular screen walls (照壁). Yan Family Compound.", "icon": "🏘️"},
    {"name": "Erhai Lake / Longkan Wharf", "lat": 25.7500, "lng": 100.1800, "day": "D7", "desc": "250 km² lake at 1,974m. Historical Bai water highway. Cycling route with Cangshan mountain views.", "icon": "🚲"},
]

# === PHOTO DATA ===
# Wikimedia Commons images (free, CC licensed)
photos = {
    "overview": [
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/1_lijiang_old_town_2012.jpg/1280px-1_lijiang_old_town_2012.jpg", "Lijiang Old Town — UNESCO World Heritage"),
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Jade_Dragon_Snow_Mountain_2.jpg/1280px-Jade_Dragon_Snow_Mountain_2.jpg", "Jade Dragon Snow Mountain from Lijiang"),
    ],
    "day1": [
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/1_lijiang_old_town_2012.jpg/800px-1_lijiang_old_town_2012.jpg", "Dayan Old Town canals at dusk"),
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Mu_Fu%2C_Lijiang.jpg/800px-Mu_Fu%2C_Lijiang.jpg", "Mu Family Mansion (木府)"),
    ],
    "day2": [
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Lijiang_Yunnan_China-Heilongtan-Park-01.jpg/800px-Lijiang_Yunnan_China-Heilongtan-Park-01.jpg", "Black Dragon Pool — classic Jade Dragon reflection"),
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Baisha_Murals_Lijiang.jpg/800px-Baisha_Murals_Lijiang.jpg", "Baisha Old Town"),
    ],
    "day3": [
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Jade_Dragon_Snow_Mountain_2.jpg/800px-Jade_Dragon_Snow_Mountain_2.jpg", "Jade Dragon Snow Mountain — 13 peaks, 5,596m"),
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Blue_Moon_Valley%2C_Lijiang.jpg/800px-Blue_Moon_Valley%2C_Lijiang.jpg", "Blue Moon Valley glacial lakes"),
    ],
    "day4": [
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Lashihai-horses.jpg/800px-Lashihai-horses.jpg", "Lashi Lake — Tea Horse Road horseback trails"),
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Shuhe_old_town.jpg/800px-Shuhe_old_town.jpg", "Shuhe Old Town"),
    ],
    "day5": [
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Tiger_leaping_gorge_2.jpg/1280px-Tiger_leaping_gorge_2.jpg", "Tiger Leaping Gorge — 3,900m deep"),
    ],
    "day6": [
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Shaxi_Pear_Orchard_Temple.jpg/800px-Shaxi_Pear_Orchard_Temple.jpg", "Shaxi — Sideng Square area"),
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Dali_old_town.jpg/800px-Dali_old_town.jpg", "Dali Old Town gate"),
    ],
    "day7": [
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Three_Pagodas-1.JPG/800px-Three_Pagodas-1.JPG", "Three Pagodas of Chongsheng Temple (崇圣寺三塔)"),
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Erhai_Lake.JPG/800px-Erhai_Lake.JPG", "Erhai Lake with Cangshan mountains"),
    ],
}

# === BUILD MAP SECTION HTML ===
markers_js = "[\n"
for loc in map_locations:
    markers_js += f'  {{name:"{loc["name"]}",lat:{loc["lat"]},lng:{loc["lng"]},day:"{loc["day"]}",desc:"{loc["desc"]}",icon:"{loc["icon"]}"}},\n'
markers_js += "]"

map_section_html = f'''
<section class="section" id="map" data-nav-id="map" style="margin-bottom:48px;scroll-margin-top:calc(var(--nav-height) + 16px)">
  <span class="section-number">Interactive Map</span>
  <h2 class="section-header">Your Route Through Yunnan</h2>
  <p style="margin-bottom:16px;font-size:0.9rem;color:var(--warm-gray)">Tap any marker to see details. Pinch to zoom. The route follows the ancient Tea Horse Road south from Lijiang to Dali.</p>
  <div id="yn-map" style="width:100%;height:480px;border-radius:var(--radius);border:1px solid var(--border);overflow:hidden;z-index:1"></div>
</section>
'''

map_script = f'''
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
(function() {{
  var map = L.map('yn-map', {{
    center: [26.5, 100.15],
    zoom: 8,
    scrollWheelZoom: false,
    zoomControl: true
  }});
  L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
    attribution: '&copy; OpenStreetMap',
    maxZoom: 18
  }}).addTo(map);

  var locs = {markers_js};
  var markers = [];
  var dayColors = {{
    'D1-D2': '#c2583a',
    'D2': '#c2583a',
    'D3': '#4a7c6f',
    'D4': '#4a7c6f',
    'D5': '#2c3e6b',
    'D5-D6': '#2c3e6b',
    'D6': '#5a6fa0',
    'D7': '#c9a84c',
  }};
  locs.forEach(function(loc) {{
    var color = dayColors[loc.day] || '#c2583a';
    var icon = L.divIcon({{
      className: 'yn-marker',
      html: '<div style="background:' + color + ';color:#fff;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;box-shadow:0 2px 8px rgba(0,0,0,0.3);border:2px solid #fff">' + loc.icon + '</div>',
      iconSize: [32, 32],
      iconAnchor: [16, 16],
      popupAnchor: [0, -20]
    }});
    var m = L.marker([loc.lat, loc.lng], {{icon: icon}}).addTo(map);
    m.bindPopup('<div style="font-family:Inter,sans-serif;max-width:220px"><strong style="font-size:0.95rem">' + loc.name + '</strong><br><span style="display:inline-block;margin:4px 0;padding:2px 8px;border-radius:10px;background:' + color + ';color:#fff;font-size:0.7rem;font-weight:600">' + loc.day + '</span><br><span style="font-size:0.82rem;color:#555;line-height:1.4">' + loc.desc + '</span></div>', {{closeButton: false}});
    markers.push(m);
  }});

  // Draw route line
  var routeCoords = locs.map(function(l) {{ return [l.lat, l.lng]; }});
  L.polyline(routeCoords, {{color: '#c2583a', weight: 2, opacity: 0.5, dashArray: '8 6'}}).addTo(map);

  // Fit bounds
  var group = L.featureGroup(markers);
  map.fitBounds(group.getBounds().pad(0.1));
}})();
</script>
'''

# === BUILD PHOTO GALLERY CSS ===
photo_css = '''
<style>
.photo-gallery { display:grid; grid-template-columns:1fr; gap:12px; margin:18px 0; }
@media(min-width:500px) { .photo-gallery.two-col { grid-template-columns:1fr 1fr; } }
.photo-card { border-radius:var(--radius-sm); overflow:hidden; border:1px solid var(--border); }
.photo-card img { width:100%; height:200px; object-fit:cover; display:block; background:var(--cream-dark); }
.photo-card figcaption { padding:8px 12px; font-size:0.78rem; color:var(--warm-gray); line-height:1.4; }
</style>
'''

def photo_gallery_html(key):
    """Generate photo gallery HTML for a given key."""
    if key not in photos:
        return ""
    items = photos[key]
    cols = "two-col" if len(items) > 1 else ""
    cards = ""
    for url, caption in items:
        cards += f'''<figure class="photo-card">
  <img src="{url}" alt="{caption}" loading="lazy" onerror="this.style.display='none'">
  <figcaption>{caption}</figcaption>
</figure>
'''
    return f'<div class="photo-gallery {cols}">\n{cards}</div>\n'

# === INJECT INTO HTML ===

# 1. Add photo CSS before </head>
html = html.replace('</head>', photo_css + '</head>')

# 2. Add map section after the hero, before main content starts
html = html.replace('<main class="content">', '<main class="content">\n' + map_section_html)

# 3. Add map script + Leaflet before </body>
html = html.replace('</body>', map_script + '\n</body>')

# 4. Add photos to day cards — inject after each day-card-body opening
for d in range(1, 9):
    key = f"day{d}"
    gallery = photo_gallery_html(key)
    if gallery:
        # Find the day card body and inject photos at the top
        marker = f'id="day{d}" data-nav-id="day{d}">'
        idx = html.find(marker)
        if idx != -1:
            # Find the <div class="day-card-body"> within this card
            body_marker = '<div class="day-card-body">'
            body_idx = html.find(body_marker, idx)
            if body_idx != -1:
                insert_pos = body_idx + len(body_marker)
                html = html[:insert_pos] + '\n' + gallery + html[insert_pos:]

# 5. Add overview photos after the overview section header
overview_gallery = photo_gallery_html("overview")
overview_marker = 'id="overview" data-nav-id="overview">'
ov_idx = html.find(overview_marker)
if ov_idx != -1:
    # Find first <p after the section header
    first_p = html.find('<p data-search=', ov_idx)
    if first_p != -1:
        html = html[:first_p] + overview_gallery + html[first_p:]

# 6. Add map to navigation menus
html = html.replace('<a href="#overview">Yunnan Overview</a>', '<a href="#map">🗺️ Interactive Map</a>\n<a href="#overview">Yunnan Overview</a>')
html = html.replace('<a href="#overview">Yunnan Overview</a>', '<a href="#map">🗺️ Interactive Map</a>\n<a href="#overview">Yunnan Overview</a>', 1)

# Write
with open('index.html', 'w') as f:
    f.write(html)

print(f"✅ Updated index.html ({len(html):,} bytes)")
print(f"   - Interactive Leaflet map with {len(map_locations)} markers")
print(f"   - Photo galleries added to {len(photos)} sections")
