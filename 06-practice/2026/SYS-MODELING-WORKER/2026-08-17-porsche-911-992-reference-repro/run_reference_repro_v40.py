#!/usr/bin/env python3
"""V40 — smooth rear cabin blend + ordered rear cap on the V34 clean primary skin.

V39 passed all projected primary-form screens but created 18 pre-aperture folds. Fold localization showed a long
cluster through x≈-1.54..-1.27 m, exactly where V34 switches from body section to cabin section over only 0.24 m,
plus the rear-axle shoulder/haunch pair. V40 fixes the cause instead of smoothing the symptom:
- extend rear body->cabin blend over ~0.84 m;
- apply the V39 rear profile cap inside that causal section generation;
- use only two linear shoulder->haunch transition rails;
- retain V37/V38 calibrated independent glass;
- keep SIDE, FRONT, wheelbase, wheel apertures and lower terminal authority frozen.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy,bmesh
HERE=Path(__file__).resolve().parent
V34=HERE/'run_reference_repro_v34.py';text=V34.read_text();marker='\nrun34()\n'
if marker not in text:raise SystemExit('V34 run marker missing')
ns={'__file__':str(V34),'__name__':'oleander_v40_declarations'};exec(compile(text.split(marker,1)[0],str(V34),'exec'),ns)
v=ns['v'];env=ns['env'];PROFILE=ns['PROFILE'];metric=ns['metric'];REAR=ns['REAR'];s01=ns['s01'];lerp=ns['lerp'];Z0=ns['Z0'];ZR=ns['ZR'];orig_build34=ns['orig_build'];base_projection=ns['projection34'];base_regression=ns['regression34'];base_surface=ns['surface34'];base_patch=ns['patch']
GREEN=json.loads((HERE/'REFERENCE_GREENHOUSE_TARGETS_992_2.json').read_text());G=[tuple(map(float,p)) for p in GREEN['side_glass_envelope_m']]
REV='V40_SMOOTH_REAR_CABIN_BLEND_ORDERED_SKIN'
v.REF='2025_992.2_CARRERA_SMOOTH_REAR_CABIN_BLEND_V40';v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v40';v.REFERENCE_CONTRACT['reference_revision']=v.REF;v.REFERENCE_CONTRACT['candidate_revision']=REV;v.REFERENCE_CONTRACT['failure_routing']='REAR_CABIN_BLEND_AND_SHOULDER_HAUNCH_TOPOLOGY';v.FAMILY_CONTROLS['SMOOTH_REAR_CABIN_BLEND_V40']={'rear_profile':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:rear.profile','rear_cabin_blend_x_m':[-1.72,-.88],'rear_cap_margin_m':.010,'shoulder_haunch_transition_rails':2,'greenhouse':'REFERENCE_GREENHOUSE_TARGETS_992_2.json','protected':['SIDE_GESTURE','SIDE_LOWER','FRONT_PROFILE','GREENHOUSE_ENVELOPE','WHEELBASE','AXLE_CENTRES','WHEEL_APERTURE']};v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

# Replace the V34 0.24 m rear body->cabin switch with a long causal blend. Front fade stays unchanged.
def cabin_weight40(x):
    x=float(x)
    if x<=-1.72:return 0.0
    if x<-.88:return s01((x+1.72)/.84)
    if x<=.58:return 1.0
    if x<.78:return 1.0-s01((x-.58)/.20)
    return 0.0
ns['cabin_weight']=cabin_weight40

def rear_cap(z):
    frac=max(.10,min(.98,(float(z)-Z0)/ZR));return .5*v.WIDTH*ns['ratio_at'](REAR,frac)+.010

def rear_weight(x):
    x=float(x)
    if x<=-.12:return 1.0
    if x>=.20:return 0.0
    return 1.0-s01((x+.12)/.32)

def hull_ring40(x):
    w=ns['plan_half_width'](x);top=ns['side_top'](x);floor=ns['terminal_floor'](x);cw=cabin_weight40(x)
    fvals=[0,.12,.24,.36,.48,.60,.70,.78,.85,.92,1.0]
    body=[ns['body_half_section'](x,w,top,f) for f in fvals];cab=ns['cabin_section_samples'](x,w,top)
    pos=[]
    for (yb,zb),(yc,zc) in zip(body,cab):pos.append([lerp(yb,yc,cw),lerp(zb,zc,cw)])
    # Rear profile contraction is generated inside the section. Use a smooth per-height scale, never a post-mesh clip.
    rw=rear_weight(x)
    if rw>0:
        vals=[]
        for i,(y,z) in enumerate(pos):
            ay=abs(y)
            if i==0 or z<.70:vals.append(ay);continue
            cap=rear_cap(z);ratio=min(1.0,cap/max(ay,1e-6));zw=s01((z-.70)/.34);vals.append(ay*lerp(1.0,ratio,rw*zw))
        vals[0]=0.0
        # enforce ordered section while respecting the outer caps: backward then forward pass.
        for i in range(len(vals)-2,0,-1):vals[i]=min(vals[i],max(.002,vals[i+1]-.002))
        for i in range(1,len(vals)):vals[i]=max(vals[i],vals[i-1]+.002)
        for i in range(len(pos)):pos[i][0]=vals[i]
    # V34 lower envelope authority. Two simple linear rails remove the abrupt side->haunch jump without a fan.
    sidez=pos[-1][1];first_low=[.998*w,max(floor+.038,min(sidez-.050,.240))]
    a=pos[-1];trans=[[lerp(a[0],first_low[0],t),lerp(a[1],first_low[1],t)] for t in (.333333,.666667)]
    pos += trans+[first_low,[.90*w,max(floor,.150)],[.68*w,max(.140,floor-.006)],[.36*w,max(.140,floor-.010)],[0.0,max(.140,floor-.012)]]
    # after maximum haunch, y decreases monotonically to floor center.
    start=11+len(trans)
    for i in range(start+1,len(pos)):pos[i][0]=max(0.0,min(pos[i][0],pos[i-1][0]-.002))
    pos[-1][0]=0.0
    ft=s01((x-1.78)/(v.FRONT_X-1.78)) if x>1.78 else 0.0;rt=s01((-x-1.78)/(-v.REAR_X-1.78)) if x<-1.78 else 0.0
    out=[]
    for y,z in pos+[[-yy,zz] for yy,zz in reversed(pos[1:-1])]:
        q=abs(y)/max(w,1e-6);setback=(.105*ft+.085*rt)*(q**1.55);xe=x-setback if x>0 else x+setback;out.append((xe,y,z))
    return out
ns['hull_ring']=hull_ring40;v.body_ring=hull_ring40

# Use V34 builder topology with the V40 global ring; keep body opaque and create diagnostic copy.
def build40(name,bodymat):
    o=orig_build34(name,bodymat)
    if name=='DERIVED_911_9922_BODY':
        for p in o.data.polygons:p.material_index=0
        o['OLEANDER_FORM_FAMILY']='SMOOTH_REAR_CABIN_BLEND_ORDERED_SKIN_V40';o['OLEANDER_FAILURE_ROUTING']='REAR_CABIN_BLEND_AND_SHOULDER_HAUNCH_TOPOLOGY'
    d=o.copy();d.data=o.data.copy();d.name='DIAG_PRE_APERTURE_VISUAL_HULL_V34';bpy.context.collection.objects.link(d);d.hide_render=True;d.hide_set(True);d['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY';return o
ns['build_visual_hull']=build40

# Calibrated independent glass from V37/V38.
def interp(seq,x,field):
    x=float(x)
    if x<=seq[0][0]:return seq[0][field]
    if x>=seq[-1][0]:return seq[-1][field]
    for a,b in zip(seq,seq[1:]):
        if a[0]<=x<=b[0]:return lerp(a[field],b[field],(x-a[0])/(b[0]-a[0]))
    return seq[-1][field]
def glass_y(x,z):
    w=ns['plan_half_width'](x);raw=.5*v.WIDTH*ns['profile_ratio'](x,z);return min(w-.008,max(.42,raw+.012))
def strip(name,pts,side,mat):
    verts=[];faces=[]
    for x,zt,zb in pts:verts.extend([(x,side*glass_y(x,zt),zt),(x,side*glass_y(x,zb),zb)])
    for i in range(len(pts)-1):a=2*i;faces.append((a,a+1,a+3,a+2))
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL';o['OLEANDER_REFERENCE']='REFERENCE_GREENHOUSE_TARGETS_992_2.json';
    for p in me.polygons:p.use_smooth=True
    return o
def glass40(M):
    out=[v.m.add_panel('REF_WINDSHIELD',[(.650,.620,.830),(.650,-.620,.830),(.235,-.545,1.215),(.235,.545,1.215)],M['glass'],.0015),v.m.add_panel('REF_REAR_GLASS',[(-.390,.490,1.215),(-.390,-.490,1.215),(-1.150,-.592,.990),(-1.150,.592,.990)],M['glass'],.0015)]
    bp=(-.20,interp(G,-.20,1),interp(G,-.20,2));q=[p for p in G if p[0]<-.20]+[bp];d=[bp]+[p for p in G if p[0]>-.20]
    for side,label in ((1,'L'),(-1,'R')):
        out+=[strip('REF_QUARTER_GLASS_'+label,q,side,M['glass']),strip('REF_DOOR_GLASS_'+label,d,side,M['glass'])]
        by=glass_y(-.20,(bp[1]+bp[2])*.5);bz=(bp[1]+bp[2])*.5;bh=max(.12,bp[1]-bp[2]);b=v.m.add_cube('REF_B_PILLAR_'+label,(-.20,side*by,bz),(.026,.016,bh),M['body_dark'],.002);b['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';out.append(b)
    for name,loc,scale in [('REF_CABIN_OCCLUSION_BACKING',(-.18,0,.785),(1.35,.80,.10)),('REF_DASH_BACKING',(.410,0,.760),(.30,.76,.09)),('REF_REAR_BULKHEAD_BACKING',(-.840,0,.745),(.16,.76,.12))]:
        o=v.m.add_cube(name,loc,scale,M['body_dark'],.006);o['OLEANDER_AUTHORITY']='DERIVED_EXECUTION_NOT_AUTHORITY';out.append(o)
    return out
v.build_glass=glass40

def projection40():
    d=base_projection();d['candidate_revision']=REV;d['primary_form_stage']='SMOOTH_REAR_CABIN_BLEND_ORDERED_SKIN';finite=[];total=0
    for s in d.get('side_upper_samples',[]):
        total+=1;e=s.get('top_error_m')
        if isinstance(e,(int,float)) and math.isfinite(float(e)):finite.append(float(e))
    cov=len(finite)/max(1,total);rmse=math.sqrt(sum(e*e for e in finite)/len(finite)) if finite else 9.0
    for m in d['metrics']:
        if m['id']=='SIDE_UPPER_EVALUATED_MESH_RMSE_M':m['candidate']=rmse;m['abs_error']=rmse;m['candidate_measurement_source']='V40_FINAL_EVALUATED_HULL_FINITE_INTERSECTIONS';m['finite_sample_coverage']=cov
        else:m['candidate_measurement_source']=str(m.get('candidate_measurement_source','')).replace('V34_','V40_')
    d['side_upper_finite_sample_coverage']=cov;d['greenhouse_representation']='INDEPENDENT_CALIBRATED_GLASS';d['status']='PROJECTION_MACHINE_SCREENING_PASS' if cov>=.90 and all(math.isfinite(float(m['abs_error'])) and float(m['abs_error'])<=float(m['limit']) for m in d['metrics']) else 'PROJECTION_MACHINE_SCREENING_FAIL';return d
env['projection30']=projection40

def regression40(pr):
    d=base_regression(pr);d['candidate_revision']=REV;d['edit_scope']=['REAR_CABIN_BLEND_LENGTH','ORDERED_REAR_PROFILE_CAP','TWO_LINEAR_SHOULDER_HAUNCH_RAILS'];d['visual_review_state']='NOT_RUN'
    if d.get('promotion_decision')=='PROMOTE_OVER_LKG':d['promotion_decision']='KEEP_LKG_HOLD_EXPERIMENT'
    return d
env['regression30']=regression40

def surface40():d=base_surface();d['revision']=REV;return d
env['surface_receipt']=surface40

def fold_diag(out):
    obj=bpy.data.objects.get('DIAG_PRE_APERTURE_VISUAL_HULL_V34');rows=[]
    if obj:
        me=obj.data;ef={}
        for p in me.polygons:
            for e in p.edge_keys:ef.setdefault(tuple(sorted(e)),[]).append(p.index)
        for e,fs in ef.items():
            if len(fs)==2:
                dot=float(me.polygons[fs[0]].normal.dot(me.polygons[fs[1]].normal))
                if dot<-.15:
                    c=(me.vertices[e[0]].co+me.vertices[e[1]].co)*.5;rows.append({'edge_vertices':list(e),'face_indices':fs,'normal_dot':dot,'center_m':[float(c.x),float(c.y),float(c.z)]})
    Path(out,'SURFACE_FOLD_DIAGNOSTIC.json').write_text(json.dumps({'schema':'oleander.3d.surface-fold-diagnostic.v1','candidate_revision':REV,'fold_count':len(rows),'folds':rows,'authority':'DIAGNOSTIC_NOT_REFERENCE_AUTHORITY'},indent=2)+'\n')
def patch40(out):
    base_patch(out);fold_diag(out)
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if p.exists():
            d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='SMOOTH_REAR_CABIN_BLEND_ORDERED_SKIN';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def run40():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:env['run30']()
    except SystemExit as e:patch40(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch40(out)
run40()
