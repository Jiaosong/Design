"""Blender display-only readback for bounded full-3D FreeCAD face rotation."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

import bpy

ROOT = Path(os.environ.get("OLEANDER_FULL3D_FACE_ROTATE_DIR", "/tmp/oleander-full3d-face-rotate"))
DISPLAY = ROOT / "oleander_full3d_face_rotate_display.json"
MANIFEST = ROOT / "oleander_full3d_face_rotate_manifest.json"
REOPEN = ROOT / "oleander_full3d_face_rotate_readback.blend"
checks: list[str] = []
EXPECTED = {
    "R001": {"yaw": 30.0, "pitch": 20.0, "angle": 4.0},
    "R002": {"yaw": -25.0, "pitch": -15.0, "angle": -4.0},
}


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


def is_full3d(v):
    n = [float(x) / max(length(v), 1e-12) for x in v]
    return all(abs(x) > 0.05 for x in n)


def main() -> None:
    display = json.loads(DISPLAY.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    check(manifest.get("schema") == "OLEANDER_FREECAD_FULL3D_FACE_ROTATE_v0.1", "manifest_schema")
    check(manifest.get("status") == "PASS", "manifest_pass")
    check(display.get("schema") == "OLEANDER_FULL3D_FACE_ROTATE_DISPLAY_v0.1", "display_schema")
    check(display.get("geometry_authority") == "FREECAD_OCCT_BREP", "occt_authority")
    check(display.get("display_authority") == "DISPLAY_DERIVATIVE_ONLY", "display_only")
    check(manifest["expected_failure_cases"] == {
        "zero_angle": "PASS",
        "excessive_angle": "PASS",
        "axis_has_normal_component": "PASS",
        "selector_miss": "PASS",
    }, "failure_gates")

    revisions = {item["revision"]: item for item in display["revisions"]}
    check(set(revisions) == set(EXPECTED), "revision_set")
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001

    for name, expected in EXPECTED.items():
        item = revisions[name]
        n = item["selector_world_normal"]
        axis = item["axis_world_direction"]
        rn = item["expected_rotated_normal"]
        check(close(float(item["yaw_deg"]), expected["yaw"]), "yaw_" + name)
        check(close(float(item["pitch_deg"]), expected["pitch"]), "pitch_" + name)
        check(close(float(item["angle_deg"]), expected["angle"]), "angle_" + name)
        check(close(float(item["actual_angle_deg"]), expected["angle"]), "actual_angle_" + name)
        check(item["selector_id"] == "SELECTOR::LOCAL_POS_X_FACE", "selector_" + name)
        check(item["axis_id"] == "AXIS::SELECTED_FACE_CENTER::LOCAL_POS_Y", "axis_id_" + name)
        check(is_full3d(n), "full3d_normal_" + name)
        check(is_full3d(axis), "full3d_axis_" + name)
        check(close(length(n), 1.0), "unit_normal_" + name)
        check(close(length(axis), 1.0), "unit_axis_" + name)
        check(abs(dot(n, axis)) < 1e-6, "axis_tangent_" + name)
        check(close(length(rn), 1.0), "unit_rotated_normal_" + name)
        check(manifest[name]["metrics"]["solid_count"] == 1, "one_solid_" + name)
        check(manifest[name]["metrics"]["face_count"] == 6, "six_faces_" + name)

        mesh = bpy.data.meshes.new("OLE_FULL3D_FACE_ROTATE_MESH_" + name)
        mesh.from_pydata(item["vertices_mm"], [], item["triangles"])
        mesh.update()
        obj = bpy.data.objects.new("OLE_FULL3D_FACE_ROTATE_" + name, mesh)
        bpy.context.collection.objects.link(obj)
        obj["ole_id"] = item["ole_id"]
        obj["yaw_deg"] = float(item["yaw_deg"])
        obj["pitch_deg"] = float(item["pitch_deg"])
        obj["angle_deg"] = float(item["angle_deg"])
        obj["actual_angle_deg"] = float(item["actual_angle_deg"])
        obj["selector_id"] = item["selector_id"]
        obj["axis_id"] = item["axis_id"]
        obj["selector_world_normal"] = n
        obj["axis_world_direction"] = axis
        obj["expected_rotated_normal"] = rn
        obj["master_locator"] = display["source_fcstd"]
        obj["source_fcstd_sha256"] = display["source_fcstd_sha256"]
        obj["source_step"] = item["source_step"]
        obj["source_step_sha256"] = item["source_step_sha256"]
        obj["geometry_authority"] = "DISPLAY_DERIVATIVE_ONLY"

    bpy.context.view_layer.update()
    for name in EXPECTED:
        obj = bpy.data.objects["OLE_FULL3D_FACE_ROTATE_" + name]
        expected_bbox = revisions[name]["bbox_mm"]
        actual_bbox = [obj.dimensions.x, obj.dimensions.y, obj.dimensions.z]
        check(all(close(a, b, 1e-3) for a, b in zip(actual_bbox, expected_bbox)), "bbox_" + name)

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    source_sha = display["source_fcstd_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    for name, expected in EXPECTED.items():
        obj = bpy.data.objects.get("OLE_FULL3D_FACE_ROTATE_" + name)
        check(obj is not None, "reopen_object_" + name)
        check(close(float(obj["yaw_deg"]), expected["yaw"]), "reopen_yaw_" + name)
        check(close(float(obj["pitch_deg"]), expected["pitch"]), "reopen_pitch_" + name)
        check(close(float(obj["angle_deg"]), expected["angle"]), "reopen_angle_" + name)
        check(is_full3d(list(obj["selector_world_normal"])), "reopen_full3d_normal_" + name)
        check(is_full3d(list(obj["axis_world_direction"])), "reopen_full3d_axis_" + name)
        check(obj["source_fcstd_sha256"] == source_sha, "reopen_fcstd_sha_" + name)
        check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "reopen_authority_" + name)

    print("OLEANDER_FULL3D_FACE_ROTATE_BLENDER_READBACK=" + json.dumps({
        "schema": "OLEANDER_FULL3D_FACE_ROTATE_BLENDER_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "revisions": sorted(EXPECTED),
        "checks": checks,
        "authority": {"master": "FreeCAD/OCCT full-3D-oriented planar face local-axis rotate", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "non_claims": ["P0_B_DIRECT_BREP_PASS", "general_face_rotate", "arbitrary_user_defined_rotation_axis", "nonplanar_face_rotate", "persistent_topological_naming"]
    }, sort_keys=True))


if __name__ == "__main__":
    main()
