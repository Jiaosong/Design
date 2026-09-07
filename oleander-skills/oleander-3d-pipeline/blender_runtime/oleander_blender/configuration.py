import json
from datetime import datetime, timezone

from .parametric import get_parameters, set_parameters


CONFIG_KEY = "oleander_configurations_v0_1"


def _object_key(obj):
    meta = getattr(obj, "oleander", None)
    return (getattr(meta, "ole_id", "") or obj.name).strip()


def load_configurations(scene):
    raw = scene.get(CONFIG_KEY, "{}")
    try:
        data = json.loads(raw) if isinstance(raw, str) else raw
    except (TypeError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def save_configurations(scene, configs):
    scene[CONFIG_KEY] = json.dumps(configs, sort_keys=True)


def capture_configuration(scene, name):
    name = name.strip()
    if not name:
        raise ValueError("configuration name is required")

    objects = {}
    for obj in scene.objects:
        key = _object_key(obj)
        objects[key] = {
            "name_at_capture": obj.name,
            "location": list(obj.location),
            "rotation_euler": list(obj.rotation_euler),
            "scale": list(obj.scale),
            "hide_viewport": bool(obj.hide_viewport),
            "hide_render": bool(obj.hide_render),
            "parameters": get_parameters(obj),
        }

    configs = load_configurations(scene)
    configs[name] = {
        "schema": "OLEANDER_CONFIGURATION_v0.1",
        "captured_utc": datetime.now(timezone.utc).isoformat(),
        "objects": objects,
        "authority_note": "Configuration records transform/visibility/parameter metadata state only; it is not a geometry or engineering approval branch.",
    }
    save_configurations(scene, configs)
    return configs[name]


def restore_configuration(scene, name):
    configs = load_configurations(scene)
    config = configs.get(name)
    if not config:
        raise KeyError(name)

    current = {_object_key(obj): obj for obj in scene.objects}
    restored = []
    missing = []

    for key, state in config.get("objects", {}).items():
        obj = current.get(key)
        if obj is None:
            missing.append(key)
            continue
        obj.location = state.get("location", obj.location)
        obj.rotation_euler = state.get("rotation_euler", obj.rotation_euler)
        obj.scale = state.get("scale", obj.scale)
        obj.hide_viewport = bool(state.get("hide_viewport", obj.hide_viewport))
        obj.hide_render = bool(state.get("hide_render", obj.hide_render))
        if isinstance(state.get("parameters"), dict):
            set_parameters(obj, state["parameters"])
        restored.append(key)

    return {"restored": restored, "missing": missing}


def configuration_names(scene):
    return sorted(load_configurations(scene))
