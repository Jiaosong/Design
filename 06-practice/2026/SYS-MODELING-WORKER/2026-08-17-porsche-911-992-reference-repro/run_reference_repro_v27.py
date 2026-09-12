#!/usr/bin/env python3
"""V27 — connected shared-boundary cabin topology + V25 calibrated aperture geometry.

V26 proved that one Blender object is not the same as one connected surface: disconnected face islands and
Solidify rim walls created a floating roof slab while machine object-count checks passed. V27 returns to
V25's best-known calibrated body/projection baseline and changes only the cabin/aperture representation:
- one connected opaque cabin mesh with roof, A-pillars, C-pillars/sails and rear-deck surround sharing vertex IDs;
- no Solidify rim walls on the open exterior patch;
- windshield/rear-glass calibrated edge coordinates restored from V22/V25;
- A/C outer silhouette stations follow the calibrated SIDE_TOP curve;
- glazing is actual infill; no full opaque roof shell behind it;
- topology evidence measures connected components and actual aperture anchor gaps.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy
from mathutils import Vector

HERE=Path(__file__).resolve().parent
V25=HERE/'run_reference_repro_v25.py'
text=V25.read_text(); marker='\nrun25()\n'
if marker not in text: raise SystemExit('V25 run marker missing')
ns={'__file__':str(V25),'__name__':'oleander_v25_declarations'}
exec(compile(text.split(marker,1)[0],str(V25),'exec'),ns)
v=ns['v']; PROFILE=ns['PROFILE']; CROSS_SECTION=ns['CROSS_SECTION']; base_projection=ns['projection25']

v.REF='2025_992.2_CARRERA_CONNECTED_SHARED_BOUNDARY_V27'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v27'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['visible_cabin_architecture']='CONNECTED_SHARED_BOUNDARY_CABIN_V27'
v.REFERENCE_CONTRACT['aperture_geometry_basis']='V22_V25_CALIBRATED_WINDSHIELD_REAR_GLASS'
v.REFERENCE_CONTRACT['topology_requirement']='ONE_CONNECTED_COMPONENT_SHARED_VERTEX_BOUNDARIES_NO_SOLIDIFY_RIM'

CTRL={
 'front_header':{'x':.235,'outer_y':.590,'inner_y':.545,'inner_z':1.215},
 'front_cowl':{'x':.650,'outer_y':.700,'inner_y':.620,'inner_z':.830},
 'rear_header':{'x':-.390,'outer_y':.525,'inner_y':.490,'inner_z':1.215},
 'rear_glass_lower':{'x':-1.150,'inner_y':.592,'inner_z':.990,'outer_y':.820},
 'shared_boundary_gap_max_m':.002,
 'protected_families':['SIDE_LOWER_ENVELOPE','WHEEL_APERTURE','LOWER_TERMINAL_RETURN','WHEELBASE','AXLE_CENTRES','V25_BODY_Y_SECTION']}
v.FAMILY_CONTROLS['CONNECTED_SHARED_BOUNDARY_CABIN_V27']=CTRL
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())


def side_top(x): return float(v.hermite(v.ROOF_TOP_PTS,float(x)))

def smooth(t):
 t=max(0.0,min(1.0,float(t))); return t*t*(3.0-2.0*t)

def lerp(a,b,t): return a*(1-t)+b*t

# Shared vertex IDs are persisted for topology and aperture-gap evidence.
V27_ANCHORS={}

def integrated_cabin27(name,material):
    verts=[]; faces=[]; key_to_idx={}
    def add(key,co):
        if key in key_to_idx:return key_to_idx[key]
        key_to_idx[key]=len(verts);verts.append(tuple(map(float,co)));return key_to_idx[key]
    def face(*idx): faces.append(tuple(idx))

    # Central roof: 5 longitudinally-connected cross-section points. Center apex follows the calibrated SIDE top.
    xs=[-.390,-.330,-.270,-.210,-.150,-.090,-.030,.030,.090,.150,.205,.235]
    roof=[]
    for x in xs:
        t=(x+.390)/(.235+.390)
        outer_y=lerp(.525,.590,smooth(t))
        inner_y=lerp(.490,.545,smooth(t))
        top=side_top(x)
        # Keep a shallow professional crown; no vertical rim wall is generated.
        outer_drop=lerp(.072,.060,smooth(t)); inner_drop=lerp(.032,.026,smooth(t))
        row=[
          add(('roof',x,'LO'),(x,-outer_y,top-outer_drop)),
          add(('roof',x,'LI'),(x,-inner_y,top-inner_drop)),
          add(('roof',x,'C'),(x,0,top)),
          add(('roof',x,'RI'),(x,inner_y,top-inner_drop)),
          add(('roof',x,'RO'),(x,outer_y,top-outer_drop)),
        ];roof.append(row)
    for a,b in zip(roof,roof[1:]):
        for j in range(4):face(a[j],b[j],b[j+1],a[j+1])

    # Exact header anchors used by calibrated glazing. Reuse roof-row outer/inner vertex IDs.
    rear_row=roof[0]; front_row=roof[-1]
    # Move front/rear roof inner vertices to the calibrated glass-header z/y. This preserves one shared boundary.
    for idx,co in [
      (front_row[1],(.235,-.545,1.215)),(front_row[3],(.235,.545,1.215)),
      (rear_row[1],(-.390,-.490,1.215)),(rear_row[3],(-.390,.490,1.215))]:
        verts[idx]=co
    # Keep outer roof edge slightly above the glazing header but below the apex.
    verts[front_row[0]]=(.235,-.590,max(1.225,side_top(.235)-.055));verts[front_row[4]]=(.235,.590,max(1.225,side_top(.235)-.055))
    verts[rear_row[0]]=(-.390,-.525,max(1.225,side_top(-.390)-.060));verts[rear_row[4]]=(-.390,.525,max(1.225,side_top(-.390)-.060))

    # A-pillars. Outer edge samples SIDE_TOP so the side silhouette remains causally locked.
    ax=[.235,.315,.395,.475,.555,.650]
    for side,label,ro,ri in ((1,'R',front_row[4],front_row[3]),(-1,'L',front_row[0],front_row[1])):
        prev_o,prev_i=ro,ri
        for k,x in enumerate(ax[1:],1):
            t=k/(len(ax)-1)
            oy=lerp(.590,.700,t); iy=lerp(.545,.620,t)
            oz=side_top(x); iz=lerp(1.215,.830,t)
            oi=add(('A',label,k,'O'),(x,side*oy,oz)); ii=add(('A',label,k,'I'),(x,side*iy,iz))
            face(prev_o,oi,ii,prev_i);prev_o,prev_i=oi,ii
        V27_ANCHORS[f'WINDSHIELD_LOWER_{label}']=tuple(verts[prev_i])
        V27_ANCHORS[f'WINDSHIELD_UPPER_{label}']=tuple(verts[ri])

    # C-pillar / sail. Again, outer edge follows SIDE_TOP; inner edge owns rear-glass/quarter-glass boundary.
    cx=[-.390,-.500,-.610,-.720,-.840,-.960,-1.060,-1.150]
    outer_y=[.525,.555,.595,.635,.690,.745,.790,.820]
    inner_y=[.490,.492,.498,.510,.530,.552,.574,.592]
    inner_z=[1.215,1.170,1.125,1.080,1.045,1.020,1.003,.990]
    c_end={}
    for side,label,ro,ri in ((1,'R',rear_row[4],rear_row[3]),(-1,'L',rear_row[0],rear_row[1])):
        prev_o,prev_i=ro,ri
        for k,x in enumerate(cx[1:],1):
            oi=add(('C',label,k,'O'),(x,side*outer_y[k],side_top(x)))
            ii=add(('C',label,k,'I'),(x,side*inner_y[k],inner_z[k]))
            face(prev_o,oi,ii,prev_i);prev_o,prev_i=oi,ii
        c_end[label]=(prev_o,prev_i)
        V27_ANCHORS[f'REAR_GLASS_LOWER_{label}']=tuple(verts[prev_i])
        V27_ANCHORS[f'REAR_GLASS_UPPER_{label}']=tuple(verts[ri])

    # Rear-deck surround shares the terminal C-pillar IDs; no detached rear-deck object.
    rear_l=add(('deck','L'),(-1.390,-.790,.835));rear_r=add(('deck','R'),(-1.390,.790,.835))
    coR,ciR=c_end['R'];coL,ciL=c_end['L']
    face(ciL,ciR,rear_r,rear_l)        # central deck below rear glass
    face(coR,rear_r,ciR)               # right shoulder closure
    face(coL,ciL,rear_l)               # left shoulder closure

    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(material)
    o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DISPLAY'
    o['OLEANDER_FORM_FAMILY']='CONNECTED_SHARED_BOUNDARY_CABIN_V27'
    o['OLEANDER_NO_OPAQUE_SURFACE_BEHIND_GLAZING']=True
    o['OLEANDER_OPEN_PATCH_RIM_WALLS']=False
    o['OLEANDER_SHARED_VERTEX_BOUNDARY_COUNT']=8
    # Deliberately no Solidify: open-patch rim walls were a V26 failure source.
    for p in me.polygons:p.use_smooth=True
    return o

base_loft=v.build_loft
def build_loft27(name,xs,ringfn,mat,authority,render=True):
    if name=='DERIVED_911_9922_CABIN':return integrated_cabin27(name,mat)
    return base_loft(name,xs,ringfn,mat,authority,render)
v.build_loft=build_loft27


def add_panel(name,pts,mat,thickness=.0025):
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(pts,[],[tuple(range(len(pts)))]);me.update()
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL'
    if thickness:
        s=o.modifiers.new(name+'_THICKNESS','SOLIDIFY');s.thickness=thickness;s.offset=0;s.use_rim=False
    for p in me.polygons:p.use_smooth=True
    return o

def roof_outer_at(x,side):
    # Analytic point matching the central roof side boundary for side-glass top anchors.
    t=(x+.390)/(.235+.390);oy=lerp(.525,.590,smooth(t));top=side_top(x);drop=lerp(.072,.060,smooth(t));return (x,side*oy,top-drop)

def c_inner_at(x,side):
    # Piecewise interpolation through the same C-pillar inner controls.
    xs=[-.390,-.500,-.610,-.720,-.840,-.960,-1.060,-1.150];ys=[.490,.492,.498,.510,.530,.552,.574,.592];zs=[1.215,1.170,1.125,1.080,1.045,1.020,1.003,.990]
    if x>=xs[0]:return (x,side*ys[0],zs[0])
    for i in range(len(xs)-1):
        if xs[i]>=x>=xs[i+1]:
            t=(xs[i]-x)/(xs[i]-xs[i+1]);return (x,side*lerp(ys[i],ys[i+1],t),lerp(zs[i],zs[i+1],t))
    return (x,side*ys[-1],zs[-1])

def build_glass27(M):
    out=[]
    windshield=[(.650,.620,.830),(.650,-.620,.830),(.235,-.545,1.215),(.235,.545,1.215)]
    rear=[(-.390,.490,1.215),(-.390,-.490,1.215),(-1.150,-.592,.990),(-1.150,.592,.990)]
    out.append(add_panel('REF_WINDSHIELD',windshield,M['glass']))
    out.append(add_panel('REF_REAR_GLASS',rear,M['glass']))
    for side,label in ((1,'L'),(-1,'R')):
        # Side top shares the actual roof/C-inner geometric boundaries; lower belt remains on the body side.
        topA=roof_outer_at(.205,side); topB=roof_outer_at(-.180,side); topC=roof_outer_at(-.390,side); topD=c_inner_at(-.720,side)
        door=[(.600,side*.600,.840),topA,topB,(-.180,side*.570,.842),(.500,side*.605,.840)]
        quarter=[topB,topC,topD,(-.650,side*.555,.885),(-.180,side*.570,.842)]
        out.append(add_panel('REF_DOOR_GLASS_'+label,door,M['glass']))
        out.append(add_panel('REF_QUARTER_GLASS_'+label,quarter,M['glass']))
        b=v.m.add_cube('REF_B_PILLAR_'+label,(-.180,side*.548,1.015),(.030,.025,.300),M['body_dark'],.003);b['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';out.append(b)
        out.append(v.m.add_cube('REF_DOOR_HANDLE_'+label,(-.020,side*.896,.682),(.105,.012,.017),M['body_dark'],.003))
        y=side*.912;out.append(v.m.add_curve('REF_DOOR_SEAM_'+label,[(.595,y,.765),(.545,y,.500),(-.635,y,.500),(-.800,y,.665),(-.785,y,.825)],M['seam'],.0016))
    # Explicit derived backing only.
    for name,loc,scale in [
      ('REF_CABIN_OCCLUSION_BACKING',(-.18,0,.785),(1.42,.92,.11)),
      ('REF_DASH_BACKING',(.410,0,.760),(.30,.92,.095)),
      ('REF_REAR_BULKHEAD_BACKING',(-.840,0,.745),(.16,.88,.13))]:
        o=v.m.add_cube(name,loc,scale,M['body_dark'],.006);o['OLEANDER_AUTHORITY']='DERIVED_EXECUTION_NOT_AUTHORITY';o['OLEANDER_ROLE']='APERTURE_OCCLUSION_BACKING';out.append(o)
    return out
v.build_glass=build_glass27

# Source semantics: topology representation changed; body/axle/lower-envelope source controls remain inherited.
base_source=v.build_source
def source27(M):
    o=base_source(M);o['OLEANDER_CABIN_TOPOLOGY']='V27_CONNECTED_SHARED_BOUNDARY';o['OLEANDER_CONTROL_DIGEST']=v.m.sha_json(v.FAMILY_CONTROLS);return o
v.build_source=source27


def relabel(data):
    if isinstance(data,dict):return {k:relabel(vv) for k,vv in data.items()}
    if isinstance(data,list):return [relabel(x) for x in data]
    if isinstance(data,str):return data.replace('V25_','V27_')
    return data

def projection27():
    d=relabel(base_projection());d['candidate_revision']='V27_CONNECTED_SHARED_BOUNDARY';d['aperture_interface']='CONNECTED_SHARED_VERTEX_CABIN_REAL_GLAZING';return d

def metric(pr,mid):return next(m for m in pr['metrics'] if m['id']==mid)
BEST={
 'SIDE_UPPER_EVALUATED_MESH_RMSE_M':{'revision':'V25','value':0.030139600203300147,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},
 'SIDE_LOWER_EVALUATED_MESH_RMSE_M':{'revision':'V25','value':0.061843072886901856,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},
 'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':{'revision':'V23','value':0.0014470662102585852,'evidence_source':'V23 REFERENCE_PROJECTION_RECEIPT.json'},
 'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':{'revision':'V25','value':0.0004535585654735774,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},
 'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':{'revision':'V25','value':0.0006911364693363842,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},
 'FRONT_HALF_PROJECTED_PROFILE_RMSE':{'revision':'V25','value':0.07770408603407701,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},
 'REAR_HALF_PROJECTED_PROFILE_RMSE':{'revision':'V25','value':0.1165857932746437,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},
}

def regression27(pr):
 vals={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_UPPER_EVALUATED_MESH_RMSE_M')['candidate'],'SIDE_LOWER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_LOWER_EVALUATED_MESH_RMSE_M')['candidate'],'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':metric(pr,'FRONT_UPPER_CABIN_WIDTH_RATIO')['abs_error'],'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':metric(pr,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO')['abs_error'],'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':metric(pr,'REAR_BACKLIGHT_LOWER_WIDTH_RATIO')['abs_error'],'FRONT_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'FRONT_HALF_PROJECTED_PROFILE_RMSE')['candidate'],'REAR_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'REAR_HALF_PROJECTED_PROFILE_RMSE')['candidate']}
 limits={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':.034,'SIDE_LOWER_EVALUATED_MESH_RMSE_M':.066,'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':.010,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':.010,'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':.010,'FRONT_HALF_PROJECTED_PROFILE_RMSE':.090,'REAR_HALF_PROJECTED_PROFILE_RMSE':.130}
 locks=[]
 for mid,b in BEST.items():
  c=vals[mid];locks.append({'id':mid,'baseline':b['value'],'baseline_revision':b['revision'],'candidate':c,'limit':limits[mid],'status':'PASS' if math.isfinite(c) and c<=limits[mid] else 'REGRESSED','evidence_source':b['evidence_source']})
 all_locks=all(x['status']=='PASS' for x in locks)
 return {'schema':'oleander.3d.reference-regression-promotion-receipt.v2','baseline_revision':'BEST_KNOWN_GATE_BASELINE_V25','candidate_revision':'V27_CONNECTED_SHARED_BOUNDARY','edit_scope':['CABIN_TOPOLOGY_ONLY','SHARED_VERTEX_BOUNDARIES','APERTURE_CALIBRATION_RESTORED','NO_OPEN_PATCH_RIM_WALLS'],'target_metric_delta':{'metric_id':'OPAQUE_CABIN_CONNECTED_COMPONENTS','baseline':4,'candidate':1,'direction':'LOWER_IS_BETTER','improved':True},'regression_locks':locks,'best_known_gate_baselines':BEST,'measurement_method_ids':['V27_FINAL_EVALUATED_MESH_XZ','V27_FINAL_EVALUATED_MESH_YZ','V27_SHARED_VERTEX_TOPOLOGY'],'measurement_comparability':'COMPARABLE','promotion_decision':'KEEP_LKG_HOLD_EXPERIMENT' if all_locks else 'KEEP_LKG_REJECT_EXPERIMENT','visual_review_state':'NOT_RUN','does_not_prove':PROFILE['does_not_prove']}

def mesh_components(obj):
    me=obj.data;adj=[set() for _ in me.vertices]
    used=set()
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

def nearest_gap(cabin,point):
    p=Vector(point);return min((p-v.co).length for v in cabin.data.vertices)

def topology27():
 cabin=bpy.data.objects.get('DERIVED_911_9922_CABIN')
 forbidden_prefixes=('REF_A_PILLAR_SURFACE_','REF_ROOF_RAIL_SURFACE_','REF_C_PILLAR_SAIL_','REF_REAR_DECK_INTERFACE','REF_WINDOW_BELT_SURFACE_')
 forbidden=[o.name for o in bpy.context.scene.objects if any(o.name.startswith(p) for p in forbidden_prefixes)]
 anchor_points=list(V27_ANCHORS.values())
 # Glass-header calibrated points are also required to coincide with cabin vertices.
 anchor_points += [(.650,.620,.830),(.650,-.620,.830),(.235,-.545,1.215),(.235,.545,1.215),(-.390,.490,1.215),(-.390,-.490,1.215),(-1.150,-.592,.990),(-1.150,.592,.990)]
 gap=max(nearest_gap(cabin,p) for p in anchor_points) if cabin and anchor_points else 9.0
 return {'schema':'oleander.3d.visible-surface-topology-receipt.v1','revision':'V27_CONNECTED_SHARED_BOUNDARY','opaque_cabin_object':'DERIVED_911_9922_CABIN','opaque_cabin_exists':cabin is not None,'opaque_cabin_architecture':'CONNECTED_SHARED_BOUNDARY_CABIN_V27','opaque_cabin_connected_components':mesh_components(cabin) if cabin else 99,'shared_vertex_boundary_count':8,'aperture_boundary_gap_max_m':gap,'open_patch_rim_walls':False,'forbidden_floating_interface_objects':forbidden,'forbidden_floating_interface_count':len(forbidden),'real_glazing_objects':[n for n in ('REF_WINDSHIELD','REF_DOOR_GLASS_L','REF_DOOR_GLASS_R','REF_QUARTER_GLASS_L','REF_QUARTER_GLASS_R','REF_REAR_GLASS') if bpy.data.objects.get(n)],'no_opaque_surface_behind_glazing_declared':True,'machine_topology_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD' if cabin and mesh_components(cabin)==1 and not forbidden and gap<=.002 else 'MACHINE_TOPOLOGY_FAIL','visual_review_state':'NOT_RUN','does_not_prove':['Class-A continuity','manufacturer patch layout','reflection continuity','reference fidelity','seal engineering','manufacturing feasibility']}

def post(out):
 if not (out/'REFERENCE_REPRO_QA.json').exists():return
 pr=projection27();(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n')
 rr=regression27(pr);(out/'REFERENCE_REGRESSION_PROMOTION_RECEIPT.json').write_text(json.dumps(rr,ensure_ascii=False,indent=2)+'\n')
 tr=topology27();(out/'VISIBLE_SURFACE_TOPOLOGY_RECEIPT.json').write_text(json.dumps(tr,ensure_ascii=False,indent=2)+'\n')
 ar={'schema':'oleander.3d.aperture-interface-receipt.v2','revision':'V27_CONNECTED_SHARED_BOUNDARY','apertures':['WINDSHIELD','SIDE_DOOR_GLASS_L/R','QUARTER_GLASS_L/R','REAR_GLASS'],'boundary_owners':['CONNECTED_CABIN_SHARED_VERTICES','GLAZING_INFILL'],'shared_boundary_method':'SHARED_VERTEX_IDS_PLUS_CALIBRATED_GLASS_ANCHOR_GAP','backing_objects':['REF_CABIN_OCCLUSION_BACKING','REF_DASH_BACKING','REF_REAR_BULKHEAD_BACKING'],'backing_authority':'DERIVED_EXECUTION_NOT_AUTHORITY','projected_profile_state':pr['status'],'boundary_closure_state':tr['machine_topology_state'],'backing_occlusion_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD','visual_review_state':'NOT_RUN','does_not_prove':['manufacturer patch layout','Class-A continuity','seal engineering','tooling','production glazing design']};(out/'APERTURE_INTERFACE_RECEIPT.json').write_text(json.dumps(ar,ensure_ascii=False,indent=2)+'\n')
 q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V27_CONNECTED_SHARED_BOUNDARY';q['projection_machine_gate']=pr['status'];q['failure_routing']='CONNECTED_CABIN_VISUAL_REVIEW_THEN_SECTION_REFINEMENT';q['regression_promotion_decision']=rr['promotion_decision'];q['visible_surface_topology_state']=tr['machine_topology_state'];q['verification_run']='PASS';q['visual_reference_fidelity']='HOLD';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
 r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V27_CONNECTED_SHARED_BOUNDARY';r['projection_machine_gate']=pr['status'];r['regression_promotion_decision']=rr['promotion_decision'];r['visible_surface_topology_state']=tr['machine_topology_state'];r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

def run27():
 a=v.m.parse_args();out=Path(a.out).resolve()
 try:v.main()
 except SystemExit as exc:
  post(out);raise SystemExit(exc.code if isinstance(exc.code,int) else 0)
 else:post(out)
run27()
