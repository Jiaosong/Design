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


def validate_svg(entry):
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
    missing = [g for g in entry["required_groups"] if g not in ids]
    if missing:
        fail(f"{entry['id']}: missing required groups: {missing}")
    texts = list(root.iter(SVG_NS + "text"))
    if len(texts) < 8:
        fail(f"{entry['id']}: too few vector text nodes ({len(texts)})")
    joined = " ".join((t.text or "") for t in texts)
    for term in ("GOLDEN", "CANDIDATE"):
        if term not in joined:
            fail(f"{entry['id']}: missing visible {term} status")
    return {
        "id": entry["id"],
        "file": entry["file"],
        "groups": len(ids),
        "text_nodes": len(texts),
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
        results = [validate_svg(entry) for entry in fixtures]
    except (AssertionError, OSError, json.JSONDecodeError) as exc:
        print(f"OLEANDER DRAWING FIXTURES: FAIL\n{exc}", file=sys.stderr)
        return 1
    print("OLEANDER DRAWING FIXTURES: STRUCTURE PASS")
    print(f"fixture count: {len(results)}")
    for r in results:
        print(f"- {r['id']} {r['file']}: groups={r['groups']} text_nodes={r['text_nodes']}")
    print("NOTE: structure PASS does not equal independent Design PASS or Golden promotion.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
