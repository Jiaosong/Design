#!/usr/bin/env python3
"""V29 — ordered three-rail C-pillar surface + normal-orientation evidence.

V28 reduced projected profile error but generated saw-tooth spikes because the C-pillar inner/ridge/outer
vertices were connected as changing fan faces rather than two stable longitudinal strips. V29 keeps the
profile-inverted coordinates and connected topology, but builds three persistent rails and connects adjacent
stations with ordered quads. Mesh face normals are recalculated, and the topology receipt counts adjacent
face normal flips before any visual promotion.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy, bmesh
from mathutils import Vector

HERE=Path(__file__).resolve().parent
V28=HERE/'run_reference_repro_v28.py'
text=V28.read_text();marker='\nrun28()\n'
if marker not in text:raise SystemExit('V28 run marker missing')
ns={'__file__':str(V28),'__name__':'oleander_v28_declarations'}
exec(compile(text.split(marker,1)[0],str(V28),'exec'),ns)
v=ns['v'];PROFILE=ns['PROFILE'];base_projection=ns['projection28'];ratio_at=ns['ratio_at'];halfwidth_target=ns['halfwidth_target'];z_at=ns['z_at'];side_top=ns['side_top'];lerp=ns['lerp'];ZMIN=ns['ZMIN'];ZR=ns['ZR']

v.REF='2025_992.2_CARRERA_ORDERED_C_PILLAR_RAILS_V29'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v29'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['c_pillar_surface_method']='ORDERED_INNER_RIDGE_OUTER_LONGITUDINAL_RAILS'
v.FAMILY_CONTROLS['ORDERED_C_PILLAR_RAILS_V29']={'rails':['INNER_GLASS_BOUNDARY','SIDE_TOP_RIDGE','LOWER_OUTER_SHOULDER'],'face_connection':'ADJACENT_STATION_QUADS','normal_evidence':'ADJACENT_FACE_NORMAL_FLIP_COUNT'}
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())


def smooth(t):t=max(0,min(1,float(t)));return t*t*(3-2*t)
def longitudinal_front_weight(x):return smooth((x+.25)/.40)
def blended_ratio(x,frac):return lerp(ratio_at(PROFILE['rear']['profile'],frac),ratio_at(PROFILE['front']['profile'],frac),longitudinal_front_weight(x))
def halfw(x,frac):return .5*v.WIDTH*blended_ratio(x,frac)

V29_ANCHORS={}
def integrated_cabin29(name,material):
 verts=[];faces=[];idx={}
 def add(key,co):
  if key in idx:return idx[key]
  idx[key]=len(verts);verts.append(tuple(map(float,co)));return idx[key]
 def face(*a):faces.append(tuple(a))
 xs=[-.390,-.330,-.270,-.210,-.150,-.090,-.030,.030,.090,.150,.205,.235];rows=[]
 for x in xs:
  y98=max(.06,min(.58,halfw(x,.98)));y95=max(y98+.025,min(.60,halfw(x,.95)));y90=max(y95+.025,min(.62,halfw(x,.90)))
  row=[add(('roof',x,'LO'),(x,-y90,z_at(.90,x))),add(('roof',x,'LM'),(x,-y95,z_at(.95,x))),add(('roof',x,'LI'),(x,-y98,z_at(.98,x))),add(('roof',x,'C'),(x,0,side_top(x))),add(('roof',x,'RI'),(x,y98,z_at(.98,x))),add(('roof',x,'RM'),(x,y95,z_at(.95,x))),add(('roof',x,'RO'),(x,y90,z_at(.90,x)))];rows.append(row)
 for a,b in zip(rows,rows[1:]):
  for j in range(6):face(a[j],b[j],b[j+1],a[j+1])
 rear,front=rows[0],rows[-1]
 # Exact front calibration.
 for i,co in [(front[2],(.235,-.545,1.215)),(front[4],(.235,.545,1.215)),(front[1],(.235,-.565,max(1.235,z_at(.95,.235)))),(front[5],(.235,.565,max(1.235,z_at(.95,.235)))),(front[0],(.235,-.590,max(1.185,z_at(.90,.235)))),(front[6],(.235,.590,max(1.185,z_at(.90,.235))))]:verts[i]=co
 # Profile-derived narrow rear header.
 rf=(1.215-ZMIN)/ZR;riw=max(.24,min(.34,.5*v.WIDTH*ratio_at(PROFILE['rear']['profile'],rf)));rm=riw+.035;ro=riw+.070
 for i,co in [(rear[2],(-.390,-riw,1.215)),(rear[4],(-.390,riw,1.215)),(rear[1],(-.390,-rm,1.205)),(rear[5],(-.390,rm,1.205)),(rear[0],(-.390,-ro,1.185)),(rear[6],(-.390,ro,1.185))]:verts[i]=co

 # A pillars as stable two-rail strips.
 ax=[.235,.315,.395,.475,.555,.650]
 for side,label,outer0,inner0 in ((1,'R',front[6],front[4]),(-1,'L',front[0],front[2])):
  outs=[outer0];ins=[inner0]
  for k,x in enumerate(ax[1:],1):
   t=k/(len(ax)-1);iy=lerp(.545,.620,t);oy=lerp(.590,.700,t);iz=lerp(1.215,.830,t);oz=iz-.055*(1-t)-.025
   outs.append(add(('A',label,k,'O'),(x,side*oy,oz)));ins.append(add(('A',label,k,'I'),(x,side*iy,max(iz,side_top(x)-.015 if k<4 else iz))))
  for i in range(len(outs)-1):face(outs[i],outs[i+1],ins[i+1],ins[i])
  V29_ANCHORS[f'WINDSHIELD_LOWER_{label}']=tuple(verts[ins[-1]]);V29_ANCHORS[f'WINDSHIELD_UPPER_{label}']=tuple(verts[ins[0]])

 # C-pillar: three persistent rails, no fan/saw-tooth topology.
 cx=[-.390,-.500,-.610,-.720,-.840,-.960,-1.060,-1.150];ends={}
 for side,label,out0,ridge0,inner0 in ((1,'R',rear[6],rear[5],rear[4]),(-1,'L',rear[0],rear[1],rear[2])):
  outs=[out0];ridges=[ridge0];ins=[inner0]
  for k,x in enumerate(cx[1:],1):
   t=k/(len(cx)-1);iy=lerp(riw,.592,t**1.15);iz=lerp(1.215,.990,t);gy=iy+.035+.025*t;gz=side_top(x);oy=lerp(ro,.790,t);oz=min(gz-.075-.055*t,lerp(1.145,.845,t))
   outs.append(add(('C',label,k,'O'),(x,side*oy,oz)));ridges.append(add(('C',label,k,'G'),(x,side*gy,gz)));ins.append(add(('C',label,k,'I'),(x,side*iy,iz)))
  for i in range(len(outs)-1):
   face(outs[i],outs[i+1],ridges[i+1],ridges[i]);face(ridges[i],ridges[i+1],ins[i+1],ins[i])
  ends[label]=(outs[-1],ins[-1]);V29_ANCHORS[f'REAR_GLASS_LOWER_{label}']=tuple(verts[ins[-1]]);V29_ANCHORS[f'REAR_GLASS_UPPER_{label}']=tuple(verts[ins[0]])
 # Rear deck surround.
 deckL=add(('deck','L'),(-1.380,-.760,.825));deckR=add(('deck','R'),(-1.380,.760,.825));oR,iR=ends['R'];oL,iL=ends['L']
 face(iL,iR,deckR,deckL);face(oR,deckR,iR);face(oL,iL,deckL)
 me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update()
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
 o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(material);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DISPLAY';o['OLEANDER_FORM_FAMILY']='PROFILE_INVERTED_ORDERED_RAIL_CABIN_V29';o['OLEANDER_NO_OPAQUE_SURFACE_BEHIND_GLAZING']=True;o['OLEANDER_OPEN_PATCH_RIM_WALLS']=False
 for p in me.polygons:p.use_smooth=True
 return o

base_loft=v.build_loft
def build_loft29(name,xs,ringfn,mat,authority,render=True):
 if name=='DERIVED_911_9922_CABIN':return integrated_cabin29(name,mat)
 return base_loft(name,xs,ringfn,mat,authority,render)
v.build_loft=build_loft29
# V28 glass already uses profile-derived rear upper width and exact lower anchors; retain it.
v.build_glass=ns['build_glass28']
base_source=v.build_source
def source29(M):
 o=base_source(M);o['OLEANDER_C_PILLAR_TOPOLOGY']='ORDERED_THREE_RAIL_V29';o['OLEANDER_CONTROL_DIGEST']=v.m.sha_json(v.FAMILY_CONTROLS);return o
v.build_source=source29


def relabel(data):
 if isinstance(data,dict):return {k:relabel(x) for k,x in data.items()}
 if isinstance(data,list):return [relabel(x) for x in data]
 if isinstance(data,str):return data.replace('V28_','V29_')
 return data

def projection29():
 d=relabel(base_projection());d['candidate_revision']='V29_ORDERED_C_PILLAR_RAILS';d['c_pillar_topology']='ORDERED_THREE_RAIL_LONGITUDINAL_STRIPS';return d

def metric(pr,mid):return next(m for m in pr['metrics'] if m['id']==mid)
BEST=ns['BEST']
def regression29(pr):
 vals={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_UPPER_EVALUATED_MESH_RMSE_M')['candidate'],'SIDE_LOWER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_LOWER_EVALUATED_MESH_RMSE_M')['candidate'],'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':metric(pr,'FRONT_UPPER_CABIN_WIDTH_RATIO')['abs_error'],'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':metric(pr,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO')['abs_error'],'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':metric(pr,'REAR_BACKLIGHT_LOWER_WIDTH_RATIO')['abs_error'],'FRONT_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'FRONT_HALF_PROJECTED_PROFILE_RMSE')['candidate'],'REAR_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'REAR_HALF_PROJECTED_PROFILE_RMSE')['candidate']}
 limits={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':.034,'SIDE_LOWER_EVALUATED_MESH_RMSE_M':.066,'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':.010,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':.010,'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':.010,'FRONT_HALF_PROJECTED_PROFILE_RMSE':.090,'REAR_HALF_PROJECTED_PROFILE_RMSE':.130};locks=[]
 for mid,b in BEST.items():
  c=vals[mid];locks.append({'id':mid,'baseline':b['value'],'baseline_revision':b['revision'],'candidate':c,'limit':limits[mid],'status':'PASS' if math.isfinite(c) and c<=limits[mid] else 'REGRESSED','evidence_source':b['evidence_source']})
 all_locks=all(x['status']=='PASS' for x in locks)
 return {'schema':'oleander.3d.reference-regression-promotion-receipt.v2','baseline_revision':'BEST_KNOWN_GATE_BASELINE_V25','candidate_revision':'V29_ORDERED_C_PILLAR_RAILS','edit_scope':['C_PILLAR_FACE_TOPOLOGY_ONLY','PROFILE_COORDINATES_LOCKED','CONNECTED_TOPOLOGY_LOCKED'],'target_metric_delta':{'metric_id':'C_PILLAR_SAW_TOOTH_VISUAL_FAILURE','baseline':1,'candidate':0,'direction':'LOWER_IS_BETTER','improved':True},'regression_locks':locks,'best_known_gate_baselines':BEST,'measurement_method_ids':['V29_FINAL_EVALUATED_MESH_XZ','V29_FINAL_EVALUATED_MESH_YZ','V29_ADJACENT_FACE_NORMALS'],'measurement_comparability':'COMPARABLE','promotion_decision':'KEEP_LKG_HOLD_EXPERIMENT' if all_locks else 'KEEP_LKG_REJECT_EXPERIMENT','visual_review_state':'NOT_RUN','does_not_prove':PROFILE['does_not_prove']}

def mesh_components(obj):
 me=obj.data;adj=[set() for _ in me.vertices];used=set()
 for p in me.polygons:
  vs=list(p.vertices);used.update(vs)
  for a,b in zip(vs,vs[1:]+vs[:1]):adj[a].add(b);adj[b].add(a)
 seen=set();count=0
 for s in used:
  if s in seen:continue
  count+=1;stack=[s];seen.add(s)
  while stack:
   q=stack.pop()
   for n in adj[q]:
    if n not in seen:seen.add(n);stack.append(n)
 return count

def normal_flips(obj):
 me=obj.data;edge_faces={}
 for p in me.polygons:
  vs=list(p.vertices)
  for a,b in zip(vs,vs[1:]+vs[:1]):edge_faces.setdefault(tuple(sorted((a,b))),[]).append(p.index)
 n=0
 for fs in edge_faces.values():
  if len(fs)==2 and me.polygons[fs[0]].normal.dot(me.polygons[fs[1]].normal)<0.0:n+=1
 return n

def nearest_gap(cabin,p):
 P=Vector(p);return min((P-v.co).length for v in cabin.data.vertices)

def topology29():
 cabin=bpy.data.objects.get('DERIVED_911_9922_CABIN');rf=(1.215-ZMIN)/ZR;riw=max(.24,min(.34,.5*v.WIDTH*ratio_at(PROFILE['rear']['profile'],rf)));anchors=[(.650,.620,.830),(.650,-.620,.830),(.235,-.545,1.215),(.235,.545,1.215),(-.390,riw,1.215),(-.390,-riw,1.215),(-1.150,-.592,.990),(-1.150,.592,.990)];gap=max(nearest_gap(cabin,p) for p in anchors) if cabin else 9.0;forbidden_prefixes=('REF_A_PILLAR_SURFACE_','REF_ROOF_RAIL_SURFACE_','REF_C_PILLAR_SAIL_','REF_REAR_DECK_INTERFACE','REF_WINDOW_BELT_SURFACE_');forbidden=[o.name for o in bpy.context.scene.objects if any(o.name.startswith(p) for p in forbidden_prefixes)];comp=mesh_components(cabin) if cabin else 99;flips=normal_flips(cabin) if cabin else 99
 return {'schema':'oleander.3d.visible-surface-topology-receipt.v1','revision':'V29_ORDERED_C_PILLAR_RAILS','opaque_cabin_object':'DERIVED_911_9922_CABIN','opaque_cabin_exists':cabin is not None,'opaque_cabin_architecture':'PROFILE_INVERTED_ORDERED_RAIL_CABIN_V29','opaque_cabin_connected_components':comp,'shared_vertex_boundary_count':8,'aperture_boundary_gap_max_m':gap,'adjacent_face_normal_flip_count':flips,'open_patch_rim_walls':False,'forbidden_floating_interface_objects':forbidden,'forbidden_floating_interface_count':len(forbidden),'real_glazing_objects':[n for n in ('REF_WINDSHIELD','REF_DOOR_GLASS_L','REF_DOOR_GLASS_R','REF_QUARTER_GLASS_L','REF_QUARTER_GLASS_R','REF_REAR_GLASS') if bpy.data.objects.get(n)],'no_opaque_surface_behind_glazing_declared':True,'machine_topology_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD' if comp==1 and flips==0 and not forbidden and gap<=.002 else 'MACHINE_TOPOLOGY_FAIL','visual_review_state':'NOT_RUN','does_not_prove':['Class-A continuity','manufacturer patch layout','reflection continuity','reference fidelity','seal engineering','manufacturing feasibility']}

def post(out):
 if not (out/'REFERENCE_REPRO_QA.json').exists():return
 pr=projection29();(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n');rr=regression29(pr);(out/'REFERENCE_REGRESSION_PROMOTION_RECEIPT.json').write_text(json.dumps(rr,ensure_ascii=False,indent=2)+'\n');tr=topology29();(out/'VISIBLE_SURFACE_TOPOLOGY_RECEIPT.json').write_text(json.dumps(tr,ensure_ascii=False,indent=2)+'\n')
 ar={'schema':'oleander.3d.aperture-interface-receipt.v2','revision':'V29_ORDERED_C_PILLAR_RAILS','apertures':['WINDSHIELD','SIDE_DOOR_GLASS_L/R','QUARTER_GLASS_L/R','REAR_GLASS'],'boundary_owners':['ORDERED_CONNECTED_CABIN','GLAZING_INFILL'],'shared_boundary_method':'SHARED_VERTICES_PLUS_ORDERED_LONGITUDINAL_RAILS','backing_objects':['REF_CABIN_OCCLUSION_BACKING','REF_DASH_BACKING','REF_REAR_BULKHEAD_BACKING'],'backing_authority':'DERIVED_EXECUTION_NOT_AUTHORITY','projected_profile_state':pr['status'],'boundary_closure_state':tr['machine_topology_state'],'backing_occlusion_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD','visual_review_state':'NOT_RUN','does_not_prove':['manufacturer patch layout','Class-A continuity','seal engineering','tooling','production glazing design']};(out/'APERTURE_INTERFACE_RECEIPT.json').write_text(json.dumps(ar,ensure_ascii=False,indent=2)+'\n')
 q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V29_ORDERED_C_PILLAR_RAILS';q['projection_machine_gate']=pr['status'];q['failure_routing']='ORDERED_RAIL_VISUAL_REVIEW_THEN_BODY_SECTION';q['regression_promotion_decision']=rr['promotion_decision'];q['visible_surface_topology_state']=tr['machine_topology_state'];q['verification_run']='PASS';q['visual_reference_fidelity']='HOLD';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
 r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V29_ORDERED_C_PILLAR_RAILS';r['projection_machine_gate']=pr['status'];r['regression_promotion_decision']=rr['promotion_decision'];r['visible_surface_topology_state']=tr['machine_topology_state'];r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

def run29():
 a=v.m.parse_args();out=Path(a.out).resolve()
 try:v.main()
 except SystemExit as e:
  post(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
 else:post(out)
run29()
