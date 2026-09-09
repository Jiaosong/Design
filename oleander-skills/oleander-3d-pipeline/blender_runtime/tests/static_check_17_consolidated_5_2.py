from __future__ import annotations

import ast
import hashlib
import json

import static_check as base
import static_check_17 as layer17

CONSOLIDATED_RECEIPT = base.RUNTIME_ROOT / "BLENDER_RUNTIME_REGRESSION_RECEIPT_5_2_LTS_20260905.json"
CAD_DIRECT_BRIDGE_RECEIPT = base.RUNTIME_ROOT / "CAD_DIRECT_INTENT_BRIDGE_RECEIPT_5_2_20260909.json"
RUNTIME_WORKFLOW = base.REPO_ROOT / ".github" / "workflows" / "oleander-blender-runtime-5-2-lts.yml"
CAD_DIRECT_BRIDGE_SCRIPT = base.RUNTIME_ROOT / "tests" / "validate_cad_direct_intent_bridge.py"
CAD_SIDECAR = base.RUNTIME_ROOT / "professional_adapter" / "cad_sidecar.py"
EXPECTED_RUNTIME = "5.2.0 LTS"
EXPECTED_BUILD = "fbe6228777e7"
EXPECTED_RUN_ID = 34302353461
EXPECTED_JOB_ID = 102311768341
EXPECTED_STAGE_COUNT = 17
EXPECTED_BRIDGE_RUN_ID = 34305925694
EXPECTED_BRIDGE_JOB_ID = 102322478236
EXPECTED_BRIDGE_REQUEST_SHA256 = "8ad5231851ff31cafac32a59e3a601201b0381c711c502cbf80c6ca3d21ba318"
FINGERPRINT_MISMATCHES: list[tuple[str, str, str]] = []

REQUIRED_BOUNDED_DIRECT_DELTA = {
    "BLENDER_NATIVE_SINGLE_FACE_NORMAL_MOVE_MM",
    "DIRECT_FACE_DOWNSTREAM_STALE_PROPAGATION",
    "CAD_NATIVE_DIRECT_EDIT_INTENT_ROUTING",
    "CAD_DISPLAY_GEOMETRY_NO_MUTATION",
    "SEMANTIC_SELECTOR_WITHOUT_PERSISTENT_TOPOLOGY_ORDINAL",
    "AMBIGUOUS_OR_MISSING_CAD_SELECTOR_FAIL_CLOSED_HOLD",
}

REQUIRED_DIRECT_NON_CLAIMS = {
    "CAD_DIRECT_EDIT_EXECUTION",
    "GENERAL_BREP_PUSH_PULL",
    "PERSISTENT_TOPOLOGICAL_NAMING_GENERALITY",
    "P0_B_DIRECT_BREP_PASS",
    "default_environment_promotion",
    "general_cad_parity",
}

BRIDGE_REQUIRED_WORKFLOW_TOKENS = {
    "validate_cad_direct_intent_bridge.py",
    "OLEANDER_CAD_DIRECT_INTENT_BRIDGE=",
    '"execution": "NOT_EXECUTED"',
    '"blender": "DISPLAY_DERIVATIVE_ONLY"',
}

BRIDGE_REQUIRED_SOURCE_TOKENS = {
    "OLEANDER_CAD_DIRECT_EDIT_INTENT_v0.1",
    "OLEANDER_CAD_DIRECT_EDIT_REQUEST_v0.1",
    "SEMANTIC_REBIND_FAIL_CLOSED",
    "FREECAD_OCCT_BREP",
    "DISPLAY_DERIVATIVE_ONLY",
    "NOT_EXECUTED",
    "STRICT_REVALIDATION",
    "validate_direct_edit_request",
    "FaceN",
    "polygon_index",
}

BRIDGE_REQUIRED_CHECKS = {
    "runtime_and_sidecar_intent_schema_match",
    "intent_sha256_deterministic",
    "direct_request_deterministic",
    "direct_request_binds_intent_sha",
    "direct_request_freecad_occt_authority",
    "direct_request_semantic_selector",
    "direct_request_fail_closed_rebind",
    "direct_request_ambiguous_hold",
    "direct_request_missing_hold",
    "direct_request_blender_display_only",
    "direct_request_no_display_mutation",
    "direct_request_no_execution_claim",
    "direct_request_strict_validation",
    "direct_request_validation_sha",
    "direct_request_validation_no_execution_claim",
    "direct_request_no_persistent_topology_ordinal",
    "direct_request_file_sha_independent_readback",
    "direct_request_json_readback",
    "direct_request_persisted_revalidation",
    "polygon_index_expected_failure",
    "face_ordinal_string_expected_failure",
    "ambiguous_resolution_expected_failure",
    "wrong_kernel_expected_failure",
    "zero_distance_expected_failure",
    "display_mutation_expected_failure",
    "request_unknown_top_level_expected_failure_writer_no_file",
    "request_unknown_top_level_expected_failure",
    "request_empty_identity_expected_failure_writer_no_file",
    "request_empty_identity_expected_failure",
    "request_revision_expected_failure_writer_no_file",
    "request_revision_expected_failure",
    "request_units_expected_failure_writer_no_file",
    "request_units_expected_failure",
    "request_source_authority_expected_failure_writer_no_file",
    "request_source_authority_expected_failure",
    "request_intent_sha_expected_failure_writer_no_file",
    "request_intent_sha_expected_failure",
    "request_master_locator_expected_failure_writer_no_file",
    "request_master_locator_expected_failure",
    "request_kernel_expected_failure_writer_no_file",
    "request_kernel_expected_failure",
    "request_operation_expected_failure_writer_no_file",
    "request_operation_expected_failure",
    "request_distance_expected_failure_writer_no_file",
    "request_distance_expected_failure",
    "request_polygon_index_expected_failure_writer_no_file",
    "request_polygon_index_expected_failure",
    "request_resolution_policy_expected_failure_writer_no_file",
    "request_resolution_policy_expected_failure",
    "request_ambiguous_result_expected_failure_writer_no_file",
    "request_ambiguous_result_expected_failure",
    "request_prohibited_set_expected_failure_writer_no_file",
    "request_prohibited_set_expected_failure",
    "request_master_type_expected_failure_writer_no_file",
    "request_master_type_expected_failure",
    "request_geometry_authority_expected_failure_writer_no_file",
    "request_geometry_authority_expected_failure",
    "request_blender_role_expected_failure_writer_no_file",
    "request_blender_role_expected_failure",
    "request_display_mutation_expected_failure_writer_no_file",
    "request_display_mutation_expected_failure",
    "request_execution_claim_expected_failure_writer_no_file",
    "request_execution_claim_expected_failure",
}

BRIDGE_REQUIRED_FAILURES = {
    "polygon_index",
    "face_ordinal_string",
    "ambiguous_resolution_select_first",
    "wrong_kernel",
    "zero_distance",
    "display_mutation_allowed",
    "request_unknown_top_level",
    "request_empty_identity",
    "request_revision",
    "request_units",
    "request_source_authority",
    "request_intent_sha",
    "request_master_locator",
    "request_kernel",
    "request_operation",
    "request_distance",
    "request_polygon_index",
    "request_resolution_policy",
    "request_ambiguous_result",
    "request_prohibited_set",
    "request_master_type",
    "request_geometry_authority",
    "request_blender_role",
    "request_display_mutation",
    "request_execution_claim",
}

BRIDGE_REQUIRED_NON_CLAIMS = {
    "cad_face_resolution",
    "cad_direct_edit_execution",
    "general_brep_push_pull",
    "persistent_topological_naming",
    "P0_B_DIRECT_BREP_PASS",
    "default_environment_promotion",
    "general_cad_parity",
}


def git_blob_sha(path) -> str:
    data = path.read_bytes()
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def validate_cad_direct_bridge_binding() -> None:
    """Static binding guard only; real PASS still comes from Blender 5.2 execution."""
    if not CAD_DIRECT_BRIDGE_SCRIPT.is_file():
        base.fail("CAD Direct Intent Bridge validation script missing")
    if not CAD_SIDECAR.is_file():
        base.fail("CAD sidecar source missing")

    for path in (CAD_DIRECT_BRIDGE_SCRIPT, CAD_SIDECAR):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    workflow_text = RUNTIME_WORKFLOW.read_text(encoding="utf-8")
    missing_workflow = sorted(token for token in BRIDGE_REQUIRED_WORKFLOW_TOKENS if token not in workflow_text)
    if missing_workflow:
        base.fail(f"CAD Direct Intent Bridge lost Blender 5.2 workflow binding: {missing_workflow}")

    combined_source = CAD_DIRECT_BRIDGE_SCRIPT.read_text(encoding="utf-8") + "\n" + CAD_SIDECAR.read_text(encoding="utf-8")
    missing_source = sorted(token for token in BRIDGE_REQUIRED_SOURCE_TOKENS if token not in combined_source)
    if missing_source:
        base.fail(f"CAD Direct Intent Bridge lost authority/fail-closed source boundary: {missing_source}")


def validate_cad_direct_bridge_receipt() -> dict:
    if not CAD_DIRECT_BRIDGE_RECEIPT.is_file():
        base.fail("CAD Direct Intent Bridge Blender 5.2 receipt missing")
    receipt = json.loads(CAD_DIRECT_BRIDGE_RECEIPT.read_text(encoding="utf-8"))
    if receipt.get("schema") != "OLEANDER_CAD_DIRECT_INTENT_BRIDGE_RECEIPT_v0.1":
        base.fail("unexpected CAD Direct Intent Bridge receipt schema")
    if receipt.get("hardening_revision") != "v0.2_STRICT_REQUEST_REVALIDATION":
        base.fail("CAD Direct Intent Bridge hardening revision is not Current")
    if receipt.get("validation_state") != "PASS" or receipt.get("runtime_result") != "PASS":
        base.fail("CAD Direct Intent Bridge receipt must be PASS")
    if receipt.get("validation_scope") != "CAD_DIRECT_INTENT_TO_REQUEST_CONTRACT":
        base.fail("CAD Direct Intent Bridge receipt scope mismatch")

    workflow = receipt.get("workflow", {})
    if (
        workflow.get("name") != "OLEANDER Blender Runtime 5.2 LTS Regression"
        or workflow.get("run_id") != EXPECTED_BRIDGE_RUN_ID
        or workflow.get("job_id") != EXPECTED_BRIDGE_JOB_ID
        or workflow.get("conclusion") != "success"
        or workflow.get("specialist_gate") != "Validate bounded CAD direct intent bridge on Blender 5.2 LTS"
    ):
        base.fail("CAD Direct Intent Bridge workflow evidence mismatch")

    host = receipt.get("host", {})
    if host.get("blender_version") != EXPECTED_RUNTIME or host.get("blender_build_hash") != EXPECTED_BUILD:
        base.fail("CAD Direct Intent Bridge Blender 5.2 host identity mismatch")
    if receipt.get("intent_schema") != "OLEANDER_CAD_DIRECT_EDIT_INTENT_v0.1":
        base.fail("CAD Direct Intent Bridge intent schema mismatch")
    if receipt.get("request_schema") != "OLEANDER_CAD_DIRECT_EDIT_REQUEST_v0.1":
        base.fail("CAD Direct Intent Bridge request schema mismatch")
    if receipt.get("request_sha256") != EXPECTED_BRIDGE_REQUEST_SHA256:
        base.fail("CAD Direct Intent Bridge deterministic request SHA mismatch")

    authority = receipt.get("authority", {})
    required_authority = {
        "required_kernel": "FREECAD_OCCT_BREP",
        "blender_role": "DISPLAY_DERIVATIVE_ONLY",
        "execution_state": "NOT_EXECUTED",
        "resolution_policy": "SEMANTIC_REBIND_FAIL_CLOSED",
        "ambiguous_result": "HOLD",
        "missing_result": "HOLD",
        "display_mutation": "NONE",
        "writer_validation": "STRICT_REVALIDATION",
    }
    for key, expected in required_authority.items():
        if authority.get(key) != expected:
            base.fail(f"CAD Direct Intent Bridge authority mismatch: {key}")

    source_blobs = receipt.get("validated_source_blobs", {})
    current_blobs = {
        "professional_adapter/cad_sidecar.py": git_blob_sha(CAD_SIDECAR),
        "tests/validate_cad_direct_intent_bridge.py": git_blob_sha(CAD_DIRECT_BRIDGE_SCRIPT),
        ".github/workflows/oleander-blender-runtime-5-2-lts.yml": git_blob_sha(RUNTIME_WORKFLOW),
    }
    for key, current_sha in current_blobs.items():
        if source_blobs.get(key) != current_sha:
            base.fail(f"CAD Direct Intent Bridge receipt source blob is stale: {key}")

    checks = set(receipt.get("runtime_checks", []))
    missing_checks = sorted(BRIDGE_REQUIRED_CHECKS - checks)
    if missing_checks:
        base.fail(f"CAD Direct Intent Bridge receipt missing runtime checks: {missing_checks}")

    failures = receipt.get("expected_failure_cases", {})
    for key in sorted(BRIDGE_REQUIRED_FAILURES):
        if failures.get(key) != "PASS":
            base.fail(f"CAD Direct Intent Bridge expected failure not PASS: {key}")

    writer_boundary = receipt.get("writer_failure_boundary", {})
    if (
        writer_boundary.get("forged_request_categories") != 19
        or writer_boundary.get("validator_rejects_each") is not True
        or writer_boundary.get("writer_rejects_each") is not True
        or writer_boundary.get("writer_creates_file_on_rejection") is not False
    ):
        base.fail("CAD Direct Intent Bridge writer failure boundary mismatch")

    stage_relation = receipt.get("stage_relation", {})
    if (
        stage_relation.get("runtime_stage_count") != EXPECTED_STAGE_COUNT
        or stage_relation.get("role") != "ADDITIONAL_BOUNDED_SPECIALIST_CONTRACT_GATE"
        or stage_relation.get("is_eighteenth_runtime_stage") is not False
        or stage_relation.get("is_frontier_family") is not False
        or stage_relation.get("creates_sixth_frontier") is not False
    ):
        base.fail("CAD Direct Intent Bridge receipt improperly changes Runtime/Frontier topology")

    non_claims = set(receipt.get("non_claims", []))
    missing_non_claims = sorted(BRIDGE_REQUIRED_NON_CLAIMS - non_claims)
    if missing_non_claims:
        base.fail(f"CAD Direct Intent Bridge non-claim boundary missing: {missing_non_claims}")
    return receipt


def load_consolidated() -> dict:
    if not CONSOLIDATED_RECEIPT.is_file():
        base.fail(f"consolidated Blender 5.2 receipt missing: {CONSOLIDATED_RECEIPT}")
    receipt = json.loads(CONSOLIDATED_RECEIPT.read_text(encoding="utf-8"))
    if receipt.get("validation_state") != "PASS" or receipt.get("runtime_result") != "PASS":
        base.fail("consolidated Blender 5.2 receipt must be PASS")
    if receipt.get("runtime_id") != "oleander-blender-runtime" or receipt.get("runtime_version") != "0.2.0":
        base.fail("consolidated Blender 5.2 runtime identity/version mismatch")

    workflow = receipt.get("workflow", {})
    if (
        workflow.get("name") != "OLEANDER Blender Runtime 5.2 LTS Regression"
        or workflow.get("run_id") != EXPECTED_RUN_ID
        or workflow.get("job_id") != EXPECTED_JOB_ID
        or workflow.get("conclusion") != "success"
    ):
        base.fail("consolidated Blender 5.2 workflow evidence mismatch")

    host = receipt.get("host", {})
    if host.get("blender_version") != EXPECTED_RUNTIME or host.get("blender_build_hash") != EXPECTED_BUILD:
        base.fail("consolidated Blender 5.2 host identity mismatch")
    if host.get("runtime_resolution_result") != "PASS" or not host.get("blender_archive_sha256"):
        base.fail("consolidated Blender 5.2 runtime resolution evidence missing")

    package = receipt.get("extension_package", {})
    for gate in ("source_manifest_validate", "build", "built_package_validate"):
        if package.get(gate) != "PASS":
            base.fail(f"consolidated Blender 5.2 package gate not PASS: {gate}")
    if not package.get("sha256") or not package.get("size_bytes"):
        base.fail("consolidated Blender 5.2 package identity missing")

    stages = receipt.get("stages", {})
    if len(stages) != EXPECTED_STAGE_COUNT:
        base.fail(f"consolidated Blender 5.2 receipt must bind exactly {EXPECTED_STAGE_COUNT} stages")

    bounded_delta = set(receipt.get("validated_bounded_delta", []))
    missing_delta = sorted(REQUIRED_BOUNDED_DIRECT_DELTA - bounded_delta)
    if missing_delta:
        base.fail(f"bounded Direct Face evidence missing from consolidated receipt: {missing_delta}")

    non_claims = set(receipt.get("non_claims", []))
    missing_non_claims = sorted(REQUIRED_DIRECT_NON_CLAIMS - non_claims)
    if missing_non_claims:
        base.fail(f"Direct Face non-claim boundaries missing from consolidated receipt: {missing_non_claims}")

    if not RUNTIME_WORKFLOW.is_file():
        base.fail("Blender 5.2 regression workflow missing")
    workflow_text = RUNTIME_WORKFLOW.read_text(encoding="utf-8")
    if "grep -F '\"status\": \"PASS\"'" not in workflow_text:
        base.fail("Blender 5.2 workflow must fail closed on every validation script status")

    return receipt


CURRENT_RECEIPT = load_consolidated()


def validate_stage_with_consolidated_receipt(capability: dict, status: dict, stage: dict) -> dict:
    validated = set(status.get(stage["status_key"], []))
    if not validated:
        base.fail(f"{stage['label']} validated capability set is empty")
    missing_caps = sorted(set(stage["capabilities"]) - validated)
    if missing_caps:
        base.fail(f"{stage['label']} validated capability set missing: {missing_caps}")

    # Existing 5.1.2 per-stage receipts are immutable provenance, not current
    # source compatibility evidence after the 5.2 repair.
    legacy = base.load_receipt(capability.get(stage["receipt_key"]), stage["label"] + " legacy provenance")
    if legacy.get("validation_state") != "PASS" or legacy.get("runtime_result") != "PASS":
        base.fail(f"{stage['label']} legacy provenance receipt must remain PASS")
    if legacy.get("validation_scope") != stage["scope"]:
        base.fail(f"{stage['label']} legacy receipt scope mismatch")
    legacy_host = legacy.get("host", {})
    if legacy_host.get("blender_version") != "5.1.2":
        base.fail(f"{stage['label']} legacy receipt is not the preserved Blender 5.1.2 provenance")
    legacy_workflow = legacy.get("workflow", {})
    environment = capability.get(stage["environment_key"], {})
    if (
        environment.get("source_fingerprint_sha256") != legacy.get("source_fingerprint_sha256")
        or environment.get("workflow_run_id") != legacy_workflow.get("run_id")
        or environment.get("runtime_result") != "PASS"
    ):
        base.fail(f"{stage['label']} historical capability environment no longer matches preserved provenance")

    # One consolidated 5.2 receipt binds all current validation scripts by
    # exact source fingerprint. This preserves the 17 historical receipts and
    # avoids manufacturing 17 replacement evidence objects.
    script = stage["script"]
    stage_evidence = CURRENT_RECEIPT["stages"].get(script)
    if not stage_evidence:
        base.fail(f"{stage['label']} missing from consolidated Blender 5.2 receipt")
    if stage_evidence.get("status") != "PASS":
        base.fail(f"{stage['label']} consolidated Blender 5.2 stage is not PASS")

    expected = base.source_fingerprint(base.RUNTIME_ROOT / "tests" / script)
    actual = stage_evidence.get("source_fingerprint_sha256")
    if actual != expected:
        FINGERPRINT_MISMATCHES.append((script, str(actual), expected))

    workflow_text = RUNTIME_WORKFLOW.read_text(encoding="utf-8")
    if script not in workflow_text:
        base.fail(f"{stage['label']} validation script is not bound into Blender 5.2 regression workflow")

    # Preserve the mature base.validate_stage return contract: base.main uses
    # Stage 2's returned extension_package as the canonical package identity.
    return CURRENT_RECEIPT


def main() -> None:
    FINGERPRINT_MISMATCHES.clear()
    validate_cad_direct_bridge_binding()
    validate_cad_direct_bridge_receipt()
    base.validate_stage = validate_stage_with_consolidated_receipt
    layer17.main()
    if FINGERPRINT_MISMATCHES:
        for script, actual, expected in FINGERPRINT_MISMATCHES:
            print(
                "CURRENT_SOURCE_FINGERPRINT "
                f"script={script} actual={actual} expected={expected}"
            )
        base.fail(
            "consolidated Blender 5.2 receipt source fingerprints are stale for "
            f"{len(FINGERPRINT_MISMATCHES)} stage(s); refresh only from a successful real Blender 5.2 regression"
        )


if __name__ == "__main__":
    main()
