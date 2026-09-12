"""OLEANDER Blender Inspector v0.3 skeleton.

Runtime UI adapter. Keeps Blender UI as a view over OLEANDER state,
not as the authority source.
"""

from __future__ import annotations


def inspector_payload(ole_object: dict, relations=None, validations=None):
    return {
        "id": ole_object.get("id"),
        "type": ole_object.get("type"),
        "intent": ole_object.get("intent", {}),
        "parameters": ole_object.get("parameters", {}),
        "relations": relations or [],
        "validations": validations or [],
        "authority": ole_object.get("validation", {}).get("state", "UNKNOWN"),
    }


__all__ = ["inspector_payload"]
