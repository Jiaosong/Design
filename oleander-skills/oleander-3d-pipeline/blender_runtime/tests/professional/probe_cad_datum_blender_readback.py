"""Blender readback for FreeCAD native datum provenance.

Blender receives reference-display objects only. The authoritative datum
objects remain PartDesign::Plane/Line/Point in the FCStd master.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import bpy
from mathutils import Quaternion

ROOT = Path(os.environ.get("OLEANDER_CAD_DATUM_DIR", "/tmp/oleander-cad-datums"))
MANIFEST = ROOT / "oleander_native_datums.json"
REOPEN = ROOT / "oleander_native_datums_readback.blend"
checks: list[str] = []


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def main() -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    check(payload.get("status") == "PASS", "freecad_manifest_pass")
    check(payload.get("schema") == "OLEANDER_FREECAD_NATIVE_DATUM_PROBE_v0.1", "manifest_schema")

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001

    names = []
    for datum in payload["datums"]:
        obj = bpy.data.objects.new(f"{datum['ole_id']}_REFERENCE", None)
        bpy.context.collection.objects.link(obj)
        position = datum["placement"]["position_mm"]
        q = datum["placement"]["quaternion_xyzw"]
        obj.location = position
        obj.rotation_mode = "QUATERNION"
        obj.rotation_quaternion = Quaternion((q[3], q[0], q[1], q[2]))
        obj.empty_display_type = "PLAIN_AXES"
        obj["ole_id"] = datum["ole_id"]
        obj["datum_kind"] = datum["kind"]
        obj["datum_role"] = datum["role"]
        obj["freecad_type_id"] = datum["freecad_type_id"]
        obj["freecad_map_mode"] = datum["map_mode"]
        obj["master_type"] = "CAD_NATIVE"
        obj["master_locator"] = payload["fcstd"]
        obj["authoritative_datum_kernel"] = "FREECAD_PARTDESIGN"
        obj["geometry_authority"] = "REFERENCE_DERIVATIVE_ONLY"
        names.append(obj.name)

    check(len(names) == 3, "three_reference_derivatives")
    ids = {bpy.data.objects[name]["ole_id"] for name in names}
    check(ids == {"OLE_DATUM::PLANE_XY", "OLE_DATUM::AXIS_X", "OLE_DATUM::POINT_ORIGIN"}, "stable_ole_ids")
    check(all(bpy.data.objects[name]["master_type"] == "CAD_NATIVE" for name in names), "cad_master_type")
    check(all(bpy.data.objects[name]["geometry_authority"] == "REFERENCE_DERIVATIVE_ONLY" for name in names), "reference_derivative_only")
    check(all(bpy.data.objects[name]["authoritative_datum_kernel"] == "FREECAD_PARTDESIGN" for name in names), "freecad_datum_authority")

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "blend_saved")
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    for name in names:
        obj = bpy.data.objects.get(name)
        check(obj is not None, f"reopen_{name}")
        check(obj["geometry_authority"] == "REFERENCE_DERIVATIVE_ONLY", f"authority_reopen_{name}")
        check(obj["master_locator"] == payload["fcstd"], f"master_locator_reopen_{name}")

    result = {
        "schema": "OLEANDER_CAD_DATUM_BLENDER_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "checks": checks,
        "authority": {
            "master": "FreeCAD PartDesign native datums",
            "blender": "REFERENCE_DERIVATIVE_ONLY"
        },
        "non_claims": [
            "P0_A_PARAMETRIC_CAD_PASS",
            "blender_empty_is_cad_datum",
            "feature_binding_to_datum",
            "assembly_reference_frame_solver"
        ]
    }
    print("OLEANDER_CAD_DATUM_BLENDER_READBACK=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
