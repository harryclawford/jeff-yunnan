# Build Brief: Yunnan Travel Guide Interactive Site

## What to Build
Turn `guide-content.txt` into a beautiful, interactive single-page static site (HTML/CSS/JS only — no build tools, no frameworks, no npm). This will be deployed on GitHub Pages and read primarily on mobile (iPhone) during a trip to Yunnan, China.

## Design Direction
- **Aesthetic:** Clean, elegant, travel-journal feel. Think: Monocle magazine meets a premium travel app
- **Color palette:** Warm earth tones inspired by Yunnan — terracotta, jade green, deep indigo (Bai tie-dye blue), off-white, charcoal text
- **Typography:** Use Google Fonts — a serif for headings (like Playfair Display or DM Serif Display), clean sans for body (like Inter or Source Sans Pro)
- **Mobile-first:** This will be read on an iPhone during travel. Everything must work beautifully at 375-430px width

## Key Interactive Features

### 1. Navigation
- Sticky top nav with the 8 days (D1-D8) + topic sections (Peoples, Tea Horse Road, etc.)
- Smooth scroll to sections
- Active section indicator as user scrolls
- Collapsible hamburger menu on mobile

### 2. Day-by-Day Cards
- Each day gets a visually distinct card/section
- Weather badge per day (hardcode these values):
  - D1 Mar 8: ☀️ 5-23°C, Clear
  - D2 Mar 9: ⛅ 7-22°C, Partly cloudy
  - D3 Mar 10: 🌧️ 6-13°C, Drizzle — COLD FRONT
  - D4 Mar 11: 🌧️ 7-14°C, Light rain
  - D5 Mar 12: 🌧️ 8-17°C, Light drizzle
  - D6 Mar 13: 🌧️ 7-10°C, Drizzle (coldest)
  - D7 Mar 14: 🌧️ 8-12°C, Light drizzle
  - D8 Mar 15: 🌧️ 9-13°C, Drizzle
- Hotel name displayed per day
- Collapsible subsections within each day (click to expand deep-dive content)

### 3. "Holy Shit Facts" Callouts
- Special styled callout boxes for the most interesting facts (the guide marks these)
- Visually distinct — maybe a different background color with an icon

### 4. Conversation Starters
- Interactive accordion or card-flip for the conversation starters section
- Group by audience (Naxi, Bai, Tea Shop, Universal)

### 5. Quick Reference
- Floating/accessible Chinese phrases section (maybe a bottom sheet or floating button that opens a phrase card)
- Pu'er tea buying cheat sheet as a compact reference card

### 6. Progress Tracker
- Optional: a subtle day progress indicator showing which day of the trip

### 7. Table of Contents
- Floating TOC sidebar on desktop, collapsible on mobile
- Shows all 11 major sections + day-by-day

### 8. Search/Find
- Simple text search within the guide (ctrl+F alternative that works on mobile)

## Content Structure
Parse the guide-content.txt and structure it into these sections:
1. Yunnan Overview
2. The Peoples (Naxi, Bai, Others)
3. The Tea Horse Road
4. Day-by-Day (D1 through D8) — each with weather, hotel, activities, deep dives
5. Jade Dragon Snow Mountain
6. Tiger Leaping Gorge
7. Dali & Kingdom of Nanzhao
8. Zhang Yimou's Impressions Lijiang
9. Pu'er Tea Primer
10. Practical Cultural Tips
11. Conversation Starters
+ Quick Reference (Chinese phrases)

## Technical Requirements
- **SINGLE index.html file** with inline CSS and JS (or at most index.html + style.css + script.js)
- **No build tools, no npm, no frameworks** — pure HTML/CSS/JS
- **Google Fonts via CDN** — that's the only external dependency allowed (besides optional images)
- **Smooth animations** — CSS transitions for expand/collapse, scroll behavior
- **Dark mode toggle** — for reading at night
- **Offline-capable** — add a simple service worker so the site works without internet (Karl will be in rural Yunnan)
- **Print-friendly** — @media print styles so Karl can print sections if needed
- **Fast** — no heavy assets, everything inline or CDN

## Deploy
After building, commit everything and push to main. The repo already has GitHub Pages — it should deploy from the main branch root.

Enable GitHub Pages:
```
gh api repos/harryclawford/yunnan-guide/pages -X POST -f "build_type=workflow" -f "source[branch]=main" -f "source[path]=/" 2>/dev/null || true
```

## DO NOT
- Use React, Vue, Svelte, or any framework
- Use npm, webpack, vite, or any build tool
- Create multiple HTML pages (single page only)
- Use placeholder content — use the ACTUAL guide text from guide-content.txt
- Skip any section of the guide
- Use AI-generated stock images — text-only is fine, emojis for visual flavor

## Final URL
https://harryclawford.github.io/yunnan-guide/

When completely finished, run this command to notify me:
openclaw system event --text "Done: Yunnan guide interactive site built and deployed to GitHub Pages" --mode now
