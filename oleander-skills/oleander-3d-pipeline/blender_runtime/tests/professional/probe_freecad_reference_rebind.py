"""OLEANDER bounded semantic B-Rep reference rebind probe.

Persistent references are stable OLE reference IDs plus geometric selector
semantics and resolution signatures. No FaceN/EdgeN ordinal is persisted.
Every authoritative geometry revision re-resolves the selector. Zero or
multiple candidates return explicit HOLD states; the resolver never chooses a
first candidate silently. This is not persistent topological naming parity.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import FreeCAD as App
import Part

OUT = Path(os.environ.get("OLEANDER_REF_REBIND_DIR", "/tmp/oleander-reference-rebind"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_reference_rebind.FCStd"
REGISTRY = OUT / "oleander_reference_registry.json"
MANIFEST = OUT / "oleander_reference_rebind_manifest.json"
TOL = 1e-7
checks: list[str] = []


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    checks.append(label)


def canonical_sha(payload) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def face_normal(face):
    u0, u1, v0, v1 = face.ParameterRange
    n = face.normalAt((u0 + u1) * 0.5, (v0 + v1) * 0.5)
    n.normalize()
    return n


def descriptor(face):
    n = face_normal(face)
    c = face.CenterOfMass
    edge_lengths = sorted(round(edge.Length, 9) for edge in face.Edges)
    payload = {
        "surface_class": type(face.Surface).__name__,
        "center_mm": [round(c.x, 9), round(c.y, 9), round(c.z, 9)],
        "normal": [round(n.x, 9), round(n.y, 9), round(n.z, 9)],
        "area_mm2": round(face.Area, 9),
        "edge_count": len(face.Edges),
        "edge_lengths_mm": edge_lengths,
        "bbox_mm": [
            round(face.BoundBox.XLength, 9),
            round(face.BoundBox.YLength, 9),
            round(face.BoundBox.ZLength, 9),
        ],
    }
    return payload, canonical_sha(payload)


def resolve_top_planar(shape, reference, revision_id):
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

    event = {
        "revision_id": revision_id,
        "candidate_count": len(candidates),
        "selector_id": reference["selector"]["selector_id"],
    }
    previous = reference.get("last_signature")
    if len(candidates) == 0:
        event.update({"state": "MISSING_HOLD", "signature": None})
        reference["state"] = "MISSING_HOLD"
        reference["history"].append(event)
        return None, event
    if len(candidates) > 1:
        event.update({
            "state": "AMBIGUOUS_HOLD",
            "signature": None,
            "candidate_signatures": sorted(item[2] for item in candidates),
        })
        reference["state"] = "AMBIGUOUS_HOLD"
        reference["history"].append(event)
        return None, event

    face, desc, signature = candidates[0]
    if previous is None:
        state = "RESOLVED_INITIAL"
    elif previous == signature:
        state = "REBOUND_SAME_SIGNATURE"
    else:
        state = "REBOUND_CHANGED_SIGNATURE"
    event.update({"state": state, "signature": signature, "descriptor": desc})
    reference["state"] = state
    reference["last_signature"] = signature
    reference["last_descriptor"] = desc
    reference["history"].append(event)
    return face, event


def vertical_edges(shape):
    zspan = shape.BoundBox.ZLength
    edges = []
    for edge in shape.Edges:
        verts = edge.Vertexes
        if len(verts) != 2:
            continue
        a, b = verts[0].Point, verts[1].Point
        if abs(a.x-b.x) <= TOL and abs(a.y-b.y) <= TOL and abs(abs(a.z-b.z)-zspan) <= TOL:
            edges.append(edge)
    return edges


def reference_template():
    return {
        "schema": "OLEANDER_BREP_REFERENCE_v0.1",
        "ref_id": "OLE_REF::PRIMARY_TOP_FACE",
        "authority": "SEMANTIC_REFERENCE_METADATA",
        "selector": {
            "selector_id": "SELECTOR::UNIQUE_GLOBAL_ZMAX_PLANAR_POSITIVE_Z",
            "kind": "EXTREME_PLANAR_FACE",
            "extreme_axis": "Z",
            "extreme": "MAX",
            "normal_target": [0.0, 0.0, 1.0],
            "normal_dot_min": 0.999999,
            "uniqueness_required": True,
        },
        "prohibited_persistence": ["FaceN", "EdgeN", "VertexN", "subshape_ordinal"],
        "state": "UNRESOLVED",
        "last_signature": None,
        "last_descriptor": None,
        "history": [],
    }


def main() -> None:
    ref = reference_template()

    r1 = Part.makeBox(80.0, 50.0, 10.0)
    face1, ev1 = resolve_top_planar(r1, ref, "R001_BASE_80")
    check(face1 is not None, "r1_reference_resolved")
    check(ev1["state"] == "RESOLVED_INITIAL", "r1_initial_state")
    sig1 = ev1["signature"]

    r2 = Part.makeBox(100.0, 50.0, 10.0)
    face2, ev2 = resolve_top_planar(r2, ref, "R002_WIDTH_100")
    check(face2 is not None, "r2_reference_resolved")
    check(ev2["state"] == "REBOUND_CHANGED_SIGNATURE", "r2_changed_signature_rebind")
    check(ev2["signature"] != sig1, "r2_signature_changes_with_geometry")
    sig2 = ev2["signature"]

    vedges = vertical_edges(r2)
    check(len(vedges) == 4, "r3_vertical_edges_selected")
    r3 = r2.makeFillet(2.0, vedges)
    check(r3.isValid() and len(r3.Solids) == 1, "r3_fillet_valid_single_solid")
    face3, ev3 = resolve_top_planar(r3, ref, "R003_VERTICAL_FILLET")
    check(face3 is not None, "r3_reference_resolved_after_topology_change")
    check(ev3["state"] == "REBOUND_CHANGED_SIGNATURE", "r3_changed_signature_rebind")
    check(ev3["signature"] != sig2, "r3_signature_changes_after_fillet")
    good_signature = ev3["signature"]

    box_a = Part.makeBox(40.0, 40.0, 10.0)
    box_b = Part.makeBox(40.0, 40.0, 10.0, App.Vector(60.0, 0.0, 0.0))
    ambiguous = Part.makeCompound([box_a, box_b])
    face_amb, ev_amb = resolve_top_planar(ambiguous, ref, "R004_AMBIGUOUS")
    check(face_amb is None, "ambiguous_returns_no_face")
    check(ev_amb["state"] == "AMBIGUOUS_HOLD", "ambiguous_explicit_hold")
    check(ev_amb["candidate_count"] == 2, "ambiguous_two_candidates")
    check(ref["last_signature"] == good_signature, "ambiguous_does_not_overwrite_last_good_signature")

    missing = Part.makeSphere(10.0)
    face_missing, ev_missing = resolve_top_planar(missing, ref, "R005_MISSING")
    check(face_missing is None, "missing_returns_no_face")
    check(ev_missing["state"] == "MISSING_HOLD", "missing_explicit_hold")
    check(ref["last_signature"] == good_signature, "missing_does_not_overwrite_last_good_signature")

    registry_text = json.dumps(ref, indent=2, sort_keys=True)
    check("Face1" not in registry_text and "Face2" not in registry_text and "Edge1" not in registry_text, "no_ordinal_subshape_tokens")
    check(all(token in registry_text for token in ["FaceN", "EdgeN", "VertexN"]), "prohibited_ordinals_declared")
    REGISTRY.write_text(registry_text, encoding="utf-8")

    doc = App.newDocument("OLEANDER_REFERENCE_REBIND")
    obj = doc.addObject("App::FeaturePython", "OLE_REFERENCE_PRIMARY_TOP")
    obj.addProperty("App::PropertyString", "OLE_RefID", "OLEANDER")
    obj.OLE_RefID = ref["ref_id"]
    obj.addProperty("App::PropertyString", "OLE_SelectorJSON", "OLEANDER")
    obj.OLE_SelectorJSON = json.dumps(ref["selector"], sort_keys=True)
    obj.addProperty("App::PropertyString", "OLE_LastSignature", "OLEANDER")
    obj.OLE_LastSignature = good_signature
    obj.addProperty("App::PropertyString", "OLE_State", "OLEANDER")
    obj.OLE_State = ref["state"]
    obj.addProperty("App::PropertyString", "OLE_HistoryJSON", "OLEANDER")
    obj.OLE_HistoryJSON = json.dumps(ref["history"], sort_keys=True)
    obj.addProperty("App::PropertyString", "OLE_PersistenceBoundary", "OLEANDER")
    obj.OLE_PersistenceBoundary = "NO_SUBSHAPE_ORDINALS;RE_RESOLVE_OR_HOLD"
    doc.recompute()
    doc.saveAs(str(FCSTD))
    check(FCSTD.exists(), "fcstd_written")
    App.closeDocument(doc.Name)

    reopened = App.openDocument(str(FCSTD))
    ro = reopened.getObject("OLE_REFERENCE_PRIMARY_TOP")
    check(ro is not None, "reference_object_reopen")
    check(ro.OLE_RefID == "OLE_REF::PRIMARY_TOP_FACE", "ref_id_reopen")
    check(ro.OLE_LastSignature == good_signature, "last_good_signature_reopen")
    check(ro.OLE_State == "MISSING_HOLD", "hold_state_reopen")
    check(json.loads(ro.OLE_SelectorJSON)["selector_id"] == "SELECTOR::UNIQUE_GLOBAL_ZMAX_PLANAR_POSITIVE_Z", "selector_semantics_reopen")
    history_reopen = json.loads(ro.OLE_HistoryJSON)
    check(len(history_reopen) == 5, "history_reopen")
    check([e["state"] for e in history_reopen[-2:]] == ["AMBIGUOUS_HOLD", "MISSING_HOLD"], "failure_history_reopen")
    App.closeDocument(reopened.Name)

    result = {
        "schema": "OLEANDER_FREECAD_REFERENCE_REBIND_v0.1",
        "status": "PASS",
        "dependency_state": "RUNTIME_PROBED",
        "freecad_version": ".".join(str(x) for x in App.Version()[:3]),
        "occ_version": getattr(Part, "OCC_VERSION", "unknown"),
        "reference_contract": {
            "stable_ref_id": ref["ref_id"],
            "persistence": "stable ref ID + selector semantics + last-good geometry signature + history",
            "ordinal_persistence": "PROHIBITED",
            "rebind_rule": "re-resolve every authoritative geometry revision; exactly one candidate required",
            "failure_rule": "zero candidates -> MISSING_HOLD; multiple candidates -> AMBIGUOUS_HOLD; never choose first silently",
        },
        "revision_states": [
            {"revision": "R001_BASE_80", "state": ev1["state"], "signature": ev1["signature"]},
            {"revision": "R002_WIDTH_100", "state": ev2["state"], "signature": ev2["signature"]},
            {"revision": "R003_VERTICAL_FILLET", "state": ev3["state"], "signature": ev3["signature"]},
            {"revision": "R004_AMBIGUOUS", "state": ev_amb["state"], "candidate_count": ev_amb["candidate_count"]},
            {"revision": "R005_MISSING", "state": ev_missing["state"], "candidate_count": ev_missing["candidate_count"]},
        ],
        "expected_failure_cases": {
            "ambiguous_reference": "PASS",
            "missing_reference": "PASS",
        },
        "artifacts": {
            "fcstd": str(FCSTD),
            "registry_json": str(REGISTRY),
        },
        "checks": checks,
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "persistent_topological_naming_parity",
            "general_face_reference_stability",
            "edge_reference_stability",
            "vertex_reference_stability",
            "nonplanar_semantic_reference_rebind",
            "automatic_ambiguous_reference_resolution"
        ]
    }
    MANIFEST.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print("OLEANDER_FREECAD_REFERENCE_REBIND=" + json.dumps(result, sort_keys=True), flush=True)


main()
