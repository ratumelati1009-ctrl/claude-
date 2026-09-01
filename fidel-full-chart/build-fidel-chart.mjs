import { writeFileSync } from 'node:fs';
import pw from '/opt/toolchains/.nvm/versions/node/v22.23.2/lib/node_modules/@playwright/mcp/node_modules/playwright-core/index.js';
const { chromium } = pw;

const OUT_HTML = '/projects/sandbox/tracing/Fidel-Chart-Tigrinya.html';
const OUT_PDF  = '/projects/sandbox/tracing/Fidel-Chart-Tigrinya.pdf';
const CHROME   = '/opt/playwright/chromium-1232/chrome-linux64/chrome';

// The 7 orders of the fidel. Header shows the traditional Ge'ez name + the vowel sound.
const ORDERS = [
  { name:'ግእዝ',  vowel:'ä' },
  { name:'ካዕብ',  vowel:'u' },
  { name:'ሣልስ',  vowel:'i' },
  { name:'ራብዕ',  vowel:'a' },
  { name:'ኃምስ',  vowel:'e' },
  { name:'ሳድስ',  vowel:'ə' },
  { name:'ሳብዕ',  vowel:'o' },
];

// Base consonants in traditional teaching order.
// For each we store the first-form (ግእዝ) code point; forms 1..7 are the next
// consecutive code points (Unicode Ethiopic block lays out syllables this way:
// base, +1(u), +2(i), +3(a), +4(e), +5(ə/6th), +6(o), +7(labialized/other)).
// name = Tigrinya letter name, r = romanized base consonant.
const BASE = [
  { first:'ሀ', name:'ሆይ',  r:'h'  },
  { first:'ለ', name:'ላዊ',  r:'l'  },
  { first:'ሐ', name:'ሓውት', r:'ḥ'  },
  { first:'መ', name:'ማይ',  r:'m'  },
  { first:'ሠ', name:'ሠውት', r:'ś'  },
  { first:'ረ', name:'ርእስ', r:'r'  },
  { first:'ሰ', name:'ሳት',  r:'s'  },
  { first:'ሸ', name:'ሻ',    r:'š'  },
  { first:'ቀ', name:'ቃፍ',  r:'q'  },
  { first:'በ', name:'ቤት',  r:'b'  },
  { first:'ቨ', name:'ቨ',    r:'v'  },
  { first:'ተ', name:'ታው',  r:'t'  },
  { first:'ቸ', name:'ቸ',    r:'č'  },
  { first:'ኀ', name:'ኀርም', r:'ḫ'  },
  { first:'ነ', name:'ናሓስ', r:'n'  },
  { first:'ኘ', name:'ኘ',    r:'ñ'  },
  { first:'አ', name:'አልፍ', r:'ʾ'  },
  { first:'ከ', name:'ካፍ',  r:'k'  },
  { first:'ኸ', name:'ኸ',    r:'ḵ'  },
  { first:'ወ', name:'ዋዌ',  r:'w'  },
  { first:'ዐ', name:'ዐይን', r:'ʿ'  },
  { first:'ዘ', name:'ዘይ',  r:'z'  },
  { first:'ዠ', name:'ዠ',    r:'ž'  },
  { first:'የ', name:'የመን', r:'y'  },
  { first:'ደ', name:'ድንት', r:'d'  },
  { first:'ጀ', name:'ጀ',    r:'ǧ'  },
  { first:'ገ', name:'ገምል', r:'g'  },
  { first:'ጠ', name:'ጠይት', r:'ṭ'  },
  { first:'ጨ', name:'ጨ',    r:'č̣'  },
  { first:'ጰ', name:'ጰይት', r:'ṗ'  },
  { first:'ጸ', name:'ጸደይ', r:'ṣ'  },
  { first:'ፀ', name:'ፀጳ',  r:'ṣ́'  },
  { first:'ፈ', name:'ኣፍ',  r:'f'  },
  { first:'ፐ', name:'ፕሳ',  r:'p'  },
];

// Build 7 forms from the first-form code point.
function forms(firstChar) {
  const cp = firstChar.codePointAt(0);
  return Array.from({ length: 7 }, (_, i) => String.fromCodePoint(cp + i));
}

// Split rows across pages so each page fits nicely on A4 (with header row per page).
const PER_PAGE = 12;
const chunks = [];
for (let i = 0; i < BASE.length; i += PER_PAGE) chunks.push(BASE.slice(i, i + PER_PAGE));

function tableFor(rows, startIndex) {
  const headCells = ORDERS.map(o =>
    `<th><div class="ord">${o.name}</div><div class="vow">(${o.vowel})</div></th>`
  ).join('');

  const bodyRows = rows.map((b, k) => {
    const idx = startIndex + k + 1;
    const fs = forms(b.first);
    const cells = fs.map((ch, j) =>
      `<td><span class="syl">${ch}</span><span class="rom">${b.r}${ORDERS[j].vowel}</span></td>`
    ).join('');
    return `<tr>
      <th class="rowhead"><span class="rnum">${idx}</span><span class="rname">${b.name}</span></th>
      ${cells}
    </tr>`;
  }).join('');

  return `<table class="fidel">
    <thead><tr><th class="corner">ፊደል</th>${headCells}</tr></thead>
    <tbody>${bodyRows}</tbody>
  </table>`;
}

let pagesHtml = '';
let running = 0;
chunks.forEach((rows, pi) => {
  pagesHtml += `
  <section class="page">
    <header class="head">
      <h1>ሙሉእ ናይ ፊደል ሰሌዳ</h1>
      <p class="sub">ሸውዓተ መደባት ፊደል ግእዝ — ${pi === 0 ? 'ክፋል 1' : 'ክፋል 2'} (ገጽ ${pi + 1} / ${chunks.length})</p>
    </header>
    ${tableFor(rows, running)}
    <footer class="foot">ብ ዳንኤል ተስፋማርያም • dannyshalomnebiy@gmail.com • ሙሉእ ፊደል (7 መደባት)</footer>
  </section>`;
  running += rows.length;
});

const css = `
  @page { size: A4 portrait; margin: 12mm; }
  * { box-sizing: border-box; }
  body { margin:0; font-family:"Noto Sans Ethiopic","Noto Sans",sans-serif; color:#2b2b2b; }
  .page { page-break-after: always; }
  .page:last-child { page-break-after: auto; }
  .head { text-align:center; margin-bottom:8px; }
  .head h1 { font-size: 24pt; margin:0; color:#14532d; font-weight:700; }
  .head .sub { font-size: 11pt; margin:2px 0 0; color:#666; }
  table.fidel { width:100%; border-collapse:collapse; table-layout:fixed; }
  table.fidel th, table.fidel td { border:1px solid #b9b9b9; text-align:center; padding:2px; }
  thead th { background:#14532d; color:#fff; padding:5px 2px; }
  thead .ord { font-size:9.5pt; font-weight:700; }
  thead .vow { font-size:8pt; opacity:.85; }
  .corner { background:#0f3d22 !important; font-size:10pt; }
  .rowhead { background:#f0fdf4; width:16%; }
  .rowhead .rnum { display:inline-block; font-size:8pt; color:#16a34a; font-weight:700; margin-right:4px; }
  .rowhead .rname { font-size:11pt; font-weight:700; color:#14532d; }
  td { height: 46px; }
  td .syl { display:block; font-size:20pt; line-height:1.05; }
  td .rom { display:block; font-size:7.5pt; color:#999; font-family:"Noto Sans",sans-serif; }
  tbody tr:nth-child(even) td { background:#fafafa; }
  .foot { text-align:center; font-size:8.5pt; color:#8a8a8a; margin-top:8px; }
`;

const html = `<!DOCTYPE html><html lang="ti"><head><meta charset="utf-8">
<title>ሙሉእ ናይ ፊደል ሰሌዳ — 7 መደባት</title><style>${css}</style></head><body>${pagesHtml}</body></html>`;

writeFileSync(OUT_HTML, html, 'utf8');

const browser = await chromium.launch({
  executablePath: CHROME, headless: true,
  args: ['--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage'],
});
const p = await browser.newPage();
await p.setContent(html, { waitUntil:'load' });
await p.pdf({ path: OUT_PDF, format:'A4', printBackground:true, margin:{top:'12mm',bottom:'12mm',left:'12mm',right:'12mm'} });
await browser.close();
console.log('Fidel CHART PDF written: ' + OUT_PDF + ' — ' + BASE.length + ' consonants x 7 forms, ' + chunks.length + ' pages');
