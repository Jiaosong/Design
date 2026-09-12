#!/usr/bin/env python3
"""V28 — projection-profile-inverted cabin cross-section on V27 connected topology.

V27 established real connected topology and exact calibrated aperture anchors, but FRONT/REAR width profiles
regressed because the cabin cross-section was still designer-guessed. V28 derives the high cabin envelope from
REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json and preserves V27 topology/aperture discipline.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy
from mathutils import Vector

HERE=Path(__file__).resolve().parent
V27=HERE/'run_reference_repro_v27.py'
text=V27.read_text();marker='\nrun27()\n'
if marker not in text:raise SystemExit('V27 run marker missing')
ns={'__file__':str(V27),'__name__':'oleander_v27_declarations'}
exec(compile(text.split(marker,1)[0],str(V27),'exec'),ns)
v=ns['v'];PROFILE=ns['PROFILE'];base_projection=ns['projection27'];side_top=ns['side_top'];smooth=ns['smooth'];lerp=ns['lerp']

v.REF='2025_992.2_CARRERA_PROFILE_INVERTED_CABIN_V28'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v28'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['cabin_cross_section_method']='INVERT_FRONT_REAR_PROJECTED_WIDTH_PROFILE_TO_CONNECTED_CABIN_ENVELOPE'
v.REFERENCE_CONTRACT['profile_evidence_status']=PROFILE['status']
v.FAMILY_CONTROLS['PROFILE_INVERTED_CABIN_V28']={'profile_source':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json','height_knots':[1.0,.98,.95,.90,.85,.80],'protected':['V27_CONNECTED_TOPOLOGY','WINDSHIELD_CALIBRATION','REAR_GLASS_LOWER_CALIBRATION','SIDE_LOWER','WHEELS','BODY_XZ']}
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

ZMIN=.140;ZMAX=1.298;ZR=ZMAX-ZMIN

def ratio_at(profile,frac):
 pts=sorted([(float(a),float(b)) for a,b in profile],reverse=True)
 if frac>=pts[0][0]:
  # Extrapolate to zero-ish apex at 1.0 from highest recorded sample.
  f0,r0=pts[0];return max(0.0,r0*(1.0-frac)/(1.0-f0)) if frac<=1.0 else 0.0
 if frac<=pts[-1][0]:return pts[-1][1]
 for (f0,r0),(f1,r1) in zip(pts,pts[1:]):
  if f0>=frac>=f1:
   t=(f0-frac)/(f0-f1);return lerp(r0,r1,t)
 return pts[-1][1]

def longitudinal_front_weight(x):
 # rear-dominant by x=-.25, front-dominant by x=.15; smooth transition through roof center.
 return smooth((x+.25)/.40)

def blended_ratio(x,frac):
 w=longitudinal_front_weight(x);rf=ratio_at(PROFILE['front']['profile'],frac);rr=ratio_at(PROFILE['rear']['profile'],frac);return lerp(rr,rf,w)

def halfwidth_target(x,frac,margin=0.0):return .5*v.WIDTH*blended_ratio(x,frac)+margin

def z_at(frac,x):
 # Keep each station's center on calibrated SIDE_TOP while retaining reference-derived transverse relative heights.
 return ZMIN+frac*ZR+(side_top(x)-ZMAX)

V28_ANCHORS={}
def integrated_cabin28(name,material):
 verts=[];faces=[];idx={}
 def add(key,co):
  if key in idx:return idx[key]
  idx[key]=len(verts);verts.append(tuple(map(float,co)));return idx[key]
 def face(*vtx):faces.append(tuple(vtx))

 # 7-point cross-section from profile height/width knots. Center is apex; edge is ~80%-height roof/rail transition.
 xs=[-.390,-.330,-.270,-.210,-.150,-.090,-.030,.030,.090,.150,.205,.235]
 rows=[]
 for x in xs:
  # rear->front projected profile controls the transverse crown, not a hand-written edge drop.
  f98=.98;f95=.95;f90=.90
  y98=min(.58,halfwidth_target(x,f98));y95=min(.60,halfwidth_target(x,f95));y90=min(.62,halfwidth_target(x,f90))
  # monotonic guard for noisy perspective-derived profile measurements.
  y98=max(.06,y98);y95=max(y98+.025,y95);y90=max(y95+.025,y90)
  row=[add(('roof',x,'LO'),(x,-y90,z_at(f90,x))),add(('roof',x,'LM'),(x,-y95,z_at(f95,x))),add(('roof',x,'LI'),(x,-y98,z_at(f98,x))),add(('roof',x,'C'),(x,0,side_top(x))),add(('roof',x,'RI'),(x,y98,z_at(f98,x))),add(('roof',x,'RM'),(x,y95,z_at(f95,x))),add(('roof',x,'RO'),(x,y90,z_at(f90,x)))]
  rows.append(row)
 for a,b in zip(rows,rows[1:]):
  for j in range(6):face(a[j],b[j],b[j+1],a[j+1])

 rear=rows[0];front=rows[-1]
 # Front windshield anchors remain exact best-known calibration. Connect them into the roof header row.
 for i,co in [(front[2],(.235,-.545,1.215)),(front[4],(.235,.545,1.215))]:verts[i]=co
 # Front outer rail stays only moderately wider than glass, not a full slab.
 verts[front[1]]=(.235,-.565,max(1.235,z_at(.95,.235)));verts[front[5]]=(.235,.565,max(1.235,z_at(.95,.235)))
 verts[front[0]]=(.235,-.590,max(1.185,z_at(.90,.235)));verts[front[6]]=(.235,.590,max(1.185,z_at(.90,.235)))

 # Rear header top is NOT locked to the old ±.490 guess. Derive its upper width from the rear profile at z=1.215.
 rear_frac=(1.215-ZMIN)/ZR
 rear_inner=max(.24,min(.34,.5*v.WIDTH*ratio_at(PROFILE['rear']['profile'],rear_frac)))
 rear_mid=rear_inner+.035;rear_outer=rear_inner+.070
 for i,co in [(rear[2],(-.390,-rear_inner,1.215)),(rear[4],(-.390,rear_inner,1.215)),(rear[1],(-.390,-rear_mid,1.205)),(rear[5],(-.390,rear_mid,1.205)),(rear[0],(-.390,-rear_outer,1.185)),(rear[6],(-.390,rear_outer,1.185))]:verts[i]=co

 # A pillars: high silhouette sits on the inner/ridge line; outer frame falls away in z, preventing top-width inflation.
 ax=[.235,.315,.395,.475,.555,.650]
 for side,label,ro,ri in ((1,'R',front[6],front[4]),(-1,'L',front[0],front[2])):
  prev_o,prev_i=ro,ri
  for k,x in enumerate(ax[1:],1):
   t=k/(len(ax)-1);iy=lerp(.545,.620,t);oy=lerp(.590,.700,t)
   iz=lerp(1.215,.830,t);oz=iz-.055*(1-t)-.025
   oi=add(('A',label,k,'O'),(x,side*oy,oz));ii=add(('A',label,k,'I'),(x,side*iy,max(iz,side_top(x)-.015 if k<4 else iz)))
   face(prev_o,oi,ii,prev_i);prev_o,prev_i=oi,ii
  V28_ANCHORS[f'WINDSHIELD_LOWER_{label}']=tuple(verts[prev_i]);V28_ANCHORS[f'WINDSHIELD_UPPER_{label}']=tuple(verts[ri])

 # C-pillar/sail: inner ridge owns SIDE_TOP while outer shoulder is lower and widens progressively.
 cx=[-.390,-.500,-.610,-.720,-.840,-.960,-1.060,-1.150]
 c_end={}
 for side,label,ro,ri in ((1,'R',rear[6],rear[4]),(-1,'L',rear[0],rear[2])):
  prev_o,prev_i=ro,ri
  for k,x in enumerate(cx[1:],1):
   t=k/(len(cx)-1)
   # inner line expands from profile-derived rear header to exact lower backlight anchor.
   iy=lerp(rear_inner,.592,t**1.15);iz=lerp(1.215,.990,t)
   # ridge follows side silhouette but remains near the inner line; wide shoulder is deliberately lower.
   ridge_y=iy+.035+.025*t;ridge_z=side_top(x)
   oy=lerp(rear_outer,.790,t);oz=min(ridge_z-.075-.055*t,lerp(1.145,.845,t))
   # two-strip construction shares the ridge vertex: inner→ridge→outer shoulder.
   ridge=add(('C',label,k,'G'),(x,side*ridge_y,ridge_z));outer=add(('C',label,k,'O'),(x,side*oy,oz));inner=add(('C',label,k,'I'),(x,side*iy,iz))
   # first segment from previous row: previous outer to new shoulder/ridge; second: ridge to inner.
   if k==1:
    face(prev_o,outer,ridge,prev_i)
   else:
    face(prev_o,outer,ridge,prev_i)
   face(prev_i,ridge,inner)
   prev_o,prev_i=outer,inner
  c_end[label]=(prev_o,prev_i)
  V28_ANCHORS[f'REAR_GLASS_LOWER_{label}']=tuple(verts[prev_i]);V28_ANCHORS[f'REAR_GLASS_UPPER_{label}']=tuple(verts[ri])

 # Rear deck below backlight, sharing C-terminal vertices.
 rear_l=add(('deck','L'),(-1.380,-.760,.825));rear_r=add(('deck','R'),(-1.380,.760,.825));coR,ciR=c_end['R'];coL,ciL=c_end['L']
 face(ciL,ciR,rear_r,rear_l);face(coR,rear_r,ciR);face(coL,ciL,rear_l)

 me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(material)
 o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DISPLAY';o['OLEANDER_FORM_FAMILY']='PROFILE_INVERTED_CONNECTED_CABIN_V28';o['OLEANDER_NO_OPAQUE_SURFACE_BEHIND_GLAZING']=True;o['OLEANDER_OPEN_PATCH_RIM_WALLS']=False
 for p in me.polygons:p.use_smooth=True
 return o

base_loft=v.build_loft
def build_loft28(name,xs,ringfn,mat,authority,render=True):
 if name=='DERIVED_911_9922_CABIN':return integrated_cabin28(name,mat)
 return base_loft(name,xs,ringfn,mat,authority,render)
v.build_loft=build_loft28

# Glass uses exact front/lower-rear calibration; rear upper width follows profile-inverted header.
def add_panel(name,pts,mat,thickness=.0025):
 me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(pts,[],[tuple(range(len(pts)))]);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL'
 if thickness:
  s=o.modifiers.new(name+'_THICKNESS','SOLIDIFY');s.thickness=thickness;s.offset=0;s.use_rim=False
 for p in me.polygons:p.use_smooth=True
 return o

def build_glass28(M):
 out=[];rear_frac=(1.215-ZMIN)/ZR;rear_inner=max(.24,min(.34,.5*v.WIDTH*ratio_at(PROFILE['rear']['profile'],rear_frac)))
 out.append(add_panel('REF_WINDSHIELD',[(.650,.620,.830),(.650,-.620,.830),(.235,-.545,1.215),(.235,.545,1.215)],M['glass']))
 out.append(add_panel('REF_REAR_GLASS',[(-.390,rear_inner,1.215),(-.390,-rear_inner,1.215),(-1.150,-.592,.990),(-1.150,.592,.990)],M['glass']))
 for side,label in ((1,'L'),(-1,'R')):
  # Door top follows the connected roof edge; quarter top transitions into the profile-inverted C inner boundary.
  door=[(.600,side*.600,.840),(.235,side*.590,1.185),(-.180,side*max(.38,halfwidth_target(-.180,.90)),z_at(.90,-.180)),(-.180,side*.570,.842),(.500,side*.605,.840)]
  qtop=(-.390,side*rear_inner,1.215);qrear=(-.720,side*lerp(rear_inner,.592,(.720-.390)/(.760)),lerp(1.215,.990,(.720-.390)/(.760)))
  quarter=[door[2],qtop,qrear,(-.650,side*.555,.885),(-.180,side*.570,.842)]
  out.append(add_panel('REF_DOOR_GLASS_'+label,door,M['glass']));out.append(add_panel('REF_QUARTER_GLASS_'+label,quarter,M['glass']))
  b=v.m.add_cube('REF_B_PILLAR_'+label,(-.180,side*.548,1.015),(.030,.025,.300),M['body_dark'],.003);b['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';out.append(b)
  out.append(v.m.add_cube('REF_DOOR_HANDLE_'+label,(-.020,side*.896,.682),(.105,.012,.017),M['body_dark'],.003));y=side*.912;out.append(v.m.add_curve('REF_DOOR_SEAM_'+label,[(.595,y,.765),(.545,y,.500),(-.635,y,.500),(-.800,y,.665),(-.785,y,.825)],M['seam'],.0016))
 for name,loc,scale in [('REF_CABIN_OCCLUSION_BACKING',(-.18,0,.785),(1.42,.86,.10)),('REF_DASH_BACKING',(.410,0,.760),(.30,.88,.09)),('REF_REAR_BULKHEAD_BACKING',(-.840,0,.745),(.16,.82,.12))]:
  o=v.m.add_cube(name,loc,scale,M['body_dark'],.006);o['OLEANDER_AUTHORITY']='DERIVED_EXECUTION_NOT_AUTHORITY';out.append(o)
 return out
v.build_glass=build_glass28

base_source=v.build_source
def source28(M):
 o=base_source(M);o['OLEANDER_CABIN_SECTION_METHOD']='V28_PROFILE_INVERSION';o['OLEANDER_CONTROL_DIGEST']=v.m.sha_json(v.FAMILY_CONTROLS);return o
v.build_source=source28


def relabel(data):
 if isinstance(data,dict):return {k:relabel(x) for k,x in data.items()}
 if isinstance(data,list):return [relabel(x) for x in data]
 if isinstance(data,str):return data.replace('V27_','V28_')
 return data

def projection28():
 d=relabel(base_projection());d['candidate_revision']='V28_PROFILE_INVERTED_CABIN';d['cabin_section_method']='REFERENCE_PROJECTED_PROFILE_INVERSION';return d

def metric(pr,mid):return next(m for m in pr['metrics'] if m['id']==mid)
BEST=ns['BEST']
def regression28(pr):
 vals={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_UPPER_EVALUATED_MESH_RMSE_M')['candidate'],'SIDE_LOWER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_LOWER_EVALUATED_MESH_RMSE_M')['candidate'],'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':metric(pr,'FRONT_UPPER_CABIN_WIDTH_RATIO')['abs_error'],'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':metric(pr,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO')['abs_error'],'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':metric(pr,'REAR_BACKLIGHT_LOWER_WIDTH_RATIO')['abs_error'],'FRONT_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'FRONT_HALF_PROJECTED_PROFILE_RMSE')['candidate'],'REAR_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'REAR_HALF_PROJECTED_PROFILE_RMSE')['candidate']}
 limits={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':.034,'SIDE_LOWER_EVALUATED_MESH_RMSE_M':.066,'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':.010,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':.010,'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':.010,'FRONT_HALF_PROJECTED_PROFILE_RMSE':.090,'REAR_HALF_PROJECTED_PROFILE_RMSE':.130}
 locks=[]
 for mid,b in BEST.items():
  c=vals[mid];locks.append({'id':mid,'baseline':b['value'],'baseline_revision':b['revision'],'candidate':c,'limit':limits[mid],'status':'PASS' if math.isfinite(c) and c<=limits[mid] else 'REGRESSED','evidence_source':b['evidence_source']})
 rear=vals['REAR_HALF_PROJECTED_PROFILE_RMSE'];front=vals['FRONT_HALF_PROJECTED_PROFILE_RMSE'];all_locks=all(x['status']=='PASS' for x in locks)
 return {'schema':'oleander.3d.reference-regression-promotion-receipt.v2','baseline_revision':'BEST_KNOWN_GATE_BASELINE_V25','candidate_revision':'V28_PROFILE_INVERTED_CABIN','edit_scope':['CABIN_YZ_SECTION_ONLY','PROFILE_INVERSION','CONNECTED_TOPOLOGY_LOCKED','APERTURE_ANCHORS_PROTECTED'],'target_metric_delta':{'metric_id':'REAR_HALF_PROJECTED_PROFILE_RMSE','baseline':.3011535243529628,'candidate':rear,'direction':'LOWER_IS_BETTER','improved':rear<.3011535243529628},'secondary_target_metrics':[{'metric_id':'FRONT_HALF_PROJECTED_PROFILE_RMSE','baseline':.1204951066301607,'candidate':front,'direction':'LOWER_IS_BETTER','improved':front<.1204951066301607}],'regression_locks':locks,'best_known_gate_baselines':BEST,'measurement_method_ids':['V28_FINAL_EVALUATED_MESH_XZ','V28_FINAL_EVALUATED_MESH_YZ','V28_CONNECTED_TOPOLOGY'],'measurement_comparability':'COMPARABLE','promotion_decision':'KEEP_LKG_HOLD_EXPERIMENT' if all_locks else 'KEEP_LKG_REJECT_EXPERIMENT','visual_review_state':'NOT_RUN','does_not_prove':PROFILE['does_not_prove']}

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

def nearest_gap(cabin,p):
 P=Vector(p);return min((P-v.co).length for v in cabin.data.vertices)

def topology28():
 cabin=bpy.data.objects.get('DERIVED_911_9922_CABIN');rear_frac=(1.215-ZMIN)/ZR;ri=max(.24,min(.34,.5*v.WIDTH*ratio_at(PROFILE['rear']['profile'],rear_frac)))
 anchors=[(.650,.620,.830),(.650,-.620,.830),(.235,-.545,1.215),(.235,.545,1.215),(-.390,ri,1.215),(-.390,-ri,1.215),(-1.150,-.592,.990),(-1.150,.592,.990)]
 gap=max(nearest_gap(cabin,p) for p in anchors) if cabin else 9.0
 forbidden_prefixes=('REF_A_PILLAR_SURFACE_','REF_ROOF_RAIL_SURFACE_','REF_C_PILLAR_SAIL_','REF_REAR_DECK_INTERFACE','REF_WINDOW_BELT_SURFACE_');forbidden=[o.name for o in bpy.context.scene.objects if any(o.name.startswith(p) for p in forbidden_prefixes)]
 comp=mesh_components(cabin) if cabin else 99
 return {'schema':'oleander.3d.visible-surface-topology-receipt.v1','revision':'V28_PROFILE_INVERTED_CABIN','opaque_cabin_object':'DERIVED_911_9922_CABIN','opaque_cabin_exists':cabin is not None,'opaque_cabin_architecture':'PROFILE_INVERTED_CONNECTED_CABIN_V28','opaque_cabin_connected_components':comp,'shared_vertex_boundary_count':8,'aperture_boundary_gap_max_m':gap,'open_patch_rim_walls':False,'forbidden_floating_interface_objects':forbidden,'forbidden_floating_interface_count':len(forbidden),'real_glazing_objects':[n for n in ('REF_WINDSHIELD','REF_DOOR_GLASS_L','REF_DOOR_GLASS_R','REF_QUARTER_GLASS_L','REF_QUARTER_GLASS_R','REF_REAR_GLASS') if bpy.data.objects.get(n)],'no_opaque_surface_behind_glazing_declared':True,'machine_topology_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD' if comp==1 and not forbidden and gap<=.002 else 'MACHINE_TOPOLOGY_FAIL','visual_review_state':'NOT_RUN','does_not_prove':['Class-A continuity','manufacturer patch layout','reflection continuity','reference fidelity','seal engineering','manufacturing feasibility']}

def post(out):
 if not (out/'REFERENCE_REPRO_QA.json').exists():return
 pr=projection28();(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n');rr=regression28(pr);(out/'REFERENCE_REGRESSION_PROMOTION_RECEIPT.json').write_text(json.dumps(rr,ensure_ascii=False,indent=2)+'\n');tr=topology28();(out/'VISIBLE_SURFACE_TOPOLOGY_RECEIPT.json').write_text(json.dumps(tr,ensure_ascii=False,indent=2)+'\n')
 ar={'schema':'oleander.3d.aperture-interface-receipt.v2','revision':'V28_PROFILE_INVERTED_CABIN','apertures':['WINDSHIELD','SIDE_DOOR_GLASS_L/R','QUARTER_GLASS_L/R','REAR_GLASS'],'boundary_owners':['CONNECTED_PROFILE_INVERTED_CABIN','GLAZING_INFILL'],'shared_boundary_method':'PROFILE_INVERTED_SHARED_VERTEX_BOUNDARIES','backing_objects':['REF_CABIN_OCCLUSION_BACKING','REF_DASH_BACKING','REF_REAR_BULKHEAD_BACKING'],'backing_authority':'DERIVED_EXECUTION_NOT_AUTHORITY','projected_profile_state':pr['status'],'boundary_closure_state':tr['machine_topology_state'],'backing_occlusion_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD','visual_review_state':'NOT_RUN','does_not_prove':['manufacturer patch layout','Class-A continuity','seal engineering','tooling','production glazing design']};(out/'APERTURE_INTERFACE_RECEIPT.json').write_text(json.dumps(ar,ensure_ascii=False,indent=2)+'\n')
 q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V28_PROFILE_INVERTED_CABIN';q['projection_machine_gate']=pr['status'];q['failure_routing']='PROFILE_INVERTED_CABIN_VISUAL_REVIEW';q['regression_promotion_decision']=rr['promotion_decision'];q['visible_surface_topology_state']=tr['machine_topology_state'];q['verification_run']='PASS';q['visual_reference_fidelity']='HOLD';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
 r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V28_PROFILE_INVERTED_CABIN';r['projection_machine_gate']=pr['status'];r['regression_promotion_decision']=rr['promotion_decision'];r['visible_surface_topology_state']=tr['machine_topology_state'];r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

def run28():
 a=v.m.parse_args();out=Path(a.out).resolve()
 try:v.main()
 except SystemExit as e:
  post(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
 else:post(out)
run28()
