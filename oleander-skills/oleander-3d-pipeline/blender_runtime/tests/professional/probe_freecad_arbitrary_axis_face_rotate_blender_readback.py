"""Blender display-only readback for bounded offset arbitrary-axis face rotation."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

import bpy

ROOT = Path(os.environ.get("OLEANDER_ARBITRARY_AXIS_ROTATE_DIR", "/tmp/oleander-arbitrary-axis-rotate"))
DISPLAY = ROOT / "oleander_arbitrary_axis_face_rotate_display.json"
MANIFEST = ROOT / "oleander_arbitrary_axis_face_rotate_manifest.json"
REOPEN = ROOT / "oleander_arbitrary_axis_face_rotate_readback.blend"
checks: list[str] = []
EXPECTED = {
    "R001": {"yaw": 30.0, "pitch": 20.0, "angle": 2.0},
    "R002": {"yaw": -25.0, "pitch": -15.0, "angle": -2.5},
}


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def close(a, b, tol=1e-5):
    return abs(float(a) - float(b)) <= tol


def dot(a, b):
    return sum(float(x) * float(y) for x, y in zip(a, b))


def length(v):
    return math.sqrt(dot(v, v))


def is_full3d(v):
    n = max(length(v), 1e-12)
    return all(abs(float(x) / n) > 0.05 for x in v)


def main():
    display = json.loads(DISPLAY.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    check(manifest.get("schema") == "OLEANDER_FREECAD_ARBITRARY_AXIS_FACE_ROTATE_v0.1", "manifest_schema")
    check(manifest.get("status") == "PASS", "manifest_pass")
    check(display.get("schema") == "OLEANDER_ARBITRARY_AXIS_FACE_ROTATE_DISPLAY_v0.1", "display_schema")
    check(display.get("geometry_authority") == "FREECAD_OCCT_BREP", "occt_authority")
    check(display.get("display_authority") == "DISPLAY_DERIVATIVE_ONLY", "display_only")
    check(manifest["expected_failure_cases"] == {
        "center_pivot": "PASS",
        "excessive_angle": "PASS",
        "far_pivot": "PASS",
        "near_normal_axis": "PASS",
        "tangent_axis": "PASS",
        "zero_angle": "PASS",
        "zero_axis_coefficients": "PASS",
    }, "failure_gates")

    revisions = {item["revision"]: item for item in display["revisions"]}
    check(set(revisions) == set(EXPECTED), "revision_set")
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001

    for name, expected in EXPECTED.items():
        item = revisions[name]
        normal = item["selector_world_normal"]
        axis = item["axis_world_direction"]
        check(close(item["yaw_deg"], expected["yaw"]), "yaw_" + name)
        check(close(item["pitch_deg"], expected["pitch"]), "pitch_" + name)
        check(close(item["angle_deg"], expected["angle"]), "angle_" + name)
        check(close(item["actual_angle_deg"], expected["angle"]), "actual_angle_" + name)
        check(item["selector_id"] == "SELECTOR::LOCAL_POS_X_FACE", "selector_" + name)
        check(item["axis_id"] == "AXIS::OFFSET_PIVOT::ARBITRARY_LOCAL_2X_4Y_3Z", "axis_id_" + name)
        check(item["axis_coefficients"] == {"local_x": 2.0, "local_y": 4.0, "local_z": 3.0}, "axis_coefficients_" + name)
        check(item["pivot_offset_local_mm"] == {"local_x": 2.0, "local_y": 7.0, "local_z": -4.0}, "pivot_offsets_" + name)
        check(is_full3d(normal), "full3d_normal_" + name)
        check(is_full3d(axis), "full3d_axis_" + name)
        check(close(length(normal), 1.0), "unit_normal_" + name)
        check(close(length(axis), 1.0), "unit_axis_" + name)
        normal_component = abs(dot(normal, axis))
        check(0.10 < normal_component < 0.90, "axis_has_normal_and_tangent_components_" + name)
        check(close(normal_component, item["axis_normal_component_abs"], 1e-6), "axis_normal_component_record_" + name)
        check(item["pivot_offset_length_mm"] > 1.0, "offset_pivot_" + name)
        check(item["target_center_shift_mm"] > 0.05, "target_center_shift_" + name)
        check(length([a-b for a,b in zip(item["target_center_after_mm"], item["target_center_before_mm"])]) > 0.05, "center_before_after_distinct_" + name)
        check(manifest[name]["metrics"]["solid_count"] == 1, "one_solid_" + name)
        check(manifest[name]["metrics"]["face_count"] == 6, "six_faces_" + name)

        mesh = bpy.data.meshes.new("OLE_ARBITRARY_AXIS_FACE_ROTATE_MESH_" + name)
        mesh.from_pydata(item["vertices_mm"], [], item["triangles"])
        mesh.update()
        obj = bpy.data.objects.new("OLE_ARBITRARY_AXIS_FACE_ROTATE_" + name, mesh)
        bpy.context.collection.objects.link(obj)
        obj["ole_id"] = item["ole_id"]
        obj["yaw_deg"] = float(item["yaw_deg"])
        obj["pitch_deg"] = float(item["pitch_deg"])
        obj["angle_deg"] = float(item["angle_deg"])
        obj["actual_angle_deg"] = float(item["actual_angle_deg"])
        obj["selector_id"] = item["selector_id"]
        obj["axis_id"] = item["axis_id"]
        obj["axis_coefficients"] = [2.0, 4.0, 3.0]
        obj["pivot_offset_local_mm"] = [2.0, 7.0, -4.0]
        obj["selector_world_normal"] = normal
        obj["axis_world_direction"] = axis
        obj["axis_origin_mm"] = item["axis_origin_mm"]
        obj["target_center_before_mm"] = item["target_center_before_mm"]
        obj["target_center_after_mm"] = item["target_center_after_mm"]
        obj["target_center_shift_mm"] = float(item["target_center_shift_mm"])
        obj["master_locator"] = display["source_fcstd"]
        obj["source_fcstd_sha256"] = display["source_fcstd_sha256"]
        obj["source_step"] = item["source_step"]
        obj["source_step_sha256"] = item["source_step_sha256"]
        obj["geometry_authority"] = "DISPLAY_DERIVATIVE_ONLY"

    bpy.context.view_layer.update()
    check(dot(revisions["R001"]["axis_world_direction"], revisions["R002"]["axis_world_direction"]) < 0.99, "axis_world_direction_changes")
    for name in EXPECTED:
        obj = bpy.data.objects["OLE_ARBITRARY_AXIS_FACE_ROTATE_" + name]
        check(all(close(a, b, 1e-3) for a, b in zip([obj.dimensions.x, obj.dimensions.y, obj.dimensions.z], revisions[name]["bbox_mm"])), "bbox_" + name)

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    source_sha = display["source_fcstd_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    for name in EXPECTED:
        obj = bpy.data.objects.get("OLE_ARBITRARY_AXIS_FACE_ROTATE_" + name)
        check(obj is not None, "reopen_object_" + name)
        check(obj["axis_id"] == "AXIS::OFFSET_PIVOT::ARBITRARY_LOCAL_2X_4Y_3Z", "reopen_axis_id_" + name)
        check(list(obj["axis_coefficients"]) == [2.0, 4.0, 3.0], "reopen_axis_coefficients_" + name)
        check(list(obj["pivot_offset_local_mm"]) == [2.0, 7.0, -4.0], "reopen_pivot_offsets_" + name)
        check(is_full3d(list(obj["axis_world_direction"])), "reopen_full3d_axis_" + name)
        check(obj["target_center_shift_mm"] > 0.05, "reopen_center_shift_" + name)
        check(obj["source_fcstd_sha256"] == source_sha, "reopen_fcstd_sha_" + name)
        check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "reopen_authority_" + name)

    print("OLEANDER_ARBITRARY_AXIS_FACE_ROTATE_BLENDER_READBACK=" + json.dumps({
        "schema": "OLEANDER_ARBITRARY_AXIS_FACE_ROTATE_BLENDER_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "revisions": sorted(EXPECTED),
        "checks": checks,
        "authority": {"master": "FreeCAD/OCCT offset arbitrary-axis planar face rotate", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "non_claims": ["P0_B_DIRECT_BREP_PASS", "unrestricted_arbitrary_axis_face_rotate", "arbitrary_pivot_placement", "nonplanar_face_rotate", "persistent_topological_naming"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
