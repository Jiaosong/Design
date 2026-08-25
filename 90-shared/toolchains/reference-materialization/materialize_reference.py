#!/usr/bin/env python3
"""Materialize a reference source into local bytes for OLEANDER fidelity review.

Supports a public URL or a local file. Produces a SHA-256 manifest and, for PDFs,
optionally renders one page to PNG using pdftoppm or pypdfium2.

This tool does not assert source authority, rights, or fidelity by itself. It only
creates a reproducible local byte copy and a locked reference frame for comparison.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_name_from_url(url: str, fallback: str = "reference.bin") -> str:
    path = urllib.parse.urlparse(url).path
    name = Path(path).name
    return name or fallback


def download(url: str, dest: Path, timeout: int) -> str | None:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "OLEANDER-Reference-Materializer/1.0"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        content_type = response.headers.get_content_type() if response.headers else None
        with dest.open("wb") as f:
            shutil.copyfileobj(response, f)
    return content_type


def render_pdf_page_pdftoppm(pdf: Path, page_1based: int, out_png: Path, dpi: int) -> bool:
    exe = shutil.which("pdftoppm")
    if not exe:
        return False
    prefix = out_png.with_suffix("")
    cmd = [
        exe,
        "-f",
        str(page_1based),
        "-singlefile",
        "-png",
        "-r",
        str(dpi),
        str(pdf),
        str(prefix),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return out_png.exists()


def render_pdf_page_pdfium(pdf: Path, page_1based: int, out_png: Path, dpi: int) -> bool:
    try:
        import pypdfium2 as pdfium
    except Exception:
        return False

    doc = pdfium.PdfDocument(str(pdf))
    index = page_1based - 1
    if index < 0 or index >= len(doc):
        raise IndexError(f"page {page_1based} outside PDF page range 1..{len(doc)}")
    scale = dpi / 72.0
    bitmap = doc[index].render(scale=scale)
    bitmap.to_pil().save(out_png)
    return out_png.exists()


def image_size(path: Path):
    try:
        from PIL import Image

        with Image.open(path) as im:
            return [int(im.width), int(im.height)]
    except Exception:
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--url", help="Public source URL to download")
    source.add_argument("--file", help="Existing local source file")
    parser.add_argument("--out-dir", required=True, help="Destination directory")
    parser.add_argument("--name", help="Destination source filename")
    parser.add_argument("--page", type=int, help="1-based PDF page to lock/render")
    parser.add_argument("--dpi", type=int, default=200, help="PDF render DPI")
    parser.add_argument("--timeout", type=int, default=45, help="URL timeout seconds")
    args = parser.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    source_url = None
    source_original = None
    content_type = None

    if args.url:
        source_url = args.url
        name = args.name or safe_name_from_url(args.url)
        dest = out_dir / name
        try:
            content_type = download(args.url, dest, args.timeout)
        except Exception as exc:
            print(f"MATERIALIZATION_FAILED: {exc}", file=sys.stderr)
            return 2
    else:
        source_original = str(Path(args.file).resolve())
        src_path = Path(args.file).resolve()
        if not src_path.exists():
            print(f"MATERIALIZATION_FAILED: missing local file {src_path}", file=sys.stderr)
            return 2
        name = args.name or src_path.name
        dest = out_dir / name
        if src_path != dest:
            shutil.copy2(src_path, dest)
        content_type = mimetypes.guess_type(dest.name)[0]

    source_sha = sha256_file(dest)
    stat = dest.stat()
    detected_pdf = (content_type == "application/pdf") or dest.suffix.lower() == ".pdf"

    locked_frame = None
    if args.page is not None:
        if not detected_pdf:
            print("MATERIALIZATION_FAILED: --page is only valid for PDF sources", file=sys.stderr)
            return 3

        out_png = out_dir / f"reference_page_{args.page:04d}_{args.dpi}dpi.png"
        renderer = None
        try:
            if render_pdf_page_pdftoppm(dest, args.page, out_png, args.dpi):
                renderer = "pdftoppm"
            elif render_pdf_page_pdfium(dest, args.page, out_png, args.dpi):
                renderer = "pypdfium2"
            else:
                print("MATERIALIZATION_FAILED: no PDF renderer available", file=sys.stderr)
                return 4
        except Exception as exc:
            print(f"MATERIALIZATION_FAILED: PDF render failed: {exc}", file=sys.stderr)
            return 4

        locked_frame = {
            "state": "LOCKED_REFERENCE_FRAME",
            "page_1based": args.page,
            "dpi": args.dpi,
            "renderer": renderer,
            "path": str(out_png),
            "bytes": out_png.stat().st_size,
            "sha256": sha256_file(out_png),
            "pixel_dimensions": image_size(out_png),
        }

    manifest = {
        "schema": "oleander.reference-materialization.v1",
        "status": "MATERIALIZED",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_url": source_url,
        "source_original_local_path": source_original,
        "materialized_source": {
            "state": "MATERIALIZED",
            "path": str(dest),
            "filename": dest.name,
            "bytes": stat.st_size,
            "sha256": source_sha,
            "content_type": content_type,
        },
        "locked_reference_frame": locked_frame,
        "does_not_prove": [
            "SOURCE_AUTHORITY",
            "RIGHTS_CLEARANCE",
            "RECONSTRUCTION_FIDELITY",
            "DESIGN_QUALITY",
        ],
    }

    manifest_path = out_dir / "reference_materialization_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "status": "MATERIALIZED",
                "source": str(dest),
                "source_sha256": source_sha,
                "locked_frame": locked_frame,
                "manifest": str(manifest_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
