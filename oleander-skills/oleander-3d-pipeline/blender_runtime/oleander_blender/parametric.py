import json


def get_parameters(obj):
    raw = obj.get("oleander_parameters", "{}")
    if isinstance(raw, dict):
        return dict(raw)
    try:
        value = json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def set_parameters(obj, params):
    clean = {}
    for key, value in params.items():
        if isinstance(value, (str, int, float, bool)) or value is None:
            clean[str(key)] = value
    obj["oleander_parameters"] = json.dumps(clean, sort_keys=True)
    return clean


def update_parameter(obj, name, value):
    params = get_parameters(obj)
    params[str(name)] = value
    return set_parameters(obj, params)


def get_constraints(obj):
    raw = obj.get("oleander_constraints", "[]")
    try:
        value = json.loads(raw) if isinstance(raw, str) else raw
    except (TypeError, json.JSONDecodeError):
        return []
    return value if isinstance(value, list) else []


def set_constraints(obj, constraints):
    clean = []
    for item in constraints:
        if not isinstance(item, dict):
            continue
        if "type" not in item:
            continue
        clean.append({str(k): v for k, v in item.items() if isinstance(v, (str, int, float, bool)) or v is None})
    obj["oleander_constraints"] = json.dumps(clean, sort_keys=True)
    return clean


def add_constraint(obj, constraint_type, **payload):
    constraints = get_constraints(obj)
    entry = {"type": constraint_type}
    entry.update(payload)
    constraints.append(entry)
    return set_constraints(obj, constraints)
