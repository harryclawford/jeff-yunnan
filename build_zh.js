#!/usr/bin/env node
/**
 * Converts Chinese translation chunk text files into a JS translation module.
 * Reads chunk1_zh.txt through chunk4_zh.txt, parses their structure,
 * and outputs translations_zh.js with HTML content per section.
 */
'use strict';

var fs = require('fs');
var path = require('path');

var chunksDir = path.join(__dirname, 'chunks');

function readChunk(filename) {
  return fs.readFileSync(path.join(chunksDir, filename), 'utf8');
}

/**
 * Convert plain text (with --- headers, ~ subheaders, - list items)
 * into simple HTML paragraphs and lists.
 */
function textToHtml(text) {
  var lines = text.split('\n');
  var html = [];
  var inList = false;

  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    var trimmed = line.trim();

    // Skip empty lines (close list if open)
    if (!trimmed) {
      if (inList) { html.push('</ul>'); inList = false; }
      continue;
    }

    // Skip separator lines
    if (/^={5,}$/.test(trimmed)) continue;

    // Skip section number lines like "1. 雲南概覽..."
    if (/^\d+\.\s/.test(trimmed) && trimmed.length < 80 && i > 0 && /^={5,}$/.test(lines[i-1] ? lines[i-1].trim() : '')) continue;

    // Subsection header: --- text ---
    var subMatch = trimmed.match(/^---\s*(.+?)\s*---$/);
    if (subMatch) {
      if (inList) { html.push('</ul>'); inList = false; }
      html.push('<h3 class="subsection-title">' + escHtml(subMatch[1]) + '</h3>');
      continue;
    }

    // Sub-subsection header: ~ text ~
    var subsubMatch = trimmed.match(/^~\s*(.+?)\s*~$/);
    if (subsubMatch) {
      if (inList) { html.push('</ul>'); inList = false; }
      html.push('<h4 class="zh-subheader">' + escHtml(subsubMatch[1]) + '</h4>');
      continue;
    }

    // List item: - text
    if (/^[-•]\s/.test(trimmed)) {
      if (!inList) { html.push('<ul>'); inList = true; }
      html.push('<li>' + escHtml(trimmed.replace(/^[-•]\s*/, '')) + '</li>');
      continue;
    }

    // Regular paragraph
    if (inList) { html.push('</ul>'); inList = false; }
    html.push('<p>' + escHtml(trimmed) + '</p>');
  }

  if (inList) html.push('</ul>');
  return html.join('\n');
}

function escHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

/**
 * Split a chunk file into sections by ===== separator lines.
 * Returns array of { title, body } objects.
 */
function splitSections(text) {
  var sections = [];
  var lines = text.split('\n');
  var current = null;
  var bodyLines = [];

  for (var i = 0; i < lines.length; i++) {
    var trimmed = lines[i].trim();

    // Check if this line is a section title (number. title)
    var titleMatch = trimmed.match(/^\d+\.\s*(.+)$/);
    if (titleMatch) {
      // Verify it's a real section title by checking surrounding === lines
      var prevIsSep = (i > 0 && /^={5,}$/.test((lines[i-1] || '').trim()));
      var nextIsSep = (i + 1 < lines.length && /^={5,}$/.test((lines[i+1] || '').trim()));
      if (prevIsSep || nextIsSep) {
        // Save previous section
        if (current !== null) {
          sections.push({ title: current, body: bodyLines.join('\n') });
        }
        current = titleMatch[1];
        bodyLines = [];
        continue;
      }
    }

    // Skip separator lines
    if (/^={5,}$/.test(trimmed)) continue;

    if (current !== null) {
      bodyLines.push(lines[i]);
    }
  }

  if (current !== null) {
    sections.push({ title: current, body: bodyLines.join('\n') });
  }

  return sections;
}

// Map Chinese section titles to HTML section IDs
var sectionIdMap = {
  // chunk1
  '雲南概覽——為什麼這個地方與中國其他地方截然不同': 'overview',
  '雲南的子民——行程中你會遇到的民族': 'peoples',
  '茶馬古道——亞洲最偉大的貿易路線': 'tea-horse-road',
  // chunk2 (days - handled separately)
  '逐日深度攻略': 'days',
  // chunk3
  '玉龍雪山（玉龍雪山）': 'jade-dragon',
  '虎跳峽（虎跳峽）': 'tiger-leaping',
  '大理與南詔王國（大理·南詔）': 'nanzhao',
  // chunk4
  '張藝謀的《印象·麗江》': 'impressions',
  '普洱茶入門': 'puer',
  '實用文化貼士': 'cultural-tips',
  '開啟對話的好問題': 'conversation',
};

// Process each chunk
var translations = {};

// chunk1: sections 1-3
var chunk1 = readChunk('chunk1_zh.txt');
var sections1 = splitSections(chunk1);
sections1.forEach(function(s) {
  var id = null;
  Object.keys(sectionIdMap).forEach(function(key) {
    if (s.title.indexOf(key.substring(0, 10)) !== -1 || key.indexOf(s.title.substring(0, 10)) !== -1) {
      id = sectionIdMap[key];
    }
  });
  // More precise matching
  if (s.title.indexOf('雲南概覽') !== -1) id = 'overview';
  else if (s.title.indexOf('子民') !== -1 || s.title.indexOf('民族') !== -1) id = 'peoples';
  else if (s.title.indexOf('茶馬古道') !== -1) id = 'tea-horse-road';

  if (id) {
    translations[id] = textToHtml(s.body);
  }
});

// chunk3: sections 5-7
var chunk3 = readChunk('chunk3_zh.txt');
var sections3 = splitSections(chunk3);
sections3.forEach(function(s) {
  var id = null;
  if (s.title.indexOf('玉龍雪山') !== -1) id = 'jade-dragon';
  else if (s.title.indexOf('虎跳峽') !== -1) id = 'tiger-leaping';
  else if (s.title.indexOf('大理') !== -1 || s.title.indexOf('南詔') !== -1) id = 'nanzhao';

  if (id) {
    translations[id] = textToHtml(s.body);
  }
});

// chunk4: sections 8-11
var chunk4 = readChunk('chunk4_zh.txt');
var sections4 = splitSections(chunk4);
sections4.forEach(function(s) {
  var id = null;
  if (s.title.indexOf('印象') !== -1 || s.title.indexOf('張藝謀') !== -1) id = 'impressions';
  else if (s.title.indexOf('普洱茶') !== -1) id = 'puer';
  else if (s.title.indexOf('實用') !== -1 || s.title.indexOf('文化貼士') !== -1) id = 'cultural-tips';
  else if (s.title.indexOf('對話') !== -1 || s.title.indexOf('好問題') !== -1 || s.title.indexOf('話匣子') !== -1) id = 'conversation';

  if (id) {
    translations[id] = textToHtml(s.body);
  }
});

// chunk2: day-by-day (split by --- D\d+ lines)
var chunk2 = readChunk('chunk2_zh.txt');
var dayRegex = /---\s*D(\d+)[：:]\s*/g;
var dayTexts = chunk2.split(/---\s*D\d+[：:][^-]*---/);
var dayMatches = [];
var m;
while ((m = dayRegex.exec(chunk2)) !== null) {
  dayMatches.push('day' + m[1]);
}

// dayTexts[0] is before first day marker, skip it
for (var i = 0; i < dayMatches.length; i++) {
  var dayBody = dayTexts[i + 1] || '';
  translations[dayMatches[i]] = textToHtml(dayBody);
}

// Also add some UI translations
translations['_ui'] = {
  heroSubtitle: '深度旅行指南',
  heroTitle: '雲南精華',
  heroMeta: '麗江 · 虎跳峽 · 沙溪 · 大理<br>2026年3月8日–15日 · 8天',
  tabMap: '地圖',
  tabItinerary: '行程',
  tabInfo: '資訊',
  expandAll: '全部展開',
  collapseAll: '全部收合',
  infoHint: '📖 點按任意章節標題以展開 · 使用 🔍 搜尋所有內容',
  searchPlaceholder: '搜尋指南內容…',
  footerPrepared: '2026年3月編纂',
  footerBy: 'Harry Clawford 為 Karl 撰寫',
  footerSources: '資料來源：實地考察、學術民族誌（Rock、McKhann、Mathieu）、歷史文獻、UNESCO文件。',
  footerWordcount: '約13,000字 · 閱讀時長45–60分鐘',
};

// Write output
var output = '/* Auto-generated Chinese translations — do not edit by hand */\n';
output += 'var TRANSLATIONS_ZH = ' + JSON.stringify(translations, null, 2) + ';\n';

fs.writeFileSync(path.join(__dirname, 'translations_zh.js'), output, 'utf8');
console.log('Generated translations_zh.js with ' + Object.keys(translations).length + ' sections');
Object.keys(translations).forEach(function(k) {
  if (k === '_ui') {
    console.log('  _ui: ' + Object.keys(translations[k]).length + ' UI strings');
  } else {
    console.log('  ' + k + ': ' + (translations[k].length) + ' chars');
  }
});
