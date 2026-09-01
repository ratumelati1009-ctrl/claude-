import { writeFileSync } from 'node:fs';
import pw from '/opt/toolchains/.nvm/versions/node/v22.23.2/lib/node_modules/@playwright/mcp/node_modules/playwright-core/index.js';
const { chromium } = pw;

const OUT_HTML = '/projects/sandbox/tracing/Tracing-Numbers-Tigrinya.html';
const OUT_PDF  = '/projects/sandbox/tracing/Tracing-Numbers-Tigrinya.pdf';
const CHROME   = '/opt/playwright/chromium-1232/chrome-linux64/chrome';

// Western digit -> Ge'ez numeral
const GEEZ = { 1:'፩', 2:'፪', 3:'፫', 4:'፬', 5:'፭', 6:'፮', 7:'፯', 8:'፰', 9:'፱' };
// Tigrinya number words (for a small caption)
const WORD = { 1:'ሓደ', 2:'ክልተ', 3:'ሰለስተ', 4:'ኣርባዕተ', 5:'ሓሙሽተ', 6:'ሽዱሽተ', 7:'ሸውዓተ', 8:'ሸሞንተ', 9:'ትሽዓተ' };

// Per-page theme colors (matching the source worksheet vibe)
const THEME = {
  1:'#F0996B', 2:'#F2D45C', 3:'#F3B89A', 4:'#F6A9CE', 5:'#4FC4BD',
  6:'#7CC6E8', 7:'#6FC898', 8:'#EE6E6E', 9:'#A7D8DA'
};

// A cute cat face SVG, colorable
function cat(color, size = 54) {
  return `
  <svg width="${size}" height="${size}" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <path d="M22 20 L36 40 L18 42 Z" fill="${color}"/>
    <path d="M78 20 L64 40 L82 42 Z" fill="${color}"/>
    <ellipse cx="50" cy="58" rx="38" ry="33" fill="${color}"/>
    <circle cx="38" cy="54" r="6" fill="#2b2b2b"/>
    <circle cx="62" cy="54" r="6" fill="#2b2b2b"/>
    <circle cx="40" cy="52" r="2" fill="#fff"/>
    <circle cx="64" cy="52" r="2" fill="#fff"/>
    <path d="M46 66 Q50 70 54 66" stroke="#2b2b2b" stroke-width="2.4" fill="none" stroke-linecap="round"/>
    <path d="M50 62 L47 66 M50 62 L53 66" stroke="#2b2b2b" stroke-width="2" fill="none" stroke-linecap="round"/>
    <ellipse cx="30" cy="63" rx="6" ry="3.5" fill="#ff9db0" opacity="0.75"/>
    <ellipse cx="70" cy="63" rx="6" ry="3.5" fill="#ff9db0" opacity="0.75"/>
    <g stroke="#2b2b2b" stroke-width="1.6" stroke-linecap="round">
      <line x1="14" y1="60" x2="30" y2="61"/><line x1="14" y1="66" x2="30" y2="65"/>
      <line x1="86" y1="60" x2="70" y2="61"/><line x1="86" y1="66" x2="70" y2="65"/>
    </g>
  </svg>`;
}

// Build one page
function page(n) {
  const color = THEME[n];
  const geez = GEEZ[n];
  const cats = Array.from({ length: n }, () => `<span class="cat">${cat(color)}</span>`).join('');
  // 4 columns x 5 rows = 20 trace cells
  const cells = Array.from({ length: 20 }, () =>
    `<div class="cell"><span class="trace">${geez}</span></div>`
  ).join('');

  return `
  <section class="page">
    <header class="head">
      <div class="titles">
        <h1 class="t1" style="color:${color}">ምስሊ ቁጽሪ</h1>
        <h2 class="t2" style="color:${color}">ትግርኛ</h2>
        <p class="sub">ኣስዕብ ቁጽሪ ${geez} (${n}) ከምኡ'ውን ደሙ ኣኽራው</p>
        <p class="word">${geez} — ${WORD[n]} (${n})</p>
      </div>
      <div class="catrow">${cats}</div>
    </header>
    <div class="grid">${cells}</div>
    <footer class="foot">ብ ዳንኤል ተስፋማርያም • KIDPID-ኣገባብ • ገጽ ${n} / 9</footer>
  </section>`;
}

const pages = Object.keys(GEEZ).map(k => page(Number(k))).join('\n');

const css = `
  @page { size: A4; margin: 12mm; }
  * { box-sizing: border-box; }
  body { margin:0; font-family:"Noto Sans Ethiopic","Noto Sans",sans-serif; color:#3a3a3a; }
  .page { page-break-after: always; height: 273mm; display:flex; flex-direction:column; }
  .page:last-child { page-break-after: auto; }
  .head { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px; }
  .titles { max-width: 66%; }
  .t1 { font-size: 40pt; margin:0; line-height:1; font-weight:700; letter-spacing:1px; }
  .t2 { font-size: 20pt; margin:2px 0 6px; font-weight:700; -webkit-text-stroke:1px currentColor; color:transparent !important; }
  .sub { font-size: 11pt; font-weight:700; margin:0 0 2px; text-transform:none; }
  .word { font-size: 12pt; margin:0; color:#666; }
  .catrow { display:flex; flex-wrap:wrap; gap:4px; max-width:34%; justify-content:flex-end; }
  .cat { display:inline-flex; }
  .grid { flex:1; display:grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(5, 1fr);
          gap:6px; border:2px solid #777; padding:6px; border-radius:4px; }
  .cell { border:1.5px solid #9a9a9a; border-radius:3px; display:flex; align-items:center; justify-content:center; }
  /* Dotted, traceable numeral: outline via text-stroke + dashed look through low-opacity dotted fill */
  .trace {
    font-size: 46pt; font-weight:700; line-height:1;
    color: #d0d0d0;
    -webkit-text-stroke: 1.4px #9a9a9a;
  }
`;

const html = `<!DOCTYPE html><html lang="ti"><head><meta charset="utf-8">
<title>ምስሊ ቁጽሪ — ትግርኛ</title><style>${css}</style></head><body>${pages}</body></html>`;

writeFileSync(OUT_HTML, html, 'utf8');

const browser = await chromium.launch({
  executablePath: CHROME, headless: true,
  args: ['--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage'],
});
const p = await browser.newPage();
await p.setContent(html, { waitUntil:'load' });
await p.pdf({ path: OUT_PDF, format:'A4', printBackground:true, margin:{top:'12mm',bottom:'12mm',left:'12mm',right:'12mm'} });
await browser.close();
console.log('Tracing PDF written to ' + OUT_PDF);
