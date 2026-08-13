#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 — R29A M7 Secondary Geometry Benchmark.

Builds two secondary-geometry families from passed M6 routing/dependency architecture:
1. four wheelhouse liner meshes from canonical wheel HP centers;
2. one separated glazing shell from exactly REG-GLASSHOUSE routing faces.

R29A Source geometry/topology is locked. All dimensions introduced by M7 are explicitly
designer-estimate modeling-validation parameters, not engineering specifications.
"""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import bpy


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


m6=load('/tmp/revise_v011_r29a_m6.py','m6_for_m7')
r29a=m6.r29a
r25=m6.r25
r20=m6.r20
r16=m6.r16
r14=m6.r14
b=m6.b
hp=m6.hp

MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R29A_M7'
CANONICAL_SOURCE_HASH='d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb'
TARGET_OD=.700
WHEEL_RADIUS=TARGET_OD*.5
WHEELHOUSE_CLEARANCE=.055
WHEELHOUSE_RADIUS=WHEEL_RADIUS+WHEELHOUSE_CLEARANCE
WHEELHOUSE_OUTBOARD_EXTRA=.018
WHEELHOUSE_INBOARD_EXTRA=.073
GLAZING_THICKNESS=.004
GLAZING_SURFACE_OFFSET=.0015

for mod in (m6,r29a,r25,m6.r24,r20,m6.r18,r16,r16.r15,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):
    mod.MODEL=MODEL

hp.install(b,TARGET_OD)

EXPECTED_REGION_COUNTS={
    'REG-GLASSHOUSE':220,
    'REG-FRONT-FENDER-L':511,
    'REG-FRONT-FENDER-R':511,
    'REG-REAR-QUARTER-L':463,
    'REG-REAR-QUARTER-R':463,
    'REG-FRONT-TERMINATION':14,
    'REG-REAR-TERMINATION':14,
    'REG-BODY-MAIN-L':260,
    'REG-BODY-MAIN-R':260,
    'REG-UNDERBODY-CENTER':77,
}

SECONDARY_DEPENDENCIES={
    'SEC-WHEELHOUSE-FL':['REG-FRONT-FENDER-L','PKG-WHEEL-FL','CONTRACT-WHEEL-HP'],
    'SEC-WHEELHOUSE-FR':['REG-FRONT-FENDER-R','PKG-WHEEL-FR','CONTRACT-WHEEL-HP'],
    'SEC-WHEELHOUSE-RL':['REG-REAR-QUARTER-L','PKG-WHEEL-RL','CONTRACT-WHEEL-HP'],
    'SEC-WHEELHOUSE-RR':['REG-REAR-QUARTER-R','PKG-WHEEL-RR','CONTRACT-WHEEL-HP'],
    'SEC-GLAZING-SHELL':['REG-GLASSHOUSE','SEC-R09-R12-GREENHOUSE','SRC-R29A'],
}

AFFECTED_VIEWS={
    'SEC-WHEELHOUSE-FL':['PACKAGE_SIDE','HERO_FRONT_3Q','FRONT_ARCH_DETAIL'],
    'SEC-WHEELHOUSE-FR':['HERO_FRONT_3Q','FRONT_ARCH_DETAIL'],
    'SEC-WHEELHOUSE-RL':['PACKAGE_SIDE','HERO_REAR_3Q','REAR_ARCH_DETAIL'],
    'SEC-WHEELHOUSE-RR':['HERO_REAR_3Q','REAR_ARCH_DETAIL'],
    'SEC-GLAZING-SHELL':['PACKAGE_SIDE','HERO_FRONT_3Q','HERO_REAR_3Q','CLAY_STRIP','CLAY_GRAZING'],
}

VALID_IDS=set(m6.REGIONS)|{
    'PKG-WHEEL-FL','PKG-WHEEL-FR','PKG-WHEEL-RL','PKG-WHEEL-RR',
    'CONTRACT-WHEEL-HP','SEC-R09-R12-GREENHOUSE','SRC-R29A',
}


def topology_stats(source):
    tri=quad=ngon=0
    for p in source.data.polygons:
        n=len(p.vertices)
        if n==3:tri+=1
        elif n==4:quad+=1
        else:ngon+=1
    return {'vertices':len(source.data.vertices),'faces':len(source.data.polygons),'tri':tri,'quad':quad,'ngon':ngon}


def make_wheelhouse(name,center,side,material):
    cx,cy,cz=center
    # Use measured package center; Y span wraps over the tire volume and extends into
    # the body cavity. This is a benchmark envelope, not a production inner fender.
    outer_abs=abs(cy)+TARGET_OD*0.0+WHEELHOUSE_OUTBOARD_EXTRA+0.077
    inner_abs=abs(cy)-0.077-WHEELHOUSE_INBOARD_EXTRA
    y_outer=side*outer_abs
    y_inner=side*inner_abs
    angles=[math.radians(v) for v in range(15,166,5)]
    verts=[];faces=[]
    for a in angles:
        x=cx+WHEELHOUSE_RADIUS*math.cos(a)
        z=cz+WHEELHOUSE_RADIUS*math.sin(a)
        verts.append((x,y_outer,z));verts.append((x,y_inner,z))
    for i in range(len(angles)-1):
        k=2*i
        f=(k,k+2,k+3,k+1)
        faces.append(f if side>0 else tuple(reversed(f)))
    me=bpy.data.meshes.new(name+'_MESH')
    me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o)
    o.data.materials.append(material)
    for p in me.polygons:p.use_smooth=True
    o['OLEANDER_AUTHORITY']='SECONDARY_GEOMETRY_WORKING'
    o['OLEANDER_STAGE']='M7'
    o['OLEANDER_DEPENDENCIES']=json.dumps(SECONDARY_DEPENDENCIES[name])
    o['OLEANDER_WHEELHOUSE_RADIUS_M']=WHEELHOUSE_RADIUS
    o['OLEANDER_WHEELHOUSE_CLEARANCE_M']=WHEELHOUSE_CLEARANCE
    o['OLEANDER_PARAMETER_STATUS']='DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION'
    return o,{
        'id':name,
        'center':[cx,cy,cz],
        'side':side,
        'radius_m':WHEELHOUSE_RADIUS,
        'radial_clearance_m':WHEELHOUSE_CLEARANCE,
        'y_outer_m':y_outer,
        'y_inner_m':y_inner,
        'angle_range_deg':[15,165],
        'dependencies':SECONDARY_DEPENDENCIES[name],
        'affected_views':AFFECTED_VIEWS[name],
        'authority':'SECONDARY_GEOMETRY_WORKING',
        'parameter_status':'DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION',
    }


def extract_glazing_shell(source,assignments,material):
    glass_polys=[p for p,r in zip(source.data.polygons,assignments) if r=='REG-GLASSHOUSE']
    old_indices=[]
    seen=set()
    for p in glass_polys:
        for vi in p.vertices:
            if vi not in seen:
                seen.add(vi);old_indices.append(vi)
    mapping={old:i for i,old in enumerate(old_indices)}
    verts=[]
    for old in old_indices:
        sv=source.data.vertices[old]
        n=sv.normal.normalized() if sv.normal.length else sv.normal
        verts.append(tuple(sv.co+n*GLAZING_SURFACE_OFFSET))
    faces=[tuple(mapping[i] for i in p.vertices) for p in glass_polys]
    me=bpy.data.meshes.new('SEC_GLAZING_SHELL_MESH')
    me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new('SEC-GLAZING-SHELL',me);bpy.context.collection.objects.link(o)
    o.data.materials.append(material)
    for p in me.polygons:p.use_smooth=True
    raw_face_count=len(me.polygons)

    # Secondary-only thin shell. Source receives no modifier/cut.
    bpy.context.view_layer.objects.active=o
    o.select_set(True)
    solid=o.modifiers.new('M7_GLAZING_THICKNESS','SOLIDIFY')
    solid.thickness=GLAZING_THICKNESS
    solid.offset=-1.0
    bpy.ops.object.modifier_apply(modifier=solid.name)
    o.select_set(False)
    o['OLEANDER_AUTHORITY']='SECONDARY_GEOMETRY_WORKING'
    o['OLEANDER_STAGE']='M7'
    o['OLEANDER_DEPENDENCIES']=json.dumps(SECONDARY_DEPENDENCIES[o.name])
    o['OLEANDER_SOURCE_ROUTING_FACE_COUNT']=raw_face_count
    o['OLEANDER_GLAZING_THICKNESS_M']=GLAZING_THICKNESS
    o['OLEANDER_PARAMETER_STATUS']='DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION'
    return o,{
        'id':o.name,
        'source_routing_face_count':raw_face_count,
        'source_unique_vertex_count':len(old_indices),
        'result_vertices':len(o.data.vertices),
        'result_faces':len(o.data.polygons),
        'surface_offset_m':GLAZING_SURFACE_OFFSET,
        'thickness_m':GLAZING_THICKNESS,
        'dependencies':SECONDARY_DEPENDENCIES[o.name],
        'affected_views':AFFECTED_VIEWS[o.name],
        'authority':'SECONDARY_GEOMETRY_WORKING',
        'parameter_status':'DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION',
    }


def make_context_body(source,material):
    o=source.copy();o.data=source.data.copy();o.name='DERIVED_M7_BODY_CONTEXT';bpy.context.collection.objects.link(o)
    o.data.materials.clear();o.data.materials.append(material)
    for p in o.data.polygons:p.material_index=0;p.use_smooth=True
    o['OLEANDER_AUTHORITY']='NONE';o['OLEANDER_ROLE']='M7_CONTEXT_DIAGNOSTIC'
    return o


def render_views(out,samples,res,M,source,body_context,wheelhouses,glazing):
    b.ground(M);L=b.rigs();b.world((.015,.015,.015),.18)
    source.hide_render=True
    rd=out/'renders';rd.mkdir(parents=True,exist_ok=True)
    wheels=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('WHEEL_')]
    wh_by_name={o.name:o for o in wheelhouses}
    views=[
        ('M7_FRONT_WHEELHOUSE_NEARSIDE',(2.65,-3.4,.95),(b.FX,-b.WY,.48),100,False,5.0,'STRIP','FR'),
        ('M7_REAR_WHEELHOUSE_NEARSIDE',(-2.55,-3.4,.95),(b.RX,-b.WY,.48),100,False,5.0,'STRIP','RR'),
        ('M7_HERO_FRONT_SECONDARY',(6.2,-7.0,2.75),(.05,0,.66),78,False,5.0,'BROAD','ALL'),
        ('M7_HERO_REAR_SECONDARY',(-6.0,6.8,2.65),(-.10,0,.66),78,False,5.0,'BROAD','ALL'),
    ]
    records=[]
    for label,loc,target,lens,ortho,scale,rig,scope in views:
        b.setrig(L,rig)
        for w in wheels:
            if scope=='ALL':w.hide_render=False
            else:w.hide_render=(scope not in w.name)
        for wh in wheelhouses:
            wh.hide_render=(scope!='ALL' and wh.name!=f'SEC-WHEELHOUSE-{scope}')
        glazing.hide_render=False
        body_context.hide_render=False
        cam=b.camera('CAM_'+label,loc,target,lens,ortho,scale);bpy.context.scene.camera=cam
        p=rd/f'{MODEL}__{label}.png';b.setup(p,samples,res);bpy.ops.render.render(write_still=True)
        records.append({'view':label,'file':str(p),'scope':scope,'authority':'DIAGNOSTIC_ONLY'})
        bpy.data.objects.remove(cam,do_unlink=True)
    for w in wheels:w.hide_render=False
    for wh in wheelhouses:wh.hide_render=False
    source.hide_render=False
    return records


def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
    b.clear();M=b.materials();glass=r14.diagnostic_glass();rows=b.controls_resampled()

    source,xs,cols,arch_meta,reuse=r29a.build_source_r29a(rows,M,glass)
    source.name='PRIMARY_R29A_M7_LOCKED_SOURCE'
    hash_before=r20.shape_hash(source);stats_before=topology_stats(source);islands_before=r16.island_count(source)
    assignments,region_counts=m6.classify_regions(source);m6.add_region_attribute(source,assignments)
    source.data.update();bpy.context.view_layer.update()
    hash_after_m6=r20.shape_hash(source)

    # Exact package components first; all M7 wheelhouse centers come from these records.
    b.wheels(M)
    wheel_records=getattr(b,'_OLEANDER_WHEEL_HP_RECORDS',[])
    wheel_exact=bool(getattr(b,'_OLEANDER_WHEEL_HP_EXACT',False)) and hp.package_exact(wheel_records,TARGET_OD)
    record_by_code={r['wheel_code']:r for r in wheel_records}

    mat_wh=b.mat('M7_SECONDARY_WHEELHOUSE',(.18,.46,.68,1),.42)
    mat_glass=b.mat('M7_SECONDARY_GLAZING',(.035,.14,.22,1),.18)
    mat_body=b.mat('M7_CONTEXT_BODY',(.36,.37,.39,1),.62)

    specs=[('FL',1),('FR',-1),('RL',1),('RR',-1)]
    wheelhouses=[];wheelhouse_manifest=[]
    for code,side in specs:
        rec=record_by_code[code]
        o,meta=make_wheelhouse('SEC-WHEELHOUSE-'+code,rec['target_center'],side,mat_wh)
        wheelhouses.append(o);wheelhouse_manifest.append(meta)

    glazing,glazing_manifest=extract_glazing_shell(source,assignments,mat_glass)
    body_context=make_context_body(source,mat_body)

    hash_after_secondary=r20.shape_hash(source);stats_after=topology_stats(source);islands_after=r16.island_count(source)
    renders=render_views(out,max(2,min(a.samples,4)),min(a.resolution,512),M,source,body_context,wheelhouses,glazing)
    hash_after_render=r20.shape_hash(source)

    secondary_ids=[m['id'] for m in wheelhouse_manifest]+[glazing_manifest['id']]
    deps_resolve=all(d in VALID_IDS for deps in SECONDARY_DEPENDENCIES.values() for d in deps)
    centers_exact=True
    for meta in wheelhouse_manifest:
        code=meta['id'].split('-')[-1];target=record_by_code[code]['target_center']
        centers_exact &= all(abs(a-bv)<1e-9 for a,bv in zip(meta['center'],target))
    clearance_exact=all(abs(m['radial_clearance_m']-WHEELHOUSE_CLEARANCE)<1e-9 for m in wheelhouse_manifest)
    all_secondary_authority=all(o.get('OLEANDER_AUTHORITY')=='SECONDARY_GEOMETRY_WORKING' for o in wheelhouses+[glazing])
    source_authority_clean=source.get('OLEANDER_AUTHORITY')!='SECONDARY_GEOMETRY_WORKING'
    selective_views_complete=set(AFFECTED_VIEWS)==set(secondary_ids)

    checks={
        'canonical_source_hash_before':hash_before==CANONICAL_SOURCE_HASH,
        'source_hash_stable_m6_annotations':hash_after_m6==hash_before,
        'source_hash_stable_secondary_build':hash_after_secondary==hash_before,
        'source_hash_stable_after_render':hash_after_render==hash_before,
        'source_topology_stable':stats_before==stats_after,
        'source_island_one':islands_before==1 and islands_after==1,
        'source_termination_triangles_four':stats_after['tri']==4,
        'source_ngon_zero':stats_after['ngon']==0,
        'm6_region_assignments_exact':region_counts==EXPECTED_REGION_COUNTS,
        'wheel_hp_package_exact':wheel_exact and len(wheel_records)==4,
        'wheelhouse_count_four':len(wheelhouses)==4,
        'wheelhouse_centers_exact':centers_exact,
        'wheelhouse_clearance_declared':clearance_exact,
        'wheelhouse_dependencies_resolve':deps_resolve,
        'glazing_source_faces_220':glazing_manifest['source_routing_face_count']==EXPECTED_REGION_COUNTS['REG-GLASSHOUSE'],
        'glazing_separate_object':glazing is not source and glazing.data is not source.data,
        'secondary_ids_unique':len(secondary_ids)==len(set(secondary_ids))==5,
        'all_secondary_authority_correct':all_secondary_authority,
        'source_not_secondary_authority':source_authority_clean,
        'selective_affected_views_complete':selective_views_complete,
        'diagnostic_render_matrix':len(renders)==4,
    }
    status='MACHINE_PASS_HUMAN_M7_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL'

    architecture={
        'schema':'oleander.auto.v0.11.m7.secondary-geometry.v1',
        'model':MODEL,'stage':'M7','status':status,
        'source_authority':'R29A_M5_PRIMARY_GEOMETRY','source_hash':hash_before,
        'm6_region_counts':region_counts,
        'wheelhouse_parameters':{'wheel_radius_m':WHEEL_RADIUS,'clearance_m':WHEELHOUSE_CLEARANCE,'liner_radius_m':WHEELHOUSE_RADIUS,'status':'DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION'},
        'glazing_parameters':{'thickness_m':GLAZING_THICKNESS,'surface_offset_m':GLAZING_SURFACE_OFFSET,'status':'DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION'},
        'secondary_components':wheelhouse_manifest+[glazing_manifest],
        'boundary':'Secondary geometry benchmark only; no production wheelhouse, glazing certification, sealing, fastening or manufacturing authority.',
        'blocked':['M8 pending Human M7 review'],
    }
    (out/'M7_SECONDARY_GEOMETRY.json').write_text(json.dumps(architecture,ensure_ascii=False,indent=2)+'\n')

    qa={
        'schema':'oleander.auto.v0.11.m7.qa.v1','model':MODEL,'stage':'M7','status':status,
        'checks':checks,'source_hash_before':hash_before,'source_hash_after':hash_after_render,
        'topology_before':stats_before,'topology_after':stats_after,'region_counts':region_counts,
        'wheel_hp_package':wheel_records,'secondary_ids':secondary_ids,'renders':renders,
        'human_review_required':['wheelhouse/opening relation','wheelhouse exterior protrusion','glazing alignment/tearing','secondary-vs-source hierarchy','occlusion','scale/proportion','cropping/framing'],
    }
    (out/'M7_SECONDARY_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')

    blend=out/'R29A_M7_SECONDARY_GEOMETRY.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    receipt={'schema':'oleander.auto.v0.11.m7.receipt.v1','model':MODEL,'blender_version':bpy.app.version_string,'status':'EXECUTED_'+status,'blend':str(blend),'qa':str(out/'M7_SECONDARY_QA.json'),'architecture':str(out/'M7_SECONDARY_GEOMETRY.json'),'renders':renders}
    (out/'M7_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':status,'source_hash':hash_before,'checks':checks,'secondary_ids':secondary_ids},ensure_ascii=False,indent=2))
    raise SystemExit(0 if status.startswith('MACHINE_PASS') else 5)


if __name__=='__main__':
    main()
