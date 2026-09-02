"""Transactional explicit application for OLEANDER Design Intent parameters.

This layer applies only a small allow-list of existing Blender-native fields.
It performs whole-parameter preflight before mutation, snapshots every target,
verifies the result, and rolls the transaction back on any apply/postcheck
failure. It is explicit invocation only: no dependency solver, no automatic
parameter-driven rebuild, no CAD/B-Rep authority.
"""

from __future__ import annotations

import json

import bpy
from mathutils import Vector

from .dependency import mark_downstream_stale, object_id
from .design_intent import (
    _append_event,
    _parameter_by_id,
    audit_design_intent_graph,
    evaluate_failure_envelope,
    get_design_parameters,
    resolve_binding,
)
from .direct_model import _apply_object_scale, _mm_to_scene_units, _scene_units_to_mm
from .feature_stack import FEATURE_HISTORY_KEY, get_feature_history, validate_feature_history
from .relation_kernel import RELATIONS_KEY, evaluate_relation, get_relations

LAST_APPLY_KEY = "oleander_design_intent_last_apply"
APPLY_SCHEMA = "OLEANDER_DESIGN_INTENT_APPLY_v0.1"

OBJECT_FIELDS = {"DIMENSION_X": 0, "DIMENSION_Y": 1, "DIMENSION_Z": 2}
FEATURE_FIELDS = {
    "PLANAR_EXTRUDE": {"depth_mm": "LENGTH_MM"},
    "SHELL": {"thickness_mm": "LENGTH_MM"},
    "BEVEL_CHAMFER": {"width_mm": "LENGTH_MM"},
    "LINEAR_PATTERN": {"count": "COUNT", "spacing_mm": "LENGTH_MM"},
}
RELATION_FIELDS = {"target_mm", "tolerance_mm", "tolerance_deg"}
DATUM_FIELDS = {
    "DATUM_AXIS": {"length_mm"},
    "DATUM_PLANE": {"size_mm"},
    "CONSTRUCTION_LINE": {"length_mm", "offset_mm"},
}


def _find_object_by_id(scene, oid):
    for obj in scene.objects:
        if object_id(obj) == oid:
            return obj
    return None


def _require_kind(parameter, expected, field):
    if parameter.get("kind") != expected:
        raise ValueError(f"{field} requires parameter kind {expected}")


def _reject_transform_authority(obj):
    if len(obj.constraints):
        raise ValueError(f"{obj.name} has external transform authority via Blender constraints")


def _preflight_object(scene, parameter, binding, resolved):
    field = binding.get("target_field", "")
    if field not in OBJECT_FIELDS:
        raise ValueError(f"unsupported OBJECT apply field: {field}")
    _require_kind(parameter, "LENGTH_MM", field)
    value = float(parameter.get("value"))
    if value <= 0.0:
        raise ValueError(f"{field} must be greater than zero")
    obj = resolved.get("target")
    if obj is None or obj.type != "MESH":
        raise ValueError("OBJECT dimension apply requires a mesh target")
    _reject_transform_authority(obj)
    return {"kind": "OBJECT", "binding": binding, "object": obj, "field": field, "value": value}


def _preflight_feature(scene, parameter, binding, resolved):
    target_id = binding.get("target_id", "")
    owner = None
    entry = None
    for obj in scene.objects:
        for candidate in get_feature_history(obj):
            if candidate.get("feature_id") == target_id:
                owner = obj
                entry = candidate
                break
        if entry is not None:
            break
    if owner is None or entry is None:
        raise ValueError(f"feature target not found during apply preflight: {target_id}")
    modifier = owner.modifiers.get(entry.get("modifier_name", ""))
    if modifier is None:
        raise ValueError(f"feature modifier missing during apply preflight: {target_id}")
    kind = entry.get("kind", "")
    field = binding.get("target_field", "")
    expected = FEATURE_FIELDS.get(kind, {}).get(field)
    if expected is None:
        raise ValueError(f"unsupported FEATURE apply field: {kind}.{field}")
    _require_kind(parameter, expected, field)
    value = parameter.get("value")
    if field in {"thickness_mm", "width_mm"} and float(value) <= 0.0:
        raise ValueError(f"{field} must be greater than zero")
    if field == "depth_mm" and abs(float(value)) < 0.001:
        raise ValueError("depth_mm must be non-zero")
    if field == "count" and int(value) < 2:
        raise ValueError("linear pattern count must be at least 2")
    if field == "spacing_mm" and float(value) < 0.0:
        raise ValueError("linear pattern spacing_mm must be non-negative")
    return {
        "kind": "FEATURE",
        "binding": binding,
        "object": owner,
        "feature": entry,
        "modifier": modifier,
        "field": field,
        "value": value,
    }


def _preflight_relation(scene, parameter, binding, resolved):
    relation = resolved.get("target")
    if relation is None:
        raise ValueError("relation target not found during apply preflight")
    field = binding.get("target_field", "")
    if field not in RELATION_FIELDS:
        raise ValueError(f"unsupported RELATION apply field: {field}")
    kind = relation.get("kind", "")
    if field == "target_mm":
        if kind not in {"ORIGIN_DISTANCE", "AXIS_OFFSET"}:
            raise ValueError(f"target_mm is not mutable for relation kind {kind}")
        _require_kind(parameter, "LENGTH_MM", field)
        if kind == "ORIGIN_DISTANCE" and float(parameter.get("value")) < 0.0:
            raise ValueError("ORIGIN_DISTANCE target_mm cannot be negative")
    elif field == "tolerance_mm":
        if kind not in {"ORIGIN_DISTANCE", "AXIS_OFFSET", "ORIGIN_COINCIDENT"}:
            raise ValueError(f"tolerance_mm is not valid for relation kind {kind}")
        _require_kind(parameter, "LENGTH_MM", field)
        if float(parameter.get("value")) < 0.0:
            raise ValueError("tolerance_mm cannot be negative")
    else:
        if kind != "AXIS_PARALLEL":
            raise ValueError(f"tolerance_deg is not valid for relation kind {kind}")
        _require_kind(parameter, "ANGLE_DEG", field)
        if float(parameter.get("value")) < 0.0:
            raise ValueError("tolerance_deg cannot be negative")
    return {"kind": "RELATION", "binding": binding, "relation": relation, "field": field, "value": parameter.get("value")}


def _preflight_datum(scene, parameter, binding, resolved):
    obj = resolved.get("target")
    if obj is None:
        raise ValueError("datum/reference target not found during apply preflight")
    guide_kind = obj.get("oleander_guide_kind", "")
    field = binding.get("target_field", "")
    if field not in DATUM_FIELDS.get(guide_kind, set()):
        raise ValueError(f"unsupported DATUM_REFERENCE apply field: {guide_kind}.{field}")
    _require_kind(parameter, "LENGTH_MM", field)
    value = float(parameter.get("value"))
    if field in {"length_mm", "size_mm"} and value <= 0.0:
        raise ValueError(f"{field} must be greater than zero")
    if obj.type != "MESH":
        raise ValueError("datum/reference apply requires editable mesh guide geometry")
    return {"kind": "DATUM_REFERENCE", "binding": binding, "object": obj, "guide_kind": guide_kind, "field": field, "value": value}


def _build_apply_plan(scene, parameter_id):
    parameters = get_design_parameters(scene)
    parameter = _parameter_by_id(parameters, parameter_id)
    if parameter is None:
        raise ValueError(f"design parameter not found: {parameter_id}")
    envelope = evaluate_failure_envelope(parameter)
    if envelope.get("status") in {"FAIL", "INVALID"}:
        raise ValueError(f"design parameter outside valid failure envelope: {parameter_id}")
    graph_audit = audit_design_intent_graph(scene)
    if graph_audit.get("status") != "PASS":
        raise ValueError("design intent graph must audit PASS before explicit apply")
    bindings = list(parameter.get("bindings", []))
    if not bindings:
        raise ValueError(f"design parameter has no bindings to apply: {parameter_id}")

    plan = []
    for binding in bindings:
        resolved = resolve_binding(scene, binding)
        if not resolved.get("valid"):
            raise ValueError(f"design-intent target not found: {binding.get('target_kind')}:{binding.get('target_id')}")
        target_kind = binding.get("target_kind", "")
        if target_kind == "OBJECT":
            item = _preflight_object(scene, parameter, binding, resolved)
        elif target_kind == "FEATURE":
            item = _preflight_feature(scene, parameter, binding, resolved)
        elif target_kind == "RELATION":
            item = _preflight_relation(scene, parameter, binding, resolved)
        elif target_kind == "DATUM_REFERENCE":
            item = _preflight_datum(scene, parameter, binding, resolved)
        else:
            raise ValueError(f"unsupported design-intent apply target kind: {target_kind}")
        plan.append(item)
    return parameter, plan, graph_audit


def preflight_design_parameter_apply(scene, parameter_id):
    parameter, plan, graph_audit = _build_apply_plan(scene, parameter_id)
    return {
        "schema": APPLY_SCHEMA,
        "status": "PASS",
        "parameter_id": parameter_id,
        "parameter_revision": int(parameter.get("revision", 0)),
        "binding_count": len(plan),
        "target_kinds": [item["kind"] for item in plan],
        "graph_audit": graph_audit.get("status"),
        "solver_claim": False,
        "automatic_parameter_geometry_rebuild": False,
        "cad_parametric_feature_rebuild_claim": False,
    }


def _snapshot_item(item):
    kind = item["kind"]
    if kind == "OBJECT":
        obj = item["object"]
        return {
            "kind": kind,
            "object": obj,
            "data_ref": obj.data,
            "matrix_world": obj.matrix_world.copy(),
            "vertex_coords": [vertex.co.copy() for vertex in obj.data.vertices],
        }
    if kind == "FEATURE":
        obj = item["object"]
        modifier = item["modifier"]
        field = item["field"]
        state = {"kind": kind, "object": obj, "history_raw": obj.get(FEATURE_HISTORY_KEY, "[]"), "modifier": modifier, "field": field}
        if field in {"depth_mm", "thickness_mm"}:
            state["modifier_value"] = float(modifier.thickness)
        elif field == "width_mm":
            state["modifier_value"] = float(modifier.width)
        elif field == "count":
            state["modifier_value"] = int(modifier.count)
        elif field == "spacing_mm":
            state["modifier_value"] = tuple(modifier.constant_offset_displace)
        return state
    if kind == "RELATION":
        return {"kind": kind, "scene": bpy.context.scene, "relations_raw": bpy.context.scene.get(RELATIONS_KEY, "[]")}
    obj = item["object"]
    props = {
        key: obj.get(key)
        for key in (
            "oleander_datum_length_mm",
            "oleander_datum_size_mm",
            "oleander_construction_length_mm",
            "oleander_construction_offset_mm",
        )
        if key in obj
    }
    return {"kind": kind, "object": obj, "vertex_coords": [vertex.co.copy() for vertex in obj.data.vertices], "props": props}


def _restore_snapshot(snapshot):
    kind = snapshot["kind"]
    if kind == "OBJECT":
        obj = snapshot["object"]
        original = snapshot["data_ref"]
        current = obj.data
        if current != original:
            obj.data = original
            if current.users == 0:
                bpy.data.meshes.remove(current)
        if len(original.vertices) == len(snapshot["vertex_coords"]):
            for vertex, coordinate in zip(original.vertices, snapshot["vertex_coords"]):
                vertex.co = coordinate
        obj.matrix_world = snapshot["matrix_world"]
        return
    if kind == "FEATURE":
        obj = snapshot["object"]
        modifier = snapshot["modifier"]
        obj[FEATURE_HISTORY_KEY] = snapshot["history_raw"]
        field = snapshot["field"]
        if field in {"depth_mm", "thickness_mm"}:
            modifier.thickness = snapshot["modifier_value"]
        elif field == "width_mm":
            modifier.width = snapshot["modifier_value"]
        elif field == "count":
            modifier.count = snapshot["modifier_value"]
        elif field == "spacing_mm":
            modifier.constant_offset_displace = Vector(snapshot["modifier_value"])
        return
    if kind == "RELATION":
        snapshot["scene"][RELATIONS_KEY] = snapshot["relations_raw"]
        return
    obj = snapshot["object"]
    if len(obj.data.vertices) == len(snapshot["vertex_coords"]):
        for vertex, coordinate in zip(obj.data.vertices, snapshot["vertex_coords"]):
            vertex.co = coordinate
    for key in (
        "oleander_datum_length_mm",
        "oleander_datum_size_mm",
        "oleander_construction_length_mm",
        "oleander_construction_offset_mm",
    ):
        if key in snapshot["props"]:
            obj[key] = snapshot["props"][key]
        elif key in obj:
            del obj[key]


def _write_feature_history(obj, history):
    obj[FEATURE_HISTORY_KEY] = json.dumps(history, sort_keys=True, ensure_ascii=False)


def _apply_object(scene, item):
    obj = item["object"]
    field = item["field"]
    value = float(item["value"])
    axis = OBJECT_FIELDS[field]
    target_dimensions = obj.dimensions.copy()
    target_dimensions[axis] = _mm_to_scene_units(bpy.context, value)
    if obj.data.users > 1:
        obj.data = obj.data.copy()
    obj.dimensions = target_dimensions
    bpy.context.view_layer.update()
    _apply_object_scale(bpy.context, obj)
    bpy.context.view_layer.update()
    return {"target_kind": "OBJECT", "target_id": object_id(obj), "field": field, "value": value, "model_geometry_mutated": True}


def _apply_feature(scene, item):
    obj = item["object"]
    feature_id = item["binding"]["target_id"]
    history = get_feature_history(obj)
    index = next((idx for idx, entry in enumerate(history) if entry.get("feature_id") == feature_id), -1)
    if index < 0:
        raise ValueError(f"feature disappeared during apply: {feature_id}")
    entry = history[index]
    modifier = obj.modifiers.get(entry.get("modifier_name", ""))
    if modifier is None:
        raise ValueError(f"feature modifier disappeared during apply: {feature_id}")
    field = item["field"]
    value = item["value"]
    params = dict(entry.get("parameters", {}))
    if field == "depth_mm":
        modifier.thickness = _mm_to_scene_units(bpy.context, float(value))
        params[field] = float(value)
    elif field == "thickness_mm":
        modifier.thickness = _mm_to_scene_units(bpy.context, float(value))
        params[field] = float(value)
    elif field == "width_mm":
        modifier.width = _mm_to_scene_units(bpy.context, float(value))
        params[field] = float(value)
    elif field == "count":
        modifier.count = int(value)
        params[field] = int(value)
    elif field == "spacing_mm":
        axis = params.get("axis", "X")
        offset = Vector((0.0, 0.0, 0.0))
        offset[{"X": 0, "Y": 1, "Z": 2}[axis]] = _mm_to_scene_units(bpy.context, float(value))
        modifier.use_relative_offset = False
        modifier.use_constant_offset = True
        modifier.constant_offset_displace = offset
        params[field] = float(value)
    else:
        raise ValueError(f"unsupported feature field reached apply: {field}")
    entry["parameters"] = params
    entry["edit_revision"] = int(entry.get("edit_revision", 0)) + 1
    entry["last_design_parameter_id"] = item.get("parameter_id", "")
    history[index] = entry
    _write_feature_history(obj, history)
    bpy.context.view_layer.update()
    return {"target_kind": "FEATURE", "target_id": feature_id, "field": field, "value": value, "model_geometry_mutated": True}


def _apply_relation(scene, item):
    relation_id = item["binding"]["target_id"]
    relations = get_relations(scene)
    index = next((idx for idx, relation in enumerate(relations) if relation.get("relation_id") == relation_id), -1)
    if index < 0:
        raise ValueError(f"relation disappeared during apply: {relation_id}")
    field = item["field"]
    value = float(item["value"])
    relations[index][field] = value
    relations[index]["last_design_parameter_id"] = item.get("parameter_id", "")
    relations[index]["design_intent_apply_revision"] = int(relations[index].get("design_intent_apply_revision", 0)) + 1
    scene[RELATIONS_KEY] = json.dumps(relations, sort_keys=True, ensure_ascii=False)
    result = evaluate_relation(scene, relations[index])
    return {"target_kind": "RELATION", "target_id": relation_id, "field": field, "value": value, "relation_status": result.get("status"), "model_geometry_mutated": False}


def _apply_datum(scene, item):
    obj = item["object"]
    kind = item["guide_kind"]
    field = item["field"]
    value = float(item["value"])
    if kind == "DATUM_AXIS":
        axis = obj.get("oleander_datum_axis", "X")
        direction = Vector((1.0, 0.0, 0.0)) if axis == "X" else Vector((0.0, 1.0, 0.0)) if axis == "Y" else Vector((0.0, 0.0, 1.0))
        half = _mm_to_scene_units(bpy.context, value) * 0.5
        obj.data.vertices[0].co = -direction * half
        obj.data.vertices[1].co = direction * half
        obj["oleander_datum_length_mm"] = value
    elif kind == "DATUM_PLANE":
        plane = obj.get("oleander_datum_plane", "XY")
        half = _mm_to_scene_units(bpy.context, value) * 0.5
        coordinates = (
            [(-half, -half, 0), (half, -half, 0), (half, half, 0), (-half, half, 0)]
            if plane == "XY"
            else [(-half, 0, -half), (half, 0, -half), (half, 0, half), (-half, 0, half)]
            if plane == "XZ"
            else [(0, -half, -half), (0, half, -half), (0, half, half), (0, -half, half)]
        )
        for vertex, coordinate in zip(obj.data.vertices, coordinates):
            vertex.co = coordinate
        obj["oleander_datum_size_mm"] = value
    else:
        axis = obj.get("oleander_construction_axis", "X")
        length_mm = value if field == "length_mm" else float(obj.get("oleander_construction_length_mm", 0.0))
        offset_mm = value if field == "offset_mm" else float(obj.get("oleander_construction_offset_mm", 0.0))
        length = _mm_to_scene_units(bpy.context, length_mm)
        offset = _mm_to_scene_units(bpy.context, offset_mm)
        coordinates = (
            [(0, offset, 0), (length, offset, 0)]
            if axis == "X"
            else [(offset, 0, 0), (offset, length, 0)]
            if axis == "Y"
            else [(offset, 0, 0), (offset, 0, length)]
        )
        for vertex, coordinate in zip(obj.data.vertices, coordinates):
            vertex.co = coordinate
        obj["oleander_construction_length_mm"] = length_mm
        obj["oleander_construction_offset_mm"] = offset_mm
    obj.data.update()
    return {"target_kind": "DATUM_REFERENCE", "target_id": item["binding"]["target_id"], "field": field, "value": value, "reference_geometry_mutated": True, "model_geometry_mutated": False}


def _apply_plan_item(scene, parameter, item):
    item["parameter_id"] = parameter.get("parameter_id", "")
    if item["kind"] == "OBJECT":
        return _apply_object(scene, item)
    if item["kind"] == "FEATURE":
        return _apply_feature(scene, item)
    if item["kind"] == "RELATION":
        return _apply_relation(scene, item)
    return _apply_datum(scene, item)


def _postcheck_plan(scene, parameter, plan):
    failures = []
    results = []
    target_value = parameter.get("value")
    for item in plan:
        kind = item["kind"]
        field = item["field"]
        if kind == "OBJECT":
            obj = item["object"]
            actual = _scene_units_to_mm(bpy.context, obj.dimensions[OBJECT_FIELDS[field]])
            ok = abs(actual - float(target_value)) <= 1e-4
        elif kind == "FEATURE":
            obj = item["object"]
            feature_id = item["binding"]["target_id"]
            entry = next((entry for entry in get_feature_history(obj) if entry.get("feature_id") == feature_id), None)
            modifier = obj.modifiers.get(entry.get("modifier_name", "")) if entry else None
            if entry is None or modifier is None:
                actual = None
                ok = False
            elif field in {"depth_mm", "thickness_mm"}:
                actual = _scene_units_to_mm(bpy.context, modifier.thickness)
                ok = abs(actual - float(target_value)) <= 1e-4
            elif field == "width_mm":
                actual = _scene_units_to_mm(bpy.context, modifier.width)
                ok = abs(actual - float(target_value)) <= 1e-4
            elif field == "count":
                actual = int(modifier.count)
                ok = actual == int(target_value)
            else:
                axis = entry.get("parameters", {}).get("axis", "X")
                actual = _scene_units_to_mm(bpy.context, modifier.constant_offset_displace[{"X": 0, "Y": 1, "Z": 2}[axis]])
                ok = abs(actual - float(target_value)) <= 1e-4
            if validate_feature_history(obj).get("status") != "PASS":
                ok = False
        elif kind == "RELATION":
            relation_id = item["binding"]["target_id"]
            relation = next((relation for relation in get_relations(scene) if relation.get("relation_id") == relation_id), None)
            actual = relation.get(field) if relation else None
            ok = relation is not None and abs(float(actual) - float(target_value)) <= 1e-9
        else:
            obj = item["object"]
            property_key = {
                ("DATUM_AXIS", "length_mm"): "oleander_datum_length_mm",
                ("DATUM_PLANE", "size_mm"): "oleander_datum_size_mm",
                ("CONSTRUCTION_LINE", "length_mm"): "oleander_construction_length_mm",
                ("CONSTRUCTION_LINE", "offset_mm"): "oleander_construction_offset_mm",
            }[(item["guide_kind"], field)]
            actual = obj.get(property_key)
            ok = actual is not None and abs(float(actual) - float(target_value)) <= 1e-9
        result = {"target_kind": kind, "target_id": item["binding"]["target_id"], "field": field, "actual": actual, "expected": target_value, "status": "PASS" if ok else "FAIL"}
        results.append(result)
        if not ok:
            failures.append(result)
    return {"status": "FAIL" if failures else "PASS", "results": results, "failures": failures, "solver_claim": False}


def _clear_direct_parameter_stale(scene, parameter_id, plan):
    reason = f"DESIGN_PARAMETER_CHANGED:{parameter_id}"
    for item in plan:
        if item["kind"] not in {"OBJECT", "FEATURE"}:
            continue
        obj = item["object"]
        obj["oleander_design_intent_stale"] = False
        obj["oleander_design_intent_last_applied_parameter"] = parameter_id
        if obj.get("oleander_stale_reason", "") == reason:
            obj["oleander_stale_reason"] = ""
            meta = getattr(obj, "oleander", None)
            if meta is not None and hasattr(meta, "stale"):
                meta.stale = False


def apply_design_parameter(scene, parameter_id):
    parameter, plan, graph_audit = _build_apply_plan(scene, parameter_id)
    snapshots = [_snapshot_item(item) for item in plan]
    applied = []
    try:
        for item in plan:
            applied.append(_apply_plan_item(scene, parameter, item))
        postcheck = _postcheck_plan(scene, parameter, plan)
        if postcheck.get("status") != "PASS":
            raise ValueError("design-intent apply postcheck failed")
    except Exception as exc:
        for snapshot in reversed(snapshots):
            _restore_snapshot(snapshot)
        for view_layer in scene.view_layers:
            view_layer.update()
        event = _append_event(scene, "APPLY_ROLLBACK", parameter_id, {"reason": str(exc), "binding_count": len(plan)})
        result = {
            "schema": APPLY_SCHEMA,
            "status": "ROLLED_BACK",
            "parameter_id": parameter_id,
            "binding_count": len(plan),
            "rollback_performed": True,
            "reason": str(exc),
            "event_id": event["event_id"],
            "solver_claim": False,
            "automatic_parameter_geometry_rebuild": False,
            "cad_parametric_feature_rebuild_claim": False,
        }
        scene[LAST_APPLY_KEY] = json.dumps(result, sort_keys=True, ensure_ascii=False)
        raise ValueError(f"design-intent apply rolled back: {exc}") from exc

    model_impacted = []
    relation_driven = []
    for item in plan:
        if item["kind"] in {"OBJECT", "FEATURE"}:
            oid = object_id(item["object"])
            if oid and oid not in model_impacted:
                model_impacted.append(oid)
        elif item["kind"] == "RELATION":
            driven_id = item["relation"].get("driven_id", "")
            if driven_id and driven_id not in relation_driven:
                relation_driven.append(driven_id)
    downstream = mark_downstream_stale(model_impacted, reason=f"DESIGN_INTENT_APPLY:{parameter_id}", scene=scene) if model_impacted else []
    relation_results = [item for item in applied if item.get("target_kind") == "RELATION"]
    failed_relation_ids = [item["target_id"] for item in relation_results if item.get("relation_status") == "FAIL"]
    relation_downstream = []
    if failed_relation_ids:
        for oid in relation_driven:
            obj = _find_object_by_id(scene, oid)
            if obj is not None:
                meta = getattr(obj, "oleander", None)
                if meta is not None and hasattr(meta, "stale"):
                    meta.stale = True
                obj["oleander_stale_reason"] = f"DESIGN_INTENT_RELATION_FAIL:{','.join(failed_relation_ids)}"
        relation_downstream = mark_downstream_stale(relation_driven, reason=f"DESIGN_INTENT_RELATION_FAIL:{parameter_id}", scene=scene) if relation_driven else []
    _clear_direct_parameter_stale(scene, parameter_id, plan)
    event = _append_event(scene, "APPLY_COMMIT", parameter_id, {"applied": applied, "postcheck": postcheck, "downstream_stale": downstream, "relation_downstream_stale": relation_downstream})
    result = {
        "schema": APPLY_SCHEMA,
        "status": "PASS",
        "parameter_id": parameter_id,
        "parameter_revision": int(parameter.get("revision", 0)),
        "preflight": "PASS",
        "postcheck": postcheck,
        "bindings_applied": len(applied),
        "applied": applied,
        "model_geometry_mutated": any(item.get("model_geometry_mutated", False) for item in applied),
        "reference_geometry_mutated": any(item.get("reference_geometry_mutated", False) for item in applied),
        "metadata_mutated": any(item.get("target_kind") == "RELATION" for item in applied),
        "rollback_performed": False,
        "downstream_stale": downstream,
        "relation_downstream_stale": relation_downstream,
        "graph_audit_before": graph_audit.get("status"),
        "event_id": event["event_id"],
        "solver_claim": False,
        "automatic_parameter_geometry_rebuild": False,
        "cad_parametric_feature_rebuild_claim": False,
    }
    scene[LAST_APPLY_KEY] = json.dumps(result, sort_keys=True, ensure_ascii=False)
    return result


class OLEANDER_OT_preflight_design_parameter_apply(bpy.types.Operator):
    bl_idname = "oleander.preflight_design_parameter_apply"
    bl_label = "Preflight Parameter Apply"
    bl_options = {"REGISTER"}

    parameter_id: bpy.props.StringProperty(name="Parameter ID")

    def execute(self, context):
        try:
            result = preflight_design_parameter_apply(context.scene, self.parameter_id)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Apply preflight PASS: {result['binding_count']} binding(s)")
        return {"FINISHED"}


class OLEANDER_OT_apply_design_parameter(bpy.types.Operator):
    bl_idname = "oleander.apply_design_parameter"
    bl_label = "Explicitly Apply Parameter"
    bl_options = {"REGISTER", "UNDO"}

    parameter_id: bpy.props.StringProperty(name="Parameter ID")

    def execute(self, context):
        try:
            result = apply_design_parameter(context.scene, self.parameter_id)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Applied {result['bindings_applied']} binding(s); solver_claim=false")
        return {"FINISHED"}


class OLEANDER_PT_design_intent_apply(bpy.types.Panel):
    bl_label = "Design Intent Apply"
    bl_idname = "OLEANDER_PT_design_intent_apply"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OLEANDER"
    bl_parent_id = "OLEANDER_PT_design_intent"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Explicit transaction only", icon="INFO")
        layout.label(text="Preflight → apply → verify → rollback", icon="INFO")
        layout.label(text="No solver / no CAD parametric rebuild", icon="INFO")


OPERATOR_CLASSES = (
    OLEANDER_OT_preflight_design_parameter_apply,
    OLEANDER_OT_apply_design_parameter,
)
PANEL_CLASSES = (OLEANDER_PT_design_intent_apply,)
