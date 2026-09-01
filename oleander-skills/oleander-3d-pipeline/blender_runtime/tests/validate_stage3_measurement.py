"""Real-Blender validation for OLEANDER Scale / Ruler / Snap foundation.

Validates scene-unit-aware measurement profiles, exact world-space quantize/nudge,
selection snapshots, editable reference rulers with major/minor ticks and labels,
reference-guide audit scoping, expected failure gates, and .blend persistence.
Viewport grid styling remains visual guidance and is not dimensional authority.
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
from oleander_blender.audit import audit_scene
from oleander_blender.measurement_system import (
    GUIDE_COLLECTION,
    SNAPSHOT_KEY,
    create_ruler_guide,
    measurement_events,
    measurement_snapshot,
    mm_to_scene_units,
    profile_values,
    quantize_world_location,
    scene_units_to_mm,
    set_profile,
    nudge_world_location,
)


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def assert_close(actual, expected, tolerance, message):
    if abs(actual - expected) > tolerance:
        raise AssertionError(f"{message}: actual={actual!r} expected={expected!r}")


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
    guides = bpy.data.collections.get(GUIDE_COLLECTION)
    if guides is not None:
        for obj in list(guides.objects):
            bpy.data.objects.remove(obj, do_unlink=True)


def add_cube(name, ole_id, location, size=100.0):
    bpy.ops.mesh.primitive_cube_add(size=size, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.oleander.ole_id = ole_id
    obj.oleander.geometry_authority = "VERIFIED_SOURCE"
    obj.oleander.field_state = "NOT_APPLICABLE"
    obj.oleander.engineering_state = "NOT_APPLICABLE"
    obj.oleander.manufacturing_state = "NOT_APPLICABLE"
    obj.oleander.design_review_state = "NA"
    return obj


def expect_value_error(callable_, expected_text):
    try:
        callable_()
    except ValueError as exc:
        assert_true(expected_text in str(exc), f"expected {expected_text!r}; got {exc!r}")
        return
    raise AssertionError(f"expected ValueError containing {expected_text!r}")


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

    # Profile changes measurement behavior but does not reinterpret the scene scale contract.
    original_scale = scene.unit_settings.scale_length
    profile = set_profile(scene, "FURNITURE_INTERIOR")
    assert_true(profile["minor_step_mm"] == 10.0 and profile["major_every"] == 10, "interior profile must expose 10 mm minor / 100 mm major")
    assert_true(profile["snap_step_mm"] == 10.0 and profile["default_ruler_mm"] == 3000.0, "interior profile snap/ruler defaults must persist")
    assert_close(scene.unit_settings.scale_length, original_scale, 1e-12, "measurement profile must not reinterpret scene scale")
    assert_close(scene_units_to_mm(scene, mm_to_scene_units(scene, 123.456)), 123.456, 1e-6, "mm conversion must round-trip")

    # Measurement snapshot: active size/origin and two-object origin delta/distance.
    a = add_cube("OLE_MEASURE_A", "OLE_MEASURE_A", (100.0, 200.0, 300.0), size=100.0)
    b = add_cube("OLE_MEASURE_B", "OLE_MEASURE_B", (400.0, 600.0, 300.0), size=100.0)
    snapshot = measurement_snapshot(scene, [a, b], a)
    assert_true(snapshot["selected_count"] == 2 and snapshot["active"]["ole_id"] == "OLE_MEASURE_A", "measurement snapshot must retain active OLE provenance")
    assert_close(snapshot["pair"]["origin_distance_mm"], 500.0, 1e-5, "pair origin distance must honor scene unit contract")
    assert_true(all(abs(value - 100.0) <= 1e-5 for value in snapshot["active"]["dimensions_mm"]), "cube dimensions must report real millimetres")
    scene[SNAPSHOT_KEY] = json.dumps(snapshot, sort_keys=True)

    # Exact quantize: only requested axes move; downstream becomes stale.
    snap_obj = add_cube("OLE_SNAP", "OLE_SNAP", (123.4, 256.6, 89.9))
    downstream = add_cube("OLE_SNAP_DOWNSTREAM", "OLE_SNAP_DOWNSTREAM", (1000.0, 0.0, 0.0))
    downstream.oleander.dependencies = "OLE_SNAP"
    before_z = snap_obj.matrix_world.translation.z
    snapped = quantize_world_location(scene, [snap_obj], 10.0, axes=(True, True, False))
    assert_true(len(snapped) == 1, "quantize must return one operation record")
    origin = snap_obj.matrix_world.translation
    assert_close(scene_units_to_mm(scene, origin.x), 120.0, 1e-5, "X must quantize to 10 mm lattice")
    assert_close(scene_units_to_mm(scene, origin.y), 260.0, 1e-5, "Y must quantize to 10 mm lattice")
    assert_close(origin.z, before_z, 1e-9, "disabled Z snap must preserve world coordinate")
    assert_true(downstream.oleander.stale, "quantize must stale downstream dependents")

    # Exact nudge by governed mm amount.
    before_x_mm = scene_units_to_mm(scene, snap_obj.matrix_world.translation.x)
    nudge = nudge_world_location(scene, snap_obj, "X", -5.0)
    assert_close(scene_units_to_mm(scene, snap_obj.matrix_world.translation.x), before_x_mm - 5.0, 1e-5, "nudge must apply exact mm amount")
    assert_true(nudge["axis"] == "X" and nudge["amount_mm"] == -5.0, "nudge record must preserve axis and amount")

    # External constraints retain transform authority; exact snap must refuse mutation.
    constrained = add_cube("OLE_SNAP_CONSTRAINED", "OLE_SNAP_CONSTRAINED", (111.0, 222.0, 333.0))
    constraint = constrained.constraints.new(type="COPY_LOCATION")
    constraint.name = "EXTERNAL_SNAP_AUTHORITY"
    before_constrained = constrained.matrix_world.translation.copy()
    expect_value_error(
        lambda: quantize_world_location(scene, [constrained], 10.0),
        "external transform authority",
    )
    assert_true((constrained.matrix_world.translation - before_constrained).length <= 1e-12, "blocked quantize must not mutate constrained object")

    # Editable world ruler: 1000 mm, 10 mm minor ticks, 100 mm major ticks.
    ruler = create_ruler_guide(
        bpy.context,
        "X",
        1000.0,
        10.0,
        10,
        origin_mode="WORLD_ORIGIN",
        labels=True,
        label_every_major=2,
    )
    assert_true(ruler.get("oleander_reference_guide") is True, "ruler must be explicitly reference-only")
    assert_true(ruler.get("oleander_guide_authority") == "REFERENCE_ONLY_NOT_MODEL_GEOMETRY", "ruler authority must deny model-geometry status")
    assert_true(ruler.hide_render and ruler.show_in_front, "ruler must be non-rendering foreground guidance")
    assert_true(ruler["oleander_ruler_minor_intervals"] == 100 and ruler["oleander_ruler_major_ticks"] == 11, "ruler tick counts must be deterministic")
    assert_true(len(ruler.data.edges) == 102, "ruler mesh must contain one baseline plus 101 tick edges")
    assert_close(scene_units_to_mm(scene, ruler.data.vertices[1].co.x), 1000.0, 1e-5, "ruler baseline must be exactly 1000 mm")
    label_names = json.loads(ruler["oleander_ruler_labels"])
    assert_true(len(label_names) == 6, "label_every_major=2 must create six labels from 0 to 1000 mm")
    label_bodies = [bpy.data.objects[name].data.body for name in label_names]
    assert_true(label_bodies[0] == "0 mm" and label_bodies[-1] == "1 m", "major labels must retain physical units")
    guide_collection = bpy.data.collections.get(GUIDE_COLLECTION)
    assert_true(guide_collection is not None and guide_collection.hide_render, "guide collection must be non-rendering")

    # Rulers are support objects and must not pollute model audit with missing IDs/non-manifold edge failures.
    audited = audit_scene(scene)
    ruler_result = next(item for item in audited["objects"] if item["name"] == ruler.name)
    assert_true(ruler_result["scope"] == "REFERENCE_GUIDE" and ruler_result["issues"] == [], "ruler must audit as reference guide without model issues")
    assert_true(audited["reference_guide_count"] >= 7, "ruler and generated labels must be counted as reference guides")

    # Positive failures: no irregular terminal tick and no pathological tick/label counts.
    expect_value_error(
        lambda: create_ruler_guide(bpy.context, "X", 1000.0, 30.0, 10, labels=False),
        "integer multiple",
    )
    expect_value_error(
        lambda: create_ruler_guide(bpy.context, "X", 6000.0, 1.0, 10, labels=False),
        "5000 minor intervals",
    )
    expect_value_error(
        lambda: create_ruler_guide(bpy.context, "X", 10000.0, 10.0, 1, labels=True, label_every_major=1),
        "100 labels",
    )

    # Operator registration and native increment-snap configuration are also exercised.
    profile_op = bpy.ops.oleander.set_measurement_profile(
        profile="PRODUCT",
        configure_native_snap=True,
        configure_viewport_grid=False,
    )
    assert_true("FINISHED" in profile_op, "measurement profile operator must execute")
    assert_true(scene.tool_settings.use_snap and "INCREMENT" in scene.tool_settings.snap_elements, "profile operator must configure native increment snap")
    assert_true(profile_values(scene)["snap_step_mm"] == 1.0, "PRODUCT profile exact snap must be 1 mm")

    # Event/snapshot/profile/ruler persistence through .blend reopen.
    events_before = measurement_events(scene)
    assert_true(events_before, "measurement actions must produce monotonic event records")
    assert_true([event["event_index"] for event in events_before] == list(range(1, len(events_before) + 1)), "measurement event log must be monotonic")
    reopen_path = "/tmp/oleander-stage3-measurement-reopen.blend"
    bpy.ops.wm.save_as_mainfile(filepath=reopen_path)
    bpy.ops.wm.open_mainfile(filepath=reopen_path)
    reopened_scene = bpy.context.scene
    reopened_ruler = bpy.data.objects.get(ruler.name)
    assert_true(reopened_ruler is not None and reopened_ruler.get("oleander_guide_kind") == "WORLD_RULER", "ruler must survive .blend reopen")
    assert_true(profile_values(reopened_scene)["profile"] == "PRODUCT", "measurement profile must survive .blend reopen")
    assert_true(SNAPSHOT_KEY in reopened_scene, "measurement snapshot must survive .blend reopen")
    assert_true(len(measurement_events(reopened_scene)) == len(events_before), "measurement event log must survive .blend reopen")

    result = {
        "runtime": "OLEANDER Blender Runtime",
        "stage": "STAGE3_MEASUREMENT_SCALE_RULER",
        "version": "0.2.0",
        "blender": bpy.app.version_string,
        "status": "PASS",
        "source_fingerprint_sha256": source_fingerprint(),
        "checks": [
            "measurement_profile_scene_scale_preservation",
            "scene_unit_mm_round_trip",
            "measurement_snapshot_active_dimensions",
            "measurement_snapshot_pair_origin_distance",
            "exact_world_location_quantize",
            "quantize_axis_mask_preservation",
            "quantize_downstream_stale_propagation",
            "exact_mm_nudge",
            "external_transform_authority_quantize_failure",
            "external_authority_failure_no_transform_mutation",
            "world_ruler_editable_mesh",
            "world_ruler_minor_major_tick_counts",
            "world_ruler_metric_baseline",
            "world_ruler_major_labels_with_units",
            "world_ruler_non_rendering_reference_scope",
            "reference_guide_audit_exclusion",
            "irregular_ruler_interval_expected_failure",
            "excessive_ruler_intervals_expected_failure",
            "excessive_ruler_labels_expected_failure",
            "native_increment_snap_configuration",
            "measurement_profile_save_reopen_persistence",
            "measurement_snapshot_save_reopen_persistence",
            "world_ruler_save_reopen_persistence",
            "measurement_event_log_save_reopen_persistence",
        ],
        "expected_failure_cases": {
            "external_transform_authority": "PASS",
            "irregular_ruler_interval": "PASS",
            "excessive_ruler_intervals": "PASS",
            "excessive_ruler_labels": "PASS",
        },
        "non_claims": [
            "screen_space_ruler_dimensional_authority",
            "viewport_grid_dimensional_authority",
            "cad_dimension_constraint_solver",
            "solver_backed_sketch_constraints",
            "field_truth",
            "engineering_approval",
            "manufacturing_release",
            "constructability",
            "design_quality",
        ],
    }
    print("OLEANDER_STAGE3_MEASUREMENT_VALIDATION=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
