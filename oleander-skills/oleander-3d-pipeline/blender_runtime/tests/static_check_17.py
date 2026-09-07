"""Seventeen-layer static contract for OLEANDER Blender Runtime v0.2.

Adds Design Intent Rebuild Plan as an independently receipt-bound stage after
Batch Apply and before Procedural. Rebuild planning derives a minimal dirty
parameter closure and an execution order, but execution remains explicit and
reuses the validated atomic Batch Apply path.

This contract does not create an equation solver, automatic value derivation,
automatic rebuild execution, or CAD parametric feature authority.
"""

from __future__ import annotations

import contextlib
import io
import json

import static_check as base
import static_check_15 as stage15
import static_check_16 as stage16


REBUILD_STAGE = {
    "label": "Stage 3 Design Intent Rebuild Plan",
    "status_key": "VALIDATED_STAGE3_DESIGN_INTENT_REBUILD",
    "receipt_key": "stage3_design_intent_rebuild_validation_receipt",
    "script": "validate_stage3_design_intent_rebuild.py",
    "scope": "STAGE3_DESIGN_INTENT_REBUILD_PLAN_FOUNDATION",
    "checks": {
        "rebuild_plan_operator_registration",
        "event_log_dirty_seed_inference",
        "direct_stale_marker_dirty_seed_inference",
        "minimal_dirty_seed_set",
        "downstream_parameter_dependency_closure",
        "selected_dependency_topological_order",
        "no_clean_upstream_expansion",
        "non_mutating_rebuild_plan",
        "impact_preview_bound_object_ids",
        "deterministic_plan_sha256",
        "event_watermark_lock",
        "parameter_revision_state_lock",
        "stale_plan_positive_failure",
        "stale_plan_failure_zero_geometry_mutation",
        "duplicate_seed_positive_failure",
        "missing_seed_positive_failure",
        "stored_plan_save_reopen_persistence",
        "explicit_rebuild_execution_via_atomic_batch",
        "downstream_stored_value_reapply_without_derivation",
        "successful_rebuild_cleans_event_dirtiness",
        "clean_graph_noop_plan",
        "rebuild_result_receipt_persistence",
        "no_solver_claim",
        "no_automatic_execution_claim",
        "no_parameter_value_derivation_claim",
        "no_automatic_geometry_rebuild_claim",
        "no_cad_parametric_rebuild_claim",
    },
    "failures": {
        "stale_plan_positive_failure",
        "duplicate_seed_positive_failure",
        "missing_seed_positive_failure",
    },
    "regressions": {
        "stage2_regression_in_same_job",
        "stage3_direct_regression_in_same_job",
        "stage3_feature_stack_regression_in_same_job",
        "stage3_feature_editing_regression_in_same_job",
        "stage3_relation_regression_in_same_job",
        "stage3_relation_apply_regression_in_same_job",
        "stage3_measurement_regression_in_same_job",
        "stage3_angular_datum_regression_in_same_job",
        "stage3_precision_inference_regression_in_same_job",
        "stage3_inference_v2_regression_in_same_job",
        "stage3_mesh_clearance_regression_in_same_job",
        "stage3_surface_diagnostics_regression_in_same_job",
        "stage3_design_intent_regression_in_same_job",
        "stage3_design_intent_apply_regression_in_same_job",
        "stage3_design_intent_batch_regression_in_same_job",
    },
    "capabilities": {
        "rebuild_plan_operator_registration",
        "event_log_dirty_seed_inference",
        "direct_stale_marker_dirty_seed_inference",
        "minimal_dirty_seed_set",
        "downstream_parameter_dependency_closure",
        "selected_dependency_topological_order",
        "no_clean_upstream_expansion",
        "non_mutating_rebuild_plan",
        "impact_preview_bound_object_ids",
        "deterministic_plan_sha256",
        "event_watermark_lock",
        "parameter_revision_state_lock",
        "stored_plan_save_reopen_persistence",
        "explicit_rebuild_execution_via_atomic_batch",
        "downstream_stored_value_reapply_without_derivation",
        "successful_rebuild_cleans_event_dirtiness",
        "clean_graph_noop_plan",
        "rebuild_result_receipt_persistence",
        "no_solver_claim",
        "no_automatic_execution_claim",
        "no_parameter_value_derivation_claim",
        "no_automatic_geometry_rebuild_claim",
        "no_cad_parametric_rebuild_claim",
    },
    "environment_key": "stage3_design_intent_rebuild_validated_environment",
}

REBUILD_NOT_IMPLEMENTED = {
    "constraint_solver",
    "equation_solver",
    "multi_parameter_solver",
    "automatic_parameter_value_derivation",
    "automatic_rebuild_execution",
    "automatic_parameter_geometry_rebuild",
    "cad_parametric_feature_rebuild",
}

REBUILD_L1 = {
    "design_intent_dirty_inference",
    "design_intent_rebuild_plan",
    "downstream_parameter_rebuild_closure",
    "rebuild_plan_event_watermark",
    "rebuild_plan_state_hash",
    "explicit_rebuild_plan_execution",
}


def insert_before_procedural(stage):
    if any(item.get("label") == stage["label"] for item in base.STAGES):
        return
    index = next(
        (i for i, item in enumerate(base.STAGES) if item.get("label") == "Stage 3 Procedural"),
        len(base.STAGES),
    )
    base.STAGES.insert(index, stage)


def main():
    # Register all stages added by 15/16 without executing their layer-count
    # assertions, then add Rebuild Plan as the 17th stage.
    stage15.insert_before_procedural(stage15.SURFACE_STAGE)
    stage15.insert_before_procedural(stage15.DESIGN_INTENT_STAGE)
    stage15.insert_before_procedural(stage15.DESIGN_INTENT_APPLY_STAGE)
    stage16.insert_before_procedural(stage16.DESIGN_INTENT_BATCH_STAGE)
    insert_before_procedural(REBUILD_STAGE)

    procedural = next(
        item for item in base.STAGES if item.get("label") == "Stage 3 Procedural"
    )
    procedural.setdefault("regressions", set()).update(
        {
            "stage3_surface_diagnostics_regression_in_same_job",
            "stage3_design_intent_regression_in_same_job",
            "stage3_design_intent_apply_regression_in_same_job",
            "stage3_design_intent_batch_regression_in_same_job",
            "stage3_design_intent_rebuild_regression_in_same_job",
        }
    )

    capability = json.loads(
        (base.PIPELINE_ROOT / "BLENDER_RUNTIME_CAPABILITY.json").read_text(encoding="utf-8")
    )

    declared_not_implemented = set(
        capability.get("implementation_status", {}).get("DECLARED_NOT_IMPLEMENTED", [])
    )
    missing_boundaries = sorted(REBUILD_NOT_IMPLEMENTED - declared_not_implemented)
    if missing_boundaries:
        base.fail(f"rebuild-plan non-implementation boundaries missing: {missing_boundaries}")

    l1 = set(capability.get("capability_levels", {}).get("L1", []))
    missing_l1 = sorted(REBUILD_L1 - l1)
    if missing_l1:
        base.fail(f"rebuild-plan L1 declarations missing: {missing_l1}")

    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        base.main()

    lines = [line for line in captured.getvalue().splitlines() if line.strip()]
    if not lines:
        base.fail("base static checker produced no PASS summary")
    summary = json.loads(lines[-1])
    if summary.get("status") != "PASS":
        base.fail("base static checker did not return PASS")
    labels = summary.get("validated_layers", [])
    if len(labels) != 17:
        base.fail("seventeen-layer static contract did not validate exactly 17 layers")
    if REBUILD_STAGE["label"] not in labels:
        base.fail("seventeen-layer static contract omitted Design Intent Rebuild Plan")

    summary["note"] = (
        "Static PASS validates seventeen receipt-bound runtime layers. Rebuild "
        "Plan is dirty-set/dependency planning plus explicit execution through "
        "validated Batch Apply; it is not a solver, automatic value derivation, "
        "automatic rebuild engine, or CAD feature-rebuild authority."
    )
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
