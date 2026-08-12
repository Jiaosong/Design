#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 — R29A M6 Component Architecture.

M6 is metadata/routing architecture only. It must not modify the validated R29A
primary-surface coordinates or topology.

Outputs:
- M6_COMPONENT_ARCHITECTURE.json
- M6_COMPONENT_QA.json
- M6_RECEIPT.json
- R29A_M6_COMPONENT_ARCHITECTURE.blend
- 3 derived diagnostic component-map renders

Face regions are routing masks, NOT physical panel seams or manufacturing splits.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import bpy


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


r29a=load('/tmp/revise_v011_r29a.py','r29a')
hp=load('/tmp/wheel_hp_contract.py','wheel_hp_contract_m6')
r25=r29a.r25
r24=r29a.r24
r20=r29a.r20
r18=r29a.r18
r16=r29a.r16
r14=r29a.r14
b=r29a.b

MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R29A_M6'
CANONICAL_M5_SOURCE_HASH='d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb'
TARGET_OD=.700

for m in (r29a,r25,r24,r20,r18,r16,r16.r15,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):
    m.MODEL=MODEL

# R29A already installs the wheel HP contract during import. Calling install again is idempotent.
hp.install(b,TARGET_OD)

REGIONS=[
    'REG-GLASSHOUSE',
    'REG-FRONT-FENDER-L',
    'REG-FRONT-FENDER-R',
    'REG-REAR-QUARTER-L',
    'REG-REAR-QUARTER-R',
    'REG-FRONT-TERMINATION',
    'REG-REAR-TERMINATION',
    'REG-BODY-MAIN-L',
    'REG-BODY-MAIN-R',
    'REG-UNDERBODY-CENTER',
]
REGION_ID={name:i+1 for i,name in enumerate(REGIONS)}

DEPENDENCIES={
    'SRC-R29A':{'kind':'SOURCE','status':'LOCKED','description':'validated R29A primary geometry'},
    'HP-WHEEL-FRONT':{'kind':'HARD_POINT','status':'LOCKED','description':'front axle wheel hard point'},
    'HP-WHEEL-REAR':{'kind':'HARD_POINT','status':'LOCKED','description':'rear axle wheel hard point'},
    'HP-PACKAGE-ENVELOPE':{'kind':'HARD_POINT','status':'LOCKED','description':'vehicle package envelope'},
    'CONTRACT-WHEEL-HP':{'kind':'CONTRACT','status':'LOCKED','description':'wheel_hp_contract.py / OD 0.700 m'},
    'REL-R29A-SHOULDER-CROWN':{'kind':'RELATION','status':'LOCKED','description':'R29A shoulder-fed crown relation'},
    'REL-R18-R20-TERMINATION':{'kind':'RELATION','status':'LOCKED','description':'structured front/rear termination construction'},
    'SEC-R09-R12-GREENHOUSE':{'kind':'SECTION_SYSTEM','status':'LOCKED','description':'retained cabin/greenhouse section progression'},
    'REL-R11-TRANSVERSE-TENSION':{'kind':'RELATION','status':'LOCKED','description':'non-wheel transverse body tension'},
    'REL-R12-PCHIP':{'kind':'RELATION','status':'LOCKED','description':'longitudinal PCHIP-like interpolation'},
}

REGION_DEPENDENCIES={
    'REG-GLASSHOUSE':['SRC-R29A','SEC-R09-R12-GREENHOUSE','REL-R12-PCHIP'],
    'REG-FRONT-FENDER-L':['SRC-R29A','HP-WHEEL-FRONT','REL-R29A-SHOULDER-CROWN','CONTRACT-WHEEL-HP'],
    'REG-FRONT-FENDER-R':['SRC-R29A','HP-WHEEL-FRONT','REL-R29A-SHOULDER-CROWN','CONTRACT-WHEEL-HP'],
    'REG-REAR-QUARTER-L':['SRC-R29A','HP-WHEEL-REAR','REL-R29A-SHOULDER-CROWN','CONTRACT-WHEEL-HP'],
    'REG-REAR-QUARTER-R':['SRC-R29A','HP-WHEEL-REAR','REL-R29A-SHOULDER-CROWN','CONTRACT-WHEEL-HP'],
    'REG-FRONT-TERMINATION':['SRC-R29A','REL-R18-R20-TERMINATION'],
    'REG-REAR-TERMINATION':['SRC-R29A','REL-R18-R20-TERMINATION'],
    'REG-BODY-MAIN-L':['SRC-R29A','REL-R11-TRANSVERSE-TENSION','REL-R12-PCHIP'],
    'REG-BODY-MAIN-R':['SRC-R29A','REL-R11-TRANSVERSE-TENSION','REL-R12-PCHIP'],
    'REG-UNDERBODY-CENTER':['SRC-R29A','HP-PACKAGE-ENVELOPE','REL-R12-PCHIP'],
}

VIEW_POLICY={
    'REG-GLASSHOUSE':['M6_COMPONENT_SIDE','M6_COMPONENT_FRONT_3Q','M6_COMPONENT_REAR_3Q'],
    'REG-FRONT-FENDER-L':['M6_COMPONENT_SIDE','M6_COMPONENT_FRONT_3Q'],
    'REG-FRONT-FENDER-R':['M6_COMPONENT_FRONT_3Q'],
    'REG-REAR-QUARTER-L':['M6_COMPONENT_SIDE','M6_COMPONENT_REAR_3Q'],
    'REG-REAR-QUARTER-R':['M6_COMPONENT_REAR_3Q'],
    'REG-FRONT-TERMINATION':['M6_COMPONENT_SIDE','M6_COMPONENT_FRONT_3Q'],
    'REG-REAR-TERMINATION':['M6_COMPONENT_SIDE','M6_COMPONENT_REAR_3Q'],
    'REG-BODY-MAIN-L':['M6_COMPONENT_SIDE','M6_COMPONENT_FRONT_3Q','M6_COMPONENT_REAR_3Q'],
    'REG-BODY-MAIN-R':['M6_COMPONENT_FRONT_3Q','M6_COMPONENT_REAR_3Q'],
    'REG-UNDERBODY-CENTER':['M6_COMPONENT_SIDE','M6_COMPONENT_FRONT_3Q','M6_COMPONENT_REAR_3Q'],
}

SELECTIVE_REBUILD={
    'REG-GLASSHOUSE':{'scope':'REGION_LOCAL','views':['SIDE_SILHOUETTE','PACKAGE_SIDE','HERO_FRONT_3Q','HERO_REAR_3Q','CLAY_STRIP','CLAY_GRAZING'],'future_m7_attachments':['SECONDARY-GLAZING-BOUNDARY']},
    'REG-FRONT-FENDER-L':{'scope':'REGION_LOCAL','views':['SIDE_SILHOUETTE','PACKAGE_SIDE','HERO_FRONT_3Q','CLAY_STRIP','CLAY_GRAZING','FRONT_ARCH_DETAIL'],'future_m7_attachments':['SECONDARY-FRONT-WHEELHOUSE-L','SECONDARY-FRONT-PANEL-BOUNDARY-L']},
    'REG-FRONT-FENDER-R':{'scope':'REGION_LOCAL','views':['HERO_FRONT_3Q','CLAY_STRIP','CLAY_GRAZING'],'future_m7_attachments':['SECONDARY-FRONT-WHEELHOUSE-R','SECONDARY-FRONT-PANEL-BOUNDARY-R']},
    'REG-REAR-QUARTER-L':{'scope':'REGION_LOCAL','views':['SIDE_SILHOUETTE','PACKAGE_SIDE','HERO_REAR_3Q','CLAY_STRIP','CLAY_GRAZING','REAR_ARCH_DETAIL'],'future_m7_attachments':['SECONDARY-REAR-WHEELHOUSE-L','SECONDARY-REAR-PANEL-BOUNDARY-L']},
    'REG-REAR-QUARTER-R':{'scope':'REGION_LOCAL','views':['HERO_REAR_3Q','CLAY_STRIP','CLAY_GRAZING'],'future_m7_attachments':['SECONDARY-REAR-WHEELHOUSE-R','SECONDARY-REAR-PANEL-BOUNDARY-R']},
    'REG-FRONT-TERMINATION':{'scope':'REGION_LOCAL','views':['HERO_FRONT_3Q','CLAY_STRIP','CLAY_GRAZING'],'future_m7_attachments':['SECONDARY-FRONT-FASCIA-BOUNDARY']},
    'REG-REAR-TERMINATION':{'scope':'REGION_LOCAL','views':['HERO_REAR_3Q','CLAY_STRIP','CLAY_GRAZING'],'future_m7_attachments':['SECONDARY-REAR-FASCIA-BOUNDARY']},
    'REG-BODY-MAIN-L':{'scope':'REGION_LOCAL','views':['SIDE_SILHOUETTE','PACKAGE_SIDE','HERO_FRONT_3Q','HERO_REAR_3Q','CLAY_STRIP','CLAY_GRAZING'],'future_m7_attachments':['SECONDARY-SIDE-PANEL-BOUNDARY-L']},
    'REG-BODY-MAIN-R':{'scope':'REGION_LOCAL','views':['HERO_FRONT_3Q','HERO_REAR_3Q','CLAY_STRIP','CLAY_GRAZING'],'future_m7_attachments':['SECONDARY-SIDE-PANEL-BOUNDARY-R']},
    'REG-UNDERBODY-CENTER':{'scope':'REGION_LOCAL','views':['PACKAGE_SIDE','HERO_FRONT_3Q','HERO_REAR_3Q'],'future_m7_attachments':['SECONDARY-UNDERBODY-BOUNDARY']},
}


def face_centroid_and_span(mesh,poly):
    pts=[mesh.vertices[i].co for i in poly.vertices]
    n=len(pts)
    c=(sum(p.x for p in pts)/n,sum(p.y for p in pts)/n,sum(p.z for p in pts)/n)
    ys=[p.y for p in pts]
    return c,min(ys),max(ys)


def classify_regions(source):
    mesh=source.data
    total=len(mesh.polygons)
    terminal_start=total-28
    assignments=[]
    counts={k:0 for k in REGIONS}

    for poly in mesh.polygons:
        (cx,cy,cz),ymin,ymax=face_centroid_and_span(mesh,poly)

        # Construction-order invariant from validated R18/R20: last 28 faces are the
        # two structured terminations. Split front/rear by X sign.
        if poly.index>=terminal_start:
            region='REG-FRONT-TERMINATION' if cx>0 else 'REG-REAR-TERMINATION'
        # Existing material index 1 is diagnostic glazing material in R29A builder.
        elif poly.material_index==1:
            region='REG-GLASSHOUSE'
        # Cross-center underbody strips span both signs of Y.
        elif ymin<0<ymax:
            region='REG-UNDERBODY-CENTER'
        elif abs(cx-b.FX)<=r29a.CROWN_ZONE:
            region='REG-FRONT-FENDER-L' if cy>0 else 'REG-FRONT-FENDER-R'
        elif abs(cx-b.RX)<=r29a.CROWN_ZONE:
            region='REG-REAR-QUARTER-L' if cy>0 else 'REG-REAR-QUARTER-R'
        else:
            region='REG-BODY-MAIN-L' if cy>0 else 'REG-BODY-MAIN-R'

        assignments.append(region)
        counts[region]+=1

    return assignments,counts


def add_region_attribute(source,assignments):
    mesh=source.data
    old=mesh.attributes.get('OLEANDER_REGION_ID')
    if old:
        mesh.attributes.remove(old)
    attr=mesh.attributes.new(name='OLEANDER_REGION_ID',type='INT',domain='FACE')
    for poly,region in zip(mesh.polygons,assignments):
        attr.data[poly.index].value=REGION_ID[region]
    source['OLEANDER_REGION_NAME_MAP']=json.dumps({str(v):k for k,v in REGION_ID.items()},ensure_ascii=False)
    source['OLEANDER_M6_AUTHORITY']='ROUTING_METADATA_ONLY'


def component_materials():
    # Diagnostic-only palette; colors have no design authority.
    colors=[
        (.16,.50,.78,1),(.87,.28,.24,1),(.92,.53,.18,1),(.41,.65,.28,1),(.13,.63,.54,1),
        (.72,.29,.67,1),(.48,.33,.73,1),(.68,.62,.18,1),(.27,.55,.72,1),(.45,.45,.45,1),
    ]
    return {region:b.mat('M6_DIAG_'+region.replace('-','_'),color,.55) for region,color in zip(REGIONS,colors)}


def make_diagnostic_map(source,assignments):
    diag=source.copy()
    diag.data=source.data.copy()
    diag.name='DERIVED_M6_COMPONENT_MAP'
    bpy.context.collection.objects.link(diag)
    diag['OLEANDER_AUTHORITY']='NONE'
    diag['OLEANDER_ROLE']='M6_COMPONENT_MAP_DIAGNOSTIC'
    mats=component_materials()
    diag.data.materials.clear()
    for region in REGIONS:
        diag.data.materials.append(mats[region])
    for poly,region in zip(diag.data.polygons,assignments):
        poly.material_index=REGIONS.index(region)
        poly.use_smooth=True
    return diag


def render_component_views(out,samples,res,M,source,diag):
    b.wheels(M)
    b.ground(M)
    L=b.rigs()
    b.world((.018,.018,.018),.18)
    source.hide_render=True
    rd=out/'renders';rd.mkdir(parents=True,exist_ok=True)
    views=[
        ('M6_COMPONENT_SIDE',(0,-8.8,1.14),(0,0,.64),85,True,5.25,'BROAD'),
        ('M6_COMPONENT_FRONT_3Q',(6.2,-7.0,2.75),(.05,0,.66),78,False,5.0,'BROAD'),
        ('M6_COMPONENT_REAR_3Q',(-6.0,6.8,2.65),(-.10,0,.66),78,False,5.0,'BROAD'),
    ]
    records=[]
    for label,loc,target,lens,ortho,scale,rig in views:
        b.setrig(L,rig)
        cam=b.camera('CAM_'+label,loc,target,lens,ortho,scale)
        bpy.context.scene.camera=cam
        p=rd/f'{MODEL}__{label}.png'
        b.setup(p,samples,res)
        bpy.ops.render.render(write_still=True)
        records.append({'view':label,'file':str(p),'authority':'DIAGNOSTIC_ONLY'})
        bpy.data.objects.remove(cam,do_unlink=True)
    source.hide_render=False
    return records


def topology_stats(source):
    tri=quad=ngon=0
    for p in source.data.polygons:
        n=len(p.vertices)
        if n==3:tri+=1
        elif n==4:quad+=1
        else:ngon+=1
    return {'vertices':len(source.data.vertices),'faces':len(source.data.polygons),'tri':tri,'quad':quad,'ngon':ngon}


def main():
    a=b.parse()
    out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
    b.clear()
    M=b.materials();glass=r14.diagnostic_glass();rows=b.controls_resampled()

    # Build R29A Source directly; do NOT call r29a.main(), which would rerender M5.
    source,xs,cols,arch_meta,reuse=r29a.build_source_r29a(rows,M,glass)
    source.name='PRIMARY_R29A_M6_LOCKED_SOURCE'
    hash_before=r20.shape_hash(source)
    stats_before=topology_stats(source)
    islands_before=r16.island_count(source)

    assignments,counts=classify_regions(source)
    add_region_attribute(source,assignments)
    source.data.update();bpy.context.view_layer.update()
    hash_after=r20.shape_hash(source)
    stats_after=topology_stats(source)
    islands_after=r16.island_count(source)

    # Package components use only the canonical HP contract.
    wheel_mats=M
    b.wheels(wheel_mats)
    wheel_records=getattr(b,'_OLEANDER_WHEEL_HP_RECORDS',[])
    wheel_exact=bool(getattr(b,'_OLEANDER_WHEEL_HP_EXACT',False)) and hp.package_exact(wheel_records,TARGET_OD)

    # Remove first set of wheels before render_component_views creates exactly one set.
    for o in list(bpy.context.scene.objects):
        if o.type=='MESH' and o.name.startswith('WHEEL_'):
            bpy.data.objects.remove(o,do_unlink=True)
    # reset wrapper records so the render wheel set becomes current evidence
    b._OLEANDER_WHEEL_HP_RECORDS=[]
    b._OLEANDER_WHEEL_HP_EXACT=False

    diag=make_diagnostic_map(source,assignments)
    renders=render_component_views(out,max(2,min(a.samples,4)),min(a.resolution,512),M,source,diag)
    wheel_records=getattr(b,'_OLEANDER_WHEEL_HP_RECORDS',[])
    wheel_exact=bool(getattr(b,'_OLEANDER_WHEEL_HP_EXACT',False)) and hp.package_exact(wheel_records,TARGET_OD)

    # Dependency resolution and semantic invariants.
    all_refs=[d for deps in REGION_DEPENDENCIES.values() for d in deps]
    deps_resolve=all(d in DEPENDENCIES for d in all_refs)
    unique_ids=len(set(REGION_ID.values()))==len(REGIONS)
    coverage_exact=sum(counts.values())==len(source.data.polygons) and len(assignments)==len(source.data.polygons)
    all_nonzero=all(counts[r]>0 for r in REGIONS)
    pair_checks={
        'front_fender':counts['REG-FRONT-FENDER-L']==counts['REG-FRONT-FENDER-R'],
        'rear_quarter':counts['REG-REAR-QUARTER-L']==counts['REG-REAR-QUARTER-R'],
        'body_main':counts['REG-BODY-MAIN-L']==counts['REG-BODY-MAIN-R'],
    }
    selective_complete=set(SELECTIVE_REBUILD)==set(REGIONS)
    diag_authority_none=diag.get('OLEANDER_AUTHORITY')=='NONE'
    no_modifiers=len(source.modifiers)==0

    components=[]
    for region in REGIONS:
        components.append({
            'id':region,
            'kind':'SOURCE_ROUTING_REGION',
            'authority':'ROUTING_ONLY',
            'face_count':counts[region],
            'dependencies':REGION_DEPENDENCIES[region],
            'diagnostic_views':VIEW_POLICY[region],
            'selective_rebuild':SELECTIVE_REBUILD[region],
            'physical_panel_seam':False,
        })

    code_to_pkg={'FL':'PKG-WHEEL-FL','FR':'PKG-WHEEL-FR','RL':'PKG-WHEEL-RL','RR':'PKG-WHEEL-RR'}
    package_components=[]
    for rec in wheel_records:
        code=rec['wheel_code']
        package_components.append({
            'id':code_to_pkg.get(code,'PKG-WHEEL-'+code),
            'kind':'PACKAGE_COMPONENT',
            'authority':'HARD_POINT_IMPLEMENTATION',
            'dependency':'CONTRACT-WHEEL-HP',
            'target_center':rec['target_center'],
            'evaluated_bounds':rec['after_evaluated'],
        })

    architecture={
        'schema':'oleander.auto.v0.11.m6.component-architecture.v1',
        'model':MODEL,
        'stage':'M6',
        'status':'MACHINE_PASS_HUMAN_M6_REVIEW_REQUIRED',
        'source_authority':'R29A_M5_PRIMARY_GEOMETRY',
        'canonical_m5_source_hash':CANONICAL_M5_SOURCE_HASH,
        'source_hash_before_annotations':hash_before,
        'source_hash_after_annotations':hash_after,
        'region_attribute':'OLEANDER_REGION_ID',
        'region_id_map':REGION_ID,
        'dependencies':DEPENDENCIES,
        'components':components,
        'package_components':package_components,
        'boundary':'Routing masks only; not panel seams, manufacturing splits, thickness, fastening or M7 detail authority.',
        'blocked':['M7 pending M6 Human review','M8'],
    }
    (out/'M6_COMPONENT_ARCHITECTURE.json').write_text(json.dumps(architecture,ensure_ascii=False,indent=2)+'\n')

    checks={
        'canonical_source_hash_before':hash_before==CANONICAL_M5_SOURCE_HASH,
        'source_hash_stable_after_annotations':hash_after==hash_before,
        'source_island_one':islands_before==1 and islands_after==1,
        'topology_stable':stats_before==stats_after,
        'termination_triangles_four':stats_after['tri']==4,
        'source_ngon_zero':stats_after['ngon']==0,
        'source_no_modifiers':no_modifiers,
        'region_coverage_exact':coverage_exact,
        'all_required_regions_nonzero':all_nonzero,
        'paired_region_symmetry':all(pair_checks.values()),
        'unique_region_ids':unique_ids,
        'dependency_refs_resolve':deps_resolve,
        'wheel_hp_package_exact':wheel_exact and len(package_components)==4,
        'selective_rebuild_matrix_complete':selective_complete,
        'derived_map_authority_none':diag_authority_none,
        'diagnostic_render_matrix':len(renders)==3,
    }
    status='MACHINE_PASS_HUMAN_M6_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL'
    qa={
        'schema':'oleander.auto.v0.11.m6.qa.v1',
        'model':MODEL,
        'stage':'M6',
        'status':status,
        'checks':checks,
        'source_hash_before':hash_before,
        'source_hash_after':hash_after,
        'topology_before':stats_before,
        'topology_after':stats_after,
        'source_islands_before_after':[islands_before,islands_after],
        'region_face_counts':counts,
        'pair_checks':pair_checks,
        'wheel_hp_package':wheel_records,
        'renders':renders,
        'human_review_required':['region boundary plausibility','occlusion/visibility','scale/proportion','cropping/framing','routing-mask-not-design-seam interpretation'],
    }
    (out/'M6_COMPONENT_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')

    blend=out/'R29A_M6_COMPONENT_ARCHITECTURE.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    receipt={
        'schema':'oleander.auto.v0.11.m6.receipt.v1',
        'model':MODEL,
        'blender_version':bpy.app.version_string,
        'status':'EXECUTED_'+status,
        'blend':str(blend),
        'architecture':str(out/'M6_COMPONENT_ARCHITECTURE.json'),
        'qa':str(out/'M6_COMPONENT_QA.json'),
        'renders':renders,
    }
    (out/'M6_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':status,'hash_before':hash_before,'hash_after':hash_after,'counts':counts,'checks':checks},ensure_ascii=False,indent=2))
    raise SystemExit(0 if status.startswith('MACHINE_PASS') else 5)


if __name__=='__main__':
    main()
