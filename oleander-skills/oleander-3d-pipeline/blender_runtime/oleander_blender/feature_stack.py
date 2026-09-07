import json

import bpy
from mathutils import Vector

from .dependency import dependency_ids, mark_downstream_stale, object_id
from .direct_model import _mm_to_scene_units


FEATURE_HISTORY_KEY = "oleander_feature_history"
FEATURE_COUNTER_KEY = "oleander_feature_counter"


def _sanitize(value):
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, (list, tuple)):
        return [_sanitize(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _sanitize(item) for key, item in value.items()}
    return str(value)


def get_feature_history(obj):
    raw = obj.get(FEATURE_HISTORY_KEY, "[]")
    if isinstance(raw, list):
        return list(raw)
    try:
        value = json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return []
    return value if isinstance(value, list) else []


def _set_feature_history(obj, history):
    obj[FEATURE_HISTORY_KEY] = json.dumps(history, sort_keys=True, ensure_ascii=False)


def _require_ole_id(operator, obj):
    oid = getattr(getattr(obj, "oleander", None), "ole_id", "").strip()
    if oid:
        return oid
    operator.report({"ERROR"}, "OLEANDER feature operations require a stable OLE ID")
    return ""


def _allocate_feature(obj, kind):
    index = int(obj.get(FEATURE_COUNTER_KEY, 0)) + 1
    obj[FEATURE_COUNTER_KEY] = index
    oid = object_id(obj)
    feature_id = f"{oid}::F{index:03d}"
    modifier_name = f"OLE_F{index:03d}_{kind}"
    return index, feature_id, modifier_name


def _record_feature(context, obj, modifier, kind, parameters, source_ids=None):
    history = get_feature_history(obj)
    index = int(obj.get(FEATURE_COUNTER_KEY, len(history)))
    feature_id = f"{object_id(obj)}::F{index:03d}"
    stack_index = obj.modifiers.find(modifier.name)
    entry = {
        "feature_id": feature_id,
        "feature_index": index,
        "kind": kind,
        "modifier_name": modifier.name,
        "modifier_type": modifier.type,
        "stack_index": stack_index,
        "parameters": _sanitize(parameters),
        "source_ids": list(source_ids or []),
        "editable": True,
        "applied": False,
        "suppressed": False,
        "geometry_authority": "BLENDER_MODIFIER_NON_BREP",
    }
    history.append(entry)
    _set_feature_history(obj, history)

    downstream = mark_downstream_stale(
        [object_id(obj)],
        reason=f"DIRECT_FEATURE_{kind}",
        scene=context.scene,
    )
    obj["oleander_last_direct_operation"] = kind
    obj["oleander_last_feature_id"] = feature_id
    obj["oleander_feature_stack_last_downstream_stale"] = json.dumps(downstream, sort_keys=True)
    return entry, downstream


def validate_feature_history(obj):
    history = get_feature_history(obj)
    missing = []
    type_mismatch = []
    order_drift = []
    suppression_drift = []
    duplicate_feature_ids = []
    seen_ids = set()

    for entry in history:
        feature_id = entry.get("feature_id", "")
        if feature_id in seen_ids:
            duplicate_feature_ids.append(feature_id)
        seen_ids.add(feature_id)

        modifier_name = entry.get("modifier_name", "")
        modifier = obj.modifiers.get(modifier_name)
        if modifier is None:
            missing.append(feature_id or modifier_name)
            continue
        if modifier.type != entry.get("modifier_type"):
            type_mismatch.append(feature_id or modifier_name)
        current_index = obj.modifiers.find(modifier_name)
        if current_index != entry.get("stack_index"):
            order_drift.append(
                {
                    "feature_id": feature_id,
                    "expected": entry.get("stack_index"),
                    "current": current_index,
                }
            )
        expected_suppressed = bool(entry.get("suppressed", False))
        actual_suppressed = not bool(modifier.show_viewport) or not bool(modifier.show_render)
        if expected_suppressed != actual_suppressed:
            suppression_drift.append(
                {
                    "feature_id": feature_id,
                    "expected_suppressed": expected_suppressed,
                    "actual_suppressed": actual_suppressed,
                }
            )

    active_indices = [entry.get("stack_index") for entry in history if isinstance(entry.get("stack_index"), int)]
    history_order_drift = active_indices != sorted(active_indices)
    failures = missing or type_mismatch or order_drift or suppression_drift or duplicate_feature_ids or history_order_drift
    return {
        "status": "FAIL" if failures else "PASS",
        "feature_count": len(history),
        "missing_modifiers": missing,
        "type_mismatch": type_mismatch,
        "order_drift": order_drift,
        "suppression_drift": suppression_drift,
        "history_order_drift": history_order_drift,
        "duplicate_feature_ids": duplicate_feature_ids,
    }


def _ensure_dependency(obj, upstream_id):
    if not upstream_id:
        return False
    current = dependency_ids(obj)
    added = upstream_id not in current
    if added:
        current.append(upstream_id)
    meta = getattr(obj, "oleander", None)
    value = ",".join(current)
    if meta is not None and hasattr(meta, "dependencies"):
        meta.dependencies = value
    else:
        obj["oleander_dependencies"] = value
    return added


def _is_planar_mesh(obj, tolerance):
    if obj.type != "MESH" or len(obj.data.vertices) < 3:
        return False
    points = [vertex.co.copy() for vertex in obj.data.vertices]
    p0 = points[0]

    p1 = None
    for point in points[1:]:
        if (point - p0).length > tolerance:
            p1 = point
            break
    if p1 is None:
        return False

    normal = None
    base = p1 - p0
    for point in points[1:]:
        candidate = base.cross(point - p0)
        if candidate.length > tolerance * tolerance:
            normal = candidate.normalized()
            break
    if normal is None:
        return False

    return all(abs(normal.dot(point - p0)) <= tolerance for point in points)


class OLEANDER_OT_add_planar_extrude(bpy.types.Operator):
    """Add a governed non-destructive planar extrude using Solidify."""

    bl_idname = "oleander.add_planar_extrude"
    bl_label = "Planar Extrude"
    bl_options = {"REGISTER", "UNDO"}

    depth_mm: bpy.props.FloatProperty(name="Depth mm", default=20.0)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH" and context.mode == "OBJECT"

    def execute(self, context):
        obj = context.active_object
        if not _require_ole_id(self, obj):
            return {"CANCELLED"}
        if abs(self.depth_mm) < 0.001:
            self.report({"ERROR"}, "Planar Extrude depth must be non-zero")
            return {"CANCELLED"}
        tolerance = _mm_to_scene_units(context, 0.01)
        if not _is_planar_mesh(obj, tolerance):
            self.report({"ERROR"}, "Planar Extrude requires a planar mesh; use Shell/other governed routes for non-planar geometry")
            return {"CANCELLED"}

        _, _, modifier_name = _allocate_feature(obj, "PLANAR_EXTRUDE")
        modifier = obj.modifiers.new(name=modifier_name, type="SOLIDIFY")
        modifier.thickness = _mm_to_scene_units(context, self.depth_mm)
        modifier.offset = 1.0
        modifier.use_even_offset = True
        _record_feature(context, obj, modifier, "PLANAR_EXTRUDE", {"depth_mm": self.depth_mm, "direction": "NORMAL"})
        self.report({"INFO"}, f"Added governed planar extrude: {self.depth_mm:.3f} mm")
        return {"FINISHED"}


class OLEANDER_OT_add_shell(bpy.types.Operator):
    """Add a governed non-destructive shell/thickness feature."""

    bl_idname = "oleander.add_shell"
    bl_label = "Shell / Thickness"
    bl_options = {"REGISTER", "UNDO"}

    thickness_mm: bpy.props.FloatProperty(name="Thickness mm", default=3.0, min=0.001)
    offset_mode: bpy.props.EnumProperty(
        name="Offset",
        items=[("INSIDE", "Inside", ""), ("CENTER", "Center", ""), ("OUTSIDE", "Outside", "")],
        default="INSIDE",
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH" and context.mode == "OBJECT"

    def execute(self, context):
        obj = context.active_object
        if not _require_ole_id(self, obj):
            return {"CANCELLED"}
        _, _, modifier_name = _allocate_feature(obj, "SHELL")
        modifier = obj.modifiers.new(name=modifier_name, type="SOLIDIFY")
        modifier.thickness = _mm_to_scene_units(context, self.thickness_mm)
        modifier.offset = {"INSIDE": -1.0, "CENTER": 0.0, "OUTSIDE": 1.0}[self.offset_mode]
        modifier.use_even_offset = True
        _record_feature(
            context,
            obj,
            modifier,
            "SHELL",
            {"thickness_mm": self.thickness_mm, "offset_mode": self.offset_mode},
        )
        self.report({"INFO"}, f"Added governed shell: {self.thickness_mm:.3f} mm")
        return {"FINISHED"}


class OLEANDER_OT_add_bevel_chamfer(bpy.types.Operator):
    """Add a governed non-destructive bevel/chamfer modifier."""

    bl_idname = "oleander.add_bevel_chamfer"
    bl_label = "Bevel / Chamfer"
    bl_options = {"REGISTER", "UNDO"}

    width_mm: bpy.props.FloatProperty(name="Width mm", default=2.0, min=0.001)
    segments: bpy.props.IntProperty(name="Segments", default=1, min=1, max=64)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH" and context.mode == "OBJECT"

    def execute(self, context):
        obj = context.active_object
        if not _require_ole_id(self, obj):
            return {"CANCELLED"}
        _, _, modifier_name = _allocate_feature(obj, "BEVEL_CHAMFER")
        modifier = obj.modifiers.new(name=modifier_name, type="BEVEL")
        modifier.width = _mm_to_scene_units(context, self.width_mm)
        modifier.segments = self.segments
        modifier.profile = 0.5
        if hasattr(modifier, "affect"):
            modifier.affect = "EDGES"
        _record_feature(
            context,
            obj,
            modifier,
            "BEVEL_CHAMFER",
            {"width_mm": self.width_mm, "segments": self.segments, "profile": 0.5},
        )
        self.report({"INFO"}, f"Added governed bevel/chamfer: {self.width_mm:.3f} mm")
        return {"FINISHED"}


class OLEANDER_OT_add_mirror(bpy.types.Operator):
    """Add a governed non-destructive mirror feature around the object origin."""

    bl_idname = "oleander.add_mirror"
    bl_label = "Mirror"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(name="Axis", items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")], default="X")
    merge: bpy.props.BoolProperty(name="Merge", default=True)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH" and context.mode == "OBJECT"

    def execute(self, context):
        obj = context.active_object
        if not _require_ole_id(self, obj):
            return {"CANCELLED"}
        _, _, modifier_name = _allocate_feature(obj, "MIRROR")
        modifier = obj.modifiers.new(name=modifier_name, type="MIRROR")
        modifier.use_axis[0] = self.axis == "X"
        modifier.use_axis[1] = self.axis == "Y"
        modifier.use_axis[2] = self.axis == "Z"
        modifier.use_clip = self.merge
        modifier.use_mirror_merge = self.merge
        _record_feature(context, obj, modifier, "MIRROR", {"axis": self.axis, "merge": self.merge})
        self.report({"INFO"}, f"Added governed mirror on {self.axis}")
        return {"FINISHED"}


class OLEANDER_OT_add_linear_pattern(bpy.types.Operator):
    """Add a governed non-destructive linear Array modifier."""

    bl_idname = "oleander.add_linear_pattern"
    bl_label = "Linear Pattern"
    bl_options = {"REGISTER", "UNDO"}

    count: bpy.props.IntProperty(name="Count", default=3, min=2, max=10000)
    spacing_mm: bpy.props.FloatProperty(name="Spacing mm", default=600.0, min=0.0)
    axis: bpy.props.EnumProperty(name="Axis", items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")], default="X")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH" and context.mode == "OBJECT"

    def execute(self, context):
        obj = context.active_object
        if not _require_ole_id(self, obj):
            return {"CANCELLED"}
        _, _, modifier_name = _allocate_feature(obj, "LINEAR_PATTERN")
        modifier = obj.modifiers.new(name=modifier_name, type="ARRAY")
        modifier.count = self.count
        modifier.use_relative_offset = False
        modifier.use_constant_offset = True
        offset = Vector((0.0, 0.0, 0.0))
        offset[{"X": 0, "Y": 1, "Z": 2}[self.axis]] = _mm_to_scene_units(context, self.spacing_mm)
        modifier.constant_offset_displace = offset
        _record_feature(
            context,
            obj,
            modifier,
            "LINEAR_PATTERN",
            {"count": self.count, "spacing_mm": self.spacing_mm, "axis": self.axis},
        )
        self.report({"INFO"}, f"Added governed linear pattern: {self.count} × {self.spacing_mm:.3f} mm")
        return {"FINISHED"}


class OLEANDER_OT_add_boolean(bpy.types.Operator):
    """Add a governed Boolean modifier using exactly one selected cutter."""

    bl_idname = "oleander.add_boolean"
    bl_label = "Boolean"
    bl_options = {"REGISTER", "UNDO"}

    operation: bpy.props.EnumProperty(
        name="Operation",
        items=[("DIFFERENCE", "Difference", ""), ("UNION", "Union", ""), ("INTERSECT", "Intersect", "")],
        default="DIFFERENCE",
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH" and context.mode == "OBJECT"

    def execute(self, context):
        obj = context.active_object
        if not _require_ole_id(self, obj):
            return {"CANCELLED"}
        cutters = [selected for selected in context.selected_objects if selected != obj and selected.type == "MESH"]
        if len(cutters) != 1:
            self.report({"ERROR"}, "Boolean requires exactly one selected mesh cutter in addition to the active target")
            return {"CANCELLED"}
        cutter = cutters[0]
        cutter_id = _require_ole_id(self, cutter)
        if not cutter_id:
            return {"CANCELLED"}

        _, _, modifier_name = _allocate_feature(obj, f"BOOLEAN_{self.operation}")
        modifier = obj.modifiers.new(name=modifier_name, type="BOOLEAN")
        modifier.operation = self.operation
        modifier.object = cutter
        if hasattr(modifier, "solver"):
            modifier.solver = "EXACT"

        dependency_added = _ensure_dependency(obj, cutter_id)
        _record_feature(
            context,
            obj,
            modifier,
            f"BOOLEAN_{self.operation}",
            {
                "operation": self.operation,
                "cutter_id": cutter_id,
                "solver": getattr(modifier, "solver", ""),
                "dependency_added_by_feature": dependency_added,
            },
            source_ids=[cutter_id],
        )
        self.report({"INFO"}, f"Added governed Boolean {self.operation} using {cutter_id}")
        return {"FINISHED"}


class OLEANDER_OT_validate_feature_stack(bpy.types.Operator):
    """Validate that recorded OLEANDER features still match Blender modifiers."""

    bl_idname = "oleander.validate_feature_stack"
    bl_label = "Validate Feature Stack"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        result = validate_feature_history(context.active_object)
        context.active_object["oleander_feature_stack_validation"] = json.dumps(result, sort_keys=True)
        level = {"INFO"} if result["status"] == "PASS" else {"WARNING"}
        self.report(level, f"Feature Stack {result['status']}: {result['feature_count']} feature(s)")
        return {"FINISHED"}


CLASSES = (
    OLEANDER_OT_add_planar_extrude,
    OLEANDER_OT_add_shell,
    OLEANDER_OT_add_bevel_chamfer,
    OLEANDER_OT_add_mirror,
    OLEANDER_OT_add_linear_pattern,
    OLEANDER_OT_add_boolean,
    OLEANDER_OT_validate_feature_stack,
)
