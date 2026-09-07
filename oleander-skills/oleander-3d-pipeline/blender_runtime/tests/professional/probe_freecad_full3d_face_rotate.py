"""OLEANDER bounded full-3D-oriented planar-face local-axis rotation probe.

A rectangular FreeCAD/OCCT solid is yawed about world Z and then pitched about
world Y. Its semantic local +X face normal and local +Y tangent axis therefore
carry non-zero X/Y/Z components. The face is re-resolved from the transformed
normal and rotated about its center along the transformed local +Y axis.

Bounded proof only. This does not establish arbitrary topology, nonplanar face
rotation, persistent topological naming, or general P0-B direct-modeling parity.
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

OUT = Path(os.environ.get("OLEANDER_FULL3D_FACE_ROTATE_DIR", "/tmp/oleander-full3d-face-rotate"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_full3d_face_rotate.FCStd"
STEP_R001 = OUT / "oleander_full3d_face_rotate_R001.step"
STEP_R002 = OUT / "oleander_full3d_face_rotate_R002.step"
DISPLAY = OUT / "oleander_full3d_face_rotate_display.json"
MANIFEST = OUT / "oleander_full3d_face_rotate_manifest.json"
TOL = 1e-6
checks: list[str] = []

REVISIONS = {
    "R001": {"dims": (80.0, 50.0, 10.0), "yaw_deg": 30.0, "pitch_deg": 20.0, "angle_deg": 4.0},
    "R002": {"dims": (100.0, 60.0, 12.0), "yaw_deg": -25.0, "pitch_deg": -15.0, "angle_deg": -4.0},
}


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def stage(label: str) -> None:
    print("OLEANDER_FULL3D_FACE_ROTATE_STAGE=" + label, flush=True)


def vec(values):
    if hasattr(values, "x") and hasattr(values, "y") and hasattr(values, "z"):
        return App.Vector(float(values.x), float(values.y), float(values.z))
    return App.Vector(float(values[0]), float(values[1]), float(values[2]))


def unit(values):
    result = vec(values)
    if result.Length <= TOL:
        raise ValueError("vector must be non-zero")
    result.normalize()
    return result


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol


def same_point(a, b, tol: float = TOL) -> bool:
    return (a - b).Length <= tol


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rotate_vector(vector, axis, angle_deg: float):
    v = vec(vector)
    k = unit(axis)
    a = math.radians(angle_deg)
    c = math.cos(a)
    s = math.sin(a)
    return v * c + k.cross(v) * s + k * (k.dot(v) * (1.0 - c))


def transformed_local_axis(local_axis, yaw_deg: float, pitch_deg: float):
    after_yaw = rotate_vector(local_axis, App.Vector(0, 0, 1), yaw_deg)
    after_pitch = rotate_vector(after_yaw, App.Vector(0, 1, 0), pitch_deg)
    return unit(after_pitch)


def face_normal(face):
    u0, u1, v0, v1 = face.ParameterRange
    n = face.normalAt((u0 + u1) * 0.5, (v0 + v1) * 0.5)
    n.normalize()
    return n


def ordered_points(face):
    points = [v.Point for v in face.OuterWire.OrderedVertexes]
    check(len(points) == 4, "rectangular_face_four_vertices")
    return points


def select_face_by_normal(shape, expected_normal):
    expected = unit(expected_normal)
    found = [face for face in shape.Faces if face_normal(face).dot(expected) > 0.999999]
    check(len(found) == 1, "semantic_face_selector_unique")
    return found[0]


def make_oriented_face(points, expected_normal):
    face = Part.Face(Part.makePolygon(points + [points[0]]))
    if face_normal(face).dot(unit(expected_normal)) < 0:
        face = face.reversed()
    check(face.isValid(), "rebuilt_face_valid")
    return face


def normalize_reshape_output(reshaped):
    candidate = reshaped.copy()
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
    check(solid.isValid(), "shell_rebuild_valid_solid")
    check(len(solid.Solids) == 1, "shell_rebuild_one_solid")
    return solid


def signed_angle(old_normal, new_normal, axis):
    old_n = unit(old_normal)
    new_n = unit(new_normal)
    k = unit(axis)
    s = k.dot(old_n.cross(new_n))
    c = max(-1.0, min(1.0, old_n.dot(new_n)))
    return math.degrees(math.atan2(s, c))


def rotate_point(point, origin, axis, angle_deg: float):
    return origin + rotate_vector(point - origin, axis, angle_deg)


def replacement_point(point, old_points, new_points):
    for old, new in zip(old_points, new_points):
        if same_point(point, old):
            return new
    return point


def is_full3d_direction(v):
    n = unit(v)
    return all(abs(component) > 0.05 for component in (n.x, n.y, n.z))


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


def rotate_full3d_face(shape, selector_normal, tangent_axis, angle_deg: float):
    check(shape.isValid() and len(shape.Solids) == 1, "input_valid_single_solid")
    if not math.isfinite(angle_deg) or abs(angle_deg) < 1e-9:
        raise ValueError("rotation angle must be finite and non-zero")
    if abs(angle_deg) > 12.0:
        raise ValueError("rotation exceeds bounded angular contract")

    n = unit(selector_normal)
    axis = unit(tangent_axis)
    check(is_full3d_direction(n), "selector_normal_has_xyz_components")
    check(is_full3d_direction(axis), "rotation_axis_has_xyz_components")
    if abs(n.dot(axis)) > 1e-7:
        raise ValueError("rotation axis must lie in selected face tangent plane")

    target = select_face_by_normal(shape, n)
    opposite = select_face_by_normal(shape, -n)
    old_points = ordered_points(target)
    center = target.CenterOfMass
    opposite_center_before = opposite.CenterOfMass
    opposite_area_before = opposite.Area
    new_points = [rotate_point(p, center, axis, angle_deg) for p in old_points]
    expected_normal = unit(rotate_vector(n, axis, angle_deg))
    new_target = make_oriented_face(new_points, expected_normal)
    actual_normal = face_normal(new_target)
    actual_angle_deg = signed_angle(n, actual_normal, axis)
    check(actual_normal.dot(expected_normal) > 0.999999, "rotated_normal_matches_expected")
    check(close(actual_angle_deg, angle_deg, 1e-6), "signed_angle_matches")
    check(close(new_target.Area, target.Area, 1e-5), "target_area_preserved")
    check((new_target.CenterOfMass - center).Length <= 1e-5, "target_center_preserved")

    replacements = [(target, new_target)]
    adjacent_count = 0
    for face in shape.Faces:
        if face.isSame(target) or face.isSame(opposite):
            continue
        points = ordered_points(face)
        shared = sum(1 for p in points if any(same_point(p, tp) for tp in old_points))
        if shared == 0:
            continue
        check(shared == 2, "adjacent_face_shares_target_edge")
        rebuilt_points = [replacement_point(p, old_points, new_points) for p in points]
        rebuilt = make_oriented_face(rebuilt_points, face_normal(face))
        replacements.append((face, rebuilt))
        adjacent_count += 1

    check(adjacent_count == 4, "four_adjacent_faces_rebuilt")
    reshaped = shape.replaceShape(replacements)
    check(not reshaped.isNull(), "reshape_non_null")
    check(len(reshaped.Faces) == 6, "reshape_six_faces")
    edited = normalize_reshape_output(reshaped)
    check(edited.isValid() and len(edited.Solids) == 1, "edited_valid_single_solid")
    check(edited.Volume > 0.0, "edited_positive_volume")

    opposite_after = select_face_by_normal(edited, -n)
    check((opposite_after.CenterOfMass - opposite_center_before).Length <= 1e-5, "opposite_center_preserved")
    check(close(opposite_after.Area, opposite_area_before, 1e-5), "opposite_area_preserved")
    selected_after = select_face_by_normal(edited, expected_normal)
    check(face_normal(selected_after).dot(expected_normal) > 0.999999, "rotated_face_reselectable")

    return edited, {
        "selector_id": "SELECTOR::LOCAL_POS_X_FACE",
        "axis_id": "AXIS::SELECTED_FACE_CENTER::LOCAL_POS_Y",
        "selector_world_normal": [n.x, n.y, n.z],
        "axis_world_direction": [axis.x, axis.y, axis.z],
        "axis_origin_mm": [center.x, center.y, center.z],
        "angle_deg": angle_deg,
        "actual_angle_deg": actual_angle_deg,
        "expected_rotated_normal": [expected_normal.x, expected_normal.y, expected_normal.z],
        "actual_rotated_normal": [actual_normal.x, actual_normal.y, actual_normal.z],
        "operation": "BRepTools_ReShape_FULL3D_PLANAR_FACE_ROTATE_LOCAL_TANGENT_AXIS",
        "replaced_face_count": 5,
        "opposite_face_untouched": True,
    }


def build_revision(name, dims, yaw_deg, pitch_deg, angle_deg):
    source = Part.makeBox(*dims)
    source.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), yaw_deg)
    source.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), pitch_deg)
    selector_normal = transformed_local_axis(App.Vector(1, 0, 0), yaw_deg, pitch_deg)
    tangent_axis = transformed_local_axis(App.Vector(0, 1, 0), yaw_deg, pitch_deg)
    edited, op = rotate_full3d_face(source, selector_normal, tangent_axis, angle_deg)
    return {
        "source": source,
        "edited": edited,
        "source_dims_mm": list(dims),
        "yaw_deg": yaw_deg,
        "pitch_deg": pitch_deg,
        "angle_deg": angle_deg,
        "operation": op,
        "metrics": metrics(edited),
    }


def add_feature(doc, name, revision):
    op = revision["operation"]
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = revision["edited"]
    obj.addProperty("App::PropertyString", "OLE_ID", "OLEANDER")
    obj.OLE_ID = "OLE_FULL3D_FACE_ROTATE::" + name
    obj.addProperty("App::PropertyString", "OLE_Operation", "OLEANDER")
    obj.OLE_Operation = op["operation"]
    obj.addProperty("App::PropertyString", "OLE_Selector", "OLEANDER")
    obj.OLE_Selector = op["selector_id"]
    obj.addProperty("App::PropertyString", "OLE_AxisID", "OLEANDER")
    obj.OLE_AxisID = op["axis_id"]
    obj.addProperty("App::PropertyVector", "OLE_AxisWorldDirection", "OLEANDER")
    obj.OLE_AxisWorldDirection = vec(op["axis_world_direction"])
    obj.addProperty("App::PropertyFloat", "OLE_YawDeg", "OLEANDER")
    obj.OLE_YawDeg = revision["yaw_deg"]
    obj.addProperty("App::PropertyFloat", "OLE_PitchDeg", "OLEANDER")
    obj.OLE_PitchDeg = revision["pitch_deg"]
    obj.addProperty("App::PropertyFloat", "OLE_AngleDeg", "OLEANDER")
    obj.OLE_AngleDeg = revision["angle_deg"]
    obj.addProperty("App::PropertyString", "OLE_GeometryAuthority", "OLEANDER")
    obj.OLE_GeometryAuthority = "FREECAD_OCCT_BREP"
    return obj


def serializable_revision(revision):
    return {
        "source_dims_mm": revision["source_dims_mm"],
        "yaw_deg": revision["yaw_deg"],
        "pitch_deg": revision["pitch_deg"],
        "angle_deg": revision["angle_deg"],
        "operation": revision["operation"],
        "metrics": revision["metrics"],
    }


def display_record(name, revision, step_path):
    verts, facets = revision["edited"].tessellate(0.25)
    check(bool(verts) and bool(facets), "display_tessellation_" + name)
    op = revision["operation"]
    return {
        "revision": name,
        "ole_id": "OLE_FULL3D_FACE_ROTATE::" + name,
        "yaw_deg": revision["yaw_deg"],
        "pitch_deg": revision["pitch_deg"],
        "angle_deg": revision["angle_deg"],
        "selector_id": op["selector_id"],
        "axis_id": op["axis_id"],
        "selector_world_normal": op["selector_world_normal"],
        "axis_world_direction": op["axis_world_direction"],
        "actual_angle_deg": op["actual_angle_deg"],
        "expected_rotated_normal": op["expected_rotated_normal"],
        "bbox_mm": revision["metrics"]["bbox_mm"],
        "volume_mm3": revision["metrics"]["volume_mm3"],
        "vertices_mm": [[v.x, v.y, v.z] for v in verts],
        "triangles": [list(f) for f in facets],
        "source_step": step_path.name,
        "source_step_sha256": sha256(step_path),
    }


def main() -> None:
    revisions = {}
    for name, spec in REVISIONS.items():
        stage(name)
        revisions[name] = build_revision(name, spec["dims"], spec["yaw_deg"], spec["pitch_deg"], spec["angle_deg"])

    check(revisions["R001"]["operation"]["selector_id"] == revisions["R002"]["operation"]["selector_id"], "selector_id_stable_across_rebuild")
    check(revisions["R001"]["operation"]["axis_id"] == revisions["R002"]["operation"]["axis_id"], "axis_id_stable_across_rebuild")
    for name, revision in revisions.items():
        check(revision["metrics"]["solid_count"] == 1, "single_solid_" + name)
        check(revision["metrics"]["face_count"] == 6, "six_faces_" + name)
        check(close(revision["operation"]["actual_angle_deg"], revision["angle_deg"], 1e-6), "signed_angle_" + name)
        check(is_full3d_direction(vec(revision["operation"]["selector_world_normal"])), "full3d_normal_" + name)
        check(is_full3d_direction(vec(revision["operation"]["axis_world_direction"])), "full3d_axis_" + name)

    stage("EXPECTED_FAILURES")
    base = revisions["R002"]["source"]
    normal = transformed_local_axis(App.Vector(1, 0, 0), REVISIONS["R002"]["yaw_deg"], REVISIONS["R002"]["pitch_deg"])
    good_axis = transformed_local_axis(App.Vector(0, 1, 0), REVISIONS["R002"]["yaw_deg"], REVISIONS["R002"]["pitch_deg"])
    failures = {}
    for label, axis, angle, needle in [
        ("zero_angle", good_axis, 0.0, "non-zero"),
        ("excessive_angle", good_axis, 15.0, "bounded angular contract"),
        ("axis_has_normal_component", normal, 4.0, "tangent plane"),
    ]:
        state = "FAIL"
        try:
            rotate_full3d_face(base, normal, axis, angle)
        except ValueError as exc:
            if needle in str(exc):
                state = "PASS"
                checks.append("expected_failure_" + label)
        check(state == "PASS", "failure_gate_" + label)
        failures[label] = state

    selector_miss = "FAIL"
    wrong_normal = transformed_local_axis(App.Vector(1, 0, 0), REVISIONS["R002"]["yaw_deg"] + 10.0, REVISIONS["R002"]["pitch_deg"])
    wrong_axis = transformed_local_axis(App.Vector(0, 1, 0), REVISIONS["R002"]["yaw_deg"] + 10.0, REVISIONS["R002"]["pitch_deg"])
    try:
        rotate_full3d_face(base, wrong_normal, wrong_axis, 4.0)
    except AssertionError as exc:
        if "semantic_face_selector_unique" in str(exc):
            selector_miss = "PASS"
            checks.append("expected_failure_selector_miss")
    check(selector_miss == "PASS", "failure_gate_selector_miss")
    failures["selector_miss"] = selector_miss

    stage("FCSTD_WRITE")
    doc = App.newDocument("OLEANDER_FULL3D_FACE_ROTATE")
    obj_r1 = add_feature(doc, "R001", revisions["R001"])
    obj_r2 = add_feature(doc, "R002", revisions["R002"])
    doc.recompute()
    doc.saveAs(str(FCSTD))
    obj_r1.Shape.exportStep(str(STEP_R001))
    obj_r2.Shape.exportStep(str(STEP_R002))
    check(FCSTD.exists() and STEP_R001.exists() and STEP_R002.exists(), "native_artifacts_written")

    stage("FCSTD_REOPEN")
    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(FCSTD))
    for name in ("R001", "R002"):
        obj = reopened.getObject(name)
        revision = revisions[name]
        check(obj is not None, "reopen_object_" + name)
        check(obj.OLE_ID == "OLE_FULL3D_FACE_ROTATE::" + name, "reopen_ole_id_" + name)
        check(obj.OLE_Selector == "SELECTOR::LOCAL_POS_X_FACE", "reopen_selector_" + name)
        check(obj.OLE_AxisID == "AXIS::SELECTED_FACE_CENTER::LOCAL_POS_Y", "reopen_axis_id_" + name)
        check(close(float(obj.OLE_YawDeg), revision["yaw_deg"]), "reopen_yaw_" + name)
        check(close(float(obj.OLE_PitchDeg), revision["pitch_deg"]), "reopen_pitch_" + name)
        check(close(float(obj.OLE_AngleDeg), revision["angle_deg"]), "reopen_angle_" + name)
        check((obj.OLE_AxisWorldDirection - vec(revision["operation"]["axis_world_direction"])).Length <= 1e-6, "reopen_axis_direction_" + name)
        check(obj.OLE_GeometryAuthority == "FREECAD_OCCT_BREP", "reopen_authority_" + name)
        check(obj.Shape.isValid() and len(obj.Shape.Solids) == 1, "reopen_solid_" + name)
    App.closeDocument(reopened.Name)

    stage("DISPLAY")
    display = {
        "schema": "OLEANDER_FULL3D_FACE_ROTATE_DISPLAY_v0.1",
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_OCCT_BREP",
        "display_authority": "DISPLAY_DERIVATIVE_ONLY",
        "units": "mm",
        "angle_units": "deg",
        "source_fcstd": FCSTD.name,
        "source_fcstd_sha256": sha256(FCSTD),
        "revisions": [
            display_record("R001", revisions["R001"], STEP_R001),
            display_record("R002", revisions["R002"], STEP_R002),
        ],
    }
    DISPLAY.write_text(json.dumps(display, indent=2, sort_keys=True), encoding="utf-8")

    manifest = {
        "schema": "OLEANDER_FREECAD_FULL3D_FACE_ROTATE_v0.1",
        "status": "PASS",
        "units": "mm",
        "angle_units": "deg",
        "authority": {"geometry_master": "FREECAD_OCCT_BREP", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "selector": "semantic local +X planar face after yaw+pitch transform",
        "axis": "selected-face center transformed local +Y tangent axis with XYZ components",
        "operation": "full-3D-oriented planar face signed local-axis rotation through BRepTools_ReShape",
        "R001": serializable_revision(revisions["R001"]),
        "R002": serializable_revision(revisions["R002"]),
        "expected_failure_cases": failures,
        "artifacts": {
            "fcstd": {"path": FCSTD.name, "sha256": sha256(FCSTD)},
            "step_R001": {"path": STEP_R001.name, "sha256": sha256(STEP_R001)},
            "step_R002": {"path": STEP_R002.name, "sha256": sha256(STEP_R002)},
            "display": {"path": DISPLAY.name, "sha256": sha256(DISPLAY)},
        },
        "checks": checks,
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "general_face_rotate",
            "arbitrary_user_defined_rotation_axis",
            "nonplanar_face_rotate",
            "persistent_topological_naming",
            "production_direct_modeling_parity"
        ]
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    stage("PASS")
    print("OLEANDER_FREECAD_FULL3D_FACE_ROTATE=" + json.dumps(manifest, sort_keys=True), flush=True)


if __name__ == "__main__":
    stage("START")
    try:
        main()
    except BaseException as exc:
        print("OLEANDER_FULL3D_FACE_ROTATE_EXCEPTION=" + repr(exc), flush=True)
        traceback.print_exc()
        raise
