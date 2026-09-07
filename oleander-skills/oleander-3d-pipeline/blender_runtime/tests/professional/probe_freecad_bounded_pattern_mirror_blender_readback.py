"""Blender display-only readback for bounded FreeCAD/OCCT pattern/mirror."""

from __future__ import annotations

import json
import os
from pathlib import Path

import bpy

ROOT = Path(os.environ.get("OLEANDER_PATTERN_MIRROR_DIR", "/tmp/oleander-pattern-mirror"))
DISPLAY = ROOT / "oleander_bounded_pattern_mirror_display.json"
MANIFEST = ROOT / "oleander_bounded_pattern_mirror_manifest.json"
REOPEN = ROOT / "oleander_bounded_pattern_mirror_readback.blend"
checks: list[str] = []


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def close(a, b, tol=1e-4):
    return abs(float(a) - float(b)) <= tol


def close_vec(a, b, tol=1e-3):
    return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))


def main():
    display = json.loads(DISPLAY.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    check(manifest["schema"] == "OLEANDER_FREECAD_BOUNDED_PATTERN_MIRROR_v0.1", "manifest_schema")
    check(manifest["status"] == "PASS", "manifest_pass")
    check(display["schema"] == "OLEANDER_BOUNDED_PATTERN_MIRROR_DISPLAY_v0.1", "display_schema")
    check(display["geometry_authority"] == "FREECAD_OCCT_BREP", "occt_authority")
    check(display["display_authority"] == "DISPLAY_DERIVATIVE_ONLY", "display_only")
    check(manifest["expected_failure_cases"] == {
        "mirror_duplicate_on_plane": "PASS",
        "mirror_outside_body": "PASS",
        "pattern_count_one": "PASS",
        "pattern_outside_body": "PASS",
        "pattern_zero_spacing": "PASS",
    }, "failure_gates")

    revisions = {r["revision"]: r for r in display["revisions"]}
    check(set(revisions) == {"R001_LINEAR_PATTERN", "R002_MIRROR"}, "revision_set")
    p = revisions["R001_LINEAR_PATTERN"]
    m = revisions["R002_MIRROR"]
    check(p["operation"] == "BRep_BOOLEAN_CUT_LINEAR_FEATURE_PATTERN", "pattern_operation")
    check(p["feature_centers_mm"] == [[30.0, 30.0, 0.0], [60.0, 30.0, 0.0], [90.0, 30.0, 0.0]], "pattern_centers")
    check(p["parameters"]["count"] == 3 and close(p["parameters"]["spacing_mm"], 30.0), "pattern_parameters")
    check(m["operation"] == "BRep_BOOLEAN_CUT_MIRRORED_FEATURE", "mirror_operation")
    check(m["feature_centers_mm"] == [[30.0, 30.0, 0.0], [90.0, 30.0, 0.0]], "mirror_centers")
    check(close(m["parameters"]["mirror_plane_x_mm"], 60.0), "mirror_plane")
    for name, item in revisions.items():
        check(close(item["feature_radius_mm"], 3.0), "radius_" + name)
        check(item["metrics"]["solid_count"] == 1, "one_solid_" + name)
        check(close_vec(item["metrics"]["bbox_mm"], [120.0, 60.0, 10.0]), "manifest_bbox_" + name)
        check(bool(item["vertices_mm"]) and bool(item["triangles"]), "display_mesh_" + name)

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    for name, item in revisions.items():
        mesh = bpy.data.meshes.new("OLE_PATTERN_MIRROR_MESH_" + name)
        mesh.from_pydata(item["vertices_mm"], [], item["triangles"])
        mesh.update()
        obj = bpy.data.objects.new("OLE_PATTERN_MIRROR_" + name, mesh)
        bpy.context.collection.objects.link(obj)
        obj["ole_id"] = item["ole_id"]
        obj["operation"] = item["operation"]
        obj["feature_type"] = item["feature_type"]
        obj["feature_radius_mm"] = item["feature_radius_mm"]
        obj["feature_centers_json"] = json.dumps(item["feature_centers_mm"])
        obj["parameters_json"] = json.dumps(item["parameters"], sort_keys=True)
        obj["source_fcstd"] = display["source_fcstd"]
        obj["source_fcstd_sha256"] = display["source_fcstd_sha256"]
        obj["source_step"] = item["source_step"]
        obj["source_step_sha256"] = item["source_step_sha256"]
        obj["geometry_authority"] = "DISPLAY_DERIVATIVE_ONLY"

    bpy.context.view_layer.update()
    for name, item in revisions.items():
        obj = bpy.data.objects["OLE_PATTERN_MIRROR_" + name]
        check(close_vec([obj.dimensions.x, obj.dimensions.y, obj.dimensions.z], item["metrics"]["bbox_mm"]), "bbox_" + name)

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    source_sha = display["source_fcstd_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    for name, item in revisions.items():
        obj = bpy.data.objects.get("OLE_PATTERN_MIRROR_" + name)
        check(obj is not None, "reopen_object_" + name)
        check(obj["ole_id"] == item["ole_id"], "reopen_id_" + name)
        check(obj["operation"] == item["operation"], "reopen_operation_" + name)
        check(json.loads(obj["feature_centers_json"]) == item["feature_centers_mm"], "reopen_centers_" + name)
        check(obj["source_fcstd_sha256"] == source_sha, "reopen_fcstd_sha_" + name)
        check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "reopen_authority_" + name)

    print("OLEANDER_BOUNDED_PATTERN_MIRROR_BLENDER_READBACK=" + json.dumps({
        "schema": "OLEANDER_BOUNDED_PATTERN_MIRROR_BLENDER_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "revisions": ["R001_LINEAR_PATTERN", "R002_MIRROR"],
        "checks": checks,
        "authority": {"master": "FreeCAD/OCCT BRep feature pattern/mirror", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "non_claims": ["P0_B_DIRECT_BREP_PASS", "general_feature_pattern_semantics", "circular_or_path_pattern", "general_mirror_semantics", "persistent_topological_naming", "assembly_pattern"],
    }, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
