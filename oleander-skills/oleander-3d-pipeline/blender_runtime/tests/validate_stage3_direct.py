"""Headless validation for OLEANDER Blender Runtime Stage 3 Direct Modeling.

This validates deterministic direct-dimension and linear-array operators in a
real Blender 5.1+ process. It does not create CAD/B-Rep, engineering, field,
manufacturing, constructability, or design authority.
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
from oleander_blender.dependency import clear_stale
from oleander_blender.direct_model import _scene_units_to_mm


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


def add_cube(name, location=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj


def select_only(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def mm_dimensions(context, obj):
    return tuple(_scene_units_to_mm(context, value) for value in obj.dimensions)


def close_tuple(actual, expected, tolerance=1e-3):
    return all(abs(a - e) <= tolerance for a, e in zip(actual, expected))


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

    source = add_cube("OLE_STAGE3_DIRECT_SOURCE")
    source.oleander.ole_id = "OLE_STAGE3_DIRECT_SOURCE"
    source.oleander.semantic_class = "direct_test_part"
    source.oleander.part_number = "DIRECT-TEST-001"

    dependent = add_cube("OLE_STAGE3_DIRECT_DEPENDENT", location=(3000.0, 0.0, 0.0))
    dependent.oleander.ole_id = "OLE_STAGE3_DIRECT_DEPENDENT"
    dependent.oleander.dependencies = "OLE_STAGE3_DIRECT_SOURCE"
    dependent.oleander.stale = False

    select_only(source)
    dimension_result = bpy.ops.oleander.apply_metric_dimensions(
        x_mm=1200.0,
        y_mm=600.0,
        z_mm=80.0,
    )
    assert_true("FINISHED" in dimension_result, "Apply mm Dimensions operator must finish")
    bpy.context.view_layer.update()

    actual_mm = mm_dimensions(bpy.context, source)
    assert_true(
        close_tuple(actual_mm, (1200.0, 600.0, 80.0)),
        f"direct dimensions must match requested millimetres; got {actual_mm!r}",
    )
    assert_true(
        all(abs(value - 1.0) <= 1e-6 for value in source.scale),
        f"direct dimension operation must leave applied scale; got {tuple(source.scale)!r}",
    )
    assert_true(
        dependent.oleander.stale,
        "direct geometry change must mark declared downstream dependency stale",
    )
    assert_true(
        dependent.get("oleander_stale_reason") == "DIRECT_DIMENSION_CHANGE",
        "downstream stale reason must identify direct dimension change",
    )
    assert_true(
        list(source["oleander_direct_dimensions_mm"]) == [1200.0, 600.0, 80.0],
        "direct dimension operator must record requested metric values",
    )

    clear_stale(dependent)
    assert_true(not dependent.oleander.stale, "test fixture stale reset must succeed")

    before_objects = set(scene.objects)
    select_only(source)
    array_result = bpy.ops.oleander.duplicate_linear(
        count=4,
        spacing_mm=600.0,
        axis="X",
        linked=True,
    )
    assert_true("FINISHED" in array_result, "Linear Duplicate operator must finish")
    bpy.context.view_layer.update()

    created = [obj for obj in scene.objects if obj not in before_objects]
    assert_true(len(created) == 3, f"count=4 must create three additional instances; got {len(created)}")
    created.sort(key=lambda obj: int(obj.get("oleander_array_index", -1)))

    expected_ids = [
        "OLE_STAGE3_DIRECT_SOURCE_A001",
        "OLE_STAGE3_DIRECT_SOURCE_A002",
        "OLE_STAGE3_DIRECT_SOURCE_A003",
    ]
    actual_ids = [obj.oleander.ole_id for obj in created]
    assert_true(actual_ids == expected_ids, f"array instance OLE IDs must be stable and unique; got {actual_ids!r}")
    assert_true(len(set(actual_ids + [source.oleander.ole_id])) == 4, "source and array instances must have unique OLE IDs")

    source_x = source.location.x
    expected_step = 600.0
    for index, obj in enumerate(created, start=1):
        assert_true(obj.data is source.data, "linked array instances must share the source mesh datablock")
        spacing_mm = _scene_units_to_mm(bpy.context, obj.location.x - source_x)
        assert_true(
            abs(spacing_mm - expected_step * index) <= 1e-3,
            f"array spacing must be deterministic in millimetres; index={index}, got {spacing_mm}",
        )
        assert_true(
            obj.get("oleander_array_source_id") == "OLE_STAGE3_DIRECT_SOURCE",
            "array provenance must use stable source OLE ID rather than mutable object name",
        )
        assert_true(
            obj.get("oleander_array_instance_role") == "LINKED_MESH_INSTANCE",
            "linked array provenance role must be explicit",
        )

    audit = audit_scene(scene)
    assert_true(not audit["duplicate_ole_ids"], f"governed linear duplicate must not create duplicate OLE IDs: {audit['duplicate_ole_ids']}")
    assert_true(
        audit["summary"]["OBJECT_DEPENDENCIES"] == "PASS",
        "direct-modeling fixture must preserve a valid dependency graph",
    )

    result = {
        "runtime": "OLEANDER Blender Runtime",
        "stage": "STAGE3_DIRECT_MODELING",
        "version": "0.2.0",
        "blender": bpy.app.version_string,
        "status": "PASS",
        "source_fingerprint_sha256": source_fingerprint(),
        "checks": [
            "direct_metric_dimensions_operator",
            "direct_dimensions_applied_scale",
            "direct_geometry_change_stale_propagation",
            "direct_operation_metric_record",
            "linear_duplicate_operator",
            "linear_duplicate_unique_ole_ids",
            "linear_duplicate_stable_source_provenance",
            "linear_duplicate_linked_mesh",
            "linear_duplicate_metric_spacing",
            "post_direct_audit_no_duplicate_ids",
        ],
        "non_claims": [
            "cad_brep",
            "solver_backed_constraints",
            "field_truth",
            "engineering_approval",
            "manufacturing_release",
            "constructability",
            "design_quality",
        ],
    }
    print("OLEANDER_STAGE3_DIRECT_VALIDATION=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
