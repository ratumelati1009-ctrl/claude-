import { writeFileSync } from 'node:fs';
import pw from '/opt/toolchains/.nvm/versions/node/v22.23.2/lib/node_modules/@playwright/mcp/node_modules/playwright-core/index.js';
const { chromium } = pw;

const OUT_HTML = '/projects/sandbox/tracing/Tracing-Fidel-Tigrinya.html';
const OUT_PDF  = '/projects/sandbox/tracing/Tracing-Fidel-Tigrinya.pdf';
const CHROME   = '/opt/playwright/chromium-1232/chrome-linux64/chrome';

// The 26 base consonants of the Ge'ez fidel, in their traditional teaching order,
// shown in the FIRST FORM (ግእዝ / geʼez order). Each entry: letter, romanization, Tigrinya name.
const FIDEL = [
  { c:'ሀ', r:'hä',  name:'ሆይ' },
  { c:'ለ', r:'lä',  name:'ላዊ' },
  { c:'ሐ', r:'ḥä',  name:'ሓውት' },
  { c:'መ', r:'mä',  name:'ማይ' },
  { c:'ሠ', r:'śä',  name:'ሠውት' },
  { c:'ረ', r:'rä',  name:'ርእስ' },
  { c:'ሰ', r:'sä',  name:'ሳት' },
  { c:'ቀ', r:'qä',  name:'ቃፍ' },
  { c:'በ', r:'bä',  name:'ቤት' },
  { c:'ተ', r:'tä',  name:'ታው' },
  { c:'ኀ', r:'ḫä',  name:'ኀርም' },
  { c:'ነ', r:'nä',  name:'ናሓስ' },
  { c:'አ', r:'ʾä',  name:'አልፍ' },
  { c:'ከ', r:'kä',  name:'ካፍ' },
  { c:'ወ', r:'wä',  name:'ዋዌ' },
  { c:'ዐ', r:'ʿä',  name:'ዐይን' },
  { c:'ዘ', r:'zä',  name:'ዘይ' },
  { c:'የ', r:'yä',  name:'የመን' },
  { c:'ደ', r:'dä',  name:'ድንት' },
  { c:'ገ', r:'gä',  name:'ገምል' },
  { c:'ጠ', r:'ṭä',  name:'ጠይት' },
  { c:'ጰ', r:'ṗä',  name:'ጰይት' },
  { c:'ጸ', r:'ṣä',  name:'ጸደይ' },
  { c:'ፀ', r:'ṣ́ä', name:'ፀጳ' },
  { c:'ፈ', r:'fä',  name:'ኣፍ' },
  { c:'ፐ', r:'pä',  name:'ፕሳ' },
];

// A rotating palette so each page feels friendly (kid-worksheet style).
const PALETTE = ['#F0996B','#F2D45C','#F3B89A','#F6A9CE','#4FC4BD','#7CC6E8','#6FC898','#EE6E6E','#A7D8DA','#C9A0DC'];

// A small star SVG used as the "count & color" motif for each page.
function star(color, size = 46) {
  return `
  <svg width="${size}" height="${size}" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <path d="M50 6 L61 38 L95 38 L67 58 L78 92 L50 71 L22 92 L33 58 L5 38 L39 38 Z"
      fill="${color}" stroke="#00000022" stroke-width="1.5"/>
    <circle cx="41" cy="46" r="3" fill="#2b2b2b"/>
    <circle cx="59" cy="46" r="3" fill="#2b2b2b"/>
    <path d="M44 55 Q50 60 56 55" stroke="#2b2b2b" stroke-width="2.2" fill="none" stroke-linecap="round"/>
  </svg>`;
}

function page(item, idx) {
  const color = PALETTE[idx % PALETTE.length];
  const num = idx + 1;
  // count motif grows a little but caps so it never crowds the header (1..10 pattern)
  const count = (idx % 10) + 1;
  const stars = Array.from({ length: count }, () => `<span class="star">${star(color)}</span>`).join('');
  // 4 columns x 5 rows = 20 trace cells
  const cells = Array.from({ length: 20 }, () =>
    `<div class="cell"><span class="trace">${item.c}</span></div>`
  ).join('');

  return `
  <section class="page">
    <header class="head">
      <div class="titles">
        <h1 class="t1" style="color:${color}">ፊደል ግእዝ</h1>
        <h2 class="t2" style="color:${color}">ቀዳማይ መደብ (ግእዝ)</h2>
        <p class="sub">ኣስዕብ ፊደል <b style="color:${color}">${item.c}</b> — ${item.name} (${item.r})</p>
        <p class="word">ፊደል ${num} ካብ 26 • ደሙ ኮዋኽብቲ (${count})</p>
      </div>
      <div class="bigletter" style="color:${color}">${item.c}</div>
    </header>
    <div class="starrow">${stars}</div>
    <div class="grid">${cells}</div>
    <footer class="foot">ብ ዳንኤል ተስፋማርያም • ፊደል ${item.c} (${item.name}) • ገጽ ${num} / 26</footer>
  </section>`;
}

const pages = FIDEL.map((it, i) => page(it, i)).join('\n');

const css = `
  @page { size: A4; margin: 12mm; }
  * { box-sizing: border-box; }
  body { margin:0; font-family:"Noto Sans Ethiopic","Noto Sans",sans-serif; color:#3a3a3a; }
  .page { page-break-after: always; height: 273mm; display:flex; flex-direction:column; }
  .page:last-child { page-break-after: auto; }
  .head { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px; }
  .titles { max-width: 74%; }
  .t1 { font-size: 34pt; margin:0; line-height:1; font-weight:700; letter-spacing:1px; }
  .t2 { font-size: 16pt; margin:2px 0 6px; font-weight:700; -webkit-text-stroke:1px currentColor; color:transparent !important; }
  .sub { font-size: 12pt; font-weight:700; margin:0 0 2px; }
  .word { font-size: 11pt; margin:0; color:#666; }
  .bigletter { font-size: 60pt; line-height:1; font-weight:700; }
  .starrow { display:flex; flex-wrap:wrap; gap:4px; margin:2px 0 6px; min-height:48px; }
  .star { display:inline-flex; }
  .grid { flex:1; display:grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(5, 1fr);
          gap:6px; border:2px solid #777; padding:6px; border-radius:4px; }
  .cell { border:1.5px solid #9a9a9a; border-radius:3px; display:flex; align-items:center; justify-content:center; }
  .trace {
    font-size: 44pt; font-weight:700; line-height:1;
    color: #d0d0d0;
    -webkit-text-stroke: 1.4px #9a9a9a;
  }
  .foot { text-align:center; font-size:9pt; color:#8a8a8a; margin-top:6px; }
`;

const html = `<!DOCTYPE html><html lang="ti"><head><meta charset="utf-8">
<title>ፊደል ግእዝ — ቀዳማይ መደብ</title><style>${css}</style></head><body>${pages}</body></html>`;

writeFileSync(OUT_HTML, html, 'utf8');

const browser = await chromium.launch({
  executablePath: CHROME, headless: true,
  args: ['--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage'],
});
const p = await browser.newPage();
await p.setContent(html, { waitUntil:'load' });
await p.pdf({ path: OUT_PDF, format:'A4', printBackground:true, margin:{top:'12mm',bottom:'12mm',left:'12mm',right:'12mm'} });
await browser.close();
console.log('Fidel PDF written to ' + OUT_PDF + ' (' + FIDEL.length + ' letters)');
