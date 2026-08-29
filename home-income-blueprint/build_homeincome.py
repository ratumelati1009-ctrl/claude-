#!/usr/bin/env python3
"""Build a styled HTML and a self-contained PDF for 'The Home Income Blueprint' ebook.
Handles: h1/h2/h3, subtitle, paragraphs, bullet & checkbox lists, blockquote
callouts (incl. story boxes), fenced code blocks (illustrations), and
markdown tables. No third-party dependencies."""
import re
import html as html_lib

SRC = "home-income-blueprint.md"
HTML_OUT = "The-Home-Income-Blueprint.html"
PDF_OUT = "The-Home-Income-Blueprint.pdf"
AUTHOR = "Daniel Tesfamariam"
EMAIL = "dannyshalomnebiy@gmail.com"

with open(SRC, encoding="utf-8") as f:
    raw = f.read()
lines = raw.split("\n")

# ---------- Parse into blocks ----------
# block types: h1,h2,h3,subtitle,p,hr,ul(list of (text,checkbox)),
#              code(list lines), table(header,rows), quote(list of (kind,text))
blocks = []
i = 0
n = len(lines)


def is_table_sep(s):
    return bool(re.match(r"^\|[\s:|-]+\|?\s*$", s)) and "-" in s


while i < n:
    line = lines[i]
    s = line.strip()
    if s == "":
        i += 1
        continue
    # fenced code inside blockquote or standalone
    if s.startswith("```") or s.startswith("> ```"):
        # handled within quote parser or standalone
        pass
    # Horizontal rule
    if s == "---":
        blocks.append(("hr", None))
        i += 1
        continue
    # Headings
    if s.startswith("### "):
        blocks.append(("h3", s[4:].strip()))
        i += 1
        continue
    if s.startswith("## "):
        blocks.append(("h2", s[3:].strip()))
        i += 1
        continue
    if s.startswith("# "):
        blocks.append(("h1", s[2:].strip()))
        i += 1
        continue
    # Blockquote group (may contain fenced code)
    if s.startswith(">"):
        qlines = []
        while i < n and lines[i].strip().startswith(">"):
            content = lines[i].strip()[1:]
            if content.startswith(" "):
                content = content[1:]
            qlines.append(content)
            i += 1
        # parse qlines into sub-blocks
        sub = []
        j = 0
        while j < len(qlines):
            q = qlines[j]
            if q.strip().startswith("```"):
                code = []
                j += 1
                while j < len(qlines) and not qlines[j].strip().startswith("```"):
                    code.append(qlines[j])
                    j += 1
                j += 1  # skip closing fence
                sub.append(("code", code))
            elif q.strip() == "":
                j += 1
            elif q.strip().startswith("- "):
                sub.append(("li", q.strip()[2:].strip()))
                j += 1
            else:
                sub.append(("p", q.strip()))
                j += 1
        blocks.append(("quote", sub))
        continue
    # Standalone fenced code
    if s.startswith("```"):
        code = []
        i += 1
        while i < n and not lines[i].strip().startswith("```"):
            code.append(lines[i])
            i += 1
        i += 1
        blocks.append(("code", code))
        continue
    # Table
    if s.startswith("|"):
        tbl = [s]
        i += 1
        while i < n and lines[i].strip().startswith("|"):
            tbl.append(lines[i].strip())
            i += 1

        def split_row(r):
            r = r.strip()
            if r.startswith("|"):
                r = r[1:]
            if r.endswith("|"):
                r = r[:-1]
            return [c.strip() for c in r.split("|")]

        header = split_row(tbl[0])
        rows = []
        for r in tbl[1:]:
            if is_table_sep(r):
                continue
            rows.append(split_row(r))
        blocks.append(("table", (header, rows)))
        continue
    # Lists
    if s.startswith("- "):
        items = []
        while i < n and lines[i].strip().startswith("- "):
            item = lines[i].strip()[2:]
            cb = None
            if item.startswith("[ ] "):
                cb = False
                item = item[4:]
            elif item.startswith("[x] ") or item.startswith("[X] "):
                cb = True
                item = item[4:]
            items.append((item.strip(), cb))
            i += 1
        blocks.append(("ul", items))
        continue
    # Subtitle heuristics handled at render (## right after #). Default paragraph.
    blocks.append(("p", s))
    i += 1


def strip_md(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"\*(.+?)\*", r"\1", t)
    t = re.sub(r"~~(.+?)~~", r"\1", t)
    return t


# ---------- HTML ----------
def inl(t):
    t = html_lib.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"~~(.+?)~~", r"<del>\1</del>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return t


def quote_is_story(sub):
    for kind, text in sub:
        if kind == "p" and (text.startswith("**") and text.endswith("**")):
            return True
        break
    return False


hp = []
title_seen = False
for bi, (kind, payload) in enumerate(blocks):
    if kind == "h1":
        if not title_seen:
            hp.append(f'<h1 class="booktitle">{inl(payload)}</h1>')
            title_seen = True
        else:
            hp.append(f'<h1 class="part">{inl(payload)}</h1>')
    elif kind == "h2":
        # subtitle = the ## immediately after the very first # (index check)
        if bi <= 2:
            hp.append(f'<p class="subtitle">{inl(payload)}</p>')
        else:
            hp.append(f"<h2>{inl(payload)}</h2>")
    elif kind == "h3":
        if bi <= 3:
            hp.append(f'<p class="tagline">{inl(payload)}</p>')
        else:
            hp.append(f"<h3>{inl(payload)}</h3>")
    elif kind == "p":
        cls = ""
        if AUTHOR in payload and payload.strip().startswith("**By"):
            cls = ' class="byline"'
        elif EMAIL in payload:
            cls = ' class="email"'
        hp.append(f"<p{cls}>{inl(payload)}</p>")
    elif kind == "hr":
        hp.append("<hr/>")
    elif kind == "ul":
        is_check = any(cb is not None for _, cb in payload)
        hp.append('<ul class="checklist">' if is_check else "<ul>")
        for text, cb in payload:
            if cb is None:
                hp.append(f"<li>{inl(text)}</li>")
            else:
                box = "&#9745;" if cb else "&#9744;"
                hp.append(f'<li class="check">{box} {inl(text)}</li>')
        hp.append("</ul>")
    elif kind == "code":
        esc = html_lib.escape("\n".join(payload))
        hp.append(f'<pre class="illus">{esc}</pre>')
    elif kind == "table":
        header, rows = payload
        hp.append('<table><thead><tr>')
        for c in header:
            hp.append(f"<th>{inl(c)}</th>")
        hp.append("</tr></thead><tbody>")
        for r in rows:
            hp.append("<tr>")
            for c in r:
                hp.append(f"<td>{inl(c)}</td>")
            hp.append("</tr>")
        hp.append("</tbody></table>")
    elif kind == "quote":
        sub = payload
        story = quote_is_story(sub)
        cls = "story" if story else "callout"
        hp.append(f'<div class="{cls}">')
        first = True
        for skind, stext in sub:
            if skind == "code":
                esc = html_lib.escape("\n".join(stext))
                hp.append(f'<pre class="illus">{esc}</pre>')
            elif skind == "li":
                hp.append(f"<p>&bull; {inl(stext)}</p>")
            else:
                if first and story:
                    hp.append(f'<p class="story-title">{inl(stext)}</p>')
                else:
                    hp.append(f"<p>{inl(stext)}</p>")
            first = False
        hp.append("</div>")

html_doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="author" content="{AUTHOR}"/>
<title>The Home Income Blueprint — Start a Side Hustle From Home</title>
<style>
 body{{font-family:Georgia,'Times New Roman',serif;line-height:1.7;color:#22252a;
   max-width:760px;margin:0 auto;padding:48px 30px;}}
 h1.booktitle{{font-size:3em;text-align:center;color:#153a66;margin:.1em 0;}}
 p.subtitle{{text-align:center;font-size:1.4em;color:#1b4f8a;font-weight:bold;margin:.2em 0;}}
 p.tagline{{text-align:center;font-size:1.05em;color:#555;font-style:italic;margin:.2em 0 1em;}}
 h1.part{{font-size:2em;color:#fff;background:#1b4f8a;padding:14px 18px;border-radius:6px;
   margin-top:2em;}}
 h2{{font-size:1.5em;color:#153a66;margin-top:1.8em;border-bottom:2px solid #c3d4e6;padding-bottom:.2em;}}
 h3{{font-size:1.15em;color:#1b4f8a;margin-top:1.4em;}}
 p{{margin:.8em 0;text-align:justify;}}
 p.byline{{text-align:center;font-size:1.2em;font-weight:bold;}}
 p.email{{text-align:center;color:#666;font-style:italic;}}
 ul{{margin:.6em 0 1em 1.4em;}} li{{margin:.3em 0;}}
 ul.checklist{{list-style:none;margin-left:.4em;}}
 li.check{{margin:.35em 0;}}
 hr{{border:none;border-top:1px solid #e0e0e0;margin:2em 0;}}
 .story{{background:#fff6ea;border-left:5px solid #e0a02f;padding:14px 20px;margin:1.6em 0;border-radius:5px;}}
 .story p{{font-style:italic;}} .story-title{{font-weight:bold;font-style:normal;color:#b9791a;}}
 .callout{{background:#eef3f9;border-left:5px solid #1b4f8a;padding:12px 18px;margin:1.4em 0;border-radius:5px;}}
 .callout p{{margin:.4em 0;}}
 pre.illus{{background:#f4f4f0;border:1px solid #ddd;border-radius:5px;padding:12px;
   font-family:'Courier New',monospace;font-size:.85em;line-height:1.35;overflow-x:auto;white-space:pre;}}
 table{{border-collapse:collapse;width:100%;margin:1em 0;font-size:.92em;}}
 th,td{{border:1px solid #c3d4e6;padding:7px 9px;text-align:left;vertical-align:top;}}
 th{{background:#1b4f8a;color:#fff;}} tr:nth-child(even) td{{background:#f3f7fb;}}
 td:empty{{height:1.6em;}}
 @media print{{body{{max-width:none;}} h1.part{{-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
   th{{-webkit-print-color-adjust:exact;print-color-adjust:exact;}}}}
</style></head><body>
{chr(10).join(hp)}
</body></html>"""
with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html_doc)
print(f"Wrote {HTML_OUT}")

# ---------- PDF ----------
HELV = [278,278,355,556,556,889,667,191,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,278,278,584,584,584,556,1015,667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611,278,278,278,469,556,333,556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500,334,260,334,584]
HELB = [278,333,474,556,556,889,722,238,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,333,333,584,584,584,611,975,722,722,722,722,667,611,778,722,278,556,722,611,833,722,778,667,778,722,667,611,722,667,944,667,667,611,333,278,333,584,556,333,556,611,556,611,556,333,611,611,278,278,556,278,889,611,611,611,611,389,556,333,611,556,778,556,556,500,389,280,389,584]


def cw(ch, font):
    o = ord(ch)
    if 32 <= o <= 126:
        return (HELB if font == "B" else HELV)[o - 32]
    return 556


def tw(s, size, font):
    return sum(cw(c, font) for c in s) * size / 1000.0


def wrap(text, size, font, maxw):
    words = text.split()
    out, cur = [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if tw(trial, size, font) <= maxw or not cur:
            cur = trial
        else:
            out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out or [""]


REPL = {"\u2019":"'","\u2018":"'","\u201c":'"',"\u201d":'"',"\u2014":"-","\u2013":"-",
        "\u2026":"...","\u2022":"-","\u2705":"[x]","\u2611":"[x]","\u2610":"[ ]",
        "\u9745":"[x]","\u9744":"[ ]","\u2013":"-"}


def clean(s):
    for k, v in REPL.items():
        s = s.replace(k, v)
    return "".join(c if ord(c) < 256 else "?" for c in s)


def esc(s):
    return s.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


PW, PH = 612, 792
ML, MR, MT, MB = 60, 60, 66, 60
CW = PW - ML - MR

# render items: dicts of type line/space/rect/hline
render = []


def sp(h):
    render.append({"t": "space", "h": h})


def ln(text, font, size, lead, indent=0, center=False, color=None, mono=False):
    render.append({"t": "line", "text": text, "font": font, "size": size, "lead": lead,
                   "indent": indent, "center": center, "color": color, "mono": mono})


def box_start(color):
    render.append({"t": "boxstart", "color": color})


def box_end(pad=0):
    render.append({"t": "boxend"})


def band(text):
    render.append({"t": "band", "text": text})


title_seen = False
for bi, (kind, payload) in enumerate(blocks):
    if kind == "hr":
        sp(4)
        render.append({"t": "hline"})
        sp(6)
    elif kind == "h1":
        if not title_seen:
            sp(60)
            for wl in wrap(clean(payload), 40, "B", CW):
                ln(wl, "B", 40, 48, center=True, color=(0.106, 0.31, 0.541))
            title_seen = True
            sp(6)
        else:
            sp(20)
            band(clean(payload))
            sp(14)
    elif kind == "h2":
        if bi <= 2:
            for wl in wrap(clean(payload), 19, "B", CW):
                ln(wl, "B", 19, 25, center=True, color=(0.106, 0.31, 0.541))
            sp(4)
        else:
            sp(16)
            for wl in wrap(clean(payload), 17, "B", CW):
                ln(wl, "B", 17, 23, color=(0.106, 0.31, 0.541))
            sp(4)
    elif kind == "h3":
        if bi <= 3:
            for wl in wrap(clean(payload), 12, "B", CW):
                ln(wl, "B", 12, 18, center=True, color=(0.35, 0.35, 0.35))
            sp(6)
        else:
            sp(10)
            for wl in wrap(clean(payload), 13, "B", CW):
                ln(wl, "B", 13, 19, color=(0.106, 0.31, 0.541))
            sp(3)
    elif kind == "p":
        plain = clean(strip_md(payload))
        if AUTHOR in payload and payload.strip().startswith("**By"):
            ln(plain, "B", 16, 24, center=True)
            sp(3)
        elif EMAIL in payload:
            for wl in wrap(plain, 12, "R", CW):
                ln(wl, "R", 12, 18, center=True, color=(0.4, 0.4, 0.4))
            sp(3)
        else:
            for wl in wrap(plain, 11, "R", CW):
                ln(wl, "R", 11, 16.5)
            sp(6)
    elif kind == "ul":
        for text, cb in payload:
            plain = clean(strip_md(text))
            prefix = ("[ ] " if cb is False else "[x] " if cb else "- ")
            wrapped = wrap(plain, 11, "R", CW - 20)
            for k2, wl in enumerate(wrapped):
                ln((prefix if k2 == 0 else "    ") + wl, "R", 11, 15.5, indent=16)
        sp(6)
    elif kind == "code":
        sp(2)
        box_start((0.95, 0.95, 0.93))
        for cl in payload:
            ln(clean(cl.rstrip()) or " ", "R", 8.5, 11.5, indent=8, mono=True,
               color=(0.15, 0.15, 0.15))
        box_end()
        sp(6)
    elif kind == "table":
        header, rows = payload
        ncol = len(header)
        colw = (CW - 6) / ncol
        # header
        def emit_row(cells, bold, shade):
            # wrap each cell
            wrapped = [wrap(clean(strip_md(c)), 8.5, "B" if bold else "R", colw - 8) for c in cells]
            h = max(len(w) for w in wrapped)
            render.append({"t": "trow", "cells": wrapped, "colw": colw, "ncol": ncol,
                           "bold": bold, "shade": shade, "rowh": h * 11 + 6})
        emit_row(header + [""] * (ncol - len(header)), True, (0.106, 0.31, 0.541))
        for ri, r in enumerate(rows):
            r = (r + [""] * ncol)[:ncol]
            shade = (0.953, 0.969, 0.984) if ri % 2 else None
            emit_row(r, False, shade)
        sp(8)
    elif kind == "quote":
        sub = payload
        story = quote_is_story(sub)
        col = (1.0, 0.965, 0.917) if story else (0.933, 0.953, 0.976)
        sp(3)
        box_start(col)
        first = True
        for skind, stext in sub:
            if skind == "code":
                for cl in stext:
                    ln(clean(cl.rstrip()) or " ", "R", 8, 11, indent=12, mono=True,
                       color=(0.15, 0.15, 0.15))
            elif skind == "li":
                for k2, wl in enumerate(wrap(clean(strip_md(stext)), 10.5, "R", CW - 40)):
                    ln(("- " if k2 == 0 else "  ") + wl, "R", 10.5, 15, indent=20)
            else:
                fnt = "B" if (first and story) else "R"
                clr = (0.72, 0.47, 0.10) if (first and story) else (0.12, 0.12, 0.12)
                sz = 11 if (first and story) else 10.5
                for wl in wrap(clean(strip_md(stext)), sz, fnt, CW - 36):
                    ln(wl, fnt, sz, 15.5, indent=14, color=clr)
            first = False
        box_end()
        sp(6)

# ---------- Paginate ----------
pages = []
cur = []
y = PH - MT
box_stack = []  # active box: {color, x0, y_top}
open_boxes = []


def new_page():
    global cur, y, open_boxes
    # close any open boxes at page bottom
    for b in open_boxes:
        cur.append(("boxdraw", b["color"], b["ytop"], MB))
        b["ytop"] = PH - MT  # continues on next page
    pages.append(cur)
    cur = []
    y = PH - MT


for item in render:
    t = item["t"]
    if t == "space":
        y -= item["h"]
        if y < MB:
            new_page()
    elif t == "hline":
        if y - 8 < MB:
            new_page()
        y -= 8
        cur.append(("hline", y + 4))
    elif t == "band":
        need = 34
        if y - need < MB:
            new_page()
        y -= 26
        cur.append(("band", item["text"], y))
        y -= 12
    elif t == "boxstart":
        if y - 14 < MB:
            new_page()
        y -= 6
        b = {"color": item["color"], "ytop": y}
        open_boxes.append(b)
        y -= 6
    elif t == "boxend":
        if open_boxes:
            b = open_boxes.pop()
            cur.append(("boxdraw", b["color"], b["ytop"], y - 4))
            y -= 8
    elif t == "line":
        lead = item["lead"]
        if y - lead < MB:
            # close/reopen boxes across page
            reopen = list(open_boxes)
            for b in open_boxes:
                cur.append(("boxdraw", b["color"], b["ytop"], MB))
            new_page()
            for b in reopen:
                b["ytop"] = y
        y -= lead
        cur.append(("text", item, y))
    elif t == "trow":
        rowh = item["rowh"]
        if y - rowh < MB:
            new_page()
        y -= rowh
        cur.append(("trow", item, y, rowh))

# close remaining
for b in open_boxes:
    cur.append(("boxdraw", b["color"], b["ytop"], y - 4))
if cur:
    pages.append(cur)

# ---------- Emit PDF ----------
FONTS = {"R": "F1", "B": "F2"}


def draw_page(items):
    # separate fills (boxes) first, then text/lines on top
    out = []
    # fills
    for it in items:
        if it[0] == "boxdraw":
            _, color, ytop, ybot = it
            out.append(f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} rg")
            x = ML - 6
            w = CW + 12
            h = ytop - ybot + 8
            out.append(f"{x:.2f} {ybot-4:.2f} {w:.2f} {h:.2f} re f")
        elif it[0] == "band":
            _, text, y = it
            out.append("0.106 0.31 0.541 rg")
            out.append(f"{ML-6:.2f} {y-8:.2f} {CW+12:.2f} 30 re f")
        elif it[0] == "trow":
            _, item, y, rowh = it
            if item["shade"]:
                sc = item["shade"]
                out.append(f"{sc[0]:.3f} {sc[1]:.3f} {sc[2]:.3f} rg")
                out.append(f"{ML-3:.2f} {y-3:.2f} {CW+6:.2f} {rowh:.2f} re f")
            elif item["bold"]:
                out.append("0.106 0.31 0.541 rg")
                out.append(f"{ML-3:.2f} {y-3:.2f} {CW+6:.2f} {rowh:.2f} re f")
    # table grid lines
    out.append("0.7 0.78 0.71 RG 0.5 w")
    for it in items:
        if it[0] == "trow":
            _, item, y, rowh = it
            ncol = item["ncol"]
            colw = item["colw"]
            for c in range(ncol + 1):
                x = ML - 3 + c * colw
                out.append(f"{x:.2f} {y-3:.2f} m {x:.2f} {y-3+rowh:.2f} l S")
            out.append(f"{ML-3:.2f} {y-3:.2f} m {ML-3+ncol*colw:.2f} {y-3:.2f} l S")
            out.append(f"{ML-3:.2f} {y-3+rowh:.2f} m {ML-3+ncol*colw:.2f} {y-3+rowh:.2f} l S")
    # hlines
    for it in items:
        if it[0] == "hline":
            _, y = it
            out.append("0.8 0.8 0.8 RG 1 w")
            out.append(f"{ML:.2f} {y:.2f} m {PW-MR:.2f} {y:.2f} l S")
    # text
    out.append("BT")
    curcolor = None
    for it in items:
        if it[0] == "band":
            _, text, y = it
            out.append("1 1 1 rg")
            curcolor = (1, 1, 1)
            out.append("/F2 17 Tf")
            out.append(f"1 0 0 1 {ML+4:.2f} {y:.2f} Tm")
            out.append(f"({esc(clean(text))}) Tj")
        elif it[0] == "text":
            _, item, y = it
            size = item["size"]
            font = item["font"]
            text = item["text"]
            color = item.get("color") or (0, 0, 0)
            fkey = FONTS[font]
            if color != curcolor:
                out.append(f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} rg")
                curcolor = color
            x = ML + item.get("indent", 0)
            if item.get("center"):
                x = ML + (CW - tw(text, size, font)) / 2.0
            out.append(f"/{fkey} {size:.2f} Tf")
            out.append(f"1 0 0 1 {x:.2f} {y:.2f} Tm")
            out.append(f"({esc(text)}) Tj")
        elif it[0] == "trow":
            _, item, y, rowh = it
            cells = item["cells"]
            colw = item["colw"]
            bold = item["bold"]
            fkey = "F2" if bold else "F1"
            color = (1, 1, 1) if bold else (0.1, 0.1, 0.1)
            if color != curcolor:
                out.append(f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} rg")
                curcolor = color
            out.append(f"/{fkey} 8.5 Tf")
            for ci, celllines in enumerate(cells):
                cx = ML - 3 + ci * colw + 4
                cy = y + rowh - 12
                for wl in celllines:
                    out.append(f"1 0 0 1 {cx:.2f} {cy:.2f} Tm")
                    out.append(f"({esc(wl)}) Tj")
                    cy -= 11
    out.append("ET")
    return "\n".join(out)


obj = {}
nid = 1
cat = nid; nid += 1
ptree = nid; nid += 1
f1 = nid; nid += 1
f2 = nid; nid += 1
pageids = []
contids = []
for _ in pages:
    pageids.append(nid); nid += 1
    contids.append(nid); nid += 1

obj[cat] = f"<< /Type /Catalog /Pages {ptree} 0 R >>".encode()
kids = " ".join(f"{p} 0 R" for p in pageids)
obj[ptree] = f"<< /Type /Pages /Count {len(pageids)} /Kids [{kids}] >>".encode()
obj[f1] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
obj[f2] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
for pi, page in enumerate(pages):
    stream = draw_page(page).encode("latin-1", "replace")
    obj[contids[pi]] = (f"<< /Length {len(stream)} >>\nstream\n".encode() + stream + b"\nendstream")
    res = f"<< /Font << /F1 {f1} 0 R /F2 {f2} 0 R >> >>"
    obj[pageids[pi]] = (f"<< /Type /Page /Parent {ptree} 0 R /MediaBox [0 0 {PW} {PH}] "
                        f"/Resources {res} /Contents {contids[pi]} 0 R >>").encode()

buf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
offs = {}
for oid in range(1, nid):
    offs[oid] = len(buf)
    buf += f"{oid} 0 obj\n".encode() + obj[oid] + b"\nendobj\n"
xref = len(buf)
buf += f"xref\n0 {nid}\n".encode() + b"0000000000 65535 f \n"
for oid in range(1, nid):
    buf += f"{offs[oid]:010d} 00000 n \n".encode()
buf += b"trailer\n" + f"<< /Size {nid} /Root {cat} 0 R >>\n".encode()
buf += b"startxref\n" + f"{xref}\n".encode() + b"%%EOF"
with open(PDF_OUT, "wb") as f:
    f.write(buf)
print(f"Wrote {PDF_OUT} ({len(pages)} pages, {len(buf)} bytes)")
