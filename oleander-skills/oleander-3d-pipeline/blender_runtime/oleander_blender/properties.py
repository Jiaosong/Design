import bpy


MASTER_TYPES = [
    ("BLENDER_NATIVE", "Blender Native", "Blender object/data is the editable master"),
    ("CAD_NATIVE", "CAD Native", "Specialist CAD source is authoritative; Blender is a derivative/review representation"),
    ("BIM_NATIVE", "BIM Native", "Specialist BIM source is authoritative"),
    ("EXTERNAL_NATIVE", "External Native", "Another governed native source is authoritative"),
]

GEOMETRY_AUTHORITY = [
    ("VERIFIED_SOURCE", "Verified Source", "Geometry is bound to a verified source"),
    ("GOVERNED_ESTIMATE", "Governed Estimate", "Geometry uses an explicit design estimate and remains subject to verification"),
    ("FIELD_OPEN", "Field Open", "Field geometry truth remains open"),
    ("VISUAL_ONLY", "Visual Only", "Geometry has visualization authority only"),
]

MATERIAL_AUTHORITY = [
    ("SPECIFIED", "Specified", "Material specification is governed"),
    ("ESTIMATE", "Estimate", "Material is an explicit estimate"),
    ("VISUAL_ONLY", "Visual Only", "Shader/appearance only"),
]

FIELD_STATE = [
    ("VERIFIED", "Verified", "Field state verified by governed evidence"),
    ("OPEN", "Open", "Field verification remains open"),
    ("NOT_APPLICABLE", "N/A", "Field verification is not applicable"),
]

ENGINEERING_STATE = [
    ("APPROVED", "Approved", "Engineering approval is recorded externally"),
    ("OPEN", "Open", "Engineering approval remains open"),
    ("NOT_APPLICABLE", "N/A", "Engineering approval is not applicable"),
]

MANUFACTURING_STATE = [
    ("RELEASED", "Released", "Manufacturing release is recorded externally"),
    ("OPEN", "Open", "Manufacturing release remains open"),
    ("NOT_APPLICABLE", "N/A", "Manufacturing release is not applicable"),
]


class OLEANDER_ObjectMetadata(bpy.types.PropertyGroup):
    ole_id: bpy.props.StringProperty(
        name="OLE ID",
        description="Persistent OLEANDER logical object identity; must remain stable across ordinary renames",
    )
    object_class: bpy.props.StringProperty(name="Object Class")
    master_type: bpy.props.EnumProperty(name="Master Type", items=MASTER_TYPES, default="BLENDER_NATIVE")
    master_locator: bpy.props.StringProperty(name="Master Locator")
    geometry_authority: bpy.props.EnumProperty(
        name="Geometry Authority", items=GEOMETRY_AUTHORITY, default="FIELD_OPEN"
    )
    material_authority: bpy.props.EnumProperty(
        name="Material Authority", items=MATERIAL_AUTHORITY, default="VISUAL_ONLY"
    )
    field_state: bpy.props.EnumProperty(name="Field", items=FIELD_STATE, default="OPEN")
    engineering_state: bpy.props.EnumProperty(
        name="Engineering", items=ENGINEERING_STATE, default="OPEN"
    )
    manufacturing_state: bpy.props.EnumProperty(
        name="Manufacturing", items=MANUFACTURING_STATE, default="OPEN"
    )
    lod: bpy.props.IntProperty(name="LOD", default=100, min=0, max=500)
    assembly_id: bpy.props.StringProperty(name="Assembly ID")
    stale: bpy.props.BoolProperty(
        name="Downstream Stale",
        description="Marks this representation/output as stale relative to an upstream authority",
        default=False,
    )
