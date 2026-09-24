"""
pdfwriter.py — minimal multi-page PDF writer (no dependencies).

Accepts a list of (width_pt, height_pt, content_stream_str) pages and writes a
valid PDF 1.4 file with a proper xref table. Content streams are produced by
artlib.to_pdf_stream.
"""
from __future__ import annotations
from typing import List, Tuple


def write_pdf(path: str, pages: List[Tuple[float, float, str]]):
    objects = []  # list of raw object body bytes (without "N 0 obj" wrapper)

    def add(obj_bytes: bytes) -> int:
        objects.append(obj_bytes)
        return len(objects)  # 1-based object number

    # Reserve: 1=Catalog, 2=Pages. Page + content objects follow.
    catalog_num = 1
    pages_num = 2
    objects.append(b"")  # placeholder 1
    objects.append(b"")  # placeholder 2

    page_obj_nums = []
    for (w, h, content) in pages:
        cbytes = content.encode("latin-1", "replace")
        content_num = add(
            b"<< /Length " + str(len(cbytes)).encode() + b" >>\nstream\n"
            + cbytes + b"\nendstream"
        )
        page_num = add(
            (
                f"<< /Type /Page /Parent {pages_num} 0 R "
                f"/MediaBox [0 0 {w:.2f} {h:.2f}] "
                f"/Contents {content_num} 0 R "
                f"/Resources << >> >>"
            ).encode()
        )
        page_obj_nums.append(page_num)

    kids = " ".join(f"{n} 0 R" for n in page_obj_nums)
    objects[pages_num - 1] = (
        f"<< /Type /Pages /Kids [{kids}] /Count {len(page_obj_nums)} >>"
    ).encode()
    objects[catalog_num - 1] = (
        f"<< /Type /Catalog /Pages {pages_num} 0 R >>"
    ).encode()

    # serialize
    out = bytearray()
    out += b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
    offsets = [0] * (len(objects) + 1)
    for i, body in enumerate(objects, start=1):
        offsets[i] = len(out)
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"

    xref_pos = len(out)
    n = len(objects) + 1
    out += f"xref\n0 {n}\n".encode()
    out += b"0000000000 65535 f \n"
    for i in range(1, n):
        out += f"{offsets[i]:010d} 00000 n \n".encode()
    out += (
        f"trailer\n<< /Size {n} /Root {catalog_num} 0 R >>\n"
        f"startxref\n{xref_pos}\n%%EOF"
    ).encode()

    with open(path, "wb") as f:
        f.write(out)
    return len(out)
