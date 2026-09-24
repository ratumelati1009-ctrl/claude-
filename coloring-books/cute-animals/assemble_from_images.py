"""
assemble_from_images.py — compile AI-generated (or scanned) coloring-page PNGs
into a print-ready 8.5 x 11 in, 300-DPI PDF for Amazon KDP. Zero dependencies.

USAGE
  1. Put your images in ./img as page_01.png ... page_42.png
     (JPEGs also OK: page_01.jpg). Optionally img/cover.png.
  2. Run:  python3 assemble_from_images.py
  3. Output: Cute-Animals-FINAL.pdf  (cover first if present, then pages in order)

Each image is centered and scaled to fit the full 8.5x11 page. PNG (RGB / RGBA /
grey) and baseline JPEG are embedded directly into the PDF.

NOTE: This is the tool to use once you have the polished AI images from
AI_IMAGE_PROMPTS.md. It does NOT generate art itself.
"""
from __future__ import annotations
import os, struct, zlib, glob, sys

DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(DIR, "img")
OUT = os.path.join(DIR, "Cute-Animals-FINAL.pdf")

PAGE_W = 8.5 * 72
PAGE_H = 11.0 * 72


# ---------------------------------------------------------------------------
# image readers -> (width, height, colorspace, bits, raw_rgb_or_jpeg, is_jpeg)
# ---------------------------------------------------------------------------
def read_png(path):
    with open(path, "rb") as f:
        data = f.read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    pos = 8
    width = height = bitdepth = colortype = None
    idat = bytearray()
    palette = None
    trns = None
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + length]
        if ctype == b"IHDR":
            width, height, bitdepth, colortype = struct.unpack(">IIBB", chunk[:10])
        elif ctype == b"PLTE":
            palette = chunk
        elif ctype == b"tRNS":
            trns = chunk
        elif ctype == b"IDAT":
            idat += chunk
        elif ctype == b"IEND":
            break
        pos += 12 + length
    raw = zlib.decompress(bytes(idat))
    # channels per colortype
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[colortype]
    bpp = max(1, ch * bitdepth // 8)
    stride = (width * ch * bitdepth + 7) // 8
    # de-filter (supports 8-bit; 16-bit downsampled)
    out = bytearray()
    prev = bytearray(stride)
    p = 0
    for _ in range(height):
        ftype = raw[p]; p += 1
        line = bytearray(raw[p:p + stride]); p += stride
        _unfilter(line, prev, ftype, bpp)
        out += line
        prev = line
    # convert to RGB 8-bit
    rgb = _to_rgb(out, width, height, ch, bitdepth, colortype, palette)
    return width, height, rgb, False


def _unfilter(line, prev, ftype, bpp):
    if ftype == 0:
        return
    for i in range(len(line)):
        a = line[i - bpp] if i >= bpp else 0
        b = prev[i]
        c = prev[i - bpp] if i >= bpp else 0
        x = line[i]
        if ftype == 1:
            line[i] = (x + a) & 0xFF
        elif ftype == 2:
            line[i] = (x + b) & 0xFF
        elif ftype == 3:
            line[i] = (x + ((a + b) >> 1)) & 0xFF
        elif ftype == 4:
            pp = a + b - c
            pa, pb, pc = abs(pp - a), abs(pp - b), abs(pp - c)
            pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
            line[i] = (x + pr) & 0xFF


def _to_rgb(buf, w, h, ch, bd, ct, palette):
    rgb = bytearray(w * h * 3)
    step = bd // 8 if bd >= 8 else 1
    def sample(v):  # collapse 16-bit to 8-bit
        return v
    if ct == 2:  # RGB
        for i in range(w * h):
            rgb[i * 3:i * 3 + 3] = buf[i * ch * step:i * ch * step + 3][:3] if bd == 8 else \
                bytes([buf[(i * ch) * 2], buf[(i * ch + 1) * 2], buf[(i * ch + 2) * 2]])
    elif ct == 6:  # RGBA -> composite on white
        for i in range(w * h):
            base = i * ch * step
            if bd == 8:
                r, g, b, a = buf[base], buf[base + 1], buf[base + 2], buf[base + 3]
            else:
                r, g, b, a = buf[base], buf[base + 2], buf[base + 4], buf[base + 6]
            af = a / 255.0
            rgb[i * 3] = int(r * af + 255 * (1 - af))
            rgb[i * 3 + 1] = int(g * af + 255 * (1 - af))
            rgb[i * 3 + 2] = int(b * af + 255 * (1 - af))
    elif ct == 0:  # grey
        for i in range(w * h):
            v = buf[i * step]
            rgb[i * 3] = rgb[i * 3 + 1] = rgb[i * 3 + 2] = v
    elif ct == 4:  # grey+alpha
        for i in range(w * h):
            v = buf[i * 2 * step]; a = buf[i * 2 * step + step]
            af = a / 255.0
            g = int(v * af + 255 * (1 - af))
            rgb[i * 3] = rgb[i * 3 + 1] = rgb[i * 3 + 2] = g
    elif ct == 3:  # palette
        for i in range(w * h):
            idx = buf[i]
            rgb[i * 3:i * 3 + 3] = palette[idx * 3:idx * 3 + 3]
    return bytes(rgb)


def read_jpeg(path):
    """Embed JPEG bytes directly; parse SOF for dimensions."""
    with open(path, "rb") as f:
        data = f.read()
    i = 2
    w = h = None
    while i < len(data):
        if data[i] != 0xFF:
            i += 1; continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3):
            h = struct.unpack(">H", data[i + 5:i + 7])[0]
            w = struct.unpack(">H", data[i + 7:i + 9])[0]
            break
        seglen = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + seglen
    return w, h, data, True


# ---------------------------------------------------------------------------
# PDF writer with images
# ---------------------------------------------------------------------------
def build(images):
    objects = []
    def add(b):
        objects.append(b); return len(objects)
    objects.append(b""); objects.append(b"")  # catalog=1, pages=2
    catalog, pages_node = 1, 2

    page_nums = []
    for (w, h, payload, is_jpeg) in images:
        if is_jpeg:
            stream = payload
            filt = b"/DCTDecode"
        else:
            stream = zlib.compress(payload, 9)
            filt = b"/FlateDecode"
        img_num = add(
            b"<< /Type /XObject /Subtype /Image /Width " + str(w).encode() +
            b" /Height " + str(h).encode() +
            b" /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter " + filt +
            b" /Length " + str(len(stream)).encode() + b" >>\nstream\n" +
            stream + b"\nendstream"
        )
        # scale to fit page, centered
        scale = min(PAGE_W / w, PAGE_H / h)
        dw, dh = w * scale, h * scale
        ox, oy = (PAGE_W - dw) / 2, (PAGE_H - dh) / 2
        content = (f"q\n1 1 1 rg 0 0 {PAGE_W:.2f} {PAGE_H:.2f} re f\n"
                   f"{dw:.2f} 0 0 {dh:.2f} {ox:.2f} {oy:.2f} cm\n"
                   f"/Im0 Do\nQ").encode()
        cont_num = add(b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n"
                       + content + b"\nendstream")
        page_num = add(
            (f"<< /Type /Page /Parent {pages_node} 0 R "
             f"/MediaBox [0 0 {PAGE_W:.2f} {PAGE_H:.2f}] "
             f"/Resources << /XObject << /Im0 {img_num} 0 R >> >> "
             f"/Contents {cont_num} 0 R >>").encode())
        page_nums.append(page_num)

    kids = " ".join(f"{n} 0 R" for n in page_nums)
    objects[pages_node - 1] = (f"<< /Type /Pages /Kids [{kids}] /Count {len(page_nums)} >>").encode()
    objects[catalog - 1] = (f"<< /Type /Catalog /Pages {pages_node} 0 R >>").encode()

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0] * (len(objects) + 1)
    for i, body in enumerate(objects, 1):
        offsets[i] = len(out)
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    n = len(objects) + 1
    out += f"xref\n0 {n}\n".encode() + b"0000000000 65535 f \n"
    for i in range(1, n):
        out += f"{offsets[i]:010d} 00000 n \n".encode()
    out += (f"trailer\n<< /Size {n} /Root {catalog} 0 R >>\nstartxref\n{xref}\n%%EOF").encode()
    with open(OUT, "wb") as f:
        f.write(out)
    return len(out)


def load(path):
    if path.lower().endswith((".jpg", ".jpeg")):
        return read_jpeg(path)
    return read_png(path)


def main():
    if not os.path.isdir(IMG_DIR):
        print(f"No img/ folder found. Create {IMG_DIR}/ and add page_01.png ... page_42.png")
        print("(See AI_IMAGE_PROMPTS.md to generate the images.)")
        sys.exit(1)
    images = []
    cover = None
    for ext in ("png", "jpg", "jpeg"):
        c = os.path.join(IMG_DIR, f"cover.{ext}")
        if os.path.exists(c):
            cover = c; break
    if cover:
        images.append(load(cover))
        print("cover:", os.path.basename(cover))
    files = sorted(glob.glob(os.path.join(IMG_DIR, "page_*.*")))
    if not files:
        print("No page_*.png images found in img/. Add them first.")
        sys.exit(1)
    for fp in files:
        images.append(load(fp))
        print("added:", os.path.basename(fp))
    size = build(images)
    print(f"\nWrote {OUT}  ({len(images)} pages, {size//1024} KB)")


if __name__ == "__main__":
    main()
