"""Thirteen-layer static contract for OLEANDER Blender Runtime v0.2.

This wrapper preserves the complete twelve-layer checker, inserts the validated
Surface Diagnostic Foundation before Procedural, adds the new authority-boundary
requirements, and rewrites only the captured summary note. It never substitutes
for real Blender runtime execution.
"""

from __future__ import annotations

import contextlib
import io
import json

import static_check as base


SURFACE_STAGE = {
    "label": "Stage 3 Surface Diagnostics",
    "status_key": "VALIDATED_STAGE3_SURFACE_DIAGNOSTICS",
    "receipt_key": "stage3_surface_diagnostics_validation_receipt",
    "script": "validate_stage3_surface_diagnostics.py",
    "scope": "STAGE3_SURFACE_DIAGNOSTIC_FOUNDATION",
    "checks": {
        "depsgraph_evaluated_surface_data",
        "evaluated_mesh_modifier_inclusion",
        "closed_two_manifold_detection",
        "boundary_edge_detection",
        "nonmanifold_edge_count",
        "closed_mesh_orientation_resolution",
        "triangulated_dihedral_diagnostic",
        "cube_hard_edge_count",
        "dihedral_class_a_boundary",
        "pull_axis_orientation_diagnostic",
        "minimum_wall_draft_flagging",
        "pull_axis_moldability_boundary",
        "normal_ray_thickness_sampling",
        "normal_ray_metric_thickness",
        "thickness_engineering_boundary",
        "surface_diagnostic_snapshot",
        "open_mesh_thickness_not_fabricated",
        "surface_diagnostic_operator_registration",
        "surface_diagnostic_ole_provenance",
        "surface_diagnostic_save_reopen_persistence",
        "invalid_triangle_budget_expected_failure",
        "invalid_dihedral_threshold_expected_failure",
        "invalid_pull_axis_expected_failure",
        "zero_pull_axis_expected_failure",
        "invalid_minimum_draft_expected_failure",
        "invalid_thickness_samples_expected_failure",
        "invalid_thickness_epsilon_expected_failure",
        "nonmesh_expected_failure",
    },
    "failures": {
        "invalid_dihedral_threshold",
        "invalid_minimum_draft",
        "invalid_pull_axis",
        "invalid_thickness_epsilon",
        "invalid_thickness_samples",
        "invalid_triangle_budget",
        "nonmesh",
        "open_mesh_thickness",
        "zero_pull_axis",
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
    },
    "capabilities": {
        "depsgraph_evaluated_surface_data",
        "closed_two_manifold_detection",
        "triangulated_dihedral_diagnostic",
        "pull_axis_orientation_diagnostic",
        "normal_ray_thickness_sampling",
        "surface_diagnostic_snapshot",
        "surface_diagnostic_save_reopen_persistence",
    },
    "environment_key": "stage3_surface_diagnostics_validated_environment",
}


SURFACE_NOT_IMPLEMENTED = {
    "class_a_surface_certification",
    "analytic_curvature_certification",
    "nurbs_fairness_certification",
    "undercut_certification",
    "moldability_certification",
    "engineering_wall_thickness_certification",
}

SURFACE_DOES_NOT_PROVE = {
    "class_a_continuity",
    "analytic_curvature",
    "nurbs_fairness",
    "undercut_certification",
    "moldability",
    "engineering_wall_thickness",
}


def main():
    if not any(stage.get("label") == SURFACE_STAGE["label"] for stage in base.STAGES):
        base.STAGES.insert(-1, SURFACE_STAGE)

    capability = json.loads(
        (base.PIPELINE_ROOT / "BLENDER_RUNTIME_CAPABILITY.json").read_text(encoding="utf-8")
    )
    status = capability.get("implementation_status", {})
    missing_not_implemented = sorted(
        SURFACE_NOT_IMPLEMENTED - set(status.get("DECLARED_NOT_IMPLEMENTED", []))
    )
    if missing_not_implemented:
        base.fail(
            f"surface diagnostics lost NOT IMPLEMENTED boundaries: {missing_not_implemented}"
        )

    missing_boundaries = sorted(
        SURFACE_DOES_NOT_PROVE - set(capability.get("does_not_prove", []))
    )
    if missing_boundaries:
        base.fail(f"surface diagnostics lost does_not_prove boundaries: {missing_boundaries}")

    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        base.main()

    lines = [line for line in captured.getvalue().splitlines() if line.strip()]
    if not lines:
        base.fail("base static checker produced no PASS summary")
    summary = json.loads(lines[-1])
    if summary.get("status") != "PASS":
        base.fail("base static checker did not return PASS")
    if len(summary.get("validated_layers", [])) != 13:
        base.fail("thirteen-layer static contract did not validate exactly 13 layers")
    summary["note"] = (
        "Static PASS validates thirteen-layer receipt/contract integrity; "
        "it is not a substitute for Blender runtime execution."
    )
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
