import json
import bpy

from .dependency import build_dependency_graph, detect_cycles, mark_downstream_stale
from .geometry_diff import diff_from_baseline, store_baseline
from .review_state import summarize_object_state


class OLEANDER_OT_store_geometry_baseline(bpy.types.Operator):
    bl_idname = "oleander.store_geometry_baseline"
    bl_label = "Store Geometry Baseline"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        sig = store_baseline(context.active_object)
        self.report({"INFO"}, f"Baseline stored {sig['sha256'][:12]}")
        return {"FINISHED"}


class OLEANDER_OT_diff_geometry(bpy.types.Operator):
    bl_idname = "oleander.diff_geometry"
    bl_label = "Diff Geometry"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        result = diff_from_baseline(context.active_object)
        context.active_object["oleander_last_geometry_diff"] = json.dumps(result, sort_keys=True)
        self.report({"INFO"}, f"Geometry diff: {result['status']} ({len(result['changed'])} fields)")
        return {"FINISHED"}


class OLEANDER_OT_mark_dependents_stale(bpy.types.Operator):
    bl_idname = "oleander.mark_dependents_stale"
    bl_label = "Mark Dependents Stale"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        meta = getattr(context.active_object, "oleander_meta", None)
        source_id = (getattr(meta, "ole_id", "") or context.active_object.name).strip()
        changed = mark_downstream_stale([source_id], scene=context.scene)
        self.report({"INFO"}, f"Marked {len(changed)} downstream objects stale")
        return {"FINISHED"}


class OLEANDER_OT_audit_dependency_graph(bpy.types.Operator):
    bl_idname = "oleander.audit_dependency_graph"
    bl_label = "Audit Dependency Graph"
    bl_options = {"REGISTER"}

    def execute(self, context):
        graph = build_dependency_graph(context.scene)
        cycles = detect_cycles(graph)
        missing_count = sum(len(v) for v in graph["missing"].values())
        context.scene["oleander_dependency_audit"] = json.dumps({
            "cycles": cycles,
            "missing": dict(graph["missing"]),
        }, sort_keys=True)
        state = "PASS" if not cycles and not missing_count else "FAIL"
        context.scene["oleander_dependency_audit_state"] = state
        self.report({"INFO"}, f"Dependency audit {state}: {len(cycles)} cycles, {missing_count} missing")
        return {"FINISHED"}


class OLEANDER_OT_summarize_review_state(bpy.types.Operator):
    bl_idname = "oleander.summarize_review_state"
    bl_label = "Summarize Review State"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        result = summarize_object_state(context.active_object)
        context.active_object["oleander_review_summary"] = json.dumps(result, sort_keys=True)
        self.report({"INFO"}, f"OLE review overall: {result['overall']}")
        return {"FINISHED"}


CLASSES = (
    OLEANDER_OT_store_geometry_baseline,
    OLEANDER_OT_diff_geometry,
    OLEANDER_OT_mark_dependents_stale,
    OLEANDER_OT_audit_dependency_graph,
    OLEANDER_OT_summarize_review_state,
)
