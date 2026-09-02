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
scene.cycles.samples = 32
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.filepath = PREVIEW
scene.render.image_settings.file_format = "PNG"
scene.world = bpy.data.worlds.new("C04_YUNSHUIYI_WORLD")
scene.world.color = (0.035, 0.04, 0.04)

root = bpy.data.collections.new("C04_YUNSHUIYI_REBUILD_v003")
geo = bpy.data.collections.new("GEO_EDITABLE")
contact_col = bpy.data.collections.new("BODY_CONTACT")
hardware_col = bpy.data.collections.new("HARDWARE")
ref = bpy.data.collections.new("REFERENCE")
scene.collection.children.link(root)
for col in (geo, contact_col, hardware_col, ref):
    root.children.link(col)


def move_to(obj, collection):
    for col in list(obj.users_collection):
        col.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def material(name, rgb, roughness, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return mat

MAT_METAL = material("MAT_YUNSHUIYI_DARK_METAL", (0.055, 0.065, 0.065), 0.34, 0.72)
MAT_WOOD = material("MAT_YUNSHUIYI_WOOD", (0.28, 0.105, 0.035), 0.48, 0.0)
MAT_CUSHION = material("MAT_YUNSHUIYI_CUSHION", (0.12, 0.14, 0.14), 0.72, 0.0)
MAT_BOLT = material("MAT_YUNSHUIYI_FASTENER", (0.16, 0.17, 0.16), 0.28, 0.78)
MAT_RAIL = material("MAT_REFERENCE_RAIL", (0.18, 0.19, 0.18), 0.42, 0.62)
MAT_GROUND = material("MAT_PREVIEW_GROUND", (0.075, 0.075, 0.075), 0.80)


def box(name, loc, dims, mat, collection=geo, bevel=0.008):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move_to(obj, collection)
    obj.data.materials.append(mat)
    if bevel > 0:
        mod = obj.modifiers.new("OLE_BEVEL", "BEVEL")
        mod.width = bevel
        mod.segments = 3
    return obj


def cyl(name, loc, radius, depth, mat, collection=hardware_col, rot=(math.pi/2, 0, 0), verts=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    move_to(obj, collection)
    obj.data.materials.append(mat)
    bev = obj.modifiers.new("OLE_BEVEL", "BEVEL")
    bev.width = min(radius * 0.18, 0.004)
    bev.segments = 2
    return obj


def beam_between(name, a, b, width, depth, mat, collection=hardware_col):
    a, b = Vector(a), Vector(b)
    mid = (a + b) * 0.5
    length = (b - a).length
    obj = box(name, mid, (width, depth, length), mat, collection, bevel=min(width, depth) * 0.12)
    obj.rotation_euler = (b - a).to_track_quat("Z", "Y").to_euler()
    return obj


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()

# SOURCE_REFERENCE proportions only. All metric values are DESIGN_ESTIMATE and FIELD_OPEN.
# Source-bound imagery shows: two dark vertical side rails, a five-slat timber back,
# a fold-down padded seat, visible pivot/fastener hardware and diagonal support arms.
FRAME_W = 0.86
BACK_H = 0.88
SEAT_W = 0.72
SEAT_D = 0.48
SEAT_Z = 0.56
UPRIGHT_Z = 1.02

# Primary bilateral frame; the first crossmember keeps the legacy validator object name.
primary = box("C04_YUNSHUIYI_PRIMARY_SHELL", (0, 0.09, 1.30), (FRAME_W, 0.055, 0.065), MAT_METAL, geo, 0.006)
primary["OLE_ID"] = "C04_YUNSHUIYI_REBUILD_MASTER_v003"
primary["PROJECT_ID"] = "PRJ-C04-QINGJIANG-SHISHU"
primary["OBJECT_ROLE"] = "BLENDER_NATIVE_EDITABLE_REBUILD_CHECKPOINT"
primary["DIMENSION_AUTHORITY"] = "DESIGN_ESTIMATE"
primary["FIELD_STATE"] = "FIELD_OPEN"
primary["SOURCE_AUTHORITY"] = "ODB-02_SOURCEBOUND_IMAGES"
primary["ENGINEERING_CLAIM"] = False
primary["DESIGN_KEEP_CLAIM"] = False
primary["DESIGN_INTENT"] = "short recovery interface: stop / lean-or-sit / look / continue"

for x, side in ((-FRAME_W/2, "L"), (FRAME_W/2, "R")):
    box(f"FRAME_UPRIGHT_{side}", (x, 0.09, UPRIGHT_Z), (0.055, 0.065, 1.34), MAT_METAL, geo, 0.007)
    box(f"BACK_EDGE_RAIL_{side}", (x * 0.82, -0.005, 1.08), (0.045, 0.055, BACK_H), MAT_METAL, geo, 0.006)

# Timber back/contact field: five independent horizontal slats, deliberately editable/separate.
slat_h = 0.135
slat_gap = 0.020
back_base = 0.76
for i in range(5):
    z = back_base + i * (slat_h + slat_gap)
    slat = box(f"BACK_Slat_{i+1:02d}", (0, -0.045, z), (0.70, 0.045, slat_h), MAT_WOOD, contact_col, 0.008)
    slat["SEMANTIC_ROLE"] = "BACK_LEAN_CONTACT_SOURCE_REFERENCE"
    slat["DIMENSION_AUTHORITY"] = "DESIGN_ESTIMATE"

# Fold-down seat: rigid pan + distinct upholstered body-contact zone.
seat_pan = box("SEAT_PAN_EDITABLE", (0, -0.245, SEAT_Z), (SEAT_W, SEAT_D, 0.055), MAT_METAL, geo, 0.014)
seat_pan["SEMANTIC_ROLE"] = "FOLD_DOWN_SEAT_SUPPORT"
contact = box("C04_YUNSHUIYI_CONTACT_ZONE", (0, -0.257, SEAT_Z + 0.047), (SEAT_W * 0.94, SEAT_D * 0.91, 0.055), MAT_CUSHION, contact_col, 0.030)
contact["SEMANTIC_ROLE"] = "BODY_CONTACT_ZONE_DESIGN_ESTIMATE"
contact["CONTACT_TYPE"] = "SHORT_RECOVERY_SIT_OR_PERCH"
contact["MECHANICAL_PART_CLAIM"] = False

# Pivot block + paired hinge pins.
for x, side in ((-0.33, "L"), (0.33, "R")):
    box(f"HINGE_BLOCK_{side}", (x, 0.015, SEAT_Z + 0.015), (0.105, 0.105, 0.13), MAT_METAL, hardware_col, 0.008)
    cyl(f"HINGE_PIN_{side}", (x, -0.045, SEAT_Z + 0.02), 0.025, 0.14, MAT_BOLT, hardware_col)
    beam_between(f"DIAGONAL_SUPPORT_{side}", (x, -0.41, SEAT_Z - 0.02), (x, 0.075, 0.28), 0.045, 0.030, MAT_METAL, hardware_col)

# Source-visible fasteners on back slats / frame. Position is diagrammatic, not engineering-authoritative.
for x in (-0.30, 0.30):
    for z in (0.82, 1.13, 1.44):
        cyl(f"FASTENER_{'L' if x < 0 else 'R'}_{z:.2f}", (x, -0.075, z), 0.018, 0.025, MAT_BOLT, hardware_col, rot=(math.pi/2, 0, 0), verts=24)

# Mount / clamp cues retained as separate objects because they carry the source attachment relation.
for x, side in ((-FRAME_W/2, "L"), (FRAME_W/2, "R")):
    box(f"MOUNT_CLAMP_{side}", (x, 0.18, 1.25), (0.11, 0.16, 0.12), MAT_METAL, hardware_col, 0.008)
    cyl(f"MOUNT_BOLT_{side}", (x, 0.265, 1.25), 0.022, 0.19, MAT_BOLT, hardware_col)

# Reference railing only: scene context / mounting read, not part of Yunshuiyi master geometry claim.
box("REFERENCE_RAIL_TOP", (0, 0.29, 1.34), (2.3, 0.12, 0.12), MAT_RAIL, ref, 0.020)
for x in (-0.82, 0.82):
    box(f"REFERENCE_RAIL_POST_{x:+.2f}", (x, 0.29, 0.76), (0.09, 0.09, 1.10), MAT_RAIL, ref, 0.010)

# Body-scale readback proxy, intentionally generic and hidden from engineering claims.
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.11, location=(0, -0.78, 1.67))
head = move_to(bpy.context.object, ref); head.name = "REFERENCE_BODY_HEAD"; head.data.materials.append(material("MAT_BODY_REF", (0.32,0.30,0.27),0.65))
beam_between("REFERENCE_BODY_TORSO", (0,-0.72,1.53), (0,-0.47,0.88), 0.22, 0.16, bpy.data.materials["MAT_BODY_REF"], ref)

curve = bpy.data.curves.new("C04_YUNSHUIYI_DATUM_CURVE", "CURVE")
curve.dimensions = "3D"; curve.bevel_depth = 0.003
sp = curve.splines.new("POLY"); sp.points.add(2)
for i, co in enumerate(((-FRAME_W/2,0,SEAT_Z),(0,0,SEAT_Z),(FRAME_W/2,0,SEAT_Z))):
    sp.points[i].co = (*co, 1)
datum = bpy.data.objects.new("DATUM_LONGITUDINAL_CENTER", curve); ref.objects.link(datum); datum.hide_render = True

# Preview ground.
gm = bpy.data.meshes.new("PREVIEW_GROUND_MESH")
gm.from_pydata([(-3,-3,0),(3,-3,0),(3,3,0),(-3,3,0)], [], [(0,1,2,3)]); gm.update()
ground = bpy.data.objects.new("PREVIEW_GROUND", gm); ref.objects.link(ground); ground.data.materials.append(MAT_GROUND)

cd = bpy.data.cameras.new("CAM_REBUILD_PREVIEW_DATA")
cam = bpy.data.objects.new("CAM_REBUILD_PREVIEW", cd); ref.objects.link(cam)
cam.location = (2.15, -3.15, 2.05); cam.data.lens = 56; aim(cam, (0, -0.02, 0.93)); scene.camera = cam
for name, loc, power, size in (("KEY",(-1.8,-2.2,3.4),850,2.5),("FILL",(2.4,-0.8,2.2),480,2.0),("RIM",(0,1.8,2.7),620,1.8)):
    ld = bpy.data.lights.new("LIGHT_"+name+"_DATA", "AREA"); ld.energy = power; ld.shape = "DISK"; ld.size = size
    lo = bpy.data.objects.new("LIGHT_"+name, ld); ref.objects.link(lo); lo.location = loc; aim(lo, (0,0,0.95))

# DESIGN INTENT metadata on all editable object families.
for obj in list(geo.objects) + list(contact_col.objects) + list(hardware_col.objects):
    obj["PROJECT_ID"] = "PRJ-C04-QINGJIANG-SHISHU"
    obj["OBJECT_ID"] = "C04_YUNSHUIYI"
    obj["DIMENSION_AUTHORITY"] = "DESIGN_ESTIMATE"
    obj["FIELD_STATE"] = "FIELD_OPEN"
    obj["SOURCE_ROLE"] = "SOURCE_REFERENCE_REBUILD"

bpy.ops.wm.save_as_mainfile(filepath=BLEND)
bpy.ops.render.render(write_still=True)

all_model_objects = list(geo.objects) + list(contact_col.objects) + list(hardware_col.objects)
manifest = {
    "schema_version": "1.1",
    "project_id": "PRJ-C04-QINGJIANG-SHISHU",
    "object_id": "C04_YUNSHUIYI_REBUILD_MASTER_v003",
    "role": "BLENDER_REBUILD_CHECKPOINT",
    "blender_version": bpy.app.version_string,
    "render_carrier": "CYCLES_CPU_HEADLESS",
    "dimension_authority": "DESIGN_ESTIMATE",
    "field_state": "FIELD_OPEN",
    "source_boundary": "ODB-02 source-bound imagery is visual authority. Metric values remain DESIGN_ESTIMATE; no engineering claim.",
    "source_read": ["bilateral dark metal side rails", "five timber back slats", "fold-down padded seat", "paired hinge/pivot hardware", "diagonal support arms", "railing mount/clamp relation"],
    "collections": ["GEO_EDITABLE", "BODY_CONTACT", "HARDWARE", "REFERENCE"],
    "editable_object_count": len(all_model_objects),
    "primary_vertices": len(primary.data.vertices),
    "primary_polygons": len(primary.data.polygons),
    "modifier_stack": [m.name+":"+m.type for m in primary.modifiers],
    "body_contact_objects": [o.name for o in contact_col.objects],
    "outputs": {"blend": os.path.basename(BLEND), "preview": os.path.basename(PREVIEW)},
    "truth_boundary": ["REBUILD_CHECKPOINT != ENGINEERING_MASTER", "REBUILD_CHECKPOINT != DESIGN_KEEP", "FIELD_PASS = NONE"]
}
with open(MANIFEST, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print("OLEANDER_C04_REBUILD_BLEND="+BLEND)
print("OLEANDER_C04_REBUILD_PREVIEW="+PREVIEW)
print("OLEANDER_C04_REBUILD_MANIFEST="+MANIFEST)
