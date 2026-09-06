"""Blender metadata-only readback for bounded FreeCAD semantic reference rebind."""

from __future__ import annotations

import json
import os
from pathlib import Path

import bpy

ROOT = Path(os.environ.get("OLEANDER_REF_REBIND_DIR", "/tmp/oleander-reference-rebind"))
REGISTRY = ROOT / "oleander_reference_registry.json"
MANIFEST = ROOT / "oleander_reference_rebind_manifest.json"
REOPEN = ROOT / "oleander_reference_rebind_readback.blend"
checks: list[str] = []


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    check(manifest.get("status") == "PASS", "freecad_manifest_pass")
    check(manifest.get("schema") == "OLEANDER_FREECAD_REFERENCE_REBIND_v0.1", "manifest_schema")
    check(registry.get("ref_id") == "OLE_REF::PRIMARY_TOP_FACE", "stable_ref_id")
    check(registry["selector"]["selector_id"] == "SELECTOR::UNIQUE_GLOBAL_ZMAX_PLANAR_POSITIVE_Z", "selector_semantics")
    check(registry["state"] == "MISSING_HOLD", "latest_hold_state")
    check(len(registry["history"]) == 5, "history_count")
    states = [event["state"] for event in registry["history"]]
    check(states[:3] == ["RESOLVED_INITIAL", "REBOUND_CHANGED_SIGNATURE", "REBOUND_CHANGED_SIGNATURE"], "positive_rebind_states")
    check(states[-2:] == ["AMBIGUOUS_HOLD", "MISSING_HOLD"], "failure_states")
    check(manifest["expected_failure_cases"]["ambiguous_reference"] == "PASS", "ambiguous_gate")
    check(manifest["expected_failure_cases"]["missing_reference"] == "PASS", "missing_gate")

    obj = bpy.data.objects.new("OLE_REFERENCE_PRIMARY_TOP", None)
    bpy.context.collection.objects.link(obj)
    obj["ole_ref_id"] = registry["ref_id"]
    obj["reference_authority"] = "REFERENCE_METADATA_ONLY"
    obj["selector_json"] = json.dumps(registry["selector"], sort_keys=True)
    obj["last_good_signature"] = registry["last_signature"]
    obj["reference_state"] = registry["state"]
    obj["history_json"] = json.dumps(registry["history"], sort_keys=True)
    obj["persistence_boundary"] = "NO_SUBSHAPE_ORDINALS;RE_RESOLVE_OR_HOLD"
    obj["geometry_authority"] = "NO_GEOMETRY_AUTHORITY"
    check(obj.type == "EMPTY", "metadata_empty_object")
    check(obj["geometry_authority"] == "NO_GEOMETRY_AUTHORITY", "no_geometry_authority")

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    r = bpy.data.objects.get("OLE_REFERENCE_PRIMARY_TOP")
    check(r is not None, "blend_reopen")
    check(r["ole_ref_id"] == "OLE_REF::PRIMARY_TOP_FACE", "ref_id_reopen")
    check(r["reference_state"] == "MISSING_HOLD", "state_reopen")
    check(r["last_good_signature"] == registry["last_signature"], "signature_reopen")
    check(json.loads(r["selector_json"])["selector_id"] == "SELECTOR::UNIQUE_GLOBAL_ZMAX_PLANAR_POSITIVE_Z", "selector_reopen")
    check([e["state"] for e in json.loads(r["history_json"])[-2:]] == ["AMBIGUOUS_HOLD", "MISSING_HOLD"], "history_reopen")
    check(r["geometry_authority"] == "NO_GEOMETRY_AUTHORITY", "authority_reopen")

    result = {
        "schema": "OLEANDER_REFERENCE_REBIND_BLENDER_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "checks": checks,
        "authority": {"freecad": "semantic B-Rep reference resolution", "blender": "REFERENCE_METADATA_ONLY"},
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "persistent_topological_naming_parity",
            "blender_face_reference_authority",
            "automatic_ambiguous_reference_resolution"
        ]
    }
    print("OLEANDER_REFERENCE_REBIND_BLENDER_READBACK=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
