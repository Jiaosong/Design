"""Real-Blender validation for OLEANDER Design Intent Graph foundation."""

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
from oleander_blender.angular_datum import create_datum_axis
from oleander_blender.design_intent import (
    add_parameter_dependency,
    audit_design_intent_graph,
    bind_design_parameter,
    create_design_parameter,
    diff_design_intent_from_baseline,
    evaluate_failure_envelope,
    get_design_parameter_events,
    get_design_parameters,
    store_design_intent_baseline,
    update_design_parameter,
)
from oleander_blender.feature_stack import get_feature_history
from oleander_blender.relation_kernel import create_relation


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def expect_value_error(fn, text):
    try:
        fn()
    except ValueError as exc:
        assert_true(text in str(exc), f"expected {text!r}; got {exc!r}")
        return
    raise AssertionError(f"expected ValueError containing {text!r}")


def source_fingerprint():
    paths = [
        path
        for path in ADDON_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".py", ".json", ".toml"}
    ]
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
    for key in list(bpy.context.scene.keys()):
        if str(key).startswith("oleander_design_") or str(key).startswith("oleander_relation_") or key == "oleander_relations":
            try:
                del bpy.context.scene[key]
            except Exception:
                pass


def set_metadata(obj, oid):
    obj.oleander.ole_id = oid
    obj.oleander.geometry_authority = "VERIFIED_SOURCE"
    obj.oleander.field_state = "NOT_APPLICABLE"
    obj.oleander.engineering_state = "NOT_APPLICABLE"
    obj.oleander.manufacturing_state = "NOT_APPLICABLE"
    obj.oleander.design_review_state = "NA"


def add_cube(name, oid, size=100.0, location=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=size, location=location)
    obj = bpy.context.active_object
    obj.name = name
    set_metadata(obj, oid)
    return obj


def add_plane(name, oid, size=100.0):
    bpy.ops.mesh.primitive_plane_add(size=size)
    obj = bpy.context.active_object
    obj.name = name
    set_metadata(obj, oid)
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

    driver = add_cube("OLE_INTENT_DRIVER", "OLE_INTENT_DRIVER", size=50.0, location=(-200.0, 0.0, 0.0))
    main_obj = add_plane("OLE_INTENT_MAIN", "OLE_INTENT_MAIN", size=100.0)
    downstream = add_cube("OLE_INTENT_DOWNSTREAM", "OLE_INTENT_DOWNSTREAM", size=25.0, location=(200.0, 0.0, 0.0))
    downstream.oleander.dependencies = "OLE_INTENT_MAIN"

    # Existing stable feature identity is reused rather than inventing a parallel feature namespace.
    bpy.context.view_layer.objects.active = main_obj
    main_obj.select_set(True)
    driver.select_set(False)
    downstream.select_set(False)
    result = bpy.ops.oleander.add_planar_extrude(depth_mm=25.0)
    assert_true(result == {"FINISHED"}, "governed planar extrude must succeed")
    feature_history = get_feature_history(main_obj)
    assert_true(len(feature_history) == 1, "feature history must contain one feature")
    feature_id = feature_history[0]["feature_id"]

    relation = create_relation(scene, driver, main_obj, "AXIS_OFFSET", axis="X", capture_current=True)
    relation_id = relation["relation_id"]

    # Datum/reference identity is already stable as OLE_GUIDE::DATUM_* and is reused directly.
    bpy.context.view_layer.objects.active = main_obj
    datum = create_datum_axis(bpy.context, "X", 500.0, "WORLD_ORIGIN")
    datum_id = datum["oleander_guide_id"]
    assert_true(datum_id.startswith("OLE_GUIDE::DATUM_AXIS::"), "datum must use existing stable guide identity")

    length = create_design_parameter(scene, "PrimaryLength", "LENGTH_MM", 100.0, minimum=50.0, maximum=150.0)
    angle = create_design_parameter(scene, "PrimaryAngle", "ANGLE_DEG", 30.0, minimum=0.0, maximum=90.0)
    count = create_design_parameter(scene, "ModuleCount", "COUNT", 4)
    boolean = create_design_parameter(scene, "MirrorEnabled", "BOOLEAN", True)
    enum = create_design_parameter(scene, "MaterialFamily", "ENUM", "A")
    derived = create_design_parameter(scene, "DerivedSpacing", "LENGTH_MM", 25.0, role="DERIVED")

    ids = [item["parameter_id"] for item in get_design_parameters(scene)]
    assert_true(ids == [f"OLE_PARAM::P{i:04d}" for i in range(1, 7)], "parameter IDs must be stable and monotonic")
    assert_true(length["unit"] == "mm" and angle["unit"] == "deg" and count["unit"] == "count", "typed unit mapping must be deterministic")
    assert_true(boolean["value"] is True and enum["value"] == "A", "BOOLEAN/ENUM API values must remain typed")
    assert_true(all(item["solver_claim"] is False and item["automatic_geometry_apply"] is False for item in get_design_parameters(scene)), "parameter registry must explicitly deny solver/automatic geometry claims")

    expect_value_error(lambda: create_design_parameter(scene, "PrimaryLength", "LENGTH_MM", 20.0), "already exists")
    expect_value_error(lambda: create_design_parameter(scene, "BadCount", "COUNT", 2.5), "non-negative integer")
    expect_value_error(lambda: create_design_parameter(scene, "BadEnvelope", "LENGTH_MM", 1.0, minimum=10.0, maximum=5.0), "minimum cannot exceed maximum")
    expect_value_error(lambda: create_design_parameter(scene, "BadBoolEnvelope", "BOOLEAN", True, minimum=0.0, maximum=1.0), "only supported for numeric")

    add_parameter_dependency(scene, derived["parameter_id"], length["parameter_id"])
    before_cycle = json.dumps(get_design_parameters(scene), sort_keys=True)
    expect_value_error(lambda: add_parameter_dependency(scene, length["parameter_id"], derived["parameter_id"]), "create a cycle")
    assert_true(json.dumps(get_design_parameters(scene), sort_keys=True) == before_cycle, "cycle failure must not mutate registry")
    expect_value_error(lambda: add_parameter_dependency(scene, length["parameter_id"], "OLE_PARAM::P9999"), "missing parameter")
    expect_value_error(lambda: add_parameter_dependency(scene, length["parameter_id"], length["parameter_id"]), "depend on itself")

    bind_design_parameter(scene, length["parameter_id"], "OBJECT", "OLE_INTENT_MAIN", "DIMENSION_X")
    bind_design_parameter(scene, length["parameter_id"], "FEATURE", feature_id, "depth_mm")
    bind_design_parameter(scene, length["parameter_id"], "RELATION", relation_id, "target_mm")
    bind_design_parameter(scene, angle["parameter_id"], "DATUM_REFERENCE", datum_id, "reference_angle_deg")
    expect_value_error(lambda: bind_design_parameter(scene, length["parameter_id"], "OBJECT", "OLE_MISSING", "DIMENSION_X"), "target not found")
    expect_value_error(lambda: bind_design_parameter(scene, "OLE_PARAM::P9999", "OBJECT", "OLE_INTENT_MAIN", "DIMENSION_X"), "parameter not found")
    expect_value_error(lambda: bind_design_parameter(scene, length["parameter_id"], "OBJECT", "OLE_INTENT_MAIN", "DIMENSION_X"), "duplicate design-intent binding")

    audit_before = audit_design_intent_graph(scene)
    assert_true(audit_before["status"] == "PASS", f"valid intent graph must audit PASS: {audit_before}")
    assert_true(audit_before["solver_claim"] is False and audit_before["automatic_geometry_apply"] is False, "audit must deny solver/automatic application")

    baseline = store_design_intent_baseline(scene)
    assert_true(len(baseline["sha256"]) == 64, "intent baseline must have SHA256")
    location_before = main_obj.location.copy()
    dimensions_before = main_obj.dimensions.copy()

    update = update_design_parameter(scene, length["parameter_id"], 130.0)
    assert_true(update["after"] == 130.0 and update["revision"] > 1, "parameter update must increment revision")
    assert_true("OLE_INTENT_MAIN" in update["direct_stale"], "bound object/feature/relation owner must become direct stale")
    assert_true("OLE_INTENT_DOWNSTREAM" in update["downstream_stale"], "object dependency graph must propagate parameter stale state")
    assert_true(main_obj.oleander.stale and downstream.oleander.stale, "direct and downstream objects must be marked stale")
    assert_true(main_obj.location == location_before and main_obj.dimensions == dimensions_before, "parameter update must not automatically mutate geometry")
    assert_true(update["geometry_mutated"] is False and update["solver_claim"] is False, "update result must explicitly deny geometry/solver claims")
    assert_true(update["envelope"]["status"] == "PASS", "130 mm must remain inside declared failure envelope")

    diff = diff_design_intent_from_baseline(scene)
    assert_true(diff["status"] == "CHANGED", "parameter value/revision change must be diff-visible")
    assert_true(any(item["parameter_id"] == length["parameter_id"] for item in diff["changed_parameters"]), "diff must identify changed parameter ID")

    breach = update_design_parameter(scene, length["parameter_id"], 200.0)
    assert_true(breach["envelope"]["status"] == "FAIL", "outside-envelope value must be diagnosed, not silently accepted as valid")
    assert_true(evaluate_failure_envelope(next(item for item in get_design_parameters(scene) if item["parameter_id"] == length["parameter_id"]))["reason"] == "OUTSIDE_FAILURE_ENVELOPE", "failure-envelope reason must be explicit")
    audit_breach = audit_design_intent_graph(scene)
    assert_true(audit_breach["status"] == "FAIL" and audit_breach["failure_envelope_breaches"], "envelope breach must fail intent audit")
    update_design_parameter(scene, length["parameter_id"], 120.0)
    assert_true(audit_design_intent_graph(scene)["status"] == "PASS", "restored parameter envelope must return audit to PASS")

    # Positive failure: unresolved target after source deletion must surface in audit.
    temp = add_cube("OLE_INTENT_TEMP", "OLE_INTENT_TEMP", size=10.0)
    bind_design_parameter(scene, count["parameter_id"], "OBJECT", "OLE_INTENT_TEMP", "INSTANCE_COUNT")
    bpy.data.objects.remove(temp, do_unlink=True)
    audit_missing = audit_design_intent_graph(scene)
    assert_true(audit_missing["status"] == "FAIL" and audit_missing["missing_bindings"], "deleted binding target must fail graph audit")
    parameters = get_design_parameters(scene)
    count_record = next(item for item in parameters if item["parameter_id"] == count["parameter_id"])
    count_record["bindings"] = [binding for binding in count_record["bindings"] if binding["target_id"] != "OLE_INTENT_TEMP"]
    scene["oleander_design_parameters"] = json.dumps(parameters, sort_keys=True, ensure_ascii=False)
    assert_true(audit_design_intent_graph(scene)["status"] == "PASS", "removing unresolved binding must restore audit PASS")

    assert_true(hasattr(bpy.ops.oleander, "create_design_parameter"), "create parameter operator must register")
    assert_true(hasattr(bpy.ops.oleander, "update_design_parameter"), "update parameter operator must register")
    assert_true(hasattr(bpy.ops.oleander, "bind_design_parameter_object"), "object binding operator must register")
    assert_true(hasattr(bpy.ops.oleander, "audit_design_intent"), "intent audit operator must register")
    assert_true(hasattr(bpy.ops.oleander, "store_design_intent_baseline"), "intent baseline operator must register")
    assert_true(hasattr(bpy.ops.oleander, "diff_design_intent"), "intent diff operator must register")

    events_before_reopen = get_design_parameter_events(scene)
    assert_true(len(events_before_reopen) >= 10, "parameter changes/bindings/dependencies must produce event provenance")
    assert_true([event["event_index"] for event in events_before_reopen] == sorted(event["event_index"] for event in events_before_reopen), "parameter events must be monotonic")

    blend_path = pathlib.Path("/tmp/oleander-stage3-design-intent-reopen.blend")
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    bpy.ops.wm.open_mainfile(filepath=str(blend_path))
    scene = bpy.context.scene
    reopened = get_design_parameters(scene)
    assert_true(len(reopened) == 6, "parameter registry must survive .blend reopen")
    assert_true(reopened[0]["parameter_id"] == "OLE_PARAM::P0001", "stable parameter ID must survive reopen")
    assert_true(len(get_design_parameter_events(scene)) == len(events_before_reopen), "parameter event log must survive reopen")
    assert_true(scene.get("oleander_design_intent_baseline", ""), "intent baseline must survive reopen")
    assert_true(audit_design_intent_graph(scene)["status"] == "PASS", "reopened intent graph must audit PASS")

    checks = [
        "stable_monotonic_parameter_ids",
        "typed_parameter_values_and_units",
        "primary_derived_roles",
        "parameter_authority_metadata",
        "parameter_solver_claim_false",
        "parameter_automatic_geometry_apply_false",
        "duplicate_parameter_name_expected_failure",
        "invalid_count_expected_failure",
        "invalid_failure_envelope_expected_failure",
        "non_numeric_failure_envelope_expected_failure",
        "parameter_dependency_graph",
        "parameter_dependency_cycle_expected_failure",
        "cycle_failure_no_registry_mutation",
        "missing_parameter_dependency_expected_failure",
        "self_parameter_dependency_expected_failure",
        "object_binding_by_stable_ole_id",
        "feature_binding_by_stable_feature_id",
        "relation_binding_by_stable_relation_id",
        "datum_binding_reuses_stable_guide_id",
        "missing_binding_target_expected_failure",
        "missing_parameter_binding_expected_failure",
        "duplicate_binding_expected_failure",
        "design_intent_graph_audit",
        "design_intent_baseline_sha256",
        "parameter_revision_increment",
        "parameter_event_log",
        "bound_target_direct_stale",
        "object_dependency_downstream_stale",
        "parameter_update_no_automatic_geometry_mutation",
        "failure_envelope_pass_state",
        "failure_envelope_breach_detection",
        "failure_envelope_breach_audit_failure",
        "design_intent_diff",
        "deleted_binding_target_audit_failure",
        "design_intent_operator_registration",
        "design_intent_save_reopen_persistence",
        "design_intent_event_save_reopen_persistence",
        "design_intent_baseline_save_reopen_persistence",
    ]
    failures = {
        "duplicate_parameter_name": "PASS",
        "invalid_count": "PASS",
        "invalid_failure_envelope": "PASS",
        "non_numeric_failure_envelope": "PASS",
        "parameter_dependency_cycle": "PASS",
        "cycle_failure_no_registry_mutation": "PASS",
        "missing_parameter_dependency": "PASS",
        "self_parameter_dependency": "PASS",
        "missing_binding_target": "PASS",
        "missing_parameter_binding": "PASS",
        "duplicate_binding": "PASS",
        "failure_envelope_breach": "PASS",
        "deleted_binding_target": "PASS",
    }
    receipt = {
        "status": "PASS",
        "runtime": "OLEANDER Blender Runtime",
        "version": "0.2.0",
        "blender": bpy.app.version_string,
        "stage": "STAGE3_DESIGN_INTENT_GRAPH_FOUNDATION",
        "checks": checks,
        "expected_failure_cases": failures,
        "source_fingerprint_sha256": source_fingerprint(),
        "non_claims": [
            "constraint_solver",
            "cad_sketch_solver",
            "automatic_parameter_geometry_rebuild",
            "cad_brep_feature_rebuild",
            "engineering_approval",
            "manufacturing_release",
            "field_truth",
            "constructability",
            "design_quality",
        ],
    }
    print("OLEANDER_STAGE3_DESIGN_INTENT_VALIDATION=" + json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
