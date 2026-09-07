"""OLEANDER bounded full-3D-oriented planar face free-move through BRep ReShape.

A rectangular FreeCAD/OCCT solid is yawed around world Z and pitched around
world Y. The semantic local +X face is therefore fully oblique in XYZ. One
selected-face move combines a signed normal component with two transformed
local tangent components. Target + four adjacent faces are rebuilt through
BRepTools_ReShape; the opposite face remains untouched.

Bounded proof only. This is not nonplanar/general face move, persistent
Topological Naming, or P0-B professional parity.
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

OUT = Path(os.environ.get("OLEANDER_FULL3D_FACE_FREE_MOVE_DIR", "/tmp/oleander-full3d-face-free-move"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_full3d_face_free_move.FCStd"
STEP_R001 = OUT / "oleander_full3d_face_free_move_R001.step"
STEP_R002 = OUT / "oleander_full3d_face_free_move_R002.step"
DISPLAY = OUT / "oleander_full3d_face_free_move_display.json"
MANIFEST = OUT / "oleander_full3d_face_free_move_manifest.json"
TOL = 1e-6
checks: list[str] = []

REVISIONS = {
    "R001": {"dims": (80.0, 50.0, 10.0), "yaw_deg": 30.0, "pitch_deg": 20.0, "normal_mm": 2.0},
    "R002": {"dims": (100.0, 60.0, 12.0), "yaw_deg": -25.0, "pitch_deg": -15.0, "normal_mm": -2.0},
}


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def stage(label: str) -> None:
    print("OLEANDER_FULL3D_FACE_FREE_MOVE_STAGE=" + label, flush=True)


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


def is_full3d(v):
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


def governed_move(yaw_deg: float, pitch_deg: float, normal_mm: float):
    n = transformed_local_axis(App.Vector(1, 0, 0), yaw_deg, pitch_deg)
    ty = transformed_local_axis(App.Vector(0, 1, 0), yaw_deg, pitch_deg)
    tz = transformed_local_axis(App.Vector(0, 0, 1), yaw_deg, pitch_deg)
    tangent = ty * 3.0 + tz * 4.0
    check(close(tangent.Length, 5.0, 1e-9), "governed_tangent_3_4_5")
    check(abs(tangent.dot(n)) <= 1e-9, "governed_tangent_orthogonal_to_normal")
    return n * normal_mm + tangent, ty, tz


def free_move_full3d_face(shape, selector_normal, move):
    check(shape.isValid() and len(shape.Solids) == 1, "input_valid_single_solid")
    n = unit(selector_normal)
    d = vec(move)
    check(is_full3d(n), "selector_normal_has_xyz_components")
    if not all(math.isfinite(x) for x in (d.x, d.y, d.z)):
        raise ValueError("move components must be finite")
    if d.Length < 1e-9:
        raise ValueError("move must be non-zero")
    if d.Length > 20.0:
        raise ValueError("move exceeds bounded magnitude contract")
    normal_component = d.dot(n)
    if abs(normal_component) > 8.0:
        raise ValueError("normal component exceeds bounded face-drag contract")
    tangent = d - n * normal_component
    check(tangent.Length > 1e-6, "combined_move_contains_tangent_component")
    check(abs(normal_component) > 1e-6, "combined_move_contains_normal_component")
    check(abs(tangent.dot(n)) <= 1e-7, "decomposed_tangent_orthogonal")

    target = select_face_by_normal(shape, n)
    opposite = select_face_by_normal(shape, -n)
    old_points = ordered_points(target)
    new_points = [p + d for p in old_points]
    old_center = target.CenterOfMass
    opposite_center = opposite.CenterOfMass
    opposite_area = opposite.Area
    area = target.Area
    new_target = make_oriented_face(new_points, n)
    check(face_normal(new_target).dot(n) > 0.999999, "target_normal_preserved")
    check((new_target.CenterOfMass - (old_center + d)).Length <= 1e-5, "target_center_moved_by_full_vector")
    check(close(new_target.Area, area, 1e-5), "target_area_preserved")

    replacements = [(target, new_target)]
    adjacent_count = 0
    for face in shape.Faces:
        if face.isSame(target) or face.isSame(opposite):
            continue
        points = ordered_points(face)
        flags = [any(same_point(p, tp) for tp in old_points) for p in points]
        shared = sum(1 for flag in flags if flag)
        if shared == 0:
            continue
        check(shared == 2, "adjacent_face_shares_target_edge")
        rebuilt_points = [p + d if flag else p for p, flag in zip(points, flags)]
        rebuilt = make_oriented_face(rebuilt_points, face_normal(face))
        replacements.append((face, rebuilt))
        adjacent_count += 1
    check(adjacent_count == 4, "four_adjacent_faces_rebuilt")

    reshaped = shape.replaceShape(replacements)
    check(not reshaped.isNull(), "reshape_non_null")
    check(len(reshaped.Faces) == 6, "reshape_six_faces")
    edited = normalize_reshape_output(reshaped)
    check(edited.isValid() and len(edited.Solids) == 1, "edited_valid_single_solid")
    expected_volume = shape.Volume + normal_component * area
    check(close(edited.Volume, expected_volume, 1e-3), "volume_matches_signed_normal_displacement")
    opposite_after = select_face_by_normal(edited, -n)
    check((opposite_after.CenterOfMass - opposite_center).Length <= 1e-5, "opposite_center_preserved")
    check(close(opposite_after.Area, opposite_area, 1e-5), "opposite_area_preserved")
    moved_after = select_face_by_normal(edited, n)
    check(face_normal(moved_after).dot(n) > 0.999999, "moved_face_reselectable")

    return edited, {
        "selector_id": "SELECTOR::LOCAL_POS_X_FACE",
        "selector_world_normal": [n.x, n.y, n.z],
        "move_world_mm": [d.x, d.y, d.z],
        "move_distance_mm": d.Length,
        "normal_component_mm": normal_component,
        "tangent_component_world_mm": [tangent.x, tangent.y, tangent.z],
        "tangent_distance_mm": tangent.Length,
        "source_face_area_mm2": area,
        "expected_volume_mm3": expected_volume,
        "operation": "BRepTools_ReShape_FULL3D_PLANAR_FACE_FREE_TRANSLATE",
        "replaced_face_count": 5,
        "opposite_face_untouched": True,
    }


def build_revision(name, dims, yaw_deg, pitch_deg, normal_mm):
    source = Part.makeBox(*dims)
    source.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), yaw_deg)
    source.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), pitch_deg)
    n = transformed_local_axis(App.Vector(1, 0, 0), yaw_deg, pitch_deg)
    move, ty, tz = governed_move(yaw_deg, pitch_deg, normal_mm)
    check(is_full3d(n), "full3d_normal_" + name)
    check(is_full3d(move), "full3d_move_vector_" + name)
    edited, op = free_move_full3d_face(source, n, move)
    op["local_y_world_direction"] = [ty.x, ty.y, ty.z]
    op["local_z_world_direction"] = [tz.x, tz.y, tz.z]
    return {
        "source": source,
        "edited": edited,
        "source_dims_mm": list(dims),
        "yaw_deg": yaw_deg,
        "pitch_deg": pitch_deg,
        "normal_mm": normal_mm,
        "operation": op,
        "metrics": metrics(edited),
    }


def add_feature(doc, name, revision):
    op = revision["operation"]
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = revision["edited"]
    obj.addProperty("App::PropertyString", "OLE_ID", "OLEANDER")
    obj.OLE_ID = "OLE_FULL3D_FACE_FREE_MOVE::" + name
    obj.addProperty("App::PropertyString", "OLE_Operation", "OLEANDER")
    obj.OLE_Operation = op["operation"]
    obj.addProperty("App::PropertyString", "OLE_Selector", "OLEANDER")
    obj.OLE_Selector = op["selector_id"]
    obj.addProperty("App::PropertyVector", "OLE_MoveWorldMM", "OLEANDER")
    obj.OLE_MoveWorldMM = vec(op["move_world_mm"])
    obj.addProperty("App::PropertyFloat", "OLE_NormalComponentMM", "OLEANDER")
    obj.OLE_NormalComponentMM = op["normal_component_mm"]
    obj.addProperty("App::PropertyFloat", "OLE_YawDeg", "OLEANDER")
    obj.OLE_YawDeg = revision["yaw_deg"]
    obj.addProperty("App::PropertyFloat", "OLE_PitchDeg", "OLEANDER")
    obj.OLE_PitchDeg = revision["pitch_deg"]
    obj.addProperty("App::PropertyString", "OLE_GeometryAuthority", "OLEANDER")
    obj.OLE_GeometryAuthority = "FREECAD_OCCT_BREP"
    return obj


def serializable_revision(revision):
    return {
        "source_dims_mm": revision["source_dims_mm"],
        "yaw_deg": revision["yaw_deg"],
        "pitch_deg": revision["pitch_deg"],
        "normal_mm": revision["normal_mm"],
        "operation": revision["operation"],
        "metrics": revision["metrics"],
    }


def display_record(name, revision, step_path):
    verts, facets = revision["edited"].tessellate(0.25)
    check(bool(verts) and bool(facets), "display_tessellation_" + name)
    op = revision["operation"]
    return {
        "revision": name,
        "ole_id": "OLE_FULL3D_FACE_FREE_MOVE::" + name,
        "yaw_deg": revision["yaw_deg"],
        "pitch_deg": revision["pitch_deg"],
        "selector_id": op["selector_id"],
        "selector_world_normal": op["selector_world_normal"],
        "move_world_mm": op["move_world_mm"],
        "move_distance_mm": op["move_distance_mm"],
        "normal_component_mm": op["normal_component_mm"],
        "tangent_component_world_mm": op["tangent_component_world_mm"],
        "tangent_distance_mm": op["tangent_distance_mm"],
        "local_y_world_direction": op["local_y_world_direction"],
        "local_z_world_direction": op["local_z_world_direction"],
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
        revisions[name] = build_revision(name, spec["dims"], spec["yaw_deg"], spec["pitch_deg"], spec["normal_mm"])

    check(revisions["R001"]["operation"]["selector_id"] == revisions["R002"]["operation"]["selector_id"], "selector_id_stable_across_rebuild")
    check(revisions["R001"]["operation"]["normal_component_mm"] > 0, "r1_outward_normal_component")
    check(revisions["R002"]["operation"]["normal_component_mm"] < 0, "r2_inward_normal_component")
    for name, revision in revisions.items():
        check(revision["metrics"]["solid_count"] == 1, "single_solid_" + name)
        check(revision["metrics"]["face_count"] == 6, "six_faces_" + name)
        check(close(revision["metrics"]["volume_mm3"], revision["operation"]["expected_volume_mm3"], 1e-3), "expected_volume_" + name)
        check(is_full3d(vec(revision["operation"]["selector_world_normal"])), "selector_xyz_" + name)
        check(is_full3d(vec(revision["operation"]["move_world_mm"])), "move_xyz_" + name)

    stage("EXPECTED_FAILURES")
    base = revisions["R002"]["source"]
    n = transformed_local_axis(App.Vector(1, 0, 0), REVISIONS["R002"]["yaw_deg"], REVISIONS["R002"]["pitch_deg"])
    ty = transformed_local_axis(App.Vector(0, 1, 0), REVISIONS["R002"]["yaw_deg"], REVISIONS["R002"]["pitch_deg"])
    failures = {}
    for label, move, needle in [
        ("zero", App.Vector(0, 0, 0), "non-zero"),
        ("excessive_magnitude", ty * 21.0, "magnitude contract"),
        ("excessive_normal_component", n * 9.0 + ty, "normal component"),
    ]:
        state = "FAIL"
        try:
            free_move_full3d_face(base, n, move)
        except ValueError as exc:
            if needle in str(exc):
                state = "PASS"
                checks.append("expected_failure_" + label)
        check(state == "PASS", "failure_gate_" + label)
        failures[label] = state

    selector_miss = "FAIL"
    wrong_n = transformed_local_axis(App.Vector(1, 0, 0), REVISIONS["R002"]["yaw_deg"] + 10.0, REVISIONS["R002"]["pitch_deg"])
    wrong_move, _, _ = governed_move(REVISIONS["R002"]["yaw_deg"] + 10.0, REVISIONS["R002"]["pitch_deg"], 2.0)
    try:
        free_move_full3d_face(base, wrong_n, wrong_move)
    except AssertionError as exc:
        if "semantic_face_selector_unique" in str(exc):
            selector_miss = "PASS"
            checks.append("expected_failure_selector_miss")
    check(selector_miss == "PASS", "failure_gate_selector_miss")
    failures["selector_miss"] = selector_miss

    stage("FCSTD_WRITE")
    doc = App.newDocument("OLEANDER_FULL3D_FACE_FREE_MOVE")
    r1 = add_feature(doc, "R001", revisions["R001"])
    r2 = add_feature(doc, "R002", revisions["R002"])
    doc.recompute()
    doc.saveAs(str(FCSTD))
    r1.Shape.exportStep(str(STEP_R001))
    r2.Shape.exportStep(str(STEP_R002))
    check(FCSTD.exists() and STEP_R001.exists() and STEP_R002.exists(), "native_artifacts_written")

    stage("FCSTD_REOPEN")
    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(FCSTD))
    for name in ("R001", "R002"):
        obj = reopened.getObject(name)
        revision = revisions[name]
        check(obj is not None, "reopen_object_" + name)
        check(obj.OLE_ID == "OLE_FULL3D_FACE_FREE_MOVE::" + name, "reopen_ole_id_" + name)
        check(obj.OLE_Selector == "SELECTOR::LOCAL_POS_X_FACE", "reopen_selector_" + name)
        check((obj.OLE_MoveWorldMM - vec(revision["operation"]["move_world_mm"])).Length <= 1e-6, "reopen_move_" + name)
        check(close(float(obj.OLE_NormalComponentMM), revision["operation"]["normal_component_mm"]), "reopen_normal_component_" + name)
        check(close(float(obj.OLE_YawDeg), revision["yaw_deg"]), "reopen_yaw_" + name)
        check(close(float(obj.OLE_PitchDeg), revision["pitch_deg"]), "reopen_pitch_" + name)
        check(obj.OLE_GeometryAuthority == "FREECAD_OCCT_BREP", "reopen_authority_" + name)
        check(obj.Shape.isValid() and len(obj.Shape.Solids) == 1, "reopen_solid_" + name)
    App.closeDocument(reopened.Name)

    stage("DISPLAY")
    display = {
        "schema": "OLEANDER_FULL3D_FACE_FREE_MOVE_DISPLAY_v0.1",
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_OCCT_BREP",
        "display_authority": "DISPLAY_DERIVATIVE_ONLY",
        "units": "mm",
        "source_fcstd": FCSTD.name,
        "source_fcstd_sha256": sha256(FCSTD),
        "revisions": [display_record("R001", revisions["R001"], STEP_R001), display_record("R002", revisions["R002"], STEP_R002)],
    }
    DISPLAY.write_text(json.dumps(display, indent=2, sort_keys=True), encoding="utf-8")

    manifest = {
        "schema": "OLEANDER_FREECAD_FULL3D_FACE_FREE_MOVE_v0.1",
        "status": "PASS",
        "units": "mm",
        "authority": {"geometry_master": "FREECAD_OCCT_BREP", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "selector": "semantic local +X planar face after yaw+pitch transform",
        "operation": "full-3D-oriented combined normal+tangent selected-face translation through BRepTools_ReShape",
        "R001": serializable_revision(revisions["R001"]),
        "R002": serializable_revision(revisions["R002"]),
        "expected_failure_cases": failures,
        "artifacts": {
            "fcstd": {"path": FCSTD.name, "sha256": sha256(FCSTD)},
            "step_R001": {"path": STEP_R001.name, "sha256": sha256(STEP_R001)},
            "step_R002": {"path": STEP_R002.name, "sha256": sha256(STEP_R002)},
            "display": {"path": DISPLAY.name, "sha256": sha256(DISPLAY)}
        },
        "checks": checks,
        "non_claims": ["P0_B_DIRECT_BREP_PASS", "general_face_move", "nonplanar_face_move", "persistent_topological_naming", "production_direct_modeling_parity"]
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    stage("PASS")
    print("OLEANDER_FREECAD_FULL3D_FACE_FREE_MOVE=" + json.dumps(manifest, sort_keys=True), flush=True)


if __name__ == "__main__":
    stage("START")
    try:
        main()
    except BaseException as exc:
        print("OLEANDER_FULL3D_FACE_FREE_MOVE_EXCEPTION=" + repr(exc), flush=True)
        traceback.print_exc()
        raise
