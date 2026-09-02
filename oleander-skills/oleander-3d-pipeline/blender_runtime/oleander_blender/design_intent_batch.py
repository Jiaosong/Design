"""Atomic dependency-ordered batch application for OLEANDER Design Intent.

This layer composes the already validated single-parameter apply primitives into
an explicit multi-parameter transaction. It expands declared upstream parameter
dependencies, orders them deterministically, preflights every parameter and
binding before the first mutation, rejects competing parameters that claim the
same target field, snapshots all targets, applies the stored parameter values,
postchecks the final combined state and rolls the entire transaction back on any
apply/postcheck failure.

It deliberately does NOT solve equations, derive parameter values, infer missing
constraints, or provide CAD/B-Rep parametric rebuild authority.
"""

from __future__ import annotations

import json

import bpy
from bpy.props import BoolProperty, StringProperty

from .dependency import mark_downstream_stale, object_id
from .design_intent import (
    _append_event,
    _parameter_by_id,
    audit_design_intent_graph,
    get_design_parameters,
)
from .design_intent_apply import (
    _apply_plan_item,
    _build_apply_plan,
    _clear_direct_parameter_stale,
    _find_object_by_id,
    _postcheck_plan,
    _restore_snapshot,
    _snapshot_item,
)

BATCH_APPLY_SCHEMA = "OLEANDER_DESIGN_INTENT_BATCH_APPLY_v0.1"
LAST_BATCH_APPLY_KEY = "oleander_design_intent_last_batch_apply"
BATCH_COUNTER_KEY = "oleander_design_intent_batch_counter"


def _normalize_parameter_ids(parameter_ids):
    if isinstance(parameter_ids, str):
        values = [item.strip() for item in parameter_ids.split(",") if item.strip()]
    else:
        values = [str(item).strip() for item in parameter_ids if str(item).strip()]
    if not values:
        raise ValueError("design-intent batch requires at least one parameter ID")
    if len(values) != len(set(values)):
        raise ValueError("design-intent batch contains duplicate parameter IDs")
    return values


def _parameter_map(parameters):
    return {item.get("parameter_id", ""): item for item in parameters if item.get("parameter_id")}


def _expand_upstream_dependencies(parameter_by_id, requested):
    selected = set()

    def include(parameter_id):
        if parameter_id in selected:
            return
        parameter = parameter_by_id.get(parameter_id)
        if parameter is None:
            raise ValueError(f"design parameter not found: {parameter_id}")
        for upstream in parameter.get("dependencies", []):
            if upstream not in parameter_by_id:
                raise ValueError(f"design parameter dependency references missing parameter: {parameter_id}->{upstream}")
            include(upstream)
        selected.add(parameter_id)

    for parameter_id in requested:
        include(parameter_id)
    return selected


def _topological_order(parameter_by_id, selected, requested):
    order = []
    visiting = set()
    visited = set()

    def visit(parameter_id):
        if parameter_id in visited:
            return
        if parameter_id in visiting:
            raise ValueError("design parameter dependency cycle detected during batch planning")
        visiting.add(parameter_id)
        parameter = parameter_by_id[parameter_id]
        for upstream in parameter.get("dependencies", []):
            if upstream in selected:
                visit(upstream)
        visiting.remove(parameter_id)
        visited.add(parameter_id)
        order.append(parameter_id)

    # Requested order is used only as a deterministic tie-breaker. Dependencies
    # always precede their consumers.
    for parameter_id in requested:
        if parameter_id in selected:
            visit(parameter_id)
    for parameter_id in sorted(selected):
        visit(parameter_id)
    return order


def _target_signature(item):
    binding = item.get("binding", {})
    return (
        str(binding.get("target_kind", "")),
        str(binding.get("target_id", "")),
        str(binding.get("target_field", "")),
    )


def _build_batch_execution_plan(scene, parameter_ids, include_dependencies=True):
    requested = _normalize_parameter_ids(parameter_ids)
    graph_audit = audit_design_intent_graph(scene)
    if graph_audit.get("status") != "PASS":
        raise ValueError("design intent graph must audit PASS before batch apply")

    parameters = get_design_parameters(scene)
    parameter_by_id = _parameter_map(parameters)
    missing = [parameter_id for parameter_id in requested if parameter_id not in parameter_by_id]
    if missing:
        raise ValueError(f"design parameter not found: {missing[0]}")

    selected = _expand_upstream_dependencies(parameter_by_id, requested) if include_dependencies else set(requested)
    order = _topological_order(parameter_by_id, selected, requested)

    entries = []
    ownership = {}
    target_signatures = []
    for parameter_id in order:
        parameter, plan, _ = _build_apply_plan(scene, parameter_id)
        for item in plan:
            signature = _target_signature(item)
            previous = ownership.get(signature)
            if previous is not None and previous != parameter_id:
                target = ":".join(signature)
                raise ValueError(f"design-intent batch target collision: {target} driven by {previous} and {parameter_id}")
            ownership[signature] = parameter_id
            if signature not in target_signatures:
                target_signatures.append(signature)
        entries.append({"parameter_id": parameter_id, "parameter": parameter, "plan": plan})

    return {
        "requested": requested,
        "selected": selected,
        "order": order,
        "entries": entries,
        "target_signatures": target_signatures,
        "graph_audit": graph_audit,
        "include_dependencies": bool(include_dependencies),
    }


def preflight_design_parameter_batch(scene, parameter_ids, include_dependencies=True):
    batch = _build_batch_execution_plan(scene, parameter_ids, include_dependencies=include_dependencies)
    return {
        "schema": BATCH_APPLY_SCHEMA,
        "status": "PASS",
        "requested_parameter_ids": list(batch["requested"]),
        "execution_order": list(batch["order"]),
        "expanded_parameter_ids": list(batch["order"]),
        "parameter_count": len(batch["entries"]),
        "binding_count": sum(len(entry["plan"]) for entry in batch["entries"]),
        "target_signatures": [": ".join(signature) for signature in batch["target_signatures"]],
        "include_dependencies": batch["include_dependencies"],
        "transaction_mode": "ATOMIC_ALL_OR_ROLLBACK",
        "dry_run": True,
        "geometry_mutated": False,
        "solver_claim": False,
        "automatic_parameter_value_derivation": False,
        "automatic_parameter_geometry_rebuild": False,
        "cad_parametric_feature_rebuild_claim": False,
    }


def _next_batch_id(scene):
    counter = int(scene.get(BATCH_COUNTER_KEY, 0)) + 1
    scene[BATCH_COUNTER_KEY] = counter
    return f"OLE_BATCH::B{counter:04d}"


def _record_last_batch(scene, payload):
    scene[LAST_BATCH_APPLY_KEY] = json.dumps(payload, sort_keys=True, ensure_ascii=False)


def _collect_impact(entry):
    model_impacted = []
    relation_driven = []
    for item in entry["plan"]:
        if item["kind"] in {"OBJECT", "FEATURE"}:
            oid = object_id(item["object"])
            if oid and oid not in model_impacted:
                model_impacted.append(oid)
        elif item["kind"] == "RELATION":
            driven_id = item["relation"].get("driven_id", "")
            if driven_id and driven_id not in relation_driven:
                relation_driven.append(driven_id)
    return model_impacted, relation_driven


def apply_design_parameter_batch(scene, parameter_ids, include_dependencies=True):
    batch = _build_batch_execution_plan(scene, parameter_ids, include_dependencies=include_dependencies)
    batch_id = _next_batch_id(scene)

    snapshots = []
    for entry in batch["entries"]:
        for item in entry["plan"]:
            snapshots.append(_snapshot_item(item))

    applied_by_parameter = {}
    postchecks = {}
    try:
        for entry in batch["entries"]:
            parameter = entry["parameter"]
            parameter_id = entry["parameter_id"]
            applied = []
            for item in entry["plan"]:
                applied.append(_apply_plan_item(scene, parameter, item))
            applied_by_parameter[parameter_id] = applied

        # Postcheck only after all mutations are present. This validates the
        # final combined state rather than a transient intermediate state.
        for entry in batch["entries"]:
            parameter_id = entry["parameter_id"]
            postcheck = _postcheck_plan(scene, entry["parameter"], entry["plan"])
            postchecks[parameter_id] = postcheck
            if postcheck.get("status") != "PASS":
                raise ValueError(f"design-intent batch postcheck failed: {parameter_id}")
    except Exception as exc:
        for snapshot in reversed(snapshots):
            _restore_snapshot(snapshot)
        for view_layer in scene.view_layers:
            view_layer.update()
        for entry in batch["entries"]:
            _append_event(
                scene,
                "BATCH_APPLY_ROLLBACK",
                entry["parameter_id"],
                {"batch_id": batch_id, "reason": str(exc), "execution_order": list(batch["order"])},
            )
        result = {
            "schema": BATCH_APPLY_SCHEMA,
            "status": "ROLLED_BACK",
            "batch_id": batch_id,
            "requested_parameter_ids": list(batch["requested"]),
            "execution_order": list(batch["order"]),
            "parameters_applied_before_failure": list(applied_by_parameter.keys()),
            "rollback_performed": True,
            "reason": str(exc),
            "solver_claim": False,
            "automatic_parameter_value_derivation": False,
            "automatic_parameter_geometry_rebuild": False,
            "cad_parametric_feature_rebuild_claim": False,
        }
        _record_last_batch(scene, result)
        raise ValueError(f"design-intent batch rolled back: {exc}") from exc

    model_impacted = []
    relation_driven = []
    failed_relation_ids = []
    geometry_mutated = False
    reference_geometry_mutated = False
    metadata_mutated = False

    for entry in batch["entries"]:
        impacted, driven = _collect_impact(entry)
        for oid in impacted:
            if oid not in model_impacted:
                model_impacted.append(oid)
        for oid in driven:
            if oid not in relation_driven:
                relation_driven.append(oid)
        for result in applied_by_parameter.get(entry["parameter_id"], []):
            geometry_mutated = geometry_mutated or bool(result.get("model_geometry_mutated"))
            reference_geometry_mutated = reference_geometry_mutated or bool(result.get("reference_geometry_mutated"))
            metadata_mutated = metadata_mutated or result.get("target_kind") == "RELATION"
            if result.get("target_kind") == "RELATION" and result.get("relation_status") == "FAIL":
                relation_id = result.get("target_id", "")
                if relation_id and relation_id not in failed_relation_ids:
                    failed_relation_ids.append(relation_id)

    downstream = (
        mark_downstream_stale(model_impacted, reason=f"DESIGN_INTENT_BATCH_APPLY:{batch_id}", scene=scene)
        if model_impacted
        else []
    )

    relation_downstream = []
    if failed_relation_ids:
        reason = f"DESIGN_INTENT_BATCH_RELATION_FAIL:{batch_id}:{','.join(failed_relation_ids)}"
        for oid in relation_driven:
            obj = _find_object_by_id(scene, oid)
            if obj is None:
                continue
            meta = getattr(obj, "oleander", None)
            if meta is not None and hasattr(meta, "stale"):
                meta.stale = True
            obj["oleander_stale_reason"] = reason
        relation_downstream = mark_downstream_stale(relation_driven, reason=reason, scene=scene) if relation_driven else []

    for entry in batch["entries"]:
        parameter_id = entry["parameter_id"]
        _clear_direct_parameter_stale(scene, parameter_id, entry["plan"])
        _append_event(
            scene,
            "BATCH_APPLY_COMMIT",
            parameter_id,
            {
                "batch_id": batch_id,
                "execution_order": list(batch["order"]),
                "applied": applied_by_parameter.get(parameter_id, []),
                "postcheck": postchecks.get(parameter_id, {}),
                "downstream_stale": downstream,
                "relation_downstream_stale": relation_downstream,
            },
        )

    result = {
        "schema": BATCH_APPLY_SCHEMA,
        "status": "PASS",
        "batch_id": batch_id,
        "requested_parameter_ids": list(batch["requested"]),
        "execution_order": list(batch["order"]),
        "parameter_count": len(batch["entries"]),
        "binding_count": sum(len(entry["plan"]) for entry in batch["entries"]),
        "postchecks": postchecks,
        "downstream_stale": downstream,
        "relation_downstream_stale": relation_downstream,
        "failed_relation_ids": failed_relation_ids,
        "model_geometry_mutated": geometry_mutated,
        "reference_geometry_mutated": reference_geometry_mutated,
        "metadata_mutated": metadata_mutated,
        "rollback_performed": False,
        "solver_claim": False,
        "automatic_parameter_value_derivation": False,
        "automatic_parameter_geometry_rebuild": False,
        "cad_parametric_feature_rebuild_claim": False,
    }
    _record_last_batch(scene, result)
    return result


class OLEANDER_OT_preflight_design_parameter_batch(bpy.types.Operator):
    bl_idname = "oleander.preflight_design_parameter_batch"
    bl_label = "Preflight Parameter Batch"
    bl_description = "Dry-run a dependency-ordered atomic Design Intent batch; does not mutate geometry"
    bl_options = {"REGISTER"}

    parameter_ids: StringProperty(name="Parameter IDs", description="Comma-separated OLE_PARAM IDs", default="")
    include_dependencies: BoolProperty(name="Include Upstream Dependencies", default=True)

    def execute(self, context):
        try:
            result = preflight_design_parameter_batch(context.scene, self.parameter_ids, self.include_dependencies)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Batch preflight PASS: {result['parameter_count']} parameter(s); solver_claim=false")
        return {"FINISHED"}


class OLEANDER_OT_apply_design_parameter_batch(bpy.types.Operator):
    bl_idname = "oleander.apply_design_parameter_batch"
    bl_label = "Apply Parameter Batch"
    bl_description = "Explicit atomic Design Intent batch apply with whole-batch rollback; not a solver"
    bl_options = {"REGISTER", "UNDO"}

    parameter_ids: StringProperty(name="Parameter IDs", description="Comma-separated OLE_PARAM IDs", default="")
    include_dependencies: BoolProperty(name="Include Upstream Dependencies", default=True)

    def execute(self, context):
        try:
            result = apply_design_parameter_batch(context.scene, self.parameter_ids, self.include_dependencies)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Batch applied {result['parameter_count']} parameter(s); solver_claim=false")
        return {"FINISHED"}


class OLEANDER_PT_design_intent_batch(bpy.types.Panel):
    bl_label = "Design Intent Batch"
    bl_idname = "OLEANDER_PT_design_intent_batch"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OLEANDER"
    bl_parent_id = "OLEANDER_PT_design_intent_apply"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Dependency-ordered explicit transaction")
        layout.label(text="Dry-run → atomic apply → postcheck/rollback")
        layout.label(text="No solver / no derived-value computation", icon="INFO")
        layout.operator("oleander.preflight_design_parameter_batch", icon="CHECKMARK")
        layout.operator("oleander.apply_design_parameter_batch", icon="FILE_REFRESH")


OPERATOR_CLASSES = (
    OLEANDER_OT_preflight_design_parameter_batch,
    OLEANDER_OT_apply_design_parameter_batch,
)

PANEL_CLASSES = (OLEANDER_PT_design_intent_batch,)
