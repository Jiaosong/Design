#!/usr/bin/env python3
import json, sys
from pathlib import Path

REQUIRED = {
    "id", "system", "semantic_class", "source_refs", "truth_state",
    "source_proves", "source_does_not_prove", "spatial_model",
    "translation_mode", "registration_class", "preserved_invariants",
    "relaxed_invariants", "geometry_type", "owner_base_object",
    "connected_object_ids", "derivation_method", "uncertainty_or_tolerance",
    "graphic_carrier_id", "visual_encoding_class", "does_not_prove"
}
MODES = {"TRACE","DERIVE","GENERALIZE","SCHEMATIZE","INFER","DESIGN"}
REG = {"MAP_BOUND","BASE_RELATION_BOUND","TOPOLOGY_BOUND","SEQUENCE_BOUND","DIAGRAM_ONLY"}
GEOM = {"POINT","LINE","CENTERLINE","EDGE_PAIR","BAND","POLYGON","FIELD","NETWORK","SECTION","VECTOR","SYMBOL_ONLY"}


def fail(msg):
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def main():
    if len(sys.argv) != 2:
        fail("usage: validate_spatial_translation.py REGISTER.json")
    p = Path(sys.argv[1])
    data = json.loads(p.read_text(encoding="utf-8"))
    if data.get("promotion") not in {"NO", "NO_PROMOTION", "CANDIDATE_NOT_PROMOTED"}:
        fail("register must remain non-promoted")
    items = data.get("items")
    if not isinstance(items, list) or not items:
        fail("items must be a non-empty list")
    ids = set()
    for i, item in enumerate(items):
        miss = REQUIRED - set(item)
        if miss:
            fail(f"item {i} missing fields: {sorted(miss)}")
        if item["id"] in ids:
            fail(f"duplicate id: {item['id']}")
        ids.add(item["id"])
        if item["translation_mode"] not in MODES:
            fail(f"{item['id']}: invalid translation_mode")
        if item["registration_class"] not in REG:
            fail(f"{item['id']}: invalid registration_class")
        if item["geometry_type"] not in GEOM:
            fail(f"{item['id']}: invalid geometry_type")
        if not item["source_refs"]:
            fail(f"{item['id']}: source_refs cannot be empty")
        if not item["source_proves"]:
            fail(f"{item['id']}: source_proves cannot be empty")
        if not item["spatial_model"]:
            fail(f"{item['id']}: spatial_model cannot be empty")
        if not item["preserved_invariants"]:
            fail(f"{item['id']}: preserved_invariants cannot be empty")
        if not item["does_not_prove"]:
            fail(f"{item['id']}: does_not_prove cannot be empty")
        if item["translation_mode"] == "SCHEMATIZE" and item["registration_class"] == "MAP_BOUND":
            fail(f"{item['id']}: SCHEMATIZE cannot claim MAP_BOUND")
        if item["registration_class"] in {"TOPOLOGY_BOUND","SEQUENCE_BOUND","DIAGRAM_ONLY"} and "POSITION" in item["preserved_invariants"]:
            fail(f"{item['id']}: non-map registration cannot claim preserved POSITION")
        if item["geometry_type"] == "SYMBOL_ONLY" and item["semantic_class"] in {"JUNCTION","VIEWPOINT","THRESHOLD","ECOLOGICAL_CORRIDOR","PEDESTRIAN_PATH"}:
            fail(f"{item['id']}: symbol-only carrier cannot stand in for spatial relation {item['semantic_class']}")
    print(f"PASS: {len(items)} translation items structurally valid")

if __name__ == "__main__":
    main()
