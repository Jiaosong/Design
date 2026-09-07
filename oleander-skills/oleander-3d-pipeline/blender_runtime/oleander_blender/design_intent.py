"""OLEANDER Design Intent Graph foundation.

This module stores primary/derived design parameters as stable scene data and
binds them to existing OLE object, datum/reference, feature and relation IDs.
It tracks parameter dependencies, revisions, failure-envelope metadata, diffs
and stale propagation. It deliberately does NOT solve constraints, rebuild CAD
features or automatically mutate geometry from parameter values.
"""

from __future__ import annotations

import hashlib
import json

import bpy

from .dependency import mark_downstream_stale, object_id
from .feature_stack import get_feature_history
from .relation_kernel import get_relations

DESIGN_INTENT_SCHEMA = "OLEANDER_DESIGN_INTENT_GRAPH_v0.1"
PARAMETERS_KEY = "oleander_design_parameters"
PARAMETER_COUNTER_KEY = "oleander_design_parameter_counter"
PARAMETER_EVENTS_KEY = "oleander_design_parameter_events"
PARAMETER_EVENT_COUNTER_KEY = "oleander_design_parameter_event_counter"
BASELINE_KEY = "oleander_design_intent_baseline"
LAST_AUDIT_KEY = "oleander_design_intent_audit"
LAST_DIFF_KEY = "oleander_design_intent_diff"

NUMERIC_KINDS = {"LENGTH_MM", "ANGLE_DEG", "COUNT", "RATIO", "SCALAR"}
PARAMETER_KINDS = NUMERIC_KINDS | {"BOOLEAN", "ENUM"}
PARAMETER_ROLES = {"PRIMARY", "DERIVED", "GOVERNED_ESTIMATE"}
PARAMETER_AUTHORITIES = {"INTENT_ONLY", "VERIFIED_SOURCE", "GOVERNED_ESTIMATE"}
TARGET_KINDS = {"OBJECT", "DATUM_REFERENCE", "FEATURE", "RELATION"}
UNIT_BY_KIND = {
    "LENGTH_MM": "mm",
    "ANGLE_DEG": "deg",
    "COUNT": "count",
    "RATIO": "ratio",
    "SCALAR": "scalar",
    "BOOLEAN": "bool",
    "ENUM": "enum",
}


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


def get_design_parameters(scene=None):
    scene = scene or bpy.context.scene
    return _read_json_list(scene, PARAMETERS_KEY)


def get_design_parameter_events(scene=None):
    scene = scene or bpy.context.scene
    return _read_json_list(scene, PARAMETER_EVENTS_KEY)


def _set_design_parameters(scene, parameters):
    _write_json_list(scene, PARAMETERS_KEY, parameters)


def _append_event(scene, action, parameter_id, payload=None):
    counter = int(scene.get(PARAMETER_EVENT_COUNTER_KEY, 0)) + 1
    scene[PARAMETER_EVENT_COUNTER_KEY] = counter
    event = {
        "event_id": f"OLE_PARAM_EVT::E{counter:04d}",
        "event_index": counter,
        "action": action,
        "parameter_id": parameter_id,
        "payload": payload or {},
    }
    events = get_design_parameter_events(scene)
    events.append(event)
    _write_json_list(scene, PARAMETER_EVENTS_KEY, events)
    return event


def _parameter_by_id(parameters, parameter_id):
    for parameter in parameters:
        if parameter.get("parameter_id") == parameter_id:
            return parameter
    return None


def _normalize_value(kind, value):
    if kind not in PARAMETER_KINDS:
        raise ValueError(f"unsupported parameter kind: {kind}")
    if kind == "BOOLEAN":
        if not isinstance(value, bool):
            raise ValueError("BOOLEAN parameter value must be bool")
        return bool(value)
    if kind == "ENUM":
        if not isinstance(value, str) or not value.strip():
            raise ValueError("ENUM parameter value must be a non-empty string")
        return value.strip()
    if isinstance(value, bool):
        raise ValueError(f"{kind} parameter value must be numeric")
    if kind == "COUNT":
        numeric = float(value)
        if not numeric.is_integer() or numeric < 0:
            raise ValueError("COUNT parameter value must be a non-negative integer")
        return int(numeric)
    return float(value)


def _normalize_envelope(kind, minimum=None, maximum=None):
    if minimum is None and maximum is None:
        return None, None
    if kind not in NUMERIC_KINDS:
        raise ValueError("failure envelope is only supported for numeric parameters")
    low = None if minimum is None else float(minimum)
    high = None if maximum is None else float(maximum)
    if low is not None and high is not None and low > high:
        raise ValueError("failure envelope minimum cannot exceed maximum")
    return low, high


def evaluate_failure_envelope(parameter):
    low = parameter.get("min_value")
    high = parameter.get("max_value")
    if low is None and high is None:
        return {"status": "NOT_DECLARED", "parameter_id": parameter.get("parameter_id", "")}
    value = parameter.get("value")
    if parameter.get("kind") not in NUMERIC_KINDS:
        return {"status": "INVALID", "parameter_id": parameter.get("parameter_id", ""), "reason": "NON_NUMERIC_ENVELOPE"}
    below = low is not None and value < low
    above = high is not None and value > high
    return {
        "status": "FAIL" if below or above else "PASS",
        "parameter_id": parameter.get("parameter_id", ""),
        "value": value,
        "minimum": low,
        "maximum": high,
        "reason": "OUTSIDE_FAILURE_ENVELOPE" if below or above else "WITHIN_FAILURE_ENVELOPE",
    }


def create_design_parameter(
    scene,
    name,
    kind,
    value,
    *,
    role="PRIMARY",
    authority="INTENT_ONLY",
    minimum=None,
    maximum=None,
):
    name = str(name).strip()
    if not name:
        raise ValueError("parameter name is required")
    if role not in PARAMETER_ROLES:
        raise ValueError(f"unsupported parameter role: {role}")
    if authority not in PARAMETER_AUTHORITIES:
        raise ValueError(f"unsupported parameter authority: {authority}")
    parameters = get_design_parameters(scene)
    if any(item.get("name") == name for item in parameters):
        raise ValueError(f"active parameter name already exists: {name}")
    normalized = _normalize_value(kind, value)
    low, high = _normalize_envelope(kind, minimum, maximum)
    counter = int(scene.get(PARAMETER_COUNTER_KEY, 0)) + 1
    scene[PARAMETER_COUNTER_KEY] = counter
    parameter_id = f"OLE_PARAM::P{counter:04d}"
    parameter = {
        "schema": DESIGN_INTENT_SCHEMA,
        "parameter_id": parameter_id,
        "name": name,
        "kind": kind,
        "unit": UNIT_BY_KIND[kind],
        "value": normalized,
        "role": role,
        "authority": authority,
        "min_value": low,
        "max_value": high,
        "revision": 1,
        "dependencies": [],
        "bindings": [],
        "solver_claim": False,
        "automatic_geometry_apply": False,
    }
    parameters.append(parameter)
    _set_design_parameters(scene, parameters)
    _append_event(scene, "CREATE", parameter_id, {"name": name, "kind": kind})
    return parameter


def _find_object_by_ole_id(scene, target_id):
    for obj in scene.objects:
        if object_id(obj) == target_id:
            return obj
    return None


def _find_datum_reference(scene, target_id):
    for obj in scene.objects:
        if obj.get("oleander_guide_id", "") != target_id:
            continue
        kind = obj.get("oleander_guide_kind", "")
        if kind in {"DATUM_AXIS", "DATUM_PLANE", "CONSTRUCTION_LINE"}:
            return obj
    return None


def _find_feature(scene, target_id):
    for obj in scene.objects:
        for feature in get_feature_history(obj):
            if feature.get("feature_id") == target_id:
                return obj, feature
    return None, None


def _find_relation(scene, target_id):
    for relation in get_relations(scene):
        if relation.get("relation_id") == target_id:
            return relation
    return None


def resolve_binding(scene, binding):
    kind = binding.get("target_kind", "")
    target_id = binding.get("target_id", "")
    if kind == "OBJECT":
        obj = _find_object_by_ole_id(scene, target_id)
        return {"valid": obj is not None, "object_ids": [target_id] if obj else [], "target": obj}
    if kind == "DATUM_REFERENCE":
        obj = _find_datum_reference(scene, target_id)
        return {"valid": obj is not None, "object_ids": [], "target": obj}
    if kind == "FEATURE":
        obj, feature = _find_feature(scene, target_id)
        return {"valid": feature is not None, "object_ids": [object_id(obj)] if obj else [], "target": feature}
    if kind == "RELATION":
        relation = _find_relation(scene, target_id)
        ids = []
        if relation:
            for key in ("driver_id", "driven_id"):
                oid = relation.get(key, "")
                if oid and oid not in ids:
                    ids.append(oid)
        return {"valid": relation is not None, "object_ids": ids, "target": relation}
    return {"valid": False, "object_ids": [], "target": None}


def bind_design_parameter(scene, parameter_id, target_kind, target_id, target_field):
    if target_kind not in TARGET_KINDS:
        raise ValueError(f"unsupported design-intent target kind: {target_kind}")
    target_id = str(target_id).strip()
    target_field = str(target_field).strip()
    if not target_id or not target_field:
        raise ValueError("design-intent binding requires target ID and target field")
    parameters = get_design_parameters(scene)
    parameter = _parameter_by_id(parameters, parameter_id)
    if parameter is None:
        raise ValueError(f"design parameter not found: {parameter_id}")
    binding = {"target_kind": target_kind, "target_id": target_id, "target_field": target_field}
    resolved = resolve_binding(scene, binding)
    if not resolved["valid"]:
        raise ValueError(f"design-intent target not found: {target_kind}:{target_id}")
    if binding in parameter.get("bindings", []):
        raise ValueError("duplicate design-intent binding")
    parameter.setdefault("bindings", []).append(binding)
    parameter["revision"] = int(parameter.get("revision", 0)) + 1
    _set_design_parameters(scene, parameters)
    _append_event(scene, "BIND", parameter_id, binding)
    return binding


def _parameter_forward(parameters):
    ids = {item.get("parameter_id") for item in parameters}
    forward = {item.get("parameter_id"): list(item.get("dependencies", [])) for item in parameters}
    missing = {
        pid: [dep for dep in dependencies if dep not in ids]
        for pid, dependencies in forward.items()
        if any(dep not in ids for dep in dependencies)
    }
    return forward, missing


def _parameter_cycles(forward):
    visiting = set()
    visited = set()
    cycles = []

    def walk(node, path):
        if node in visiting:
            try:
                index = path.index(node)
            except ValueError:
                index = 0
            cycles.append(path[index:] + [node])
            return
        if node in visited:
            return
        visiting.add(node)
        path.append(node)
        for dep in forward.get(node, []):
            walk(dep, path)
        path.pop()
        visiting.remove(node)
        visited.add(node)

    for node in forward:
        walk(node, [])
    return cycles


def add_parameter_dependency(scene, parameter_id, upstream_parameter_id):
    if parameter_id == upstream_parameter_id:
        raise ValueError("design parameter cannot depend on itself")
    parameters = get_design_parameters(scene)
    parameter = _parameter_by_id(parameters, parameter_id)
    upstream = _parameter_by_id(parameters, upstream_parameter_id)
    if parameter is None or upstream is None:
        raise ValueError("design parameter dependency references a missing parameter")
    dependencies = parameter.setdefault("dependencies", [])
    if upstream_parameter_id in dependencies:
        raise ValueError("duplicate design parameter dependency")
    trial = json.loads(json.dumps(parameters))
    _parameter_by_id(trial, parameter_id).setdefault("dependencies", []).append(upstream_parameter_id)
    forward, _ = _parameter_forward(trial)
    if _parameter_cycles(forward):
        raise ValueError("design parameter dependency would create a cycle")
    dependencies.append(upstream_parameter_id)
    parameter["revision"] = int(parameter.get("revision", 0)) + 1
    _set_design_parameters(scene, parameters)
    _append_event(scene, "DEPENDENCY_ADD", parameter_id, {"upstream_parameter_id": upstream_parameter_id})
    return list(dependencies)


def _mark_object_intent_stale(obj, reason):
    if obj is None:
        return
    meta = getattr(obj, "oleander", None)
    if meta is not None and hasattr(meta, "stale"):
        meta.stale = True
    obj["oleander_design_intent_stale"] = True
    obj["oleander_stale_reason"] = reason


def update_design_parameter(scene, parameter_id, value):
    parameters = get_design_parameters(scene)
    parameter = _parameter_by_id(parameters, parameter_id)
    if parameter is None:
        raise ValueError(f"design parameter not found: {parameter_id}")
    before = parameter.get("value")
    after = _normalize_value(parameter.get("kind"), value)
    parameter["value"] = after
    parameter["revision"] = int(parameter.get("revision", 0)) + 1
    _set_design_parameters(scene, parameters)

    direct_ids = []
    unresolved = []
    for binding in parameter.get("bindings", []):
        resolved = resolve_binding(scene, binding)
        if not resolved["valid"]:
            unresolved.append(binding)
            continue
        for oid in resolved.get("object_ids", []):
            if oid not in direct_ids:
                direct_ids.append(oid)
        if binding.get("target_kind") == "DATUM_REFERENCE" and resolved.get("target") is not None:
            resolved["target"]["oleander_design_intent_review_required"] = True

    reason = f"DESIGN_PARAMETER_CHANGED:{parameter_id}"
    for oid in direct_ids:
        _mark_object_intent_stale(_find_object_by_ole_id(scene, oid), reason)
    downstream = mark_downstream_stale(direct_ids, reason=reason, scene=scene) if direct_ids else []
    event = _append_event(
        scene,
        "VALUE_UPDATE",
        parameter_id,
        {"before": before, "after": after, "direct_stale": direct_ids, "downstream_stale": downstream, "unresolved_bindings": unresolved},
    )
    return {
        "parameter_id": parameter_id,
        "before": before,
        "after": after,
        "revision": parameter["revision"],
        "direct_stale": direct_ids,
        "downstream_stale": downstream,
        "unresolved_bindings": unresolved,
        "envelope": evaluate_failure_envelope(parameter),
        "event_id": event["event_id"],
        "geometry_mutated": False,
        "solver_claim": False,
    }


def audit_design_intent_graph(scene=None):
    scene = scene or bpy.context.scene
    parameters = get_design_parameters(scene)
    ids = [item.get("parameter_id", "") for item in parameters]
    names = [item.get("name", "") for item in parameters]
    duplicate_ids = sorted({item for item in ids if item and ids.count(item) > 1})
    duplicate_names = sorted({item for item in names if item and names.count(item) > 1})
    forward, missing_parameter_dependencies = _parameter_forward(parameters)
    cycles = _parameter_cycles(forward)
    missing_bindings = []
    envelope_failures = []
    for parameter in parameters:
        envelope = evaluate_failure_envelope(parameter)
        if envelope.get("status") in {"FAIL", "INVALID"}:
            envelope_failures.append(envelope)
        for binding in parameter.get("bindings", []):
            if not resolve_binding(scene, binding)["valid"]:
                missing_bindings.append({"parameter_id": parameter.get("parameter_id"), **binding})
    failed = duplicate_ids or duplicate_names or missing_parameter_dependencies or cycles or missing_bindings or envelope_failures
    result = {
        "schema": DESIGN_INTENT_SCHEMA,
        "status": "FAIL" if failed else "PASS",
        "parameter_count": len(parameters),
        "duplicate_parameter_ids": duplicate_ids,
        "duplicate_parameter_names": duplicate_names,
        "missing_parameter_dependencies": missing_parameter_dependencies,
        "dependency_cycles": cycles,
        "missing_bindings": missing_bindings,
        "failure_envelope_breaches": envelope_failures,
        "solver_claim": False,
        "automatic_geometry_apply": False,
        "authority": "DESIGN_INTENT_METADATA_AND_DEPENDENCY_STATE_NOT_CAD_SOLVER",
    }
    scene[LAST_AUDIT_KEY] = json.dumps(result, sort_keys=True, ensure_ascii=False)
    return result


def _canonical_state(scene):
    parameters = get_design_parameters(scene)
    payload = {
        "schema": DESIGN_INTENT_SCHEMA,
        "parameters": sorted(parameters, key=lambda item: item.get("parameter_id", "")),
    }
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    payload["sha256"] = hashlib.sha256(encoded.encode("utf-8")).hexdigest()
    return payload


def store_design_intent_baseline(scene=None):
    scene = scene or bpy.context.scene
    payload = _canonical_state(scene)
    scene[BASELINE_KEY] = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return payload


def diff_design_intent_from_baseline(scene=None):
    scene = scene or bpy.context.scene
    raw = scene.get(BASELINE_KEY, "")
    if not raw:
        return {"status": "NO_BASELINE", "changed_parameters": [], "solver_claim": False}
    try:
        baseline = json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return {"status": "INVALID_BASELINE", "changed_parameters": [], "solver_claim": False}
    current = _canonical_state(scene)
    before = {item.get("parameter_id"): item for item in baseline.get("parameters", [])}
    after = {item.get("parameter_id"): item for item in current.get("parameters", [])}
    changed = []
    for pid in sorted(set(before) | set(after)):
        if before.get(pid) != after.get(pid):
            changed.append({"parameter_id": pid, "before": before.get(pid), "after": after.get(pid)})
    result = {
        "status": "CHANGED" if changed else "UNCHANGED",
        "baseline_sha256": baseline.get("sha256", ""),
        "current_sha256": current.get("sha256", ""),
        "changed_parameters": changed,
        "solver_claim": False,
        "automatic_geometry_apply": False,
    }
    scene[LAST_DIFF_KEY] = json.dumps(result, sort_keys=True, ensure_ascii=False)
    return result


PARAM_KIND_ITEMS = tuple((item, item.replace("_", " ").title(), "") for item in ("LENGTH_MM", "ANGLE_DEG", "COUNT", "RATIO", "SCALAR"))


class OLEANDER_OT_create_design_parameter(bpy.types.Operator):
    bl_idname = "oleander.create_design_parameter"
    bl_label = "Create Primary Parameter"
    bl_options = {"REGISTER", "UNDO"}

    name: bpy.props.StringProperty(name="Name", default="PrimaryLength")
    kind: bpy.props.EnumProperty(name="Kind", items=PARAM_KIND_ITEMS, default="LENGTH_MM")
    value: bpy.props.FloatProperty(name="Value", default=100.0)
    use_envelope: bpy.props.BoolProperty(name="Failure Envelope", default=False)
    minimum: bpy.props.FloatProperty(name="Minimum", default=0.0)
    maximum: bpy.props.FloatProperty(name="Maximum", default=1000.0)

    def execute(self, context):
        try:
            create_design_parameter(
                context.scene,
                self.name,
                self.kind,
                self.value,
                minimum=self.minimum if self.use_envelope else None,
                maximum=self.maximum if self.use_envelope else None,
            )
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        return {"FINISHED"}


class OLEANDER_OT_update_design_parameter(bpy.types.Operator):
    bl_idname = "oleander.update_design_parameter"
    bl_label = "Update Parameter Value"
    bl_options = {"REGISTER", "UNDO"}

    parameter_id: bpy.props.StringProperty(name="Parameter ID")
    value: bpy.props.FloatProperty(name="Value")

    def execute(self, context):
        try:
            result = update_design_parameter(context.scene, self.parameter_id, self.value)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"{self.parameter_id} rev {result['revision']}; geometry not auto-applied")
        return {"FINISHED"}


class OLEANDER_OT_bind_design_parameter_object(bpy.types.Operator):
    bl_idname = "oleander.bind_design_parameter_object"
    bl_label = "Bind Parameter to Active Object"
    bl_options = {"REGISTER", "UNDO"}

    parameter_id: bpy.props.StringProperty(name="Parameter ID")
    target_field: bpy.props.StringProperty(name="Intent Field", default="DIMENSION_X")

    def execute(self, context):
        obj = context.active_object
        if obj is None:
            self.report({"ERROR"}, "Select an active object")
            return {"CANCELLED"}
        target_id = getattr(getattr(obj, "oleander", None), "ole_id", "").strip()
        if not target_id:
            self.report({"ERROR"}, "Active object requires a stable OLE ID")
            return {"CANCELLED"}
        try:
            bind_design_parameter(context.scene, self.parameter_id, "OBJECT", target_id, self.target_field)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        return {"FINISHED"}


class OLEANDER_OT_audit_design_intent(bpy.types.Operator):
    bl_idname = "oleander.audit_design_intent"
    bl_label = "Audit Design Intent Graph"
    bl_options = {"REGISTER"}

    def execute(self, context):
        result = audit_design_intent_graph(context.scene)
        self.report({"INFO"}, f"Design Intent audit {result['status']}: {result['parameter_count']} parameter(s)")
        return {"FINISHED"}


class OLEANDER_OT_store_design_intent_baseline(bpy.types.Operator):
    bl_idname = "oleander.store_design_intent_baseline"
    bl_label = "Store Intent Baseline"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        payload = store_design_intent_baseline(context.scene)
        self.report({"INFO"}, f"Intent baseline {payload['sha256'][:12]}")
        return {"FINISHED"}


class OLEANDER_OT_diff_design_intent(bpy.types.Operator):
    bl_idname = "oleander.diff_design_intent"
    bl_label = "Diff Design Intent"
    bl_options = {"REGISTER"}

    def execute(self, context):
        result = diff_design_intent_from_baseline(context.scene)
        self.report({"INFO"}, f"Intent diff: {result['status']}")
        return {"FINISHED"}


class OLEANDER_PT_design_intent(bpy.types.Panel):
    bl_label = "Design Intent Graph"
    bl_idname = "OLEANDER_PT_design_intent"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OLEANDER"
    bl_parent_id = "OLEANDER_PT_runtime_panel"

    def draw(self, context):
        layout = self.layout
        layout.operator("oleander.create_design_parameter", text="Create Primary Parameter")
        layout.operator("oleander.audit_design_intent", text="Audit Intent Graph")
        row = layout.row(align=True)
        row.operator("oleander.store_design_intent_baseline", text="Baseline")
        row.operator("oleander.diff_design_intent", text="Diff")
        layout.label(text=f"Parameters: {len(get_design_parameters(context.scene))}")
        layout.label(text="Stable IDs + bindings + stale propagation", icon="INFO")
        layout.label(text="No solver / no automatic geometry rebuild", icon="INFO")


OPERATOR_CLASSES = (
    OLEANDER_OT_create_design_parameter,
    OLEANDER_OT_update_design_parameter,
    OLEANDER_OT_bind_design_parameter_object,
    OLEANDER_OT_audit_design_intent,
    OLEANDER_OT_store_design_intent_baseline,
    OLEANDER_OT_diff_design_intent,
)
PANEL_CLASSES = (OLEANDER_PT_design_intent,)
