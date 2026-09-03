"""OLEANDER bounded planar face in-plane translation through FreeCAD/OCCT BRep ReShape.

The unique +Z planar top face of a rectangular prismatic solid is selected by
geometry and translated rigidly within its own plane. The selected face and its
four adjacent faces are replaced through TopoShape.replaceShape /
BRepTools_ReShape while the opposite bottom face remains untouched.

This is a bounded direct B-Rep translation probe, not a general push/pull,
nonplanar-face edit, persistent topological naming system, or P0-B parity claim.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path

import FreeCAD as App
import Part

OUT = Path(os.environ.get("OLEANDER_FACE_TRANSLATE_DIR", "/tmp/oleander-face-translate"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_planar_face_translate.FCStd"
STEP_X = OUT / "oleander_planar_face_translate_x_R002.step"
STEP_Y = OUT / "oleander_planar_face_translate_y_R002.step"
STEP_DIAG = OUT / "oleander_planar_face_translate_diag_R002.step"
DISPLAY = OUT / "oleander_planar_face_translate_display.json"
MANIFEST = OUT / "oleander_planar_face_translate_manifest.json"
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


def translate_top_face(shape, dx_mm: float, dy_mm: float):
    check(shape.isValid() and len(shape.Solids) == 1, "input_single_valid_solid")
    if not math.isfinite(dx_mm) or not math.isfinite(dy_mm):
        raise ValueError("face translation components must be finite")
    distance = math.hypot(dx_mm, dy_mm)
    if distance < 1e-9:
        raise ValueError("face translation must be non-zero")
    if distance > 20.0:
        raise ValueError("face translation exceeds bounded in-plane contract")

    top, bottom = select_top_bottom(shape)
    top_pts = oriented_top_points(top)
    zmin = shape.BoundBox.ZMin
    zmax = shape.BoundBox.ZMax
    translated = [App.Vector(p.x + dx_mm, p.y + dy_mm, p.z) for p in top_pts]

    new_top = make_oriented_face(translated, App.Vector(0.0, 0.0, 1.0))
    check(close(new_top.BoundBox.ZMin, zmax), "translated_top_remains_coplanar_z")
    check(close(new_top.Area, top.Area, 1e-5), "translated_top_area_preserved")

    replacements = [(top, new_top)]
    bottom_pts = [App.Vector(p.x, p.y, zmin) for p in top_pts]
    side_meta = []
    for i, p0 in enumerate(top_pts):
        p1 = top_pts[(i + 1) % 4]
        old_side = adjacent_side(shape, p0, p1, top, bottom)
        poly = [
            bottom_pts[i],
            bottom_pts[(i + 1) % 4],
            translated[(i + 1) % 4],
            translated[i],
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
    check(edited.isValid() and len(edited.Solids) == 1, "translated_shape_valid_single_solid")
    check(close(edited.BoundBox.ZMin, shape.BoundBox.ZMin), "bottom_zmin_preserved")
    check(close(edited.BoundBox.ZMax, shape.BoundBox.ZMax), "height_envelope_preserved")
    check(close(edited.BoundBox.ZLength, shape.BoundBox.ZLength), "height_preserved")
    check(close(edited.Volume, shape.Volume, 1e-4), "shear_translation_volume_preserved")

    return edited, {
        "selector_id": "SELECTOR::TOP_PLANAR_FACE",
        "operation": "BRepTools_ReShape_TOP_FACE_TRANSLATE_IN_PLANE",
        "translation_mm": [dx_mm, dy_mm, 0.0],
        "translation_distance_mm": distance,
        "plane_normal": [0.0, 0.0, 1.0],
        "replaced_face_count": 5,
        "bottom_face_untouched": True,
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


def add_feature(doc, name, ole_id, shape, dx_mm, dy_mm):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = shape
    obj.addProperty("App::PropertyString", "OLE_ID", "OLEANDER")
    obj.OLE_ID = ole_id
    obj.addProperty("App::PropertyString", "OLE_Operation", "OLEANDER")
    obj.OLE_Operation = "PLANAR_TOP_FACE_TRANSLATE_IN_PLANE_RESHAPE"
    obj.addProperty("App::PropertyFloat", "OLE_TranslateXmm", "OLEANDER")
    obj.OLE_TranslateXmm = dx_mm
    obj.addProperty("App::PropertyFloat", "OLE_TranslateYmm", "OLEANDER")
    obj.OLE_TranslateYmm = dy_mm
    obj.addProperty("App::PropertyString", "OLE_TranslationUnits", "OLEANDER")
    obj.OLE_TranslationUnits = "mm"
    obj.addProperty("App::PropertyString", "OLE_Selector", "OLEANDER")
    obj.OLE_Selector = "SELECTOR::TOP_PLANAR_FACE"
    obj.addProperty("App::PropertyString", "OLE_GeometryAuthority", "OLEANDER")
    obj.OLE_GeometryAuthority = "FREECAD_OCCT_BREP"
    return obj


def main() -> None:
    base_r1 = Part.makeBox(80.0, 50.0, 10.0)
    x_r1, x_meta_r1 = translate_top_face(base_r1, 5.0, 0.0)
    y_r1, y_meta_r1 = translate_top_face(base_r1, 0.0, -4.0)
    diag_r1, diag_meta_r1 = translate_top_face(base_r1, 3.0, 4.0)
    check(close(x_r1.Volume, base_r1.Volume, 1e-4), "r1_x_volume")
    check(close(y_r1.Volume, base_r1.Volume, 1e-4), "r1_y_volume")
    check(close(diag_r1.Volume, base_r1.Volume, 1e-4), "r1_diag_volume")

    base_r2 = Part.makeBox(100.0, 50.0, 10.0)
    x_r2, x_meta_r2 = translate_top_face(base_r2, 5.0, 0.0)
    y_r2, y_meta_r2 = translate_top_face(base_r2, 0.0, -4.0)
    diag_r2, diag_meta_r2 = translate_top_face(base_r2, 3.0, 4.0)
    check(close(x_r2.Volume, base_r2.Volume, 1e-4), "r2_x_volume")
    check(close(y_r2.Volume, base_r2.Volume, 1e-4), "r2_y_volume")
    check(close(diag_r2.Volume, base_r2.Volume, 1e-4), "r2_diag_volume")
    check(x_meta_r1["selector_id"] == x_meta_r2["selector_id"], "selector_id_stable_across_rebuild")
    check(x_meta_r1["replaced_face_count"] == x_meta_r2["replaced_face_count"] == 5, "replacement_cardinality_stable_across_rebuild")
    check(close(x_meta_r2["translation_distance_mm"], 5.0), "x_translation_distance")
    check(close(y_meta_r2["translation_distance_mm"], 4.0), "y_translation_distance")
    check(close(diag_meta_r2["translation_distance_mm"], 5.0), "diagonal_translation_distance")

    zero_failure = "FAIL"
    try:
        translate_top_face(base_r2, 0.0, 0.0)
    except ValueError as exc:
        if "non-zero" in str(exc):
            zero_failure = "PASS"
            checks.append("zero_translation_expected_failure")
    check(zero_failure == "PASS", "zero_translation_failure_gate")

    excessive_failure = "FAIL"
    try:
        translate_top_face(base_r2, 21.0, 0.0)
    except ValueError as exc:
        if "bounded in-plane contract" in str(exc):
            excessive_failure = "PASS"
            checks.append("excessive_translation_expected_failure")
    check(excessive_failure == "PASS", "excessive_translation_failure_gate")

    doc = App.newDocument("OLEANDER_PLANAR_FACE_TRANSLATE")
    x_obj = add_feature(doc, "OLE_X_R002", "OLE_DIRECT_FACE_TRANSLATE::X_R002", x_r2, 5.0, 0.0)
    y_obj = add_feature(doc, "OLE_Y_R002", "OLE_DIRECT_FACE_TRANSLATE::Y_R002", y_r2, 0.0, -4.0)
    diag_obj = add_feature(doc, "OLE_DIAG_R002", "OLE_DIRECT_FACE_TRANSLATE::DIAG_R002", diag_r2, 3.0, 4.0)
    doc.recompute()
    doc.saveAs(str(FCSTD))
    x_obj.Shape.exportStep(str(STEP_X))
    y_obj.Shape.exportStep(str(STEP_Y))
    diag_obj.Shape.exportStep(str(STEP_DIAG))
    check(FCSTD.exists() and STEP_X.exists() and STEP_Y.exists() and STEP_DIAG.exists(), "native_translate_artifacts_written")

    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(FCSTD))
    expected = [
        ("OLE_X_R002", "OLE_DIRECT_FACE_TRANSLATE::X_R002", 5.0, 0.0),
        ("OLE_Y_R002", "OLE_DIRECT_FACE_TRANSLATE::Y_R002", 0.0, -4.0),
        ("OLE_DIAG_R002", "OLE_DIRECT_FACE_TRANSLATE::DIAG_R002", 3.0, 4.0),
    ]
    for name, ole_id, dx, dy in expected:
        obj = reopened.getObject(name)
        check(obj is not None, f"{name}_reopen")
        check(obj.OLE_ID == ole_id, f"{name}_ole_id_reopen")
        check(obj.OLE_Operation == "PLANAR_TOP_FACE_TRANSLATE_IN_PLANE_RESHAPE", f"{name}_operation_reopen")
        check(obj.OLE_Selector == "SELECTOR::TOP_PLANAR_FACE", f"{name}_selector_reopen")
        check(obj.OLE_TranslationUnits == "mm", f"{name}_units_reopen")
        check(close(float(obj.OLE_TranslateXmm), dx), f"{name}_x_reopen")
        check(close(float(obj.OLE_TranslateYmm), dy), f"{name}_y_reopen")
        check(obj.OLE_GeometryAuthority == "FREECAD_OCCT_BREP", f"{name}_authority_reopen")
        check(obj.Shape.isValid() and len(obj.Shape.Solids) == 1, f"{name}_solid_reopen")
    App.closeDocument(reopened.Name)

    verts, facets = diag_r2.tessellate(0.25)
    check(bool(verts) and bool(facets), "display_tessellation")
    display = {
        "schema": "OLEANDER_PLANAR_FACE_TRANSLATE_DISPLAY_v0.1",
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_OCCT_BREP",
        "display_authority": "DISPLAY_DERIVATIVE_ONLY",
        "units": "mm",
        "ole_id": "OLE_DIRECT_FACE_TRANSLATE::DIAG_R002",
        "selector_id": "SELECTOR::TOP_PLANAR_FACE",
        "operation": "BRepTools_ReShape_TOP_FACE_TRANSLATE_IN_PLANE",
        "translation_mm": [3.0, 4.0, 0.0],
        "translation_distance_mm": 5.0,
        "bbox_mm": metrics(diag_r2)["bbox_mm"],
        "vertices_mm": [[v.x, v.y, v.z] for v in verts],
        "triangles": [list(f) for f in facets],
        "source_fcstd": FCSTD.name,
        "source_fcstd_sha256": sha256(FCSTD),
        "source_step": STEP_DIAG.name,
        "source_step_sha256": sha256(STEP_DIAG),
    }
    DISPLAY.write_text(json.dumps(display, indent=2, sort_keys=True), encoding="utf-8")

    manifest = {
        "schema": "OLEANDER_FREECAD_PLANAR_FACE_TRANSLATE_v0.1",
        "status": "PASS",
        "units": "mm",
        "authority": {
            "geometry_master": "FREECAD_OCCT_BREP",
            "blender": "DISPLAY_DERIVATIVE_ONLY",
        },
        "selector": "unique +Z top planar face by geometry rule",
        "operation": "selected top-face rigid in-plane translation with adjacent-face topology update through BRepTools_ReShape",
        "revision1": {
            "base_width_mm": 80.0,
            "x": metrics(x_r1),
            "y": metrics(y_r1),
            "diag": metrics(diag_r1),
            "x_operation": x_meta_r1,
            "y_operation": y_meta_r1,
            "diag_operation": diag_meta_r1,
        },
        "revision2": {
            "base_width_mm": 100.0,
            "x": metrics(x_r2),
            "y": metrics(y_r2),
            "diag": metrics(diag_r2),
            "x_operation": x_meta_r2,
            "y_operation": y_meta_r2,
            "diag_operation": diag_meta_r2,
        },
        "expected_failure_cases": {
            "zero_translation": zero_failure,
            "excessive_translation": excessive_failure,
        },
        "artifacts": {
            "fcstd": {"path": FCSTD.name, "sha256": sha256(FCSTD)},
            "step_x": {"path": STEP_X.name, "sha256": sha256(STEP_X)},
            "step_y": {"path": STEP_Y.name, "sha256": sha256(STEP_Y)},
            "step_diag": {"path": STEP_DIAG.name, "sha256": sha256(STEP_DIAG)},
            "display": {"path": DISPLAY.name, "sha256": sha256(DISPLAY)},
        },
        "checks": checks,
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "general_face_translate",
            "normal_direction_push_pull",
            "arbitrary_face_rotate",
            "nonplanar_face_translate",
            "persistent_topological_naming",
            "production_direct_modeling_parity",
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print("OLEANDER_FREECAD_PLANAR_FACE_TRANSLATE=" + json.dumps(manifest, sort_keys=True))


if __name__ == "__main__":
    main()
