"""Headless validation for OLEANDER Blender Runtime Stage 3 Direct Feature Stack.

This validates governed Blender-native non-destructive modifier features and
feature-history integrity in a real Blender 5.1+ process. It does not claim
CAD/B-Rep, solver-backed constraints, engineering, manufacturing, field,
constructability, or design authority.
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
from oleander_blender.dependency import clear_stale, mark_downstream_stale
from oleander_blender.direct_model import _scene_units_to_mm
from oleander_blender.feature_stack import get_feature_history, validate_feature_history


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


def select_only(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def select_boolean(target, cutter):
    bpy.ops.object.select_all(action="DESELECT")
    target.select_set(True)
    cutter.select_set(True)
    bpy.context.view_layer.objects.active = target


def add_cube(name, ole_id, location=(0.0, 0.0, 0.0), size=1000.0):
    bpy.ops.mesh.primitive_cube_add(size=size, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.oleander.ole_id = ole_id
    return obj


def add_plane(name, ole_id, size=1000.0):
    bpy.ops.mesh.primitive_plane_add(size=size)
    obj = bpy.context.active_object
    obj.name = name
    obj.oleander.ole_id = ole_id
    return obj


def evaluated_vertex_count(obj):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    try:
        return len(mesh.vertices)
    finally:
        evaluated.to_mesh_clear()


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

    planar = add_plane("OLE_STAGE3_FEATURE_PLANAR", "OLE_STAGE3_FEATURE_PLANAR")
    dependent = add_cube(
        "OLE_STAGE3_FEATURE_DEPENDENT",
        "OLE_STAGE3_FEATURE_DEPENDENT",
        location=(3000.0, 0.0, 0.0),
        size=250.0,
    )
    dependent.oleander.dependencies = "OLE_STAGE3_FEATURE_PLANAR"
    dependent.oleander.stale = False

    select_only(planar)
    extrude = bpy.ops.oleander.add_planar_extrude(depth_mm=40.0)
    assert_true("FINISHED" in extrude, "planar extrude must finish on a planar mesh")
    bpy.context.view_layer.update()
    history = get_feature_history(planar)
    assert_true(len(history) == 1 and history[0]["kind"] == "PLANAR_EXTRUDE", "planar extrude must create first governed feature")
    extrude_modifier = planar.modifiers.get(history[0]["modifier_name"])
    assert_true(extrude_modifier is not None and extrude_modifier.type == "SOLIDIFY", "planar extrude must remain an editable Solidify modifier")
    assert_true(
        abs(_scene_units_to_mm(bpy.context, extrude_modifier.thickness) - 40.0) <= 1e-3,
        "planar extrude modifier thickness must preserve requested millimetres",
    )
    assert_true(evaluated_vertex_count(planar) > len(planar.data.vertices), "planar extrude must change evaluated geometry without applying the source mesh")
    assert_true(dependent.oleander.stale, "adding a direct feature must stale declared downstream objects")

    clear_stale(dependent)
    select_only(planar)
    bevel = bpy.ops.oleander.add_bevel_chamfer(width_mm=5.0, segments=2)
    mirror = bpy.ops.oleander.add_mirror(axis="X", merge=True)
    pattern = bpy.ops.oleander.add_linear_pattern(count=4, spacing_mm=250.0, axis="Y")
    assert_true(all("FINISHED" in result for result in (bevel, mirror, pattern)), "bevel, mirror, and linear pattern operators must finish")

    history = get_feature_history(planar)
    assert_true(
        [entry["kind"] for entry in history] == ["PLANAR_EXTRUDE", "BEVEL_CHAMFER", "MIRROR", "LINEAR_PATTERN"],
        f"feature history must preserve deterministic feature order; got {[entry['kind'] for entry in history]!r}",
    )
    assert_true(validate_feature_history(planar)["status"] == "PASS", "recorded feature stack must initially match Blender modifier stack")

    pattern_modifier = planar.modifiers.get(history[-1]["modifier_name"])
    assert_true(pattern_modifier is not None and pattern_modifier.type == "ARRAY", "linear pattern must use editable Array modifier")
    assert_true(pattern_modifier.count == 4, "linear pattern count must be retained")
    assert_true(
        abs(_scene_units_to_mm(bpy.context, pattern_modifier.constant_offset_displace.y) - 250.0) <= 1e-3,
        "linear pattern spacing must preserve requested millimetres",
    )

    # Positive failure: modifier order drift must be detected rather than silently
    # rewriting the feature history to match a manually reordered Blender stack.
    planar.modifiers.move(0, 1)
    drift = validate_feature_history(planar)
    assert_true(drift["status"] == "FAIL" and drift["order_drift"], "manual modifier reorder must trigger feature-history order drift")
    planar.modifiers.move(1, 0)
    assert_true(validate_feature_history(planar)["status"] == "PASS", "restoring modifier order must restore feature-stack PASS")

    nonplanar = add_cube("OLE_STAGE3_FEATURE_NONPLANAR", "OLE_STAGE3_FEATURE_NONPLANAR", location=(6000.0, 0.0, 0.0), size=500.0)
    select_only(nonplanar)
    invalid_extrude = bpy.ops.oleander.add_planar_extrude(depth_mm=20.0)
    assert_true("CANCELLED" in invalid_extrude, "Planar Extrude must explicitly reject non-planar source meshes")
    assert_true(not get_feature_history(nonplanar), "failed Planar Extrude must not pollute feature history")

    shell_obj = add_cube("OLE_STAGE3_FEATURE_SHELL", "OLE_STAGE3_FEATURE_SHELL", location=(9000.0, 0.0, 0.0), size=500.0)
    select_only(shell_obj)
    shell = bpy.ops.oleander.add_shell(thickness_mm=8.0, offset_mode="INSIDE")
    assert_true("FINISHED" in shell, "Shell operator must finish")
    shell_history = get_feature_history(shell_obj)
    assert_true(len(shell_history) == 1 and shell_history[0]["kind"] == "SHELL", "Shell must create governed feature history")
    shell_modifier = shell_obj.modifiers.get(shell_history[0]["modifier_name"])
    assert_true(shell_modifier is not None and shell_modifier.type == "SOLIDIFY", "Shell must remain an editable Solidify modifier")

    boolean_base = add_cube("OLE_STAGE3_FEATURE_BOOLEAN_BASE", "OLE_STAGE3_FEATURE_BOOLEAN_BASE", location=(12000.0, 0.0, 0.0), size=1000.0)
    cutter = add_cube("OLE_STAGE3_FEATURE_BOOLEAN_CUTTER", "OLE_STAGE3_FEATURE_BOOLEAN_CUTTER", location=(12250.0, 0.0, 0.0), size=750.0)
    select_boolean(boolean_base, cutter)
    boolean_result = bpy.ops.oleander.add_boolean(operation="DIFFERENCE")
    assert_true("FINISHED" in boolean_result, "Boolean feature operator must finish with one governed cutter")
    boolean_history = get_feature_history(boolean_base)
    assert_true(len(boolean_history) == 1 and boolean_history[0]["kind"] == "BOOLEAN_DIFFERENCE", "Boolean must create governed feature record")
    boolean_modifier = boolean_base.modifiers.get(boolean_history[0]["modifier_name"])
    assert_true(boolean_modifier is not None and boolean_modifier.type == "BOOLEAN", "Boolean must remain an editable Boolean modifier")
    assert_true(boolean_modifier.object is cutter, "Boolean modifier must bind the declared cutter object")
    assert_true(
        "OLE_STAGE3_FEATURE_BOOLEAN_CUTTER" in boolean_base.oleander.dependencies,
        "Boolean cutter OLE ID must be promoted into the object dependency graph",
    )
    assert_true(
        boolean_history[0]["source_ids"] == ["OLE_STAGE3_FEATURE_BOOLEAN_CUTTER"],
        "Boolean feature history must preserve stable cutter OLE ID provenance",
    )

    clear_stale(boolean_base)
    changed = mark_downstream_stale(["OLE_STAGE3_FEATURE_BOOLEAN_CUTTER"], reason="BOOLEAN_CUTTER_CHANGED", scene=scene)
    assert_true("OLE_STAGE3_FEATURE_BOOLEAN_BASE" in changed, "cutter change must propagate stale state to Boolean target through dependency graph")
    assert_true(boolean_base.oleander.stale, "Boolean target must be stale after governed cutter change")
    assert_true(validate_feature_history(boolean_base)["status"] == "PASS", "Boolean feature history must match Blender modifier stack")

    reopen_path = "/tmp/oleander-stage3-features-reopen.blend"
    bpy.ops.wm.save_as_mainfile(filepath=reopen_path)
    bpy.ops.wm.open_mainfile(filepath=reopen_path)

    reopened_planar = bpy.data.objects.get("OLE_STAGE3_FEATURE_PLANAR")
    reopened_boolean = bpy.data.objects.get("OLE_STAGE3_FEATURE_BOOLEAN_BASE")
    assert_true(reopened_planar is not None and reopened_boolean is not None, "feature-stack objects must survive .blend save/reopen")
    assert_true(len(get_feature_history(reopened_planar)) == 4, "direct feature history must survive .blend save/reopen")
    assert_true(validate_feature_history(reopened_planar)["status"] == "PASS", "reopened direct feature stack must validate")
    assert_true(validate_feature_history(reopened_boolean)["status"] == "PASS", "reopened Boolean feature stack must validate")

    result = {
        "runtime": "OLEANDER Blender Runtime",
        "stage": "STAGE3_DIRECT_FEATURE_STACK",
        "version": "0.2.0",
        "blender": bpy.app.version_string,
        "status": "PASS",
        "source_fingerprint_sha256": source_fingerprint(),
        "checks": [
            "planar_extrude_modifier_feature",
            "planar_extrude_metric_depth",
            "planar_extrude_evaluated_geometry",
            "nonplanar_extrude_expected_failure",
            "shell_modifier_feature",
            "bevel_chamfer_modifier_feature",
            "mirror_modifier_feature",
            "linear_pattern_modifier_feature",
            "linear_pattern_metric_spacing",
            "feature_history_stable_ids_and_order",
            "feature_stack_order_drift_expected_failure",
            "feature_geometry_change_stale_propagation",
            "boolean_modifier_feature",
            "boolean_cutter_ole_provenance",
            "boolean_dependency_graph_binding",
            "boolean_cutter_change_stale_propagation",
            "feature_stack_save_reopen_persistence",
        ],
        "expected_failure_cases": {
            "nonplanar_planar_extrude": "PASS",
            "manual_modifier_order_drift": "PASS",
        },
        "non_claims": [
            "cad_brep",
            "solver_backed_constraints",
            "feature_solver",
            "class_a_surface",
            "field_truth",
            "engineering_approval",
            "manufacturing_release",
            "constructability",
            "design_quality",
        ],
    }
    print("OLEANDER_STAGE3_FEATURES_VALIDATION=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
