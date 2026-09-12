"""OLEANDER Surface System Adapter v0.4."""

from datetime import datetime, timezone


def bind_surface_source(surface_id="OLE-GEO-0001"):
    return {
        "id": surface_id,
        "system": "Blender Surface System v1.21",
        "kernel": "Geometry Kernel",
        "authority": "SOURCE",
        "created": datetime.now(timezone.utc).isoformat(),
    }


def make_surface_validation(surface_id, check, result):
    return {
        "target": surface_id,
        "domain": "surface",
        "check": check,
        "result": result,
        "authority": "DERIVED",
    }


__all__ = ["bind_surface_source", "make_surface_validation"]
