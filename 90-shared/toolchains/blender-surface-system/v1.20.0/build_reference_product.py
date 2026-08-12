#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math, sys, traceback
from pathlib import Path
import bpy, bmesh
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

MODEL='OLEANDER_CMF_Reference_Product_v0.1'
LAB='2026-08-12｜IP03｜CMF Reference Product｜Product Geometry × Material Binding Validation'
MATS={'powder':'OL_MAT_PowderCoatFineMatte_v1','pp':'OL_MAT_PPFineMatte_v1','pu':'OL_MAT_PUSoftMatte_v1','al':'OL_MAT_BrushedAnodizedAl_v1','diffuser':'OL_MAT_MilkyDiffuser_v1'}
PRE={'powder':'PAR-SIM-POWDER-FINE-MATTE-001','pp':'PAR-SIM-PP-FINE-MATTE-001','pu':'PAR-SIM-PU-SOFT-MATTE-001','al':'PAR-SIM-AL-BRUSHED-ANODIZED-001','diffuser':'PAR-SIM-DIFFUSER-MILKY-001'}
RIGS={
 'BROAD':{'key':('DISK',16,.42,None,(-.34,-.52,.40)),'fill':('DISK',2.8,.24,None,(.30,-.24,.22))},
 'STRIP':{'key':('RECTANGLE',13,.026,.30,(-.24,-.34,.22)),'fill':('DISK',1.5,.18,None,(.28,-.22,.20))},
 'GRAZING':{'key':('RECTANGLE',18,.018,.28,(-.30,-.08,.13)),'fill':('DISK',.8,.14,None,(.26,-.20,.18))}}
VIEWS={
 'HERO':((.230,-.320,.180),(0,0,.046),68),
 'TOP':((.018,-.020,.420),(0,0,.040),65),
 'SIDE':((.380,-.010,.115),(0,0,.047),70),
 'CMF_MACRO':((.125,-.165,.100),(.028,-.012,.050),92)}
PLAN=[('HERO','BROAD'),('HERO','STRIP'),('HERO','GRAZING'),('TOP','BROAD'),('SIDE','STRIP'),('CMF_MACRO','GRAZING')]

def args():
 av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
 p=argparse.ArgumentParser(); p.add_argument('--out',required=True); p.add_argument('--samples',type=int,default=8); p.add_argument('--resolution',type=int,default=720); return p.parse_args(av)
def look(o,t): o.rotation_euler=(Vector(t)-o.location).to_track_quat('-Z','Y').to_euler()
def clear():
 bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
 for coll in (bpy.data.lights,bpy.data.cameras,bpy.data.curves):
  for x in list(coll):
   if x.users==0: coll.remove(x)
def reqmats():
 miss=[v for v in MATS.values() if bpy.data.materials.get(v) is None]
 if miss: raise RuntimeError('Missing v1.20 D2 materials: '+repr(miss))
 return {k:bpy.data.materials[v] for k,v in MATS.items()}
def bind(o,m,key,role):
 o.data.materials.clear(); o.data.materials.append(m); o['OLEANDER_MATERIAL_ROLE']=role; o['OLEANDER_D2_PARAMETER_PRESET']=PRE[key]; o['OLEANDER_BINDING_STATE']='D2_BOUND_TO_REFERENCE_GEOMETRY'; o['OLEANDER_MODEL']=MODEL; o['OLEANDER_AUTHORITY_STATE']='WORKING_SOURCE'; o['OLEANDER_SCOPE']='DESIGN VALIDATION / NOT ENGINEERING'
def rounded(name,dims,loc,bev,m,key,role):
 bpy.ops.mesh.primitive_cube_add(location=loc); o=bpy.context.object; o.name=name; o.dimensions=dims; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 md=o.modifiers.new('OL_Bevel','BEVEL'); md.width=bev; md.segments=8; md.limit_method='ANGLE'; bpy.context.view_layer.objects.active=o; bpy.ops.object.modifier_apply(modifier=md.name)
 for p in o.data.polygons: p.use_smooth=True
 bind(o,m,key,role); return o
def cyl(name,r,d,loc,m,key,role,verts=96):
 bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=d,location=loc); o=bpy.context.object; o.name=name
 md=o.modifiers.new('OL_Bevel','BEVEL'); md.width=min(.0015,d*.18); md.segments=6; bpy.context.view_layer.objects.active=o; bpy.ops.object.modifier_apply(modifier=md.name)
 for p in o.data.polygons:p.use_smooth=True
 try:
  bpy.context.view_layer.objects.active=o; o.select_set(True); bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.uv.smart_project(angle_limit=math.radians(66)); bpy.ops.object.mode_set(mode='OBJECT')
 except Exception:
  try:bpy.ops.object.mode_set(mode='OBJECT')
  except Exception:pass
 bind(o,m,key,role); return o
def utube(m):
 c=bpy.data.curves.new('OL_REF_CoatedTubeCurve','CURVE'); c.dimensions='3D'; c.resolution_u=20; c.bevel_depth=.004; c.bevel_resolution=6; c.use_fill_caps=True
 s=c.splines.new('BEZIER'); s.bezier_points.add(3)
 for bp,co in zip(s.bezier_points,[(-.054,.034,.031),(-.054,.034,.095),(.054,.034,.095),(.054,.034,.031)]): bp.co=co; bp.handle_left_type='AUTO'; bp.handle_right_type='AUTO'
 o=bpy.data.objects.new('OL_REF_PowderCoated_U_Frame',c); bpy.context.collection.objects.link(o); c.materials.append(m); o['OLEANDER_MATERIAL_ROLE']='powder-coated structural frame'; o['OLEANDER_D2_PARAMETER_PRESET']=PRE['powder']; o['OLEANDER_BINDING_STATE']='D2_BOUND_TO_REFERENCE_GEOMETRY'; o['OLEANDER_MODEL']=MODEL; o['OLEANDER_AUTHORITY_STATE']='WORKING_SOURCE'; o['OLEANDER_SCOPE']='DESIGN VALIDATION / NOT ENGINEERING'; return o
def ground():
 bpy.ops.mesh.primitive_plane_add(size=1.6,location=(0,0,0)); o=bpy.context.object; o.name='OL_REF_StudioGround'; m=bpy.data.materials.get('OL_MAT_ReferenceGround') or bpy.data.materials.new('OL_MAT_ReferenceGround'); m.use_nodes=True; bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(.055,.055,.058,1); bs.inputs['Roughness'].default_value=.68; o.data.materials.append(m)
def product(m):
 a=[]
 a+=[rounded('OL_REF_PU_Contact_Pad',(.118,.078,.004),(0,0,.002),.002,m['pu'],'pu','soft contact / anti-slip pad')]
 a+=[rounded('OL_REF_PU_Front_Grip',(.056,.004,.010),(0,-.0505,.015),.0018,m['pu'],'pu','front soft-contact grip rail')]
 a+=[rounded('OL_REF_PP_Housing_Lower',(.140,.100,.028),(0,0,.018),.012,m['pp'],'pp','primary housing / lower shell')]
 a+=[rounded('OL_REF_PP_Housing_Lid',(.134,.094,.014),(0,0,.035),.007,m['pp'],'pp','primary housing / upper shell')]
 a+=[rounded('OL_REF_Milky_Diffuser',(.090,.056,.008),(-.012,.004,.046),.004,m['diffuser'],'diffuser','milky transmissive diffuser / signal field')]
 a+=[cyl('OL_REF_Anodized_Al_Knob',.0145,.012,(.044,-.026,.048),m['al'],'al','primary control / brushed anodized aluminum')]
 a+=[rounded('OL_REF_Knob_Index',(.0022,.010,.0012),(.044,-.026,.0544),.0004,m['al'],'al','knob index / same aluminum')]
 a+=[utube(m['powder'])]
 l=cyl('OL_REF_PP_FrameAnchor_L',.007,.012,(-.054,.034,.031),m['pp'],'pp','frame anchor / PP',64); l.rotation_euler[0]=math.radians(90); a.append(l)
 r=cyl('OL_REF_PP_FrameAnchor_R',.007,.012,(.054,.034,.031),m['pp'],'pp','frame anchor / PP',64); r.rotation_euler[0]=math.radians(90); a.append(r)
 return a
def camera(name,spec):
 loc,t,lens=spec; d=bpy.data.cameras.new(name); d.lens=lens; d.sensor_width=36; o=bpy.data.objects.new(name,d); bpy.context.collection.objects.link(o); o.location=loc; look(o,t); return o
def light(name,tup,target=(0,0,.045)):
 shape,en,size,sy,loc=tup; d=bpy.data.lights.new(name,'AREA'); d.energy=en; d.shape=shape; d.size=size
 if shape=='RECTANGLE':d.size_y=sy
 o=bpy.data.objects.new(name,d); bpy.context.collection.objects.link(o); o.location=loc; look(o,target)
def removelights():
 for o in list(bpy.data.objects):
  if o.type=='LIGHT':bpy.data.objects.remove(o,do_unlink=True)
def internal():
 d=bpy.data.lights.new('OL_REF_Diffuser_Internal','AREA'); d.energy=1; d.shape='RECTANGLE'; d.size=.055; d.size_y=.030; o=bpy.data.objects.new('OL_REF_Diffuser_Internal',d); bpy.context.collection.objects.link(o); o.location=(-.012,.004,.044); o.rotation_euler[0]=math.radians(180)
def rig(n):
 removelights(); light('OL_REF_'+n+'_Key',RIGS[n]['key']); light('OL_REF_'+n+'_Fill',RIGS[n]['fill']); internal()
def setup(path,samp,res):
 s=bpy.context.scene; s.render.engine='CYCLES'; s.cycles.samples=samp; s.cycles.use_adaptive_sampling=True
 try:s.cycles.adaptive_threshold=.08
 except Exception:pass
 s.render.use_persistent_data=True; s.render.resolution_x=res; s.render.resolution_y=res; s.render.resolution_percentage=100; s.render.image_settings.file_format='PNG'; s.render.image_settings.color_mode='RGB'; s.render.filepath=str(path)
 try:s.view_settings.view_transform='Khronos PBR Neutral'
 except Exception:pass
 s.world.use_nodes=True; bg=s.world.node_tree.nodes.get('Background'); bg.inputs['Color'].default_value=(.010,.010,.012,1); bg.inputs['Strength'].default_value=.06
def manifold(o):
 if o.type!='MESH':return None
 bm=bmesh.new(); bm.from_mesh(o.data); v=all(e.is_manifold for e in bm.edges); bm.free(); return v
def bounds(objs):
 pts=[]
 for o in objs:
  if o.type in {'MESH','CURVE'}:pts += [o.matrix_world@Vector(c) for c in o.bound_box]
 mn=Vector((min(p.x for p in pts),min(p.y for p in pts),min(p.z for p in pts))); mx=Vector((max(p.x for p in pts),max(p.y for p in pts),max(p.z for p in pts))); return mn,mx
def frame(scene,cam,objs,margin=.015):
 vals=[]
 for o in objs:
  if o.type in {'MESH','CURVE'}:
   vals += [world_to_camera_view(scene,cam,o.matrix_world@Vector(c)) for c in o.bound_box]
 xs=[v.x for v in vals]; ys=[v.y for v in vals]; zs=[v.z for v in vals]; return {'pass':min(xs)>=margin and max(xs)<=1-margin and min(ys)>=margin and max(ys)<=1-margin and min(zs)>0,'x_range':[min(xs),max(xs)],'y_range':[min(ys),max(ys)],'min_depth':min(zs)}
def main():
 a=args(); out=Path(a.out).resolve(); (out/'renders').mkdir(parents=True,exist_ok=True); (out/'receipts').mkdir(parents=True,exist_ok=True)
 m=reqmats(); clear(); ground(); objs=product(m); mn,mx=bounds(objs); size=[mx[i]-mn[i] for i in range(3)]
 cams={k:camera('OL_REF_CAM_'+k,v) for k,v in VIEWS.items()}; bpy.context.view_layer.update(); scene=bpy.context.scene; scene.camera=cams['HERO']
 q={'schema':'oleander.reference-product-geometry-qa.v1','lab':LAB,'model':MODEL,'authority_state':'WORKING_SOURCE','scope':'DESIGN VALIDATION / NOT ENGINEERING','bounds_m':{'min':[round(v,6) for v in mn],'max':[round(v,6) for v in mx],'size':[round(v,6) for v in size]},'objects':[{'object':o.name,'type':o.type,'preset':o.get('OLEANDER_D2_PARAMETER_PRESET'),'role':o.get('OLEANDER_MATERIAL_ROLE'),'manifold':manifold(o),'scale':[round(v,6) for v in o.scale]} for o in objs]}
 q['material_binding_complete']=set(PRE.values()).issubset({o.get('OLEANDER_D2_PARAMETER_PRESET') for o in objs}); q['mesh_manifold_complete']=all(x['manifold'] is not False for x in q['objects']); q['bounds_corridor_pass']=.13<=size[0]<=.16 and .09<=size[1]<=.12 and .085<=size[2]<=.130; q['framing_preflight']={n:frame(scene,cams[n],objs) for n in ('HERO','TOP','SIDE')}; q['framing_gate']='PASS' if all(v['pass'] for v in q['framing_preflight'].values()) else 'FAIL'; q['machine_gate']='PASS' if q['material_binding_complete'] and q['mesh_manifold_complete'] and q['bounds_corridor_pass'] and q['framing_gate']=='PASS' else 'FAIL'
 model=out/(MODEL+'.blend'); bpy.ops.wm.save_as_mainfile(filepath=str(model))
 rec={'schema':'oleander.reference-product-render-receipt.v1','lab':LAB,'model':MODEL,'blender_version':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),'renderer':'Cycles','samples':a.samples,'resolution':[a.resolution,a.resolution],'adaptive_sampling':True,'persistent_data':True,'scene_compile_count':1,'material_library_source':'verified v1.20 D2 Material Preset blend','model_file':str(model),'renders':[],'status':'RUNNING'}
 for view,r in PLAN:
  scene.camera=cams[view]; rig(r); png=out/'renders'/f'{MODEL}__{view}__{r}.png'; setup(png,a.samples,a.resolution); bpy.ops.render.render(write_still=True); rec['renders'].append({'view':view,'rig':r,'file':str(png),'status':'RENDERED_POST_REVIEW_REQUIRED'})
 rec['status']=f"{len(rec['renders'])}_RENDERED_POST_REVIEW_REQUIRED"; (out/'receipts'/'REFERENCE_PRODUCT_GEOMETRY_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); (out/'receipts'/'REFERENCE_PRODUCT_RENDER_RECEIPT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps({'geometry_qa':q,'render_receipt':rec},ensure_ascii=False,indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e: print('OLEANDER_REFERENCE_PRODUCT_FAILED',repr(e)); traceback.print_exc(); raise
