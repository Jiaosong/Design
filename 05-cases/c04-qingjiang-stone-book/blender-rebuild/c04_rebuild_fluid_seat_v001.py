import bpy
import json
import math
import os
from mathutils import Vector

OUT = os.environ.get("OLEANDER_JOB_OUTPUT_DIR") or os.environ.get("C04_REBUILD_OUT", "/tmp/c04-fluid-seat-rebuild")
os.makedirs(OUT, exist_ok=True)
BLEND = os.path.join(OUT, "C04_FLUID_SEAT_REBUILD_MASTER_v001.blend")
PREVIEW = os.path.join(OUT, "C04_FLUID_SEAT_REBUILD_MASTER_v001_preview.png")
MANIFEST = os.path.join(OUT, "C04_FLUID_SEAT_REBUILD_MASTER_v001_manifest.json")

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 1.0
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 24
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.filepath = PREVIEW
scene.render.image_settings.file_format = "PNG"
scene.world = bpy.data.worlds.new("C04_FLUID_SEAT_WORLD")
scene.world.color = (0.035, 0.04, 0.04)

root = bpy.data.collections.new("C04_FLUID_SEAT_REBUILD_v001")
geo = bpy.data.collections.new("GEO_EDITABLE")
contact_col = bpy.data.collections.new("BODY_CONTACT")
ref = bpy.data.collections.new("REFERENCE")
scene.collection.children.link(root)
root.children.link(geo)
root.children.link(contact_col)
root.children.link(ref)

# SOURCE/GEOMETRY AUTHORITY BOUNDARY
# No verified dimensions are available in the Current machine job. Values below are DESIGN_ESTIMATE
# proportions used to create an editable Blender-native ergonomic study only. FIELD/ENGINEERING remain OPEN.
SEAT_W = 0.64
SEAT_D = 0.56
SEAT_H = 0.46
BACK_H = 0.62
NU = 28
NV = 18


def mat(name, rgb, rough=0.5, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*rgb, 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    return m


def seat_point(u, v, zoff=0.0):
    # u: left-right, v: front-back. Central basin + raised perimeter + soft front roll-off.
    x = (u - 0.5) * SEAT_W
    y = (v - 0.5) * SEAT_D
    cx = (u - 0.5) / 0.5
    cy = (v - 0.52) / 0.5
    edge = max(abs(cx), abs(cy))
    basin = -0.030 * math.exp(-((cx / 0.72) ** 2 + (cy / 0.66) ** 2))
    side_support = 0.030 * (abs(cx) ** 2.2)
    rear_support = 0.032 * max(cy, 0.0) ** 2
    front_relief = -0.018 * math.exp(-((v - 0.05) / 0.13) ** 2)
    z = SEAT_H + basin + side_support + rear_support + front_relief + zoff
    return (x, y, z)


def make_grid(name, point_fn, un, vn, collection):
    verts = [point_fn(i / un, j / vn) for i in range(un + 1) for j in range(vn + 1)]
    row = vn + 1
    faces = []
    for i in range(un):
        for j in range(vn):
            a = i * row + j
            faces.append((a, a + row, a + row + 1, a + 1))
    mesh = bpy.data.meshes.new(name + "_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    return obj


seat = make_grid("C04_FLUID_SEAT_PRIMARY_SEAT", seat_point, NU, NV, geo)
seat.data.materials.append(mat("MAT_FLUID_SEAT_SHELL", (0.18, 0.21, 0.20), 0.38, 0.03))
seat["OLE_ID"] = "C04_FLUID_SEAT_REBUILD_MASTER_v001"
seat["PROJECT_ID"] = "PRJ-C04-QINGJIANG-SHISHU"
seat["CHILD_ITEM"] = "流体座椅人体工"
seat["OBJECT_ROLE"] = "BLENDER_REBUILD_CANDIDATE"
seat["DIMENSION_AUTHORITY"] = "DESIGN_ESTIMATE"
seat["FIELD_STATE"] = "FIELD_OPEN"
seat["ENGINEERING_CLAIM"] = False
seat["DESIGN_KEEP_CLAIM"] = False
seat["DESIGN_INTENT"] = "continuous seated-contact basin with lateral guidance and front pressure relief"
sol = seat.modifiers.new("OLE_SEAT_SOLIDIFY", "SOLIDIFY"); sol.thickness = 0.035; sol.offset = -0.45
bev = seat.modifiers.new("OLE_SEAT_BEVEL", "BEVEL"); bev.width = 0.012; bev.segments = 3
sub = seat.modifiers.new("OLE_SEAT_SUBD", "SUBSURF"); sub.levels = 2; sub.render_levels = 2

# Backrest: a continuous ruled surface, progressively cupped toward lumbar height.
def back_point(u, v):
    x = (u - 0.5) * (SEAT_W * (0.90 + 0.08 * v))
    z = SEAT_H + 0.08 + v * BACK_H
    lumbar = 0.055 * math.exp(-((v - 0.38) / 0.23) ** 2)
    shoulder_release = -0.018 * math.exp(-((v - 0.88) / 0.18) ** 2)
    lateral_cup = 0.040 * (abs((u - 0.5) / 0.5) ** 1.8) * (0.55 + 0.45 * v)
    y = SEAT_D * 0.39 + lumbar + shoulder_release - lateral_cup
    return (x, y, z)

back = make_grid("C04_FLUID_SEAT_BACKREST", back_point, 26, 22, geo)
back.data.materials.append(mat("MAT_FLUID_BACK", (0.16, 0.19, 0.18), 0.42, 0.02))
back["SEMANTIC_ROLE"] = "BACK_SUPPORT_CONTINUITY_DESIGN_ESTIMATE"
bs = back.modifiers.new("OLE_BACK_SOLIDIFY", "SOLIDIFY"); bs.thickness = 0.030; bs.offset = -0.5
bb = back.modifiers.new("OLE_BACK_BEVEL", "BEVEL"); bb.width = 0.010; bb.segments = 3
bsub = back.modifiers.new("OLE_BACK_SUBD", "SUBSURF"); bsub.levels = 2; bsub.render_levels = 2

# Explicit contact-zone overlays remain independently addressable for later validation overlays.
contact = make_grid("C04_FLUID_SEAT_CONTACT_ZONE", lambda u, v: seat_point(0.18 + 0.64*u, 0.16 + 0.66*v, 0.010), 14, 10, contact_col)
contact.data.materials.append(mat("MAT_FLUID_CONTACT", (0.34, 0.30, 0.23), 0.62))
contact["SEMANTIC_ROLE"] = "SEATED_BODY_CONTACT_ZONE_DESIGN_ESTIMATE"
contact["MECHANICAL_PART_CLAIM"] = False
cs = contact.modifiers.new("OLE_CONTACT_SOLIDIFY", "SOLIDIFY"); cs.thickness = 0.006

lumbar = make_grid("C04_FLUID_SEAT_LUMBAR_ZONE", lambda u, v: back_point(0.22 + 0.56*u, 0.18 + 0.44*v), 12, 8, contact_col)
lumbar.data.materials.append(mat("MAT_FLUID_LUMBAR", (0.30, 0.26, 0.20), 0.62))
lumbar["SEMANTIC_ROLE"] = "LUMBAR_CONTACT_ZONE_DESIGN_ESTIMATE"
ls = lumbar.modifiers.new("OLE_LUMBAR_SOLIDIFY", "SOLIDIFY"); ls.thickness = 0.006

# Central pedestal is a visual support proxy only, intentionally separate from engineering authority.
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.12, depth=SEAT_H - 0.06, location=(0, 0.04, (SEAT_H - 0.06)/2))
ped = bpy.context.object
for c in list(ped.users_collection): c.objects.unlink(ped)
geo.objects.link(ped)
ped.name = "C04_FLUID_SEAT_SUPPORT_PROXY"
ped.data.materials.append(mat("MAT_FLUID_SUPPORT", (0.08, 0.09, 0.09), 0.34, 0.65))
ped["SEMANTIC_ROLE"] = "SUPPORT_PROXY_NOT_ENGINEERING_STRUCTURE"
ped["DIMENSION_AUTHORITY"] = "DESIGN_ESTIMATE"

# Reference seated-body proxy for posture/contact readback only.
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=(0, -0.02, SEAT_H + 0.48), scale=(0.18, 0.13, 0.28))
torso = bpy.context.object
for c in list(torso.users_collection): c.objects.unlink(torso)
ref.objects.link(torso)
torso.name = "REFERENCE_TORSO_PROXY"
torso.data.materials.append(mat("MAT_REFERENCE_BODY", (0.42, 0.42, 0.40), 0.75))
torso.display_type = "WIRE"
torso.hide_render = True

# Ground plane / lighting / camera.
gm = bpy.data.meshes.new("PREVIEW_GROUND_MESH")
gm.from_pydata([(-3,-3,0),(3,-3,0),(3,3,0),(-3,3,0)], [], [(0,1,2,3)])
gm.update()
ground = bpy.data.objects.new("PREVIEW_GROUND", gm); ref.objects.link(ground)
ground.data.materials.append(mat("MAT_PREVIEW_GROUND", (0.065,0.07,0.068), 0.82))


def aim(obj, target):
    obj.rotation_euler = (Vector(target)-obj.location).to_track_quat("-Z", "Y").to_euler()

cd = bpy.data.cameras.new("CAM_FLUID_SEAT_PREVIEW_DATA")
cam = bpy.data.objects.new("CAM_FLUID_SEAT_PREVIEW", cd); ref.objects.link(cam)
cam.location = (1.65, -2.05, 1.48); cam.data.lens = 58; aim(cam, (0,0.10,0.64)); scene.camera = cam
for name, loc, energy, size in (("KEY",(1.7,-1.5,2.4),850,2.4),("FILL",(-1.6,0.8,1.5),420,2.0),("RIM",(0.2,1.5,2.0),520,1.8)):
    ld = bpy.data.lights.new("LIGHT_"+name+"_DATA", "AREA"); ld.energy=energy; ld.shape="DISK"; ld.size=size
    lo = bpy.data.objects.new("LIGHT_"+name, ld); ref.objects.link(lo); lo.location=loc; aim(lo,(0,0.08,0.62))

bpy.ops.wm.save_as_mainfile(filepath=BLEND)
bpy.ops.render.render(write_still=True)

manifest = {
  "schema_version":"1.0",
  "project_id":"PRJ-C04-QINGJIANG-SHISHU",
  "child_item":"流体座椅人体工",
  "object_id":"C04_FLUID_SEAT_REBUILD_MASTER_v001",
  "role":"BLENDER_REBUILD_CANDIDATE",
  "blender_version":bpy.app.version_string,
  "render_carrier":"CYCLES_CPU_HEADLESS",
  "dimension_authority":"DESIGN_ESTIMATE",
  "field_state":"FIELD_OPEN",
  "source_boundary":"Current machine-job exposes no verified dimensions; rebuild is a Blender-native ergonomic design estimate, not a decimated source or engineering master.",
  "design_intent":["continuous seat-basin silhouette","lateral seated guidance","front pressure relief","lumbar support continuity","separable body-contact zones"],
  "editable_objects":[seat.name, back.name, contact.name, lumbar.name, ped.name],
  "modifier_stacks":{
    seat.name:[m.name+":"+m.type for m in seat.modifiers],
    back.name:[m.name+":"+m.type for m in back.modifiers],
    contact.name:[m.name+":"+m.type for m in contact.modifiers]
  },
  "outputs":{"blend":os.path.basename(BLEND),"preview":os.path.basename(PREVIEW)},
  "truth_boundary":["REBUILD_CANDIDATE != ENGINEERING_MASTER","REBUILD_CANDIDATE != FINAL_DESIGN_KEEP","HUMAN_FACTORS_DIMENSIONS = DESIGN_ESTIMATE","FIELD_PASS = NONE"]
}
with open(MANIFEST,"w",encoding="utf-8") as f: json.dump(manifest,f,ensure_ascii=False,indent=2)
print("OLEANDER_C04_REBUILD_BLEND="+BLEND)
print("OLEANDER_C04_REBUILD_PREVIEW="+PREVIEW)
print("OLEANDER_C04_REBUILD_MANIFEST="+MANIFEST)
