#!/usr/bin/env python3
import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "{http://www.w3.org/2000/svg}"
ALLOWED_STATES = {"DRAWN", "PARTIAL", "TEXT-ONLY", "UNRECOVERABLE"}


def fail(message: str):
    raise AssertionError(message)


def local_name(tag: str) -> str:
    return tag.split("}", 1)[-1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--svg", required=True)
    parser.add_argument("--register", required=True)
    args = parser.parse_args()

    svg_path = Path(args.svg)
    register_path = Path(args.register)

    try:
        register = json.loads(register_path.read_text(encoding="utf-8"))
        root = ET.fromstring(svg_path.read_text(encoding="utf-8"))
        if root.tag != SVG_NS + "svg":
            fail("root is not svg")

        nodes = {}
        for node in root.iter():
            node_id = node.attrib.get("id")
            if node_id:
                if node_id in nodes:
                    fail(f"duplicate svg id: {node_id}")
                nodes[node_id] = node

        if register.get("status") not in {"CANDIDATE_NOT_PROMOTED", "REVIEW_PENDING", "REVISE"}:
            fail("register must remain non-promoted")
        if register.get("semantic_editability_target") != "SEMANTIC_VECTOR":
            fail("semantic editability target must be SEMANTIC_VECTOR")

        master = register["master_base"]["id"]
        if master not in nodes:
            fail(f"missing master base {master}")
        instances = register["master_base"].get("instances") or []
        if len(instances) < 2:
            fail("multilayer reconstruction requires repeated master-base instances")
        for instance_id in instances:
            if instance_id not in nodes:
                fail(f"missing base instance {instance_id}")
            node = nodes[instance_id]
            if local_name(node.tag) != "use":
                fail(f"{instance_id} must be <use>")
            href = node.attrib.get("href") or node.attrib.get("{http://www.w3.org/1999/xlink}href")
            if href != f"#{master}":
                fail(f"{instance_id} does not reuse #{master}")

        panels = register.get("panels") or []
        if len(panels) < 2:
            fail("multilayer fixture requires >= 2 panels")

        relations = register.get("relations") or []
        relation_by_id = {relation["id"]: relation for relation in relations}
        if len(relation_by_id) != len(relations):
            fail("duplicate relation ids in register")

        for panel in panels:
            if panel["id"] not in nodes:
                fail(f"missing panel group {panel['id']}")
            if panel["base_instance"] not in instances:
                fail(f"{panel['id']} base instance is not registered")
            for relation_id in panel.get("relations") or []:
                if relation_id not in relation_by_id:
                    fail(f"{panel['id']} references unknown relation {relation_id}")

        for relation in relations:
            relation_id = relation["id"]
            state = relation.get("state")
            if state not in ALLOWED_STATES:
                fail(f"{relation_id} invalid state {state}")
            if relation_id not in nodes:
                fail(f"missing relation group {relation_id}")

            carriers = relation.get("carrier_ids") or []
            if state == "DRAWN" and not carriers:
                fail(f"{relation_id} DRAWN relation has no carrier geometry")
            for carrier_id in carriers:
                if carrier_id not in nodes:
                    fail(f"{relation_id} missing carrier {carrier_id}")
                if local_name(nodes[carrier_id].tag) == "text":
                    fail(f"{relation_id} carrier {carrier_id} is text-only")

            targets = relation.get("target_ids") or []
            for target_id in targets:
                if target_id not in nodes:
                    fail(f"{relation_id} missing target {target_id}")

            callout = relation.get("callout")
            if callout:
                for key in ("label_id", "leader_id", "anchor_id", "target_id"):
                    if not callout.get(key) or callout[key] not in nodes:
                        fail(f"{relation_id} callout missing {key}")
                if local_name(nodes[callout["label_id"]].tag) != "text":
                    fail(f"{relation_id} callout label must be text")
                if local_name(nodes[callout["leader_id"]].tag) not in {"path", "polyline", "line"}:
                    fail(f"{relation_id} leader must be geometry")
                if callout["target_id"] not in targets:
                    fail(f"{relation_id} callout target is not relation target")

        for symbol_id, specification in (register.get("symbol_dictionary") or {}).items():
            if symbol_id not in nodes:
                fail(f"missing symbol component {symbol_id}")
            instance_count = 0
            for node in root.iter():
                if local_name(node.tag) != "use":
                    continue
                href = node.attrib.get("href") or node.attrib.get("{http://www.w3.org/1999/xlink}href")
                if href == f"#{symbol_id}":
                    instance_count += 1
            required = int(specification.get("min_instances", 1))
            if instance_count < required:
                fail(f"symbol {symbol_id} has {instance_count} instances, expected >= {required}")

    except (AssertionError, OSError, json.JSONDecodeError, ET.ParseError, KeyError) as exc:
        print(f"OLEANDER SEMANTIC RECONSTRUCTION: FAIL\n{exc}", file=sys.stderr)
        return 1

    print("OLEANDER SEMANTIC RECONSTRUCTION: STRUCTURE PASS")
    print(f"panels={len(panels)} relations={len(relations)} shared_base_instances={len(instances)}")
    print("NOTE: relationship-structure/editability PASS does not equal pixel fidelity, Design KEEP, or technical truth.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
