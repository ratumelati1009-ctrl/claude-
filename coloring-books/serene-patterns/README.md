# Serene Patterns — A Coloring Journey

A complete, **print-ready 42-page coloring book** generated entirely from
zero-dependency Python. Every illustration is original vector line art, so it
scales to any print resolution without pixelation.

## What you get

| File | Description |
|------|-------------|
| `interior.pdf` | The full book interior — **46 pages**: title, "this book belongs to", how-to, **42 coloring pages**, and a closing thank-you page. Sized **8.5 × 11 in**. |
| `cover.pdf` | A matching front cover (8.5 × 11 in). |
| `pages/*.svg` | Every page as a standalone scalable SVG (edit or re-color freely). |

## The 42 coloring pages

Ten popular, high-demand coloring themes, rotated with varied parameters so no
two pages are identical:

1. Mandalas (the best-selling coloring niche)
2. Floral bouquets
3. Wise owls
4. Symmetric butterflies
5. Under-the-sea fish scenes
6. Zen / geometric pattern tiles
7. Tree of life
8. Outer space (rockets, planets, stars)
9. Hot air balloons
10. Dream feathers

## Regenerate / customize

```bash
python3 build_book.py
```

Everything is pure Python 3 with **no external packages** (works fully offline).

- `artlib.py` — vector Canvas that exports to both SVG and PDF.
- `scenes.py` — the illustration library (add your own `def myscene(c, ...)`).
- `vecfont.py` — single-stroke vector font for all text (no font embedding).
- `pdfwriter.py` — minimal multi-page PDF writer.
- `build_book.py` — page layout, front/back matter, and the build entrypoint.

### Common tweaks

- **Rename the book:** edit `BOOK_TITLE` / `BOOK_SUB` in `build_book.py`.
- **Change page count:** edit the `range(42)` in `_plan()`.
- **Reorder / swap themes:** edit the `themes` list in `_plan()`.
- **Trim size:** change `PAGE_W` / `PAGE_H` (values are in points; 72 pt = 1 in).

## Print / self-publish notes

- Interior is designed for **8.5 × 11 in** with a **0.5 in safe margin**.
- Line art is pure black on white — ideal for print-on-demand (Amazon KDP,
  Lulu, IngramSpark) and for home printing.
- For KDP paperback you may want to add bleed and a spine to the cover based on
  your final page count and paper choice — see `LISTING.md` for a checklist.

## A note on the artwork

These illustrations are generated procedurally from geometric primitives
(mandalas, florals, animals, etc.). They are original and royalty-free for you
to sell. They are intentionally clean and bold so they color beautifully with
pencils, gel pens, or markers.
