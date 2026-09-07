"""OLEANDER bounded full-3D planar-face rotation about an offset arbitrary axis.

The semantic local +X face of a yaw+pitch transformed FreeCAD/OCCT box is
selected geometrically. The rotation axis is user-defined from transformed
local coefficients normalize(2*localX + 4*localY + 3*localZ), so it contains
both face-normal and tangent components. The axis origin is intentionally
offset from the selected-face center by +2*localX + 7*localY - 4*localZ mm.

The target face is rigidly rotated about that 3D line. The four adjacent faces
are rebuilt as OCCT ruled surfaces between fixed opposite edges and the rotated
target edges, then applied through BRepTools_ReShape. This proves one bounded
non-tangent, offset-pivot arbitrary-axis family. It does not prove unrestricted
arbitrary-axis direct editing, arbitrary pivot placement, nonplanar-face direct
editing, persistent topological naming, or P0-B parity.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import traceback
from pathlib import Path

import FreeCAD as App
import Part

OUT = Path(os.environ.get("OLEANDER_ARBITRARY_AXIS_ROTATE_DIR", "/tmp/oleander-arbitrary-axis-rotate"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_arbitrary_axis_face_rotate.FCStd"
STEP_R001 = OUT / "oleander_arbitrary_axis_face_rotate_R001.step"
STEP_R002 = OUT / "oleander_arbitrary_axis_face_rotate_R002.step"
DISPLAY = OUT / "oleander_arbitrary_axis_face_rotate_display.json"
MANIFEST = OUT / "oleander_arbitrary_axis_face_rotate_manifest.json"
TOL = 1e-6
checks: list[str] = []

REVISIONS = {
    "R001": {"dims": (80.0, 50.0, 10.0), "yaw_deg": 30.0, "pitch_deg": 20.0, "angle_deg": 2.0},
    "R002": {"dims": (100.0, 60.0, 12.0), "yaw_deg": -25.0, "pitch_deg": -15.0, "angle_deg": -2.5},
}
AXIS_COEFF = {"local_x": 2.0, "local_y": 4.0, "local_z": 3.0}
PIVOT_OFFSET_LOCAL_MM = {"local_x": 2.0, "local_y": 7.0, "local_z": -4.0}


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def stage(label: str) -> None:
    print("OLEANDER_ARBITRARY_AXIS_ROTATE_STAGE=" + label, flush=True)


def vec(v):
    if hasattr(v, "x") and hasattr(v, "y") and hasattr(v, "z"):
        return App.Vector(float(v.x), float(v.y), float(v.z))
    return App.Vector(float(v[0]), float(v[1]), float(v[2]))


def unit(v):
    r = vec(v)
    if r.Length <= TOL:
        raise ValueError("vector must be non-zero")
    r.normalize()
    return r


def close(a, b, tol=TOL):
    return abs(float(a) - float(b)) <= tol


def same_point(a, b, tol=TOL):
    return (a - b).Length <= tol


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rotate_vector(vector, axis, angle_deg):
    v = vec(vector)
    k = unit(axis)
    a = math.radians(angle_deg)
    c, s = math.cos(a), math.sin(a)
    return v * c + k.cross(v) * s + k * (k.dot(v) * (1.0 - c))


def rotate_point(point, origin, axis, angle_deg):
    return origin + rotate_vector(point - origin, axis, angle_deg)


def transformed_local(local_axis, yaw_deg, pitch_deg):
    return unit(rotate_vector(rotate_vector(local_axis, App.Vector(0, 0, 1), yaw_deg), App.Vector(0, 1, 0), pitch_deg))


def face_normal(face):
    u0, u1, v0, v1 = face.ParameterRange
    n = face.normalAt((u0 + u1) * 0.5, (v0 + v1) * 0.5)
    n.normalize()
    return n


def ordered_points(face):
    pts = [v.Point for v in face.OuterWire.OrderedVertexes]
    check(len(pts) == 4, "rectangular_face_four_vertices")
    return pts


def select_face(shape, expected_normal):
    n = unit(expected_normal)
    found = [f for f in shape.Faces if face_normal(f).dot(n) > 0.999999]
    check(len(found) == 1, "semantic_face_selector_unique")
    return found[0]


def make_face(points, expected_normal):
    face = Part.Face(Part.makePolygon(points + [points[0]]))
    if face_normal(face).dot(unit(expected_normal)) < 0:
        face = face.reversed()
    check(face.isValid(), "rebuilt_face_valid")
    return face


def edge_connects(face, a, b):
    for edge in face.Edges:
        verts = edge.Vertexes
        if len(verts) != 2:
            continue
        p0, p1 = verts[0].Point, verts[1].Point
        if (same_point(p0, a) and same_point(p1, b)) or (same_point(p0, b) and same_point(p1, a)):
            return True
    return False


def replace_point(point, old_points, new_points):
    for old, new in zip(old_points, new_points):
        if same_point(point, old):
            return new
    return point


def make_ruled_adjacent_face(face, old_target_points, new_target_points):
    pts = ordered_points(face)
    shared = [p for p in pts if any(same_point(p, q) for q in old_target_points)]
    fixed = [p for p in pts if not any(same_point(p, q) for q in old_target_points)]
    check(len(shared) == 2 and len(fixed) == 2, "ruled_side_two_shared_two_fixed")
    check(edge_connects(face, shared[0], shared[1]), "ruled_side_shared_edge_exists")
    check(edge_connects(face, fixed[0], fixed[1]), "ruled_side_fixed_edge_exists")
    fixed_for_shared = []
    for sp in shared:
        candidates = [fp for fp in fixed if edge_connects(face, sp, fp)]
        check(len(candidates) == 1, "ruled_side_unique_correspondence")
        fixed_for_shared.append(candidates[0])
    check(not same_point(fixed_for_shared[0], fixed_for_shared[1]), "ruled_side_distinct_fixed_endpoints")
    moved = [replace_point(sp, old_target_points, new_target_points) for sp in shared]
    ruled = Part.makeRuledSurface(Part.makeLine(fixed_for_shared[0], fixed_for_shared[1]), Part.makeLine(moved[0], moved[1]))
    check(not ruled.isNull() and ruled.isValid(), "ruled_side_shape_valid")
    check(len(ruled.Faces) == 1, "ruled_side_single_face")
    rebuilt = ruled.Faces[0]
    if face_normal(rebuilt).dot(face_normal(face)) < 0:
        rebuilt = rebuilt.reversed()
    check(rebuilt.isValid(), "ruled_side_face_valid")
    check(len(rebuilt.Vertexes) == 4, "ruled_side_four_boundary_vertices")
    return rebuilt


def normalize_reshape(shape):
    candidate = shape.copy()
    candidate.sewShape(1e-7)
    candidate.fix(1e-7, 1e-7, 1e-7)
    candidate = candidate.removeSplitter()
    if candidate.isValid() and len(candidate.Solids) == 1:
        checks.append("reshape_direct_single_solid")
        return candidate.Solids[0]
    check(candidate.isValid(), "reshape_valid_before_shell_rebuild")
    check(candidate.ShapeType == "Shell", "reshape_shell_fallback")
    shell = Part.makeShell(candidate.Faces)
    shell.sewShape(1e-7)
    shell.fix(1e-7, 1e-7, 1e-7)
    solid = Part.makeSolid(shell).removeSplitter()
    check(solid.isValid() and len(solid.Solids) == 1, "shell_rebuild_valid_single_solid")
    return solid


def projected_signed_angle(old_normal, new_normal, axis):
    k = unit(axis)
    a = vec(old_normal) - k * k.dot(vec(old_normal))
    b = vec(new_normal) - k * k.dot(vec(new_normal))
    if a.Length <= TOL or b.Length <= TOL:
        raise ValueError("normal projection onto axis-normal plane is degenerate")
    a.normalize(); b.normalize()
    return math.degrees(math.atan2(k.dot(a.cross(b)), max(-1.0, min(1.0, a.dot(b)))))


def is_full3d(v):
    n = unit(v)
    return all(abs(c) > 0.05 for c in (n.x, n.y, n.z))


def metrics(shape):
    return {"bbox_mm": [shape.BoundBox.XLength, shape.BoundBox.YLength, shape.BoundBox.ZLength], "volume_mm3": shape.Volume, "solid_count": len(shape.Solids), "face_count": len(shape.Faces), "edge_count": len(shape.Edges)}


def local_frame(yaw_deg, pitch_deg):
    return (
        transformed_local(App.Vector(1, 0, 0), yaw_deg, pitch_deg),
        transformed_local(App.Vector(0, 1, 0), yaw_deg, pitch_deg),
        transformed_local(App.Vector(0, 0, 1), yaw_deg, pitch_deg),
    )


def arbitrary_axis(lx, ly, lz, coeff_x=2.0, coeff_y=4.0, coeff_z=3.0):
    vals = [coeff_x, coeff_y, coeff_z]
    if not all(math.isfinite(v) for v in vals):
        raise ValueError("axis coefficients must be finite")
    if math.sqrt(sum(v * v for v in vals)) < 1e-9:
        raise ValueError("arbitrary axis coefficients must be non-zero")
    return unit(lx * coeff_x + ly * coeff_y + lz * coeff_z)


def offset_pivot(center, lx, ly, lz, off_x=2.0, off_y=7.0, off_z=-4.0):
    vals = [off_x, off_y, off_z]
    if not all(math.isfinite(v) for v in vals):
        raise ValueError("pivot offsets must be finite")
    offset = lx * off_x + ly * off_y + lz * off_z
    if offset.Length < 1.0:
        raise ValueError("pivot must be offset from selected-face center")
    if offset.Length > 25.0:
        raise ValueError("pivot offset exceeds bounded contract")
    return center + offset


def rotate_selected_face(shape, selector_normal, axis, pivot, angle_deg):
    check(shape.isValid() and len(shape.Solids) == 1, "input_valid_single_solid")
    if not math.isfinite(angle_deg) or abs(angle_deg) < 1e-9:
        raise ValueError("rotation angle must be finite and non-zero")
    if abs(angle_deg) > 6.0:
        raise ValueError("rotation exceeds bounded angular contract")
    n, k = unit(selector_normal), unit(axis)
    check(is_full3d(n), "selector_normal_has_xyz_components")
    check(is_full3d(k), "arbitrary_axis_has_xyz_components")
    normal_component = abs(n.dot(k))
    if normal_component < 0.10:
        raise ValueError("rotation axis must include bounded normal component")
    if normal_component > 0.90:
        raise ValueError("rotation axis must include bounded tangent component")
    target = select_face(shape, n)
    opposite = select_face(shape, -n)
    old_pts = ordered_points(target)
    center = target.CenterOfMass
    pivot_vec = vec(pivot)
    pivot_offset = (pivot_vec - center).Length
    if pivot_offset < 1.0:
        raise ValueError("pivot must be offset from selected-face center")
    if pivot_offset > 25.0:
        raise ValueError("pivot offset exceeds bounded contract")
    opposite_center = opposite.CenterOfMass
    opposite_area = opposite.Area
    new_pts = [rotate_point(p, pivot_vec, k, angle_deg) for p in old_pts]
    expected_normal = unit(rotate_vector(n, k, angle_deg))
    expected_center = rotate_point(center, pivot_vec, k, angle_deg)
    new_target = make_face(new_pts, expected_normal)
    actual_normal = face_normal(new_target)
    actual_angle = projected_signed_angle(n, actual_normal, k)
    check(actual_normal.dot(expected_normal) > 0.999999, "rotated_normal_matches_expected")
    check(close(actual_angle, angle_deg, 1e-6), "projected_signed_angle_matches")
    check(close(new_target.Area, target.Area, 1e-5), "target_area_preserved")
    check((new_target.CenterOfMass - expected_center).Length <= 1e-5, "target_center_matches_offset_pivot_rotation")
    center_shift = (new_target.CenterOfMass - center).Length
    check(center_shift > 0.05, "offset_pivot_moves_target_center")
    replacements = [(target, new_target)]
    adjacent = 0
    for face in shape.Faces:
        if face.isSame(target) or face.isSame(opposite):
            continue
        pts = ordered_points(face)
        shared = sum(1 for p in pts if any(same_point(p, q) for q in old_pts))
        if shared == 0:
            continue
        check(shared == 2, "adjacent_face_shares_target_edge")
        replacements.append((face, make_ruled_adjacent_face(face, old_pts, new_pts)))
        adjacent += 1
    check(adjacent == 4 and len(replacements) == 5, "target_plus_four_adjacent_faces")
    reshaped = shape.replaceShape(replacements)
    check(not reshaped.isNull() and len(reshaped.Faces) == 6, "reshape_non_null_six_faces")
    edited = normalize_reshape(reshaped)
    check(edited.isValid() and len(edited.Solids) == 1, "edited_valid_single_solid")
    opposite_after = select_face(edited, -n)
    check((opposite_after.CenterOfMass - opposite_center).Length <= 1e-5, "opposite_center_preserved")
    check(close(opposite_after.Area, opposite_area, 1e-5), "opposite_area_preserved")
    target_after = select_face(edited, expected_normal)
    check((target_after.CenterOfMass - expected_center).Length <= 1e-5, "rotated_face_center_reselectable")
    return edited, {
        "selector_id": "SELECTOR::LOCAL_POS_X_FACE",
        "axis_id": "AXIS::OFFSET_PIVOT::ARBITRARY_LOCAL_2X_4Y_3Z",
        "axis_coefficients": dict(AXIS_COEFF),
        "pivot_offset_local_mm": dict(PIVOT_OFFSET_LOCAL_MM),
        "selector_world_normal": [n.x, n.y, n.z],
        "axis_world_direction": [k.x, k.y, k.z],
        "axis_normal_component_abs": normal_component,
        "axis_origin_mm": [pivot_vec.x, pivot_vec.y, pivot_vec.z],
        "target_center_before_mm": [center.x, center.y, center.z],
        "target_center_after_mm": [expected_center.x, expected_center.y, expected_center.z],
        "target_center_shift_mm": center_shift,
        "pivot_offset_length_mm": pivot_offset,
        "angle_deg": angle_deg,
        "actual_angle_deg": actual_angle,
        "expected_rotated_normal": [expected_normal.x, expected_normal.y, expected_normal.z],
        "operation": "BRepTools_ReShape_FULL3D_PLANAR_FACE_ROTATE_OFFSET_ARBITRARY_AXIS_RULED_SIDES",
        "replaced_face_count": 5,
        "adjacent_surface_model": "OCCT_RULED_SURFACE_BETWEEN_FIXED_AND_ROTATED_EDGES",
        "opposite_face_untouched": True,
    }


def build_revision(name, spec):
    source = Part.makeBox(*spec["dims"])
    source.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), spec["yaw_deg"])
    source.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), spec["pitch_deg"])
    lx, ly, lz = local_frame(spec["yaw_deg"], spec["pitch_deg"])
    target = select_face(source, lx)
    axis = arbitrary_axis(lx, ly, lz)
    pivot = offset_pivot(target.CenterOfMass, lx, ly, lz)
    check(0.10 < abs(lx.dot(axis)) < 0.90, "axis_has_bounded_normal_and_tangent_components_" + name)
    check((pivot - target.CenterOfMass).Length > 1.0, "offset_pivot_not_face_center_" + name)
    edited, op = rotate_selected_face(source, lx, axis, pivot, spec["angle_deg"])
    op["local_x_world_direction"] = [lx.x, lx.y, lx.z]
    op["local_y_world_direction"] = [ly.x, ly.y, ly.z]
    op["local_z_world_direction"] = [lz.x, lz.y, lz.z]
    return {"source": source, "edited": edited, "source_dims_mm": list(spec["dims"]), "yaw_deg": spec["yaw_deg"], "pitch_deg": spec["pitch_deg"], "angle_deg": spec["angle_deg"], "operation": op, "metrics": metrics(edited)}


def add_feature(doc, name, rev):
    op = rev["operation"]
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = rev["edited"]
    for prop, value in [("OLE_ID", "OLE_ARBITRARY_AXIS_FACE_ROTATE::" + name), ("OLE_Operation", op["operation"]), ("OLE_Selector", op["selector_id"]), ("OLE_AxisID", op["axis_id"]), ("OLE_GeometryAuthority", "FREECAD_OCCT_BREP")]:
        obj.addProperty("App::PropertyString", prop, "OLEANDER"); setattr(obj, prop, value)
    obj.addProperty("App::PropertyVector", "OLE_AxisWorldDirection", "OLEANDER"); obj.OLE_AxisWorldDirection = vec(op["axis_world_direction"])
    obj.addProperty("App::PropertyVector", "OLE_AxisOrigin", "OLEANDER"); obj.OLE_AxisOrigin = vec(op["axis_origin_mm"])
    for prop, value in [("OLE_YawDeg", rev["yaw_deg"]), ("OLE_PitchDeg", rev["pitch_deg"]), ("OLE_AngleDeg", rev["angle_deg"]), ("OLE_AxisCoeffX", 2.0), ("OLE_AxisCoeffY", 4.0), ("OLE_AxisCoeffZ", 3.0), ("OLE_PivotOffsetXmm", 2.0), ("OLE_PivotOffsetYmm", 7.0), ("OLE_PivotOffsetZmm", -4.0)]:
        obj.addProperty("App::PropertyFloat", prop, "OLEANDER"); setattr(obj, prop, value)
    return obj


def serializable(rev):
    return {"source_dims_mm": rev["source_dims_mm"], "yaw_deg": rev["yaw_deg"], "pitch_deg": rev["pitch_deg"], "angle_deg": rev["angle_deg"], "operation": rev["operation"], "metrics": rev["metrics"]}


def display_record(name, rev, step):
    verts, facets = rev["edited"].tessellate(0.25)
    check(bool(verts) and bool(facets), "display_tessellation_" + name)
    op = rev["operation"]
    return {"revision": name, "ole_id": "OLE_ARBITRARY_AXIS_FACE_ROTATE::" + name, "yaw_deg": rev["yaw_deg"], "pitch_deg": rev["pitch_deg"], "angle_deg": rev["angle_deg"], "actual_angle_deg": op["actual_angle_deg"], "selector_id": op["selector_id"], "axis_id": op["axis_id"], "axis_coefficients": op["axis_coefficients"], "pivot_offset_local_mm": op["pivot_offset_local_mm"], "selector_world_normal": op["selector_world_normal"], "axis_world_direction": op["axis_world_direction"], "axis_normal_component_abs": op["axis_normal_component_abs"], "axis_origin_mm": op["axis_origin_mm"], "target_center_before_mm": op["target_center_before_mm"], "target_center_after_mm": op["target_center_after_mm"], "target_center_shift_mm": op["target_center_shift_mm"], "pivot_offset_length_mm": op["pivot_offset_length_mm"], "expected_rotated_normal": op["expected_rotated_normal"], "bbox_mm": rev["metrics"]["bbox_mm"], "volume_mm3": rev["metrics"]["volume_mm3"], "vertices_mm": [[v.x, v.y, v.z] for v in verts], "triangles": [list(f) for f in facets], "source_step": step.name, "source_step_sha256": sha256(step)}


def main():
    revs = {}
    for name, spec in REVISIONS.items():
        stage(name); revs[name] = build_revision(name, spec)
    check(revs["R001"]["operation"]["selector_id"] == revs["R002"]["operation"]["selector_id"], "selector_id_stable")
    check(revs["R001"]["operation"]["axis_id"] == revs["R002"]["operation"]["axis_id"], "arbitrary_axis_id_stable")
    check(vec(revs["R001"]["operation"]["axis_world_direction"]).dot(vec(revs["R002"]["operation"]["axis_world_direction"])) < 0.99, "arbitrary_axis_world_direction_changes")
    for name, rev in revs.items():
        op = rev["operation"]
        check(rev["metrics"]["solid_count"] == 1 and rev["metrics"]["face_count"] == 6, "topology_" + name)
        check(close(op["actual_angle_deg"], rev["angle_deg"], 1e-6), "signed_angle_" + name)
        check(is_full3d(vec(op["axis_world_direction"])), "full3d_arbitrary_axis_" + name)
        check(0.10 < op["axis_normal_component_abs"] < 0.90, "non_tangent_non_normal_axis_" + name)
        check(op["target_center_shift_mm"] > 0.05, "offset_pivot_center_shift_" + name)
        check(op["adjacent_surface_model"] == "OCCT_RULED_SURFACE_BETWEEN_FIXED_AND_ROTATED_EDGES", "ruled_side_model_" + name)

    stage("EXPECTED_FAILURES")
    base = revs["R002"]["source"]
    lx, ly, lz = local_frame(REVISIONS["R002"]["yaw_deg"], REVISIONS["R002"]["pitch_deg"])
    target = select_face(base, lx); good_axis = arbitrary_axis(lx, ly, lz); good_pivot = offset_pivot(target.CenterOfMass, lx, ly, lz)
    failures = {}
    cases = [
        ("zero_angle", good_axis, good_pivot, 0.0, "non-zero"),
        ("excessive_angle", good_axis, good_pivot, 8.0, "bounded angular contract"),
        ("tangent_axis", unit(ly * 4.0 + lz * 3.0), good_pivot, 2.0, "normal component"),
        ("near_normal_axis", unit(lx * 20.0 + ly), good_pivot, 2.0, "tangent component"),
        ("center_pivot", good_axis, target.CenterOfMass, 2.0, "offset from selected-face center"),
        ("far_pivot", good_axis, target.CenterOfMass + ly * 30.0, 2.0, "pivot offset exceeds"),
    ]
    for label, axis, pivot, angle, needle in cases:
        state = "FAIL"
        try: rotate_selected_face(base, lx, axis, pivot, angle)
        except ValueError as exc:
            if needle in str(exc): state = "PASS"; checks.append("expected_failure_" + label)
        check(state == "PASS", "failure_gate_" + label); failures[label] = state
    coeff_failure = "FAIL"
    try: arbitrary_axis(lx, ly, lz, 0.0, 0.0, 0.0)
    except ValueError as exc:
        if "non-zero" in str(exc): coeff_failure = "PASS"; checks.append("expected_failure_zero_axis_coefficients")
    check(coeff_failure == "PASS", "failure_gate_zero_axis_coefficients"); failures["zero_axis_coefficients"] = coeff_failure

    stage("FCSTD_WRITE")
    doc = App.newDocument("OLEANDER_ARBITRARY_AXIS_FACE_ROTATE")
    o1, o2 = add_feature(doc, "R001", revs["R001"]), add_feature(doc, "R002", revs["R002"])
    doc.recompute(); doc.saveAs(str(FCSTD)); o1.Shape.exportStep(str(STEP_R001)); o2.Shape.exportStep(str(STEP_R002))
    check(FCSTD.exists() and STEP_R001.exists() and STEP_R002.exists(), "native_artifacts_written")
    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(FCSTD))
    for name in ("R001", "R002"):
        obj = reopened.getObject(name); op = revs[name]["operation"]
        check(obj is not None and obj.Shape.isValid() and len(obj.Shape.Solids) == 1, "reopen_object_solid_" + name)
        check(obj.OLE_AxisID == "AXIS::OFFSET_PIVOT::ARBITRARY_LOCAL_2X_4Y_3Z", "reopen_axis_id_" + name)
        check(close(float(obj.OLE_AxisCoeffX), 2.0) and close(float(obj.OLE_AxisCoeffY), 4.0) and close(float(obj.OLE_AxisCoeffZ), 3.0), "reopen_axis_coefficients_" + name)
        check(close(float(obj.OLE_PivotOffsetXmm), 2.0) and close(float(obj.OLE_PivotOffsetYmm), 7.0) and close(float(obj.OLE_PivotOffsetZmm), -4.0), "reopen_pivot_offsets_" + name)
        check((obj.OLE_AxisWorldDirection - vec(op["axis_world_direction"])).Length <= 1e-6, "reopen_axis_direction_" + name)
        check((obj.OLE_AxisOrigin - vec(op["axis_origin_mm"])).Length <= 1e-6, "reopen_axis_origin_" + name)
        check(obj.OLE_GeometryAuthority == "FREECAD_OCCT_BREP", "reopen_authority_" + name)
    App.closeDocument(reopened.Name)

    stage("DISPLAY")
    display = {"schema": "OLEANDER_ARBITRARY_AXIS_FACE_ROTATE_DISPLAY_v0.1", "master_type": "CAD_NATIVE", "geometry_authority": "FREECAD_OCCT_BREP", "display_authority": "DISPLAY_DERIVATIVE_ONLY", "units": "mm", "angle_units": "deg", "source_fcstd": FCSTD.name, "source_fcstd_sha256": sha256(FCSTD), "revisions": [display_record("R001", revs["R001"], STEP_R001), display_record("R002", revs["R002"], STEP_R002)]}
    DISPLAY.write_text(json.dumps(display, indent=2, sort_keys=True), encoding="utf-8")
    manifest = {"schema": "OLEANDER_FREECAD_ARBITRARY_AXIS_FACE_ROTATE_v0.1", "status": "PASS", "units": "mm", "angle_units": "deg", "authority": {"geometry_master": "FREECAD_OCCT_BREP", "blender": "DISPLAY_DERIVATIVE_ONLY"}, "selector": "semantic local +X planar face after yaw+pitch transform", "axis": "offset-pivot normalize(2*localX+4*localY+3*localZ) line with both normal and tangent components", "pivot": "selected-face center +2*localX +7*localY -4*localZ mm", "side_surface_model": "OCCT ruled surfaces between fixed opposite edges and rotated target edges", "R001": serializable(revs["R001"]), "R002": serializable(revs["R002"]), "expected_failure_cases": failures, "artifacts": {"fcstd": {"path": FCSTD.name, "sha256": sha256(FCSTD)}, "step_R001": {"path": STEP_R001.name, "sha256": sha256(STEP_R001)}, "step_R002": {"path": STEP_R002.name, "sha256": sha256(STEP_R002)}, "display": {"path": DISPLAY.name, "sha256": sha256(DISPLAY)}}, "checks": checks, "non_claims": ["P0_B_DIRECT_BREP_PASS", "unrestricted_arbitrary_axis_face_rotate", "arbitrary_pivot_placement", "general_nonplanar_face_direct_edit", "persistent_topological_naming", "production_direct_modeling_parity"]}
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    stage("PASS"); print("OLEANDER_FREECAD_ARBITRARY_AXIS_FACE_ROTATE=" + json.dumps(manifest, sort_keys=True), flush=True)


if __name__ == "__main__":
    stage("START")
    try: main()
    except BaseException as exc:
        print("OLEANDER_ARBITRARY_AXIS_ROTATE_EXCEPTION=" + repr(exc), flush=True); traceback.print_exc(); raise
