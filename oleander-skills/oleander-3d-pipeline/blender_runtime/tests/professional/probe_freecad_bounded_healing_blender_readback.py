"""Blender readback for bounded FreeCAD/OCCT healing foundation v0.2."""

from __future__ import annotations

import json
import os
from pathlib import Path

import bpy

ROOT = Path(os.environ.get("OLEANDER_HEAL_DIR", "/tmp/oleander-bounded-healing"))
DISPLAY = ROOT / "oleander_bounded_healing_display.json"
MANIFEST = ROOT / "oleander_bounded_healing_manifest.json"
REOPEN = ROOT / "oleander_bounded_healing_readback.blend"
checks: list[str] = []


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def main() -> None:
    display = json.loads(DISPLAY.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    check(manifest.get("schema") == "OLEANDER_FREECAD_BOUNDED_HEALING_v0.2", "manifest_schema")
    check(manifest.get("status") == "PASS", "freecad_manifest_pass")
    check(display.get("schema") == "OLEANDER_BOUNDED_HEALING_DISPLAY_v0.2", "display_schema")
    check(display.get("master_type") == "CAD_NATIVE", "cad_native_master")
    check(display.get("geometry_authority") == "FREECAD_OCCT_BREP", "occt_authority")
    check(display.get("display_authority") == "DISPLAY_DERIVATIVE_ONLY", "display_only")
    check(display.get("ole_id") == "OLE_BREP_HEAL::SEWN_R002", "ole_id")
    check(display.get("operation") == "SEW_COINCIDENT_BOUNDARY_FACES", "sewing_operation")
    check(abs(float(display.get("sewing_tolerance_mm")) - 1.0e-6) < 1e-15, "sewing_tolerance")
    check(display.get("gap_repair_state") == "NOT_VALIDATED", "gap_repair_not_validated")

    r2 = manifest["revision2"]
    check(r2["disconnected"]["solid_count"] == 0, "preheal_disconnected_has_no_solid")
    check(r2["sewn"]["solid_count"] == 1, "sewn_has_one_solid")
    check(r2["sewn"]["is_valid"] is True, "sewn_valid")
    check(abs(r2["sewn"]["volume_mm3"] - r2["source"]["volume_mm3"]) < 1e-5, "sewn_volume_preserved")
    check(r2["raw_fused"]["solid_count"] == 1, "raw_fused_single_solid")
    check(r2["refined"]["solid_count"] == 1 and r2["refined"]["is_valid"] is True, "refined_valid_single_solid")
    check(abs(r2["refined"]["volume_mm3"] - r2["raw_fused"]["volume_mm3"]) < 1e-5, "refined_volume_preserved")
    check(
        r2["refined"]["face_count"] < r2["raw_fused"]["face_count"]
        or r2["refined"]["edge_count"] < r2["raw_fused"]["edge_count"],
        "redundant_topology_reduced",
    )
    check(manifest["expected_failure_cases"]["nonzero_geometric_gap_repair"] == "PASS", "nonzero_gap_repair_failure_gate")
    check(manifest["healing_contract"]["nonzero_gap_repair"] == "NOT_VALIDATED_AND_REJECTED", "gap_repair_contract_boundary")

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    mesh = bpy.data.meshes.new("OLE_BREP_HEAL_DISPLAY_MESH")
    mesh.from_pydata(display["vertices_mm"], [], display["triangles"])
    mesh.update()
    obj = bpy.data.objects.new("OLE_BREP_HEAL_DISPLAY", mesh)
    bpy.context.collection.objects.link(obj)
    obj["ole_id"] = display["ole_id"]
    obj["operation"] = display["operation"]
    obj["sewing_tolerance_mm"] = float(display["sewing_tolerance_mm"])
    obj["gap_repair_state"] = display["gap_repair_state"]
    obj["master_type"] = "CAD_NATIVE"
    obj["master_locator"] = display["source_fcstd"]
    obj["source_fcstd_sha256"] = display["source_fcstd_sha256"]
    obj["source_step"] = display["source_step"]
    obj["source_step_sha256"] = display["source_step_sha256"]
    obj["refined_step"] = display["refined_step"]
    obj["refined_step_sha256"] = display["refined_step_sha256"]
    obj["authoritative_geometry_kernel"] = "FREECAD_OCCT_BREP"
    obj["geometry_authority"] = "DISPLAY_DERIVATIVE_ONLY"
    bpy.context.view_layer.update()

    bbox = display["bbox_mm"]
    check(abs(obj.dimensions.x - bbox[0]) < 1e-3, "display_width")
    check(abs(obj.dimensions.y - bbox[1]) < 1e-3, "display_depth")
    check(abs(obj.dimensions.z - bbox[2]) < 1e-3, "display_height")
    check(abs(obj.dimensions.x - 100.0) < 1e-3, "display_width_100")
    check(abs(obj.dimensions.y - 50.0) < 1e-3, "display_depth_50")
    check(abs(obj.dimensions.z - 10.0) < 1e-3, "display_height_10")
    check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "mesh_not_brep_authority")

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    name = obj.name
    fcstd_sha = obj["source_fcstd_sha256"]
    sewn_step_sha = obj["source_step_sha256"]
    refined_step_sha = obj["refined_step_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    reopened = bpy.data.objects.get(name)
    check(reopened is not None, "blend_reopen")
    check(reopened["ole_id"] == "OLE_BREP_HEAL::SEWN_R002", "ole_id_reopen")
    check(reopened["operation"] == "SEW_COINCIDENT_BOUNDARY_FACES", "operation_reopen")
    check(abs(float(reopened["sewing_tolerance_mm"]) - 1.0e-6) < 1e-15, "tolerance_reopen")
    check(reopened["gap_repair_state"] == "NOT_VALIDATED", "gap_state_reopen")
    check(reopened["source_fcstd_sha256"] == fcstd_sha, "fcstd_sha_reopen")
    check(reopened["source_step_sha256"] == sewn_step_sha, "sewn_step_sha_reopen")
    check(reopened["refined_step_sha256"] == refined_step_sha, "refined_step_sha_reopen")
    check(reopened["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "authority_reopen")

    result = {
        "schema": "OLEANDER_BOUNDED_HEALING_BLENDER_READBACK_v0.2",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "checks": checks,
        "authority": {"master": "FreeCAD/OCCT healed B-Rep", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "blender_mesh_is_brep",
            "general_brep_healing",
            "nonzero_gap_repair",
            "arbitrary_import_repair",
            "self_intersection_repair",
            "nonmanifold_repair",
            "topological_naming_stability",
        ],
    }
    print("OLEANDER_BOUNDED_HEALING_BLENDER_READBACK=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
