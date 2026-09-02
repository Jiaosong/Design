import bpy
import json
import math
import os
from mathutils import Vector

OUT_DIR = os.environ.get("C04_REBUILD_OUT", "/tmp/c04-yunshuiyi-rebuild")
os.makedirs(OUT_DIR, exist_ok=True)
BLEND_PATH = os.path.join(OUT_DIR, "C04_YUNSHUIYI_REBUILD_MASTER_v002.blend")
PREVIEW_PATH = os.path.join(OUT_DIR, "C04_YUNSHUIYI_REBUILD_MASTER_v002_preview.png")
MANIFEST_PATH = os.path.join(OUT_DIR, "C04_YUNSHUIYI_REBUILD_MASTER_v002_manifest.json")

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
scene.world.color = (0.035, 0.035, 0.035)

master_col = bpy.data.collections.new("C04_YUNSHUIYI_REBUILD_v002")
scene.collection.children.link(master_col)
geo_col = bpy.data.collections.new("GEO")
ref_col = bpy.data.collections.new("REFERENCE")
master_col.children.link(geo_col)
master_col.children.link(ref_col)

# DESIGN_ESTIMATE envelope only. No engineering/field authority.
L, W = 2.80, 0.92
NU, NV = 40, 16


def surface_point(u, v, offset=0.0):
    x = (u - 0.5) * L
    y = (v - 0.5) * W
    edge = abs(v - 0.5) * 2.0
    z = 0.18 + 0.22 * math.exp(-((u - 0.56) / 0.22) ** 2)
    z += 0.10 * math.sin(math.pi * u) ** 2
    z += 0.13 * edge ** 2
    z += 0.11 * math.exp(-((u - 0.63) / 0.16) ** 2) * (0.35 + 0.65 * edge)
    z -= 0.035 * math.exp(-((v - 0.5) / 0.24) ** 2) * math.sin(math.pi * u) ** 2
    return (x, y, z + offset)


def grid_mesh(name, u0, u1, un, v0, v1, vn, offset=0.0):
    verts, faces = [], []
    for i in range(un + 1):
        u = u0 + (u1 - u0) * i / un
        for j in range(vn + 1):
            v = v0 + (v1 - v0) * j / vn
            verts.append(surface_point(u, v, offset))
    row = vn + 1
    for i in range(un):
        for j in range(vn):
            a = i * row + j
            faces.append((a, a + 1, a + row + 1, a + row))
    mesh = bpy.data.meshes.new(name + "_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    geo_col.objects.link(obj)
    return obj


def make_mat(name, rgb, roughness, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return mat


shell = grid_mesh("C04_YUNSHUIYI_PRIMARY_SHELL", 0.0, 1.0, NU, 0.0, 1.0, NV)
shell.data.materials.append(make_mat("MAT_YUNSHUIYI_SHELL", (0.19, 0.22, 0.22), 0.42, 0.05))
shell["OLE_ID"] = "C04_YUNSHUIYI_REBUILD_MASTER_v002"
shell["PROJECT_ID"] = "PRJ-C04-QINGJIANG-SHISHU"
shell["OBJECT_ROLE"] = "BLENDER_REBUILD_CANDIDATE"
shell["DIMENSION_AUTHORITY"] = "DESIGN_ESTIMATE"
shell["FIELD_STATE"] = "FIELD_OPEN"
shell["SOURCE_ROLE"] = "SOURCE_REFERENCE_DERIVED_FORM_INTENT"
shell["ENGINEERING_CLAIM"] = False
shell["DESIGN_KEEP_CLAIM"] = False

solid = shell.modifiers.new("OLE_SOLIDIFY", 'SOLIDIFY')
solid.thickness = 0.045
solid.offset = -0.25
bevel = shell.modifiers.new("OLE_BEVEL", 'BEVEL')
bevel.width = 0.018
bevel.segments = 3
subd = shell.modifiers.new("OLE_SUBD", 'SUBSURF')
subd.levels = 2
subd.render_levels = 2

contact = grid_mesh("C04_YUNSHUIYI_CONTACT_ZONE", 0.38, 0.76, 16, 0.24, 0.76, 8, 0.012)
contact.data.materials.append(make_mat("MAT_YUNSHUIYI_CONTACT_ZONE", (0.33, 0.29, 0.23), 0.58))
contact["SEMANTIC_ROLE"] = "BODY_CONTACT_ZONE_DESIGN_ESTIMATE"
contact["MECHANICAL_PART_CLAIM"] = False
csolid = contact.modifiers.new("OLE_CONTACT_SOLIDIFY", 'SOLIDIFY')
csolid.thickness = 0.008
cbevel = contact.modifiers.new("OLE_CONTACT_BEVEL", 'BEVEL')
cbevel.width = 0.006
cbevel.segments = 2

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

# Preview ground/camera/lights remain presentation-only references.
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0))
ground = bpy.context.object
ground.name = "PREVIEW_GROUND"
for c in list(ground.users_collection):
    c.objects.unlink(ground)
ref_col.objects.link(ground)
ground.data.materials.append(make_mat("MAT_PREVIEW_GROUND", (0.075, 0.075, 0.075), 0.78))


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()

bpy.ops.object.camera_add(location=(4.2, -4.6, 3.2))
cam = bpy.context.object
cam.name = "CAM_REBUILD_PREVIEW"
for c in list(cam.users_collection):
    c.objects.unlink(cam)
ref_col.objects.link(cam)
cam.data.lens = 58
look_at(cam, (0.15, 0.0, 0.38))
scene.camera = cam

for name, loc, energy, size in (
    ("KEY", (1.6, -1.8, 3.4), 900, 3.0),
    ("FILL", (-2.5, 1.4, 1.9), 450, 2.5),
):
    bpy.ops.object.light_add(type='AREA', location=loc)
    light = bpy.context.object
    light.name = "LIGHT_" + name
    light.data.energy = energy
    light.data.shape = 'DISK'
    light.data.size = size
    look_at(light, (0, 0, 0.4))
    for c in list(light.users_collection):
        c.objects.unlink(light)
    ref_col.objects.link(light)

bpy.context.view_layer.objects.active = shell
shell.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
bpy.ops.render.render(write_still=True)

bbox_world = [shell.matrix_world @ Vector(corner) for corner in shell.bound_box]
mins = [min(v[k] for v in bbox_world) for k in range(3)]
maxs = [max(v[k] for v in bbox_world) for k in range(3)]
manifest = {
    "schema_version": "1.0",
    "project_id": "PRJ-C04-QINGJIANG-SHISHU",
    "object_id": "C04_YUNSHUIYI_REBUILD_MASTER_v002",
    "role": "BLENDER_REBUILD_CANDIDATE",
    "repair_from": "v001 failed on Blender 5.2 render-engine enum; v002 uses BLENDER_EEVEE and is retested with --python-exit-code.",
    "blender_version": bpy.app.version_string,
    "dimension_authority": "DESIGN_ESTIMATE",
    "field_state": "FIELD_OPEN",
    "source_boundary": "Meshy/product imagery are SOURCE_REFERENCE only; no engineering fidelity claim.",
    "primary_mesh_vertices": len(shell.data.vertices),
    "primary_mesh_polygons": len(shell.data.polygons),
    "modifier_stack": [m.name + ":" + m.type for m in shell.modifiers],
    "bbox_m": {"min": mins, "max": maxs},
    "outputs": {"blend": os.path.basename(BLEND_PATH), "preview": os.path.basename(PREVIEW_PATH)},
    "truth_boundary": ["REBUILD_CANDIDATE != ENGINEERING_MASTER", "REBUILD_CANDIDATE != DESIGN_KEEP", "FIELD_PASS = NONE"]
}
with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("OLEANDER_C04_REBUILD_BLEND=" + BLEND_PATH)
print("OLEANDER_C04_REBUILD_PREVIEW=" + PREVIEW_PATH)
print("OLEANDER_C04_REBUILD_MANIFEST=" + MANIFEST_PATH)
