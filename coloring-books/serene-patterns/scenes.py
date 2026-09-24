"""
scenes.py — a library of original coloring-book illustrations.

Each function takes a Canvas and draws inside a content box. Designs are built
from vector primitives so they scale to any print resolution. Complexity is
tuned for a general audience: bold, clean outlines with plenty of open regions
to color. Themes chosen for strong marketability (mandalas, animals, florals,
nature, ocean, patterns) — the most popular adult/all-ages coloring niches.
"""

from __future__ import annotations
import math
from artlib import Canvas


# ---------------------------------------------------------------------------
# helpers scoped to a centered content box
# ---------------------------------------------------------------------------
def _box(c: Canvas, inset):
    return inset, inset, c.w - inset, c.h - inset  # x0,y0,x1,y1


def _center(c: Canvas):
    return c.w / 2, c.h / 2


# ===========================================================================
# 1. MANDALAS  (the #1 best-selling coloring niche)
# ===========================================================================
def mandala(c: Canvas, rings=6, petals=12, seed=0):
    cx, cy = _center(c)
    R = min(c.w, c.h) / 2 - 60
    rnd = _rng(seed)

    c.circle(cx, cy, R * 0.06, width=2.6)
    ring_rs = [R * (0.14 + 0.86 * i / (rings - 1)) for i in range(rings)]

    for idx, r in enumerate(ring_rs):
        c.circle(cx, cy, r, width=2.4)
        p = petals if idx % 2 == 0 else petals // 2 * 2 + petals
        p = petals + (idx % 3) * 4
        style = idx % 4
        for k in range(p):
            a = 360.0 * k / p
            rad = math.radians(a)
            px, py = cx + r * math.cos(rad), cy + r * math.sin(rad)
            inner = ring_rs[idx - 1] if idx > 0 else R * 0.06
            ipx = cx + inner * math.cos(rad)
            ipy = cy + inner * math.sin(rad)
            if style == 0:
                c.petal(cx, cy, r, a, spread=360.0 / p * 0.9, width=2.0)
            elif style == 1:
                c.circle(px, py, (r - inner) * 0.28, width=2.0)
            elif style == 2:
                c.line((ipx, ipy), (px, py), width=1.8)
                c.circle(px, py, 4, width=1.8)
            else:
                a2 = math.radians(a + 360.0 / p / 2)
                mx = cx + (r + inner) / 2 * math.cos(a2)
                my = cy + (r + inner) / 2 * math.sin(a2)
                c.star(mx, my, (r - inner) * 0.22, (r - inner) * 0.09,
                       points=5, rot_deg=a, width=1.8)
    # outer scallop
    outer = R
    scal = petals * 2
    for k in range(scal):
        a = math.radians(360.0 * k / scal)
        px, py = cx + outer * math.cos(a), cy + outer * math.sin(a)
        c.circle(px, py, outer * math.pi / scal * 0.9, width=1.8)


# ===========================================================================
# 2. FLORAL BOUQUET
# ===========================================================================
def floral(c: Canvas, seed=0):
    x0, y0, x1, y1 = _box(c, 56)
    cx = c.w / 2
    base_y = y1 - 30
    # vase
    vw = (x1 - x0) * 0.28
    c.polyline([(cx - vw / 2, y1 - 150), (cx - vw / 2 * 0.7, base_y),
                (cx + vw / 2 * 0.7, base_y), (cx + vw / 2, y1 - 150)], width=2.6)
    c.ellipse(cx, y1 - 150, vw / 2, 12, width=2.4)
    for i in range(3):
        yy = base_y - 30 - i * 30
        c.wavy(cx - vw / 2 * 0.65, yy, cx + vw / 2 * 0.65, yy, 3, 3, width=1.6)
    # stems + flowers
    tops = [(cx, y0 + 40, 60), (cx - 120, y0 + 110, 48), (cx + 120, y0 + 110, 48),
            (cx - 70, y0 + 190, 40), (cx + 70, y0 + 190, 40)]
    for (fx, fy, fr) in tops:
        c.wavy(fx, fy + fr, cx, y1 - 155, 8, 2, width=2.2)
        _flower(c, fx, fy, fr)
    # leaves
    for (fx, fy, fr) in tops[1:]:
        side = 1 if fx > cx else -1
        _leaf(c, (fx + cx) / 2, (fy + y1 - 155) / 2, 34, side)


def _flower(c: Canvas, cx, cy, r, petals=8):
    c.circle(cx, cy, r * 0.34, width=2.2)
    for k in range(petals):
        a = 360.0 * k / petals
        c.petal(cx, cy, r, a, spread=360.0 / petals * 0.85, width=2.0)
    for k in range(petals):
        a = math.radians(360.0 * k / petals)
        c.line((cx + r * 0.2 * math.cos(a), cy + r * 0.2 * math.sin(a)),
               (cx + r * 0.32 * math.cos(a), cy + r * 0.32 * math.sin(a)), width=1.6)


def _leaf(c: Canvas, cx, cy, r, side=1):
    a = -90 + 40 * side
    c.petal(cx, cy, r, a, spread=36, width=2.0)


# ===========================================================================
# 3. CUTE ANIMALS — OWL
# ===========================================================================
def owl(c: Canvas):
    cx = c.w / 2
    cy = c.h * 0.44
    R = min(c.w, c.h) * 0.30
    # body
    c.path([("M", (cx - R, cy)),
            ("C", (cx - R, cy + R * 1.5), (cx + R, cy + R * 1.5), (cx + R, cy)),
            ("C", (cx + R, cy - R * 1.2), (cx - R, cy - R * 1.2), (cx - R, cy))],
           width=2.8, closed=True)
    # ear tufts
    c.polyline([(cx - R * 0.7, cy - R * 0.85), (cx - R * 0.95, cy - R * 1.25),
                (cx - R * 0.45, cy - R * 1.0)], width=2.4)
    c.polyline([(cx + R * 0.7, cy - R * 0.85), (cx + R * 0.95, cy - R * 1.25),
                (cx + R * 0.45, cy - R * 1.0)], width=2.4)
    # eyes
    for s in (-1, 1):
        ex = cx + s * R * 0.42
        ey = cy - R * 0.35
        c.circle(ex, ey, R * 0.34, width=2.6)
        c.circle(ex, ey, R * 0.16, width=2.2)
        c.circle(ex + s * R * 0.05, ey - R * 0.05, R * 0.05, width=1.8)
    # beak
    c.polyline([(cx, cy - R * 0.15), (cx - R * 0.12, cy + R * 0.08),
                (cx + R * 0.12, cy + R * 0.08)], width=2.4, closed=True)
    # wing feathers (scallops)
    for row in range(4):
        yy = cy + R * (0.15 + row * 0.28)
        cols = 5 + row
        for k in range(cols):
            fx = cx - R * 0.8 + (1.6 * R) * k / (cols - 1)
            c.arc(fx, yy, R * 0.16, 180, 360, width=1.8)
    # feet
    for s in (-1, 1):
        fx = cx + s * R * 0.35
        c.polyline([(fx, cy + R * 1.35), (fx, cy + R * 1.55)], width=2.4)
        for d in (-1, 0, 1):
            c.line((fx, cy + R * 1.55), (fx + d * 10, cy + R * 1.72), width=2.0)
    # branch
    c.line((cx - R * 1.4, cy + R * 1.6), (cx + R * 1.4, cy + R * 1.6), width=3.0)


# ===========================================================================
# 4. BUTTERFLY (symmetric, mandala-style wings)
# ===========================================================================
def butterfly(c: Canvas):
    cx = c.w / 2
    cy = c.h / 2
    L = min(c.w, c.h) * 0.34
    # body
    c.ellipse(cx, cy, L * 0.06, L * 0.62, width=2.6)
    c.circle(cx, cy - L * 0.62, L * 0.07, width=2.4)
    for a in (-1, 1):
        c.polyline([(cx, cy - L * 0.66),
                    (cx + a * L * 0.18, cy - L * 0.95),
                    (cx + a * L * 0.24, cy - L * 0.9)], width=2.0)  # antennae
        c.circle(cx + a * L * 0.24, cy - L * 0.9, 4, width=1.8)
    for s in (-1, 1):
        # upper wing
        c.path([("M", (cx, cy - L * 0.4)),
                ("C", (cx + s * L * 0.9, cy - L * 1.1),
                 (cx + s * L * 1.2, cy - L * 0.2), (cx + s * L * 0.5, cy - L * 0.05)),
                ("C", (cx + s * L * 0.3, cy - L * 0.1), (cx, cy - L * 0.2),
                 (cx, cy - L * 0.4))], width=2.6, closed=True)
        # lower wing
        c.path([("M", (cx, cy - L * 0.05)),
                ("C", (cx + s * L * 0.6, cy + L * 0.1),
                 (cx + s * L * 0.75, cy + L * 0.8), (cx + s * L * 0.2, cy + L * 0.7)),
                ("C", (cx + s * L * 0.1, cy + L * 0.5), (cx, cy + L * 0.1),
                 (cx, cy - L * 0.05))], width=2.6, closed=True)
        # decorations
        c.ellipse(cx + s * L * 0.55, cy - L * 0.45, L * 0.13, L * 0.18, width=2.0)
        c.circle(cx + s * L * 0.6, cy - L * 0.45, L * 0.05, width=1.8)
        c.ellipse(cx + s * L * 0.32, cy + L * 0.4, L * 0.09, L * 0.13, width=2.0)
        c.circle(cx + s * L * 0.42, cy - L * 0.15, L * 0.045, width=1.8)


# ===========================================================================
# 5. OCEAN — FISH & BUBBLES
# ===========================================================================
def ocean(c: Canvas, seed=0):
    rnd = _rng(seed)
    x0, y0, x1, y1 = _box(c, 44)
    # waterline
    c.wavy(x0, y0 + 24, x1, y0 + 24, 8, 6, width=2.2)
    # seaweed
    for k in range(4):
        sx = x0 + (x1 - x0) * (0.1 + 0.26 * k)
        c.wavy(sx, y1, sx, y1 - 160 - (k % 2) * 40, 16, 3, width=2.2)
    # fish
    fishes = [(0.5, 0.42, 70), (0.28, 0.6, 48), (0.72, 0.66, 54), (0.4, 0.8, 40)]
    for (fx, fy, fr) in fishes:
        _fish(c, x0 + (x1 - x0) * fx, y0 + (y1 - y0) * fy, fr,
              flip=1 if fx < 0.5 else -1)
    # bubbles
    for k in range(14):
        bx = x0 + (x1 - x0) * rnd()
        by = y0 + (y1 - y0) * rnd()
        c.circle(bx, by, 4 + 10 * rnd(), width=1.8)


def _fish(c: Canvas, cx, cy, r, flip=1):
    c.path([("M", (cx - flip * r, cy)),
            ("C", (cx - flip * r, cy - r * 0.7), (cx + flip * r, cy - r * 0.7),
             (cx + flip * r, cy)),
            ("C", (cx + flip * r, cy + r * 0.7), (cx - flip * r, cy + r * 0.7),
             (cx - flip * r, cy))], width=2.6, closed=True)
    # tail
    c.polyline([(cx + flip * r, cy), (cx + flip * r * 1.6, cy - r * 0.5),
                (cx + flip * r * 1.4, cy), (cx + flip * r * 1.6, cy + r * 0.5),
                (cx + flip * r, cy)], width=2.2)
    # eye
    c.circle(cx - flip * r * 0.55, cy - r * 0.15, r * 0.1, width=2.0)
    # fin + scales
    c.arc(cx, cy, r * 0.5, 200, 340, width=1.8)
    for row in range(3):
        for k in range(4):
            c.arc(cx - flip * r * 0.3 + k * r * 0.3 * flip,
                  cy - r * 0.25 + row * r * 0.22, r * 0.16, 200, 340, width=1.6)


# ===========================================================================
# 6. GEOMETRIC / ZENTANGLE PATTERN (full-page repeating pattern)
# ===========================================================================
def pattern(c: Canvas, seed=0):
    x0, y0, x1, y1 = _box(c, 40)
    c.polyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], width=2.6, closed=True)
    cols, rows = 6, 8
    cw = (x1 - x0) / cols
    ch = (y1 - y0) / rows
    for r in range(rows):
        for cidx in range(cols):
            gx = x0 + cidx * cw
            gy = y0 + r * ch
            style = (r * cols + cidx + seed) % 5
            _tile(c, gx, gy, cw, ch, style)


def _tile(c: Canvas, x, y, w, h, style):
    cx, cy = x + w / 2, y + h / 2
    if style == 0:
        for i in range(1, 4):
            c.circle(cx, cy, min(w, h) / 2 * i / 4, width=1.8)
    elif style == 1:
        for i in range(4):
            t = i / 3
            c.line((x + w * t, y), (x + w, y + h * t), width=1.6)
            c.line((x, y + h * t), (x + w * t, y + h), width=1.6)
    elif style == 2:
        c.star(cx, cy, min(w, h) / 2 * 0.8, min(w, h) / 2 * 0.35, 6, width=1.8)
    elif style == 3:
        c.arc(x, y, w * 0.8, 0, 90, width=1.8)
        c.arc(x + w, y + h, w * 0.8, 180, 270, width=1.8)
    else:
        for i in range(3):
            c.rounded_rect(cx - (min(w, h) / 2) * (i + 1) / 3,
                           cy - (min(w, h) / 2) * (i + 1) / 3,
                           (min(w, h)) * (i + 1) / 3,
                           (min(w, h)) * (i + 1) / 3, 4, width=1.6)


# ===========================================================================
# 7. NATURE SCENE — TREE OF LIFE
# ===========================================================================
def tree(c: Canvas):
    cx = c.w / 2
    ground = c.h - 90
    # ground
    c.wavy(60, ground, c.w - 60, ground, 6, 4, width=2.4)
    # trunk
    c.polyline([(cx - 26, ground), (cx - 16, c.h * 0.5),
                (cx + 16, c.h * 0.5), (cx + 26, ground)], width=2.8)
    c.wavy(cx - 8, ground, cx - 4, c.h * 0.52, 3, 5, width=1.4)
    # roots
    for s in (-1, 1):
        c.wavy(cx + s * 20, ground, cx + s * 90, ground + 4, 6, 2, width=2.0)
    # branches + canopy
    top = c.h * 0.5
    c.circle(cx, top - 70, 130, width=2.8)
    for a in range(0, 360, 30):
        rad = math.radians(a)
        c.circle(cx + 130 * math.cos(rad), top - 70 + 130 * math.sin(rad),
                 42, width=2.2)
    # inner leaves
    rnd = _rng(3)
    for _ in range(40):
        a = rnd() * 2 * math.pi
        rr = 120 * rnd()
        lx = cx + rr * math.cos(a)
        ly = top - 70 + rr * math.sin(a)
        c.petal(lx, ly, 16, math.degrees(a), spread=40, width=1.6)
    # sun
    _sun(c, c.w - 110, 110, 34)


def _sun(c: Canvas, cx, cy, r):
    c.circle(cx, cy, r, width=2.4)
    for a in range(0, 360, 30):
        rad = math.radians(a)
        c.line((cx + r * 1.25 * math.cos(rad), cy + r * 1.25 * math.sin(rad)),
               (cx + r * 1.7 * math.cos(rad), cy + r * 1.7 * math.sin(rad)),
               width=2.0)


# ===========================================================================
# 8. SPACE — ROCKET, PLANETS, STARS
# ===========================================================================
def space(c: Canvas, seed=0):
    rnd = _rng(seed)
    cx = c.w / 2
    cy = c.h / 2
    # rocket
    rx, ry = cx, cy + 20
    c.path([("M", (rx, ry - 150)),
            ("C", (rx + 46, ry - 110), (rx + 46, ry + 60), (rx + 30, ry + 90)),
            ("L", (rx - 30, ry + 90)),
            ("C", (rx - 46, ry + 60), (rx - 46, ry - 110), (rx, ry - 150))],
           width=2.8, closed=True)
    c.circle(rx, ry - 60, 26, width=2.4)
    c.circle(rx, ry - 60, 14, width=2.0)
    for s in (-1, 1):
        c.polyline([(rx + s * 30, ry + 30), (rx + s * 70, ry + 100),
                    (rx + s * 30, ry + 90)], width=2.4)
    # flames
    c.polyline([(rx - 22, ry + 92), (rx - 10, ry + 140), (rx, ry + 100),
                (rx + 10, ry + 140), (rx + 22, ry + 92)], width=2.2)
    # planets
    _planet(c, 120, 140, 54, ring=True)
    _planet(c, c.w - 130, c.h - 170, 66, ring=False)
    c.circle(c.w - 120, 150, 30, width=2.2)
    for cr in [(c.w - 128, 142, 6), (c.w - 108, 158, 8), (c.w - 118, 165, 5)]:
        c.circle(*cr[:2], cr[2], width=1.8)
    # stars
    for _ in range(24):
        c.star(60 + rnd() * (c.w - 120), 60 + rnd() * (c.h - 120),
               6 + rnd() * 8, 3 + rnd() * 3, 5, rot_deg=rnd() * 72, width=1.6)


def _planet(c: Canvas, cx, cy, r, ring=False):
    c.circle(cx, cy, r, width=2.6)
    c.wavy(cx - r, cy - r * 0.2, cx + r, cy - r * 0.2, r * 0.12, 2, width=1.6)
    c.wavy(cx - r * 0.9, cy + r * 0.3, cx + r * 0.9, cy + r * 0.3, r * 0.1, 2, width=1.6)
    c.circle(cx - r * 0.3, cy - r * 0.3, r * 0.18, width=1.6)
    if ring:
        c.ellipse(cx, cy, r * 1.6, r * 0.5, width=2.2)


# ===========================================================================
# 9. HOT AIR BALLOON
# ===========================================================================
def balloon(c: Canvas):
    cx = c.w / 2
    top = c.h * 0.16
    R = min(c.w, c.h) * 0.24
    c.path([("M", (cx - R, top + R)),
            ("C", (cx - R, top - R * 0.4), (cx + R, top - R * 0.4),
             (cx + R, top + R)),
            ("C", (cx + R * 0.6, top + R * 1.7), (cx - R * 0.6, top + R * 1.7),
             (cx - R, top + R))], width=2.8, closed=True)
    # gores
    for f in (-0.66, -0.33, 0, 0.33, 0.66):
        c.path([("M", (cx + R * f, top + R * 1.65)),
                ("C", (cx + R * f * 1.6, top + R * 0.4),
                 (cx + R * f * 1.6, top),
                 (cx + R * f, top - R * 0.35 * (1 - abs(f))))], width=1.8)
    c.wavy(cx - R * 0.7, top + R * 1.55, cx + R * 0.7, top + R * 1.55, 6, 4, width=1.8)
    # basket + ropes
    bw = R * 0.5
    by = top + R * 2.3
    for s in (-1, 1):
        c.line((cx + s * R * 0.7, top + R * 1.6), (cx + s * bw / 2, by), width=1.8)
    c.polyline([(cx - bw / 2, by), (cx - bw / 2 * 0.85, by + 46),
                (cx + bw / 2 * 0.85, by + 46), (cx + bw / 2, by)],
               width=2.6, closed=True)
    for i in range(1, 4):
        xx = cx - bw / 2 + bw * i / 4
        c.line((xx, by), (xx - 4, by + 46), width=1.4)
    # clouds
    _cloud(c, 120, top + 20, 40)
    _cloud(c, c.w - 130, top + R * 1.4, 46)


def _cloud(c: Canvas, cx, cy, r):
    c.arc(cx - r, cy, r * 0.6, 90, 270, width=2.2)
    c.arc(cx - r * 0.4, cy - r * 0.4, r * 0.6, 130, 360, width=2.2)
    c.arc(cx + r * 0.4, cy - r * 0.3, r * 0.55, 180, 400, width=2.2)
    c.arc(cx + r, cy, r * 0.55, 270, 450, width=2.2)
    c.line((cx - r, cy + r * 0.6), (cx + r, cy + r * 0.55), width=2.2)


# ===========================================================================
# 10. PAISLEY / DECORATIVE FEATHER
# ===========================================================================
def feather(c: Canvas):
    cx = c.w / 2
    top = c.h * 0.16
    bot = c.h * 0.86
    c.line((cx, top), (cx, bot), width=2.8)  # rachis
    n = 16
    for i in range(1, n + 1):
        t = i / (n + 1)
        y = top + (bot - top) * t
        w = (min(c.w, c.h) * 0.22) * math.sin(t * math.pi) + 20
        for s in (-1, 1):
            c.path([("M", (cx, y)),
                    ("C", (cx + s * w * 0.6, y - 18),
                     (cx + s * w, y - 26), (cx + s * w, y)),
                    ("C", (cx + s * w, y + 20), (cx + s * w * 0.5, y + 14),
                     (cx, y + 6))], width=1.8)
    # decorative beads hanging
    for s in (-1, 0, 1):
        bx = cx + s * 40
        c.line((bx, bot), (bx, bot + 40), width=1.6)
        c.circle(bx, bot + 50, 8, width=1.8)
        c.star(bx, bot + 50, 5, 2, 5, width=1.2)


# ---------------------------------------------------------------------------
# tiny deterministic RNG so pages are reproducible
# ---------------------------------------------------------------------------
def _rng(seed):
    state = [ (seed * 2654435761 + 12345) & 0xFFFFFFFF ]
    def nxt():
        state[0] = (1103515245 * state[0] + 12345) & 0x7FFFFFFF
        return state[0] / 0x7FFFFFFF
    return nxt
