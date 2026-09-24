"""
animals.py — 42 cute-animal coloring scenes (ages 4-10).

Each function draws ONE adorable animal (or a small related group) centered on
the page with a simple, uncluttered background, using the shared `kit` so the
whole book has a single consistent style. Signature: fn(c: Canvas).

The page frame + footer are added by build_book.py, so these draw only the art
inside a comfortable margin.
"""
from __future__ import annotations
import math
from artlib import Canvas
import kit as K
from kit import BOLD, MID, THIN


def _cxy(c):
    return c.w / 2, c.h / 2


# ---- shared head helpers ---------------------------------------------------
def _round_head(c, cx, cy, r):
    c.circle(cx, cy, r, width=BOLD)


# 1. Cute puppy sitting in a flower garden
def puppy_garden(c):
    cx, cy = c.w / 2, c.h * 0.44
    r = 92
    K.blob_body(c, cx, cy + r * 1.5, r * 0.9, r * 0.9)
    _round_head(c, cx, cy, r)
    # floppy ears
    c.ellipse(cx - r * 0.95, cy + r * 0.1, r * 0.34, r * 0.7, width=BOLD)
    c.ellipse(cx + r * 0.95, cy + r * 0.1, r * 0.34, r * 0.7, width=BOLD)
    K.eyes(c, cx, cy - r * 0.1, r * 0.7, r * 0.22)
    K.nose_muzzle(c, cx, cy + r * 0.4, r * 0.16)
    K.blush(c, cx, cy + r * 0.35, r * 1.3, r * 0.12)
    # front paws
    K.paw(c, cx - r * 0.45, cy + r * 2.2, r * 0.3)
    K.paw(c, cx + r * 0.45, cy + r * 2.2, r * 0.3)
    _flower_row(c)
    K.sun(c, c.w - 110, 120, 30)


# 2. Adorable kitten playing with butterflies
def kitten_butterflies(c):
    cx, cy = c.w / 2, c.h * 0.5
    r = 88
    K.blob_body(c, cx, cy + r * 1.4, r * 0.85, r * 0.85)
    _round_head(c, cx, cy, r)
    K.ear_pointy(c, (cx - r * 0.7, cy - r * 1.25), (cx - r * 1.0, cy - r * 0.55),
                 (cx - r * 0.35, cy - r * 0.7))
    K.ear_pointy(c, (cx + r * 0.7, cy - r * 1.25), (cx + r * 0.35, cy - r * 0.7),
                 (cx + r * 1.0, cy - r * 0.55))
    K.eyes(c, cx, cy - r * 0.05, r * 0.7, r * 0.22)
    c.polyline([(cx, cy + r * 0.25), (cx - r * 0.1, cy + r * 0.4),
                (cx + r * 0.1, cy + r * 0.4)], width=MID, closed=True)
    K.smile(c, cx, cy + r * 0.4, r * 0.35)
    for s in (-1, 1):  # whiskers
        for dy in (-1, 0, 1):
            c.line((cx + s * r * 0.3, cy + r * 0.4 + dy * 6),
                   (cx + s * r * 1.0, cy + r * 0.4 + dy * 12), width=THIN)
    K.tail_curl(c, cx + r * 1.1, cy + r * 1.6, r * 0.5, 1)
    K.butterfly(c, c.w * 0.28, c.h * 0.28, 46)
    K.butterfly(c, c.w * 0.75, c.h * 0.34, 40)


# 3. Happy bunny surrounded by spring flowers
def bunny_flowers(c):
    cx, cy = c.w / 2, c.h * 0.48
    r = 84
    K.blob_body(c, cx, cy + r * 1.5, r * 0.85, r * 0.9)
    _round_head(c, cx, cy, r)
    K.ear_long(c, cx - r * 0.4, cy - r * 0.9, r * 0.24, r * 1.1, tilt=-8)
    K.ear_long(c, cx + r * 0.4, cy - r * 0.9, r * 0.24, r * 1.1, tilt=8)
    K.eyes(c, cx, cy - r * 0.05, r * 0.7, r * 0.2)
    c.ellipse(cx, cy + r * 0.28, r * 0.1, r * 0.08, width=MID)
    K.smile(c, cx, cy + r * 0.45, r * 0.3)
    K.blush(c, cx, cy + r * 0.3, r * 1.3, r * 0.12)
    c.circle(cx, cy + r * 2.35, r * 0.22, width=MID)  # tail
    _flower_row(c)


# 4. Baby elephant holding a flower with its trunk
def elephant_flower(c):
    cx, cy = c.w / 2, c.h * 0.46
    r = 96
    K.blob_body(c, cx, cy + r * 1.4, r * 1.1, r)
    _round_head(c, cx, cy, r)
    c.ellipse(cx - r * 1.05, cy, r * 0.55, r * 0.8, width=BOLD)  # ears
    c.ellipse(cx + r * 1.05, cy, r * 0.55, r * 0.8, width=BOLD)
    K.eyes(c, cx, cy - r * 0.05, r * 0.7, r * 0.18)
    # trunk curling up holding a flower
    c.path([("M", (cx, cy + r * 0.3)),
            ("C", (cx + r * 0.1, cy + r * 1.1), (cx - r * 0.6, cy + r * 1.3),
             (cx - r * 0.5, cy + r * 0.7))], width=BOLD)
    K.flower(c, cx - r * 0.5, cy + r * 0.55, r * 0.28)
    # legs
    for s in (-0.5, 0.5):
        c.rounded_rect(cx + s * r * 0.9 - r * 0.2, cy + r * 2.1, r * 0.4, r * 0.5, 8, width=MID)
    K.ground(c, 70, c.w - 70, c.h - 90)


# 5. Cute panda eating bamboo
def panda_bamboo(c):
    cx, cy = c.w / 2, c.h * 0.46
    r = 92
    K.blob_body(c, cx, cy + r * 1.4, r * 0.95, r * 0.95)
    _round_head(c, cx, cy, r)
    K.ear_round(c, cx - r * 0.8, cy - r * 0.8, r * 0.34)
    K.ear_round(c, cx + r * 0.8, cy - r * 0.8, r * 0.34)
    for s in (-1, 1):  # eye patches
        c.ellipse(cx + s * r * 0.4, cy, r * 0.28, r * 0.36, width=MID)
    K.eyes(c, cx, cy, r * 0.8, r * 0.16)
    c.circle(cx, cy + r * 0.35, r * 0.12, width=MID)
    K.smile(c, cx, cy + r * 0.5, r * 0.28)
    # bamboo
    for bx in (cx + r * 1.3, cx + r * 1.55):
        c.line((bx, cy), (bx, c.h - 126), width=MID)
        for yy in range(int(cy), int(c.h - 126), 40):
            c.line((bx - 8, yy), (bx + 8, yy), width=THIN)
    K.leaf(c, cx + r * 1.3, cy - 10, 26, -1)


# 6. Baby deer resting among wildflowers
def deer_wildflowers(c):
    cx, cy = c.w / 2, c.h * 0.42
    r = 78
    # resting body (oval low)
    c.ellipse(cx, cy + r * 1.7, r * 1.5, r * 0.8, width=BOLD)
    _round_head(c, cx, cy, r)
    K.ear_long(c, cx - r * 0.7, cy - r * 0.4, r * 0.22, r * 0.7, tilt=-40)
    K.ear_long(c, cx + r * 0.7, cy - r * 0.4, r * 0.22, r * 0.7, tilt=40)
    K.eyes(c, cx, cy, r * 0.7, r * 0.2)
    c.ellipse(cx, cy + r * 0.35, r * 0.14, r * 0.1, width=MID)
    K.blush(c, cx, cy + r * 0.3, r * 1.2, r * 0.12)
    # spots
    for (dx, dy) in [(-0.5, 1.4), (0.3, 1.7), (0.7, 1.3), (-0.1, 1.9)]:
        c.circle(cx + dx * r, cy + dy * r, r * 0.1, width=THIN)
    _flower_row(c)


# 7. Little hedgehog carrying flowers
def hedgehog_flowers(c):
    cx, cy = c.w / 2, c.h * 0.5
    r = 96
    # spiky dome
    c.arc(cx, cy, r, 180, 360, width=BOLD)
    for a in range(190, 351, 12):
        rad = math.radians(a)
        c.line((cx + r * math.cos(rad), cy + r * math.sin(rad)),
               (cx + r * 1.25 * math.cos(rad), cy + r * 1.25 * math.sin(rad)),
               width=MID)
    # face
    c.path([("M", (cx - r * 0.2, cy)),
            ("C", (cx - r * 0.5, cy + r * 0.5), (cx - r * 0.2, cy + r * 0.7),
             (cx + r * 0.1, cy + r * 0.6)),
            ("C", (cx + r * 0.3, cy + r * 0.5), (cx + r * 0.3, cy), (cx + r * 0.1, cy))],
           width=BOLD)
    c.circle(cx - r * 0.35, cy + r * 0.55, r * 0.07, width=MID)  # nose
    K.eyes(c, cx - r * 0.02, cy + r * 0.25, r * 0.3, r * 0.1)
    c.line((cx - r, cy), (cx + r, cy), width=MID)
    K.flower(c, cx + r * 0.6, cy - r * 0.2, r * 0.3)
    K.flower(c, cx - r * 0.7, cy - r * 0.35, r * 0.26)
    K.grass(c, 90, c.w - 90, c.h - 122, 12)


# 8. Friendly owl on a branch under stars
def owl_branch(c):
    cx, cy = c.w / 2, c.h * 0.46
    r = 90
    K.blob_body(c, cx, cy + r * 0.5, r, r * 1.2)
    K.ear_pointy(c, (cx - r * 0.75, cy - r * 1.15), (cx - r * 0.95, cy - r * 0.5),
                 (cx - r * 0.4, cy - r * 0.7))
    K.ear_pointy(c, (cx + r * 0.75, cy - r * 1.15), (cx + r * 0.4, cy - r * 0.7),
                 (cx + r * 0.95, cy - r * 0.5))
    for s in (-1, 1):
        c.circle(cx + s * r * 0.42, cy - r * 0.35, r * 0.36, width=MID)
        c.circle(cx + s * r * 0.42, cy - r * 0.35, r * 0.16, width=THIN)
    c.polyline([(cx, cy - r * 0.2), (cx - r * 0.1, cy), (cx + r * 0.1, cy)],
               width=MID, closed=True)
    for row in range(3):
        yy = cy + r * (0.4 + row * 0.4)
        for k in range(4 + row):
            fx = cx - r * 0.7 + (1.4 * r) * k / (3 + row)
            c.arc(fx, yy, r * 0.16, 180, 360, width=THIN)
    c.line((cx - r * 1.4, cy + r * 1.7), (cx + r * 1.4, cy + r * 1.7), width=BOLD)
    for s in (-1, 1):
        c.line((cx + s * r * 0.3, cy + r * 1.55), (cx + s * r * 0.3, cy + r * 1.7), width=MID)
    for (sx, sy) in [(0.2, 0.16), (0.8, 0.2), (0.15, 0.4), (0.85, 0.42), (0.5, 0.1)]:
        K.star(c, c.w * sx, c.h * sy, 12)
    K.crescent_moon(c, c.w - 110, 120, 34)


# 9. Cute fox sleeping beneath a crescent moon
def fox_sleeping(c):
    cx, cy = c.w / 2, c.h * 0.52
    r = 84
    c.ellipse(cx, cy + r * 0.6, r * 1.6, r * 0.7, width=BOLD)  # curled body
    _round_head(c, cx - r * 0.8, cy, r * 0.8)
    K.ear_pointy(c, (cx - r * 1.4, cy - r * 0.9), (cx - r * 1.3, cy - r * 0.35),
                 (cx - r * 0.9, cy - r * 0.5))
    K.ear_pointy(c, (cx - r * 0.4, cy - r * 0.95), (cx - r * 0.6, cy - r * 0.5),
                 (cx - r * 0.15, cy - r * 0.4))
    K.eyes(c, cx - r * 0.8, cy - r * 0.05, r * 0.55, r * 0.16, style="closed")
    c.circle(cx - r * 1.55, cy + r * 0.1, r * 0.1, width=MID)  # nose
    # big tail curling over
    c.path([("M", (cx + r * 1.4, cy + r * 0.4)),
            ("C", (cx + r * 2.0, cy - r * 0.6), (cx + r * 0.3, cy - r * 0.9),
             (cx - r * 0.2, cy - r * 0.3))], width=BOLD)
    c.arc(cx + r * 1.4, cy + r * 0.3, r * 0.4, 0, 200, width=THIN)
    K.crescent_moon(c, c.w * 0.5, c.h * 0.2, 40)
    for (sx, sy) in [(0.25, 0.18), (0.7, 0.16), (0.8, 0.3)]:
        K.star(c, c.w * sx, c.h * sy, 10)


# 10. Happy turtle swimming with little tropical fish
def turtle_fish(c):
    cx, cy = c.w / 2, c.h * 0.5
    r = 96
    c.ellipse(cx, cy, r, r * 0.75, width=BOLD)  # shell
    c.ellipse(cx, cy, r * 0.7, r * 0.5, width=MID)
    for a in range(0, 360, 60):
        rad = math.radians(a)
        c.line((cx + r * 0.2 * math.cos(rad), cy + r * 0.15 * math.sin(rad)),
               (cx + r * 0.7 * math.cos(rad), cy + r * 0.5 * math.sin(rad)), width=THIN)
    _round_head(c, cx - r * 1.1, cy + r * 0.1, r * 0.4)
    K.eyes(c, cx - r * 1.1, cy, r * 0.3, r * 0.1)
    K.smile(c, cx - r * 1.1, cy + r * 0.15, r * 0.2)
    for (dx, dy) in [(-0.7, 0.7), (0.7, 0.7), (0.9, -0.5)]:
        c.ellipse(cx + dx * r, cy + dy * r * 0.7, r * 0.28, r * 0.18, width=MID)
    K.small_fish(c, c.w * 0.24, c.h * 0.3, 26)
    K.small_fish(c, c.w * 0.78, c.h * 0.32, 22, flip=-1)
    K.water_waves(c, 70, c.w - 70, c.h * 0.16, 2)
    K.bubbles(c, c.w * 0.7, c.h * 0.6, 5, 60)


# 11. Baby llama in a mountain meadow
def llama_meadow(c):
    cx = c.w / 2
    # background mountains (drawn first, sit behind the llama, up near the top)
    c.polyline([(70, c.h * 0.3), (c.w * 0.3, c.h * 0.16), (c.w * 0.52, c.h * 0.3)], width=MID)
    c.polyline([(c.w * 0.48, c.h * 0.3), (c.w * 0.72, c.h * 0.14), (c.w - 70, c.h * 0.3)], width=MID)
    K.sun(c, c.w - 110, c.h * 0.16, 26)
    # llama built bottom-up: body, neck, head
    body_cy = c.h * 0.62
    r = 66
    c.rounded_rect(cx - r * 0.85, body_cy - r, r * 1.7, r * 2.0, 28, width=BOLD)  # body
    # neck rises from top of body
    neck_top = body_cy - r - r * 1.5
    c.rounded_rect(cx - r * 0.42, neck_top, r * 0.84, r * 1.7, 20, width=BOLD)   # neck
    # head sits on top of neck
    hcy = neck_top - r * 0.5
    _round_head(c, cx, hcy, r * 0.55)
    K.ear_long(c, cx - r * 0.28, hcy - r * 0.55, r * 0.12, r * 0.5, tilt=-14)
    K.ear_long(c, cx + r * 0.28, hcy - r * 0.55, r * 0.12, r * 0.5, tilt=14)
    K.eyes(c, cx, hcy - r * 0.02, r * 0.42, r * 0.13)
    c.ellipse(cx, hcy + r * 0.28, r * 0.16, r * 0.12, width=MID)
    K.smile(c, cx, hcy + r * 0.42, r * 0.18)
    K.blush(c, cx, hcy + r * 0.25, r * 1.0, r * 0.1)
    # legs
    for s in (-0.5, 0.5):
        c.line((cx + s * r * 0.9, body_cy + r), (cx + s * r * 0.9, body_cy + r + r * 0.6), width=BOLD)
    K.grass(c, 80, c.w - 80, c.h - 122, 12)


# 12. Cute koala hugging a eucalyptus tree
def koala_tree(c):
    tx = c.w / 2
    c.rounded_rect(tx - 26, c.h * 0.2, 52, c.h * 0.62, 12, width=BOLD)  # trunk
    cy = c.h * 0.5
    r = 78
    K.blob_body(c, tx, cy + r * 0.6, r * 0.8, r)
    _round_head(c, tx, cy, r)
    K.ear_round(c, tx - r * 0.9, cy - r * 0.4, r * 0.42)
    K.ear_round(c, tx + r * 0.9, cy - r * 0.4, r * 0.42)
    K.eyes(c, tx, cy - r * 0.05, r * 0.7, r * 0.2)
    c.ellipse(tx, cy + r * 0.35, r * 0.28, r * 0.34, width=MID)  # big nose
    # arms hugging
    for s in (-1, 1):
        c.arc(tx + s * r * 0.9, cy + r * 0.9, r * 0.5, 90 if s < 0 else 90, 270, width=BOLD)
    K.leaf(c, tx - 50, c.h * 0.26, 30, -1)
    K.leaf(c, tx + 50, c.h * 0.3, 30, 1)


# 13. Baby lion among savanna flowers
def lion_savanna(c):
    cx, cy = c.w / 2, c.h * 0.44
    r = 74
    K.blob_body(c, cx, cy + r * 1.6, r, r)
    # mane
    for a in range(0, 360, 24):
        rad = math.radians(a)
        c.circle(cx + r * 1.15 * math.cos(rad), cy + r * 1.15 * math.sin(rad),
                 r * 0.3, width=MID)
    _round_head(c, cx, cy, r)
    K.ear_round(c, cx - r * 0.75, cy - r * 0.75, r * 0.24)
    K.ear_round(c, cx + r * 0.75, cy - r * 0.75, r * 0.24)
    K.eyes(c, cx, cy - r * 0.05, r * 0.65, r * 0.2)
    c.polyline([(cx, cy + r * 0.3), (cx - r * 0.12, cy + r * 0.45),
                (cx + r * 0.12, cy + r * 0.45)], width=MID, closed=True)
    K.smile(c, cx, cy + r * 0.45, r * 0.3)
    _flower_row(c)
    K.sun(c, c.w - 110, 120, 30)


# 14. Happy monkey holding a banana
def monkey_banana(c):
    cx, cy = c.w / 2, c.h * 0.44
    r = 82
    K.blob_body(c, cx, cy + r * 1.5, r * 0.9, r)
    _round_head(c, cx, cy, r)
    K.ear_round(c, cx - r * 1.0, cy, r * 0.32)
    K.ear_round(c, cx + r * 1.0, cy, r * 0.32)
    c.ellipse(cx, cy + r * 0.25, r * 0.7, r * 0.6, width=MID)  # face patch
    K.eyes(c, cx, cy - r * 0.1, r * 0.6, r * 0.2)
    c.circle(cx, cy + r * 0.25, r * 0.08, width=MID)
    K.smile(c, cx, cy + r * 0.4, r * 0.3)
    # arm + banana
    c.arc(cx + r * 0.8, cy + r * 1.4, r * 0.6, 200, 20, width=BOLD)
    c.path([("M", (cx + r * 1.3, cy + r * 1.0)),
            ("C", (cx + r * 1.8, cy + r * 0.6), (cx + r * 1.9, cy + r * 1.4),
             (cx + r * 1.4, cy + r * 1.5))], width=MID, closed=True)
    K.tail_curl(c, cx - r * 1.2, cy + r * 1.8, r * 0.6, -1)


# 15. Cute giraffe surrounded by butterflies
def giraffe_butterflies(c):
    cx = c.w / 2
    r = 60
    c.rounded_rect(cx - r * 0.6, c.h * 0.55, r * 1.2, r * 1.6, 22, width=BOLD)  # body
    c.rounded_rect(cx - r * 0.4, c.h * 0.28, r * 0.8, c.h * 0.3, 16, width=BOLD)  # neck
    cy = c.h * 0.24
    _round_head(c, cx, cy, r * 0.6)
    K.ear_long(c, cx - r * 0.55, cy - r * 0.4, r * 0.14, r * 0.4, tilt=-40)
    K.ear_long(c, cx + r * 0.55, cy - r * 0.4, r * 0.14, r * 0.4, tilt=40)
    for s in (-1, 1):  # ossicones
        c.line((cx + s * r * 0.2, cy - r * 0.55), (cx + s * r * 0.2, cy - r * 0.85), width=MID)
        c.circle(cx + s * r * 0.2, cy - r * 0.9, r * 0.1, width=MID)
    K.eyes(c, cx, cy - r * 0.05, r * 0.4, r * 0.12)
    K.smile(c, cx, cy + r * 0.2, r * 0.16)
    # spots
    for (dx, dy) in [(-0.3, 0.7), (0.3, 0.9), (0.0, 1.2), (-0.35, 1.4), (0.35, 1.6)]:
        c.circle(cx + dx * r, c.h * 0.55 + dy * r, r * 0.16, width=THIN)
    for s in (-0.4, 0.4):
        c.line((cx + s * r, c.h * 0.55 + r * 1.6), (cx + s * r, c.h * 0.55 + r * 2.1), width=BOLD)
    K.butterfly(c, c.w * 0.26, c.h * 0.3, 40)
    K.butterfly(c, c.w * 0.74, c.h * 0.38, 36)


# 16. Baby zebra in a grassy field
def zebra_field(c):
    cx, cy = c.w / 2, c.h * 0.46
    r = 78
    K.blob_body(c, cx, cy + r * 1.3, r * 1.1, r * 0.9)
    _round_head(c, cx, cy, r * 0.85)
    K.ear_pointy(c, (cx - r * 0.55, cy - r * 1.15), (cx - r * 0.7, cy - r * 0.6),
                 (cx - r * 0.3, cy - r * 0.7))
    K.ear_pointy(c, (cx + r * 0.55, cy - r * 1.15), (cx + r * 0.3, cy - r * 0.7),
                 (cx + r * 0.7, cy - r * 0.6))
    K.eyes(c, cx, cy - r * 0.05, r * 0.6, r * 0.18)
    c.ellipse(cx, cy + r * 0.35, r * 0.16, r * 0.1, width=MID)
    K.smile(c, cx, cy + r * 0.5, r * 0.24)
    # stripes on body
    for k in range(5):
        xx = cx - r * 0.8 + k * r * 0.4
        c.arc(xx, cy + r * 1.3, r * 0.9, 250, 290, width=THIN)
    for s in (-0.5, 0.5):
        c.line((cx + s * r, cy + r * 2.1), (cx + s * r, cy + r * 2.6), width=BOLD)
    K.grass(c, 80, c.w - 80, c.h - 122, 12)


# 17. Adorable hippo playing beside a pond
def hippo_pond(c):
    cx, cy = c.w / 2, c.h * 0.42
    r = 96
    K.blob_body(c, cx, cy + r * 1.3, r * 1.15, r)
    c.ellipse(cx, cy + r * 0.2, r, r * 0.8, width=BOLD)  # big snout head
    K.ear_round(c, cx - r * 0.75, cy - r * 0.55, r * 0.2)
    K.ear_round(c, cx + r * 0.75, cy - r * 0.55, r * 0.2)
    K.eyes(c, cx, cy - r * 0.25, r * 0.7, r * 0.16)
    for s in (-1, 1):
        c.circle(cx + s * r * 0.3, cy + r * 0.45, r * 0.1, width=MID)  # nostrils
    K.smile(c, cx, cy + r * 0.55, r * 0.4)
    K.water_waves(c, 70, c.w - 70, c.h * 0.72, 2)
    K.lily_pad(c, c.w * 0.75, c.h * 0.68, 40)


# 18. Happy crocodile wearing a flower crown
def croc_crown(c):
    cx, cy = c.w / 2, c.h * 0.5
    r = 70
    c.ellipse(cx, cy, r * 1.7, r * 0.7, width=BOLD)  # body
    # long snout
    c.path([("M", (cx - r * 1.6, cy)),
            ("C", (cx - r * 3.0, cy - r * 0.3), (cx - r * 3.0, cy + r * 0.5),
             (cx - r * 1.6, cy + r * 0.4))], width=BOLD, closed=True)
    for k in range(6):  # teeth
        tx = cx - r * 2.7 + k * r * 0.25
        c.polyline([(tx, cy + r * 0.15), (tx + r * 0.1, cy - r * 0.05),
                    (tx + r * 0.2, cy + r * 0.15)], width=THIN)
    c.circle(cx - r * 1.2, cy - r * 0.4, r * 0.22, width=MID)
    c.circle(cx - r * 1.2, cy - r * 0.4, r * 0.1, width=THIN)
    # flower crown
    for k in range(5):
        K.flower(c, cx - r * 1.5 + k * r * 0.6, cy - r * 0.75, r * 0.18)
    for (dx) in (-0.6, 0.2, 0.9):
        c.polyline([(cx + dx * r, cy + r * 0.6), (cx + dx * r, cy + r), 
                    (cx + dx * r + r * 0.2, cy + r)], width=MID)  # legs
    K.tail_curl(c, cx + r * 1.6, cy, r * 0.5, 1)


# 19. Cute penguin holding a snowflake
def penguin_snowflake(c):
    cx, cy = c.w / 2, c.h * 0.46
    r = 92
    K.blob_body(c, cx, cy + r * 0.4, r * 0.85, r * 1.2)
    c.path([("M", (cx - r * 0.55, cy)),  # belly
            ("C", (cx - r * 0.55, cy + r * 1.3), (cx + r * 0.55, cy + r * 1.3),
             (cx + r * 0.55, cy))], width=MID)
    K.eyes(c, cx, cy - r * 0.35, r * 0.5, r * 0.16)
    c.polyline([(cx, cy - r * 0.15), (cx - r * 0.12, cy), (cx + r * 0.12, cy)],
               width=MID, closed=True)
    for s in (-1, 1):  # flippers
        c.ellipse(cx + s * r * 0.9, cy + r * 0.4, r * 0.2, r * 0.55, width=BOLD)
    for s in (-1, 1):  # feet
        c.ellipse(cx + s * r * 0.35, cy + r * 1.55, r * 0.22, r * 0.12, width=MID)
    _snowflake(c, c.w * 0.72, c.h * 0.3, 42)
    _snowflake(c, c.w * 0.25, c.h * 0.24, 30)


def _snowflake(c, cx, cy, r):
    for a in range(0, 360, 60):
        rad = math.radians(a)
        ex, ey = cx + r * math.cos(rad), cy + r * math.sin(rad)
        c.line((cx, cy), (ex, ey), width=THIN)
        for t in (0.5, 0.75):
            bx, by = cx + r * t * math.cos(rad), cy + r * t * math.sin(rad)
            c.line((bx, by), (bx + r * 0.18 * math.cos(rad + 0.9),
                              by + r * 0.18 * math.sin(rad + 0.9)), width=THIN)
            c.line((bx, by), (bx + r * 0.18 * math.cos(rad - 0.9),
                              by + r * 0.18 * math.sin(rad - 0.9)), width=THIN)


# 20. Baby polar bear playing in soft snow
def polar_bear_snow(c):
    cx, cy = c.w / 2, c.h * 0.44
    r = 90
    K.blob_body(c, cx, cy + r * 1.4, r, r)
    _round_head(c, cx, cy, r)
    K.ear_round(c, cx - r * 0.7, cy - r * 0.8, r * 0.28, inner=False)
    K.ear_round(c, cx + r * 0.7, cy - r * 0.8, r * 0.28, inner=False)
    K.eyes(c, cx, cy - r * 0.05, r * 0.6, r * 0.18)
    c.ellipse(cx, cy + r * 0.3, r * 0.4, r * 0.34, width=MID)
    c.circle(cx, cy + r * 0.18, r * 0.1, width=MID)
    K.smile(c, cx, cy + r * 0.4, r * 0.26)
    K.paw(c, cx - r * 0.5, cy + r * 2.2, r * 0.3)
    K.paw(c, cx + r * 0.5, cy + r * 2.2, r * 0.3)
    for (sx, sy) in [(0.2, 0.2), (0.8, 0.24), (0.15, 0.5), (0.85, 0.5), (0.3, 0.14)]:
        _snowflake(c, c.w * sx, c.h * sy, 18)
    K.ground(c, 70, c.w - 70, c.h - 122)


# 21. Friendly dolphin jumping above ocean waves
def dolphin_jump(c):
    cx, cy = c.w / 2, c.h * 0.44
    r = 70
    c.path([("M", (cx - r * 2, cy + r)),
            ("C", (cx - r * 1.5, cy - r * 1.5), (cx + r * 1.5, cy - r * 1.5),
             (cx + r * 2, cy + r * 0.2))], width=BOLD)  # arched back
    c.path([("M", (cx - r * 2, cy + r)),
            ("C", (cx - r * 1.2, cy - r * 0.4), (cx + r * 1.2, cy - r * 0.3),
             (cx + r * 2, cy + r * 0.2))], width=BOLD)  # belly
    # snout
    c.polyline([(cx - r * 2, cy + r), (cx - r * 2.6, cy + r * 1.2),
                (cx - r * 1.7, cy + r * 1.05)], width=MID)
    K.eyes(c, cx - r * 1.3, cy + r * 0.2, 0, r * 0.14)
    c.polyline([(cx - r * 0.2, cy - r * 1.2), (cx + r * 0.3, cy - r * 1.7),
                (cx + r * 0.2, cy - r * 1.1)], width=MID)  # dorsal fin
    c.polyline([(cx + r * 2, cy + r * 0.2), (cx + r * 2.6, cy - r * 0.3),
                (cx + r * 2.5, cy + r * 0.6), (cx + r * 2, cy + r * 0.2)], width=MID)  # tail
    K.water_waves(c, 60, c.w - 60, c.h * 0.66, 2)


# 22. Cute whale swimming with small fish and bubbles
def whale_bubbles(c):
    cx, cy = c.w / 2, c.h * 0.5
    r = 110
    c.path([("M", (cx - r * 1.3, cy)),
            ("C", (cx - r * 1.3, cy + r * 0.9), (cx + r, cy + r * 0.9),
             (cx + r, cy)),
            ("C", (cx + r, cy - r * 0.7), (cx - r * 1.3, cy - r * 0.7),
             (cx - r * 1.3, cy))], width=BOLD, closed=True)
    c.polyline([(cx + r, cy), (cx + r * 1.5, cy - r * 0.5),
                (cx + r * 1.4, cy), (cx + r * 1.5, cy + r * 0.5),
                (cx + r, cy)], width=MID)  # tail
    K.eyes(c, cx - r * 0.75, cy - r * 0.05, r * 0.35, r * 0.13)
    K.smile(c, cx - r * 0.6, cy + r * 0.2, r * 0.3)
    c.path([("M", (cx - r * 0.4, cy - r * 0.6)),
            ("C", (cx - r * 0.5, cy - r), (cx - r * 0.2, cy - r), 
             (cx - r * 0.3, cy - r * 0.6))], width=MID)  # spout base
    K.bubbles(c, cx - r * 0.35, cy - r * 1.0, 5, 60)
    K.small_fish(c, c.w * 0.8, c.h * 0.34, 22, flip=-1)
    K.small_fish(c, c.w * 0.78, c.h * 0.66, 20, flip=-1)
    K.water_waves(c, 60, c.w - 60, c.h * 0.16, 2)


# 23. Baby seal resting beside seashells
def seal_shells(c):
    cx, cy = c.w / 2, c.h * 0.46
    c.ellipse(cx, cy + 30, 130, 78, width=BOLD)  # body
    _round_head(c, cx - 70, cy - 40, 56)
    K.eyes(c, cx - 70, cy - 44, 44, 16)
    c.ellipse(cx - 70, cy - 20, 12, 9, width=MID)
    for s in (-1, 1):
        for dy in (-4, 4):
            c.line((cx - 60, cy - 16 + dy), (cx - 20, cy - 10 + dy * 1.5), width=THIN)
    c.polyline([(cx + 120, cy + 30), (cx + 175, cy + 5),
                (cx + 175, cy + 60)], width=MID, closed=True)  # tail flippers
    K.shell(c, c.w * 0.28, c.h * 0.66, 28)
    K.shell(c, c.w * 0.7, c.h * 0.68, 24)
    K.starfish(c, c.w * 0.6, c.h * 0.72, 22)
    K.ground(c, 60, c.w - 60, c.h - 122)


# 24. Happy octopus surrounded by bubbles and starfish
def octopus_bubbles(c):
    cx, cy = c.w / 2, c.h * 0.4
    r = 96
    c.arc(cx, cy, r, 180, 360, width=BOLD)  # head dome
    K.eyes(c, cx, cy - r * 0.1, r * 0.7, r * 0.22)
    K.smile(c, cx, cy + r * 0.25, r * 0.3)
    K.blush(c, cx, cy + r * 0.15, r * 1.3, r * 0.12)
    for k in range(8):  # tentacles
        tx = cx - r * 0.9 + (1.8 * r) * k / 7
        dirn = 1 if k % 2 == 0 else -1
        c.path([("M", (tx, cy)),
                ("C", (tx + dirn * 20, cy + r * 0.7), (tx - dirn * 24, cy + r * 1.1),
                 (tx + dirn * 14, cy + r * 1.5))], width=MID)
    K.bubbles(c, c.w * 0.75, c.h * 0.4, 5, 60)
    K.bubbles(c, c.w * 0.2, c.h * 0.4, 4, 50)
    K.starfish(c, c.w * 0.5, c.h * 0.86, 30)
    K.water_waves(c, 60, c.w - 60, c.h * 0.14, 2)


# 25. Cute seahorse swimming through coral
def seahorse_coral(c):
    cx, cy = c.w * 0.46, c.h * 0.46
    c.path([("M", (cx, cy - 120)),  # head + body S-curve
            ("C", (cx + 70, cy - 90), (cx + 40, cy - 10), (cx - 10, cy + 30)),
            ("C", (cx - 60, cy + 70), (cx - 30, cy + 140), (cx + 30, cy + 130))],
           width=BOLD)
    c.path([("M", (cx - 20, cy - 120)),
            ("C", (cx + 40, cy - 130), (cx + 10, cy - 30), (cx - 40, cy + 20)),
            ("C", (cx - 90, cy + 70), (cx - 60, cy + 160), (cx + 20, cy + 150))],
           width=BOLD)
    c.polyline([(cx - 20, cy - 120), (cx - 60, cy - 150),
                (cx - 10, cy - 140)], width=MID)  # snout
    K.eyes(c, cx + 8, cy - 108, 0, 12)
    for i in range(6):  # dorsal fin ridges
        yy = cy - 90 + i * 30
        c.line((cx + 30, yy), (cx + 46, yy - 6), width=THIN)
    # coral
    _coral(c, c.w * 0.78, c.h - 122, 70)
    _coral(c, c.w * 0.2, c.h - 122, 56)
    K.bubbles(c, c.w * 0.7, c.h * 0.3, 4, 50)


def _coral(c, cx, base_y, h):
    c.path([("M", (cx, base_y)), ("C", (cx, base_y - h * 0.6),
            (cx - h * 0.4, base_y - h * 0.5), (cx - h * 0.4, base_y - h))], width=MID)
    c.path([("M", (cx, base_y)), ("C", (cx, base_y - h * 0.5),
            (cx + h * 0.4, base_y - h * 0.5), (cx + h * 0.45, base_y - h * 1.1))], width=MID)
    c.path([("M", (cx, base_y)), ("L", (cx, base_y - h * 0.9))], width=MID)


# 26. Baby duck splashing in a small pond
def duck_pond(c):
    cx, cy = c.w / 2, c.h * 0.44
    r = 78
    K.blob_body(c, cx, cy + r * 0.6, r * 0.95, r)
    _round_head(c, cx + r * 0.6, cy - r * 0.5, r * 0.55)
    c.polyline([(cx + r * 1.15, cy - r * 0.55), (cx + r * 1.6, cy - r * 0.4),
                (cx + r * 1.15, cy - r * 0.25)], width=MID, closed=True)  # bill
    K.eyes(c, cx + r * 0.7, cy - r * 0.65, 0, r * 0.13)
    c.arc(cx - r * 0.4, cy + r * 0.5, r * 0.5, 200, 340, width=MID)  # wing
    K.water_waves(c, 60, c.w - 60, c.h * 0.62, 2)
    K.bubbles(c, c.w * 0.3, c.h * 0.5, 4, 44)


# 27. Cute chick among spring flowers
def chick_flowers(c):
    cx, cy = c.w / 2, c.h * 0.46
    r = 90
    c.circle(cx, cy + r * 0.7, r * 0.85, width=BOLD)  # body
    _round_head(c, cx, cy - r * 0.4, r * 0.6)
    c.polyline([(cx, cy - r * 0.9), (cx - 8, cy - r * 1.15), (cx + 8, cy - r * 1.15)], width=THIN)  # tuft
    c.line((cx, cy - r * 1.15), (cx, cy - r * 1.25), width=THIN)
    K.eyes(c, cx, cy - r * 0.45, r * 0.4, r * 0.15)
    c.polyline([(cx, cy - r * 0.2), (cx - r * 0.14, cy - r * 0.05),
                (cx + r * 0.14, cy - r * 0.05)], width=MID, closed=True)  # beak
    for s in (-1, 1):
        c.arc(cx + s * r * 0.75, cy + r * 0.7, r * 0.4, 300, 60, width=MID)  # wings
    for s in (-1, 1):
        c.polyline([(cx + s * r * 0.25, cy + r * 1.5), (cx + s * r * 0.25, cy + r * 1.75)], width=MID)
        for d in (-1, 0, 1):
            c.line((cx + s * r * 0.25, cy + r * 1.75), (cx + s * r * 0.25 + d * 8, cy + r * 1.9), width=THIN)
    _flower_row(c)


# 28. Happy lamb resting in a meadow
def lamb_meadow(c):
    cx, cy = c.w / 2, c.h * 0.46
    r = 88
    # fluffy body
    for a in range(0, 360, 30):
        rad = math.radians(a)
        c.circle(cx + r * math.cos(rad), cy + r * 0.6 + r * 0.7 * math.sin(rad),
                 r * 0.3, width=MID)
    _round_head(c, cx, cy - r * 0.2, r * 0.5)
    K.ear_long(c, cx - r * 0.5, cy - r * 0.2, r * 0.16, r * 0.4, tilt=-70)
    K.ear_long(c, cx + r * 0.5, cy - r * 0.2, r * 0.16, r * 0.4, tilt=70)
    for a in range(160, 381, 40):  # wool tuft on head
        rad = math.radians(a)
        c.circle(cx + r * 0.35 * math.cos(rad), cy - r * 0.55 + r * 0.25 * math.sin(rad), r * 0.13, width=THIN)
    K.eyes(c, cx, cy - r * 0.2, r * 0.35, r * 0.12)
    K.smile(c, cx, cy, r * 0.16)
    for s in (-0.4, 0.4):
        c.line((cx + s * r, cy + r * 1.3), (cx + s * r, cy + r * 1.7), width=BOLD)
    K.grass(c, 80, c.w - 80, c.h - 122, 12)


# 29. Baby goat beside a country fence
def goat_fence(c):
    cx, cy = c.w * 0.42, c.h * 0.5
    r = 74
    K.blob_body(c, cx, cy + r * 1.1, r * 0.95, r * 0.85)
    _round_head(c, cx, cy, r * 0.75)
    for s in (-1, 1):  # small horns
        c.arc(cx + s * r * 0.4, cy - r * 0.7, r * 0.3, 250 if s < 0 else 250, 290, width=MID)
    K.ear_long(c, cx - r * 0.7, cy - r * 0.2, r * 0.15, r * 0.4, tilt=-70)
    K.ear_long(c, cx + r * 0.7, cy - r * 0.2, r * 0.15, r * 0.4, tilt=70)
    K.eyes(c, cx, cy - r * 0.05, r * 0.55, r * 0.16)
    c.ellipse(cx, cy + r * 0.35, r * 0.16, r * 0.1, width=MID)
    c.line((cx, cy + r * 0.45), (cx, cy + r * 0.7), width=THIN)  # beard
    for s in (-0.5, 0.5):
        c.line((cx + s * r * 0.9, cy + r * 1.9), (cx + s * r * 0.9, cy + r * 2.3), width=BOLD)
    K.fence(c, c.w * 0.55, c.w - 70, c.h - 90, 4)
    K.grass(c, 70, c.w - 70, c.h - 90, 10)


# 30. Cute piglet playing among daisies
def piglet_daisies(c):
    cx, cy = c.w / 2, c.h * 0.46
    r = 90
    K.blob_body(c, cx, cy + r * 1.4, r, r * 0.95)
    _round_head(c, cx, cy, r)
    K.ear_pointy(c, (cx - r * 0.85, cy - r * 1.05), (cx - r * 0.95, cy - r * 0.55),
                 (cx - r * 0.45, cy - r * 0.7))
    K.ear_pointy(c, (cx + r * 0.85, cy - r * 1.05), (cx + r * 0.45, cy - r * 0.7),
                 (cx + r * 0.95, cy - r * 0.55))
    K.eyes(c, cx, cy - r * 0.1, r * 0.7, r * 0.18)
    c.ellipse(cx, cy + r * 0.35, r * 0.3, r * 0.22, width=MID)  # snout
    for s in (-1, 1):
        c.circle(cx + s * r * 0.1, cy + r * 0.35, r * 0.05, width=THIN)
    K.smile(c, cx, cy + r * 0.55, r * 0.24)
    K.tail_curl(c, cx + r * 1.1, cy + r * 1.6, r * 0.24, 1)
    _flower_row(c)


# 31. Happy calf in a flower-filled farm field
def calf_field(c):
    cx, cy = c.w / 2, c.h * 0.44
    r = 82
    K.blob_body(c, cx, cy + r * 1.4, r * 1.1, r)
    _round_head(c, cx, cy, r * 0.9)
    K.ear_long(c, cx - r * 0.85, cy - r * 0.3, r * 0.2, r * 0.5, tilt=-70)
    K.ear_long(c, cx + r * 0.85, cy - r * 0.3, r * 0.2, r * 0.5, tilt=70)
    for s in (-1, 1):  # tiny horn buds
        c.circle(cx + s * r * 0.3, cy - r * 0.85, r * 0.1, width=MID)
    K.eyes(c, cx, cy - r * 0.05, r * 0.6, r * 0.18)
    c.ellipse(cx, cy + r * 0.4, r * 0.34, r * 0.24, width=MID)  # muzzle
    for s in (-1, 1):
        c.circle(cx + s * r * 0.12, cy + r * 0.4, r * 0.05, width=THIN)
    # spots
    c.circle(cx - r * 0.5, cy + r * 1.5, r * 0.25, width=THIN)
    c.circle(cx + r * 0.5, cy + r * 1.7, r * 0.2, width=THIN)
    for s in (-0.5, 0.5):
        c.line((cx + s * r, cy + r * 2.2), (cx + s * r, cy + r * 2.6), width=BOLD)
    _flower_row(c)


# 32. Cute horse surrounded by countryside flowers
def horse_flowers(c):
    cx, cy = c.w / 2, c.h * 0.44
    r = 80
    K.blob_body(c, cx, cy + r * 1.4, r * 1.05, r)
    _round_head(c, cx, cy, r * 0.85)
    K.ear_pointy(c, (cx - r * 0.5, cy - r * 1.2), (cx - r * 0.65, cy - r * 0.65),
                 (cx - r * 0.25, cy - r * 0.7))
    K.ear_pointy(c, (cx + r * 0.5, cy - r * 1.2), (cx + r * 0.25, cy - r * 0.7),
                 (cx + r * 0.65, cy - r * 0.65))
    # mane
    c.wavy(cx - r * 0.6, cy - r * 0.9, cx - r * 0.2, cy + r * 0.8, 10, 4, width=MID)
    K.eyes(c, cx, cy - r * 0.05, r * 0.6, r * 0.18)
    c.ellipse(cx, cy + r * 0.45, r * 0.24, r * 0.28, width=MID)  # long muzzle
    for s in (-1, 1):
        c.circle(cx + s * r * 0.08, cy + r * 0.5, r * 0.05, width=THIN)
    for s in (-0.5, 0.5):
        c.line((cx + s * r, cy + r * 2.2), (cx + s * r, cy + r * 2.6), width=BOLD)
    _flower_row(c)


# 33. Baby raccoon holding a small flower
def raccoon_flower(c):
    cx, cy = c.w / 2, c.h * 0.46
    r = 84
    K.blob_body(c, cx, cy + r * 1.4, r * 0.9, r)
    _round_head(c, cx, cy, r)
    K.ear_pointy(c, (cx - r * 0.7, cy - r * 1.2), (cx - r * 0.95, cy - r * 0.6),
                 (cx - r * 0.4, cy - r * 0.75))
    K.ear_pointy(c, (cx + r * 0.7, cy - r * 1.2), (cx + r * 0.4, cy - r * 0.75),
                 (cx + r * 0.95, cy - r * 0.6))
    for s in (-1, 1):  # mask
        c.ellipse(cx + s * r * 0.4, cy, r * 0.3, r * 0.24, width=MID)
    K.eyes(c, cx, cy, r * 0.8, r * 0.15)
    c.circle(cx, cy + r * 0.35, r * 0.1, width=MID)
    K.smile(c, cx, cy + r * 0.5, r * 0.22)
    # paw holding flower
    K.paw(c, cx - r * 0.5, cy + r * 1.9, r * 0.26)
    K.flower(c, cx - r * 0.5, cy + r * 1.5, r * 0.24)
    # striped tail
    c.path([("M", (cx + r * 0.9, cy + r * 1.6)),
            ("C", (cx + r * 1.6, cy + r * 1.4), (cx + r * 1.6, cy + r * 0.4),
             (cx + r * 1.1, cy + r * 0.5))], width=BOLD)
    for i in range(3):
        c.arc(cx + r * (1.35 - i * 0.02), cy + r * (1.4 - i * 0.35), r * 0.28, 250, 360, width=THIN)


# 34. Cute squirrel collecting acorns
def squirrel_acorns(c):
    cx, cy = c.w * 0.44, c.h * 0.48
    r = 72
    K.blob_body(c, cx, cy + r * 0.9, r * 0.75, r * 0.9)
    _round_head(c, cx, cy, r * 0.7)
    K.ear_pointy(c, (cx - r * 0.5, cy - r * 1.0), (cx - r * 0.6, cy - r * 0.5),
                 (cx - r * 0.25, cy - r * 0.6))
    K.ear_pointy(c, (cx + r * 0.5, cy - r * 1.0), (cx + r * 0.25, cy - r * 0.6),
                 (cx + r * 0.6, cy - r * 0.5))
    K.eyes(c, cx, cy - r * 0.05, r * 0.5, r * 0.16)
    c.circle(cx, cy + r * 0.25, r * 0.08, width=MID)
    K.smile(c, cx, cy + r * 0.35, r * 0.18)
    # big bushy tail
    c.path([("M", (cx + r * 0.7, cy + r * 1.6)),
            ("C", (cx + r * 2.0, cy + r * 1.4), (cx + r * 1.8, cy - r * 0.8),
             (cx + r * 0.6, cy - r * 0.4))], width=BOLD)
    c.wavy(cx + r * 0.9, cy + r * 1.3, cx + r * 1.5, cy - r * 0.4, 8, 3, width=THIN)
    # acorns
    _acorn(c, cx - r * 0.4, cy + r * 1.6, 20)
    _acorn(c, c.w * 0.78, c.h - 132, 26)
    _acorn(c, c.w * 0.7, c.h - 122, 22)


def _acorn(c, cx, cy, r):
    c.arc(cx, cy, r, 180, 360, width=MID)
    c.line((cx - r, cy), (cx + r, cy), width=MID)
    c.path([("M", (cx - r, cy)), ("C", (cx - r, cy + r), (cx + r, cy + r),
            (cx + r, cy))], width=MID)
    c.line((cx, cy - r), (cx, cy - r * 1.4), width=THIN)


# 35. Happy bear cub having a woodland picnic
def bear_picnic(c):
    cx, cy = c.w / 2, c.h * 0.42
    r = 84
    K.blob_body(c, cx, cy + r * 1.3, r, r)
    _round_head(c, cx, cy, r)
    K.ear_round(c, cx - r * 0.75, cy - r * 0.8, r * 0.3)
    K.ear_round(c, cx + r * 0.75, cy - r * 0.8, r * 0.3)
    K.eyes(c, cx, cy - r * 0.05, r * 0.6, r * 0.18)
    c.ellipse(cx, cy + r * 0.3, r * 0.4, r * 0.32, width=MID)
    c.circle(cx, cy + r * 0.18, r * 0.1, width=MID)
    K.smile(c, cx, cy + r * 0.4, r * 0.26)
    # picnic basket
    c.rounded_rect(cx - r * 0.6, cy + r * 2.0, r * 1.2, r * 0.6, 8, width=MID)
    c.arc(cx, cy + r * 2.0, r * 0.6, 180, 360, width=MID)  # handle
    for k in range(4):
        xx = cx - r * 0.6 + r * 1.2 * k / 3
        c.line((xx, cy + r * 2.0), (xx, cy + r * 2.6), width=THIN)
    K.tree_simple(c, c.w * 0.82, c.h - 122, 150)
    K.grass(c, 70, c.w - 70, c.h - 122, 10)


# 36. Cute sloth hanging gently from a tree branch
def sloth_branch(c):
    cx = c.w / 2
    by = c.h * 0.26
    c.line((80, by), (c.w - 80, by), width=BOLD)  # branch
    cy = c.h * 0.5
    r = 82
    c.ellipse(cx, cy, r * 0.8, r * 1.1, width=BOLD)  # body
    _round_head(c, cx, cy - r * 0.9, r * 0.7)
    for s in (-1, 1):  # eye patches
        c.ellipse(cx + s * r * 0.3, cy - r * 0.9, r * 0.22, r * 0.3, width=THIN)
    K.eyes(c, cx, cy - r * 0.9, r * 0.6, r * 0.14, style="closed")
    c.circle(cx, cy - r * 0.6, r * 0.09, width=MID)
    K.smile(c, cx, cy - r * 0.5, r * 0.2)
    # arms reaching up to branch
    for s in (-1, 1):
        c.path([("M", (cx + s * r * 0.6, cy - r * 0.2)),
                ("C", (cx + s * r * 1.2, cy - r * 0.8), (cx + s * r * 1.0, by),
                 (cx + s * r * 0.7, by))], width=BOLD)
        for d in range(3):
            c.arc(cx + s * r * 0.7 + d * 6, by, 8, 0, 180, width=THIN)  # claws
    K.leaf(c, c.w * 0.28, by - 6, 26, -1)
    K.leaf(c, c.w * 0.72, by - 6, 26, 1)


# 37. Baby kangaroo with a joey
def kangaroo_joey(c):
    cx, cy = c.w / 2, c.h * 0.44
    r = 78
    # big body sitting on tail
    c.path([("M", (cx - r * 0.8, cy)),
            ("C", (cx - r * 1.0, cy + r * 1.8), (cx + r * 1.0, cy + r * 1.8),
             (cx + r * 0.8, cy))], width=BOLD)
    _round_head(c, cx, cy - r * 0.3, r * 0.7)
    K.ear_long(c, cx - r * 0.4, cy - r * 0.9, r * 0.16, r * 0.6, tilt=-14)
    K.ear_long(c, cx + r * 0.4, cy - r * 0.9, r * 0.16, r * 0.6, tilt=14)
    K.eyes(c, cx, cy - r * 0.3, r * 0.5, r * 0.16)
    c.ellipse(cx, cy - r * 0.02, r * 0.14, r * 0.1, width=MID)
    K.smile(c, cx, cy + r * 0.1, r * 0.18)
    # pouch with joey peeking
    c.arc(cx, cy + r * 1.1, r * 0.55, 200, 340, width=MID)
    _round_head(c, cx, cy + r * 0.85, r * 0.3)
    K.eyes(c, cx, cy + r * 0.8, r * 0.24, r * 0.08)
    K.ear_long(c, cx - r * 0.16, cy + r * 0.55, r * 0.08, r * 0.28, tilt=-10)
    K.ear_long(c, cx + r * 0.16, cy + r * 0.55, r * 0.08, r * 0.28, tilt=10)
    # tail + feet
    c.path([("M", (cx + r * 0.7, cy + r * 1.6)),
            ("C", (cx + r * 1.6, cy + r * 1.9), (cx + r * 1.9, cy + r * 1.4),
             (cx + r * 1.8, cy + r * 1.1))], width=BOLD)
    c.ellipse(cx - r * 0.4, cy + r * 1.75, r * 0.4, r * 0.16, width=MID)
    K.ground(c, 70, c.w - 70, c.h - 122)


# 38. Cute alpaca surrounded by cactus flowers
def alpaca_cactus(c):
    cx, cy = c.w / 2, c.h * 0.5
    r = 68
    # fluffy body
    for a in range(0, 360, 40):
        rad = math.radians(a)
        c.circle(cx + r * math.cos(rad), cy + r * 0.4 + r * 0.9 * math.sin(rad),
                 r * 0.32, width=MID)
    c.rounded_rect(cx - r * 0.35, cy - r * 1.8, r * 0.7, r * 1.3, 16, width=BOLD)  # neck
    _round_head(c, cx, cy - r * 2.0, r * 0.5)
    for a in range(150, 391, 40):  # top fluff
        rad = math.radians(a)
        c.circle(cx + r * 0.3 * math.cos(rad), cy - r * 2.35 + r * 0.2 * math.sin(rad), r * 0.12, width=THIN)
    K.ear_long(c, cx - r * 0.3, cy - r * 2.5, r * 0.1, r * 0.35, tilt=-16)
    K.ear_long(c, cx + r * 0.3, cy - r * 2.5, r * 0.1, r * 0.35, tilt=16)
    K.eyes(c, cx, cy - r * 2.05, r * 0.35, r * 0.1)
    K.smile(c, cx, cy - r * 1.85, r * 0.14)
    _cactus(c, c.w * 0.78, c.h - 122, 90)
    _cactus(c, c.w * 0.2, c.h - 122, 70)


def _cactus(c, cx, base_y, h):
    c.rounded_rect(cx - h * 0.16, base_y - h, h * 0.32, h, h * 0.16, width=MID)
    c.arc(cx - h * 0.16, base_y - h * 0.5, h * 0.24, 90, 270, width=MID)
    c.line((cx - h * 0.4, base_y - h * 0.5), (cx - h * 0.4, base_y - h * 0.75), width=MID)
    K.flower(c, cx, base_y - h, h * 0.14)


# 39. Happy frog sitting on a lily pad
def frog_lilypad(c):
    cx, cy = c.w / 2, c.h * 0.44
    r = 96
    c.ellipse(cx, cy + r * 0.3, r, r * 0.8, width=BOLD)  # body
    for s in (-1, 1):  # eye bumps
        c.circle(cx + s * r * 0.45, cy - r * 0.55, r * 0.32, width=BOLD)
        c.circle(cx + s * r * 0.45, cy - r * 0.55, r * 0.16, width=THIN)
    K.smile(c, cx, cy + r * 0.05, r * 0.55)
    for s in (-1, 1):  # front feet
        c.ellipse(cx + s * r * 0.55, cy + r * 0.95, r * 0.28, r * 0.12, width=MID)
        for d in (-1, 0, 1):
            c.line((cx + s * r * 0.55 + d * r * 0.12, cy + r * 0.95),
                   (cx + s * r * 0.55 + d * r * 0.18, cy + r * 1.1), width=THIN)
    K.lily_pad(c, cx, cy + r * 1.35, r * 1.3)
    K.water_waves(c, 60, c.w - 60, c.h * 0.72, 2)
    K.flower(c, c.w * 0.74, c.h * 0.6, 30)


# 40. Cute snail exploring a mushroom garden
def snail_mushrooms(c):
    cx, cy = c.w * 0.46, c.h * 0.52
    r = 92
    # shell spiral
    c.circle(cx, cy, r, width=BOLD)
    for i in range(4):
        c.arc(cx, cy, r * (1 - i * 0.22), 0 + i * 40, 320 + i * 40, width=MID, segments=28)
    # body
    c.path([("M", (cx - r * 0.9, cy + r * 0.6)),
            ("C", (cx - r * 1.9, cy + r * 0.8), (cx - r * 1.9, cy - r * 0.4),
             (cx - r * 1.4, cy - r * 0.5))], width=BOLD)
    c.line((cx - r * 0.9, cy + r * 0.9), (cx - r * 1.7, cy + r * 0.95), width=BOLD)
    for s in (0, 1):  # eye stalks
        sx = cx - r * 1.5 - s * 12
        c.line((cx - r * 1.55 + s * 8, cy - r * 0.45), (sx, cy - r * 0.95), width=MID)
        c.circle(sx, cy - r, 8, width=MID)
    K.smile(c, cx - r * 1.4, cy - r * 0.25, r * 0.18)
    K.mushroom(c, c.w * 0.78, c.h - 122, 44)
    K.mushroom(c, c.w * 0.9, c.h - 122, 30)
    K.grass(c, 70, c.w - 70, c.h - 122, 10)


# 41. Adorable puppy, kitten and bunny sitting together
def trio_friends(c):
    base = c.h * 0.56
    # bunny (left)
    bx = c.w * 0.28
    _round_head(c, bx, base - 70, 58)
    K.ear_long(c, bx - 20, base - 130, 14, 70, tilt=-8)
    K.ear_long(c, bx + 20, base - 130, 14, 70, tilt=8)
    K.eyes(c, bx, base - 72, 44, 14)
    K.smile(c, bx, base - 50, 22)
    c.ellipse(bx, base + 6, 56, 60, width=BOLD)
    # puppy (center)
    px = c.w * 0.5
    _round_head(c, px, base - 80, 66)
    c.ellipse(px - 62, base - 66, 22, 44, width=BOLD)
    c.ellipse(px + 62, base - 66, 22, 44, width=BOLD)
    K.eyes(c, px, base - 82, 50, 16)
    K.nose_muzzle(c, px, base - 52, 12)
    c.ellipse(px, base + 8, 64, 66, width=BOLD)
    # kitten (right)
    kx = c.w * 0.72
    _round_head(c, kx, base - 70, 58)
    K.ear_pointy(c, (kx - 40, base - 128), (kx - 56, base - 84), (kx - 22, base - 92))
    K.ear_pointy(c, (kx + 40, base - 128), (kx + 22, base - 92), (kx + 56, base - 84))
    K.eyes(c, kx, base - 72, 44, 14)
    for s in (-1, 1):
        for dy in (-3, 3):
            c.line((kx + s * 14, base - 50 + dy), (kx + s * 44, base - 46 + dy * 1.4), width=THIN)
    c.ellipse(kx, base + 6, 56, 60, width=BOLD)
    K.grass(c, 60, c.w - 60, c.h - 122, 14)
    K.flower(c, c.w * 0.16, c.h * 0.78, 26)
    K.flower(c, c.w * 0.86, c.h * 0.78, 26)


# 42. Grand finale: several cute animal friends celebrating in a meadow
def finale_meadow(c):
    base = c.h * 0.56
    # bunny
    _mini_bunny(c, c.w * 0.2, base)
    # bear
    _mini_bear(c, c.w * 0.4, base + 6)
    # cat
    _mini_cat(c, c.w * 0.6, base)
    # fox
    _mini_fox(c, c.w * 0.8, base + 4)
    # bunting / celebration
    c.wavy(70, c.h * 0.2, c.w - 70, c.h * 0.2, 14, 3, width=MID)
    for k in range(7):
        fx = 90 + (c.w - 180) * k / 6
        fy = c.h * 0.2 + (14 if k % 2 else -6)
        c.polyline([(fx - 12, fy), (fx + 12, fy), (fx, fy + 24)], width=THIN, closed=True)
    K.sun(c, c.w * 0.5, c.h * 0.12, 26)
    K.grass(c, 60, c.w - 60, c.h - 122, 18)
    for xx in (0.12, 0.5, 0.9):
        K.flower(c, c.w * xx, c.h * 0.8, 24)


def _mini_bunny(c, cx, base):
    r = 46
    _round_head(c, cx, base - r, r)
    K.ear_long(c, cx - 16, base - r * 2.1, 10, 48, tilt=-8)
    K.ear_long(c, cx + 16, base - r * 2.1, 10, 48, tilt=8)
    K.eyes(c, cx, base - r, 34, 11)
    K.smile(c, cx, base - r * 0.6, 16)
    c.ellipse(cx, base + 20, 44, 48, width=BOLD)


def _mini_bear(c, cx, base):
    r = 50
    _round_head(c, cx, base - r, r)
    K.ear_round(c, cx - r * 0.7, base - r * 1.7, r * 0.3)
    K.ear_round(c, cx + r * 0.7, base - r * 1.7, r * 0.3)
    K.eyes(c, cx, base - r, 36, 12)
    c.ellipse(cx, base - r * 0.6, 20, 16, width=MID)
    c.ellipse(cx, base + 24, 50, 52, width=BOLD)


def _mini_cat(c, cx, base):
    r = 46
    _round_head(c, cx, base - r, r)
    K.ear_pointy(c, (cx - 32, base - r * 2.0), (cx - 46, base - r * 1.1), (cx - 16, base - r * 1.2))
    K.ear_pointy(c, (cx + 32, base - r * 2.0), (cx + 16, base - r * 1.2), (cx + 46, base - r * 1.1))
    K.eyes(c, cx, base - r, 34, 11)
    K.smile(c, cx, base - r * 0.6, 14)
    c.ellipse(cx, base + 20, 44, 48, width=BOLD)


def _mini_fox(c, cx, base):
    r = 46
    _round_head(c, cx, base - r, r)
    K.ear_pointy(c, (cx - 32, base - r * 2.0), (cx - 44, base - r * 1.15), (cx - 14, base - r * 1.25))
    K.ear_pointy(c, (cx + 32, base - r * 2.0), (cx + 14, base - r * 1.25), (cx + 44, base - r * 1.15))
    K.eyes(c, cx, base - r, 34, 11)
    c.polyline([(cx, base - r * 0.7), (cx - 8, base - r * 0.5), (cx + 8, base - r * 0.5)], width=MID, closed=True)
    c.ellipse(cx, base + 20, 44, 48, width=BOLD)


# ---- shared decorative flower row along the bottom -------------------------
def _flower_row(c):
    y = c.h - 122
    K.ground(c, 60, c.w - 60, y + 8)
    xs = [0.12, 0.26, 0.74, 0.88]
    for xx in xs:
        K.flower(c, c.w * xx, y - 10, 26)
        c.line((c.w * xx, y - 10 + 26 * 0.35), (c.w * xx, y + 8), width=THIN)
    K.grass(c, 60, c.w - 60, y + 8, 12)


# ---- ordered list of all 42 --------------------------------------------------
PAGES = [
    ("PUPPY IN A FLOWER GARDEN", puppy_garden),
    ("KITTEN & BUTTERFLIES", kitten_butterflies),
    ("BUNNY & SPRING FLOWERS", bunny_flowers),
    ("BABY ELEPHANT & FLOWER", elephant_flower),
    ("PANDA EATING BAMBOO", panda_bamboo),
    ("BABY DEER & WILDFLOWERS", deer_wildflowers),
    ("HEDGEHOG WITH FLOWERS", hedgehog_flowers),
    ("OWL ON A BRANCH", owl_branch),
    ("SLEEPY FOX & MOON", fox_sleeping),
    ("TURTLE & LITTLE FISH", turtle_fish),
    ("LLAMA IN THE MEADOW", llama_meadow),
    ("KOALA HUGGING A TREE", koala_tree),
    ("BABY LION & FLOWERS", lion_savanna),
    ("MONKEY WITH A BANANA", monkey_banana),
    ("GIRAFFE & BUTTERFLIES", giraffe_butterflies),
    ("BABY ZEBRA", zebra_field),
    ("HIPPO BY THE POND", hippo_pond),
    ("CROCODILE FLOWER CROWN", croc_crown),
    ("PENGUIN & SNOWFLAKE", penguin_snowflake),
    ("POLAR BEAR IN THE SNOW", polar_bear_snow),
    ("DOLPHIN JUMPING", dolphin_jump),
    ("WHALE & BUBBLES", whale_bubbles),
    ("BABY SEAL & SEASHELLS", seal_shells),
    ("HAPPY OCTOPUS", octopus_bubbles),
    ("SEAHORSE & CORAL", seahorse_coral),
    ("DUCK IN THE POND", duck_pond),
    ("CHICK & SPRING FLOWERS", chick_flowers),
    ("LAMB IN THE MEADOW", lamb_meadow),
    ("GOAT BY THE FENCE", goat_fence),
    ("PIGLET & DAISIES", piglet_daisies),
    ("CALF IN THE FIELD", calf_field),
    ("HORSE & FLOWERS", horse_flowers),
    ("RACCOON WITH A FLOWER", raccoon_flower),
    ("SQUIRREL & ACORNS", squirrel_acorns),
    ("BEAR CUB PICNIC", bear_picnic),
    ("SLOTH ON A BRANCH", sloth_branch),
    ("KANGAROO & JOEY", kangaroo_joey),
    ("ALPACA & CACTUS FLOWERS", alpaca_cactus),
    ("FROG ON A LILY PAD", frog_lilypad),
    ("SNAIL & MUSHROOMS", snail_mushrooms),
    ("PUPPY KITTEN & BUNNY", trio_friends),
    ("MEADOW CELEBRATION", finale_meadow),
]
