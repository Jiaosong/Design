"""Real-Blender validation for OLEANDER Design Intent Rebuild Plan foundation."""

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
from oleander_blender.design_intent import (
    add_parameter_dependency,
    bind_design_parameter,
    create_design_parameter,
    update_design_parameter,
)
from oleander_blender.design_intent_batch import apply_design_parameter_batch
from oleander_blender.design_intent_rebuild import (
    LAST_REBUILD_PLAN_KEY,
    LAST_REBUILD_RESULT_KEY,
    build_design_intent_rebuild_plan,
    execute_design_intent_rebuild_plan,
    infer_dirty_design_parameters,
    store_design_intent_rebuild_plan,
)
from oleander_blender.direct_model import _scene_units_to_mm


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


def add_cube(name, oid, location):
    bpy.ops.mesh.primitive_cube_add(size=100.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    set_metadata(obj, oid)
    return obj


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

    object_a = add_cube("OLE_REBUILD_A", "OLE_REBUILD_A", (0.0, 0.0, 0.0))
    object_b = add_cube("OLE_REBUILD_B", "OLE_REBUILD_B", (400.0, 0.0, 0.0))
    object_c = add_cube("OLE_REBUILD_C", "OLE_REBUILD_C", (800.0, 0.0, 0.0))
    object_b.oleander.dependencies = "OLE_REBUILD_A"
    object_c.oleander.dependencies = "OLE_REBUILD_B"

    parameter_a = create_design_parameter(scene, "RebuildA", "LENGTH_MM", 120.0, minimum=10.0, maximum=500.0)
    parameter_b = create_design_parameter(scene, "RebuildB", "LENGTH_MM", 130.0, role="DERIVED", minimum=10.0, maximum=500.0)
    parameter_c = create_design_parameter(scene, "RebuildC", "LENGTH_MM", 140.0, role="DERIVED", minimum=10.0, maximum=500.0)

    bind_design_parameter(scene, parameter_a["parameter_id"], "OBJECT", "OLE_REBUILD_A", "DIMENSION_X")
    bind_design_parameter(scene, parameter_b["parameter_id"], "OBJECT", "OLE_REBUILD_B", "DIMENSION_X")
    bind_design_parameter(scene, parameter_c["parameter_id"], "OBJECT", "OLE_REBUILD_C", "DIMENSION_X")
    add_parameter_dependency(scene, parameter_b["parameter_id"], parameter_a["parameter_id"])
    add_parameter_dependency(scene, parameter_c["parameter_id"], parameter_b["parameter_id"])

    # Establish a clean applied baseline so the later dirty inference is isolated.
    baseline = apply_design_parameter_batch(
        scene,
        [parameter_a["parameter_id"], parameter_b["parameter_id"], parameter_c["parameter_id"]],
        include_dependencies=False,
    )
    assert_true(baseline["status"] == "PASS", "baseline batch must pass")
    assert_true(infer_dirty_design_parameters(scene) == [], "baseline batch commits must clean parameter-event dirtiness")

    before_a = mm(object_a.dimensions.x)
    before_b = mm(object_b.dimensions.x)
    before_c = mm(object_c.dimensions.x)
    update_design_parameter(scene, parameter_a["parameter_id"], 155.0)

    dirty = infer_dirty_design_parameters(scene)
    assert_true([item["parameter_id"] for item in dirty] == [parameter_a["parameter_id"]], "dirty inference must identify only the directly changed seed")

    plan = build_design_intent_rebuild_plan(scene)
    expected_order = [parameter_a["parameter_id"], parameter_b["parameter_id"], parameter_c["parameter_id"]]
    assert_true(plan["status"] == "PASS", "inferred rebuild plan must pass")
    assert_true(plan["seed_mode"] == "INFERRED_DIRTY", "blank seed mode must infer dirty parameters")
    assert_true(plan["seed_parameter_ids"] == [parameter_a["parameter_id"]], "dirty seed must remain minimal")
    assert_true(plan["execution_order"] == expected_order, f"downstream parameter closure/order mismatch: {plan['execution_order']}")
    assert_true(plan["expanded_downstream_parameter_ids"] == [parameter_b["parameter_id"], parameter_c["parameter_id"]], "rebuild plan must expand downstream dependents only")
    assert_true(parameter_a["parameter_id"] not in plan["expanded_downstream_parameter_ids"], "seed must not be mislabeled as downstream expansion")
    assert_true(plan["impact"]["direct_object_ids"] == ["OLE_REBUILD_A", "OLE_REBUILD_B", "OLE_REBUILD_C"], "impact preview must resolve bound object IDs")
    assert_true(plan["impact"]["downstream_object_ids"] == [], "selected direct objects already cover the full object dependency chain")
    assert_true(plan["geometry_mutated"] is False and plan["automatic_execution"] is False, "planning must be mutation-free and non-automatic")
    assert_true(plan["solver_claim"] is False and plan["automatic_parameter_value_derivation"] is False, "planning must deny solver/value-derivation authority")
    assert_true(abs(mm(object_a.dimensions.x) - before_a) < 1e-6, "plan build must not mutate changed target geometry")
    assert_true(abs(mm(object_b.dimensions.x) - before_b) < 1e-6, "plan build must not mutate downstream target geometry")
    assert_true(abs(mm(object_c.dimensions.x) - before_c) < 1e-6, "plan build must not mutate downstream target geometry")

    store_design_intent_rebuild_plan(scene, plan)
    stored = json.loads(scene.get(LAST_REBUILD_PLAN_KEY, "{}"))
    assert_true(stored.get("plan_sha256") == plan["plan_sha256"], "stored plan must preserve deterministic plan identity")

    # A stored plan must survive save/reopen and remain executable when its event
    # watermark and selected parameter state have not changed.
    blend_path = pathlib.Path("/tmp/oleander-stage3-design-intent-rebuild-reopen.blend")
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    bpy.ops.wm.open_mainfile(filepath=str(blend_path))
    scene = bpy.context.scene
    reopened_plan = json.loads(scene.get(LAST_REBUILD_PLAN_KEY, "{}"))
    assert_true(reopened_plan.get("plan_sha256") == plan["plan_sha256"], "rebuild plan must persist through blend reopen")
    result = execute_design_intent_rebuild_plan(scene)
    assert_true(result["status"] == "PASS", "stored fresh rebuild plan must execute")
    assert_true(result["execution_order"] == expected_order, "rebuild execution order must match locked plan")
    assert_true(result["explicit_execution"] is True and result["solver_claim"] is False, "rebuild execution must remain explicit/no-solver")

    object_a = scene.objects["OLE_REBUILD_A"]
    object_b = scene.objects["OLE_REBUILD_B"]
    object_c = scene.objects["OLE_REBUILD_C"]
    assert_true(abs(mm(object_a.dimensions.x) - 155.0) < 1e-4, "rebuild execution must apply changed seed value")
    assert_true(abs(mm(object_b.dimensions.x) - 130.0) < 1e-4, "rebuild execution must reapply downstream stored value without deriving it")
    assert_true(abs(mm(object_c.dimensions.x) - 140.0) < 1e-4, "rebuild execution must reapply downstream stored value without deriving it")
    last_result = json.loads(scene.get(LAST_REBUILD_RESULT_KEY, "{}"))
    assert_true(last_result.get("status") == "PASS" and last_result.get("plan_sha256") == plan["plan_sha256"], "rebuild result receipt must persist")
    assert_true(infer_dirty_design_parameters(scene) == [], "successful rebuild batch commits must clear inferred parameter dirtiness")

    clean = build_design_intent_rebuild_plan(scene)
    assert_true(clean["status"] == "CLEAN" and clean["parameter_count"] == 0, "clean graph must produce an explicit no-op plan")

    # Explicit seeds use downstream closure only. A clean upstream must not be
    # pulled back into a minimal rebuild set.
    explicit = build_design_intent_rebuild_plan(scene, [parameter_b["parameter_id"]])
    assert_true(explicit["execution_order"] == [parameter_b["parameter_id"], parameter_c["parameter_id"]], "explicit mid-graph seed must not pull clean upstream parameter")
    assert_true(parameter_a["parameter_id"] not in explicit["execution_order"], "minimal downstream rebuild must exclude clean upstream parameter")

    expect_value_error(
        lambda: build_design_intent_rebuild_plan(scene, [parameter_b["parameter_id"], parameter_b["parameter_id"]]),
        "duplicate seed parameter IDs",
    )
    expect_value_error(lambda: build_design_intent_rebuild_plan(scene, ["OLE_PARAM::P9999"]), "design parameter not found")

    # Plan freshness is locked to event watermark + selected parameter revisions/state.
    update_design_parameter(scene, parameter_a["parameter_id"], 165.0)
    stale_plan = build_design_intent_rebuild_plan(scene)
    store_design_intent_rebuild_plan(scene, stale_plan)
    stale_geometry_before = mm(scene.objects["OLE_REBUILD_A"].dimensions.x)
    update_design_parameter(scene, parameter_a["parameter_id"], 175.0)
    expect_value_error(lambda: execute_design_intent_rebuild_plan(scene, stale_plan), "rebuild plan is stale")
    assert_true(abs(mm(scene.objects["OLE_REBUILD_A"].dimensions.x) - stale_geometry_before) < 1e-6, "stale-plan rejection must perform zero geometry mutation")

    # Direct stale markers are also valid dirty evidence even without a newer
    # parameter mutation event, preserving existing single-authority stale state.
    fresh_all = apply_design_parameter_batch(
        scene,
        [parameter_a["parameter_id"], parameter_b["parameter_id"], parameter_c["parameter_id"]],
        include_dependencies=False,
    )
    assert_true(fresh_all["status"] == "PASS", "cleanup batch must pass")
    scene.objects["OLE_REBUILD_B"]["oleander_design_intent_stale"] = True
    marker_dirty = infer_dirty_design_parameters(scene)
    assert_true([item["parameter_id"] for item in marker_dirty] == [parameter_b["parameter_id"]], "direct stale marker must seed its bound parameter")
    marker_plan = build_design_intent_rebuild_plan(scene)
    assert_true(marker_plan["execution_order"] == [parameter_b["parameter_id"], parameter_c["parameter_id"]], "direct stale marker must expand downstream parameter dependents")

    assert_true(hasattr(bpy.ops.oleander, "build_design_intent_rebuild_plan"), "rebuild-plan build operator must register")
    assert_true(hasattr(bpy.ops.oleander, "execute_design_intent_rebuild_plan"), "rebuild-plan execute operator must register")

    checks = [
        "rebuild_plan_operator_registration",
        "event_log_dirty_seed_inference",
        "direct_stale_marker_dirty_seed_inference",
        "minimal_dirty_seed_set",
        "downstream_parameter_dependency_closure",
        "selected_dependency_topological_order",
        "no_clean_upstream_expansion",
        "non_mutating_rebuild_plan",
        "impact_preview_bound_object_ids",
        "deterministic_plan_sha256",
        "event_watermark_lock",
        "parameter_revision_state_lock",
        "stale_plan_positive_failure",
        "stale_plan_failure_zero_geometry_mutation",
        "duplicate_seed_positive_failure",
        "missing_seed_positive_failure",
        "stored_plan_save_reopen_persistence",
        "explicit_rebuild_execution_via_atomic_batch",
        "downstream_stored_value_reapply_without_derivation",
        "successful_rebuild_cleans_event_dirtiness",
        "clean_graph_noop_plan",
        "rebuild_result_receipt_persistence",
        "no_solver_claim",
        "no_automatic_execution_claim",
        "no_parameter_value_derivation_claim",
        "no_automatic_geometry_rebuild_claim",
        "no_cad_parametric_rebuild_claim",
    ]
    payload = {
        "runtime": "OLEANDER Blender Runtime",
        "version": "0.2.0",
        "blender": bpy.app.version_string,
        "stage": "STAGE3_DESIGN_INTENT_REBUILD_PLAN_FOUNDATION",
        "status": "PASS",
        "checks": checks,
        "expected_failure_checks": [
            "stale_plan_positive_failure",
            "duplicate_seed_positive_failure",
            "missing_seed_positive_failure",
        ],
        "non_claims": [
            "constraint_solver",
            "equation_solver",
            "automatic_parameter_value_derivation",
            "automatic_rebuild_execution",
            "automatic_parameter_geometry_rebuild",
            "cad_parametric_feature_rebuild",
            "engineering_approval",
            "manufacturing_release",
            "field_truth",
            "constructability",
            "design_quality",
        ],
        "source_fingerprint": source_fingerprint(),
    }
    print("OLEANDER_STAGE3_DESIGN_INTENT_REBUILD_VALIDATION=" + json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
