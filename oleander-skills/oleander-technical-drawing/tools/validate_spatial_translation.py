#!/usr/bin/env python3
import json, sys
from pathlib import Path

REQUIRED = {
    "id", "system", "semantic_class", "source_refs", "truth_state",
    "source_proves", "source_does_not_prove", "spatial_model",
    "translation_mode", "registration_class", "preserved_invariants",
    "relaxed_invariants", "geometry_type", "owner_base_object",
    "connected_object_ids", "derivation_method", "uncertainty_or_tolerance",
    "graphic_carrier_id", "visual_encoding_class", "does_not_prove",
    "source_carrier_state", "source_carrier_scope",
    "carrier_precedence_decision", "redraw_justification"
}
MODES = {"TRACE","DERIVE","GENERALIZE","SCHEMATIZE","INFER","DESIGN"}
REG = {"MAP_BOUND","BASE_RELATION_BOUND","TOPOLOGY_BOUND","SEQUENCE_BOUND","DIAGRAM_ONLY"}
GEOM = {"POINT","LINE","CENTERLINE","EDGE_PAIR","BAND","POLYGON","FIELD","NETWORK","SECTION","VECTOR","SYMBOL_ONLY","DIRECT_SOURCE_VISUAL"}
SOURCE_CARRIER_STATES = {
    "SOURCE_CARRIER_ABSENT",
    "SOURCE_CARRIER_INSUFFICIENT",
    "SOURCE_CARRIER_SUFFICIENT",
    "SOURCE_CARRIER_AUTHORITY",
}
PRECEDENCE = {
    "REUSE_DIRECT",
    "TRACE_BOUNDED",
    "DERIVE_REQUIRED",
    "GENERALIZE_REQUIRED",
    "SCHEMATIZE_SEPARATELY",
    "REDRAW_JUSTIFIED",
}
SUFFICIENT_STATES = {"SOURCE_CARRIER_SUFFICIENT", "SOURCE_CARRIER_AUTHORITY"}


def fail(msg):
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def material_justification(text):
    if not isinstance(text, str) or not text.strip():
        return False
    t = text.strip().lower()
    if t in {"n/a", "na", "none"}:
        return False
    aesthetic_only = {
        "cleaner", "prettier", "more professional", "better composition",
        "style match", "match reference style", "easier to color",
        "更干净", "更漂亮", "更专业", "构图更好", "匹配风格", "方便上色"
    }
    return t not in aesthetic_only


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
        if item["source_carrier_state"] not in SOURCE_CARRIER_STATES:
            fail(f"{item['id']}: invalid source_carrier_state")
        if item["carrier_precedence_decision"] not in PRECEDENCE:
            fail(f"{item['id']}: invalid carrier_precedence_decision")
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
        if not item["source_carrier_scope"]:
            fail(f"{item['id']}: source_carrier_scope cannot be empty")

        if item["translation_mode"] == "SCHEMATIZE" and item["registration_class"] == "MAP_BOUND":
            fail(f"{item['id']}: SCHEMATIZE cannot claim MAP_BOUND")
        if item["registration_class"] in {"TOPOLOGY_BOUND","SEQUENCE_BOUND","DIAGRAM_ONLY"} and "POSITION" in item["preserved_invariants"]:
            fail(f"{item['id']}: non-map registration cannot claim preserved POSITION")
        if item["geometry_type"] == "SYMBOL_ONLY" and item["semantic_class"] in {"JUNCTION","VIEWPOINT","THRESHOLD","ECOLOGICAL_CORRIDOR","PEDESTRIAN_PATH"}:
            fail(f"{item['id']}: symbol-only carrier cannot stand in for spatial relation {item['semantic_class']}")

        # Source-carrier precedence gate.
        if item["source_carrier_state"] in SUFFICIENT_STATES:
            decision = item["carrier_precedence_decision"]
            if decision != "REUSE_DIRECT" and not material_justification(item["redraw_justification"]):
                fail(f"{item['id']}: sufficient/authoritative source carrier requires material justification before redraw/translation")
        if item["carrier_precedence_decision"] == "REUSE_DIRECT":
            if item["source_carrier_state"] not in SUFFICIENT_STATES:
                fail(f"{item['id']}: REUSE_DIRECT requires sufficient or authoritative source carrier")
            if item["geometry_type"] != "DIRECT_SOURCE_VISUAL":
                fail(f"{item['id']}: REUSE_DIRECT must use DIRECT_SOURCE_VISUAL geometry type")
            if str(item["redraw_justification"]).strip().lower() not in {"n/a", "na", "none"}:
                fail(f"{item['id']}: direct reuse should not carry a redraw justification")
        if item["carrier_precedence_decision"] == "SCHEMATIZE_SEPARATELY" and item["registration_class"] not in {"TOPOLOGY_BOUND","SEQUENCE_BOUND","DIAGRAM_ONLY"}:
            fail(f"{item['id']}: SCHEMATIZE_SEPARATELY cannot claim map/base registration")

    print(f"PASS: {len(items)} translation items structurally valid, including source-carrier precedence")

if __name__ == "__main__":
    main()
