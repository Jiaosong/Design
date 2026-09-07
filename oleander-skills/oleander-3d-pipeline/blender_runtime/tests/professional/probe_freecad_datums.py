"""OLEANDER professional probe for native FreeCAD PartDesign datums.

Executed by FreeCADCmd. The scope is deliberately bounded to actual
PartDesign::Plane / PartDesign::Line / PartDesign::Point objects attached to the
Body origin references. OLE stable IDs and a compact datum manifest are added as
OLEANDER governance metadata; the underlying datum geometry remains FreeCAD
native authority.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import FreeCAD as App

OUT = Path(os.environ.get("OLEANDER_CAD_DATUM_DIR", "/tmp/oleander-cad-datums"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_native_datums.FCStd"
MANIFEST = OUT / "oleander_native_datums.json"
checks: list[str] = []


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def add_ole_properties(obj, ole_id: str, datum_role: str) -> None:
    obj.addProperty("App::PropertyString", "OLE_ID", "OLEANDER")
    obj.OLE_ID = ole_id
    obj.addProperty("App::PropertyString", "OLE_DatumRole", "OLEANDER")
    obj.OLE_DatumRole = datum_role
    obj.addProperty("App::PropertyString", "OLE_Authority", "OLEANDER")
    obj.OLE_Authority = "FREECAD_NATIVE_DATUM"


def placement_payload(obj) -> dict:
    p = obj.Placement
    q = p.Rotation.Q
    return {
        "position_mm": [p.Base.x, p.Base.y, p.Base.z],
        "quaternion_xyzw": [q[0], q[1], q[2], q[3]],
    }


def main() -> None:
    doc = App.newDocument("OLEANDER_NATIVE_DATUMS")
    body = doc.addObject("PartDesign::Body", "OLE_CAD_BODY")
    body.Label = "OLEANDER CAD Body"

    plane = doc.addObject("PartDesign::Plane", "OLE_DATUM_PLANE_XY")
    plane.AttachmentSupport = [(doc.XY_Plane, "")]
    plane.MapMode = "FlatFace"
    body.addObject(plane)
    add_ole_properties(plane, "OLE_DATUM::PLANE_XY", "PRIMARY_SKETCH_PLANE")

    axis = doc.addObject("PartDesign::Line", "OLE_DATUM_AXIS_X")
    axis.AttachmentSupport = [(doc.XY_Plane, "")]
    axis.MapMode = "ObjectX"
    body.addObject(axis)
    add_ole_properties(axis, "OLE_DATUM::AXIS_X", "PRIMARY_X_AXIS")

    point = doc.addObject("PartDesign::Point", "OLE_DATUM_POINT_ORIGIN")
    point.AttachmentSupport = [(doc.XY_Plane, "")]
    point.MapMode = "ObjectOrigin"
    body.addObject(point)
    add_ole_properties(point, "OLE_DATUM::POINT_ORIGIN", "PRIMARY_ORIGIN")

    doc.recompute()
    check(plane.TypeId == "PartDesign::Plane", "native_plane_type")
    check(axis.TypeId == "PartDesign::Line", "native_axis_type")
    check(point.TypeId == "PartDesign::Point", "native_point_type")
    check(plane.OLE_ID == "OLE_DATUM::PLANE_XY", "plane_ole_id")
    check(axis.OLE_ID == "OLE_DATUM::AXIS_X", "axis_ole_id")
    check(point.OLE_ID == "OLE_DATUM::POINT_ORIGIN", "point_ole_id")
    check(plane.OLE_Authority == "FREECAD_NATIVE_DATUM", "plane_authority")
    check(axis.OLE_Authority == "FREECAD_NATIVE_DATUM", "axis_authority")
    check(point.OLE_Authority == "FREECAD_NATIVE_DATUM", "point_authority")
    check(plane.MapMode == "FlatFace", "plane_map_mode")
    check(axis.MapMode == "ObjectX", "axis_map_mode")
    check(point.MapMode == "ObjectOrigin", "point_map_mode")

    doc.saveAs(str(FCSTD))
    check(FCSTD.exists() and FCSTD.stat().st_size > 0, "fcstd_saved")
    App.closeDocument(doc.Name)

    reopened = App.openDocument(str(FCSTD))
    r_plane = reopened.getObject("OLE_DATUM_PLANE_XY")
    r_axis = reopened.getObject("OLE_DATUM_AXIS_X")
    r_point = reopened.getObject("OLE_DATUM_POINT_ORIGIN")
    check(r_plane is not None and r_plane.TypeId == "PartDesign::Plane", "plane_reopen")
    check(r_axis is not None and r_axis.TypeId == "PartDesign::Line", "axis_reopen")
    check(r_point is not None and r_point.TypeId == "PartDesign::Point", "point_reopen")
    check(r_plane.OLE_ID == "OLE_DATUM::PLANE_XY", "plane_ole_id_reopen")
    check(r_axis.OLE_ID == "OLE_DATUM::AXIS_X", "axis_ole_id_reopen")
    check(r_point.OLE_ID == "OLE_DATUM::POINT_ORIGIN", "point_ole_id_reopen")
    check(r_plane.MapMode == "FlatFace", "plane_map_mode_reopen")
    check(r_axis.MapMode == "ObjectX", "axis_map_mode_reopen")
    check(r_point.MapMode == "ObjectOrigin", "point_map_mode_reopen")

    datums = []
    for obj, kind, role in (
        (r_plane, "PLANE", "PRIMARY_SKETCH_PLANE"),
        (r_axis, "AXIS", "PRIMARY_X_AXIS"),
        (r_point, "POINT", "PRIMARY_ORIGIN"),
    ):
        datums.append({
            "ole_id": obj.OLE_ID,
            "kind": kind,
            "role": role,
            "freecad_name": obj.Name,
            "freecad_type_id": obj.TypeId,
            "map_mode": obj.MapMode,
            "authority": obj.OLE_Authority,
            "placement": placement_payload(obj),
        })

    result = {
        "schema": "OLEANDER_FREECAD_NATIVE_DATUM_PROBE_v0.1",
        "status": "PASS",
        "dependency_state": "RUNTIME_PROBED",
        "freecad_version": ".".join(str(x) for x in App.Version()[:3]),
        "fcstd": str(FCSTD),
        "datums": datums,
        "checks": checks,
        "non_claims": [
            "P0_A_PARAMETRIC_CAD_PASS",
            "feature_binding_to_datum",
            "topological_naming_stability",
            "assembly_reference_frames",
            "engineering_approval",
        ],
    }
    MANIFEST.write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
    print("OLEANDER_FREECAD_NATIVE_DATUM_PROBE=" + json.dumps(result, sort_keys=True))


main()
