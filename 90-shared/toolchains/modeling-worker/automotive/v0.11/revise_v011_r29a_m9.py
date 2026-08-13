#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 — R29A M9 Semantic Material Binding.

Neutral benchmark material binding only. No final CMF authority.
Geometry authority from M5-M8 remains locked and is verified before/after binding.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import bpy


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

m8=load('/tmp/revise_v011_r29a_m8.py','m8_for_m9')
m8.WHEEL_RADIUS=m8.TARGET_OD*.5
m7=m8.m7;m6=m8.m6;r29a=m8.r29a;r20=m8.r20;r16=m8.r16;r14=m8.r14;b=m8.b;hp=m8.hp

MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R29A_M9'
CANONICAL_SOURCE_HASH='d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb'
TARGET_OD=.700

for mod in (m8,m7,m6,r29a,m7.r25,m6.r24,r20,m6.r18,r16,r16.r15,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):
    mod.MODEL=MODEL
hp.install(b,TARGET_OD)

MATERIAL_IDS=[
    'MAT-BODY-NEUTRAL-COAT',
    'MAT-GLASSHOUSE-BACKER',
    'MAT-GLAZING-NEUTRAL',
    'MAT-WHEELHOUSE-DARK-POLYMER',
    'MAT-TIRE-RUBBER',
    'MAT-WHEEL-DETAIL-METAL',
]

AFFECTED_VIEWS={
    'MAT-BODY-NEUTRAL-COAT':['M9_SIDE_BINDING','M9_HERO_FRONT_BINDING','M9_HERO_REAR_BINDING'],
    'MAT-GLASSHOUSE-BACKER':['M9_SIDE_BINDING','M9_HERO_FRONT_BINDING','M9_HERO_REAR_BINDING'],
    'MAT-GLAZING-NEUTRAL':['M9_SIDE_BINDING','M9_HERO_FRONT_BINDING','M9_HERO_REAR_BINDING'],
    'MAT-WHEELHOUSE-DARK-POLYMER':['M9_FRONT_WHEEL_BINDING','M9_HERO_FRONT_BINDING','M9_HERO_REAR_BINDING'],
    'MAT-TIRE-RUBBER':['M9_FRONT_WHEEL_BINDING','M9_HERO_FRONT_BINDING','M9_HERO_REAR_BINDING'],
    'MAT-WHEEL-DETAIL-METAL':['M9_FRONT_WHEEL_BINDING','M9_HERO_FRONT_BINDING','M9_HERO_REAR_BINDING'],
}


def pbr_material(name,base,roughness,metallic=0.0,transmission=0.0,ior=1.45,coat=0.0,coat_roughness=.12):
    ma=bpy.data.materials.new(name)
    ma.use_nodes=True
    nt=ma.node_tree;nt.nodes.clear()
    out=nt.nodes.new('ShaderNodeOutputMaterial')
    bs=nt.nodes.new('ShaderNodeBsdfPrincipled')
    bs.inputs['Base Color'].default_value=base
    bs.inputs['Roughness'].default_value=roughness
    bs.inputs['Metallic'].default_value=metallic
    if 'IOR' in bs.inputs:bs.inputs['IOR'].default_value=ior
    if 'Transmission Weight' in bs.inputs:bs.inputs['Transmission Weight'].default_value=transmission
    if 'Coat Weight' in bs.inputs:bs.inputs['Coat Weight'].default_value=coat
    if 'Coat Roughness' in bs.inputs:bs.inputs['Coat Roughness'].default_value=coat_roughness
    nt.links.new(bs.outputs['BSDF'],out.inputs['Surface'])
    ma['OLEANDER_AUTHORITY']='M9_BENCHMARK_MATERIAL'
    ma['OLEANDER_CMF_STATUS']='NOT_FINAL_CMF'
    return ma


def material_registry():
    return {
        'MAT-BODY-NEUTRAL-COAT':pbr_material('MAT-BODY-NEUTRAL-COAT',(.34,.35,.36,1),.28,coat=.35,coat_roughness=.12),
        'MAT-GLASSHOUSE-BACKER':pbr_material('MAT-GLASSHOUSE-BACKER',(.018,.022,.026,1),.48),
        'MAT-GLAZING-NEUTRAL':pbr_material('MAT-GLAZING-NEUTRAL',(.045,.105,.135,1),.08,transmission=.90,ior=1.45),
        'MAT-WHEELHOUSE-DARK-POLYMER':pbr_material('MAT-WHEELHOUSE-DARK-POLYMER',(.025,.030,.034,1),.62),
        'MAT-TIRE-RUBBER':pbr_material('MAT-TIRE-RUBBER',(.012,.014,.016,1),.80),
        'MAT-WHEEL-DETAIL-METAL':pbr_material('MAT-WHEEL-DETAIL-METAL',(.34,.36,.38,1),.28,metallic=.88),
    }


def obj_transform_signature(o):
    return {
        'location':[round(v,9) for v in o.location],
        'rotation':[round(v,9) for v in o.rotation_euler],
        'scale':[round(v,9) for v in o.scale],
        'mesh':o.data.name if o.type=='MESH' else None,
    }


def bind_single_material(o,ma):
    o.data.materials.clear();o.data.materials.append(ma)
    for p in o.data.polygons:p.material_index=0


def render_views(out,samples,res,M,source,wheelhouses,glazing,spokes,rings):
    b.ground(M);L=b.rigs();b.world((.018,.018,.018),.20)
    rd=out/'renders';rd.mkdir(parents=True,exist_ok=True)
    wheels=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('WHEEL_')]
    views=[
        ('M9_SIDE_BINDING',(0,-8.8,1.14),(0,0,.64),85,True,5.25,'BROAD','ALL'),
        ('M9_HERO_FRONT_BINDING',(6.2,-7.0,2.75),(.05,0,.66),78,False,5.0,'BROAD','ALL'),
        ('M9_HERO_REAR_BINDING',(-6.0,6.8,2.65),(-.10,0,.66),78,False,5.0,'BROAD','ALL'),
        ('M9_FRONT_WHEEL_BINDING',(2.65,-3.4,.95),(b.FX,-b.WY,.48),100,False,5.0,'STRIP','FR'),
    ]
    R=[]
    for label,loc,target,lens,ortho,scale,rig,scope in views:
        b.setrig(L,rig)
        for w in wheels:w.hide_render=(scope!='ALL' and scope not in w.name)
        for wh in wheelhouses:wh.hide_render=(scope!='ALL' and not wh.name.endswith(scope))
        for o in spokes+rings:o.hide_render=(scope!='ALL' and f'-{scope}' not in o.name)
        cam=b.camera('CAM_'+label,loc,target,lens,ortho,scale);bpy.context.scene.camera=cam
        p=rd/f'{MODEL}__{label}.png';b.setup(p,samples,res);bpy.ops.render.render(write_still=True)
        R.append({'view':label,'file':str(p),'scope':scope,'authority':'M9_DIAGNOSTIC_ONLY'});bpy.data.objects.remove(cam,do_unlink=True)
    for w in wheels:w.hide_render=False
    for wh in wheelhouses:wh.hide_render=False
    for o in spokes+rings:o.hide_render=False
    return R


def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
    b.clear();baseM=b.materials();diag_glass=r14.diagnostic_glass();rows=b.controls_resampled()

    source,xs,cols,arch_meta,reuse=r29a.build_source_r29a(rows,baseM,diag_glass);source.name='PRIMARY_R29A_M9_LOCKED_SOURCE'
    assignments,region_counts=m6.classify_regions(source);m6.add_region_attribute(source,assignments);source.data.update();bpy.context.view_layer.update()
    source_hash_before=r20.shape_hash(source);source_topology_before=m8.topology_stats(source)

    b.wheels(baseM);wheel_records=getattr(b,'_OLEANDER_WHEEL_HP_RECORDS',[]);wheel_exact=bool(getattr(b,'_OLEANDER_WHEEL_HP_EXACT',False)) and hp.package_exact(wheel_records,TARGET_OD)
    by_code={r['wheel_code']:r for r in wheel_records}

    # Rebuild the passed M7 secondary families with identical geometry parameters.
    tmp_wh=b.mat('M9_PREBIND_WHEELHOUSE',(.1,.2,.3,1),.5);tmp_glass=b.mat('M9_PREBIND_GLAZING',(.05,.15,.22,1),.2);tmp_detail=b.mat('M9_PREBIND_DETAIL',(.5,.5,.5,1),.4)
    wheelhouses=[]
    for code,side in (('FL',1),('FR',-1),('RL',1),('RR',-1)):
        o,_=m7.make_wheelhouse('SEC-WHEELHOUSE-'+code,by_code[code]['target_center'],side,tmp_wh);wheelhouses.append(o)
    glazing,_=m7.extract_glazing_shell(source,assignments,tmp_glass)
    secondary=wheelhouses+[glazing]
    secondary_sig_before={o.name:m8.mesh_signature(o) for o in secondary}

    spoke_proto=m8.make_spoke_prototype(tmp_detail);ring_proto=m8.make_ring_prototype(tmp_detail)
    spokes,rings,instance_manifest=m8.instantiate_details(wheel_records,spoke_proto,ring_proto)
    prototype_sig_before={spoke_proto.name:m8.mesh_signature(spoke_proto),ring_proto.name:m8.mesh_signature(ring_proto)}
    instance_transform_before={o.name:obj_transform_signature(o) for o in spokes+rings}
    linked_before={'spoke':len({id(o.data) for o in spokes}),'ring':len({id(o.data) for o in rings})}

    mats=material_registry()

    # Source binding: exact M6 face routing determines neutral body vs glasshouse backer.
    source.data.materials.clear();source.data.materials.append(mats['MAT-BODY-NEUTRAL-COAT']);source.data.materials.append(mats['MAT-GLASSHOUSE-BACKER'])
    backer_faces=0
    for p,region in zip(source.data.polygons,assignments):
        if region=='REG-GLASSHOUSE':p.material_index=1;backer_faces+=1
        else:p.material_index=0

    bind_single_material(glazing,mats['MAT-GLAZING-NEUTRAL'])
    for wh in wheelhouses:bind_single_material(wh,mats['MAT-WHEELHOUSE-DARK-POLYMER'])
    tire_names={r['name'] for r in wheel_records};tire_objs=[]
    for name in tire_names:
        o=bpy.data.objects.get(name)
        if o is not None:
            bind_single_material(o,mats['MAT-TIRE-RUBBER']);tire_objs.append(o)
    bind_single_material(spoke_proto,mats['MAT-WHEEL-DETAIL-METAL'])
    bind_single_material(ring_proto,mats['MAT-WHEEL-DETAIL-METAL'])

    source.data.update();bpy.context.view_layer.update()
    source_hash_after_binding=r20.shape_hash(source);source_topology_after=m8.topology_stats(source)
    secondary_sig_after={o.name:m8.mesh_signature(o) for o in secondary}
    prototype_sig_after={spoke_proto.name:m8.mesh_signature(spoke_proto),ring_proto.name:m8.mesh_signature(ring_proto)}
    instance_transform_after={o.name:obj_transform_signature(o) for o in spokes+rings}
    linked_after={'spoke':len({id(o.data) for o in spokes}),'ring':len({id(o.data) for o in rings})}

    # Binding manifest is explicit and independent from diagnostic render colors.
    bindings=[
        {'material':'MAT-BODY-NEUTRAL-COAT','targets':['R29A_SOURCE_EXCEPT_REG-GLASSHOUSE'],'binding_mode':'FACE_REGION','affected_views':AFFECTED_VIEWS['MAT-BODY-NEUTRAL-COAT']},
        {'material':'MAT-GLASSHOUSE-BACKER','targets':['REG-GLASSHOUSE'],'binding_mode':'FACE_REGION','affected_views':AFFECTED_VIEWS['MAT-GLASSHOUSE-BACKER']},
        {'material':'MAT-GLAZING-NEUTRAL','targets':['SEC-GLAZING-SHELL'],'binding_mode':'OBJECT','affected_views':AFFECTED_VIEWS['MAT-GLAZING-NEUTRAL']},
        {'material':'MAT-WHEELHOUSE-DARK-POLYMER','targets':[o.name for o in wheelhouses],'binding_mode':'OBJECT_FAMILY','affected_views':AFFECTED_VIEWS['MAT-WHEELHOUSE-DARK-POLYMER']},
        {'material':'MAT-TIRE-RUBBER','targets':sorted(tire_names),'binding_mode':'CANONICAL_HP_OBJECTS','affected_views':AFFECTED_VIEWS['MAT-TIRE-RUBBER']},
        {'material':'MAT-WHEEL-DETAIL-METAL','targets':['PROTO-WHEEL-SPOKE','PROTO-WHEEL-RIM-RING'],'binding_mode':'LINKED_PROTOTYPE_MESH','inherited_instance_count':len(spokes)+len(rings),'affected_views':AFFECTED_VIEWS['MAT-WHEEL-DETAIL-METAL']},
    ]

    renders=render_views(out,max(2,min(a.samples,6)),min(a.resolution,640),baseM,source,wheelhouses,glazing,spokes,rings)
    source_hash_after_render=r20.shape_hash(source);secondary_sig_final={o.name:m8.mesh_signature(o) for o in secondary};prototype_sig_final={spoke_proto.name:m8.mesh_signature(spoke_proto),ring_proto.name:m8.mesh_signature(ring_proto)};instance_transform_final={o.name:obj_transform_signature(o) for o in spokes+rings}

    body_faces=sum(1 for r in assignments if r!='REG-GLASSHOUSE')
    required_targets_resolve=(len(tire_objs)==4 and len(wheelhouses)==4 and glazing is not None and len(spokes)==40 and len(rings)==4)
    detail_material_inherited=all(len(o.data.materials)==1 and o.data.materials[0].name=='MAT-WHEEL-DETAIL-METAL' for o in spokes+rings)
    authorities_ok=(source.get('OLEANDER_AUTHORITY')!='M9_BENCHMARK_MATERIAL' and all(o.get('OLEANDER_AUTHORITY')=='SECONDARY_GEOMETRY_WORKING' for o in secondary) and all(o.get('OLEANDER_AUTHORITY')=='DETAIL_INSTANCE' for o in spokes+rings))

    checks={
        'canonical_source_hash_before':source_hash_before==CANONICAL_SOURCE_HASH,
        'source_hash_stable_after_binding':source_hash_after_binding==source_hash_before,
        'source_hash_stable_after_render':source_hash_after_render==source_hash_before,
        'source_topology_stable':source_topology_before==source_topology_after,
        'm6_region_assignments_retained':region_counts==m7.EXPECTED_REGION_COUNTS,
        'm7_secondary_geometry_stable':secondary_sig_before==secondary_sig_after==secondary_sig_final,
        'm8_prototype_geometry_stable':prototype_sig_before==prototype_sig_after==prototype_sig_final,
        'm8_instance_transforms_stable':instance_transform_before==instance_transform_after==instance_transform_final,
        'm8_linked_mesh_relationships_stable':linked_before==linked_after=={'spoke':1,'ring':1},
        'wheel_hp_package_exact':wheel_exact and len(wheel_records)==4,
        'six_required_material_ids_exist':set(mats)==set(MATERIAL_IDS),
        'required_semantic_targets_resolve':required_targets_resolve,
        'source_face_material_coverage_exact':body_faces+backer_faces==len(source.data.polygons),
        'glasshouse_backer_faces_220':backer_faces==220,
        'wheelhouse_material_bound_4':all(len(o.data.materials)==1 and o.data.materials[0].name=='MAT-WHEELHOUSE-DARK-POLYMER' for o in wheelhouses),
        'tire_material_bound_4':len(tire_objs)==4 and all(len(o.data.materials)==1 and o.data.materials[0].name=='MAT-TIRE-RUBBER' for o in tire_objs),
        'glazing_material_bound':len(glazing.data.materials)==1 and glazing.data.materials[0].name=='MAT-GLAZING-NEUTRAL',
        'detail_material_inherited_44':detail_material_inherited,
        'authority_labels_unchanged':authorities_ok,
        'binding_affected_views_complete':len(bindings)==6 and all(bd.get('affected_views') for bd in bindings),
        'diagnostic_render_matrix':len(renders)==4,
    }
    status='MACHINE_PASS_HUMAN_M9_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL'

    registry={
        'schema':'oleander.auto.v0.11.m9.material-binding.v1','model':MODEL,'stage':'M9','status':status,
        'source_hash':source_hash_before,'cmf_authority':'NOT_FINAL_CMF',
        'materials':[
            {'id':'MAT-BODY-NEUTRAL-COAT','class':'COATED_NONMETAL','intent':'neutral coated body benchmark'},
            {'id':'MAT-GLASSHOUSE-BACKER','class':'OPAQUE_DARK_BACKER','intent':'diagnostic substrate under glazing shell'},
            {'id':'MAT-GLAZING-NEUTRAL','class':'TRANSPARENT_DIELECTRIC','intent':'neutral glazing benchmark'},
            {'id':'MAT-WHEELHOUSE-DARK-POLYMER','class':'ROUGH_DARK_NONMETAL','intent':'secondary wheelhouse benchmark'},
            {'id':'MAT-TIRE-RUBBER','class':'ROUGH_RUBBER_LIKE','intent':'canonical tire benchmark'},
            {'id':'MAT-WHEEL-DETAIL-METAL','class':'METALLIC_NEUTRAL','intent':'linked detail instance benchmark'},
        ],
        'bindings':bindings,
        'boundary':'Semantic material binding benchmark only. No final CMF, supplier, grade, coating-stack or production-process authority.',
        'blocked':['M10 pending Human M9 review'],
    }
    (out/'M9_MATERIAL_BINDING.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
    qa={'schema':'oleander.auto.v0.11.m9.qa.v1','model':MODEL,'stage':'M9','status':status,'checks':checks,'source_hash_before':source_hash_before,'source_hash_after':source_hash_after_render,'source_topology':source_topology_after,'region_counts':region_counts,'secondary_signatures':secondary_sig_final,'prototype_signatures':prototype_sig_final,'wheel_hp_package':wheel_records,'bindings':bindings,'renders':renders,'human_review_required':['missing material/pink fallback','body/glazing separation','glasshouse backer leakage','wheelhouse containment','tire-only binding','linked-detail consistency','hierarchy','occlusion','scale/proportion','cropping/framing','lighting sufficiency']}
    (out/'M9_MATERIAL_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')

    blend=out/'R29A_M9_MATERIAL_BINDING.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    receipt={'schema':'oleander.auto.v0.11.m9.receipt.v1','model':MODEL,'blender_version':bpy.app.version_string,'status':'EXECUTED_'+status,'blend':str(blend),'qa':str(out/'M9_MATERIAL_QA.json'),'registry':str(out/'M9_MATERIAL_BINDING.json'),'renders':renders}
    (out/'M9_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':status,'checks':checks,'source_hash':source_hash_before},ensure_ascii=False,indent=2))
    raise SystemExit(0 if status.startswith('MACHINE_PASS') else 5)

if __name__=='__main__':main()
