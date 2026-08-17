#!/usr/bin/env python3
"""OLEANDER reference reconstruction fidelity diagnostics.

This tool compares already-normalized raster renders of a reference and a
candidate. It is intentionally diagnostic: a low pixel error does not prove
vector editability, technical correctness, engineering validity, field truth,
or design promotion.

Inputs must have the same pixel dimensions. Registration/dewarp belongs to a
separate documented normalization step; this tool will not warp a candidate to
make it look more accurate.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageChops, ImageFilter


def load_rgb(path: Path) -> Image.Image:
    image = Image.open(path)
    if image.mode in {"RGBA", "LA"}:
        background = Image.new("RGBA", image.size, (255, 255, 255, 255))
        image = Image.alpha_composite(background, image.convert("RGBA"))
    return image.convert("RGB")


def array_metrics(reference: np.ndarray, candidate: np.ndarray, tolerance: int) -> dict[str, Any]:
    delta = np.abs(reference.astype(np.int16) - candidate.astype(np.int16))
    per_pixel_max = delta.max(axis=2)
    changed = per_pixel_max > tolerance
    exact_equal = np.all(delta == 0, axis=2)
    flat = delta.astype(np.float64).reshape(-1)

    return {
        "total_pixels": int(reference.shape[0] * reference.shape[1]),
        "exact_equal_pixel_ratio": float(exact_equal.mean()),
        "changed_pixel_ratio_above_tolerance": float(changed.mean()),
        "mean_absolute_channel_error": float(flat.mean()),
        "rmse_channel_error": float(math.sqrt(np.mean(flat * flat))),
        "p95_absolute_channel_error": float(np.percentile(flat, 95)),
        "max_absolute_channel_error": int(delta.max()),
    }


def edge_mask(image: Image.Image, threshold: int = 24) -> np.ndarray:
    edges = image.convert("L").filter(ImageFilter.FIND_EDGES)
    arr = np.asarray(edges, dtype=np.uint8)
    return arr > threshold


def edge_metrics(reference: Image.Image, candidate: Image.Image) -> dict[str, float]:
    a = edge_mask(reference)
    b = edge_mask(candidate)
    union = np.logical_or(a, b)
    disagreement = np.logical_xor(a, b)
    if not union.any():
        return {"edge_disagreement_ratio_of_union": 0.0, "edge_union_pixel_ratio": 0.0}
    return {
        "edge_disagreement_ratio_of_union": float(disagreement.sum() / union.sum()),
        "edge_union_pixel_ratio": float(union.mean()),
    }


def parse_rois(path: Path | None, width: int, height: int) -> list[dict[str, Any]]:
    if path is None:
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    rois = payload.get("rois", payload if isinstance(payload, list) else [])
    parsed = []
    for raw in rois:
        roi = {
            "id": str(raw["id"]),
            "x": int(raw["x"]),
            "y": int(raw["y"]),
            "w": int(raw["w"]),
            "h": int(raw["h"]),
        }
        if roi["w"] <= 0 or roi["h"] <= 0:
            raise ValueError(f"ROI {roi['id']} has non-positive size")
        if roi["x"] < 0 or roi["y"] < 0 or roi["x"] + roi["w"] > width or roi["y"] + roi["h"] > height:
            raise ValueError(f"ROI {roi['id']} is outside the comparison canvas")
        parsed.append(roi)
    return parsed


def save_visuals(reference: Image.Image, candidate: Image.Image, out_dir: Path, tolerance: int) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    Image.blend(reference, candidate, 0.5).save(out_dir / "overlay_50.png")

    difference = ImageChops.difference(reference, candidate)
    difference.save(out_dir / "difference_absolute.png")

    delta = np.asarray(difference, dtype=np.uint8)
    mask = (delta.max(axis=2) > tolerance).astype(np.uint8) * 255
    Image.fromarray(mask, mode="L").save(out_dir / "changed_pixel_mask.png")

    # A magnified diagnostic difference helps reviewers see small residuals.
    magnified = np.clip(delta.astype(np.int16) * 4, 0, 255).astype(np.uint8)
    Image.fromarray(magnified, mode="RGB").save(out_dir / "difference_x4.png")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare normalized reference/candidate renders for OLEANDER reconstruction fidelity.")
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--tolerance", type=int, default=0, help="Per-channel max difference threshold, 0..255")
    parser.add_argument("--rois", type=Path, default=None, help="Optional JSON containing {rois:[{id,x,y,w,h}, ...]}")
    args = parser.parse_args()

    if not 0 <= args.tolerance <= 255:
        parser.error("--tolerance must be between 0 and 255")

    reference = load_rgb(args.reference)
    candidate = load_rgb(args.candidate)

    result: dict[str, Any] = {
        "tool": "oleander-technical-drawing/reference_fidelity.py",
        "reference": str(args.reference),
        "candidate": str(args.candidate),
        "tolerance": args.tolerance,
        "does_not_prove": [
            "vector editability",
            "technical correctness",
            "engineering adequacy",
            "field truth",
            "fabrication or construction permission",
            "design KEEP or promotion",
        ],
    }

    if reference.size != candidate.size:
        result.update({
            "same_canvas": False,
            "reference_size": list(reference.size),
            "candidate_size": list(candidate.size),
            "status": "RF-G1_FAIL_CANVAS_MISMATCH",
        })
        args.out_dir.mkdir(parents=True, exist_ok=True)
        (args.out_dir / "FIDELITY_METRICS.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result, indent=2))
        return 2

    width, height = reference.size
    ref_arr = np.asarray(reference, dtype=np.uint8)
    cand_arr = np.asarray(candidate, dtype=np.uint8)

    result.update({
        "same_canvas": True,
        "canvas": {"width": width, "height": height},
        "global": array_metrics(ref_arr, cand_arr, args.tolerance),
        "edge": edge_metrics(reference, candidate),
        "status": "DIAGNOSTIC_COMPLETE_REVIEW_REQUIRED",
    })

    rois = parse_rois(args.rois, width, height)
    roi_results = []
    for roi in rois:
        x, y, w, h = roi["x"], roi["y"], roi["w"], roi["h"]
        roi_results.append({
            **roi,
            "metrics": array_metrics(ref_arr[y:y+h, x:x+w], cand_arr[y:y+h, x:x+w], args.tolerance),
        })
    if roi_results:
        result["rois"] = roi_results

    save_visuals(reference, candidate, args.out_dir, args.tolerance)
    (args.out_dir / "FIDELITY_METRICS.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
