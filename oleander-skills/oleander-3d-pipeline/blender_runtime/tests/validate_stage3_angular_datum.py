"""Real-Blender validation for OLEANDER Angular / Datum / Construction foundation."""

from __future__ import annotations

import hashlib
import math
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
from oleander_blender.angular_datum import (
    create_angle_guide,
    create_construction_line,
    create_datum_axis,
    create_datum_plane,
    nudge_world_rotation,
    quantize_world_rotation,
)
from oleander_blender.audit import audit_scene
from oleander_blender.measurement_system import GUIDE_COLLECTION, scene_units_to_mm

DEG_TOL = 1e-4
MM_TOL = 1e-3


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def assert_close(actual, expected, tolerance, message):
    if abs(actual - expected) > tolerance:
        raise AssertionError(f"{message}: actual={actual!r} expected={expected!r}")


def expect_value_error(callable_, expected_text):
    try:
        callable_()
    except ValueError as exc:
        assert_true(expected_text in str(exc), f"expected {expected_text!r}; got {exc!r}")
        return
    raise AssertionError(f"expected ValueError containing {expected_text!r}")


def source_fingerprint():
    paths = [path for path in ADDON_ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".py", ".json", ".toml"}]
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


def add_cube(name, ole_id, rotation_degrees=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=100.0)
    obj = bpy.context.active_object
    obj.name = name
    obj.oleander.ole_id = ole_id
    obj.oleander.geometry_authority = "VERIFIED_SOURCE"
    obj.oleander.field_state = "NOT_APPLICABLE"
    obj.oleander.engineering_state = "NOT_APPLICABLE"
    obj.oleander.manufacturing_state = "NOT_APPLICABLE"
    obj.oleander.design_review_state = "NA"
    obj.rotation_mode = "XYZ"
    obj.rotation_euler = [math.radians(value) for value in rotation_degrees]
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

    # Deterministic angular quantize with axis mask and downstream stale propagation.
    rot = add_cube("OLE_ROTATE", "OLE_ROTATE", (7.2, 14.1, 44.1))
    downstream = add_cube("OLE_ROTATE_DOWNSTREAM", "OLE_ROTATE_DOWNSTREAM")
    downstream.oleander.dependencies = "OLE_ROTATE"
    before_x = math.degrees(rot.rotation_euler.x)
    result = quantize_world_rotation(scene, [rot], 15.0, axes=(False, True, True))
    assert_true(len(result) == 1 and result[0]["step_degrees"] == 15.0, "angle quantize must emit deterministic record")
    assert_close(math.degrees(rot.rotation_euler.x), before_x, DEG_TOL, "disabled X angular snap must preserve angle")
    assert_close(math.degrees(rot.rotation_euler.y), 15.0, DEG_TOL, "Y must quantize to 15 degrees")
    assert_close(math.degrees(rot.rotation_euler.z), 45.0, DEG_TOL, "Z must quantize to 45 degrees")
    assert_true(downstream.oleander.stale, "angular quantize must stale downstream dependents")

    # Exact angular nudge.
    nudge = nudge_world_rotation(scene, rot, "Z", -5.0)
    assert_close(math.degrees(rot.rotation_euler.z), 40.0, DEG_TOL, "rotation nudge must apply exact degree amount")
    assert_true(nudge["axis"] == "Z" and nudge["amount_degrees"] == -5.0, "nudge record must preserve angular operation")

    # Batch preflight is atomic under external transform authority.
    free = add_cube("OLE_ROT_ATOMIC_FREE", "OLE_ROT_ATOMIC_FREE", (0.0, 0.0, 13.0))
    blocked = add_cube("OLE_ROT_ATOMIC_BLOCKED", "OLE_ROT_ATOMIC_BLOCKED", (0.0, 0.0, 29.0))
    constraint = blocked.constraints.new(type="COPY_ROTATION")
    constraint.name = "EXTERNAL_ANGULAR_AUTHORITY"
    free_before = free.rotation_euler.copy()
    blocked_before = blocked.rotation_euler.copy()
    expect_value_error(lambda: quantize_world_rotation(scene, [free, blocked], 15.0), "external transform authority")
    assert_true(sum(abs(free.rotation_euler[i] - free_before[i]) for i in range(3)) <= 1e-12, "failed angular batch must not partially mutate earlier objects")
    assert_true(sum(abs(blocked.rotation_euler[i] - blocked_before[i]) for i in range(3)) <= 1e-12, "failed angular batch must not mutate constrained object")

    # Editable 90-degree angle guide: 5-degree minor, 15-degree major.
    angle = create_angle_guide(bpy.context, "XY", 500.0, 90.0, 5.0, 3, labels=True)
    angle_name = angle.name
    assert_true(angle.get("oleander_reference_guide") is True and angle.get("oleander_guide_kind") == "ANGLE_GUIDE", "angle guide must be explicit reference-only geometry")
    assert_true(angle["oleander_angle_intervals"] == 18, "90/5 angle guide must expose 18 intervals")
    assert_close(angle["oleander_angle_radius_mm"], 500.0, MM_TOL, "angle guide must preserve physical radius")
    arc_vertex = angle.data.vertices[1].co
    assert_close(scene_units_to_mm(scene, arc_vertex.length), 500.0, MM_TOL, "angle-guide arc radius must be real metric geometry")

    # Datum axis / plane and construction line retain metric contracts.
    datum_axis = create_datum_axis(bpy.context, "X", 2000.0)
    datum_axis_name = datum_axis.name
    axis_span = datum_axis.data.vertices[1].co - datum_axis.data.vertices[0].co
    assert_close(scene_units_to_mm(scene, axis_span.length), 2000.0, MM_TOL, "datum axis must preserve requested length")
    assert_true(datum_axis["oleander_guide_kind"] == "DATUM_AXIS" and datum_axis["oleander_datum_axis"] == "X", "datum axis metadata must be stable")

    datum_plane = create_datum_plane(bpy.context, "XZ", 1200.0)
    datum_plane_name = datum_plane.name
    assert_true(datum_plane["oleander_guide_kind"] == "DATUM_PLANE" and datum_plane["oleander_datum_plane"] == "XZ", "datum plane metadata must be stable")
    assert_close(scene_units_to_mm(scene, abs(datum_plane.data.vertices[1].co.x - datum_plane.data.vertices[0].co.x)), 1200.0, MM_TOL, "datum plane must preserve requested size")

    construction = create_construction_line(bpy.context, "X", 3000.0, 150.0)
    construction_name = construction.name
    line_span = construction.data.vertices[1].co - construction.data.vertices[0].co
    assert_close(scene_units_to_mm(scene, line_span.length), 3000.0, MM_TOL, "construction line must preserve requested length")
    assert_close(scene_units_to_mm(scene, construction.data.vertices[0].co.y), 150.0, MM_TOL, "construction line must preserve exact offset")
    assert_true(construction["oleander_guide_kind"] == "CONSTRUCTION_LINE", "construction guide kind must be explicit")

    # All guides remain reference-only in audit and do not pollute governed model checks.
    audited = audit_scene(scene)
    for name in (angle_name, datum_axis_name, datum_plane_name, construction_name):
        item = next(record for record in audited["objects"] if record["name"] == name)
        assert_true(item["scope"] == "REFERENCE_GUIDE" and item["issues"] == [], f"{name} must stay outside governed model geometry")

    # Positive failure cases reject ambiguous/pathological guide parameters.
    expect_value_error(lambda: quantize_world_rotation(scene, [rot], 0.0), "rotation step")
    expect_value_error(lambda: create_angle_guide(bpy.context, "XY", 500.0, 91.0, 5.0, 3), "integer multiple")
    expect_value_error(lambda: create_angle_guide(bpy.context, "XY", 500.0, 360.0, 0.1, 10), "720 angular intervals")
    expect_value_error(lambda: create_datum_axis(bpy.context, "X", 0.0), "positive")
    expect_value_error(lambda: create_datum_plane(bpy.context, "AB", 1000.0), "unsupported datum plane")
    expect_value_error(lambda: create_construction_line(bpy.context, "X", -1.0), "positive")

    # Operator registration smoke tests.
    bpy.ops.object.select_all(action="DESELECT")
    rot.select_set(True)
    bpy.context.view_layer.objects.active = rot
    op = bpy.ops.oleander.quantize_rotation(step_degrees="5", axis_x=False, axis_y=False, axis_z=True)
    assert_true("FINISHED" in op, "angular quantize operator must execute")
    datum_op = bpy.ops.oleander.create_datum_axis(axis="Y", length_mm=1000.0, origin_mode="WORLD_ORIGIN")
    assert_true("FINISHED" in datum_op, "datum axis operator must execute")

    # Persistence through save/reopen.
    reopen_path = "/tmp/oleander-stage3-angular-datum-reopen.blend"
    bpy.ops.wm.save_as_mainfile(filepath=reopen_path)
    bpy.ops.wm.open_mainfile(filepath=reopen_path)
    for name, kind in (
        (angle_name, "ANGLE_GUIDE"),
        (datum_axis_name, "DATUM_AXIS"),
        (datum_plane_name, "DATUM_PLANE"),
        (construction_name, "CONSTRUCTION_LINE"),
    ):
        reopened = bpy.data.objects.get(name)
        assert_true(reopened is not None and reopened.get("oleander_guide_kind") == kind, f"{kind} must survive .blend reopen")

    result = {
        "runtime": "OLEANDER Blender Runtime",
        "stage": "STAGE3_ANGULAR_DATUM_CONSTRUCTION",
        "version": "0.2.0",
        "blender": bpy.app.version_string,
        "status": "PASS",
        "source_fingerprint_sha256": source_fingerprint(),
        "checks": [
            "angular_quantize_axis_mask",
            "angular_quantize_metric_degree_contract",
            "angular_quantize_downstream_stale",
            "angular_nudge_exact_degrees",
            "angular_batch_transform_authority_preflight",
            "angular_batch_failure_no_partial_mutation",
            "angle_guide_editable_reference_geometry",
            "angle_guide_metric_radius",
            "angle_guide_minor_major_interval_contract",
            "datum_axis_metric_length",
            "datum_plane_metric_size",
            "construction_line_metric_length_offset",
            "angular_datum_reference_guide_audit_exclusion",
            "invalid_rotation_step_expected_failure",
            "irregular_angle_interval_expected_failure",
            "excessive_angle_intervals_expected_failure",
            "invalid_datum_axis_expected_failure",
            "invalid_datum_plane_expected_failure",
            "invalid_construction_line_expected_failure",
            "angular_operator_registration",
            "datum_operator_registration",
            "angular_datum_save_reopen_persistence",
        ],
        "expected_failure_cases": {
            "external_transform_authority": "PASS",
            "invalid_rotation_step": "PASS",
            "irregular_angle_interval": "PASS",
            "excessive_angle_intervals": "PASS",
            "invalid_datum_axis": "PASS",
            "invalid_datum_plane": "PASS",
            "invalid_construction_line": "PASS",
        },
        "non_claims": [
            "solver_backed_angular_constraints",
            "cad_datum_feature_authority",
            "screen_space_angle_dimensional_authority",
            "field_truth",
            "engineering_approval",
            "manufacturing_release",
            "constructability",
            "design_quality",
        ],
    }
    import json
    print("OLEANDER_STAGE3_ANGULAR_DATUM_VALIDATION=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
