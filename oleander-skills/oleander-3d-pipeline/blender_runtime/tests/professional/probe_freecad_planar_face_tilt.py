"""OLEANDER bounded planar top-face tilt through FreeCAD/OCCT BRep ReShape.

The unique +Z planar top face of a rectangular prismatic solid is selected by
geometry, tilted about its own center Y axis, and replaced together with the
four adjacent side faces using TopoShape.replaceShape / BRepTools_ReShape.
The bottom face is not replaced. ReShape may emit an invalid intermediate
solid for this edit; bounded sew/fix then produces a shell from the emitted
faces and makeSolid closes that shell. No source box dimensions are used to
rebuild the edited result.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path

import FreeCAD as App
import Part

OUT = Path(os.environ.get("OLEANDER_FACE_TILT_DIR", "/tmp/oleander-face-tilt"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_planar_face_tilt.FCStd"
STEP_POS = OUT / "oleander_planar_face_tilt_positive_R002.step"
STEP_NEG = OUT / "oleander_planar_face_tilt_negative_R002.step"
DISPLAY = OUT / "oleander_planar_face_tilt_display.json"
MANIFEST = OUT / "oleander_planar_face_tilt_manifest.json"
TOL = 1e-6
checks: list[str] = []


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol


def same_point(a, b, tol: float = TOL) -> bool:
    return (a - b).Length <= tol


def face_normal(face):
    u0, u1, v0, v1 = face.ParameterRange
    n = face.normalAt((u0 + u1) * 0.5, (v0 + v1) * 0.5)
    n.normalize()
    return n


def select_top_bottom(shape):
    zmax = shape.BoundBox.ZMax
    zmin = shape.BoundBox.ZMin
    tops = []
    bottoms = []
    for face in shape.Faces:
        bb = face.BoundBox
        if bb.ZLength > TOL:
            continue
        n = face_normal(face)
        if close(bb.ZMax, zmax) and n.z > 0.999999:
            tops.append(face)
        if close(bb.ZMin, zmin) and n.z < -0.999999:
            bottoms.append(face)
    check(len(tops) == 1, "top_face_selector_unique")
    check(len(bottoms) == 1, "bottom_face_selector_unique")
    return tops[0], bottoms[0]


def oriented_top_points(face):
    pts = [v.Point for v in face.OuterWire.OrderedVertexes]
    check(len(pts) == 4, "top_face_four_vertices")
    area2 = sum(
        p.x * pts[(i + 1) % 4].y - pts[(i + 1) % 4].x * p.y
        for i, p in enumerate(pts)
    )
    if area2 < 0:
        pts.reverse()
    return pts


def make_oriented_face(points, expected_normal):
    face = Part.Face(Part.makePolygon(points + [points[0]]))
    if face_normal(face).dot(expected_normal) < 0:
        face = face.reversed()
    check(face.isValid(), "constructed_planar_face_valid")
    return face


def adjacent_side(shape, p0, p1, top, bottom):
    found = []
    for face in shape.Faces:
        if face.isSame(top) or face.isSame(bottom):
            continue
        vertices = [v.Point for v in face.Vertexes]
        if any(same_point(v, p0) for v in vertices) and any(same_point(v, p1) for v in vertices):
            found.append(face)
    check(len(found) == 1, "adjacent_side_face_unique")
    return found[0]


def rotate_about_y(point, center, angle_rad: float):
    dx = point.x - center.x
    dz = point.z - center.z
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    return App.Vector(
        center.x + c * dx + s * dz,
        point.y,
        center.z - s * dx + c * dz,
    )


def normalize_reshape_output(reshaped):
    candidate = reshaped.copy()
    candidate.sewShape(1e-7)
    candidate.fix(1e-7, 1e-7, 1e-7)
    candidate = candidate.removeSplitter()
    if candidate.isValid() and len(candidate.Solids) == 1:
        checks.append("reshape_normalized_direct_single_solid")
        return candidate.Solids[0]

    check(candidate.isValid(), "reshape_emitted_valid_shell")
    check(candidate.ShapeType == "Shell", "reshape_normalized_to_shell")
    check(len(candidate.Solids) == 0, "reshape_shell_has_no_false_solid")
    shell = Part.makeShell(candidate.Faces)
    shell.sewShape(1e-7)
    shell.fix(1e-7, 1e-7, 1e-7)
    solid = Part.makeSolid(shell).removeSplitter()
    check(solid.isValid(), "shell_rebuild_valid_solid")
    check(len(solid.Solids) == 1, "shell_rebuild_single_solid")
    return solid


def tilt_top_face(shape, angle_deg: float):
    check(shape.isValid() and len(shape.Solids) == 1, "input_single_valid_solid")
    if not math.isfinite(angle_deg) or abs(angle_deg) < 1e-9:
        raise ValueError("face tilt angle must be finite and non-zero")
    if abs(angle_deg) > 20.0:
        raise ValueError("face tilt exceeds bounded angular contract")

    top, bottom = select_top_bottom(shape)
    top_pts = oriented_top_points(top)
    center = top.CenterOfMass
    angle_rad = math.radians(angle_deg)
    new_top_pts = [rotate_about_y(p, center, angle_rad) for p in top_pts]
    min_top_z = min(p.z for p in new_top_pts)
    zmin = shape.BoundBox.ZMin
    if min_top_z <= zmin + 0.25:
        raise ValueError("face tilt would cross or approach the opposite face")

    expected_normal = App.Vector(math.sin(angle_rad), 0.0, math.cos(angle_rad))
    new_top = make_oriented_face(new_top_pts, expected_normal)
    actual_normal = face_normal(new_top)
    actual_angle_deg = math.degrees(math.atan2(actual_normal.x, actual_normal.z))
    check(actual_normal.dot(expected_normal) > 0.999999, "tilted_top_normal_matches_angle")
    check(close(actual_angle_deg, angle_deg, 1e-6), "tilted_top_signed_angle")

    replacements = [(top, new_top)]
    bottom_pts = [App.Vector(p.x, p.y, zmin) for p in top_pts]
    side_meta = []
    for i, p0 in enumerate(top_pts):
        p1 = top_pts[(i + 1) % 4]
        old_side = adjacent_side(shape, p0, p1, top, bottom)
        poly = [
            bottom_pts[i],
            bottom_pts[(i + 1) % 4],
            new_top_pts[(i + 1) % 4],
            new_top_pts[i],
        ]
        new_side = make_oriented_face(poly, face_normal(old_side))
        replacements.append((old_side, new_side))
        side_meta.append({
            "old_center_mm": [old_side.CenterOfMass.x, old_side.CenterOfMass.y, old_side.CenterOfMass.z],
            "new_center_mm": [new_side.CenterOfMass.x, new_side.CenterOfMass.y, new_side.CenterOfMass.z],
        })

    check(len(replacements) == 5, "replace_top_plus_four_adjacent_faces")
    reshaped = shape.replaceShape(replacements)
    check(not reshaped.isNull(), "replace_shape_non_null")
    check(len(reshaped.Faces) == 6, "reshape_face_cardinality")
    edited = normalize_reshape_output(reshaped)
    check(edited.isValid() and len(edited.Solids) == 1, "tilted_shape_valid_single_solid")
    check(close(edited.BoundBox.XMin, shape.BoundBox.XMin), "bottom_preserves_xmin_extent")
    check(close(edited.BoundBox.XMax, shape.BoundBox.XMax), "bottom_preserves_xmax_extent")
    check(close(edited.BoundBox.YLength, shape.BoundBox.YLength), "depth_preserved")
    check(edited.Volume > 0.0, "tilted_positive_volume")

    return edited, {
        "selector_id": "SELECTOR::TOP_PLANAR_FACE",
        "operation": "BRepTools_ReShape_TOP_FACE_TILT_Y",
        "angle_deg": angle_deg,
        "actual_angle_deg": actual_angle_deg,
        "actual_top_normal": [actual_normal.x, actual_normal.y, actual_normal.z],
        "axis": "TOP_FACE_CENTER_Y",
        "axis_origin_mm": [center.x, center.y, center.z],
        "min_top_z_mm": min_top_z,
        "replaced_face_count": 5,
        "side_faces": side_meta,
    }


def metrics(shape):
    return {
        "bbox_mm": [shape.BoundBox.XLength, shape.BoundBox.YLength, shape.BoundBox.ZLength],
        "bbox_min_mm": [shape.BoundBox.XMin, shape.BoundBox.YMin, shape.BoundBox.ZMin],
        "bbox_max_mm": [shape.BoundBox.XMax, shape.BoundBox.YMax, shape.BoundBox.ZMax],
        "volume_mm3": shape.Volume,
        "solid_count": len(shape.Solids),
        "face_count": len(shape.Faces),
        "edge_count": len(shape.Edges),
    }


def add_feature(doc, name, ole_id, shape, angle_deg):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = shape
    obj.addProperty("App::PropertyString", "OLE_ID", "OLEANDER")
    obj.OLE_ID = ole_id
    obj.addProperty("App::PropertyString", "OLE_Operation", "OLEANDER")
    obj.OLE_Operation = "PLANAR_TOP_FACE_TILT_RESHAPE"
    obj.addProperty("App::PropertyFloat", "OLE_AngleDeg", "OLEANDER")
    obj.OLE_AngleDeg = angle_deg
    obj.addProperty("App::PropertyString", "OLE_AngleUnits", "OLEANDER")
    obj.OLE_AngleUnits = "deg"
    obj.addProperty("App::PropertyString", "OLE_Axis", "OLEANDER")
    obj.OLE_Axis = "TOP_FACE_CENTER_Y"
    obj.addProperty("App::PropertyString", "OLE_Selector", "OLEANDER")
    obj.OLE_Selector = "SELECTOR::TOP_PLANAR_FACE"
    obj.addProperty("App::PropertyString", "OLE_GeometryAuthority", "OLEANDER")
    obj.OLE_GeometryAuthority = "FREECAD_OCCT_BREP"
    return obj


def main() -> None:
    base_r1 = Part.makeBox(80.0, 50.0, 10.0)
    pos_r1, pos_meta_r1 = tilt_top_face(base_r1, 5.0)
    neg_r1, neg_meta_r1 = tilt_top_face(base_r1, -5.0)
    check(close(pos_meta_r1["actual_angle_deg"], 5.0, 1e-6), "r1_positive_angle")
    check(close(neg_meta_r1["actual_angle_deg"], -5.0, 1e-6), "r1_negative_angle")
    check(close(pos_r1.Volume, neg_r1.Volume, 1e-4), "r1_signed_tilt_volume_symmetry")

    base_r2 = Part.makeBox(100.0, 50.0, 10.0)
    pos_r2, pos_meta_r2 = tilt_top_face(base_r2, 5.0)
    neg_r2, neg_meta_r2 = tilt_top_face(base_r2, -5.0)
    check(close(pos_meta_r2["actual_angle_deg"], 5.0, 1e-6), "r2_positive_angle")
    check(close(neg_meta_r2["actual_angle_deg"], -5.0, 1e-6), "r2_negative_angle")
    check(close(pos_r2.Volume, neg_r2.Volume, 1e-4), "r2_signed_tilt_volume_symmetry")
    check(pos_meta_r1["selector_id"] == pos_meta_r2["selector_id"], "selector_id_stable_across_rebuild")
    check(pos_meta_r1["replaced_face_count"] == pos_meta_r2["replaced_face_count"] == 5, "replacement_cardinality_stable_across_rebuild")

    failure = "FAIL"
    try:
        tilt_top_face(base_r2, 30.0)
    except ValueError as exc:
        if "bounded angular contract" in str(exc) or "opposite face" in str(exc):
            failure = "PASS"
            checks.append("excessive_tilt_expected_failure")
    check(failure == "PASS", "excessive_tilt_failure_gate")

    doc = App.newDocument("OLEANDER_PLANAR_FACE_TILT")
    pos_obj = add_feature(doc, "OLE_POS_R002", "OLE_DIRECT_FACE_TILT::POS_R002", pos_r2, 5.0)
    neg_obj = add_feature(doc, "OLE_NEG_R002", "OLE_DIRECT_FACE_TILT::NEG_R002", neg_r2, -5.0)
    doc.recompute()
    doc.saveAs(str(FCSTD))
    pos_obj.Shape.exportStep(str(STEP_POS))
    neg_obj.Shape.exportStep(str(STEP_NEG))
    check(FCSTD.exists() and STEP_POS.exists() and STEP_NEG.exists(), "native_tilt_artifacts_written")

    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(FCSTD))
    for name, ole_id, angle in [
        ("OLE_POS_R002", "OLE_DIRECT_FACE_TILT::POS_R002", 5.0),
        ("OLE_NEG_R002", "OLE_DIRECT_FACE_TILT::NEG_R002", -5.0),
    ]:
        obj = reopened.getObject(name)
        check(obj is not None, f"{name}_reopen")
        check(obj.OLE_ID == ole_id, f"{name}_ole_id_reopen")
        check(obj.OLE_Operation == "PLANAR_TOP_FACE_TILT_RESHAPE", f"{name}_operation_reopen")
        check(obj.OLE_Selector == "SELECTOR::TOP_PLANAR_FACE", f"{name}_selector_reopen")
        check(obj.OLE_Axis == "TOP_FACE_CENTER_Y", f"{name}_axis_reopen")
        check(obj.OLE_AngleUnits == "deg", f"{name}_angle_units_reopen")
        check(close(float(obj.OLE_AngleDeg), angle, 1e-6), f"{name}_signed_angle_reopen")
        check(obj.OLE_GeometryAuthority == "FREECAD_OCCT_BREP", f"{name}_authority_reopen")
        check(obj.Shape.isValid() and len(obj.Shape.Solids) == 1, f"{name}_solid_reopen")
    App.closeDocument(reopened.Name)

    verts, facets = pos_r2.tessellate(0.25)
    check(bool(verts) and bool(facets), "display_tessellation")
    display = {
        "schema": "OLEANDER_PLANAR_FACE_TILT_DISPLAY_v0.1",
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_OCCT_BREP",
        "display_authority": "DISPLAY_DERIVATIVE_ONLY",
        "units": "mm",
        "angle_units": "deg",
        "ole_id": "OLE_DIRECT_FACE_TILT::POS_R002",
        "selector_id": "SELECTOR::TOP_PLANAR_FACE",
        "operation": "BRepTools_ReShape_TOP_FACE_TILT_Y",
        "axis": "TOP_FACE_CENTER_Y",
        "angle_deg": 5.0,
        "actual_angle_deg": pos_meta_r2["actual_angle_deg"],
        "source_fcstd": str(FCSTD),
        "source_fcstd_sha256": sha256(FCSTD),
        "source_step": str(STEP_POS),
        "source_step_sha256": sha256(STEP_POS),
        "bbox_mm": metrics(pos_r2)["bbox_mm"],
        "volume_mm3": pos_r2.Volume,
        "vertices_mm": [[v.x, v.y, v.z] for v in verts],
        "triangles": [list(t) for t in facets],
    }
    DISPLAY.write_text(json.dumps(display, sort_keys=True), encoding="utf-8")
    check(DISPLAY.exists() and DISPLAY.stat().st_size > 0, "display_payload_written")

    result = {
        "schema": "OLEANDER_FREECAD_PLANAR_FACE_TILT_v0.1",
        "status": "PASS",
        "dependency_state": "RUNTIME_PROBED",
        "freecad_version": ".".join(str(x) for x in App.Version()[:3]),
        "occ_version": getattr(Part, "OCC_VERSION", "unknown"),
        "operation_contract": {
            "selector": "SELECTOR::TOP_PLANAR_FACE",
            "kernel_route": "TopoShape.replaceShape / BRepTools_ReShape -> sew/fix shell normalization -> makeSolid when required",
            "axis": "selected top-face center Y axis",
            "replaced_subshapes": "selected top planar face plus its four adjacent planar side faces",
            "opposite_face": "preserved",
            "angles_deg": [5.0, -5.0],
            "angle_storage": "OLE_AngleDeg App::PropertyFloat + OLE_AngleUnits=deg",
            "source_dimension_rebuild_used_for_edited_result": false
        },
        "revision1": {
            "base": metrics(base_r1),
            "positive": metrics(pos_r1),
            "negative": metrics(neg_r1),
            "positive_operation": pos_meta_r1,
            "negative_operation": neg_meta_r1,
        },
        "revision2": {
            "base": metrics(base_r2),
            "positive": metrics(pos_r2),
            "negative": metrics(neg_r2),
            "positive_operation": pos_meta_r2,
            "negative_operation": neg_meta_r2,
        },
        "expected_failure_cases": {"excessive_or_inverting_face_tilt": failure},
        "artifacts": {
            "fcstd": {"path": str(FCSTD), "sha256": sha256(FCSTD)},
            "positive_step": {"path": str(STEP_POS), "sha256": sha256(STEP_POS)},
            "negative_step": {"path": str(STEP_NEG), "sha256": sha256(STEP_NEG)},
            "display": {"path": str(DISPLAY), "sha256": sha256(DISPLAY)},
        },
        "checks": checks,
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "general_face_rotate",
            "arbitrary_rotation_axis",
            "nonplanar_face_rotate",
            "multi_loop_face_rotate",
            "persistent_topological_naming",
            "general_push_pull",
            "general_split_trim",
            "production_direct_modeling_parity"
        ]
    }
    MANIFEST.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print("OLEANDER_FREECAD_PLANAR_FACE_TILT=" + json.dumps(result, sort_keys=True), flush=True)


# FreeCADCmd executes a supplied Python file in its console namespace rather
# than guaranteeing CPython's __main__ script guard semantics. Probe files are
# executable test entrypoints, so invoke explicitly.
main()
