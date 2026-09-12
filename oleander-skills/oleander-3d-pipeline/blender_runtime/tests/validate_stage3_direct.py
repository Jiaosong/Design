"""Headless validation for OLEANDER Blender Runtime Stage 3 Direct Modeling.

This validates deterministic direct dimensions, linear duplication, bounded
face-normal move, bounded face-tangent move, and bounded U/V-axis face rotation in a real Blender process.
CAD_NATIVE normal, tangent, and rotate entrypoints may prepare governed sidecar intents while
leaving Blender display geometry unchanged; authoritative B-Rep execution is proved
separately by the professional CAD-sidecar integration surface. This does not
establish general CAD/B-Rep push-pull, general planar translation, persistent
topological naming, engineering, field, manufacturing, constructability, or design
authority.
"""

from __future__ import annotations

import bmesh
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
from oleander_blender.direct_model import (
    CAD_DIRECT_EDIT_INTENT_SCHEMA,
    _scene_units_to_mm,
)


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
    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def add_cube(name, location=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj


def select_only(obj):
    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def select_top_face_for_intent(obj):
    select_only(obj)
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(obj.data)
    bm.normal_update()
    for face in bm.faces:
        face.select = False
    candidates = [face for face in bm.faces if face.normal.z > 0.9]
    assert_true(candidates, "fixture must expose a positive-Z face")
    target = max(candidates, key=lambda face: face.calc_center_median().z)
    target.select = True
    bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
    return target


def mm_dimensions(context, obj):
    return tuple(_scene_units_to_mm(context, value) for value in obj.dimensions)


def close_tuple(actual, expected, tolerance=1e-3):
    return all(abs(a - e) <= tolerance for a, e in zip(actual, expected))


def mesh_vertex_snapshot(obj):
    return tuple(tuple(round(float(value), 9) for value in vertex.co) for vertex in obj.data.vertices)


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

    native_face = add_cube("OLE_STAGE3_DIRECT_FACE_NATIVE", location=(0.0, 2000.0, 0.0))
    native_face.oleander.ole_id = "OLE_STAGE3_DIRECT_FACE_NATIVE"
    select_only(native_face)
    native_dims = bpy.ops.oleander.apply_metric_dimensions(x_mm=100.0, y_mm=100.0, z_mm=100.0)
    assert_true("FINISHED" in native_dims, "native face fixture dimensions must apply")

    native_face_dependent = add_cube("OLE_STAGE3_DIRECT_FACE_DEPENDENT", location=(500.0, 2000.0, 0.0))
    native_face_dependent.oleander.ole_id = "OLE_STAGE3_DIRECT_FACE_DEPENDENT"
    native_face_dependent.oleander.dependencies = "OLE_STAGE3_DIRECT_FACE_NATIVE"
    native_face_dependent.oleander.stale = False

    select_top_face_for_intent(native_face)
    native_move = bpy.ops.oleander.direct_face_normal_move(distance_mm=25.0)
    assert_true("FINISHED" in native_move, "BLENDER_NATIVE Face Normal Move must finish")
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.update()
    assert_true(
        close_tuple(mm_dimensions(bpy.context, native_face), (100.0, 100.0, 125.0)),
        f"native face normal move must produce 125 mm Z extent; got {mm_dimensions(bpy.context, native_face)!r}",
    )
    assert_true(
        native_face_dependent.oleander.stale
        and native_face_dependent.get("oleander_stale_reason") == "DIRECT_FACE_NORMAL_MOVE",
        "native face move must propagate a specific stale reason",
    )
    assert_true(
        native_face.get("oleander_last_direct_operation") == "FACE_NORMAL_MOVE"
        and native_face.get("oleander_direct_authority_route") == "BLENDER_NATIVE",
        "native face move must record explicit Blender authority routing",
    )
    native_descriptor = json.loads(native_face["oleander_direct_face_target_descriptor"])
    assert_true("polygon_index" not in native_descriptor, "native semantic descriptor must not persist a polygon index")

    # BLENDER_NATIVE bounded tangent move. The selected top face is translated
    # in a geometry-derived U/V basis while keeping the move exactly tangent.
    tangent_face = add_cube("OLE_STAGE3_DIRECT_FACE_TANGENT", location=(0.0, 3000.0, 0.0))
    tangent_face.oleander.ole_id = "OLE_STAGE3_DIRECT_FACE_TANGENT"
    select_only(tangent_face)
    tangent_dims = bpy.ops.oleander.apply_metric_dimensions(x_mm=100.0, y_mm=100.0, z_mm=100.0)
    assert_true("FINISHED" in tangent_dims, "tangent face fixture dimensions must apply")

    tangent_dependent = add_cube("OLE_STAGE3_DIRECT_TANGENT_DEPENDENT", location=(500.0, 3000.0, 0.0))
    tangent_dependent.oleander.ole_id = "OLE_STAGE3_DIRECT_TANGENT_DEPENDENT"
    tangent_dependent.oleander.dependencies = "OLE_STAGE3_DIRECT_FACE_TANGENT"
    tangent_dependent.oleander.stale = False

    select_top_face_for_intent(tangent_face)
    tangent_move = bpy.ops.oleander.direct_face_tangent_move(u_mm=20.0, v_mm=10.0)
    assert_true("FINISHED" in tangent_move, "BLENDER_NATIVE Face Tangent Move must finish")
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.update()
    tangent_actual = mm_dimensions(bpy.context, tangent_face)
    assert_true(
        close_tuple(tangent_actual, (120.0, 110.0, 100.0)),
        f"tangent move must shear the top face to a 120x110x100 mm bbox; got {tangent_actual!r}",
    )
    assert_true(
        tangent_dependent.oleander.stale
        and tangent_dependent.get("oleander_stale_reason") == "DIRECT_FACE_TANGENT_MOVE",
        "tangent face move must propagate a specific stale reason",
    )
    assert_true(
        tangent_face.get("oleander_last_direct_operation") == "FACE_TANGENT_MOVE"
        and tangent_face.get("oleander_direct_authority_route") == "BLENDER_NATIVE",
        "tangent face move must record explicit Blender authority routing",
    )
    assert_true(
        list(tangent_face["oleander_direct_face_tangent_uv_mm"]) == [20.0, 10.0],
        "tangent move must preserve requested U/V metric values",
    )
    tangent_u = tangent_face["oleander_direct_face_tangent_u_local"]
    tangent_v = tangent_face["oleander_direct_face_tangent_v_local"]
    assert_true(len(tangent_u) == 3 and len(tangent_v) == 3, "tangent basis must be persisted as two local vectors")
    assert_true(
        abs(sum(float(a) * float(b) for a, b in zip(tangent_u, tangent_v))) <= 1e-6,
        "tangent U/V basis must remain orthogonal",
    )


    # BLENDER_NATIVE bounded face rotation around the deterministic U tangent through face center.
    rotate_face = add_cube("OLE_STAGE3_DIRECT_FACE_ROTATE", location=(0.0, 3500.0, 0.0))
    rotate_face.oleander.ole_id = "OLE_STAGE3_DIRECT_FACE_ROTATE"
    select_only(rotate_face)
    rotate_dims = bpy.ops.oleander.apply_metric_dimensions(x_mm=100.0, y_mm=100.0, z_mm=100.0)
    assert_true("FINISHED" in rotate_dims, "rotate face fixture dimensions must apply")
    rotate_dependent = add_cube("OLE_STAGE3_DIRECT_ROTATE_DEPENDENT", location=(500.0, 3500.0, 0.0))
    rotate_dependent.oleander.ole_id = "OLE_STAGE3_DIRECT_ROTATE_DEPENDENT"
    rotate_dependent.oleander.dependencies = "OLE_STAGE3_DIRECT_FACE_ROTATE"
    rotate_dependent.oleander.stale = False
    select_top_face_for_intent(rotate_face)
    rotate_result = bpy.ops.oleander.direct_face_rotate(axis_mode="U", angle_deg=5.0)
    assert_true("FINISHED" in rotate_result, "BLENDER_NATIVE Face Rotate must finish")
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.update()
    rotate_actual = mm_dimensions(bpy.context, rotate_face)
    assert_true(abs(rotate_actual[0] - 100.0) <= 1e-3, f"U-axis rotate must preserve X extent; got {rotate_actual!r}")
    assert_true(100.0 < rotate_actual[2] < 105.0, f"5 degree top-face rotate must increase Z bbox within bounded fixture; got {rotate_actual!r}")
    assert_true(rotate_dependent.oleander.stale and rotate_dependent.get("oleander_stale_reason") == "DIRECT_FACE_ROTATE", "face rotate must propagate specific stale reason")
    assert_true(rotate_face.get("oleander_last_direct_operation") == "FACE_ROTATE", "face rotate provenance must record operation")
    assert_true(rotate_face.get("oleander_direct_face_rotate_axis_mode") == "U", "face rotate must retain U axis mode")
    assert_true(abs(float(rotate_face.get("oleander_direct_face_rotate_angle_deg")) - 5.0) <= 1e-9, "face rotate must retain requested angle")
    rotate_axis = list(rotate_face["oleander_direct_face_rotate_axis_local"])
    assert_true(len(rotate_axis) == 3 and abs(sum(v * v for v in rotate_axis) - 1.0) <= 1e-6, "face rotate axis must be unit length")

    cad_face = add_cube("OLE_STAGE3_DIRECT_FACE_CAD", location=(0.0, 4000.0, 0.0))
    cad_face.oleander.ole_id = "OLE_STAGE3_DIRECT_FACE_CAD"
    select_only(cad_face)
    cad_dims = bpy.ops.oleander.apply_metric_dimensions(x_mm=100.0, y_mm=100.0, z_mm=100.0)
    assert_true("FINISHED" in cad_dims, "CAD display fixture dimensions must apply before authority handoff")
    cad_face.oleander.master_type = "CAD_NATIVE"
    cad_face.oleander.master_locator = "governed://cad/OLE_STAGE3_DIRECT_FACE_CAD/master.FCStd"
    cad_face.oleander.geometry_authority = "VISUAL_ONLY"
    cad_before = mesh_vertex_snapshot(cad_face)

    select_top_face_for_intent(cad_face)
    cad_move = bpy.ops.oleander.direct_face_normal_move(distance_mm=15.0)
    assert_true("FINISHED" in cad_move, "CAD_NATIVE Face Normal Move entrypoint must prepare an intent")
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.update()
    cad_after = mesh_vertex_snapshot(cad_face)
    assert_true(cad_after == cad_before, "CAD_NATIVE direct-edit intent must not mutate Blender display geometry")
    assert_true(
        cad_face.get("oleander_cad_direct_edit_state") == "PENDING_SIDECAR"
        and cad_face.get("oleander_direct_authority_route") == "CAD_NATIVE",
        "CAD direct edit must remain pending specialist-sidecar execution",
    )

    raw_intent = cad_face["oleander_cad_direct_edit_intent"]
    intent = json.loads(raw_intent)
    assert_true(intent["schema"] == CAD_DIRECT_EDIT_INTENT_SCHEMA, "CAD intent schema must be explicit")
    assert_true(intent["operation"] == "FACE_NORMAL_MOVE", "CAD intent operation must remain bounded to face normal move")
    assert_true(
        intent["authority"]["required_kernel"] == "FREECAD_OCCT_BREP"
        and intent["authority"]["blender_role"] == "DISPLAY_DERIVATIVE_ONLY"
        and intent["authority"]["display_mutation"] == "NONE",
        "CAD intent must preserve FreeCAD/OCCT authority and no-display-mutation boundary",
    )
    assert_true(
        intent["resolution"]["policy"] == "SEMANTIC_REBIND_FAIL_CLOSED"
        and intent["resolution"]["ambiguous_result"] == "HOLD"
        and intent["resolution"]["missing_result"] == "HOLD",
        "CAD direct edit must require fail-closed semantic rebind",
    )
    target_keys = set(intent["target"].keys())
    assert_true(
        "polygon_index" not in target_keys and "subshape_ordinal" not in target_keys,
        "CAD target descriptor must not persist Blender or CAD topology ordinals",
    )
    assert_true(
        set(intent["resolution"]["prohibited_persistence"])
        >= {"FaceN", "EdgeN", "VertexN", "subshape_ordinal", "polygon_index"},
        "CAD intent must explicitly prohibit unstable topology persistence",
    )
    assert_true(
        cad_face["oleander_cad_direct_edit_intent_sha256"]
        == hashlib.sha256(raw_intent.encode("utf-8")).hexdigest(),
        "CAD direct-edit intent must carry deterministic SHA identity",
    )

    # CAD tangent entrypoint now prepares a governed FACE_TANGENT_MOVE sidecar
    # intent. The Stage 3 runtime still does not execute B-Rep mutation itself.
    cad_tangent_before = mesh_vertex_snapshot(cad_face)
    select_top_face_for_intent(cad_face)
    cad_tangent_move = bpy.ops.oleander.direct_face_tangent_move(u_mm=5.0, v_mm=0.0)
    assert_true("FINISHED" in cad_tangent_move, "CAD_NATIVE Face Tangent Move must prepare an intent")
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.update()
    assert_true(mesh_vertex_snapshot(cad_face) == cad_tangent_before, "CAD tangent intent must not mutate display geometry")
    assert_true(
        cad_face.get("oleander_cad_direct_edit_state") == "PENDING_SIDECAR"
        and cad_face.get("oleander_direct_authority_route") == "CAD_NATIVE",
        "CAD tangent edit must remain pending specialist-sidecar execution",
    )
    raw_tangent_intent = cad_face["oleander_cad_direct_edit_intent"]
    tangent_intent = json.loads(raw_tangent_intent)
    assert_true(tangent_intent["operation"] == "FACE_TANGENT_MOVE", "CAD tangent intent operation must be explicit")
    assert_true(
        tangent_intent["parameters"]["translation_local_mm"] == [5.0, 0.0, 0.0],
        "CAD tangent intent must normalize U/V provenance into local-mm translation",
    )
    assert_true(
        tangent_intent["parameters"]["u_mm"] == 5.0
        and tangent_intent["parameters"]["v_mm"] == 0.0,
        "CAD tangent intent must retain interaction U/V provenance",
    )
    assert_true(
        cad_face["oleander_cad_direct_edit_intent_sha256"]
        == hashlib.sha256(raw_tangent_intent.encode("utf-8")).hexdigest(),
        "CAD tangent intent must carry deterministic SHA identity",
    )

    # CAD face rotate prepares the same governed intent envelope without mutating display geometry.
    cad_rotate_before = mesh_vertex_snapshot(cad_face)
    select_top_face_for_intent(cad_face)
    cad_rotate = bpy.ops.oleander.direct_face_rotate(axis_mode="U", angle_deg=5.0)
    assert_true("FINISHED" in cad_rotate, "CAD_NATIVE Face Rotate must prepare an intent")
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.update()
    assert_true(mesh_vertex_snapshot(cad_face) == cad_rotate_before, "CAD face-rotate intent must not mutate display geometry")
    raw_rotate_intent = cad_face["oleander_cad_direct_edit_intent"]
    rotate_intent = json.loads(raw_rotate_intent)
    assert_true(rotate_intent["operation"] == "FACE_ROTATE", "CAD face-rotate intent operation must be explicit")
    assert_true(rotate_intent["parameters"]["axis_mode"] == "U", "CAD face-rotate intent must retain axis mode")
    assert_true(abs(rotate_intent["parameters"]["angle_deg"] - 5.0) <= 1e-9, "CAD face-rotate intent must retain angle")
    assert_true(rotate_intent["parameters"]["axis_origin_local_mm"] == rotate_intent["target"]["center_local_mm"], "CAD face-rotate first contract axis must pass through semantic face center")
    rotate_normal = rotate_intent["target"]["normal_local"]
    rotate_axis = rotate_intent["parameters"]["axis_direction_local"]
    assert_true(abs(sum(float(a) * float(b) for a, b in zip(rotate_normal, rotate_axis))) <= 1e-6, "CAD face-rotate axis must be tangent to semantic face")
    assert_true(cad_face["oleander_cad_direct_edit_intent_sha256"] == hashlib.sha256(raw_rotate_intent.encode("utf-8")).hexdigest(), "CAD face-rotate intent must carry deterministic SHA identity")

    audit = audit_scene(scene)
    assert_true(not audit["duplicate_ole_ids"], f"governed direct modeling must not create duplicate OLE IDs: {audit['duplicate_ole_ids']}")
    assert_true(
        audit["summary"]["OBJECT_DEPENDENCIES"] == "PASS",
        "direct-modeling fixture must preserve a valid dependency graph",
    )

    result = {
        "runtime": "OLEANDER Blender Runtime",
        "stage": "STAGE3_DIRECT_MODELING",
        "version": "0.3.0",
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
            "face_normal_move_operator",
            "blender_native_face_normal_move_metric",
            "face_normal_move_downstream_stale_propagation",
            "face_tangent_move_operator",
            "blender_native_face_tangent_move_metric",
            "face_tangent_move_geometry_based_uv_basis",
            "face_tangent_move_downstream_stale_propagation",
            "face_rotate_operator",
            "blender_native_face_rotate_bounded_angle",
            "face_rotate_geometry_based_axis",
            "face_rotate_downstream_stale_propagation",
            "cad_native_direct_edit_intent_routing",
            "cad_native_display_geometry_unchanged",
            "cad_native_tangent_intent_routing",
            "cad_native_tangent_move_no_display_mutation",
            "cad_native_tangent_uv_translation_normalization",
            "cad_native_face_rotate_intent_routing",
            "cad_native_face_rotate_no_display_mutation",
            "cad_native_face_rotate_center_tangent_axis",
            "cad_intent_semantic_selector_no_persistent_face_index",
            "cad_intent_fail_closed_resolution_policy",
            "post_direct_audit_no_duplicate_ids",
        ],
        "expected_failure_cases": {},
        "non_claims": [
            "cad_face_rotate_direct_edit_execution",
            "general_arbitrary_axis_face_rotate",
            "general_brep_push_pull",
            "persistent_topological_naming",
            "cad_brep_generality",
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
