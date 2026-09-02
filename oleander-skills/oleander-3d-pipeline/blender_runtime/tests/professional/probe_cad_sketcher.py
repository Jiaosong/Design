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
from mathutils import Vector

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


def solve_and_refresh(sketch, curve_data, label: str) -> bool:
    """Match CAD Sketcher's handler/operator lifecycle in headless mode."""
    ok = sketch.solve(bpy.context)
    if ok:
        curve_data.refresh_curve_geometry(sketch)
        bpy.context.view_layer.update()
    check(ok, label)
    return ok


def set_driving_value(constraint, displayed_value: float) -> str:
    """Use CAD Sketcher's Blender-5 scene endpoint, the same value source used by UI."""
    scene = bpy.context.scene
    endpoint = scene.sketcher.get_constraint_value_endpoint(constraint)
    check(bool(endpoint), "constraint_value_endpoint_exists")
    scene[endpoint] = float(constraint.from_displayed_value(displayed_value))
    check(
        abs(float(constraint.value) - displayed_value) < 1e-9,
        "constraint_value_endpoint_readback",
    )
    return endpoint


def point_distance(p0, p1) -> float:
    return (Vector(p1.co) - Vector(p0.co)).length


def main() -> None:
    addon, curve_data, sketch_ref, curve_ref = load_api()
    check(hasattr(bpy.context.scene, "sketcher"), "cad_sketcher_registered")

    # 1) Geometric constraint path.
    horizontal_sketch = new_sketch(curve_data, sketch_ref, "OLEANDER_HORIZONTAL")
    h0 = curve_ref.PointRef.create(horizontal_sketch, (0.0, 0.0), fixed=True)
    h1 = curve_ref.PointRef.create(horizontal_sketch, (3.0, 1.0))
    hline = curve_ref.LineRef.create(horizontal_sketch, h0, h1)
    hc = horizontal_sketch.constraints.add_horizontal(curve_id_1=hline.curve_id)
    solve_and_refresh(horizontal_sketch, curve_data, "horizontal_solver_pass")
    check(abs(h1.co.y) < 1e-7, "horizontal_constraint_geometry")
    check(not hc.failed, "horizontal_constraint_not_failed")

    # 2) Driving dimension lifecycle. Use point-to-point distance because it is
    # the native-curve solver path at this pinned CAD Sketcher commit. The same
    # public dimensional endpoint used by the Blender UI drives repeated edits.
    sketch = new_sketch(curve_data, sketch_ref, "OLEANDER_DRIVING_DIMENSION")
    p0 = curve_ref.PointRef.create(sketch, (0.0, 0.0), fixed=True)
    p1 = curve_ref.PointRef.create(sketch, (3.0, 0.0))
    distance = sketch.constraints.add_distance(
        init=True,
        curve_id_1=p0.curve_id,
        curve_id_2=p1.curve_id,
    )
    solve_and_refresh(sketch, curve_data, "driving_dimension_initial_solve")
    check(abs(point_distance(p0, p1) - 3.0) < 1e-6, "driving_dimension_initial_geometry")
    check(abs(float(distance.value) - 3.0) < 1e-6, "driving_dimension_initialized_value")
    check(not distance.failed, "driving_dimension_not_failed")

    endpoint = set_driving_value(distance, 4.0)
    solve_and_refresh(sketch, curve_data, "driving_dimension_edit_4_resolve")
    check(abs(point_distance(p0, p1) - 4.0) < 1e-6, "driving_dimension_edit_4_geometry")

    set_driving_value(distance, 5.0)
    solve_and_refresh(sketch, curve_data, "driving_dimension_edit_5_resolve")
    check(abs(point_distance(p0, p1) - 5.0) < 1e-6, "driving_dimension_edit_5_geometry")
    check(math.isfinite(point_distance(p0, p1)), "resolved_geometry_finite")
    check(
        endpoint == bpy.context.scene.sketcher.get_constraint_value_endpoint(distance),
        "stable_constraint_value_endpoint",
    )

    positive_object_name = sketch.target_object.name
    positive_distance_value = float(distance.value)
    positive_constraint_uid = distance.constraint_uid
    positive_p0_id = p0.curve_id
    positive_p1_id = p1.curve_id

    # 3) Contradictory constraints must report a controlled inconsistent state.
    bad = new_sketch(curve_data, sketch_ref, "OLEANDER_SOLVER_INCONSISTENT")
    q0 = curve_ref.PointRef.create(bad, (0.0, 0.0), fixed=True)
    q1 = curve_ref.PointRef.create(bad, (3.0, 0.0))
    c1 = bad.constraints.add_distance(
        init=True,
        curve_id_1=q0.curve_id,
        curve_id_2=q1.curve_id,
    )
    c2 = bad.constraints.add_distance(
        init=True,
        curve_id_1=q0.curve_id,
        curve_id_2=q1.curve_id,
    )
    set_driving_value(c1, 3.0)
    set_driving_value(c2, 5.0)
    solve_ok = bad.solve(bpy.context)
    check(not solve_ok, "contradictory_constraints_expected_failure")
    check(bad.solver_state == "INCONSISTENT", "inconsistent_solver_state")
    all_constraints = list(bad.target_object.data.sketch_constraints.all)
    check(any(item.failed for item in all_constraints), "failed_constraint_feedback")

    # Save/reopen proves editable native constraint state survives.
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
    check(len(reopened_constraints) >= 1, "constraint_data_reopen")
    reopened_distance = next(
        (
            item
            for item in reopened_constraints
            if getattr(item, "constraint_uid", "") == positive_constraint_uid
        ),
        None,
    )
    check(reopened_distance is not None, "constraint_uid_reopen")
    reopened_endpoint = bpy.context.scene.sketcher.get_constraint_value_endpoint(
        reopened_distance
    )
    check(bool(reopened_endpoint), "constraint_value_endpoint_reopen")
    check(
        abs(float(reopened_distance.value) - positive_distance_value) < 1e-6,
        "driving_dimension_value_reopen",
    )
    solve_and_refresh(reopened, curve_data, "reopened_sketch_resolve")
    rp0 = curve_data.get_curve_position(reopened, positive_p0_id)
    rp1 = curve_data.get_curve_position(reopened, positive_p1_id)
    check(rp0 is not None and rp1 is not None, "driving_points_reopen")
    check(
        abs((Vector(rp1) - Vector(rp0)).length - positive_distance_value) < 1e-6,
        "driving_geometry_reopen",
    )

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
