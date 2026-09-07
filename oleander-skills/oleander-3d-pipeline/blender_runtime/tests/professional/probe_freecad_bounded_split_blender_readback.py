"""Blender readback for bounded FreeCAD BOPTools SplitAPI result."""

from __future__ import annotations

import json
import os
from pathlib import Path

import bpy

ROOT = Path(os.environ.get("OLEANDER_SPLIT_DIR", "/tmp/oleander-bounded-split"))
DISPLAY = ROOT / "oleander_bounded_split_display.json"
MANIFEST = ROOT / "oleander_bounded_split_manifest.json"
REOPEN = ROOT / "oleander_bounded_split_readback.blend"
checks: list[str] = []


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def main() -> None:
    display = json.loads(DISPLAY.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    check(manifest.get("status") == "PASS", "freecad_manifest_pass")
    check(display.get("schema") == "OLEANDER_BOUNDED_SPLIT_DISPLAY_v0.1", "display_schema")
    check(display.get("master_type") == "CAD_NATIVE", "cad_native_master")
    check(display.get("geometry_authority") == "FREECAD_OCCT_BREP", "occt_authority")
    check(display.get("display_authority") == "DISPLAY_DERIVATIVE_ONLY", "display_only")
    check(display.get("operation") == "BOPTOOLS_SPLIT_API", "split_operation")
    check(display.get("split_datum") == {"axis": "X", "value_mm": 40.0}, "split_datum")
    pieces = display.get("pieces") or []
    check(len(pieces) == 2, "two_display_pieces")

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    objects = []
    expected = {
        "OLE_SPLIT::PIECE_A_R002": (40.0, 0.0),
        "OLE_SPLIT::PIECE_B_R002": (80.0, 40.0),
    }
    for index, piece in enumerate(pieces):
        ole_id = piece["ole_id"]
        check(ole_id in expected, f"piece_{index}_known_ole_id")
        mesh = bpy.data.meshes.new(f"OLE_SPLIT_MESH_{index}")
        mesh.from_pydata(piece["vertices_mm"], [], piece["triangles"])
        mesh.update()
        obj = bpy.data.objects.new(f"OLE_SPLIT_DISPLAY_{index}", mesh)
        bpy.context.collection.objects.link(obj)
        obj["ole_id"] = ole_id
        obj["operation"] = "BOPTOOLS_SPLIT_API"
        obj["split_datum"] = "DATUM::X=40mm"
        obj["master_type"] = "CAD_NATIVE"
        obj["master_locator"] = display["source_fcstd"]
        obj["source_fcstd_sha256"] = display["source_fcstd_sha256"]
        obj["source_step"] = piece["source_step"]
        obj["source_step_sha256"] = piece["source_step_sha256"]
        obj["authoritative_geometry_kernel"] = "FREECAD_OCCT_BREP"
        obj["geometry_authority"] = "DISPLAY_DERIVATIVE_ONLY"
        bpy.context.view_layer.update()
        width, xmin = expected[ole_id]
        check(abs(obj.dimensions.x - width) < 1e-3, f"{ole_id}_width")
        check(abs(obj.dimensions.y - 50.0) < 1e-3, f"{ole_id}_depth")
        check(abs(obj.dimensions.z - 10.0) < 1e-3, f"{ole_id}_height")
        check(abs(piece["origin_mm"][0] - xmin) < 1e-6, f"{ole_id}_origin")
        check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", f"{ole_id}_display_only")
        objects.append(obj)

    r2 = manifest["revision2"]
    check(abs(r2["piece_a"]["volume_mm3"] + r2["piece_b"]["volume_mm3"] - r2["base"]["volume_mm3"]) < 1e-4, "volume_conservation")
    check(manifest["expected_failure_cases"]["nonintersecting_split_datum"] == "PASS", "failure_gate")

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    saved = [(o.name, o["ole_id"], o["source_step_sha256"]) for o in objects]
    fcstd_sha = display["source_fcstd_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    for name, ole_id, step_sha in saved:
        obj = bpy.data.objects.get(name)
        check(obj is not None, f"{ole_id}_blend_reopen")
        check(obj["ole_id"] == ole_id, f"{ole_id}_ole_id_reopen")
        check(obj["operation"] == "BOPTOOLS_SPLIT_API", f"{ole_id}_operation_reopen")
        check(obj["split_datum"] == "DATUM::X=40mm", f"{ole_id}_datum_reopen")
        check(obj["source_fcstd_sha256"] == fcstd_sha, f"{ole_id}_fcstd_sha_reopen")
        check(obj["source_step_sha256"] == step_sha, f"{ole_id}_step_sha_reopen")
        check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", f"{ole_id}_authority_reopen")

    result = {
        "schema": "OLEANDER_BOUNDED_SPLIT_BLENDER_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "checks": checks,
        "authority": {"master": "FreeCAD/OCCT B-Rep split pieces", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "non_claims": ["P0_B_DIRECT_BREP_PASS", "blender_mesh_is_brep", "general_split_trim", "trim_surface_editing", "persistent_topological_naming"]
    }
    print("OLEANDER_BOUNDED_SPLIT_BLENDER_READBACK=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
