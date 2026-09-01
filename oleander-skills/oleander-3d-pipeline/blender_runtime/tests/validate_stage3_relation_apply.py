"""Real-Blender validation for deterministic OLEANDER Relation Apply.

This stage validates explicit one-shot transform correction for uniquely
resolvable translation relations. It intentionally rejects multi-solution
rotation, uncaptured distance direction, and externally constrained transforms.
It is not an iterative constraint solver or CAD/B-Rep regeneration system.
"""

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
from oleander_blender.dependency import clear_stale
from oleander_blender.relation_apply import REFERENCE_KEY, get_relation_events
from oleander_blender.relation_kernel import evaluate_relation, get_relations


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def source_fingerprint():
    paths = [
        path
        for path in ADDON_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".py", ".json", ".toml"}
    ]
    paths.append(SCRIPT)
    digest = hashlib.sha256()
    for path in sorted(set(paths), key=lambda item: item.as_posix()):
        rel = path.relative_to(PIPELINE_ROOT).as_posix().encode("utf-8")
        digest.update(rel)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def add_cube(name, ole_id, location):
    bpy.ops.mesh.primitive_cube_add(size=100.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.oleander.ole_id = ole_id
    return obj


def select_pair(driver, driven):
    bpy.ops.object.select_all(action="DESELECT")
    driver.select_set(True)
    driven.select_set(True)
    bpy.context.view_layer.objects.active = driven


def scene_units_for_mm(scene, value_mm):
    return (value_mm / 1000.0) / (scene.unit_settings.scale_length or 1.0)


def expect_runtime_failure(callable_, expected_text):
    try:
        callable_()
    except RuntimeError as exc:
        assert_true(expected_text in str(exc), f"expected {expected_text!r}; got {exc!r}")
        return
    raise AssertionError(f"expected RuntimeError containing {expected_text!r}")


def relation_by_id(scene, relation_id):
    return next(item for item in get_relations(scene) if item.get("relation_id") == relation_id)


def world_origin(obj):
    bpy.context.view_layer.update()
    return obj.matrix_world.translation.copy()


def euler_delta_length(a, b):
    return Vector((a.x - b.x, a.y - b.y, a.z - b.z)).length


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

    # AXIS_OFFSET: correct only the governed world axis and preserve orthogonal coordinates.
    axis_driver = add_cube("OLE_APPLY_AXIS_DRIVER", "OLE_APPLY_AXIS_DRIVER", (0.0, 0.0, 0.0))
    axis_driven = add_cube("OLE_APPLY_AXIS_DRIVEN", "OLE_APPLY_AXIS_DRIVEN", (1000.0, 300.0, 200.0))
    axis_downstream = add_cube("OLE_APPLY_AXIS_DOWNSTREAM", "OLE_APPLY_AXIS_DOWNSTREAM", (2000.0, 0.0, 0.0))
    axis_downstream.oleander.dependencies = "OLE_APPLY_AXIS_DRIVEN"
    select_pair(axis_driver, axis_driven)
    created = bpy.ops.oleander.add_relation(kind="AXIS_OFFSET", axis="X", capture_current=True, tolerance_mm=0.1)
    assert_true("FINISHED" in created, "axis-offset relation creation must finish")
    axis_relation = get_relations(scene)[-1]
    axis_id = axis_relation["relation_id"]
    original = world_origin(axis_driven)
    axis_driven.location.x += scene_units_for_mm(scene, 75.0)
    axis_driven.location.y += scene_units_for_mm(scene, 20.0)
    bpy.context.view_layer.update()
    drifted = world_origin(axis_driven)
    assert_true(evaluate_relation(scene, axis_relation)["status"] == "FAIL", "axis-offset drift must fail before apply")
    clear_stale(axis_downstream)
    applied = bpy.ops.oleander.apply_relation_once(relation_id=axis_id)
    assert_true("FINISHED" in applied, "axis-offset deterministic apply must finish")
    restored = world_origin(axis_driven)
    assert_true(abs(restored.x - original.x) <= 1e-9, "axis-offset apply must restore governed X coordinate")
    assert_true(abs(restored.y - drifted.y) <= 1e-9 and abs(restored.z - drifted.z) <= 1e-9, "axis-offset apply must not rewrite orthogonal coordinates")
    assert_true(evaluate_relation(scene, relation_by_id(scene, axis_id))["status"] == "PASS", "axis-offset apply must restore relation PASS")
    assert_true(axis_downstream.oleander.stale, "relation apply must stale downstream dependents")

    # ORIGIN_COINCIDENT: unique translation solution only.
    coincident_driver = add_cube("OLE_APPLY_COIN_DRIVER", "OLE_APPLY_COIN_DRIVER", (0.0, 3000.0, 0.0))
    coincident_driven = add_cube("OLE_APPLY_COIN_DRIVEN", "OLE_APPLY_COIN_DRIVEN", (0.0, 3000.0, 0.0))
    select_pair(coincident_driver, coincident_driven)
    coincident_create = bpy.ops.oleander.add_relation(kind="ORIGIN_COINCIDENT", tolerance_mm=0.1, capture_current=False)
    assert_true("FINISHED" in coincident_create, "coincident relation creation must finish")
    coincident_id = get_relations(scene)[-1]["relation_id"]
    coincident_driven.location.x += scene_units_for_mm(scene, 40.0)
    coincident_driven.location.z -= scene_units_for_mm(scene, 25.0)
    bpy.context.view_layer.update()
    coincident_apply = bpy.ops.oleander.apply_relation_once(relation_id=coincident_id)
    assert_true("FINISHED" in coincident_apply, "coincident one-shot apply must finish")
    assert_true((world_origin(coincident_driven) - world_origin(coincident_driver)).length <= 1e-9, "coincident apply must align world origins exactly")
    assert_true(evaluate_relation(scene, relation_by_id(scene, coincident_id))["status"] == "PASS", "coincident apply must restore PASS")

    # ORIGIN_DISTANCE: direction must be captured from PASS geometry before drift.
    distance_driver = add_cube("OLE_APPLY_DISTANCE_DRIVER", "OLE_APPLY_DISTANCE_DRIVER", (0.0, 6000.0, 0.0))
    distance_driven = add_cube("OLE_APPLY_DISTANCE_DRIVEN", "OLE_APPLY_DISTANCE_DRIVEN", (300.0, 6400.0, 0.0))
    select_pair(distance_driver, distance_driven)
    distance_create = bpy.ops.oleander.add_relation(kind="ORIGIN_DISTANCE", capture_current=True, tolerance_mm=0.1)
    assert_true("FINISHED" in distance_create, "distance relation creation must finish")
    distance_id = get_relations(scene)[-1]["relation_id"]
    initial_direction = (world_origin(distance_driven) - world_origin(distance_driver)).normalized()
    capture = bpy.ops.oleander.capture_relation_apply_reference(relation_id=distance_id)
    assert_true("FINISHED" in capture, "PASS distance relation must allow apply-reference capture")
    captured_relation = relation_by_id(scene, distance_id)
    captured = Vector(captured_relation[REFERENCE_KEY])
    assert_true((captured - initial_direction).length <= 1e-9, "captured direction must preserve PASS driver→driven direction")
    assert_true(captured_relation.get("apply_solver_claim") is False, "captured apply metadata must explicitly deny solver claim")

    distance_driven.location.x += scene_units_for_mm(scene, 150.0)
    distance_driven.location.y -= scene_units_for_mm(scene, 220.0)
    bpy.context.view_layer.update()
    assert_true(evaluate_relation(scene, captured_relation)["status"] == "FAIL", "distance drift must fail before apply")
    distance_apply = bpy.ops.oleander.apply_relation_once(relation_id=distance_id)
    assert_true("FINISHED" in distance_apply, "captured distance relation must support deterministic one-shot apply")
    distance_after = relation_by_id(scene, distance_id)
    assert_true(evaluate_relation(scene, distance_after)["status"] == "PASS", "distance apply must restore PASS")
    final_direction = (world_origin(distance_driven) - world_origin(distance_driver)).normalized()
    assert_true((final_direction - initial_direction).length <= 1e-9, "distance apply must restore captured direction, not current drift direction")
    assert_true(distance_after.get("apply_revision") == 1 and distance_after.get("apply_solver_claim") is False, "distance apply revision and non-solver boundary must persist")

    # Positive failure: distance apply without a PASS reference direction is forbidden.
    uncaptured_driver = add_cube("OLE_APPLY_UNCAP_DRIVER", "OLE_APPLY_UNCAP_DRIVER", (0.0, 9000.0, 0.0))
    uncaptured_driven = add_cube("OLE_APPLY_UNCAP_DRIVEN", "OLE_APPLY_UNCAP_DRIVEN", (500.0, 9000.0, 0.0))
    select_pair(uncaptured_driver, uncaptured_driven)
    uncaptured_create = bpy.ops.oleander.add_relation(kind="ORIGIN_DISTANCE", capture_current=True)
    assert_true("FINISHED" in uncaptured_create, "uncaptured distance relation fixture must be created")
    uncaptured_id = get_relations(scene)[-1]["relation_id"]
    uncaptured_driven.location.x += scene_units_for_mm(scene, 100.0)
    bpy.context.view_layer.update()
    before_uncaptured = world_origin(uncaptured_driven)
    expect_runtime_failure(
        lambda: bpy.ops.oleander.apply_relation_once(relation_id=uncaptured_id),
        "requires a captured PASS reference direction",
    )
    assert_true((world_origin(uncaptured_driven) - before_uncaptured).length <= 1e-12, "failed uncaptured distance apply must not mutate geometry")

    # Positive failure: zero-distance direction cannot be captured.
    ambiguous_driver = add_cube("OLE_APPLY_AMBIG_DRIVER", "OLE_APPLY_AMBIG_DRIVER", (0.0, 12000.0, 0.0))
    ambiguous_driven = add_cube("OLE_APPLY_AMBIG_DRIVEN", "OLE_APPLY_AMBIG_DRIVEN", (0.0, 12000.0, 0.0))
    select_pair(ambiguous_driver, ambiguous_driven)
    ambiguous_create = bpy.ops.oleander.add_relation(kind="ORIGIN_DISTANCE", capture_current=True)
    assert_true("FINISHED" in ambiguous_create, "zero-distance relation fixture must be created")
    ambiguous_id = get_relations(scene)[-1]["relation_id"]
    expect_runtime_failure(
        lambda: bpy.ops.oleander.capture_relation_apply_reference(relation_id=ambiguous_id),
        "ambiguous ORIGIN_DISTANCE direction",
    )

    # Positive failure: AXIS_PARALLEL has twist ambiguity; no rotation is silently chosen.
    parallel_driver = add_cube("OLE_APPLY_PAR_DRIVER", "OLE_APPLY_PAR_DRIVER", (0.0, 15000.0, 0.0))
    parallel_driven = add_cube("OLE_APPLY_PAR_DRIVEN", "OLE_APPLY_PAR_DRIVEN", (500.0, 15000.0, 0.0))
    select_pair(parallel_driver, parallel_driven)
    parallel_create = bpy.ops.oleander.add_relation(kind="AXIS_PARALLEL", axis="X", tolerance_deg=0.1, capture_current=False)
    assert_true("FINISHED" in parallel_create, "parallel relation fixture must be created")
    parallel_id = get_relations(scene)[-1]["relation_id"]
    parallel_driven.rotation_euler.z = 0.2
    bpy.context.view_layer.update()
    before_rotation = parallel_driven.rotation_euler.copy()
    expect_runtime_failure(
        lambda: bpy.ops.oleander.apply_relation_once(relation_id=parallel_id),
        "multi-solution and intentionally unsupported",
    )
    assert_true(euler_delta_length(parallel_driven.rotation_euler, before_rotation) <= 1e-12, "failed parallel apply must not choose an arbitrary rotation")

    # Positive failure: external Blender transform constraints retain authority.
    constrained_driver = add_cube("OLE_APPLY_CON_DRIVER", "OLE_APPLY_CON_DRIVER", (0.0, 18000.0, 0.0))
    constrained_driven = add_cube("OLE_APPLY_CON_DRIVEN", "OLE_APPLY_CON_DRIVEN", (700.0, 18000.0, 0.0))
    select_pair(constrained_driver, constrained_driven)
    constrained_create = bpy.ops.oleander.add_relation(kind="AXIS_OFFSET", axis="X", capture_current=True)
    assert_true("FINISHED" in constrained_create, "constrained relation fixture must be created")
    constrained_id = get_relations(scene)[-1]["relation_id"]
    constrained_driven.location.x += scene_units_for_mm(scene, 80.0)
    constraint = constrained_driven.constraints.new(type="COPY_LOCATION")
    constraint.name = "EXTERNAL_AUTHORITY_TEST"
    bpy.context.view_layer.update()
    before_constrained = world_origin(constrained_driven)
    expect_runtime_failure(
        lambda: bpy.ops.oleander.apply_relation_once(relation_id=constrained_id),
        "external transform authority",
    )
    assert_true((world_origin(constrained_driven) - before_constrained).length <= 1e-12, "blocked external-authority apply must not mutate world transform")

    expect_runtime_failure(
        lambda: bpy.ops.oleander.apply_relation_once(relation_id="OLE_REL::R9999"),
        "relation not found",
    )

    events = get_relation_events(scene)
    actions = [event.get("action") for event in events]
    assert_true("APPLY_REFERENCE_CAPTURE" in actions and "APPLY_ONE_SHOT" in actions, "relation event log must record capture and one-shot apply")
    assert_true([event["event_index"] for event in events] == list(range(1, len(events) + 1)), "relation/apply event log must remain monotonic")

    reopen_path = "/tmp/oleander-stage3-relation-apply-reopen.blend"
    bpy.ops.wm.save_as_mainfile(filepath=reopen_path)
    bpy.ops.wm.open_mainfile(filepath=reopen_path)
    reopened_scene = bpy.context.scene
    reopened_distance = relation_by_id(reopened_scene, distance_id)
    assert_true(isinstance(reopened_distance.get(REFERENCE_KEY), list) and len(reopened_distance[REFERENCE_KEY]) == 3, "captured distance direction must survive .blend reopen")
    assert_true(reopened_distance.get("apply_revision") == 1, "apply revision must survive .blend reopen")
    reopened_actions = [event.get("action") for event in get_relation_events(reopened_scene)]
    assert_true("APPLY_REFERENCE_CAPTURE" in reopened_actions and "APPLY_ONE_SHOT" in reopened_actions, "apply events must survive .blend reopen")

    result = {
        "runtime": "OLEANDER Blender Runtime",
        "stage": "STAGE3_RELATION_APPLY",
        "version": "0.2.0",
        "blender": bpy.app.version_string,
        "status": "PASS",
        "source_fingerprint_sha256": source_fingerprint(),
        "checks": [
            "axis_offset_one_shot_apply",
            "axis_offset_preserves_orthogonal_world_coordinates",
            "axis_offset_restores_relation_pass",
            "origin_coincident_one_shot_apply",
            "origin_distance_pass_reference_capture",
            "origin_distance_reference_direction_provenance",
            "origin_distance_one_shot_restore",
            "origin_distance_restores_captured_direction",
            "relation_apply_solver_claim_false",
            "relation_apply_revision",
            "relation_apply_downstream_stale_propagation",
            "relation_apply_event_log",
            "uncaptured_distance_apply_expected_failure",
            "uncaptured_distance_failure_no_geometry_mutation",
            "ambiguous_distance_direction_expected_failure",
            "axis_parallel_multisolution_expected_failure",
            "axis_parallel_failure_no_rotation_mutation",
            "external_transform_authority_expected_failure",
            "external_authority_failure_no_transform_mutation",
            "missing_relation_apply_expected_failure",
            "relation_apply_reference_save_reopen_persistence",
            "relation_apply_revision_save_reopen_persistence",
            "relation_apply_event_save_reopen_persistence",
        ],
        "expected_failure_cases": {
            "uncaptured_distance_direction": "PASS",
            "ambiguous_distance_direction": "PASS",
            "axis_parallel_multisolution": "PASS",
            "external_transform_authority": "PASS",
            "missing_relation_id": "PASS",
        },
        "non_claims": [
            "constraint_solver",
            "iterative_solver",
            "multi_relation_solver",
            "solver_backed_sketch_constraints",
            "cad_brep",
            "feature_solver",
            "class_a_surface",
            "field_truth",
            "engineering_approval",
            "manufacturing_release",
            "constructability",
            "design_quality",
        ],
    }
    print("OLEANDER_STAGE3_RELATION_APPLY_VALIDATION=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
