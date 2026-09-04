import bpy
import json
import math
import os
from mathutils import Vector

OUT = os.environ.get("OLEANDER_JOB_OUTPUT_DIR") or os.environ.get("C04_REBUILD_OUT", "/tmp/c04-jiangpan-folding-observation")
os.makedirs(OUT, exist_ok=True)
BLEND = os.path.join(OUT, "C04_JIANGPAN_FOLDING_OBSERVATION_REBUILD_MASTER_v001.blend")
PREVIEW = os.path.join(OUT, "C04_JIANGPAN_FOLDING_OBSERVATION_REBUILD_MASTER_v001_preview.png")
MANIFEST = os.path.join(OUT, "C04_JIANGPAN_FOLDING_OBSERVATION_REBUILD_MASTER_v001_manifest.json")

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
scene.world = bpy.data.worlds.new("C04_JIANGPAN_WORLD")
scene.world.color = (0.028, 0.034, 0.035)

root = bpy.data.collections.new("C04_JIANGPAN_FOLDING_OBSERVATION_REBUILD_v001")
geo = bpy.data.collections.new("GEO_EDITABLE")
contact_col = bpy.data.collections.new("BODY_CONTACT")
feature_col = bpy.data.collections.new("FEATURE_STRUCTURE")
ref = bpy.data.collections.new("REFERENCE")
scene.collection.children.link(root)
for c in (geo, contact_col, feature_col, ref): root.children.link(c)

# SOURCE AUTHORITY BOUNDARY
# Current Queue legally leases this logical child, but no verified dimensions or source image geometry are
# available to this producer. All proportions below are DESIGN_ESTIMATE for a Blender-native folding-
# observation relation study only. FIELD / engineering / manufacturing remain OPEN.
W = 0.66
D = 0.50
H = 0.47
BACK_H = 0.50
FRAME_T = 0.035


def mat(name, rgb, rough=0.5, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*rgb, 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    return m

MAT_FRAME = mat("MAT_JIANGPAN_FRAME", (0.075, 0.085, 0.082), 0.30, 0.72)
MAT_CONTACT = mat("MAT_JIANGPAN_CONTACT", (0.28, 0.24, 0.18), 0.58, 0.02)
MAT_HINGE = mat("MAT_JIANGPAN_HINGE", (0.13, 0.14, 0.14), 0.25, 0.82)
MAT_REF = mat("MAT_JIANGPAN_REFERENCE", (0.30, 0.33, 0.32), 0.75, 0.0)


def move_to(obj, collection):
    for c in list(obj.users_collection): c.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def cube(name, loc, scale, material, collection=geo, bevel=0.012):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = move_to(bpy.context.object, collection)
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        b = o.modifiers.new("OLE_BEVEL", "BEVEL"); b.width = bevel; b.segments = 3
    o.data.materials.append(material)
    return o


def cyl(name, loc, radius, depth, rot, material, collection=feature_col):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=radius, depth=depth, location=loc, rotation=rot)
    o = move_to(bpy.context.object, collection); o.name = name; o.data.materials.append(material)
    b = o.modifiers.new("OLE_EDGE_SOFTEN", "BEVEL"); b.width = 0.004; b.segments = 2
    return o

# Primary side frames: paired folded profiles keep the object visually light and leave a clear observation aperture.
left = cube("C04_JIANGPAN_LEFT_FRAME", (-W/2, 0.02, H/2), (FRAME_T/2, D*0.46, H/2), MAT_FRAME)
right = cube("C04_JIANGPAN_RIGHT_FRAME", (W/2, 0.02, H/2), (FRAME_T/2, D*0.46, H/2), MAT_FRAME)
for o in (left, right):
    o["SEMANTIC_ROLE"] = "PAIRED_SIDE_FRAME_DESIGN_ESTIMATE"

# Folding seat/contact plane: deliberately independent and addressable for later fidelity / body-contact validation.
seat = cube("C04_JIANGPAN_FOLDING_SEAT", (0, -0.035, H), (W*0.46, D*0.38, 0.026), MAT_CONTACT, contact_col, 0.018)
seat["OLE_ID"] = "C04_JIANGPAN_FOLDING_OBSERVATION_REBUILD_MASTER_v001"
seat["PROJECT_ID"] = "PRJ-C04-QINGJIANG-SHISHU"
seat["CHILD_ITEM"] = "江畔停泊折叠观"
seat["OBJECT_ROLE"] = "BLENDER_REBUILD_CANDIDATE"
seat["DIMENSION_AUTHORITY"] = "DESIGN_ESTIMATE"
seat["FIELD_STATE"] = "FIELD_OPEN"
seat["ENGINEERING_CLAIM"] = False
seat["DESIGN_KEEP_CLAIM"] = False
seat["DESIGN_INTENT"] = "folding short-stop observation surface; body supported without turning landscape into product backdrop"

# Back/lean surface: open horizontal rails preserve visual permeability toward the landscape rather than a solid wall.
back_rails = []
for i in range(3):
    z = H + 0.14 + i * 0.13
    rail = cube(f"C04_JIANGPAN_BACK_RAIL_{i+1:02d}", (0, D*0.34, z), (W*0.44, 0.025, 0.032), MAT_CONTACT, contact_col, 0.014)
    rail["SEMANTIC_ROLE"] = "LEAN_BACK_CONTACT_DESIGN_ESTIMATE"
    back_rails.append(rail)

# Hinge axis and paired pivots make folding intent explicit but do not claim a buildable mechanism.
hinge_y = D*0.31
for side, x in (("L", -W*0.43), ("R", W*0.43)):
    p = cyl(f"C04_JIANGPAN_HINGE_PIN_{side}", (x, hinge_y, H+0.015), 0.034, 0.075, (0, math.radians(90), 0), MAT_HINGE)
    p["SEMANTIC_ROLE"] = "HINGE_AXIS_PROXY_NOT_ENGINEERING"

# Diagonal braces communicate deployed load path visually; engineering sizing remains explicitly open.
for side, x in (("L", -W*0.39), ("R", W*0.39)):
    start = Vector((x, D*0.30, H-0.03)); end = Vector((x, -D*0.31, 0.12))
    vec = end-start; mid = (start+end)/2
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.018, depth=vec.length, location=mid)
    brace = move_to(bpy.context.object, feature_col); brace.name=f"C04_JIANGPAN_DIAGONAL_BRACE_{side}"
    brace.rotation_euler = vec.to_track_quat("Z", "Y").to_euler(); brace.data.materials.append(MAT_FRAME)
    brace["SEMANTIC_ROLE"] = "DEPLOYED_BRACE_PROXY_NOT_ENGINEERING"

# Small front edge relief keeps the seat from reading as a deep lounge object; this is a short-stop observation relation.
front = cube("C04_JIANGPAN_FRONT_EDGE", (0, -D*0.40, H-0.015), (W*0.45, 0.022, 0.020), MAT_CONTACT, contact_col, 0.012)
front["SEMANTIC_ROLE"] = "SHORT_STOP_FRONT_EDGE_DESIGN_ESTIMATE"

# Human posture proxy: seated/half-perched torso, hidden from final render by default; retained for native readback.
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=(0, -0.03, H+0.52), scale=(0.17, 0.13, 0.27))
torso = move_to(bpy.context.object, ref); torso.name = "REFERENCE_BODY_PROXY"; torso.data.materials.append(MAT_REF); torso.display_type="WIRE"; torso.hide_render=True

# Landscape-view direction proxy stays reference-only; it establishes orientation without pretending to be Qingjiang geometry.
view = cube("REFERENCE_VIEW_DIRECTION", (0, 1.12, H+0.50), (0.008, 0.52, 0.008), MAT_REF, ref, 0.0)
view["SEMANTIC_ROLE"] = "REFERENCE_ONLY_LANDSCAPE_VIEW_AXIS"

# Ground, camera, lighting.
ground = cube("PREVIEW_GROUND", (0,0,-0.025), (2.6,2.6,0.025), mat("MAT_PREVIEW_GROUND", (0.055,0.062,0.061), 0.82), ref, 0.0)

def aim(obj, target): obj.rotation_euler = (Vector(target)-obj.location).to_track_quat("-Z", "Y").to_euler()
cd = bpy.data.cameras.new("CAM_JIANGPAN_PREVIEW_DATA")
cam = bpy.data.objects.new("CAM_JIANGPAN_PREVIEW", cd); ref.objects.link(cam)
cam.location=(1.55,-2.05,1.35); cam.data.lens=58; aim(cam,(0,0.06,0.62)); scene.camera=cam
for name, loc, energy, size in (("KEY",(1.6,-1.5,2.4),820,2.4),("FILL",(-1.5,0.6,1.5),380,2.0),("RIM",(0.2,1.5,2.0),500,1.8)):
    ld=bpy.data.lights.new("LIGHT_"+name+"_DATA","AREA"); ld.energy=energy; ld.shape="DISK"; ld.size=size
    lo=bpy.data.objects.new("LIGHT_"+name,ld); ref.objects.link(lo); lo.location=loc; aim(lo,(0,0.08,0.62))

bpy.ops.wm.save_as_mainfile(filepath=BLEND)
bpy.ops.render.render(write_still=True)

manifest = {
  "schema_version":"1.0",
  "project_id":"PRJ-C04-QINGJIANG-SHISHU",
  "child_item":"江畔停泊折叠观",
  "object_id":"C04_JIANGPAN_FOLDING_OBSERVATION_REBUILD_MASTER_v001",
  "role":"BLENDER_REBUILD_CANDIDATE",
  "blender_version":bpy.app.version_string,
  "render_carrier":"CYCLES_CPU_HEADLESS",
  "dimension_authority":"DESIGN_ESTIMATE",
  "field_state":"FIELD_OPEN",
  "source_boundary":"Current Queue authorizes the logical child but no verified dimensions/source geometry are available to this producer; geometry is an editable folding-observation relation study, not a decimated source or engineering master.",
  "design_intent":["short-stop observation rather than long lounge","paired side-frame silhouette","folding seat/contact surface","open lean-back rails preserve landscape permeability","explicit hinge/brace proxies without engineering claim","separable body-contact zones"],
  "editable_objects":[left.name,right.name,seat.name,*[o.name for o in back_rails],front.name],
  "feature_objects":["C04_JIANGPAN_HINGE_PIN_L","C04_JIANGPAN_HINGE_PIN_R","C04_JIANGPAN_DIAGONAL_BRACE_L","C04_JIANGPAN_DIAGONAL_BRACE_R"],
  "outputs":{"blend":os.path.basename(BLEND),"preview":os.path.basename(PREVIEW)},
  "truth_boundary":["REBUILD_CANDIDATE != ENGINEERING_MASTER","REBUILD_CANDIDATE != FINAL_DESIGN_KEEP","DIMENSIONS = DESIGN_ESTIMATE","HINGE/BRACE = VISUAL RELATION PROXY","FIELD_PASS = NONE"]
}
with open(MANIFEST,"w",encoding="utf-8") as f: json.dump(manifest,f,ensure_ascii=False,indent=2)
print("OLEANDER_C04_REBUILD_BLEND="+BLEND)
print("OLEANDER_C04_REBUILD_PREVIEW="+PREVIEW)
print("OLEANDER_C04_REBUILD_MANIFEST="+MANIFEST)
