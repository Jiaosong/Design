import json

import bpy
from mathutils import Vector

from .dependency import dependency_ids, mark_downstream_stale, object_id
from .direct_model import _mm_to_scene_units, _scene_units_to_mm
from .feature_stack import get_feature_history, validate_feature_history


FEATURE_HISTORY_KEY = "oleander_feature_history"
FEATURE_TOMBSTONES_KEY = "oleander_feature_tombstones"
FEATURE_EVENTS_KEY = "oleander_feature_events"
FEATURE_EVENT_COUNTER_KEY = "oleander_feature_event_counter"


def _read_json_list(obj, key):
    raw = obj.get(key, "[]")
    if isinstance(raw, list):
        return list(raw)
    try:
        value = json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return []
    return value if isinstance(value, list) else []


def _write_json_list(obj, key, value):
    obj[key] = json.dumps(value, sort_keys=True, ensure_ascii=False)


def get_feature_tombstones(obj):
    return _read_json_list(obj, FEATURE_TOMBSTONES_KEY)


def get_feature_events(obj):
    return _read_json_list(obj, FEATURE_EVENTS_KEY)


def _set_feature_history(obj, history):
    _write_json_list(obj, FEATURE_HISTORY_KEY, history)


def _find_feature(obj, feature_id):
    history = get_feature_history(obj)
    for index, entry in enumerate(history):
        if entry.get("feature_id") == feature_id:
            return history, index, entry
    return history, -1, None


def _default_feature_id(obj):
    history = get_feature_history(obj)
    return history[-1].get("feature_id", "") if history else ""


def _sync_stack_indices(obj, history):
    for entry in history:
        entry["stack_index"] = obj.modifiers.find(entry.get("modifier_name", ""))
    history.sort(key=lambda entry: entry.get("stack_index", 10**9))
    _set_feature_history(obj, history)


def _append_event(context, obj, action, feature_id, payload=None):
    counter = int(obj.get(FEATURE_EVENT_COUNTER_KEY, 0)) + 1
    obj[FEATURE_EVENT_COUNTER_KEY] = counter
    oid = object_id(obj)
    event = {
        "event_id": f"{oid}::E{counter:04d}",
        "event_index": counter,
        "action": action,
        "feature_id": feature_id,
        "payload": payload or {},
    }
    events = get_feature_events(obj)
    events.append(event)
    _write_json_list(obj, FEATURE_EVENTS_KEY, events)
    downstream = mark_downstream_stale(
        [oid],
        reason=f"FEATURE_{action}",
        scene=context.scene,
    )
    obj["oleander_last_feature_event"] = event["event_id"]
    obj["oleander_feature_edit_last_downstream_stale"] = json.dumps(downstream, sort_keys=True)
    return event


def _set_dependencies(obj, ids):
    value = ",".join(ids)
    meta = getattr(obj, "oleander", None)
    if meta is not None and hasattr(meta, "dependencies"):
        meta.dependencies = value
    else:
        obj["oleander_dependencies"] = value


def _cleanup_removed_feature_dependencies(obj, removed_entry, remaining_history):
    params = removed_entry.get("parameters", {})
    if not bool(params.get("dependency_added_by_feature", False)):
        return []
    remaining_sources = {
        source_id
        for entry in remaining_history
        for source_id in entry.get("source_ids", [])
        if source_id
    }
    removable = {
        source_id
        for source_id in removed_entry.get("source_ids", [])
        if source_id and source_id not in remaining_sources
    }
    if not removable:
        return []
    current = dependency_ids(obj)
    updated = [item for item in current if item not in removable]
    _set_dependencies(obj, updated)
    return sorted(removable)


def _require_feature(operator, obj, feature_id):
    history, index, entry = _find_feature(obj, feature_id)
    if entry is None:
        operator.report({"ERROR"}, f"OLEANDER feature not found: {feature_id}")
        return history, -1, None, None
    modifier = obj.modifiers.get(entry.get("modifier_name", ""))
    if modifier is None:
        operator.report({"ERROR"}, f"Feature modifier missing: {entry.get('modifier_name', '')}")
        return history, index, entry, None
    return history, index, entry, modifier


def _populate_edit_properties(operator, context, obj, entry, modifier):
    kind = entry.get("kind", "")
    params = entry.get("parameters", {})
    operator.feature_id = entry.get("feature_id", "")
    if kind == "PLANAR_EXTRUDE":
        operator.value_mm = float(params.get("depth_mm", _scene_units_to_mm(context, modifier.thickness)))
    elif kind == "SHELL":
        operator.value_mm = float(params.get("thickness_mm", _scene_units_to_mm(context, modifier.thickness)))
        operator.offset_mode = params.get("offset_mode", "INSIDE")
    elif kind == "BEVEL_CHAMFER":
        operator.value_mm = float(params.get("width_mm", _scene_units_to_mm(context, modifier.width)))
        operator.segments = int(params.get("segments", modifier.segments))
    elif kind == "MIRROR":
        operator.axis = params.get("axis", "X")
        operator.merge = bool(params.get("merge", True))
    elif kind == "LINEAR_PATTERN":
        operator.count = int(params.get("count", modifier.count))
        operator.value_mm = float(params.get("spacing_mm", 0.0))
        operator.axis = params.get("axis", "X")
    elif kind.startswith("BOOLEAN_"):
        operator.operation = params.get("operation", modifier.operation)


class OLEANDER_OT_edit_feature_parameters(bpy.types.Operator):
    """Edit an existing governed feature by stable feature ID."""

    bl_idname = "oleander.edit_feature_parameters"
    bl_label = "Edit Feature Parameters"
    bl_options = {"REGISTER", "UNDO"}

    feature_id: bpy.props.StringProperty(name="Feature ID")
    value_mm: bpy.props.FloatProperty(name="Primary mm", default=10.0)
    count: bpy.props.IntProperty(name="Count", default=3, min=2, max=10000)
    segments: bpy.props.IntProperty(name="Segments", default=1, min=1, max=64)
    axis: bpy.props.EnumProperty(name="Axis", items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")], default="X")
    merge: bpy.props.BoolProperty(name="Merge", default=True)
    offset_mode: bpy.props.EnumProperty(
        name="Offset",
        items=[("INSIDE", "Inside", ""), ("CENTER", "Center", ""), ("OUTSIDE", "Outside", "")],
        default="INSIDE",
    )
    operation: bpy.props.EnumProperty(
        name="Boolean",
        items=[("DIFFERENCE", "Difference", ""), ("UNION", "Union", ""), ("INTERSECT", "Intersect", "")],
        default="DIFFERENCE",
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.mode == "OBJECT"

    def invoke(self, context, event):
        obj = context.active_object
        if not self.feature_id:
            self.feature_id = _default_feature_id(obj)
        history, index, entry, modifier = _require_feature(self, obj, self.feature_id)
        if modifier is None:
            return {"CANCELLED"}
        _populate_edit_properties(self, context, obj, entry, modifier)
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        history, index, entry = _find_feature(obj, self.feature_id)
        kind = entry.get("kind", "") if entry else "UNKNOWN"
        layout.label(text=f"Feature: {self.feature_id}")
        layout.label(text=f"Kind: {kind}")
        if kind in {"PLANAR_EXTRUDE", "SHELL", "BEVEL_CHAMFER", "LINEAR_PATTERN"}:
            label = {
                "PLANAR_EXTRUDE": "Depth mm",
                "SHELL": "Thickness mm",
                "BEVEL_CHAMFER": "Width mm",
                "LINEAR_PATTERN": "Spacing mm",
            }[kind]
            layout.prop(self, "value_mm", text=label)
        if kind == "SHELL":
            layout.prop(self, "offset_mode")
        elif kind == "BEVEL_CHAMFER":
            layout.prop(self, "segments")
        elif kind == "MIRROR":
            layout.prop(self, "axis")
            layout.prop(self, "merge")
        elif kind == "LINEAR_PATTERN":
            layout.prop(self, "count")
            layout.prop(self, "axis")
        elif kind.startswith("BOOLEAN_"):
            layout.prop(self, "operation")

    def execute(self, context):
        obj = context.active_object
        history, index, entry, modifier = _require_feature(self, obj, self.feature_id)
        if modifier is None:
            return {"CANCELLED"}
        kind = entry.get("kind", "")
        before = dict(entry.get("parameters", {}))
        params = dict(before)

        if kind == "PLANAR_EXTRUDE":
            if abs(self.value_mm) < 0.001:
                self.report({"ERROR"}, "Planar Extrude depth must be non-zero")
                return {"CANCELLED"}
            modifier.thickness = _mm_to_scene_units(context, self.value_mm)
            params["depth_mm"] = self.value_mm
        elif kind == "SHELL":
            if self.value_mm <= 0.0:
                self.report({"ERROR"}, "Shell thickness must be greater than zero")
                return {"CANCELLED"}
            modifier.thickness = _mm_to_scene_units(context, self.value_mm)
            modifier.offset = {"INSIDE": -1.0, "CENTER": 0.0, "OUTSIDE": 1.0}[self.offset_mode]
            params.update({"thickness_mm": self.value_mm, "offset_mode": self.offset_mode})
        elif kind == "BEVEL_CHAMFER":
            if self.value_mm <= 0.0:
                self.report({"ERROR"}, "Bevel/Chamfer width must be greater than zero")
                return {"CANCELLED"}
            modifier.width = _mm_to_scene_units(context, self.value_mm)
            modifier.segments = self.segments
            params.update({"width_mm": self.value_mm, "segments": self.segments})
        elif kind == "MIRROR":
            modifier.use_axis[0] = self.axis == "X"
            modifier.use_axis[1] = self.axis == "Y"
            modifier.use_axis[2] = self.axis == "Z"
            modifier.use_clip = self.merge
            modifier.use_mirror_merge = self.merge
            params.update({"axis": self.axis, "merge": self.merge})
        elif kind == "LINEAR_PATTERN":
            modifier.count = self.count
            offset = Vector((0.0, 0.0, 0.0))
            offset[{"X": 0, "Y": 1, "Z": 2}[self.axis]] = _mm_to_scene_units(context, self.value_mm)
            modifier.constant_offset_displace = offset
            params.update({"count": self.count, "spacing_mm": self.value_mm, "axis": self.axis})
        elif kind.startswith("BOOLEAN_"):
            modifier.operation = self.operation
            params["operation"] = self.operation
            entry["kind"] = f"BOOLEAN_{self.operation}"
        else:
            self.report({"ERROR"}, f"Feature kind is not editable by this operator: {kind}")
            return {"CANCELLED"}

        entry["parameters"] = params
        entry["edit_revision"] = int(entry.get("edit_revision", 0)) + 1
        history[index] = entry
        _set_feature_history(obj, history)
        _append_event(context, obj, "EDIT", self.feature_id, {"before": before, "after": params})
        self.report({"INFO"}, f"Edited governed feature {self.feature_id}")
        return {"FINISHED"}


class OLEANDER_OT_set_feature_suppressed(bpy.types.Operator):
    """Suppress or restore a governed feature without deleting its history."""

    bl_idname = "oleander.set_feature_suppressed"
    bl_label = "Suppress / Restore Feature"
    bl_options = {"REGISTER", "UNDO"}

    feature_id: bpy.props.StringProperty(name="Feature ID")
    state: bpy.props.EnumProperty(
        name="State",
        items=[("SUPPRESS", "Suppress", "Disable viewport/render evaluation"), ("RESTORE", "Restore", "Enable viewport/render evaluation")],
        default="SUPPRESS",
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.mode == "OBJECT"

    def invoke(self, context, event):
        if not self.feature_id:
            self.feature_id = _default_feature_id(context.active_object)
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        obj = context.active_object
        history, index, entry, modifier = _require_feature(self, obj, self.feature_id)
        if modifier is None:
            return {"CANCELLED"}
        suppressed = self.state == "SUPPRESS"
        modifier.show_viewport = not suppressed
        modifier.show_render = not suppressed
        entry["suppressed"] = suppressed
        history[index] = entry
        _set_feature_history(obj, history)
        _append_event(context, obj, self.state, self.feature_id, {"suppressed": suppressed})
        self.report({"INFO"}, f"{self.state.title()} feature {self.feature_id}")
        return {"FINISHED"}


class OLEANDER_OT_move_feature(bpy.types.Operator):
    """Move a governed feature in the modifier stack and update recorded order."""

    bl_idname = "oleander.move_feature"
    bl_label = "Move Feature"
    bl_options = {"REGISTER", "UNDO"}

    feature_id: bpy.props.StringProperty(name="Feature ID")
    direction: bpy.props.EnumProperty(name="Direction", items=[("UP", "Up", ""), ("DOWN", "Down", "")], default="UP")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.mode == "OBJECT"

    def invoke(self, context, event):
        if not self.feature_id:
            self.feature_id = _default_feature_id(context.active_object)
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        obj = context.active_object
        history, index, entry, modifier = _require_feature(self, obj, self.feature_id)
        if modifier is None:
            return {"CANCELLED"}
        current = obj.modifiers.find(modifier.name)
        target = current - 1 if self.direction == "UP" else current + 1
        if target < 0 or target >= len(obj.modifiers):
            self.report({"ERROR"}, f"Feature cannot move {self.direction.lower()} from stack index {current}")
            return {"CANCELLED"}
        obj.modifiers.move(current, target)
        _sync_stack_indices(obj, history)
        _append_event(context, obj, "REORDER", self.feature_id, {"from": current, "to": target})
        result = validate_feature_history(obj)
        if result.get("status") != "PASS":
            self.report({"ERROR"}, "Governed feature reorder produced invalid stack state")
            return {"CANCELLED"}
        self.report({"INFO"}, f"Moved feature {self.feature_id} {self.direction.lower()}")
        return {"FINISHED"}


class OLEANDER_OT_remove_feature(bpy.types.Operator):
    """Remove a governed feature while preserving a tombstone and event record."""

    bl_idname = "oleander.remove_feature"
    bl_label = "Remove Feature (Tombstone)"
    bl_options = {"REGISTER", "UNDO"}

    feature_id: bpy.props.StringProperty(name="Feature ID")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.mode == "OBJECT"

    def invoke(self, context, event):
        if not self.feature_id:
            self.feature_id = _default_feature_id(context.active_object)
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        obj = context.active_object
        history, index, entry, modifier = _require_feature(self, obj, self.feature_id)
        if modifier is None:
            return {"CANCELLED"}
        removed_entry = json.loads(json.dumps(entry))
        obj.modifiers.remove(modifier)
        history.pop(index)
        _sync_stack_indices(obj, history)
        removed_dependencies = _cleanup_removed_feature_dependencies(obj, removed_entry, history)

        tombstones = get_feature_tombstones(obj)
        tombstone = {
            "feature": removed_entry,
            "tombstone_index": len(tombstones) + 1,
            "removed_dependencies": removed_dependencies,
        }
        tombstones.append(tombstone)
        _write_json_list(obj, FEATURE_TOMBSTONES_KEY, tombstones)
        _append_event(
            context,
            obj,
            "REMOVE",
            self.feature_id,
            {"tombstone_index": tombstone["tombstone_index"], "removed_dependencies": removed_dependencies},
        )
        self.report({"INFO"}, f"Removed feature {self.feature_id}; tombstone preserved")
        return {"FINISHED"}


class OLEANDER_PT_feature_edit(bpy.types.Panel):
    bl_label = "OLEANDER Feature Edit"
    bl_idname = "OLEANDER_PT_feature_edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OLEANDER"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        if obj is None:
            layout.label(text="No active object")
            return
        history = get_feature_history(obj)
        tombstones = get_feature_tombstones(obj)
        events = get_feature_events(obj)
        layout.label(text=f"Active features: {len(history)}")
        layout.label(text=f"Tombstones: {len(tombstones)}")
        layout.label(text=f"Events: {len(events)}")
        if not history:
            layout.label(text="No governed features")
            return
        last = history[-1]
        layout.label(text=f"Last: {last.get('feature_id', '')}")
        layout.label(text=f"Kind: {last.get('kind', 'UNKNOWN')}")
        row = layout.row(align=True)
        row.operator("oleander.edit_feature_parameters", icon="PREFERENCES")
        row.operator("oleander.set_feature_suppressed", icon="HIDE_OFF")
        row = layout.row(align=True)
        move_up = row.operator("oleander.move_feature", text="Move Up", icon="TRIA_UP")
        move_up.direction = "UP"
        move_down = row.operator("oleander.move_feature", text="Move Down", icon="TRIA_DOWN")
        move_down.direction = "DOWN"
        layout.operator("oleander.remove_feature", icon="TRASH")


OPERATOR_CLASSES = (
    OLEANDER_OT_edit_feature_parameters,
    OLEANDER_OT_set_feature_suppressed,
    OLEANDER_OT_move_feature,
    OLEANDER_OT_remove_feature,
)

PANEL_CLASSES = (OLEANDER_PT_feature_edit,)
