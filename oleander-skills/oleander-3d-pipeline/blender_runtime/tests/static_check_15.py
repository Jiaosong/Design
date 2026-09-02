"""Fifteen-layer static contract for OLEANDER Blender Runtime v0.2.

Adds Design Intent Apply as an independently receipt-bound stage while retaining
Surface Diagnostics and Design Intent Graph governance. Explicit application is
allow-listed and transactional; it does not promote the runtime to a parameter,
constraint or CAD/B-Rep solver. Static PASS never substitutes for Blender runtime.
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
from static_check_14 import (
    DESIGN_INTENT_DOES_NOT_PROVE,
    DESIGN_INTENT_NOT_IMPLEMENTED,
    DESIGN_INTENT_STAGE,
)


DESIGN_INTENT_APPLY_STAGE = {
    "label": "Stage 3 Design Intent Apply",
    "status_key": "VALIDATED_STAGE3_DESIGN_INTENT_APPLY",
    "receipt_key": "stage3_design_intent_apply_validation_receipt",
    "script": "validate_stage3_design_intent_apply.py",
    "scope": "STAGE3_DESIGN_INTENT_APPLY_FOUNDATION",
    "checks": {
        "explicit_apply_separate_from_parameter_update",
        "whole_parameter_preflight",
        "object_dimension_apply",
        "object_dimension_postcheck",
        "object_apply_breaks_no_solver_boundary",
        "object_apply_downstream_stale_propagation",
        "feature_parameter_apply",
        "feature_modifier_history_synchronization",
        "feature_history_postcheck",
        "relation_target_metadata_apply",
        "relation_apply_no_geometry_motion",
        "datum_reference_geometry_apply",
        "datum_reference_authority_separation",
        "unsupported_field_expected_failure",
        "unsupported_field_no_mutation",
        "external_transform_authority_expected_failure",
        "external_authority_no_mutation",
        "transaction_postcheck_failure_rollback",
        "rollback_restores_object_geometry",
        "rollback_restores_feature_modifier_and_history",
        "rollback_event_provenance",
        "failure_envelope_expected_failure",
        "failure_envelope_no_mutation",
        "apply_commit_event_provenance",
        "design_intent_apply_operator_registration",
        "explicit_apply_save_reopen_persistence",
    },
    "failures": {
        "external_transform_authority",
        "failure_envelope_breach",
        "forced_postcheck_transaction_rollback",
        "unsupported_target_field",
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
    },
    "capabilities": {
        "explicit_apply_separate_from_parameter_update",
        "whole_parameter_preflight",
        "object_dimension_apply",
        "feature_parameter_apply",
        "relation_target_metadata_apply",
        "datum_reference_geometry_apply",
        "transaction_postcheck_failure_rollback",
        "rollback_event_provenance",
        "apply_commit_event_provenance",
        "explicit_apply_save_reopen_persistence",
    },
    "environment_key": "stage3_design_intent_apply_validated_environment",
}

APPLY_NOT_IMPLEMENTED = {
    "automatic_parameter_geometry_rebuild",
    "cad_parametric_feature_rebuild",
    "multi_parameter_solver",
    "automatic_multi_parameter_rebuild",
}

APPLY_DOES_NOT_PROVE = {
    "automatic_parameter_geometry_rebuild",
    "cad_parametric_feature_rebuild",
    "multi_parameter_solver",
    "automatic_multi_parameter_rebuild",
    "constraint_solver",
    "cad_sketch_solver",
}

APPLY_L1 = {
    "design_intent_explicit_apply",
    "design_intent_apply_preflight",
    "design_intent_apply_postcheck",
    "design_intent_apply_transaction_rollback",
    "object_dimension_parameter_apply",
    "feature_parameter_apply",
    "relation_target_parameter_apply",
    "datum_reference_parameter_apply",
    "design_intent_apply_event_provenance",
}


def insert_before_procedural(stage):
    if any(item.get("label") == stage["label"] for item in base.STAGES):
        return
    index = next(
        (i for i, item in enumerate(base.STAGES) if item.get("label") == "Stage 3 Procedural"),
        len(base.STAGES),
    )
    base.STAGES.insert(index, stage)


def require_boundaries(capability, not_implemented, does_not_prove, label):
    status = capability.get("implementation_status", {})
    missing_not_implemented = sorted(
        not_implemented - set(status.get("DECLARED_NOT_IMPLEMENTED", []))
    )
    if missing_not_implemented:
        base.fail(f"{label} lost NOT IMPLEMENTED boundaries: {missing_not_implemented}")
    missing_boundaries = sorted(does_not_prove - set(capability.get("does_not_prove", [])))
    if missing_boundaries:
        base.fail(f"{label} lost does_not_prove boundaries: {missing_boundaries}")


def main():
    insert_before_procedural(SURFACE_STAGE)
    insert_before_procedural(DESIGN_INTENT_STAGE)
    insert_before_procedural(DESIGN_INTENT_APPLY_STAGE)

    procedural = next(
        item for item in base.STAGES if item.get("label") == "Stage 3 Procedural"
    )
    procedural.setdefault("regressions", set()).update(
        {
            "stage3_surface_diagnostics_regression_in_same_job",
            "stage3_design_intent_regression_in_same_job",
            "stage3_design_intent_apply_regression_in_same_job",
        }
    )

    capability = json.loads(
        (base.PIPELINE_ROOT / "BLENDER_RUNTIME_CAPABILITY.json").read_text(encoding="utf-8")
    )

    require_boundaries(capability, SURFACE_NOT_IMPLEMENTED, SURFACE_DOES_NOT_PROVE, "surface diagnostics")
    require_boundaries(capability, DESIGN_INTENT_NOT_IMPLEMENTED, DESIGN_INTENT_DOES_NOT_PROVE, "design intent")
    require_boundaries(capability, APPLY_NOT_IMPLEMENTED, APPLY_DOES_NOT_PROVE, "design intent apply")

    l1 = set(capability.get("capability_levels", {}).get("L1", []))
    intent_l1 = {
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
    missing_intent_l1 = sorted(intent_l1 - l1)
    if missing_intent_l1:
        base.fail(f"design intent L1 capability declaration missing: {missing_intent_l1}")
    missing_apply_l1 = sorted(APPLY_L1 - l1)
    if missing_apply_l1:
        base.fail(f"design intent apply L1 capability declaration missing: {missing_apply_l1}")

    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        base.main()

    lines = [line for line in captured.getvalue().splitlines() if line.strip()]
    if not lines:
        base.fail("base static checker produced no PASS summary")
    summary = json.loads(lines[-1])
    if summary.get("status") != "PASS":
        base.fail("base static checker did not return PASS")
    if len(summary.get("validated_layers", [])) != 15:
        base.fail("fifteen-layer static contract did not validate exactly 15 layers")
    summary["note"] = (
        "Static PASS validates fifteen-layer receipt/contract integrity; "
        "it is not a substitute for Blender runtime execution."
    )
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
