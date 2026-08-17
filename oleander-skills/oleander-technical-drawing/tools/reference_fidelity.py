#!/usr/bin/env python3
"""OLEANDER reference reconstruction fidelity diagnostics.

Compares already-normalized reference/candidate raster renders without moving,
warping, scaling, or otherwise repairing the candidate. The tool is diagnostic
and may enforce a declared fidelity contract; it cannot grant Design KEEP,
technical correctness, engineering adequacy, field truth, or promotion.

For RF-C3 / PIXEL-EXACT candidates, use tolerance 0 under a locked render
environment. A global similarity percentage is never sufficient: critical ROIs,
edge alignment and spatial mismatch concentration are reported separately.
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


def gray_array(image: Image.Image) -> np.ndarray:
    arr = np.asarray(image, dtype=np.float64)
    # Fixed luminance transform; used only for registration diagnosis.
    return arr[..., 0] * 0.2126 + arr[..., 1] * 0.7152 + arr[..., 2] * 0.0722


def estimate_translation(reference: Image.Image, candidate: Image.Image) -> dict[str, Any]:
    """Estimate integer translation by phase correlation; never apply it."""
    a = gray_array(reference)
    b = gray_array(candidate)
    a = a - a.mean()
    b = b - b.mean()
    fa = np.fft.fft2(a)
    fb = np.fft.fft2(b)
    cross = fa * np.conj(fb)
    denom = np.abs(cross)
    cross = np.divide(cross, denom, out=np.zeros_like(cross), where=denom > 1e-12)
    corr = np.abs(np.fft.ifft2(cross))
    peak_y, peak_x = np.unravel_index(np.argmax(corr), corr.shape)
    h, w = corr.shape
    dy = int(peak_y if peak_y <= h // 2 else peak_y - h)
    dx = int(peak_x if peak_x <= w // 2 else peak_x - w)
    return {
        "suggested_candidate_shift_to_align_px": {"dx": dx, "dy": dy},
        "abs_dx": abs(dx),
        "abs_dy": abs(dy),
        "peak_strength": float(corr[peak_y, peak_x]),
        "note": "diagnostic only; candidate is not translated by this tool",
    }


def edge_mask(image: Image.Image, threshold: int = 24) -> np.ndarray:
    edges = image.convert("L").filter(ImageFilter.FIND_EDGES)
    arr = np.asarray(edges, dtype=np.uint8)
    return arr > threshold


def dilate_bool(mask: np.ndarray, radius: int) -> np.ndarray:
    if radius <= 0:
        return mask
    im = Image.fromarray((mask.astype(np.uint8) * 255), mode="L")
    # MaxFilter size must be odd.
    out = im.filter(ImageFilter.MaxFilter(size=radius * 2 + 1))
    return np.asarray(out, dtype=np.uint8) > 0


def edge_alignment_metrics(reference: Image.Image, candidate: Image.Image) -> dict[str, Any]:
    a = edge_mask(reference)
    b = edge_mask(candidate)
    union = np.logical_or(a, b)
    result: dict[str, Any] = {
        "edge_union_pixel_ratio": float(union.mean()),
        "reference_edge_pixel_ratio": float(a.mean()),
        "candidate_edge_pixel_ratio": float(b.mean()),
    }
    for radius in (0, 1, 2):
        b_near = dilate_bool(b, radius)
        a_near = dilate_bool(a, radius)
        ref_unmatched = np.logical_and(a, np.logical_not(b_near))
        cand_unmatched = np.logical_and(b, np.logical_not(a_near))
        result[f"reference_unmatched_ratio_r{radius}"] = float(ref_unmatched.sum() / max(int(a.sum()), 1))
        result[f"candidate_unmatched_ratio_r{radius}"] = float(cand_unmatched.sum() / max(int(b.sum()), 1))
    if union.any():
        result["edge_disagreement_ratio_of_union_r0"] = float(np.logical_xor(a, b).sum() / union.sum())
    else:
        result["edge_disagreement_ratio_of_union_r0"] = 0.0
    return result


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
            "criticality": str(raw.get("criticality", "UNSPECIFIED")),
        }
        if roi["w"] <= 0 or roi["h"] <= 0:
            raise ValueError(f"ROI {roi['id']} has non-positive size")
        if roi["x"] < 0 or roi["y"] < 0 or roi["x"] + roi["w"] > width or roi["y"] + roi["h"] > height:
            raise ValueError(f"ROI {roi['id']} is outside the comparison canvas")
        parsed.append(roi)
    return parsed


def changed_spatial_metrics(changed: np.ndarray, tile_size: int = 64) -> dict[str, Any]:
    ys, xs = np.nonzero(changed)
    if len(xs) == 0:
        bbox = None
    else:
        bbox = {
            "x0": int(xs.min()),
            "y0": int(ys.min()),
            "x1_inclusive": int(xs.max()),
            "y1_inclusive": int(ys.max()),
            "w": int(xs.max() - xs.min() + 1),
            "h": int(ys.max() - ys.min() + 1),
        }

    row_ratio = changed.mean(axis=1)
    col_ratio = changed.mean(axis=0)
    top_rows = np.argsort(row_ratio)[-8:][::-1]
    top_cols = np.argsort(col_ratio)[-8:][::-1]

    h, w = changed.shape
    tiles = []
    for y0 in range(0, h, tile_size):
        for x0 in range(0, w, tile_size):
            tile = changed[y0:min(y0 + tile_size, h), x0:min(x0 + tile_size, w)]
            ratio = float(tile.mean())
            if ratio > 0:
                tiles.append({
                    "x": x0,
                    "y": y0,
                    "w": int(tile.shape[1]),
                    "h": int(tile.shape[0]),
                    "changed_ratio": ratio,
                    "changed_pixels": int(tile.sum()),
                })
    tiles.sort(key=lambda item: (item["changed_pixels"], item["changed_ratio"]), reverse=True)

    return {
        "changed_pixel_bbox": bbox,
        "top_mismatch_rows": [{"y": int(i), "changed_ratio": float(row_ratio[i])} for i in top_rows if row_ratio[i] > 0],
        "top_mismatch_columns": [{"x": int(i), "changed_ratio": float(col_ratio[i])} for i in top_cols if col_ratio[i] > 0],
        "tile_size": tile_size,
        "top_mismatch_tiles": tiles[:12],
    }


def crop_image(image: Image.Image, roi: dict[str, Any]) -> Image.Image:
    x, y, w, h = roi["x"], roi["y"], roi["w"], roi["h"]
    return image.crop((x, y, x + w, y + h))


def roi_diagnostics(reference: Image.Image, candidate: Image.Image, roi: dict[str, Any], tolerance: int) -> dict[str, Any]:
    ref_crop = crop_image(reference, roi)
    cand_crop = crop_image(candidate, roi)
    ref_arr = np.asarray(ref_crop, dtype=np.uint8)
    cand_arr = np.asarray(cand_crop, dtype=np.uint8)
    delta = np.abs(ref_arr.astype(np.int16) - cand_arr.astype(np.int16))
    changed = delta.max(axis=2) > tolerance
    return {
        **roi,
        "metrics": array_metrics(ref_arr, cand_arr, tolerance),
        "edge": edge_alignment_metrics(ref_crop, cand_crop),
        "spatial": changed_spatial_metrics(changed, tile_size=min(32, max(8, min(roi["w"], roi["h"]) // 4))),
    }


def save_visuals(reference: Image.Image, candidate: Image.Image, out_dir: Path, tolerance: int) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    Image.blend(reference, candidate, 0.5).save(out_dir / "overlay_50.png")
    difference = ImageChops.difference(reference, candidate)
    difference.save(out_dir / "difference_absolute.png")
    delta = np.asarray(difference, dtype=np.uint8)
    mask = (delta.max(axis=2) > tolerance).astype(np.uint8) * 255
    Image.fromarray(mask, mode="L").save(out_dir / "changed_pixel_mask.png")
    magnified = np.clip(delta.astype(np.int16) * 4, 0, 255).astype(np.uint8)
    Image.fromarray(magnified, mode="RGB").save(out_dir / "difference_x4.png")


def get_path(payload: dict[str, Any], dotted: str) -> Any:
    current: Any = payload
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(dotted)
        current = current[part]
    return current


def evaluate_limits(scope_name: str, payload: dict[str, Any], limits: dict[str, Any]) -> list[dict[str, Any]]:
    failures = []
    for dotted, rule in limits.items():
        actual = get_path(payload, dotted)
        if isinstance(rule, (int, float)):
            rule = {"max": rule}
        if "max" in rule and actual > rule["max"]:
            failures.append({"scope": scope_name, "metric": dotted, "actual": actual, "rule": {"max": rule["max"]}})
        if "min" in rule and actual < rule["min"]:
            failures.append({"scope": scope_name, "metric": dotted, "actual": actual, "rule": {"min": rule["min"]}})
        if "eq" in rule and actual != rule["eq"]:
            failures.append({"scope": scope_name, "metric": dotted, "actual": actual, "rule": {"eq": rule["eq"]}})
    return failures


def evaluate_contract(result: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    required_tolerance = contract.get("required_tolerance")
    if required_tolerance is not None and result.get("tolerance") != required_tolerance:
        failures.append({
            "scope": "contract",
            "metric": "tolerance",
            "actual": result.get("tolerance"),
            "rule": {"eq": required_tolerance},
        })

    failures.extend(evaluate_limits("global", result, contract.get("global_limits", {})))

    roi_map = {item["id"]: item for item in result.get("rois", [])}
    for roi_id, limits in contract.get("roi_limits", {}).items():
        if roi_id not in roi_map:
            failures.append({"scope": roi_id, "metric": "roi_presence", "actual": False, "rule": {"eq": True}})
            continue
        failures.extend(evaluate_limits(f"roi:{roi_id}", roi_map[roi_id], limits))

    return {
        "claim": contract.get("claim", "UNSPECIFIED"),
        "passed": len(failures) == 0,
        "failure_count": len(failures),
        "failures": failures,
        "note": "contract pass is fidelity evidence only; it is not Design KEEP or technical approval",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare normalized reference/candidate renders for OLEANDER reconstruction fidelity.")
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--tolerance", type=int, default=0, help="Per-channel max difference threshold, 0..255. RF-C3 requires 0.")
    parser.add_argument("--rois", type=Path, default=None, help="Optional JSON containing {rois:[{id,x,y,w,h,criticality?}, ...]}")
    parser.add_argument("--contract", type=Path, default=None, help="Optional hard fidelity contract JSON; failures return exit code 3.")
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
    delta = np.abs(ref_arr.astype(np.int16) - cand_arr.astype(np.int16))
    changed = delta.max(axis=2) > args.tolerance

    result.update({
        "same_canvas": True,
        "canvas": {"width": width, "height": height},
        "global": array_metrics(ref_arr, cand_arr, args.tolerance),
        "registration_diagnostic": estimate_translation(reference, candidate),
        "edge": edge_alignment_metrics(reference, candidate),
        "spatial": changed_spatial_metrics(changed),
        "status": "DIAGNOSTIC_COMPLETE_REVIEW_REQUIRED",
    })

    rois = parse_rois(args.rois, width, height)
    if rois:
        result["rois"] = [roi_diagnostics(reference, candidate, roi, args.tolerance) for roi in rois]

    save_visuals(reference, candidate, args.out_dir, args.tolerance)

    exit_code = 0
    if args.contract is not None:
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
        result["contract"] = evaluate_contract(result, contract)
        if result["contract"]["passed"]:
            result["status"] = "FIDELITY_CONTRACT_PASS_REVIEW_REQUIRED"
        else:
            result["status"] = "FIDELITY_CONTRACT_FAIL_REVISE"
            exit_code = 3

    (args.out_dir / "FIDELITY_METRICS.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
