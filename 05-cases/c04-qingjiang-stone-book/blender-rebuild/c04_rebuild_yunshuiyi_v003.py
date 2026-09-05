import bpy
import json
import math
import os
from mathutils import Vector

OUT = os.environ.get("OLEANDER_JOB_OUTPUT_DIR") or os.environ.get("C04_REBUILD_OUT", "/tmp/c04-yunshuiyi-rebuild")
os.makedirs(OUT, exist_ok=True)
BLEND = os.path.join(OUT, "C04_YUNSHUIYI_REBUILD_MASTER_v003.blend")
PREVIEW = os.path.join(OUT, "C04_YUNSHUIYI_REBUILD_MASTER_v003_preview.png")
MANIFEST = os.path.join(OUT, "C04_YUNSHUIYI_REBUILD_MASTER_v003_manifest.json")

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
scene.world = bpy.data.worlds.new("C04_YUNSHUIYI_WORLD")
scene.world.color = (0.04, 0.04, 0.04)

root = bpy.data.collections.new("C04_YUNSHUIYI_REBUILD_v003")
geo = bpy.data.collections.new("GEO")
ref = bpy.data.collections.new("REFERENCE")
scene.collection.children.link(root)
root.children.link(geo)
root.children.link(ref)

# DESIGN_ESTIMATE only. The reference assets remain the visual authority for later fidelity refinement.
L, W, NU, NV = 2.80, 0.92, 40, 16


def point(u, v, dz=0.0):
    x, y = (u - 0.5) * L, (v - 0.5) * W
    edge = abs(v - 0.5) * 2.0
    z = 0.18 + 0.22 * math.exp(-((u - 0.56) / 0.22) ** 2)
    z += 0.10 * math.sin(math.pi * u) ** 2 + 0.13 * edge ** 2
    z += 0.11 * math.exp(-((u - 0.63) / 0.16) ** 2) * (0.35 + 0.65 * edge)
    z -= 0.035 * math.exp(-((v - 0.5) / 0.24) ** 2) * math.sin(math.pi * u) ** 2
    return (x, y, z + dz)


def grid(name, u0, u1, un, v0, v1, vn, dz=0.0):
    vs = [point(u0 + (u1-u0)*i/un, v0 + (v1-v0)*j/vn, dz)
          for i in range(un+1) for j in range(vn+1)]
    row = vn + 1
    fs = []
    for i in range(un):
        for j in range(vn):
            a = i*row+j
            fs.append((a, a+1, a+row+1, a+row))
    mesh = bpy.data.meshes.new(name + "_MESH")
    mesh.from_pydata(vs, [], fs)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    geo.objects.link(obj)
    return obj


def material(name, rgb, roughness, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return mat


def aim(obj, target):
    obj.rotation_euler = (Vector(target)-obj.location).to_track_quat("-Z", "Y").to_euler()


shell = grid("C04_YUNSHUIYI_PRIMARY_SHELL", 0, 1, NU, 0, 1, NV)
shell.data.materials.append(material("MAT_YUNSHUIYI_SHELL", (0.19, 0.22, 0.22), 0.42, 0.05))
shell["OLE_ID"] = "C04_YUNSHUIYI_REBUILD_MASTER_v003"
shell["PROJECT_ID"] = "PRJ-C04-QINGJIANG-SHISHU"
shell["OBJECT_ROLE"] = "BLENDER_REBUILD_CANDIDATE"
shell["DIMENSION_AUTHORITY"] = "DESIGN_ESTIMATE"
shell["FIELD_STATE"] = "FIELD_OPEN"
shell["ENGINEERING_CLAIM"] = False
shell["DESIGN_KEEP_CLAIM"] = False

sol = shell.modifiers.new("OLE_SOLIDIFY", "SOLIDIFY"); sol.thickness = 0.045; sol.offset = -0.25
bev = shell.modifiers.new("OLE_BEVEL", "BEVEL"); bev.width = 0.018; bev.segments = 3
sub = shell.modifiers.new("OLE_SUBD", "SUBSURF"); sub.levels = 2; sub.render_levels = 2

contact = grid("C04_YUNSHUIYI_CONTACT_ZONE", .38, .76, 16, .24, .76, 8, .012)
contact.data.materials.append(material("MAT_YUNSHUIYI_CONTACT_ZONE", (.33, .29, .23), .58))
contact["SEMANTIC_ROLE"] = "BODY_CONTACT_ZONE_DESIGN_ESTIMATE"
contact["MECHANICAL_PART_CLAIM"] = False
cs = contact.modifiers.new("OLE_CONTACT_SOLIDIFY", "SOLIDIFY"); cs.thickness = .008
cb = contact.modifiers.new("OLE_CONTACT_BEVEL", "BEVEL"); cb.width = .006; cb.segments = 2

curve = bpy.data.curves.new("C04_YUNSHUIYI_DATUM_CURVE", "CURVE"); curve.dimensions = "3D"; curve.bevel_depth = .004
sp = curve.splines.new("POLY"); sp.points.add(2)
for i, co in enumerate(((-L/2,0,.05),(0,0,.05),(L/2,0,.05))): sp.points[i].co = (*co,1)
datum = bpy.data.objects.new("DATUM_LONGITUDINAL_CENTER", curve); ref.objects.link(datum); datum.hide_render = True

gm = bpy.data.meshes.new("PREVIEW_GROUND_MESH")
gm.from_pydata([(-4,-4,0),(4,-4,0),(4,4,0),(-4,4,0)], [], [(0,1,2,3)]); gm.update()
ground = bpy.data.objects.new("PREVIEW_GROUND", gm); ref.objects.link(ground)
ground.data.materials.append(material("MAT_PREVIEW_GROUND", (.075,.075,.075), .78))

cd = bpy.data.cameras.new("CAM_REBUILD_PREVIEW_DATA"); cam = bpy.data.objects.new("CAM_REBUILD_PREVIEW", cd); ref.objects.link(cam)
cam.location=(4.2,-4.6,3.2); cam.data.lens=58; aim(cam,(.15,0,.38)); scene.camera=cam
for name, loc, power, size in (("KEY",(1.6,-1.8,3.4),900,3.0),("FILL",(-2.5,1.4,1.9),450,2.5)):
    ld=bpy.data.lights.new("LIGHT_"+name+"_DATA","AREA"); ld.energy=power; ld.shape="DISK"; ld.size=size
    lo=bpy.data.objects.new("LIGHT_"+name,ld); ref.objects.link(lo); lo.location=loc; aim(lo,(0,0,.4))

bpy.ops.wm.save_as_mainfile(filepath=BLEND)
bpy.ops.render.render(write_still=True)

manifest = {
  "schema_version":"1.0",
  "project_id":"PRJ-C04-QINGJIANG-SHISHU",
  "object_id":"C04_YUNSHUIYI_REBUILD_MASTER_v003",
  "role":"BLENDER_REBUILD_CANDIDATE",
  "blender_version":bpy.app.version_string,
  "render_carrier":"CYCLES_CPU_HEADLESS",
  "dimension_authority":"DESIGN_ESTIMATE",
  "field_state":"FIELD_OPEN",
  "source_boundary":"Meshy/product imagery are SOURCE_REFERENCE; this baseline is not engineering fidelity.",
  "primary_vertices":len(shell.data.vertices),
  "primary_polygons":len(shell.data.polygons),
  "modifier_stack":[m.name+":"+m.type for m in shell.modifiers],
  "outputs":{"blend":os.path.basename(BLEND),"preview":os.path.basename(PREVIEW)},
  "truth_boundary":["REBUILD_CANDIDATE != ENGINEERING_MASTER","REBUILD_CANDIDATE != DESIGN_KEEP","FIELD_PASS = NONE"]
}
with open(MANIFEST,"w",encoding="utf-8") as f: json.dump(manifest,f,ensure_ascii=False,indent=2)
print("OLEANDER_C04_REBUILD_BLEND="+BLEND)
print("OLEANDER_C04_REBUILD_PREVIEW="+PREVIEW)
print("OLEANDER_C04_REBUILD_MANIFEST="+MANIFEST)
