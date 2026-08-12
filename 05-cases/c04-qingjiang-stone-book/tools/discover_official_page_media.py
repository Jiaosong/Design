#!/usr/bin/env python3
"""Discover image assets embedded in one project-approved official article body.

This tool extracts and downloads images only from the article content container
`.v_news_content`, preserving document order and producing a contact sheet for
human node identification. It deliberately does NOT infer a Node PASS from DOM
adjacency or article text.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

PAGE_URL = "https://www.eslygroup.com/media_focus/3229.html"
ARTICLE_CLASS = "v_news_content"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "official-page-media-discovery" / "3229"
ORIGINALS = OUT / "originals"


class ArticleImgParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images: list[dict[str, str]] = []
        self.article_depth = 0
        self.article_found = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {k.lower(): (v or "") for k, v in attrs}
        tag_lower = tag.lower()

        if tag_lower == "div":
            classes = set(data.get("class", "").split())
            if self.article_depth > 0:
                self.article_depth += 1
            elif ARTICLE_CLASS in classes:
                self.article_depth = 1
                self.article_found = True

        if tag_lower != "img" or self.article_depth <= 0:
            return
        src = data.get("src") or data.get("data-src") or data.get("data-original")
        if not src:
            return
        self.images.append({
            "src": src,
            "alt": data.get("alt", ""),
            "title": data.get("title", ""),
        })

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "div" and self.article_depth > 0:
            self.article_depth -= 1


@dataclass
class ImageRecord:
    order: int
    url: str
    alt: str
    title: str
    filename: str
    bytes: int
    sha256: str
    width: int
    height: int
    orientation: str


def request_bytes(url: str, accept: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 OLEANDER-C04-Official-Page-Media/1.1",
            "Accept": accept,
            "Referer": PAGE_URL,
        },
    )
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read()


def normalize_url(src: str) -> str:
    return urllib.parse.urljoin(PAGE_URL, src.strip())


def candidate_url(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc not in {"www.eslygroup.com", "eslygroup.com"}:
        return False
    lower = parsed.path.lower()
    if not lower.endswith((".jpg", ".jpeg", ".png", ".webp")):
        return False
    return "/uploadfile/" in lower or "/uploads/" in lower or "/upload/" in lower


def reset_output() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    ORIGINALS.mkdir(parents=True, exist_ok=True)


def make_sheet(records: list[ImageRecord]) -> None:
    if not records:
        return
    cell_w, cell_h = 430, 330
    cols = 2
    rows = (len(records) + cols - 1) // cols
    margin = 20
    label_h = 62
    sheet = Image.new("RGB", (cols * cell_w + (cols + 1) * margin, rows * (cell_h + label_h) + (rows + 1) * margin), "white")
    draw = ImageDraw.Draw(sheet)
    for i, record in enumerate(records):
        row, col = divmod(i, cols)
        x = margin + col * (cell_w + margin)
        y = margin + row * (cell_h + label_h)
        image_path = ORIGINALS / record.filename
        with Image.open(image_path) as src:
            img = ImageOps.exif_transpose(src).convert("RGB")
            thumb = ImageOps.contain(img, (cell_w, cell_h))
        sheet.paste(thumb, (x + (cell_w - thumb.width) // 2, y + (cell_h - thumb.height) // 2))
        label = f"ARTICLE #{record.order:02d}  {record.width}x{record.height}\n{record.filename}"
        draw.text((x, y + cell_h + 4), label, fill="black")
    sheet.save(OUT / "CONTACT-SHEET.jpg", quality=92)


def main() -> int:
    reset_output()
    html_bytes = request_bytes(PAGE_URL, "text/html,application/xhtml+xml")
    html = html_bytes.decode("utf-8", errors="replace")
    (OUT / "page.html").write_text(html, encoding="utf-8")

    parser = ArticleImgParser()
    parser.feed(html)
    if not parser.article_found:
        raise RuntimeError(f"article container .{ARTICLE_CLASS} not found")

    ordered: list[dict[str, str]] = []
    seen: set[str] = set()
    for image in parser.images:
        url = normalize_url(image["src"])
        if url in seen or not candidate_url(url):
            continue
        seen.add(url)
        ordered.append({**image, "url": url})

    records: list[ImageRecord] = []
    failures: list[str] = []
    for order, image in enumerate(ordered, start=1):
        try:
            data = request_bytes(image["url"], "image/avif,image/webp,image/apng,image/*,*/*;q=0.8")
            suffix = Path(urllib.parse.urlparse(image["url"]).path).suffix.lower() or ".jpg"
            filename = f"{order:02d}{suffix}"
            path = ORIGINALS / filename
            path.write_bytes(data)
            with Image.open(path) as src:
                img = ImageOps.exif_transpose(src)
                width, height = img.size
            records.append(ImageRecord(
                order=order,
                url=image["url"],
                alt=image["alt"],
                title=image["title"],
                filename=filename,
                bytes=len(data),
                sha256=hashlib.sha256(data).hexdigest(),
                width=width,
                height=height,
                orientation="landscape" if width > height else "portrait" if height > width else "square",
            ))
        except Exception as exc:
            failures.append(f"#{order} {image['url']}: {type(exc).__name__}: {exc}")

    payload = {
        "schema": "oleander.c04.official-page-media-discovery.v0.2",
        "page_url": PAGE_URL,
        "article_selector": f".{ARTICLE_CLASS}",
        "policy": {
            "rights": "PROJECT_USE_APPROVED_OFFICIAL_WEB",
            "scope": "ARTICLE_BODY_ONLY",
            "node_pass_inferred": False,
            "dom_adjacency_is_not_node_evidence": True,
        },
        "images": [asdict(record) for record in records],
        "failures": failures,
    }
    (OUT / "DISCOVERY.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# C04 Official Page Media Discovery｜3229",
        "",
        f"Source: {PAGE_URL}",
        f"Scope: article body `.{ARTICLE_CLASS}` only.",
        "",
        "Machine extraction only. Image order/DOM adjacency does not establish R13/R06 Node PASS.",
        "",
        "| Article order | px | Bytes | SHA256 | URL |",
        "|---:|---:|---:|---|---|",
    ]
    for record in records:
        lines.append(f"| {record.order} | {record.width}×{record.height} | {record.bytes} | `{record.sha256}` | {record.url} |")
    if failures:
        lines.extend(["", "## Failures", *[f"- {item}" for item in failures]])
    (OUT / "DISCOVERY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    make_sheet(records)

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 1 if not records or failures else 0


if __name__ == "__main__":
    sys.exit(main())
