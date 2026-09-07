import json
import bpy

from .dependency import build_dependency_graph, detect_cycles, mark_downstream_stale
from .geometry_diff import diff_from_baseline, store_baseline
from .review_state import summarize_object_state
from .semantic import store_semantic_snapshot


class OLEANDER_OT_store_geometry_baseline(bpy.types.Operator):
    bl_idname = "oleander.store_geometry_baseline"
    bl_label = "Store Geometry Baseline"
    bl_description = "Store an inspectable geometry baseline. This does not approve geometry quality."
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
    bl_description = "Compare current geometry against the stored baseline and mark governed downstream dependents stale when changed."
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.active_object
        result = diff_from_baseline(obj)
        obj["oleander_last_geometry_diff"] = json.dumps(result, sort_keys=True)
        downstream = []
        if result["status"] == "CHANGED":
            source_id = (obj.oleander.ole_id or obj.name).strip()
            downstream = mark_downstream_stale([source_id], reason="GEOMETRY_BASELINE_CHANGED", scene=context.scene)
        self.report({"INFO"}, f"Geometry diff: {result['status']} ({len(result['changed'])} fields); downstream stale: {len(downstream)}")
        return {"FINISHED"}


class OLEANDER_OT_mark_dependents_stale(bpy.types.Operator):
    bl_idname = "oleander.mark_dependents_stale"
    bl_label = "Mark Dependents Stale"
    bl_description = "Propagate an upstream-change stale state through the declared OLE dependency graph."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.active_object
        source_id = (obj.oleander.ole_id or obj.name).strip()
        changed = mark_downstream_stale([source_id], scene=context.scene)
        self.report({"INFO"}, f"Marked {len(changed)} downstream objects stale")
        return {"FINISHED"}


class OLEANDER_OT_audit_dependency_graph(bpy.types.Operator):
    bl_idname = "oleander.audit_dependency_graph"
    bl_label = "Audit Dependency Graph"
    bl_description = "Detect missing upstream OLE IDs and dependency cycles."
    bl_options = {"REGISTER"}

    def execute(self, context):
        graph = build_dependency_graph(context.scene)
        cycles = detect_cycles(graph)
        missing = {key: value for key, value in graph["missing"].items() if value}
        missing_count = sum(len(v) for v in missing.values())
        context.scene["oleander_dependency_audit"] = json.dumps({
            "cycles": cycles,
            "missing": missing,
        }, sort_keys=True)
        state = "PASS" if not cycles and not missing_count else "FAIL"
        context.scene["oleander_dependency_audit_state"] = state
        self.report({"INFO"}, f"Dependency audit {state}: {len(cycles)} cycles, {missing_count} missing")
        return {"FINISHED"}


class OLEANDER_OT_snapshot_semantics(bpy.types.Operator):
    bl_idname = "oleander.snapshot_semantics"
    bl_label = "Snapshot Semantics"
    bl_description = "Store the current governed semantic payload for inspection/diff handoff."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        payload = store_semantic_snapshot(context.active_object)
        self.report({"INFO"}, f"Semantic snapshot stored for {payload.get('ole_id') or payload['object_name']}")
        return {"FINISHED"}


class OLEANDER_OT_summarize_review_state(bpy.types.Operator):
    bl_idname = "oleander.summarize_review_state"
    bl_label = "Summarize Review State"
    bl_description = "Summarize geometry, field, engineering, manufacturing, design and stale states without collapsing their authority boundaries."
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
    OLEANDER_OT_snapshot_semantics,
    OLEANDER_OT_summarize_review_state,
)
