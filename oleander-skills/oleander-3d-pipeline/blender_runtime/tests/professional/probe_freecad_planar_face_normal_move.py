"""Bounded planar face-normal B-Rep edit using TopoShape.replaceShape.

Scope: rectangular prismatic single solid only. A stable +Z top-face selector is
re-resolved from geometry. The selected face and its four adjacent side faces
are replaced through FreeCAD/OCCT BRepTools_ReShape, then sewn/fixed. This is
not a claim of arbitrary/general push-pull.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import FreeCAD as App
import Part

OUT = Path(os.environ.get("OLEANDER_FACE_MOVE_DIR", "/tmp/oleander-face-move"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_planar_face_move.FCStd"
STEP_PUSH = OUT / "oleander_planar_face_move_push_R002.step"
STEP_PULL = OUT / "oleander_planar_face_move_pull_R002.step"
DISPLAY = OUT / "oleander_planar_face_move_display.json"
MANIFEST = OUT / "oleander_planar_face_move_manifest.json"
TOL = 1e-6
checks: list[str] = []


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol


def same_point(a, b, tol: float = TOL) -> bool:
    return (a - b).Length <= tol


def face_normal(face):
    """FreeCAD face.normalAt() already follows face orientation."""
    try:
        u0, u1, v0, v1 = face.ParameterRange
        n = face.normalAt((u0 + u1) * 0.5, (v0 + v1) * 0.5)
    except Exception:
        n = face.normalAt(0, 0)
    return n.normalize()


def select_horizontal_face(shape, top: bool):
    target = shape.BoundBox.ZMax if top else shape.BoundBox.ZMin
    sign = 1.0 if top else -1.0
    found = []
    for face in shape.Faces:
        bb = face.BoundBox
        boundary = bb.ZMax if top else bb.ZMin
        if bb.ZLength > TOL or not close(boundary, target):
            continue
        n = face_normal(face)
        if n.z * sign > 0.999999:
            found.append(face)
    check(len(found) == 1, "top_face_selector_unique" if top else "bottom_face_selector_unique")
    return found[0]


def oriented_top_points(face):
    pts = [v.Point for v in face.OuterWire.OrderedVertexes]
    check(len(pts) == 4, "top_face_four_vertices")
    area2 = sum(
        pts[i].x * pts[(i + 1) % 4].y - pts[(i + 1) % 4].x * pts[i].y
        for i in range(4)
    )
    if area2 < 0:
        pts.reverse()
    return pts


def make_face(points, expected_normal):
    face = Part.Face(Part.makePolygon(points + [points[0]]))
    if face_normal(face).dot(expected_normal) < 0:
        face = face.reversed()
    return face


def adjacent_side(shape, p0, p1, top, bottom):
    found = []
    for face in shape.Faces:
        if face.isSame(top) or face.isSame(bottom):
            continue
        pts = [v.Point for v in face.Vertexes]
        if any(same_point(v, p0) for v in pts) and any(same_point(v, p1) for v in pts):
            found.append(face)
    check(len(found) == 1, "adjacent_side_face_unique")
    return found[0]


def normalize_replaced(shape):
    candidate = shape.copy()
    try:
        candidate.sewShape(1e-7)
    except TypeError:
        candidate.sewShape()
    try:
        candidate.fix(1e-7, 1e-7, 1e-7)
    except TypeError:
        candidate.fix()
    candidate = candidate.removeSplitter()
    if candidate.isValid() and len(candidate.Solids) == 1:
        return candidate
    shell = Part.makeShell(candidate.Faces)
    try:
        shell.sewShape(1e-7)
    except TypeError:
        shell.sewShape()
    try:
        shell.fix(1e-7, 1e-7, 1e-7)
    except TypeError:
        shell.fix()
    return Part.makeSolid(shell).removeSplitter()


def move_top_face(shape, delta_mm: float):
    check(shape.isValid() and len(shape.Solids) == 1, "input_single_valid_solid")
    height = shape.BoundBox.ZLength
    if delta_mm <= -height + TOL:
        raise ValueError("face move would collapse or invert the solid")

    top = select_horizontal_face(shape, True)
    bottom = select_horizontal_face(shape, False)
    normal = face_normal(top)
    check(normal.z > 0.999999, "top_face_positive_z_normal")
    top_pts = oriented_top_points(top)
    bottom_pts = [App.Vector(p.x, p.y, shape.BoundBox.ZMin) for p in top_pts]
    new_top_pts = [p + normal * delta_mm for p in top_pts]
    new_top = make_face(new_top_pts, normal)

    replacements = [(top, new_top)]
    side_meta = []
    for i in range(4):
        p0, p1 = top_pts[i], top_pts[(i + 1) % 4]
        q0, q1 = new_top_pts[i], new_top_pts[(i + 1) % 4]
        b0, b1 = bottom_pts[i], bottom_pts[(i + 1) % 4]
        old = adjacent_side(shape, p0, p1, top, bottom)
        new = make_face([b0, b1, q1, q0], face_normal(old))
        replacements.append((old, new))
        side_meta.append({
            "old_center_mm": [old.CenterOfMass.x, old.CenterOfMass.y, old.CenterOfMass.z],
            "new_center_mm": [new.CenterOfMass.x, new.CenterOfMass.y, new.CenterOfMass.z],
        })

    check(len(replacements) == 5, "replace_top_plus_four_adjacent_faces")
    reshaped = shape.replaceShape(replacements)
    check(not reshaped.isNull(), "replace_shape_non_null")
    edited = normalize_replaced(reshaped)
    check(edited.isValid(), "edited_shape_valid")
    check(len(edited.Solids) == 1, "edited_shape_single_solid")
    check(close(edited.BoundBox.XLength, shape.BoundBox.XLength), "edited_width_preserved")
    check(close(edited.BoundBox.YLength, shape.BoundBox.YLength), "edited_depth_preserved")
    expected_h = height + delta_mm
    check(close(edited.BoundBox.ZLength, expected_h), "edited_height_matches_face_move")
    expected_v = shape.BoundBox.XLength * shape.BoundBox.YLength * expected_h
    check(close(edited.Volume, expected_v, 1e-4), "edited_volume_matches_prism")
    return edited, {
        "selector_id": "SELECTOR::TOP_PLANAR_FACE",
        "operation": "BRepTools_ReShape_FACE_AND_ADJACENT_FACE_REPLACEMENT",
        "delta_mm": delta_mm,
        "replaced_face_count": 5,
        "top_center_before_mm": [top.CenterOfMass.x, top.CenterOfMass.y, top.CenterOfMass.z],
        "top_center_after_mm": [new_top.CenterOfMass.x, new_top.CenterOfMass.y, new_top.CenterOfMass.z],
        "side_faces": side_meta,
    }


def metrics(shape):
    return {
        "bbox_mm": [shape.BoundBox.XLength, shape.BoundBox.YLength, shape.BoundBox.ZLength],
        "volume_mm3": shape.Volume,
        "solid_count": len(shape.Solids),
        "face_count": len(shape.Faces),
        "edge_count": len(shape.Edges),
    }


def add_feature(doc, name, ole_id, shape, delta):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = shape
    for prop, value in [
        ("OLE_ID", ole_id),
        ("OLE_Operation", "PLANAR_FACE_NORMAL_MOVE_RESHAPE"),
        ("OLE_Selector", "SELECTOR::TOP_PLANAR_FACE"),
        ("OLE_GeometryAuthority", "FREECAD_OCCT_BREP"),
    ]:
        obj.addProperty("App::PropertyString", prop, "OLEANDER")
        setattr(obj, prop, value)
    obj.addProperty("App::PropertyLength", "OLE_Delta", "OLEANDER")
    obj.OLE_Delta = delta
    return obj


def display_payload(shape, meta):
    verts, tris = shape.tessellate(0.25)
    check(bool(verts) and bool(tris), "display_tessellation")
    return {
        "schema": "OLEANDER_PLANAR_FACE_MOVE_DISPLAY_DERIVATIVE_v0.1",
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_OCCT_BREP",
        "display_authority": "DISPLAY_DERIVATIVE_ONLY",
        "units": "mm",
        "ole_id": "OLE_DIRECT_FACE_MOVE::PUSH_R002",
        "selector_id": meta["selector_id"],
        "operation": meta["operation"],
        "delta_mm": meta["delta_mm"],
        "source_fcstd": str(FCSTD),
        "source_fcstd_sha256": sha256(FCSTD),
        "source_step": str(STEP_PUSH),
        "source_step_sha256": sha256(STEP_PUSH),
        "bbox_mm": metrics(shape)["bbox_mm"],
        "volume_mm3": shape.Volume,
        "vertices_mm": [[v.x, v.y, v.z] for v in verts],
        "triangles": [list(t) for t in tris],
    }


def main() -> None:
    base1 = Part.makeBox(80.0, 50.0, 10.0)
    push1, m_push1 = move_top_face(base1, 5.0)
    check(close(push1.BoundBox.ZLength, 15.0), "r1_push_height_15")

    base2 = Part.makeBox(100.0, 50.0, 10.0)
    push2, m_push2 = move_top_face(base2, 5.0)
    pull2, m_pull2 = move_top_face(base2, -3.0)
    check(close(push2.BoundBox.ZLength, 15.0), "r2_push_height_15")
    check(close(pull2.BoundBox.ZLength, 7.0), "r2_pull_height_7")
    check(push2.Volume > base2.Volume, "push_increases_volume")
    check(pull2.Volume < base2.Volume, "pull_decreases_volume")
    check(m_push1["replaced_face_count"] == m_push2["replaced_face_count"] == 5, "replacement_cardinality_stable_across_rebuild")
    check(m_push1["selector_id"] == m_push2["selector_id"], "selector_id_stable_across_rebuild")

    failure = "FAIL"
    try:
        move_top_face(base2, -10.0)
    except ValueError as exc:
        if "collapse or invert" in str(exc):
            failure = "PASS"
            checks.append("collapse_invert_expected_failure")
    check(failure == "PASS", "collapse_invert_failure_gate")

    doc = App.newDocument("OLEANDER_PLANAR_FACE_MOVE")
    p = add_feature(doc, "OLE_PUSH_R002", "OLE_DIRECT_FACE_MOVE::PUSH_R002", push2, 5.0)
    q = add_feature(doc, "OLE_PULL_R002", "OLE_DIRECT_FACE_MOVE::PULL_R002", pull2, -3.0)
    doc.recompute()
    doc.saveAs(str(FCSTD))
    p.Shape.exportStep(str(STEP_PUSH))
    q.Shape.exportStep(str(STEP_PULL))
    check(FCSTD.exists() and STEP_PUSH.exists() and STEP_PULL.exists(), "native_artifacts_written")

    DISPLAY.write_text(json.dumps(display_payload(push2, m_push2), sort_keys=True), encoding="utf-8")
    check(DISPLAY.exists() and DISPLAY.stat().st_size > 0, "display_payload_written")

    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(FCSTD))
    for name, ole_id, delta, height in [
        ("OLE_PUSH_R002", "OLE_DIRECT_FACE_MOVE::PUSH_R002", 5.0, 15.0),
        ("OLE_PULL_R002", "OLE_DIRECT_FACE_MOVE::PULL_R002", -3.0, 7.0),
    ]:
        obj = reopened.getObject(name)
        check(obj is not None, f"{name}_reopen")
        check(obj.OLE_ID == ole_id, f"{name}_ole_id_reopen")
        check(obj.OLE_Operation == "PLANAR_FACE_NORMAL_MOVE_RESHAPE", f"{name}_operation_reopen")
        check(obj.OLE_Selector == "SELECTOR::TOP_PLANAR_FACE", f"{name}_selector_reopen")
        check(obj.OLE_GeometryAuthority == "FREECAD_OCCT_BREP", f"{name}_authority_reopen")
        check(close(obj.OLE_Delta.Value, delta), f"{name}_delta_reopen")
        check(obj.Shape.isValid() and len(obj.Shape.Solids) == 1, f"{name}_solid_reopen")
        check(close(obj.Shape.BoundBox.ZLength, height), f"{name}_height_reopen")

    result = {
        "schema": "OLEANDER_FREECAD_PLANAR_FACE_NORMAL_MOVE_v0.1",
        "status": "PASS",
        "dependency_state": "RUNTIME_PROBED",
        "freecad_version": ".".join(str(x) for x in App.Version()[:3]),
        "occ_version": getattr(Part, "OCC_VERSION", "unknown"),
        "operation_contract": {
            "selector": "SELECTOR::TOP_PLANAR_FACE",
            "kernel_route": "TopoShape.replaceShape / BRepTools_ReShape + bounded sew/fix normalization",
            "replaced_subshapes": "selected top planar face plus its four adjacent planar side faces",
            "opposite_face": "preserved",
        },
        "revision1": {"base": metrics(base1), "push": metrics(push1), "operation": m_push1},
        "revision2": {
            "base": metrics(base2), "push": metrics(push2), "pull": metrics(pull2),
            "push_operation": m_push2, "pull_operation": m_pull2,
        },
        "expected_failure_cases": {"collapse_or_invert_face_move": failure},
        "artifacts": {
            "fcstd": {"path": str(FCSTD), "sha256": sha256(FCSTD)},
            "push_step": {"path": str(STEP_PUSH), "sha256": sha256(STEP_PUSH)},
            "pull_step": {"path": str(STEP_PULL), "sha256": sha256(STEP_PULL)},
            "display": {"path": str(DISPLAY), "sha256": sha256(DISPLAY)},
        },
        "checks": checks,
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS", "general_push_pull", "arbitrary_face_move",
            "nonplanar_face_move", "multi_loop_face_move", "persistent_topological_naming",
            "face_rotate", "split_trim", "brep_healing_parity", "production_direct_modeling_parity"
        ],
    }
    MANIFEST.write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
    print("OLEANDER_FREECAD_PLANAR_FACE_NORMAL_MOVE=" + json.dumps(result, sort_keys=True))


main()
