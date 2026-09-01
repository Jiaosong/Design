bl_info = {
    "name": "OLEANDER Blender Runtime",
    "author": "OLEANDER",
    "version": (0, 1, 0),
    "blender": (5, 1, 0),
    "location": "View3D > Sidebar > OLEANDER",
    "description": "Governed object identity, authority metadata, audit and manifest tools for OLEANDER 3D",
    "category": "3D View",
}

import bpy

from .properties import OLEANDER_ObjectMetadata
from .operators import (
    OLEANDER_OT_assign_identity,
    OLEANDER_OT_run_audit,
    OLEANDER_OT_mark_stale,
    OLEANDER_OT_export_manifest,
)
from .panel import OLEANDER_PT_runtime_panel

CLASSES = (
    OLEANDER_ObjectMetadata,
    OLEANDER_OT_assign_identity,
    OLEANDER_OT_run_audit,
    OLEANDER_OT_mark_stale,
    OLEANDER_OT_export_manifest,
    OLEANDER_PT_runtime_panel,
)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Object.oleander = bpy.props.PointerProperty(type=OLEANDER_ObjectMetadata)


def unregister():
    if hasattr(bpy.types.Object, "oleander"):
        del bpy.types.Object.oleander
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
