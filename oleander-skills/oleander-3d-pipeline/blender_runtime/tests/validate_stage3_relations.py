"""Headless validation for OLEANDER Blender Runtime Stage 3 Relation Kernel.

This validates check-only geometric relations, tolerance evaluation, dependency
ownership, cycle prevention, failure-driven stale propagation, tombstones and
.blend persistence in real Blender 5.1+. It does not claim a geometric solver,
CAD/B-Rep constraints, engineering approval, manufacturing release, field truth,
constructability or design authority.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys

import bpy

SCRIPT = pathlib.Path(__file__).resolve()
RUNTIME_ROOT = SCRIPT.parents[1]
PIPELINE_ROOT = SCRIPT.parents[2]
ADDON_ROOT = RUNTIME_ROOT / "oleander_blender"
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))

import oleander_blender
from oleander_blender.dependency import clear_stale, dependency_ids
from oleander_blender.relation_kernel import (
    audit_relations,
    evaluate_relation,
    get_relation_events,
    get_relation_tombstones,
    get_relations,
)


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


def find_result(summary, relation_id):
    return next(result for result in summary["results"] if result.get("relation_id") == relation_id)


def expect_runtime_failure(callable_, expected_text):
    try:
        callable_()
    except RuntimeError as exc:
        assert_true(expected_text in str(exc), f"expected RuntimeError containing {expected_text!r}; got {exc!r}")
        return
    raise AssertionError(f"expected RuntimeError containing {expected_text!r}")


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

    driver = add_cube("OLE_REL_DRIVER", "OLE_REL_DRIVER", (0.0, 0.0, 0.0))
    driven = add_cube("OLE_REL_DRIVEN", "OLE_REL_DRIVEN", (1200.0, 0.0, 0.0))
    downstream = add_cube("OLE_REL_DOWNSTREAM", "OLE_REL_DOWNSTREAM", (2400.0, 0.0, 0.0))
    downstream.oleander.dependencies = "OLE_REL_DRIVEN"

    select_pair(driver, driven)
    created = bpy.ops.oleander.add_relation(
        kind="ORIGIN_DISTANCE",
        capture_current=True,
        tolerance_mm=0.5,
    )
    assert_true("FINISHED" in created, "captured origin-distance relation must be created")
    relations = get_relations(scene)
    assert_true(len(relations) == 1, "one governed relation must be recorded")
    distance_relation = relations[0]
    distance_id = distance_relation["relation_id"]
    assert_true(distance_relation["solver_claim"] is False, "relation kernel must explicitly deny solver claim")
    assert_true(distance_relation["dependency_added_by_relation"] is True, "new driver dependency must record relation ownership")
    assert_true("OLE_REL_DRIVER" in dependency_ids(driven), "driver must be promoted into driven dependency graph")
    assert_true(abs(distance_relation["target_mm"] - 1200.0) <= 1e-6, "capture_current must store real metric origin distance")
    assert_true(evaluate_relation(scene, distance_relation)["status"] == "PASS", "captured relation must initially pass")

    clear_stale(driven)
    clear_stale(downstream)
    driven.location.x = 1250.0
    bpy.context.view_layer.update()
    failed_summary = audit_relations(scene, propagate_stale=True)
    failed_distance = find_result(failed_summary, distance_id)
    assert_true(failed_distance["status"] == "FAIL" and failed_distance["reason"] == "OUT_OF_TOLERANCE", "relation drift must fail tolerance audit")
    assert_true(driven.oleander.stale, "failed relation must stale the driven object")
    assert_true(downstream.oleander.stale, "failed relation must propagate stale state downstream")

    driven.location.x = 1200.0
    bpy.context.view_layer.update()
    clear_stale(driven)
    clear_stale(downstream)
    restored_summary = audit_relations(scene, propagate_stale=True)
    assert_true(find_result(restored_summary, distance_id)["status"] == "PASS", "restored geometry must restore relation PASS")
    assert_true(not driven.oleander.stale and not downstream.oleander.stale, "PASS audit must not create new stale state")

    select_pair(driver, driven)
    axis_offset = bpy.ops.oleander.add_relation(
        kind="AXIS_OFFSET",
        axis="X",
        capture_current=True,
        tolerance_mm=0.25,
    )
    assert_true("FINISHED" in axis_offset, "axis-offset relation must be created")
    axis_relation = get_relations(scene)[-1]
    axis_result = evaluate_relation(scene, axis_relation)
    assert_true(axis_result["status"] == "PASS" and abs(axis_result["actual"] - 1200.0) <= 1e-6, "axis offset must use signed world-axis metric value")

    select_pair(driver, driven)
    parallel = bpy.ops.oleander.add_relation(
        kind="AXIS_PARALLEL",
        axis="X",
        tolerance_deg=0.5,
        capture_current=False,
    )
    assert_true("FINISHED" in parallel, "axis-parallel relation must be created")
    parallel_relation = get_relations(scene)[-1]
    assert_true(evaluate_relation(scene, parallel_relation)["status"] == "PASS", "aligned local axes must initially pass parallel relation")
    driven.rotation_euler.z = 0.1
    bpy.context.view_layer.update()
    assert_true(evaluate_relation(scene, parallel_relation)["status"] == "FAIL", "rotated local axis must fail strict parallel tolerance")
    driven.rotation_euler.z = 0.0
    bpy.context.view_layer.update()

    # Positive failure: duplicate active relation for the same pair/kind/axis.
    select_pair(driver, driven)
    expect_runtime_failure(
        lambda: bpy.ops.oleander.add_relation(kind="AXIS_OFFSET", axis="X", capture_current=True, tolerance_mm=0.25),
        "duplicate active relation",
    )

    # Positive failure: relation dependency must not close an existing dependency cycle.
    cycle_driver = add_cube("OLE_REL_CYCLE_DRIVER", "OLE_REL_CYCLE_DRIVER", (0.0, 3000.0, 0.0))
    cycle_driven = add_cube("OLE_REL_CYCLE_DRIVEN", "OLE_REL_CYCLE_DRIVEN", (1000.0, 3000.0, 0.0))
    cycle_driver.oleander.dependencies = "OLE_REL_CYCLE_DRIVEN"
    select_pair(cycle_driver, cycle_driven)
    relation_count_before_cycle_attempt = len(get_relations(scene))
    expect_runtime_failure(
        lambda: bpy.ops.oleander.add_relation(kind="ORIGIN_DISTANCE", capture_current=True),
        "would create a cycle",
    )
    assert_true(len(get_relations(scene)) == relation_count_before_cycle_attempt, "cycle failure must not pollute relation registry")
    assert_true("OLE_REL_CYCLE_DRIVER" not in dependency_ids(cycle_driven), "cycle failure must not mutate driven dependencies")

    # Missing-object positive failure is detected during audit rather than guessed away.
    missing_driver = add_cube("OLE_REL_MISSING_DRIVER", "OLE_REL_MISSING_DRIVER", (0.0, 6000.0, 0.0))
    missing_driven = add_cube("OLE_REL_MISSING_DRIVEN", "OLE_REL_MISSING_DRIVEN", (500.0, 6000.0, 0.0))
    select_pair(missing_driver, missing_driven)
    missing_create = bpy.ops.oleander.add_relation(kind="ORIGIN_DISTANCE", capture_current=True)
    assert_true("FINISHED" in missing_create, "missing-object test relation must first be created")
    missing_relation_id = get_relations(scene)[-1]["relation_id"]
    bpy.data.objects.remove(missing_driver, do_unlink=True)
    missing_summary = audit_relations(scene, propagate_stale=True)
    missing_result = find_result(missing_summary, missing_relation_id)
    assert_true(missing_result["status"] == "FAIL" and missing_result["reason"] == "MISSING_OBJECT", "deleted driver must produce explicit missing-object relation failure")

    # Relation-owned dependency cleanup.
    owned_driver = add_cube("OLE_REL_OWNED_DRIVER", "OLE_REL_OWNED_DRIVER", (0.0, 9000.0, 0.0))
    owned_driven = add_cube("OLE_REL_OWNED_DRIVEN", "OLE_REL_OWNED_DRIVEN", (700.0, 9000.0, 0.0))
    select_pair(owned_driver, owned_driven)
    owned_create = bpy.ops.oleander.add_relation(kind="ORIGIN_DISTANCE", capture_current=True)
    assert_true("FINISHED" in owned_create, "owned-dependency relation must be created")
    owned_relation = get_relations(scene)[-1]
    owned_id = owned_relation["relation_id"]
    assert_true(owned_relation["dependency_added_by_relation"], "owned dependency provenance must be true")
    removed_owned = bpy.ops.oleander.remove_relation(relation_id=owned_id)
    assert_true("FINISHED" in removed_owned, "owned relation removal must finish")
    assert_true("OLE_REL_OWNED_DRIVER" not in dependency_ids(owned_driven), "relation-owned dependency must be cleaned when no remaining relation needs it")
    owned_tombstone = next(item for item in get_relation_tombstones(scene) if item["relation_id"] == owned_id)
    assert_true(owned_tombstone["dependency_removed_with_relation"], "owned relation tombstone must record dependency cleanup")

    # Pre-existing dependency must survive relation removal.
    preserve_driver = add_cube("OLE_REL_PRESERVE_DRIVER", "OLE_REL_PRESERVE_DRIVER", (0.0, 12000.0, 0.0))
    preserve_driven = add_cube("OLE_REL_PRESERVE_DRIVEN", "OLE_REL_PRESERVE_DRIVEN", (800.0, 12000.0, 0.0))
    preserve_driven.oleander.dependencies = "OLE_REL_PRESERVE_DRIVER"
    select_pair(preserve_driver, preserve_driven)
    preserve_create = bpy.ops.oleander.add_relation(kind="ORIGIN_DISTANCE", capture_current=True)
    assert_true("FINISHED" in preserve_create, "pre-existing dependency relation must be created")
    preserve_relation = get_relations(scene)[-1]
    preserve_id = preserve_relation["relation_id"]
    assert_true(not preserve_relation["dependency_added_by_relation"], "relation must record that dependency pre-existed")
    removed_preserve = bpy.ops.oleander.remove_relation(relation_id=preserve_id)
    assert_true("FINISHED" in removed_preserve, "pre-existing dependency relation removal must finish")
    assert_true("OLE_REL_PRESERVE_DRIVER" in dependency_ids(preserve_driven), "pre-existing dependency must survive relation removal")

    events = get_relation_events(scene)
    assert_true(events and [item["event_index"] for item in events] == list(range(1, len(events) + 1)), "relation event log must remain monotonic")

    reopen_path = "/tmp/oleander-stage3-relations-reopen.blend"
    bpy.ops.wm.save_as_mainfile(filepath=reopen_path)
    bpy.ops.wm.open_mainfile(filepath=reopen_path)

    reopened_scene = bpy.context.scene
    reopened_relations = get_relations(reopened_scene)
    reopened_tombstones = get_relation_tombstones(reopened_scene)
    reopened_events = get_relation_events(reopened_scene)
    assert_true(any(item["relation_id"] == distance_id for item in reopened_relations), "active relation registry must survive .blend save/reopen")
    assert_true(any(item["relation_id"] == owned_id for item in reopened_tombstones), "relation tombstones must survive .blend save/reopen")
    assert_true(len(reopened_events) == len(events), "relation event log must survive .blend save/reopen")
    assert_true(find_result(audit_relations(reopened_scene, propagate_stale=False), distance_id)["status"] == "PASS", "reopened valid relation must still evaluate PASS")

    result = {
        "runtime": "OLEANDER Blender Runtime",
        "stage": "STAGE3_RELATION_KERNEL",
        "version": "0.2.0",
        "blender": bpy.app.version_string,
        "status": "PASS",
        "source_fingerprint_sha256": source_fingerprint(),
        "checks": [
            "stable_relation_id_registry",
            "driver_driven_ole_provenance",
            "origin_distance_capture_current_metric",
            "origin_distance_tolerance_evaluation",
            "axis_offset_signed_metric_evaluation",
            "axis_parallel_angular_evaluation",
            "relation_solver_claim_false",
            "relation_dependency_graph_binding",
            "relation_failure_driven_stale",
            "relation_failure_downstream_stale_propagation",
            "relation_restore_pass",
            "duplicate_relation_expected_failure",
            "relation_dependency_cycle_expected_failure",
            "relation_cycle_failure_no_registry_pollution",
            "relation_cycle_failure_no_dependency_mutation",
            "missing_relation_object_expected_failure",
            "relation_dependency_added_by_relation_provenance",
            "relation_owned_dependency_cleanup",
            "relation_preexisting_dependency_preservation",
            "relation_remove_tombstone",
            "relation_event_log_monotonic",
            "relation_registry_save_reopen_persistence",
            "relation_tombstone_save_reopen_persistence",
            "relation_event_log_save_reopen_persistence",
        ],
        "expected_failure_cases": {
            "duplicate_active_relation": "PASS",
            "relation_dependency_cycle": "PASS",
            "missing_relation_object": "PASS",
        },
        "non_claims": [
            "constraint_solver",
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
    print("OLEANDER_STAGE3_RELATION_VALIDATION=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
