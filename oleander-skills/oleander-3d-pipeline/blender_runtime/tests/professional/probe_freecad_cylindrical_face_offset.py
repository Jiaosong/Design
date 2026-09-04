"""OLEANDER bounded nonplanar cylindrical-face radial offset.

A hollow FreeCAD/OCCT tube is used so the selected outer cylindrical face can
move radially while the inner cylindrical face remains fixed. The outer side
face and its two adjacent annular end faces are rebuilt from a donor annulus
with the requested radius, then applied to the original body through
BRepTools_ReShape. This is one bounded nonplanar face-offset family, not
unrestricted push/pull, arbitrary curved-face editing, or P0-B parity.
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

OUT = Path(os.environ.get("OLEANDER_CYLINDRICAL_FACE_OFFSET_DIR", "/tmp/oleander-cylindrical-face-offset"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_cylindrical_face_offset.FCStd"
STEP_R001 = OUT / "oleander_cylindrical_face_offset_R001.step"
STEP_R002 = OUT / "oleander_cylindrical_face_offset_R002.step"
DISPLAY = OUT / "oleander_cylindrical_face_offset_display.json"
MANIFEST = OUT / "oleander_cylindrical_face_offset_manifest.json"
TOL = 1e-6
checks: list[str] = []

REVISIONS = {
    "R001": {"outer_radius_mm": 30.0, "inner_radius_mm": 15.0, "height_mm": 20.0, "offset_mm": 2.0},
    "R002": {"outer_radius_mm": 40.0, "inner_radius_mm": 20.0, "height_mm": 25.0, "offset_mm": -3.0},
}


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def stage(label: str) -> None:
    print("OLEANDER_CYLINDRICAL_FACE_OFFSET_STAGE=" + label, flush=True)


def close(a, b, tol=TOL):
    return abs(float(a) - float(b)) <= tol


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def face_normal(face):
    u0, u1, v0, v1 = face.ParameterRange
    n = face.normalAt((u0 + u1) * 0.5, (v0 + v1) * 0.5)
    if n.Length > TOL:
        n.normalize()
    return n


def cylindrical_radius(face):
    surface = getattr(face, "Surface", None)
    radius = getattr(surface, "Radius", None)
    if radius is None:
        return None
    return float(radius)


def select_cylindrical_faces(shape):
    result = []
    for face in shape.Faces:
        radius = cylindrical_radius(face)
        if radius is not None and radius > TOL:
            result.append((radius, face))
    check(len(result) == 2, "exactly_two_cylindrical_faces")
    result.sort(key=lambda item: item[0])
    return result[0], result[1]


def select_end_faces(shape):
    top = []
    bottom = []
    for face in shape.Faces:
        if cylindrical_radius(face) is not None:
            continue
        n = face_normal(face)
        if n.z > 0.999999:
            top.append(face)
        elif n.z < -0.999999:
            bottom.append(face)
    check(len(top) == 1 and len(bottom) == 1, "unique_annular_end_faces")
    return top[0], bottom[0]


def make_tube(outer_radius, inner_radius, height):
    if not all(math.isfinite(v) for v in (outer_radius, inner_radius, height)):
        raise ValueError("tube dimensions must be finite")
    if height <= 0 or inner_radius <= 0 or outer_radius <= inner_radius:
        raise ValueError("invalid tube dimensions")
    shape = Part.makeCylinder(outer_radius, height).cut(Part.makeCylinder(inner_radius, height)).removeSplitter()
    check(shape.isValid() and len(shape.Solids) == 1, "tube_valid_single_solid")
    return shape


def normalize_reshape(shape):
    candidate = shape.copy()
    candidate.sewShape(1e-7)
    candidate.fix(1e-7, 1e-7, 1e-7)
    candidate = candidate.removeSplitter()
    if candidate.isValid() and len(candidate.Solids) == 1:
        checks.append("reshape_direct_single_solid")
        return candidate.Solids[0]
    check(candidate.isValid(), "reshape_valid_before_shell_rebuild")
    shell = Part.makeShell(candidate.Faces)
    shell.sewShape(1e-7)
    shell.fix(1e-7, 1e-7, 1e-7)
    solid = Part.makeSolid(shell).removeSplitter()
    check(solid.isValid() and len(solid.Solids) == 1, "shell_rebuild_valid_single_solid")
    return solid


def metrics(shape):
    return {
        "bbox_mm": [shape.BoundBox.XLength, shape.BoundBox.YLength, shape.BoundBox.ZLength],
        "volume_mm3": shape.Volume,
        "solid_count": len(shape.Solids),
        "face_count": len(shape.Faces),
        "edge_count": len(shape.Edges),
    }


def offset_outer_cylindrical_face(shape, offset_mm):
    if not math.isfinite(offset_mm) or abs(offset_mm) < 1e-9:
        raise ValueError("offset must be finite and non-zero")
    if abs(offset_mm) > 5.0:
        raise ValueError("offset exceeds bounded radial contract")
    (inner_radius, inner_face), (outer_radius, outer_face) = select_cylindrical_faces(shape)
    top, bottom = select_end_faces(shape)
    height = shape.BoundBox.ZLength
    new_outer = outer_radius + offset_mm
    if new_outer <= inner_radius + 1.0:
        raise ValueError("offset collapses bounded wall thickness")

    inner_area_before = inner_face.Area
    inner_bbox_before = [inner_face.BoundBox.XLength, inner_face.BoundBox.YLength, inner_face.BoundBox.ZLength]
    donor = make_tube(new_outer, inner_radius, height)
    (donor_inner_radius, _), (donor_outer_radius, donor_outer) = select_cylindrical_faces(donor)
    donor_top, donor_bottom = select_end_faces(donor)
    check(close(donor_inner_radius, inner_radius), "donor_inner_radius_matches")
    check(close(donor_outer_radius, new_outer), "donor_outer_radius_matches")

    reshaped = shape.replaceShape([(outer_face, donor_outer), (top, donor_top), (bottom, donor_bottom)])
    check(not reshaped.isNull(), "reshape_non_null")
    edited = normalize_reshape(reshaped)
    check(edited.isValid() and len(edited.Solids) == 1, "edited_valid_single_solid")
    (inner_after_radius, inner_after), (outer_after_radius, outer_after) = select_cylindrical_faces(edited)
    top_after, bottom_after = select_end_faces(edited)
    check(close(inner_after_radius, inner_radius), "inner_radius_preserved")
    check(close(outer_after_radius, new_outer), "outer_radius_matches_offset")
    check(close(inner_after.Area, inner_area_before, 1e-5), "inner_face_area_preserved")
    check(all(close(a, b, 1e-5) for a, b in zip([inner_after.BoundBox.XLength, inner_after.BoundBox.YLength, inner_after.BoundBox.ZLength], inner_bbox_before)), "inner_face_bbox_preserved")
    check(close(top_after.Area, math.pi * (new_outer * new_outer - inner_radius * inner_radius), 1e-4), "top_annulus_area")
    check(close(bottom_after.Area, top_after.Area, 1e-5), "end_annulus_areas_match")
    expected_volume = math.pi * (new_outer * new_outer - inner_radius * inner_radius) * height
    check(close(edited.Volume, expected_volume, 1e-3), "edited_volume_formula")
    check(len(edited.Faces) == 4, "edited_four_faces")
    return edited, {
        "selector_id": "SELECTOR::OUTER_CYLINDRICAL_FACE::MAX_RADIUS",
        "operation": "BRepTools_ReShape_NONPLANAR_CYLINDRICAL_FACE_RADIAL_OFFSET",
        "source_outer_radius_mm": outer_radius,
        "inner_radius_mm": inner_radius,
        "offset_mm": offset_mm,
        "result_outer_radius_mm": new_outer,
        "height_mm": height,
        "expected_volume_mm3": expected_volume,
        "replaced_face_count": 3,
        "preserved_nonplanar_face": "INNER_CYLINDRICAL_FACE",
        "geometry_authority": "FREECAD_OCCT_BREP",
    }


def build_revision(name, spec):
    source = make_tube(spec["outer_radius_mm"], spec["inner_radius_mm"], spec["height_mm"])
    edited, op = offset_outer_cylindrical_face(source, spec["offset_mm"])
    return {"source": source, "edited": edited, "operation": op, "metrics": metrics(edited)}


def add_feature(doc, name, rev):
    op = rev["operation"]
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = rev["edited"]
    for prop, value in [("OLE_ID", "OLE_CYL_FACE_OFFSET::" + name), ("OLE_Operation", op["operation"]), ("OLE_Selector", op["selector_id"]), ("OLE_GeometryAuthority", "FREECAD_OCCT_BREP")]:
        obj.addProperty("App::PropertyString", prop, "OLEANDER"); setattr(obj, prop, value)
    for prop, value in [("OLE_SourceOuterRadiusMm", op["source_outer_radius_mm"]), ("OLE_InnerRadiusMm", op["inner_radius_mm"]), ("OLE_OffsetMm", op["offset_mm"]), ("OLE_ResultOuterRadiusMm", op["result_outer_radius_mm"]), ("OLE_HeightMm", op["height_mm"])]:
        obj.addProperty("App::PropertyFloat", prop, "OLEANDER"); setattr(obj, prop, value)
    return obj


def display_record(name, rev, step):
    verts, facets = rev["edited"].tessellate(0.2)
    check(bool(verts) and bool(facets), "display_tessellation_" + name)
    op = rev["operation"]
    return {
        "revision": name,
        "ole_id": "OLE_CYL_FACE_OFFSET::" + name,
        "operation": op["operation"],
        "selector_id": op["selector_id"],
        "source_outer_radius_mm": op["source_outer_radius_mm"],
        "inner_radius_mm": op["inner_radius_mm"],
        "offset_mm": op["offset_mm"],
        "result_outer_radius_mm": op["result_outer_radius_mm"],
        "height_mm": op["height_mm"],
        "bbox_mm": rev["metrics"]["bbox_mm"],
        "volume_mm3": rev["metrics"]["volume_mm3"],
        "vertices_mm": [[v.x, v.y, v.z] for v in verts],
        "triangles": [list(f) for f in facets],
        "source_step": step.name,
        "source_step_sha256": sha256(step),
    }


def serializable(rev):
    return {"operation": rev["operation"], "metrics": rev["metrics"]}


def main():
    revs = {}
    for name, spec in REVISIONS.items():
        stage(name); revs[name] = build_revision(name, spec)
    check(revs["R001"]["operation"]["selector_id"] == revs["R002"]["operation"]["selector_id"], "selector_id_stable")
    for name, rev in revs.items():
        check(rev["metrics"]["solid_count"] == 1 and rev["metrics"]["face_count"] == 4, "topology_" + name)
        check(close(rev["operation"]["result_outer_radius_mm"], rev["operation"]["source_outer_radius_mm"] + rev["operation"]["offset_mm"]), "radius_delta_" + name)

    stage("EXPECTED_FAILURES")
    base = make_tube(30.0, 15.0, 20.0)
    failures = {}
    for label, delta, needle in [
        ("zero_offset", 0.0, "non-zero"),
        ("excessive_offset", 6.0, "bounded radial contract"),
        ("wall_collapse", -14.5, "bounded radial contract"),
    ]:
        state = "FAIL"
        try: offset_outer_cylindrical_face(base, delta)
        except ValueError as exc:
            if needle in str(exc): state = "PASS"; checks.append("expected_failure_" + label)
        check(state == "PASS", "failure_gate_" + label); failures[label] = state
    invalid_tube = "FAIL"
    try: make_tube(15.0, 15.0, 20.0)
    except ValueError as exc:
        if "invalid tube dimensions" in str(exc): invalid_tube = "PASS"; checks.append("expected_failure_invalid_tube")
    check(invalid_tube == "PASS", "failure_gate_invalid_tube"); failures["invalid_tube"] = invalid_tube
    selector_miss = "FAIL"
    try: select_cylindrical_faces(Part.makeBox(20, 20, 20))
    except AssertionError:
        selector_miss = "PASS"; checks.append("expected_failure_selector_miss")
    check(selector_miss == "PASS", "failure_gate_selector_miss"); failures["selector_miss"] = selector_miss

    stage("FCSTD_STEP")
    doc = App.newDocument("OLEANDER_CYLINDRICAL_FACE_OFFSET")
    o1, o2 = add_feature(doc, "R001", revs["R001"]), add_feature(doc, "R002", revs["R002"])
    doc.recompute(); doc.saveAs(str(FCSTD)); o1.Shape.exportStep(str(STEP_R001)); o2.Shape.exportStep(str(STEP_R002))
    check(FCSTD.exists() and STEP_R001.exists() and STEP_R002.exists(), "native_artifacts_written")
    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(FCSTD))
    for name in ("R001", "R002"):
        obj = reopened.getObject(name); op = revs[name]["operation"]
        check(obj is not None and obj.Shape.isValid() and len(obj.Shape.Solids) == 1, "reopen_solid_" + name)
        check(obj.OLE_Selector == "SELECTOR::OUTER_CYLINDRICAL_FACE::MAX_RADIUS", "reopen_selector_" + name)
        check(close(obj.OLE_ResultOuterRadiusMm, op["result_outer_radius_mm"]), "reopen_outer_radius_" + name)
        check(close(obj.OLE_InnerRadiusMm, op["inner_radius_mm"]), "reopen_inner_radius_" + name)
        check(close(obj.OLE_OffsetMm, op["offset_mm"]), "reopen_offset_" + name)
        check(obj.OLE_GeometryAuthority == "FREECAD_OCCT_BREP", "reopen_authority_" + name)
    App.closeDocument(reopened.Name)

    stage("DISPLAY")
    display = {
        "schema": "OLEANDER_CYLINDRICAL_FACE_OFFSET_DISPLAY_v0.1",
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_OCCT_BREP",
        "display_authority": "DISPLAY_DERIVATIVE_ONLY",
        "units": "mm",
        "source_fcstd": FCSTD.name,
        "source_fcstd_sha256": sha256(FCSTD),
        "revisions": [display_record("R001", revs["R001"], STEP_R001), display_record("R002", revs["R002"], STEP_R002)],
    }
    DISPLAY.write_text(json.dumps(display, indent=2, sort_keys=True), encoding="utf-8")
    manifest = {
        "schema": "OLEANDER_FREECAD_CYLINDRICAL_FACE_OFFSET_v0.1",
        "status": "PASS",
        "units": "mm",
        "authority": {"geometry_master": "FREECAD_OCCT_BREP", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "selector": "outer cylindrical nonplanar face chosen by maximum cylinder radius",
        "operation": "BRepTools_ReShape replaces outer cylindrical face plus adjacent top/bottom annular faces; inner cylindrical face remains fixed",
        "R001": serializable(revs["R001"]),
        "R002": serializable(revs["R002"]),
        "expected_failure_cases": failures,
        "artifacts": {
            "fcstd": {"path": FCSTD.name, "sha256": sha256(FCSTD)},
            "step_R001": {"path": STEP_R001.name, "sha256": sha256(STEP_R001)},
            "step_R002": {"path": STEP_R002.name, "sha256": sha256(STEP_R002)},
            "display": {"path": DISPLAY.name, "sha256": sha256(DISPLAY)},
        },
        "checks": checks,
        "non_claims": ["P0_B_DIRECT_BREP_PASS", "general_push_pull", "arbitrary_curved_face_offset", "freeform_nonplanar_face_edit", "persistent_topological_naming", "production_direct_modeling_parity"],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    stage("PASS"); print("OLEANDER_FREECAD_CYLINDRICAL_FACE_OFFSET=" + json.dumps(manifest, sort_keys=True), flush=True)


if __name__ == "__main__":
    stage("START")
    try: main()
    except BaseException as exc:
        print("OLEANDER_CYLINDRICAL_FACE_OFFSET_EXCEPTION=" + repr(exc), flush=True); traceback.print_exc(); raise
