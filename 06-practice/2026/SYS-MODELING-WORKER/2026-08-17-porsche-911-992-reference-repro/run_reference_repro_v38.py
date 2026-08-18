#!/usr/bin/env python3
"""V38 — ordered rear-profile cap on clean V34 hull + calibrated independent glass.

V37 improved the greenhouse read but regressed the rear profile and retained six face folds. V38 returns to the
V34 zero-fold topology and changes the smallest causal set: cap rear-half upper rails by the rear width-by-height
screen inside the ring generator, re-order the section after capping, add only one lower-side intermediate rail to
reduce V34's p95 edge stretch, and keep V37-style calibrated glass surfaces. A fold-location diagnostic is emitted.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy,bmesh
HERE=Path(__file__).resolve().parent
V34=HERE/'run_reference_repro_v34.py';text=V34.read_text();marker='\nrun34()\n'
if marker not in text:raise SystemExit('V34 run marker missing')
ns={'__file__':str(V34),'__name__':'oleander_v38_declarations'};exec(compile(text.split(marker,1)[0],str(V34),'exec'),ns)
v=ns['v'];env=ns['env'];PROFILE=ns['PROFILE'];metric=ns['metric'];REAR=ns['REAR'];s01=ns['s01'];lerp=ns['lerp'];Z0=ns['Z0'];ZR=ns['ZR'];base_hull=ns['hull_ring'];orig_build34=ns['orig_build'];base_projection=ns['projection34'];base_regression=ns['regression34'];base_surface=ns['surface34'];base_patch=ns['patch']
GREEN=json.loads((HERE/'REFERENCE_GREENHOUSE_TARGETS_992_2.json').read_text());G=[tuple(map(float,p)) for p in GREEN['side_glass_envelope_m']]
REV='V38_ORDERED_REAR_CAP_REAL_GLASS_HULL'
v.REF='2025_992.2_CARRERA_ORDERED_REAR_CAP_REAL_GLASS_V38';v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v38';v.REFERENCE_CONTRACT['reference_revision']=v.REF;v.REFERENCE_CONTRACT['candidate_revision']=REV;v.REFERENCE_CONTRACT['primary_form_method']='V34_CLEAN_HULL_ORDERED_REAR_PROFILE_CAP_PLUS_REAL_GLASS';v.REFERENCE_CONTRACT['greenhouse_target']='REFERENCE_GREENHOUSE_TARGETS_992_2.json';v.FAMILY_CONTROLS['ORDERED_REAR_CAP_V38']={'rear_profile':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:rear.profile','greenhouse':'REFERENCE_GREENHOUSE_TARGETS_992_2.json','surface_topology':'V34_ZERO_FOLD_BASELINE_PLUS_ONE_LOWER_INTERMEDIATE_RAIL','protected':['LENGTH','WIDTH','HEIGHT','WHEELBASE','AXLE_CENTRES','SIDE_TOP','SIDE_LOWER','FRONT_PROFILE']};v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

def rear_cap(z):
    frac=max(.10,min(.98,(float(z)-Z0)/ZR));return .5*v.WIDTH*ns['ratio_at'](REAR,frac)+.018

def rear_weight(x):
    x=float(x)
    if x<=-.12:return 1.0
    if x>=.22:return 0.0
    return 1.0-s01((x+.12)/.34)

def hull_ring38(x):
    ring=base_hull(x);n=len(ring);half=(n+2)//2;pos=[list(p) for p in ring[:half]]
    # V34 positive half: 11 upper + 5 lower. Cap only upper high/mid rails; preserve low wide haunch and all X/Z targets.
    rw=rear_weight(x)
    if rw>0:
        for i in range(min(11,len(pos))):
            xe,y,z=pos[i]
            if i==0 or z<.72:continue
            ay=abs(y);cap=rear_cap(z);desired=min(ay,cap);strength=rw*s01((z-.72)/.34)*.94
            pos[i][1]=lerp(ay,desired,strength)
        # causal rail ordering after the cap. No post-mesh vertex clipping.
        pos[0][1]=0.0
        for i in range(1,min(11,len(pos))):pos[i][1]=max(pos[i][1],pos[i-1][1]+.002)
    # Insert one intermediate between the upper side rail and V34 first lower rail; retain rest of V34 lower section.
    if len(pos)>=12:
        a=pos[10];b=pos[11];mid=[lerp(a[0],b[0],.5),lerp(a[1],b[1],.5),lerp(a[2],b[2],.5)];pos=pos[:11]+[mid]+pos[11:]
    # lower-side Y must decrease monotonically from side to floor center.
    for i in range(12,len(pos)):
        pos[i][1]=max(0.0,min(pos[i][1],pos[i-1][1]-.002))
    pos[-1][1]=0.0
    full=[tuple(p) for p in pos]+[(xe,-y,z) for xe,y,z in reversed([tuple(p) for p in pos[1:-1]])]
    return full
ns['hull_ring']=hull_ring38;v.body_ring=hull_ring38

# Reuse the V34 original builder but remove material-region fake glazing; recreate V34 diagnostic copy around our hull.
def build_visual_hull38(name,bodymat):
    o=orig_build34(name,bodymat)
    if name=='DERIVED_911_9922_BODY':
        for p in o.data.polygons:p.material_index=0
        o['OLEANDER_FORM_FAMILY']='ORDERED_REAR_CAP_OPAQUE_HULL_V38';o['OLEANDER_GREENHOUSE_STAGE']='INDEPENDENT_CALIBRATED_GLASS'
    d=o.copy();d.data=o.data.copy();d.name='DIAG_PRE_APERTURE_VISUAL_HULL_V34';bpy.context.collection.objects.link(d);d.hide_render=True;d.hide_set(True);d['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY'
    return o
ns['build_visual_hull']=build_visual_hull38

# Calibrated side glass surfaces.
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
def glass38(M):
    out=[v.m.add_panel('REF_WINDSHIELD',[(.650,.620,.830),(.650,-.620,.830),(.235,-.545,1.215),(.235,.545,1.215)],M['glass'],.0015),v.m.add_panel('REF_REAR_GLASS',[(-.390,.490,1.215),(-.390,-.490,1.215),(-1.150,-.592,.990),(-1.150,.592,.990)],M['glass'],.0015)]
    bp=(-.20,interp(G,-.20,1),interp(G,-.20,2));q=[p for p in G if p[0]<-.20]+[bp];d=[bp]+[p for p in G if p[0]>-.20]
    for side,label in ((1,'L'),(-1,'R')):
        out+=[strip('REF_QUARTER_GLASS_'+label,q,side,M['glass']),strip('REF_DOOR_GLASS_'+label,d,side,M['glass'])]
        by=glass_y(-.20,(bp[1]+bp[2])*.5);bz=(bp[1]+bp[2])*.5;bh=max(.12,bp[1]-bp[2]);b=v.m.add_cube('REF_B_PILLAR_'+label,(-.20,side*by,bz),(.026,.016,bh),M['body_dark'],.002);b['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';out.append(b)
        out.append(v.m.add_cube('REF_DOOR_HANDLE_'+label,(-.020,side*.896,.682),(.105,.012,.017),M['body_dark'],.003))
    for name,loc,scale in [('REF_CABIN_OCCLUSION_BACKING',(-.18,0,.785),(1.35,.80,.10)),('REF_DASH_BACKING',(.410,0,.760),(.30,.76,.09)),('REF_REAR_BULKHEAD_BACKING',(-.840,0,.745),(.16,.76,.12))]:
        o=v.m.add_cube(name,loc,scale,M['body_dark'],.006);o['OLEANDER_AUTHORITY']='DERIVED_EXECUTION_NOT_AUTHORITY';out.append(o)
    return out
v.build_glass=glass38

# robust projection label / finite endpoint handling.
def projection38():
    d=base_projection();d['candidate_revision']=REV;d['primary_form_stage']='ORDERED_REAR_CAP_REAL_GLASS_PRIMARY_HULL';finite=[];total=0
    for s in d.get('side_upper_samples',[]):
        total+=1;e=s.get('top_error_m')
        if isinstance(e,(int,float)) and math.isfinite(float(e)):finite.append(float(e))
    cov=len(finite)/max(1,total);rmse=math.sqrt(sum(e*e for e in finite)/len(finite)) if finite else 9.0
    for m in d['metrics']:
        if m['id']=='SIDE_UPPER_EVALUATED_MESH_RMSE_M':m['candidate']=rmse;m['abs_error']=rmse;m['candidate_measurement_source']='V38_FINAL_EVALUATED_HULL_FINITE_INTERSECTIONS';m['finite_sample_coverage']=cov
        else:m['candidate_measurement_source']=str(m.get('candidate_measurement_source','')).replace('V34_','V38_')
    d['side_upper_finite_sample_coverage']=cov;d['greenhouse_representation']='INDEPENDENT_CALIBRATED_GLASS';d['status']='PROJECTION_MACHINE_SCREENING_PASS' if cov>=.90 and all(math.isfinite(float(m['abs_error'])) and float(m['abs_error'])<=float(m['limit']) for m in d['metrics']) else 'PROJECTION_MACHINE_SCREENING_FAIL';return d
env['projection30']=projection38

def regression38(pr):
    d=base_regression(pr);d['candidate_revision']=REV;d['edit_scope']=['ORDERED_REAR_PROFILE_CAP','ONE_LOWER_INTERMEDIATE_RAIL','INDEPENDENT_CALIBRATED_GLASS'];d['visual_review_state']='NOT_RUN'
    if d.get('promotion_decision')=='PROMOTE_OVER_LKG':d['promotion_decision']='KEEP_LKG_HOLD_EXPERIMENT'
    return d
env['regression30']=regression38

def surface38():d=base_surface();d['revision']=REV;return d
env['surface_receipt']=surface38

def fold_diagnostic(out):
    obj=bpy.data.objects.get('DIAG_PRE_APERTURE_VISUAL_HULL_V34');rows=[]
    if obj:
        me=obj.data;ef={}
        for p in me.polygons:
            for e in p.edge_keys:ef.setdefault(tuple(sorted(e)),[]).append(p.index)
        for e,fs in ef.items():
            if len(fs)!=2:continue
            a,b=me.polygons[fs[0]],me.polygons[fs[1]];dot=float(a.normal.dot(b.normal))
            if dot<-.15:
                va=me.vertices[e[0]].co;vb=me.vertices[e[1]].co;c=(va+vb)*.5;rows.append({'edge_vertices':list(e),'face_indices':fs,'normal_dot':dot,'center_m':[float(c.x),float(c.y),float(c.z)]})
    Path(out,'SURFACE_FOLD_DIAGNOSTIC.json').write_text(json.dumps({'schema':'oleander.3d.surface-fold-diagnostic.v1','candidate_revision':REV,'fold_count':len(rows),'folds':rows,'authority':'DIAGNOSTIC_NOT_REFERENCE_AUTHORITY'},indent=2)+'\n')

def patch38(out):
    base_patch(out);fold_diagnostic(out)
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if p.exists():
            d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='ORDERED_REAR_CAP_REAL_GLASS_PRIMARY_HULL';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def run38():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:env['run30']()
    except SystemExit as e:patch38(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch38(out)
run38()
