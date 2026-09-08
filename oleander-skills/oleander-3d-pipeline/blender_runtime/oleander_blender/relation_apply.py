import json
import math

import bpy
from mathutils import Vector

from .dependency import mark_downstream_stale, object_id
from .relation_kernel import (
    RELATION_EVENTS_KEY,
    RELATION_EVENT_COUNTER_KEY,
    RELATIONS_KEY,
    evaluate_relation,
    get_relation_events,
    get_relations,
)


REFERENCE_KEY = "apply_reference_direction_world"
REFERENCE_STATE_KEY = "apply_reference_state"
APPLY_MODE = "DETERMINISTIC_ONE_SHOT"
AXIS_PARALLEL_APPLY_POLICY = "NEAREST_POLARITY_SHORTEST_ROTATION"


def _write_json_list(owner, key, value):
    owner[key] = json.dumps(value, sort_keys=True, ensure_ascii=False)


def _set_relations(scene, relations):
    _write_json_list(scene, RELATIONS_KEY, relations)


def _find_relation(scene, relation_id):
    relations = get_relations(scene)
    for index, relation in enumerate(relations):
        if relation.get("relation_id") == relation_id:
            return relations, index, relation
    return relations, -1, None


def _find_object_by_id(scene, ole_id):
    for obj in scene.objects:
        if object_id(obj) == ole_id:
            return obj
    return None


def _update_scene_transforms(scene):
    for view_layer in scene.view_layers:
        view_layer.update()


def _mm_to_scene_value(scene, value_mm):
    scale_length = scene.unit_settings.scale_length or 1.0
    return (float(value_mm) / 1000.0) / scale_length


def _vector_payload(vector):
    return [float(vector.x), float(vector.y), float(vector.z)]


def _append_event(scene, action, relation_id, payload=None):
    counter = int(scene.get(RELATION_EVENT_COUNTER_KEY, 0)) + 1
    scene[RELATION_EVENT_COUNTER_KEY] = counter
    event = {
        "event_id": f"OLE_REL_EVT::E{counter:04d}",
        "event_index": counter,
        "action": action,
        "relation_id": relation_id,
        "payload": payload or {},
    }
    events = get_relation_events(scene)
    events.append(event)
    _write_json_list(scene, RELATION_EVENTS_KEY, events)
    return event


def _require_relation_objects(scene, relation):
    driver = _find_object_by_id(scene, relation.get("driver_id", ""))
    driven = _find_object_by_id(scene, relation.get("driven_id", ""))
    if driver is None or driven is None:
        missing = []
        if driver is None:
            missing.append("driver")
        if driven is None:
            missing.append("driven")
        raise ValueError("relation apply missing object: " + ",".join(missing))
    return driver, driven


def _world_axis(obj, axis):
    index = {"X": 0, "Y": 1, "Z": 2}[axis]
    unit = Vector((0.0, 0.0, 0.0))
    unit[index] = 1.0
    vector = obj.matrix_world.to_3x3() @ unit
    if vector.length <= 1e-12:
        raise ValueError("AXIS_PARALLEL apply requires a non-degenerate world axis")
    return vector.normalized()


def capture_apply_reference(scene, relation_id):
    relations, index, relation = _find_relation(scene, relation_id)
    if relation is None:
        raise ValueError(f"relation not found: {relation_id}")
    if not relation.get("active", True):
        raise ValueError("cannot capture apply reference for inactive relation")
    if relation.get("kind") != "ORIGIN_DISTANCE":
        raise ValueError("apply reference capture is only required for ORIGIN_DISTANCE")

    result = evaluate_relation(scene, relation)
    if result.get("status") != "PASS":
        raise ValueError("ORIGIN_DISTANCE apply reference can only be captured while relation is PASS")

    driver, driven = _require_relation_objects(scene, relation)
    _update_scene_transforms(scene)
    delta = driven.matrix_world.translation - driver.matrix_world.translation
    if delta.length <= 1e-12 or float(relation.get("target_mm", 0.0)) <= 0.0:
        raise ValueError("ambiguous ORIGIN_DISTANCE direction; non-zero PASS geometry is required")

    direction = delta.normalized()
    relation[REFERENCE_KEY] = _vector_payload(direction)
    relation[REFERENCE_STATE_KEY] = "CAPTURED_FROM_PASS_GEOMETRY"
    relation["apply_mode"] = APPLY_MODE
    relation["apply_solver_claim"] = False
    relations[index] = relation
    _set_relations(scene, relations)
    event = _append_event(
        scene,
        "APPLY_REFERENCE_CAPTURE",
        relation_id,
        {
            "direction_world": relation[REFERENCE_KEY],
            "source_status": result.get("status"),
            "solver_claim": False,
        },
    )
    return relation, event


def _desired_world_origin(scene, relation, driver, driven):
    kind = relation.get("kind", "")
    axis = relation.get("axis", "X")
    driver_origin = driver.matrix_world.translation.copy()
    driven_origin = driven.matrix_world.translation.copy()

    if kind == "ORIGIN_COINCIDENT":
        return driver_origin

    if kind == "AXIS_OFFSET":
        desired = driven_origin.copy()
        axis_index = {"X": 0, "Y": 1, "Z": 2}[axis]
        desired[axis_index] = driver_origin[axis_index] + _mm_to_scene_value(scene, relation.get("target_mm", 0.0))
        return desired

    if kind == "ORIGIN_DISTANCE":
        raw = relation.get(REFERENCE_KEY)
        if not isinstance(raw, list) or len(raw) != 3:
            raise ValueError("ORIGIN_DISTANCE apply requires a captured PASS reference direction")
        direction = Vector((float(raw[0]), float(raw[1]), float(raw[2])))
        if direction.length <= 1e-12:
            raise ValueError("ambiguous ORIGIN_DISTANCE reference direction")
        direction.normalize()
        return driver_origin + direction * _mm_to_scene_value(scene, relation.get("target_mm", 0.0))

    raise ValueError(f"relation kind is not supported for deterministic one-shot translation apply: {kind}")


def _axis_parallel_world_matrix(relation, driver, driven, before_matrix):
    axis = relation.get("axis", "X")
    driver_axis = _world_axis(driver, axis)
    driven_axis = _world_axis(driven, axis)

    # AXIS_PARALLEL is polarity-insensitive in the relation kernel. Preserve
    # that contract by selecting whichever driver polarity is already nearest
    # to the driven axis, then apply only the shortest rotation needed to
    # remove angular deviation. No extra twist about the target axis is chosen.
    dot = max(-1.0, min(1.0, driven_axis.dot(driver_axis)))
    target_axis = driver_axis if dot >= 0.0 else -driver_axis
    delta_rotation = driven_axis.rotation_difference(target_axis)

    next_matrix = delta_rotation.to_matrix().to_4x4() @ before_matrix
    next_matrix.translation = before_matrix.translation.copy()
    payload = {
        "axis": axis,
        "policy": AXIS_PARALLEL_APPLY_POLICY,
        "before_world_axis": _vector_payload(driven_axis),
        "target_world_axis": _vector_payload(target_axis),
        "rotation_delta_deg": float(math.degrees(delta_rotation.angle)),
        "position_preserved": True,
        "twist_solver_claim": False,
    }
    return next_matrix, payload


def apply_relation_once(scene, relation_id):
    relations, index, relation = _find_relation(scene, relation_id)
    if relation is None:
        raise ValueError(f"relation not found: {relation_id}")
    if not relation.get("active", True):
        raise ValueError("cannot apply inactive relation")

    driver, driven = _require_relation_objects(scene, relation)
    if len(driven.constraints) > 0:
        raise ValueError("relation apply blocked: Driven has Blender constraints and external transform authority")

    _update_scene_transforms(scene)
    before_matrix = driven.matrix_world.copy()
    before_origin = before_matrix.translation.copy()
    kind = relation.get("kind", "")
    rotation_payload = None

    if kind == "AXIS_PARALLEL":
        next_matrix, rotation_payload = _axis_parallel_world_matrix(relation, driver, driven, before_matrix)
        desired_origin = before_origin.copy()
    else:
        desired_origin = _desired_world_origin(scene, relation, driver, driven)
        next_matrix = before_matrix.copy()
        next_matrix.translation = desired_origin

    driven.matrix_world = next_matrix
    _update_scene_transforms(scene)

    result = evaluate_relation(scene, relation)
    if result.get("status") != "PASS":
        driven.matrix_world = before_matrix
        _update_scene_transforms(scene)
        raise ValueError(
            f"deterministic relation apply did not produce PASS: {result.get('reason', 'UNKNOWN')}"
        )

    downstream = mark_downstream_stale(
        [relation.get("driven_id", "")],
        reason=f"RELATION_APPLY:{relation_id}",
        scene=scene,
    )
    relation["last_apply_result"] = result
    relation["apply_mode"] = APPLY_MODE
    relation["apply_solver_claim"] = False
    relation["apply_revision"] = int(relation.get("apply_revision", 0)) + 1
    if rotation_payload is not None:
        relation["axis_parallel_apply_policy"] = AXIS_PARALLEL_APPLY_POLICY
        relation["axis_parallel_twist_solver_claim"] = False
    relations[index] = relation
    _set_relations(scene, relations)

    event_payload = {
        "before_world_origin": _vector_payload(before_origin),
        "after_world_origin": _vector_payload(desired_origin),
        "result_status": result.get("status"),
        "apply_mode": APPLY_MODE,
        "solver_claim": False,
        "downstream_stale": downstream,
    }
    if rotation_payload is not None:
        event_payload["axis_parallel"] = rotation_payload
    event = _append_event(
        scene,
        "APPLY_ONE_SHOT",
        relation_id,
        event_payload,
    )
    driven["oleander_last_relation_apply"] = relation_id
    driven["oleander_last_relation_apply_event"] = event["event_id"]
    return result, event, downstream


class OLEANDER_OT_capture_relation_apply_reference(bpy.types.Operator):
    """Freeze a PASS ORIGIN_DISTANCE direction for later deterministic restore."""

    bl_idname = "oleander.capture_relation_apply_reference"
    bl_label = "Capture Apply Reference"
    bl_options = {"REGISTER", "UNDO"}

    relation_id: bpy.props.StringProperty(name="Relation ID")

    @classmethod
    def poll(cls, context):
        return bool(get_relations(context.scene))

    def invoke(self, context, event):
        relations = get_relations(context.scene)
        if not self.relation_id and relations:
            self.relation_id = relations[-1].get("relation_id", "")
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        try:
            capture_apply_reference(context.scene, self.relation_id)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Captured PASS direction for {self.relation_id}")
        return {"FINISHED"}


class OLEANDER_OT_apply_relation_once(bpy.types.Operator):
    """Apply one deterministic relation correction without iterative solving."""

    bl_idname = "oleander.apply_relation_once"
    bl_label = "Apply Relation Once"
    bl_options = {"REGISTER", "UNDO"}

    relation_id: bpy.props.StringProperty(name="Relation ID")

    @classmethod
    def poll(cls, context):
        return bool(get_relations(context.scene))

    def invoke(self, context, event):
        relations = get_relations(context.scene)
        if not self.relation_id and relations:
            self.relation_id = relations[-1].get("relation_id", "")
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        try:
            result, _, downstream = apply_relation_once(context.scene, self.relation_id)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Applied {self.relation_id} once → {result['status']}; downstream stale: {len(downstream)}")
        return {"FINISHED"}


class OLEANDER_PT_relation_apply(bpy.types.Panel):
    bl_label = "Relation Apply"
    bl_idname = "OLEANDER_PT_relation_apply"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OLEANDER"
    bl_parent_id = "OLEANDER_PT_relation_kernel"

    def draw(self, context):
        layout = self.layout
        relations = get_relations(context.scene)
        if not relations:
            layout.label(text="No active relations")
            return
        relation = relations[-1]
        relation_id = relation.get("relation_id", "")
        layout.label(text=f"Latest: {relation_id}")
        if relation.get("kind") == "ORIGIN_DISTANCE":
            op = layout.operator("oleander.capture_relation_apply_reference")
            op.relation_id = relation_id
        op = layout.operator("oleander.apply_relation_once")
        op.relation_id = relation_id
        layout.label(text="Deterministic one-shot only")
        layout.label(text="solver_claim = false")


OPERATOR_CLASSES = (
    OLEANDER_OT_capture_relation_apply_reference,
    OLEANDER_OT_apply_relation_once,
)

PANEL_CLASSES = (OLEANDER_PT_relation_apply,)