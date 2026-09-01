"""Real-Blender validation for OLEANDER Inference Engine v2."""

from __future__ import annotations

import hashlib
import json
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
from oleander_blender.inference_engine import (
    INFERENCE_V2_SNAPSHOT_KEY,
    TRACKING_POINTS_KEY,
    add_tracking_point,
    analyze_infinite_lines,
    axis_lock_projection,
    clear_tracking_points,
    compare_mesh_edges,
    extension_line_candidate,
    inference_v2_snapshot,
    nearest_tracking_point,
    remove_tracking_point,
    tracking_points,
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


def add_edge_object(name, oid, start, end, location=(0.0, 0.0, 0.0)):
    mesh = bpy.data.meshes.new(name + "_MESH")
    mesh.from_pydata([start, end], [(0, 1)], [])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location
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

    # Infinite-line relation inference.
    parallel = analyze_infinite_lines(scene, (0,0,0), (1,0,0), (0,50,0), (-1,0,0), 0.1, 0.1)
    assert_true(parallel["parallel"] and not parallel["collinear"], "offset lines must resolve PARALLEL without COLLINEAR")
    assert_close(parallel["line_offset_mm"], 50.0, MM_TOL, "parallel line offset must be metric")
    assert_true("PARALLEL" in parallel["relations"], "parallel relation label missing")

    collinear = analyze_infinite_lines(scene, (0,0,0), (1,0,0), (100,0,0), (-5,0,0), 0.1, 0.1)
    assert_true(collinear["collinear"] and "COLLINEAR" in collinear["relations"], "same infinite line must resolve COLLINEAR")

    perpendicular = analyze_infinite_lines(scene, (0,0,0), (1,0,0), (10,-20,0), (0,1,0), 0.1, 0.1)
    assert_true(perpendicular["perpendicular"], "orthogonal lines must resolve PERPENDICULAR")
    assert_true(perpendicular["intersecting"], "coplanar orthogonal lines must resolve INTERSECTING")
    assert_close(perpendicular["intersection_world_mm"][0], 10.0, MM_TOL, "intersection X must be metric")
    assert_close(perpendicular["intersection_world_mm"][1], 0.0, MM_TOL, "intersection Y must be metric")
    assert_true(perpendicular["authority"] == "GEOMETRIC_INFERENCE_CHECK_ONLY_NO_CONSTRAINT_SOLVER", "inference authority boundary must be explicit")

    skew_perpendicular = analyze_infinite_lines(scene, (0,0,0), (1,0,0), (10,-20,50), (0,1,0), 0.1, 0.1)
    assert_true(skew_perpendicular["perpendicular"] and not skew_perpendicular["intersecting"], "3D perpendicular directions may remain spatially skew")
    assert_close(skew_perpendicular["closest_distance_mm"], 50.0, MM_TOL, "skew line distance must remain metric")

    expect_value_error(lambda: analyze_infinite_lines(scene, (0,0,0), (0,0,0), (0,0,0), (1,0,0)), "non-zero")
    expect_value_error(lambda: analyze_infinite_lines(scene, (0,0,0), (1,0,0), (0,0,0), (0,1,0), angular_tolerance_deg=50), "between 0 and 45")
    expect_value_error(lambda: analyze_infinite_lines(scene, (0,0,0), (1,0,0), (0,0,0), (0,1,0), linear_tolerance_mm=-1), "non-negative")

    # Mesh-edge wrapper preserves object/edge provenance.
    edge_a = add_edge_object("OLE_INF_EDGE_A", "OLE_INF_EDGE_A", (0,0,0), (100,0,0))
    edge_b = add_edge_object("OLE_INF_EDGE_B", "OLE_INF_EDGE_B", (0,-50,0), (0,50,0), location=(25,0,0))
    comparison = compare_mesh_edges(scene, edge_a, 0, edge_b, 0)
    assert_true(comparison["perpendicular"] and comparison["intersecting"], "mesh edge wrapper must resolve perpendicular intersection")
    assert_true(comparison["a"] == "OLE_INF_EDGE_A" and comparison["b"] == "OLE_INF_EDGE_B", "mesh edge provenance must preserve OLE IDs")
    expect_value_error(lambda: compare_mesh_edges(scene, edge_a, 5, edge_b, 0), "edge index")

    # Extension line is transient and only outside finite segment.
    extension = extension_line_candidate(scene, edge_a, 0, Vector((150,5,0)), 10.0)
    assert_true(extension is not None and extension["kind"] == "EXTENSION", "outside projection must create extension candidate")
    assert_close(extension["edge_parameter"], 1.5, 1e-6, "extension parameter must preserve infinite-line projection")
    assert_close(extension["distance_to_target_mm"], 5.0, MM_TOL, "extension snap distance must be metric")
    assert_true(extension["authority"] == "TEMPORARY_INFERENCE_CANDIDATE_NO_CONSTRAINT", "extension must remain transient")
    assert_true(extension_line_candidate(scene, edge_a, 0, Vector((50,5,0)), 10.0) is None, "finite-edge projection must not be mislabeled as extension")
    assert_true(extension_line_candidate(scene, edge_a, 0, Vector((150,20,0)), 10.0) is None, "extension outside snap radius must miss")
    expect_value_error(lambda: extension_line_candidate(scene, edge_a, 0, (150,0,0), 0.0), "snap radius")

    # World-axis lock projection must not mutate either input.
    axis = axis_lock_projection(scene, (10,20,30), (70,80,90), "Y")
    assert_true(axis["projected_world_scene"] == [10.0,80.0,30.0], f"unexpected Y-axis projection: {axis}")
    assert_true(axis["authority"] == "TRANSIENT_AXIS_INFERENCE_NO_TRANSFORM_MUTATION", "axis lock must deny transform mutation authority")
    expect_value_error(lambda: axis_lock_projection(scene, (0,0,0), (1,2,3), "Q"), "X, Y or Z")

    # Temporary tracking points: stable monotonic IDs, metric nearest query, explicit lifecycle.
    first = add_tracking_point(scene, (10,20,30), "A")
    second = add_tracking_point(scene, (100,200,300), "B")
    assert_true(first["tracking_id"] == "OLE_TRACK::T0001" and second["tracking_id"] == "OLE_TRACK::T0002", "tracking IDs must be stable/monotonic")
    nearest = nearest_tracking_point(scene, (11,20,30), 2.0)
    assert_true(nearest is not None and nearest["tracking_id"] == first["tracking_id"], "nearest tracking point must resolve by metric radius")
    assert_close(nearest["distance_to_target_mm"], 1.0, MM_TOL, "tracking distance must be metric")
    assert_true(nearest_tracking_point(scene, (20,20,30), 2.0) is None, "tracking query must miss outside radius")
    expect_value_error(lambda: nearest_tracking_point(scene, (0,0,0), 0), "snap radius")
    remove_tracking_point(scene, first["tracking_id"])
    assert_true([item["tracking_id"] for item in tracking_points(scene)] == [second["tracking_id"]], "tracking removal must target ID exactly")
    expect_value_error(lambda: remove_tracking_point(scene, "OLE_TRACK::T9999"), "not found")

    # Operators use cursor state and preserve explicit inference-only snapshot.
    scene.cursor.location = (7,8,9)
    op = bpy.ops.oleander.add_cursor_tracking_point()
    assert_true("FINISHED" in op, "cursor tracking operator must execute")
    snapshot_op = bpy.ops.oleander.inference_v2_snapshot()
    assert_true("FINISHED" in snapshot_op and INFERENCE_V2_SNAPSHOT_KEY in scene, "inference v2 snapshot operator must persist state")
    snapshot = json.loads(scene[INFERENCE_V2_SNAPSHOT_KEY])
    assert_true(snapshot["authority"] == "INFERENCE_STATE_ONLY_NO_CONSTRAINT_SOLVER", "snapshot must deny solver authority")
    assert_true(snapshot["tracking_point_count"] == 2, "snapshot must include surviving + cursor tracking points")

    reopen_path = "/tmp/oleander-stage3-inference-v2-reopen.blend"
    bpy.ops.wm.save_as_mainfile(filepath=reopen_path)
    bpy.ops.wm.open_mainfile(filepath=reopen_path)
    reopened = bpy.context.scene
    assert_true(TRACKING_POINTS_KEY in reopened and INFERENCE_V2_SNAPSHOT_KEY in reopened, "tracking/snapshot state must survive .blend reopen")
    assert_true(len(tracking_points(reopened)) == 2, "tracking point registry must survive reopen")
    cleared = clear_tracking_points(reopened)
    assert_true(cleared == 2 and tracking_points(reopened) == [], "clear tracking points must be deterministic")

    result = {
        "runtime":"OLEANDER Blender Runtime",
        "stage":"STAGE3_INFERENCE_ENGINE_V2",
        "version":"0.2.0",
        "blender":bpy.app.version_string,
        "status":"PASS",
        "source_fingerprint_sha256":source_fingerprint(),
        "checks":[
            "parallel_inference","collinear_inference","perpendicular_inference","intersection_inference","skew_perpendicular_distance",
            "line_relation_metric_tolerances","line_relation_no_solver_authority","zero_direction_expected_failure","invalid_angular_tolerance_expected_failure","invalid_linear_tolerance_expected_failure",
            "mesh_edge_relation_wrapper","mesh_edge_ole_provenance","invalid_edge_index_expected_failure",
            "extension_line_projection","extension_only_outside_segment","extension_snap_radius","extension_no_constraint_authority","invalid_extension_radius_expected_failure",
            "world_axis_lock_projection","axis_lock_no_transform_mutation","invalid_axis_lock_expected_failure",
            "tracking_point_monotonic_ids","tracking_point_metric_nearest","tracking_point_radius_miss","tracking_point_remove_by_id","missing_tracking_point_expected_failure","invalid_tracking_radius_expected_failure",
            "cursor_tracking_operator_registration","inference_v2_snapshot_operator_registration","inference_v2_no_solver_snapshot","tracking_point_save_reopen_persistence","inference_v2_snapshot_save_reopen_persistence"
        ],
        "expected_failure_cases":{
            "zero_direction":"PASS","invalid_angular_tolerance":"PASS","invalid_linear_tolerance":"PASS","invalid_edge_index":"PASS",
            "invalid_extension_radius":"PASS","invalid_axis_lock":"PASS","missing_tracking_point":"PASS","invalid_tracking_radius":"PASS"
        },
        "non_claims":[
            "persistent_snap_constraint","constraint_solver","cad_sketch_solver","automatic_transform_mutation","field_truth","engineering_approval","manufacturing_release","constructability","design_quality"
        ]
    }
    print("OLEANDER_STAGE3_INFERENCE_V2_VALIDATION=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
