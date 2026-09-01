"""Repository-level static checks for the OLEANDER Blender Runtime.

This checker does not import bpy. It verifies Python syntax, runtime/version
contracts, ten independently fingerprint-bound real-Blender receipts,
positive-failure evidence, same-job regression ordering, package identity and
explicit authority boundaries. Static PASS is never a Blender runtime PASS.
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


def fail(message):
    raise SystemExit(f"STATIC_CHECK_FAIL: {message}")


def parse_bl_info_version(path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "bl_info" for target in node.targets):
            value = ast.literal_eval(node.value)
            version = value.get("version")
            if not isinstance(version, tuple) or not all(isinstance(item, int) for item in version):
                fail("bl_info.version is not an integer tuple")
            return ".".join(str(item) for item in version)
    fail("bl_info assignment not found")


def source_fingerprint(validation_script):
    paths = [path for path in ADDON_ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".py", ".json", ".toml"}]
    paths.append(validation_script)
    digest = hashlib.sha256()
    for path in sorted(set(paths), key=lambda item: item.as_posix()):
        digest.update(path.relative_to(PIPELINE_ROOT).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def load_receipt(reference, label):
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


STAGES = [
    {"label":"Stage 2","status_key":"VALIDATED_STAGE2_HEADLESS","receipt_key":"validation_receipt","script":"validate_stage2.py","scope":"STAGE2_HEADLESS_CORE_AND_EXTENSION_PACKAGE","checks":{"registration","persistent_metadata","duplicate_ole_id_expected_failure","identity_collision_repair_operator","missing_dependency_expected_failure","dependency_cycle_expected_failure","dependency_graph","stale_propagation","geometry_baseline_diff","configuration_capture_restore","bom_grouping_and_conflict_detection","review_state_separation","scene_unit_scale_round_trip","blend_save_reopen_persistence","audit_v0.2","manifest_v0.2"},"failures":{"duplicate_ole_id_detect_and_repair","missing_dependency_expected_failure","dependency_cycle_expected_failure"},"capabilities":{"dependency_graph_resolution","stale_dependency_propagation","geometry_baseline_diff","review_state_separation","export_manifest_v0.2_core"},"environment_key":"validated_environment"},
    {"label":"Stage 3 Direct","status_key":"VALIDATED_STAGE3_DIRECT","receipt_key":"stage3_direct_validation_receipt","script":"validate_stage3_direct.py","scope":"STAGE3_DIRECT_MODELING","checks":{"direct_metric_dimensions_operator","direct_dimensions_applied_scale","direct_geometry_change_stale_propagation","direct_operation_metric_record","linear_duplicate_operator","linear_duplicate_unique_ole_ids","linear_duplicate_stable_source_provenance","linear_duplicate_linked_mesh","linear_duplicate_metric_spacing","post_direct_audit_no_duplicate_ids"},"regressions":{"stage2_regression_in_same_job"},"capabilities":{"direct_metric_dimensions_operator","deterministic_linear_duplicate_operator"},"environment_key":"stage3_direct_validated_environment"},
    {"label":"Stage 3 Feature Stack","status_key":"VALIDATED_STAGE3_FEATURE_STACK","receipt_key":"stage3_feature_stack_validation_receipt","script":"validate_stage3_features.py","scope":"STAGE3_DIRECT_FEATURE_STACK","checks":{"planar_extrude_modifier_feature","planar_extrude_metric_depth","planar_extrude_evaluated_geometry","nonplanar_extrude_expected_failure","shell_modifier_feature","bevel_chamfer_modifier_feature","mirror_modifier_feature","linear_pattern_modifier_feature","linear_pattern_metric_spacing","feature_history_stable_ids_and_order","feature_stack_order_drift_expected_failure","feature_geometry_change_stale_propagation","boolean_modifier_feature","boolean_cutter_ole_provenance","boolean_dependency_graph_binding","boolean_cutter_change_stale_propagation","feature_stack_save_reopen_persistence"},"failures":{"nonplanar_planar_extrude","manual_modifier_order_drift"},"regressions":{"stage2_regression_in_same_job","stage3_direct_regression_in_same_job"},"capabilities":{"planar_extrude_modifier_feature","shell_modifier_feature","bevel_chamfer_modifier_feature","mirror_modifier_feature","linear_pattern_modifier_feature","boolean_modifier_feature","feature_history_stable_ids_and_order"},"environment_key":"stage3_feature_stack_validated_environment"},
    {"label":"Stage 3 Feature Editing","status_key":"VALIDATED_STAGE3_FEATURE_EDITING","receipt_key":"stage3_feature_editing_validation_receipt","script":"validate_stage3_feature_editing.py","scope":"STAGE3_FEATURE_EDITING","checks":{"stable_feature_id_parameter_edit","feature_parameter_edit_hits_real_modifier","feature_edit_revision_increment","feature_edit_downstream_stale_propagation","feature_suppress_restore","feature_suppression_history_modifier_sync","governed_feature_reorder","governed_reorder_history_order_sync","feature_remove_tombstone","feature_event_log_monotonic","boolean_dependency_added_by_feature_provenance","boolean_feature_owned_dependency_cleanup","boolean_preexisting_dependency_preservation","unknown_feature_id_expected_failure","feature_edit_save_reopen_persistence","tombstone_save_reopen_persistence","event_log_save_reopen_persistence"},"failures":{"unknown_feature_id"},"regressions":{"stage2_regression_in_same_job","stage3_direct_regression_in_same_job","stage3_feature_stack_regression_in_same_job"},"capabilities":{"stable_feature_id_parameter_edit","feature_suppress_restore","governed_feature_reorder","feature_remove_tombstone","feature_event_log_monotonic","boolean_preexisting_dependency_preservation"},"environment_key":"stage3_feature_editing_validated_environment"},
    {"label":"Stage 3 Relation Kernel","status_key":"VALIDATED_STAGE3_RELATION","receipt_key":"stage3_relation_validation_receipt","script":"validate_stage3_relations.py","scope":"STAGE3_RELATION_KERNEL","checks":{"stable_relation_id_registry","driver_driven_ole_provenance","scene_unit_metric_contract_independent_expectation","origin_distance_capture_current_metric","origin_distance_tolerance_evaluation","axis_offset_signed_metric_evaluation","axis_parallel_angular_evaluation","relation_solver_claim_false","relation_dependency_graph_binding","relation_failure_driven_stale","relation_failure_downstream_stale_propagation","relation_restore_pass","duplicate_relation_expected_failure","relation_dependency_cycle_expected_failure","relation_cycle_failure_no_registry_pollution","relation_cycle_failure_no_dependency_mutation","missing_relation_object_expected_failure","relation_dependency_added_by_relation_provenance","relation_owned_dependency_cleanup","relation_preexisting_dependency_preservation","relation_remove_tombstone","relation_event_log_monotonic","relation_registry_save_reopen_persistence","relation_tombstone_save_reopen_persistence","relation_event_log_save_reopen_persistence"},"failures":{"duplicate_active_relation","relation_dependency_cycle","missing_relation_object"},"regressions":{"stage2_regression_in_same_job","stage3_direct_regression_in_same_job","stage3_feature_stack_regression_in_same_job","stage3_feature_editing_regression_in_same_job"},"capabilities":{"stable_relation_id_registry","origin_distance_tolerance_evaluation","relation_dependency_graph_binding","relation_failure_downstream_stale_propagation","relation_dependency_cycle_failure_gate","missing_relation_object_failure_gate","relation_remove_tombstone"},"environment_key":"stage3_relation_validated_environment"},
    {"label":"Stage 3 Relation Apply","status_key":"VALIDATED_STAGE3_RELATION_APPLY","receipt_key":"stage3_relation_apply_validation_receipt","script":"validate_stage3_relation_apply.py","scope":"STAGE3_RELATION_APPLY","checks":{"axis_offset_one_shot_apply","axis_offset_preserves_orthogonal_world_coordinates","axis_offset_restores_relation_pass","origin_coincident_one_shot_apply","origin_distance_pass_reference_capture","origin_distance_reference_direction_provenance","origin_distance_one_shot_restore","origin_distance_restores_captured_direction","relation_apply_solver_claim_false","relation_apply_revision","relation_apply_downstream_stale_propagation","relation_apply_event_log","uncaptured_distance_apply_expected_failure","uncaptured_distance_failure_no_geometry_mutation","ambiguous_distance_direction_expected_failure","axis_parallel_multisolution_expected_failure","axis_parallel_failure_no_rotation_mutation","external_transform_authority_expected_failure","external_authority_failure_no_transform_mutation","missing_relation_apply_expected_failure","relation_apply_reference_save_reopen_persistence","relation_apply_revision_save_reopen_persistence","relation_apply_event_save_reopen_persistence"},"failures":{"uncaptured_distance_direction","ambiguous_distance_direction","axis_parallel_multisolution","external_transform_authority","missing_relation_id"},"regressions":{"stage2_regression_in_same_job","stage3_direct_regression_in_same_job","stage3_feature_stack_regression_in_same_job","stage3_feature_editing_regression_in_same_job","stage3_relation_regression_in_same_job"},"capabilities":{"axis_offset_one_shot_apply","origin_coincident_one_shot_apply","origin_distance_pass_reference_capture","origin_distance_one_shot_restore","relation_apply_solver_claim_false","external_transform_authority_apply_failure_gate"},"environment_key":"stage3_relation_apply_validated_environment"},
    {"label":"Stage 3 Measurement","status_key":"VALIDATED_STAGE3_MEASUREMENT","receipt_key":"stage3_measurement_validation_receipt","script":"validate_stage3_measurement.py","scope":"STAGE3_MEASUREMENT_SCALE_RULER","checks":{"measurement_profile_scene_scale_preservation","scene_unit_mm_round_trip","measurement_snapshot_active_dimensions","measurement_snapshot_pair_origin_distance","exact_world_location_quantize","quantize_axis_mask_preservation","quantize_downstream_stale_propagation","exact_mm_nudge","external_transform_authority_quantize_failure","external_authority_failure_no_transform_mutation","atomic_multi_object_quantize_preflight","atomic_quantize_failure_no_partial_mutation","world_ruler_editable_mesh","world_ruler_minor_major_tick_counts","world_ruler_metric_baseline","world_ruler_major_labels_with_units","world_ruler_non_rendering_reference_scope","reference_guide_audit_exclusion","irregular_ruler_interval_expected_failure","excessive_ruler_intervals_expected_failure","excessive_ruler_labels_expected_failure","native_increment_snap_configuration","measurement_profile_save_reopen_persistence","measurement_snapshot_save_reopen_persistence","world_ruler_save_reopen_persistence","measurement_event_log_save_reopen_persistence"},"failures":{"external_transform_authority","atomic_batch_transform_authority","irregular_ruler_interval","excessive_ruler_intervals","excessive_ruler_labels"},"regressions":{"stage2_regression_in_same_job","stage3_direct_regression_in_same_job","stage3_feature_stack_regression_in_same_job","stage3_feature_editing_regression_in_same_job","stage3_relation_regression_in_same_job","stage3_relation_apply_regression_in_same_job"},"capabilities":{"measurement_profile_scene_scale_preservation","measurement_snapshot_active_dimensions","exact_world_location_quantize","exact_mm_nudge","atomic_multi_object_quantize_preflight","world_ruler_editable_mesh","reference_guide_audit_exclusion","native_increment_snap_configuration"},"environment_key":"stage3_measurement_validated_environment"},
    {"label":"Stage 3 Angular Datum","status_key":"VALIDATED_STAGE3_ANGULAR_DATUM","receipt_key":"stage3_angular_datum_validation_receipt","script":"validate_stage3_angular_datum.py","scope":"STAGE3_ANGULAR_DATUM_CONSTRUCTION","checks":{"angular_quantize_axis_mask","angular_quantize_metric_degree_contract","angular_quantize_downstream_stale","angular_nudge_exact_degrees","angular_batch_transform_authority_preflight","angular_batch_failure_no_partial_mutation","angle_guide_editable_reference_geometry","angle_guide_metric_radius","angle_guide_minor_major_interval_contract","datum_axis_metric_length","datum_plane_metric_size","construction_line_metric_length_offset","angular_datum_reference_guide_audit_exclusion","invalid_rotation_step_expected_failure","irregular_angle_interval_expected_failure","excessive_angle_intervals_expected_failure","invalid_datum_axis_expected_failure","invalid_datum_plane_expected_failure","invalid_construction_line_expected_failure","angular_operator_registration","datum_operator_registration","angular_datum_save_reopen_persistence"},"failures":{"external_transform_authority","invalid_rotation_step","irregular_angle_interval","excessive_angle_intervals","invalid_datum_axis","invalid_datum_plane","invalid_construction_line"},"regressions":{"stage2_regression_in_same_job","stage3_direct_regression_in_same_job","stage3_feature_stack_regression_in_same_job","stage3_feature_editing_regression_in_same_job","stage3_relation_regression_in_same_job","stage3_relation_apply_regression_in_same_job","stage3_measurement_regression_in_same_job"},"capabilities":{"angular_quantize_axis_mask","angular_nudge_exact_degrees","angle_guide_editable_reference_geometry","datum_axis_metric_length","datum_plane_metric_size","construction_line_metric_length_offset","angular_datum_reference_guide_audit_exclusion"},"environment_key":"stage3_angular_datum_validated_environment"},
    {"label":"Stage 3 Precision Inference","status_key":"VALIDATED_STAGE3_PRECISION_INFERENCE","receipt_key":"stage3_precision_inference_validation_receipt","script":"validate_stage3_precision_inference.py","scope":"STAGE3_PRECISION_INFERENCE_FOUNDATION","checks":{"display_precision_state","linear_display_formatting","angular_display_formatting","display_precision_range_failure","signed_component_world_measurement","component_origin_distance_metric","aabb_axis_gap_metric","aabb_clearance_authority_boundary","mesh_endpoint_candidates","mesh_midpoint_candidates","mesh_face_center_candidates","mesh_origin_candidate","inference_no_solver_claim","nearest_inference_metric_radius","nearest_inference_kind_filter","inference_radius_miss","invalid_snap_radius_expected_failure","candidate_limit_expected_failure","nonmesh_inference_expected_failure","precision_snapshot_combined_measurement","precision_snapshot_inference_summary","display_precision_operator_registration","precision_snapshot_operator_registration","display_precision_save_reopen_persistence","precision_snapshot_save_reopen_persistence"},"failures":{"invalid_display_precision","invalid_snap_radius","candidate_limit","nonmesh_inference"},"regressions":{"stage2_regression_in_same_job","stage3_direct_regression_in_same_job","stage3_feature_stack_regression_in_same_job","stage3_feature_editing_regression_in_same_job","stage3_relation_regression_in_same_job","stage3_relation_apply_regression_in_same_job","stage3_measurement_regression_in_same_job","stage3_angular_datum_regression_in_same_job"},"capabilities":{"display_precision_state","signed_component_world_measurement","aabb_clearance_authority_boundary","mesh_endpoint_candidates","mesh_midpoint_candidates","mesh_face_center_candidates","nearest_inference_metric_radius","precision_snapshot_save_reopen_persistence"},"environment_key":"stage3_precision_inference_validated_environment"},
    {"label":"Stage 3 Procedural","status_key":"VALIDATED_STAGE3_PROCEDURAL","receipt_key":"stage3_procedural_validation_receipt","script":"validate_stage3_procedural.py","scope":"STAGE3_PROCEDURAL_FOUNDATION","checks":{"parameter_metadata_mutation_api","parameter_metadata_sanitization","constraint_metadata_mutation_api","constraint_metadata_sanitization","metadata_mutation_does_not_claim_solver_geometry","geometry_nodes_tree_creation","geometry_nodes_modifier_binding","geometry_nodes_passthrough_evaluation","geometry_nodes_ole_provenance","geometry_nodes_explicit_no_solver_claim","geometry_nodes_save_reopen_persistence","parameter_constraint_save_reopen_persistence"},"regressions":{"stage2_regression_in_same_job","stage3_direct_regression_in_same_job","stage3_feature_stack_regression_in_same_job","stage3_feature_editing_regression_in_same_job","stage3_relation_regression_in_same_job","stage3_relation_apply_regression_in_same_job","stage3_measurement_regression_in_same_job","stage3_angular_datum_regression_in_same_job","stage3_precision_inference_regression_in_same_job"},"capabilities":{"parameter_constraint_metadata_mutation_api","geometry_nodes_support_probe"},"environment_key":"stage3_procedural_validated_environment"}
]


def validate_stage(capability, status, stage):
    validated = set(status.get(stage["status_key"], []))
    if not validated:
        fail(f"{stage['label']} validated capability set is empty")
    missing_caps = sorted(set(stage["capabilities"]) - validated)
    if missing_caps:
        fail(f"{stage['label']} validated capability set missing: {missing_caps}")
    receipt = load_receipt(capability.get(stage["receipt_key"]), stage["label"])
    if receipt.get("validation_state") != "PASS" or receipt.get("runtime_result") != "PASS":
        fail(f"{stage['label']} receipt must be PASS")
    if receipt.get("validation_scope") != stage["scope"]:
        fail(f"{stage['label']} receipt scope mismatch")
    if receipt.get("runtime_id") != capability.get("runtime_id") or receipt.get("runtime_version") != capability.get("runtime_version"):
        fail(f"{stage['label']} runtime identity/version mismatch")
    expected = source_fingerprint(RUNTIME_ROOT / "tests" / stage["script"])
    if receipt.get("source_fingerprint_sha256") != expected:
        fail(f"{stage['label']} receipt stale: {receipt.get('source_fingerprint_sha256')} != {expected}")
    workflow = receipt.get("workflow", {})
    package = receipt.get("extension_package", {})
    host = receipt.get("host", {})
    if workflow.get("conclusion") != "success" or not workflow.get("run_id") or not workflow.get("job_id"):
        fail(f"{stage['label']} successful workflow evidence missing")
    if host.get("blender_version") != "5.1.2" or host.get("checksum_manifest_result") != "PASS" or not host.get("blender_archive_sha256"):
        fail(f"{stage['label']} Blender checksum evidence invalid")
    for gate in ("source_manifest_validate","build","built_package_validate"):
        if package.get(gate) != "PASS":
            fail(f"{stage['label']} extension package gate not PASS: {gate}")
    if not package.get("sha256") or not package.get("size_bytes"):
        fail(f"{stage['label']} extension package identity missing")
    missing_checks = sorted(set(stage["checks"]) - set(receipt.get("runtime_checks", [])))
    if missing_checks:
        fail(f"{stage['label']} receipt missing runtime checks: {missing_checks}")
    failures = receipt.get("expected_failure_cases", {})
    for case in stage.get("failures", set()):
        if failures.get(case) != "PASS":
            fail(f"{stage['label']} expected failure not PASS: {case}")
    for regression in stage.get("regressions", set()):
        if receipt.get(regression) != "PASS":
            fail(f"{stage['label']} same-job regression missing: {regression}")
    environment = capability.get(stage["environment_key"], {})
    if environment.get("source_fingerprint_sha256") != expected or environment.get("workflow_run_id") != workflow.get("run_id") or environment.get("runtime_result") != "PASS":
        fail(f"{stage['label']} capability validated environment does not match receipt")
    if environment.get("tested_branch_head") != receipt.get("tested_branch_head"):
        fail(f"{stage['label']} validated environment head does not match receipt")
    return receipt


def main():
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
    if len({bl_info_version, manifest.get("version"), capability.get("runtime_version")}) != 1:
        fail("runtime version mismatch")
    if manifest.get("blender_version_min") != "5.1.0":
        fail("unexpected minimum Blender version")
    if schema.get("properties", {}).get("schema", {}).get("const") != "OLEANDER_BLENDER_WORKBENCH_MANIFEST_v0.2":
        fail("workbench manifest schema const mismatch")
    lifecycle = capability.get("lifecycle_state")
    if lifecycle == UNVERIFIED_STATE:
        if capability.get("validation_receipt"):
            fail("unverified lifecycle must not claim validation receipt")
        return
    if lifecycle != VALIDATED_STATE:
        fail(f"unsupported lifecycle_state: {lifecycle}")
    status = capability.get("implementation_status", {})
    receipts = {stage["label"]: validate_stage(capability, status, stage) for stage in STAGES}
    stage2 = receipts["Stage 2"]
    canonical_package = stage2["extension_package"]
    canonical_workflow = stage2["workflow"]
    for label, receipt in receipts.items():
        package = receipt["extension_package"]
        workflow = receipt["workflow"]
        if package.get("sha256") != canonical_package.get("sha256") or package.get("size_bytes") != canonical_package.get("size_bytes"):
            fail(f"{label} receipt does not reference same Extension package as Stage 2")
        if workflow.get("run_id") != canonical_workflow.get("run_id") or workflow.get("job_id") != canonical_workflow.get("job_id"):
            fail(f"{label} receipt does not reference same real-Blender job as Stage 2")
    declared = set(status.get("DECLARED_NOT_IMPLEMENTED", []))
    required_not_implemented = {"cad_brep_sidecar","solver_backed_sketch_constraints","constraint_solver","multi_relation_solver","solver_backed_angular_constraints","cad_datum_feature_authority","true_surface_clearance","perpendicular_constraint_solver","parallel_constraint_solver","intersection_constraint_solver","persistent_snap_constraint","cad_sketch_solver","feature_solver","engineering_approval","manufacturing_release"}
    missing_declared = sorted(required_not_implemented - declared)
    if missing_declared:
        fail(f"capability lost NOT IMPLEMENTED boundaries: {missing_declared}")
    boundaries = set(capability.get("does_not_prove", []))
    required_boundaries = {"field_truth","engineering_approval","manufacturing_release","constructability","constraint_solver","iterative_solver","multi_relation_solver","solver_backed_angular_constraints","cad_datum_feature_authority","true_surface_clearance","perpendicular_constraint_solver","parallel_constraint_solver","intersection_constraint_solver","persistent_snap_constraint","cad_sketch_solver","cad_brep","viewport_grid_dimensional_authority","screen_space_ruler_dimensional_authority","screen_space_angle_dimensional_authority","design_pass"}
    missing_boundaries = sorted(required_boundaries - boundaries)
    if missing_boundaries:
        fail(f"capability lost does_not_prove boundaries: {missing_boundaries}")
    print(json.dumps({"status":"PASS","python_files_parsed":len(python_files),"runtime_version":bl_info_version,"lifecycle_state":lifecycle,"validated_layers":[stage["label"] for stage in STAGES],"extension_package_sha256":canonical_package["sha256"],"extension_package_size_bytes":canonical_package["size_bytes"],"workflow_run_id":canonical_workflow["run_id"],"source_fingerprints":{stage["label"]:source_fingerprint(RUNTIME_ROOT / "tests" / stage["script"]) for stage in STAGES},"note":"Static PASS validates ten-layer receipt/contract integrity; it is not a substitute for Blender runtime execution."}, sort_keys=True))


if __name__ == "__main__":
    main()
