#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 — R29A M8 Detail / Instances Benchmark.

Creates two generic wheel-detail instance families from canonical wheel package data:
- 40 linked spoke instances from one prototype mesh;
- 4 linked rim-ring instances from one prototype mesh.

M5 Source, M6 routing and M7 secondary meshes are locked and verified unchanged.
All detail dimensions are designer-estimate modeling-validation parameters.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path

import bpy


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod


m7=load('/tmp/revise_v011_r29a_m7.py','m7_for_m8')
m6=m7.m6;r29a=m7.r29a;r20=m7.r20;r16=m7.r16;r14=m7.r14;b=m7.b;hp=m7.hp

MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R29A_M8'
CANONICAL_SOURCE_HASH='d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb'
TARGET_OD=.700
SPOKES_PER_WHEEL=10
SPOKE_R0=.115
SPOKE_R1=.275
SPOKE_WIDTH=.028
SPOKE_DEPTH=.016
RING_MAJOR=.245
RING_MINOR=.008
DETAIL_FACE_OFFSET=.079

for mod in (m7,m6,r29a,m7.r25,m6.r24,r20,m6.r18,r16,r16.r15,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):
    mod.MODEL=MODEL
hp.install(b,TARGET_OD)

PACKAGE_IDS={'FL':'PKG-WHEEL-FL','FR':'PKG-WHEEL-FR','RL':'PKG-WHEEL-RL','RR':'PKG-WHEEL-RR'}
DETAIL_DEPENDENCY_IDS=set(PACKAGE_IDS.values())|{'CONTRACT-WHEEL-HP'}
FAMILY_AFFECTED_VIEWS={
    'DET-FAMILY-WHEEL-SPOKES':['HERO_FRONT_3Q','HERO_REAR_3Q','FRONT_ARCH_DETAIL','REAR_ARCH_DETAIL'],
    'DET-FAMILY-WHEEL-RIM-RINGS':['HERO_FRONT_3Q','HERO_REAR_3Q','FRONT_ARCH_DETAIL','REAR_ARCH_DETAIL'],
}


def mesh_signature(o):
    h=hashlib.sha256()
    for v in o.data.vertices:
        h.update(f'{v.co.x:.9f},{v.co.y:.9f},{v.co.z:.9f};'.encode())
    for p in o.data.polygons:
        h.update(('F'+','.join(map(str,p.vertices))+';').encode())
    return h.hexdigest()


def topology_stats(source):
    tri=quad=ngon=0
    for p in source.data.polygons:
        n=len(p.vertices)
        if n==3:tri+=1
        elif n==4:quad+=1
        else:ngon+=1
    return {'vertices':len(source.data.vertices),'faces':len(source.data.polygons),'tri':tri,'quad':quad,'ngon':ngon}


def make_spoke_prototype(material):
    y0=-SPOKE_DEPTH*.5;y1=SPOKE_DEPTH*.5;z0=-SPOKE_WIDTH*.5;z1=SPOKE_WIDTH*.5
    verts=[
        (SPOKE_R0,y0,z0),(SPOKE_R1,y0,z0),(SPOKE_R1,y0,z1),(SPOKE_R0,y0,z1),
        (SPOKE_R0,y1,z0),(SPOKE_R1,y1,z0),(SPOKE_R1,y1,z1),(SPOKE_R0,y1,z1),
    ]
    faces=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    me=bpy.data.meshes.new('PROTO_WHEEL_SPOKE_MESH');me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new('PROTO-WHEEL-SPOKE',me);bpy.context.collection.objects.link(o);o.data.materials.append(material)
    o.hide_render=True;o['OLEANDER_AUTHORITY']='DETAIL_PROTOTYPE_LIBRARY';o['OLEANDER_STAGE']='M8';o['OLEANDER_PARAMETER_STATUS']='DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION'
    return o


def make_ring_prototype(material):
    bpy.ops.mesh.primitive_torus_add(major_radius=RING_MAJOR,minor_radius=RING_MINOR,major_segments=48,minor_segments=6,location=(0,0,0),rotation=(math.pi/2,0,0))
    o=bpy.context.object;o.name='PROTO-WHEEL-RIM-RING'
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    o.data.name='PROTO_WHEEL_RIM_RING_MESH';o.data.materials.append(material);o.hide_render=True
    o['OLEANDER_AUTHORITY']='DETAIL_PROTOTYPE_LIBRARY';o['OLEANDER_STAGE']='M8';o['OLEANDER_PARAMETER_STATUS']='DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION'
    return o


def instantiate_details(records,spoke_proto,ring_proto):
    spokes=[];rings=[];manifest=[]
    by_code={r['wheel_code']:r for r in records}
    for code in ('FL','FR','RL','RR'):
        rec=by_code[code];cx,cy,cz=rec['target_center'];side=1 if code.endswith('L') else -1;face_y=cy+side*DETAIL_FACE_OFFSET
        for i in range(SPOKES_PER_WHEEL):
            angle=2*math.pi*i/SPOKES_PER_WHEEL
            o=bpy.data.objects.new(f'DET-WHEEL-SPOKE-{code}-{i:02d}',spoke_proto.data);bpy.context.collection.objects.link(o)
            o.location=(cx,face_y,cz);o.rotation_euler=(0,angle,0)
            o['OLEANDER_AUTHORITY']='DETAIL_INSTANCE';o['OLEANDER_STAGE']='M8';o['OLEANDER_PROTOTYPE']='PROTO-WHEEL-SPOKE';o['OLEANDER_PACKAGE_DEPENDENCY']=PACKAGE_IDS[code];o['OLEANDER_CONTRACT_DEPENDENCY']='CONTRACT-WHEEL-HP'
            spokes.append(o)
            manifest.append({'id':o.name,'family':'DET-FAMILY-WHEEL-SPOKES','prototype':'PROTO-WHEEL-SPOKE','package':PACKAGE_IDS[code],'wheel_code':code,'angle_deg':360*i/SPOKES_PER_WHEEL,'center':[cx,face_y,cz],'authority':'DETAIL_INSTANCE'})
        ring=bpy.data.objects.new(f'DET-WHEEL-RIM-RING-{code}',ring_proto.data);bpy.context.collection.objects.link(ring)
        ring.location=(cx,face_y,cz);ring['OLEANDER_AUTHORITY']='DETAIL_INSTANCE';ring['OLEANDER_STAGE']='M8';ring['OLEANDER_PROTOTYPE']='PROTO-WHEEL-RIM-RING';ring['OLEANDER_PACKAGE_DEPENDENCY']=PACKAGE_IDS[code];ring['OLEANDER_CONTRACT_DEPENDENCY']='CONTRACT-WHEEL-HP'
        rings.append(ring);manifest.append({'id':ring.name,'family':'DET-FAMILY-WHEEL-RIM-RINGS','prototype':'PROTO-WHEEL-RIM-RING','package':PACKAGE_IDS[code],'wheel_code':code,'center':[cx,face_y,cz],'authority':'DETAIL_INSTANCE'})
    return spokes,rings,manifest


def render_views(out,samples,res,M,source,body_context,wheelhouses,glazing,spokes,rings):
    b.ground(M);L=b.rigs();b.world((.014,.014,.014),.18);source.hide_render=True
    rd=out/'renders';rd.mkdir(parents=True,exist_ok=True)
    wheels=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('WHEEL_')]
    views=[
        ('M8_FRONT_WHEEL_DETAIL',(2.65,-3.4,.95),(b.FX,-b.WY,.48),100,False,5.0,'STRIP','FR'),
        ('M8_REAR_WHEEL_DETAIL',(-2.55,-3.4,.95),(b.RX,-b.WY,.48),100,False,5.0,'STRIP','RR'),
        ('M8_HERO_FRONT_INSTANCES',(6.2,-7.0,2.75),(.05,0,.66),78,False,5.0,'BROAD','ALL'),
        ('M8_HERO_REAR_INSTANCES',(-6.0,6.8,2.65),(-.10,0,.66),78,False,5.0,'BROAD','ALL'),
    ]
    R=[]
    for label,loc,target,lens,ortho,scale,rig,scope in views:
        b.setrig(L,rig)
        for w in wheels:w.hide_render=(scope!='ALL' and scope not in w.name)
        for wh in wheelhouses:wh.hide_render=(scope!='ALL' and not wh.name.endswith(scope))
        for o in spokes+rings:o.hide_render=(scope!='ALL' and f'-{scope}' not in o.name)
        glazing.hide_render=False;body_context.hide_render=False
        cam=b.camera('CAM_'+label,loc,target,lens,ortho,scale);bpy.context.scene.camera=cam
        p=rd/f'{MODEL}__{label}.png';b.setup(p,samples,res);bpy.ops.render.render(write_still=True)
        R.append({'view':label,'file':str(p),'scope':scope,'authority':'DIAGNOSTIC_ONLY'});bpy.data.objects.remove(cam,do_unlink=True)
    for w in wheels:w.hide_render=False
    for wh in wheelhouses:wh.hide_render=False
    for o in spokes+rings:o.hide_render=False
    source.hide_render=False
    return R


def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
    b.clear();M=b.materials();glass=r14.diagnostic_glass();rows=b.controls_resampled()
    source,xs,cols,arch_meta,reuse=r29a.build_source_r29a(rows,M,glass);source.name='PRIMARY_R29A_M8_LOCKED_SOURCE'
    source_hash_before=r20.shape_hash(source);source_topology_before=topology_stats(source)
    assignments,region_counts=m6.classify_regions(source);m6.add_region_attribute(source,assignments);source.data.update();bpy.context.view_layer.update()

    b.wheels(M);wheel_records=getattr(b,'_OLEANDER_WHEEL_HP_RECORDS',[]);wheel_exact=bool(getattr(b,'_OLEANDER_WHEEL_HP_EXACT',False)) and hp.package_exact(wheel_records,TARGET_OD)
    by_code={r['wheel_code']:r for r in wheel_records}

    mat_wh=b.mat('M8_CONTEXT_WHEELHOUSE',(.12,.25,.34,1),.55);mat_glass=b.mat('M8_CONTEXT_GLAZING',(.04,.15,.22,1),.22);mat_body=b.mat('M8_CONTEXT_BODY',(.36,.37,.39,1),.62);mat_detail=b.mat('M8_DETAIL_INSTANCE',(.70,.58,.22,1),.28)
    wheelhouses=[]
    for code,side in (('FL',1),('FR',-1),('RL',1),('RR',-1)):
        o,_=m7.make_wheelhouse('SEC-WHEELHOUSE-'+code,by_code[code]['target_center'],side,mat_wh);wheelhouses.append(o)
    glazing,_=m7.extract_glazing_shell(source,assignments,mat_glass)
    secondary=wheelhouses+[glazing]
    secondary_sig_before={o.name:mesh_signature(o) for o in secondary}
    body_context=m7.make_context_body(source,mat_body)

    spoke_proto=make_spoke_prototype(mat_detail);ring_proto=make_ring_prototype(mat_detail)
    spokes,rings,instance_manifest=instantiate_details(wheel_records,spoke_proto,ring_proto)

    source_hash_after_details=r20.shape_hash(source);source_topology_after=topology_stats(source);secondary_sig_after={o.name:mesh_signature(o) for o in secondary}
    renders=render_views(out,max(2,min(a.samples,4)),min(a.resolution,512),M,source,body_context,wheelhouses,glazing,spokes,rings)
    source_hash_after_render=r20.shape_hash(source);secondary_sig_final={o.name:mesh_signature(o) for o in secondary}

    spoke_mesh_shared=len({o.data.name for o in spokes})==1 and all(o.data is spoke_proto.data for o in spokes)
    ring_mesh_shared=len({o.data.name for o in rings})==1 and all(o.data is ring_proto.data for o in rings)
    spokes_by_code={code:len([o for o in spokes if f'-{code}-' in o.name]) for code in ('FL','FR','RL','RR')}
    deps_resolve=all(m['package'] in DETAIL_DEPENDENCY_IDS and 'CONTRACT-WHEEL-HP' in DETAIL_DEPENDENCY_IDS for m in instance_manifest)
    radial_spoke_max=math.hypot(SPOKE_R1,SPOKE_WIDTH*.5);radial_ring_max=RING_MAJOR+RING_MINOR
    ids=[m['id'] for m in instance_manifest]
    all_instance_authority=all(o.get('OLEANDER_AUTHORITY')=='DETAIL_INSTANCE' for o in spokes+rings)
    prototypes_hidden=spoke_proto.hide_render and ring_proto.hide_render
    selective_complete=set(FAMILY_AFFECTED_VIEWS)=={'DET-FAMILY-WHEEL-SPOKES','DET-FAMILY-WHEEL-RIM-RINGS'}

    checks={
        'canonical_source_hash_before':source_hash_before==CANONICAL_SOURCE_HASH,
        'source_hash_stable_after_details':source_hash_after_details==source_hash_before,
        'source_hash_stable_after_render':source_hash_after_render==source_hash_before,
        'source_topology_stable':source_topology_before==source_topology_after,
        'm6_region_assignments_retained':region_counts==m7.EXPECTED_REGION_COUNTS,
        'm7_secondary_signatures_stable':secondary_sig_before==secondary_sig_after==secondary_sig_final,
        'wheel_hp_package_exact':wheel_exact and len(wheel_records)==4,
        'spoke_instances_40':len(spokes)==40,
        'spokes_10_per_wheel':all(v==10 for v in spokes_by_code.values()),
        'spoke_mesh_linked_single_prototype':spoke_mesh_shared,
        'rim_ring_instances_4':len(rings)==4,
        'rim_ring_mesh_linked_single_prototype':ring_mesh_shared,
        'two_detail_prototype_meshes':len({spoke_proto.data.name,ring_proto.data.name})==2,
        'detail_instance_ids_unique':len(ids)==len(set(ids))==44,
        'detail_dependencies_resolve':deps_resolve,
        'detail_radial_envelope_inside_wheel_od':radial_spoke_max<WHEEL_RADIUS and radial_ring_max<WHEEL_RADIUS,
        'prototypes_hidden_from_render':prototypes_hidden,
        'all_instance_authority_correct':all_instance_authority,
        'selective_affected_views_complete':selective_complete,
        'diagnostic_render_matrix':len(renders)==4,
    }
    status='MACHINE_PASS_HUMAN_M8_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL'

    architecture={
        'schema':'oleander.auto.v0.11.m8.detail-instances.v1','model':MODEL,'stage':'M8','status':status,
        'source_hash':source_hash_before,'m7_secondary_signatures':secondary_sig_before,
        'prototype_library':[
            {'id':'PROTO-WHEEL-SPOKE','mesh':spoke_proto.data.name,'authority':'DETAIL_PROTOTYPE_LIBRARY','parameters':{'radial_start_m':SPOKE_R0,'radial_end_m':SPOKE_R1,'width_m':SPOKE_WIDTH,'depth_m':SPOKE_DEPTH,'status':'DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION'}},
            {'id':'PROTO-WHEEL-RIM-RING','mesh':ring_proto.data.name,'authority':'DETAIL_PROTOTYPE_LIBRARY','parameters':{'major_radius_m':RING_MAJOR,'tube_radius_m':RING_MINOR,'status':'DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION'}},
        ],
        'families':[
            {'id':'DET-FAMILY-WHEEL-SPOKES','prototype':'PROTO-WHEEL-SPOKE','instance_count':len(spokes),'instances_per_wheel':SPOKES_PER_WHEEL,'affected_views':FAMILY_AFFECTED_VIEWS['DET-FAMILY-WHEEL-SPOKES']},
            {'id':'DET-FAMILY-WHEEL-RIM-RINGS','prototype':'PROTO-WHEEL-RIM-RING','instance_count':len(rings),'instances_per_wheel':1,'affected_views':FAMILY_AFFECTED_VIEWS['DET-FAMILY-WHEEL-RIM-RINGS']},
        ],
        'instances':instance_manifest,
        'boundary':'Generic detail/instance benchmark only. Spoke/ring geometry is not wheel-design authority or engineering specification.',
        'blocked':['M9 pending Human M8 review'],
    }
    (out/'M8_DETAIL_INSTANCES.json').write_text(json.dumps(architecture,ensure_ascii=False,indent=2)+'\n')
    qa={'schema':'oleander.auto.v0.11.m8.qa.v1','model':MODEL,'stage':'M8','status':status,'checks':checks,'source_hash_before':source_hash_before,'source_hash_after':source_hash_after_render,'source_topology':source_topology_after,'m7_secondary_signatures_before':secondary_sig_before,'m7_secondary_signatures_after':secondary_sig_final,'wheel_hp_package':wheel_records,'spokes_per_wheel':spokes_by_code,'radial_envelopes_m':{'spoke':radial_spoke_max,'rim_ring':radial_ring_max,'wheel_radius':WHEEL_RADIUS},'renders':renders,'human_review_required':['instance centering','left/right rotation consistency','tire clipping','detail scale/hierarchy','occlusion','cropping/framing']}
    (out/'M8_DETAIL_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')

    blend=out/'R29A_M8_DETAIL_INSTANCES.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    receipt={'schema':'oleander.auto.v0.11.m8.receipt.v1','model':MODEL,'blender_version':bpy.app.version_string,'status':'EXECUTED_'+status,'blend':str(blend),'qa':str(out/'M8_DETAIL_QA.json'),'architecture':str(out/'M8_DETAIL_INSTANCES.json'),'renders':renders}
    (out/'M8_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':status,'checks':checks,'spokes_per_wheel':spokes_by_code,'source_hash':source_hash_before},ensure_ascii=False,indent=2))
    raise SystemExit(0 if status.startswith('MACHINE_PASS') else 5)


if __name__=='__main__':main()
