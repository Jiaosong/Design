#!/usr/bin/env python3
"""V37 — causal rear-profile section + calibrated glass surfaces on clean V34 topology.

V36 proved two things: the same-revision greenhouse envelope is useful, but polygon-level dark material assignment
still reads as a wedge; and post-generated per-rail rear edits create face folds. V37 therefore returns to V34's
clean generator and moves all form corrections upstream into the section evaluator. The visible body stays opaque;
windshield, rear glass and side glass are independent surfaces. This is still a primary-form benchmark, not final
production aperture/flange architecture.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy,bmesh
HERE=Path(__file__).resolve().parent
V34=HERE/'run_reference_repro_v34.py';text=V34.read_text();marker='\nrun34()\n'
if marker not in text:raise SystemExit('V34 run marker missing')
ns={'__file__':str(V34),'__name__':'oleander_v37_declarations'};exec(compile(text.split(marker,1)[0],str(V34),'exec'),ns)
v=ns['v'];env=ns['env'];PROFILE=ns['PROFILE'];VIS=ns['VIS'];metric=ns['metric'];REAR=ns['REAR'];FRONT=ns['FRONT'];s01=ns['s01'];lerp=ns['lerp'];h=ns['h'];Z0=ns['Z0'];ZR=ns['ZR']
GREEN=json.loads((HERE/'REFERENCE_GREENHOUSE_TARGETS_992_2.json').read_text());G=[tuple(map(float,p)) for p in GREEN['side_glass_envelope_m']]
REV='V37_CAUSAL_SECTION_REAL_GLASS_HULL'
base_body_half=ns['body_half_section'];base_builder=ns['build_visual_hull'];base_projection=ns['projection34'];base_regression=ns['regression34'];base_surface=ns['surface34'];base_patch=ns['patch'];base_glass=v.build_glass
v.REF='2025_992.2_CARRERA_CAUSAL_SECTION_REAL_GLASS_V37';v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v37';v.REFERENCE_CONTRACT['reference_revision']=v.REF;v.REFERENCE_CONTRACT['candidate_revision']=REV;v.REFERENCE_CONTRACT['primary_form_method']='CLEAN_SINGLE_HULL_CAUSAL_SECTION_PLUS_INDEPENDENT_CALIBRATED_GLASS';v.REFERENCE_CONTRACT['greenhouse_target']='REFERENCE_GREENHOUSE_TARGETS_992_2.json';v.REFERENCE_CONTRACT['aperture_stage']='INDEPENDENT_GLASS_SURFACE_PRIMARY_FORM_NOT_FINAL_FLANGE';v.FAMILY_CONTROLS['CAUSAL_SECTION_REAL_GLASS_V37']={'rear_profile':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:rear.profile','front_profile':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:front.profile','greenhouse':'REFERENCE_GREENHOUSE_TARGETS_992_2.json','protected':['LENGTH','WIDTH','HEIGHT','WHEELBASE','AXLE_CENTRES','SIDE_TOP','SIDE_LOWER','WHEEL_APERTURE','LOWER_TERMINAL_RETURN']};v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

# Shift FRONT/REAR section blending forward. Rear orthographic screening must not be dominated by a half-front blend at x≈0.
def front_weight37(x):
    x=float(x)
    if x<=-.02:return 0.0
    if x>=.46:return 1.0
    return s01((x+.02)/.48)
ns['front_weight']=front_weight37

# Keep the V34 section topology but introduce a modest front hood valley causally, before mesh generation.
def body_half_section37(x,w,top,f):
    y,z=base_body_half(x,w,top,f)
    fi=math.exp(-((float(x)-v.FRONT_AXLE)/.57)**4)
    # f is normalized center->outer. Depress center/inner hood, leave crown/outer top alone.
    if f<.58:z-=.030*fi*(1-f/.58)**1.45
    return y,z
ns['body_half_section']=body_half_section37

def terminal_floor(x):return float(ns['terminal_floor'](x))

# Rebuild only the ring function: same upper section logic, denser causal lower-side rails, no post-generation clipping.
def hull_ring37(x):
    w=ns['plan_half_width'](x);top=ns['side_top'](x);floor=terminal_floor(x);cw=ns['cabin_weight'](x)
    fvals=[0,.12,.24,.36,.48,.60,.70,.78,.85,.92,1.0]
    body=[body_half_section37(x,w,top,f) for f in fvals];cab=ns['cabin_section_samples'](x,w,top)
    upper=[]
    for (yb,zb),(yc,zc) in zip(body,cab):upper.append((lerp(yb,yc,cw),lerp(zb,zc,cw)))
    # enforce ordered positive-half rail without changing top gesture.
    u=[list(p) for p in upper];u[0][0]=0.0
    for i in range(1,len(u)):u[i][0]=max(u[i][0],u[i-1][0]+.002)
    wout=u[-1][0];sidez=u[-1][1];rocker=max(floor+.055,.185)
    lower=[]
    # dense surface from belt/outer side down to rocker; all stations use identical topology.
    for j,t in enumerate((.16,.32,.48,.64,.78,.89)):
        yy=wout*(1-.002*j);zz=lerp(sidez,rocker,t);lower.append((yy,zz))
    lower += [(.975*wout,rocker),(.91*wout,max(floor+.020,.155)),(.78*wout,max(floor,.145)),(.64*wout,max(.140,floor-.003)),(.50*wout,max(.140,floor-.006)),(.36*wout,max(.140,floor-.008)),(.22*wout,max(.140,floor-.010)),(.10*wout,max(.140,floor-.011)),(0.0,max(.140,floor-.012))]
    pos=[tuple(p) for p in u]+lower
    ft=s01((x-1.78)/(v.FRONT_X-1.78)) if x>1.78 else 0.0;rt=s01((-x-1.78)/(-v.REAR_X-1.78)) if x<-1.78 else 0.0
    out=[]
    for y,z in pos+[(-yy,zz) for yy,zz in reversed(pos[1:-1])]:
        q=abs(y)/max(w,1e-6);setback=(.105*ft+.085*rt)*(q**1.55);xe=x-setback if x>0 else x+setback;out.append((xe,y,z))
    return out
ns['hull_ring']=hull_ring37;v.body_ring=hull_ring37

# Body remains opaque. Glass is no longer encoded by polygon material classification.
def build_visual_hull37(name,bodymat):
    o=base_builder(name,bodymat)
    if name=='DERIVED_911_9922_BODY':
        for p in o.data.polygons:p.material_index=0
        o['OLEANDER_FORM_FAMILY']='SINGLE_CAUSAL_SECTION_OPAQUE_HULL_V37';o['OLEANDER_GREENHOUSE_STAGE']='INDEPENDENT_GLASS_SURFACES'
    return o
ns['build_visual_hull']=build_visual_hull37

def interp(seq,x,field):
    x=float(x)
    if x<=seq[0][0]:return seq[0][field]
    if x>=seq[-1][0]:return seq[-1][field]
    for a,b in zip(seq,seq[1:]):
        if a[0]<=x<=b[0]:return lerp(a[field],b[field],(x-a[0])/(b[0]-a[0]))
    return seq[-1][field]

def glass_y(x,z):
    # place glazing just outside the causal greenhouse hull at the same height.
    w=ns['plan_half_width'](x);raw=.5*v.WIDTH*ns['profile_ratio'](x,z);return min(w-.010,max(.42,raw+.010))

def make_glass_strip(name,pts,side,mat):
    verts=[];faces=[]
    for x,zt,zb in pts:
        yt=glass_y(x,zt);yb=glass_y(x,zb);verts.extend([(x,side*yt,zt),(x,side*yb,zb)])
    for i in range(len(pts)-1):a=2*i;b=a+1;c=a+3;d=a+2;faces.append((a,b,c,d))
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL';o['OLEANDER_REFERENCE']='REFERENCE_GREENHOUSE_TARGETS_992_2.json';
    for p in me.polygons:p.use_smooth=True
    return o

def glass37(M):
    out=[]
    # visible windshield and rear glass from existing calibrated anchors.
    out.append(v.m.add_panel('REF_WINDSHIELD',[(.650,.620,.830),(.650,-.620,.830),(.235,-.545,1.215),(.235,.545,1.215)],M['glass'],.0015))
    out.append(v.m.add_panel('REF_REAR_GLASS',[(-.390,.490,1.215),(-.390,-.490,1.215),(-1.150,-.592,.990),(-1.150,.592,.990)],M['glass'],.0015))
    # split calibrated side glass at B pillar x≈-0.20 without changing the measured envelope.
    for side,label in ((1,'L'),(-1,'R')):
        q=[p for p in G if p[0]<=-.20];d=[p for p in G if p[0]>=-.20]
        # interpolate exact B section into both surfaces.
        bp=(-.20,interp(G,-.20,1),interp(G,-.20,2));q=q+[bp];d=[bp]+d
        out.append(make_glass_strip('REF_QUARTER_GLASS_'+label,q,side,M['glass']));out.append(make_glass_strip('REF_DOOR_GLASS_'+label,d,side,M['glass']))
        by=glass_y(-.20,(bp[1]+bp[2])*.5);bz=(bp[1]+bp[2])*.5;bh=max(.12,bp[1]-bp[2]);b=v.m.add_cube('REF_B_PILLAR_'+label,(-.20,side*by,bz),(.030,.018,bh),M['body_dark'],.002);b['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';out.append(b)
        out.append(v.m.add_cube('REF_DOOR_HANDLE_'+label,(-.020,side*.896,.682),(.105,.012,.017),M['body_dark'],.003))
    # restrained interior backing only.
    for name,loc,scale in [('REF_CABIN_OCCLUSION_BACKING',(-.18,0,.785),(1.35,.80,.10)),('REF_DASH_BACKING',(.410,0,.760),(.30,.76,.09)),('REF_REAR_BULKHEAD_BACKING',(-.840,0,.745),(.16,.76,.12))]:
        o=v.m.add_cube(name,loc,scale,M['body_dark'],.006);o['OLEANDER_AUTHORITY']='DERIVED_EXECUTION_NOT_AUTHORITY';out.append(o)
    return out
v.build_glass=glass37

# Finite endpoint screening + V37 candidate labels.
def projection37():
    d=base_projection();d['candidate_revision']=REV;d['primary_form_stage']='CAUSAL_SECTION_REAL_GLASS_PRIMARY_HULL';finite=[];total=0
    for s in d.get('side_upper_samples',[]):
        total+=1;e=s.get('top_error_m')
        if isinstance(e,(int,float)) and math.isfinite(float(e)):finite.append(float(e))
    cov=len(finite)/max(1,total);rmse=math.sqrt(sum(e*e for e in finite)/len(finite)) if finite else 9.0
    for m in d['metrics']:
        if m['id']=='SIDE_UPPER_EVALUATED_MESH_RMSE_M':m['candidate']=rmse;m['abs_error']=rmse;m['candidate_measurement_source']='V37_FINAL_EVALUATED_HULL_FINITE_INTERSECTIONS';m['finite_sample_coverage']=cov
        else:m['candidate_measurement_source']=str(m.get('candidate_measurement_source','')).replace('V34_','V37_')
    d['side_upper_finite_sample_coverage']=cov;d['greenhouse_target']='REFERENCE_GREENHOUSE_TARGETS_992_2.json';d['greenhouse_representation']='INDEPENDENT_GLASS_SURFACES';d['status']='PROJECTION_MACHINE_SCREENING_PASS' if cov>=.90 and all(math.isfinite(float(m['abs_error'])) and float(m['abs_error'])<=float(m['limit']) for m in d['metrics']) else 'PROJECTION_MACHINE_SCREENING_FAIL';return d
env['projection30']=projection37

def regression37(pr):
    d=base_regression(pr);d['candidate_revision']=REV;d['edit_scope']=['CAUSAL_REAR_FRONT_SECTION_BLEND','CAUSAL_HOOD_VALLEY','DENSE_LOWER_SIDE_RAILS','INDEPENDENT_CALIBRATED_GLASS'];d['visual_review_state']='NOT_RUN'
    if d.get('promotion_decision')=='PROMOTE_OVER_LKG':d['promotion_decision']='KEEP_LKG_HOLD_EXPERIMENT'
    return d
env['regression30']=regression37

def surface37():d=base_surface();d['revision']=REV;return d
env['surface_receipt']=surface37

def patch37(out):
    base_patch(out)
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if p.exists():
            d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='CAUSAL_SECTION_REAL_GLASS_PRIMARY_HULL';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def run37():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:env['run30']()
    except SystemExit as e:patch37(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch37(out)
run37()
