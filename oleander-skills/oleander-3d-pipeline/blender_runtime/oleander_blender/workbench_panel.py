import json
import bpy

from .configuration import configuration_names
from .feature_stack import get_feature_history


class OLEANDER_PT_workbench(bpy.types.Panel):
    bl_label = "OLEANDER Workbench"
    bl_idname = "OLEANDER_PT_workbench"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OLEANDER"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        direct = layout.box()
        direct.label(text="Direct Modeling")
        direct.operator("oleander.apply_metric_dimensions", icon="DRIVER_DISTANCE")
        direct.operator("oleander.duplicate_linear", icon="DUPLICATE")

        features = layout.box()
        features.label(text="Direct Feature Stack")
        row = features.row(align=True)
        row.operator("oleander.add_planar_extrude", icon="MOD_SOLIDIFY")
        row.operator("oleander.add_shell", icon="MOD_SOLIDIFY")
        row = features.row(align=True)
        row.operator("oleander.add_bevel_chamfer", icon="MOD_BEVEL")
        row.operator("oleander.add_mirror", icon="MOD_MIRROR")
        row = features.row(align=True)
        row.operator("oleander.add_linear_pattern", icon="MOD_ARRAY")
        row.operator("oleander.add_boolean", icon="MOD_BOOLEAN")
        features.operator("oleander.validate_feature_stack", icon="CHECKMARK")
        if obj:
            history = get_feature_history(obj)
            features.label(text=f"Governed features: {len(history)}")
            if history:
                last = history[-1]
                features.label(text=f"Last: {last.get('kind', 'UNKNOWN')}")
            raw_validation = obj.get("oleander_feature_stack_validation")
            if raw_validation:
                try:
                    validation = json.loads(raw_validation)
                except (TypeError, json.JSONDecodeError):
                    validation = None
                if validation:
                    features.label(text=f"Stack: {validation.get('status', 'OPEN')}")

        config = layout.box()
        config.label(text="Configurations")
        row = config.row(align=True)
        row.operator("oleander.save_configuration", icon="ADD")
        row.operator("oleander.restore_configuration", icon="RECOVER_LAST")
        config.operator("oleander.list_configurations", icon="TEXT")
        names = configuration_names(context.scene)
        if names:
            config.label(text="Saved: " + ", ".join(names[:4]))
            if len(names) > 4:
                config.label(text=f"+ {len(names) - 4} more")
        else:
            config.label(text="Saved: none")

        graph = layout.box()
        graph.label(text="Dependency Graph")
        graph.operator("oleander.mark_dependents_stale", icon="FILE_REFRESH")
        graph.operator("oleander.audit_dependency_graph", icon="NODETREE")
        scene_state = context.scene.get("oleander_dependency_audit_state")
        if scene_state:
            graph.label(text=f"Graph: {scene_state}")

        diff = layout.box()
        diff.label(text="Geometry Baseline / Diff")
        diff.operator("oleander.store_geometry_baseline", icon="BOOKMARKS")
        diff.operator("oleander.diff_geometry", icon="ARROW_LEFTRIGHT")

        semantic = layout.box()
        semantic.label(text="Semantic / Quantity")
        semantic.operator("oleander.snapshot_semantics", icon="PRESET")
        semantic.operator("oleander.build_bom", icon="OUTLINER_COLLECTION")

        review = layout.box()
        review.label(text="Review State")
        review.operator("oleander.summarize_review_state", icon="CHECKMARK")

        if obj:
            meta = getattr(obj, "oleander", None)
            stale = bool(getattr(meta, "stale", False)) if meta else False
            review.label(text=f"Stale: {'YES' if stale else 'NO'}")
            raw = obj.get("oleander_review_summary")
            if raw:
                try:
                    summary = json.loads(raw)
                except (TypeError, json.JSONDecodeError):
                    summary = None
                if summary:
                    review.label(text=f"Overall: {summary.get('overall', 'OPEN')}")
                    col = review.column(align=True)
                    for key in ("geometry", "field", "engineering", "manufacturing", "design"):
                        col.label(text=f"{key.title()}: {summary.get(key, 'OPEN')}")


CLASSES = (OLEANDER_PT_workbench,)
