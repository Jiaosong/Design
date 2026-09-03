"""Blender readback for bounded FreeCAD/OCCT healing result."""

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
    check(manifest.get("status") == "PASS", "freecad_manifest_pass")
    check(display.get("schema") == "OLEANDER_BOUNDED_HEALING_DISPLAY_v0.1", "display_schema")
    check(display.get("master_type") == "CAD_NATIVE", "cad_native_master")
    check(display.get("geometry_authority") == "FREECAD_OCCT_BREP", "occt_authority")
    check(display.get("display_authority") == "DISPLAY_DERIVATIVE_ONLY", "display_only")
    check(display.get("ole_id") == "OLE_BREP_HEAL::R002", "ole_id")
    check(display.get("operation") == "SEW_FIX_REMOVE_SPLITTER_MAKE_SOLID", "healing_operation")
    check(abs(float(display.get("source_gap_mm")) - 0.0005) < 1e-12, "source_gap")
    check(abs(float(display.get("healing_tolerance_mm")) - 0.001) < 1e-12, "healing_tolerance")
    check(manifest["revision2"]["damaged"]["solid_count"] == 0, "preheal_no_solid")
    check(manifest["revision2"]["healed"]["solid_count"] == 1, "postheal_one_solid")
    check(manifest["revision2"]["healed"]["is_valid"] is True, "postheal_valid")
    check(manifest["expected_failure_cases"]["gap_exceeds_governed_tolerance"] == "PASS", "over_tolerance_failure")

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
    obj["source_gap_mm"] = float(display["source_gap_mm"])
    obj["healing_tolerance_mm"] = float(display["healing_tolerance_mm"])
    obj["master_type"] = "CAD_NATIVE"
    obj["master_locator"] = display["source_fcstd"]
    obj["source_fcstd_sha256"] = display["source_fcstd_sha256"]
    obj["source_step"] = display["source_step"]
    obj["source_step_sha256"] = display["source_step_sha256"]
    obj["authoritative_geometry_kernel"] = "FREECAD_OCCT_BREP"
    obj["geometry_authority"] = "DISPLAY_DERIVATIVE_ONLY"
    bpy.context.view_layer.update()

    bbox = display["bbox_mm"]
    check(abs(obj.dimensions.x - bbox[0]) < 1e-3, "display_width")
    check(abs(obj.dimensions.y - bbox[1]) < 1e-3, "display_depth")
    check(abs(obj.dimensions.z - bbox[2]) < 1e-3, "display_height")
    check(abs(obj.dimensions.x - 100.0) < 1e-3, "display_width_100")
    check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "mesh_not_brep_authority")

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    name = obj.name
    fcstd_sha = obj["source_fcstd_sha256"]
    step_sha = obj["source_step_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    r = bpy.data.objects.get(name)
    check(r is not None, "blend_reopen")
    check(r["ole_id"] == "OLE_BREP_HEAL::R002", "ole_id_reopen")
    check(r["operation"] == "SEW_FIX_REMOVE_SPLITTER_MAKE_SOLID", "operation_reopen")
    check(abs(float(r["source_gap_mm"]) - 0.0005) < 1e-12, "source_gap_reopen")
    check(abs(float(r["healing_tolerance_mm"]) - 0.001) < 1e-12, "healing_tolerance_reopen")
    check(r["source_fcstd_sha256"] == fcstd_sha, "fcstd_sha_reopen")
    check(r["source_step_sha256"] == step_sha, "step_sha_reopen")
    check(r["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "authority_reopen")

    result = {
        "schema": "OLEANDER_BOUNDED_HEALING_BLENDER_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "checks": checks,
        "authority": {"master": "FreeCAD/OCCT healed B-Rep", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "non_claims": ["P0_B_DIRECT_BREP_PASS", "blender_mesh_is_brep", "general_brep_healing", "arbitrary_import_repair", "topological_naming_stability"]
    }
    print("OLEANDER_BOUNDED_HEALING_BLENDER_READBACK=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
