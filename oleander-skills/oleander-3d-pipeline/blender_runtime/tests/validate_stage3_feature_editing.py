"""Real-Blender validation for governed OLEANDER feature editing.

Covers parameter edit, suppression/restoration, governed reorder, tombstone
removal, dependency-provenance cleanup, event history and save/reopen. This is
Blender-native modifier governance, not a CAD/B-Rep feature solver.
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
from oleander_blender.direct_model import _scene_units_to_mm
from oleander_blender.feature_edit import get_feature_events, get_feature_tombstones
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


def add_cube(name, ole_id, location=(0.0, 0.0, 0.0), size=500.0):
    bpy.ops.mesh.primitive_cube_add(size=size, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.oleander.ole_id = ole_id
    return obj


def add_plane(name, ole_id, location=(0.0, 0.0, 0.0), size=1000.0):
    bpy.ops.mesh.primitive_plane_add(size=size, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.oleander.ole_id = ole_id
    return obj


def feature_by_kind(obj, kind):
    for entry in get_feature_history(obj):
        if entry.get("kind") == kind:
            return entry
    return None


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

    obj = add_plane("OLE_FEATURE_EDIT_MAIN", "OLE_FEATURE_EDIT_MAIN")
    downstream = add_cube("OLE_FEATURE_EDIT_DOWNSTREAM", "OLE_FEATURE_EDIT_DOWNSTREAM", location=(3000.0, 0.0, 0.0))
    downstream.oleander.dependencies = "OLE_FEATURE_EDIT_MAIN"
    downstream.oleander.stale = False

    select_only(obj)
    assert_true("FINISHED" in bpy.ops.oleander.add_planar_extrude(depth_mm=30.0), "base planar extrude must finish")
    assert_true("FINISHED" in bpy.ops.oleander.add_bevel_chamfer(width_mm=3.0, segments=1), "base bevel must finish")
    assert_true("FINISHED" in bpy.ops.oleander.add_linear_pattern(count=3, spacing_mm=200.0, axis="X"), "base linear pattern must finish")
    history = get_feature_history(obj)
    assert_true(len(history) == 3, "editing fixture must begin with three governed features")
    extrude_id, bevel_id, pattern_id = [entry["feature_id"] for entry in history]

    clear_stale(downstream)
    edit = bpy.ops.oleander.edit_feature_parameters(
        feature_id=pattern_id,
        value_mm=180.0,
        count=5,
        axis="Z",
    )
    assert_true("FINISHED" in edit, "stable-ID feature parameter edit must finish")
    pattern = next(entry for entry in get_feature_history(obj) if entry["feature_id"] == pattern_id)
    modifier = obj.modifiers.get(pattern["modifier_name"])
    assert_true(modifier is not None and modifier.type == "ARRAY", "edited pattern must retain Array modifier identity")
    assert_true(modifier.count == 5, "edited pattern count must reach real modifier")
    assert_true(abs(_scene_units_to_mm(bpy.context, modifier.constant_offset_displace.z) - 180.0) <= 1e-3, "edited pattern metric spacing must reach real modifier")
    assert_true(pattern.get("edit_revision") == 1, "feature edit revision must increment")
    assert_true(pattern["parameters"]["axis"] == "Z", "feature history must capture edited axis")
    assert_true(downstream.oleander.stale, "feature parameter edit must stale downstream objects")

    clear_stale(downstream)
    suppressed = bpy.ops.oleander.set_feature_suppressed(feature_id=pattern_id, state="SUPPRESS")
    assert_true("FINISHED" in suppressed, "feature suppression must finish")
    pattern = next(entry for entry in get_feature_history(obj) if entry["feature_id"] == pattern_id)
    modifier = obj.modifiers.get(pattern["modifier_name"])
    assert_true(pattern.get("suppressed") is True, "feature history must record suppression")
    assert_true(not modifier.show_viewport and not modifier.show_render, "suppression must disable modifier evaluation surfaces")
    assert_true(validate_feature_history(obj)["status"] == "PASS", "suppressed stack must still validate when history and modifier agree")
    assert_true(downstream.oleander.stale, "feature suppression must stale downstream objects")

    clear_stale(downstream)
    restored = bpy.ops.oleander.set_feature_suppressed(feature_id=pattern_id, state="RESTORE")
    assert_true("FINISHED" in restored, "feature restore must finish")
    pattern = next(entry for entry in get_feature_history(obj) if entry["feature_id"] == pattern_id)
    modifier = obj.modifiers.get(pattern["modifier_name"])
    assert_true(pattern.get("suppressed") is False and modifier.show_viewport and modifier.show_render, "restore must synchronize history and modifier visibility")
    assert_true(validate_feature_history(obj)["status"] == "PASS", "restored stack must validate")

    # Governed reorder must update both Blender modifier order and recorded history,
    # unlike the manual-drift failure gate tested in validate_stage3_features.py.
    reordered = bpy.ops.oleander.move_feature(feature_id=pattern_id, direction="UP")
    assert_true("FINISHED" in reordered, "governed feature reorder must finish")
    reordered_history = get_feature_history(obj)
    assert_true([entry["feature_id"] for entry in reordered_history] == [extrude_id, pattern_id, bevel_id], "governed reorder must rewrite active history order to match modifier stack")
    assert_true([entry["stack_index"] for entry in reordered_history] == [0, 1, 2], "governed reorder must normalize recorded stack indices")
    assert_true(validate_feature_history(obj)["status"] == "PASS", "governed reorder must preserve feature-stack PASS")

    removed = bpy.ops.oleander.remove_feature(feature_id=bevel_id)
    assert_true("FINISHED" in removed, "feature removal must finish")
    assert_true(all(entry["feature_id"] != bevel_id for entry in get_feature_history(obj)), "removed feature must leave active feature history")
    tombstones = get_feature_tombstones(obj)
    assert_true(len(tombstones) == 1 and tombstones[0]["feature"]["feature_id"] == bevel_id, "removed feature must be preserved as tombstone")
    assert_true(tombstones[0]["feature"]["kind"] == "BEVEL_CHAMFER", "tombstone must preserve removed feature semantics")
    assert_true(validate_feature_history(obj)["status"] == "PASS", "stack must validate after governed tombstone removal")

    # Boolean dependency added by the feature may be removed when the feature is
    # removed and no remaining feature uses that source.
    boolean_target = add_cube("OLE_EDIT_BOOL_ADDED_TARGET", "OLE_EDIT_BOOL_ADDED_TARGET", location=(6000.0, 0.0, 0.0), size=1000.0)
    cutter_added = add_cube("OLE_EDIT_BOOL_ADDED_CUTTER", "OLE_EDIT_BOOL_ADDED_CUTTER", location=(6250.0, 0.0, 0.0), size=700.0)
    select_boolean(boolean_target, cutter_added)
    assert_true("FINISHED" in bpy.ops.oleander.add_boolean(operation="DIFFERENCE"), "Boolean fixture with feature-added dependency must finish")
    bool_entry = feature_by_kind(boolean_target, "BOOLEAN_DIFFERENCE")
    assert_true(bool_entry["parameters"].get("dependency_added_by_feature") is True, "Boolean history must prove when dependency was added by feature")
    assert_true("OLE_EDIT_BOOL_ADDED_CUTTER" in dependency_ids(boolean_target), "Boolean feature must create cutter dependency")
    select_only(boolean_target)
    assert_true("FINISHED" in bpy.ops.oleander.remove_feature(feature_id=bool_entry["feature_id"]), "Boolean feature removal must finish")
    assert_true("OLE_EDIT_BOOL_ADDED_CUTTER" not in dependency_ids(boolean_target), "feature-owned cutter dependency must be cleaned after Boolean removal")
    bool_tombstone = get_feature_tombstones(boolean_target)[0]
    assert_true(bool_tombstone["removed_dependencies"] == ["OLE_EDIT_BOOL_ADDED_CUTTER"], "Boolean tombstone must record removed feature-owned dependency")

    # A pre-existing dependency must never be removed just because a Boolean uses it.
    preserved_target = add_cube("OLE_EDIT_BOOL_PRESERVE_TARGET", "OLE_EDIT_BOOL_PRESERVE_TARGET", location=(9000.0, 0.0, 0.0), size=1000.0)
    cutter_preserved = add_cube("OLE_EDIT_BOOL_PRESERVE_CUTTER", "OLE_EDIT_BOOL_PRESERVE_CUTTER", location=(9250.0, 0.0, 0.0), size=700.0)
    preserved_target.oleander.dependencies = "OLE_EDIT_BOOL_PRESERVE_CUTTER"
    select_boolean(preserved_target, cutter_preserved)
    assert_true("FINISHED" in bpy.ops.oleander.add_boolean(operation="UNION"), "Boolean fixture with pre-existing dependency must finish")
    preserve_entry = feature_by_kind(preserved_target, "BOOLEAN_UNION")
    assert_true(preserve_entry["parameters"].get("dependency_added_by_feature") is False, "Boolean history must prove pre-existing dependency ownership")
    select_only(preserved_target)
    assert_true("FINISHED" in bpy.ops.oleander.remove_feature(feature_id=preserve_entry["feature_id"]), "Boolean with pre-existing dependency must remove feature")
    assert_true("OLE_EDIT_BOOL_PRESERVE_CUTTER" in dependency_ids(preserved_target), "pre-existing dependency must survive Boolean feature removal")
    preserve_tombstone = get_feature_tombstones(preserved_target)[0]
    assert_true(preserve_tombstone["removed_dependencies"] == [], "tombstone must show no pre-existing dependency was deleted")

    # Positive failure: unknown stable feature IDs must reject rather than mutate
    # the last/nearest modifier by accident.
    select_only(obj)
    missing_feature_failure = False
    try:
        bpy.ops.oleander.edit_feature_parameters(feature_id="OLE_FEATURE_EDIT_MAIN::F999", value_mm=99.0)
    except RuntimeError as exc:
        missing_feature_failure = "OLEANDER feature not found" in str(exc)
    assert_true(missing_feature_failure, "unknown feature ID must produce explicit expected failure")

    events = get_feature_events(obj)
    actions = [event["action"] for event in events]
    assert_true(actions == ["EDIT", "SUPPRESS", "RESTORE", "REORDER", "REMOVE"], f"feature event log must preserve deterministic mutation order; got {actions!r}")
    assert_true([event["event_index"] for event in events] == [1, 2, 3, 4, 5], "feature event indices must be monotonic")

    reopen_path = "/tmp/oleander-stage3-feature-editing-reopen.blend"
    bpy.ops.wm.save_as_mainfile(filepath=reopen_path)
    bpy.ops.wm.open_mainfile(filepath=reopen_path)

    reopened = bpy.data.objects.get("OLE_FEATURE_EDIT_MAIN")
    reopened_boolean = bpy.data.objects.get("OLE_EDIT_BOOL_ADDED_TARGET")
    reopened_preserved = bpy.data.objects.get("OLE_EDIT_BOOL_PRESERVE_TARGET")
    assert_true(reopened is not None and reopened_boolean is not None and reopened_preserved is not None, "feature-edit fixtures must survive save/reopen")
    assert_true(validate_feature_history(reopened)["status"] == "PASS", "edited feature stack must validate after reopen")
    assert_true(len(get_feature_tombstones(reopened)) == 1, "feature tombstones must survive save/reopen")
    assert_true(len(get_feature_events(reopened)) == 5, "feature event log must survive save/reopen")
    assert_true("OLE_EDIT_BOOL_ADDED_CUTTER" not in dependency_ids(reopened_boolean), "feature-owned dependency cleanup must persist after reopen")
    assert_true("OLE_EDIT_BOOL_PRESERVE_CUTTER" in dependency_ids(reopened_preserved), "pre-existing dependency preservation must persist after reopen")

    result = {
        "runtime": "OLEANDER Blender Runtime",
        "stage": "STAGE3_FEATURE_EDITING",
        "version": "0.2.0",
        "blender": bpy.app.version_string,
        "status": "PASS",
        "source_fingerprint_sha256": source_fingerprint(),
        "checks": [
            "stable_feature_id_parameter_edit",
            "feature_parameter_edit_hits_real_modifier",
            "feature_edit_revision_increment",
            "feature_edit_downstream_stale_propagation",
            "feature_suppress_restore",
            "feature_suppression_history_modifier_sync",
            "governed_feature_reorder",
            "governed_reorder_history_order_sync",
            "feature_remove_tombstone",
            "feature_event_log_monotonic",
            "boolean_dependency_added_by_feature_provenance",
            "boolean_feature_owned_dependency_cleanup",
            "boolean_preexisting_dependency_preservation",
            "unknown_feature_id_expected_failure",
            "feature_edit_save_reopen_persistence",
            "tombstone_save_reopen_persistence",
            "event_log_save_reopen_persistence",
        ],
        "expected_failure_cases": {
            "unknown_feature_id": "PASS"
        },
        "non_claims": [
            "cad_brep",
            "feature_solver",
            "solver_backed_constraints",
            "class_a_surface",
            "field_truth",
            "engineering_approval",
            "manufacturing_release",
            "constructability",
            "design_quality",
        ],
    }
    print("OLEANDER_STAGE3_FEATURE_EDITING_VALIDATION=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
