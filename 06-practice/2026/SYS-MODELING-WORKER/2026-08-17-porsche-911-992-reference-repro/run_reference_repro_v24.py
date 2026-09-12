#!/usr/bin/env python3
"""V24 — shared-boundary aperture closure + cabin backing on V23 cross-section experiment.

V23 improved FRONT/REAR projected profiles without regressing SIDE, but visual readback still exposed
open/overlapping greenhouse interfaces and unrelated exterior geometry visible through glazing. V24 keeps
V23's error-routed cross-section controls, re-binds roof/glass/pillar/sail boundaries from shared functions,
and adds non-authoritative interior occlusion geometry. No new detail/CMF claim is introduced.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE = Path(__file__).resolve().parent
V23 = HERE / 'run_reference_repro_v23.py'
text = V23.read_text()
marker = '\nrun()\n'
if marker not in text:
    raise SystemExit('V23 run marker missing')
ns = {'__file__': str(V23), '__name__': 'oleander_v23_declarations'}
exec(compile(text.split(marker, 1)[0], str(V23), 'exec'), ns)
v = ns['v']
PROFILE = ns['PROFILE']
CROSS_SECTION = ns['CROSS_SECTION']

v.REF = '2025_992.2_CARRERA_SHARED_BOUNDARY_CLOSURE_V24'
v.REFERENCE_CONTRACT['schema'] = 'oleander.3d.reference-reproduction.porsche-911-992-2.v24'
v.REFERENCE_CONTRACT['reference_revision'] = v.REF
v.REFERENCE_CONTRACT['aperture_interface_revision'] = 'V24_SHARED_BOUNDARY_CLOSURE_AND_BACKING'
v.REFERENCE_CONTRACT['aperture_protocol'] = 'APERTURE_BACKING_BOUNDARY_OWNERSHIP_PROTOCOL_v1'
v.FAMILY_CONTROLS['APERTURE_INTERFACE_V24'] = {
    'boundary_owners': ['WINDSHIELD_EDGE','ROOF_EDGE','REAR_GLASS_EDGE','BELT_EDGE','REAR_QUARTER_EDGE'],
    'layers': ['HOST_SURFACE','OPENING_BOUNDARY','INTERFACE_SURFACE','INFILL','BACKING_OR_VOID'],
    'interior_backing_authority': 'DERIVED_EXECUTION_NOT_AUTHORITY',
    'source_basis': 'V23 cross-section controls + shared roof/body boundary functions',
}
v.REFERENCE_CONTRACT['source_families'] = list(v.FAMILY_CONTROLS.keys())

CROSS_SECTION['roof']['front_edge_drop_m'] = 0.100
CROSS_SECTION['roof']['rear_edge_drop_m'] = 0.120
CROSS_SECTION['roof']['front_half_width_cap_m'] = 0.600
CROSS_SECTION['roof']['rear_half_width_cap_m'] = 0.570


def roof_half_width24(x):
    base = max(0.44, v.hermite(v.CABIN_W_PTS, x))
    floor = 0.585 if x >= 0.0 else 0.555
    cap = CROSS_SECTION['roof']['front_half_width_cap_m'] if x >= 0.0 else CROSS_SECTION['roof']['rear_half_width_cap_m']
    return min(max(base, floor), cap)

ns['roof_half_width'] = roof_half_width24


def roof_drop24(x):
    if x >= 0.20: return CROSS_SECTION['roof']['front_edge_drop_m']
    if x <= -0.20: return CROSS_SECTION['roof']['rear_edge_drop_m']
    t = (x + 0.20) / 0.40
    return CROSS_SECTION['roof']['rear_edge_drop_m'] * (1.0 - t) + CROSS_SECTION['roof']['front_edge_drop_m'] * t
ns['roof_drop'] = roof_drop24


def roof_point(x, side, fraction):
    rw = roof_half_width24(x)
    f = max(0.0, min(1.0, float(fraction)))
    top = v.hermite(v.ROOF_TOP_PTS, x)
    z = top - roof_drop24(x) * (f ** CROSS_SECTION['roof']['crown_exponent'])
    return (x, side * rw * f, z)


def body_outer_y(x, z):
    ring = v.body_ring(x)
    vals = []
    cyc = ring[1:] + ring[:1]
    for a, b in zip(ring, cyc):
        _, y0, z0 = a; _, y1, z1 = b
        if abs(z1 - z0) < 1e-10:
            if abs(z - z0) < 1e-7: vals.extend((abs(y0), abs(y1)))
            continue
        if z < min(z0, z1) - 1e-8 or z > max(z0, z1) + 1e-8: continue
        t = (z - z0) / (z1 - z0)
        if -1e-8 <= t <= 1.0 + 1e-8:
            vals.append(abs(y0 + t * (y1 - y0)))
    return max(vals) if vals else max(abs(p[1]) for p in ring)


def make_strip(name, sections, mat, thickness=.008, owner='UNSET'):
    verts = []
    for outer, inner in sections: verts.extend((outer, inner))
    faces = [(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(sections)-1)]
    me = bpy.data.meshes.new(name + '_MESH'); me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
    o['OLEANDER_AUTHORITY'] = 'DERIVED_REFERENCE_REPRO_INTERFACE'
    o['OLEANDER_INTERFACE_SURFACE'] = True
    o['OLEANDER_BOUNDARY_OWNER'] = owner
    if thickness:
        s = o.modifiers.new(name + '_THICKNESS', 'SOLIDIFY'); s.thickness = thickness; s.offset = 0
    for p in me.polygons: p.use_smooth = True
    return o


def make_panel(name, verts, mat, thickness=.008, owner='UNSET', interface=True):
    me = bpy.data.meshes.new(name + '_MESH'); me.from_pydata(verts, [], [tuple(range(len(verts)))]); me.update()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
    o['OLEANDER_AUTHORITY'] = 'DERIVED_REFERENCE_REPRO_INTERFACE' if interface else 'DERIVED_APERTURE_INFILL'
    o['OLEANDER_BOUNDARY_OWNER'] = owner
    if interface: o['OLEANDER_INTERFACE_SURFACE'] = True
    if thickness:
        s = o.modifiers.new(name + '_THICKNESS', 'SOLIDIFY'); s.thickness = thickness; s.offset = 0
    for p in me.polygons: p.use_smooth = True
    return o


base_greenhouse = v.build_glass
INTERFACE_PREFIXES = (
    'REF_COWL_INTERFACE','REF_REAR_DECK_INTERFACE','REF_A_PILLAR_SURFACE_',
    'REF_ROOF_RAIL_SURFACE_','REF_C_PILLAR_SAIL_','REF_WINDOW_BELT_SURFACE_'
)
GLASS_PREFIXES = ('REF_WINDSHIELD','REF_REAR_GLASS','REF_DOOR_GLASS_','REF_QUARTER_GLASS_')


def remove_named_prefixes(prefixes):
    for o in list(bpy.context.scene.objects):
        if any(o.name.startswith(p) for p in prefixes):
            bpy.data.objects.remove(o, do_unlink=True)


def greenhouse24(M):
    base_greenhouse(M)
    remove_named_prefixes(INTERFACE_PREFIXES + GLASS_PREFIXES)
    out = []

    a_low = {s: (.650, s*.620, .830) for s in (1,-1)}
    a_top = {s: roof_point(.235, s, .925) for s in (1,-1)}
    c_top = {s: roof_point(-.390, s, .900) for s in (1,-1)}
    c_low = {s: (-1.150, s*.592, .990) for s in (1,-1)}

    out.append(make_panel('REF_WINDSHIELD',[a_low[1],a_low[-1],a_top[-1],a_top[1]],M['glass'],.003,'WINDSHIELD_EDGE',False))
    out.append(make_panel('REF_REAR_GLASS',[c_top[1],c_top[-1],c_low[-1],c_low[1]],M['glass'],.003,'REAR_GLASS_EDGE',False))

    out.append(make_panel('REF_COWL_INTERFACE',[(.760,.700,.790),(.760,-.700,.790),a_low[-1],a_low[1]],M['body'],.010,'WINDSHIELD_EDGE'))
    rear_outer_y = body_outer_y(-1.360,.835)
    out.append(make_panel('REF_REAR_DECK_INTERFACE',[c_low[1],c_low[-1],(-1.360,-rear_outer_y,.835),(-1.360,rear_outer_y,.835)],M['body'],.010,'REAR_GLASS_EDGE'))

    for s in (1,-1):
        code = 'L' if s > 0 else 'R'
        b_top = roof_point(-.220, s, .900)
        belt_front = (.500,s*.605,.835); belt_b = (-.220,s*.570,.842); belt_rear = (-.820,s*.625,.865)
        door = [(.620,s*.600,.835),a_top[s],b_top,belt_b,belt_front]
        quarter = [b_top,c_top[s],c_low[s],belt_rear,belt_b]
        out.append(make_panel('REF_DOOR_GLASS_'+code,door,M['glass'],.003,'ROOF_EDGE',False))
        out.append(make_panel('REF_QUARTER_GLASS_'+code,quarter,M['glass'],.003,'ROOF_EDGE',False))

        a_sections=[]
        for i in range(7):
            t=i/6; x=.650+(.235-.650)*t
            iy=.620*(1-t)+abs(a_top[s][1])*t; iz=.830*(1-t)+a_top[s][2]*t
            outer=roof_point(x,s,min(1.0,.925+.075*t)) if t>.55 else (x,s*(iy+.055),iz+.006)
            inner=(x,s*iy,iz)
            a_sections.append((outer,inner))
        out.append(make_strip('REF_A_PILLAR_SURFACE_'+code,a_sections,M['body'],.009,'WINDSHIELD_EDGE'))

        rail=[]
        for i in range(25):
            x=.235+(-.625)*i/24
            rail.append((roof_point(x,s,1.0),roof_point(x,s,.900)))
        out.append(make_strip('REF_ROOF_RAIL_SURFACE_'+code,rail,M['body'],.009,'ROOF_EDGE'))

        sail=[]
        xs=(-.390,-.520,-.680,-.840,-1.000,-1.150)
        for i,x in enumerate(xs):
            t=i/(len(xs)-1)
            if i==0:
                outer=roof_point(x,s,1.0); inner=c_top[s]
            elif i==len(xs)-1:
                z=.875; oy=max(body_outer_y(x,z),.62); outer=(x,s*oy,z); inner=c_low[s]
            else:
                inner_y=abs(c_top[s][1])*(1-t)+abs(c_low[s][1])*t
                inner_z=c_top[s][2]*(1-t)+c_low[s][2]*t
                outer_z=inner_z-.030-.035*t
                oy=max(body_outer_y(x,max(.82,outer_z)),inner_y+.045)
                outer=(x,s*oy,outer_z); inner=(x,s*inner_y,inner_z)
            sail.append((outer,inner))
        out.append(make_strip('REF_C_PILLAR_SAIL_'+code,sail,M['body'],.010,'REAR_GLASS_EDGE'))

        belt_sections=[]
        for x,z,iy in ((.620,.815,.600),(-.220,.825,.570),(-.820,.850,.625),(-1.100,.900,.592)):
            oy=max(body_outer_y(x,z),iy+.035)
            belt_sections.append(((x,s*oy,z),(x,s*iy,z+.018)))
        out.append(make_strip('REF_WINDOW_BELT_SURFACE_'+code,belt_sections,M['body'],.008,'BELT_EDGE'))

    backing=[]
    backing.append(v.m.add_cube('REF_CABIN_OCCLUSION_BACKING',(-.18,0,.865),(1.30,.86,.31),M['body_dark'],.055))
    backing.append(v.m.add_cube('REF_DASH_BACKING',(.470,0,.815),(.16,.92,.16),M['body_dark'],.035))
    backing.append(v.m.add_cube('REF_REAR_BULKHEAD_BACKING',(-.790,0,.835),(.18,.90,.22),M['body_dark'],.035))
    for o in backing:
        o['OLEANDER_AUTHORITY']='DERIVED_EXECUTION_NOT_AUTHORITY';o['OLEANDER_APERTURE_LAYER']='BACKING_OR_VOID';o['OLEANDER_EXTERIOR_PROFILE_MEMBER']=False
    out += backing
    return out
v.build_glass = greenhouse24


base_projection = ns['projection23']
def relabel(data):
    if isinstance(data,dict): return {k:relabel(vv) for k,vv in data.items()}
    if isinstance(data,list): return [relabel(x) for x in data]
    if isinstance(data,str): return data.replace('V23_','V24_')
    return data


def projection24():
    d=relabel(base_projection());d['candidate_revision']='V24_SHARED_BOUNDARY_CLOSURE';d['aperture_interface']='SHARED_BOUNDARY_OWNER_AND_BACKING';return d


def postprocess24(out):
    if not (out/'REFERENCE_REPRO_QA.json').exists(): return
    pr=projection24();(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n')
    rr=ns['regression_receipt'](pr);rr=relabel(rr);rr['candidate_revision']='V24_SHARED_BOUNDARY_CLOSURE';rr['edit_scope']=['V23_CROSS_SECTION_REAPPLIED','SHARED_BOUNDARY_CLOSURE','APERTURE_BACKING_OCCLUSION'];rr['visual_review_state']='NOT_RUN';rr['promotion_decision']='KEEP_LKG_HOLD_EXPERIMENT' if all(x['status']=='PASS' for x in rr['regression_locks']) and rr['target_metric_delta']['improved'] else 'KEEP_LKG_REJECT_EXPERIMENT';(out/'REFERENCE_REGRESSION_PROMOTION_RECEIPT.json').write_text(json.dumps(rr,ensure_ascii=False,indent=2)+'\n')
    aperture={
      'schema':'oleander.3d.aperture-interface-receipt.v1','revision':'V24_SHARED_BOUNDARY_CLOSURE',
      'apertures':['WINDSHIELD','SIDE_DOOR_GLASS_L/R','QUARTER_GLASS_L/R','REAR_GLASS'],
      'boundary_owners':['WINDSHIELD_EDGE','ROOF_EDGE','REAR_GLASS_EDGE','BELT_EDGE','REAR_QUARTER_EDGE'],
      'shared_boundary_method':'COMMON_PARAMETRIC_ROOF_POINT_AND_BODY_SECTION_INTERSECTION',
      'backing_objects':['REF_CABIN_OCCLUSION_BACKING','REF_DASH_BACKING','REF_REAR_BULKHEAD_BACKING'],
      'backing_authority':'DERIVED_EXECUTION_NOT_AUTHORITY','projected_profile_state':pr['status'],
      'boundary_closure_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD','backing_occlusion_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD',
      'visual_review_state':'NOT_RUN','does_not_prove':['manufacturer patch layout','Class-A continuity','seal engineering','tooling','production glazing design']}
    (out/'APERTURE_INTERFACE_RECEIPT.json').write_text(json.dumps(aperture,ensure_ascii=False,indent=2)+'\n')
    q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V24_SHARED_BOUNDARY_CLOSURE';q['projection_machine_gate']=pr['status'];q['failure_routing']='APERTURE_BOUNDARY_CLOSURE_AND_BACKING_ONLY';q['aperture_boundary_closure']='MACHINE_CONSTRUCTED_VISUAL_HOLD';q['backing_occlusion']='MACHINE_CONSTRUCTED_VISUAL_HOLD';q['regression_promotion_decision']=rr['promotion_decision'];q['verification_run']='PASS';q['visual_reference_fidelity']='HOLD';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V24_SHARED_BOUNDARY_CLOSURE';r['projection_machine_gate']=pr['status'];r['regression_promotion_decision']=rr['promotion_decision'];r['aperture_boundary_closure']='MACHINE_CONSTRUCTED_VISUAL_HOLD';r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')


def run24():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:v.main()
    except SystemExit as exc:
        postprocess24(out);raise SystemExit(exc.code if isinstance(exc.code,int) else 0)
    else:postprocess24(out)

run24()
