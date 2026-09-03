"""OLEANDER bounded planar face-normal Direct B-Rep edit probe.

This probe intentionally does not call a face-derived extrusion/boolean a
"push/pull". It uses FreeCAD/OCCT TopoShape.replaceShape (BRepTools_ReShape)
to replace one selected planar top face and its four adjacent planar faces,
then performs bounded B-Rep sew/fix normalization.

Scope is deliberately narrow: a rectangular prismatic single solid with a
unique +Z top face and four vertical planar side faces. The selected face is
moved along its normal while the opposite face remains fixed.
"""

from __future__ import annotations

import hashlib
import json
import math
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


def check(condition: bool, label: str) -> None:
    if not condition:
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
    try:
        u0, u1, v0, v1 = face.ParameterRange
        n = face.normalAt((u0 + u1) * 0.5, (v0 + v1) * 0.5)
    except Exception:
        n = face.normalAt(0, 0)
    if face.Orientation == "Reversed":
        n = n.negative()
    return n.normalize()


def select_top_face(shape):
    zmax = shape.BoundBox.ZMax
    found = []
    for face in shape.Faces:
        bb = face.BoundBox
        if bb.ZLength > TOL or not close(bb.ZMax, zmax):
            continue
        n = face_normal(face)
        if n.z < 0.999999:
            continue
        found.append(face)
    check(len(found) == 1, "top_face_selector_unique")
    return found[0]


def select_bottom_face(shape):
    zmin = shape.BoundBox.ZMin
    found = []
    for face in shape.Faces:
        bb = face.BoundBox
        if bb.ZLength > TOL or not close(bb.ZMin, zmin):
            continue
        n = face_normal(face)
        if n.z > -0.999999:
            continue
        found.append(face)
    check(len(found) == 1, "bottom_face_selector_unique")
    return found[0]


def oriented_top_points(face):
    pts = [v.Point for v in face.OuterWire.OrderedVertexes]
    check(len(pts) == 4, "top_face_four_vertices")
    # Ensure CCW as viewed from +Z so side-face construction has outward normals.
    area2 = 0.0
    for i, p in enumerate(pts):
        q = pts[(i + 1) % len(pts)]
        area2 += p.x * q.y - q.x * p.y
    if area2 < 0:
        pts.reverse()
    return pts


def make_planar_face(points, expected_normal):
    wire = Part.makePolygon(points + [points[0]])
    face = Part.Face(wire)
    n = face_normal(face)
    if n.dot(expected_normal) < 0:
        face = face.reversed()
    return face


def side_face_for_top_edge(shape, p0, p1, top_face, bottom_face):
    found = []
    for face in shape.Faces:
        if face.isSame(top_face) or face.isSame(bottom_face):
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

    # Bounded normalization: rebuild a shell only from the faces emitted by the
    # ReShape result. No original parametric dimensions are re-used here.
    shell = Part.makeShell(candidate.Faces)
    try:
        shell.sewShape(1e-7)
    except TypeError:
        shell.sewShape()
    try:
        shell.fix(1e-7, 1e-7, 1e-7)
    except TypeError:
        shell.fix()
    solid = Part.makeSolid(shell)
    return solid.removeSplitter()


def move_top_face(shape, delta_mm: float):
    check(len(shape.Solids) == 1 and shape.isValid(), "input_single_valid_solid")
    height = shape.BoundBox.ZLength
    if delta_mm <= -height + TOL:
        raise ValueError("face move would collapse or invert the solid")

    top = select_top_face(shape)
    bottom = select_bottom_face(shape)
    normal = face_normal(top)
    check(normal.z > 0.999999, "top_face_positive_z_normal")
    top_pts = oriented_top_points(top)
    zmin = shape.BoundBox.ZMin
    bottom_pts = [App.Vector(p.x, p.y, zmin) for p in top_pts]
    new_top_pts = [p + normal * delta_mm for p in top_pts]

    new_top = make_planar_face(new_top_pts, normal)
    replacements = [(top, new_top)]
    side_descriptors = []
    for i, p0 in enumerate(top_pts):
        p1 = top_pts[(i + 1) % len(top_pts)]
        q0 = new_top_pts[i]
        q1 = new_top_pts[(i + 1) % len(top_pts)]
        b0 = bottom_pts[i]
        b1 = bottom_pts[(i + 1) % len(top_pts)]
        old_side = side_face_for_top_edge(shape, p0, p1, top, bottom)
        # CCW top footprint -> b0,b1,q1,q0 produces outward vertical normal.
        new_side = make_planar_face([b0, b1, q1, q0], face_normal(old_side))
        replacements.append((old_side, new_side))
        side_descriptors.append({
            "old_center_mm": [old_side.CenterOfMass.x, old_side.CenterOfMass.y, old_side.CenterOfMass.z],
            "new_center_mm": [new_side.CenterOfMass.x, new_side.CenterOfMass.y, new_side.CenterOfMass.z],
        })

    check(len(replacements) == 5, "replace_top_plus_four_adjacent_faces")
    reshaped = shape.replaceShape(replacements)
    check(not reshaped.isNull(), "replace_shape_non_null")
    edited = normalize_replaced(reshaped)
    check(edited.isValid(), "edited_shape_valid")
    check(len(edited.Solids) == 1, "edited_shape_single_solid")
    check(close(edited.BoundBox.XLength, shape.BoundBox.XLength), "edited_width_preserved")
    check(close(edited.BoundBox.YLength, shape.BoundBox.YLength), "edited_depth_preserved")
    expected_height = height + delta_mm
    check(close(edited.BoundBox.ZLength, expected_height), "edited_height_matches_face_move")
    expected_volume = shape.BoundBox.XLength * shape.BoundBox.YLength * expected_height
    check(close(edited.Volume, expected_volume, 1e-4), "edited_volume_matches_prism")
    return edited, {
        "selector_id": "SELECTOR::TOP_PLANAR_FACE",
        "operation": "BRepTools_ReShape_FACE_AND_ADJACENT_FACE_REPLACEMENT",
        "delta_mm": delta_mm,
        "replaced_face_count": len(replacements),
        "top_center_before_mm": [top.CenterOfMass.x, top.CenterOfMass.y, top.CenterOfMass.z],
        "top_center_after_mm": [new_top.CenterOfMass.x, new_top.CenterOfMass.y, new_top.CenterOfMass.z],
        "side_faces": side_descriptors,
    }


def shape_metrics(shape):
    return {
        "bbox_mm": [shape.BoundBox.XLength, shape.BoundBox.YLength, shape.BoundBox.ZLength],
        "volume_mm3": shape.Volume,
        "solid_count": len(shape.Solids),
        "face_count": len(shape.Faces),
        "edge_count": len(shape.Edges),
    }


def add_feature(doc, name, ole_id, shape, delta, selector):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = shape
    obj.addProperty("App::PropertyString", "OLE_ID", "OLEANDER")
    obj.OLE_ID = ole_id
    obj.addProperty("App::PropertyString", "OLE_Operation", "OLEANDER")
    obj.OLE_Operation = "PLANAR_FACE_NORMAL_MOVE_RESHAPE"
    obj.addProperty("App::PropertyLength", "OLE_Delta", "OLEANDER")
    obj.OLE_Delta = delta
    obj.addProperty("App::PropertyString", "OLE_Selector", "OLEANDER")
    obj.OLE_Selector = selector
    obj.addProperty("App::PropertyString", "OLE_GeometryAuthority", "OLEANDER")
    obj.OLE_GeometryAuthority = "FREECAD_OCCT_BREP"
    return obj


def tessellated_payload(shape, source_fcstd, source_step, operation_meta):
    verts, facets = shape.tessellate(0.25)
    check(bool(verts) and bool(facets), "display_tessellation")
    return {
        "schema": "OLEANDER_PLANAR_FACE_MOVE_DISPLAY_DERIVATIVE_v0.1",
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_OCCT_BREP",
        "display_authority": "DISPLAY_DERIVATIVE_ONLY",
        "units": "mm",
        "ole_id": "OLE_DIRECT_FACE_MOVE::PUSH_R002",
        "selector_id": operation_meta["selector_id"],
        "operation": operation_meta["operation"],
        "delta_mm": operation_meta["delta_mm"],
        "source_fcstd": str(source_fcstd),
        "source_fcstd_sha256": sha256(source_fcstd),
        "source_step": str(source_step),
        "source_step_sha256": sha256(source_step),
        "bbox_mm": shape_metrics(shape)["bbox_mm"],
        "volume_mm3": shape.Volume,
        "vertices_mm": [[v.x, v.y, v.z] for v in verts],
        "triangles": [list(t) for t in facets],
    }


def main() -> None:
    # Revision 1 proves the selector and replacement route on the 80 mm base.
    base_r1 = Part.makeBox(80.0, 50.0, 10.0)
    push_r1, meta_push_r1 = move_top_face(base_r1, 5.0)
    check(close(push_r1.BoundBox.ZLength, 15.0), "r1_push_height_15")

    # Revision 2 changes the authoritative width and re-resolves every face.
    base_r2 = Part.makeBox(100.0, 50.0, 10.0)
    push_r2, meta_push_r2 = move_top_face(base_r2, 5.0)
    pull_r2, meta_pull_r2 = move_top_face(base_r2, -3.0)
    check(close(push_r2.BoundBox.ZLength, 15.0), "r2_push_height_15")
    check(close(pull_r2.BoundBox.ZLength, 7.0), "r2_pull_height_7")
    check(push_r2.Volume > base_r2.Volume, "push_increases_volume")
    check(pull_r2.Volume < base_r2.Volume, "pull_decreases_volume")
    check(meta_push_r1["replaced_face_count"] == meta_push_r2["replaced_face_count"] == 5, "replacement_cardinality_stable_across_rebuild")
    check(meta_push_r1["selector_id"] == meta_push_r2["selector_id"], "selector_id_stable_across_rebuild")

    failure = "FAIL"
    try:
        move_top_face(base_r2, -10.0)
    except ValueError as exc:
        if "collapse or invert" in str(exc):
            failure = "PASS"
            checks.append("collapse_invert_expected_failure")
    check(failure == "PASS", "collapse_invert_failure_gate")

    doc = App.newDocument("OLEANDER_PLANAR_FACE_MOVE")
    push_obj = add_feature(doc, "OLE_PUSH_R002", "OLE_DIRECT_FACE_MOVE::PUSH_R002", push_r2, 5.0, meta_push_r2["selector_id"])
    pull_obj = add_feature(doc, "OLE_PULL_R002", "OLE_DIRECT_FACE_MOVE::PULL_R002", pull_r2, -3.0, meta_pull_r2["selector_id"])
    doc.recompute()
    doc.saveAs(str(FCSTD))
    push_obj.Shape.exportStep(str(STEP_PUSH))
    pull_obj.Shape.exportStep(str(STEP_PULL))
    check(FCSTD.exists() and STEP_PUSH.exists() and STEP_PULL.exists(), "native_artifacts_written")

    display = tessellated_payload(push_r2, FCSTD, STEP_PUSH, meta_push_r2)
    DISPLAY.write_text(json.dumps(display, sort_keys=True), encoding="utf-8")
    check(DISPLAY.exists() and DISPLAY.stat().st_size > 0, "display_payload_written")

    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(FCSTD))
    rp = reopened.getObject("OLE_PUSH_R002")
    rl = reopened.getObject("OLE_PULL_R002")
    for obj, ole_id, delta, height in [
        (rp, "OLE_DIRECT_FACE_MOVE::PUSH_R002", 5.0, 15.0),
        (rl, "OLE_DIRECT_FACE_MOVE::PULL_R002", -3.0, 7.0),
    ]:
        check(obj is not None, f"{ole_id}_reopen")
        check(obj.OLE_ID == ole_id, f"{ole_id}_ole_id_reopen")
        check(obj.OLE_Operation == "PLANAR_FACE_NORMAL_MOVE_RESHAPE", f"{ole_id}_operation_reopen")
        check(obj.OLE_Selector == "SELECTOR::TOP_PLANAR_FACE", f"{ole_id}_selector_reopen")
        check(obj.OLE_GeometryAuthority == "FREECAD_OCCT_BREP", f"{ole_id}_authority_reopen")
        check(close(obj.OLE_Delta.Value, delta), f"{ole_id}_delta_reopen")
        check(obj.Shape.isValid() and len(obj.Shape.Solids) == 1, f"{ole_id}_solid_reopen")
        check(close(obj.Shape.BoundBox.ZLength, height), f"{ole_id}_height_reopen")

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
        "revision1": {"base": shape_metrics(base_r1), "push": shape_metrics(push_r1), "operation": meta_push_r1},
        "revision2": {
            "base": shape_metrics(base_r2),
            "push": shape_metrics(push_r2),
            "pull": shape_metrics(pull_r2),
            "push_operation": meta_push_r2,
            "pull_operation": meta_pull_r2,
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
            "P0_B_DIRECT_BREP_PASS",
            "general_push_pull",
            "arbitrary_face_move",
            "nonplanar_face_move",
            "multi_loop_face_move",
            "persistent_topological_naming",
            "face_rotate",
            "split_trim",
            "brep_healing_parity",
            "production_direct_modeling_parity",
        ],
    }
    MANIFEST.write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
    print("OLEANDER_FREECAD_PLANAR_FACE_NORMAL_MOVE=" + json.dumps(result, sort_keys=True))


main()
