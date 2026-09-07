from __future__ import annotations

import json

import static_check as base
import static_check_17 as layer17

CONSOLIDATED_RECEIPT = base.RUNTIME_ROOT / "BLENDER_RUNTIME_REGRESSION_RECEIPT_5_2_LTS_20260905.json"
RUNTIME_WORKFLOW = base.REPO_ROOT / ".github" / "workflows" / "oleander-blender-runtime-5-2-lts.yml"
EXPECTED_RUNTIME = "5.2.0 LTS"
EXPECTED_BUILD = "fbe6228777e7"
EXPECTED_RUN_ID = 33935040543
EXPECTED_JOB_ID = 101221190932
EXPECTED_STAGE_COUNT = 17


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
        base.fail(f"{stage['label']} consolidated 5.2 receipt stale: {actual} != {expected}")

    workflow_text = RUNTIME_WORKFLOW.read_text(encoding="utf-8")
    if script not in workflow_text:
        base.fail(f"{stage['label']} validation script is not bound into Blender 5.2 regression workflow")

    # Preserve the mature base.validate_stage return contract: base.main uses
    # Stage 2's returned extension_package as the canonical package identity.
    return CURRENT_RECEIPT


def main() -> None:
    base.validate_stage = validate_stage_with_consolidated_receipt
    layer17.main()


if __name__ == "__main__":
    main()
