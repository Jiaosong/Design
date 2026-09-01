import json
import bpy


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
        direct.label(text="Direct")
        direct.operator("oleander.apply_metric_dimensions", icon="DRIVER_DISTANCE")
        direct.operator("oleander.duplicate_linear", icon="DUPLICATE")

        graph = layout.box()
        graph.label(text="Dependency")
        graph.operator("oleander.mark_dependents_stale", icon="FILE_REFRESH")
        graph.operator("oleander.audit_dependency_graph", icon="NODETREE")
        scene_state = context.scene.get("oleander_dependency_audit_state")
        if scene_state:
            graph.label(text=f"Graph: {scene_state}")

        diff = layout.box()
        diff.label(text="Geometry Diff")
        diff.operator("oleander.store_geometry_baseline", icon="BOOKMARKS")
        diff.operator("oleander.diff_geometry", icon="ARROW_LEFTRIGHT")

        review = layout.box()
        review.label(text="Review")
        review.operator("oleander.summarize_review_state", icon="CHECKMARK")

        if obj:
            stale = getattr(getattr(obj, "oleander_meta", None), "stale", False)
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
