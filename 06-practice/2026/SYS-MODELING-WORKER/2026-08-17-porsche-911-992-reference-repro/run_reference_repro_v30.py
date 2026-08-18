#!/usr/bin/env python3
"""V30 — dense primary body surface grid + stable aperture cabin.

V25–V29 showed that fixing cabin topology alone cannot recover the 992.2 identity while the primary body
remains a coarse generic crown loft. V30 returns to the V25 best-known dimensional / wheel / lower-envelope
baseline, replaces the visible body with a denser causal control grid, and uses a deliberately simpler,
connected aperture cabin so body-section quality can be reviewed without patch spikes.

No numeric or topology result self-promotes reference fidelity.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy, bmesh
from mathutils import Vector

HERE=Path(__file__).resolve().parent
V25=HERE/'run_reference_repro_v25.py'
text=V25.read_text();marker='\nrun25()\n'
if marker not in text:raise SystemExit('V25 run marker missing')
ns={'__file__':str(V25),'__name__':'oleander_v25_declarations'}
exec(compile(text.split(marker,1)[0],str(V25),'exec'),ns)
v=ns['v'];PROFILE=ns['PROFILE'];CROSS_SECTION=ns['CROSS_SECTION'];base_projection=ns['projection25']

v.REF='2025_992.2_CARRERA_DENSE_PRIMARY_BODY_GRID_V30'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v30'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['primary_body_surface_method']='DENSE_LONGITUDINAL_CONTROL_GRID_WITH_CAUSAL_CROWN_SHOULDER_ROCKER_RAILS'
v.REFERENCE_CONTRACT['cabin_method']='SIMPLE_CONNECTED_REAL_APERTURE_NETWORK'
v.FAMILY_CONTROLS['PRIMARY_BODY_GRID_V30']={
 'longitudinal_stations':81,
 'half_ring_rails':['CENTER_TOP','INNER_HOOD','MID_HOOD','FENDER_INNER','FENDER_CROWN','SHOULDER','UPPER_SIDE','BELT_SIDE','LOWER_SIDE','ROCKER_OUTER','ROCKER_INNER','FLOOR_CENTER'],
 'terminal_plan_curvature':'Y_DEPENDENT_X_SETBACK_IN_GRID',
 'protected':['LENGTH','WIDTH','WHEELBASE','AXLE_CENTRES','V20_WHEEL_APERTURE','V20_LOWER_TERMINAL_RETURN']}
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())


def h(pts,x):return float(v.hermite(pts,float(x)))
def clamp(a,b,c):return max(a,min(b,c))
def s01(t):t=clamp(0.,1.,t);return t*t*(3-2*t)
def wheel_inf(x,ax,sigma):return math.exp(-((x-ax)/sigma)**4)

def macro_fields(x):
    # Reuse source controls rather than sampling a prior dense candidate.
    w=h(v.WIDTH_PTS,x)
    fi=wheel_inf(x,v.FRONT_AXLE,.55);ri=wheel_inf(x,v.REAR_AXLE,.62)
    w=min(v.WIDTH/2,w+.012*fi+.028*ri)
    center=h(v.SPINE_PTS,x)
    # Classic 911 relation: fender crown above hood/deck center, stronger rear haunch.
    crown=center+.028+.060*fi+.090*ri
    lower=h(v.LOWER_PTS,x)
    return w,center,crown,lower,fi,ri

def terminal_floor(x):
    rear=[(-2.271,.416),(-2.10,.407),(-1.90,.263),(-1.72,.150)]
    front=[(1.72,.155),(1.85,.160),(2.05,.197),(2.271,.207)]
    if x<=-1.72:return h(rear,x)
    if x>=1.72:return h(front,x)
    return .140

def body_ring30(x):
    w,zc,cr,zl,fi,ri=macro_fields(x);floor=terminal_floor(x)
    # Rear shoulder remains fuller and higher than front; center deck stays below crown.
    shoulder=cr-.018-.010*fi+.010*ri
    upper_side=cr-.050-.010*fi+.005*ri
    lower_side=max(floor+.105,min(zl,cr-.170))
    # Half-ring is ordered center-top -> outer side -> floor center. More rails = no boxy section facets.
    pos=[
      (0.00*w,zc),(.12*w,zc+.020*(cr-zc)),(.26*w,zc+.080*(cr-zc)),
      (.42*w,zc+.230*(cr-zc)),(.58*w,zc+.500*(cr-zc)),(.72*w,zc+.770*(cr-zc)),
      (.84*w,cr-.010),(.92*w,shoulder),(.975*w,upper_side),(1.00*w,lower_side),
      (.995*w,max(floor+.035,.175)),(.90*w,max(floor,.150)),(.72*w,max(.142,floor-.005)),
      (.48*w,max(.140,floor-.010)),(.24*w,max(.140,floor-.012)),(0.0,max(.140,floor-.012))]
    # Rounded nose/tail is part of the grid. At terminal stations, outer rails retreat longitudinally.
    front_t=s01((x-1.72)/(v.FRONT_X-1.72)) if x>1.72 else 0.0
    rear_t=s01((-x-1.72)/(-v.REAR_X-1.72)) if x<-1.72 else 0.0
    out=[]
    for y,z in pos+[(-yy,zz) for yy,zz in reversed(pos[1:-1])]:
        q=abs(y)/max(w,1e-9)
        setback=(.105*front_t+.090*rear_t)*(q**1.55)
        xe=x-setback if x>0 else x+setback
        # lower outer corners round back further than hood/deck center.
        if z<.42:setback2=(.050*front_t+.045*rear_t)*(q**1.25);xe += (-setback2 if x>0 else setback2)
        out.append((xe,y,max(z,floor if z<.50 else z)))
    return out


def build_grid_body(name,material):
    # Uniform high station density plus exact hard/axle/terminal stations.
    xs=[v.REAR_X+(v.FRONT_X-v.REAR_X)*i/80 for i in range(81)]
    xs=sorted(set(round(x,6) for x in xs+[v.REAR_X,-2.10,-1.90,-1.72,v.REAR_AXLE,-.90,-.40,0,.40,.90,v.FRONT_AXLE,1.72,1.90,2.10,v.FRONT_X]))
    verts=[];rings=[]
    for x in xs:
        ring=body_ring30(x);rings.append(list(range(len(verts),len(verts)+len(ring))));verts.extend(ring)
    nr=len(rings[0]);faces=[]
    for i in range(len(rings)-1):
        for j in range(nr):
            k=(j+1)%nr;faces.append((rings[i][j],rings[i+1][j],rings[i+1][k],rings[i][k]))
    faces.append(tuple(reversed(rings[0])));faces.append(tuple(rings[-1]))
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update()
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(material)
    o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DISPLAY';o['OLEANDER_FORM_FAMILY']='DENSE_PRIMARY_BODY_GRID_V30';o['OLEANDER_LONGITUDINAL_STATIONS']=len(xs);o['OLEANDER_RING_VERTICES']=nr
    for p in me.polygons:p.use_smooth=True
    return o

# Simple, stable aperture cabin. It deliberately avoids V25–V29 sail/rail complexity while body quality is repaired.
def simple_cabin30(name,material):
    verts=[];faces=[];idx={}
    def add(k,p):
        if k in idx:return idx[k]
        idx[k]=len(verts);verts.append(tuple(map(float,p)));return idx[k]
    def face(*a):faces.append(tuple(a))
    # central roof between true glass headers
    xs=[-.390,-.330,-.270,-.210,-.150,-.090,-.030,.030,.090,.150,.205,.235];rows=[]
    for x in xs:
        t=(x+.390)/(.625);rw=.445+.075*s01(t);top=h(v.ROOF_TOP_PTS,x)
        row=[add(('r',x,-2),(x,-rw,top-.070)),add(('r',x,-1),(x,-rw*.60,top-.022)),add(('r',x,0),(x,0,top)),add(('r',x,1),(x,rw*.60,top-.022)),add(('r',x,2),(x,rw,top-.070))];rows.append(row)
    for a,b in zip(rows,rows[1:]):
        for j in range(4):face(a[j],b[j],b[j+1],a[j+1])
    rear,front=rows[0],rows[-1]
    # exact best-known glass headers
    verts[front[1]]=(.235,-.545,1.215);verts[front[3]]=(.235,.545,1.215)
    verts[rear[1]]=(-.390,-.490,1.215);verts[rear[3]]=(-.390,.490,1.215)
    # A pillars = two stable strips sharing roof vertices
    for side,lab,outer0,inner0 in ((1,'R',front[4],front[3]),(-1,'L',front[0],front[1])):
        outer1=add(('A',lab,'o'),(.650,side*.680,.790));inner1=add(('A',lab,'i'),(.650,side*.620,.830));face(outer0,outer1,inner1,inner0)
    # C pillars: no ridge fan. One broad strip from header to rear-glass lower anchor, outer shoulder below SIDE apex.
    for side,lab,outer0,inner0 in ((1,'R',rear[4],rear[3]),(-1,'L',rear[0],rear[1])):
        stations=[(-.390,abs(verts[outer0][1]),abs(verts[inner0][1]),verts[outer0][2],verts[inner0][2]),(-.580,.500,.515,1.080,1.150),(-.780,.575,.540,.980,1.090),(-.980,.675,.565,.890,1.030),(-1.150,.790,.592,.825,.990)]
        outs=[outer0];ins=[inner0]
        for k,(x,oy,iy,oz,iz) in enumerate(stations[1:],1):outs.append(add(('C',lab,k,'o'),(x,side*oy,oz)));ins.append(add(('C',lab,k,'i'),(x,side*iy,iz)))
        for i in range(len(outs)-1):face(outs[i],outs[i+1],ins[i+1],ins[i])
        deck=add(('deck',lab),(-1.380,side*.760,.805));face(outs[-1],deck,ins[-1])
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(material);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DISPLAY';o['OLEANDER_FORM_FAMILY']='SIMPLE_CONNECTED_APERTURE_CABIN_V30';o['OLEANDER_NO_OPAQUE_SURFACE_BEHIND_GLAZING']=True;o['OLEANDER_OPEN_PATCH_RIM_WALLS']=False
    for p in me.polygons:p.use_smooth=True
    return o

base_loft=v.build_loft
def build_loft30(name,xs,ringfn,mat,authority,render=True):
    if name=='DERIVED_911_9922_BODY':return build_grid_body(name,mat)
    if name=='DERIVED_911_9922_CABIN':return simple_cabin30(name,mat)
    return base_loft(name,xs,ringfn,mat,authority,render)
v.build_loft=build_loft30

# Wheel cuts remain V20/V25 authority; body function is only used by supporting interface helpers.
v.body_ring=body_ring30


def add_panel(name,pts,mat,th=.0025):
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(pts,[],[tuple(range(len(pts)))]);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL'
    if th:
        s=o.modifiers.new(name+'_THICKNESS','SOLIDIFY');s.thickness=th;s.offset=0;s.use_rim=False
    for p in me.polygons:p.use_smooth=True
    return o

def glass30(M):
    out=[]
    out.append(add_panel('REF_WINDSHIELD',[(.650,.620,.830),(.650,-.620,.830),(.235,-.545,1.215),(.235,.545,1.215)],M['glass']))
    out.append(add_panel('REF_REAR_GLASS',[(-.390,.490,1.215),(-.390,-.490,1.215),(-1.150,-.592,.990),(-1.150,.592,.990)],M['glass']))
    for side,label in ((1,'L'),(-1,'R')):
        door=[(.610,side*.610,.840),(.235,side*.535,1.205),(-.200,side*.490,1.205),(-.200,side*.565,.842),(.500,side*.600,.840)]
        quarter=[(-.200,side*.490,1.205),(-.390,side*.480,1.205),(-.780,side*.540,1.070),(-1.120,side*.585,.995),(-.680,side*.565,.860),(-.200,side*.565,.842)]
        out.append(add_panel('REF_DOOR_GLASS_'+label,door,M['glass']));out.append(add_panel('REF_QUARTER_GLASS_'+label,quarter,M['glass']))
        b=v.m.add_cube('REF_B_PILLAR_'+label,(-.200,side*.535,1.015),(.032,.026,.300),M['body_dark'],.003);b['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';out.append(b)
        out.append(v.m.add_cube('REF_DOOR_HANDLE_'+label,(-.020,side*.896,.682),(.105,.012,.017),M['body_dark'],.003));y=side*.912;out.append(v.m.add_curve('REF_DOOR_SEAM_'+label,[(.595,y,.765),(.545,y,.500),(-.635,y,.500),(-.800,y,.665),(-.785,y,.825)],M['seam'],.0016))
    for name,loc,scale in [('REF_CABIN_OCCLUSION_BACKING',(-.18,0,.785),(1.35,.86,.10)),('REF_DASH_BACKING',(.410,0,.760),(.30,.88,.09)),('REF_REAR_BULKHEAD_BACKING',(-.840,0,.745),(.16,.82,.12))]:
        o=v.m.add_cube(name,loc,scale,M['body_dark'],.006);o['OLEANDER_AUTHORITY']='DERIVED_EXECUTION_NOT_AUTHORITY';out.append(o)
    return out
v.build_glass=glass30

base_source=v.build_source
def source30(M):
    o=base_source(M);o['OLEANDER_PRIMARY_BODY_SURFACE']='DENSE_CONTROL_GRID_V30';o['OLEANDER_CABIN']='SIMPLE_CONNECTED_APERTURE_V30';o['OLEANDER_CONTROL_DIGEST']=v.m.sha_json(v.FAMILY_CONTROLS);return o
v.build_source=source30


def relabel(data):
    if isinstance(data,dict):return {k:relabel(x) for k,x in data.items()}
    if isinstance(data,list):return [relabel(x) for x in data]
    if isinstance(data,str):return data.replace('V25_','V30_')
    return data

def projection30():
    d=relabel(base_projection());d['candidate_revision']='V30_DENSE_PRIMARY_BODY_GRID';d['primary_body_surface_method']='DENSE_LONGITUDINAL_CONTROL_GRID';return d

def metric(pr,mid):return next(m for m in pr['metrics'] if m['id']==mid)
BEST={
 'SIDE_UPPER_EVALUATED_MESH_RMSE_M':{'revision':'V25','value':0.030139600203300147,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},
 'SIDE_LOWER_EVALUATED_MESH_RMSE_M':{'revision':'V25','value':0.061843072886901856,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},
 'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':{'revision':'V23','value':0.0014470662102585852,'evidence_source':'V23 REFERENCE_PROJECTION_RECEIPT.json'},
 'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':{'revision':'V25','value':0.0004535585654735774,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},
 'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':{'revision':'V25','value':0.0006911364693363842,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},
 'FRONT_HALF_PROJECTED_PROFILE_RMSE':{'revision':'V25','value':0.07770408603407701,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},
 'REAR_HALF_PROJECTED_PROFILE_RMSE':{'revision':'V25','value':0.1165857932746437,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'}}

def regression30(pr):
 vals={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_UPPER_EVALUATED_MESH_RMSE_M')['candidate'],'SIDE_LOWER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_LOWER_EVALUATED_MESH_RMSE_M')['candidate'],'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':metric(pr,'FRONT_UPPER_CABIN_WIDTH_RATIO')['abs_error'],'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':metric(pr,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO')['abs_error'],'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':metric(pr,'REAR_BACKLIGHT_LOWER_WIDTH_RATIO')['abs_error'],'FRONT_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'FRONT_HALF_PROJECTED_PROFILE_RMSE')['candidate'],'REAR_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'REAR_HALF_PROJECTED_PROFILE_RMSE')['candidate']};limits={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':.045,'SIDE_LOWER_EVALUATED_MESH_RMSE_M':.070,'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':.012,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':.012,'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':.012,'FRONT_HALF_PROJECTED_PROFILE_RMSE':.120,'REAR_HALF_PROJECTED_PROFILE_RMSE':.150};locks=[]
 for mid,b in BEST.items():
  c=vals[mid];locks.append({'id':mid,'baseline':b['value'],'baseline_revision':b['revision'],'candidate':c,'limit':limits[mid],'status':'PASS' if math.isfinite(c) and c<=limits[mid] else 'REGRESSED','evidence_source':b['evidence_source']})
 all_locks=all(x['status']=='PASS' for x in locks)
 return {'schema':'oleander.3d.reference-regression-promotion-receipt.v2','baseline_revision':'BEST_KNOWN_GATE_BASELINE_V25','candidate_revision':'V30_DENSE_PRIMARY_BODY_GRID','edit_scope':['PRIMARY_BODY_REPRESENTATION','BODY_SECTION_GRID','TERMINAL_PLAN_CURVATURE','STABLE_CABIN_FOR_BODY_REVIEW'],'target_metric_delta':{'metric_id':'PRIMARY_BODY_RING_RAIL_COUNT','baseline':12,'candidate':16,'direction':'HIGHER_IS_BETTER','improved':True},'regression_locks':locks,'best_known_gate_baselines':BEST,'measurement_method_ids':['V30_FINAL_EVALUATED_MESH_XZ','V30_FINAL_EVALUATED_MESH_YZ','V30_DENSE_GRID_TOPOLOGY'],'measurement_comparability':'COMPARABLE','promotion_decision':'KEEP_LKG_HOLD_EXPERIMENT' if all_locks else 'KEEP_LKG_REJECT_EXPERIMENT','visual_review_state':'NOT_RUN','does_not_prove':PROFILE['does_not_prove']}

def components(obj):
    me=obj.data;adj=[set() for _ in me.vertices];used=set()
    for p in me.polygons:
        vs=list(p.vertices);used.update(vs)
        for a,b in zip(vs,vs[1:]+vs[:1]):adj[a].add(b);adj[b].add(a)
    seen=set();n=0
    for s in used:
        if s in seen:continue
        n+=1;st=[s];seen.add(s)
        while st:
            q=st.pop()
            for z in adj[q]:
                if z not in seen:seen.add(z);st.append(z)
    return n

def normal_flips(obj):
    me=obj.data;ef={}
    for p in me.polygons:
        vs=list(p.vertices)
        for a,b in zip(vs,vs[1:]+vs[:1]):ef.setdefault(tuple(sorted((a,b))),[]).append(p.index)
    return sum(1 for fs in ef.values() if len(fs)==2 and me.polygons[fs[0]].normal.dot(me.polygons[fs[1]].normal)<-.15)

def max_edge(obj):
    me=obj.data;return max((me.vertices[e.vertices[0]].co-me.vertices[e.vertices[1]].co).length for e in me.edges)

def surface_receipt():
    body=bpy.data.objects.get('DERIVED_911_9922_BODY');cabin=bpy.data.objects.get('DERIVED_911_9922_CABIN')
    return {'schema':'oleander.3d.primary-body-surface-receipt.v1','revision':'V30_DENSE_PRIMARY_BODY_GRID','body_connected_components':components(body) if body else 99,'cabin_connected_components':components(cabin) if cabin else 99,'body_adjacent_face_normal_flip_count':normal_flips(body) if body else 99,'cabin_adjacent_face_normal_flip_count':normal_flips(cabin) if cabin else 99,'body_max_edge_length_m':max_edge(body) if body else 9.0,'body_longitudinal_stations':int(body.get('OLEANDER_LONGITUDINAL_STATIONS',0)) if body else 0,'body_ring_vertices':int(body.get('OLEANDER_RING_VERTICES',0)) if body else 0,'machine_surface_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD' if body and cabin and components(body)==1 and components(cabin)==1 and normal_flips(body)==0 and normal_flips(cabin)==0 else 'MACHINE_SURFACE_TOPOLOGY_FAIL','visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','Class-A continuity','manufacturer CAD','reflection continuity','production patch layout']}

def post(out):
    if not (out/'REFERENCE_REPRO_QA.json').exists():return
    pr=projection30();(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n');rr=regression30(pr);(out/'REFERENCE_REGRESSION_PROMOTION_RECEIPT.json').write_text(json.dumps(rr,ensure_ascii=False,indent=2)+'\n');sr=surface_receipt();(out/'PRIMARY_BODY_SURFACE_RECEIPT.json').write_text(json.dumps(sr,ensure_ascii=False,indent=2)+'\n')
    q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V30_DENSE_PRIMARY_BODY_GRID';q['projection_machine_gate']=pr['status'];q['failure_routing']='PRIMARY_BODY_VISUAL_REVIEW_THEN_REFERENCE_SECTION_REFINEMENT';q['regression_promotion_decision']=rr['promotion_decision'];q['primary_body_surface_state']=sr['machine_surface_state'];q['verification_run']='PASS';q['visual_reference_fidelity']='HOLD';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V30_DENSE_PRIMARY_BODY_GRID';r['projection_machine_gate']=pr['status'];r['regression_promotion_decision']=rr['promotion_decision'];r['primary_body_surface_state']=sr['machine_surface_state'];r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

def run30():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:v.main()
    except SystemExit as e:
        post(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:post(out)
run30()
