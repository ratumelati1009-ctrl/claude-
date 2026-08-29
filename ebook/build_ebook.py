#!/usr/bin/env python3
"""Build a styled HTML and a self-contained PDF ebook from the Markdown manuscript.
No third-party dependencies required."""
import re
import html as html_lib

SRC = "top-tips-for-personal-development.md"
HTML_OUT = "Top-Tips-for-Personal-Development.html"
PDF_OUT = "Top-Tips-for-Personal-Development.pdf"

AUTHOR = "Daniel Tesfamariam"
EMAIL = "dannyshalomnebiy@gmail.com"

with open(SRC, encoding="utf-8") as f:
    raw = f.read()

# ---------- Parse markdown into a simple block list ----------
# Blocks: ('h1', text), ('h2', text), ('p', text), ('li', text),
#         ('quote_title', text), ('quote', text), ('hr', None)
lines = raw.split("\n")
blocks = []
i = 0
while i < len(lines):
    line = lines[i].rstrip("\n")
    stripped = line.strip()
    if not stripped:
        i += 1
        continue
    if stripped == "---":
        blocks.append(("hr", None))
    elif stripped.startswith("# "):
        blocks.append(("h1", stripped[2:].strip()))
    elif stripped.startswith("## "):
        blocks.append(("h2", stripped[3:].strip()))
    elif stripped.startswith("> "):
        content = stripped[2:].strip()
        if content.startswith("**") and content.endswith("**"):
            blocks.append(("quote_title", content.strip("*").strip()))
        elif content == "":
            pass
        else:
            blocks.append(("quote", content))
    elif stripped.startswith("- "):
        blocks.append(("li", stripped[2:].strip()))
    else:
        blocks.append(("p", stripped))
    i += 1


def strip_md(text):
    """Remove inline markdown emphasis markers, return plain text."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    return text


# ---------- HTML output ----------
def inline_html(text):
    text = html_lib.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


html_parts = []
in_list = False
for kind, text in blocks:
    if kind != "li" and in_list:
        html_parts.append("</ul>")
        in_list = False
    if kind == "h1":
        html_parts.append(f"<h1>{inline_html(text)}</h1>")
    elif kind == "h2":
        html_parts.append(f'<h2>{inline_html(text)}</h2>')
    elif kind == "p":
        html_parts.append(f"<p>{inline_html(text)}</p>")
    elif kind == "li":
        if not in_list:
            html_parts.append("<ul>")
            in_list = True
        html_parts.append(f"<li>{inline_html(text)}</li>")
    elif kind == "quote_title":
        html_parts.append(f'<div class="story"><p class="story-title">{inline_html(text)}</p>')
        html_parts.append("__STORY_OPEN__")
    elif kind == "quote":
        html_parts.append(f"<p>{inline_html(text)}</p>")
    elif kind == "hr":
        html_parts.append("<hr/>")
if in_list:
    html_parts.append("</ul>")

# Close story divs: a story block is quote_title followed by quote paragraphs
# Simplify: rebuild with proper story wrapping
html_body = []
i = 0
parts = [p for p in html_parts if p != "__STORY_OPEN__"]
# Re-detect stories to wrap them properly
html_body = []
idx = 0
raw_parts = html_parts
while idx < len(raw_parts):
    part = raw_parts[idx]
    if part.startswith('<div class="story">'):
        html_body.append(part)
        idx += 1
        if idx < len(raw_parts) and raw_parts[idx] == "__STORY_OPEN__":
            idx += 1
        # consume following <p> until hr/h1/h2
        while idx < len(raw_parts) and raw_parts[idx].startswith("<p>"):
            html_body.append(raw_parts[idx])
            idx += 1
        html_body.append("</div>")
    elif part == "__STORY_OPEN__":
        idx += 1
    else:
        html_body.append(part)
        idx += 1

html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="author" content="{AUTHOR}"/>
<title>Top Tips for Personal Development</title>
<style>
  body {{ font-family: Georgia, 'Times New Roman', serif; line-height: 1.7;
          color: #1a1a1a; max-width: 720px; margin: 0 auto; padding: 48px 28px; }}
  h1 {{ font-size: 2.4em; text-align: center; margin: 0.2em 0 0.1em; line-height:1.2; }}
  h2 {{ font-size: 1.5em; margin-top: 2em; border-bottom: 2px solid #ddd;
        padding-bottom: 0.2em; }}
  p {{ margin: 0.8em 0; text-align: justify; }}
  ul {{ margin: 0.6em 0 1em 1.4em; }}
  li {{ margin: 0.3em 0; }}
  hr {{ border: none; border-top: 1px solid #e0e0e0; margin: 2em 0; }}
  .story {{ background: #f6f4ee; border-left: 4px solid #b58a3c;
            padding: 14px 20px; margin: 1.6em 0; border-radius: 4px; }}
  .story-title {{ font-weight: bold; color: #8a6320; margin-top: 0; }}
  .story p {{ font-style: italic; }}
  .byline {{ text-align: center; font-size: 1.1em; color: #444; margin-top: 0.4em; }}
  .email {{ text-align: center; color: #666; font-style: italic; }}
  @media print {{ body {{ max-width: none; }} }}
</style>
</head>
<body>
{chr(10).join(html_body)}
</body>
</html>"""

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html_doc)
print(f"Wrote {HTML_OUT}")


# ---------- PDF output (pure python) ----------
# Helvetica AFM widths (units per 1000). Covers ASCII 32..126.
HELV_W = [278,278,355,556,556,889,667,191,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,278,278,584,584,584,556,1015,667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611,278,278,278,469,556,333,556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500,334,260,334,584]
HELVB_W = [278,333,474,556,556,889,722,238,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,333,333,584,584,584,611,975,722,722,722,722,667,611,778,722,278,556,722,611,833,722,778,667,778,722,667,611,722,667,944,667,667,611,333,278,333,584,556,333,556,611,556,611,556,333,611,611,278,278,556,278,889,611,611,611,611,389,556,333,611,556,778,556,556,500,389,280,389,584]
HELVO_W = HELV_W  # oblique same widths


def char_width(ch, font):
    o = ord(ch)
    if 32 <= o <= 126:
        idx = o - 32
        if font == "B":
            return HELVB_W[idx]
        return HELV_W[idx]
    return 556  # default for non-ascii


def text_width(s, size, font):
    return sum(char_width(c, font) for c in s) * size / 1000.0


def wrap(text, size, font, max_w):
    words = text.split()
    out, cur = [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if text_width(trial, size, font) <= max_w or not cur:
            cur = trial
        else:
            out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out or [""]


# Convert non-latin1 chars so they encode in WinAnsi PDF strings
REPL = {"\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"',
        "\u2014": "-", "\u2013": "-", "\u2026": "...", "\u2022": "-"}


def clean(s):
    for k, v in REPL.items():
        s = s.replace(k, v)
    return "".join(c if ord(c) < 256 else "?" for c in s)


def esc(s):
    return s.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


# Page geometry (Letter)
PW, PH = 612, 792
ML, MR, MT, MB = 72, 72, 72, 72
CW = PW - ML - MR

# Build a flat list of "lines to render": (font, size, text, extra_gap_before, indent, is_title_center)
render = []  # each: dict


def add_spacer(h):
    render.append({"type": "space", "h": h})


def add_line(text, font, size, leading, indent=0, center=False, color=None):
    render.append({"type": "line", "text": text, "font": font, "size": size,
                   "leading": leading, "indent": indent, "center": center, "color": color})


title_mode = False
in_story = False
for kind, text in blocks:
    if kind == "hr":
        add_spacer(6)
        continue
    if kind == "h1":
        add_spacer(40)
        for wl in wrap(clean(text), 30, "B", CW):
            add_line(wl, "B", 30, 38, center=True)
        add_spacer(6)
        continue
    if kind == "h2":
        add_spacer(22)
        for wl in wrap(clean(text), 18, "B", CW):
            add_line(wl, "B", 18, 24)
        add_spacer(6)
        continue
    if kind == "p":
        # byline / email detection (italic centered small)
        plain = clean(strip_md(text))
        if AUTHOR in text and text.startswith("**By"):
            add_line(plain, "B", 15, 22, center=True)
            add_spacer(4)
        elif EMAIL in text:
            for wl in wrap(plain, 12, "O", CW):
                add_line(wl, "O", 12, 18, center=True, color=(0.3, 0.3, 0.3))
            add_spacer(4)
        else:
            for wl in wrap(plain, 11.5, "R", CW):
                add_line(wl, "R", 11.5, 17)
            add_spacer(7)
        continue
    if kind == "li":
        plain = clean(strip_md(text))
        wrapped = wrap(plain, 11.5, "R", CW - 18)
        for j, wl in enumerate(wrapped):
            prefix = "\u2022 " if j == 0 else "  "
            add_line(("- " if j == 0 else "  ") + wl, "R", 11.5, 16, indent=14)
        add_spacer(2)
        continue
    if kind == "quote_title":
        add_spacer(10)
        for wl in wrap(clean(text), 12.5, "B", CW - 24):
            add_line(wl, "B", 12.5, 18, indent=14, color=(0.54, 0.39, 0.13))
        add_spacer(3)
        continue
    if kind == "quote":
        plain = clean(strip_md(text))
        for wl in wrap(plain, 11, "O", CW - 24):
            add_line(wl, "O", 11, 16.5, indent=14, color=(0.2, 0.2, 0.2))
        add_spacer(8)
        continue

# ---------- Paginate ----------
pages = []
cur_page = []
y = PH - MT
for item in render:
    if item["type"] == "space":
        y -= item["h"]
        if y < MB:
            pages.append(cur_page)
            cur_page = []
            y = PH - MT
        continue
    lead = item["leading"]
    if y - lead < MB:
        pages.append(cur_page)
        cur_page = []
        y = PH - MT
    y -= lead
    cur_page.append((item, y))
if cur_page:
    pages.append(cur_page)

# ---------- Emit PDF ----------
FONTS = {"R": "F1", "B": "F2", "O": "F3"}


def content_stream(page_items):
    out = ["BT"]
    cur_font = None
    cur_size = None
    cur_color = None
    for item, y in page_items:
        size = item["size"]
        font = item["font"]
        text = item["text"]
        indent = item.get("indent", 0)
        color = item.get("color")
        if item.get("center"):
            x = ML + (CW - text_width(text, size, font)) / 2.0
        else:
            x = ML + indent
        # color
        c = color if color else (0, 0, 0)
        if c != cur_color:
            out.append(f"{c[0]:.3f} {c[1]:.3f} {c[2]:.3f} rg")
            cur_color = c
        out.append(f"/{FONTS[font]} {size:.2f} Tf")
        out.append(f"1 0 0 1 {x:.2f} {y:.2f} Tm")
        out.append(f"({esc(text)}) Tj")
    out.append("ET")
    return "\n".join(out)


objects = []  # list of (id, bytes)


def add_obj(body: bytes):
    objects.append(body)
    return len(objects)  # id


# Reserve: 1 catalog, 2 pages tree, fonts, then page objs + content objs
# We'll assign ids sequentially.
font_r = None
# Build font objects
# Order: catalog(1), pagestree(2), F1(3), F2(4), F3(5), then pages + contents
obj_bytes = {}
next_id = 1
catalog_id = next_id; next_id += 1
pages_id = next_id; next_id += 1
f1_id = next_id; next_id += 1
f2_id = next_id; next_id += 1
f3_id = next_id; next_id += 1

page_ids = []
content_ids = []
for _ in pages:
    page_ids.append(next_id); next_id += 1
    content_ids.append(next_id); next_id += 1

obj_bytes[catalog_id] = f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("latin-1")
kids = " ".join(f"{pid} 0 R" for pid in page_ids)
obj_bytes[pages_id] = (f"<< /Type /Pages /Count {len(page_ids)} /Kids [{kids}] >>").encode("latin-1")
obj_bytes[f1_id] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
obj_bytes[f2_id] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
obj_bytes[f3_id] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>"

for pi, page in enumerate(pages):
    stream = content_stream(page).encode("latin-1")
    obj_bytes[content_ids[pi]] = (
        f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1") + stream + b"\nendstream"
    )
    res = (f"<< /Font << /F1 {f1_id} 0 R /F2 {f2_id} 0 R /F3 {f3_id} 0 R >> >>")
    obj_bytes[page_ids[pi]] = (
        f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {PW} {PH}] "
        f"/Resources {res} /Contents {content_ids[pi]} 0 R >>"
    ).encode("latin-1")

# Serialize
buf = bytearray()
buf += b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
offsets = {}
for oid in range(1, next_id):
    offsets[oid] = len(buf)
    buf += f"{oid} 0 obj\n".encode("latin-1")
    buf += obj_bytes[oid]
    buf += b"\nendobj\n"

xref_pos = len(buf)
count = next_id  # objects 0..next_id-1
buf += f"xref\n0 {count}\n".encode("latin-1")
buf += b"0000000000 65535 f \n"
for oid in range(1, next_id):
    buf += f"{offsets[oid]:010d} 00000 n \n".encode("latin-1")
buf += b"trailer\n"
buf += f"<< /Size {count} /Root {catalog_id} 0 R >>\n".encode("latin-1")
buf += b"startxref\n"
buf += f"{xref_pos}\n".encode("latin-1")
buf += b"%%EOF"

with open(PDF_OUT, "wb") as f:
    f.write(buf)
print(f"Wrote {PDF_OUT} ({len(pages)} pages, {len(buf)} bytes)")
