"""Blender readback for bounded FreeCAD planar face-normal B-Rep edit."""

from __future__ import annotations

import json
import os
from pathlib import Path

import bpy

ROOT = Path(os.environ.get("OLEANDER_FACE_MOVE_DIR", "/tmp/oleander-face-move"))
DISPLAY = ROOT / "oleander_planar_face_move_display.json"
MANIFEST = ROOT / "oleander_planar_face_move_manifest.json"
REOPEN = ROOT / "oleander_planar_face_move_readback.blend"
checks: list[str] = []


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def main() -> None:
    display = json.loads(DISPLAY.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    check(manifest.get("status") == "PASS", "freecad_manifest_pass")
    check(display.get("schema") == "OLEANDER_PLANAR_FACE_MOVE_DISPLAY_DERIVATIVE_v0.1", "display_schema")
    check(display.get("master_type") == "CAD_NATIVE", "cad_native_master")
    check(display.get("geometry_authority") == "FREECAD_OCCT_BREP", "occt_authority")
    check(display.get("display_authority") == "DISPLAY_DERIVATIVE_ONLY", "display_only")
    check(display.get("ole_id") == "OLE_DIRECT_FACE_MOVE::PUSH_R002", "ole_id")
    check(display.get("selector_id") == "SELECTOR::TOP_PLANAR_FACE", "selector_id")
    check(display.get("operation") == "BRepTools_ReShape_FACE_AND_ADJACENT_FACE_REPLACEMENT", "kernel_operation")
    check(abs(float(display.get("delta_mm")) - 5.0) < 1e-9, "push_delta_5")
    check(display.get("units") == "mm", "metric_units")

    r1 = manifest["revision1"]
    r2 = manifest["revision2"]
    check(abs(r1["push"]["bbox_mm"][2] - 15.0) < 1e-6, "r1_push_height_15")
    check(abs(r2["push"]["bbox_mm"][2] - 15.0) < 1e-6, "r2_push_height_15")
    check(abs(r2["pull"]["bbox_mm"][2] - 7.0) < 1e-6, "r2_pull_height_7")
    check(r2["push_operation"]["replaced_face_count"] == 5, "push_replaced_face_count")
    check(r2["pull_operation"]["replaced_face_count"] == 5, "pull_replaced_face_count")
    check(manifest["expected_failure_cases"]["collapse_or_invert_face_move"] == "PASS", "collapse_failure_gate")

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    mesh = bpy.data.meshes.new("OLE_PLANAR_FACE_MOVE_DISPLAY_MESH")
    mesh.from_pydata(display["vertices_mm"], [], display["triangles"])
    mesh.update()
    obj = bpy.data.objects.new("OLE_PLANAR_FACE_MOVE_DISPLAY", mesh)
    bpy.context.collection.objects.link(obj)
    obj["ole_id"] = display["ole_id"]
    obj["selector_id"] = display["selector_id"]
    obj["operation"] = display["operation"]
    obj["delta_mm"] = float(display["delta_mm"])
    obj["master_type"] = "CAD_NATIVE"
    obj["master_locator"] = display["source_fcstd"]
    obj["source_fcstd_sha256"] = display["source_fcstd_sha256"]
    obj["source_step"] = display["source_step"]
    obj["source_step_sha256"] = display["source_step_sha256"]
    obj["authoritative_geometry_kernel"] = "FREECAD_OCCT_BREP"
    obj["geometry_authority"] = "DISPLAY_DERIVATIVE_ONLY"

    bpy.context.view_layer.update()
    expected = display["bbox_mm"]
    check(abs(obj.dimensions.x - expected[0]) < 1e-3, "display_width")
    check(abs(obj.dimensions.y - expected[1]) < 1e-3, "display_depth")
    check(abs(obj.dimensions.z - expected[2]) < 1e-3, "display_height")
    check(abs(obj.dimensions.x - 100.0) < 1e-3, "display_width_100")
    check(abs(obj.dimensions.y - 50.0) < 1e-3, "display_depth_50")
    check(abs(obj.dimensions.z - 15.0) < 1e-3, "display_height_15")
    check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "mesh_not_brep_authority")

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    name = obj.name
    fcstd_sha = obj["source_fcstd_sha256"]
    step_sha = obj["source_step_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    reopened = bpy.data.objects.get(name)
    check(reopened is not None, "blend_reopen")
    check(reopened["ole_id"] == "OLE_DIRECT_FACE_MOVE::PUSH_R002", "ole_id_reopen")
    check(reopened["selector_id"] == "SELECTOR::TOP_PLANAR_FACE", "selector_reopen")
    check(reopened["operation"] == "BRepTools_ReShape_FACE_AND_ADJACENT_FACE_REPLACEMENT", "operation_reopen")
    check(abs(float(reopened["delta_mm"]) - 5.0) < 1e-9, "delta_reopen")
    check(reopened["source_fcstd_sha256"] == fcstd_sha, "fcstd_sha_reopen")
    check(reopened["source_step_sha256"] == step_sha, "step_sha_reopen")
    check(reopened["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "authority_reopen")

    result = {
        "schema": "OLEANDER_PLANAR_FACE_MOVE_BLENDER_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "checks": checks,
        "authority": {"master": "FreeCAD/OCCT B-Rep", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "blender_mesh_is_brep",
            "general_push_pull",
            "arbitrary_face_move",
            "persistent_topological_naming",
            "face_rotate",
            "split_trim"
        ]
    }
    print("OLEANDER_PLANAR_FACE_MOVE_BLENDER_READBACK=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
