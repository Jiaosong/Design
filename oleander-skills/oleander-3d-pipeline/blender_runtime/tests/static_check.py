"""Repository-level static checks for the OLEANDER Blender Runtime.

This intentionally does not import bpy. It verifies syntax, contract/version
consistency, and validation-receipt integrity in ordinary CPython. Blender
runtime behavior is covered separately inside real Blender validation scripts.
"""

from __future__ import annotations

import ast
import hashlib
import json
import pathlib
import tomllib

SCRIPT = pathlib.Path(__file__).resolve()
RUNTIME_ROOT = SCRIPT.parents[1]
PIPELINE_ROOT = SCRIPT.parents[2]
ADDON_ROOT = RUNTIME_ROOT / "oleander_blender"
STAGE2_VALIDATION_SCRIPT = RUNTIME_ROOT / "tests" / "validate_stage2.py"
STAGE3_DIRECT_VALIDATION_SCRIPT = RUNTIME_ROOT / "tests" / "validate_stage3_direct.py"
STAGE3_PROCEDURAL_VALIDATION_SCRIPT = RUNTIME_ROOT / "tests" / "validate_stage3_procedural.py"

UNVERIFIED_STATE = "PROPOSED_UNVERIFIED_RUNTIME"
VALIDATED_STATE = "VALIDATED_STAGE2_HEADLESS_CORE"
STAGE2_SCOPE = "STAGE2_HEADLESS_CORE_AND_EXTENSION_PACKAGE"
STAGE3_DIRECT_SCOPE = "STAGE3_DIRECT_MODELING"
STAGE3_PROCEDURAL_SCOPE = "STAGE3_PROCEDURAL_FOUNDATION"


def fail(message: str) -> None:
    raise SystemExit(f"STATIC_CHECK_FAIL: {message}")


def parse_bl_info_version(init_path: pathlib.Path) -> str:
    tree = ast.parse(init_path.read_text(encoding="utf-8"), filename=str(init_path))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "bl_info" for target in node.targets):
            continue
        value = ast.literal_eval(node.value)
        version = value.get("version")
        if not isinstance(version, tuple) or not all(isinstance(v, int) for v in version):
            fail("bl_info.version is not an integer tuple")
        return ".".join(str(v) for v in version)
    fail("bl_info assignment not found")
    return ""


def source_fingerprint(validation_script: pathlib.Path) -> str:
    paths = [
        path
        for path in ADDON_ROOT.rglob("*")
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


def validate_common_receipt(receipt: dict, capability: dict, scope: str, expected_fingerprint: str, label: str) -> None:
    if receipt.get("validation_state") != "PASS":
        fail(f"{label} receipt requires validation_state PASS")
    if receipt.get("validation_scope") != scope:
        fail(f"unexpected {label} validation scope: {receipt.get('validation_scope')}")
    if receipt.get("runtime_id") != capability.get("runtime_id"):
        fail(f"{label} receipt runtime_id mismatch")
    if receipt.get("runtime_version") != capability.get("runtime_version"):
        fail(f"{label} receipt runtime_version mismatch")
    if receipt.get("runtime_result") != "PASS":
        fail(f"{label} receipt runtime_result must be PASS")
    if receipt.get("source_fingerprint_sha256") != expected_fingerprint:
        fail(
            f"{label} validation receipt is stale for current source fingerprint "
            f"receipt={receipt.get('source_fingerprint_sha256')!r} current={expected_fingerprint}"
        )

    workflow = receipt.get("workflow", {})
    if workflow.get("conclusion") != "success" or not workflow.get("run_id") or not workflow.get("job_id"):
        fail(f"{label} receipt must identify a successful workflow run and job")

    package = receipt.get("extension_package", {})
    package_gates = ("source_manifest_validate", "build", "built_package_validate")
    failed_package_gates = [gate for gate in package_gates if package.get(gate) != "PASS"]
    if failed_package_gates:
        fail(f"{label} extension-package validation gates not PASS: {failed_package_gates}")
    if not package.get("sha256") or not package.get("size_bytes"):
        fail(f"{label} validated extension package requires SHA256 and byte size")

    host = receipt.get("host", {})
    if host.get("checksum_manifest_result") != "PASS" or not host.get("blender_archive_sha256"):
        fail(f"{label} validated Blender host requires official checksum PASS and archive SHA256")

    tested_head = receipt.get("tested_branch_head")
    if not isinstance(tested_head, str) or len(tested_head) != 40:
        fail(f"{label} receipt tested_branch_head must be a full commit SHA")


def load_receipt(receipt_ref: str, label: str) -> dict:
    if not isinstance(receipt_ref, str) or not receipt_ref.strip():
        fail(f"{label} validated capability requires receipt path")
    repo_root = PIPELINE_ROOT.parents[1]
    receipt_path = repo_root / receipt_ref
    try:
        receipt_path.relative_to(repo_root)
    except ValueError:
        fail(f"{label} validation receipt must resolve inside repository")
    if not receipt_path.is_file():
        fail(f"{label} validation receipt not found: {receipt_ref}")
    return json.loads(receipt_path.read_text(encoding="utf-8"))


def load_stage2_receipt(capability: dict) -> dict | None:
    lifecycle = capability.get("lifecycle_state")
    receipt_ref = capability.get("validation_receipt")
    if lifecycle == UNVERIFIED_STATE:
        if receipt_ref:
            fail("unverified lifecycle must not claim a validation receipt")
        return None
    if lifecycle != VALIDATED_STATE:
        fail(f"unsupported lifecycle_state: {lifecycle}")
    receipt = load_receipt(receipt_ref, "Stage 2")
    validate_common_receipt(receipt, capability, STAGE2_SCOPE, source_fingerprint(STAGE2_VALIDATION_SCRIPT), "Stage 2")
    return receipt


def load_stage3_direct_receipt(capability: dict, status: dict) -> dict | None:
    validated = set(status.get("VALIDATED_STAGE3_DIRECT", []))
    receipt_ref = capability.get("stage3_direct_validation_receipt")
    if not validated:
        if receipt_ref:
            fail("Stage 3 Direct receipt exists but no VALIDATED_STAGE3_DIRECT capabilities are declared")
        return None
    receipt = load_receipt(receipt_ref, "Stage 3 Direct")
    validate_common_receipt(receipt, capability, STAGE3_DIRECT_SCOPE, source_fingerprint(STAGE3_DIRECT_VALIDATION_SCRIPT), "Stage 3 Direct")
    if receipt.get("stage2_regression_in_same_job") != "PASS":
        fail("Stage 3 Direct validation must include PASS Stage-2 regression in the same job")
    required_checks = {
        "direct_metric_dimensions_operator",
        "direct_dimensions_applied_scale",
        "direct_geometry_change_stale_propagation",
        "direct_operation_metric_record",
        "linear_duplicate_operator",
        "linear_duplicate_unique_ole_ids",
        "linear_duplicate_stable_source_provenance",
        "linear_duplicate_linked_mesh",
        "linear_duplicate_metric_spacing",
        "post_direct_audit_no_duplicate_ids",
    }
    missing_checks = sorted(required_checks - set(receipt.get("runtime_checks", [])))
    if missing_checks:
        fail(f"Stage 3 Direct receipt missing runtime checks: {missing_checks}")
    required_capabilities = {"direct_metric_dimensions_operator", "deterministic_linear_duplicate_operator"}
    missing_capabilities = sorted(required_capabilities - validated)
    if missing_capabilities:
        fail(f"Stage 3 Direct validated capability set missing: {missing_capabilities}")
    return receipt


def load_stage3_procedural_receipt(capability: dict, status: dict) -> dict | None:
    validated = set(status.get("VALIDATED_STAGE3_PROCEDURAL", []))
    receipt_ref = capability.get("stage3_procedural_validation_receipt")
    if not validated:
        if receipt_ref:
            fail("Stage 3 Procedural receipt exists but no VALIDATED_STAGE3_PROCEDURAL capabilities are declared")
        return None
    receipt = load_receipt(receipt_ref, "Stage 3 Procedural")
    validate_common_receipt(
        receipt,
        capability,
        STAGE3_PROCEDURAL_SCOPE,
        source_fingerprint(STAGE3_PROCEDURAL_VALIDATION_SCRIPT),
        "Stage 3 Procedural",
    )
    if receipt.get("stage2_regression_in_same_job") != "PASS":
        fail("Stage 3 Procedural validation must include PASS Stage-2 regression in the same job")
    if receipt.get("stage3_direct_regression_in_same_job") != "PASS":
        fail("Stage 3 Procedural validation must include PASS Stage-3 Direct regression in the same job")
    required_checks = {
        "parameter_metadata_mutation_api",
        "parameter_metadata_sanitization",
        "constraint_metadata_mutation_api",
        "constraint_metadata_sanitization",
        "metadata_mutation_does_not_claim_solver_geometry",
        "geometry_nodes_tree_creation",
        "geometry_nodes_modifier_binding",
        "geometry_nodes_passthrough_evaluation",
        "geometry_nodes_ole_provenance",
        "geometry_nodes_explicit_no_solver_claim",
        "geometry_nodes_save_reopen_persistence",
        "parameter_constraint_save_reopen_persistence",
    }
    missing_checks = sorted(required_checks - set(receipt.get("runtime_checks", [])))
    if missing_checks:
        fail(f"Stage 3 Procedural receipt missing runtime checks: {missing_checks}")
    required_capabilities = {"parameter_constraint_metadata_mutation_api", "geometry_nodes_support_probe"}
    missing_capabilities = sorted(required_capabilities - validated)
    if missing_capabilities:
        fail(f"Stage 3 Procedural validated capability set missing: {missing_capabilities}")
    return receipt


def main() -> None:
    python_files = sorted(ADDON_ROOT.rglob("*.py")) + sorted((RUNTIME_ROOT / "tests").rglob("*.py"))
    if not python_files:
        fail("no Python files found")
    for path in python_files:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    manifest_path = ADDON_ROOT / "blender_manifest.toml"
    with manifest_path.open("rb") as handle:
        manifest = tomllib.load(handle)

    capability = json.loads((PIPELINE_ROOT / "BLENDER_RUNTIME_CAPABILITY.json").read_text(encoding="utf-8"))
    schema = json.loads((ADDON_ROOT / "workbench_manifest.schema.json").read_text(encoding="utf-8"))
    bl_info_version = parse_bl_info_version(ADDON_ROOT / "__init__.py")
    versions = {bl_info_version, manifest.get("version"), capability.get("runtime_version")}
    if len(versions) != 1:
        fail(f"version mismatch bl_info={bl_info_version} manifest={manifest.get('version')} capability={capability.get('runtime_version')}")

    status = capability.get("implementation_status", {})
    stage2_receipt = load_stage2_receipt(capability)
    stage3_direct_receipt = load_stage3_direct_receipt(capability, status)
    stage3_procedural_receipt = load_stage3_procedural_receipt(capability, status)

    if manifest.get("blender_version_min") != "5.1.0":
        fail("unexpected minimum Blender version")

    required_impl = {"dependency_graph_resolution", "stale_dependency_propagation", "geometry_baseline_diff", "review_state_separation", "export_manifest_v0.2_core"}
    declared = (
        set(status.get("VALIDATED_STAGE2_HEADLESS", []))
        | set(status.get("VALIDATED_STAGE3_DIRECT", []))
        | set(status.get("VALIDATED_STAGE3_PROCEDURAL", []))
        | set(status.get("IMPLEMENTED_UNVERIFIED", []))
    )
    missing = sorted(required_impl - declared)
    if missing:
        fail(f"capability contract missing required implementation entries: {missing}")

    validated_stage2 = set(status.get("VALIDATED_STAGE2_HEADLESS", []))
    if capability.get("lifecycle_state") == VALIDATED_STATE:
        required_receipt_checks = {
            "registration", "persistent_metadata", "dependency_graph", "stale_propagation",
            "geometry_baseline_diff", "configuration_capture_restore",
            "bom_grouping_and_conflict_detection", "review_state_separation",
            "scene_unit_scale_round_trip", "blend_save_reopen_persistence", "audit_v0.2", "manifest_v0.2",
        }
        missing_checks = sorted(required_receipt_checks - set((stage2_receipt or {}).get("runtime_checks", [])))
        if missing_checks:
            fail(f"validated lifecycle receipt missing required runtime checks: {missing_checks}")
        if not validated_stage2:
            fail("validated lifecycle requires non-empty VALIDATED_STAGE2_HEADLESS capability set")

    schema_const = schema.get("properties", {}).get("schema", {}).get("const")
    if schema_const != "OLEANDER_BLENDER_WORKBENCH_MANIFEST_v0.2":
        fail(f"workbench manifest schema const mismatch: {schema_const}")

    print(json.dumps({
        "status": "PASS",
        "python_files_parsed": len(python_files),
        "runtime_version": bl_info_version,
        "lifecycle_state": capability["lifecycle_state"],
        "stage2_source_fingerprint_sha256": source_fingerprint(STAGE2_VALIDATION_SCRIPT),
        "stage3_direct_source_fingerprint_sha256": source_fingerprint(STAGE3_DIRECT_VALIDATION_SCRIPT),
        "stage3_procedural_source_fingerprint_sha256": source_fingerprint(STAGE3_PROCEDURAL_VALIDATION_SCRIPT),
        "validation_receipt": capability.get("validation_receipt", ""),
        "stage3_direct_validation_receipt": capability.get("stage3_direct_validation_receipt", ""),
        "stage3_procedural_validation_receipt": capability.get("stage3_procedural_validation_receipt", ""),
        "stage3_direct_receipt_loaded": bool(stage3_direct_receipt),
        "stage3_procedural_receipt_loaded": bool(stage3_procedural_receipt),
        "note": "Static PASS validates receipt/contract integrity; it is not a substitute for Blender runtime execution.",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
