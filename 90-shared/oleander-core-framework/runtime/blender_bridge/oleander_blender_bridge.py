"""OLEANDER Blender Bridge v0.1

Initial runtime adapter. The bridge keeps Blender objects and OLEANDER
semantic objects linked through stable IDs without replacing Blender's
native geometry ownership.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_ole_object(object_id: str, object_type: str, intent: dict, source: dict):
    return {
        "id": object_id,
        "type": object_type,
        "intent": intent,
        "parameters": {},
        "constraints": [],
        "source": source,
        "material": {},
        "manufacturing": {},
        "validation": {
            "state": "WORKING_SOURCE",
            "checks": []
        },
        "evidence": []
    }


def attach_blender_properties(obj, ole_object: dict):
    """Attach semantic identity to a Blender object.

    Designed to run inside Blender where obj supports custom properties.
    """
    obj["OLE_ID"] = ole_object["id"]
    obj["OLE_TYPE"] = ole_object["type"]
    obj["OLE_STATE"] = ole_object["validation"]["state"]


def export_registry(objects, output: str):
    payload = {
        "objects": objects,
        "version": "0.2.0",
        "authority": "WORKING_SOURCE",
        "generated": utc_now()
    }
    Path(output).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def scan_blender_object(obj):
    """Read OLE identity from Blender custom properties."""
    return {
        "id": obj.get("OLE_ID"),
        "type": obj.get("OLE_TYPE"),
        "state": obj.get("OLE_STATE")
    }


__all__ = ["make_ole_object", "attach_blender_properties", "scan_blender_object", "export_registry"]
