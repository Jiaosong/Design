"""OLEANDER bounded full-3D planar-face rotation about a custom tangent axis.

The semantic local +X face of a yaw+pitch transformed FreeCAD/OCCT box is
selected by transformed normal. A user-defined tangent axis is constructed at
the selected-face center from normalize(4*localY + 3*localZ), transformed with
the same source orientation. The face and four adjacent faces are rebuilt via
BRepTools_ReShape.

This proves one bounded custom tangent-axis family, not unrestricted arbitrary
axis rotation, nonplanar editing, persistent topological naming, or P0-B parity.
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

OUT = Path(os.environ.get("OLEANDER_CUSTOM_AXIS_ROTATE_DIR", "/tmp/oleander-custom-axis-rotate"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_custom_tangent_axis_face_rotate.FCStd"
STEP_R001 = OUT / "oleander_custom_tangent_axis_face_rotate_R001.step"
STEP_R002 = OUT / "oleander_custom_tangent_axis_face_rotate_R002.step"
DISPLAY = OUT / "oleander_custom_tangent_axis_face_rotate_display.json"
MANIFEST = OUT / "oleander_custom_tangent_axis_face_rotate_manifest.json"
TOL = 1e-6
checks: list[str] = []

REVISIONS = {
    "R001": {"dims": (80.0, 50.0, 10.0), "yaw_deg": 30.0, "pitch_deg": 20.0, "angle_deg": 3.0},
    "R002": {"dims": (100.0, 60.0, 12.0), "yaw_deg": -25.0, "pitch_deg": -15.0, "angle_deg": -3.0},
}
AXIS_COEFF = {"local_y": 4.0, "local_z": 3.0}


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def stage(label: str) -> None:
    print("OLEANDER_CUSTOM_AXIS_ROTATE_STAGE=" + label, flush=True)


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
    return abs(a - b) <= tol


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


def signed_angle(old_normal, new_normal, axis):
    a, b, k = unit(old_normal), unit(new_normal), unit(axis)
    return math.degrees(math.atan2(k.dot(a.cross(b)), max(-1.0, min(1.0, a.dot(b)))))


def rotate_point(point, origin, axis, angle_deg):
    return origin + rotate_vector(point - origin, axis, angle_deg)


def replace_point(point, old_points, new_points):
    for old, new in zip(old_points, new_points):
        if same_point(point, old):
            return new
    return point


def is_full3d(v):
    n = unit(v)
    return all(abs(c) > 0.05 for c in (n.x, n.y, n.z))


def metrics(shape):
    return {
        "bbox_mm": [shape.BoundBox.XLength, shape.BoundBox.YLength, shape.BoundBox.ZLength],
        "volume_mm3": shape.Volume,
        "solid_count": len(shape.Solids),
        "face_count": len(shape.Faces),
        "edge_count": len(shape.Edges),
    }


def custom_axis(yaw_deg, pitch_deg, coeff_y=4.0, coeff_z=3.0):
    if not math.isfinite(coeff_y) or not math.isfinite(coeff_z):
        raise ValueError("axis coefficients must be finite")
    if math.hypot(coeff_y, coeff_z) < 1e-9:
        raise ValueError("custom tangent axis coefficients must be non-zero")
    ly = transformed_local(App.Vector(0, 1, 0), yaw_deg, pitch_deg)
    lz = transformed_local(App.Vector(0, 0, 1), yaw_deg, pitch_deg)
    return unit(ly * coeff_y + lz * coeff_z), ly, lz


def rotate_selected_face(shape, selector_normal, axis, angle_deg):
    check(shape.isValid() and len(shape.Solids) == 1, "input_valid_single_solid")
    if not math.isfinite(angle_deg) or abs(angle_deg) < 1e-9:
        raise ValueError("rotation angle must be finite and non-zero")
    if abs(angle_deg) > 10.0:
        raise ValueError("rotation exceeds bounded angular contract")
    n, k = unit(selector_normal), unit(axis)
    check(is_full3d(n), "selector_normal_has_xyz_components")
    check(is_full3d(k), "custom_axis_has_xyz_components")
    if abs(n.dot(k)) > 1e-7:
        raise ValueError("rotation axis must lie in selected face tangent plane")

    target = select_face(shape, n)
    opposite = select_face(shape, -n)
    old_pts = ordered_points(target)
    center = target.CenterOfMass
    opposite_center = opposite.CenterOfMass
    opposite_area = opposite.Area
    new_pts = [rotate_point(p, center, k, angle_deg) for p in old_pts]
    expected_normal = unit(rotate_vector(n, k, angle_deg))
    new_target = make_face(new_pts, expected_normal)
    actual_normal = face_normal(new_target)
    actual_angle = signed_angle(n, actual_normal, k)
    check(actual_normal.dot(expected_normal) > 0.999999, "rotated_normal_matches_expected")
    check(close(actual_angle, angle_deg, 1e-6), "signed_angle_matches")
    check(close(new_target.Area, target.Area, 1e-5), "target_area_preserved")
    check((new_target.CenterOfMass - center).Length <= 1e-5, "target_center_preserved")

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
        rebuilt = make_face([replace_point(p, old_pts, new_pts) for p in pts], face_normal(face))
        replacements.append((face, rebuilt))
        adjacent += 1
    check(adjacent == 4 and len(replacements) == 5, "target_plus_four_adjacent_faces")

    reshaped = shape.replaceShape(replacements)
    check(not reshaped.isNull() and len(reshaped.Faces) == 6, "reshape_non_null_six_faces")
    edited = normalize_reshape(reshaped)
    check(edited.isValid() and len(edited.Solids) == 1, "edited_valid_single_solid")
    opposite_after = select_face(edited, -n)
    check((opposite_after.CenterOfMass - opposite_center).Length <= 1e-5, "opposite_center_preserved")
    check(close(opposite_after.Area, opposite_area, 1e-5), "opposite_area_preserved")
    check(face_normal(select_face(edited, expected_normal)).dot(expected_normal) > 0.999999, "rotated_face_reselectable")

    return edited, {
        "selector_id": "SELECTOR::LOCAL_POS_X_FACE",
        "axis_id": "AXIS::SELECTED_FACE_CENTER::CUSTOM_TANGENT_4Y_3Z",
        "axis_coefficients": {"local_y": 4.0, "local_z": 3.0},
        "selector_world_normal": [n.x, n.y, n.z],
        "axis_world_direction": [k.x, k.y, k.z],
        "axis_origin_mm": [center.x, center.y, center.z],
        "angle_deg": angle_deg,
        "actual_angle_deg": actual_angle,
        "expected_rotated_normal": [expected_normal.x, expected_normal.y, expected_normal.z],
        "operation": "BRepTools_ReShape_FULL3D_PLANAR_FACE_ROTATE_CUSTOM_TANGENT_AXIS",
        "replaced_face_count": 5,
        "opposite_face_untouched": True,
    }


def build_revision(name, spec):
    source = Part.makeBox(*spec["dims"])
    source.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), spec["yaw_deg"])
    source.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), spec["pitch_deg"])
    n = transformed_local(App.Vector(1, 0, 0), spec["yaw_deg"], spec["pitch_deg"])
    axis, ly, lz = custom_axis(spec["yaw_deg"], spec["pitch_deg"])
    check(abs(n.dot(axis)) <= 1e-7, "custom_axis_tangent_" + name)
    edited, op = rotate_selected_face(source, n, axis, spec["angle_deg"])
    op["local_y_world_direction"] = [ly.x, ly.y, ly.z]
    op["local_z_world_direction"] = [lz.x, lz.y, lz.z]
    return {"source": source, "edited": edited, "source_dims_mm": list(spec["dims"]), "yaw_deg": spec["yaw_deg"], "pitch_deg": spec["pitch_deg"], "angle_deg": spec["angle_deg"], "operation": op, "metrics": metrics(edited)}


def add_feature(doc, name, rev):
    op = rev["operation"]
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = rev["edited"]
    for prop, value in [("OLE_ID", "OLE_CUSTOM_AXIS_FACE_ROTATE::" + name), ("OLE_Operation", op["operation"]), ("OLE_Selector", op["selector_id"]), ("OLE_AxisID", op["axis_id"]), ("OLE_GeometryAuthority", "FREECAD_OCCT_BREP")]:
        obj.addProperty("App::PropertyString", prop, "OLEANDER")
        setattr(obj, prop, value)
    obj.addProperty("App::PropertyVector", "OLE_AxisWorldDirection", "OLEANDER")
    obj.OLE_AxisWorldDirection = vec(op["axis_world_direction"])
    for prop, value in [("OLE_YawDeg", rev["yaw_deg"]), ("OLE_PitchDeg", rev["pitch_deg"]), ("OLE_AngleDeg", rev["angle_deg"]), ("OLE_AxisCoeffY", 4.0), ("OLE_AxisCoeffZ", 3.0)]:
        obj.addProperty("App::PropertyFloat", prop, "OLEANDER")
        setattr(obj, prop, value)
    return obj


def serializable(rev):
    return {"source_dims_mm": rev["source_dims_mm"], "yaw_deg": rev["yaw_deg"], "pitch_deg": rev["pitch_deg"], "angle_deg": rev["angle_deg"], "operation": rev["operation"], "metrics": rev["metrics"]}


def display_record(name, rev, step):
    verts, facets = rev["edited"].tessellate(0.25)
    check(bool(verts) and bool(facets), "display_tessellation_" + name)
    op = rev["operation"]
    return {
        "revision": name, "ole_id": "OLE_CUSTOM_AXIS_FACE_ROTATE::" + name,
        "yaw_deg": rev["yaw_deg"], "pitch_deg": rev["pitch_deg"], "angle_deg": rev["angle_deg"], "actual_angle_deg": op["actual_angle_deg"],
        "selector_id": op["selector_id"], "axis_id": op["axis_id"], "axis_coefficients": op["axis_coefficients"],
        "selector_world_normal": op["selector_world_normal"], "axis_world_direction": op["axis_world_direction"], "expected_rotated_normal": op["expected_rotated_normal"],
        "bbox_mm": rev["metrics"]["bbox_mm"], "volume_mm3": rev["metrics"]["volume_mm3"],
        "vertices_mm": [[v.x, v.y, v.z] for v in verts], "triangles": [list(f) for f in facets],
        "source_step": step.name, "source_step_sha256": sha256(step)
    }


def main():
    revs = {}
    for name, spec in REVISIONS.items():
        stage(name)
        revs[name] = build_revision(name, spec)
    check(revs["R001"]["operation"]["selector_id"] == revs["R002"]["operation"]["selector_id"], "selector_id_stable")
    check(revs["R001"]["operation"]["axis_id"] == revs["R002"]["operation"]["axis_id"], "custom_axis_id_stable")
    check(vec(revs["R001"]["operation"]["axis_world_direction"]).dot(vec(revs["R002"]["operation"]["axis_world_direction"])) < 0.99, "custom_axis_world_direction_changes")
    for name, rev in revs.items():
        check(rev["metrics"]["solid_count"] == 1 and rev["metrics"]["face_count"] == 6, "topology_" + name)
        check(close(rev["operation"]["actual_angle_deg"], rev["angle_deg"], 1e-6), "signed_angle_" + name)
        check(is_full3d(vec(rev["operation"]["axis_world_direction"])), "full3d_custom_axis_" + name)

    stage("EXPECTED_FAILURES")
    base = revs["R002"]["source"]
    n = transformed_local(App.Vector(1,0,0), REVISIONS["R002"]["yaw_deg"], REVISIONS["R002"]["pitch_deg"])
    good_axis, _, _ = custom_axis(REVISIONS["R002"]["yaw_deg"], REVISIONS["R002"]["pitch_deg"])
    failures = {}
    for label, axis, angle, needle in [
        ("zero_angle", good_axis, 0.0, "non-zero"),
        ("excessive_angle", good_axis, 12.0, "bounded angular contract"),
        ("axis_has_normal_component", unit(good_axis + n * 0.5), 3.0, "tangent plane")
    ]:
        state = "FAIL"
        try:
            rotate_selected_face(base, n, axis, angle)
        except ValueError as exc:
            if needle in str(exc):
                state = "PASS"; checks.append("expected_failure_" + label)
        check(state == "PASS", "failure_gate_" + label); failures[label] = state
    coeff_failure = "FAIL"
    try:
        custom_axis(REVISIONS["R002"]["yaw_deg"], REVISIONS["R002"]["pitch_deg"], 0.0, 0.0)
    except ValueError as exc:
        if "non-zero" in str(exc):
            coeff_failure = "PASS"; checks.append("expected_failure_zero_axis_coefficients")
    check(coeff_failure == "PASS", "failure_gate_zero_axis_coefficients"); failures["zero_axis_coefficients"] = coeff_failure

    stage("FCSTD_WRITE")
    doc = App.newDocument("OLEANDER_CUSTOM_TANGENT_AXIS_FACE_ROTATE")
    o1, o2 = add_feature(doc, "R001", revs["R001"]), add_feature(doc, "R002", revs["R002"])
    doc.recompute(); doc.saveAs(str(FCSTD)); o1.Shape.exportStep(str(STEP_R001)); o2.Shape.exportStep(str(STEP_R002))
    check(FCSTD.exists() and STEP_R001.exists() and STEP_R002.exists(), "native_artifacts_written")
    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(FCSTD))
    for name in ("R001", "R002"):
        obj = reopened.getObject(name); rev = revs[name]
        check(obj is not None and obj.Shape.isValid() and len(obj.Shape.Solids) == 1, "reopen_object_solid_" + name)
        check(obj.OLE_Selector == "SELECTOR::LOCAL_POS_X_FACE", "reopen_selector_" + name)
        check(obj.OLE_AxisID == "AXIS::SELECTED_FACE_CENTER::CUSTOM_TANGENT_4Y_3Z", "reopen_axis_id_" + name)
        check(close(float(obj.OLE_AxisCoeffY), 4.0) and close(float(obj.OLE_AxisCoeffZ), 3.0), "reopen_axis_coefficients_" + name)
        check((obj.OLE_AxisWorldDirection - vec(rev["operation"]["axis_world_direction"])).Length <= 1e-6, "reopen_axis_direction_" + name)
        check(obj.OLE_GeometryAuthority == "FREECAD_OCCT_BREP", "reopen_authority_" + name)
    App.closeDocument(reopened.Name)

    stage("DISPLAY")
    display = {"schema":"OLEANDER_CUSTOM_TANGENT_AXIS_FACE_ROTATE_DISPLAY_v0.1","master_type":"CAD_NATIVE","geometry_authority":"FREECAD_OCCT_BREP","display_authority":"DISPLAY_DERIVATIVE_ONLY","units":"mm","angle_units":"deg","source_fcstd":FCSTD.name,"source_fcstd_sha256":sha256(FCSTD),"revisions":[display_record("R001",revs["R001"],STEP_R001),display_record("R002",revs["R002"],STEP_R002)]}
    DISPLAY.write_text(json.dumps(display, indent=2, sort_keys=True), encoding="utf-8")
    manifest = {"schema":"OLEANDER_FREECAD_CUSTOM_TANGENT_AXIS_FACE_ROTATE_v0.1","status":"PASS","units":"mm","angle_units":"deg","authority":{"geometry_master":"FREECAD_OCCT_BREP","blender":"DISPLAY_DERIVATIVE_ONLY"},"selector":"semantic local +X planar face after yaw+pitch transform","axis":"selected-face-center user-defined normalize(4*localY+3*localZ) tangent axis","R001":serializable(revs["R001"]),"R002":serializable(revs["R002"]),"expected_failure_cases":failures,"artifacts":{"fcstd":{"path":FCSTD.name,"sha256":sha256(FCSTD)},"step_R001":{"path":STEP_R001.name,"sha256":sha256(STEP_R001)},"step_R002":{"path":STEP_R002.name,"sha256":sha256(STEP_R002)},"display":{"path":DISPLAY.name,"sha256":sha256(DISPLAY)}},"checks":checks,"non_claims":["P0_B_DIRECT_BREP_PASS","general_arbitrary_axis_face_rotate","axis_not_constrained_to_face_tangent_plane","nonplanar_face_rotate","persistent_topological_naming","production_direct_modeling_parity"]}
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    stage("PASS"); print("OLEANDER_FREECAD_CUSTOM_TANGENT_AXIS_FACE_ROTATE=" + json.dumps(manifest, sort_keys=True), flush=True)


if __name__ == "__main__":
    stage("START")
    try: main()
    except BaseException as exc:
        print("OLEANDER_CUSTOM_AXIS_ROTATE_EXCEPTION=" + repr(exc), flush=True); traceback.print_exc(); raise
