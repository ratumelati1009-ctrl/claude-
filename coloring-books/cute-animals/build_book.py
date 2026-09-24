"""
build_book.py — assembles the 42-page Cute Animals Coloring Book.

Outputs:
  - interior.pdf        print-ready interior, 8.5 x 11 in, portrait, white bg
  - cover.pdf           front cover, 8.5 x 11 in
  - pages/*.svg         every page as scalable SVG

Spec: ages 4-10, black line art only, single-sided friendly, comfortable
white margins so nothing important is cropped.
"""
from __future__ import annotations
import os
from artlib import Canvas, to_svg, to_pdf_stream
from pdfwriter import write_pdf
import vecfont as vf
import kit as K
from animals import PAGES

DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(DIR, "pages")

DPI = 72
PAGE_W = 8.5 * DPI      # 612 pt  (300-DPI equivalent when printed: 2550x3300 px)
PAGE_H = 11.0 * DPI     # 792 pt
MARGIN = 0.5 * DPI

BOOK_TITLE = "CUTE ANIMAL FRIENDS"
BOOK_SUB = "A COLORING BOOK"


def _frame(c: Canvas):
    m = MARGIN * 0.55
    c.rounded_rect(m, m, c.w - 2 * m, c.h - 2 * m, 16, width=1.4)


def _footer(c: Canvas, number, label):
    # sits just inside the bottom border, below all artwork
    y = c.h - MARGIN * 0.42
    vf.draw_text_fit(c, label, c.w / 2, y - 14, 10, c.w * 0.7, width=1.3)
    vf.draw_text(c, str(number), c.w / 2, y, 12, width=1.5, center=True)


def coloring_page(number, label, fn):
    c = Canvas(PAGE_W, PAGE_H)
    _frame(c)
    fn(c)
    _footer(c, number, label)
    return c


# ---- front / back matter ---------------------------------------------------
def title_page():
    c = Canvas(PAGE_W, PAGE_H)
    _frame(c)
    cx = c.w / 2
    # cheerful animal trio banner up top
    from animals import _mini_bunny, _mini_bear, _mini_cat
    band = c.h * 0.3
    _mini_bunny(c, cx - 130, band)
    _mini_bear(c, cx, band + 6)
    _mini_cat(c, cx + 130, band)
    vf.draw_text_fit(c, BOOK_TITLE, cx, c.h * 0.56, 24, c.w * 0.78, width=2.6)
    c.line((cx - 180, c.h * 0.56 + 24), (cx + 180, c.h * 0.56 + 24), width=1.6)
    vf.draw_text(c, BOOK_SUB, cx, c.h * 0.56 + 58, 15, width=1.8, center=True)
    vf.draw_text_fit(c, "42 ADORABLE DESIGNS - AGES 4 TO 10", cx, c.h * 0.56 + 96,
                     10, c.w * 0.72, width=1.3)
    K.flower(c, cx - 170, c.h * 0.8, 30)
    K.flower(c, cx + 170, c.h * 0.8, 30)
    K.grass(c, 120, c.w - 120, c.h * 0.86, 14)
    return c


def belongs_page():
    c = Canvas(PAGE_W, PAGE_H)
    _frame(c)
    cx = c.w / 2
    vf.draw_text(c, "THIS BOOK BELONGS TO", cx, c.h * 0.36, 16, width=2.0, center=True)
    c.line((cx - 190, c.h * 0.46), (cx + 190, c.h * 0.46), width=1.6)
    from animals import _mini_fox, _mini_bunny
    _mini_fox(c, cx - 90, c.h * 0.68)
    _mini_bunny(c, cx + 90, c.h * 0.68)
    K.flower(c, cx, c.h * 0.62, 30)
    K.grass(c, 140, c.w - 140, c.h * 0.74, 12)
    return c


def howto_page():
    c = Canvas(PAGE_W, PAGE_H)
    _frame(c)
    cx = c.w / 2
    vf.draw_text(c, "LET'S COLOR", cx, c.h * 0.2, 20, width=2.2, center=True)
    lines = [
        "PICK YOUR FAVORITE COLORS",
        "STAY INSIDE THE LINES OR DON'T",
        "USE CRAYONS PENCILS OR MARKERS",
        "COLOR EACH CUTE ANIMAL FRIEND",
        "HAVE LOTS AND LOTS OF FUN",
    ]
    y = c.h * 0.34
    for ln in lines:
        vf.draw_text_fit(c, ln, cx, y, 12, c.w * 0.72, width=1.4)
        y += 46
    from animals import _mini_bear
    _mini_bear(c, cx, c.h * 0.82)
    K.grass(c, 140, c.w - 140, c.h * 0.88, 12)
    return c


def thanks_page():
    c = Canvas(PAGE_W, PAGE_H)
    _frame(c)
    cx = c.w / 2
    from animals import _mini_bunny, _mini_cat
    _mini_bunny(c, cx - 90, c.h * 0.34)
    _mini_cat(c, cx + 90, c.h * 0.34)
    vf.draw_text(c, "THE END", cx, c.h * 0.56, 26, width=2.6, center=True)
    vf.draw_text(c, "GREAT JOB LITTLE ARTIST", cx, c.h * 0.62, 12,
                 width=1.4, center=True)
    K.flower(c, cx - 150, c.h * 0.78, 30)
    K.flower(c, cx + 150, c.h * 0.78, 30)
    K.grass(c, 120, c.w - 120, c.h * 0.84, 14)
    return c


def cover_page():
    c = Canvas(PAGE_W, PAGE_H)
    m = 20
    c.rounded_rect(m, m, c.w - 2 * m, c.h - 2 * m, 20, width=3.0)
    c.rounded_rect(m + 10, m + 10, c.w - 2 * m - 20, c.h - 2 * m - 20, 16, width=1.4)
    cx = c.w / 2
    from animals import _mini_bunny, _mini_bear, _mini_cat, _mini_fox
    band = c.h * 0.34
    _mini_bunny(c, cx - 180, band)
    _mini_bear(c, cx - 60, band + 8)
    _mini_cat(c, cx + 60, band + 8)
    _mini_fox(c, cx + 180, band)
    vf.draw_text_fit(c, BOOK_TITLE, cx, c.h * 0.6, 26, c.w * 0.74, width=2.8)
    c.line((cx - 190, c.h * 0.6 + 26), (cx + 190, c.h * 0.6 + 26), width=2.0)
    vf.draw_text(c, BOOK_SUB, cx, c.h * 0.6 + 60, 15, width=1.8, center=True)
    vf.draw_text_fit(c, "42 ADORABLE DESIGNS FOR KIDS", cx, c.h * 0.72, 11,
                     c.w * 0.7, width=1.4)
    K.flower(c, cx - 150, c.h * 0.84, 34)
    K.flower(c, cx + 150, c.h * 0.84, 34)
    K.grass(c, 120, c.w - 120, c.h * 0.9, 16)
    return c


def build():
    os.makedirs(PAGES_DIR, exist_ok=True)
    canvases = []
    canvases.append(("front_title", title_page()))
    canvases.append(("front_belongs", belongs_page()))
    canvases.append(("front_howto", howto_page()))

    for i, (label, fn) in enumerate(PAGES, start=1):
        canvases.append((f"page_{i:02d}", coloring_page(i, label, fn)))

    canvases.append(("back_thanks", thanks_page()))

    for name, c in canvases:
        with open(os.path.join(PAGES_DIR, f"{name}.svg"), "w") as f:
            f.write(to_svg(c))

    pdf_pages = [(c.w, c.h, to_pdf_stream(c)) for _, c in canvases]
    size = write_pdf(os.path.join(DIR, "interior.pdf"), pdf_pages)

    cov = cover_page()
    with open(os.path.join(PAGES_DIR, "cover.svg"), "w") as f:
        f.write(to_svg(cov))
    write_pdf(os.path.join(DIR, "cover.pdf"), [(cov.w, cov.h, to_pdf_stream(cov))])

    return len(canvases), len(PAGES), size


if __name__ == "__main__":
    total, coloring, size = build()
    print(f"Total interior pages: {total}  (coloring: {coloring}, matter: {total - coloring})")
    print(f"interior.pdf: {size} bytes")
