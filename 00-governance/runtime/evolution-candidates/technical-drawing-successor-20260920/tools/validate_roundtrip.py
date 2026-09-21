#!/usr/bin/env python3
"""Validate OLEANDER Technical Drawing successor DXF/SVG round-trip receipts.

This validator checks deterministic machine structure only:
- referenced ASCII DXF and SVG exist;
- DXF LINE extents by layer match declared expected geometry;
- SVG rect extents by id match declared expected geometry;
- source/claim boundary fields remain explicit.

It does not award professional, engineering, statutory, field or Design approval.
"""

from __future__ import annotations

import json
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[5]


def _float(value: str) -> float:
    return float(value.strip())


def parse_ascii_dxf_line_bboxes(path: Path) -> dict[str, tuple[float, float, float, float]]:
    lines = [line.rstrip("\r\n") for line in path.read_text(encoding="utf-8").splitlines()]
    pairs: list[tuple[str, str]] = []
    if len(lines) % 2:
        raise ValueError(f"{path}: malformed ASCII DXF group-code/value sequence")
    for i in range(0, len(lines), 2):
        pairs.append((lines[i].strip(), lines[i + 1].strip()))

    boxes: dict[str, list[float]] = {}
    i = 0
    while i < len(pairs):
        code, value = pairs[i]
        if code == "0" and value == "LINE":
            entity: dict[str, str] = {}
            i += 1
            while i < len(pairs) and pairs[i][0] != "0":
                c, v = pairs[i]
                entity[c] = v
                i += 1
            layer = entity.get("8")
            if not layer:
                raise ValueError(f"{path}: LINE missing layer")
            required = ("10", "20", "11", "21")
            if any(k not in entity for k in required):
                raise ValueError(f"{path}: LINE on {layer} missing 2D coordinates")
            x1, y1, x2, y2 = (_float(entity[k]) for k in required)
            if layer not in boxes:
                boxes[layer] = [x1, y1, x1, y1]
            box = boxes[layer]
            box[0] = min(box[0], x1, x2)
            box[1] = min(box[1], y1, y2)
            box[2] = max(box[2], x1, x2)
            box[3] = max(box[3], y1, y2)
            continue
        i += 1

    return {k: tuple(v) for k, v in boxes.items()}


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_svg_rects(path: Path) -> dict[str, tuple[float, float, float, float]]:
    root = ET.parse(path).getroot()
    out: dict[str, tuple[float, float, float, float]] = {}
    for element in root.iter():
        if _local_name(element.tag) != "rect":
            continue
        rid = element.attrib.get("id")
        if not rid:
            continue
        x = float(element.attrib.get("x", "0"))
        y = float(element.attrib.get("y", "0"))
        w = float(element.attrib["width"])
        h = float(element.attrib["height"])
        out[rid] = (x, y, x + w, y + h)
    return out


def _size(box: tuple[float, float, float, float]) -> tuple[float, float]:
    return (box[2] - box[0], box[3] - box[1])


def _close(a: float, b: float, tol: float) -> bool:
    return math.isclose(a, b, abs_tol=tol, rel_tol=0.0)


def validate_receipt(payload: dict[str, Any], repo_root: Path = REPO_ROOT) -> list[str]:
    errors: list[str] = []
    for field in (
        "drawing_id",
        "project_id",
        "decision_object",
        "drawing_status",
        "claim_ceiling",
        "source_authority",
        "native_outputs",
        "expected_geometry",
        "actual_readback",
        "independent_review",
        "does_not_prove",
    ):
        if field not in payload:
            errors.append(f"missing required field: {field}")

    if errors:
        return errors

    if not payload.get("does_not_prove"):
        errors.append("does_not_prove must be non-empty")

    source = payload.get("source_authority") or {}
    if not source.get("dimension_state"):
        errors.append("source_authority.dimension_state required")

    native = payload.get("native_outputs") or {}
    dxf_ref = native.get("dxf_ref")
    svg_ref = native.get("svg_ref")
    if not dxf_ref or not svg_ref:
        errors.append("native_outputs must include dxf_ref and svg_ref")
        return errors

    dxf_path = repo_root / dxf_ref
    svg_path = repo_root / svg_ref
    if not dxf_path.is_file():
        errors.append(f"DXF missing: {dxf_ref}")
    if not svg_path.is_file():
        errors.append(f"SVG missing: {svg_ref}")
    if errors:
        return errors

    try:
        dxf = parse_ascii_dxf_line_bboxes(dxf_path)
    except Exception as exc:
        errors.append(f"DXF parse failed: {exc}")
        dxf = {}
    try:
        svg = parse_svg_rects(svg_path)
    except Exception as exc:
        errors.append(f"SVG parse failed: {exc}")
        svg = {}

    ids: set[str] = set()
    for item in payload.get("expected_geometry") or []:
        gid = item.get("id")
        layer = item.get("dxf_layer")
        sid = item.get("svg_id")
        if not gid or gid in ids:
            errors.append(f"invalid/duplicate expected geometry id: {gid!r}")
            continue
        ids.add(gid)
        if layer not in dxf:
            errors.append(f"{gid}: DXF layer missing: {layer}")
            continue
        if sid not in svg:
            errors.append(f"{gid}: SVG rect missing: {sid}")
            continue
        ew = float(item["width"])
        eh = float(item["height"])
        tol = float(item.get("tolerance", 0.001))
        dw, dh = _size(dxf[layer])
        sw, sh = _size(svg[sid])
        for label, actual_w, actual_h in (("DXF", dw, dh), ("SVG", sw, sh)):
            if not _close(actual_w, ew, tol):
                errors.append(f"{gid}: {label} width {actual_w} != expected {ew} ± {tol}")
            if not _close(actual_h, eh, tol):
                errors.append(f"{gid}: {label} height {actual_h} != expected {eh} ± {tol}")

    if payload.get("actual_readback", {}).get("required") is not True:
        errors.append("actual_readback.required must be true")
    if not payload.get("actual_readback", {}).get("method"):
        errors.append("actual_readback.method required")

    if payload.get("result") == "PASS_CURRENTIZATION":
        errors.append("successor fixture/receipt may not self-award PASS_CURRENTIZATION")
    if payload.get("independent_review", {}).get("state") == "PASS" and not payload.get("independent_review", {}).get("reviewer_ref"):
        errors.append("independent review PASS requires reviewer_ref")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_roundtrip.py RECEIPT.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.is_absolute():
        path = REPO_ROOT / path
    payload = json.loads(path.read_text(encoding="utf-8"))
    errors = validate_receipt(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PASS")
    print("NOTE: machine round-trip PASS does not prove professional drawing adequacy, engineering validity, field truth, construction readiness or Current Skill promotion.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
