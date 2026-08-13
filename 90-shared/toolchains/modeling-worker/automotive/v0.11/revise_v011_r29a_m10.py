#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 — R29A M10 Multi-Scale QA.

Final Modeling Contract validation for the generic automotive Modeling Worker benchmark.
No new design variables are introduced. Rebuilds the passed M5-M9 authority chain and
renders Macro / Meso / Micro diagnostic views while verifying all geometry/signature locks.
"""
from __future__ import annotations

import importlib.util
import json
import time
from pathlib import Path

import bpy


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

m9=load('/tmp/revise_v011_r29a_m9.py','m9_for_m10')
m8=m9.m8;m7=m9.m7;m6=m9.m6;r29a=m9.r29a;r20=m9.r20;r16=m9.r16;r14=m9.r14;b=m9.b;hp=m9.hp
m8.WHEEL_RADIUS=m8.TARGET_OD*.5

MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R29A_M10'
CANONICAL_SOURCE_HASH='d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb'
TARGET_OD=.700

for mod in (m9,m8,m7,m6,r29a,m7.r25,m6.r24,r20,m6.r18,r16,r16.r15,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):
    mod.MODEL=MODEL
hp.install(b,TARGET_OD)


def render_multiscale(out,samples,res,baseM,source,wheelhouses,glazing,spokes,rings):
    b.ground(baseM);L=b.rigs();b.world((.018,.018,.018),.20)
    rd=out/'renders';rd.mkdir(parents=True,exist_ok=True)
    wheels=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('WHEEL_')]
    views=[
        ('M10_MACRO_SIDE','MACRO',(0,-8.8,1.14),(0,0,.64),85,True,5.25,'BROAD','ALL'),
        ('M10_MACRO_HERO_FRONT','MACRO',(6.2,-7.0,2.75),(.05,0,.66),78,False,5.0,'BROAD','ALL'),
        ('M10_MACRO_HERO_REAR','MACRO',(-6.0,6.8,2.65),(-.10,0,.66),78,False,5.0,'BROAD','ALL'),
        ('M10_MESO_FRONT_ARCH','MESO',(2.75,-3.65,1.18),(b.FX,-b.WY,.56),92,False,5.0,'STRIP','FR'),
        ('M10_MESO_REAR_ARCH','MESO',(-2.65,-3.65,1.18),(b.RX,-b.WY,.56),92,False,5.0,'STRIP','RR'),
        ('M10_MESO_GLASSHOUSE','MESO',(3.6,-4.8,2.45),(-.05,-.05,1.02),95,False,5.0,'BROAD','ALL'),
        ('M10_MICRO_FRONT_WHEEL','MICRO',(2.55,-3.1,.86),(b.FX,-b.WY,.39),110,False,5.0,'STRIP','FR'),
        ('M10_MICRO_REAR_WHEEL','MICRO',(-2.45,-3.1,.86),(b.RX,-b.WY,.39),110,False,5.0,'STRIP','RR'),
    ]
    records=[]
    for label,scale_class,loc,target,lens,ortho,ortho_scale,rig,scope in views:
        b.setrig(L,rig)
        for w in wheels:w.hide_render=(scope!='ALL' and scope not in w.name)
        for wh in wheelhouses:wh.hide_render=(scope!='ALL' and not wh.name.endswith(scope))
        for o in spokes+rings:o.hide_render=(scope!='ALL' and f'-{scope}' not in o.name)
        cam=b.camera('CAM_'+label,loc,target,lens,ortho,ortho_scale);bpy.context.scene.camera=cam
        p=rd/f'{MODEL}__{label}.png';b.setup(p,samples,res);bpy.ops.render.render(write_still=True)
        records.append({'view':label,'scale':scale_class,'file':str(p),'scope':scope,'authority':'DIAGNOSTIC_ONLY','engineering_authority':False})
        bpy.data.objects.remove(cam,do_unlink=True)
    for w in wheels:w.hide_render=False
    for wh in wheelhouses:wh.hide_render=False
    for o in spokes+rings:o.hide_render=False
    return records


def main():
    started=time.time()
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
    b.clear();baseM=b.materials();diag_glass=r14.diagnostic_glass();rows=b.controls_resampled()

    # M5 primary authority.
    source,xs,cols,arch_meta,reuse=r29a.build_source_r29a(rows,baseM,diag_glass);source.name='PRIMARY_R29A_M10_LOCKED_SOURCE'
    assignments,region_counts=m6.classify_regions(source);m6.add_region_attribute(source,assignments);source.data.update();bpy.context.view_layer.update()
    source_hash_before=r20.shape_hash(source);source_topology_before=m8.topology_stats(source)

    # Canonical package + M7 secondary authority.
    b.wheels(baseM);wheel_records=getattr(b,'_OLEANDER_WHEEL_HP_RECORDS',[]);wheel_exact=bool(getattr(b,'_OLEANDER_WHEEL_HP_EXACT',False)) and hp.package_exact(wheel_records,TARGET_OD);by_code={r['wheel_code']:r for r in wheel_records}
    tmp_wh=b.mat('M10_PREBIND_WHEELHOUSE',(.1,.2,.3,1),.5);tmp_glass=b.mat('M10_PREBIND_GLAZING',(.05,.15,.22,1),.2);tmp_detail=b.mat('M10_PREBIND_DETAIL',(.5,.5,.5,1),.4)
    wheelhouses=[]
    for code,side in (('FL',1),('FR',-1),('RL',1),('RR',-1)):
        o,_=m7.make_wheelhouse('SEC-WHEELHOUSE-'+code,by_code[code]['target_center'],side,tmp_wh);wheelhouses.append(o)
    glazing,_=m7.extract_glazing_shell(source,assignments,tmp_glass)
    secondary=wheelhouses+[glazing]
    secondary_sig_before={o.name:m8.mesh_signature(o) for o in secondary}

    # M8 linked detail authority.
    spoke_proto=m8.make_spoke_prototype(tmp_detail);ring_proto=m8.make_ring_prototype(tmp_detail)
    spokes,rings,instance_manifest=m8.instantiate_details(wheel_records,spoke_proto,ring_proto)
    prototype_sig_before={spoke_proto.name:m8.mesh_signature(spoke_proto),ring_proto.name:m8.mesh_signature(ring_proto)}
    instance_transform_before={o.name:m9.obj_transform_signature(o) for o in spokes+rings}
    linked_before={'spoke':len({id(o.data) for o in spokes}),'ring':len({id(o.data) for o in rings})}

    # M9 neutral semantic material binding — same registry and binding rules.
    mats=m9.material_registry()
    source.data.materials.clear();source.data.materials.append(mats['MAT-BODY-NEUTRAL-COAT']);source.data.materials.append(mats['MAT-GLASSHOUSE-BACKER'])
    backer_faces=0
    for p,region in zip(source.data.polygons,assignments):
        if region=='REG-GLASSHOUSE':p.material_index=1;backer_faces+=1
        else:p.material_index=0
    m9.bind_single_material(glazing,mats['MAT-GLAZING-NEUTRAL'])
    for wh in wheelhouses:m9.bind_single_material(wh,mats['MAT-WHEELHOUSE-DARK-POLYMER'])
    tire_objs=[]
    for rec in wheel_records:
        o=bpy.data.objects.get(rec['name'])
        if o is not None:m9.bind_single_material(o,mats['MAT-TIRE-RUBBER']);tire_objs.append(o)
    m9.bind_single_material(spoke_proto,mats['MAT-WHEEL-DETAIL-METAL']);m9.bind_single_material(ring_proto,mats['MAT-WHEEL-DETAIL-METAL'])
    source.data.update();bpy.context.view_layer.update()

    source_hash_assembled=r20.shape_hash(source);source_topology_assembled=m8.topology_stats(source)
    secondary_sig_assembled={o.name:m8.mesh_signature(o) for o in secondary}
    prototype_sig_assembled={spoke_proto.name:m8.mesh_signature(spoke_proto),ring_proto.name:m8.mesh_signature(ring_proto)}
    instance_transform_assembled={o.name:m9.obj_transform_signature(o) for o in spokes+rings}
    linked_assembled={'spoke':len({id(o.data) for o in spokes}),'ring':len({id(o.data) for o in rings})}

    renders=render_multiscale(out,max(2,min(a.samples,4)),min(a.resolution,640),baseM,source,wheelhouses,glazing,spokes,rings)

    source_hash_final=r20.shape_hash(source);source_topology_final=m8.topology_stats(source)
    secondary_sig_final={o.name:m8.mesh_signature(o) for o in secondary}
    prototype_sig_final={spoke_proto.name:m8.mesh_signature(spoke_proto),ring_proto.name:m8.mesh_signature(ring_proto)}
    instance_transform_final={o.name:m9.obj_transform_signature(o) for o in spokes+rings}
    linked_final={'spoke':len({id(o.data) for o in spokes}),'ring':len({id(o.data) for o in rings})}

    scale_counts={s:len([r for r in renders if r['scale']==s]) for s in ('MACRO','MESO','MICRO')}
    m9_binding_complete=(set(mats)==set(m9.MATERIAL_IDS) and backer_faces==220 and len(tire_objs)==4 and all(len(o.data.materials)==1 for o in wheelhouses+[glazing]+tire_objs) and all(len(o.data.materials)==1 and o.data.materials[0].name=='MAT-WHEEL-DETAIL-METAL' for o in spokes+rings))
    all_diag_authority=all(r['authority']=='DIAGNOSTIC_ONLY' and r['engineering_authority'] is False for r in renders)

    checks={
        'canonical_source_hash_before':source_hash_before==CANONICAL_SOURCE_HASH,
        'source_hash_stable_assembled':source_hash_assembled==source_hash_before,
        'source_hash_stable_after_render':source_hash_final==source_hash_before,
        'source_topology_stable':source_topology_before==source_topology_assembled==source_topology_final,
        'm6_region_counts_exact':region_counts==m7.EXPECTED_REGION_COUNTS,
        'm7_secondary_signatures_stable':secondary_sig_before==secondary_sig_assembled==secondary_sig_final,
        'm8_prototype_signatures_stable':prototype_sig_before==prototype_sig_assembled==prototype_sig_final,
        'm8_instance_transforms_stable':instance_transform_before==instance_transform_assembled==instance_transform_final,
        'm8_linked_mesh_relationships_stable':linked_before==linked_assembled==linked_final=={'spoke':1,'ring':1},
        'm9_six_material_binding_complete':m9_binding_complete,
        'wheel_hp_package_exact':wheel_exact and len(wheel_records)==4,
        'spoke_instances_40':len(spokes)==40,
        'rim_ring_instances_4':len(rings)==4,
        'macro_views_present':scale_counts['MACRO']==3,
        'meso_views_present':scale_counts['MESO']==3,
        'micro_views_present':scale_counts['MICRO']==2,
        'eight_diagnostic_views':len(renders)==8,
        'no_engineering_authority_views':all_diag_authority,
    }
    status='MACHINE_PASS_HUMAN_M10_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL'
    elapsed=time.time()-started

    qa={
        'schema':'oleander.auto.v0.11.m10.qa.v1','model':MODEL,'stage':'M10','status':status,
        'checks':checks,'source_hash_before':source_hash_before,'source_hash_after':source_hash_final,
        'source_topology':source_topology_final,'region_counts':region_counts,
        'secondary_signatures':secondary_sig_final,'prototype_signatures':prototype_sig_final,
        'wheel_hp_package':wheel_records,'instance_counts':{'spokes':len(spokes),'rim_rings':len(rings)},
        'material_ids':sorted(mats.keys()),'scale_counts':scale_counts,'renders':renders,
        'human_review_required':{
            'MACRO':['silhouette/package','wheel-body proportion','broad crown/body flow','detail/material hierarchy','occlusion','cropping/framing'],
            'MESO':['front/rear fender-wheelhouse relation','glazing alignment','secondary containment','material masking','lighting adequacy'],
            'MICRO':['instance centering','radial containment','material consistency','near-side occlusion','detail scale'],
        },
        'boundary':'Final generic Modeling Worker multi-scale QA only; no Class-A, engineering, manufacturing, homologation or final CMF authority.',
    }
    (out/'M10_MULTI_SCALE_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')

    receipt={
        'schema':'oleander.auto.v0.11.m10.receipt.v1','model':MODEL,'blender_version':bpy.app.version_string,'status':'EXECUTED_'+status,
        'samples':max(2,min(a.samples,4)),'resolution':[min(a.resolution,640),min(a.resolution,640)],'render_count':len(renders),
        'scale_counts':scale_counts,'script_elapsed_seconds':elapsed,'source_hash':source_hash_final,'renders':renders,
        'candidate_authority_if_human_pass':'MODELING_WORKER_v0.11_CANDIDATE_AUTHORITY',
    }
    (out/'M10_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')

    blend=out/'R29A_M10_MULTI_SCALE_QA.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    print(json.dumps({'status':status,'checks':checks,'scale_counts':scale_counts,'elapsed':elapsed},ensure_ascii=False,indent=2))
    raise SystemExit(0 if status.startswith('MACHINE_PASS') else 5)

if __name__=='__main__':main()
