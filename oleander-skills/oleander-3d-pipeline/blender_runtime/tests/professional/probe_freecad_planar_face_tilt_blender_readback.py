"""Blender display-only readback for bounded FreeCAD planar face tilt."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

import bpy

ROOT = Path(os.environ.get("OLEANDER_FACE_TILT_DIR", "/tmp/oleander-face-tilt"))
DISPLAY = ROOT / "oleander_planar_face_tilt_display.json"
MANIFEST = ROOT / "oleander_planar_face_tilt_manifest.json"
REOPEN = ROOT / "oleander_planar_face_tilt_readback.blend"
checks: list[str] = []


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def close(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol


def main() -> None:
    display = json.loads(DISPLAY.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    check(manifest.get("schema") == "OLEANDER_FREECAD_PLANAR_FACE_TILT_v0.1", "manifest_schema")
    check(manifest.get("status") == "PASS", "freecad_manifest_pass")
    check(display.get("schema") == "OLEANDER_PLANAR_FACE_TILT_DISPLAY_v0.1", "display_schema")
    check(display.get("master_type") == "CAD_NATIVE", "cad_native_master")
    check(display.get("geometry_authority") == "FREECAD_OCCT_BREP", "occt_authority")
    check(display.get("display_authority") == "DISPLAY_DERIVATIVE_ONLY", "display_only")
    check(display.get("ole_id") == "OLE_DIRECT_FACE_TILT::POS_R002", "ole_id")
    check(display.get("selector_id") == "SELECTOR::TOP_PLANAR_FACE", "selector")
    check(display.get("operation") == "BRepTools_ReShape_TOP_FACE_TILT_Y", "operation")
    check(display.get("axis") == "TOP_FACE_CENTER_Y", "axis")
    check(display.get("angle_units") == "deg", "angle_units")
    check(close(float(display.get("angle_deg")), 5.0), "positive_angle")
    check(close(float(display.get("actual_angle_deg")), 5.0, 1e-5), "actual_positive_angle")
    check(close(float(manifest["revision2"]["positive_operation"]["actual_angle_deg"]), 5.0, 1e-5), "manifest_positive_angle")
    check(close(float(manifest["revision2"]["negative_operation"]["actual_angle_deg"]), -5.0, 1e-5), "manifest_negative_angle")
    check(manifest["revision2"]["positive"]["solid_count"] == 1, "positive_one_solid")
    check(manifest["revision2"]["negative"]["solid_count"] == 1, "negative_one_solid")
    check(manifest["revision2"]["positive_operation"]["replaced_face_count"] == 5, "positive_five_replacements")
    check(manifest["revision2"]["negative_operation"]["replaced_face_count"] == 5, "negative_five_replacements")
    check(manifest["expected_failure_cases"]["excessive_or_inverting_face_tilt"] == "PASS", "excessive_tilt_failure_gate")

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    mesh = bpy.data.meshes.new("OLE_FACE_TILT_DISPLAY_MESH")
    mesh.from_pydata(display["vertices_mm"], [], display["triangles"])
    mesh.update()
    obj = bpy.data.objects.new("OLE_FACE_TILT_DISPLAY", mesh)
    bpy.context.collection.objects.link(obj)
    obj["ole_id"] = display["ole_id"]
    obj["selector_id"] = display["selector_id"]
    obj["operation"] = display["operation"]
    obj["axis"] = display["axis"]
    obj["angle_deg"] = float(display["angle_deg"])
    obj["angle_units"] = "deg"
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
    check(abs(obj.dimensions.x - 100.0) < 1e-3, "display_base_width_100")
    check(abs(obj.dimensions.y - 50.0) < 1e-3, "display_depth_50")
    check(obj.dimensions.z > 10.0, "tilt_increases_bbox_height")
    check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "mesh_not_brep_authority")

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    name = obj.name
    fcstd_sha = obj["source_fcstd_sha256"]
    step_sha = obj["source_step_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    r = bpy.data.objects.get(name)
    check(r is not None, "blend_reopen")
    check(r["ole_id"] == "OLE_DIRECT_FACE_TILT::POS_R002", "ole_id_reopen")
    check(r["selector_id"] == "SELECTOR::TOP_PLANANAR_FACE" if False else r["selector_id"] == "SELECTOR::TOP_PLANAR_FACE", "selector_reopen")
    check(r["operation"] == "BRepTools_ReShape_TOP_FACE_TILT_Y", "operation_reopen")
    check(r["axis"] == "TOP_FACE_CENTER_Y", "axis_reopen")
    check(close(float(r["angle_deg"]), 5.0), "angle_reopen")
    check(r["angle_units"] == "deg", "angle_units_reopen")
    check(r["source_fcstd_sha256"] == fcstd_sha, "fcstd_sha_reopen")
    check(r["source_step_sha256"] == step_sha, "step_sha_reopen")
    check(r["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "authority_reopen")

    result = {
        "schema": "OLEANDER_PLANAR_FACE_TILT_BLENDER_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "checks": checks,
        "authority": {"master": "FreeCAD/OCCT B-Rep face tilt", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "blender_mesh_is_brep",
            "general_face_rotate",
            "arbitrary_rotation_axis",
            "nonplanar_face_rotate",
            "persistent_topological_naming"
        ]
    }
    print("OLEANDER_PLANAR_FACE_TILT_BLENDER_READBACK=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
