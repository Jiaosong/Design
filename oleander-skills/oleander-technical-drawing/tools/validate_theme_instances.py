#!/usr/bin/env python3
import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "{http://www.w3.org/2000/svg}"


def local_name(tag):
    return tag.split("}", 1)[-1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--svg", required=True)
    parser.add_argument("--register", required=True)
    args = parser.parse_args()
    try:
        register = json.loads(Path(args.register).read_text(encoding="utf-8"))
        root = ET.fromstring(Path(args.svg).read_text(encoding="utf-8"))
        nodes = {}
        for node in root.iter():
            node_id = node.attrib.get("id")
            if node_id:
                if node_id in nodes:
                    raise AssertionError(f"duplicate id {node_id}")
                nodes[node_id] = node
        if register.get("status") not in {"REVISE", "REVIEW_PENDING", "CANDIDATE_NOT_PROMOTED"}:
            raise AssertionError("register must remain non-promoted")
        themes = register.get("themes") or []
        if len(themes) < 2:
            raise AssertionError("need at least two theme instances")
        for theme in themes:
            semantic_id = theme["semantic_group"]
            carrier_id = theme["visual_carrier"]
            if semantic_id not in nodes or carrier_id not in nodes:
                raise AssertionError(f"missing semantic/carrier for {theme['id']}")
            carrier = nodes[carrier_id]
            if carrier.attrib.get("data-role") != "STRUCTURED_THEME_VISUAL_VECTOR_NON_AUTHORITY":
                raise AssertionError(f"carrier role invalid {carrier_id}")
            if theme.get("authority") != "NON_AUTHORITY":
                raise AssertionError(f"theme carrier must be non-authority {carrier_id}")
            for node in carrier.iter():
                if local_name(node.tag) in {"image", "text", "foreignObject"}:
                    raise AssertionError(f"theme carrier contamination {carrier_id}")
        print("OLEANDER THEME INSTANCE: STRUCTURE PASS")
        print(f"themes={len(themes)}")
        print("NOTE: structure PASS does not equal pixel fidelity, semantic relation PASS, or Design KEEP.")
        return 0
    except Exception as exc:
        print(f"OLEANDER THEME INSTANCE: FAIL\n{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
