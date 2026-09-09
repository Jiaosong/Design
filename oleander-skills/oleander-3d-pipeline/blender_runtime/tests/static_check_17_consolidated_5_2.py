from __future__ import annotations

import ast
import json

import static_check as base
import static_check_17 as layer17

CONSOLIDATED_RECEIPT = base.RUNTIME_ROOT / "BLENDER_RUNTIME_REGRESSION_RECEIPT_5_2_LTS_20260905.json"
RUNTIME_WORKFLOW = base.REPO_ROOT / ".github" / "workflows" / "oleander-blender-runtime-5-2-lts.yml"
CAD_DIRECT_BRIDGE_SCRIPT = base.RUNTIME_ROOT / "tests" / "validate_cad_direct_intent_bridge.py"
CAD_SIDECAR = base.RUNTIME_ROOT / "professional_adapter" / "cad_sidecar.py"
EXPECTED_RUNTIME = "5.2.0 LTS"
EXPECTED_BUILD = "fbe6228777e7"
EXPECTED_RUN_ID = 34302353461
EXPECTED_JOB_ID = 102311768341
EXPECTED_STAGE_COUNT = 17
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
    "FaceN",
    "polygon_index",
}


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
