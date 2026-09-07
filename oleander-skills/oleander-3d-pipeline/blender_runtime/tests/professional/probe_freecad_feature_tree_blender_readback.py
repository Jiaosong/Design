"""Blender readback for bounded FreeCAD native parametric feature tree.

The FCStd PartDesign tree remains authoritative. Blender receives only the R002
triangulated display derivative plus explicit OLE lineage/provenance.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import bpy

ROOT = Path(os.environ.get("OLEANDER_CAD_FEATURE_TREE_DIR", "/tmp/oleander-cad-feature-tree"))
DISPLAY = ROOT / "oleander_feature_tree_R002_display.json"
REOPEN = ROOT / "oleander_feature_tree_R002_readback.blend"
checks: list[str] = []


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def main() -> None:
    data = json.loads(DISPLAY.read_text(encoding="utf-8"))
    check(data.get("schema") == "OLEANDER_CAD_FEATURE_TREE_DISPLAY_DERIVATIVE_v0.1", "display_schema")
    check(data.get("master_type") == "CAD_NATIVE", "cad_native_master")
    check(data.get("geometry_authority") == "FREECAD_PARTDESIGN_FEATURE_TREE", "feature_tree_authority")
    check(data.get("display_authority") == "DISPLAY_DERIVATIVE_ONLY", "display_only")
    check(data.get("units") == "mm", "metric_units")
    check(data.get("ole_lineage") == ["OLE_DATUM::BRACKET_SKETCH_PLANE", "OLE_SKETCH::BRACKET_PROFILE", "OLE_FEATURE::PAD_001"], "ole_lineage")

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001

    mesh = bpy.data.meshes.new("OLE_FEATURE_TREE_R002_DISPLAY_MESH")
    mesh.from_pydata(data["vertices_mm"], [], data["triangles"])
    mesh.update()
    obj = bpy.data.objects.new("OLE_FEATURE_TREE_R002_DISPLAY", mesh)
    bpy.context.collection.objects.link(obj)
    obj["ole_id"] = "OLE_FEATURE::PAD_001"
    obj["master_type"] = "CAD_NATIVE"
    obj["master_locator"] = data["source_fcstd"]
    obj["source_fcstd_sha256"] = data["source_fcstd_sha256"]
    obj["source_step"] = data["source_step"]
    obj["source_step_sha256"] = data["source_step_sha256"]
    obj["authoritative_geometry_kernel"] = "FREECAD_PARTDESIGN_FEATURE_TREE"
    obj["geometry_authority"] = "DISPLAY_DERIVATIVE_ONLY"
    obj["datum_ole_id"] = data["ole_lineage"][0]
    obj["sketch_ole_id"] = data["ole_lineage"][1]
    obj["feature_ole_id"] = data["ole_lineage"][2]

    bpy.context.view_layer.update()
    check(abs(obj.dimensions.x - 100.0) < 1e-3, "display_width_100")
    check(abs(obj.dimensions.y - 50.0) < 1e-3, "display_depth_50")
    check(abs(obj.dimensions.z - 10.0) < 1e-3, "display_height_10")
    check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "mesh_not_feature_tree_authority")

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    name = obj.name
    fcstd_sha = obj["source_fcstd_sha256"]
    step_sha = obj["source_step_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    reopened = bpy.data.objects.get(name)
    check(reopened is not None, "blend_reopen")
    check(reopened["ole_id"] == "OLE_FEATURE::PAD_001", "feature_id_reopen")
    check(reopened["datum_ole_id"] == "OLE_DATUM::BRACKET_SKETCH_PLANE", "datum_id_reopen")
    check(reopened["sketch_ole_id"] == "OLE_SKETCH::BRACKET_PROFILE", "sketch_id_reopen")
    check(reopened["source_fcstd_sha256"] == fcstd_sha, "fcstd_sha_reopen")
    check(reopened["source_step_sha256"] == step_sha, "step_sha_reopen")
    check(reopened["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "authority_reopen")

    result = {
        "schema": "OLEANDER_FREECAD_FEATURE_TREE_BLENDER_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "checks": checks,
        "authority": {"master": "FreeCAD PartDesign feature tree", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "non_claims": ["P0_A_PARAMETRIC_CAD_PASS", "blender_mesh_is_parametric_cad", "general_feature_tree", "assembly_mates"]
    }
    print("OLEANDER_FREECAD_FEATURE_TREE_BLENDER_READBACK=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
