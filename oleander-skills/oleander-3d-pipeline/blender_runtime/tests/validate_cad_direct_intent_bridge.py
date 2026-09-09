"""Blender 5.2 contract validation for the bounded CAD Direct Face intent bridge.

This validates deterministic conversion from the Runtime's CAD direct-edit intent
into a specialist-sidecar request. It deliberately does not resolve a FreeCAD
face or execute any B-Rep mutation; semantic rebind and authoritative mutation
remain specialist execution responsibilities and must fail closed on ambiguity.
"""

from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import sys
import tempfile

import bpy

SCRIPT = pathlib.Path(__file__).resolve()
RUNTIME_ROOT = SCRIPT.parents[1]
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))

from oleander_blender.direct_model import CAD_DIRECT_EDIT_INTENT_SCHEMA
from professional_adapter.cad_sidecar import (
    CADSidecarContractError,
    DIRECT_EDIT_INTENT_SCHEMA,
    DIRECT_EDIT_REQUEST_SCHEMA,
    build_direct_edit_request_from_intent,
    file_sha256,
    payload_sha256,
    validate_direct_edit_intent,
    write_direct_edit_request,
)


def check(condition: bool, label: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def expect_failure(mutator, label: str, checks: list[str]) -> None:
    candidate = copy.deepcopy(valid_intent())
    mutator(candidate)
    try:
        build_direct_edit_request_from_intent(
            request_id="OLE_CAD_DIRECT_REQ_FAIL",
            revision=1,
            intent=candidate,
        )
    except CADSidecarContractError:
        checks.append(label)
    else:
        raise AssertionError(label)


def valid_intent() -> dict:
    return {
        "schema": CAD_DIRECT_EDIT_INTENT_SCHEMA,
        "ole_id": "OLE_CAD_DIRECT_FACE_001",
        "units": "mm",
        "operation": "FACE_NORMAL_MOVE",
        "parameters": {"distance_mm": 12.5},
        "target": {
            "selector_semantics": "BLENDER_SELECTED_DISPLAY_FACE_INTENT",
            "normal_local": [0.0, 0.0, 1.0],
            "center_local_mm": [0.0, 0.0, 50.0],
            "area_mm2": 10000.0,
            "edge_count": 4,
            "edge_lengths_mm": [100.0, 100.0, 100.0, 100.0],
            "bbox_local_mm": {
                "min": [-50.0, -50.0, 50.0],
                "max": [50.0, 50.0, 50.0],
            },
        },
        "authority": {
            "master_type": "CAD_NATIVE",
            "master_locator": "governed://cad/OLE_CAD_DIRECT_FACE_001/master.FCStd",
            "required_kernel": "FREECAD_OCCT_BREP",
            "blender_role": "DISPLAY_DERIVATIVE_ONLY",
            "display_mutation": "NONE",
        },
        "resolution": {
            "policy": "SEMANTIC_REBIND_FAIL_CLOSED",
            "ambiguous_result": "HOLD",
            "missing_result": "HOLD",
            "prohibited_persistence": [
                "FaceN",
                "EdgeN",
                "VertexN",
                "subshape_ordinal",
                "polygon_index",
            ],
        },
    }


def main() -> None:
    checks: list[str] = []
    check(
        CAD_DIRECT_EDIT_INTENT_SCHEMA == DIRECT_EDIT_INTENT_SCHEMA,
        "runtime_and_sidecar_intent_schema_match",
        checks,
    )

    intent = valid_intent()
    validated = validate_direct_edit_intent(intent)
    check(validated["ole_id"] == intent["ole_id"], "intent_ole_id_preserved", checks)
    check(abs(validated["distance_mm"] - 12.5) <= 1e-9, "intent_metric_distance_preserved", checks)
    check(validated["intent_sha256"] == payload_sha256(intent), "intent_sha256_deterministic", checks)

    request1 = build_direct_edit_request_from_intent(
        request_id="OLE_CAD_DIRECT_REQ_001",
        revision=1,
        intent=intent,
    )
    request2 = build_direct_edit_request_from_intent(
        request_id="OLE_CAD_DIRECT_REQ_001",
        revision=1,
        intent=copy.deepcopy(intent),
    )
    check(request1 == request2, "direct_request_deterministic", checks)
    check(request1["schema"] == DIRECT_EDIT_REQUEST_SCHEMA, "direct_request_schema", checks)
    check(request1["source"]["intent_sha256"] == payload_sha256(intent), "direct_request_binds_intent_sha", checks)
    check(request1["source"]["required_kernel"] == "FREECAD_OCCT_BREP", "direct_request_freecad_occt_authority", checks)
    check(request1["operation"] == {"kind": "FACE_NORMAL_MOVE", "distance_mm": 12.5}, "direct_request_bounded_operation", checks)
    check(request1["target_selector"]["kind"] == "SEMANTIC_FACE_DESCRIPTOR", "direct_request_semantic_selector", checks)
    check(request1["target_selector"]["resolution_policy"] == "SEMANTIC_REBIND_FAIL_CLOSED", "direct_request_fail_closed_rebind", checks)
    check(request1["target_selector"]["ambiguous_result"] == "HOLD", "direct_request_ambiguous_hold", checks)
    check(request1["target_selector"]["missing_result"] == "HOLD", "direct_request_missing_hold", checks)
    check(request1["authority"]["blender_role"] == "DISPLAY_DERIVATIVE_ONLY", "direct_request_blender_display_only", checks)
    check(request1["authority"]["display_mutation"] == "NONE", "direct_request_no_display_mutation", checks)
    check(request1["authority"]["execution_state"] == "NOT_EXECUTED", "direct_request_no_execution_claim", checks)

    serialized = json.dumps(request1, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    check("Face17" not in serialized and "polygon_index\":" not in serialized, "direct_request_no_persistent_topology_ordinal", checks)

    with tempfile.TemporaryDirectory(prefix="oleander-cad-direct-") as temp_dir:
        request_path = pathlib.Path(temp_dir) / "direct_request.json"
        written_sha = write_direct_edit_request(request_path, request1)
        check(request_path.exists(), "direct_request_written", checks)
        check(written_sha == file_sha256(request_path), "direct_request_file_sha", checks)
        check(
            written_sha == hashlib.sha256(request_path.read_bytes()).hexdigest(),
            "direct_request_file_sha_independent_readback",
            checks,
        )
        check(json.loads(request_path.read_text(encoding="utf-8")) == request1, "direct_request_json_readback", checks)

    expect_failure(lambda payload: payload["target"].__setitem__("polygon_index", 5), "polygon_index_expected_failure", checks)
    expect_failure(lambda payload: payload["target"].__setitem__("legacy_reference", "Face17"), "face_ordinal_string_expected_failure", checks)
    expect_failure(lambda payload: payload["resolution"].__setitem__("ambiguous_result", "SELECT_FIRST"), "ambiguous_resolution_expected_failure", checks)
    expect_failure(lambda payload: payload["authority"].__setitem__("required_kernel", "BLENDER_MESH"), "wrong_kernel_expected_failure", checks)
    expect_failure(lambda payload: payload["parameters"].__setitem__("distance_mm", 0.0), "zero_distance_expected_failure", checks)
    expect_failure(lambda payload: payload["authority"].__setitem__("display_mutation", "ALLOWED"), "display_mutation_expected_failure", checks)

    result = {
        "schema": "OLEANDER_CAD_DIRECT_INTENT_BRIDGE_VALIDATION_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "checks": checks,
        "intent_schema": DIRECT_EDIT_INTENT_SCHEMA,
        "request_schema": DIRECT_EDIT_REQUEST_SCHEMA,
        "request_sha256": payload_sha256(request1),
        "authority": {
            "required_kernel": "FREECAD_OCCT_BREP",
            "blender": "DISPLAY_DERIVATIVE_ONLY",
            "execution": "NOT_EXECUTED",
        },
        "non_claims": [
            "cad_face_resolution",
            "cad_direct_edit_execution",
            "general_brep_push_pull",
            "persistent_topological_naming",
            "P0_B_DIRECT_BREP_PASS",
            "engineering_approval",
            "manufacturing_release",
            "field_truth",
        ],
    }
    print("OLEANDER_CAD_DIRECT_INTENT_BRIDGE=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
