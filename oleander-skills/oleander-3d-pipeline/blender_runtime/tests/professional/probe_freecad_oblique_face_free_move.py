"""OLEANDER bounded oblique planar-face free translation through BRep ReShape.

Combines normal and tangent components into one selected-face translation. The
semantic local +X face of a yawed rectangular B-Rep is resolved from its world
normal, translated by a governed 3D vector, and rebuilt with its four adjacent
faces. This approximates one bounded direct face-drag primitive while keeping
FreeCAD/OCCT authoritative and Blender display-only.

This does not prove general face move, nonplanar editing, topology naming, or
production direct-modeling parity.
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

OUT = Path(os.environ.get("OLEANDER_OBLIQUE_FACE_FREE_MOVE_DIR", "/tmp/oleander-oblique-face-free-move"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_oblique_face_free_move.FCStd"
STEP_R001 = OUT / "oleander_oblique_face_free_move_R001.step"
STEP_R002 = OUT / "oleander_oblique_face_free_move_R002.step"
DISPLAY = OUT / "oleander_oblique_face_free_move_display.json"
MANIFEST = OUT / "oleander_oblique_face_free_move_manifest.json"
TOL = 1e-6
checks: list[str] = []

REVISIONS = {
    "R001": {"dims": (80.0, 50.0, 10.0), "yaw_deg": 30.0, "normal_mm": 2.0},
    "R002": {"dims": (100.0, 60.0, 12.0), "yaw_deg": -25.0, "normal_mm": -2.0},
}


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def stage(label: str) -> None:
    print("OLEANDER_OBLIQUE_FACE_FREE_MOVE_STAGE=" + label, flush=True)


def vec(values):
    if hasattr(values, "x") and hasattr(values, "y") and hasattr(values, "z"):
        return App.Vector(float(values.x), float(values.y), float(values.z))
    return App.Vector(float(values[0]), float(values[1]), float(values[2]))


def unit(values):
    r = vec(values)
    if r.Length <= TOL:
        raise ValueError("vector must be non-zero")
    r.normalize()
    return r


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


def local_pos_x_world_normal(yaw_deg: float):
    a = math.radians(yaw_deg)
    return App.Vector(math.cos(a), math.sin(a), 0.0)


def local_pos_y_world_tangent(yaw_deg: float):
    a = math.radians(yaw_deg)
    return App.Vector(-math.sin(a), math.cos(a), 0.0)


def governed_delta(yaw_deg: float, normal_mm: float):
    n = local_pos_x_world_normal(yaw_deg)
    ty = local_pos_y_world_tangent(yaw_deg)
    return n * normal_mm + ty * 3.0 + App.Vector(0.0, 0.0, 4.0)


def is_world_axis_aligned(v):
    values = [abs(v.x), abs(v.y), abs(v.z)]
    return max(values) > 0.999999 and sum(x > 1e-6 for x in values) == 1


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


def free_move_face(shape, selector_normal, delta):
    check(shape.isValid() and len(shape.Solids) == 1, "input_valid_single_solid")
    n = unit(selector_normal)
    d = vec(delta)
    check(not is_world_axis_aligned(n), "selector_normal_oblique_to_world_axes")
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

    target = select_face_by_normal(shape, n)
    opposite = select_face_by_normal(shape, -n)
    old_points = ordered_points(target)
    new_points = [p + d for p in old_points]
    target_center_before = target.CenterOfMass
    opposite_center_before = opposite.CenterOfMass
    opposite_area_before = opposite.Area
    target_area = target.Area
    new_target = make_oriented_face(new_points, n)
    check(face_normal(new_target).dot(n) > 0.999999, "target_plane_normal_preserved")
    check((new_target.CenterOfMass - (target_center_before + d)).Length <= 1e-5, "target_center_moved_by_full_vector")
    check(close(new_target.Area, target_area, 1e-5), "target_area_preserved")

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

    expected_volume = shape.Volume + normal_component * target_area
    check(close(edited.Volume, expected_volume, 1e-3), "volume_matches_normal_component_times_face_area")
    opposite_after = select_face_by_normal(edited, -n)
    check((opposite_after.CenterOfMass - opposite_center_before).Length <= 1e-5, "opposite_center_preserved")
    check(close(opposite_after.Area, opposite_area_before, 1e-5), "opposite_area_preserved")

    return edited, {
        "selector_id": "SELECTOR::LOCAL_POS_X_FACE",
        "selector_world_normal": [n.x, n.y, n.z],
        "move_world_mm": [d.x, d.y, d.z],
        "move_distance_mm": d.Length,
        "normal_component_mm": normal_component,
        "tangent_component_world_mm": [tangent.x, tangent.y, tangent.z],
        "tangent_distance_mm": tangent.Length,
        "source_face_area_mm2": target_area,
        "expected_volume_mm3": expected_volume,
        "operation": "BRepTools_ReShape_OBLIQUE_PLANAR_FACE_FREE_TRANSLATE",
        "replaced_face_count": 5,
        "opposite_face_untouched": True,
    }


def build_revision(name, dims, yaw_deg, normal_mm):
    source = Part.makeBox(*dims)
    source.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), yaw_deg)
    n = local_pos_x_world_normal(yaw_deg)
    d = governed_delta(yaw_deg, normal_mm)
    edited, op = free_move_face(source, n, d)
    return {
        "source": source,
        "edited": edited,
        "source_dims_mm": list(dims),
        "yaw_deg": yaw_deg,
        "normal_mm": normal_mm,
        "operation": op,
        "metrics": metrics(edited),
    }


def add_feature(doc, name, revision):
    op = revision["operation"]
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = revision["edited"]
    obj.addProperty("App::PropertyString", "OLE_ID", "OLEANDER")
    obj.OLE_ID = "OLE_OBLIQUE_FACE_FREE_MOVE::" + name
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
    obj.addProperty("App::PropertyString", "OLE_GeometryAuthority", "OLEANDER")
    obj.OLE_GeometryAuthority = "FREECAD_OCCT_BREP"
    return obj


def serializable_revision(revision):
    return {
        "source_dims_mm": revision["source_dims_mm"],
        "yaw_deg": revision["yaw_deg"],
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
        "ole_id": "OLE_OBLIQUE_FACE_FREE_MOVE::" + name,
        "yaw_deg": revision["yaw_deg"],
        "selector_id": op["selector_id"],
        "selector_world_normal": op["selector_world_normal"],
        "move_world_mm": op["move_world_mm"],
        "move_distance_mm": op["move_distance_mm"],
        "normal_component_mm": op["normal_component_mm"],
        "tangent_component_world_mm": op["tangent_component_world_mm"],
        "tangent_distance_mm": op["tangent_distance_mm"],
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
        revisions[name] = build_revision(name, spec["dims"], spec["yaw_deg"], spec["normal_mm"])

    check(revisions["R001"]["operation"]["selector_id"] == revisions["R002"]["operation"]["selector_id"], "selector_id_stable_across_rebuild")
    check(revisions["R001"]["operation"]["normal_component_mm"] > 0, "r1_outward_normal_component")
    check(revisions["R002"]["operation"]["normal_component_mm"] < 0, "r2_inward_normal_component")
    for name, revision in revisions.items():
        check(revision["metrics"]["solid_count"] == 1, "single_solid_" + name)
        check(revision["metrics"]["face_count"] == 6, "six_faces_" + name)
        check(close(revision["metrics"]["volume_mm3"], revision["operation"]["expected_volume_mm3"], 1e-3), "expected_volume_" + name)

    stage("EXPECTED_FAILURES")
    base = revisions["R002"]["source"]
    n = local_pos_x_world_normal(REVISIONS["R002"]["yaw_deg"])
    tangent = local_pos_y_world_tangent(REVISIONS["R002"]["yaw_deg"])
    failures = {}
    for label, delta, needle in [
        ("zero", App.Vector(0, 0, 0), "non-zero"),
        ("excessive_magnitude", tangent * 21.0, "magnitude contract"),
        ("excessive_normal_component", n * 9.0 + tangent * 1.0, "normal component"),
    ]:
        state = "FAIL"
        try:
            free_move_face(base, n, delta)
        except ValueError as exc:
            if needle in str(exc):
                state = "PASS"
                checks.append("expected_failure_" + label)
        check(state == "PASS", "failure_gate_" + label)
        failures[label] = state

    selector_miss = "FAIL"
    wrong_n = local_pos_x_world_normal(REVISIONS["R002"]["yaw_deg"] + 11.0)
    try:
        free_move_face(base, wrong_n, governed_delta(REVISIONS["R002"]["yaw_deg"] + 11.0, 2.0))
    except AssertionError as exc:
        if "semantic_face_selector_unique" in str(exc):
            selector_miss = "PASS"
            checks.append("expected_failure_selector_miss")
    check(selector_miss == "PASS", "failure_gate_selector_miss")
    failures["selector_miss"] = selector_miss

    stage("FCSTD_WRITE")
    doc = App.newDocument("OLEANDER_OBLIQUE_FACE_FREE_MOVE")
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
        check(obj.OLE_ID == "OLE_OBLIQUE_FACE_FREE_MOVE::" + name, "reopen_ole_id_" + name)
        check(obj.OLE_Selector == "SELECTOR::LOCAL_POS_X_FACE", "reopen_selector_" + name)
        check((obj.OLE_MoveWorldMM - vec(revision["operation"]["move_world_mm"])).Length <= 1e-6, "reopen_move_" + name)
        check(close(float(obj.OLE_NormalComponentMM), revision["operation"]["normal_component_mm"]), "reopen_normal_component_" + name)
        check(close(float(obj.OLE_YawDeg), revision["yaw_deg"]), "reopen_yaw_" + name)
        check(obj.OLE_GeometryAuthority == "FREECAD_OCCT_BREP", "reopen_authority_" + name)
        check(obj.Shape.isValid() and len(obj.Shape.Solids) == 1, "reopen_solid_" + name)
    App.closeDocument(reopened.Name)

    stage("DISPLAY")
    display = {
        "schema": "OLEANDER_OBLIQUE_FACE_FREE_MOVE_DISPLAY_v0.1",
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_OCCT_BREP",
        "display_authority": "DISPLAY_DERIVATIVE_ONLY",
        "units": "mm",
        "source_fcstd": FCSTD.name,
        "source_fcstd_sha256": sha256(FCSTD),
        "revisions": [
            display_record("R001", revisions["R001"], STEP_R001),
            display_record("R002", revisions["R002"], STEP_R002),
        ],
    }
    DISPLAY.write_text(json.dumps(display, indent=2, sort_keys=True), encoding="utf-8")

    manifest = {
        "schema": "OLEANDER_FREECAD_OBLIQUE_FACE_FREE_MOVE_v0.1",
        "status": "PASS",
        "units": "mm",
        "authority": {"geometry_master": "FREECAD_OCCT_BREP", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "selector": "semantic local +X planar face re-resolved from yaw-transformed world normal",
        "operation": "combined normal+tangent selected-face translation through BRepTools_ReShape",
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
            "general_face_move",
            "arbitrary_full_3d_face_orientation",
            "nonplanar_face_move",
            "persistent_topological_naming",
            "production_direct_modeling_parity"
        ]
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    stage("PASS")
    print("OLEANDER_FREECAD_OBLIQUE_FACE_FREE_MOVE=" + json.dumps(manifest, sort_keys=True), flush=True)


if __name__ == "__main__":
    stage("START")
    try:
        main()
    except BaseException as exc:
        print("OLEANDER_OBLIQUE_FACE_FREE_MOVE_EXCEPTION=" + repr(exc), flush=True)
        traceback.print_exc()
        raise
