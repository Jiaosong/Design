"""Sixteen-layer static contract for OLEANDER Blender Runtime v0.2.

Adds Design Intent Batch Apply as an independently receipt-bound stage after the
single-parameter Apply foundation and before Procedural. The batch layer accepts
stored parameter values only, expands declared parameter dependencies, performs
whole-batch dry-run/preflight, rejects competing target ownership, applies one
atomic transaction, postchecks the final combined state and rolls all targets
back on failure.

It is explicitly not an equation solver, constraint solver, automatic value
Deriver, automatic multi-parameter rebuild engine or CAD parametric feature
rebuild authority. Static PASS never substitutes for real Blender execution.
"""

from __future__ import annotations

import contextlib
import io
import json

import static_check as base
import static_check_15 as previous


DESIGN_INTENT_BATCH_STAGE = {
    "label": "Stage 3 Design Intent Batch Apply",
    "status_key": "VALIDATED_STAGE3_DESIGN_INTENT_BATCH",
    "receipt_key": "stage3_design_intent_batch_validation_receipt",
    "script": "validate_stage3_design_intent_batch.py",
    "scope": "STAGE3_DESIGN_INTENT_BATCH_APPLY_FOUNDATION",
    "checks": {
        "batch_operator_registration",
        "dependency_expansion",
        "dependency_topological_order",
        "dry_run_zero_mutation",
        "atomic_cross_object_feature_relation_datum_apply",
        "final_combined_state_postcheck",
        "model_downstream_stale_propagation",
        "separated_model_reference_metadata_mutation_classes",
        "include_dependencies_false_scope",
        "target_field_collision_positive_failure",
        "duplicate_parameter_id_positive_failure",
        "missing_parameter_positive_failure",
        "whole_batch_postcheck_rollback",
        "rollback_object_geometry_restore",
        "rollback_modifier_restore",
        "rollback_feature_history_restore",
        "failure_envelope_positive_failure",
        "monotonic_batch_identity",
        "batch_commit_event_provenance",
        "batch_rollback_event_provenance",
        "blend_save_reopen_persistence",
        "no_solver_claim",
        "no_parameter_value_derivation_claim",
        "no_automatic_geometry_rebuild_claim",
        "no_cad_parametric_rebuild_claim",
    },
    "failures": {
        "target_field_collision_positive_failure",
        "duplicate_parameter_id_positive_failure",
        "missing_parameter_positive_failure",
        "whole_batch_postcheck_rollback",
        "failure_envelope_positive_failure",
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
    },
    "capabilities": {
        "batch_operator_registration",
        "dependency_expansion",
        "dependency_topological_order",
        "dry_run_zero_mutation",
        "atomic_cross_object_feature_relation_datum_apply",
        "final_combined_state_postcheck",
        "model_downstream_stale_propagation",
        "separated_model_reference_metadata_mutation_classes",
        "include_dependencies_false_scope",
        "whole_batch_postcheck_rollback",
        "rollback_object_geometry_restore",
        "rollback_modifier_restore",
        "rollback_feature_history_restore",
        "monotonic_batch_identity",
        "batch_commit_event_provenance",
        "batch_rollback_event_provenance",
        "blend_save_reopen_persistence",
        "no_solver_claim",
        "no_parameter_value_derivation_claim",
        "no_automatic_geometry_rebuild_claim",
        "no_cad_parametric_rebuild_claim",
    },
    "environment_key": "stage3_design_intent_batch_validated_environment",
}

BATCH_NOT_IMPLEMENTED = {
    "constraint_solver",
    "equation_solver",
    "multi_parameter_solver",
    "automatic_parameter_value_derivation",
    "automatic_multi_parameter_rebuild",
    "automatic_parameter_geometry_rebuild",
    "cad_parametric_feature_rebuild",
}

BATCH_DOES_NOT_PROVE = {
    "constraint_solver",
    "equation_solver",
    "multi_parameter_solver",
    "automatic_parameter_value_derivation",
    "automatic_multi_parameter_rebuild",
    "automatic_parameter_geometry_rebuild",
    "cad_parametric_feature_rebuild",
    "design_intent_batch_is_solver",
}

BATCH_L1 = {
    "design_intent_batch_preflight",
    "design_intent_dependency_ordered_batch_apply",
    "design_intent_batch_target_collision_gate",
    "design_intent_batch_transaction_rollback",
    "design_intent_batch_event_provenance",
    "design_intent_batch_save_reopen_persistence",
}

BATCH_PROBES = {
    "design_intent_batch_preflight_stage3",
    "design_intent_batch_dependency_order_stage3",
    "design_intent_batch_target_collision_stage3",
    "design_intent_batch_atomic_transaction_stage3",
    "design_intent_batch_whole_rollback_stage3",
    "design_intent_batch_persistence_stage3",
    "design_intent_batch_no_solver_stage3",
    "design_intent_batch_no_value_derivation_stage3",
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
    # Reproduce the previous 15-layer stage registration without executing its
    # base.main() yet, then add the new independently receipt-bound Batch stage.
    previous.insert_before_procedural(previous.SURFACE_STAGE)
    previous.insert_before_procedural(previous.DESIGN_INTENT_STAGE)
    previous.insert_before_procedural(previous.DESIGN_INTENT_APPLY_STAGE)
    insert_before_procedural(DESIGN_INTENT_BATCH_STAGE)

    procedural = next(
        item for item in base.STAGES if item.get("label") == "Stage 3 Procedural"
    )
    procedural.setdefault("regressions", set()).update(
        {
            "stage3_surface_diagnostics_regression_in_same_job",
            "stage3_design_intent_regression_in_same_job",
            "stage3_design_intent_apply_regression_in_same_job",
            "stage3_design_intent_batch_regression_in_same_job",
        }
    )

    capability = json.loads(
        (base.PIPELINE_ROOT / "BLENDER_RUNTIME_CAPABILITY.json").read_text(encoding="utf-8")
    )

    previous.require_boundaries(
        capability,
        previous.SURFACE_NOT_IMPLEMENTED,
        previous.SURFACE_DOES_NOT_PROVE,
        "surface diagnostics",
    )
    previous.require_boundaries(
        capability,
        previous.DESIGN_INTENT_NOT_IMPLEMENTED,
        previous.DESIGN_INTENT_DOES_NOT_PROVE,
        "design intent",
    )
    previous.require_boundaries(
        capability,
        previous.APPLY_NOT_IMPLEMENTED,
        previous.APPLY_DOES_NOT_PROVE,
        "design intent apply",
    )
    previous.require_boundaries(
        capability,
        BATCH_NOT_IMPLEMENTED,
        BATCH_DOES_NOT_PROVE,
        "design intent batch apply",
    )

    l1 = set(capability.get("capability_levels", {}).get("L1", []))
    missing_batch_l1 = sorted(BATCH_L1 - l1)
    if missing_batch_l1:
        base.fail(f"design intent batch L1 capability declaration missing: {missing_batch_l1}")

    probes = set(capability.get("required_runtime_probes", []))
    missing_batch_probes = sorted(BATCH_PROBES - probes)
    if missing_batch_probes:
        base.fail(f"design intent batch runtime probes missing: {missing_batch_probes}")

    if "design_intent_batch_receipt" not in set(capability.get("representation_outputs", [])):
        base.fail("design intent batch receipt representation output missing")

    governance_required = {
        "design_intent_batch_preflight",
        "design_intent_batch_dependency_order",
        "design_intent_batch_target_ownership_gate",
        "design_intent_batch_atomic_transaction",
        "design_intent_batch_postcheck",
        "design_intent_batch_transaction_rollback",
        "design_intent_batch_event_provenance",
    }
    governance = set(capability.get("governance_functions", []))
    missing_governance = sorted(governance_required - governance)
    if missing_governance:
        base.fail(f"design intent batch governance declarations missing: {missing_governance}")

    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        base.main()

    lines = [line for line in captured.getvalue().splitlines() if line.strip()]
    if not lines:
        base.fail("base static checker produced no PASS summary")
    summary = json.loads(lines[-1])
    if summary.get("status") != "PASS":
        base.fail("base static checker did not return PASS")
    if len(summary.get("validated_layers", [])) != 16:
        base.fail("sixteen-layer static contract did not validate exactly 16 layers")
    labels = summary.get("validated_layers", [])
    if DESIGN_INTENT_BATCH_STAGE["label"] not in labels:
        base.fail("sixteen-layer static contract omitted Design Intent Batch Apply")
    summary["note"] = (
        "Static PASS validates sixteen-layer receipt/contract integrity; "
        "Batch Apply remains stored-value explicit transaction orchestration, "
        "not a solver or automatic CAD parametric rebuild. Static PASS is not "
        "a substitute for Blender runtime execution."
    )
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
