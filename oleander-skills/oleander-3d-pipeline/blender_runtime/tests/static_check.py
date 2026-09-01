"""Repository-level static checks for the OLEANDER Blender Runtime.

This checker does not import bpy. It validates Python syntax, runtime/version
contracts, independently fingerprint-bound real-Blender receipts, regression
ordering, positive-failure evidence and package identity. A Static PASS is never
a substitute for Blender runtime execution.
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
REPO_ROOT = PIPELINE_ROOT.parents[1]

UNVERIFIED_STATE = "PROPOSED_UNVERIFIED_RUNTIME"
VALIDATED_STATE = "VALIDATED_STAGE2_HEADLESS_CORE"


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
        if not isinstance(version, tuple) or not all(isinstance(item, int) for item in version):
            fail("bl_info.version is not an integer tuple")
        return ".".join(str(item) for item in version)
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


def load_receipt(reference: str, label: str) -> dict:
    if not isinstance(reference, str) or not reference.strip():
        fail(f"{label} validated capability requires a receipt path")
    path = REPO_ROOT / reference
    try:
        path.relative_to(REPO_ROOT)
    except ValueError:
        fail(f"{label} receipt must resolve inside repository")
    if not path.is_file():
        fail(f"{label} receipt not found: {reference}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_common_receipt(receipt: dict, capability: dict, stage: dict) -> None:
    label = stage["label"]
    if receipt.get("validation_state") != "PASS":
        fail(f"{label} receipt requires validation_state PASS")
    if receipt.get("validation_scope") != stage["scope"]:
        fail(f"{label} receipt scope mismatch: {receipt.get('validation_scope')!r}")
    if receipt.get("runtime_id") != capability.get("runtime_id"):
        fail(f"{label} receipt runtime_id mismatch")
    if receipt.get("runtime_version") != capability.get("runtime_version"):
        fail(f"{label} receipt runtime_version mismatch")
    if receipt.get("runtime_result") != "PASS":
        fail(f"{label} receipt runtime_result must be PASS")

    expected_fingerprint = source_fingerprint(stage["script"])
    if receipt.get("source_fingerprint_sha256") != expected_fingerprint:
        fail(
            f"{label} receipt stale: receipt={receipt.get('source_fingerprint_sha256')!r} "
            f"current={expected_fingerprint}"
        )

    workflow = receipt.get("workflow", {})
    if workflow.get("conclusion") != "success" or not workflow.get("run_id") or not workflow.get("job_id"):
        fail(f"{label} receipt must identify a successful workflow run and job")

    package = receipt.get("extension_package", {})
    for gate in ("source_manifest_validate", "build", "built_package_validate"):
        if package.get(gate) != "PASS":
            fail(f"{label} package gate not PASS: {gate}")
    if not package.get("sha256") or not package.get("size_bytes"):
        fail(f"{label} receipt requires extension package SHA256 and byte size")

    host = receipt.get("host", {})
    if host.get("checksum_manifest_result") != "PASS" or not host.get("blender_archive_sha256"):
        fail(f"{label} receipt requires official Blender checksum evidence")
    if host.get("blender_version") != "5.1.2":
        fail(f"{label} receipt must be bound to Blender 5.1.2")

    tested_head = receipt.get("tested_branch_head")
    if not isinstance(tested_head, str) or len(tested_head) != 40:
        fail(f"{label} tested_branch_head must be a full commit SHA")

    runtime_checks = set(receipt.get("runtime_checks", []))
    missing_checks = sorted(set(stage["checks"]) - runtime_checks)
    if missing_checks:
        fail(f"{label} receipt missing runtime checks: {missing_checks}")

    failures = receipt.get("expected_failure_cases", {})
    for case in stage.get("failures", ()):
        if failures.get(case) != "PASS":
            fail(f"{label} expected failure case not PASS: {case}")

    for regression in stage.get("regressions", ()):
        if receipt.get(regression) != "PASS":
            fail(f"{label} missing same-job regression PASS: {regression}")


def validate_stage_receipt(capability: dict, status: dict, stage: dict) -> dict | None:
    validated = set(status.get(stage["status_key"], []))
    receipt_ref = capability.get(stage["receipt_key"])
    if not validated:
        if receipt_ref:
            fail(f"{stage['label']} receipt exists but {stage['status_key']} is empty")
        return None
    missing_caps = sorted(set(stage["capabilities"]) - validated)
    if missing_caps:
        fail(f"{stage['label']} validated capability set missing: {missing_caps}")
    receipt = load_receipt(receipt_ref, stage["label"])
    validate_common_receipt(receipt, capability, stage)
    return receipt


STAGES = [
    {
        "label": "Stage 2",
        "status_key": "VALIDATED_STAGE2_HEADLESS",
        "receipt_key": "validation_receipt",
        "script": RUNTIME_ROOT / "tests" / "validate_stage2.py",
        "scope": "STAGE2_HEADLESS_CORE_AND_EXTENSION_PACKAGE",
        "checks": {
            "registration", "persistent_metadata", "duplicate_ole_id_expected_failure",
            "identity_collision_repair_operator", "missing_dependency_expected_failure",
            "dependency_cycle_expected_failure", "dependency_graph", "stale_propagation",
            "geometry_baseline_diff", "configuration_capture_restore",
            "bom_grouping_and_conflict_detection", "review_state_separation",
            "scene_unit_scale_round_trip", "blend_save_reopen_persistence",
            "audit_v0.2", "manifest_v0.2",
        },
        "failures": {
            "duplicate_ole_id_detect_and_repair", "missing_dependency_expected_failure",
            "dependency_cycle_expected_failure",
        },
        "capabilities": {
            "dependency_graph_resolution", "stale_dependency_propagation",
            "geometry_baseline_diff", "review_state_separation", "export_manifest_v0.2_core",
        },
    },
    {
        "label": "Stage 3 Direct",
        "status_key": "VALIDATED_STAGE3_DIRECT",
        "receipt_key": "stage3_direct_validation_receipt",
        "script": RUNTIME_ROOT / "tests" / "validate_stage3_direct.py",
        "scope": "STAGE3_DIRECT_MODELING",
        "checks": {
            "direct_metric_dimensions_operator", "direct_dimensions_applied_scale",
            "direct_geometry_change_stale_propagation", "direct_operation_metric_record",
            "linear_duplicate_operator", "linear_duplicate_unique_ole_ids",
            "linear_duplicate_stable_source_provenance", "linear_duplicate_linked_mesh",
            "linear_duplicate_metric_spacing", "post_direct_audit_no_duplicate_ids",
        },
        "regressions": {"stage2_regression_in_same_job"},
        "capabilities": {"direct_metric_dimensions_operator", "deterministic_linear_duplicate_operator"},
    },
    {
        "label": "Stage 3 Feature Stack",
        "status_key": "VALIDATED_STAGE3_FEATURE_STACK",
        "receipt_key": "stage3_feature_stack_validation_receipt",
        "script": RUNTIME_ROOT / "tests" / "validate_stage3_features.py",
        "scope": "STAGE3_DIRECT_FEATURE_STACK",
        "checks": {
            "planar_extrude_modifier_feature", "planar_extrude_metric_depth",
            "planar_extrude_evaluated_geometry", "nonplanar_extrude_expected_failure",
            "shell_modifier_feature", "bevel_chamfer_modifier_feature", "mirror_modifier_feature",
            "linear_pattern_modifier_feature", "linear_pattern_metric_spacing",
            "feature_history_stable_ids_and_order", "feature_stack_order_drift_expected_failure",
            "feature_geometry_change_stale_propagation", "boolean_modifier_feature",
            "boolean_cutter_ole_provenance", "boolean_dependency_graph_binding",
            "boolean_cutter_change_stale_propagation", "feature_stack_save_reopen_persistence",
        },
        "failures": {"nonplanar_planar_extrude", "manual_modifier_order_drift"},
        "regressions": {"stage2_regression_in_same_job", "stage3_direct_regression_in_same_job"},
        "capabilities": {
            "planar_extrude_modifier_feature", "shell_modifier_feature", "bevel_chamfer_modifier_feature",
            "mirror_modifier_feature", "linear_pattern_modifier_feature", "boolean_modifier_feature",
            "feature_history_stable_ids_and_order",
        },
    },
    {
        "label": "Stage 3 Feature Editing",
        "status_key": "VALIDATED_STAGE3_FEATURE_EDITING",
        "receipt_key": "stage3_feature_editing_validation_receipt",
        "script": RUNTIME_ROOT / "tests" / "validate_stage3_feature_editing.py",
        "scope": "STAGE3_FEATURE_EDITING",
        "checks": {
            "stable_feature_id_parameter_edit", "feature_parameter_edit_hits_real_modifier",
            "feature_edit_revision_increment", "feature_edit_downstream_stale_propagation",
            "feature_suppress_restore", "feature_suppression_history_modifier_sync",
            "governed_feature_reorder", "governed_reorder_history_order_sync",
            "feature_remove_tombstone", "feature_event_log_monotonic",
            "boolean_dependency_added_by_feature_provenance", "boolean_feature_owned_dependency_cleanup",
            "boolean_preexisting_dependency_preservation", "unknown_feature_id_expected_failure",
            "feature_edit_save_reopen_persistence", "tombstone_save_reopen_persistence",
            "event_log_save_reopen_persistence",
        },
        "failures": {"unknown_feature_id"},
        "regressions": {
            "stage2_regression_in_same_job", "stage3_direct_regression_in_same_job",
            "stage3_feature_stack_regression_in_same_job",
        },
        "capabilities": {
            "stable_feature_id_parameter_edit", "feature_suppress_restore", "governed_feature_reorder",
            "feature_remove_tombstone", "feature_event_log_monotonic",
            "boolean_preexisting_dependency_preservation",
        },
    },
    {
        "label": "Stage 3 Relation Kernel",
        "status_key": "VALIDATED_STAGE3_RELATION",
        "receipt_key": "stage3_relation_validation_receipt",
        "script": RUNTIME_ROOT / "tests" / "validate_stage3_relations.py",
        "scope": "STAGE3_RELATION_KERNEL",
        "checks": {
            "stable_relation_id_registry", "driver_driven_ole_provenance",
            "scene_unit_metric_contract_independent_expectation", "origin_distance_capture_current_metric",
            "origin_distance_tolerance_evaluation", "axis_offset_signed_metric_evaluation",
            "axis_parallel_angular_evaluation", "relation_solver_claim_false",
            "relation_dependency_graph_binding", "relation_failure_driven_stale",
            "relation_failure_downstream_stale_propagation", "relation_restore_pass",
            "duplicate_relation_expected_failure", "relation_dependency_cycle_expected_failure",
            "relation_cycle_failure_no_registry_pollution", "relation_cycle_failure_no_dependency_mutation",
            "missing_relation_object_expected_failure", "relation_dependency_added_by_relation_provenance",
            "relation_owned_dependency_cleanup", "relation_preexisting_dependency_preservation",
            "relation_remove_tombstone", "relation_event_log_monotonic",
            "relation_registry_save_reopen_persistence", "relation_tombstone_save_reopen_persistence",
            "relation_event_log_save_reopen_persistence",
        },
        "failures": {"duplicate_active_relation", "relation_dependency_cycle", "missing_relation_object"},
        "regressions": {
            "stage2_regression_in_same_job", "stage3_direct_regression_in_same_job",
            "stage3_feature_stack_regression_in_same_job", "stage3_feature_editing_regression_in_same_job",
        },
        "capabilities": {
            "stable_relation_id_registry", "origin_distance_tolerance_evaluation",
            "relation_dependency_graph_binding", "relation_failure_downstream_stale_propagation",
            "relation_dependency_cycle_failure_gate", "missing_relation_object_failure_gate",
            "relation_remove_tombstone",
        },
    },
    {
        "label": "Stage 3 Relation Apply",
        "status_key": "VALIDATED_STAGE3_RELATION_APPLY",
        "receipt_key": "stage3_relation_apply_validation_receipt",
        "script": RUNTIME_ROOT / "tests" / "validate_stage3_relation_apply.py",
        "scope": "STAGE3_RELATION_APPLY",
        "checks": {
            "axis_offset_one_shot_apply", "axis_offset_preserves_orthogonal_world_coordinates",
            "axis_offset_restores_relation_pass", "origin_coincident_one_shot_apply",
            "origin_distance_pass_reference_capture", "origin_distance_reference_direction_provenance",
            "origin_distance_one_shot_restore", "origin_distance_restores_captured_direction",
            "relation_apply_solver_claim_false", "relation_apply_revision",
            "relation_apply_downstream_stale_propagation", "relation_apply_event_log",
            "uncaptured_distance_apply_expected_failure", "uncaptured_distance_failure_no_geometry_mutation",
            "ambiguous_distance_direction_expected_failure", "axis_parallel_multisolution_expected_failure",
            "axis_parallel_failure_no_rotation_mutation", "external_transform_authority_expected_failure",
            "external_authority_failure_no_transform_mutation", "missing_relation_apply_expected_failure",
            "relation_apply_reference_save_reopen_persistence", "relation_apply_revision_save_reopen_persistence",
            "relation_apply_event_save_reopen_persistence",
        },
        "failures": {
            "uncaptured_distance_direction", "ambiguous_distance_direction", "axis_parallel_multisolution",
            "external_transform_authority", "missing_relation_id",
        },
        "regressions": {
            "stage2_regression_in_same_job", "stage3_direct_regression_in_same_job",
            "stage3_feature_stack_regression_in_same_job", "stage3_feature_editing_regression_in_same_job",
            "stage3_relation_regression_in_same_job",
        },
        "capabilities": {
            "axis_offset_one_shot_apply", "origin_coincident_one_shot_apply",
            "origin_distance_pass_reference_capture", "origin_distance_one_shot_restore",
            "relation_apply_solver_claim_false", "external_transform_authority_apply_failure_gate",
        },
    },
    {
        "label": "Stage 3 Measurement",
        "status_key": "VALIDATED_STAGE3_MEASUREMENT",
        "receipt_key": "stage3_measurement_validation_receipt",
        "script": RUNTIME_ROOT / "tests" / "validate_stage3_measurement.py",
        "scope": "STAGE3_MEASUREMENT_SCALE_RULER",
        "checks": {
            "measurement_profile_scene_scale_preservation", "scene_unit_mm_round_trip",
            "measurement_snapshot_active_dimensions", "measurement_snapshot_pair_origin_distance",
            "exact_world_location_quantize", "quantize_axis_mask_preservation",
            "quantize_downstream_stale_propagation", "exact_mm_nudge",
            "external_transform_authority_quantize_failure", "external_authority_failure_no_transform_mutation",
            "atomic_multi_object_quantize_preflight", "atomic_quantize_failure_no_partial_mutation",
            "world_ruler_editable_mesh", "world_ruler_minor_major_tick_counts",
            "world_ruler_metric_baseline", "world_ruler_major_labels_with_units",
            "world_ruler_non_rendering_reference_scope", "reference_guide_audit_exclusion",
            "irregular_ruler_interval_expected_failure", "excessive_ruler_intervals_expected_failure",
            "excessive_ruler_labels_expected_failure", "native_increment_snap_configuration",
            "measurement_profile_save_reopen_persistence", "measurement_snapshot_save_reopen_persistence",
            "world_ruler_save_reopen_persistence", "measurement_event_log_save_reopen_persistence",
        },
        "failures": {
            "external_transform_authority", "atomic_batch_transform_authority",
            "irregular_ruler_interval", "excessive_ruler_intervals", "excessive_ruler_labels",
        },
        "regressions": {
            "stage2_regression_in_same_job", "stage3_direct_regression_in_same_job",
            "stage3_feature_stack_regression_in_same_job", "stage3_feature_editing_regression_in_same_job",
            "stage3_relation_regression_in_same_job", "stage3_relation_apply_regression_in_same_job",
        },
        "capabilities": {
            "measurement_profile_scene_scale_preservation", "measurement_snapshot_active_dimensions",
            "exact_world_location_quantize", "exact_mm_nudge", "atomic_multi_object_quantize_preflight",
            "world_ruler_editable_mesh", "reference_guide_audit_exclusion",
            "native_increment_snap_configuration",
        },
    },
    {
        "label": "Stage 3 Procedural",
        "status_key": "VALIDATED_STAGE3_PROCEDURAL",
        "receipt_key": "stage3_procedural_validation_receipt",
        "script": RUNTIME_ROOT / "tests" / "validate_stage3_procedural.py",
        "scope": "STAGE3_PROCEDURAL_FOUNDATION",
        "checks": {
            "parameter_metadata_mutation_api", "parameter_metadata_sanitization",
            "constraint_metadata_mutation_api", "constraint_metadata_sanitization",
            "metadata_mutation_does_not_claim_solver_geometry", "geometry_nodes_tree_creation",
            "geometry_nodes_modifier_binding", "geometry_nodes_passthrough_evaluation",
            "geometry_nodes_ole_provenance", "geometry_nodes_explicit_no_solver_claim",
            "geometry_nodes_save_reopen_persistence", "parameter_constraint_save_reopen_persistence",
        },
        "regressions": {
            "stage2_regression_in_same_job", "stage3_direct_regression_in_same_job",
            "stage3_feature_stack_regression_in_same_job", "stage3_feature_editing_regression_in_same_job",
            "stage3_relation_regression_in_same_job", "stage3_relation_apply_regression_in_same_job",
            "stage3_measurement_regression_in_same_job",
        },
        "capabilities": {"parameter_constraint_metadata_mutation_api", "geometry_nodes_support_probe"},
    },
]


def main() -> None:
    python_files = sorted(ADDON_ROOT.rglob("*.py")) + sorted((RUNTIME_ROOT / "tests").rglob("*.py"))
    if not python_files:
        fail("no Python files found")
    for path in python_files:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    with (ADDON_ROOT / "blender_manifest.toml").open("rb") as handle:
        manifest = tomllib.load(handle)
    capability = json.loads((PIPELINE_ROOT / "BLENDER_RUNTIME_CAPABILITY.json").read_text(encoding="utf-8"))
    schema = json.loads((ADDON_ROOT / "workbench_manifest.schema.json").read_text(encoding="utf-8"))
    bl_info_version = parse_bl_info_version(ADDON_ROOT / "__init__.py")
    versions = {bl_info_version, manifest.get("version"), capability.get("runtime_version")}
    if len(versions) != 1:
        fail(
            f"version mismatch bl_info={bl_info_version} manifest={manifest.get('version')} "
            f"capability={capability.get('runtime_version')}"
        )
    if manifest.get("blender_version_min") != "5.1.0":
        fail("unexpected minimum Blender version")
    schema_const = schema.get("properties", {}).get("schema", {}).get("const")
    if schema_const != "OLEANDER_BLENDER_WORKBENCH_MANIFEST_v0.2":
        fail(f"workbench manifest schema const mismatch: {schema_const}")

    lifecycle = capability.get("lifecycle_state")
    if lifecycle == UNVERIFIED_STATE:
        if capability.get("validation_receipt"):
            fail("unverified lifecycle must not claim a validation receipt")
        return
    if lifecycle != VALIDATED_STATE:
        fail(f"unsupported lifecycle_state: {lifecycle}")

    status = capability.get("implementation_status", {})
    receipts = {}
    for stage in STAGES:
        receipts[stage["label"]] = validate_stage_receipt(capability, status, stage)

    stage2 = receipts["Stage 2"]
    if stage2 is None:
        fail("validated lifecycle requires Stage 2 receipt")
    canonical_package = stage2["extension_package"]
    canonical_workflow = stage2["workflow"]
    for label, receipt in receipts.items():
        if receipt is None:
            fail(f"validated eight-layer contract requires non-empty {label} receipt")
        package = receipt["extension_package"]
        if package.get("sha256") != canonical_package.get("sha256") or package.get("size_bytes") != canonical_package.get("size_bytes"):
            fail(f"{label} receipt does not reference the same validated Extension package as Stage 2")
        workflow = receipt["workflow"]
        if workflow.get("run_id") != canonical_workflow.get("run_id") or workflow.get("job_id") != canonical_workflow.get("job_id"):
            fail(f"{label} receipt is not bound to the same real-Blender workflow/job as Stage 2")

    declared_not_implemented = set(status.get("DECLARED_NOT_IMPLEMENTED", []))
    required_nonclaims = {
        "cad_brep_sidecar", "solver_backed_sketch_constraints", "constraint_solver",
        "multi_relation_solver", "feature_solver", "engineering_approval", "manufacturing_release",
    }
    missing_nonclaims = sorted(required_nonclaims - declared_not_implemented)
    if missing_nonclaims:
        fail(f"capability contract lost required NOT IMPLEMENTED boundaries: {missing_nonclaims}")

    does_not_prove = set(capability.get("does_not_prove", []))
    required_boundaries = {
        "field_truth", "engineering_approval", "manufacturing_release", "constructability",
        "constraint_solver", "iterative_solver", "multi_relation_solver", "cad_brep",
        "viewport_grid_dimensional_authority", "screen_space_ruler_dimensional_authority", "design_pass",
    }
    missing_boundaries = sorted(required_boundaries - does_not_prove)
    if missing_boundaries:
        fail(f"capability contract lost does_not_prove boundaries: {missing_boundaries}")

    output = {
        "status": "PASS",
        "python_files_parsed": len(python_files),
        "runtime_version": bl_info_version,
        "lifecycle_state": lifecycle,
        "validated_layers": [stage["label"] for stage in STAGES],
        "extension_package_sha256": canonical_package["sha256"],
        "extension_package_size_bytes": canonical_package["size_bytes"],
        "workflow_run_id": canonical_workflow["run_id"],
        "source_fingerprints": {
            stage["label"]: source_fingerprint(stage["script"]) for stage in STAGES
        },
        "note": "Static PASS validates eight-layer receipt/contract integrity; it is not a substitute for Blender runtime execution.",
    }
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
