"""OLEANDER bounded authoritative B-Rep split probe using FreeCAD BOPTools.SplitAPI.

Validates a real partition operation, not a boolean-cut substitute. A finite
planar tool face intersects a rectangular prismatic solid at a governed datum
X coordinate. Split pieces are preserved as separate authoritative solids.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import FreeCAD as App
import Part
from BOPTools import SplitAPI

OUT = Path(os.environ.get("OLEANDER_SPLIT_DIR", "/tmp/oleander-bounded-split"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_bounded_split.FCStd"
STEP_A = OUT / "oleander_split_piece_A_R002.step"
STEP_B = OUT / "oleander_split_piece_B_R002.step"
DISPLAY = OUT / "oleander_bounded_split_display.json"
MANIFEST = OUT / "oleander_bounded_split_manifest.json"
TOL = 1e-6
SPLIT_X_MM = 40.0
checks: list[str] = []


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def make_split_plane(x_mm: float):
    pts = [
        App.Vector(x_mm, -10.0, -10.0),
        App.Vector(x_mm, 60.0, -10.0),
        App.Vector(x_mm, 60.0, 20.0),
        App.Vector(x_mm, -10.0, 20.0),
    ]
    return Part.Face(Part.makePolygon(pts + [pts[0]]))


def split_preflight(base, x_mm: float) -> None:
    if not (base.BoundBox.XMin + TOL < x_mm < base.BoundBox.XMax - TOL):
        raise ValueError("split datum does not intersect the interior of the authoritative solid")


def metrics(shape):
    return {
        "bbox_mm": [shape.BoundBox.XLength, shape.BoundBox.YLength, shape.BoundBox.ZLength],
        "origin_mm": [shape.BoundBox.XMin, shape.BoundBox.YMin, shape.BoundBox.ZMin],
        "volume_mm3": shape.Volume,
        "solid_count": len(shape.Solids),
        "face_count": len(shape.Faces),
        "edge_count": len(shape.Edges),
    }


def build_revision(width_mm: float, revision: int):
    base = Part.makeBox(width_mm, 50.0, 10.0)
    check(base.isValid() and len(base.Solids) == 1, f"r{revision}_base_valid_single_solid")
    split_preflight(base, SPLIT_X_MM)
    tool = make_split_plane(SPLIT_X_MM)
    check(tool.isValid() and len(tool.Faces) == 1, f"r{revision}_tool_planar_face")

    result = SplitAPI.slice(base, [tool], "Split", 0.0)
    check(result.isValid(), f"r{revision}_split_result_valid")
    solids = list(result.Solids)
    check(len(solids) == 2, f"r{revision}_exactly_two_solids")
    solids.sort(key=lambda s: s.BoundBox.XMin)
    a, b = solids
    check(a.isValid() and b.isValid(), f"r{revision}_piece_validity")
    check(len(a.Solids) == 1 and len(b.Solids) == 1, f"r{revision}_piece_single_solids")
    check(close(a.BoundBox.XMin, 0.0) and close(a.BoundBox.XMax, SPLIT_X_MM), f"r{revision}_piece_a_bounds")
    check(close(b.BoundBox.XMin, SPLIT_X_MM) and close(b.BoundBox.XMax, width_mm), f"r{revision}_piece_b_bounds")
    check(close(a.BoundBox.YLength, 50.0) and close(b.BoundBox.YLength, 50.0), f"r{revision}_depth_preserved")
    check(close(a.BoundBox.ZLength, 10.0) and close(b.BoundBox.ZLength, 10.0), f"r{revision}_height_preserved")
    check(close(a.Volume + b.Volume, base.Volume, 1e-4), f"r{revision}_volume_conservation")
    check(close(a.Volume, SPLIT_X_MM * 50.0 * 10.0, 1e-4), f"r{revision}_piece_a_volume")
    check(close(b.Volume, (width_mm - SPLIT_X_MM) * 50.0 * 10.0, 1e-4), f"r{revision}_piece_b_volume")
    return base, a, b


def add_piece(doc, name, ole_id, shape, role):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = shape
    for prop, value in [
        ("OLE_ID", ole_id),
        ("OLE_Operation", "BOPTOOLS_SPLIT_API"),
        ("OLE_SplitDatum", "DATUM::X=40mm"),
        ("OLE_PieceRole", role),
        ("OLE_GeometryAuthority", "FREECAD_OCCT_BREP"),
    ]:
        obj.addProperty("App::PropertyString", prop, "OLEANDER")
        setattr(obj, prop, value)
    obj.addProperty("App::PropertyFloat", "OLE_SplitXMM", "OLEANDER")
    obj.OLE_SplitXMM = SPLIT_X_MM
    obj.addProperty("App::PropertyString", "OLE_SplitUnits", "OLEANDER")
    obj.OLE_SplitUnits = "mm"
    return obj


def tessellate(shape):
    verts, tris = shape.tessellate(0.25)
    check(bool(verts) and bool(tris), "display_piece_tessellation")
    return {
        "vertices_mm": [[v.x, v.y, v.z] for v in verts],
        "triangles": [list(t) for t in tris],
        "bbox_mm": metrics(shape)["bbox_mm"],
        "origin_mm": metrics(shape)["origin_mm"],
        "volume_mm3": shape.Volume,
    }


def main() -> None:
    base1, a1, b1 = build_revision(100.0, 1)
    base2, a2, b2 = build_revision(120.0, 2)
    check(close(a1.BoundBox.XLength, 40.0) and close(a2.BoundBox.XLength, 40.0), "datum_anchored_piece_a_stable")
    check(close(b1.BoundBox.XLength, 60.0) and close(b2.BoundBox.XLength, 80.0), "downstream_piece_b_rebuilds_with_width")

    expected_failure = "FAIL"
    try:
        split_preflight(base2, 200.0)
    except ValueError as exc:
        if "does not intersect" in str(exc):
            expected_failure = "PASS"
            checks.append("nonintersecting_split_datum_expected_failure")
    check(expected_failure == "PASS", "nonintersecting_split_failure_gate")

    doc = App.newDocument("OLEANDER_BOUNDED_SPLIT")
    oa = add_piece(doc, "OLE_SPLIT_A_R002", "OLE_SPLIT::PIECE_A_R002", a2, "NEGATIVE_X_SIDE")
    ob = add_piece(doc, "OLE_SPLIT_B_R002", "OLE_SPLIT::PIECE_B_R002", b2, "POSITIVE_X_SIDE")
    doc.recompute()
    doc.saveAs(str(FCSTD))
    oa.Shape.exportStep(str(STEP_A))
    ob.Shape.exportStep(str(STEP_B))
    check(FCSTD.exists() and STEP_A.exists() and STEP_B.exists(), "native_split_artifacts_written")

    display = {
        "schema": "OLEANDER_BOUNDED_SPLIT_DISPLAY_v0.1",
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_OCCT_BREP",
        "display_authority": "DISPLAY_DERIVATIVE_ONLY",
        "units": "mm",
        "operation": "BOPTOOLS_SPLIT_API",
        "split_datum": {"axis": "X", "value_mm": SPLIT_X_MM},
        "source_fcstd": str(FCSTD),
        "source_fcstd_sha256": sha256(FCSTD),
        "pieces": [
            {"ole_id": "OLE_SPLIT::PIECE_A_R002", "source_step": str(STEP_A), "source_step_sha256": sha256(STEP_A), **tessellate(a2)},
            {"ole_id": "OLE_SPLIT::PIECE_B_R002", "source_step": str(STEP_B), "source_step_sha256": sha256(STEP_B), **tessellate(b2)},
        ],
    }
    DISPLAY.write_text(json.dumps(display, sort_keys=True), encoding="utf-8")
    check(DISPLAY.exists() and DISPLAY.stat().st_size > 0, "split_display_written")

    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(FCSTD))
    for name, ole_id, width in [
        ("OLE_SPLIT_A_R002", "OLE_SPLIT::PIECE_A_R002", 40.0),
        ("OLE_SPLIT_B_R002", "OLE_SPLIT::PIECE_B_R002", 80.0),
    ]:
        obj = reopened.getObject(name)
        check(obj is not None, f"{name}_reopen")
        check(obj.OLE_ID == ole_id, f"{name}_ole_id_reopen")
        check(obj.OLE_Operation == "BOPTOOLS_SPLIT_API", f"{name}_operation_reopen")
        check(obj.OLE_SplitDatum == "DATUM::X=40mm", f"{name}_datum_reopen")
        check(close(float(obj.OLE_SplitXMM), SPLIT_X_MM), f"{name}_split_value_reopen")
        check(obj.OLE_SplitUnits == "mm", f"{name}_units_reopen")
        check(obj.OLE_GeometryAuthority == "FREECAD_OCCT_BREP", f"{name}_authority_reopen")
        check(obj.Shape.isValid() and len(obj.Shape.Solids) == 1, f"{name}_solid_reopen")
        check(close(obj.Shape.BoundBox.XLength, width), f"{name}_width_reopen")

    result = {
        "schema": "OLEANDER_FREECAD_BOUNDED_SPLIT_v0.1",
        "status": "PASS",
        "dependency_state": "RUNTIME_PROBED",
        "freecad_version": ".".join(str(x) for x in App.Version()[:3]),
        "occ_version": getattr(Part, "OCC_VERSION", "unknown"),
        "operation_contract": {
            "api": "BOPTools.SplitAPI.slice",
            "mode": "Split",
            "split_datum": {"axis": "X", "value_mm": SPLIT_X_MM},
            "tool": "finite planar face spanning beyond Y/Z bounds",
            "piece_authority": "separate FreeCAD/OCCT solids",
        },
        "revision1": {"base": metrics(base1), "piece_a": metrics(a1), "piece_b": metrics(b1)},
        "revision2": {"base": metrics(base2), "piece_a": metrics(a2), "piece_b": metrics(b2)},
        "expected_failure_cases": {"nonintersecting_split_datum": expected_failure},
        "artifacts": {
            "fcstd": {"path": str(FCSTD), "sha256": sha256(FCSTD)},
            "piece_a_step": {"path": str(STEP_A), "sha256": sha256(STEP_A)},
            "piece_b_step": {"path": str(STEP_B), "sha256": sha256(STEP_B)},
            "display": {"path": str(DISPLAY), "sha256": sha256(DISPLAY)},
        },
        "checks": checks,
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "general_split_trim",
            "arbitrary_surface_split",
            "trim_surface_editing",
            "persistent_topological_naming",
            "production_partition_robustness",
            "brep_healing_parity",
        ],
    }
    MANIFEST.write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
    print("OLEANDER_FREECAD_BOUNDED_SPLIT=" + json.dumps(result, sort_keys=True))


main()
