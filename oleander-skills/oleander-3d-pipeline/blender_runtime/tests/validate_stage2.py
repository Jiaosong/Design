"""Headless validation for OLEANDER Blender Runtime Stage 2.

Run from a Blender 5.1+ build, from repository root or with an absolute script path:

    blender --background --factory-startup --python \
      oleander-skills/oleander-3d-pipeline/blender_runtime/tests/validate_stage2.py

This validation checks runtime mechanics only. It does not prove field truth,
engineering approval, manufacturing release, constructability or design quality.
"""

from __future__ import annotations

import json
import pathlib
import sys

import bpy

SCRIPT = pathlib.Path(__file__).resolve()
RUNTIME_ROOT = SCRIPT.parents[1]
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))

import oleander_blender
from oleander_blender.bom import build_bom
from oleander_blender.configuration import capture_configuration, restore_configuration
from oleander_blender.dependency import build_dependency_graph, detect_cycles, mark_downstream_stale
from oleander_blender.direct_model import _mm_to_scene_units
from oleander_blender.geometry_diff import diff_from_baseline, store_baseline
from oleander_blender.review_state import summarize_object_state


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def add_cube(name, location=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
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

    changed = mark_downstream_stale(["OLE_TEST_SOURCE"], scene=scene)
    assert_true("OLE_TEST_DERIVATIVE" in changed, "downstream object should be marked stale")
    assert_true(dst.oleander.stale, "downstream stale flag should persist on metadata")

    store_baseline(src)
    src.dimensions.x *= 1.25
    geo_diff = diff_from_baseline(src)
    assert_true(geo_diff["status"] == "CHANGED", "geometry diff should detect changed dimensions")
    assert_true(any(item["field"] == "dimensions" for item in geo_diff["changed"]), "dimension change should be explicit")

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
    assert_true(abs(one_meter_scene_units - 1000.0) < 1e-9, "Unit Scale 0.001 must map 1000 mm to 1000 scene units")

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
        "checks": [
            "registration",
            "persistent_metadata",
            "dependency_graph",
            "stale_propagation",
            "geometry_baseline_diff",
            "configuration_capture_restore",
            "bom_grouping_and_conflict_detection",
            "review_state_separation",
            "scene_unit_scale_conversion",
            "audit_v0.2",
            "manifest_v0.2",
        ],
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
