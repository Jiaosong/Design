import bpy
import json
import math
import os
import sys
from mathutils import Vector

# C04 Yunshuiyi rebuild baseline v001
# Purpose: prove and persist a Blender-native editable rebuild route.
# Geometry is DESIGN_ESTIMATE / FIELD_OPEN and must not be read as engineering truth.

OUT_DIR = os.environ.get("C04_REBUILD_OUT", "/tmp/c04-yunshuiyi-rebuild")
os.makedirs(OUT_DIR, exist_ok=True)
BLEND_PATH = os.path.join(OUT_DIR, "C04_YUNSHUIYI_REBUILD_MASTER_v001.blend")
PREVIEW_PATH = os.path.join(OUT_DIR, "C04_YUNSHUIYI_REBUILD_MASTER_v001_preview.png")
MANIFEST_PATH = os.path.join(OUT_DIR, "C04_YUNSHUIYI_REBUILD_MASTER_v001_manifest.json")

# Clean scene.
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.filepath = PREVIEW_PATH
scene.render.image_settings.file_format = 'PNG'
if scene.world is None:
    scene.world = bpy.data.worlds.new("C04_YUNSHUIYI_WORLD")
scene.world.color = (0.035, 0.035, 0.035)

# Collection architecture.
master_col = bpy.data.collections.new("C04_YUNSHUIYI_REBUILD_v001")
scene.collection.children.link(master_col)
geo_col = bpy.data.collections.new("GEO")
ref_col = bpy.data.collections.new("REFERENCE")
master_col.children.link(geo_col)
master_col.children.link(ref_col)

# Remove default active collection link target ambiguity.
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[master_col.name]

# Design-estimate envelope in metres; no engineering authority.
L = 2.80
W = 0.92
H = 0.88
NU = 40
NV = 16

# Parametric ribbon surface: broad rest/lean object with a restrained rise.
verts = []
faces = []
for i in range(NU + 1):
    u = i / NU
    x = (u - 0.5) * L
    # Longitudinal profile: low entry, central support rise, tapered exit.
    longitudinal = 0.18 + 0.22 * math.exp(-((u - 0.56) / 0.22) ** 2)
    longitudinal += 0.10 * math.sin(math.pi * u) ** 2
    for j in range(NV + 1):
        v = j / NV
        y = (v - 0.5) * W
        edge = abs(v - 0.5) * 2.0
        # Edge rise + subtle asymmetric body-support bias.
        z = longitudinal + 0.13 * edge ** 2
        z += 0.11 * math.exp(-((u - 0.63) / 0.16) ** 2) * (0.35 + 0.65 * edge)
        # Keep a calmer contact basin near centreline.
        z -= 0.035 * math.exp(-((v - 0.5) / 0.24) ** 2) * math.sin(math.pi * u) ** 2
        verts.append((x, y, z))

row = NV + 1
for i in range(NU):
    for j in range(NV):
        a = i * row + j
        b = a + 1
        c = (i + 1) * row + j + 1
        d = (i + 1) * row + j
        faces.append((a, b, c, d))

mesh = bpy.data.meshes.new("C04_YUNSHUIYI_PRIMARY_SHELL_MESH")
mesh.from_pydata(verts, [], faces)
mesh.update()
obj = bpy.data.objects.new("C04_YUNSHUIYI_PRIMARY_SHELL", mesh)
geo_col.objects.link(obj)

# Governed metadata.
obj["OLE_ID"] = "C04_YUNSHUIYI_REBUILD_MASTER_v001"
obj["PROJECT_ID"] = "PRJ-C04-QINGJIANG-SHISHU"
obj["OBJECT_ROLE"] = "BLENDER_REBUILD_CANDIDATE"
obj["SOURCE_ROLE"] = "SOURCE_REFERENCE_DERIVED_FORM_INTENT"
obj["DIMENSION_AUTHORITY"] = "DESIGN_ESTIMATE"
obj["FIELD_STATE"] = "FIELD_OPEN"
obj["ENGINEERING_CLAIM"] = False
obj["DESIGN_KEEP_CLAIM"] = False

# Non-destructive feature stack.
solid = obj.modifiers.new("OLE_SOLIDIFY", 'SOLIDIFY')
solid.thickness = 0.045
solid.offset = -0.25
bev = obj.modifiers.new("OLE_BEVEL", 'BEVEL')
bev.width = 0.018
bev.segments = 3
subd = obj.modifiers.new("OLE_SUBD", 'SUBSURF')
subd.subdivision_type = 'CATMULL_CLARK'
subd.levels = 2
subd.render_levels = 2

# Material zones: one shell material + one non-mechanical contact overlay.
def make_mat(name, base, roughness, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*base, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return m

shell_mat = make_mat("MAT_YUNSHUIYI_SHELL", (0.19, 0.22, 0.22), 0.42, 0.05)
contact_mat = make_mat("MAT_YUNSHUIYI_CONTACT_ZONE", (0.33, 0.29, 0.23), 0.58, 0.0)
obj.data.materials.append(shell_mat)

# Contact zone is an explicit design/ergonomic semantic surface, not a claimed mechanical part.
contact_verts = []
contact_faces = []
ciu0, ciu1 = int(NU * 0.38), int(NU * 0.76)
cj0, cj1 = int(NV * 0.24), int(NV * 0.76)
for i in range(ciu0, ciu1 + 1):
    u = i / NU
    x = (u - 0.5) * L
    longitudinal = 0.18 + 0.22 * math.exp(-((u - 0.56) / 0.22) ** 2)
    longitudinal += 0.10 * math.sin(math.pi * u) ** 2
    for j in range(cj0, cj1 + 1):
        v = j / NV
        y = (v - 0.5) * W
        edge = abs(v - 0.5) * 2.0
        z = longitudinal + 0.13 * edge ** 2
        z += 0.11 * math.exp(-((u - 0.63) / 0.16) ** 2) * (0.35 + 0.65 * edge)
        z -= 0.035 * math.exp(-((v - 0.5) / 0.24) ** 2) * math.sin(math.pi * u) ** 2
        contact_verts.append((x, y, z + 0.012))

cnv = cj1 - cj0 + 1
cnu = ciu1 - ciu0 + 1
for i in range(cnu - 1):
    for j in range(cnv - 1):
        a = i * cnv + j
        b = a + 1
        c = (i + 1) * cnv + j + 1
        d = (i + 1) * cnv + j
        contact_faces.append((a, b, c, d))

cmesh = bpy.data.meshes.new("C04_YUNSHUIYI_CONTACT_ZONE_MESH")
cmesh.from_pydata(contact_verts, [], contact_faces)
cmesh.update()
contact = bpy.data.objects.new("C04_YUNSHUIYI_CONTACT_ZONE", cmesh)
geo_col.objects.link(contact)
contact.data.materials.append(contact_mat)
contact["SEMANTIC_ROLE"] = "BODY_CONTACT_ZONE_DESIGN_ESTIMATE"
contact["MECHANICAL_PART_CLAIM"] = False
csolid = contact.modifiers.new("OLE_CONTACT_SOLIDIFY", 'SOLIDIFY')
csolid.thickness = 0.008
cbev = contact.modifiers.new("OLE_CONTACT_BEVEL", 'BEVEL')
cbev.width = 0.006
cbev.segments = 2

# Editable centre datum/reference curve.
curve_data = bpy.data.curves.new("C04_YUNSHUIYI_DATUM_CURVE", type='CURVE')
curve_data.dimensions = '3D'
curve_data.bevel_depth = 0.004
spline = curve_data.splines.new('POLY')
spline.points.add(2)
for idx, co in enumerate(((-L/2, 0, 0.05), (0, 0, 0.05), (L/2, 0, 0.05))):
    spline.points[idx].co = (*co, 1.0)
datum = bpy.data.objects.new("DATUM_LONGITUDINAL_CENTER", curve_data)
ref_col.objects.link(datum)
datum.hide_render = True
datum["OLE_REFERENCE_ONLY"] = True

# Ground plane for preview only.
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0))
ground = bpy.context.object
ground.name = "PREVIEW_GROUND"
# Relink into reference collection.
for col in list(ground.users_collection):
    col.objects.unlink(ground)
ref_col.objects.link(ground)
ground.data.materials.append(make_mat("MAT_PREVIEW_GROUND", (0.075, 0.075, 0.075), 0.78))

# Camera.
bpy.ops.object.camera_add(location=(4.2, -4.6, 3.2))
cam = bpy.context.object
cam.name = "CAM_REBUILD_PREVIEW"
for col in list(cam.users_collection):
    col.objects.unlink(cam)
ref_col.objects.link(cam)
scene.camera = cam

def look_at(o, target):
    direction = Vector(target) - o.location
    o.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
look_at(cam, (0.15, 0.0, 0.38))
cam.data.lens = 58

# Lighting.
bpy.ops.object.light_add(type='AREA', location=(1.6, -1.8, 3.4))
key = bpy.context.object
key.data.energy = 900
key.data.shape = 'DISK'
key.data.size = 3.0
look_at(key, (0, 0, 0.4))
for col in list(key.users_collection):
    col.objects.unlink(key)
ref_col.objects.link(key)

bpy.ops.object.light_add(type='AREA', location=(-2.5, 1.4, 1.9))
fill = bpy.context.object
fill.data.energy = 450
fill.data.size = 2.5
look_at(fill, (0, 0, 0.35))
for col in list(fill.users_collection):
    col.objects.unlink(fill)
ref_col.objects.link(fill)

# Save and render.
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
bpy.ops.render.render(write_still=True)

# Manifest after actual Blender generation.
bbox_world = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
mins = [min(v[k] for v in bbox_world) for k in range(3)]
maxs = [max(v[k] for v in bbox_world) for k in range(3)]
manifest = {
    "schema_version": "1.0",
    "project_id": "PRJ-C04-QINGJIANG-SHISHU",
    "object_id": "C04_YUNSHUIYI_REBUILD_MASTER_v001",
    "role": "BLENDER_REBUILD_CANDIDATE",
    "blender_version": bpy.app.version_string,
    "dimension_authority": "DESIGN_ESTIMATE",
    "field_state": "FIELD_OPEN",
    "source_boundary": "Meshy/product imagery are SOURCE_REFERENCE only; this baseline does not claim engineering fidelity.",
    "objects": [o.name for o in master_col.all_objects],
    "primary_mesh_vertices": len(mesh.vertices),
    "primary_mesh_polygons": len(mesh.polygons),
    "modifier_stack": [m.name + ":" + m.type for m in obj.modifiers],
    "bbox_m": {"min": mins, "max": maxs},
    "outputs": {
        "blend": os.path.basename(BLEND_PATH),
        "preview": os.path.basename(PREVIEW_PATH)
    },
    "truth_boundary": [
        "REBUILD_CANDIDATE != ENGINEERING_MASTER",
        "REBUILD_CANDIDATE != DESIGN_KEEP",
        "FIELD_PASS = NONE"
    ]
}
with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("OLEANDER_C04_REBUILD_BLEND=" + BLEND_PATH)
print("OLEANDER_C04_REBUILD_PREVIEW=" + PREVIEW_PATH)
print("OLEANDER_C04_REBUILD_MANIFEST=" + MANIFEST_PATH)
