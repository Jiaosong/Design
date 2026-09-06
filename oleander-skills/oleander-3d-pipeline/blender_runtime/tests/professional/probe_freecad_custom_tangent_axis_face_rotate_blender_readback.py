"""Blender display-only readback for bounded custom tangent-axis face rotation."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

import bpy

ROOT = Path(os.environ.get("OLEANDER_CUSTOM_AXIS_ROTATE_DIR", "/tmp/oleander-custom-axis-rotate"))
DISPLAY = ROOT / "oleander_custom_tangent_axis_face_rotate_display.json"
MANIFEST = ROOT / "oleander_custom_tangent_axis_face_rotate_manifest.json"
REOPEN = ROOT / "oleander_custom_tangent_axis_face_rotate_readback.blend"
checks: list[str] = []
EXPECTED = {
    "R001": {"yaw": 30.0, "pitch": 20.0, "angle": 3.0},
    "R002": {"yaw": -25.0, "pitch": -15.0, "angle": -3.0},
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
    check(manifest.get("schema") == "OLEANDER_FREECAD_CUSTOM_TANGENT_AXIS_FACE_ROTATE_v0.1", "manifest_schema")
    check(manifest.get("status") == "PASS", "manifest_pass")
    check(display.get("schema") == "OLEANDER_CUSTOM_TANGENT_AXIS_FACE_ROTATE_DISPLAY_v0.1", "display_schema")
    check(display.get("geometry_authority") == "FREECAD_OCCT_BREP", "occt_authority")
    check(display.get("display_authority") == "DISPLAY_DERIVATIVE_ONLY", "display_only")
    check(manifest["expected_failure_cases"] == {"zero_angle":"PASS","excessive_angle":"PASS","axis_has_normal_component":"PASS","zero_axis_coefficients":"PASS"}, "failure_gates")

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
        check(item["axis_id"] == "AXIS::SELECTED_FACE_CENTER::CUSTOM_TANGENT_4Y_3Z", "axis_id_" + name)
        check(item["axis_coefficients"] == {"local_y":4.0,"local_z":3.0}, "axis_coefficients_" + name)
        check(is_full3d(normal), "full3d_normal_" + name)
        check(is_full3d(axis), "full3d_custom_axis_" + name)
        check(close(length(normal), 1.0), "unit_normal_" + name)
        check(close(length(axis), 1.0), "unit_axis_" + name)
        check(abs(dot(normal, axis)) < 1e-6, "axis_tangent_" + name)
        check(manifest[name]["metrics"]["solid_count"] == 1, "one_solid_" + name)
        check(manifest[name]["metrics"]["face_count"] == 6, "six_faces_" + name)

        mesh = bpy.data.meshes.new("OLE_CUSTOM_AXIS_FACE_ROTATE_MESH_" + name)
        mesh.from_pydata(item["vertices_mm"], [], item["triangles"])
        mesh.update()
        obj = bpy.data.objects.new("OLE_CUSTOM_AXIS_FACE_ROTATE_" + name, mesh)
        bpy.context.collection.objects.link(obj)
        obj["ole_id"] = item["ole_id"]
        obj["yaw_deg"] = float(item["yaw_deg"])
        obj["pitch_deg"] = float(item["pitch_deg"])
        obj["angle_deg"] = float(item["angle_deg"])
        obj["actual_angle_deg"] = float(item["actual_angle_deg"])
        obj["selector_id"] = item["selector_id"]
        obj["axis_id"] = item["axis_id"]
        obj["axis_coeff_y"] = 4.0
        obj["axis_coeff_z"] = 3.0
        obj["selector_world_normal"] = normal
        obj["axis_world_direction"] = axis
        obj["expected_rotated_normal"] = item["expected_rotated_normal"]
        obj["master_locator"] = display["source_fcstd"]
        obj["source_fcstd_sha256"] = display["source_fcstd_sha256"]
        obj["source_step"] = item["source_step"]
        obj["source_step_sha256"] = item["source_step_sha256"]
        obj["geometry_authority"] = "DISPLAY_DERIVATIVE_ONLY"

    bpy.context.view_layer.update()
    check(dot(revisions["R001"]["axis_world_direction"], revisions["R002"]["axis_world_direction"]) < 0.99, "custom_axis_world_direction_changes")
    for name in EXPECTED:
        obj = bpy.data.objects["OLE_CUSTOM_AXIS_FACE_ROTATE_" + name]
        check(all(close(a,b,1e-3) for a,b in zip([obj.dimensions.x,obj.dimensions.y,obj.dimensions.z], revisions[name]["bbox_mm"])), "bbox_" + name)

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    source_sha = display["source_fcstd_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    for name, expected in EXPECTED.items():
        obj = bpy.data.objects.get("OLE_CUSTOM_AXIS_FACE_ROTATE_" + name)
        check(obj is not None, "reopen_object_" + name)
        check(obj["axis_id"] == "AXIS::SELECTED_FACE_CENTER::CUSTOM_TANGENT_4Y_3Z", "reopen_axis_id_" + name)
        check(close(obj["axis_coeff_y"],4.0) and close(obj["axis_coeff_z"],3.0), "reopen_coefficients_" + name)
        check(is_full3d(list(obj["axis_world_direction"])), "reopen_full3d_axis_" + name)
        check(obj["source_fcstd_sha256"] == source_sha, "reopen_fcstd_sha_" + name)
        check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "reopen_authority_" + name)

    print("OLEANDER_CUSTOM_TANGENT_AXIS_FACE_ROTATE_BLENDER_READBACK=" + json.dumps({
        "schema":"OLEANDER_CUSTOM_TANGENT_AXIS_FACE_ROTATE_BLENDER_READBACK_v0.1",
        "status":"PASS",
        "blender":bpy.app.version_string,
        "revisions":sorted(EXPECTED),
        "checks":checks,
        "authority":{"master":"FreeCAD/OCCT custom tangent-axis planar face rotate","blender":"DISPLAY_DERIVATIVE_ONLY"},
        "non_claims":["P0_B_DIRECT_BREP_PASS","general_arbitrary_axis_face_rotate","axis_not_constrained_to_face_tangent_plane","nonplanar_face_rotate","persistent_topological_naming"]
    }, sort_keys=True))


if __name__ == "__main__":
    main()
