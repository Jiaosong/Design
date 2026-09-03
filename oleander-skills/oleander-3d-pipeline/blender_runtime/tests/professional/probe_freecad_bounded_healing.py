"""OLEANDER bounded FreeCAD/OCCT B-Rep healing probe.

Creates a controlled open shell by lifting one planar face of a box by a small
gap. The pre-heal shape must contain no solid. A declared sewing tolerance may
repair only gaps within the governed healing budget; larger gaps are rejected
before kernel healing. This is not a claim of general B-Rep healing parity.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import FreeCAD as App
import Part

OUT = Path(os.environ.get("OLEANDER_HEAL_DIR", "/tmp/oleander-bounded-healing"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_bounded_healing.FCStd"
STEP = OUT / "oleander_bounded_healing_R002.step"
DISPLAY = OUT / "oleander_bounded_healing_display.json"
MANIFEST = OUT / "oleander_bounded_healing_manifest.json"
TOL = 1e-9
HEAL_TOL_MM = 0.001
SMALL_GAP_MM = 0.0005
LARGE_GAP_MM = 0.01
checks: list[str] = []


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def face_normal(face):
    try:
        u0, u1, v0, v1 = face.ParameterRange
        return face.normalAt((u0 + u1) * 0.5, (v0 + v1) * 0.5).normalize()
    except Exception:
        return face.normalAt(0, 0).normalize()


def select_top_face(shape):
    zmax = shape.BoundBox.ZMax
    found = []
    for face in shape.Faces:
        bb = face.BoundBox
        if bb.ZLength <= 1e-7 and abs(bb.ZMax - zmax) <= 1e-7 and face_normal(face).z > 0.999999:
            found.append(face)
    check(len(found) == 1, "unique_top_face")
    return found[0]


def make_gapped_face_compound(width_mm: float, gap_mm: float):
    base = Part.makeBox(width_mm, 50.0, 10.0)
    check(base.isValid() and len(base.Solids) == 1, "source_valid_single_solid")
    top = select_top_face(base)
    faces = []
    for face in base.Faces:
        copied = face.copy()
        if face.isSame(top):
            copied.translate(App.Vector(0.0, 0.0, gap_mm))
        faces.append(copied)
    damaged = Part.makeCompound(faces)
    check(len(damaged.Faces) == 6, "damaged_six_faces")
    check(len(damaged.Solids) == 0, "damaged_has_no_solid")
    check(damaged.BoundBox.ZLength > 10.0, "damaged_gap_visible_in_bbox")
    return base, damaged


def heal_preflight(gap_mm: float, tolerance_mm: float) -> None:
    if gap_mm <= 0:
        raise ValueError("healing gap must be positive")
    if gap_mm > tolerance_mm:
        raise ValueError("healing gap exceeds governed sewing tolerance")


def heal_compound(damaged, gap_mm: float, tolerance_mm: float):
    heal_preflight(gap_mm, tolerance_mm)
    work = damaged.copy()
    work.sewShape(tolerance_mm)
    try:
        work.fix(1e-7, 1e-7, 1e-7)
    except TypeError:
        work.fix()
    work = work.removeSplitter()

    if len(work.Solids) == 1 and work.isValid():
        solid = work.Solids[0]
    else:
        shells = list(work.Shells)
        check(len(shells) == 1, "healed_exactly_one_shell")
        shell = shells[0]
        try:
            shell.fix(1e-7, 1e-7, 1e-7)
        except TypeError:
            shell.fix()
        solid = Part.makeSolid(shell).removeSplitter()

    check(solid.isValid(), "healed_solid_valid")
    check(len(solid.Solids) == 1, "healed_single_solid")
    check(len(solid.Faces) == 6, "healed_six_faces")
    return solid


def metrics(shape):
    return {
        "bbox_mm": [shape.BoundBox.XLength, shape.BoundBox.YLength, shape.BoundBox.ZLength],
        "volume_mm3": shape.Volume,
        "solid_count": len(shape.Solids),
        "shell_count": len(shape.Shells),
        "face_count": len(shape.Faces),
        "edge_count": len(shape.Edges),
        "is_valid": bool(shape.isValid()),
    }


def run_revision(width_mm: float, revision: int):
    base, damaged = make_gapped_face_compound(width_mm, SMALL_GAP_MM)
    healed = heal_compound(damaged, SMALL_GAP_MM, HEAL_TOL_MM)
    check(abs(healed.BoundBox.XLength - width_mm) <= 1e-6, f"r{revision}_width_preserved")
    check(abs(healed.BoundBox.YLength - 50.0) <= 1e-6, f"r{revision}_depth_preserved")
    # Sewing is allowed to resolve the tiny top-face gap to either adjacent edge
    # tolerance or the translated face location. It must stay within the budget.
    check(abs(healed.BoundBox.ZLength - 10.0) <= HEAL_TOL_MM + 1e-6, f"r{revision}_height_within_healing_budget")
    expected_volume = width_mm * 50.0 * 10.0
    max_volume_delta = width_mm * 50.0 * HEAL_TOL_MM + 1e-3
    check(abs(healed.Volume - expected_volume) <= max_volume_delta, f"r{revision}_volume_within_healing_budget")
    return base, damaged, healed


def add_feature(doc, shape):
    obj = doc.addObject("PartDesign::Feature", "OLE_HEALED_R002")
    obj.Shape = shape
    for prop, value in [
        ("OLE_ID", "OLE_BREP_HEAL::R002"),
        ("OLE_Operation", "SEW_FIX_REMOVE_SPLITTER_MAKE_SOLID"),
        ("OLE_GeometryAuthority", "FREECAD_OCCT_BREP"),
        ("OLE_HealingUnits", "mm"),
    ]:
        obj.addProperty("App::PropertyString", prop, "OLEANDER")
        setattr(obj, prop, value)
    obj.addProperty("App::PropertyFloat", "OLE_SourceGapMM", "OLEANDER")
    obj.OLE_SourceGapMM = SMALL_GAP_MM
    obj.addProperty("App::PropertyFloat", "OLE_HealingToleranceMM", "OLEANDER")
    obj.OLE_HealingToleranceMM = HEAL_TOL_MM
    return obj


def tessellate(shape):
    verts, tris = shape.tessellate(0.25)
    check(bool(verts) and bool(tris), "display_tessellation")
    return {
        "vertices_mm": [[v.x, v.y, v.z] for v in verts],
        "triangles": [list(t) for t in tris],
    }


def main() -> None:
    b1, d1, h1 = run_revision(80.0, 1)
    b2, d2, h2 = run_revision(100.0, 2)
    check(len(d1.Solids) == 0 and len(d2.Solids) == 0, "both_damaged_revisions_have_no_solid")
    check(h1.isValid() and h2.isValid(), "both_healed_revisions_valid")

    failure = "FAIL"
    try:
        heal_preflight(LARGE_GAP_MM, HEAL_TOL_MM)
    except ValueError as exc:
        if "exceeds governed sewing tolerance" in str(exc):
            failure = "PASS"
            checks.append("over_tolerance_gap_expected_failure")
    check(failure == "PASS", "over_tolerance_failure_gate")

    doc = App.newDocument("OLEANDER_BOUNDED_HEALING")
    obj = add_feature(doc, h2)
    doc.recompute()
    doc.saveAs(str(FCSTD))
    obj.Shape.exportStep(str(STEP))
    check(FCSTD.exists() and STEP.exists(), "native_healing_artifacts_written")

    display = {
        "schema": "OLEANDER_BOUNDED_HEALING_DISPLAY_v0.1",
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_OCCT_BREP",
        "display_authority": "DISPLAY_DERIVATIVE_ONLY",
        "units": "mm",
        "ole_id": "OLE_BREP_HEAL::R002",
        "operation": "SEW_FIX_REMOVE_SPLITTER_MAKE_SOLID",
        "source_gap_mm": SMALL_GAP_MM,
        "healing_tolerance_mm": HEAL_TOL_MM,
        "source_fcstd": str(FCSTD),
        "source_fcstd_sha256": sha256(FCSTD),
        "source_step": str(STEP),
        "source_step_sha256": sha256(STEP),
        "bbox_mm": metrics(h2)["bbox_mm"],
        "volume_mm3": h2.Volume,
        **tessellate(h2),
    }
    DISPLAY.write_text(json.dumps(display, sort_keys=True), encoding="utf-8")
    check(DISPLAY.exists() and DISPLAY.stat().st_size > 0, "healing_display_written")

    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(FCSTD))
    r = reopened.getObject("OLE_HEALED_R002")
    check(r is not None, "healed_object_reopen")
    check(r.OLE_ID == "OLE_BREP_HEAL::R002", "healed_ole_id_reopen")
    check(r.OLE_Operation == "SEW_FIX_REMOVE_SPLITTER_MAKE_SOLID", "healing_operation_reopen")
    check(r.OLE_GeometryAuthority == "FREECAD_OCCT_BREP", "healing_authority_reopen")
    check(r.OLE_HealingUnits == "mm", "healing_units_reopen")
    check(close(float(r.OLE_SourceGapMM), SMALL_GAP_MM, 1e-12), "source_gap_reopen")
    check(close(float(r.OLE_HealingToleranceMM), HEAL_TOL_MM, 1e-12), "healing_tolerance_reopen")
    check(r.Shape.isValid() and len(r.Shape.Solids) == 1, "healed_solid_reopen")

    result = {
        "schema": "OLEANDER_FREECAD_BOUNDED_HEALING_v0.1",
        "status": "PASS",
        "dependency_state": "RUNTIME_PROBED",
        "freecad_version": ".".join(str(x) for x in App.Version()[:3]),
        "occ_version": getattr(Part, "OCC_VERSION", "unknown"),
        "healing_contract": {
            "source_defect": "one translated top planar face creating an open shell",
            "source_gap_mm": SMALL_GAP_MM,
            "sewing_tolerance_mm": HEAL_TOL_MM,
            "pipeline": ["sewShape(tolerance)", "fix", "removeSplitter", "makeSolid when required"],
            "over_tolerance_policy": "reject before healing"
        },
        "revision1": {"base": metrics(b1), "damaged": metrics(d1), "healed": metrics(h1)},
        "revision2": {"base": metrics(b2), "damaged": metrics(d2), "healed": metrics(h2)},
        "expected_failure_cases": {"gap_exceeds_governed_tolerance": failure},
        "artifacts": {
            "fcstd": {"path": str(FCSTD), "sha256": sha256(FCSTD)},
            "step": {"path": str(STEP), "sha256": sha256(STEP)},
            "display": {"path": str(DISPLAY), "sha256": sha256(DISPLAY)}
        },
        "checks": checks,
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "general_brep_healing",
            "arbitrary_import_repair",
            "large_gap_repair",
            "self_intersection_repair",
            "nonmanifold_repair",
            "topological_naming_stability",
            "manufacturing_release"
        ]
    }
    MANIFEST.write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
    print("OLEANDER_FREECAD_BOUNDED_HEALING=" + json.dumps(result, sort_keys=True))


main()
