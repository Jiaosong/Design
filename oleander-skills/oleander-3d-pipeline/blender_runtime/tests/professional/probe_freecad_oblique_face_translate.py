"""OLEANDER bounded oblique planar-face tangential translation probe.

A rectangular FreeCAD/OCCT B-Rep is rotated about world Z so its semantic local
+X face no longer aligns with any world principal axis. The face is re-resolved
from its transformed world normal and translated strictly inside its own tangent
plane. The target and four adjacent faces are replaced through BRep ReShape.

This validates a bounded oblique-planar case only. It does not prove arbitrary
3D orientation, nonplanar editing, persistent topological naming, or P0-B parity.
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

OUT = Path(os.environ.get("OLEANDER_OBLIQUE_FACE_TRANSLATE_DIR", "/tmp/oleander-oblique-face-translate"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_oblique_face_translate.FCStd"
STEP_R001 = OUT / "oleander_oblique_face_translate_R001.step"
STEP_R002 = OUT / "oleander_oblique_face_translate_R002.step"
DISPLAY = OUT / "oleander_oblique_face_translate_display.json"
MANIFEST = OUT / "oleander_oblique_face_translate_manifest.json"
TOL = 1e-6
checks: list[str] = []

REVISIONS = {
    "R001": {"dims": (80.0, 50.0, 10.0), "yaw_deg": 30.0},
    "R002": {"dims": (100.0, 60.0, 12.0), "yaw_deg": -25.0},
}


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def stage(label: str) -> None:
    print("OLEANDER_OBLIQUE_FACE_TRANSLATE_STAGE=" + label, flush=True)


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
    found = []
    for face in shape.Faces:
        if face_normal(face).dot(expected) > 0.999999:
            found.append(face)
    check(len(found) == 1, "semantic_oblique_selector_unique")
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


def world_normal_for_local_pos_x(yaw_deg: float):
    angle = math.radians(yaw_deg)
    return App.Vector(math.cos(angle), math.sin(angle), 0.0)


def world_tangent_for_local_pos_y(yaw_deg: float):
    angle = math.radians(yaw_deg)
    return App.Vector(-math.sin(angle), math.cos(angle), 0.0)


def translation_for_revision(yaw_deg: float):
    tangent_y = world_tangent_for_local_pos_y(yaw_deg)
    return tangent_y * 4.0 + App.Vector(0.0, 0.0, 3.0)


def is_world_axis_aligned(n):
    values = [abs(n.x), abs(n.y), abs(n.z)]
    return max(values) > 0.999999 and sum(v > 1e-6 for v in values) == 1


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


def translate_oblique_face(shape, expected_normal, delta):
    check(shape.isValid() and len(shape.Solids) == 1, "input_valid_single_solid")
    n = unit(expected_normal)
    d = vec(delta)
    check(not is_world_axis_aligned(n), "selector_normal_is_oblique_to_world_axes")
    if not all(math.isfinite(v) for v in (d.x, d.y, d.z)):
        raise ValueError("translation components must be finite")
    if d.Length < 1e-9:
        raise ValueError("translation must be non-zero")
    if d.Length > 20.0:
        raise ValueError("translation exceeds bounded contract")
    if abs(d.dot(n)) > 1e-7:
        raise ValueError("translation must remain in selected face tangent plane")

    target = select_face_by_normal(shape, n)
    opposite = select_face_by_normal(shape, -n)
    target_normal_before = face_normal(target)
    target_pts = ordered_points(target)
    target_center_before = target.CenterOfMass
    opposite_center_before = opposite.CenterOfMass
    opposite_area_before = opposite.Area

    moved_target_pts = [p + d for p in target_pts]
    new_target = make_oriented_face(moved_target_pts, n)
    check((new_target.CenterOfMass - (target_center_before + d)).Length <= 1e-5, "target_center_translation_exact")
    check(close(new_target.Area, target.Area, 1e-5), "target_area_preserved")
    check(face_normal(new_target).dot(target_normal_before) > 0.999999, "target_plane_normal_preserved")

    replacements = [(target, new_target)]
    adjacent_count = 0
    for face in shape.Faces:
        if face.isSame(target) or face.isSame(opposite):
            continue
        points = ordered_points(face)
        on_target = [any(same_point(p, tp) for tp in target_pts) for p in points]
        shared = sum(1 for flag in on_target if flag)
        if shared == 0:
            continue
        check(shared == 2, "adjacent_face_shares_one_target_edge")
        rebuilt_points = [p + d if flag else p for p, flag in zip(points, on_target)]
        rebuilt = make_oriented_face(rebuilt_points, face_normal(face))
        replacements.append((face, rebuilt))
        adjacent_count += 1

    check(adjacent_count == 4, "four_adjacent_faces_rebuilt")
    check(len(replacements) == 5, "target_plus_four_replacements")
    reshaped = shape.replaceShape(replacements)
    check(not reshaped.isNull(), "reshape_non_null")
    check(len(reshaped.Faces) == 6, "reshape_six_faces")
    edited = normalize_reshape_output(reshaped)
    check(edited.isValid() and len(edited.Solids) == 1, "edited_valid_single_solid")
    check(close(edited.Volume, shape.Volume, 1e-4), "volume_preserved")

    opposite_after = select_face_by_normal(edited, -n)
    check((opposite_after.CenterOfMass - opposite_center_before).Length <= 1e-5, "opposite_center_preserved")
    check(close(opposite_after.Area, opposite_area_before, 1e-5), "opposite_area_preserved")

    return edited, {
        "selector_id": "SELECTOR::LOCAL_POS_X_FACE",
        "selector_world_normal": [n.x, n.y, n.z],
        "translation_world_mm": [d.x, d.y, d.z],
        "translation_distance_mm": d.Length,
        "tangent_dot_normal": d.dot(n),
        "operation": "BRepTools_ReShape_OBLIQUE_PLANAR_FACE_TANGENTIAL_TRANSLATE",
        "replaced_face_count": 5,
        "opposite_face_untouched": True,
        "target_center_before_mm": [target_center_before.x, target_center_before.y, target_center_before.z],
        "target_center_after_mm": [new_target.CenterOfMass.x, new_target.CenterOfMass.y, new_target.CenterOfMass.z],
        "target_normal_before": [target_normal_before.x, target_normal_before.y, target_normal_before.z],
        "target_normal_after": [face_normal(new_target).x, face_normal(new_target).y, face_normal(new_target).z],
    }


def build_revision(name, dims, yaw_deg):
    base = Part.makeBox(*dims)
    base.rotate(App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, 0.0, 1.0), yaw_deg)
    expected_normal = world_normal_for_local_pos_x(yaw_deg)
    delta = translation_for_revision(yaw_deg)
    check(abs(delta.Length - 5.0) <= 1e-9, "five_mm_translation_" + name)
    check(abs(delta.dot(expected_normal)) <= 1e-9, "tangent_translation_" + name)
    edited, operation = translate_oblique_face(base, expected_normal, delta)
    return {
        "base": base,
        "edited": edited,
        "operation": operation,
        "dims": list(dims),
        "yaw_deg": yaw_deg,
        "metrics": metrics(edited),
    }


def add_feature(doc, name, revision):
    op = revision["operation"]
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = revision["edited"]
    obj.addProperty("App::PropertyString", "OLE_ID", "OLEANDER")
    obj.OLE_ID = "OLE_OBLIQUE_FACE_TRANSLATE::" + name
    obj.addProperty("App::PropertyString", "OLE_Operation", "OLEANDER")
    obj.OLE_Operation = op["operation"]
    obj.addProperty("App::PropertyString", "OLE_Selector", "OLEANDER")
    obj.OLE_Selector = op["selector_id"]
    obj.addProperty("App::PropertyFloat", "OLE_YawDeg", "OLEANDER")
    obj.OLE_YawDeg = revision["yaw_deg"]
    obj.addProperty("App::PropertyVector", "OLE_SelectorWorldNormal", "OLEANDER")
    obj.OLE_SelectorWorldNormal = vec(op["selector_world_normal"])
    obj.addProperty("App::PropertyVector", "OLE_TranslationWorldMM", "OLEANDER")
    obj.OLE_TranslationWorldMM = vec(op["translation_world_mm"])
    obj.addProperty("App::PropertyString", "OLE_GeometryAuthority", "OLEANDER")
    obj.OLE_GeometryAuthority = "FREECAD_OCCT_BREP"
    return obj


def display_record(name, revision, step_path):
    verts, facets = revision["edited"].tessellate(0.25)
    check(bool(verts) and bool(facets), "display_tessellation_" + name)
    op = revision["operation"]
    return {
        "revision": name,
        "ole_id": "OLE_OBLIQUE_FACE_TRANSLATE::" + name,
        "yaw_deg": revision["yaw_deg"],
        "selector_id": op["selector_id"],
        "selector_world_normal": op["selector_world_normal"],
        "translation_world_mm": op["translation_world_mm"],
        "translation_distance_mm": op["translation_distance_mm"],
        "bbox_mm": revision["metrics"]["bbox_mm"],
        "volume_mm3": revision["metrics"]["volume_mm3"],
        "vertices_mm": [[v.x, v.y, v.z] for v in verts],
        "triangles": [list(f) for f in facets],
        "source_step": step_path.name,
        "source_step_sha256": sha256(step_path),
    }


def serializable_revision(revision):
    return {
        "source_dims_mm": revision["dims"],
        "yaw_deg": revision["yaw_deg"],
        "metrics": revision["metrics"],
        "operation": revision["operation"],
    }


def main() -> None:
    revisions = {}
    for name, spec in REVISIONS.items():
        stage(name)
        revisions[name] = build_revision(name, spec["dims"], spec["yaw_deg"])

    check(revisions["R001"]["operation"]["selector_id"] == revisions["R002"]["operation"]["selector_id"], "semantic_selector_id_stable_across_rotation_and_dimension_rebuild")
    for name, revision in revisions.items():
        check(revision["metrics"]["solid_count"] == 1, "single_solid_" + name)
        check(revision["metrics"]["face_count"] == 6, "six_faces_" + name)
        check(close(revision["metrics"]["volume_mm3"], revision["base"].Volume, 1e-4), "volume_matches_rotated_source_" + name)
        normal = vec(revision["operation"]["selector_world_normal"])
        check(not is_world_axis_aligned(normal), "oblique_normal_" + name)

    stage("EXPECTED_FAILURES")
    failures = {}
    base = revisions["R002"]["base"]
    n = world_normal_for_local_pos_x(REVISIONS["R002"]["yaw_deg"])
    for label, delta, needle in [
        ("zero", App.Vector(0, 0, 0), "non-zero"),
        ("normal_component", n * 2.0, "tangent plane"),
        ("excessive", translation_for_revision(REVISIONS["R002"]["yaw_deg"]) * 5.0, "bounded contract"),
    ]:
        state = "FAIL"
        try:
            translate_oblique_face(base, n, delta)
        except ValueError as exc:
            if needle in str(exc):
                state = "PASS"
                checks.append("expected_failure_" + label)
        check(state == "PASS", "failure_gate_" + label)
        failures[label] = state

    selector_miss = "FAIL"
    bad_n = world_normal_for_local_pos_x(REVISIONS["R002"]["yaw_deg"] + 10.0)
    try:
        translate_oblique_face(base, bad_n, translation_for_revision(REVISIONS["R002"]["yaw_deg"] + 10.0))
    except AssertionError as exc:
        if "semantic_oblique_selector_unique" in str(exc):
            selector_miss = "PASS"
            checks.append("expected_failure_selector_miss")
    check(selector_miss == "PASS", "failure_gate_selector_miss")
    failures["selector_miss"] = selector_miss

    stage("FCSTD_WRITE")
    doc = App.newDocument("OLEANDER_OBLIQUE_FACE_TRANSLATE")
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
        check(obj.OLE_ID == "OLE_OBLIQUE_FACE_TRANSLATE::" + name, "reopen_ole_id_" + name)
        check(obj.OLE_Selector == "SELECTOR::LOCAL_POS_X_FACE", "reopen_selector_" + name)
        check(close(float(obj.OLE_YawDeg), revision["yaw_deg"]), "reopen_yaw_" + name)
        check((obj.OLE_SelectorWorldNormal - vec(revision["operation"]["selector_world_normal"])).Length <= 1e-6, "reopen_normal_" + name)
        check((obj.OLE_TranslationWorldMM - vec(revision["operation"]["translation_world_mm"])).Length <= 1e-6, "reopen_translation_" + name)
        check(obj.OLE_GeometryAuthority == "FREECAD_OCCT_BREP", "reopen_authority_" + name)
        check(obj.Shape.isValid() and len(obj.Shape.Solids) == 1, "reopen_solid_" + name)
    App.closeDocument(reopened.Name)

    stage("DISPLAY")
    display = {
        "schema": "OLEANDER_OBLIQUE_FACE_TRANSLATE_DISPLAY_v0.1",
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
        "schema": "OLEANDER_FREECAD_OBLIQUE_FACE_TRANSLATE_v0.1",
        "status": "PASS",
        "units": "mm",
        "authority": {"geometry_master": "FREECAD_OCCT_BREP", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "selector": "semantic local +X face re-resolved from yaw-transformed world normal",
        "operation": "oblique planar face tangential translation through BRepTools_ReShape",
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
            "arbitrary_3d_oriented_planar_face_translate",
            "nonplanar_face_translate",
            "normal_direction_push_pull",
            "arbitrary_face_rotate",
            "persistent_topological_naming",
            "production_direct_modeling_parity",
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    stage("PASS")
    print("OLEANDER_FREECAD_OBLIQUE_FACE_TRANSLATE=" + json.dumps(manifest, sort_keys=True), flush=True)


if __name__ == "__main__":
    stage("START")
    try:
        main()
    except BaseException as exc:
        print("OLEANDER_OBLIQUE_FACE_TRANSLATE_EXCEPTION=" + repr(exc), flush=True)
        traceback.print_exc()
        raise
