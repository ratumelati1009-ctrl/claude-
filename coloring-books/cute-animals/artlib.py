"""
artlib.py — a tiny zero-dependency vector drawing library.

Every shape appends to a Canvas as normalized primitives. A Canvas can then be
rendered to (a) an SVG string and (b) a PDF content stream. This lets us author
each coloring illustration ONCE and export it to both formats.

Coordinate system: user space in points (1/72 inch), origin top-left, y grows
DOWN (like SVG). The PDF exporter flips y for us.

Line art only: strokes are black, no fills (so pages are colorable). Stroke
width is chosen to print cleanly on paper.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import List, Tuple

Pt = Tuple[float, float]


@dataclass
class Shape:
    kind: str                 # 'path'
    d: List[Tuple]            # list of subpath commands
    width: float = 2.2        # stroke width in points
    closed: bool = False


@dataclass
class Canvas:
    w: float
    h: float
    shapes: List[Shape] = field(default_factory=list)

    # --- primitive builders -------------------------------------------------
    def path(self, cmds, width=2.2, closed=False):
        self.shapes.append(Shape("path", cmds, width, closed))

    def line(self, p0: Pt, p1: Pt, width=2.2):
        self.path([("M", p0), ("L", p1)], width)

    def polyline(self, pts: List[Pt], width=2.2, closed=False):
        cmds = [("M", pts[0])] + [("L", p) for p in pts[1:]]
        self.path(cmds, width, closed)

    def circle(self, cx, cy, r, width=2.2):
        self.ellipse(cx, cy, r, r, width)

    def ellipse(self, cx, cy, rx, ry, width=2.2):
        # 4-arc bezier approximation of an ellipse
        k = 0.5522847498
        ox, oy = rx * k, ry * k
        cmds = [
            ("M", (cx + rx, cy)),
            ("C", (cx + rx, cy + oy), (cx + ox, cy + ry), (cx, cy + ry)),
            ("C", (cx - ox, cy + ry), (cx - rx, cy + oy), (cx - rx, cy)),
            ("C", (cx - rx, cy - oy), (cx - ox, cy - ry), (cx, cy - ry)),
            ("C", (cx + ox, cy - ry), (cx + rx, cy - oy), (cx + rx, cy)),
        ]
        self.path(cmds, width, closed=True)

    def rounded_rect(self, x, y, w, h, r, width=2.2):
        r = min(r, w / 2, h / 2)
        k = 0.5522847498 * r
        cmds = [
            ("M", (x + r, y)),
            ("L", (x + w - r, y)),
            ("C", (x + w - r + k, y), (x + w, y + r - k), (x + w, y + r)),
            ("L", (x + w, y + h - r)),
            ("C", (x + w, y + h - r + k), (x + w - r + k, y + h), (x + w - r, y + h)),
            ("L", (x + r, y + h)),
            ("C", (x + r - k, y + h), (x, y + h - r + k), (x, y + h - r)),
            ("L", (x, y + r)),
            ("C", (x, y + r - k), (x + r - k, y), (x + r, y)),
        ]
        self.path(cmds, width, closed=True)

    def arc(self, cx, cy, r, a0_deg, a1_deg, width=2.2, segments=None):
        """Circular arc from a0 to a1 (degrees, 0=east, CW positive in screen)."""
        a0 = math.radians(a0_deg)
        a1 = math.radians(a1_deg)
        if segments is None:
            segments = max(8, int(abs(a1_deg - a0_deg) / 15))
        pts = []
        for i in range(segments + 1):
            t = a0 + (a1 - a0) * i / segments
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
        self.polyline(pts, width)

    def wavy(self, x0, y0, x1, y1, amp, waves, width=2.2):
        """A sinusoidal wave between two points (used for water, hair, clouds)."""
        pts = []
        n = max(24, waves * 12)
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy)
        nx, ny = (-dy / length, dx / length)  # normal
        for i in range(n + 1):
            t = i / n
            base_x = x0 + dx * t
            base_y = y0 + dy * t
            off = amp * math.sin(t * waves * 2 * math.pi)
            pts.append((base_x + nx * off, base_y + ny * off))
        self.polyline(pts, width)

    def star(self, cx, cy, r_out, r_in, points=5, rot_deg=-90, width=2.2):
        pts = []
        for i in range(points * 2):
            r = r_out if i % 2 == 0 else r_in
            a = math.radians(rot_deg + i * 180.0 / points)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        self.polyline(pts, width, closed=True)

    def petal(self, cx, cy, r, angle_deg, spread=40, width=2.2):
        """A single flower petal as two bezier curves forming a leaf shape."""
        a = math.radians(angle_deg)
        tip = (cx + r * math.cos(a), cy + r * math.sin(a))
        s1 = math.radians(angle_deg - spread / 2)
        s2 = math.radians(angle_deg + spread / 2)
        c1 = (cx + r * 0.6 * math.cos(s1), cy + r * 0.6 * math.sin(s1))
        c2 = (cx + r * 0.6 * math.cos(s2), cy + r * 0.6 * math.sin(s2))
        cmds = [
            ("M", (cx, cy)),
            ("C", (cx, cy), c1, tip),
            ("C", c2, (cx, cy), (cx, cy)),
        ]
        self.path(cmds, width, closed=True)


# ---------------------------------------------------------------------------
# SVG export
# ---------------------------------------------------------------------------
def _fmt(n: float) -> str:
    return f"{n:.2f}".rstrip("0").rstrip(".")


def to_svg(c: Canvas, margin_box: bool = True) -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{_fmt(c.w)}" '
        f'height="{_fmt(c.h)}" viewBox="0 0 {_fmt(c.w)} {_fmt(c.h)}">',
        f'<rect x="0" y="0" width="{_fmt(c.w)}" height="{_fmt(c.h)}" fill="white"/>',
    ]
    for s in c.shapes:
        d = _svg_path_d(s.d, s.closed)
        parts.append(
            f'<path d="{d}" fill="none" stroke="black" '
            f'stroke-width="{_fmt(s.width)}" stroke-linecap="round" '
            f'stroke-linejoin="round"/>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def _svg_path_d(cmds, closed) -> str:
    out = []
    for cmd in cmds:
        op = cmd[0]
        if op == "M":
            out.append(f"M {_fmt(cmd[1][0])} {_fmt(cmd[1][1])}")
        elif op == "L":
            out.append(f"L {_fmt(cmd[1][0])} {_fmt(cmd[1][1])}")
        elif op == "C":
            out.append(
                "C "
                + " ".join(f"{_fmt(p[0])} {_fmt(p[1])}" for p in cmd[1:])
            )
    if closed:
        out.append("Z")
    return " ".join(out)


# ---------------------------------------------------------------------------
# PDF content-stream export (paths only)
# ---------------------------------------------------------------------------
def to_pdf_stream(c: Canvas) -> str:
    """Return a PDF content stream string. y is flipped: pdf_y = h - y."""
    H = c.h
    out = ["1 1 1 rg", f"0 0 {_fmt(c.w)} {_fmt(c.h)} re f",  # white bg
           "0 0 0 RG", "1 j", "1 J"]  # black stroke, round joins/caps

    def y(v):  # flip
        return H - v

    for s in c.shapes:
        out.append(f"{_fmt(s.width)} w")
        for cmd in s.d:
            op = cmd[0]
            if op == "M":
                out.append(f"{_fmt(cmd[1][0])} {_fmt(y(cmd[1][1]))} m")
            elif op == "L":
                out.append(f"{_fmt(cmd[1][0])} {_fmt(y(cmd[1][1]))} l")
            elif op == "C":
                pts = cmd[1:]
                out.append(
                    " ".join(f"{_fmt(p[0])} {_fmt(y(p[1]))}" for p in pts) + " c"
                )
        out.append("h S" if s.closed else "S")
    return "\n".join(out)
