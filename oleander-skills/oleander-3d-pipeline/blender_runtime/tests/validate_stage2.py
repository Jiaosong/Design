"""Headless validation for OLEANDER Blender Runtime Stage 2.

Run from a Blender 5.1+ build, from repository root or with an absolute script path:

    blender --background --factory-startup --python \
      oleander-skills/oleander-3d-pipeline/blender_runtime/tests/validate_stage2.py

This validation checks runtime mechanics only. It does not prove field truth,
engineering approval, manufacturing release, constructability or design quality.
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
from oleander_blender.audit import audit_scene
from oleander_blender.bom import build_bom
from oleander_blender.configuration import capture_configuration, configuration_names, restore_configuration
from oleander_blender.dependency import build_dependency_graph, detect_cycles, mark_downstream_stale
from oleander_blender.direct_model import _mm_to_scene_units, _scene_units_to_mm
from oleander_blender.geometry_diff import diff_from_baseline, store_baseline
from oleander_blender.review_state import summarize_object_state


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def runtime_source_fingerprint():
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


def add_cube(name, location=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj


def find_by_ole_id(scene, ole_id):
    for obj in scene.objects:
        if getattr(obj, "oleander", None) and obj.oleander.ole_id == ole_id:
            return obj
    return None


def delete_objects(objects):
    for obj in objects:
        if obj and obj.name in bpy.data.objects:
            bpy.data.objects.remove(obj, do_unlink=True)


def run_expected_failure_cases(scene):
    """Prove invalid governed states fail visibly in a real Blender process."""
    results = {}

    # 1) Duplicate OLE IDs must be detected, then the repair operator must make
    # the selected pair unique without silently accepting the collision.
    dup_a = add_cube("OLE_FAIL_DUP_A", location=(10.0, 0.0, 0.0))
    dup_b = add_cube("OLE_FAIL_DUP_B", location=(12.0, 0.0, 0.0))
    dup_a.oleander.ole_id = "OLE_DUPLICATE_EXPECTED_FAIL"
    dup_b.oleander.ole_id = "OLE_DUPLICATE_EXPECTED_FAIL"
    duplicate_audit = audit_scene(scene)
    assert_true(
        "OLE_DUPLICATE_EXPECTED_FAIL" in duplicate_audit["duplicate_ole_ids"],
        "duplicate OLE ID fixture must be detected",
    )
    duplicate_issue_count = sum(
        1 for item in duplicate_audit["objects"] if "DUPLICATE_OLE_ID" in item["issues"]
    )
    assert_true(duplicate_issue_count == 2, "both colliding objects must carry DUPLICATE_OLE_ID")

    bpy.ops.object.select_all(action="DESELECT")
    dup_a.select_set(True)
    dup_b.select_set(True)
    bpy.context.view_layer.objects.active = dup_a
    repair_result = bpy.ops.oleander.assign_identity()
    assert_true("FINISHED" in repair_result, "identity collision repair operator must finish")
    assert_true(dup_a.oleander.ole_id != dup_b.oleander.ole_id, "repair must produce unique OLE IDs")
    assert_true(dup_a.oleander.ole_id and dup_b.oleander.ole_id, "repair must leave both objects identified")
    repaired_audit = audit_scene(scene)
    assert_true(
        "OLE_DUPLICATE_EXPECTED_FAIL" not in repaired_audit["duplicate_ole_ids"],
        "repaired scene must no longer report the original duplicate ID",
    )
    results["duplicate_ole_id_detect_and_repair"] = "PASS"
    delete_objects([dup_a, dup_b])

    # 2) Missing dependency must force OBJECT_DEPENDENCIES=FAIL and be attached
    # to the declaring object, rather than degrading to a warning/pass.
    missing_obj = add_cube("OLE_FAIL_MISSING_DEP", location=(14.0, 0.0, 0.0))
    missing_obj.oleander.ole_id = "OLE_FAIL_MISSING_DEP"
    missing_obj.oleander.dependencies = "OLE_DOES_NOT_EXIST"
    missing_graph = build_dependency_graph(scene)
    assert_true(
        missing_graph["missing"].get("OLE_FAIL_MISSING_DEP") == ["OLE_DOES_NOT_EXIST"],
        "missing dependency graph entry must preserve the unresolved OLE ID",
    )
    missing_audit = audit_scene(scene)
    assert_true(
        missing_audit["summary"]["OBJECT_DEPENDENCIES"] == "FAIL",
        "missing dependency must fail OBJECT_DEPENDENCIES",
    )
    missing_record = next(item for item in missing_audit["objects"] if item["ole_id"] == "OLE_FAIL_MISSING_DEP")
    assert_true(
        "MISSING_OBJECT_DEPENDENCY" in missing_record["issues"],
        "declaring object must expose MISSING_OBJECT_DEPENDENCY",
    )
    results["missing_dependency_expected_failure"] = "PASS"
    delete_objects([missing_obj])

    # 3) Dependency cycles must be positively detected and fail the dependency
    # gate. This prevents a cyclic graph from being treated as a valid build.
    cycle_a = add_cube("OLE_FAIL_CYCLE_A", location=(16.0, 0.0, 0.0))
    cycle_b = add_cube("OLE_FAIL_CYCLE_B", location=(18.0, 0.0, 0.0))
    cycle_a.oleander.ole_id = "OLE_FAIL_CYCLE_A"
    cycle_b.oleander.ole_id = "OLE_FAIL_CYCLE_B"
    cycle_a.oleander.dependencies = "OLE_FAIL_CYCLE_B"
    cycle_b.oleander.dependencies = "OLE_FAIL_CYCLE_A"
    cycle_graph = build_dependency_graph(scene)
    cycles = detect_cycles(cycle_graph)
    assert_true(cycles, "dependency cycle fixture must produce at least one cycle")
    flattened = {node for cycle in cycles for node in cycle}
    assert_true(
        {"OLE_FAIL_CYCLE_A", "OLE_FAIL_CYCLE_B"}.issubset(flattened),
        "detected cycle must contain both cyclic OLE IDs",
    )
    cycle_audit = audit_scene(scene)
    assert_true(
        cycle_audit["summary"]["OBJECT_DEPENDENCIES"] == "FAIL",
        "dependency cycle must fail OBJECT_DEPENDENCIES",
    )
    assert_true(cycle_audit["dependency_cycles"], "audit payload must expose dependency cycle evidence")
    results["dependency_cycle_expected_failure"] = "PASS"
    delete_objects([cycle_a, cycle_b])

    return results


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

    src = add_cube("OLE_TEST_SOURCE")
    dst = add_cube("OLE_TEST_DERIVATIVE", location=(2.0, 0.0, 0.0))
    src.oleander.ole_id = "OLE_TEST_SOURCE"
    dst.oleander.ole_id = "OLE_TEST_DERIVATIVE"
    dst.oleander.dependencies = "OLE_TEST_SOURCE"
    for obj in (src, dst):
        obj.oleander.semantic_class = "test_part"
        obj.oleander.part_number = "TEST-PART-001"
        obj.oleander.material_spec = "TEST_MATERIAL"
        obj.oleander.fabrication_process = "TEST_PROCESS"

    graph = build_dependency_graph(scene)
    assert_true(not graph["missing"], "declared source dependency should resolve")
    assert_true(not detect_cycles(graph), "simple source->derivative graph should be acyclic")

    expected_failures = run_expected_failure_cases(scene)
    assert_true(len(scene.objects) == 2, "failure fixtures must cleanly remove temporary objects")

    changed = mark_downstream_stale(["OLE_TEST_SOURCE"], scene=scene)
    assert_true("OLE_TEST_DERIVATIVE" in changed, "downstream object should be marked stale")
    assert_true(dst.oleander.stale, "downstream stale flag should persist on metadata")

    store_baseline(src)
    current_dimensions = src.dimensions.copy()
    src.dimensions = (
        current_dimensions.x * 1.25,
        current_dimensions.y,
        current_dimensions.z,
    )
    bpy.context.view_layer.update()
    geo_diff = diff_from_baseline(src)
    assert_true(geo_diff["status"] == "CHANGED", "geometry diff should detect changed dimensions")
    assert_true(any(item["field"] == "dimensions" for item in geo_diff["changed"]), "dimension change should be explicit")

    store_baseline(src)
    original_name = src.name
    src.name = "OLE_TEST_SOURCE_RENAMED"
    rename_diff = diff_from_baseline(src)
    assert_true(rename_diff["status"] == "UNCHANGED", "object rename must not be reported as geometry change")
    src.name = original_name

    store_baseline(src)
    original_vertex = src.data.vertices[0].co.copy()
    src.data.vertices[0].co *= 0.9
    src.data.update()
    content_diff = diff_from_baseline(src)
    assert_true(content_diff["status"] == "CHANGED", "internal mesh-content edit must be detected")
    assert_true(
        any(item["field"] == "mesh_content_sha256" for item in content_diff["changed"]),
        "mesh content hash should expose internal vertex edits",
    )
    src.data.vertices[0].co = original_vertex
    src.data.update()

    bevel = src.modifiers.new(name="OLE_TEST_BEVEL", type="BEVEL")
    bevel.width = 0.01
    bpy.context.view_layer.update()
    store_baseline(src)
    bevel.width = 0.02
    bpy.context.view_layer.update()
    modifier_diff = diff_from_baseline(src)
    assert_true(modifier_diff["status"] == "CHANGED", "modifier parameter edit must be detected")
    assert_true(
        any(item["field"] == "modifier_stack" for item in modifier_diff["changed"]),
        "modifier parameter edit should appear in modifier_stack diff",
    )
    src.modifiers.remove(bevel)
    bpy.context.view_layer.update()

    original_location = tuple(src.location)
    capture_configuration(scene, "NORMAL")
    src.location.x += 10.0
    restore_result = restore_configuration(scene, "NORMAL")
    assert_true("OLE_TEST_SOURCE" in restore_result["restored"], "configuration restore should resolve source by OLE ID")
    assert_true(tuple(round(v, 6) for v in src.location) == tuple(round(v, 6) for v in original_location), "configuration restore should restore transforms")

    bom = build_bom(scene)
    assert_true(bom["schema"] == "OLEANDER_BOM_v0.2", "BOM schema version mismatch")
    assert_true(len(bom["items"]) == 1, "same part number should group into one BOM item")
    assert_true(bom["items"][0]["quantity"] == 2, "BOM quantity should count both governed objects")
    assert_true(bom["items"][0]["metadata_conflict"], "same part number with different dimensions must be flagged")

    src["oleander_geometry_audit_state"] = "PASS"
    src.oleander.field_state = "VERIFIED"
    src.oleander.engineering_state = "APPROVED"
    src.oleander.manufacturing_state = "RELEASED"
    src.oleander.design_review_state = "PASS"
    src.oleander.stale = False
    review = summarize_object_state(src)
    assert_true(review["overall"] == "PASS", "all scoped PASS/NA states should summarize to PASS")

    src.oleander.stale = True
    review_stale = summarize_object_state(src)
    assert_true(review_stale["overall"] == "HOLD", "stale object should summarize to HOLD")
    src.oleander.stale = False

    one_meter_scene_units = _mm_to_scene_units(bpy.context, 1000.0)
    assert_true(
        abs(one_meter_scene_units - 1000.0) < 1e-3,
        f"Unit Scale 0.001 should map 1000 mm to approximately 1000 scene units; got {one_meter_scene_units!r}",
    )
    round_trip_mm = _scene_units_to_mm(bpy.context, one_meter_scene_units)
    assert_true(
        abs(round_trip_mm - 1000.0) < 1e-6,
        f"mm -> scene units -> mm round trip should preserve 1000 mm; got {round_trip_mm!r}",
    )

    reopen_path = "/tmp/oleander-stage2-reopen.blend"
    bpy.ops.wm.save_as_mainfile(filepath=reopen_path)
    assert_true(pathlib.Path(reopen_path).is_file(), "runtime fixture .blend should be written")
    bpy.ops.wm.open_mainfile(filepath=reopen_path)

    scene = bpy.context.scene
    src = find_by_ole_id(scene, "OLE_TEST_SOURCE")
    dst = find_by_ole_id(scene, "OLE_TEST_DERIVATIVE")
    assert_true(src is not None and dst is not None, "OLE IDs must survive save/reopen")
    assert_true(src.oleander.semantic_class == "test_part", "semantic class must survive save/reopen")
    assert_true(src.oleander.part_number == "TEST-PART-001", "part number must survive save/reopen")
    assert_true(dst.oleander.dependencies == "OLE_TEST_SOURCE", "dependency metadata must survive save/reopen")
    assert_true("oleander_geometry_baseline" in src, "geometry baseline must survive save/reopen")
    assert_true("NORMAL" in configuration_names(scene), "configuration index must survive save/reopen")
    assert_true(src.oleander.field_state == "VERIFIED", "field state must survive save/reopen")
    assert_true(src.oleander.engineering_state == "APPROVED", "engineering state must survive save/reopen")
    assert_true(src.oleander.manufacturing_state == "RELEASED", "manufacturing state must survive save/reopen")
    assert_true(src.oleander.design_review_state == "PASS", "design review state must survive save/reopen")

    bpy.context.view_layer.objects.active = src
    src.select_set(True)
    bpy.ops.oleander.run_audit()
    audit_text = bpy.data.texts.get("OLEANDER_AUDIT.json")
    assert_true(audit_text is not None, "audit should create OLEANDER_AUDIT.json")
    audit = json.loads(audit_text.as_string())
    assert_true(audit["schema"] == "OLEANDER_BLENDER_AUDIT_v0.2", "audit schema version mismatch")
    assert_true(audit["summary"]["OBJECT_DEPENDENCIES"] == "PASS", "object dependency audit should pass")

    bpy.ops.oleander.build_bom()
    bom_text = bpy.data.texts.get("OLEANDER_BOM.json")
    assert_true(bom_text is not None, "BOM operator should create OLEANDER_BOM.json")

    bpy.ops.oleander.export_manifest()
    manifest_text = bpy.data.texts.get("OLEANDER_MANIFEST.json")
    assert_true(manifest_text is not None, "manifest should create OLEANDER_MANIFEST.json")
    manifest = json.loads(manifest_text.as_string())
    assert_true(manifest["schema"] == "OLEANDER_BLENDER_WORKBENCH_MANIFEST_v0.2", "manifest schema version mismatch")
    assert_true(len(manifest["objects"]) == 2, "manifest should include both test objects")
    assert_true("NORMAL" in manifest["scene"]["configurations"], "manifest should expose saved configuration names")

    result = {
        "runtime": "OLEANDER Blender Runtime",
        "version": "0.2.0",
        "blender": bpy.app.version_string,
        "status": "PASS",
        "source_fingerprint_sha256": runtime_source_fingerprint(),
        "checks": [
            "registration",
            "persistent_metadata",
            "duplicate_ole_id_expected_failure",
            "identity_collision_repair_operator",
            "missing_dependency_expected_failure",
            "dependency_cycle_expected_failure",
            "dependency_graph",
            "stale_propagation",
            "geometry_baseline_diff",
            "rename_is_not_geometry_change",
            "mesh_content_hash",
            "modifier_parameter_diff",
            "configuration_capture_restore",
            "bom_grouping_and_conflict_detection",
            "review_state_separation",
            "scene_unit_scale_conversion",
            "scene_unit_scale_round_trip",
            "blend_save_reopen_persistence",
            "audit_v0.2",
            "manifest_v0.2",
        ],
        "expected_failure_cases": expected_failures,
        "non_claims": [
            "field_truth",
            "engineering_approval",
            "manufacturing_release",
            "constructability",
            "design_quality",
        ],
    }
    print("OLEANDER_STAGE2_VALIDATION=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
