"""Blender display-only readback for bounded cylindrical nonplanar face offset."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

import bpy

ROOT = Path(os.environ.get("OLEANDER_CYLINDRICAL_FACE_OFFSET_DIR", "/tmp/oleander-cylindrical-face-offset"))
DISPLAY = ROOT / "oleander_cylindrical_face_offset_display.json"
MANIFEST = ROOT / "oleander_cylindrical_face_offset_manifest.json"
REOPEN = ROOT / "oleander_cylindrical_face_offset_readback.blend"
checks: list[str] = []
EXPECTED = {
    "R001": {"source_outer": 30.0, "inner": 15.0, "height": 20.0, "offset": 2.0, "result_outer": 32.0},
    "R002": {"source_outer": 40.0, "inner": 20.0, "height": 25.0, "offset": -3.0, "result_outer": 37.0},
}
TESSELLATION_BBOX_DEFICIT_MM = 0.5


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def close(a, b, tol=1e-5):
    return abs(float(a) - float(b)) <= tol


def main():
    display = json.loads(DISPLAY.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    check(manifest.get("schema") == "OLEANDER_FREECAD_CYLINDRICAL_FACE_OFFSET_v0.1", "manifest_schema")
    check(manifest.get("status") == "PASS", "manifest_pass")
    check(display.get("schema") == "OLEANDER_CYLINDRICAL_FACE_OFFSET_DISPLAY_v0.1", "display_schema")
    check(display.get("geometry_authority") == "FREECAD_OCCT_BREP", "occt_authority")
    check(display.get("display_authority") == "DISPLAY_DERIVATIVE_ONLY", "display_only")
    check(manifest["expected_failure_cases"] == {"excessive_offset": "PASS", "invalid_tube": "PASS", "selector_miss": "PASS", "wall_collapse": "PASS", "zero_offset": "PASS"}, "failure_gates")
    revisions = {item["revision"]: item for item in display["revisions"]}
    check(set(revisions) == set(EXPECTED), "revision_set")

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    for name, expected in EXPECTED.items():
        item = revisions[name]
        check(item["operation"] == "BRepTools_ReShape_NONPLANAR_CYLINDRICAL_FACE_RADIAL_OFFSET", "operation_" + name)
        check(item["selector_id"] == "SELECTOR::OUTER_CYLINDRICAL_FACE::MAX_RADIUS", "selector_" + name)
        for key, field in [("source_outer", "source_outer_radius_mm"), ("inner", "inner_radius_mm"), ("height", "height_mm"), ("offset", "offset_mm"), ("result_outer", "result_outer_radius_mm")]:
            check(close(item[field], expected[key]), field + "_" + name)
        expected_volume = math.pi * (expected["result_outer"] ** 2 - expected["inner"] ** 2) * expected["height"]
        check(close(item["volume_mm3"], expected_volume, 1e-3), "volume_formula_" + name)
        check(manifest[name]["metrics"]["solid_count"] == 1, "one_solid_" + name)
        check(manifest[name]["metrics"]["face_count"] == 4, "four_faces_" + name)

        mesh = bpy.data.meshes.new("OLE_CYL_FACE_OFFSET_MESH_" + name)
        mesh.from_pydata(item["vertices_mm"], [], item["triangles"])
        mesh.update()
        obj = bpy.data.objects.new("OLE_CYL_FACE_OFFSET_" + name, mesh)
        bpy.context.collection.objects.link(obj)
        obj["ole_id"] = item["ole_id"]
        obj["operation"] = item["operation"]
        obj["selector_id"] = item["selector_id"]
        obj["source_outer_radius_mm"] = float(item["source_outer_radius_mm"])
        obj["inner_radius_mm"] = float(item["inner_radius_mm"])
        obj["offset_mm"] = float(item["offset_mm"])
        obj["result_outer_radius_mm"] = float(item["result_outer_radius_mm"])
        obj["height_mm"] = float(item["height_mm"])
        obj["master_locator"] = display["source_fcstd"]
        obj["source_fcstd_sha256"] = display["source_fcstd_sha256"]
        obj["source_step"] = item["source_step"]
        obj["source_step_sha256"] = item["source_step_sha256"]
        obj["geometry_authority"] = "DISPLAY_DERIVATIVE_ONLY"

    bpy.context.view_layer.update()
    for name in EXPECTED:
        obj = bpy.data.objects["OLE_CYL_FACE_OFFSET_" + name]
        mesh_dims = [obj.dimensions.x, obj.dimensions.y, obj.dimensions.z]
        brep_bbox = revisions[name]["bbox_mm"]
        for axis, mesh_dim, brep_dim in zip("XYZ", mesh_dims, brep_bbox):
            check(mesh_dim <= brep_dim + 1e-3, "display_bbox_not_exceed_brep_" + axis + "_" + name)
            check(brep_dim - mesh_dim <= TESSELLATION_BBOX_DEFICIT_MM, "display_bbox_deficit_bounded_" + axis + "_" + name)
        check(close(mesh_dims[2], EXPECTED[name]["height"], 1e-3), "display_height_exact_" + name)

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    source_sha = display["source_fcstd_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    for name, expected in EXPECTED.items():
        obj = bpy.data.objects.get("OLE_CYL_FACE_OFFSET_" + name)
        check(obj is not None, "reopen_object_" + name)
        check(obj["selector_id"] == "SELECTOR::OUTER_CYLINDRICAL_FACE::MAX_RADIUS", "reopen_selector_" + name)
        check(close(obj["result_outer_radius_mm"], expected["result_outer"]), "reopen_outer_radius_" + name)
        check(close(obj["inner_radius_mm"], expected["inner"]), "reopen_inner_radius_" + name)
        check(close(obj["offset_mm"], expected["offset"]), "reopen_offset_" + name)
        check(obj["source_fcstd_sha256"] == source_sha, "reopen_fcstd_sha_" + name)
        check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "reopen_authority_" + name)

    print("OLEANDER_CYLINDRICAL_FACE_OFFSET_BLENDER_READBACK=" + json.dumps({
        "schema": "OLEANDER_CYLINDRICAL_FACE_OFFSET_BLENDER_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "revisions": sorted(EXPECTED),
        "tessellation_bbox_deficit_limit_mm": TESSELLATION_BBOX_DEFICIT_MM,
        "checks": checks,
        "authority": {"master": "FreeCAD/OCCT nonplanar cylindrical face offset", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "non_claims": ["P0_B_DIRECT_BREP_PASS", "general_push_pull", "arbitrary_curved_face_offset", "freeform_nonplanar_face_edit", "persistent_topological_naming"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
