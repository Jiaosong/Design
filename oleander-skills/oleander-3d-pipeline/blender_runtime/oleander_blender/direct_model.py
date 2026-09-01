import bpy
from mathutils import Vector


def _mm_to_scene_units(context, value_mm):
    scale_length = context.scene.unit_settings.scale_length or 1.0
    return (value_mm / 1000.0) / scale_length


class OLEANDER_OT_apply_metric_dimensions(bpy.types.Operator):
    """Set active mesh dimensions from millimetres using the scene unit scale."""

    bl_idname = "oleander.apply_metric_dimensions"
    bl_label = "Apply mm Dimensions"
    bl_options = {"REGISTER", "UNDO"}

    x_mm: bpy.props.FloatProperty(name="X mm", default=1000.0, min=0.001)
    y_mm: bpy.props.FloatProperty(name="Y mm", default=1000.0, min=0.001)
    z_mm: bpy.props.FloatProperty(name="Z mm", default=1000.0, min=0.001)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"

    def execute(self, context):
        obj = context.active_object
        target = Vector(tuple(_mm_to_scene_units(context, v) for v in (self.x_mm, self.y_mm, self.z_mm)))
        obj.dimensions = target
        obj["oleander_last_direct_operation"] = "SET_DIMENSIONS_MM"
        obj["oleander_direct_dimensions_mm"] = [self.x_mm, self.y_mm, self.z_mm]
        self.report({"INFO"}, f"Dimensions set to {self.x_mm:.1f} × {self.y_mm:.1f} × {self.z_mm:.1f} mm")
        return {"FINISHED"}


class OLEANDER_OT_duplicate_linear(bpy.types.Operator):
    """Create a deterministic linked or unlinked linear duplicate set."""

    bl_idname = "oleander.duplicate_linear"
    bl_label = "Linear Duplicate"
    bl_options = {"REGISTER", "UNDO"}

    count: bpy.props.IntProperty(name="Count", default=3, min=2, max=10000)
    spacing_mm: bpy.props.FloatProperty(name="Spacing mm", default=600.0, min=0.0)
    axis: bpy.props.EnumProperty(
        name="Axis",
        items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")],
        default="X",
    )
    linked: bpy.props.BoolProperty(name="Linked Mesh", default=True)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        source = context.active_object
        step = Vector((0.0, 0.0, 0.0))
        step[{"X": 0, "Y": 1, "Z": 2}[self.axis]] = _mm_to_scene_units(context, self.spacing_mm)
        collection = source.users_collection[0] if source.users_collection else context.collection

        created = []
        for idx in range(1, self.count):
            dup = source.copy()
            if getattr(source, "data", None) and not self.linked:
                dup.data = source.data.copy()
            dup.location = source.location + step * idx
            dup.name = f"{source.name}_A{idx:03d}"
            dup["oleander_array_source"] = source.name
            dup["oleander_array_index"] = idx
            collection.objects.link(dup)
            created.append(dup.name)

        source["oleander_last_direct_operation"] = "LINEAR_DUPLICATE"
        source["oleander_array_count"] = self.count
        source["oleander_array_spacing_mm"] = self.spacing_mm
        source["oleander_array_axis"] = self.axis
        self.report({"INFO"}, f"Created {len(created)} duplicates")
        return {"FINISHED"}


CLASSES = (
    OLEANDER_OT_apply_metric_dimensions,
    OLEANDER_OT_duplicate_linear,
)
