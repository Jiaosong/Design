import json
import math

import bpy
from mathutils import Vector

from .dependency import build_dependency_graph, dependency_ids, mark_downstream_stale, object_id


RELATIONS_KEY = "oleander_relations"
RELATION_COUNTER_KEY = "oleander_relation_counter"
RELATION_TOMBSTONES_KEY = "oleander_relation_tombstones"
RELATION_EVENTS_KEY = "oleander_relation_events"
RELATION_EVENT_COUNTER_KEY = "oleander_relation_event_counter"

RELATION_TYPES = (
    ("ORIGIN_DISTANCE", "Origin Distance", "Check world-space origin distance against a governed millimetre target"),
    ("AXIS_OFFSET", "Axis Offset", "Check signed world-axis origin offset against a governed millimetre target"),
    ("ORIGIN_COINCIDENT", "Origin Coincident", "Check that two world-space origins are coincident within tolerance"),
    ("AXIS_PARALLEL", "Local Axis Parallel", "Check that selected local axes are parallel within angular tolerance"),
)

AXIS_ITEMS = (("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", ""))


def _read_json_list(owner, key):
    raw = owner.get(key, "[]")
    if isinstance(raw, list):
        return list(raw)
    try:
        value = json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return []
    return value if isinstance(value, list) else []


def _write_json_list(owner, key, value):
    owner[key] = json.dumps(value, sort_keys=True, ensure_ascii=False)


def get_relations(scene=None):
    scene = scene or bpy.context.scene
    return _read_json_list(scene, RELATIONS_KEY)


def get_relation_tombstones(scene=None):
    scene = scene or bpy.context.scene
    return _read_json_list(scene, RELATION_TOMBSTONES_KEY)


def get_relation_events(scene=None):
    scene = scene or bpy.context.scene
    return _read_json_list(scene, RELATION_EVENTS_KEY)


def _set_relations(scene, relations):
    _write_json_list(scene, RELATIONS_KEY, relations)


def _set_dependencies(obj, ids):
    value = ",".join(ids)
    meta = getattr(obj, "oleander", None)
    if meta is not None and hasattr(meta, "dependencies"):
        meta.dependencies = value
    else:
        obj["oleander_dependencies"] = value


def _require_stable_ole_id(operator, obj, role):
    oid = getattr(getattr(obj, "oleander", None), "ole_id", "").strip()
    if oid:
        return oid
    operator.report({"ERROR"}, f"Relation {role} requires a stable OLE ID")
    return ""


def _find_object_by_id(scene, oid):
    for obj in scene.objects:
        if object_id(obj) == oid:
            return obj
    return None


def _axis_index(axis):
    return {"X": 0, "Y": 1, "Z": 2}[axis]


def _update_scene_transforms(scene):
    """Flush transform evaluation before measuring world-space relations.

    Headless Blender can retain a stale matrix_world immediately after scripted
    object creation or transform mutation. Relation checks therefore force a
    view-layer update instead of relying on UI redraw side effects.
    """
    for view_layer in scene.view_layers:
        view_layer.update()


def _scene_value_to_mm(scene, value_scene):
    scale_length = scene.unit_settings.scale_length or 1.0
    return value_scene * scale_length * 1000.0


def _world_axis(obj, axis):
    unit = Vector((0.0, 0.0, 0.0))
    unit[_axis_index(axis)] = 1.0
    vector = obj.matrix_world.to_3x3() @ unit
    if vector.length == 0.0:
        return unit
    return vector.normalized()


def _actual_metric(scene, driver, driven, kind, axis):
    _update_scene_transforms(scene)
    driver_origin = driver.matrix_world.translation
    driven_origin = driven.matrix_world.translation
    delta = driven_origin - driver_origin

    if kind in {"ORIGIN_DISTANCE", "ORIGIN_COINCIDENT"}:
        return "mm", _scene_value_to_mm(scene, delta.length)
    if kind == "AXIS_OFFSET":
        return "mm", _scene_value_to_mm(scene, delta[_axis_index(axis)])
    if kind == "AXIS_PARALLEL":
        a = _world_axis(driver, axis)
        b = _world_axis(driven, axis)
        dot = max(-1.0, min(1.0, abs(a.dot(b))))
        return "deg", math.degrees(math.acos(dot))
    raise ValueError(f"unsupported relation kind: {kind}")


def _relation_target(kind, target_mm):
    if kind in {"ORIGIN_COINCIDENT", "AXIS_PARALLEL"}:
        return 0.0
    return float(target_mm)


def evaluate_relation(scene, relation):
    driver_id = relation.get("driver_id", "")
    driven_id = relation.get("driven_id", "")
    driver = _find_object_by_id(scene, driver_id)
    driven = _find_object_by_id(scene, driven_id)

    if not relation.get("active", True):
        return {
            "relation_id": relation.get("relation_id", ""),
            "status": "SUPPRESSED",
            "reason": "RELATION_INACTIVE",
            "driver_id": driver_id,
            "driven_id": driven_id,
        }
    if driver is None or driven is None:
        missing = []
        if driver is None:
            missing.append("driver")
        if driven is None:
            missing.append("driven")
        return {
            "relation_id": relation.get("relation_id", ""),
            "status": "FAIL",
            "reason": "MISSING_OBJECT",
            "missing": missing,
            "driver_id": driver_id,
            "driven_id": driven_id,
        }

    kind = relation.get("kind", "")
    axis = relation.get("axis", "X")
    unit, actual = _actual_metric(scene, driver, driven, kind, axis)
    target = _relation_target(kind, relation.get("target_mm", 0.0))
    tolerance = float(relation.get("tolerance_deg", 0.1) if unit == "deg" else relation.get("tolerance_mm", 0.1))
    deviation = abs(actual - target)
    status = "PASS" if deviation <= tolerance else "FAIL"
    return {
        "relation_id": relation.get("relation_id", ""),
        "status": status,
        "reason": "WITHIN_TOLERANCE" if status == "PASS" else "OUT_OF_TOLERANCE",
        "kind": kind,
        "axis": axis,
        "driver_id": driver_id,
        "driven_id": driven_id,
        "unit": unit,
        "actual": actual,
        "target": target,
        "deviation": deviation,
        "tolerance": tolerance,
    }


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


def _dependency_reaches(graph, start_id, target_id):
    forward = graph["forward"]
    stack = [start_id]
    seen = set()
    while stack:
        current = stack.pop()
        if current == target_id:
            return True
        if current in seen:
            continue
        seen.add(current)
        stack.extend(forward.get(current, ()))
    return False


def would_create_relation_cycle(scene, driver_id, driven_id):
    graph = build_dependency_graph(scene)
    return _dependency_reaches(graph, driver_id, driven_id)


def _duplicate_relation(relations, driver_id, driven_id, kind, axis):
    return any(
        relation.get("active", True)
        and relation.get("driver_id") == driver_id
        and relation.get("driven_id") == driven_id
        and relation.get("kind") == kind
        and relation.get("axis", "X") == axis
        for relation in relations
    )


def create_relation(scene, driver, driven, kind, axis="X", target_mm=0.0, tolerance_mm=0.1, tolerance_deg=0.1, capture_current=False):
    driver_id = getattr(getattr(driver, "oleander", None), "ole_id", "").strip()
    driven_id = getattr(getattr(driven, "oleander", None), "ole_id", "").strip()
    if not driver_id or not driven_id:
        raise ValueError("driver and driven require stable OLE IDs")
    if driver_id == driven_id:
        raise ValueError("relation driver and driven must be different OLE IDs")
    if kind not in {item[0] for item in RELATION_TYPES}:
        raise ValueError(f"unsupported relation kind: {kind}")
    if axis not in {"X", "Y", "Z"}:
        raise ValueError(f"unsupported axis: {axis}")
    if tolerance_mm < 0.0 or tolerance_deg < 0.0:
        raise ValueError("relation tolerances must be non-negative")
    if kind == "ORIGIN_DISTANCE" and target_mm < 0.0 and not capture_current:
        raise ValueError("origin distance target cannot be negative")
    if would_create_relation_cycle(scene, driver_id, driven_id):
        raise ValueError("relation dependency would create a cycle")

    relations = get_relations(scene)
    if _duplicate_relation(relations, driver_id, driven_id, kind, axis):
        raise ValueError("duplicate active relation for driver/driven/kind/axis")

    if capture_current and kind in {"ORIGIN_DISTANCE", "AXIS_OFFSET"}:
        unit, actual = _actual_metric(scene, driver, driven, kind, axis)
        if unit != "mm":
            raise ValueError("capture_current is only valid for millimetre relations")
        target_mm = actual

    counter = int(scene.get(RELATION_COUNTER_KEY, 0)) + 1
    scene[RELATION_COUNTER_KEY] = counter
    relation_id = f"OLE_REL::R{counter:04d}"

    current_dependencies = dependency_ids(driven)
    dependency_added = driver_id not in current_dependencies
    if dependency_added:
        _set_dependencies(driven, current_dependencies + [driver_id])

    relation = {
        "relation_id": relation_id,
        "relation_index": counter,
        "kind": kind,
        "axis": axis,
        "driver_id": driver_id,
        "driven_id": driven_id,
        "target_mm": float(target_mm),
        "tolerance_mm": float(tolerance_mm),
        "tolerance_deg": float(tolerance_deg),
        "active": True,
        "dependency_added_by_relation": dependency_added,
        "solver_claim": False,
        "geometry_authority": "BLENDER_RELATION_CHECK_ONLY",
    }
    relations.append(relation)
    _set_relations(scene, relations)
    _append_event(scene, "ADD", relation_id, {"driver_id": driver_id, "driven_id": driven_id, "kind": kind})
    return relation


def audit_relations(scene=None, propagate_stale=True):
    scene = scene or bpy.context.scene
    relations = get_relations(scene)
    results = []
    for relation in relations:
        result = evaluate_relation(scene, relation)
        results.append(result)
        relation["last_result"] = result
        if propagate_stale and result.get("status") == "FAIL":
            driven = _find_object_by_id(scene, relation.get("driven_id", ""))
            if driven is not None:
                meta = getattr(driven, "oleander", None)
                if meta is not None and hasattr(meta, "stale"):
                    meta.stale = True
                driven["oleander_stale_reason"] = f"RELATION_FAIL:{relation.get('relation_id', '')}"
                mark_downstream_stale(
                    [relation.get("driven_id", "")],
                    reason=f"RELATION_FAIL:{relation.get('relation_id', '')}",
                    scene=scene,
                )
    _set_relations(scene, relations)
    summary = {
        "status": "FAIL" if any(result.get("status") == "FAIL" for result in results) else "PASS",
        "relation_count": len(results),
        "pass_count": sum(result.get("status") == "PASS" for result in results),
        "fail_count": sum(result.get("status") == "FAIL" for result in results),
        "suppressed_count": sum(result.get("status") == "SUPPRESSED" for result in results),
        "results": results,
    }
    scene["oleander_relation_audit"] = json.dumps(summary, sort_keys=True)
    return summary


def remove_relation(scene, relation_id):
    relations = get_relations(scene)
    index = next((i for i, relation in enumerate(relations) if relation.get("relation_id") == relation_id), -1)
    if index < 0:
        raise ValueError(f"relation not found: {relation_id}")
    removed = relations.pop(index)

    removed_dependency = False
    if removed.get("dependency_added_by_relation"):
        same_dependency_still_required = any(
            relation.get("active", True)
            and relation.get("driver_id") == removed.get("driver_id")
            and relation.get("driven_id") == removed.get("driven_id")
            for relation in relations
        )
        if not same_dependency_still_required:
            driven = _find_object_by_id(scene, removed.get("driven_id", ""))
            if driven is not None:
                current = dependency_ids(driven)
                driver_id = removed.get("driver_id", "")
                if driver_id in current:
                    _set_dependencies(driven, [item for item in current if item != driver_id])
                    removed_dependency = True

    tombstone = dict(removed)
    tombstone["active"] = False
    tombstone["tombstone_state"] = "REMOVED"
    tombstone["dependency_removed_with_relation"] = removed_dependency
    tombstones = get_relation_tombstones(scene)
    tombstones.append(tombstone)
    _write_json_list(scene, RELATION_TOMBSTONES_KEY, tombstones)
    _set_relations(scene, relations)
    _append_event(scene, "REMOVE", relation_id, {"dependency_removed": removed_dependency})
    return tombstone


class OLEANDER_OT_add_relation(bpy.types.Operator):
    """Create a governed driver→driven relation without claiming solver authority."""

    bl_idname = "oleander.add_relation"
    bl_label = "Add Governed Relation"
    bl_options = {"REGISTER", "UNDO"}

    kind: bpy.props.EnumProperty(name="Relation", items=RELATION_TYPES, default="ORIGIN_DISTANCE")
    axis: bpy.props.EnumProperty(name="Axis", items=AXIS_ITEMS, default="X")
    target_mm: bpy.props.FloatProperty(name="Target mm", default=0.0)
    tolerance_mm: bpy.props.FloatProperty(name="Tolerance mm", default=0.1, min=0.0)
    tolerance_deg: bpy.props.FloatProperty(name="Tolerance deg", default=0.1, min=0.0)
    capture_current: bpy.props.BoolProperty(name="Capture Current", default=True)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.mode == "OBJECT"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Active object = Driven")
        layout.label(text="Other selected object = Driver")
        layout.prop(self, "kind")
        if self.kind in {"AXIS_OFFSET", "AXIS_PARALLEL"}:
            layout.prop(self, "axis")
        if self.kind in {"ORIGIN_DISTANCE", "AXIS_OFFSET"}:
            layout.prop(self, "capture_current")
            if not self.capture_current:
                layout.prop(self, "target_mm")
            layout.prop(self, "tolerance_mm")
        elif self.kind == "ORIGIN_COINCIDENT":
            layout.prop(self, "tolerance_mm")
        else:
            layout.prop(self, "tolerance_deg")
        layout.label(text="Check-only relation; solver_claim = false")

    def execute(self, context):
        driven = context.active_object
        drivers = [obj for obj in context.selected_objects if obj != driven]
        if len(drivers) != 1:
            self.report({"ERROR"}, "Relation requires exactly two selected objects: active Driven + one Driver")
            return {"CANCELLED"}
        driver = drivers[0]
        if not _require_stable_ole_id(self, driver, "driver") or not _require_stable_ole_id(self, driven, "driven"):
            return {"CANCELLED"}
        try:
            relation = create_relation(
                context.scene,
                driver,
                driven,
                self.kind,
                axis=self.axis,
                target_mm=self.target_mm,
                tolerance_mm=self.tolerance_mm,
                tolerance_deg=self.tolerance_deg,
                capture_current=self.capture_current,
            )
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        result = evaluate_relation(context.scene, relation)
        self.report({"INFO"}, f"Added {relation['relation_id']} {relation['kind']} → {result['status']}")
        return {"FINISHED"}


class OLEANDER_OT_audit_relations(bpy.types.Operator):
    """Evaluate every governed relation and propagate stale state on failures."""

    bl_idname = "oleander.audit_relations"
    bl_label = "Audit Governed Relations"
    bl_options = {"REGISTER"}

    def execute(self, context):
        summary = audit_relations(context.scene, propagate_stale=True)
        level = {"INFO"} if summary["status"] == "PASS" else {"WARNING"}
        self.report(level, f"Relation audit {summary['status']}: {summary['pass_count']} pass / {summary['fail_count']} fail")
        return {"FINISHED"}


class OLEANDER_OT_remove_relation(bpy.types.Operator):
    """Remove a governed relation while retaining a tombstone and dependency ownership evidence."""

    bl_idname = "oleander.remove_relation"
    bl_label = "Remove Governed Relation"
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
            remove_relation(context.scene, self.relation_id)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Removed {self.relation_id}; tombstone preserved")
        return {"FINISHED"}


class OLEANDER_PT_relation_kernel(bpy.types.Panel):
    bl_label = "Relation Kernel"
    bl_idname = "OLEANDER_PT_relation_kernel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OLEANDER"
    bl_parent_id = "OLEANDER_PT_runtime_panel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        relations = get_relations(scene)
        layout.label(text=f"Relations: {len(relations)}")
        layout.operator("oleander.add_relation")
        layout.operator("oleander.audit_relations")
        if relations:
            op = layout.operator("oleander.remove_relation")
            op.relation_id = relations[-1].get("relation_id", "")
        layout.label(text="Detection + governance only")
        layout.label(text="No solver / CAD authority")


OPERATOR_CLASSES = (
    OLEANDER_OT_add_relation,
    OLEANDER_OT_audit_relations,
    OLEANDER_OT_remove_relation,
)

PANEL_CLASSES = (OLEANDER_PT_relation_kernel,)
