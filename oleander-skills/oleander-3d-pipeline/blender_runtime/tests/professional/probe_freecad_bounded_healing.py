"""OLEANDER bounded FreeCAD/OCCT B-Rep healing foundation.

This probe validates two repair/cleanup classes that the kernel can actually
support deterministically:
1) coincident but disconnected boundary faces -> sew into one closed shell/solid;
2) valid fused solid with redundant splitter topology -> removeSplitter while
   preserving geometry and volume.

Nonzero geometric-gap repair is explicitly rejected and remains unproven.
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
STEP_SEWN = OUT / "oleander_bounded_healing_sewn_R002.step"
STEP_REFINED = OUT / "oleander_bounded_healing_refined_R002.step"
DISPLAY = OUT / "oleander_bounded_healing_display.json"
MANIFEST = OUT / "oleander_bounded_healing_manifest.json"
SEW_TOL_MM = 1.0e-6
UNSUPPORTED_GAP_MM = 0.0005
TOL = 1e-8
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


def metrics(shape):
    return {
        "shape_type": shape.ShapeType,
        "bbox_mm": [shape.BoundBox.XLength, shape.BoundBox.YLength, shape.BoundBox.ZLength],
        "volume_mm3": shape.Volume,
        "solid_count": len(shape.Solids),
        "shell_count": len(shape.Shells),
        "face_count": len(shape.Faces),
        "edge_count": len(shape.Edges),
        "is_valid": bool(shape.isValid()),
    }


def make_disconnected_face_compound(width_mm: float):
    source = Part.makeBox(width_mm, 50.0, 10.0)
    check(source.isValid() and len(source.Solids) == 1, "source_valid_single_solid")
    compound = Part.makeCompound([face.copy() for face in source.Faces])
    check(len(compound.Faces) == 6, "disconnected_six_faces")
    check(len(compound.Solids) == 0, "disconnected_has_no_solid")
    check(close(compound.BoundBox.XLength, width_mm), "disconnected_width")
    check(close(compound.BoundBox.YLength, 50.0), "disconnected_depth")
    check(close(compound.BoundBox.ZLength, 10.0), "disconnected_height")
    return source, compound


def sew_coincident_faces(compound):
    work = compound.copy()
    work.sewShape(SEW_TOL_MM)
    try:
        work.fix(1e-7, 1e-7, 1e-7)
    except TypeError:
        work.fix()
    work = work.removeSplitter()

    if len(work.Solids) == 1 and work.isValid():
        solid = work.Solids[0]
    else:
        shells = list(work.Shells)
        check(len(shells) == 1, "sewn_exactly_one_shell")
        shell = shells[0]
        check(shell.isValid(), "sewn_shell_valid")
        solid = Part.makeSolid(shell).removeSplitter()

    check(solid.isValid(), "sewn_solid_valid")
    check(len(solid.Solids) == 1, "sewn_single_solid")
    check(len(solid.Faces) == 6, "sewn_six_faces")
    return solid


def make_redundant_splitter_solid(width_mm: float):
    split_x = width_mm * 0.5
    left = Part.makeBox(split_x, 50.0, 10.0)
    right = Part.makeBox(width_mm - split_x, 50.0, 10.0, App.Vector(split_x, 0.0, 0.0))
    fused = left.fuse(right)
    check(fused.isValid() and len(fused.Solids) == 1, "raw_fuse_valid_single_solid")
    return fused


def refine_splitter_topology(raw, width_mm: float):
    refined = raw.removeSplitter()
    check(refined.isValid(), "refined_shape_valid")
    check(len(refined.Solids) == 1, "refined_single_solid")
    check(close(refined.BoundBox.XLength, width_mm), "refined_width_preserved")
    check(close(refined.BoundBox.YLength, 50.0), "refined_depth_preserved")
    check(close(refined.BoundBox.ZLength, 10.0), "refined_height_preserved")
    check(close(refined.Volume, raw.Volume, 1e-5), "refined_volume_preserved")
    check(len(refined.Faces) <= len(raw.Faces), "refined_face_count_not_increased")
    check(len(refined.Edges) <= len(raw.Edges), "refined_edge_count_not_increased")
    check(len(refined.Faces) < len(raw.Faces) or len(refined.Edges) < len(raw.Edges), "redundant_topology_actually_reduced")
    return refined


def reject_nonzero_gap_repair(gap_mm: float):
    if gap_mm > 0:
        raise ValueError("nonzero geometric-gap repair is outside the bounded healing contract")


def run_revision(width_mm: float, revision: int):
    source, disconnected = make_disconnected_face_compound(width_mm)
    sewn = sew_coincident_faces(disconnected)
    check(close(sewn.BoundBox.XLength, width_mm), f"r{revision}_sewn_width")
    check(close(sewn.BoundBox.YLength, 50.0), f"r{revision}_sewn_depth")
    check(close(sewn.BoundBox.ZLength, 10.0), f"r{revision}_sewn_height")
    check(close(sewn.Volume, source.Volume, 1e-5), f"r{revision}_sewn_volume")

    raw = make_redundant_splitter_solid(width_mm)
    refined = refine_splitter_topology(raw, width_mm)
    check(close(refined.Volume, source.Volume, 1e-5), f"r{revision}_refined_matches_source_volume")
    return source, disconnected, sewn, raw, refined


def add_feature(doc, name, ole_id, shape, operation):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = shape
    for prop, value in [
        ("OLE_ID", ole_id),
        ("OLE_Operation", operation),
        ("OLE_GeometryAuthority", "FREECAD_OCCT_BREP"),
        ("OLE_HealingUnits", "mm"),
        ("OLE_GapRepairState", "NOT_VALIDATED"),
    ]:
        obj.addProperty("App::PropertyString", prop, "OLEANDER")
        setattr(obj, prop, value)
    obj.addProperty("App::PropertyFloat", "OLE_SewToleranceMM", "OLEANDER")
    obj.OLE_SewToleranceMM = SEW_TOL_MM
    return obj


def tessellate(shape):
    verts, tris = shape.tessellate(0.25)
    check(bool(verts) and bool(tris), "display_tessellation")
    return {
        "vertices_mm": [[v.x, v.y, v.z] for v in verts],
        "triangles": [list(t) for t in tris],
        "bbox_mm": metrics(shape)["bbox_mm"],
        "volume_mm3": shape.Volume,
    }


def main() -> None:
    s1, d1, sewn1, raw1, ref1 = run_revision(80.0, 1)
    s2, d2, sewn2, raw2, ref2 = run_revision(100.0, 2)
    check(len(d1.Solids) == 0 and len(d2.Solids) == 0, "both_disconnected_inputs_have_no_solid")
    check(sewn1.isValid() and sewn2.isValid(), "both_sewn_revisions_valid")
    check(ref1.isValid() and ref2.isValid(), "both_refined_revisions_valid")

    unsupported = "FAIL"
    try:
        reject_nonzero_gap_repair(UNSUPPORTED_GAP_MM)
    except ValueError as exc:
        if "outside the bounded healing contract" in str(exc):
            unsupported = "PASS"
            checks.append("nonzero_gap_repair_expected_failure")
    check(unsupported == "PASS", "nonzero_gap_repair_failure_gate")

    doc = App.newDocument("OLEANDER_BOUNDED_HEALING")
    sewn_obj = add_feature(doc, "OLE_SEWN_R002", "OLE_BREP_HEAL::SEWN_R002", sewn2, "SEW_COINCIDENT_BOUNDARY_FACES")
    refined_obj = add_feature(doc, "OLE_REFINED_R002", "OLE_BREP_HEAL::REFINED_R002", ref2, "REMOVE_REDUNDANT_SPLITTER_TOPOLOGY")
    doc.recompute()
    doc.saveAs(str(FCSTD))
    sewn_obj.Shape.exportStep(str(STEP_SEWN))
    refined_obj.Shape.exportStep(str(STEP_REFINED))
    check(FCSTD.exists() and STEP_SEWN.exists() and STEP_REFINED.exists(), "native_healing_artifacts_written")

    display = {
        "schema": "OLEANDER_BOUNDED_HEALING_DISPLAY_v0.2",
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_OCCT_BREP",
        "display_authority": "DISPLAY_DERIVATIVE_ONLY",
        "units": "mm",
        "ole_id": "OLE_BREP_HEAL::SEWN_R002",
        "operation": "SEW_COINCIDENT_BOUNDARY_FACES",
        "sewing_tolerance_mm": SEW_TOL_MM,
        "gap_repair_state": "NOT_VALIDATED",
        "source_fcstd": str(FCSTD),
        "source_fcstd_sha256": sha256(FCSTD),
        "source_step": str(STEP_SEWN),
        "source_step_sha256": sha256(STEP_SEWN),
        "refined_step": str(STEP_REFINED),
        "refined_step_sha256": sha256(STEP_REFINED),
        **tessellate(sewn2),
    }
    DISPLAY.write_text(json.dumps(display, sort_keys=True), encoding="utf-8")
    check(DISPLAY.exists() and DISPLAY.stat().st_size > 0, "healing_display_written")

    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(FCSTD))
    for name, ole_id, operation in [
        ("OLE_SEWN_R002", "OLE_BREP_HEAL::SEWN_R002", "SEW_COINCIDENT_BOUNDARY_FACES"),
        ("OLE_REFINED_R002", "OLE_BREP_HEAL::REFINED_R002", "REMOVE_REDUNDANT_SPLITTER_TOPOLOGY"),
    ]:
        obj = reopened.getObject(name)
        check(obj is not None, f"{name}_reopen")
        check(obj.OLE_ID == ole_id, f"{name}_ole_id_reopen")
        check(obj.OLE_Operation == operation, f"{name}_operation_reopen")
        check(obj.OLE_GeometryAuthority == "FREECAD_OCCT_BREP", f"{name}_authority_reopen")
        check(obj.OLE_HealingUnits == "mm", f"{name}_units_reopen")
        check(obj.OLE_GapRepairState == "NOT_VALIDATED", f"{name}_gap_state_reopen")
        check(close(float(obj.OLE_SewToleranceMM), SEW_TOL_MM, 1e-12), f"{name}_tolerance_reopen")
        check(obj.Shape.isValid() and len(obj.Shape.Solids) == 1, f"{name}_solid_reopen")

    result = {
        "schema": "OLEANDER_FREECAD_BOUNDED_HEALING_v0.2",
        "status": "PASS",
        "dependency_state": "RUNTIME_PROBED",
        "freecad_version": ".".join(str(x) for x in App.Version()[:3]),
        "occ_version": getattr(Part, "OCC_VERSION", "unknown"),
        "healing_contract": {
            "sewing_case": "six coincident but disconnected boundary faces",
            "sewing_tolerance_mm": SEW_TOL_MM,
            "sewing_pipeline": ["sewShape(tolerance)", "fix", "removeSplitter", "makeSolid when required"],
            "topology_cleanup_case": "valid fused solid with redundant splitter topology",
            "topology_cleanup_pipeline": ["removeSplitter"],
            "nonzero_gap_repair": "NOT_VALIDATED_AND_REJECTED"
        },
        "revision1": {
            "source": metrics(s1), "disconnected": metrics(d1), "sewn": metrics(sewn1),
            "raw_fused": metrics(raw1), "refined": metrics(ref1)
        },
        "revision2": {
            "source": metrics(s2), "disconnected": metrics(d2), "sewn": metrics(sewn2),
            "raw_fused": metrics(raw2), "refined": metrics(ref2)
        },
        "expected_failure_cases": {"nonzero_geometric_gap_repair": unsupported},
        "artifacts": {
            "fcstd": {"path": str(FCSTD), "sha256": sha256(FCSTD)},
            "sewn_step": {"path": str(STEP_SEWN), "sha256": sha256(STEP_SEWN)},
            "refined_step": {"path": str(STEP_REFINED), "sha256": sha256(STEP_REFINED)},
            "display": {"path": str(DISPLAY), "sha256": sha256(DISPLAY)}
        },
        "checks": checks,
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS", "general_brep_healing", "nonzero_gap_repair",
            "arbitrary_import_repair", "large_gap_repair", "self_intersection_repair",
            "nonmanifold_repair", "topological_naming_stability", "manufacturing_release"
        ]
    }
    MANIFEST.write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
    print("OLEANDER_FREECAD_BOUNDED_HEALING=" + json.dumps(result, sort_keys=True))


main()
