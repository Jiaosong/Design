"""Real-Blender validation for precision display, component measure and inference candidates."""

from __future__ import annotations

import hashlib
import json
import math
import pathlib
import sys

import bpy
from mathutils import Vector

SCRIPT = pathlib.Path(__file__).resolve()
RUNTIME_ROOT = SCRIPT.parents[1]
PIPELINE_ROOT = SCRIPT.parents[2]
ADDON_ROOT = RUNTIME_ROOT / "oleander_blender"
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))

import oleander_blender
from oleander_blender.precision_inference import (
    PRECISION_SNAPSHOT_KEY,
    bbox_clearance,
    component_measurement,
    display_precision,
    format_degrees,
    format_mm,
    mesh_inference_candidates,
    nearest_inference_candidate,
    precision_snapshot,
    set_display_precision,
)

MM_TOL = 1e-3


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def assert_close(actual, expected, tolerance, message):
    if abs(actual - expected) > tolerance:
        raise AssertionError(f"{message}: actual={actual!r} expected={expected!r}")


def expect_value_error(fn, text):
    try:
        fn()
    except ValueError as exc:
        assert_true(text in str(exc), f"expected {text!r}; got {exc!r}")
        return
    raise AssertionError(f"expected ValueError containing {text!r}")


def source_fingerprint():
    paths = [path for path in ADDON_ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".py", ".json", ".toml"}]
    paths.append(SCRIPT)
    digest = hashlib.sha256()
    for path in sorted(set(paths), key=lambda item: item.as_posix()):
        digest.update(path.relative_to(PIPELINE_ROOT).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def add_cube(name, oid, location, size=100.0):
    bpy.ops.mesh.primitive_cube_add(size=size, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.oleander.ole_id = oid
    obj.oleander.geometry_authority = "VERIFIED_SOURCE"
    obj.oleander.field_state = "NOT_APPLICABLE"
    obj.oleander.engineering_state = "NOT_APPLICABLE"
    obj.oleander.manufacturing_state = "NOT_APPLICABLE"
    obj.oleander.design_review_state = "NA"
    return obj


def main():
    if hasattr(bpy.types.Object, "oleander"):
        try:
            oleander_blender.unregister()
        except Exception:
            pass
    oleander_blender.register()
    clear_scene()
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001

    # Formatting precision is presentation state only.
    state = set_display_precision(scene, 3, 1)
    assert_true(state == {"linear_decimals": 3, "angle_decimals": 1}, "precision state must persist exact decimal settings")
    assert_true(format_mm(scene, 12.34567) == "12.346 mm", "linear formatting must obey display precision")
    assert_true(format_degrees(scene, 12.34567) == "12.3°", "angle formatting must obey display precision")
    expect_value_error(lambda: set_display_precision(scene, 7, 1), "between 0 and 6")

    # Signed component measurement is world-origin geometry, independent of display rounding.
    a = add_cube("OLE_PREC_A", "OLE_PREC_A", (100.0, 200.0, 300.0))
    b = add_cube("OLE_PREC_B", "OLE_PREC_B", (400.0, 600.0, 300.0))
    measure = component_measurement(scene, a, b)
    for actual, expected in zip(measure["signed_delta_mm"], (300.0, 400.0, 0.0)):
        assert_close(actual, expected, MM_TOL, "component deltas must preserve world metric values")
    assert_close(measure["origin_distance_mm"], 500.0, MM_TOL, "component measurement distance must be metric")
    assert_true(measure["authority"] == "WORLD_ORIGIN_MEASUREMENT", "component measurement authority must be explicit")

    # AABB clearance is deterministic and explicitly approximate.
    c = add_cube("OLE_CLEAR_A", "OLE_CLEAR_A", (0.0, 0.0, 0.0), size=100.0)
    d = add_cube("OLE_CLEAR_B", "OLE_CLEAR_B", (250.0, 0.0, 0.0), size=100.0)
    clearance = bbox_clearance(scene, c, d)
    assert_close(clearance["axis_gap_mm"][0], 150.0, MM_TOL, "AABB X gap must be exact for axis-aligned cubes")
    assert_close(clearance["bbox_separation_lower_bound_mm"], 150.0, MM_TOL, "AABB lower-bound separation must be deterministic")
    assert_true(clearance["authority"] == "AABB_APPROXIMATION_ONLY_NOT_SURFACE_CLEARANCE", "clearance must deny true-surface authority")

    # Blender cube topology produces 8 endpoints, 12 midpoints, 6 face centers + origin.
    candidates = mesh_inference_candidates(scene, c)
    counts = {kind: sum(1 for item in candidates["candidates"] if item["kind"] == kind) for kind in ("ORIGIN", "ENDPOINT", "MIDPOINT", "FACE_CENTER")}
    assert_true(counts == {"ORIGIN":1,"ENDPOINT":8,"MIDPOINT":12,"FACE_CENTER":6}, f"unexpected inference counts: {counts}")
    assert_true(candidates["authority"] == "SNAP_CANDIDATE_ONLY_NO_CONSTRAINT_SOLVER", "inference candidate authority must be explicit")

    # Nearest candidate resolves by world metric radius and kind filter.
    target = Vector((50.5, 50.0, 50.0))
    nearest = nearest_inference_candidate(scene, c, target, 1.0, allowed_kinds=("ENDPOINT",))
    assert_true(nearest is not None and nearest["kind"] == "ENDPOINT", "nearest endpoint must resolve inside metric snap radius")
    assert_close(nearest["distance_to_target_mm"], 0.5, MM_TOL, "nearest inference distance must use metric scene contract")
    miss = nearest_inference_candidate(scene, c, target, 0.1, allowed_kinds=("ENDPOINT",))
    assert_true(miss is None, "inference query must return None outside snap radius")
    expect_value_error(lambda: nearest_inference_candidate(scene, c, target, 0.0), "snap radius")
    expect_value_error(lambda: mesh_inference_candidates(scene, c, max_candidates=5), "exceeds 5")

    # Non-mesh inference must fail instead of silently inventing candidates.
    bpy.ops.object.empty_add(type="PLAIN_AXES")
    empty = bpy.context.active_object
    expect_value_error(lambda: mesh_inference_candidates(scene, empty), "mesh object")

    # Snapshot combines display precision, two-object components/AABB and active inference summary.
    snapshot = precision_snapshot(scene, [c, d], c)
    assert_true(snapshot["selected_count"] == 2 and "component_measurement" in snapshot and "bbox_clearance" in snapshot, "precision snapshot must combine two-object measurements")
    assert_true(snapshot["active_inference_summary"]["counts"]["MIDPOINT"] == 12, "precision snapshot must expose inference counts")
    assert_true(PRECISION_SNAPSHOT_KEY in scene, "precision snapshot must persist to scene")

    # Operator smoke tests.
    op = bpy.ops.oleander.set_display_precision(linear_decimals=2, angle_decimals=3)
    assert_true("FINISHED" in op and display_precision(scene) == {"linear_decimals":2,"angle_decimals":3}, "display precision operator must execute")
    bpy.ops.object.select_all(action="DESELECT")
    c.select_set(True)
    d.select_set(True)
    bpy.context.view_layer.objects.active = c
    snap_op = bpy.ops.oleander.precision_snapshot()
    assert_true("FINISHED" in snap_op, "precision snapshot operator must execute")

    # Persistence through .blend reopen.
    reopen_path = "/tmp/oleander-stage3-precision-inference-reopen.blend"
    bpy.ops.wm.save_as_mainfile(filepath=reopen_path)
    bpy.ops.wm.open_mainfile(filepath=reopen_path)
    reopened = bpy.context.scene
    assert_true(display_precision(reopened) == {"linear_decimals":2,"angle_decimals":3}, "display precision must survive reopen")
    assert_true(PRECISION_SNAPSHOT_KEY in reopened, "precision snapshot must survive reopen")
    stored = json.loads(reopened[PRECISION_SNAPSHOT_KEY])
    assert_true(stored["bbox_clearance"]["authority"] == "AABB_APPROXIMATION_ONLY_NOT_SURFACE_CLEARANCE", "AABB authority boundary must persist")

    result = {
        "runtime":"OLEANDER Blender Runtime",
        "stage":"STAGE3_PRECISION_INFERENCE_FOUNDATION",
        "version":"0.2.0",
        "blender":bpy.app.version_string,
        "status":"PASS",
        "source_fingerprint_sha256":source_fingerprint(),
        "checks":[
            "display_precision_state","linear_display_formatting","angular_display_formatting","display_precision_range_failure",
            "signed_component_world_measurement","component_origin_distance_metric","aabb_axis_gap_metric","aabb_clearance_authority_boundary",
            "mesh_endpoint_candidates","mesh_midpoint_candidates","mesh_face_center_candidates","mesh_origin_candidate","inference_no_solver_claim",
            "nearest_inference_metric_radius","nearest_inference_kind_filter","inference_radius_miss","invalid_snap_radius_expected_failure",
            "candidate_limit_expected_failure","nonmesh_inference_expected_failure","precision_snapshot_combined_measurement","precision_snapshot_inference_summary",
            "display_precision_operator_registration","precision_snapshot_operator_registration","display_precision_save_reopen_persistence","precision_snapshot_save_reopen_persistence"
        ],
        "expected_failure_cases":{
            "invalid_display_precision":"PASS","invalid_snap_radius":"PASS","candidate_limit":"PASS","nonmesh_inference":"PASS"
        },
        "non_claims":[
            "true_surface_clearance","perpendicular_constraint_solver","parallel_constraint_solver","intersection_constraint_solver",
            "persistent_snap_constraint","cad_sketch_solver","field_truth","engineering_approval","manufacturing_release","constructability","design_quality"
        ]
    }
    print("OLEANDER_STAGE3_PRECISION_INFERENCE_VALIDATION=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
