"""Blender display-only readback for multi-orientation FreeCAD face translation."""

from __future__ import annotations

import json
import os
from pathlib import Path

import bpy

ROOT = Path(os.environ.get("OLEANDER_MULTI_FACE_TRANSLATE_DIR", "/tmp/oleander-multi-face-translate"))
DISPLAY = ROOT / "oleander_multi_orientation_face_translate_display.json"
MANIFEST = ROOT / "oleander_multi_orientation_face_translate_manifest.json"
REOPEN = ROOT / "oleander_multi_orientation_face_translate_readback.blend"
checks: list[str] = []

EXPECTED = {
    "TOP_Z": {"normal": [0.0, 0.0, 1.0], "delta": [3.0, 4.0, 0.0], "bbox": [103.0, 64.0, 12.0]},
    "SIDE_X": {"normal": [1.0, 0.0, 0.0], "delta": [0.0, 4.0, 3.0], "bbox": [100.0, 64.0, 15.0]},
    "SIDE_Y": {"normal": [0.0, 1.0, 0.0], "delta": [4.0, 0.0, 3.0], "bbox": [104.0, 60.0, 15.0]},
}


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def close(a: float, b: float, tol: float = 1e-5) -> bool:
    return abs(a - b) <= tol


def main() -> None:
    display = json.loads(DISPLAY.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    check(manifest.get("schema") == "OLEANDER_FREECAD_MULTI_ORIENTATION_FACE_TRANSLATE_v0.1", "manifest_schema")
    check(manifest.get("status") == "PASS", "manifest_pass")
    check(display.get("schema") == "OLEANDER_MULTI_ORIENTATION_FACE_TRANSLATE_DISPLAY_v0.1", "display_schema")
    check(display.get("master_type") == "CAD_NATIVE", "cad_native_master")
    check(display.get("geometry_authority") == "FREECAD_OCCT_BREP", "occt_authority")
    check(display.get("display_authority") == "DISPLAY_DERIVATIVE_ONLY", "display_only")
    check(display.get("units") == "mm", "units")
    check(manifest["expected_failure_cases"] == {"zero": "PASS", "normal_component": "PASS", "excessive": "PASS"}, "failure_gates")

    cases = {case["case"]: case for case in display["cases"]}
    check(set(cases) == set(EXPECTED), "display_case_set")

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    created = []
    for name, expected in EXPECTED.items():
        case = cases[name]
        check(case["selector_normal"] == expected["normal"], "normal_" + name)
        check(case["translation_mm"] == expected["delta"], "delta_" + name)
        check(close(float(case["translation_distance_mm"]), 5.0), "distance_" + name)
        check(all(close(a, b) for a, b in zip(case["bbox_mm"], expected["bbox"])), "manifest_bbox_" + name)

        mesh = bpy.data.meshes.new("OLE_MULTI_FACE_TRANSLATE_MESH_" + name)
        mesh.from_pydata(case["vertices_mm"], [], case["triangles"])
        mesh.update()
        obj = bpy.data.objects.new("OLE_MULTI_FACE_TRANSLATE_" + name, mesh)
        bpy.context.collection.objects.link(obj)
        obj["ole_id"] = case["ole_id"]
        obj["selector_id"] = case["selector_id"]
        obj["selector_normal"] = case["selector_normal"]
        obj["translation_mm"] = case["translation_mm"]
        obj["translation_distance_mm"] = float(case["translation_distance_mm"])
        obj["units"] = "mm"
        obj["master_type"] = "CAD_NATIVE"
        obj["master_locator"] = display["source_fcstd"]
        obj["source_fcstd_sha256"] = display["source_fcstd_sha256"]
        obj["source_step"] = case["source_step"]
        obj["source_step_sha256"] = case["source_step_sha256"]
        obj["authoritative_geometry_kernel"] = "FREECAD_OCCT_BREP"
        obj["geometry_authority"] = "DISPLAY_DERIVATIVE_ONLY"
        created.append(obj)

    bpy.context.view_layer.update()
    for obj in created:
        name = obj.name.removeprefix("OLE_MULTI_FACE_TRANSLATE_")
        expected = EXPECTED[name]
        dims = [obj.dimensions.x, obj.dimensions.y, obj.dimensions.z]
        check(all(close(a, b, 1e-3) for a, b in zip(dims, expected["bbox"])), "object_bbox_" + name)
        check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "display_authority_" + name)

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    fcstd_sha = display["source_fcstd_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    for name, expected in EXPECTED.items():
        obj = bpy.data.objects.get("OLE_MULTI_FACE_TRANSLATE_" + name)
        check(obj is not None, "reopen_object_" + name)
        check(list(obj["selector_normal"]) == expected["normal"], "reopen_normal_" + name)
        check(list(obj["translation_mm"]) == expected["delta"], "reopen_delta_" + name)
        check(close(float(obj["translation_distance_mm"]), 5.0), "reopen_distance_" + name)
        check(obj["source_fcstd_sha256"] == fcstd_sha, "reopen_fcstd_sha_" + name)
        check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "reopen_authority_" + name)

    result = {
        "schema": "OLEANDER_MULTI_ORIENTATION_FACE_TRANSLATE_BLENDER_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "cases": sorted(EXPECTED),
        "checks": checks,
        "authority": {"master": "FreeCAD/OCCT multi-orientation planar face translate", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "arbitrary_oblique_planar_face_translate",
            "nonplanar_face_translate",
            "normal_direction_push_pull",
            "arbitrary_face_rotate",
            "persistent_topological_naming",
        ],
    }
    print("OLEANDER_MULTI_ORIENTATION_FACE_TRANSLATE_BLENDER_READBACK=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
