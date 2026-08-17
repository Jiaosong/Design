#!/usr/bin/env python3
import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "{http://www.w3.org/2000/svg}"
NON_PROMOTED = {"CANDIDATE_NOT_PROMOTED", "REVIEW_PENDING", "REVISE", "REVISE_REVIEW_PENDING"}
ALLOWED_CARRIER_STATES = {"STRUCTURED_VISUAL_VECTOR_NON_AUTHORITY"}


def fail(msg):
    raise AssertionError(msg)


def local(tag):
    return tag.split("}", 1)[-1]


def parse_rgb(value):
    if not value or value in {"none", "transparent"}:
        return None
    value = value.strip().lower()
    if value.startswith("#"):
        h = value[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) == 6:
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    m = re.fullmatch(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", value)
    if m:
        return tuple(map(int, m.groups()))
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--svg", required=True)
    ap.add_argument("--register", required=True)
    args = ap.parse_args()
    try:
        register = json.loads(Path(args.register).read_text(encoding="utf-8"))
        root = ET.fromstring(Path(args.svg).read_text(encoding="utf-8"))
        if root.tag != SVG_NS + "svg":
            fail("root is not svg")

        nodes = {}
        for n in root.iter():
            node_id = n.attrib.get("id")
            if node_id:
                if node_id in nodes:
                    fail(f"duplicate svg id: {node_id}")
                nodes[node_id] = n

        if register.get("status") not in NON_PROMOTED:
            fail("base-instance register must remain non-promoted")
        master = register.get("geometry_master")
        if not master or master not in nodes:
            fail("semantic geometry_master missing")
        panels = register.get("panels") or []
        if len(panels) < 2:
            fail("base-instance fidelity requires >=2 panels")

        carrier_ids = []
        for panel in panels:
            pid = panel.get("panel_id")
            if not pid:
                fail("panel_id missing")
            sem = panel.get("semantic_base_instance")
            if not sem or sem not in nodes:
                fail(f"{pid} semantic_base_instance missing")
            vis = panel.get("visual_carrier_id")
            if not vis or vis not in nodes:
                fail(f"{pid} visual_carrier_id missing")
            carrier_ids.append(vis)
            if panel.get("carrier_state") not in ALLOWED_CARRIER_STATES:
                fail(f"{pid} visual carrier must be non-authoritative structured visual vector")
            if panel.get("authority") not in {False, "false", "NON_AUTHORITY"}:
                fail(f"{pid} visual carrier must not claim geometry authority")
            if not panel.get("roi") or len(panel["roi"]) != 4:
                fail(f"{pid} missing declared ROI")
            if not panel.get("does_not_prove"):
                fail(f"{pid} missing does_not_prove boundary")

            carrier = nodes[vis]
            if local(carrier.tag) != "g":
                fail(f"{pid} visual carrier must be a group")
            for n in carrier.iter():
                kind = local(n.tag)
                if kind == "image":
                    fail(f"{pid} visual carrier embeds raster image")
                if kind == "text":
                    fail(f"{pid} visual carrier contains text; label contamination")
                for attr in ("fill", "stroke"):
                    rgb = parse_rgb(n.attrib.get(attr))
                    if rgb is None:
                        continue
                    if max(rgb) - min(rgb) > 24:
                        fail(f"{pid} visual carrier contains non-neutral {attr}={n.attrib.get(attr)}")

        if len(set(carrier_ids)) != len(carrier_ids):
            fail("panels claiming panel-specific rendering must use distinct visual-carrier IDs")

    except (AssertionError, OSError, json.JSONDecodeError, ET.ParseError) as exc:
        print(f"OLEANDER BASE INSTANCE: FAIL\n{exc}", file=sys.stderr)
        return 1

    print("OLEANDER BASE INSTANCE: STRUCTURE PASS")
    print(f"panels={len(panels)} distinct_visual_carriers={len(set(carrier_ids))} master={master}")
    print("NOTE: base-instance structure PASS does not equal pixel fidelity, geometry authority, or Design KEEP.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
