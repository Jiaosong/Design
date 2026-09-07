"""OLEANDER bounded semantic-reference-bound FreeCAD/OCCT B-Rep operation.

A stable OLE face reference is re-resolved on each authoritative source revision.
The resolved unique primary +Z planar face then drives an actual cylinder-cut
operation using its center and normal. Dimensional changes, outer-edge filleting,
one bounded inner-wire topology mutation, and one bounded raised-boss topology
mutation change geometry/topology signatures, but the same semantic ref ID binds
the correct operation. Ambiguous or missing resolution returns HOLD with zero
mutation.

The v0.3 selector deliberately identifies the unique largest-area +Z planar face,
rather than requiring the referenced face itself to remain at global Zmax. This
lets a small raised boss exist above the primary face without stealing the
reference. Equal-area ties remain ambiguous and fail closed.

This is stronger than metadata-only rebind, but is not persistent topological
naming parity or general face-reference stability.
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

OUT = Path(os.environ.get("OLEANDER_REF_OPERATION_DIR", "/tmp/oleander-reference-operation"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_reference_bound_operation.FCStd"
STEP_R001 = OUT / "oleander_reference_bound_operation_R001.step"
STEP_R002 = OUT / "oleander_reference_bound_operation_R002.step"
STEP_R003 = OUT / "oleander_reference_bound_operation_R003.step"
STEP_R004 = OUT / "oleander_reference_bound_operation_R004.step"
STEP_R005 = OUT / "oleander_reference_bound_operation_R005.step"
REGISTRY = OUT / "oleander_reference_bound_operation_registry.json"
DISPLAY = OUT / "oleander_reference_bound_operation_display.json"
MANIFEST = OUT / "oleander_reference_bound_operation_manifest.json"
TOL = 1e-7
checks: list[str] = []

REF_ID = "OLE_REF::PRIMARY_TOP_FACE"
SELECTOR_ID = "SELECTOR::UNIQUE_LARGEST_AREA_PLANAR_POSITIVE_Z"
OP_ID = "OLE_OP::TOP_FACE_CENTER_THROUGH_HOLE"
RADIUS_MM = 3.0
INNER_WIRE_RADIUS_MM = 4.0
INNER_WIRE_CENTER_MM = (20.0, 15.0)
BOSS_ORIGIN_MM = (70.0, 30.0, 10.0)
BOSS_SIZE_MM = (20.0, 12.0, 4.0)


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def stage(label: str) -> None:
    print("OLEANDER_REF_OPERATION_STAGE=" + label, flush=True)


def canonical_sha(payload) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


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


def descriptor(face):
    n = face_normal(face)
    c = face.CenterOfMass
    payload = {
        "surface_class": type(face.Surface).__name__,
        "center_mm": [round(c.x, 9), round(c.y, 9), round(c.z, 9)],
        "normal": [round(n.x, 9), round(n.y, 9), round(n.z, 9)],
        "area_mm2": round(face.Area, 9),
        "edge_count": len(face.Edges),
        "edge_lengths_mm": sorted(round(e.Length, 9) for e in face.Edges),
        "bbox_mm": [round(face.BoundBox.XLength, 9), round(face.BoundBox.YLength, 9), round(face.BoundBox.ZLength, 9)],
        "z_level_mm": round(c.z, 9),
    }
    return payload, canonical_sha(payload)


def reference_template():
    return {
        "schema": "OLEANDER_BREP_OPERATION_REFERENCE_v0.3",
        "ref_id": REF_ID,
        "selector": {
            "selector_id": SELECTOR_ID,
            "kind": "LARGEST_AREA_PLANAR_FACE",
            "normal_target": [0.0, 0.0, 1.0],
            "area_rank": "MAX",
            "uniqueness_required": True,
            "tie_rule": "equal-largest-area -> AMBIGUOUS_HOLD",
        },
        "prohibited_persistence": ["FaceN", "EdgeN", "VertexN", "subshape_ordinal"],
        "last_good_signature": None,
        "history": [],
        "operation_history": [],
    }


def resolve(shape, reference, revision_id):
    eligible = []
    for face in shape.Faces:
        bb = face.BoundBox
        if bb.ZLength > TOL:
            continue
        try:
            n = face_normal(face)
        except Exception:
            continue
        if abs(n.x) <= 1e-6 and abs(n.y) <= 1e-6 and n.z > 0.999999:
            desc, signature = descriptor(face)
            eligible.append((face, desc, signature))

    event = {
        "revision_id": revision_id,
        "ref_id": REF_ID,
        "selector_id": SELECTOR_ID,
        "eligible_count": len(eligible),
    }
    if not eligible:
        event["state"] = "MISSING_HOLD"
        event["candidate_count"] = 0
        reference["history"].append(event)
        return None, event

    max_area = max(item[0].Area for item in eligible)
    area_tol = max(1e-6, abs(max_area) * 1e-9)
    candidates = [item for item in eligible if abs(item[0].Area - max_area) <= area_tol]
    event["max_area_mm2"] = max_area
    event["candidate_count"] = len(candidates)
    event["eligible_signatures"] = sorted(item[2] for item in eligible)

    if len(candidates) > 1:
        event["state"] = "AMBIGUOUS_HOLD"
        event["candidate_signatures"] = sorted(item[2] for item in candidates)
        reference["history"].append(event)
        return None, event

    face, desc, signature = candidates[0]
    previous = reference.get("last_good_signature")
    event.update(
        {
            "state": "RESOLVED_INITIAL"
            if previous is None
            else ("REBOUND_SAME_SIGNATURE" if previous == signature else "REBOUND_CHANGED_SIGNATURE"),
            "signature": signature,
            "descriptor": desc,
        }
    )
    reference["last_good_signature"] = signature
    reference["history"].append(event)
    return face, event


def vertical_edges(shape):
    zspan = shape.BoundBox.ZLength
    found = []
    for edge in shape.Edges:
        verts = edge.Vertexes
        if len(verts) != 2:
            continue
        a, b = verts[0].Point, verts[1].Point
        if abs(a.x - b.x) <= TOL and abs(a.y - b.y) <= TOL and abs(abs(a.z - b.z) - zspan) <= TOL:
            found.append(edge)
    return found


def apply_bound_hole(shape, reference, revision_id):
    source_volume = shape.Volume
    face, event = resolve(shape, reference, revision_id)
    if face is None:
        operation = {
            "revision_id": revision_id,
            "operation_id": OP_ID,
            "ref_id": REF_ID,
            "selector_id": SELECTOR_ID,
            "state": event["state"],
            "candidate_count": event["candidate_count"],
            "eligible_count": event.get("eligible_count", 0),
            "mutation": "NONE",
            "source_volume_mm3": source_volume,
            "result_volume_mm3": source_volume,
        }
        reference["operation_history"].append(operation)
        return shape.copy(), operation

    center = face.CenterOfMass
    normal = face_normal(face)
    check(normal.z > 0.999999, "resolved_face_positive_z_normal")
    material_depth = center.z - shape.BoundBox.ZMin
    check(material_depth > RADIUS_MM, "resolved_face_has_positive_material_depth")
    origin = center + normal * 2.0
    cutter = Part.makeCylinder(RADIUS_MM, material_depth + 4.0, origin, -normal)
    result = shape.cut(cutter).removeSplitter()
    check(result.isValid() and len(result.Solids) == 1, "reference_bound_cut_valid_single_solid")
    check(result.Volume < source_volume, "reference_bound_cut_reduces_volume")
    expected_removed = math.pi * RADIUS_MM * RADIUS_MM * material_depth
    actual_removed = source_volume - result.Volume
    check(abs(actual_removed - expected_removed) <= 1e-3, "through_hole_removed_volume")

    operation = {
        "revision_id": revision_id,
        "operation_id": OP_ID,
        "ref_id": REF_ID,
        "selector_id": SELECTOR_ID,
        "state": "APPLIED",
        "resolved_signature": event["signature"],
        "resolved_descriptor": event["descriptor"],
        "resolved_center_mm": [center.x, center.y, center.z],
        "resolved_normal": [normal.x, normal.y, normal.z],
        "radius_mm": RADIUS_MM,
        "material_depth_mm": material_depth,
        "source_zmin_mm": shape.BoundBox.ZMin,
        "source_zmax_mm": shape.BoundBox.ZMax,
        "cutter_origin_mm": [origin.x, origin.y, origin.z],
        "cutter_direction": [-normal.x, -normal.y, -normal.z],
        "source_volume_mm3": source_volume,
        "result_volume_mm3": result.Volume,
        "removed_volume_mm3": actual_removed,
    }
    reference["operation_history"].append(operation)
    return result, operation


def metrics(shape):
    return {
        "bbox_mm": [shape.BoundBox.XLength, shape.BoundBox.YLength, shape.BoundBox.ZLength],
        "volume_mm3": shape.Volume,
        "solid_count": len(shape.Solids),
        "face_count": len(shape.Faces),
        "edge_count": len(shape.Edges),
    }


def add_feature(doc, name, shape, op):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = shape
    for prop, value in [
        ("OLE_ID", "OLE_REFERENCE_BOUND_OPERATION::" + name),
        ("OLE_OperationID", OP_ID),
        ("OLE_RefID", REF_ID),
        ("OLE_SelectorID", SELECTOR_ID),
        ("OLE_ResolvedSignature", op["resolved_signature"]),
        ("OLE_GeometryAuthority", "FREECAD_OCCT_BREP"),
    ]:
        obj.addProperty("App::PropertyString", prop, "OLEANDER")
        setattr(obj, prop, value)
    obj.addProperty("App::PropertyFloat", "OLE_RadiusMM", "OLEANDER")
    obj.OLE_RadiusMM = RADIUS_MM
    obj.addProperty("App::PropertyFloat", "OLE_MaterialDepthMM", "OLEANDER")
    obj.OLE_MaterialDepthMM = float(op["material_depth_mm"])
    return obj


def display_record(name, shape, op, step):
    verts, facets = shape.tessellate(0.25)
    check(bool(verts) and bool(facets), "display_tessellation_" + name)
    return {
        "revision": name,
        "ole_id": "OLE_REFERENCE_BOUND_OPERATION::" + name,
        "operation_id": OP_ID,
        "ref_id": REF_ID,
        "selector_id": SELECTOR_ID,
        "resolved_signature": op["resolved_signature"],
        "resolved_descriptor": op["resolved_descriptor"],
        "resolved_center_mm": op["resolved_center_mm"],
        "radius_mm": RADIUS_MM,
        "material_depth_mm": op["material_depth_mm"],
        "source_zmin_mm": op["source_zmin_mm"],
        "source_zmax_mm": op["source_zmax_mm"],
        "bbox_mm": metrics(shape)["bbox_mm"],
        "volume_mm3": shape.Volume,
        "vertices_mm": [[v.x, v.y, v.z] for v in verts],
        "triangles": [list(f) for f in facets],
        "source_step": step.name,
        "source_step_sha256": sha256(step),
    }


def main():
    ref = reference_template()

    stage("R001")
    r1_source = Part.makeBox(80.0, 50.0, 10.0)
    r1, op1 = apply_bound_hole(r1_source, ref, "R001_BASE_80")
    check(op1["state"] == "APPLIED", "r1_operation_applied")
    sig1 = op1["resolved_signature"]
    check(abs(op1["resolved_center_mm"][0] - 40.0) <= TOL, "r1_center_tracks_width")

    stage("R002")
    r2_source = Part.makeBox(100.0, 50.0, 10.0)
    r2, op2 = apply_bound_hole(r2_source, ref, "R002_WIDTH_100")
    check(op2["state"] == "APPLIED", "r2_operation_applied")
    check(op2["resolved_signature"] != sig1, "r2_signature_changed")
    check(abs(op2["resolved_center_mm"][0] - 50.0) <= TOL, "r2_center_rebound_after_width_change")
    sig2 = op2["resolved_signature"]

    stage("R003")
    vedges = vertical_edges(r2_source)
    check(len(vedges) == 4, "r3_vertical_edges_selected")
    r3_source = r2_source.makeFillet(2.0, vedges)
    check(r3_source.isValid() and len(r3_source.Solids) == 1, "r3_source_fillet_valid")
    r3, op3 = apply_bound_hole(r3_source, ref, "R003_VERTICAL_FILLET")
    check(op3["state"] == "APPLIED", "r3_operation_applied_after_topology_change")
    check(op3["resolved_signature"] != sig2, "r3_signature_changed_after_fillet")
    check(
        abs(op3["resolved_center_mm"][0] - 50.0) <= 1e-6
        and abs(op3["resolved_center_mm"][1] - 25.0) <= 1e-6,
        "r3_center_semantics_preserved",
    )

    stage("R004_INNER_WIRE")
    secondary_hole = Part.makeCylinder(
        INNER_WIRE_RADIUS_MM,
        12.0,
        App.Vector(INNER_WIRE_CENTER_MM[0], INNER_WIRE_CENTER_MM[1], -1.0),
        App.Vector(0.0, 0.0, 1.0),
    )
    r4_source = r2_source.cut(secondary_hole).removeSplitter()
    check(r4_source.isValid() and len(r4_source.Solids) == 1, "r4_inner_wire_source_valid_single_solid")
    check(len(r4_source.Faces) > len(r2_source.Faces), "r4_source_topology_changed")
    r4, op4 = apply_bound_hole(r4_source, ref, "R004_TOP_FACE_INNER_WIRE")
    check(op4["state"] == "APPLIED", "r4_operation_applied_after_inner_wire_topology")
    check(op4["resolved_signature"] != op3["resolved_signature"], "r4_signature_changed_after_inner_wire")
    check(op4["resolved_descriptor"]["edge_count"] >= 5, "r4_resolved_top_face_has_inner_wire_edges")
    check(op4["resolved_descriptor"]["area_mm2"] < 100.0 * 50.0, "r4_resolved_top_face_area_reduced")
    rect_area = 100.0 * 50.0
    hole_area = math.pi * INNER_WIRE_RADIUS_MM * INNER_WIRE_RADIUS_MM
    expected_x = (rect_area * 50.0 - hole_area * INNER_WIRE_CENTER_MM[0]) / (rect_area - hole_area)
    expected_y = (rect_area * 25.0 - hole_area * INNER_WIRE_CENTER_MM[1]) / (rect_area - hole_area)
    check(abs(op4["resolved_center_mm"][0] - expected_x) <= 1e-5, "r4_center_tracks_inner_wire_centroid_x")
    check(abs(op4["resolved_center_mm"][1] - expected_y) <= 1e-5, "r4_center_tracks_inner_wire_centroid_y")
    check(abs(op4["resolved_center_mm"][2] - 10.0) <= TOL, "r4_center_remains_top_z")

    stage("R005_RAISED_BOSS")
    boss = Part.makeBox(
        BOSS_SIZE_MM[0],
        BOSS_SIZE_MM[1],
        BOSS_SIZE_MM[2],
        App.Vector(BOSS_ORIGIN_MM[0], BOSS_ORIGIN_MM[1], BOSS_ORIGIN_MM[2]),
    )
    r5_source = r2_source.fuse(boss).removeSplitter()
    check(r5_source.isValid() and len(r5_source.Solids) == 1, "r5_boss_source_valid_single_solid")
    check(abs(r5_source.BoundBox.ZMax - 14.0) <= TOL, "r5_boss_raises_global_zmax")
    r5, op5 = apply_bound_hole(r5_source, ref, "R005_RAISED_BOSS_ABOVE_PRIMARY")
    check(op5["state"] == "APPLIED", "r5_operation_applied_with_higher_boss_face")
    check(op5["resolved_signature"] != op4["resolved_signature"], "r5_signature_changed_after_boss")
    check(abs(op5["resolved_center_mm"][2] - 10.0) <= TOL, "r5_primary_face_remains_base_z10")
    check(op5["source_zmax_mm"] > op5["resolved_center_mm"][2], "r5_selected_primary_not_global_zmax")
    boss_area = BOSS_SIZE_MM[0] * BOSS_SIZE_MM[1]
    boss_cx = BOSS_ORIGIN_MM[0] + BOSS_SIZE_MM[0] * 0.5
    boss_cy = BOSS_ORIGIN_MM[1] + BOSS_SIZE_MM[1] * 0.5
    primary_area = rect_area - boss_area
    expected_boss_x = (rect_area * 50.0 - boss_area * boss_cx) / primary_area
    expected_boss_y = (rect_area * 25.0 - boss_area * boss_cy) / primary_area
    check(abs(op5["resolved_center_mm"][0] - expected_boss_x) <= 1e-5, "r5_center_tracks_boss_void_centroid_x")
    check(abs(op5["resolved_center_mm"][1] - expected_boss_y) <= 1e-5, "r5_center_tracks_boss_void_centroid_y")
    check(abs(op5["material_depth_mm"] - 10.0) <= TOL, "r5_material_depth_uses_selected_face_not_bbox_height")
    check(op5["resolved_descriptor"]["area_mm2"] > boss_area, "r5_largest_area_selector_prefers_primary_face")

    stage("HOLDS")
    split_slot = Part.makeBox(6.0, 52.0, 6.0, App.Vector(47.0, -1.0, 5.0))
    split_amb_source = r2_source.cut(split_slot).removeSplitter()
    check(split_amb_source.isValid() and len(split_amb_source.Solids) == 1, "split_top_source_valid_single_solid")
    split_before = split_amb_source.Volume
    split_result, op_split = apply_bound_hole(split_amb_source, ref, "R006_SPLIT_TOP_AMBIGUOUS")
    split_event = ref["history"][-1]
    check(op_split["state"] == "AMBIGUOUS_HOLD" and op_split["mutation"] == "NONE", "split_top_ambiguous_hold_blocks_operation")
    check(op_split["candidate_count"] == 2 and split_event["candidate_count"] == 2, "split_top_exact_two_candidates")
    check(abs(split_result.Volume - split_before) <= TOL, "split_top_ambiguous_zero_mutation")

    amb_source = Part.makeCompound([Part.makeBox(40, 40, 10), Part.makeBox(40, 40, 10, App.Vector(60, 0, 0))])
    amb_before = amb_source.Volume
    amb_result, op_amb = apply_bound_hole(amb_source, ref, "R007_COMPOUND_AMBIGUOUS")
    check(op_amb["state"] == "AMBIGUOUS_HOLD" and op_amb["mutation"] == "NONE", "ambiguous_hold_blocks_operation")
    check(abs(amb_result.Volume - amb_before) <= TOL, "ambiguous_zero_mutation")

    missing_source = Part.makeSphere(10.0)
    missing_before = missing_source.Volume
    missing_result, op_missing = apply_bound_hole(missing_source, ref, "R008_MISSING")
    check(op_missing["state"] == "MISSING_HOLD" and op_missing["mutation"] == "NONE", "missing_hold_blocks_operation")
    check(abs(missing_result.Volume - missing_before) <= TOL, "missing_zero_mutation")
    check(ref["last_good_signature"] == op5["resolved_signature"], "holds_preserve_last_good_signature")

    registry_text = json.dumps(ref, indent=2, sort_keys=True)
    check(
        "Face1" not in registry_text and "Edge1" not in registry_text and "Vertex1" not in registry_text,
        "no_concrete_subshape_ordinal_persistence",
    )
    REGISTRY.write_text(registry_text, encoding="utf-8")

    stage("FCSTD")
    doc = App.newDocument("OLEANDER_REFERENCE_BOUND_OPERATION")
    o1 = add_feature(doc, "R001", r1, op1)
    o2 = add_feature(doc, "R002", r2, op2)
    o3 = add_feature(doc, "R003", r3, op3)
    o4 = add_feature(doc, "R004", r4, op4)
    o5 = add_feature(doc, "R005", r5, op5)
    ref_obj = doc.addObject("App::FeaturePython", "OLE_REFERENCE_REGISTRY")
    for prop, value in [
        ("OLE_RefID", REF_ID),
        ("OLE_SelectorID", SELECTOR_ID),
        ("OLE_LastGoodSignature", ref["last_good_signature"]),
        ("OLE_RegistryJSON", json.dumps(ref, sort_keys=True)),
        ("OLE_PersistenceBoundary", "NO_SUBSHAPE_ORDINALS;RE_RESOLVE_OR_HOLD;UNIQUE_LARGEST_POSITIVE_Z_PRIMARY_FACE"),
    ]:
        ref_obj.addProperty("App::PropertyString", prop, "OLEANDER")
        setattr(ref_obj, prop, value)
    doc.recompute()
    doc.saveAs(str(FCSTD))
    o1.Shape.exportStep(str(STEP_R001))
    o2.Shape.exportStep(str(STEP_R002))
    o3.Shape.exportStep(str(STEP_R003))
    o4.Shape.exportStep(str(STEP_R004))
    o5.Shape.exportStep(str(STEP_R005))
    check(
        FCSTD.exists()
        and STEP_R001.exists()
        and STEP_R002.exists()
        and STEP_R003.exists()
        and STEP_R004.exists()
        and STEP_R005.exists(),
        "native_artifacts_written",
    )
    App.closeDocument(doc.Name)

    reopened = App.openDocument(str(FCSTD))
    for name, op in [("R001", op1), ("R002", op2), ("R003", op3), ("R004", op4), ("R005", op5)]:
        obj = reopened.getObject(name)
        check(obj is not None and obj.Shape.isValid() and len(obj.Shape.Solids) == 1, "reopen_solid_" + name)
        check(
            obj.OLE_RefID == REF_ID
            and obj.OLE_SelectorID == SELECTOR_ID
            and obj.OLE_ResolvedSignature == op["resolved_signature"],
            "reopen_binding_" + name,
        )
        check(abs(float(obj.OLE_RadiusMM) - RADIUS_MM) <= TOL, "reopen_radius_" + name)
        check(abs(float(obj.OLE_MaterialDepthMM) - float(op["material_depth_mm"])) <= TOL, "reopen_material_depth_" + name)
    rr = reopened.getObject("OLE_REFERENCE_REGISTRY")
    check(rr.OLE_LastGoodSignature == op5["resolved_signature"], "registry_last_good_reopen")
    check(
        [x["state"] for x in json.loads(rr.OLE_RegistryJSON)["history"][-3:]]
        == ["AMBIGUOUS_HOLD", "AMBIGUOUS_HOLD", "MISSING_HOLD"],
        "registry_hold_history_reopen",
    )
    App.closeDocument(reopened.Name)

    stage("DISPLAY")
    display = {
        "schema": "OLEANDER_REFERENCE_BOUND_OPERATION_DISPLAY_v0.3",
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_OCCT_BREP",
        "display_authority": "DISPLAY_DERIVATIVE_ONLY",
        "source_fcstd": FCSTD.name,
        "source_fcstd_sha256": sha256(FCSTD),
        "ref_id": REF_ID,
        "selector_id": SELECTOR_ID,
        "operation_id": OP_ID,
        "registry": REGISTRY.name,
        "registry_sha256": sha256(REGISTRY),
        "revisions": [
            display_record("R001", r1, op1, STEP_R001),
            display_record("R002", r2, op2, STEP_R002),
            display_record("R003", r3, op3, STEP_R003),
            display_record("R004", r4, op4, STEP_R004),
            display_record("R005", r5, op5, STEP_R005),
        ],
    }
    DISPLAY.write_text(json.dumps(display, indent=2, sort_keys=True), encoding="utf-8")
    manifest = {
        "schema": "OLEANDER_FREECAD_REFERENCE_BOUND_OPERATION_v0.3",
        "status": "PASS",
        "dependency_state": "VALIDATED_FOR_BOUNDED_SCOPE",
        "authority": {"geometry_master": "FREECAD_OCCT_BREP", "blender": "DISPLAY_DERIVATIVE_ONLY"},
        "reference_contract": {
            "ref_id": REF_ID,
            "selector_id": SELECTOR_ID,
            "operation_id": OP_ID,
            "binding": "ref_id -> per-revision semantic largest-area +Z planar resolution -> resolved signature -> actual BRep cut",
            "failure_rule": "missing or equal-largest-area ambiguity -> HOLD and zero mutation",
            "ordinal_persistence": "PROHIBITED",
            "bounded_topology_extension": "primary +Z planar face may carry one bounded inner wire or sit below one smaller raised +Z boss face; unique largest area required",
        },
        "revision_operations": [op1, op2, op3, op4, op5, op_split, op_amb, op_missing],
        "positive_extension_cases": {
            "inner_wire_top_face_rebind_and_operation": "PASS",
            "raised_boss_above_primary_face_does_not_steal_reference": "PASS",
            "selected_face_material_depth_not_global_bbox_height": "PASS",
        },
        "expected_failure_cases": {
            "single_solid_equal_area_split_top_ambiguity_blocks_mutation": "PASS",
            "compound_equal_area_ambiguity_blocks_mutation": "PASS",
            "missing_reference_blocks_mutation": "PASS",
        },
        "artifacts": {
            "fcstd": {"path": FCSTD.name, "sha256": sha256(FCSTD)},
            "registry": {"path": REGISTRY.name, "sha256": sha256(REGISTRY)},
            "display": {"path": DISPLAY.name, "sha256": sha256(DISPLAY)},
            "step_R001": {"path": STEP_R001.name, "sha256": sha256(STEP_R001)},
            "step_R002": {"path": STEP_R002.name, "sha256": sha256(STEP_R002)},
            "step_R003": {"path": STEP_R003.name, "sha256": sha256(STEP_R003)},
            "step_R004": {"path": STEP_R004.name, "sha256": sha256(STEP_R004)},
            "step_R005": {"path": STEP_R005.name, "sha256": sha256(STEP_R005)},
        },
        "checks": checks,
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "persistent_topological_naming_parity",
            "general_face_reference_stability",
            "general_multi_wire_reference_stability",
            "general_split_face_reference_stability",
            "edge_reference_stability",
            "vertex_reference_stability",
            "nonplanar_semantic_reference_rebind",
            "automatic_ambiguous_reference_resolution",
            "general_largest_area_selector_correctness",
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    stage("PASS")
    print("OLEANDER_FREECAD_REFERENCE_BOUND_OPERATION=" + json.dumps(manifest, sort_keys=True), flush=True)


if __name__ == "__main__":
    stage("START")
    try:
        main()
    except BaseException as exc:
        print("OLEANDER_REF_OPERATION_EXCEPTION=" + repr(exc), flush=True)
        traceback.print_exc()
        raise
