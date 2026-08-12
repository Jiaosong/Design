#!/usr/bin/env python3
"""C04 official-web media technical audit.

Downloads project-approved official/operator images, records immutable technical
metadata, generates deterministic center-cover crop previews for the three
WS-07A viewport contracts, and writes contact sheets for human visual review.

A generated crop is NOT a visual/composition PASS. The script only establishes
technical evidence: source payload, decoded dimensions, resolution threshold,
and whether each viewport can be rendered without upscaling beyond the source.
"""

from __future__ import annotations

import json
import math
import sys
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "official-media-tech-audit"
ORIGINALS = OUT / "originals"
CROPS = OUT / "crops"
SHEETS = OUT / "contact-sheets"

VIEWPORTS = {
    "1080x1920": (1080, 1920),
    "390x844": (390, 844),
    "844x390": (844, 390),
}

CANDIDATES = [
    {
        "asset_id": "OW-20230616-2a923422a",
        "node": "R05",
        "url": "https://www.eslygroup.com/uploadfile/image/20230616/2a923422a.jpg",
        "role": "R05_HIGH_CANDIDATE",
    },
    {
        "asset_id": "OW-20230711-mnq9o6767b",
        "node": "R05",
        "url": "https://www.eslygroup.com/uploadfile/image/20230711/mnq9o6767b.jpg",
        "role": "R05_HIGH_CANDIDATE",
    },
    {
        "asset_id": "OW-20230718-v0ii0wjlhe",
        "node": "R06",
        "url": "https://www.eslygroup.com/uploadfile/image/20230718/v0ii0wjlhe.jpg",
        "role": "R06_RELATION_REFERENCE_HERO_HOLD",
    },
    {
        "asset_id": "OW-20230619-pbxolmbgx1",
        "node": "R01",
        "url": "https://www.eslygroup.com/uploadfile/image/20230619/pbxolmbgx1.jpg",
        "role": "R01_RELATION_HIGH_CANDIDATE",
    },
]


@dataclass
class CropResult:
    viewport: str
    target_width: int
    target_height: int
    crop_width: int
    crop_height: int
    retained_area_ratio: float
    upscale_required: bool
    output: str


@dataclass
class AssetResult:
    asset_id: str
    node: str
    role: str
    url: str
    source_bytes: int
    width: int
    height: int
    aspect_ratio: float
    long_edge: int
    short_edge: int
    orientation: str
    resolution_gate: str
    crops: list[CropResult]


def ensure_dirs() -> None:
    for path in (OUT, ORIGINALS, CROPS, SHEETS):
        path.mkdir(parents=True, exist_ok=True)


def download(url: str, dest: Path) -> int:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 OLEANDER-C04-Media-Audit/1.0",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as response:
        data = response.read()
    dest.write_bytes(data)
    return len(data)


def cover_box(width: int, height: int, target_w: int, target_h: int) -> tuple[int, int, int, int]:
    src_ratio = width / height
    dst_ratio = target_w / target_h
    if src_ratio > dst_ratio:
        crop_h = height
        crop_w = round(height * dst_ratio)
    else:
        crop_w = width
        crop_h = round(width / dst_ratio)
    left = (width - crop_w) // 2
    top = (height - crop_h) // 2
    return left, top, left + crop_w, top + crop_h


def resolution_gate(long_edge: int) -> str:
    if long_edge >= 4000:
        return "PASS_PREFERRED_GE4000"
    if long_edge >= 2400:
        return "PASS_FALLBACK_GE2400"
    return "FAIL_LT2400"


def create_contact_sheet(asset: AssetResult, original: Image.Image) -> None:
    cell_w, cell_h = 360, 260
    margin = 20
    header_h = 92
    sheet = Image.new("RGB", (cell_w * 4 + margin * 5, cell_h + header_h + margin * 2), "white")
    draw = ImageDraw.Draw(sheet)
    title = f"{asset.asset_id} | {asset.node} | {asset.width}x{asset.height} | {asset.resolution_gate}"
    draw.text((margin, margin), title, fill="black")
    labels = ["ORIGINAL", "1080x1920", "390x844", "844x390"]

    imgs = [original.copy()]
    for crop in asset.crops:
        imgs.append(Image.open(OUT / crop.output).convert("RGB"))

    for i, (label, img) in enumerate(zip(labels, imgs)):
        thumb = ImageOps.contain(img, (cell_w, cell_h))
        x = margin + i * (cell_w + margin)
        y = header_h
        sheet.paste(thumb, (x + (cell_w - thumb.width) // 2, y + (cell_h - thumb.height) // 2))
        draw.text((x, y + cell_h + 4), label, fill="black")

    sheet.save(SHEETS / f"{asset.asset_id}__contact.jpg", quality=90)


def audit(candidate: dict[str, str]) -> AssetResult:
    asset_id = candidate["asset_id"]
    original_path = ORIGINALS / f"{asset_id}.jpg"
    source_bytes = download(candidate["url"], original_path)

    with Image.open(original_path) as img_src:
        img = ImageOps.exif_transpose(img_src).convert("RGB")
        width, height = img.size
        crops: list[CropResult] = []

        for viewport, (target_w, target_h) in VIEWPORTS.items():
            box = cover_box(width, height, target_w, target_h)
            crop_img = img.crop(box)
            crop_w, crop_h = crop_img.size
            upscale_required = crop_w < target_w or crop_h < target_h
            output_rel = Path("crops") / f"{asset_id}__{viewport}.jpg"
            output_path = OUT / output_rel
            # Produce the review viewport deterministically. Upscale state is recorded separately.
            crop_img.resize((target_w, target_h), Image.Resampling.LANCZOS).save(output_path, quality=92)
            crops.append(
                CropResult(
                    viewport=viewport,
                    target_width=target_w,
                    target_height=target_h,
                    crop_width=crop_w,
                    crop_height=crop_h,
                    retained_area_ratio=round((crop_w * crop_h) / (width * height), 4),
                    upscale_required=upscale_required,
                    output=str(output_rel),
                )
            )

        result = AssetResult(
            asset_id=asset_id,
            node=candidate["node"],
            role=candidate["role"],
            url=candidate["url"],
            source_bytes=source_bytes,
            width=width,
            height=height,
            aspect_ratio=round(width / height, 4),
            long_edge=max(width, height),
            short_edge=min(width, height),
            orientation="landscape" if width > height else "portrait" if height > width else "square",
            resolution_gate=resolution_gate(max(width, height)),
            crops=crops,
        )
        create_contact_sheet(result, img)
        return result


def write_markdown(results: list[AssetResult]) -> None:
    lines = [
        "# C04 Official Web Media Technical Audit",
        "",
        "Machine-generated technical evidence. Crop generation is not a visual/composition PASS.",
        "",
        "| Asset | Node | Source px | Bytes | Resolution gate | 1080x1920 upscale | 390x844 upscale | 844x390 upscale |",
        "|---|---|---:|---:|---|---|---|---|",
    ]
    for r in results:
        crop_map = {c.viewport: c for c in r.crops}
        lines.append(
            f"| `{r.asset_id}` | `{r.node}` | {r.width}×{r.height} | {r.source_bytes} | `{r.resolution_gate}` | "
            f"{crop_map['1080x1920'].upscale_required} | {crop_map['390x844'].upscale_required} | {crop_map['844x390'].upscale_required} |"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "- Preferred hero threshold: long edge >= 4000 px.",
        "- Fallback threshold: long edge >= 2400 px.",
        "- Below 2400 px: technical FAIL for current hero contract.",
        "- `upscale_required=true` means the deterministic viewport render exceeds the retained source crop resolution.",
        "- Human review must still judge subject retention, occlusion, landscape-first hierarchy and whether the crop preserves the intended node relation.",
        "",
    ])
    (OUT / "TECH-AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    results: list[AssetResult] = []
    failures: list[str] = []

    for candidate in CANDIDATES:
        try:
            results.append(audit(candidate))
        except Exception as exc:  # fail closed but retain prior evidence
            failures.append(f"{candidate['asset_id']}: {type(exc).__name__}: {exc}")

    payload = {
        "schema": "oleander.c04.official-media-tech-audit.v0.1",
        "policy": {
            "preferred_long_edge": 4000,
            "fallback_long_edge": 2400,
            "crop_mode": "deterministic_center_cover_for_review_only",
            "visual_pass_inferred": False,
        },
        "results": [
            {**asdict(r), "crops": [asdict(c) for c in r.crops]}
            for r in results
        ],
        "failures": failures,
    }
    (OUT / "tech-audit.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(results)

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
