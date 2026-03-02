#!/usr/bin/env python3
"""Add interactive Leaflet map + Wikimedia photos to the Yunnan guide."""

import re

# ============================================================
# LOCATION DATA — every major spot on the itinerary
# ============================================================
locations = [
    {
        "id": "dayan",
        "name": "Dayan Old Town (大研古城)",
        "lat": 26.8724,
        "lng": 100.2260,
        "day": "D1–D4",
        "desc": "UNESCO World Heritage Naxi old town. 354 stone bridges, 3-tier water system, Sifang Square market center.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/1_lijiang_old_town_2012.jpg/800px-1_lijiang_old_town_2012.jpg",
        "photo_caption": "Dayan Old Town canal at dusk"
    },
    {
        "id": "black-dragon",
        "name": "Black Dragon Pool (黑龍潭)",
        "lat": 26.8850,
        "lng": 100.2280,
        "day": "D2",
        "desc": "Spring-fed pool with cyan-blue water. Classic view: Deyue Pavilion reflected with Jade Dragon Snow Mountain behind. Home to the Dongba Culture Museum.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Lijiang_Yunnan_China-Heilongtan-Park-01.jpg/800px-Lijiang_Yunnan_China-Heilongtan-Park-01.jpg",
        "photo_caption": "Black Dragon Pool with Jade Dragon Snow Mountain"
    },
    {
        "id": "baisha",
        "name": "Baisha Old Town (白沙古鎮)",
        "lat": 26.9085,
        "lng": 100.1690,
        "day": "D2",
        "desc": "Original Naxi capital before Lijiang. Home to the Baisha Murals — 14th-16th century Buddhist/Taoist/Dongba paintings by Han, Tibetan, and Naxi artists.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Baisha_Old_Town%2CLiJiang.jpg/800px-Baisha_Old_Town%2CLiJiang.jpg",
        "photo_caption": "Baisha Old Town with mountain backdrop"
    },
    {
        "id": "jade-dragon",
        "name": "Jade Dragon Snow Mountain (玉龍雪山)",
        "lat": 27.1167,
        "lng": 100.1833,
        "day": "D3",
        "desc": "Sacred Naxi mountain, 5,596m. Never summited (religious prohibition). Cable car to 4,506m. Glacier, Blue Moon Valley, Impressions Lijiang show.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Jade_Dragon_Snow_Mountain%2C_September_2019.jpg/800px-Jade_Dragon_Snow_Mountain%2C_September_2019.jpg",
        "photo_caption": "Jade Dragon Snow Mountain from Lijiang"
    },
    {
        "id": "blue-moon",
        "name": "Blue Moon Valley (藍月谷)",
        "lat": 27.0910,
        "lng": 100.1920,
        "day": "D3",
        "desc": "Series of glacial meltwater lakes — turquoise to electric blue from suspended glacial flour. Jade Lake, Pearl Shoal, Blue Moon Lake.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Blue_Moon_Valley_%2820171107135428%29.jpg/800px-Blue_Moon_Valley_%2820171107135428%29.jpg",
        "photo_caption": "Blue Moon Valley's turquoise glacial lakes"
    },
    {
        "id": "yuhu",
        "name": "Yuhu Village (玉湖村)",
        "lat": 27.0400,
        "lng": 100.1850,
        "day": "D3",
        "desc": "Joseph Rock's base for 27 years. His preserved house is now a museum. Naxi home visits here connect to descendants of families who hosted Rock.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Yuhu-village-china-2.jpg/800px-Yuhu-village-china-2.jpg",
        "photo_caption": "Yuhu Village at the foot of Jade Dragon Snow Mountain"
    },
    {
        "id": "lashi",
        "name": "Lashi Lake (拉市海)",
        "lat": 26.8580,
        "lng": 100.1150,
        "day": "D4",
        "desc": "Where the Tea Horse Road originated. Horseback trails follow the ancient caravan routes. Migratory bird wetland — bar-headed geese fly over the Himalayas.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Lashihai1.jpg/800px-Lashihai1.jpg",
        "photo_caption": "Lashi Lake wetland"
    },
    {
        "id": "shuhe",
        "name": "Shuhe Old Town (束河古鎮)",
        "lat": 26.9030,
        "lng": 100.2070,
        "day": "D4",
        "desc": "Older than Dayan, historically known for leather goods for Tea Horse Road caravans. UNESCO-listed. Jiuding Dragon Pool spring complex.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Shuhe_ancient_town_in_lijiang.JPG/800px-Shuhe_ancient_town_in_lijiang.JPG",
        "photo_caption": "Shuhe Old Town"
    },
    {
        "id": "tiger-leaping",
        "name": "Tiger Leaping Gorge (虎跳峽)",
        "lat": 27.1850,
        "lng": 100.1100,
        "day": "D5",
        "desc": "One of the deepest gorges on Earth — 3,900m from river to summit. The Jinsha River (upper Yangtze) at its most dramatic. Named for a tiger's legendary leap.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Hutiaoxia.jpg/800px-Hutiaoxia.jpg",
        "photo_caption": "Tiger Leaping Gorge — the Jinsha River below"
    },
    {
        "id": "shaxi",
        "name": "Shaxi (沙溪)",
        "lat": 26.3150,
        "lng": 99.9250,
        "day": "D5–D6",
        "desc": "Only surviving Tea Horse Road market town with original market square intact. Sideng Square, Xingjiao Temple, original caravanserai archways. UNESCO restored.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Shaxi_Old_Town.jpg/800px-Shaxi_Old_Town.jpg",
        "photo_caption": "Shaxi's Sideng Square"
    },
    {
        "id": "dali",
        "name": "Dali Old Town (大理古城)",
        "lat": 25.6940,
        "lng": 100.1540,
        "day": "D6–D7",
        "desc": "Former Kingdom of Nanzhao/Dali. Defeated Tang Dynasty armies in 754 AD. Catholic church with Bai-European fusion architecture. Three Pagodas nearby.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/The_Three_Pagodas_of_Chongsheng_Temple%2C_April_2018.jpg/800px-The_Three_Pagodas_of_Chongsheng_Temple%2C_April_2018.jpg",
        "photo_caption": "Three Pagodas of Chongsheng Temple, Dali"
    },
    {
        "id": "xizhou",
        "name": "Xizhou Village (喜洲)",
        "lat": 25.8530,
        "lng": 100.1200,
        "day": "D7",
        "desc": "Best-preserved Bai village architecture. Elaborate screen walls (照壁), nested courtyards. Yan Family Compound. Tie-dye workshop nearby.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Xizhou_%E5%96%9C%E6%B4%B2_-_panoramio.jpg/800px-Xizhou_%E5%96%9C%E6%B4%B2_-_panoramio.jpg",
        "photo_caption": "Traditional Bai architecture in Xizhou"
    },
    {
        "id": "erhai",
        "name": "Erhai Lake (洱海)",
        "lat": 25.7800,
        "lng": 100.2000,
        "day": "D7",
        "desc": "250 km² lake at 1,974m. 'Ear Sea' from its shape. Historical highway for the Bai kingdom. Cycling route at Longkan Wharf with Cangshan Mountain views.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Erhai_Lake_from_Jizu_Mountain.JPG/800px-Erhai_Lake_from_Jizu_Mountain.JPG",
        "photo_caption": "Erhai Lake with Cangshan Mountains"
    },
]

# Day route colors
day_colors = {
    "D1": "#c2583a",  # terracotta
    "D2": "#c2583a",
    "D3": "#4a7c6f",  # jade
    "D4": "#4a7c6f",
    "D5": "#2c3e6b",  # indigo
    "D6": "#2c3e6b",
    "D7": "#c9a84c",  # gold
    "D8": "#8a8279",  # gray
}

# Route connections (day-by-day path)
routes = [
    # D1-D4: Lijiang area
    {"day": "D2", "points": [("dayan", "black-dragon"), ("black-dragon", "baisha")]},
    {"day": "D3", "points": [("dayan", "jade-dragon"), ("jade-dragon", "blue-moon"), ("blue-moon", "yuhu")]},
    {"day": "D4", "points": [("dayan", "lashi"), ("lashi", "shuhe")]},
    # D5: TLG to Shaxi
    {"day": "D5", "points": [("shuhe", "tiger-leaping"), ("tiger-leaping", "shaxi")]},
    # D6: Shaxi to Dali
    {"day": "D6", "points": [("shaxi", "dali")]},
    # D7: Dali area
    {"day": "D7", "points": [("dali", "xizhou"), ("xizhou", "erhai")]},
]

# Build location lookup
loc_lookup = {l["id"]: l for l in locations}

# ============================================================
# Generate map HTML section and photo gallery sections
# ============================================================

# Map section HTML
markers_js = ""
for loc in locations:
    popup = f"""<div style="max-width:260px">
<img src="{loc['photo']}" style="width:100%;border-radius:6px;margin-bottom:8px" alt="{loc['photo_caption']}" loading="lazy">
<strong style="font-size:14px">{loc['name']}</strong><br>
<span style="display:inline-block;background:#c2583a;color:#fff;padding:2px 8px;border-radius:10px;font-size:11px;margin:4px 0">{loc['day']}</span><br>
<span style="font-size:12px;color:#5a5650;line-height:1.4">{loc['desc']}</span>
</div>""".replace('\n', '').replace("'", "\\'")
    markers_js += f"  L.marker([{loc['lat']}, {loc['lng']}]).addTo(map).bindPopup('{popup}');\n"

# Route lines
route_lines_js = ""
for route in routes:
    for start_id, end_id in route["points"]:
        s = loc_lookup[start_id]
        e = loc_lookup[end_id]
        color = day_colors.get(route["day"], "#888")
        route_lines_js += f"  L.polyline([[{s['lat']},{s['lng']}],[{e['lat']},{e['lng']}]], {{color:'{color}',weight:3,opacity:0.6,dashArray:'8 6'}}).addTo(map);\n"

map_section_html = f'''
<section class="section" id="map" data-nav-id="map" style="scroll-margin-top:calc(var(--nav-height) + 16px)">
  <span class="section-number">Interactive Map</span>
  <h2 class="section-header">Your Route Through Yunnan</h2>
  <p style="margin-bottom:16px;font-size:0.9rem;color:var(--warm-gray)">Tap any marker to see photos and details. Dashed lines show your day-by-day route.</p>
  <div id="yunnan-map" style="width:100%;height:420px;border-radius:var(--radius);border:1px solid var(--border);overflow:hidden;margin-bottom:24px"></div>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"><\/script>
  <script>
  (function(){{
    var map = L.map('yunnan-map', {{scrollWheelZoom: false}}).setView([26.5, 100.15], 8);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      attribution: '&copy; OpenStreetMap',
      maxZoom: 17
    }}).addTo(map);
{markers_js}
{route_lines_js}
    // Fit bounds
    var bounds = L.latLngBounds([{', '.join(f'[{l["lat"]},{l["lng"]}]' for l in locations)}]);
    map.fitBounds(bounds.pad(0.15));
  }})();
  <\/script>
</section>'''

# ============================================================
# Photo gallery per day section
# ============================================================

# Group photos by day
day_photos = {}
for loc in locations:
    days = loc["day"].replace("–", "-").split("-")
    primary_day = days[0].strip()
    if primary_day not in day_photos:
        day_photos[primary_day] = []
    day_photos[primary_day].append(loc)

photo_css = '''
/* === PHOTO GALLERY === */
.photo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  margin: 16px 0;
}
.photo-card {
  border-radius: var(--radius-sm);
  overflow: hidden;
  border: 1px solid var(--border);
  background: var(--cream-dark);
}
.photo-card img {
  width: 100%;
  height: 160px;
  object-fit: cover;
  display: block;
}
.photo-card-caption {
  padding: 8px 10px;
  font-size: 0.78rem;
  color: var(--charcoal-light);
  line-height: 1.3;
}
.photo-card-caption strong {
  display: block;
  color: var(--charcoal);
  font-size: 0.82rem;
  margin-bottom: 2px;
}

/* Map section */
#yunnan-map .leaflet-popup-content-wrapper {
  border-radius: 10px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}
#yunnan-map .leaflet-popup-content {
  margin: 12px;
}
'''

# ============================================================
# Now patch the existing files
# ============================================================

# Read current index.html
with open('index.html', 'r') as f:
    html = f.read()

# 1. Add map section after the hero, before main content sections
# Insert map after opening of <main class="content">
html = html.replace(
    '<main class="content">',
    f'<main class="content">\n{map_section_html}\n'
)

# 2. Add photo grids inside each day card body (after existing content)
for day_key, photos in sorted(day_photos.items()):
    if not photos:
        continue
    day_num = day_key.replace("D", "")
    
    photo_grid = '<div class="photo-grid">\n'
    for p in photos:
        photo_grid += f'''  <div class="photo-card">
    <img src="{p['photo']}" alt="{p['photo_caption']}" loading="lazy">
    <div class="photo-card-caption"><strong>{p['name']}</strong>{p['photo_caption']}</div>
  </div>\n'''
    photo_grid += '</div>'
    
    # Insert before closing </div> of day-card-body for this day
    marker = f'id="day{day_num}"'
    if marker in html:
        # Find the day card body end — look for the closing pattern
        day_start = html.find(marker)
        # Find the day-card-body div
        body_start = html.find('class="day-card-body"', day_start)
        if body_start != -1:
            # Find the last </div> that closes the day-card-body before next day-card
            next_day_marker = f'id="day{int(day_num)+1}"' if int(day_num) < 8 else '</section>'
            next_day_pos = html.find(next_day_marker, body_start)
            if next_day_pos == -1:
                next_day_pos = len(html)
            
            # Insert photo grid before the closing </div></div> of this day card
            # Go backwards from next_day_pos to find </div>\n</div>
            search_region = html[body_start:next_day_pos]
            # Find last occurrence of </div> before next card
            last_close = search_region.rfind('</div>')
            second_last = search_region.rfind('</div>', 0, last_close)
            if second_last != -1:
                insert_pos = body_start + second_last
                html = html[:insert_pos] + f'\n    {photo_grid}\n  ' + html[insert_pos:]

# 3. Add map and photos nav items to menu
html = html.replace(
    '<div class="menu-section-label">Sections</div>',
    '<div class="menu-section-label">Sections</div>\n<a href="#map">🗺️ Interactive Map</a>'
)

# 4. Add map to TOC sidebar  
html = html.replace(
    '<div class="toc-label">Sections</div>',
    '<div class="toc-label">Sections</div>\n<a href="#map">🗺️ Map</a>'
)

# 5. Fix script tags (the \/ escaping)
html = html.replace('<\\/script>', '</script>')

# Write updated index.html
with open('index.html', 'w') as f:
    f.write(html)

# Append photo CSS to style.css
with open('style.css', 'a') as f:
    f.write('\n' + photo_css)

print(f"✅ Updated index.html ({len(html):,} bytes)")
print(f"✅ Added {len(locations)} map markers")
print(f"✅ Added {sum(len(v) for v in day_photos.values())} photo cards across {len(day_photos)} days")
print(f"✅ Added route lines for {len(routes)} day routes")
print(f"✅ Appended photo/map CSS to style.css")
