"""Blender display-only readback for bounded FreeCAD planar face in-plane translation."""

from __future__ import annotations

import json
import os
from pathlib import Path

import bpy

ROOT = Path(os.environ.get("OLEANDER_FACE_TRANSLATE_DIR", "/tmp/oleander-face-translate"))
DISPLAY = ROOT / "oleander_planar_face_translate_display.json"
MANIFEST = ROOT / "oleander_planar_face_translate_manifest.json"
REOPEN = ROOT / "oleander_planar_face_translate_readback.blend"
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
    check(manifest.get("schema") == "OLEANDER_FREECAD_PLANAR_FACE_TRANSLATE_v0.1", "manifest_schema")
    check(manifest.get("status") == "PASS", "freecad_manifest_pass")
    check(display.get("schema") == "OLEANDER_PLANAR_FACE_TRANSLATE_DISPLAY_v0.1", "display_schema")
    check(display.get("master_type") == "CAD_NATIVE", "cad_native_master")
    check(display.get("geometry_authority") == "FREECAD_OCCT_BREP", "occt_authority")
    check(display.get("display_authority") == "DISPLAY_DERIVATIVE_ONLY", "display_only")
    check(display.get("ole_id") == "OLE_DIRECT_FACE_TRANSLATE::DIAG_R002", "ole_id")
    check(display.get("selector_id") == "SELECTOR::TOP_PLANAR_FACE", "selector")
    check(display.get("operation") == "BRepTools_ReShape_TOP_FACE_TRANSLATE_IN_PLANE", "operation")
    check(display.get("units") == "mm", "units")
    check(display.get("translation_mm") == [3.0, 4.0, 0.0], "diagonal_translation_vector")
    check(close(float(display.get("translation_distance_mm")), 5.0), "diagonal_translation_distance")
    check(manifest["revision2"]["x_operation"]["translation_mm"] == [5.0, 0.0, 0.0], "manifest_x_translation")
    check(manifest["revision2"]["y_operation"]["translation_mm"] == [0.0, -4.0, 0.0], "manifest_y_translation")
    check(manifest["revision2"]["diag_operation"]["translation_mm"] == [3.0, 4.0, 0.0], "manifest_diag_translation")
    check(manifest["revision2"]["x"]["solid_count"] == 1, "x_one_solid")
    check(manifest["revision2"]["y"]["solid_count"] == 1, "y_one_solid")
    check(manifest["revision2"]["diag"]["solid_count"] == 1, "diag_one_solid")
    check(manifest["revision2"]["diag_operation"]["replaced_face_count"] == 5, "diag_five_replacements")
    check(manifest["expected_failure_cases"]["zero_translation"] == "PASS", "zero_translation_failure_gate")
    check(manifest["expected_failure_cases"]["excessive_translation"] == "PASS", "excessive_translation_failure_gate")

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    mesh = bpy.data.meshes.new("OLE_FACE_TRANSLATE_DISPLAY_MESH")
    mesh.from_pydata(display["vertices_mm"], [], display["triangles"])
    mesh.update()
    obj = bpy.data.objects.new("OLE_FACE_TRANSLATE_DISPLAY", mesh)
    bpy.context.collection.objects.link(obj)
    obj["ole_id"] = display["ole_id"]
    obj["selector_id"] = display["selector_id"]
    obj["operation"] = display["operation"]
    obj["translation_mm"] = display["translation_mm"]
    obj["translation_distance_mm"] = float(display["translation_distance_mm"])
    obj["units"] = "mm"
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
    check(abs(obj.dimensions.x - 103.0) < 1e-3, "diagonal_translation_x_envelope")
    check(abs(obj.dimensions.y - 54.0) < 1e-3, "diagonal_translation_y_envelope")
    check(abs(obj.dimensions.z - 10.0) < 1e-3, "height_preserved")
    check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "mesh_not_brep_authority")

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    name = obj.name
    fcstd_sha = obj["source_fcstd_sha256"]
    step_sha = obj["source_step_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    r = bpy.data.objects.get(name)
    check(r is not None, "blend_reopen")
    check(r["ole_id"] == "OLE_DIRECT_FACE_TRANSLATE::DIAG_R002", "ole_id_reopen")
    check(r["selector_id"] == "SELECTOR::TOP_PLANAR_FACE", "selector_reopen")
    check(r["operation"] == "BRepTools_ReShape_TOP_FACE_TRANSLATE_IN_PLANE", "operation_reopen")
    check(list(r["translation_mm"]) == [3.0, 4.0, 0.0], "translation_reopen")
    check(close(float(r["translation_distance_mm"]), 5.0), "translation_distance_reopen")
    check(r["units"] == "mm", "units_reopen")
    check(r["source_fcstd_sha256"] == fcstd_sha, "fcstd_sha_reopen")
    check(r["source_step_sha256"] == step_sha, "step_sha_reopen")
    check(r["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "authority_reopen")

    result = {
        "schema": "OLEANDER_PLANAR_FACE_TRANSLATE_BLENDER_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "checks": checks,
        "authority": {"master": "FreeCAD/OCCT B-Rep face translate", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "general_face_translate",
            "normal_direction_push_pull",
            "arbitrary_face_rotate",
            "nonplanar_face_translate",
            "persistent_topological_naming",
        ],
    }
    print("OLEANDER_PLANAR_FACE_TRANSLATE_BLENDER_READBACK=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
