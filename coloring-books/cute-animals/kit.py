"""
kit.py — a consistent "cute animal" drawing kit.

Reusable parts so all 42 pages share ONE style: the same bold rounded outlines,
the same big friendly eyes, the same flower/leaf/background motifs. Each helper
draws onto a Canvas from artlib. Line weights: BOLD for main outline, MID for
secondary shapes, THIN for tiny accents — matching the book's style rules.
"""
from __future__ import annotations
import math
from artlib import Canvas

BOLD = 3.4
MID = 2.4
THIN = 1.8

# --------------------------------------------------------------------------
# EYES / FACE — the signature look (large, round, happy)
# --------------------------------------------------------------------------
def eyes(c: Canvas, cx, cy, spacing, r, style="happy"):
    for s in (-1, 1):
        ex = cx + s * spacing / 2
        if style == "closed":
            c.arc(ex, cy, r, 200, 340, width=MID)
            continue
        c.circle(ex, cy, r, width=MID)              # eye outline
        c.circle(ex, cy + r * 0.1, r * 0.55, width=THIN)  # pupil
        c.circle(ex + s * r * 0.25, cy - r * 0.2, r * 0.18, width=THIN)  # sparkle


def blush(c: Canvas, cx, cy, spacing, r):
    for s in (-1, 1):
        c.circle(cx + s * spacing / 2, cy, r, width=THIN)


def smile(c: Canvas, cx, cy, w, depth=1.0):
    c.arc(cx, cy, w, 20 * depth + 10, 170 - 20 * depth + 10, width=MID)


def nose_muzzle(c: Canvas, cx, cy, r):
    c.ellipse(cx, cy, r, r * 0.7, width=MID)          # nose
    c.line((cx, cy + r * 0.7), (cx, cy + r * 1.6), width=THIN)  # philtrum
    c.arc(cx - r, cy + r * 1.6, r, 20, 160, width=THIN)
    c.arc(cx + r, cy + r * 1.6, r, 20, 160, width=THIN)


def ear_round(c: Canvas, cx, cy, r, inner=True):
    c.circle(cx, cy, r, width=BOLD)
    if inner:
        c.circle(cx, cy, r * 0.55, width=THIN)


def ear_pointy(c: Canvas, tip, base_l, base_r, inner=True):
    c.polyline([base_l, tip, base_r], width=BOLD, closed=True)
    if inner:
        mx = (base_l[0] + base_r[0]) / 2
        my = (base_l[1] + base_r[1]) / 2
        c.polyline([( (base_l[0]+mx)/2, (base_l[1]+my)/2 ), tip,
                    ( (base_r[0]+mx)/2, (base_r[1]+my)/2 )], width=THIN)


def ear_long(c: Canvas, cx, cy, w, h, tilt=0, inner=True):
    a = math.radians(tilt)
    dx, dy = math.sin(a), -math.cos(a)
    tip = (cx + dx * h, cy + dy * h)
    c.path([("M", (cx - w, cy)),
            ("C", (cx - w, cy + dy * h), (tip[0] - w * 0.4, tip[1]), tip),
            ("C", (tip[0] + w * 0.4, tip[1]), (cx + w, cy + dy * h), (cx + w, cy))],
           width=BOLD, closed=True)
    if inner:
        c.path([("M", (cx - w * 0.5, cy)),
                ("C", (cx - w * 0.5, cy + dy * h * 0.6),
                 (tip[0], tip[1] - dy * h * 0.3), tip),
                ("C", (tip[0], tip[1] - dy * h * 0.3),
                 (cx + w * 0.5, cy + dy * h * 0.6), (cx + w * 0.5, cy))],
               width=THIN)


# --------------------------------------------------------------------------
# BODIES / LIMBS
# --------------------------------------------------------------------------
def blob_body(c: Canvas, cx, cy, w, h):
    """A friendly rounded body (egg-ish)."""
    c.path([("M", (cx - w, cy)),
            ("C", (cx - w, cy + h * 1.2), (cx + w, cy + h * 1.2), (cx + w, cy)),
            ("C", (cx + w, cy - h), (cx - w, cy - h), (cx - w, cy))],
           width=BOLD, closed=True)


def paw(c: Canvas, cx, cy, r):
    c.ellipse(cx, cy, r, r * 0.8, width=MID)
    for d in (-1, 0, 1):
        c.line((cx + d * r * 0.45, cy + r * 0.5),
               (cx + d * r * 0.45, cy + r * 0.8), width=THIN)


def leg(c: Canvas, x, y0, y1, wdt=None):
    c.line((x, y0), (x, y1), width=BOLD)


def tail_curl(c: Canvas, x, y, r, dirn=1):
    c.arc(x, y, r, 0, 300 * dirn if dirn > 0 else -60, width=BOLD, segments=24)


# --------------------------------------------------------------------------
# NATURE / BACKGROUND MOTIFS (simple, uncluttered)
# --------------------------------------------------------------------------
def flower(c: Canvas, cx, cy, r, petals=5):
    c.circle(cx, cy, r * 0.35, width=MID)
    for k in range(petals):
        a = 360.0 * k / petals - 90
        rad = math.radians(a)
        px, py = cx + r * math.cos(rad), cy + r * math.sin(rad)
        c.circle(px, py, r * 0.42, width=MID)


def tulip(c: Canvas, cx, base_y, h):
    c.line((cx, base_y), (cx, base_y - h), width=MID)
    top = base_y - h
    c.polyline([(cx - h * 0.22, top), (cx - h * 0.22, top - h * 0.28),
                (cx, top - h * 0.14), (cx + h * 0.22, top - h * 0.28),
                (cx + h * 0.22, top)], width=MID, closed=True)
    leaf(c, cx, base_y - h * 0.4, h * 0.4, 1)


def leaf(c: Canvas, cx, cy, r, side=1):
    a = -90 + 50 * side
    c.petal(cx, cy, r, a, spread=34, width=MID)


def grass(c: Canvas, x0, x1, y, tufts=10):
    n = tufts
    for k in range(n):
        gx = x0 + (x1 - x0) * (k + 0.5) / n
        c.polyline([(gx - 6, y), (gx, y - 16), (gx + 6, y)], width=THIN)


def ground(c: Canvas, x0, x1, y):
    c.wavy(x0, y, x1, y, 5, 4, width=MID)


def butterfly(c: Canvas, cx, cy, r):
    c.ellipse(cx, cy, r * 0.12, r * 0.5, width=THIN)
    for s in (-1, 1):
        c.circle(cx + s * r * 0.5, cy - r * 0.25, r * 0.42, width=MID)
        c.circle(cx + s * r * 0.42, cy + r * 0.3, r * 0.32, width=MID)
    for s in (-1, 1):
        c.line((cx, cy - r * 0.5), (cx + s * r * 0.3, cy - r * 0.85), width=THIN)
        c.circle(cx + s * r * 0.3, cy - r * 0.85, 3, width=THIN)


def star(c: Canvas, cx, cy, r):
    c.star(cx, cy, r, r * 0.42, 5, rot_deg=-90, width=THIN)


def crescent_moon(c: Canvas, cx, cy, r):
    c.circle(cx, cy, r, width=MID)
    c.arc(cx + r * 0.5, cy - r * 0.1, r, 60, 300, width=MID)


def cloud(c: Canvas, cx, cy, r):
    c.arc(cx - r, cy, r * 0.6, 90, 270, width=MID)
    c.arc(cx - r * 0.4, cy - r * 0.4, r * 0.6, 130, 360, width=MID)
    c.arc(cx + r * 0.4, cy - r * 0.3, r * 0.55, 180, 400, width=MID)
    c.arc(cx + r, cy, r * 0.55, 270, 450, width=MID)
    c.line((cx - r, cy + r * 0.6), (cx + r, cy + r * 0.55), width=MID)


def sun(c: Canvas, cx, cy, r):
    c.circle(cx, cy, r, width=MID)
    for a in range(0, 360, 45):
        rad = math.radians(a)
        c.line((cx + r * 1.2 * math.cos(rad), cy + r * 1.2 * math.sin(rad)),
               (cx + r * 1.7 * math.cos(rad), cy + r * 1.7 * math.sin(rad)),
               width=THIN)


def water_waves(c: Canvas, x0, x1, y, rows=2):
    for r in range(rows):
        c.wavy(x0, y + r * 20, x1, y + r * 20, 7, 5, width=MID)


def bubbles(c: Canvas, cx, cy, count, spread):
    seq = [(0.0, 0.0, 1.0), (0.4, -0.3, 0.6), (-0.35, -0.5, 0.7),
           (0.2, -0.8, 0.5), (-0.15, -1.0, 0.4), (0.45, -1.2, 0.45)]
    for i in range(min(count, len(seq))):
        dx, dy, sc = seq[i]
        c.circle(cx + dx * spread, cy + dy * spread, spread * 0.14 * sc, width=THIN)


def small_fish(c: Canvas, cx, cy, r, flip=1):
    c.ellipse(cx, cy, r, r * 0.6, width=MID)
    c.polyline([(cx + flip * r, cy), (cx + flip * r * 1.5, cy - r * 0.5),
                (cx + flip * r * 1.5, cy + r * 0.5), (cx + flip * r, cy)], width=THIN)
    c.circle(cx - flip * r * 0.4, cy - r * 0.1, r * 0.12, width=THIN)


def starfish(c: Canvas, cx, cy, r):
    c.star(cx, cy, r, r * 0.45, 5, rot_deg=-90, width=MID)
    c.circle(cx, cy, r * 0.18, width=THIN)


def shell(c: Canvas, cx, cy, r):
    c.arc(cx, cy + r, r, 180, 360, width=MID)
    for a in (200, 230, 270, 310, 340):
        rad = math.radians(a)
        c.line((cx, cy + r), (cx + r * math.cos(rad), cy + r + r * math.sin(rad)),
               width=THIN)


def mushroom(c: Canvas, cx, base_y, r):
    c.arc(cx, base_y - r, r, 180, 360, width=MID)
    c.line((cx - r, base_y - r), (cx + r, base_y - r), width=MID)
    c.polyline([(cx - r * 0.4, base_y - r), (cx - r * 0.4, base_y),
                (cx + r * 0.4, base_y), (cx + r * 0.4, base_y - r)], width=MID)
    c.circle(cx - r * 0.35, base_y - r * 1.4, r * 0.16, width=THIN)
    c.circle(cx + r * 0.3, base_y - r * 1.5, r * 0.12, width=THIN)


def lily_pad(c: Canvas, cx, cy, r):
    c.arc(cx, cy, r, 30, 330, width=MID)
    c.line((cx + r * math.cos(math.radians(30)), cy + r * math.sin(math.radians(30))),
           (cx, cy), width=THIN)
    c.line((cx + r * math.cos(math.radians(330)), cy + r * math.sin(math.radians(330))),
           (cx, cy), width=THIN)


def tree_simple(c: Canvas, cx, base_y, h):
    c.polyline([(cx - 14, base_y), (cx - 10, base_y - h * 0.5),
                (cx + 10, base_y - h * 0.5), (cx + 14, base_y)], width=BOLD)
    c.circle(cx, base_y - h * 0.72, h * 0.32, width=BOLD)


def fence(c: Canvas, x0, x1, y, posts=5):
    c.line((x0, y - 26), (x1, y - 26), width=MID)
    c.line((x0, y - 46), (x1, y - 46), width=MID)
    for k in range(posts):
        px = x0 + (x1 - x0) * k / (posts - 1)
        c.polyline([(px, y), (px, y - 58), (px - 6, y - 66), (px + 6, y - 66),
                    (px, y - 58)], width=MID)
