import bpy, json, os, math
from mathutils import Vector
OUT=os.environ.get('OLEANDER_JOB_OUTPUT_DIR') or '/tmp/c04-yunshuiyi-rebuild'; os.makedirs(OUT,exist_ok=True)
BLEND=os.path.join(OUT,'C04_YUNSHUIYI_REBUILD_MASTER_v003.blend'); PREVIEW=os.path.join(OUT,'C04_YUNSHUIYI_REBUILD_MASTER_v003_preview.png'); MANIFEST=os.path.join(OUT,'C04_YUNSHUIYI_REBUILD_MASTER_v003_manifest.json')
bpy.ops.wm.read_factory_settings(use_empty=True); s=bpy.context.scene; s.unit_settings.system='METRIC'; s.render.engine='BLENDER_EEVEE'; s.render.resolution_x=960; s.render.resolution_y=540; s.render.resolution_percentage=100; s.render.filepath=PREVIEW; s.world.color=(.055,.06,.06)
root=bpy.data.collections.new('C04_YUNSHUIYI_REBUILD_v003'); geo=bpy.data.collections.new('GEO_EDITABLE'); contact=bpy.data.collections.new('BODY_CONTACT'); hardware=bpy.data.collections.new('HARDWARE'); ref=bpy.data.collections.new('REFERENCE'); s.collection.children.link(root)
for c in (geo,contact,hardware,ref): root.children.link(c)
def mat(n,c,metal=0,rough=.45):
 m=bpy.data.materials.new(n); m.diffuse_color=(*c,1); m.metallic=metal; m.roughness=rough; return m
steel=mat('MAT_DARK_FRAME',(.08,.09,.085),.7,.32); wood=mat('MAT_WOOD_SLATS',(.38,.22,.11),0,.48); pad=mat('MAT_CONTACT_PAD',(.25,.27,.24),0,.62); hw=mat('MAT_HARDWARE',(.12,.13,.12),.8,.26)
def cube(n,loc,scale,ma,coll=geo,rot=(0,0,0)):
 bpy.ops.mesh.primitive_cube_add(location=loc,rotation=rot); o=bpy.context.object; o.name=n; o.scale=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(ma); coll.objects.link(o); bpy.context.collection.objects.unlink(o); b=o.modifiers.new('OLE_BEVEL','BEVEL'); b.width=.018; b.segments=3; return o
def cyl(n,loc,r,depth,ma,coll=hardware,rot=(math.pi/2,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=depth,location=loc,rotation=rot); o=bpy.context.object; o.name=n; o.data.materials.append(ma); coll.objects.link(o); bpy.context.collection.objects.unlink(o); return o
def beam(n,a,b,r=.035,ma=steel,coll=hardware):
 a,b=Vector(a),Vector(b); d=b-a; mid=(a+b)/2; o=cyl(n,mid,r,d.length,ma,coll,(0,0,0)); o.rotation_euler=d.to_track_quat('Z','Y').to_euler(); return o
# DESIGN_ESTIMATE proportions only; ODB-02 imagery remains visual authority.
# Bilateral side architecture.
for side,y in [('L',-.62),('R',.62)]:
 cube('FRAME_'+side+'_REAR',(-.66,y,.86),(.045,.045,.72),steel)
 cube('FRAME_'+side+'_FRONT',(.58,y,.55),(.045,.045,.48),steel)
 beam('FRAME_'+side+'_TOP',(-.66,y,1.55),(.42,y,1.46),.042,steel,geo)
 beam('FRAME_'+side+'_LOWER',(-.62,y,.25),(.58,y,.16),.042,steel,geo)
 # source-defining diagonal support arm, deliberately exposed in preview
 beam('DIAGONAL_SUPPORT_ARM_'+side,(-.50,y,.35),(.42,y,.92),.038,hw,hardware)
 cyl('HINGE_PIVOT_'+side,(.42,y,.92),.065,.13,hw,hardware)
 cube('RAILING_MOUNT_CLAMP_'+side,(-.73,y,1.23),(.11,.075,.15),hw,hardware)
# five independent back slats
for i,z in enumerate([.72,.90,1.08,1.26,1.44],1): cube('BACK_SLAT_%02d'%i,(-.12,0,z),(.72,.055,.055),wood,geo)
# fold-down seat and separately addressable contact zone
seat=cube('FOLD_DOWN_SEAT',(.12,0,.62),(.70,.48,.045),wood,geo,rot=(0,.10,0)); seat['OLE_ID']='C04_YUNSHUIYI_REBUILD_MASTER_v003'; seat['DIMENSION_AUTHORITY']='DESIGN_ESTIMATE'; seat['FIELD_STATE']='FIELD_OPEN'; seat['DESIGN_KEEP_CLAIM']=False
cp=cube('BODY_CONTACT_ZONE',(.12,0,.685),(.58,.40,.022),pad,contact,rot=(0,.10,0)); cp['SEMANTIC_ROLE']='SHORT_RECOVERY_LEAN_SIT_CONTACT'
# railing context remains reference, not design geometry
for y in (-.82,.82): beam('REFERENCE_RAIL_'+('L' if y<0 else 'R'),(-1.0,y,.25),(-1.0,y,1.65),.025,hw,ref)
# camera/light
def aim(o,t): o.rotation_euler=(Vector(t)-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(3.3,-4.2,2.65)); cam=bpy.context.object; cam.name='CAM_FIDELITY_PREVIEW'; aim(cam,(0,0,.85)); s.camera=cam
for n,loc,pow,size in [('KEY',(2,-2,4),1100,4),('FILL',(-3,1.5,2.5),650,3)]:
 ld=bpy.data.lights.new('LIGHT_'+n,'AREA'); ld.energy=pow; ld.shape='DISK'; ld.size=size; o=bpy.data.objects.new('LIGHT_'+n,ld); s.collection.objects.link(o); o.location=loc; aim(o,(0,0,.8))
bpy.ops.wm.save_as_mainfile(filepath=BLEND); bpy.ops.render.render(write_still=True)
required=['FOLD_DOWN_SEAT','BODY_CONTACT_ZONE','BACK_SLAT_01','BACK_SLAT_05','DIAGONAL_SUPPORT_ARM_L','DIAGONAL_SUPPORT_ARM_R','HINGE_PIVOT_L','HINGE_PIVOT_R','RAILING_MOUNT_CLAMP_L','RAILING_MOUNT_CLAMP_R']
manifest={'schema_version':'1.1','project_id':'PRJ-C04-QINGJIANG-SHISHU','object_id':'C04_YUNSHUIYI_REBUILD_MASTER_v003','revision':'FIDELITY_REPAIR_R04','dimension_authority':'DESIGN_ESTIMATE','field_state':'FIELD_OPEN','source_authority':'ODB-02 source-bound imagery + Design Fidelity Brief R01','repair_focus':['source-defining diagonal support arm','paired hinge/pivot hardware','railing mount/clamp relation','bilateral side-support architecture'],'required_objects':required,'truth_boundary':['NOT_ENGINEERING_MASTER','NOT_DESIGN_KEEP','FIELD_PASS_NONE']}
with open(MANIFEST,'w',encoding='utf-8') as f: json.dump(manifest,f,ensure_ascii=False,indent=2)
print('OLEANDER_C04_REBUILD_BLEND='+BLEND); print('OLEANDER_C04_REBUILD_PREVIEW='+PREVIEW); print('OLEANDER_C04_REBUILD_MANIFEST='+MANIFEST)