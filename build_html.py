#!/usr/bin/env python3
"""Build index.html for the Yunnan guide from guide-content.txt and existing CSS/JS."""

import re

def escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def md_inline(text):
    """Convert basic inline formatting."""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    return text

# Read content
with open('guide-content.txt', 'r') as f:
    raw = f.read()

# Weather data per day
weather = {
    'D1': ('☀️', '5–23°C', 'Clear skies'),
    'D2': ('⛅', '7–22°C', 'Partly cloudy'),
    'D3': ('🌧️', '6–13°C', 'Drizzle — cold front'),
    'D4': ('🌧️', '7–14°C', 'Light rain'),
    'D5': ('🌧️', '8–17°C', 'Light drizzle'),
    'D6': ('🌧️', '7–10°C', 'Drizzle — coldest day'),
    'D7': ('🌧️', '8–12°C', 'Light drizzle'),
    'D8': ('🌧️', '9–13°C', 'Drizzle'),
}

hotels = {
    'D1': 'Kuanshang Lijiang',
    'D2': 'Kuanshang Lijiang',
    'D3': 'Kuanshang Lijiang',
    'D4': 'Kuanshang Lijiang',
    'D5': 'Sunyata Shaxi',
    'D6': 'Daji Dali',
    'D7': 'Daji Dali',
    'D8': 'Depart DLU → CAN',
}

day_dates = {
    'D1': 'March 8',
    'D2': 'March 9',
    'D3': 'March 10',
    'D4': 'March 11',
    'D5': 'March 12',
    'D6': 'March 13',
    'D7': 'March 14',
    'D8': 'March 15',
}

day_titles = {
    'D1': 'Arrive Lijiang, Dayan Old Town',
    'D2': 'Black Dragon Pool, Dayan, Baisha',
    'D3': 'Jade Dragon Snow Mountain, Blue Moon Valley, Yuhu',
    'D4': 'Lashi Lake Horseback, Shuhe Old Town',
    'D5': 'Tiger Leaping Gorge → Shaxi',
    'D6': 'Shaxi Village, Dali Old Town',
    'D7': 'Xizhou, Mushroom Hotpot, Tie-Dye, Erhai Lake',
    'D8': 'Depart Dali',
}

# Now let's parse the content file into sections
# We'll manually structure the HTML based on the known sections

def read_section(start_marker, end_marker=None):
    """Extract text between markers from the raw content."""
    start = raw.find(start_marker)
    if start == -1:
        return ""
    start = raw.find('\n', start) + 1
    if end_marker:
        end = raw.find(end_marker, start)
        if end == -1:
            end = len(raw)
    else:
        end = len(raw)
    return raw[start:end].strip()

def text_to_html(text, section_name=""):
    """Convert plain text section to HTML with proper formatting."""
    lines = text.split('\n')
    html_parts = []
    in_list = False
    para_buffer = []
    
    def flush_para():
        nonlocal para_buffer
        if para_buffer:
            content = ' '.join(para_buffer)
            content = md_inline(escape(content))
            html_parts.append(f'<p data-search="{escape(section_name)}">{content}</p>')
            para_buffer = []
    
    def close_list():
        nonlocal in_list
        if in_list:
            html_parts.append('</ul>')
            in_list = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Skip separator lines
        if stripped.startswith('===') or stripped.startswith('---') and len(stripped) > 5:
            flush_para()
            close_list()
            i += 1
            continue
        
        # Empty line = paragraph break
        if not stripped:
            flush_para()
            close_list()
            i += 1
            continue
        
        # Subsection headers (~ delimited or ALL CAPS with specific patterns)
        if stripped.startswith('~ ') and stripped.endswith(' ~'):
            flush_para()
            close_list()
            title = stripped[2:-2].strip()
            html_parts.append(f'<h4 class="sub-subsection-title">{escape(title)}</h4>')
            i += 1
            continue
        
        # List items
        if stripped.startswith('- '):
            flush_para()
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            content = md_inline(escape(stripped[2:]))
            html_parts.append(f'<li data-search="{escape(section_name)}">{content}</li>')
            i += 1
            continue
        
        # Numbered list
        if re.match(r'^\d+\.?\s', stripped):
            flush_para()
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            content = re.sub(r'^\d+\.?\s*', '', stripped)
            content = md_inline(escape(content))
            html_parts.append(f'<li data-search="{escape(section_name)}">{content}</li>')
            i += 1
            continue
        
        # "The holy shit fact:" pattern → callout
        if 'holy shit fact' in stripped.lower():
            flush_para()
            close_list()
            # Collect the full fact paragraph
            fact_lines = [stripped]
            i += 1
            while i < len(lines) and lines[i].strip():
                fact_lines.append(lines[i].strip())
                i += 1
            fact_text = md_inline(escape(' '.join(fact_lines)))
            html_parts.append(f'''<div class="fact-callout">
  <div class="fact-callout-label">🤯 Holy Shit Fact</div>
  <p data-search="{escape(section_name)}">{fact_text}</p>
</div>''')
            continue
        
        # Regular paragraph line
        close_list()
        para_buffer.append(stripped)
        i += 1
    
    flush_para()
    close_list()
    return '\n'.join(html_parts)


# ===== PARSE EACH MAIN SECTION =====

sections_raw = {}

# Section markers in the file
section_markers = [
    ("1. YUNNAN OVERVIEW", "2. THE PEOPLES"),
    ("2. THE PEOPLES", "3. THE TEA HORSE ROAD"),
    ("3. THE TEA HORSE ROAD", "4. DAY-BY-DAY DEEP DIVES"),
    ("4. DAY-BY-DAY DEEP DIVES", "5. JADE DRAGON SNOW MOUNTAIN"),
    ("5. JADE DRAGON SNOW MOUNTAIN", "6. TIGER LEAPING GORGE"),
    ("6. TIGER LEAPING GORGE", "7. DALI & THE KINGDOM OF NANZHAO"),
    ("7. DALI & THE KINGDOM OF NANZHAO", "8. ZHANG YIMOU'S IMPRESSIONS LIJIANG"),
    ("8. ZHANG YIMOU'S IMPRESSIONS LIJIANG", "9. PU'ER TEA PRIMER"),
    ("9. PU'ER TEA PRIMER", "10. PRACTICAL CULTURAL TIPS"),
    ("10. PRACTICAL CULTURAL TIPS", "11. CONVERSATION STARTERS"),
    ("11. CONVERSATION STARTERS", "QUICK REFERENCE"),
]

# Extract raw section text
for start, end in section_markers:
    key = start.split('. ', 1)[1] if '. ' in start else start
    text = read_section(start, end)
    sections_raw[key] = text

# Also get quick reference
sections_raw['QUICK REFERENCE'] = read_section("QUICK REFERENCE: KEY CHINESE PHRASES", "FINAL NOTE")
sections_raw['FINAL NOTE'] = read_section("FINAL NOTE", "END OF GUIDE")

# Parse day sections from the day-by-day section
day_section_text = sections_raw.get("DAY-BY-DAY DEEP DIVES", "")

# Split by day markers
day_texts = {}
day_pattern = r'--- D(\d): '
day_splits = re.split(r'(--- D\d: )', day_section_text)

current_day = None
for part in day_splits:
    m = re.match(r'--- D(\d): ', part)
    if m:
        current_day = f"D{m.group(1)}"
    elif current_day:
        day_texts[current_day] = part.strip()
        current_day = None

# ===== BUILD THE HTML =====

# Section nav items
section_nav = [
    ("overview", "Yunnan Overview"),
    ("peoples", "The Peoples"),
    ("tea-horse-road", "Tea Horse Road"),
    ("days", "Day-by-Day"),
    ("jade-dragon", "Jade Dragon Snow Mountain"),
    ("tiger-leaping", "Tiger Leaping Gorge"),
    ("nanzhao", "Dali & Nanzhao"),
    ("impressions", "Impressions Lijiang"),
    ("puer", "Pu'er Tea Primer"),
    ("cultural-tips", "Cultural Tips"),
    ("conversation", "Conversation Starters"),
]

# Build menu overlay links
menu_html = '<div class="menu-section-label">Sections</div>\n'
for sid, label in section_nav:
    menu_html += f'<a href="#{sid}">{label}</a>\n'
menu_html += '<div class="menu-section-label">Days</div>\n'
for d in range(1, 9):
    menu_html += f'<a href="#day{d}">D{d} — {day_dates[f"D{d}"]}</a>\n'

# Day pills
day_pills = ''.join(f'<a class="day-pill" href="#day{d}">D{d}</a>' for d in range(1, 9))

# TOC sidebar
toc_html = '<div class="toc-label">Sections</div>\n'
for sid, label in section_nav:
    toc_html += f'<a href="#{sid}">{label}</a>\n'
toc_html += '<div class="toc-label">Days</div>\n'
for d in range(1, 9):
    toc_html += f'<a href="#day{d}">D{d} · {day_dates[f"D{d}"]}</a>\n'

# Build day cards
def build_day_card(day_num):
    dk = f"D{day_num}"
    w_icon, w_temp, w_desc = weather[dk]
    hotel = hotels[dk]
    date = day_dates[dk]
    title = day_titles[dk]
    
    day_text = day_texts.get(dk, "")
    
    # Split into subsections by ~ markers
    subsections = re.split(r'~ (.+?) ~', day_text)
    
    body_html = ""
    if len(subsections) > 1:
        # First part before any subsection
        intro = subsections[0].strip()
        if intro:
            body_html += text_to_html(intro, f"Day {day_num}")
        
        # Each subsection pair: title, content
        for j in range(1, len(subsections), 2):
            sub_title = subsections[j].strip()
            sub_content = subsections[j+1].strip() if j+1 < len(subsections) else ""
            sub_html = text_to_html(sub_content, f"Day {day_num} — {sub_title}")
            body_html += f'''
<div class="collapsible">
  <button class="collapsible-toggle">{escape(sub_title)} <span class="chevron">▼</span></button>
  <div class="collapsible-content" style="max-height:0px">
    <div class="collapsible-content-inner">
      {sub_html}
    </div>
  </div>
</div>'''
    else:
        body_html = text_to_html(day_text, f"Day {day_num}")
    
    is_cold = day_num >= 3
    weather_extra = ' style="border-color:var(--terracotta);color:var(--terracotta)"' if is_cold and day_num == 3 else ''
    
    return f'''
<div class="day-card" id="day{day_num}" data-nav-id="day{day_num}">
  <div class="day-card-header">
    <span class="day-badge">{dk}</span>
    <div class="day-info">
      <div class="day-date">{date}</div>
      <div class="day-title">{escape(title)}</div>
    </div>
    <span class="weather-badge"{weather_extra}>{w_icon} {w_temp} · {escape(w_desc)}</span>
  </div>
  <div class="hotel-badge">🏨 {escape(hotel)}</div>
  <div class="day-card-body">
    {body_html}
  </div>
</div>'''

day_cards_html = '\n'.join(build_day_card(d) for d in range(1, 9))

# Build main section HTML
def build_section(section_id, section_num, section_title, raw_key):
    text = sections_raw.get(raw_key, "")
    
    # Split by subsection headers (--- TITLE --- pattern or similar)
    # Find subsection markers
    subsection_pattern = r'--- (.+?) ---'
    parts = re.split(subsection_pattern, text)
    
    body_html = ""
    if len(parts) > 1:
        intro = parts[0].strip()
        if intro:
            body_html += text_to_html(intro, section_title)
        
        for j in range(1, len(parts), 2):
            sub_title = parts[j].strip()
            sub_content = parts[j+1].strip() if j+1 < len(parts) else ""
            
            # Further split by ~ subsub headers
            subsub_parts = re.split(r'~ (.+?) ~', sub_content)
            
            inner_html = ""
            if len(subsub_parts) > 1:
                intro2 = subsub_parts[0].strip()
                if intro2:
                    inner_html += text_to_html(intro2, f"{section_title} — {sub_title}")
                for k in range(1, len(subsub_parts), 2):
                    subsub_title = subsub_parts[k].strip()
                    subsub_content = subsub_parts[k+1].strip() if k+1 < len(subsub_parts) else ""
                    inner_html += f'<h4 class="sub-subsection-title">{escape(subsub_title)}</h4>\n'
                    inner_html += text_to_html(subsub_content, f"{section_title} — {subsub_title}")
            else:
                inner_html = text_to_html(sub_content, f"{section_title} — {sub_title}")
            
            body_html += f'''
<div class="subsection">
  <h3 class="subsection-title">{escape(sub_title)}</h3>
  {inner_html}
</div>'''
    else:
        # No subsection markers, try ~ markers directly
        subsub_parts = re.split(r'~ (.+?) ~', text)
        if len(subsub_parts) > 1:
            intro = subsub_parts[0].strip()
            if intro:
                body_html += text_to_html(intro, section_title)
            for j in range(1, len(subsub_parts), 2):
                sub_title = subsub_parts[j].strip()
                sub_content = subsub_parts[j+1].strip() if j+1 < len(subsub_parts) else ""
                sub_html = text_to_html(sub_content, f"{section_title} — {sub_title}")
                body_html += f'''
<div class="collapsible">
  <button class="collapsible-toggle">{escape(sub_title)} <span class="chevron">▼</span></button>
  <div class="collapsible-content" style="max-height:0px">
    <div class="collapsible-content-inner">
      {sub_html}
    </div>
  </div>
</div>'''
        else:
            body_html = text_to_html(text, section_title)
    
    return f'''
<section class="section" id="{section_id}" data-nav-id="{section_id}">
  <span class="section-number">Section {section_num}</span>
  <h2 class="section-header">{escape(section_title)}</h2>
  {body_html}
</section>'''

# Build conversation starters section specially
def build_conversation_section():
    text = sections_raw.get("CONVERSATION STARTERS", "")
    # Split by --- FOR ... --- groups
    groups = re.split(r'--- (FOR .+?) ---', text)
    
    html = ""
    intro = groups[0].strip()
    if intro:
        html += text_to_html(intro, "Conversation Starters")
    
    for j in range(1, len(groups), 2):
        group_title = groups[j].strip()
        group_content = groups[j+1].strip() if j+1 < len(groups) else ""
        
        # Extract question/answer pairs
        # Questions start with " and answers start with →
        lines = group_content.split('\n')
        cards_html = ""
        current_q = ""
        current_a_lines = []
        
        def flush_qa():
            nonlocal cards_html, current_q, current_a_lines
            if current_q:
                answer = ' '.join(l.strip() for l in current_a_lines if l.strip())
                answer = answer.lstrip('→ ').strip()
                answer = md_inline(escape(answer))
                q_text = md_inline(escape(current_q.strip('""\u201c\u201d')))
                cards_html += f'''<div class="convo-card">
  <button class="convo-question">{q_text}</button>
  <div class="convo-answer" style="max-height:0px">
    <div class="convo-answer-inner">{answer}</div>
  </div>
</div>
'''
            current_q = ""
            current_a_lines = []
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('"') or stripped.startswith('\u201c'):
                flush_qa()
                current_q = stripped
            elif stripped.startswith('→') or stripped.startswith('->'):
                current_a_lines.append(stripped)
            elif current_a_lines:
                current_a_lines.append(stripped)
        flush_qa()
        
        if cards_html:
            html += f'''
<div class="convo-group">
  <div class="convo-group-label">{escape(group_title)}</div>
  {cards_html}
</div>'''
    
    return f'''
<section class="section" id="conversation" data-nav-id="conversation">
  <span class="section-number">Section 11</span>
  <h2 class="section-header">Conversation Starters</h2>
  {html}
</section>'''

# Chinese phrases for quick reference
phrases = [
    ("你好", "Nǐ hǎo", "Hello"),
    ("谢谢", "Xièxiè", "Thank you"),
    ("这个多少钱？", "Zhège duōshao qián?", "How much?"),
    ("太贵了", "Tài guì le", "Too expensive"),
    ("不要太辣", "Bù yào tài là", "Not too spicy"),
    ("可以试喝吗？", "Kěyǐ shì hē ma?", "Can I taste it?"),
    ("我可以给您拍照吗？", "Wǒ kěyǐ gěi nín pāizhào ma?", "May I take your photo?"),
    ("这是什么？", "Zhè shì shénme?", "What is this?"),
    ("哪里有...？", "Nǎlǐ yǒu...?", "Where is...?"),
    ("很好吃！", "Hěn hǎo chī!", "Delicious!"),
    ("你们这里有什么特别的吗？", "Nǐmen zhèlǐ yǒu shénme tèbié de ma?", "Anything special here?"),
]

phrases_html = '\n'.join(
    f'<div class="phrase-item"><span class="phrase-cn">{cn} <span class="text-muted" style="font-weight:400;font-size:0.78rem">{py}</span></span><span class="phrase-en">{en}</span></div>'
    for cn, py, en in phrases
)

tea_tips = [
    ("Leaf quality", "Look for intact large leaves with visible veins, not powdery debris"),
    ("Compression", "Firm but not concrete-hard — should yield to a tea needle"),
    ("Smell test", "Clean & aromatic (young sheng) or complex/earthy (aged). Any mold = skip"),
    ("Always taste", "Any serious shop will brew for you — one steep tells the story"),
    ("Price reality", "Under ¥80 = plantation; ¥150-400 = decent; '30-year aged' under ¥800 = lying"),
    ("Storage question", "Ask: 乾倉還是濕倉？(Dry or wet storage?) — dry is better"),
    ("Buy small", "Get several small samples of different types rather than one big purchase"),
]

tea_html = '\n'.join(
    f'<div class="tea-tip"><strong>{escape(label)}:</strong> {escape(desc)}</div>'
    for label, desc in tea_tips
)

# ===== ASSEMBLE FULL HTML =====

section_htmls = [
    build_section("overview", "01", "Yunnan Overview — Why This Place Is Not Like the Rest of China", "YUNNAN OVERVIEW — WHY THIS PLACE IS NOT LIKE THE REST OF CHINA"),
    build_section("peoples", "02", "The Peoples", "THE PEOPLES"),
    build_section("tea-horse-road", "03", "The Tea Horse Road (茶馬古道)", "THE TEA HORSE ROAD (茶馬古道 — Chámǎ Gǔdào)"),
]

# Days section
days_section = f'''
<section class="section" id="days" data-nav-id="days">
  <span class="section-number">Section 04</span>
  <h2 class="section-header">Day-by-Day Deep Dives</h2>
  {day_cards_html}
</section>'''

section_htmls.append(days_section)

section_htmls += [
    build_section("jade-dragon", "05", "Jade Dragon Snow Mountain (玉龍雪山)", "JADE DRAGON SNOW MOUNTAIN (玉龍雪山)"),
    build_section("tiger-leaping", "06", "Tiger Leaping Gorge (虎跳峽)", "TIGER LEAPING GORGE (虎跳峽)"),
    build_section("nanzhao", "07", "Dali & The Kingdom of Nanzhao", "DALI & THE KINGDOM OF NANZHAO"),
    build_section("impressions", "08", "Zhang Yimou's Impressions Lijiang", "ZHANG YIMOU'S IMPRESSIONS LIJIANG"),
    build_section("puer", "09", "Pu'er Tea Primer", "PU'ER TEA PRIMER"),
    build_section("cultural-tips", "10", "Practical Cultural Tips", "PRACTICAL CULTURAL TIPS"),
    build_conversation_section(),
]

# Final note
final_note = sections_raw.get("FINAL NOTE", "")
final_note_html = text_to_html(final_note, "Final Note")

all_sections = '\n'.join(section_htmls)

html = f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Interactive deep-dive travel guide for Yunnan, China — Lijiang, Tiger Leaping Gorge, Dali, and the Tea Horse Road. March 8–15, 2026.">
  <meta name="theme-color" content="#c2583a">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <title>Yunnan Deep-Dive Guide — Mar 8–15, 2026</title>
  <link rel="stylesheet" href="style.css">
  <link rel="manifest" href="manifest.json">
</head>
<body>
  <!-- Progress bar -->
  <div class="progress-bar" id="progress-bar"></div>

  <!-- Navigation -->
  <nav class="nav">
    <div class="nav-inner">
      <a href="#" class="nav-brand">雲南 Yunnan Guide</a>
      <div class="nav-controls">
        <button class="nav-btn" id="search-btn" aria-label="Search">🔍</button>
        <button class="nav-btn" id="theme-btn" aria-label="Toggle dark mode">🌙</button>
        <button class="nav-btn" id="menu-btn" aria-label="Menu">☰</button>
      </div>
    </div>
  </nav>

  <!-- Day strip -->
  <div class="day-strip" id="day-strip">
    {day_pills}
  </div>

  <!-- Mobile menu overlay -->
  <div class="menu-overlay" id="menu-overlay">
    {menu_html}
  </div>

  <!-- Search overlay -->
  <div class="search-overlay" id="search-overlay">
    <div class="search-box">
      <div class="search-input-wrap">
        <span class="icon">🔍</span>
        <input type="text" class="search-input" id="search-input" placeholder="Search the guide... (⌘K)">
      </div>
      <div class="search-results" id="search-results"></div>
    </div>
  </div>

  <!-- Desktop TOC sidebar -->
  <nav class="toc-sidebar">
    {toc_html}
  </nav>

  <!-- Hero -->
  <header class="hero">
    <div class="hero-subtitle">Deep-Dive Travel Guide</div>
    <h1>Essential <span>Yunnan</span></h1>
    <div class="hero-divider"></div>
    <p class="hero-meta">
      Lijiang · Tiger Leaping Gorge · Shaxi · Dali<br>
      March 8–15, 2026 · 8 Days
    </p>
  </header>

  <!-- Main content -->
  <main class="content">
    {all_sections}

    <!-- Footer / Final Note -->
    <footer class="footer">
      <p>{final_note_html}</p>
      <br>
      <p><strong>Prepared March 2026</strong> · Harry Clawford for Karl<br>
      Sources: field research, academic ethnography (Rock, McKhann, Mathieu), historical records, UNESCO documentation.<br>
      ~13,000 words · 45–60 min read</p>
    </footer>
  </main>

  <!-- Quick Reference FAB -->
  <button class="qr-fab" id="qr-fab" aria-label="Quick Reference">中</button>

  <!-- Quick Reference Bottom Sheet -->
  <div class="qr-sheet" id="qr-sheet">
    <div class="qr-sheet-header">
      <span class="qr-sheet-title">Quick Reference</span>
      <button class="qr-close" id="qr-close" aria-label="Close">✕</button>
    </div>
    <div class="qr-tabs">
      <button class="qr-tab active" data-panel="qr-phrases">Phrases</button>
      <button class="qr-tab" data-panel="qr-tea">Pu'er Buying</button>
    </div>
    <div class="qr-panel active" id="qr-phrases">
      {phrases_html}
    </div>
    <div class="qr-panel" id="qr-tea">
      {tea_html}
    </div>
  </div>

  <script src="script.js"></script>
</body>
</html>'''

# Write
with open('index.html', 'w') as f:
    f.write(html)

# Also create manifest.json for PWA
import json
manifest = {
    "name": "Yunnan Deep-Dive Guide",
    "short_name": "Yunnan Guide",
    "start_url": "/yunnan-guide/",
    "display": "standalone",
    "background_color": "#faf6f0",
    "theme_color": "#c2583a",
    "description": "Interactive travel guide for Yunnan, China — March 2026"
}
with open('manifest.json', 'w') as f:
    json.dump(manifest, f, indent=2)

print(f"✅ Built index.html ({len(html):,} bytes)")
print(f"✅ Built manifest.json")
