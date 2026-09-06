"""OLEANDER bounded authoritative B-Rep feature pattern/mirror probe.

This probe cuts real cylindrical through-hole features from FreeCAD/OCCT plate
solids. R001 creates a governed linear pattern from one seed feature; R002
mirrors one seed feature across a governed plane. The result remains an
FCStd/STEP authoritative B-Rep master and Blender is display-only.

This proves bounded pattern/mirror feature replication only. It does not prove
general feature-pattern semantics, arbitrary path/circular patterns, persistent
topological naming, assembly patterns, or P0-B parity.
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

OUT = Path(os.environ.get("OLEANDER_PATTERN_MIRROR_DIR", "/tmp/oleander-pattern-mirror"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_bounded_pattern_mirror.FCStd"
STEP_PATTERN = OUT / "oleander_bounded_pattern_R001.step"
STEP_MIRROR = OUT / "oleander_bounded_mirror_R002.step"
DISPLAY = OUT / "oleander_bounded_pattern_mirror_display.json"
MANIFEST = OUT / "oleander_bounded_pattern_mirror_manifest.json"
TOL = 1e-6
checks: list[str] = []

PLATE = (120.0, 60.0, 10.0)
RADIUS = 3.0
Y = 30.0


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def stage(label: str) -> None:
    print("OLEANDER_PATTERN_MIRROR_STAGE=" + label, flush=True)


def close(a: float, b: float, tol: float = 1e-5) -> bool:
    return abs(float(a) - float(b)) <= tol


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_center(center, dims=PLATE, radius=RADIUS) -> None:
    x, y = center
    w, d, _ = dims
    if not (radius < x < w - radius and radius < y < d - radius):
        raise ValueError("feature center must remain inside bounded source body")


def through_hole(shape, center, radius=RADIUS, height=None):
    w, d, h = PLATE
    if height is None:
        height = h
    validate_center(center, (w, d, h), radius)
    x, y = center
    cutter = Part.makeCylinder(radius, height + 2.0, App.Vector(x, y, -1.0), App.Vector(0, 0, 1))
    result = shape.cut(cutter).removeSplitter()
    check(result.isValid(), "cut_valid")
    check(len(result.Solids) == 1, "cut_single_solid")
    return result


def expected_volume(hole_count: int, dims=PLATE, radius=RADIUS) -> float:
    w, d, h = dims
    return w * d * h - hole_count * math.pi * radius * radius * h


def apply_linear_pattern(source, seed_center, count, spacing):
    if not isinstance(count, int) or count < 2:
        raise ValueError("linear pattern count must be integer >= 2")
    if not math.isfinite(spacing) or spacing <= 0:
        raise ValueError("linear pattern spacing must be finite and positive")
    centers = [(seed_center[0] + i * spacing, seed_center[1]) for i in range(count)]
    for center in centers:
        validate_center(center)
    if len({(round(x, 8), round(y, 8)) for x, y in centers}) != count:
        raise ValueError("linear pattern centers must be unique")
    edited = source
    for center in centers:
        edited = through_hole(edited, center)
    check(edited.isValid() and len(edited.Solids) == 1, "linear_pattern_valid_single_solid")
    check(close(edited.Volume, expected_volume(count), 1e-4), "linear_pattern_expected_volume")
    return edited, centers


def apply_mirror(source, seed_center, plane_x):
    if not math.isfinite(plane_x):
        raise ValueError("mirror plane must be finite")
    validate_center(seed_center)
    mirrored = (2.0 * plane_x - seed_center[0], seed_center[1])
    validate_center(mirrored)
    if math.hypot(mirrored[0] - seed_center[0], mirrored[1] - seed_center[1]) <= TOL:
        raise ValueError("mirror must produce a distinct feature center")
    edited = through_hole(source, seed_center)
    edited = through_hole(edited, mirrored)
    check(edited.isValid() and len(edited.Solids) == 1, "mirror_valid_single_solid")
    check(close(edited.Volume, expected_volume(2), 1e-4), "mirror_expected_volume")
    return edited, [seed_center, mirrored]


def metrics(shape):
    return {
        "bbox_mm": [shape.BoundBox.XLength, shape.BoundBox.YLength, shape.BoundBox.ZLength],
        "volume_mm3": shape.Volume,
        "solid_count": len(shape.Solids),
        "face_count": len(shape.Faces),
        "edge_count": len(shape.Edges),
    }


def add_feature(doc, name, shape, operation, centers, params):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = shape
    props = {
        "OLE_ID": "OLE_BREP_PATTERN_MIRROR::" + name,
        "OLE_Operation": operation,
        "OLE_GeometryAuthority": "FREECAD_OCCT_BREP",
        "OLE_FeatureType": "THROUGH_HOLE",
        "OLE_FeatureCentersJSON": json.dumps(centers),
        "OLE_ParametersJSON": json.dumps(params, sort_keys=True),
    }
    for prop, value in props.items():
        obj.addProperty("App::PropertyString", prop, "OLEANDER")
        setattr(obj, prop, value)
    obj.addProperty("App::PropertyFloat", "OLE_RadiusMM", "OLEANDER")
    obj.OLE_RadiusMM = RADIUS
    return obj


def display_record(name, shape, centers, operation, params, step_path):
    verts, facets = shape.tessellate(0.25)
    check(bool(verts) and bool(facets), "display_tessellation_" + name)
    return {
        "revision": name,
        "ole_id": "OLE_BREP_PATTERN_MIRROR::" + name,
        "operation": operation,
        "feature_type": "THROUGH_HOLE",
        "feature_radius_mm": RADIUS,
        "feature_centers_mm": [[x, y, 0.0] for x, y in centers],
        "parameters": params,
        "metrics": metrics(shape),
        "vertices_mm": [[v.x, v.y, v.z] for v in verts],
        "triangles": [list(f) for f in facets],
        "source_step": step_path.name,
        "source_step_sha256": sha256(step_path),
    }


def main():
    stage("R001_LINEAR_PATTERN")
    source1 = Part.makeBox(*PLATE)
    pattern, pattern_centers = apply_linear_pattern(source1, (30.0, Y), 3, 30.0)
    check(pattern_centers == [(30.0, 30.0), (60.0, 30.0), (90.0, 30.0)], "pattern_centers")
    check(close(pattern.BoundBox.XLength, 120.0) and close(pattern.BoundBox.YLength, 60.0) and close(pattern.BoundBox.ZLength, 10.0), "pattern_bbox_preserved")

    stage("R002_MIRROR")
    source2 = Part.makeBox(*PLATE)
    mirror, mirror_centers = apply_mirror(source2, (30.0, Y), 60.0)
    check(mirror_centers == [(30.0, 30.0), (90.0, 30.0)], "mirror_centers")
    check(close(mirror.BoundBox.XLength, 120.0) and close(mirror.BoundBox.YLength, 60.0) and close(mirror.BoundBox.ZLength, 10.0), "mirror_bbox_preserved")

    stage("EXPECTED_FAILURES")
    failures = {}
    cases = [
        ("pattern_count_one", lambda: apply_linear_pattern(Part.makeBox(*PLATE), (30.0, Y), 1, 30.0), "count"),
        ("pattern_zero_spacing", lambda: apply_linear_pattern(Part.makeBox(*PLATE), (30.0, Y), 3, 0.0), "spacing"),
        ("pattern_outside_body", lambda: apply_linear_pattern(Part.makeBox(*PLATE), (80.0, Y), 3, 30.0), "inside"),
        ("mirror_duplicate_on_plane", lambda: apply_mirror(Part.makeBox(*PLATE), (60.0, Y), 60.0), "distinct"),
        ("mirror_outside_body", lambda: apply_mirror(Part.makeBox(*PLATE), (20.0, Y), 100.0), "inside"),
    ]
    for label, fn, needle in cases:
        state = "FAIL"
        try:
            fn()
        except ValueError as exc:
            if needle in str(exc):
                state = "PASS"
                checks.append("expected_failure_" + label)
        check(state == "PASS", "failure_gate_" + label)
        failures[label] = state

    stage("FCSTD_STEP")
    doc = App.newDocument("OLEANDER_BOUNDED_PATTERN_MIRROR")
    p_params = {"seed_center_mm": [30.0, Y, 0.0], "direction": "WORLD_X", "count": 3, "spacing_mm": 30.0}
    m_params = {"seed_center_mm": [30.0, Y, 0.0], "mirror_plane": "WORLD_X_EQ_60MM", "mirror_plane_x_mm": 60.0}
    pobj = add_feature(doc, "R001_LINEAR_PATTERN", pattern, "BRep_BOOLEAN_CUT_LINEAR_FEATURE_PATTERN", pattern_centers, p_params)
    mobj = add_feature(doc, "R002_MIRROR", mirror, "BRep_BOOLEAN_CUT_MIRRORED_FEATURE", mirror_centers, m_params)
    doc.recompute()
    doc.saveAs(str(FCSTD))
    pobj.Shape.exportStep(str(STEP_PATTERN))
    mobj.Shape.exportStep(str(STEP_MIRROR))
    check(FCSTD.exists() and STEP_PATTERN.exists() and STEP_MIRROR.exists(), "native_artifacts_written")
    App.closeDocument(doc.Name)

    reopened = App.openDocument(str(FCSTD))
    for name, operation, centers in [
        ("R001_LINEAR_PATTERN", "BRep_BOOLEAN_CUT_LINEAR_FEATURE_PATTERN", pattern_centers),
        ("R002_MIRROR", "BRep_BOOLEAN_CUT_MIRRORED_FEATURE", mirror_centers),
    ]:
        obj = reopened.getObject(name)
        check(obj is not None and obj.Shape.isValid() and len(obj.Shape.Solids) == 1, "reopen_valid_" + name)
        check(obj.OLE_Operation == operation, "reopen_operation_" + name)
        check(json.loads(obj.OLE_FeatureCentersJSON) == [list(c) for c in centers], "reopen_centers_" + name)
        check(obj.OLE_GeometryAuthority == "FREECAD_OCCT_BREP", "reopen_authority_" + name)
        check(close(obj.OLE_RadiusMM, RADIUS), "reopen_radius_" + name)
    App.closeDocument(reopened.Name)

    stage("DISPLAY")
    display = {
        "schema": "OLEANDER_BOUNDED_PATTERN_MIRROR_DISPLAY_v0.1",
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_OCCT_BREP",
        "display_authority": "DISPLAY_DERIVATIVE_ONLY",
        "units": "mm",
        "source_fcstd": FCSTD.name,
        "source_fcstd_sha256": sha256(FCSTD),
        "revisions": [
            display_record("R001_LINEAR_PATTERN", pattern, pattern_centers, "BRep_BOOLEAN_CUT_LINEAR_FEATURE_PATTERN", p_params, STEP_PATTERN),
            display_record("R002_MIRROR", mirror, mirror_centers, "BRep_BOOLEAN_CUT_MIRRORED_FEATURE", m_params, STEP_MIRROR),
        ],
    }
    DISPLAY.write_text(json.dumps(display, indent=2, sort_keys=True), encoding="utf-8")
    manifest = {
        "schema": "OLEANDER_FREECAD_BOUNDED_PATTERN_MIRROR_v0.1",
        "status": "PASS",
        "units": "mm",
        "authority": {"geometry_master": "FREECAD_OCCT_BREP", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "R001": {"operation": "LINEAR_FEATURE_PATTERN", "centers_mm": pattern_centers, "count": 3, "spacing_mm": 30.0, "metrics": metrics(pattern)},
        "R002": {"operation": "MIRRORED_FEATURE", "centers_mm": mirror_centers, "mirror_plane_x_mm": 60.0, "metrics": metrics(mirror)},
        "expected_failure_cases": failures,
        "artifacts": {
            "fcstd": {"path": FCSTD.name, "sha256": sha256(FCSTD)},
            "step_R001": {"path": STEP_PATTERN.name, "sha256": sha256(STEP_PATTERN)},
            "step_R002": {"path": STEP_MIRROR.name, "sha256": sha256(STEP_MIRROR)},
            "display": {"path": DISPLAY.name, "sha256": sha256(DISPLAY)},
        },
        "checks": checks,
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "general_feature_pattern_semantics",
            "circular_or_path_pattern",
            "general_mirror_semantics",
            "persistent_topological_naming",
            "assembly_pattern",
            "production_direct_modeling_parity"
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    stage("PASS")
    print("OLEANDER_FREECAD_BOUNDED_PATTERN_MIRROR=" + json.dumps(manifest, sort_keys=True), flush=True)


if __name__ == "__main__":
    stage("START")
    try:
        main()
    except BaseException as exc:
        print("OLEANDER_PATTERN_MIRROR_EXCEPTION=" + repr(exc), flush=True)
        traceback.print_exc()
        raise
