"""Incremental static gate for OLEANDER Stage 3 Angular/Datum/Construction.

The mature static_check.py remains the eight-layer base gate. This file verifies
that the ninth validated layer is fingerprint-bound to the same real-Blender
package/workflow and that its explicit authority boundaries remain intact.
"""

from __future__ import annotations

import hashlib
import json
import pathlib

SCRIPT = pathlib.Path(__file__).resolve()
RUNTIME_ROOT = SCRIPT.parents[1]
PIPELINE_ROOT = SCRIPT.parents[2]
ADDON_ROOT = RUNTIME_ROOT / "oleander_blender"
REPO_ROOT = PIPELINE_ROOT.parents[1]


def fail(message):
    raise SystemExit(f"ANGULAR_DATUM_STATIC_FAIL: {message}")


def fingerprint(validation_script):
    paths = [
        path for path in ADDON_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".py", ".json", ".toml"}
    ]
    paths.append(validation_script)
    digest = hashlib.sha256()
    for path in sorted(set(paths), key=lambda item: item.as_posix()):
        rel = path.relative_to(PIPELINE_ROOT).as_posix().encode("utf-8")
        digest.update(rel)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def load_repo_json(reference):
    path = REPO_ROOT / reference
    try:
        path.relative_to(REPO_ROOT)
    except ValueError:
        fail("receipt path escapes repository")
    if not path.is_file():
        fail(f"missing receipt: {reference}")
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    capability = json.loads((PIPELINE_ROOT / "BLENDER_RUNTIME_CAPABILITY.json").read_text(encoding="utf-8"))
    status = capability.get("implementation_status", {})
    validated = set(status.get("VALIDATED_STAGE3_ANGULAR_DATUM", []))
    required_caps = {
        "angular_quantize_axis_mask",
        "angular_nudge_exact_degrees",
        "angle_guide_editable_reference_geometry",
        "datum_axis_metric_length",
        "datum_plane_metric_size",
        "construction_line_metric_length_offset",
        "angular_datum_reference_guide_audit_exclusion",
    }
    missing = sorted(required_caps - validated)
    if missing:
        fail(f"validated Angular/Datum capabilities missing: {missing}")

    receipt_ref = capability.get("stage3_angular_datum_validation_receipt")
    if not receipt_ref:
        fail("capability lacks Angular/Datum receipt pointer")
    receipt = load_repo_json(receipt_ref)
    if receipt.get("validation_state") != "PASS" or receipt.get("runtime_result") != "PASS":
        fail("Angular/Datum receipt must be PASS")
    if receipt.get("validation_scope") != "STAGE3_ANGULAR_DATUM_CONSTRUCTION":
        fail("Angular/Datum receipt scope mismatch")
    if receipt.get("runtime_id") != capability.get("runtime_id") or receipt.get("runtime_version") != capability.get("runtime_version"):
        fail("runtime identity/version mismatch")

    expected = fingerprint(RUNTIME_ROOT / "tests" / "validate_stage3_angular_datum.py")
    if receipt.get("source_fingerprint_sha256") != expected:
        fail(f"Angular/Datum receipt stale: {receipt.get('source_fingerprint_sha256')} != {expected}")

    workflow = receipt.get("workflow", {})
    package = receipt.get("extension_package", {})
    host = receipt.get("host", {})
    if workflow.get("conclusion") != "success" or not workflow.get("run_id") or not workflow.get("job_id"):
        fail("Angular/Datum receipt lacks successful workflow evidence")
    if host.get("blender_version") != "5.1.2" or host.get("checksum_manifest_result") != "PASS":
        fail("Angular/Datum receipt lacks Blender 5.1.2 official checksum evidence")
    for gate in ("source_manifest_validate", "build", "built_package_validate"):
        if package.get(gate) != "PASS":
            fail(f"extension package gate failed: {gate}")
    if not package.get("sha256") or not package.get("size_bytes"):
        fail("extension package SHA/size missing")

    base_receipt = load_repo_json(capability["validation_receipt"])
    if package.get("sha256") != base_receipt.get("extension_package", {}).get("sha256") or package.get("size_bytes") != base_receipt.get("extension_package", {}).get("size_bytes"):
        fail("Angular/Datum receipt does not use same extension package as Stage 2")
    if workflow.get("run_id") != base_receipt.get("workflow", {}).get("run_id") or workflow.get("job_id") != base_receipt.get("workflow", {}).get("job_id"):
        fail("Angular/Datum receipt does not use same real-Blender job as Stage 2")

    required_checks = {
        "angular_quantize_axis_mask", "angular_quantize_metric_degree_contract",
        "angular_quantize_downstream_stale", "angular_nudge_exact_degrees",
        "angular_batch_transform_authority_preflight", "angular_batch_failure_no_partial_mutation",
        "angle_guide_editable_reference_geometry", "angle_guide_metric_radius",
        "angle_guide_minor_major_interval_contract", "datum_axis_metric_length",
        "datum_plane_metric_size", "construction_line_metric_length_offset",
        "angular_datum_reference_guide_audit_exclusion", "angular_operator_registration",
        "datum_operator_registration", "angular_datum_save_reopen_persistence",
    }
    missing_checks = sorted(required_checks - set(receipt.get("runtime_checks", [])))
    if missing_checks:
        fail(f"receipt missing checks: {missing_checks}")

    failures = receipt.get("expected_failure_cases", {})
    for case in (
        "external_transform_authority", "invalid_rotation_step", "irregular_angle_interval",
        "excessive_angle_intervals", "invalid_datum_axis", "invalid_datum_plane",
        "invalid_construction_line",
    ):
        if failures.get(case) != "PASS":
            fail(f"expected failure case not PASS: {case}")

    for regression in (
        "stage2_regression_in_same_job", "stage3_direct_regression_in_same_job",
        "stage3_feature_stack_regression_in_same_job", "stage3_feature_editing_regression_in_same_job",
        "stage3_relation_regression_in_same_job", "stage3_relation_apply_regression_in_same_job",
        "stage3_measurement_regression_in_same_job",
    ):
        if receipt.get(regression) != "PASS":
            fail(f"same-job regression missing: {regression}")

    procedural = load_repo_json(capability["stage3_procedural_validation_receipt"])
    if procedural.get("stage3_angular_datum_regression_in_same_job") != "PASS":
        fail("Procedural receipt does not prove Angular/Datum upstream regression in same job")

    declared = set(status.get("DECLARED_NOT_IMPLEMENTED", []))
    boundaries = set(capability.get("does_not_prove", []))
    for item in ("solver_backed_angular_constraints", "cad_datum_feature_authority"):
        if item not in declared:
            fail(f"missing DECLARED_NOT_IMPLEMENTED boundary: {item}")
        if item not in boundaries:
            fail(f"missing does_not_prove boundary: {item}")
    if "screen_space_angle_dimensional_authority" not in boundaries:
        fail("screen-space angle authority boundary missing")

    env = capability.get("stage3_angular_datum_validated_environment", {})
    if env.get("source_fingerprint_sha256") != expected or env.get("workflow_run_id") != workflow.get("run_id") or env.get("runtime_result") != "PASS":
        fail("capability Angular/Datum validated environment does not match receipt")

    print(json.dumps({
        "status": "PASS",
        "validated_layer": "Stage 3 Angular Datum",
        "source_fingerprint_sha256": expected,
        "extension_package_sha256": package["sha256"],
        "extension_package_size_bytes": package["size_bytes"],
        "workflow_run_id": workflow["run_id"],
        "note": "Incremental ninth-layer static gate; real Blender runtime evidence remains authoritative for execution.",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
