bl_info = {
    "name": "OLEANDER Blender Runtime",
    "author": "OLEANDER",
    "version": (0, 2, 0),
    "blender": (5, 1, 0),
    "location": "View3D > Sidebar > OLEANDER",
    "description": "Governed identity, semantics, configurations, relation/dependency/diff, BOM, audit and manifest workbench for OLEANDER 3D",
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
from .direct_model import CLASSES as DIRECT_MODEL_CLASSES
from .feature_stack import CLASSES as FEATURE_STACK_CLASSES
from .feature_edit import OPERATOR_CLASSES as FEATURE_EDIT_OPERATOR_CLASSES
from .feature_edit import PANEL_CLASSES as FEATURE_EDIT_PANEL_CLASSES
from .relation_kernel import OPERATOR_CLASSES as RELATION_OPERATOR_CLASSES
from .relation_kernel import PANEL_CLASSES as RELATION_PANEL_CLASSES
from .workbench_ops import CLASSES as WORKBENCH_OPERATOR_CLASSES
from .configuration_ops import CLASSES as CONFIGURATION_CLASSES
from .bom import CLASSES as BOM_CLASSES
from .panel import OLEANDER_PT_runtime_panel
from .workbench_panel import CLASSES as WORKBENCH_PANEL_CLASSES

OPERATOR_CLASSES = (
    OLEANDER_OT_assign_identity,
    OLEANDER_OT_run_audit,
    OLEANDER_OT_mark_stale,
    OLEANDER_OT_export_manifest,
    *DIRECT_MODEL_CLASSES,
    *FEATURE_STACK_CLASSES,
    *FEATURE_EDIT_OPERATOR_CLASSES,
    *RELATION_OPERATOR_CLASSES,
    *WORKBENCH_OPERATOR_CLASSES,
    *CONFIGURATION_CLASSES,
    *BOM_CLASSES,
)

PANEL_CLASSES = (
    OLEANDER_PT_runtime_panel,
    *WORKBENCH_PANEL_CLASSES,
    *FEATURE_EDIT_PANEL_CLASSES,
    *RELATION_PANEL_CLASSES,
)


def register():
    bpy.utils.register_class(OLEANDER_ObjectMetadata)
    bpy.types.Object.oleander = bpy.props.PointerProperty(type=OLEANDER_ObjectMetadata)
    for cls in OPERATOR_CLASSES:
        bpy.utils.register_class(cls)
    for cls in PANEL_CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(PANEL_CLASSES):
        bpy.utils.unregister_class(cls)
    for cls in reversed(OPERATOR_CLASSES):
        bpy.utils.unregister_class(cls)
    if hasattr(bpy.types.Object, "oleander"):
        del bpy.types.Object.oleander
    bpy.utils.unregister_class(OLEANDER_ObjectMetadata)


if __name__ == "__main__":
    register()
