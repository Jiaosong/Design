"""Blender readback for the stable-selector FreeCAD/OCCT B-Rep feature probe."""

from __future__ import annotations

import json
import os
from pathlib import Path

import bpy

ROOT = Path(os.environ.get("OLEANDER_DIRECT_BREP_DIR", "/tmp/oleander-direct-brep"))
DISPLAY = ROOT / "oleander_stable_selector_brep_display.json"
MANIFEST = ROOT / "oleander_stable_selector_brep.json"
REOPEN = ROOT / "oleander_stable_selector_brep_readback.blend"
checks: list[str] = []


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def main() -> None:
    display = json.loads(DISPLAY.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    check(manifest.get("status") == "PASS", "freecad_manifest_pass")
    check(display.get("schema") == "OLEANDER_STABLE_SELECTOR_BREP_DISPLAY_v0.1", "display_schema")
    check(display.get("master_type") == "CAD_NATIVE", "cad_native_master")
    check(display.get("geometry_authority") == "FREECAD_OCCT_BREP", "occt_authority")
    check(display.get("display_authority") == "DISPLAY_DERIVATIVE_ONLY", "display_only")
    check(display.get("feature_role") == "FILLET", "feature_role")
    check(display.get("selector_id") == "SELECTOR::VERTICAL_STRAIGHT_OUTER_EDGES", "selector_id")
    check(int(display.get("revision")) == 2, "revision2")
    check(display.get("units") == "mm", "metric_units")

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001

    mesh = bpy.data.meshes.new("OLE_STABLE_SELECTOR_BREP_DISPLAY_MESH")
    mesh.from_pydata(display["vertices_mm"], [], display["triangles"])
    mesh.update()
    obj = bpy.data.objects.new("OLE_STABLE_SELECTOR_BREP_DISPLAY", mesh)
    bpy.context.collection.objects.link(obj)
    obj["ole_id"] = display["feature_ole_id"]
    obj["feature_role"] = display["feature_role"]
    obj["selector_id"] = display["selector_id"]
    obj["revision"] = int(display["revision"])
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
    check(abs(obj.dimensions.x - 100.0) < 1e-3, "revision2_width_100")
    check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "mesh_not_brep_authority")

    r1 = manifest["revision1"]
    r2 = manifest["revision2"]
    check(r1["selectors"]["vertical_edges"]["selected_count"] == 4, "revision1_selector_count")
    check(r2["selectors"]["vertical_edges"]["selected_count"] == 4, "revision2_selector_count")
    check(r1["selectors"]["top_face"]["selected_count"] == 1, "revision1_top_face_count")
    check(r2["selectors"]["top_face"]["selected_count"] == 1, "revision2_top_face_count")
    check(r2["fillet"]["volume_mm3"] > r1["fillet"]["volume_mm3"], "fillet_revision_volume_change")
    check(r2["chamfer"]["volume_mm3"] > r1["chamfer"]["volume_mm3"], "chamfer_revision_volume_change")
    check(r2["shell"]["volume_mm3"] > r1["shell"]["volume_mm3"], "shell_revision_volume_change")

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    name = obj.name
    fcstd_sha = obj["source_fcstd_sha256"]
    step_sha = obj["source_step_sha256"]
    selector_id = obj["selector_id"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    reopened = bpy.data.objects.get(name)
    check(reopened is not None, "blend_reopen")
    check(reopened["ole_id"] == "OLE_BREP::FILLET_002", "ole_id_reopen")
    check(reopened["selector_id"] == selector_id, "selector_reopen")
    check(reopened["source_fcstd_sha256"] == fcstd_sha, "fcstd_sha_reopen")
    check(reopened["source_step_sha256"] == step_sha, "step_sha_reopen")
    check(reopened["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "authority_reopen")

    result = {
        "schema": "OLEANDER_STABLE_SELECTOR_BREP_BLENDER_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "checks": checks,
        "authority": {"master": "FreeCAD/OCCT B-Rep", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "blender_mesh_is_brep",
            "persistent_topological_naming",
            "direct_face_push_pull",
            "general_fillet_shell_robustness"
        ]
    }
    print("OLEANDER_STABLE_SELECTOR_BREP_BLENDER_READBACK=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
