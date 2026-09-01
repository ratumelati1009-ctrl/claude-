import { readFileSync, writeFileSync } from 'node:fs';
import pw from '/opt/toolchains/.nvm/versions/node/v22.23.2/lib/node_modules/@playwright/mcp/node_modules/playwright-core/index.js';
const { chromium } = pw;

const SRC = '/projects/sandbox/ebook/The-Busy-Parents-Natural-Reset.md';
const OUT_HTML = '/projects/sandbox/ebook/The-Busy-Parents-Natural-Reset.html';
const OUT_PDF = '/projects/sandbox/ebook/The-Busy-Parents-Natural-Reset.pdf';
const CHROME = '/opt/playwright/chromium-1232/chrome-linux64/chrome';

const md = readFileSync(SRC, 'utf8');

// ---------- tiny, purpose-built Markdown -> HTML ----------
function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
function inline(s) {
  s = esc(s);
  // bold
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  // italics (single * not adjacent to another *)
  s = s.replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g, '$1<em>$2</em>');
  // inline code / backtick
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  return s;
}

const lines = md.split('\n');
let html = '';
let i = 0;

function flushParagraph(buf) {
  if (buf.trim()) html += `<p>${inline(buf.trim())}</p>\n`;
}

while (i < lines.length) {
  let line = lines[i];

  // horizontal rule
  if (/^---\s*$/.test(line)) {
    html += '<hr/>\n';
    i++;
    continue;
  }

  // headings
  const h = line.match(/^(#{1,6})\s+(.*)$/);
  if (h) {
    const level = h[1].length;
    const cls = level === 1 ? ' class="chapter"' : '';
    html += `<h${level}${cls}>${inline(h[2])}</h${level}>\n`;
    i++;
    continue;
  }

  // blockquote
  if (/^>\s?/.test(line)) {
    let quote = [];
    while (i < lines.length && /^>\s?/.test(lines[i])) {
      quote.push(lines[i].replace(/^>\s?/, ''));
      i++;
    }
    html += `<blockquote>${inline(quote.join(' '))}</blockquote>\n`;
    continue;
  }

  // table (line with | followed by a separator row)
  if (line.includes('|') && i + 1 < lines.length && /^\s*\|?[\s:|-]+\|[\s:|-]+/.test(lines[i + 1]) && lines[i+1].includes('-')) {
    const header = line;
    i += 2; // skip header + separator
    const parseRow = (r) => r.replace(/^\s*\|/, '').replace(/\|\s*$/, '').split('|').map(c => c.trim());
    const headers = parseRow(header);
    let rows = [];
    while (i < lines.length && lines[i].includes('|')) {
      rows.push(parseRow(lines[i]));
      i++;
    }
    html += '<table>\n<thead><tr>' + headers.map(c => `<th>${inline(c)}</th>`).join('') + '</tr></thead>\n<tbody>\n';
    for (const r of rows) {
      html += '<tr>' + r.map(c => `<td>${inline(c)}</td>`).join('') + '</tr>\n';
    }
    html += '</tbody></table>\n';
    continue;
  }

  // unordered / checkbox list
  if (/^\s*-\s+/.test(line)) {
    html += '<ul>\n';
    while (i < lines.length && /^\s*-\s+/.test(lines[i])) {
      let item = lines[i].replace(/^\s*-\s+/, '');
      const cb = item.match(/^\[( |x|X)\]\s+(.*)$/);
      if (cb) {
        const checked = cb[1].toLowerCase() === 'x';
        html += `<li class="task"><span class="box">${checked ? '☑' : '☐'}</span> ${inline(cb[2])}</li>\n`;
      } else {
        html += `<li>${inline(item)}</li>\n`;
      }
      i++;
    }
    html += '</ul>\n';
    continue;
  }

  // ordered list
  if (/^\s*\d+\.\s+/.test(line)) {
    html += '<ol>\n';
    while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) {
      html += `<li>${inline(lines[i].replace(/^\s*\d+\.\s+/, ''))}</li>\n`;
      i++;
    }
    html += '</ol>\n';
    continue;
  }

  // blank line
  if (line.trim() === '') {
    i++;
    continue;
  }

  // paragraph (gather until blank / block element)
  let para = [];
  while (
    i < lines.length &&
    lines[i].trim() !== '' &&
    !/^(#{1,6})\s/.test(lines[i]) &&
    !/^>\s?/.test(lines[i]) &&
    !/^\s*-\s+/.test(lines[i]) &&
    !/^\s*\d+\.\s+/.test(lines[i]) &&
    !/^---\s*$/.test(lines[i]) &&
    !(lines[i].includes('|') && i + 1 < lines.length && lines[i+1].includes('-') && /^\s*\|?[\s:|-]+\|/.test(lines[i+1]))
  ) {
    para.push(lines[i]);
    i++;
  }
  flushParagraph(para.join(' '));
}

const css = `
  @page { size: A4; margin: 22mm 20mm 20mm 20mm; }
  * { box-sizing: border-box; }
  body {
    font-family: "Georgia", "Times New Roman", serif;
    color: #1f2933;
    line-height: 1.55;
    font-size: 11.5pt;
  }
  h1, h2, h3, h4 { font-family: "Helvetica Neue", Arial, sans-serif; color: #14532d; line-height: 1.25; }
  h1.chapter { font-size: 22pt; margin: 0 0 14px; padding-bottom: 8px; border-bottom: 3px solid #22c55e; page-break-before: always; }
  /* first h1 (title) shouldn't force a page break */
  h1.chapter:first-of-type { page-break-before: avoid; }
  h2 { font-size: 15pt; margin: 22px 0 8px; }
  h3 { font-size: 12.5pt; margin: 16px 0 6px; color: #166534; }
  h4 { font-size: 11pt; margin: 12px 0 4px; color: #166534; }
  p { margin: 0 0 9px; }
  strong { color: #14532d; }
  hr { border: none; border-top: 1px solid #d1d5db; margin: 16px 0; }
  blockquote {
    margin: 14px 0; padding: 10px 16px; background: #f0fdf4;
    border-left: 4px solid #22c55e; font-style: italic; color: #374151;
    border-radius: 3px;
  }
  ul, ol { margin: 6px 0 12px; padding-left: 22px; }
  li { margin: 3px 0; }
  li.task { list-style: none; margin-left: -18px; }
  li.task .box { font-size: 12pt; margin-right: 6px; }
  code { font-family: "Courier New", monospace; background: #f3f4f6; padding: 1px 4px; border-radius: 3px; font-size: 10pt; }
  table { border-collapse: collapse; width: 100%; margin: 10px 0 16px; font-family: "Helvetica Neue", Arial, sans-serif; font-size: 10pt; page-break-inside: avoid; }
  th { background: #14532d; color: #fff; text-align: left; padding: 7px 9px; }
  td { border: 1px solid #d1d5db; padding: 6px 9px; vertical-align: top; }
  tbody tr:nth-child(even) td, tr:nth-child(even) td { background: #f9fafb; }
  h2, h3, h4 { page-break-after: avoid; }
`;

// Build a clean title block: treat the very top of the doc specially so the cover looks like a cover.
const fullHtml = `<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>The Busy Parent's Natural Reset</title>
<style>${css}</style></head>
<body>
${html}
</body></html>`;

writeFileSync(OUT_HTML, fullHtml, 'utf8');

// ---------- render to PDF ----------
const browser = await chromium.launch({
  executablePath: CHROME,
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
});
const page = await browser.newPage();
await page.setContent(fullHtml, { waitUntil: 'load' });
await page.pdf({
  path: OUT_PDF,
  format: 'A4',
  printBackground: true,
  displayHeaderFooter: true,
  headerTemplate: '<div></div>',
  footerTemplate: '<div style="width:100%; font-size:8px; color:#9ca3af; font-family:Arial; text-align:center;">The Busy Parent\\u2019s Natural Reset &nbsp;\\u2022&nbsp; Daniel Tesfamariam &nbsp;\\u2022&nbsp; Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>',
  margin: { top: '22mm', bottom: '18mm', left: '20mm', right: '20mm' },
});
await browser.close();
console.log('PDF written to ' + OUT_PDF);
