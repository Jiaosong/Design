"""OLEANDER professional dependency probe: CAD Sketcher + SolveSpace.

This probe validates a bounded external sketch-solver capability inside the
supported Blender runtime. PASS means the pinned CAD Sketcher dependency is
callable and demonstrates constraint solve/failure/reopen behavior. It does NOT
make P0-A Parametric CAD PASS and does not prove B-Rep, assembly, STEP, or CAD
feature-rebuild authority.
"""

from __future__ import annotations

import importlib
import json
import math
import os
from pathlib import Path

import bpy


ROOT_PACKAGE = os.environ.get(
    "OLEANDER_CAD_SKETCHER_PACKAGE",
    "bl_ext.oleander_professional.CAD_Sketcher",
)
REOPEN_PATH = Path("/tmp/oleander-cad-sketcher-probe.blend")


checks: list[str] = []


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def load_api():
    addon = importlib.import_module(ROOT_PACKAGE)
    if not hasattr(bpy.context.scene, "sketcher"):
        addon.register()
    curve_data = importlib.import_module(f"{ROOT_PACKAGE}.utilities.curve_data")
    sketch_ref = importlib.import_module(f"{ROOT_PACKAGE}.model.sketch_ref")
    curve_ref = importlib.import_module(f"{ROOT_PACKAGE}.model.curve_ref")
    return addon, curve_data, sketch_ref, curve_ref


def new_sketch(curve_data, sketch_ref, name: str):
    entities = bpy.context.scene.sketcher.entities
    entities.ensure_origin_elements(bpy.context)
    wp = entities.origin_plane_XY
    entity_sketch = entities.add_sketch(wp)
    curve_data.ensure_sketch_curve_object(entity_sketch)
    sketch_ref.stamp_sketch_props(entity_sketch.target_object)
    sketch = sketch_ref.Sketch(entity_sketch.target_object)
    sketch.name = name
    sketch_ref.set_active_sketch(bpy.context, sketch.target_object)
    return sketch


def main() -> None:
    addon, curve_data, sketch_ref, curve_ref = load_api()
    check(hasattr(bpy.context.scene, "sketcher"), "cad_sketcher_registered")

    # Positive solver path: horizontal + driving distance. CAD Sketcher's
    # init=True contract initializes a dimension from the current geometry; the
    # driving value is then edited explicitly and the sketch is re-solved.
    sketch = new_sketch(curve_data, sketch_ref, "OLEANDER_SOLVER_POSITIVE")
    p0 = curve_ref.PointRef.create(sketch, (0.0, 0.0), fixed=True)
    p1 = curve_ref.PointRef.create(sketch, (3.0, 1.0))
    line = curve_ref.LineRef.create(sketch, p0, p1)
    horizontal = sketch.constraints.add_horizontal(curve_id_1=line.curve_id)
    distance = sketch.constraints.add_distance(
        init=True,
        curve_id_1=line.curve_id,
    )
    check(sketch.solve(bpy.context), "horizontal_distance_solver_pass")
    check(abs(p1.co.y) < 1e-7, "horizontal_constraint_geometry")
    check(abs(float(distance.value) - line.length) < 1e-6, "driving_distance_initialized_from_geometry")
    check(not horizontal.failed and not distance.failed, "positive_constraints_not_failed")

    # First driving edit.
    distance.value = 4.0
    check(sketch.solve(bpy.context), "driving_dimension_edit_4_resolve")
    check(abs(line.length - 4.0) < 1e-6, "driving_dimension_edit_4_geometry")

    # Second edit proves the value remains a live driving constraint rather than
    # a one-shot initialization/bake.
    distance.value = 5.0
    check(sketch.solve(bpy.context), "driving_dimension_edit_5_resolve")
    check(abs(line.length - 5.0) < 1e-6, "driving_dimension_edit_5_geometry")
    check(math.isfinite(line.length), "resolved_geometry_finite")

    positive_object_name = sketch.target_object.name
    positive_distance_value = float(distance.value)

    # Positive failure gate: contradictory driving dimensions must not silently
    # mutate into an arbitrary result. CAD Sketcher should report INCONSISTENT
    # and flag at least one failed constraint.
    bad = new_sketch(curve_data, sketch_ref, "OLEANDER_SOLVER_INCONSISTENT")
    q0 = curve_ref.PointRef.create(bad, (0.0, 0.0), fixed=True)
    q1 = curve_ref.PointRef.create(bad, (3.0, 0.0))
    c1 = bad.constraints.add_distance(
        init=True,
        curve_id_1=q0.curve_id,
        curve_id_2=q1.curve_id,
    )
    c1.value = 3.0
    c2 = bad.constraints.add_distance(
        init=True,
        curve_id_1=q0.curve_id,
        curve_id_2=q1.curve_id,
    )
    c2.value = 5.0
    solve_ok = bad.solve(bpy.context)
    check(not solve_ok, "contradictory_constraints_expected_failure")
    check(bad.solver_state == "INCONSISTENT", "inconsistent_solver_state")
    all_constraints = list(bad.target_object.data.sketch_constraints.all)
    check(any(item.failed for item in all_constraints), "failed_constraint_feedback")

    # Save/reopen: dependency state must remain editable and the driving
    # dimension must survive as sketch data, not merely as baked mesh output.
    sketch_ref.set_active_sketch(bpy.context, None)
    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN_PATH))
    check(REOPEN_PATH.exists(), "blend_saved")
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN_PATH))

    addon, curve_data, sketch_ref, curve_ref = load_api()
    obj = bpy.data.objects.get(positive_object_name)
    check(obj is not None, "sketch_object_reopen")
    reopened = sketch_ref.Sketch(obj)
    check(reopened is not None, "sketch_accessor_reopen")
    reopened_constraints = list(obj.data.sketch_constraints.all)
    check(len(reopened_constraints) >= 2, "constraint_data_reopen")
    driving_values = [
        float(item.value)
        for item in reopened_constraints
        if hasattr(item, "value") and not getattr(item, "is_reference", False)
    ]
    check(
        any(abs(value - positive_distance_value) < 1e-6 for value in driving_values),
        "driving_dimension_value_reopen",
    )
    check(reopened.solve(bpy.context), "reopened_sketch_resolve")

    result = {
        "schema": "OLEANDER_PROFESSIONAL_DEPENDENCY_PROBE_v0.1",
        "dependency": "CAD Sketcher + SolveSpace",
        "package": ROOT_PACKAGE,
        "blender": bpy.app.version_string,
        "status": "PASS",
        "dependency_state": "RUNTIME_PROBED",
        "checks": checks,
        "non_claims": [
            "P0_A_PARAMETRIC_CAD_PASS",
            "brep_authority",
            "cad_feature_rebuild",
            "assembly_mates",
            "step_round_trip",
            "engineering_approval",
            "manufacturing_release",
        ],
    }
    print("OLEANDER_CAD_SKETCHER_PROBE=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
