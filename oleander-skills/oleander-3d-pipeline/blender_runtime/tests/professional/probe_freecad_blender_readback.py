"""Blender-side readback for the FreeCAD/OCCT professional probe.

The FreeCAD FCStd/STEP/BREP source remains authoritative. Blender receives only
a typed triangulated display derivative and must preserve source identity,
metric scale and non-authoritative mesh status through save/reopen.
"""

from __future__ import annotations

import json
from pathlib import Path

import bpy

PAYLOAD = Path("/tmp/oleander-freecad-probe/oleander_brep_display_mesh.json")
REOPEN = Path("/tmp/oleander-freecad-probe/oleander_brep_display_readback.blend")
checks: list[str] = []


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def main() -> None:
    data = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    check(data.get("schema") == "OLEANDER_CAD_DISPLAY_DERIVATIVE_v0.1", "display_payload_schema")
    check(data.get("master_type") == "CAD_NATIVE", "cad_master_type_declared")
    check(data.get("geometry_authority") == "FREECAD_OCCT_BREP", "brep_authority_declared")
    check(data.get("units") == "mm", "display_payload_metric_units")

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001  # 1 Blender unit == 1 mm.

    mesh = bpy.data.meshes.new("OLE_BREP_DISPLAY_MESH")
    mesh.from_pydata(data["vertices_mm"], [], data["triangles"])
    mesh.update()
    obj = bpy.data.objects.new("OLE_PRO_PRODUCT_BREP_001_DISPLAY", mesh)
    bpy.context.collection.objects.link(obj)

    obj["ole_id"] = "OLE_PRO_PRODUCT_BREP_001"
    obj["master_type"] = "CAD_NATIVE"
    obj["master_locator"] = data["source_master"]
    obj["source_step"] = data["source_step"]
    obj["source_step_sha256"] = data["source_step_sha256"]
    obj["geometry_authority"] = "DISPLAY_DERIVATIVE_ONLY"
    obj["authoritative_geometry_kernel"] = "FREECAD_OCCT_BREP"
    obj["units_contract"] = "mm"

    check(len(mesh.vertices) == len(data["vertices_mm"]), "display_vertex_count")
    check(len(mesh.polygons) == len(data["triangles"]), "display_triangle_count")

    bpy.context.view_layer.update()
    dims = obj.dimensions
    source_bbox = data["source_bbox"]
    check(abs(dims.x - source_bbox["x_length_mm"]) < 1e-3, "blender_display_width_mm")
    check(abs(dims.y - source_bbox["y_length_mm"]) < 1e-3, "blender_display_depth_mm")
    check(abs(dims.z - source_bbox["z_length_mm"]) < 1e-3, "blender_display_height_mm")
    check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "mesh_not_promoted_to_brep_authority")

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blender_display_saved")
    name = obj.name
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    reopened = bpy.data.objects.get(name)
    check(reopened is not None, "blender_display_reopen")
    check(reopened["ole_id"] == "OLE_PRO_PRODUCT_BREP_001", "ole_identity_reopen")
    check(reopened["master_type"] == "CAD_NATIVE", "cad_master_type_reopen")
    check(reopened["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "display_authority_reopen")
    check(reopened["authoritative_geometry_kernel"] == "FREECAD_OCCT_BREP", "brep_kernel_provenance_reopen")
    check(reopened["source_step_sha256"] == data["source_step_sha256"], "step_hash_reopen")

    result = {
        "schema": "OLEANDER_PROFESSIONAL_DEPENDENCY_BLENDER_READBACK_v0.1",
        "dependency": "FreeCAD + OpenCascade",
        "blender": bpy.app.version_string,
        "status": "PASS",
        "dependency_state": "RUNTIME_PROBED",
        "checks": checks,
        "authority": {
            "master": "FreeCAD/OCCT B-Rep",
            "blender_object": "DISPLAY_DERIVATIVE_ONLY",
        },
        "non_claims": [
            "P0_A_PARAMETRIC_CAD_PASS",
            "P0_B_DIRECT_BREP_PASS",
            "blender_mesh_is_brep",
            "engineering_approval",
            "manufacturing_release",
        ],
    }
    print("OLEANDER_FREECAD_BLENDER_READBACK=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
