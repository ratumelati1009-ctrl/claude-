# ሙሉእ ናይ ፊደል ሰሌዳ — Full 7-Form Ge'ez Fidel Chart

A complete reference chart of the **Ge'ez fidel (ፊደል)** showing **all seven forms (orders)** for each base consonant.

- **By:** Daniel Tesfamariam
- **Contact:** dannyshalomnebiy@gmail.com

## 📥 Download (PDF)

👉 **[Fidel-Chart-Tigrinya.pdf](Fidel-Chart-Tigrinya.pdf)** — 3 pages, A4, print-ready.

## What's inside

- **34 base consonants**, each shown across all **7 orders**:
  ግእዝ (ä) · ካዕብ (u) · ሣልስ (i) · ራብዕ (a) · ኃምስ (e) · ሳድስ (ə) · ሳብዕ (o)
- That's **238 syllables** in total.
- Each cell shows the **syllable** plus its **romanization** (e.g. bä, bu, bi, ba, be, bə, bo).
- Row labels give the **number** and the **Tigrinya letter name** (ሆይ, ላዊ, ማይ …).
- Column headers give the traditional **order name** and the **vowel sound**.

## The seven orders

| # | Order | Vowel | Example (በ) |
|---|-------|-------|-------------|
| 1 | ግእዝ | ä | በ |
| 2 | ካዕብ | u | ቡ |
| 3 | ሣልስ | i | ቢ |
| 4 | ራብዕ | a | ባ |
| 5 | ኃምስ | e | ቤ |
| 6 | ሳድስ | ə | ብ |
| 7 | ሳብዕ | o | ቦ |

## Files

| File | Description |
|------|-------------|
| `Fidel-Chart-Tigrinya.pdf` | 📄 Print-ready full fidel chart (3 pages, A4) |
| `Fidel-Chart-Tigrinya.html` | Styled HTML source |
| `build-fidel-chart.mjs` | Generator that rebuilds the PDF (uses the Noto Sans Ethiopic font) |

## Rebuilding

```bash
node build-fidel-chart.mjs   # requires a Ge'ez/Ethiopic font, e.g. Noto Sans Ethiopic
```

---

*© Daniel Tesfamariam — dannyshalomnebiy@gmail.com*

> The forms are computed directly from Unicode: in the Ethiopic block each base consonant's seven orders occupy consecutive code points, so the chart is generated programmatically and is consistent across every letter.
