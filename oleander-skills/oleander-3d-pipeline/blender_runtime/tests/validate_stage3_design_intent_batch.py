"""Real-Blender validation for OLEANDER Design Intent Batch Apply foundation."""

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
import oleander_blender.design_intent_batch as batch_layer
from oleander_blender.angular_datum import create_datum_axis
from oleander_blender.design_intent import (
    add_parameter_dependency,
    bind_design_parameter,
    create_design_parameter,
    get_design_parameter_events,
)
from oleander_blender.design_intent_batch import (
    LAST_BATCH_APPLY_KEY,
    apply_design_parameter_batch,
    preflight_design_parameter_batch,
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
        return str(exc)
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


def mm(value):
    return _scene_units_to_mm(bpy.context, value)


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

    model = add_cube("OLE_BATCH_MODEL", "OLE_BATCH_MODEL", size=100.0)
    downstream = add_cube("OLE_BATCH_DOWNSTREAM", "OLE_BATCH_DOWNSTREAM", size=25.0, location=(500.0, 0.0, 0.0))
    downstream.oleander.dependencies = "OLE_BATCH_MODEL"

    feature_obj = add_plane("OLE_BATCH_FEATURE", "OLE_BATCH_FEATURE", size=100.0, location=(0.0, 300.0, 0.0))
    select_only(feature_obj)
    assert_true(bpy.ops.oleander.add_planar_extrude(depth_mm=20.0) == {"FINISHED"}, "feature setup must succeed")
    feature_entry = get_feature_history(feature_obj)[0]
    feature_id = feature_entry["feature_id"]
    feature_modifier = feature_obj.modifiers.get(feature_entry["modifier_name"])
    assert_true(feature_modifier is not None, "feature modifier must exist")

    driver = add_cube("OLE_BATCH_DRIVER", "OLE_BATCH_DRIVER", size=30.0, location=(-300.0, -300.0, 0.0))
    relation_driven = add_cube("OLE_BATCH_REL_DRIVEN", "OLE_BATCH_REL_DRIVEN", size=30.0, location=(0.0, -300.0, 0.0))
    relation = create_relation(scene, driver, relation_driven, "AXIS_OFFSET", axis="X", capture_current=True)
    relation_id = relation["relation_id"]

    select_only(model)
    datum = create_datum_axis(bpy.context, "X", 400.0, "WORLD_ORIGIN")
    datum_id = datum["oleander_guide_id"]

    width = create_design_parameter(scene, "BatchWidth", "LENGTH_MM", 150.0, minimum=50.0, maximum=300.0)
    depth = create_design_parameter(scene, "BatchDepth", "LENGTH_MM", 45.0, role="DERIVED", minimum=1.0, maximum=200.0)
    relation_target = create_design_parameter(scene, "BatchRelation", "LENGTH_MM", 420.0, role="DERIVED", minimum=0.0, maximum=1000.0)
    datum_length = create_design_parameter(scene, "BatchDatum", "LENGTH_MM", 700.0, minimum=10.0, maximum=2000.0)

    bind_design_parameter(scene, width["parameter_id"], "OBJECT", "OLE_BATCH_MODEL", "DIMENSION_X")
    bind_design_parameter(scene, depth["parameter_id"], "FEATURE", feature_id, "depth_mm")
    bind_design_parameter(scene, relation_target["parameter_id"], "RELATION", relation_id, "target_mm")
    bind_design_parameter(scene, datum_length["parameter_id"], "DATUM_REFERENCE", datum_id, "length_mm")

    add_parameter_dependency(scene, depth["parameter_id"], width["parameter_id"])
    add_parameter_dependency(scene, relation_target["parameter_id"], depth["parameter_id"])

    before_width = mm(model.dimensions.x)
    before_depth = mm(feature_modifier.thickness)
    before_relation = next(item for item in get_relations(scene) if item["relation_id"] == relation_id)["target_mm"]
    before_datum = float(datum["oleander_datum_length_mm"])

    preflight = preflight_design_parameter_batch(
        scene,
        [relation_target["parameter_id"], datum_length["parameter_id"]],
        include_dependencies=True,
    )
    expected_order = [width["parameter_id"], depth["parameter_id"], relation_target["parameter_id"], datum_length["parameter_id"]]
    assert_true(preflight["status"] == "PASS", "batch dry-run must pass")
    assert_true(preflight["execution_order"] == expected_order, f"dependency order mismatch: {preflight['execution_order']}")
    assert_true(preflight["parameter_count"] == 4 and preflight["binding_count"] == 4, "batch dry-run must expand upstream dependencies")
    assert_true(preflight["dry_run"] is True and preflight["geometry_mutated"] is False, "batch preflight must be mutation-free")
    assert_true(preflight["solver_claim"] is False and preflight["automatic_parameter_value_derivation"] is False, "batch preflight must deny solver/derivation authority")
    assert_true(abs(mm(model.dimensions.x) - before_width) < 1e-6, "dry-run must not mutate object")
    assert_true(abs(mm(feature_modifier.thickness) - before_depth) < 1e-6, "dry-run must not mutate feature")
    assert_true(next(item for item in get_relations(scene) if item["relation_id"] == relation_id)["target_mm"] == before_relation, "dry-run must not mutate relation")
    assert_true(float(datum["oleander_datum_length_mm"]) == before_datum, "dry-run must not mutate datum")

    downstream.oleander.stale = False
    result = apply_design_parameter_batch(
        scene,
        [relation_target["parameter_id"], datum_length["parameter_id"]],
        include_dependencies=True,
    )
    assert_true(result["status"] == "PASS", "batch apply must pass")
    assert_true(result["execution_order"] == expected_order, "batch apply must preserve dependency order")
    assert_true(result["parameter_count"] == 4 and result["binding_count"] == 4, "batch result counts must match")
    assert_true(abs(mm(model.dimensions.x) - 150.0) < 1e-4, "batch must apply object dimension")
    assert_true(abs(mm(feature_modifier.thickness) - 45.0) < 1e-4, "batch must apply feature parameter")
    relation_after = next(item for item in get_relations(scene) if item["relation_id"] == relation_id)
    assert_true(relation_after["target_mm"] == 420.0, "batch must apply relation metadata")
    assert_true(abs(float(datum["oleander_datum_length_mm"]) - 700.0) < 1e-9, "batch must apply datum metadata")
    datum_length_mm = mm((datum.data.vertices[1].co - datum.data.vertices[0].co).length)
    assert_true(abs(datum_length_mm - 700.0) < 1e-4, "batch must apply datum reference geometry")
    assert_true(downstream.oleander.stale, "batch model mutation must propagate downstream stale")
    assert_true(result["model_geometry_mutated"] is True and result["reference_geometry_mutated"] is True and result["metadata_mutated"] is True, "batch mutation classes must remain separated")
    assert_true(result["solver_claim"] is False and result["automatic_parameter_value_derivation"] is False, "batch result must preserve no-solver/no-derived-value boundary")

    last_batch = json.loads(scene.get(LAST_BATCH_APPLY_KEY, "{}"))
    assert_true(last_batch.get("status") == "PASS" and last_batch.get("batch_id") == result["batch_id"], "successful batch receipt must persist on scene")
    first_batch_id = result["batch_id"]

    # Without dependency expansion, only the explicitly requested parameter is planned.
    no_expand = preflight_design_parameter_batch(scene, [relation_target["parameter_id"]], include_dependencies=False)
    assert_true(no_expand["execution_order"] == [relation_target["parameter_id"]], "include_dependencies=false must not silently add upstream parameters")

    # Competing parameters claiming the same target field are rejected before mutation.
    collision = create_design_parameter(scene, "BatchWidthCollision", "LENGTH_MM", 175.0, minimum=50.0, maximum=300.0)
    bind_design_parameter(scene, collision["parameter_id"], "OBJECT", "OLE_BATCH_MODEL", "DIMENSION_X")
    collision_before = mm(model.dimensions.x)
    expect_value_error(
        lambda: preflight_design_parameter_batch(scene, [width["parameter_id"], collision["parameter_id"]]),
        "target collision",
    )
    assert_true(abs(mm(model.dimensions.x) - collision_before) < 1e-6, "collision preflight failure must perform zero mutation")

    expect_value_error(lambda: preflight_design_parameter_batch(scene, [width["parameter_id"], width["parameter_id"]]), "duplicate parameter IDs")
    expect_value_error(lambda: preflight_design_parameter_batch(scene, ["OLE_PARAM::P9999"]), "design parameter not found")

    # Whole-batch rollback: both a real object mutation and a real feature mutation
    # happen before a forced final-state postcheck failure.
    rollback_object = create_design_parameter(scene, "BatchRollbackObject", "LENGTH_MM", 165.0, minimum=50.0, maximum=300.0)
    rollback_feature = create_design_parameter(scene, "BatchRollbackFeature", "LENGTH_MM", 65.0, minimum=1.0, maximum=200.0)
    bind_design_parameter(scene, rollback_object["parameter_id"], "OBJECT", "OLE_BATCH_MODEL", "DIMENSION_Y")
    bind_design_parameter(scene, rollback_feature["parameter_id"], "FEATURE", feature_id, "depth_mm")
    add_parameter_dependency(scene, rollback_feature["parameter_id"], rollback_object["parameter_id"])

    rollback_y_before = mm(model.dimensions.y)
    rollback_modifier_before = float(feature_modifier.thickness)
    rollback_history_before = feature_obj.get(FEATURE_HISTORY_KEY, "")
    original_postcheck = batch_layer._postcheck_plan
    calls = {"count": 0}

    def forced_postcheck(scene_arg, parameter, plan):
        calls["count"] += 1
        if calls["count"] == 2:
            return {"status": "FAIL", "results": [], "failures": [{"forced": True}], "solver_claim": False}
        return original_postcheck(scene_arg, parameter, plan)

    try:
        batch_layer._postcheck_plan = forced_postcheck
        expect_value_error(
            lambda: apply_design_parameter_batch(scene, [rollback_feature["parameter_id"]], include_dependencies=True),
            "batch rolled back",
        )
    finally:
        batch_layer._postcheck_plan = original_postcheck

    assert_true(abs(mm(model.dimensions.y) - rollback_y_before) < 1e-4, "whole-batch rollback must restore object geometry")
    assert_true(abs(float(feature_modifier.thickness) - rollback_modifier_before) < 1e-9, "whole-batch rollback must restore modifier")
    assert_true(feature_obj.get(FEATURE_HISTORY_KEY, "") == rollback_history_before, "whole-batch rollback must restore feature history")
    rollback_receipt = json.loads(scene.get(LAST_BATCH_APPLY_KEY, "{}"))
    assert_true(rollback_receipt.get("status") == "ROLLED_BACK" and rollback_receipt.get("rollback_performed") is True, "whole-batch rollback receipt must persist")
    assert_true(rollback_receipt.get("batch_id") != first_batch_id, "batch IDs must be monotonic")

    # Failure envelope rejects the batch before mutation.
    envelope = create_design_parameter(scene, "BatchEnvelopeReject", "LENGTH_MM", 500.0, minimum=1.0, maximum=100.0)
    bind_design_parameter(scene, envelope["parameter_id"], "OBJECT", "OLE_BATCH_MODEL", "DIMENSION_Z")
    z_before = mm(model.dimensions.z)
    expect_value_error(lambda: preflight_design_parameter_batch(scene, [envelope["parameter_id"]]), "outside valid failure envelope")
    assert_true(abs(mm(model.dimensions.z) - z_before) < 1e-6, "envelope failure must perform zero target mutation")

    assert_true(hasattr(bpy.ops.oleander, "preflight_design_parameter_batch"), "batch preflight operator must register")
    assert_true(hasattr(bpy.ops.oleander, "apply_design_parameter_batch"), "batch apply operator must register")

    events = get_design_parameter_events(scene)
    commit_events = [event for event in events if event.get("action") == "BATCH_APPLY_COMMIT"]
    rollback_events = [event for event in events if event.get("action") == "BATCH_APPLY_ROLLBACK"]
    assert_true(len(commit_events) >= 4, "successful batch must create per-parameter batch commit provenance")
    assert_true(len(rollback_events) >= 2, "rolled-back batch must create per-parameter rollback provenance")
    assert_true(all(event.get("payload", {}).get("batch_id") for event in commit_events + rollback_events), "batch events must carry stable batch provenance")

    blend_path = pathlib.Path("/tmp/oleander-stage3-design-intent-batch-reopen.blend")
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    bpy.ops.wm.open_mainfile(filepath=str(blend_path))
    scene = bpy.context.scene
    reopened_model = next(obj for obj in scene.objects if getattr(getattr(obj, "oleander", None), "ole_id", "") == "OLE_BATCH_MODEL")
    reopened_feature = next(obj for obj in scene.objects if getattr(getattr(obj, "oleander", None), "ole_id", "") == "OLE_BATCH_FEATURE")
    reopened_datum = next(obj for obj in scene.objects if obj.get("oleander_guide_id", "") == datum_id)
    reopened_relation = next(item for item in get_relations(scene) if item["relation_id"] == relation_id)
    reopened_feature_entry = next(item for item in get_feature_history(reopened_feature) if item["feature_id"] == feature_id)
    reopened_modifier = reopened_feature.modifiers.get(reopened_feature_entry["modifier_name"])
    assert_true(abs(mm(reopened_model.dimensions.x) - 150.0) < 1e-4, "batch object result must survive reopen")
    assert_true(abs(mm(reopened_modifier.thickness) - 45.0) < 1e-4, "successful batch feature result must survive reopen after later rollback")
    assert_true(reopened_relation["target_mm"] == 420.0, "batch relation metadata must survive reopen")
    assert_true(abs(float(reopened_datum["oleander_datum_length_mm"]) - 700.0) < 1e-9, "batch datum result must survive reopen")
    reopened_receipt = json.loads(scene.get(LAST_BATCH_APPLY_KEY, "{}"))
    assert_true(reopened_receipt.get("status") == "ROLLED_BACK", "latest batch receipt must survive reopen")
    assert_true(any(event.get("action") == "BATCH_APPLY_COMMIT" for event in get_design_parameter_events(scene)), "batch provenance must survive reopen")

    result_payload = {
        "status": "PASS",
        "runtime": "OLEANDER Blender Runtime",
        "version": "0.2.0",
        "blender": bpy.app.version_string,
        "source_fingerprint": source_fingerprint(),
        "checks": [
            "batch_operator_registration",
            "dependency_expansion",
            "dependency_topological_order",
            "dry_run_zero_mutation",
            "atomic_cross_object_feature_relation_datum_apply",
            "final_combined_state_postcheck",
            "model_downstream_stale_propagation",
            "separated_model_reference_metadata_mutation_classes",
            "include_dependencies_false_scope",
            "target_field_collision_positive_failure",
            "duplicate_parameter_id_positive_failure",
            "missing_parameter_positive_failure",
            "whole_batch_postcheck_rollback",
            "rollback_object_geometry_restore",
            "rollback_modifier_restore",
            "rollback_feature_history_restore",
            "failure_envelope_positive_failure",
            "monotonic_batch_identity",
            "batch_commit_event_provenance",
            "batch_rollback_event_provenance",
            "blend_save_reopen_persistence",
            "no_solver_claim",
            "no_parameter_value_derivation_claim",
            "no_automatic_geometry_rebuild_claim",
            "no_cad_parametric_rebuild_claim",
        ],
        "expected_failure_checks": [
            "target_field_collision_positive_failure",
            "duplicate_parameter_id_positive_failure",
            "missing_parameter_positive_failure",
            "whole_batch_postcheck_rollback",
            "failure_envelope_positive_failure",
        ],
        "non_claims": [
            "constraint_solver",
            "equation_solver",
            "automatic_parameter_value_derivation",
            "automatic_multi_parameter_rebuild",
            "cad_parametric_feature_rebuild",
            "engineering_approval",
            "manufacturing_release",
            "field_truth",
            "constructability",
            "design_quality",
        ],
    }
    print("OLEANDER_STAGE3_DESIGN_INTENT_BATCH_VALIDATION=" + json.dumps(result_payload, sort_keys=True))


if __name__ == "__main__":
    main()
