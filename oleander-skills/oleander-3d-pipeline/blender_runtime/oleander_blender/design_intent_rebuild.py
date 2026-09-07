"""Dirty-set and deterministic rebuild planning for OLEANDER Design Intent.

The planner infers dirty parameters from the existing parameter event log and
from direct design-intent stale markers already written by parameter updates. It
then expands only downstream parameter dependents, orders the selected set by
its declared dependency graph, computes a non-mutating impact preview and
reuses the validated atomic Batch Apply layer for explicit execution.

It deliberately does NOT solve equations, derive values, infer constraints,
automatically execute rebuilds, or claim CAD/B-Rep parametric authority.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict, deque

import bpy
from bpy.props import StringProperty

from .dependency import build_dependency_graph, object_id
from .design_intent import (
    PARAMETER_EVENT_COUNTER_KEY,
    get_design_parameter_events,
    get_design_parameters,
    resolve_binding,
)
from .design_intent_batch import apply_design_parameter_batch, preflight_design_parameter_batch

REBUILD_PLAN_SCHEMA = "OLEANDER_DESIGN_INTENT_REBUILD_PLAN_v0.1"
LAST_REBUILD_PLAN_KEY = "oleander_design_intent_last_rebuild_plan"
LAST_REBUILD_RESULT_KEY = "oleander_design_intent_last_rebuild_result"

DIRTY_EVENT_ACTIONS = {"VALUE_UPDATE", "BIND", "DEPENDENCY_ADD"}
CLEAN_EVENT_ACTIONS = {"APPLY_COMMIT", "BATCH_APPLY_COMMIT"}


def _parameter_map(parameters):
    return {item.get("parameter_id", ""): item for item in parameters if item.get("parameter_id")}


def _normalize_parameter_ids(parameter_ids):
    if parameter_ids is None:
        return []
    if isinstance(parameter_ids, str):
        values = [item.strip() for item in parameter_ids.split(",") if item.strip()]
    else:
        values = [str(item).strip() for item in parameter_ids if str(item).strip()]
    if len(values) != len(set(values)):
        raise ValueError("rebuild plan contains duplicate seed parameter IDs")
    return values


def _latest_event_indexes(events):
    dirty = {}
    clean = {}
    for event in events:
        parameter_id = str(event.get("parameter_id", ""))
        if not parameter_id:
            continue
        index = int(event.get("event_index", 0))
        action = event.get("action", "")
        if action in DIRTY_EVENT_ACTIONS:
            dirty[parameter_id] = max(index, dirty.get(parameter_id, 0))
        if action in CLEAN_EVENT_ACTIONS:
            clean[parameter_id] = max(index, clean.get(parameter_id, 0))
    return dirty, clean


def _direct_design_intent_stale(scene, parameter):
    reasons = []
    for binding in parameter.get("bindings", []):
        resolved = resolve_binding(scene, binding)
        if not resolved.get("valid"):
            continue
        if binding.get("target_kind") == "DATUM_REFERENCE":
            target = resolved.get("target")
            if target is not None and bool(target.get("oleander_design_intent_review_required", False)):
                reasons.append(f"DATUM_REVIEW_REQUIRED:{binding.get('target_id', '')}")
            continue
        for oid in resolved.get("object_ids", []):
            obj = next((item for item in scene.objects if object_id(item) == oid), None)
            if obj is not None and bool(obj.get("oleander_design_intent_stale", False)):
                reasons.append(f"BOUND_TARGET_STALE:{oid}")
    return sorted(set(reasons))


def infer_dirty_design_parameters(scene=None):
    scene = scene or bpy.context.scene
    parameters = get_design_parameters(scene)
    events = get_design_parameter_events(scene)
    latest_dirty, latest_clean = _latest_event_indexes(events)
    dirty = []

    for parameter in parameters:
        parameter_id = parameter.get("parameter_id", "")
        reasons = []
        dirty_index = latest_dirty.get(parameter_id, 0)
        clean_index = latest_clean.get(parameter_id, 0)
        if dirty_index > clean_index:
            reasons.append(f"EVENT_AFTER_LAST_APPLY:{dirty_index}>{clean_index}")
        reasons.extend(_direct_design_intent_stale(scene, parameter))
        if reasons:
            dirty.append(
                {
                    "parameter_id": parameter_id,
                    "revision": int(parameter.get("revision", 0)),
                    "reasons": sorted(set(reasons)),
                    "latest_dirty_event_index": dirty_index,
                    "latest_clean_event_index": clean_index,
                }
            )
    return dirty


def _parameter_reverse(parameters):
    reverse = defaultdict(set)
    for parameter in parameters:
        parameter_id = parameter.get("parameter_id", "")
        for upstream in parameter.get("dependencies", []):
            reverse[upstream].add(parameter_id)
    return reverse


def _downstream_parameter_closure(parameters, seed_ids):
    reverse = _parameter_reverse(parameters)
    selected = set(seed_ids)
    queue = deque(seed_ids)
    while queue:
        current = queue.popleft()
        for downstream in sorted(reverse.get(current, ())):
            if downstream in selected:
                continue
            selected.add(downstream)
            queue.append(downstream)
    return selected


def _selected_topological_order(parameter_by_id, selected, seed_order):
    order = []
    visiting = set()
    visited = set()

    def visit(parameter_id):
        if parameter_id in visited:
            return
        if parameter_id in visiting:
            raise ValueError("design parameter dependency cycle detected during rebuild planning")
        visiting.add(parameter_id)
        parameter = parameter_by_id[parameter_id]
        for upstream in parameter.get("dependencies", []):
            if upstream in selected:
                visit(upstream)
        visiting.remove(parameter_id)
        visited.add(parameter_id)
        order.append(parameter_id)

    for parameter_id in seed_order:
        if parameter_id in selected:
            visit(parameter_id)
    for parameter_id in sorted(selected):
        visit(parameter_id)
    return order


def _object_downstream_preview(scene, source_ids):
    graph = build_dependency_graph(scene)
    reverse = graph["reverse"]
    queue = deque(source_ids)
    seen = set(source_ids)
    downstream = []
    while queue:
        current = queue.popleft()
        for oid in sorted(reverse.get(current, ())):
            if oid in seen:
                continue
            seen.add(oid)
            queue.append(oid)
            downstream.append(oid)
    return downstream


def _impact_preview(scene, parameters):
    direct_object_ids = []
    datum_reference_ids = []
    relation_ids = []
    feature_ids = []
    target_signatures = []

    for parameter in parameters:
        for binding in parameter.get("bindings", []):
            signature = ":".join(
                [
                    str(binding.get("target_kind", "")),
                    str(binding.get("target_id", "")),
                    str(binding.get("target_field", "")),
                ]
            )
            if signature not in target_signatures:
                target_signatures.append(signature)
            kind = binding.get("target_kind", "")
            target_id = binding.get("target_id", "")
            if kind == "DATUM_REFERENCE":
                if target_id not in datum_reference_ids:
                    datum_reference_ids.append(target_id)
                continue
            if kind == "RELATION" and target_id not in relation_ids:
                relation_ids.append(target_id)
            if kind == "FEATURE" and target_id not in feature_ids:
                feature_ids.append(target_id)
            resolved = resolve_binding(scene, binding)
            for oid in resolved.get("object_ids", []):
                if oid not in direct_object_ids:
                    direct_object_ids.append(oid)

    return {
        "direct_object_ids": direct_object_ids,
        "downstream_object_ids": _object_downstream_preview(scene, direct_object_ids),
        "datum_reference_ids": datum_reference_ids,
        "relation_ids": relation_ids,
        "feature_ids": feature_ids,
        "target_signatures": target_signatures,
    }


def _parameter_state_payload(parameter):
    return {
        "parameter_id": parameter.get("parameter_id", ""),
        "revision": int(parameter.get("revision", 0)),
        "kind": parameter.get("kind", ""),
        "value": parameter.get("value"),
        "dependencies": list(parameter.get("dependencies", [])),
        "bindings": list(parameter.get("bindings", [])),
    }


def _state_sha256(parameters):
    payload = [_parameter_state_payload(parameter) for parameter in parameters]
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _plan_sha256(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def build_design_intent_rebuild_plan(scene=None, seed_parameter_ids=None):
    scene = scene or bpy.context.scene
    parameters = get_design_parameters(scene)
    parameter_by_id = _parameter_map(parameters)
    explicit_seeds = _normalize_parameter_ids(seed_parameter_ids)

    if explicit_seeds:
        missing = [parameter_id for parameter_id in explicit_seeds if parameter_id not in parameter_by_id]
        if missing:
            raise ValueError(f"design parameter not found: {missing[0]}")
        dirty_records = [
            {
                "parameter_id": parameter_id,
                "revision": int(parameter_by_id[parameter_id].get("revision", 0)),
                "reasons": ["EXPLICIT_REBUILD_SEED"],
                "latest_dirty_event_index": 0,
                "latest_clean_event_index": 0,
            }
            for parameter_id in explicit_seeds
        ]
        seed_ids = list(explicit_seeds)
        seed_mode = "EXPLICIT"
    else:
        dirty_records = infer_dirty_design_parameters(scene)
        seed_ids = [record["parameter_id"] for record in dirty_records]
        seed_mode = "INFERRED_DIRTY"

    event_watermark = int(scene.get(PARAMETER_EVENT_COUNTER_KEY, 0))
    if not seed_ids:
        result = {
            "schema": REBUILD_PLAN_SCHEMA,
            "status": "CLEAN",
            "seed_mode": seed_mode,
            "seed_parameter_ids": [],
            "execution_order": [],
            "event_watermark": event_watermark,
            "parameter_count": 0,
            "binding_count": 0,
            "geometry_mutated": False,
            "solver_claim": False,
            "automatic_execution": False,
            "automatic_parameter_value_derivation": False,
            "automatic_parameter_geometry_rebuild": False,
            "cad_parametric_feature_rebuild_claim": False,
        }
        result["plan_sha256"] = _plan_sha256(result)
        return result

    selected = _downstream_parameter_closure(parameters, seed_ids)
    order = _selected_topological_order(parameter_by_id, selected, seed_ids)
    selected_parameters = [parameter_by_id[parameter_id] for parameter_id in order]

    batch_preflight = preflight_design_parameter_batch(scene, order, include_dependencies=False)
    impact = _impact_preview(scene, selected_parameters)
    state_sha = _state_sha256(selected_parameters)
    revisions = {parameter_id: int(parameter_by_id[parameter_id].get("revision", 0)) for parameter_id in order}

    result = {
        "schema": REBUILD_PLAN_SCHEMA,
        "status": "PASS",
        "seed_mode": seed_mode,
        "dirty_seeds": dirty_records,
        "seed_parameter_ids": seed_ids,
        "execution_order": order,
        "expanded_downstream_parameter_ids": [parameter_id for parameter_id in order if parameter_id not in seed_ids],
        "event_watermark": event_watermark,
        "parameter_revisions": revisions,
        "parameter_state_sha256": state_sha,
        "parameter_count": len(order),
        "binding_count": int(batch_preflight.get("binding_count", 0)),
        "target_signatures": list(batch_preflight.get("target_signatures", [])),
        "impact": impact,
        "transaction_mode": "ATOMIC_ALL_OR_ROLLBACK_VIA_BATCH_APPLY",
        "geometry_mutated": False,
        "solver_claim": False,
        "automatic_execution": False,
        "automatic_parameter_value_derivation": False,
        "automatic_parameter_geometry_rebuild": False,
        "cad_parametric_feature_rebuild_claim": False,
    }
    hash_payload = dict(result)
    result["plan_sha256"] = _plan_sha256(hash_payload)
    return result


def store_design_intent_rebuild_plan(scene, plan):
    scene[LAST_REBUILD_PLAN_KEY] = json.dumps(plan, sort_keys=True, ensure_ascii=False)
    return plan


def _validate_plan_freshness(scene, plan):
    if plan.get("schema") != REBUILD_PLAN_SCHEMA or plan.get("status") != "PASS":
        raise ValueError("rebuild plan is not an executable PASS plan")
    if int(scene.get(PARAMETER_EVENT_COUNTER_KEY, 0)) != int(plan.get("event_watermark", -1)):
        raise ValueError("rebuild plan is stale: parameter event watermark changed")

    parameter_by_id = _parameter_map(get_design_parameters(scene))
    current = []
    for parameter_id in plan.get("execution_order", []):
        parameter = parameter_by_id.get(parameter_id)
        if parameter is None:
            raise ValueError(f"rebuild plan is stale: parameter missing: {parameter_id}")
        expected_revision = int(plan.get("parameter_revisions", {}).get(parameter_id, -1))
        if int(parameter.get("revision", 0)) != expected_revision:
            raise ValueError(f"rebuild plan is stale: parameter revision changed: {parameter_id}")
        current.append(parameter)
    if _state_sha256(current) != plan.get("parameter_state_sha256"):
        raise ValueError("rebuild plan is stale: parameter state hash changed")


def execute_design_intent_rebuild_plan(scene=None, plan=None):
    scene = scene or bpy.context.scene
    if plan is None:
        raw = scene.get(LAST_REBUILD_PLAN_KEY, "")
        if not raw:
            raise ValueError("no stored rebuild plan")
        try:
            plan = json.loads(raw)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ValueError("stored rebuild plan is invalid JSON") from exc

    _validate_plan_freshness(scene, plan)
    try:
        batch = apply_design_parameter_batch(scene, plan.get("execution_order", []), include_dependencies=False)
    except ValueError as exc:
        result = {
            "schema": REBUILD_PLAN_SCHEMA,
            "status": "ROLLED_BACK",
            "plan_sha256": plan.get("plan_sha256", ""),
            "reason": str(exc),
            "rollback_delegated_to_batch_apply": True,
            "solver_claim": False,
            "automatic_parameter_value_derivation": False,
            "automatic_parameter_geometry_rebuild": False,
            "cad_parametric_feature_rebuild_claim": False,
        }
        scene[LAST_REBUILD_RESULT_KEY] = json.dumps(result, sort_keys=True, ensure_ascii=False)
        raise

    result = {
        "schema": REBUILD_PLAN_SCHEMA,
        "status": "PASS",
        "plan_sha256": plan.get("plan_sha256", ""),
        "batch_id": batch.get("batch_id", ""),
        "execution_order": list(plan.get("execution_order", [])),
        "parameter_count": int(plan.get("parameter_count", 0)),
        "binding_count": int(plan.get("binding_count", 0)),
        "batch_result": batch,
        "explicit_execution": True,
        "solver_claim": False,
        "automatic_parameter_value_derivation": False,
        "automatic_parameter_geometry_rebuild": False,
        "cad_parametric_feature_rebuild_claim": False,
    }
    scene[LAST_REBUILD_RESULT_KEY] = json.dumps(result, sort_keys=True, ensure_ascii=False)
    return result


class OLEANDER_OT_build_design_intent_rebuild_plan(bpy.types.Operator):
    bl_idname = "oleander.build_design_intent_rebuild_plan"
    bl_label = "Build Rebuild Plan"
    bl_description = "Infer dirty Design Intent parameters and build a non-mutating minimal downstream rebuild plan"
    bl_options = {"REGISTER"}

    seed_parameter_ids: StringProperty(
        name="Seed Parameter IDs",
        description="Optional comma-separated OLE_PARAM IDs; blank infers dirty parameters",
        default="",
    )

    def execute(self, context):
        try:
            plan = build_design_intent_rebuild_plan(context.scene, self.seed_parameter_ids or None)
            store_design_intent_rebuild_plan(context.scene, plan)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Rebuild plan {plan['status']}: {plan['parameter_count']} parameter(s); solver_claim=false")
        return {"FINISHED"}


class OLEANDER_OT_execute_design_intent_rebuild_plan(bpy.types.Operator):
    bl_idname = "oleander.execute_design_intent_rebuild_plan"
    bl_label = "Execute Rebuild Plan"
    bl_description = "Explicitly execute the stored rebuild plan through atomic Batch Apply; not a solver"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            result = execute_design_intent_rebuild_plan(context.scene)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Rebuild plan applied through {result['batch_id']}; solver_claim=false")
        return {"FINISHED"}


class OLEANDER_PT_design_intent_rebuild(bpy.types.Panel):
    bl_label = "Rebuild Plan"
    bl_idname = "OLEANDER_PT_design_intent_rebuild"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OLEANDER"
    bl_parent_id = "OLEANDER_PT_design_intent_batch"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Dirty set → downstream closure → ordered plan")
        layout.label(text="Plan is explicit and event/revision locked")
        layout.label(text="No solver / no derived-value computation", icon="INFO")
        layout.operator("oleander.build_design_intent_rebuild_plan", icon="PREVIEW_RANGE")
        layout.operator("oleander.execute_design_intent_rebuild_plan", icon="FILE_REFRESH")


OPERATOR_CLASSES = (
    OLEANDER_OT_build_design_intent_rebuild_plan,
    OLEANDER_OT_execute_design_intent_rebuild_plan,
)

PANEL_CLASSES = (OLEANDER_PT_design_intent_rebuild,)
