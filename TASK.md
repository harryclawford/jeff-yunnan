# Yunnan Travel Guide — Full Audit + Rebuild

## Context
This is a travel guide site for a Yunnan trip (Mar 8-15, 2026). It's deployed on GitHub Pages at:
https://harryclawford.github.io/jeff-yunnan/

The site has accumulated bugs from multiple rounds of manual edits. It needs a proper audit and restructure.

## Required Changes

### 1. Bottom Tab Navigation (4 tabs)
Replace the current navigation with a **fixed bottom tab bar** (mobile-first, like an app):
- **🗺️ Map** — The interactive Leaflet map with all markers
- **📅 Itinerary** — Day-by-day cards (D1-D8) with weather badges, hotel info, photos, collapsible deep-dives
- **ℹ️ Info** — All the deep-dive topic sections (Peoples, Tea Horse Road, Jade Dragon, Tiger Leaping, Nanzhao, Impressions, Pu'er, Cultural Tips, Conversation Starters)
- Keep the day pill strip (D1-D8) visible within the Itinerary tab

### 2. Full HTML Audit
- Fix ALL HTML nesting errors (unclosed divs, mismatched tags)
- Validate the entire document structure
- Remove any orphaned/duplicate elements
- Ensure all images load (they're in `images/` folder locally)

### 3. Best Practices for Sharing
- Add proper Open Graph meta tags (og:title, og:description, og:image) so it previews well when shared
- Add a nice hero/header when the page first loads
- Smooth tab transitions
- Make sure the service worker caches everything for offline use (update sw.js if needed)
- Touch-friendly: all tap targets ≥44px
- Fast: lazy load images below the fold
- Accessible: proper aria labels on interactive elements

### 4. Visual Polish
- Clean, modern travel app feel
- The existing color palette is good (terracotta, jade green, cream)
- Make the tab bar visually clear with active state indicators
- Smooth scroll when navigating between days
- The map should fill most of the viewport when on the Map tab
- Photos should look good on mobile (proper aspect ratios, no stretching)

### 5. Don't Break
- Keep ALL existing content (day cards, topic sections, map markers, photos)
- Keep the Leaflet map with all 14 markers
- Keep the collapsible deep-dive sections within day cards
- Keep dark mode toggle
- Keep search functionality
- Keep offline support (service worker)

## Technical Constraints
- Single index.html + style.css + script.js (no build tools, no frameworks)
- Google Fonts CDN only external dependency (besides Leaflet)
- All images served locally from `images/`
- Must work on iPhone Safari (primary device)

## When Done
1. Commit and push: `git add -A && git commit -m "feat: tab navigation, full audit, sharing optimization" && git push origin main`
2. Run: `openclaw system event --text "Done: Yunnan guide rebuilt with tab navigation, full audit complete" --mode now`
