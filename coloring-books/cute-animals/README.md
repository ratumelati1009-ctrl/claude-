# Cute Animal Friends — A Coloring Book (Ages 4–10)

A complete, **print-ready 42-page Cute Animals Coloring Book** built entirely
from zero-dependency Python. Every illustration is original vector line art —
bold, clean outlines with big open coloring spaces and friendly faces — so it
scales to any print resolution without pixelation.

## What you get

| File | Description |
|------|-------------|
| `interior.pdf` | The full book interior — **46 pages**: title, "this book belongs to", "let's color" how-to, **42 cute-animal coloring pages**, and a closing page. Sized **8.5 × 11 in**, portrait, pure white background. |
| `cover.pdf` | A matching front cover (8.5 × 11 in). |
| `pages/*.svg` | Every page as a standalone scalable SVG. |

## The 42 coloring pages

Matches the requested subject list exactly, all drawn in one consistent style:

1. Puppy in a flower garden · 2. Kitten & butterflies · 3. Bunny & spring
flowers · 4. Baby elephant holding a flower · 5. Panda eating bamboo ·
6. Baby deer among wildflowers · 7. Hedgehog with flowers · 8. Owl on a branch
under stars · 9. Sleepy fox & crescent moon · 10. Turtle & little fish ·
11. Llama in a mountain meadow · 12. Koala hugging a tree · 13. Baby lion &
flowers · 14. Monkey with a banana · 15. Giraffe & butterflies · 16. Baby zebra
· 17. Hippo by the pond · 18. Crocodile with a flower crown · 19. Penguin &
snowflake · 20. Polar bear in the snow · 21. Dolphin jumping · 22. Whale &
bubbles · 23. Baby seal & seashells · 24. Happy octopus · 25. Seahorse & coral
· 26. Duck in the pond · 27. Chick & spring flowers · 28. Lamb in the meadow ·
29. Goat by the fence · 30. Piglet & daisies · 31. Calf in the field ·
32. Horse & flowers · 33. Raccoon with a flower · 34. Squirrel & acorns ·
35. Bear cub picnic · 36. Sloth on a branch · 37. Kangaroo & joey · 38. Alpaca
& cactus flowers · 39. Frog on a lily pad · 40. Snail & mushrooms · 41. Puppy,
kitten & bunny together · 42. Meadow celebration (grand finale).

## Style & consistency

The whole book shares one look via a common drawing kit (`kit.py`): identical
line thickness (bold main outline, medium secondary, thin accents), the same
big round sparkle eyes, the same flower/grass/leaf motifs, and child-friendly
proportions — so it reads like one artist illustrated the entire book.

## Want the soft "AI-illustrated" look from the reference?

The polished fluffy-fur style (like the marketing samples) is produced by an AI
**image** generator, not by code. This project includes everything to get there:

- **`AI_IMAGE_PROMPTS.md`** — a cover prompt + **42 ready-to-paste prompts**
  (one per page) for Midjourney / DALL·E / Leonardo / Ideogram, sharing one
  consistent style block so the whole book matches.
- **`assemble_from_images.py`** — drop your generated PNGs into `img/`
  (`page_01.png` … `page_42.png`, optional `cover.png`) and run it to compile a
  print-ready **8.5 × 11 in, 300-DPI KDP PDF** (`Cute-Animals-FINAL.pdf`).
  Zero dependencies; handles PNG (RGB/RGBA/grey/palette) and JPEG.

```bash
# after saving your AI images into ./img
python3 assemble_from_images.py
```

The included `interior.pdf` is the **code-drawn line-art version** (clean cartoon
outlines) — a complete, usable book on its own, or a backup.

## Regenerate / customize the line-art version

```bash
python3 build_book.py
```

Pure Python 3, **no external packages** (works fully offline).

- `artlib.py` — vector Canvas that exports to both SVG and PDF.
- `kit.py` — the reusable cute-animal parts + background motifs.
- `animals.py` — the 42 scene builders and the ordered `PAGES` list.
- `vecfont.py` — single-stroke vector font (auto-fits titles; no font embedding).
- `pdfwriter.py` — minimal multi-page PDF writer.
- `build_book.py` — page layout, front/back matter, build entrypoint.

### Common tweaks

- **Rename the book:** edit `BOOK_TITLE` / `BOOK_SUB` in `build_book.py`.
- **Reorder / swap pages:** edit the `PAGES` list in `animals.py`.
- **Add an animal:** write `def my_animal(c): ...` using `kit` helpers, then add
  `("MY ANIMAL", my_animal)` to `PAGES`.
- **Trim size:** change `PAGE_W` / `PAGE_H` in `build_book.py` (72 pt = 1 in).

## Print / self-publish notes

- Interior: **8.5 × 11 in**, portrait, 0.5 in safe margin — vector art prints at
  any DPI (equivalent to 2550 × 3300 px at 300 DPI).
- Black line art on white — ideal for print-on-demand (Amazon KDP, Lulu,
  IngramSpark) and home printing.
- **Single-sided friendly:** if your printer prints double-sided, insert a blank
  page between designs so colors don't show through.
- For a KDP paperback cover you'll build a full wrap (back + spine + front);
  spine width depends on final page count and paper. See `LISTING.md`.
