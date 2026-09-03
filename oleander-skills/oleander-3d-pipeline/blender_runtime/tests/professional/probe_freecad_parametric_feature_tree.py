"""OLEANDER bounded native FreeCAD parametric feature-tree probe.

Validates actual FreeCAD objects and dependencies:
PartDesign::Plane -> Sketcher::SketchObject -> PartDesign::Pad.
The sketch is dimensionally constrained and the width driving datum is edited
from 80 mm to 100 mm; the native Pad must recompute accordingly without manual
mesh editing. R002 also emits a typed tessellated display derivative for Blender
readback; the FCStd PartDesign tree remains authoritative.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import FreeCAD as App
import Part
import Sketcher

OUT = Path(os.environ.get("OLEANDER_CAD_FEATURE_TREE_DIR", "/tmp/oleander-cad-feature-tree"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD_R1 = OUT / "oleander_feature_tree_R001.FCStd"
FCSTD_R2 = OUT / "oleander_feature_tree_R002.FCStd"
STEP_R1 = OUT / "oleander_feature_tree_R001.step"
STEP_R2 = OUT / "oleander_feature_tree_R002.step"
DISPLAY_R2 = OUT / "oleander_feature_tree_R002_display.json"
MANIFEST = OUT / "oleander_feature_tree_manifest.json"
checks: list[str] = []


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def linked_object(value):
    """Normalize FreeCAD link / link-sub Python wrappers to their object."""
    if isinstance(value, (tuple, list)) and value:
        return value[0]
    return value


def add_ole(obj, ole_id: str, role: str) -> None:
    obj.addProperty("App::PropertyString", "OLE_ID", "OLEANDER")
    obj.OLE_ID = ole_id
    obj.addProperty("App::PropertyString", "OLE_Role", "OLEANDER")
    obj.OLE_Role = role


def add_rectangle(sketch, width: float, depth: float):
    lines = [
        Part.LineSegment(App.Vector(0, 0, 0), App.Vector(width, 0, 0)),
        Part.LineSegment(App.Vector(width, 0, 0), App.Vector(width, depth, 0)),
        Part.LineSegment(App.Vector(width, depth, 0), App.Vector(0, depth, 0)),
        Part.LineSegment(App.Vector(0, depth, 0), App.Vector(0, 0, 0)),
    ]
    ids = sketch.addGeometry(lines, False)
    if isinstance(ids, int):
        ids = [ids]
    check(len(ids) == 4, "four_rectangle_edges")
    sketch.addConstraint(Sketcher.Constraint("Coincident", 0, 2, 1, 1))
    sketch.addConstraint(Sketcher.Constraint("Coincident", 1, 2, 2, 1))
    sketch.addConstraint(Sketcher.Constraint("Coincident", 2, 2, 3, 1))
    sketch.addConstraint(Sketcher.Constraint("Coincident", 3, 2, 0, 1))
    sketch.addConstraint(Sketcher.Constraint("Horizontal", 0))
    sketch.addConstraint(Sketcher.Constraint("Vertical", 1))
    sketch.addConstraint(Sketcher.Constraint("Horizontal", 2))
    sketch.addConstraint(Sketcher.Constraint("Vertical", 3))
    sketch.addConstraint(Sketcher.Constraint("Coincident", 0, 1, -1, 1))
    width_id = sketch.addConstraint(Sketcher.Constraint("Distance", 0, width))
    depth_id = sketch.addConstraint(Sketcher.Constraint("Distance", 1, depth))
    return int(width_id), int(depth_id)


def shape_metrics(shape) -> dict:
    return {
        "bbox_mm": [shape.BoundBox.XLength, shape.BoundBox.YLength, shape.BoundBox.ZLength],
        "volume_mm3": shape.Volume,
        "solid_count": len(shape.Solids),
    }


def main() -> None:
    doc = App.newDocument("OLEANDER_NATIVE_FEATURE_TREE")
    body = doc.addObject("PartDesign::Body", "OLE_BODY")
    add_ole(body, "OLE_BODY::BRACKET_001", "CAD_BODY")

    datum = doc.addObject("PartDesign::Plane", "OLE_DATUM_PLANE")
    datum.AttachmentSupport = (doc.XY_Plane, [""])
    datum.MapMode = "FlatFace"
    body.addObject(datum)
    add_ole(datum, "OLE_DATUM::BRACKET_SKETCH_PLANE", "SKETCH_SUPPORT")

    sketch = doc.addObject("Sketcher::SketchObject", "OLE_SKETCH_PROFILE")
    sketch.AttachmentSupport = (datum, [""])
    sketch.MapMode = "FlatFace"
    body.addObject(sketch)
    add_ole(sketch, "OLE_SKETCH::BRACKET_PROFILE", "DRIVING_PROFILE")
    width_id, depth_id = add_rectangle(sketch, 80.0, 50.0)
    doc.recompute()
    check(sketch.solve() == 0, "revision1_sketch_solve")
    doc.recompute()
    check(bool(sketch.FullyConstrained), "revision1_fully_constrained")

    pad = doc.addObject("PartDesign::Pad", "OLE_PAD")
    pad.Profile = sketch
    pad.Length = 10.0
    body.addObject(pad)
    add_ole(pad, "OLE_FEATURE::PAD_001", "AUTHORITATIVE_SOLID_FEATURE")
    doc.recompute()
    check(linked_object(pad.Profile) == sketch, "pad_profile_dependency")
    check(linked_object(sketch.AttachmentSupport[0]) == datum, "sketch_datum_dependency")
    check(pad.Shape.isValid(), "revision1_pad_valid")
    check(len(pad.Shape.Solids) == 1, "revision1_single_solid")
    m1 = shape_metrics(pad.Shape)
    check(abs(m1["bbox_mm"][0] - 80.0) < 1e-6, "revision1_width")
    check(abs(m1["bbox_mm"][1] - 50.0) < 1e-6, "revision1_depth")
    check(abs(m1["bbox_mm"][2] - 10.0) < 1e-6, "revision1_height")
    doc.saveAs(str(FCSTD_R1))
    pad.Shape.exportStep(str(STEP_R1))
    check(FCSTD_R1.exists() and STEP_R1.exists(), "revision1_artifacts")

    rc = sketch.setDatum(width_id, App.Units.Quantity("100 mm"))
    check(rc == 0, "revision2_set_width_datum")
    doc.recompute()
    check(sketch.solve() == 0, "revision2_sketch_solve")
    doc.recompute()
    check(bool(sketch.FullyConstrained), "revision2_fully_constrained")
    check(pad.Shape.isValid(), "revision2_pad_valid")
    check(len(pad.Shape.Solids) == 1, "revision2_single_solid")
    m2 = shape_metrics(pad.Shape)
    check(abs(m2["bbox_mm"][0] - 100.0) < 1e-6, "revision2_width")
    check(abs(m2["bbox_mm"][1] - 50.0) < 1e-6, "revision2_depth_preserved")
    check(abs(m2["bbox_mm"][2] - 10.0) < 1e-6, "revision2_height_preserved")
    check(m2["volume_mm3"] > m1["volume_mm3"], "revision2_volume_changed")
    doc.saveAs(str(FCSTD_R2))
    pad.Shape.exportStep(str(STEP_R2))
    check(FCSTD_R2.exists() and STEP_R2.exists(), "revision2_artifacts")

    vertices, facets = pad.Shape.tessellate(0.25)
    check(bool(vertices) and bool(facets), "revision2_display_tessellation")
    display = {
        "schema": "OLEANDER_CAD_FEATURE_TREE_DISPLAY_DERIVATIVE_v0.1",
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_PARTDESIGN_FEATURE_TREE",
        "display_authority": "DISPLAY_DERIVATIVE_ONLY",
        "units": "mm",
        "source_fcstd": str(FCSTD_R2),
        "source_fcstd_sha256": file_sha256(FCSTD_R2),
        "source_step": str(STEP_R2),
        "source_step_sha256": file_sha256(STEP_R2),
        "ole_lineage": ["OLE_DATUM::BRACKET_SKETCH_PLANE", "OLE_SKETCH::BRACKET_PROFILE", "OLE_FEATURE::PAD_001"],
        "vertices_mm": [[v.x, v.y, v.z] for v in vertices],
        "triangles": [list(face) for face in facets],
        "bbox_mm": m2["bbox_mm"],
        "volume_mm3": m2["volume_mm3"],
    }
    DISPLAY_R2.write_text(json.dumps(display, sort_keys=True), encoding="utf-8")
    check(DISPLAY_R2.exists() and DISPLAY_R2.stat().st_size > 0, "revision2_display_payload")

    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(FCSTD_R2))
    r_datum = reopened.getObject("OLE_DATUM_PLANE")
    r_sketch = reopened.getObject("OLE_SKETCH_PROFILE")
    r_pad = reopened.getObject("OLE_PAD")
    check(r_datum is not None and r_datum.TypeId == "PartDesign::Plane", "datum_reopen")
    check(r_sketch is not None and r_sketch.TypeId == "Sketcher::SketchObject", "sketch_reopen")
    check(r_pad is not None and r_pad.TypeId == "PartDesign::Pad", "pad_reopen")
    check(r_datum.OLE_ID == "OLE_DATUM::BRACKET_SKETCH_PLANE", "datum_id_reopen")
    check(r_sketch.OLE_ID == "OLE_SKETCH::BRACKET_PROFILE", "sketch_id_reopen")
    check(r_pad.OLE_ID == "OLE_FEATURE::PAD_001", "pad_id_reopen")
    check(linked_object(r_pad.Profile) == r_sketch, "pad_profile_dependency_reopen")
    check(linked_object(r_sketch.AttachmentSupport[0]) == r_datum, "sketch_datum_dependency_reopen")
    check(bool(r_sketch.FullyConstrained), "fully_constrained_reopen")
    check(abs(r_pad.Shape.BoundBox.XLength - 100.0) < 1e-6, "rebuilt_width_reopen")

    result = {
        "schema": "OLEANDER_FREECAD_NATIVE_FEATURE_TREE_PROBE_v0.1",
        "status": "PASS",
        "dependency_state": "RUNTIME_PROBED",
        "freecad_version": ".".join(str(x) for x in App.Version()[:3]),
        "feature_tree": [
            {"ole_id": r_datum.OLE_ID, "type": r_datum.TypeId},
            {"ole_id": r_sketch.OLE_ID, "type": r_sketch.TypeId, "fully_constrained": bool(r_sketch.FullyConstrained)},
            {"ole_id": r_pad.OLE_ID, "type": r_pad.TypeId, "profile_ole_id": r_sketch.OLE_ID},
        ],
        "driving_constraints": {"width_constraint_id": width_id, "depth_constraint_id": depth_id},
        "revision1": m1,
        "revision2": m2,
        "artifacts": {
            "fcstd_r1": str(FCSTD_R1), "step_r1": str(STEP_R1),
            "fcstd_r2": str(FCSTD_R2), "step_r2": str(STEP_R2),
            "display_r2": str(DISPLAY_R2)
        },
        "checks": checks,
        "non_claims": [
            "P0_A_PARAMETRIC_CAD_PASS",
            "general_feature_tree",
            "revolve_sweep_loft",
            "fillet_chamfer_shell_draft",
            "topological_naming_stability",
            "assembly_mates"
        ]
    }
    MANIFEST.write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
    print("OLEANDER_FREECAD_NATIVE_FEATURE_TREE=" + json.dumps(result, sort_keys=True))


main()
