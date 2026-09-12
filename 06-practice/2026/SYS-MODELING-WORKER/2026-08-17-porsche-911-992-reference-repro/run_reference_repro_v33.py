#!/usr/bin/env python3
"""V33 — monotonic rear ring + smooth connected greenhouse canopy/frame.

V32 proved rear Y/Z routing (rear profile 0.2646 -> 0.1487) but introduced 10 pre-aperture body face flips and
left the greenhouse visually as wedges/panels. V33 keeps the useful rear contraction, projects each body
cross-section back to an ordered symmetric ring, and replaces the greenhouse with a connected roof/A/C frame
plus coherent glazing canopy. Strict mixed per-gate baselines remain; no self-promotion.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy,bmesh

HERE=Path(__file__).resolve().parent
V32=HERE/'run_reference_repro_v32.py'
text=V32.read_text();marker="\ncore['run30']()\n"
if marker not in text:raise SystemExit('V32 run marker missing')
env={'__file__':str(V32),'__name__':'oleander_v33_declarations'}
exec(compile(text.split(marker,1)[0],str(V32),'exec'),env)
core=env['core'];v=env['v'];v31=env['outer'];PROFILE=env['PROFILE'];metric=env['metric'];surface31=env['surface31']
old_ring=core['body_ring30'];side_ref=v31['side_ref'];s01=env['s01']
REV='V33_MONOTONIC_REAR_SMOOTH_CANOPY'

v.REF='2025_992.2_CARRERA_MONOTONIC_REAR_SMOOTH_CANOPY_V33'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v33'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['body_ring_constraint']='ORDERED_SYMMETRIC_CROSS_SECTION_AFTER_REAR_YZ_ROUTING'
v.REFERENCE_CONTRACT['greenhouse_method']='CONNECTED_OPAQUE_FRAME_PLUS_COHERENT_GLAZING_CANOPY'
v.FAMILY_CONTROLS['V33_MONOTONIC_REAR_SMOOTH_CANOPY']={
 'body':'V32 rear YZ constraint + monotonic ring projection',
 'greenhouse':['ROOF_PANEL','A_PILLAR_FRAME','C_PILLAR_FRAME','REAR_DECK_BRIDGE','WINDSHIELD','SIDE_GLAZING','REAR_GLASS'],
 'protected':['V31_FRONT_PROFILE','V25_SIDE/LOWER/APERTURE_BASELINES','WHEELBASE','AXLE_CENTRES','WHEEL_APERTURES']}
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

# Cross-section isotonic repair: preserve each point's X/Z and only remove Y ordering inversions.
def body_ring33(x):
    r=old_ring(x)
    if len(r)!=30:return r
    pos=[list(p) for p in r[:16]]
    # positive half: center -> widest side must increase through rail 9.
    pos[0][1]=0.0
    for i in range(1,10):
        pos[i][1]=max(float(pos[i][1]),float(pos[i-1][1])+.0015)
    # widest side -> floor center must decrease monotonically.
    for i in range(10,16):
        pos[i][1]=max(0.0,min(float(pos[i][1]),float(pos[i-1][1])-.0015))
    # enforce exact terminal floor-center symmetry.
    pos[-1][1]=0.0
    pos=[tuple(p) for p in pos]
    neg=[(xe,-y,z) for xe,y,z in reversed(pos[1:-1])]
    return pos+neg
core['body_ring30']=body_ring33
v.body_ring=body_ring33

# Helpers for greenhouse frame / glass.
def lerp(a,b,t):return a*(1-t)+b*t
def roof_top(x):return float(side_ref(float(x)))
def panel(name,pts,mat,th=.0025,authority='DERIVED_APERTURE_INFILL'):
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(pts,[],[tuple(range(len(pts)))]);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['OLEANDER_AUTHORITY']=authority
    if th:
        s=o.modifiers.new(name+'_THICKNESS','SOLIDIFY');s.thickness=th;s.offset=0;s.use_rim=False
    for p in me.polygons:p.use_smooth=True
    return o

# One connected opaque frame object: central roof + A/C pillars + rear deck bridge.
def frame33(name,material):
    verts=[];faces=[];idx={}
    def add(k,p):
        if k in idx:return idx[k]
        idx[k]=len(verts);verts.append(tuple(map(float,p)));return idx[k]
    def face(*a):faces.append(tuple(a))
    xs=[-.55,-.47,-.39,-.31,-.23,-.15,-.07,.01,.09,.17,.25]
    rows=[]
    for x in xs:
        t=(x+.55)/.80;outer=lerp(.42,.58,s01(t));inner=max(.30,outer-.075);top=roof_top(x)
        row=[add(('roof',x,'LO'),(x,-outer,top-.035)),add(('roof',x,'LI'),(x,-inner,top-.010)),add(('roof',x,'C'),(x,0,top)),add(('roof',x,'RI'),(x,inner,top-.010)),add(('roof',x,'RO'),(x,outer,top-.035))];rows.append(row)
    for a,b in zip(rows,rows[1:]):
        for j in range(4):face(a[j],b[j],b[j+1],a[j+1])
    rear,front=rows[0],rows[-1]
    # A-pillar frame shares front roof row and lands at windshield lower boundary.
    for side,lab,ro,ri in ((1,'R',front[4],front[3]),(-1,'L',front[0],front[1])):
        oo=add(('A',lab,'O'),(.650,side*.660,.805));ii=add(('A',lab,'I'),(.650,side*.600,.840));face(ro,oo,ii,ri)
    # C-pillar frame: high roof end stays narrow; width grows only while Z falls toward quarter/rear deck.
    for side,lab,ro,ri in ((1,'R',rear[4],rear[3]),(-1,'L',rear[0],rear[1])):
        stations=[(-.55,abs(verts[ro][1]),abs(verts[ri][1]),verts[ro][2],verts[ri][2]),(-.72,.46,.40,1.105,1.145),(-.90,.54,.47,1.015,1.070),(-1.05,.62,.53,.930,1.025),(-1.15,.70,.592,.850,.990)]
        outs=[ro];ins=[ri]
        for k,(x,oy,iy,oz,iz) in enumerate(stations[1:],1):outs.append(add(('C',lab,k,'O'),(x,side*oy,oz)));ins.append(add(('C',lab,k,'I'),(x,side*iy,iz)))
        for i in range(len(outs)-1):face(outs[i],outs[i+1],ins[i+1],ins[i])
        deck=add(('deck',lab),(-1.38,side*.75,.805));face(outs[-1],deck,ins[-1])
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(material);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DISPLAY';o['OLEANDER_FORM_FAMILY']='CONNECTED_SMOOTH_CANOPY_FRAME_V33';o['OLEANDER_NO_OPAQUE_SURFACE_BEHIND_GLAZING']=True;o['OLEANDER_OPEN_PATCH_RIM_WALLS']=False
    for p in me.polygons:p.use_smooth=True
    return o
core['simple_cabin30']=frame33
v.build_loft=core['build_loft30']

# Coherent glazing family. It follows the same roof side target but remains open between opaque frame bands.
def glass33(M):
    out=[]
    ftop=roof_top(.25)-.018;rtop=roof_top(-.55)-.020
    out.append(panel('REF_WINDSHIELD',[(.650,.600,.840),(.650,-.600,.840),(.25,-.505,ftop),(.25,.505,ftop)],M['glass']))
    out.append(panel('REF_REAR_GLASS',[(-.55,.345,rtop),(-.55,-.345,rtop),(-1.15,-.592,.990),(-1.15,.592,.990)],M['glass']))
    for side,label in ((1,'L'),(-1,'R')):
        # One clean door glazing and one quarter glazing; top points remain under the roof rail.
        door=[(.620,side*.595,.845),(.25,side*.495,ftop-.010),(-.20,side*.420,roof_top(-.20)-.045),(-.20,side*.560,.850),(.500,side*.600,.842)]
        quarter=[door[2],(-.55,side*.335,rtop-.010),(-.82,side*.430,1.085),(-1.10,side*.565,1.005),(-.68,side*.555,.875),(-.20,side*.560,.850)]
        out.append(panel('REF_DOOR_GLASS_'+label,door,M['glass']));out.append(panel('REF_QUARTER_GLASS_'+label,quarter,M['glass']))
        b=v.m.add_cube('REF_B_PILLAR_'+label,(-.20,side*.500,1.020),(.028,.024,.290),M['body_dark'],.003);b['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';out.append(b)
        out.append(v.m.add_cube('REF_DOOR_HANDLE_'+label,(-.020,side*.896,.682),(.105,.012,.017),M['body_dark'],.003));y=side*.912;out.append(v.m.add_curve('REF_DOOR_SEAM_'+label,[(.595,y,.765),(.545,y,.500),(-.635,y,.500),(-.800,y,.665),(-.785,y,.825)],M['seam'],.0016))
    # Interior occlusion only; never exterior authority.
    for nm,loc,scale in [('REF_CABIN_OCCLUSION_BACKING',(-.18,0,.785),(1.34,.78,.09)),('REF_DASH_BACKING',(.410,0,.760),(.30,.82,.08)),('REF_REAR_BULKHEAD_BACKING',(-.86,0,.760),(.16,.76,.11))]:
        o=v.m.add_cube(nm,loc,scale,M['body_dark'],.006);o['OLEANDER_AUTHORITY']='DERIVED_EXECUTION_NOT_AUTHORITY';out.append(o)
    return out
v.build_glass=glass33

base_source=v.build_source
def source33(M):
    o=base_source(M);o['OLEANDER_BODY_RING']='V33_MONOTONIC_REAR';o['OLEANDER_GREENHOUSE']='V33_CONNECTED_FRAME_COHERENT_GLAZING';o['OLEANDER_CONTROL_DIGEST']=v.m.sha_json(v.FAMILY_CONTROLS);return o
v.build_source=source33

base_projection=env['projection32']
def relabel(data):
    if isinstance(data,dict):return {k:relabel(x) for k,x in data.items()}
    if isinstance(data,list):return [relabel(x) for x in data]
    if isinstance(data,str):return data.replace('V32_','V33_')
    return data

def projection33():
    d=relabel(base_projection());d['candidate_revision']=REV;d['greenhouse_method']='CONNECTED_SMOOTH_CANOPY_FRAME';return d
core['projection30']=projection33

BEST33=env['BEST32']
def regression33(pr):
    vals={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_UPPER_EVALUATED_MESH_RMSE_M')['candidate'],'SIDE_LOWER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_LOWER_EVALUATED_MESH_RMSE_M')['candidate'],'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':metric(pr,'FRONT_UPPER_CABIN_WIDTH_RATIO')['abs_error'],'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':metric(pr,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO')['abs_error'],'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':metric(pr,'REAR_BACKLIGHT_LOWER_WIDTH_RATIO')['abs_error'],'FRONT_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'FRONT_HALF_PROJECTED_PROFILE_RMSE')['candidate'],'REAR_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'REAR_HALF_PROJECTED_PROFILE_RMSE')['candidate']}
    limits={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':.034,'SIDE_LOWER_EVALUATED_MESH_RMSE_M':.066,'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':.010,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':.010,'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':.010,'FRONT_HALF_PROJECTED_PROFILE_RMSE':.078,'REAR_HALF_PROJECTED_PROFILE_RMSE':.130}
    locks=[]
    for mid,b in BEST33.items():
        c=vals[mid];locks.append({'id':mid,'baseline':b['value'],'baseline_revision':b['revision'],'candidate':c,'limit':limits[mid],'status':'PASS' if math.isfinite(c) and c<=limits[mid] else 'REGRESSED','evidence_source':b['evidence_source']})
    rear=vals['REAR_HALF_PROJECTED_PROFILE_RMSE'];side=vals['SIDE_UPPER_EVALUATED_MESH_RMSE_M'];all_locks=all(x['status']=='PASS' for x in locks)
    return {'schema':'oleander.3d.reference-regression-promotion-receipt.v2','baseline_revision':'MIXED_PER_GATE_BEST_KNOWN_V25_V23_V31','candidate_revision':REV,'edit_scope':['REAR_BODY_RING_ORDERING','GREENHOUSE_REPRESENTATION','FRONT_BODY_LOCKED','LOWER_GEOMETRY_LOCKED'],'target_metric_delta':{'metric_id':'REAR_HALF_PROJECTED_PROFILE_RMSE','baseline':0.14874601652245933,'candidate':rear,'direction':'LOWER_IS_BETTER','improved':rear<0.14874601652245933},'secondary_target_metrics':[{'metric_id':'SIDE_UPPER_EVALUATED_MESH_RMSE_M','baseline':0.05497396595366651,'candidate':side,'direction':'LOWER_IS_BETTER','improved':side<0.05497396595366651}],'regression_locks':locks,'best_known_gate_baselines':BEST33,'measurement_method_ids':['V33_FINAL_EVALUATED_MESH_XZ','V33_FINAL_EVALUATED_MESH_YZ','V33_PRE_APERTURE_SKIN'],'measurement_comparability':'COMPARABLE','promotion_decision':'KEEP_LKG_HOLD_EXPERIMENT' if all_locks else 'KEEP_LKG_REJECT_EXPERIMENT','visual_review_state':'NOT_RUN','does_not_prove':PROFILE['does_not_prove']}
core['regression30']=regression33

def surface33():
    d=surface31();d['revision']=REV;return d
core['surface_receipt']=surface33

# Core run writes inherited QA fields; patch them after execution, then enforce one candidate revision across receipts.
def patch_revision(out):
    for fname in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=out/fname
        if not p.exists():continue
        d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['failure_routing']='V33_VISUAL_REVIEW_THEN_PRIMARY_SECTION_REFINEMENT';d['visual_reference_fidelity']='HOLD' if fname.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def run33():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:core['run30']()
    except SystemExit as e:
        patch_revision(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch_revision(out)
run33()
