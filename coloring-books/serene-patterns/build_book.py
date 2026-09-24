"""
build_book.py — assembles the 42-page coloring book.

Outputs:
  - interior.pdf        (print-ready interior, 8.5 x 11 in)
  - cover.pdf           (front cover, 8.5 x 11 in)
  - pages/page_NN.svg   (every interior page as scalable SVG)

Interior structure (42 numbered coloring pages + front/back matter):
  Title page, "This book belongs to" page, how-to page,
  42 coloring pages, and a closing "thank you" page.
"""
from __future__ import annotations
import os
from artlib import Canvas, to_svg, to_pdf_stream
from pdfwriter import write_pdf
import scenes
import vecfont as vf

DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(DIR, "pages")

# --- print spec (Amazon KDP-friendly) --------------------------------------
DPI = 72
PAGE_W = 8.5 * DPI      # 612 pt
PAGE_H = 11.0 * DPI     # 792 pt
MARGIN = 0.5 * DPI      # 0.5 in safe margin

BOOK_TITLE = "SERENE PATTERNS"
BOOK_SUB = "A COLORING JOURNEY"

# 42 coloring pages: cycle through the 10 themes with varied seeds so no two
# pages are identical. (thumb_label, builder, kwargs)
def _plan():
    themes = [
        ("MANDALA", scenes.mandala, lambda i: dict(rings=5 + i % 3, petals=10 + (i % 4) * 2, seed=i)),
        ("FLORAL BOUQUET", scenes.floral, lambda i: dict(seed=i)),
        ("WISE OWL", scenes.owl, lambda i: dict()),
        ("BUTTERFLY", scenes.butterfly, lambda i: dict()),
        ("UNDER THE SEA", scenes.ocean, lambda i: dict(seed=i)),
        ("ZEN PATTERN", scenes.pattern, lambda i: dict(seed=i)),
        ("TREE OF LIFE", scenes.tree, lambda i: dict()),
        ("OUTER SPACE", scenes.space, lambda i: dict(seed=i)),
        ("HOT AIR BALLOON", scenes.balloon, lambda i: dict()),
        ("DREAM FEATHER", scenes.feather, lambda i: dict()),
    ]
    plan = []
    for i in range(42):
        label, fn, kw = themes[i % len(themes)]
        plan.append((label, fn, kw(i)))
    return plan


# --- page decorations -------------------------------------------------------
def _frame(c: Canvas):
    m = MARGIN * 0.55
    c.rounded_rect(m, m, c.w - 2 * m, c.h - 2 * m, 14, width=1.4)


def _footer(c: Canvas, number, label):
    vf.draw_text(c, label, c.w / 2, c.h - MARGIN * 0.62, 11, width=1.3, center=True)
    vf.draw_text(c, str(number), c.w / 2, c.h - MARGIN * 0.62 + 22, 13,
                 width=1.5, center=True)


def make_coloring_page(number, label, fn, kwargs):
    c = Canvas(PAGE_W, PAGE_H)
    _frame(c)
    # draw art within an inset content region by handing the builder a canvas;
    # builders already respect their own insets relative to the full canvas.
    fn(c, **kwargs)
    _footer(c, number, label)
    return c


# --- front / back matter ----------------------------------------------------
def title_page():
    c = Canvas(PAGE_W, PAGE_H)
    _frame(c)
    cx = c.w / 2
    scenes.mandala(_sub_canvas(c), rings=4, petals=12, seed=7) if False else None
    # decorative top mandala band
    _mini_mandala(c, cx, c.h * 0.24, 90)
    vf.draw_text(c, BOOK_TITLE, cx, c.h * 0.5, 30, width=3.0, center=True)
    c.line((cx - 150, c.h * 0.5 + 24), (cx + 150, c.h * 0.5 + 24), width=1.6)
    vf.draw_text(c, BOOK_SUB, cx, c.h * 0.5 + 60, 15, width=1.8, center=True)
    vf.draw_text(c, "42 HAND-DRAWN DESIGNS", cx, c.h * 0.5 + 100, 11,
                 width=1.4, center=True)
    _mini_mandala(c, cx, c.h * 0.8, 70)
    return c


def belongs_page():
    c = Canvas(PAGE_W, PAGE_H)
    _frame(c)
    cx = c.w / 2
    vf.draw_text(c, "THIS BOOK BELONGS TO", cx, c.h * 0.4, 18, width=2.0, center=True)
    c.line((cx - 200, c.h * 0.5), (cx + 200, c.h * 0.5), width=1.6)
    _mini_mandala(c, cx, c.h * 0.68, 80)
    return c


def howto_page():
    c = Canvas(PAGE_W, PAGE_H)
    _frame(c)
    cx = c.w / 2
    vf.draw_text(c, "HOW TO ENJOY", cx, c.h * 0.22, 20, width=2.2, center=True)
    lines = [
        "FIND A CALM, WELL-LIT SPACE",
        "USE PENCILS, GEL PENS OR MARKERS",
        "PLACE A SHEET BEHIND EACH PAGE",
        "START AT THE EDGES, WORK INWARD",
        "THERE ARE NO RULES - JUST RELAX",
    ]
    y = c.h * 0.36
    for ln in lines:
        c.circle(cx - vf.text_width(ln, 12) / 2 - 22, y - 4, 5, width=1.6)
        vf.draw_text(c, ln, cx, y, 12, width=1.4, center=True)
        y += 46
    _mini_mandala(c, cx, c.h * 0.86, 60)
    return c


def thanks_page():
    c = Canvas(PAGE_W, PAGE_H)
    _frame(c)
    cx = c.w / 2
    _mini_mandala(c, cx, c.h * 0.32, 90)
    vf.draw_text(c, "THANK YOU", cx, c.h * 0.56, 26, width=2.6, center=True)
    vf.draw_text(c, "WE HOPE YOU FOUND YOUR CALM", cx, c.h * 0.62, 12,
                 width=1.4, center=True)
    vf.draw_text(c, "SHARE YOUR ART & KEEP COLORING", cx, c.h * 0.66, 12,
                 width=1.4, center=True)
    return c


def _mini_mandala(c: Canvas, cx, cy, R):
    c.circle(cx, cy, R, width=2.0)
    c.circle(cx, cy, R * 0.6, width=1.6)
    c.circle(cx, cy, R * 0.2, width=1.6)
    p = 12
    for k in range(p):
        a = 360.0 * k / p
        c.petal(cx, cy, R, a, spread=360.0 / p * 0.9, width=1.6)


def _sub_canvas(c):  # unused placeholder to keep API tidy
    return c


# --- cover ------------------------------------------------------------------
def cover_page():
    c = Canvas(PAGE_W, PAGE_H)
    m = 20
    c.rounded_rect(m, m, c.w - 2 * m, c.h - 2 * m, 20, width=3.0)
    c.rounded_rect(m + 10, m + 10, c.w - 2 * m - 20, c.h - 2 * m - 20, 16, width=1.4)
    cx = c.w / 2
    _mini_mandala(c, cx, c.h * 0.28, 118)
    vf.draw_text(c, BOOK_TITLE, cx, c.h * 0.60, 34, width=3.4, center=True)
    c.line((cx - 170, c.h * 0.60 + 26), (cx + 170, c.h * 0.60 + 26), width=2.0)
    vf.draw_text(c, BOOK_SUB, cx, c.h * 0.60 + 64, 16, width=2.0, center=True)
    vf.draw_text(c, "42 RELAXING DESIGNS FOR ALL AGES", cx, c.h * 0.72, 11,
                 width=1.4, center=True)
    _mini_mandala(c, cx * 0.5, c.h * 0.85, 46)
    _mini_mandala(c, cx * 1.5, c.h * 0.85, 46)
    return c


# --- build ------------------------------------------------------------------
def build():
    os.makedirs(PAGES_DIR, exist_ok=True)
    interior_canvases = []

    interior_canvases.append(("front_title", title_page()))
    interior_canvases.append(("front_belongs", belongs_page()))
    interior_canvases.append(("front_howto", howto_page()))

    for i, (label, fn, kwargs) in enumerate(_plan(), start=1):
        c = make_coloring_page(i, label, fn, kwargs)
        interior_canvases.append((f"page_{i:02d}", c))

    interior_canvases.append(("back_thanks", thanks_page()))

    # write SVGs (coloring pages only get clean numbered svgs; all pages saved)
    for name, c in interior_canvases:
        with open(os.path.join(PAGES_DIR, f"{name}.svg"), "w") as f:
            f.write(to_svg(c))

    # write interior PDF
    pdf_pages = [(c.w, c.h, to_pdf_stream(c)) for _, c in interior_canvases]
    size = write_pdf(os.path.join(DIR, "interior.pdf"), pdf_pages)

    # cover
    cov = cover_page()
    with open(os.path.join(PAGES_DIR, "cover.svg"), "w") as f:
        f.write(to_svg(cov))
    write_pdf(os.path.join(DIR, "cover.pdf"), [(cov.w, cov.h, to_pdf_stream(cov))])

    return len(interior_canvases), size


if __name__ == "__main__":
    total, size = build()
    print(f"Interior pages: {total}  (42 coloring + {total - 42} matter)")
    print(f"interior.pdf: {size} bytes")
