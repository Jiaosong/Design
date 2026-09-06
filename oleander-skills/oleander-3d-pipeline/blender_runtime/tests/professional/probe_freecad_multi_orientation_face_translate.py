"""OLEANDER bounded multi-orientation planar-face in-plane translation probe.

Extends the earlier +Z-only bounded ReShape experiment to three semantic face
orientations (+Z, +X, +Y). Each target is resolved from face geometry, translated
only inside its own tangent plane, and rebuilt together with its four adjacent
faces through FreeCAD/OCCT BRep ReShape. The opposite face is not replaced.

This remains a bounded axis-aligned planar-solid probe. It does not prove
arbitrary oblique/nonplanar face edits, persistent topological naming, or P0-B.
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

OUT = Path(os.environ.get("OLEANDER_MULTI_FACE_TRANSLATE_DIR", "/tmp/oleander-multi-face-translate"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_multi_orientation_face_translate.FCStd"
DISPLAY = OUT / "oleander_multi_orientation_face_translate_display.json"
MANIFEST = OUT / "oleander_multi_orientation_face_translate_manifest.json"
TOL = 1e-6
checks: list[str] = []

CASES = {
    "TOP_Z": {"normal": (0.0, 0.0, 1.0), "delta": (3.0, 4.0, 0.0)},
    "SIDE_X": {"normal": (1.0, 0.0, 0.0), "delta": (0.0, 4.0, 3.0)},
    "SIDE_Y": {"normal": (0.0, 1.0, 0.0), "delta": (4.0, 0.0, 3.0)},
}


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def stage(label: str) -> None:
    print("OLEANDER_MULTI_FACE_TRANSLATE_STAGE=" + label, flush=True)


def vec(values):
    if hasattr(values, "x") and hasattr(values, "y") and hasattr(values, "z"):
        return App.Vector(float(values.x), float(values.y), float(values.z))
    return App.Vector(float(values[0]), float(values[1]), float(values[2]))


def unit(v):
    r = vec(v)
    if r.Length <= TOL:
        raise ValueError("normal must be non-zero")
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


def select_face_by_normal(shape, normal):
    target = unit(normal)
    found = []
    for face in shape.Faces:
        n = face_normal(face)
        if n.dot(target) > 0.999999:
            found.append(face)
    check(len(found) == 1, "semantic_normal_selector_unique")
    return found[0]


def make_oriented_face(points, expected_normal):
    face = Part.Face(Part.makePolygon(points + [points[0]]))
    if face_normal(face).dot(unit(expected_normal)) < 0:
        face = face.reversed()
    check(face.isValid(), "rebuilt_planar_face_valid")
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


def center_tuple(face):
    c = face.CenterOfMass
    return [c.x, c.y, c.z]


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


def translate_selected_face(shape, selector_normal, translation):
    check(shape.isValid() and len(shape.Solids) == 1, "input_valid_single_solid")
    n = unit(selector_normal)
    delta = vec(translation)
    if not all(math.isfinite(v) for v in (delta.x, delta.y, delta.z)):
        raise ValueError("translation components must be finite")
    if delta.Length < 1e-9:
        raise ValueError("translation must be non-zero")
    if delta.Length > 20.0:
        raise ValueError("translation exceeds bounded contract")
    if abs(delta.dot(n)) > 1e-7:
        raise ValueError("translation must remain in selected face tangent plane")

    target = select_face_by_normal(shape, n)
    opposite = select_face_by_normal(shape, -n)
    target_pts = ordered_points(target)
    opposite_center_before = opposite.CenterOfMass
    target_center_before = target.CenterOfMass

    moved_target_pts = [p + delta for p in target_pts]
    new_target = make_oriented_face(moved_target_pts, n)
    check((new_target.CenterOfMass - (target_center_before + delta)).Length <= 1e-5, "target_center_translated_exactly")
    check(close(new_target.Area, target.Area, 1e-5), "target_area_preserved")

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
        check(shared == 2, "adjacent_face_shares_target_edge")
        rebuilt_points = [p + delta if flag else p for p, flag in zip(points, on_target)]
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
    check(close(edited.Volume, shape.Volume, 1e-4), "shear_volume_preserved")

    opposite_after = select_face_by_normal(edited, -n)
    check((opposite_after.CenterOfMass - opposite_center_before).Length <= 1e-5, "opposite_face_center_preserved")
    check(close(opposite_after.Area, opposite.Area, 1e-5), "opposite_face_area_preserved")

    return edited, {
        "selector_id": "SELECTOR::FACE_NORMAL::%.0f_%.0f_%.0f" % (n.x, n.y, n.z),
        "selector_normal": [n.x, n.y, n.z],
        "translation_mm": [delta.x, delta.y, delta.z],
        "translation_distance_mm": delta.Length,
        "tangent_dot_normal": delta.dot(n),
        "operation": "BRepTools_ReShape_PLANAR_FACE_TANGENTIAL_TRANSLATE",
        "replaced_face_count": 5,
        "opposite_face_untouched": True,
        "target_center_before_mm": center_tuple(target),
        "target_center_after_mm": center_tuple(new_target),
        "opposite_center_mm": center_tuple(opposite),
    }


def run_revision(dimensions):
    base = Part.makeBox(*dimensions)
    result = {}
    for name, spec in CASES.items():
        stage("CASE_" + name)
        edited, op = translate_selected_face(base, spec["normal"], spec["delta"])
        result[name] = {"metrics": metrics(edited), "operation": op, "shape": edited}
    return base, result


def add_feature(doc, name, shape, op):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = shape
    obj.addProperty("App::PropertyString", "OLE_ID", "OLEANDER")
    obj.OLE_ID = "OLE_MULTI_FACE_TRANSLATE::" + name
    obj.addProperty("App::PropertyString", "OLE_Operation", "OLEANDER")
    obj.OLE_Operation = op["operation"]
    obj.addProperty("App::PropertyString", "OLE_Selector", "OLEANDER")
    obj.OLE_Selector = op["selector_id"]
    obj.addProperty("App::PropertyVector", "OLE_SelectorNormal", "OLEANDER")
    obj.OLE_SelectorNormal = vec(op["selector_normal"])
    obj.addProperty("App::PropertyVector", "OLE_TranslationMM", "OLEANDER")
    obj.OLE_TranslationMM = vec(op["translation_mm"])
    obj.addProperty("App::PropertyString", "OLE_GeometryAuthority", "OLEANDER")
    obj.OLE_GeometryAuthority = "FREECAD_OCCT_BREP"
    return obj


def display_record(name, shape, op, step_path):
    verts, facets = shape.tessellate(0.25)
    check(bool(verts) and bool(facets), "display_tessellation_" + name)
    return {
        "case": name,
        "ole_id": "OLE_MULTI_FACE_TRANSLATE::" + name,
        "selector_id": op["selector_id"],
        "selector_normal": op["selector_normal"],
        "translation_mm": op["translation_mm"],
        "translation_distance_mm": op["translation_distance_mm"],
        "bbox_mm": metrics(shape)["bbox_mm"],
        "vertices_mm": [[v.x, v.y, v.z] for v in verts],
        "triangles": [list(f) for f in facets],
        "source_step": step_path.name,
        "source_step_sha256": sha256(step_path),
    }


def serializable_revision(revision):
    return {
        name: {"metrics": item["metrics"], "operation": item["operation"]}
        for name, item in revision.items()
    }


def main() -> None:
    stage("R001")
    base_r1, r1 = run_revision((80.0, 50.0, 10.0))
    stage("R002")
    base_r2, r2 = run_revision((100.0, 60.0, 12.0))

    for name in CASES:
        check(r1[name]["operation"]["selector_id"] == r2[name]["operation"]["selector_id"], "selector_stable_" + name)
        check(r1[name]["metrics"]["solid_count"] == r2[name]["metrics"]["solid_count"] == 1, "one_solid_both_revisions_" + name)
        check(close(r1[name]["metrics"]["volume_mm3"], base_r1.Volume, 1e-4), "r1_volume_" + name)
        check(close(r2[name]["metrics"]["volume_mm3"], base_r2.Volume, 1e-4), "r2_volume_" + name)

    expected_r2_bbox = {
        "TOP_Z": [103.0, 64.0, 12.0],
        "SIDE_X": [100.0, 64.0, 15.0],
        "SIDE_Y": [104.0, 60.0, 15.0],
    }
    for name, expected in expected_r2_bbox.items():
        actual = r2[name]["metrics"]["bbox_mm"]
        check(all(close(a, b, 1e-5) for a, b in zip(actual, expected)), "r2_bbox_" + name)

    stage("EXPECTED_FAILURES")
    failure = {}
    for label, normal, delta, needle in [
        ("zero", (0, 0, 1), (0, 0, 0), "non-zero"),
        ("normal_component", (1, 0, 0), (1, 0, 0), "tangent plane"),
        ("excessive", (0, 1, 0), (21, 0, 0), "bounded contract"),
    ]:
        state = "FAIL"
        try:
            translate_selected_face(base_r2, normal, delta)
        except ValueError as exc:
            if needle in str(exc):
                state = "PASS"
                checks.append("expected_failure_" + label)
        check(state == "PASS", "failure_gate_" + label)
        failure[label] = state

    stage("FCSTD_WRITE")
    doc = App.newDocument("OLEANDER_MULTI_ORIENTATION_FACE_TRANSLATE")
    objects = {}
    steps = {}
    for name in CASES:
        objects[name] = add_feature(doc, name, r2[name]["shape"], r2[name]["operation"])
    doc.recompute()
    doc.saveAs(str(FCSTD))
    for name, obj in objects.items():
        step = OUT / ("oleander_multi_face_translate_" + name.lower() + "_R002.step")
        obj.Shape.exportStep(str(step))
        check(step.exists() and step.stat().st_size > 0, "step_written_" + name)
        steps[name] = step
    check(FCSTD.exists() and FCSTD.stat().st_size > 0, "fcstd_written")

    stage("FCSTD_REOPEN")
    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(FCSTD))
    for name, spec in CASES.items():
        obj = reopened.getObject(name)
        check(obj is not None, "reopen_object_" + name)
        check(obj.OLE_ID == "OLE_MULTI_FACE_TRANSLATE::" + name, "reopen_ole_id_" + name)
        check(obj.OLE_GeometryAuthority == "FREECAD_OCCT_BREP", "reopen_authority_" + name)
        check(obj.Shape.isValid() and len(obj.Shape.Solids) == 1, "reopen_solid_" + name)
        delta = obj.OLE_TranslationMM
        expected_delta = vec(spec["delta"])
        check((delta - expected_delta).Length <= 1e-6, "reopen_translation_" + name)
    App.closeDocument(reopened.Name)

    stage("DISPLAY")
    display_cases = [display_record(name, r2[name]["shape"], r2[name]["operation"], steps[name]) for name in CASES]
    display = {
        "schema": "OLEANDER_MULTI_ORIENTATION_FACE_TRANSLATE_DISPLAY_v0.1",
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_OCCT_BREP",
        "display_authority": "DISPLAY_DERIVATIVE_ONLY",
        "units": "mm",
        "source_fcstd": FCSTD.name,
        "source_fcstd_sha256": sha256(FCSTD),
        "cases": display_cases,
    }
    DISPLAY.write_text(json.dumps(display, indent=2, sort_keys=True), encoding="utf-8")

    manifest = {
        "schema": "OLEANDER_FREECAD_MULTI_ORIENTATION_FACE_TRANSLATE_v0.1",
        "status": "PASS",
        "units": "mm",
        "authority": {"geometry_master": "FREECAD_OCCT_BREP", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "operation": "semantic-normal-selected axis-aligned planar face tangential translation through BRepTools_ReShape",
        "revision1": {"base_mm": [80.0, 50.0, 10.0], "cases": serializable_revision(r1)},
        "revision2": {"base_mm": [100.0, 60.0, 12.0], "cases": serializable_revision(r2)},
        "expected_failure_cases": failure,
        "artifacts": {
            "fcstd": {"path": FCSTD.name, "sha256": sha256(FCSTD)},
            "display": {"path": DISPLAY.name, "sha256": sha256(DISPLAY)},
            "steps": {name: {"path": path.name, "sha256": sha256(path)} for name, path in steps.items()},
        },
        "checks": checks,
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "arbitrary_oblique_planar_face_translate",
            "nonplanar_face_translate",
            "normal_direction_push_pull",
            "arbitrary_face_rotate",
            "persistent_topological_naming",
            "production_direct_modeling_parity",
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    stage("PASS")
    print("OLEANDER_FREECAD_MULTI_ORIENTATION_FACE_TRANSLATE=" + json.dumps(manifest, sort_keys=True), flush=True)


if __name__ == "__main__":
    stage("START")
    try:
        main()
    except BaseException as exc:
        print("OLEANDER_MULTI_FACE_TRANSLATE_EXCEPTION=" + repr(exc), flush=True)
        traceback.print_exc()
        raise
