"""Blender display-only readback for bounded oblique FreeCAD face translation."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

import bpy

ROOT = Path(os.environ.get("OLEANDER_OBLIQUE_FACE_TRANSLATE_DIR", "/tmp/oleander-oblique-face-translate"))
DISPLAY = ROOT / "oleander_oblique_face_translate_display.json"
MANIFEST = ROOT / "oleander_oblique_face_translate_manifest.json"
REOPEN = ROOT / "oleander_oblique_face_translate_readback.blend"
checks: list[str] = []

EXPECTED_YAW = {"R001": 30.0, "R002": -25.0}


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def close(a: float, b: float, tol: float = 1e-5) -> bool:
    return abs(a - b) <= tol


def dot(a, b):
    return sum(float(x) * float(y) for x, y in zip(a, b))


def length(v):
    return math.sqrt(dot(v, v))


def is_axis_aligned(n):
    values = [abs(float(v)) for v in n]
    return max(values) > 0.999999 and sum(v > 1e-6 for v in values) == 1


def main() -> None:
    display = json.loads(DISPLAY.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    check(manifest.get("schema") == "OLEANDER_FREECAD_OBLIQUE_FACE_TRANSLATE_v0.1", "manifest_schema")
    check(manifest.get("status") == "PASS", "manifest_pass")
    check(display.get("schema") == "OLEANDER_OBLIQUE_FACE_TRANSLATE_DISPLAY_v0.1", "display_schema")
    check(display.get("master_type") == "CAD_NATIVE", "cad_native_master")
    check(display.get("geometry_authority") == "FREECAD_OCCT_BREP", "occt_authority")
    check(display.get("display_authority") == "DISPLAY_DERIVATIVE_ONLY", "display_only")
    check(manifest["expected_failure_cases"] == {"zero": "PASS", "normal_component": "PASS", "excessive": "PASS", "selector_miss": "PASS"}, "failure_gates")

    revisions = {item["revision"]: item for item in display["revisions"]}
    check(set(revisions) == set(EXPECTED_YAW), "revision_set")
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001

    created = []
    for name, yaw in EXPECTED_YAW.items():
        item = revisions[name]
        normal = item["selector_world_normal"]
        delta = item["translation_world_mm"]
        check(close(float(item["yaw_deg"]), yaw), "yaw_" + name)
        check(item["selector_id"] == "SELECTOR::LOCAL_POS_X_FACE", "selector_" + name)
        check(not is_axis_aligned(normal), "oblique_normal_" + name)
        check(close(length(normal), 1.0), "unit_normal_" + name)
        check(close(length(delta), 5.0), "five_mm_delta_" + name)
        check(abs(dot(normal, delta)) < 1e-6, "tangent_delta_" + name)
        check(manifest[name]["metrics"]["solid_count"] == 1, "one_solid_" + name)
        check(manifest[name]["metrics"]["face_count"] == 6, "six_faces_" + name)
        check(close(float(manifest[name]["operation"]["translation_distance_mm"]), 5.0), "manifest_distance_" + name)

        mesh = bpy.data.meshes.new("OLE_OBLIQUE_FACE_TRANSLATE_MESH_" + name)
        mesh.from_pydata(item["vertices_mm"], [], item["triangles"])
        mesh.update()
        obj = bpy.data.objects.new("OLE_OBLIQUE_FACE_TRANSLATE_" + name, mesh)
        bpy.context.collection.objects.link(obj)
        obj["ole_id"] = item["ole_id"]
        obj["yaw_deg"] = float(item["yaw_deg"])
        obj["selector_id"] = item["selector_id"]
        obj["selector_world_normal"] = normal
        obj["translation_world_mm"] = delta
        obj["translation_distance_mm"] = float(item["translation_distance_mm"])
        obj["units"] = "mm"
        obj["master_type"] = "CAD_NATIVE"
        obj["master_locator"] = display["source_fcstd"]
        obj["source_fcstd_sha256"] = display["source_fcstd_sha256"]
        obj["source_step"] = item["source_step"]
        obj["source_step_sha256"] = item["source_step_sha256"]
        obj["authoritative_geometry_kernel"] = "FREECAD_OCCT_BREP"
        obj["geometry_authority"] = "DISPLAY_DERIVATIVE_ONLY"
        created.append(obj)

    bpy.context.view_layer.update()
    for obj in created:
        name = obj.name.removeprefix("OLE_OBLIQUE_FACE_TRANSLATE_")
        expected_bbox = revisions[name]["bbox_mm"]
        actual_bbox = [obj.dimensions.x, obj.dimensions.y, obj.dimensions.z]
        check(all(close(a, b, 1e-3) for a, b in zip(actual_bbox, expected_bbox)), "object_bbox_" + name)
        check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "display_authority_" + name)

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    source_sha = display["source_fcstd_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    for name, yaw in EXPECTED_YAW.items():
        obj = bpy.data.objects.get("OLE_OBLIQUE_FACE_TRANSLATE_" + name)
        check(obj is not None, "reopen_object_" + name)
        check(close(float(obj["yaw_deg"]), yaw), "reopen_yaw_" + name)
        check(obj["selector_id"] == "SELECTOR::LOCAL_POS_X_FACE", "reopen_selector_" + name)
        check(not is_axis_aligned(list(obj["selector_world_normal"])), "reopen_oblique_normal_" + name)
        check(close(length(list(obj["translation_world_mm"])), 5.0), "reopen_translation_" + name)
        check(obj["source_fcstd_sha256"] == source_sha, "reopen_fcstd_sha_" + name)
        check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "reopen_authority_" + name)

    result = {
        "schema": "OLEANDER_OBLIQUE_FACE_TRANSLATE_BLENDER_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "revisions": sorted(EXPECTED_YAW),
        "checks": checks,
        "authority": {"master": "FreeCAD/OCCT oblique planar face translate", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "arbitrary_3d_oriented_planar_face_translate",
            "nonplanar_face_translate",
            "normal_direction_push_pull",
            "arbitrary_face_rotate",
            "persistent_topological_naming"
        ]
    }
    print("OLEANDER_OBLIQUE_FACE_TRANSLATE_BLENDER_READBACK=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
