"""Real-Blender validation for OLEANDER Design Intent Apply foundation."""

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
import oleander_blender.design_intent_apply as apply_layer
from oleander_blender.angular_datum import create_datum_axis
from oleander_blender.design_intent import (
    bind_design_parameter,
    create_design_parameter,
    get_design_parameter_events,
    get_design_parameters,
    update_design_parameter,
)
from oleander_blender.design_intent_apply import (
    apply_design_parameter,
    preflight_design_parameter_apply,
)
from oleander_blender.direct_model import _scene_units_to_mm
from oleander_blender.feature_stack import FEATURE_HISTORY_KEY, get_feature_history
from oleander_blender.relation_kernel import create_relation, get_relations


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


def add_plane(name, oid, size=100.0, location=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_plane_add(size=size, location=location)
    obj = bpy.context.active_object
    obj.name = name
    set_metadata(obj, oid)
    return obj


def select_only(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


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

    model = add_cube("OLE_APPLY_MODEL", "OLE_APPLY_MODEL", size=100.0)
    downstream = add_cube("OLE_APPLY_DOWNSTREAM", "OLE_APPLY_DOWNSTREAM", size=25.0, location=(400.0, 0.0, 0.0))
    downstream.oleander.dependencies = "OLE_APPLY_MODEL"

    feature_obj = add_plane("OLE_APPLY_FEATURE", "OLE_APPLY_FEATURE", size=100.0, location=(0.0, 300.0, 0.0))
    select_only(feature_obj)
    assert_true(bpy.ops.oleander.add_planar_extrude(depth_mm=25.0) == {"FINISHED"}, "feature setup must succeed")
    feature = get_feature_history(feature_obj)[0]
    feature_id = feature["feature_id"]
    modifier = feature_obj.modifiers.get(feature["modifier_name"])
    assert_true(modifier is not None, "feature modifier must exist")

    driver = add_cube("OLE_APPLY_DRIVER", "OLE_APPLY_DRIVER", size=30.0, location=(-200.0, -300.0, 0.0))
    relation_driven = add_cube("OLE_APPLY_REL_DRIVEN", "OLE_APPLY_REL_DRIVEN", size=30.0, location=(100.0, -300.0, 0.0))
    relation = create_relation(scene, driver, relation_driven, "AXIS_OFFSET", axis="X", capture_current=True)
    relation_id = relation["relation_id"]

    select_only(model)
    datum = create_datum_axis(bpy.context, "X", 500.0, "WORLD_ORIGIN")
    datum_id = datum["oleander_guide_id"]

    object_param = create_design_parameter(scene, "AppliedWidth", "LENGTH_MM", 140.0, minimum=50.0, maximum=300.0)
    feature_param = create_design_parameter(scene, "AppliedExtrude", "LENGTH_MM", 40.0, minimum=1.0, maximum=200.0)
    relation_param = create_design_parameter(scene, "AppliedRelationTarget", "LENGTH_MM", 450.0, minimum=0.0, maximum=1000.0)
    datum_param = create_design_parameter(scene, "AppliedDatumLength", "LENGTH_MM", 800.0, minimum=10.0, maximum=2000.0)
    rollback_param = create_design_parameter(scene, "RollbackMultiTarget", "LENGTH_MM", 160.0, minimum=1.0, maximum=500.0)
    unsupported_param = create_design_parameter(scene, "UnsupportedField", "LENGTH_MM", 111.0, minimum=1.0, maximum=500.0)
    constrained_param = create_design_parameter(scene, "ConstrainedTarget", "LENGTH_MM", 125.0, minimum=1.0, maximum=500.0)

    bind_design_parameter(scene, object_param["parameter_id"], "OBJECT", "OLE_APPLY_MODEL", "DIMENSION_X")
    bind_design_parameter(scene, feature_param["parameter_id"], "FEATURE", feature_id, "depth_mm")
    bind_design_parameter(scene, relation_param["parameter_id"], "RELATION", relation_id, "target_mm")
    bind_design_parameter(scene, datum_param["parameter_id"], "DATUM_REFERENCE", datum_id, "length_mm")
    bind_design_parameter(scene, rollback_param["parameter_id"], "OBJECT", "OLE_APPLY_MODEL", "DIMENSION_Y")
    bind_design_parameter(scene, rollback_param["parameter_id"], "FEATURE", feature_id, "depth_mm")
    bind_design_parameter(scene, unsupported_param["parameter_id"], "OBJECT", "OLE_APPLY_MODEL", "LOCATION_X")

    constrained = add_cube("OLE_APPLY_CONSTRAINED", "OLE_APPLY_CONSTRAINED", size=60.0, location=(700.0, 0.0, 0.0))
    constrained.constraints.new(type="COPY_LOCATION")
    bind_design_parameter(scene, constrained_param["parameter_id"], "OBJECT", "OLE_APPLY_CONSTRAINED", "DIMENSION_X")

    # Explicit apply is a separate action: updating intent alone still does not mutate geometry.
    before_x = _scene_units_to_mm(bpy.context, model.dimensions.x)
    update_design_parameter(scene, object_param["parameter_id"], 150.0)
    assert_true(abs(_scene_units_to_mm(bpy.context, model.dimensions.x) - before_x) < 1e-6, "intent update must not auto-apply object geometry")
    downstream.oleander.stale = False
    downstream["oleander_stale_reason"] = ""

    preflight = preflight_design_parameter_apply(scene, object_param["parameter_id"])
    assert_true(preflight["status"] == "PASS" and preflight["binding_count"] == 1, "object apply preflight must pass")
    assert_true(preflight["solver_claim"] is False and preflight["automatic_parameter_geometry_rebuild"] is False, "preflight must preserve no-solver boundary")

    object_result = apply_design_parameter(scene, object_param["parameter_id"])
    assert_true(object_result["status"] == "PASS", "explicit object apply must pass")
    assert_true(abs(_scene_units_to_mm(bpy.context, model.dimensions.x) - 150.0) < 1e-4, "object DIMENSION_X must reach parameter value")
    assert_true(object_result["model_geometry_mutated"] is True, "explicit object dimension apply must report model geometry mutation")
    assert_true(downstream.oleander.stale, "explicit model apply must propagate downstream stale state")
    assert_true(object_result["solver_claim"] is False and object_result["cad_parametric_feature_rebuild_claim"] is False, "explicit apply must deny solver/CAD rebuild authority")

    feature_result = apply_design_parameter(scene, feature_param["parameter_id"])
    history_after_feature = get_feature_history(feature_obj)
    feature_after = next(item for item in history_after_feature if item["feature_id"] == feature_id)
    assert_true(abs(_scene_units_to_mm(bpy.context, modifier.thickness) - 40.0) < 1e-4, "feature modifier must receive parameter value")
    assert_true(feature_after["parameters"]["depth_mm"] == 40.0, "feature history must stay synchronized with modifier")
    assert_true(feature_after.get("edit_revision", 0) >= 1, "feature apply must increment edit revision")
    assert_true(feature_result["postcheck"]["status"] == "PASS", "feature postcheck must pass")

    relation_location_before = relation_driven.location.copy()
    relation_result = apply_design_parameter(scene, relation_param["parameter_id"])
    relation_after = next(item for item in get_relations(scene) if item["relation_id"] == relation_id)
    assert_true(relation_after["target_mm"] == 450.0, "relation target metadata must receive parameter value")
    assert_true(relation_driven.location == relation_location_before, "relation target apply must not move driven geometry")
    assert_true(relation_result["model_geometry_mutated"] is False and relation_result["metadata_mutated"] is True, "relation apply must be metadata-only")

    datum_vertices_before = [vertex.co.copy() for vertex in datum.data.vertices]
    datum_result = apply_design_parameter(scene, datum_param["parameter_id"])
    assert_true(abs(float(datum["oleander_datum_length_mm"]) - 800.0) < 1e-9, "datum length metadata must update")
    assert_true(abs((datum.data.vertices[1].co - datum.data.vertices[0].co).length - 800.0) < 1e-6, "datum reference geometry must update to requested length")
    assert_true(datum_vertices_before != [vertex.co.copy() for vertex in datum.data.vertices], "datum reference geometry must actually change")
    assert_true(datum_result["reference_geometry_mutated"] is True and datum_result["model_geometry_mutated"] is False, "datum mutation must remain reference-only")

    # Unsupported target fields are rejected in whole-parameter preflight with zero mutation.
    unsupported_before = model.matrix_world.copy()
    unsupported_data_before = [vertex.co.copy() for vertex in model.data.vertices]
    expect_value_error(lambda: preflight_design_parameter_apply(scene, unsupported_param["parameter_id"]), "unsupported OBJECT apply field")
    assert_true(model.matrix_world == unsupported_before, "preflight failure must not mutate object transform")
    assert_true([vertex.co.copy() for vertex in model.data.vertices] == unsupported_data_before, "preflight failure must not mutate mesh")

    # External transform authority blocks object dimensions before mutation.
    constrained_before = constrained.matrix_world.copy()
    expect_value_error(lambda: preflight_design_parameter_apply(scene, constrained_param["parameter_id"]), "external transform authority")
    assert_true(constrained.matrix_world == constrained_before, "authority preflight failure must not mutate constrained object")

    # Forced postcheck failure proves reverse snapshot rollback after real mutations.
    rollback_y_before = _scene_units_to_mm(bpy.context, model.dimensions.y)
    rollback_feature_before = float(modifier.thickness)
    rollback_history_before = feature_obj.get(FEATURE_HISTORY_KEY, "")
    original_postcheck = apply_layer._postcheck_plan
    try:
        apply_layer._postcheck_plan = lambda scene, parameter, plan: {"status": "FAIL", "results": [], "failures": [{"forced": True}], "solver_claim": False}
        expect_value_error(lambda: apply_design_parameter(scene, rollback_param["parameter_id"]), "rolled back")
    finally:
        apply_layer._postcheck_plan = original_postcheck
    assert_true(abs(_scene_units_to_mm(bpy.context, model.dimensions.y) - rollback_y_before) < 1e-4, "rollback must restore object dimension")
    assert_true(abs(float(modifier.thickness) - rollback_feature_before) < 1e-9, "rollback must restore feature modifier")
    assert_true(feature_obj.get(FEATURE_HISTORY_KEY, "") == rollback_history_before, "rollback must restore feature history")
    last_apply = json.loads(scene.get("oleander_design_intent_last_apply", "{}"))
    assert_true(last_apply.get("status") == "ROLLED_BACK" and last_apply.get("rollback_performed") is True, "rollback receipt must be stored")

    # Failure envelope blocks apply before any target mutation.
    envelope_param = create_design_parameter(scene, "EnvelopeReject", "LENGTH_MM", 500.0, minimum=1.0, maximum=100.0)
    bind_design_parameter(scene, envelope_param["parameter_id"], "OBJECT", "OLE_APPLY_MODEL", "DIMENSION_Z")
    z_before = _scene_units_to_mm(bpy.context, model.dimensions.z)
    expect_value_error(lambda: preflight_design_parameter_apply(scene, envelope_param["parameter_id"]), "outside valid failure envelope")
    assert_true(abs(_scene_units_to_mm(bpy.context, model.dimensions.z) - z_before) < 1e-6, "failure-envelope rejection must not mutate target")
    update_design_parameter(scene, envelope_param["parameter_id"], 90.0)

    assert_true(hasattr(bpy.ops.oleander, "preflight_design_parameter_apply"), "preflight apply operator must register")
    assert_true(hasattr(bpy.ops.oleander, "apply_design_parameter"), "explicit apply operator must register")

    events = get_design_parameter_events(scene)
    actions = [event.get("action") for event in events]
    assert_true("APPLY_COMMIT" in actions, "successful explicit apply must create commit provenance")
    assert_true("APPLY_ROLLBACK" in actions, "rolled-back explicit apply must create rollback provenance")

    blend_path = pathlib.Path("/tmp/oleander-stage3-design-intent-apply-reopen.blend")
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    bpy.ops.wm.open_mainfile(filepath=str(blend_path))
    scene = bpy.context.scene
    reopened_model = next(obj for obj in scene.objects if getattr(getattr(obj, "oleander", None), "ole_id", "") == "OLE_APPLY_MODEL")
    reopened_feature = next(obj for obj in scene.objects if getattr(getattr(obj, "oleander", None), "ole_id", "") == "OLE_APPLY_FEATURE")
    reopened_datum = next(obj for obj in scene.objects if obj.get("oleander_guide_id", "") == datum_id)
    reopened_relation = next(item for item in get_relations(scene) if item["relation_id"] == relation_id)
    assert_true(abs(_scene_units_to_mm(bpy.context, reopened_model.dimensions.x) - 150.0) < 1e-4, "applied object dimension must survive reopen")
    reopened_feature_entry = next(item for item in get_feature_history(reopened_feature) if item["feature_id"] == feature_id)
    reopened_modifier = reopened_feature.modifiers.get(reopened_feature_entry["modifier_name"])
    assert_true(abs(_scene_units_to_mm(bpy.context, reopened_modifier.thickness) - 40.0) < 1e-4, "applied feature value must survive reopen")
    assert_true(reopened_relation["target_mm"] == 450.0, "applied relation metadata must survive reopen")
    assert_true(reopened_datum["oleander_datum_length_mm"] == 800.0, "applied datum reference value must survive reopen")
    assert_true(get_design_parameters(scene), "design parameters must survive reopen")
    assert_true(get_design_parameter_events(scene), "apply event provenance must survive reopen")

    checks = [
        "explicit_apply_separate_from_parameter_update",
        "whole_parameter_preflight",
        "object_dimension_apply",
        "object_dimension_postcheck",
        "object_apply_breaks_no_solver_boundary",
        "object_apply_downstream_stale_propagation",
        "feature_parameter_apply",
        "feature_modifier_history_synchronization",
        "feature_history_postcheck",
        "relation_target_metadata_apply",
        "relation_apply_no_geometry_motion",
        "datum_reference_geometry_apply",
        "datum_reference_authority_separation",
        "unsupported_field_expected_failure",
        "unsupported_field_no_mutation",
        "external_transform_authority_expected_failure",
        "external_authority_no_mutation",
        "transaction_postcheck_failure_rollback",
        "rollback_restores_object_geometry",
        "rollback_restores_feature_modifier_and_history",
        "rollback_event_provenance",
        "failure_envelope_expected_failure",
        "failure_envelope_no_mutation",
        "apply_commit_event_provenance",
        "design_intent_apply_operator_registration",
        "explicit_apply_save_reopen_persistence",
    ]
    failures = {
        "unsupported_target_field": "PASS",
        "external_transform_authority": "PASS",
        "forced_postcheck_transaction_rollback": "PASS",
        "failure_envelope_breach": "PASS",
    }
    result = {
        "runtime": "OLEANDER Blender Runtime",
        "version": "0.2.0",
        "blender": bpy.app.version_string,
        "stage": "STAGE3_DESIGN_INTENT_APPLY_FOUNDATION",
        "status": "PASS",
        "checks": checks,
        "expected_failure_cases": failures,
        "source_fingerprint_sha256": source_fingerprint(),
        "non_claims": [
            "constraint_solver",
            "cad_sketch_solver",
            "automatic_parameter_geometry_rebuild",
            "cad_brep_feature_rebuild",
            "multi_parameter_solver",
            "engineering_approval",
            "manufacturing_release",
            "field_truth",
            "constructability",
            "design_quality",
        ],
    }
    print("OLEANDER_STAGE3_DESIGN_INTENT_APPLY_VALIDATION=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
