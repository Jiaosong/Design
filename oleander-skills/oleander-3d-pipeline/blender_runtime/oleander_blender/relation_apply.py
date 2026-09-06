import json

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

    if kind == "AXIS_PARALLEL":
        raise ValueError("AXIS_PARALLEL apply is multi-solution and intentionally unsupported")

    raise ValueError(f"relation kind is not supported for deterministic one-shot apply: {kind}")


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
    relations[index] = relation
    _set_relations(scene, relations)

    event = _append_event(
        scene,
        "APPLY_ONE_SHOT",
        relation_id,
        {
            "before_world_origin": _vector_payload(before_origin),
            "after_world_origin": _vector_payload(desired_origin),
            "result_status": result.get("status"),
            "apply_mode": APPLY_MODE,
            "solver_claim": False,
            "downstream_stale": downstream,
        },
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
