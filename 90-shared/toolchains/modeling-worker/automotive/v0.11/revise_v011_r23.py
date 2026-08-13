#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R23 — Wheelhouse Diagnostic Isolation.

R22 source geometry is fully LOCKED.
No source vertex/topology/hard-point/section changes.

Adds derived diagnostic-only inner wheelhouse walls and isolates the near-side wheel in
front/rear arch detail views. Purpose: distinguish true Source arch failure from an open
wheel-cavity / far-wheel visualization artifact before reopening M4.
"""
from __future__ import annotations
import importlib.util,bpy,json,math,hashlib
from pathlib import Path

BASE='/tmp/revise_v011_r22.py'
spec=importlib.util.spec_from_file_location('r22',BASE)
r22=importlib.util.module_from_spec(spec);spec.loader.exec_module(r22)
r20=r22.r20;r18=r22.r18;r16=r22.r16;r14=r22.r14;b=r22.b

MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R23'
r22.MODEL=MODEL;r20.MODEL=MODEL;r18.MODEL=MODEL;r16.MODEL=MODEL
r16.r15.MODEL=MODEL;r14.MODEL=MODEL;r14.r12.MODEL=MODEL;r14.r11.MODEL=MODEL
r14.r10.MODEL=MODEL;r14.r09.MODEL=MODEL;r14.r08.MODEL=MODEL;r14.r08.r.MODEL=MODEL;b.MODEL=MODEL

def diag_mat():
    return b.mat('MAT_WHEELHOUSE_DIAGNOSTIC',(.055,.060,.065,1),.58)

def make_wheelhouse(name,wx,side,ma):
    r=.418
    angles=[math.radians(v) for v in range(12,169,6)]
    y0=side*.655; y1=side*.515
    verts=[];faces=[]
    for a in angles:
        x=wx+r*math.cos(a);z=b.WZ+r*math.sin(a)
        verts.append((x,y0,z));verts.append((x,y1,z))
    for i in range(len(angles)-1):
        k=2*i;f=(k,k+2,k+3,k+1);faces.append(f if side>0 else tuple(reversed(f)))
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(ma)
    for p in me.polygons:p.use_smooth=True
    o['OLEANDER_ROLE']='DERIVED_DIAGNOSTIC_WHEELHOUSE';o['OLEANDER_AUTHORITY']='NONE'
    return o

def build_locked_source(M,glass):
    r16.deform_at_x=r22.deform_at_x;r16.ARCH_ZONE_R=r22.SAMPLE_ZONE
    return r22.build_r20_current(M,glass)

def render_views(out,samples,res,M,L,source,liners):
    rd=out/'renders';rd.mkdir(parents=True,exist_ok=True);R=[]
    V=[
      ('FRONT_ARCH_ISOLATED',(2.65,-3.4,.95),(b.FX,-b.WY,.48),100,'STRIP','front'),
      ('REAR_ARCH_ISOLATED',(-2.55,-3.4,.95),(b.RX,-b.WY,.48),100,'STRIP','rear'),
      ('FRONT_ARCH_GRAZING',(2.65,-3.4,.95),(b.FX,-b.WY,.48),100,'GRAZING','front'),
      ('REAR_ARCH_GRAZING',(-2.55,-3.4,.95),(b.RX,-b.WY,.48),100,'GRAZING','rear'),
      ('PACKAGE_SIDE_WITH_WHEELHOUSE',(0,-8.8,1.14),(0,0,.64),85,'BROAD','all'),
      ('HERO_FRONT_WITH_WHEELHOUSE',(6.2,-7.0,2.75),(.05,0,.66),78,'BROAD','all'),
    ]
    wheel_objs=[o for o in bpy.context.scene.objects if o.name.startswith('WHEEL_')]
    for lab,loc,tgt,lens,rig,scope in V:
        b.setrig(L,rig);b.world((.012,.012,.012),.16)
        for o in wheel_objs:
            if scope=='all':o.hide_render=False
            elif scope=='front':o.hide_render=(o.location.y>0 or abs(o.location.x-b.FX)>.2)
            elif scope=='rear':o.hide_render=(o.location.y>0 or abs(o.location.x-b.RX)>.2)
        for wh in liners:
            if scope=='all':wh.hide_render=False
            elif scope=='front':wh.hide_render=('FRONT' not in wh.name or wh.location.y>0)
            elif scope=='rear':wh.hide_render=('REAR' not in wh.name or wh.location.y>0)
        c=b.camera('CAM_'+lab,loc,tgt,lens,False,5);bpy.context.scene.camera=c
        p=rd/f'{MODEL}__{lab}.png';b.setup(p,samples,res);bpy.ops.render.render(write_still=True)
        R.append({'view':lab,'file':str(p),'scope':scope});bpy.data.objects.remove(c,do_unlink=True)
    for o in wheel_objs:o.hide_render=False
    for wh in liners:wh.hide_render=False
    return R

def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);b.clear();M=b.materials();glass=r14.diagnostic_glass()
    source,xs,cols,flipped=build_locked_source(M,glass)
    h0=r20.shape_hash(source);top0=r22.topology_membership_hash(source)
    b.wheels(M);whm=diag_mat();liners=[]
    for wx,wname in ((b.FX,'FRONT'),(b.RX,'REAR')):
        for side,sname in ((1,'L'),(-1,'R')):
            wh=make_wheelhouse(f'DIAG_WHEELHOUSE_{wname}_{sname}',wx,side,whm)
            wh['SIDE']=side;liners.append(wh)
    for wh in liners:
        wh.location.y=.001 if wh.name.endswith('_L') else -.001
    b.ground(M);L=b.rigs();b.world((.012,.012,.012),.16)
    h1=r20.shape_hash(source);top1=r22.topology_membership_hash(source)

    scene=bpy.context.scene;scene['OLEANDER_MODEL']=MODEL;scene['OLEANDER_STAGE']='M5';scene['OLEANDER_REVISION']='R23 diagnostic-only wheelhouse isolation; R22 source locked'
    r14.write_contract(out,source,r14.topology_stats(source),0)
    cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text())
    c['job_id']='SYS-MODELING-WORKER-AUTO-M5-v0.11-R23'
    c['decision_question']='With R22 source completely locked, do derived wheelhouse liners and near-side wheel isolation show that the remaining black wheel-zone regions were diagnostic cavity/far-wheel artifacts rather than Source arch tears?'
    c['source_authority']['editable_source']=f'{MODEL}.blend';c['source_authority']['artifact_hash']=h0;c['source_authority']['derived_models']=['DIAG_WHEELHOUSE_FRONT_L/R','DIAG_WHEELHOUSE_REAR_L/R']
    c['locks'].append({'target':'entire R22 source coordinates/topology/hard points/sections','state':'LOCKED','reason':'R23 is diagnostic isolation only','unlock_trigger':'R23 Visual QA confirms genuine Source failure'})
    c['revision']={'revision_id':'R23-WHEELHOUSE-DIAGNOSTIC','semantic_targets':['derived diagnostic only'],'parameters':{'source_change':False,'wheelhouse_radius_m':.418,'far_wheel_hidden_in_detail':True},'expected_affected_components':['render evidence only'],'affected_view_policy':'MANUAL'}
    c['qa']['construction']=['R22 shape hash before == after','R22 topology membership hash before == after','four derived wheelhouse liners only','no source modifier/change']
    c['qa']['project']=['if isolated outer arch is clean, retain R22 curvature and proceed to full M5 matrix','if outer edge still tears/scallops materially, reopen wheel-zone M4','wheelhouse is not M6/M7 authority']
    c['resource_budget']['max_render_views']=6
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')

    blend=out/f'{MODEL}.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    R=render_views(out,a.samples,a.resolution,M,L,source,liners)
    h2=r20.shape_hash(source);top2=r22.topology_membership_hash(source)
    checks={'source_shape_hash_locked':h0==h1==h2,'source_topology_hash_locked':top0==top1==top2,'wheelhouse_count_four':len(liners)==4,
            'termination_winding_repair_retained':len(flipped)==28,'source_no_boolean':not any(m.type=='BOOLEAN' for m in source.modifiers),
            'source_no_subd':not any(m.type=='SUBSURF' for m in source.modifiers),'render_matrix':len(R)==6}
    q={'schema':'oleander.auto.v0.11.r23.qa','model':MODEL,'status':'MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL',
       'source_shape_hash':h0,'source_topology_membership_hash':top0,'checks':checks,'renders':R,
       'boundary':'R23 adds derived diagnostic wheelhouses and view isolation only. R22 Source geometry is unchanged.'}
    (out/'AUTOMOTIVE_V011_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    rec={'schema':'oleander.auto.v0.11.r23.receipt','model':MODEL,'blender_version':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),'renderer':'Cycles CPU','samples':a.samples,'resolution':[a.resolution,a.resolution],'status':'EXECUTED_'+q['status'],'blend':str(blend),'qa':str(out/'AUTOMOTIVE_V011_QA.json'),'renders':R}
    (out/'AUTOMOTIVE_V011_RECEIPT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if all(checks.values()) else 5)

if __name__=='__main__':main()
