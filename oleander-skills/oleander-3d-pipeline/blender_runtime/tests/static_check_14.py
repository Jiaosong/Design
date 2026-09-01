"""Fourteen-layer static contract for OLEANDER Blender Runtime v0.2.

Preserves the proven base checker, adds Surface Diagnostics and Design Intent
Graph as independently receipt-bound stages, strengthens Procedural same-job
regression requirements, and enforces the no-solver/no-auto-rebuild authority
boundary. Static PASS never substitutes for real Blender execution.
"""

from __future__ import annotations

import contextlib
import io
import json

import static_check as base
from static_check_13 import (
    SURFACE_DOES_NOT_PROVE,
    SURFACE_NOT_IMPLEMENTED,
    SURFACE_STAGE,
)


DESIGN_INTENT_STAGE = {
    "label": "Stage 3 Design Intent Graph",
    "status_key": "VALIDATED_STAGE3_DESIGN_INTENT",
    "receipt_key": "stage3_design_intent_validation_receipt",
    "script": "validate_stage3_design_intent.py",
    "scope": "STAGE3_DESIGN_INTENT_GRAPH_FOUNDATION",
    "checks": {
        "stable_monotonic_parameter_ids",
        "typed_parameter_values_and_units",
        "primary_derived_roles",
        "parameter_authority_metadata",
        "parameter_solver_claim_false",
        "parameter_automatic_geometry_apply_false",
        "duplicate_parameter_name_expected_failure",
        "invalid_count_expected_failure",
        "invalid_failure_envelope_expected_failure",
        "non_numeric_failure_envelope_expected_failure",
        "parameter_dependency_graph",
        "parameter_dependency_cycle_expected_failure",
        "cycle_failure_no_registry_mutation",
        "missing_parameter_dependency_expected_failure",
        "self_parameter_dependency_expected_failure",
        "object_binding_by_stable_ole_id",
        "feature_binding_by_stable_feature_id",
        "relation_binding_by_stable_relation_id",
        "datum_binding_reuses_stable_guide_id",
        "missing_binding_target_expected_failure",
        "missing_parameter_binding_expected_failure",
        "duplicate_binding_expected_failure",
        "design_intent_graph_audit",
        "design_intent_baseline_sha256",
        "parameter_revision_increment",
        "parameter_event_log",
        "bound_target_direct_stale",
        "object_dependency_downstream_stale",
        "parameter_update_no_automatic_geometry_mutation",
        "failure_envelope_pass_state",
        "failure_envelope_breach_detection",
        "failure_envelope_breach_audit_failure",
        "design_intent_diff",
        "deleted_binding_target_audit_failure",
        "design_intent_operator_registration",
        "design_intent_save_reopen_persistence",
        "design_intent_event_save_reopen_persistence",
        "design_intent_baseline_save_reopen_persistence",
    },
    "failures": {
        "cycle_failure_no_registry_mutation",
        "deleted_binding_target",
        "duplicate_binding",
        "duplicate_parameter_name",
        "failure_envelope_breach",
        "invalid_count",
        "invalid_failure_envelope",
        "missing_binding_target",
        "missing_parameter_binding",
        "missing_parameter_dependency",
        "non_numeric_failure_envelope",
        "parameter_dependency_cycle",
        "self_parameter_dependency",
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
    },
    "capabilities": {
        "stable_monotonic_parameter_ids",
        "typed_parameter_values_and_units",
        "parameter_dependency_graph",
        "object_binding_by_stable_ole_id",
        "feature_binding_by_stable_feature_id",
        "relation_binding_by_stable_relation_id",
        "datum_binding_reuses_stable_guide_id",
        "parameter_event_log",
        "parameter_update_no_automatic_geometry_mutation",
        "failure_envelope_breach_detection",
        "design_intent_diff",
        "design_intent_save_reopen_persistence",
    },
    "environment_key": "stage3_design_intent_validated_environment",
}


DESIGN_INTENT_NOT_IMPLEMENTED = {
    "automatic_parameter_geometry_rebuild",
    "cad_parametric_feature_rebuild",
}

DESIGN_INTENT_DOES_NOT_PROVE = {
    "automatic_parameter_geometry_rebuild",
    "cad_parametric_feature_rebuild",
    "design_intent_metadata_is_solver",
}


def _insert_before_procedural(stage):
    if any(item.get("label") == stage["label"] for item in base.STAGES):
        return
    index = next(
        (i for i, item in enumerate(base.STAGES) if item.get("label") == "Stage 3 Procedural"),
        len(base.STAGES),
    )
    base.STAGES.insert(index, stage)


def main():
    _insert_before_procedural(SURFACE_STAGE)
    _insert_before_procedural(DESIGN_INTENT_STAGE)

    procedural = next(
        item for item in base.STAGES if item.get("label") == "Stage 3 Procedural"
    )
    procedural.setdefault("regressions", set()).update(
        {
            "stage3_surface_diagnostics_regression_in_same_job",
            "stage3_design_intent_regression_in_same_job",
        }
    )

    capability = json.loads(
        (base.PIPELINE_ROOT / "BLENDER_RUNTIME_CAPABILITY.json").read_text(encoding="utf-8")
    )
    status = capability.get("implementation_status", {})

    missing_surface_not_implemented = sorted(
        SURFACE_NOT_IMPLEMENTED - set(status.get("DECLARED_NOT_IMPLEMENTED", []))
    )
    if missing_surface_not_implemented:
        base.fail(
            f"surface diagnostics lost NOT IMPLEMENTED boundaries: {missing_surface_not_implemented}"
        )
    missing_surface_boundaries = sorted(
        SURFACE_DOES_NOT_PROVE - set(capability.get("does_not_prove", []))
    )
    if missing_surface_boundaries:
        base.fail(
            f"surface diagnostics lost does_not_prove boundaries: {missing_surface_boundaries}"
        )

    missing_intent_not_implemented = sorted(
        DESIGN_INTENT_NOT_IMPLEMENTED - set(status.get("DECLARED_NOT_IMPLEMENTED", []))
    )
    if missing_intent_not_implemented:
        base.fail(
            f"design intent lost NOT IMPLEMENTED boundaries: {missing_intent_not_implemented}"
        )
    missing_intent_boundaries = sorted(
        DESIGN_INTENT_DOES_NOT_PROVE - set(capability.get("does_not_prove", []))
    )
    if missing_intent_boundaries:
        base.fail(
            f"design intent lost does_not_prove boundaries: {missing_intent_boundaries}"
        )

    l1 = set(capability.get("capability_levels", {}).get("L1", []))
    required_l1 = {
        "stable_design_parameter_registry",
        "typed_design_parameters",
        "design_parameter_dependency_graph",
        "design_intent_bindings",
        "design_parameter_event_log",
        "failure_envelope_metadata",
        "design_intent_baseline",
        "design_intent_diff",
        "design_intent_stale_propagation",
    }
    missing_l1 = sorted(required_l1 - l1)
    if missing_l1:
        base.fail(f"design intent L1 capability declaration missing: {missing_l1}")

    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        base.main()

    lines = [line for line in captured.getvalue().splitlines() if line.strip()]
    if not lines:
        base.fail("base static checker produced no PASS summary")
    summary = json.loads(lines[-1])
    if summary.get("status") != "PASS":
        base.fail("base static checker did not return PASS")
    if len(summary.get("validated_layers", [])) != 14:
        base.fail("fourteen-layer static contract did not validate exactly 14 layers")
    summary["note"] = (
        "Static PASS validates fourteen-layer receipt/contract integrity; "
        "it is not a substitute for Blender runtime execution."
    )
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
