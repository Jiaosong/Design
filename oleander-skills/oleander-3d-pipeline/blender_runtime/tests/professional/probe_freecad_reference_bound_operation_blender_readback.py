"""Blender display-only readback for bounded semantic-reference-bound B-Rep operation."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

import bpy

ROOT = Path(os.environ.get("OLEANDER_REF_OPERATION_DIR", "/tmp/oleander-reference-operation"))
DISPLAY = ROOT / "oleander_reference_bound_operation_display.json"
MANIFEST = ROOT / "oleander_reference_bound_operation_manifest.json"
REGISTRY = ROOT / "oleander_reference_bound_operation_registry.json"
REOPEN = ROOT / "oleander_reference_bound_operation_readback.blend"
checks: list[str] = []

REF_ID = "OLE_REF::PRIMARY_TOP_FACE"
SELECTOR_ID = "SELECTOR::UNIQUE_GLOBAL_ZMAX_PLANAR_POSITIVE_Z"
OP_ID = "OLE_OP::TOP_FACE_CENTER_THROUGH_HOLE"
EXPECTED_CENTERS = {
    "R001": [40.0, 25.0, 10.0],
    "R002": [50.0, 25.0, 10.0],
    "R003": [50.0, 25.0, 10.0],
}


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def close(a, b, tol=1e-5):
    return abs(float(a) - float(b)) <= tol


def close_vec(a, b, tol=1e-5):
    return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))


def main():
    display = json.loads(DISPLAY.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    check(manifest.get("schema") == "OLEANDER_FREECAD_REFERENCE_BOUND_OPERATION_v0.1", "manifest_schema")
    check(manifest.get("status") == "PASS", "manifest_pass")
    check(manifest.get("dependency_state") == "VALIDATED_FOR_BOUNDED_SCOPE", "bounded_dependency_state")
    check(display.get("schema") == "OLEANDER_REFERENCE_BOUND_OPERATION_DISPLAY_v0.1", "display_schema")
    check(display.get("geometry_authority") == "FREECAD_OCCT_BREP", "occt_authority")
    check(display.get("display_authority") == "DISPLAY_DERIVATIVE_ONLY", "display_only")
    check(display.get("ref_id") == REF_ID, "display_ref_id")
    check(display.get("selector_id") == SELECTOR_ID, "display_selector_id")
    check(display.get("operation_id") == OP_ID, "display_operation_id")

    contract = manifest["reference_contract"]
    check(contract["ref_id"] == REF_ID, "contract_ref_id")
    check(contract["selector_id"] == SELECTOR_ID, "contract_selector_id")
    check(contract["operation_id"] == OP_ID, "contract_operation_id")
    check(contract["ordinal_persistence"] == "PROHIBITED", "ordinal_persistence_prohibited")
    check(manifest["expected_failure_cases"] == {
        "ambiguous_reference_blocks_mutation": "PASS",
        "missing_reference_blocks_mutation": "PASS",
    }, "failure_gates")

    history = registry["history"]
    op_history = registry["operation_history"]
    check([item["state"] for item in history[-2:]] == ["AMBIGUOUS_HOLD", "MISSING_HOLD"], "registry_hold_tail")
    check([item["state"] for item in op_history[-2:]] == ["AMBIGUOUS_HOLD", "MISSING_HOLD"], "operation_hold_tail")
    check(all(item.get("mutation") == "NONE" for item in op_history[-2:]), "holds_zero_mutation")

    revisions = {item["revision"]: item for item in display["revisions"]}
    check(set(revisions) == set(EXPECTED_CENTERS), "revision_set")
    signatures = [revisions[name]["resolved_signature"] for name in ("R001", "R002", "R003")]
    check(len(set(signatures)) == 3, "signature_changes_across_geometry_revisions")
    check(registry["last_good_signature"] == revisions["R003"]["resolved_signature"], "last_good_matches_r3")

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001

    for name in ("R001", "R002", "R003"):
        item = revisions[name]
        check(item["ole_id"] == "OLE_REFERENCE_BOUND_OPERATION::" + name, "ole_id_" + name)
        check(item["operation_id"] == OP_ID, "operation_id_" + name)
        check(item["ref_id"] == REF_ID, "ref_id_" + name)
        check(item["selector_id"] == SELECTOR_ID, "selector_id_" + name)
        check(close(item["radius_mm"], 3.0), "radius_" + name)
        check(close_vec(item["resolved_center_mm"], EXPECTED_CENTERS[name]), "resolved_center_" + name)
        check(item["volume_mm3"] > 0.0, "positive_volume_" + name)
        check(bool(item["vertices_mm"]) and bool(item["triangles"]), "display_mesh_data_" + name)

        mesh = bpy.data.meshes.new("OLE_REFERENCE_BOUND_OPERATION_MESH_" + name)
        mesh.from_pydata(item["vertices_mm"], [], item["triangles"])
        mesh.update()
        obj = bpy.data.objects.new("OLE_REFERENCE_BOUND_OPERATION_" + name, mesh)
        bpy.context.collection.objects.link(obj)
        obj["ole_id"] = item["ole_id"]
        obj["operation_id"] = OP_ID
        obj["ref_id"] = REF_ID
        obj["selector_id"] = SELECTOR_ID
        obj["resolved_signature"] = item["resolved_signature"]
        obj["resolved_center_mm"] = item["resolved_center_mm"]
        obj["radius_mm"] = float(item["radius_mm"])
        obj["master_locator"] = display["source_fcstd"]
        obj["source_fcstd_sha256"] = display["source_fcstd_sha256"]
        obj["source_step"] = item["source_step"]
        obj["source_step_sha256"] = item["source_step_sha256"]
        obj["geometry_authority"] = "DISPLAY_DERIVATIVE_ONLY"

    bpy.context.view_layer.update()
    for name in ("R001", "R002", "R003"):
        obj = bpy.data.objects["OLE_REFERENCE_BOUND_OPERATION_" + name]
        check(close_vec([obj.dimensions.x, obj.dimensions.y, obj.dimensions.z], revisions[name]["bbox_mm"], 1e-3), "bbox_" + name)

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    source_sha = display["source_fcstd_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    for name in ("R001", "R002", "R003"):
        obj = bpy.data.objects.get("OLE_REFERENCE_BOUND_OPERATION_" + name)
        check(obj is not None, "reopen_object_" + name)
        check(obj["ref_id"] == REF_ID, "reopen_ref_id_" + name)
        check(obj["selector_id"] == SELECTOR_ID, "reopen_selector_id_" + name)
        check(obj["operation_id"] == OP_ID, "reopen_operation_id_" + name)
        check(obj["resolved_signature"] == revisions[name]["resolved_signature"], "reopen_signature_" + name)
        check(close(obj["radius_mm"], 3.0), "reopen_radius_" + name)
        check(obj["source_fcstd_sha256"] == source_sha, "reopen_fcstd_sha_" + name)
        check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "reopen_authority_" + name)

    print("OLEANDER_REFERENCE_BOUND_OPERATION_BLENDER_READBACK=" + json.dumps({
        "schema": "OLEANDER_REFERENCE_BOUND_OPERATION_BLENDER_READBACK_v0.1",
        "status": "PASS",
        "blender_version": bpy.app.version_string,
        "revisions": ["R001", "R002", "R003"],
        "ref_id": REF_ID,
        "operation_id": OP_ID,
        "checks": checks,
        "authority": {
            "master": "FreeCAD/OCCT semantic-reference-bound BRep cut",
            "blender": "DISPLAY_DERIVATIVE_ONLY",
        },
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "persistent_topological_naming_parity",
            "general_face_reference_stability",
            "edge_reference_stability",
            "vertex_reference_stability",
            "nonplanar_semantic_reference_rebind",
            "automatic_ambiguous_reference_resolution",
        ],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
