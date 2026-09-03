"""OLEANDER bounded semantic-reference-bound FreeCAD/OCCT B-Rep operation.

A stable OLE face reference is re-resolved on each authoritative source revision.
The resolved unique global +Z top planar face then drives an actual cylinder-cut
operation using its center and normal. Width changes and a vertical-edge fillet
change the geometry/topology signature, but the same semantic ref ID binds the
correct operation. Ambiguous or missing resolution returns HOLD with no cut.

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
REGISTRY = OUT / "oleander_reference_bound_operation_registry.json"
DISPLAY = OUT / "oleander_reference_bound_operation_display.json"
MANIFEST = OUT / "oleander_reference_bound_operation_manifest.json"
TOL = 1e-7
checks: list[str] = []

REF_ID = "OLE_REF::PRIMARY_TOP_FACE"
SELECTOR_ID = "SELECTOR::UNIQUE_GLOBAL_ZMAX_PLANAR_POSITIVE_Z"
OP_ID = "OLE_OP::TOP_FACE_CENTER_THROUGH_HOLE"
RADIUS_MM = 3.0


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
    }
    return payload, canonical_sha(payload)


def reference_template():
    return {
        "schema": "OLEANDER_BREP_OPERATION_REFERENCE_v0.1",
        "ref_id": REF_ID,
        "selector": {
            "selector_id": SELECTOR_ID,
            "kind": "EXTREME_PLANAR_FACE",
            "extreme_axis": "Z",
            "extreme": "MAX",
            "normal_target": [0.0, 0.0, 1.0],
            "uniqueness_required": True,
        },
        "prohibited_persistence": ["FaceN", "EdgeN", "VertexN", "subshape_ordinal"],
        "last_good_signature": None,
        "history": [],
        "operation_history": [],
    }


def resolve(shape, reference, revision_id):
    zmax = shape.BoundBox.ZMax
    candidates = []
    for face in shape.Faces:
        bb = face.BoundBox
        if bb.ZLength > TOL or abs(bb.ZMax - zmax) > TOL:
            continue
        try:
            n = face_normal(face)
        except Exception:
            continue
        if abs(n.x) <= 1e-6 and abs(n.y) <= 1e-6 and n.z > 0.999999:
            desc, signature = descriptor(face)
            candidates.append((face, desc, signature))
    event = {"revision_id": revision_id, "ref_id": REF_ID, "selector_id": SELECTOR_ID, "candidate_count": len(candidates)}
    if len(candidates) == 0:
        event["state"] = "MISSING_HOLD"
        reference["history"].append(event)
        return None, event
    if len(candidates) > 1:
        event["state"] = "AMBIGUOUS_HOLD"
        event["candidate_signatures"] = sorted(x[2] for x in candidates)
        reference["history"].append(event)
        return None, event
    face, desc, signature = candidates[0]
    previous = reference.get("last_good_signature")
    event.update({"state": "RESOLVED_INITIAL" if previous is None else ("REBOUND_SAME_SIGNATURE" if previous == signature else "REBOUND_CHANGED_SIGNATURE"), "signature": signature, "descriptor": desc})
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
            "state": event["state"],
            "mutation": "NONE",
            "source_volume_mm3": source_volume,
            "result_volume_mm3": source_volume,
        }
        reference["operation_history"].append(operation)
        return shape.copy(), operation

    center = face.CenterOfMass
    normal = face_normal(face)
    check(normal.z > 0.999999, "resolved_face_positive_z_normal")
    length = shape.BoundBox.ZLength + 4.0
    origin = center + normal * 2.0
    cutter = Part.makeCylinder(RADIUS_MM, length, origin, -normal)
    result = shape.cut(cutter).removeSplitter()
    check(result.isValid() and len(result.Solids) == 1, "reference_bound_cut_valid_single_solid")
    check(result.Volume < source_volume, "reference_bound_cut_reduces_volume")
    expected_removed = math.pi * RADIUS_MM * RADIUS_MM * shape.BoundBox.ZLength
    actual_removed = source_volume - result.Volume
    check(abs(actual_removed - expected_removed) <= 1e-3, "through_hole_removed_volume")

    operation = {
        "revision_id": revision_id,
        "operation_id": OP_ID,
        "ref_id": REF_ID,
        "selector_id": SELECTOR_ID,
        "state": "APPLIED",
        "resolved_signature": event["signature"],
        "resolved_center_mm": [center.x, center.y, center.z],
        "resolved_normal": [normal.x, normal.y, normal.z],
        "radius_mm": RADIUS_MM,
        "cutter_origin_mm": [origin.x, origin.y, origin.z],
        "cutter_direction": [-normal.x, -normal.y, -normal.z],
        "source_volume_mm3": source_volume,
        "result_volume_mm3": result.Volume,
        "removed_volume_mm3": actual_removed,
    }
    reference["operation_history"].append(operation)
    return result, operation


def metrics(shape):
    return {"bbox_mm": [shape.BoundBox.XLength, shape.BoundBox.YLength, shape.BoundBox.ZLength], "volume_mm3": shape.Volume, "solid_count": len(shape.Solids), "face_count": len(shape.Faces), "edge_count": len(shape.Edges)}


def add_feature(doc, name, shape, op):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = shape
    for prop, value in [("OLE_ID", "OLE_REFERENCE_BOUND_OPERATION::" + name), ("OLE_OperationID", OP_ID), ("OLE_RefID", REF_ID), ("OLE_SelectorID", SELECTOR_ID), ("OLE_ResolvedSignature", op["resolved_signature"]), ("OLE_GeometryAuthority", "FREECAD_OCCT_BREP")]:
        obj.addProperty("App::PropertyString", prop, "OLEANDER")
        setattr(obj, prop, value)
    obj.addProperty("App::PropertyFloat", "OLE_RadiusMM", "OLEANDER")
    obj.OLE_RadiusMM = RADIUS_MM
    return obj


def display_record(name, shape, op, step):
    verts, facets = shape.tessellate(0.25)
    check(bool(verts) and bool(facets), "display_tessellation_" + name)
    return {"revision": name, "ole_id": "OLE_REFERENCE_BOUND_OPERATION::" + name, "operation_id": OP_ID, "ref_id": REF_ID, "selector_id": SELECTOR_ID, "resolved_signature": op["resolved_signature"], "resolved_center_mm": op["resolved_center_mm"], "radius_mm": RADIUS_MM, "bbox_mm": metrics(shape)["bbox_mm"], "volume_mm3": shape.Volume, "vertices_mm": [[v.x,v.y,v.z] for v in verts], "triangles": [list(f) for f in facets], "source_step": step.name, "source_step_sha256": sha256(step)}


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
    check(abs(op3["resolved_center_mm"][0] - 50.0) <= 1e-6 and abs(op3["resolved_center_mm"][1] - 25.0) <= 1e-6, "r3_center_semantics_preserved")

    stage("HOLDS")
    amb_source = Part.makeCompound([Part.makeBox(40,40,10), Part.makeBox(40,40,10,App.Vector(60,0,0))])
    amb_before = amb_source.Volume
    amb_result, op_amb = apply_bound_hole(amb_source, ref, "R004_AMBIGUOUS")
    check(op_amb["state"] == "AMBIGUOUS_HOLD" and op_amb["mutation"] == "NONE", "ambiguous_hold_blocks_operation")
    check(abs(amb_result.Volume - amb_before) <= TOL, "ambiguous_zero_mutation")
    missing_source = Part.makeSphere(10.0)
    missing_before = missing_source.Volume
    missing_result, op_missing = apply_bound_hole(missing_source, ref, "R005_MISSING")
    check(op_missing["state"] == "MISSING_HOLD" and op_missing["mutation"] == "NONE", "missing_hold_blocks_operation")
    check(abs(missing_result.Volume - missing_before) <= TOL, "missing_zero_mutation")
    check(ref["last_good_signature"] == op3["resolved_signature"], "holds_preserve_last_good_signature")

    registry_text = json.dumps(ref, indent=2, sort_keys=True)
    check("Face1" not in registry_text and "Edge1" not in registry_text, "no_concrete_subshape_ordinal_persistence")
    REGISTRY.write_text(registry_text, encoding="utf-8")

    stage("FCSTD")
    doc = App.newDocument("OLEANDER_REFERENCE_BOUND_OPERATION")
    o1, o2, o3 = add_feature(doc,"R001",r1,op1), add_feature(doc,"R002",r2,op2), add_feature(doc,"R003",r3,op3)
    ref_obj = doc.addObject("App::FeaturePython", "OLE_REFERENCE_REGISTRY")
    for prop, value in [("OLE_RefID",REF_ID),("OLE_SelectorID",SELECTOR_ID),("OLE_LastGoodSignature",ref["last_good_signature"]),("OLE_RegistryJSON",json.dumps(ref,sort_keys=True)),("OLE_PersistenceBoundary","NO_SUBSHAPE_ORDINALS;RE_RESOLVE_OR_HOLD")]:
        ref_obj.addProperty("App::PropertyString",prop,"OLEANDER"); setattr(ref_obj,prop,value)
    doc.recompute(); doc.saveAs(str(FCSTD)); o1.Shape.exportStep(str(STEP_R001)); o2.Shape.exportStep(str(STEP_R002)); o3.Shape.exportStep(str(STEP_R003))
    check(FCSTD.exists() and STEP_R001.exists() and STEP_R002.exists() and STEP_R003.exists(), "native_artifacts_written")
    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(FCSTD))
    for name, op in [("R001",op1),("R002",op2),("R003",op3)]:
        obj = reopened.getObject(name)
        check(obj is not None and obj.Shape.isValid() and len(obj.Shape.Solids)==1, "reopen_solid_"+name)
        check(obj.OLE_RefID==REF_ID and obj.OLE_SelectorID==SELECTOR_ID and obj.OLE_ResolvedSignature==op["resolved_signature"], "reopen_binding_"+name)
        check(abs(float(obj.OLE_RadiusMM)-RADIUS_MM)<=TOL, "reopen_radius_"+name)
    rr = reopened.getObject("OLE_REFERENCE_REGISTRY")
    check(rr.OLE_LastGoodSignature==op3["resolved_signature"], "registry_last_good_reopen")
    check([x["state"] for x in json.loads(rr.OLE_RegistryJSON)["history"][-2:]]==["AMBIGUOUS_HOLD","MISSING_HOLD"], "registry_hold_history_reopen")
    App.closeDocument(reopened.Name)

    stage("DISPLAY")
    display={"schema":"OLEANDER_REFERENCE_BOUND_OPERATION_DISPLAY_v0.1","master_type":"CAD_NATIVE","geometry_authority":"FREECAD_OCCT_BREP","display_authority":"DISPLAY_DERIVATIVE_ONLY","source_fcstd":FCSTD.name,"source_fcstd_sha256":sha256(FCSTD),"ref_id":REF_ID,"selector_id":SELECTOR_ID,"operation_id":OP_ID,"registry":REGISTRY.name,"registry_sha256":sha256(REGISTRY),"revisions":[display_record("R001",r1,op1,STEP_R001),display_record("R002",r2,op2,STEP_R002),display_record("R003",r3,op3,STEP_R003)]}
    DISPLAY.write_text(json.dumps(display,indent=2,sort_keys=True),encoding="utf-8")
    manifest={"schema":"OLEANDER_FREECAD_REFERENCE_BOUND_OPERATION_v0.1","status":"PASS","dependency_state":"VALIDATED_FOR_BOUNDED_SCOPE","authority":{"geometry_master":"FREECAD_OCCT_BREP","blender":"DISPLAY_DERIVATIVE_ONLY"},"reference_contract":{"ref_id":REF_ID,"selector_id":SELECTOR_ID,"operation_id":OP_ID,"binding":"ref_id -> per-revision semantic resolution -> resolved signature -> actual BRep cut","failure_rule":"ambiguous/missing -> HOLD and zero mutation","ordinal_persistence":"PROHIBITED"},"revision_operations":[op1,op2,op3,op_amb,op_missing],"expected_failure_cases":{"ambiguous_reference_blocks_mutation":"PASS","missing_reference_blocks_mutation":"PASS"},"artifacts":{"fcstd":{"path":FCSTD.name,"sha256":sha256(FCSTD)},"registry":{"path":REGISTRY.name,"sha256":sha256(REGISTRY)},"display":{"path":DISPLAY.name,"sha256":sha256(DISPLAY)},"step_R001":{"path":STEP_R001.name,"sha256":sha256(STEP_R001)},"step_R002":{"path":STEP_R002.name,"sha256":sha256(STEP_R002)},"step_R003":{"path":STEP_R003.name,"sha256":sha256(STEP_R003)}},"checks":checks,"non_claims":["P0_B_DIRECT_BREP_PASS","persistent_topological_naming_parity","general_face_reference_stability","edge_reference_stability","vertex_reference_stability","nonplanar_semantic_reference_rebind","automatic_ambiguous_reference_resolution"]}
    MANIFEST.write_text(json.dumps(manifest,indent=2,sort_keys=True),encoding="utf-8")
    stage("PASS"); print("OLEANDER_FREECAD_REFERENCE_BOUND_OPERATION="+json.dumps(manifest,sort_keys=True),flush=True)


if __name__=="__main__":
    stage("START")
    try: main()
    except BaseException as exc:
        print("OLEANDER_REF_OPERATION_EXCEPTION="+repr(exc),flush=True); traceback.print_exc(); raise
