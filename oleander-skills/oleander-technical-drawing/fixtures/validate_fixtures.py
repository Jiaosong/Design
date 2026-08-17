#!/usr/bin/env python3
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GOLDEN = ROOT / "golden"
MANIFEST = GOLDEN / "FIXTURE_MANIFEST.json"
SVG_NS = "{http://www.w3.org/2000/svg}"


def fail(message: str):
    raise AssertionError(message)


def validate_svg(entry, global_required_groups):
    path = GOLDEN / entry["file"]
    if not path.exists():
        fail(f"{entry['id']}: missing fixture {entry['file']}")
    text = path.read_text(encoding="utf-8")
    if "<image" in text or "data:image" in text:
        fail(f"{entry['id']}: golden fixture must keep core content vector; raster image found")
    if "<foreignObject" in text:
        fail(f"{entry['id']}: foreignObject is not allowed in golden SVG fixtures")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        fail(f"{entry['id']}: invalid SVG XML: {exc}")
    if root.tag != SVG_NS + "svg":
        fail(f"{entry['id']}: root is not SVG")
    view_box = root.attrib.get("viewBox")
    if view_box != "0 0 1800 1200":
        fail(f"{entry['id']}: fixture canvas drifted; expected viewBox 0 0 1800 1200, got {view_box!r}")

    ids = []
    for node in root.iter():
        node_id = node.attrib.get("id")
        if node_id:
            ids.append(node_id)
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    if duplicates:
        fail(f"{entry['id']}: duplicate SVG ids: {duplicates}")

    required = list(global_required_groups) + list(entry["required_groups"])
    missing = [g for g in required if g not in ids]
    if missing:
        fail(f"{entry['id']}: missing required groups: {missing}")

    texts = list(root.iter(SVG_NS + "text"))
    if len(texts) < 8:
        fail(f"{entry['id']}: too few vector text nodes ({len(texts)})")
    joined = " ".join((t.text or "") for t in texts)
    for term in ("GOLDEN", "CANDIDATE"):
        if term not in joined:
            fail(f"{entry['id']}: missing visible {term} status")

    claim_group = next(node for node in root.iter() if node.attrib.get("id") == "PRIMARY_CLAIM")
    claim_text = " ".join((t.text or "") for t in claim_group.iter(SVG_NS + "text")).strip()
    if len(claim_text) < 8:
        fail(f"{entry['id']}: PRIMARY_CLAIM is structurally present but effectively empty")

    if entry.get("type") == "technical_drawing":
        density_target = (entry.get("density_target") or "").strip()
        if len(density_target) < 20:
            fail(f"{entry['id']}: technical fixture lacks a meaningful density_target")
        depth_levels = entry.get("depth_levels_present") or []
        valid_depth = {f"D{i}" for i in range(7)}
        if any(level not in valid_depth for level in depth_levels):
            fail(f"{entry['id']}: invalid depth level in {depth_levels}")
        if len(set(depth_levels)) < 5:
            fail(f"{entry['id']}: professional-density calibration requires at least five represented depth levels")
        if "D0" not in depth_levels or "D1" not in depth_levels or "D6" not in depth_levels:
            fail(f"{entry['id']}: technical fixture must retain identity, primary relation and unresolved-closure depth (D0/D1/D6)")
        if len(texts) < 24:
            fail(f"{entry['id']}: detail-density fixture has too little recoverable vector annotation ({len(texts)} text nodes)")

    return {
        "id": entry["id"],
        "file": entry["file"],
        "groups": len(ids),
        "text_nodes": len(texts),
        "depth": entry.get("depth_levels_present"),
    }


def main():
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if manifest.get("status") != "GOLDEN_CANDIDATE_NOT_PROMOTED":
            fail("manifest must not self-promote fixture suite")
        fixtures = manifest.get("fixtures") or []
        if len(fixtures) < 6:
            fail("golden suite requires at least 6 fixtures")
        ids = [f["id"] for f in fixtures]
        if len(ids) != len(set(ids)):
            fail("duplicate fixture ids")
        types = {f["type"] for f in fixtures}
        if "technical_drawing" not in types or "analysis_drawing" not in types:
            fail("suite must cover both technical_drawing and analysis_drawing")
        global_required_groups = manifest.get("global_required_groups") or []
        for expected in ("HIERARCHY_FRAME", "PRIMARY_CLAIM", "ANNOTATION_RAIL"):
            if expected not in global_required_groups:
                fail(f"manifest hierarchy scaffold is missing {expected}")
        results = [validate_svg(entry, global_required_groups) for entry in fixtures]
    except (AssertionError, OSError, json.JSONDecodeError, StopIteration) as exc:
        print(f"OLEANDER DRAWING FIXTURES: FAIL\n{exc}", file=sys.stderr)
        return 1
    print("OLEANDER DRAWING FIXTURES: STRUCTURE PASS")
    print(f"fixture count: {len(results)}")
    print("hierarchy scaffold: HIERARCHY_FRAME / PRIMARY_CLAIM / ANNOTATION_RAIL")
    print("technical density contract: density_target + D0..D6 coverage + graphical groups")
    for r in results:
        depth = f" depth={','.join(r['depth'])}" if r.get("depth") else ""
        print(f"- {r['id']} {r['file']}: groups={r['groups']} text_nodes={r['text_nodes']}{depth}")
    print("NOTE: structure/density-contract PASS does not equal 3s/30s/near-read Design PASS, engineering approval or Golden promotion.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
