#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R29A-DIAG.

Source-locked Human M5 diagnostic for the retained R29A shoulder-fed crown direction.
No Source coordinate/topology/design-variable changes. It adds derived-only near-side
wheelhouse liners and hides far-side wheels so the black open-cavity artifact can be
separated from true lip / hood-fender continuity defects.
"""
from __future__ import annotations
import importlib.util,bpy,json,math
from pathlib import Path

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
r29a=load('/tmp/revise_v011_r29a.py','r29a')
r25=r29a.r25;r24=r29a.r24;r20=r29a.r20;r14=r29a.r14;b=r29a.b
MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R29A_DIAG'
for m in (r29a,r25,r24,r20,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):m.MODEL=MODEL

def diag_mat():return b.mat('MAT_WHEELHOUSE_DIAGNOSTIC',(.055,.060,.065,1),.58)
def make_wheelhouse(name,wx,side,ma):
    r=.405;angles=[math.radians(v) for v in range(10,171,5)];y0=side*.690;y1=side*.535;verts=[];faces=[]
    for a in angles:
        x=wx+r*math.cos(a);z=b.WZ+r*math.sin(a);verts.extend([(x,y0,z),(x,y1,z)])
    for i in range(len(angles)-1):
        k=2*i;f=(k,k+2,k+3,k+1);faces.append(f if side>0 else tuple(reversed(f)))
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(ma)
    for p in me.polygons:p.use_smooth=True
    o['OLEANDER_ROLE']='DERIVED_DIAGNOSTIC_WHEELHOUSE';o['OLEANDER_AUTHORITY']='NONE';return o

def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);b.clear();M=b.materials();glass=r14.diagnostic_glass();rows=b.controls_resampled();source,xs,cols,arch_meta,reuse=r29a.build_source_r29a(rows,M,glass);h0=r20.shape_hash(source);features=r24.feature_guides(source,xs,cols,arch_meta,M)
    b.wheels(M);wheel_exact=bool(getattr(b,'_OLEANDER_WHEEL_HP_EXACT',False));wheel_records=getattr(b,'_OLEANDER_WHEEL_HP_RECORDS',[])
    whm=diag_mat();liners=[]
    for wx,wname in ((b.FX,'FRONT'),(b.RX,'REAR')):
        for side,sname in ((1,'L'),(-1,'R')):liners.append(make_wheelhouse(f'DIAG_WHEELHOUSE_{wname}_{sname}',wx,side,whm))
    b.ground(M);L=b.rigs();b.world((.012,.012,.012),.16);h1=r20.shape_hash(source)
    rd=out/'renders';rd.mkdir(parents=True,exist_ok=True);R=[];wheel_objs=[o for o in bpy.context.scene.objects if o.name.startswith('WHEEL_')]
    views=[
      ('FRONT_ARCH_BROAD_ISOLATED',(2.65,-3.4,.95),(b.FX,-b.WY,.48),100,'BROAD','front'),
      ('FRONT_ARCH_STRIP_ISOLATED',(2.65,-3.4,.95),(b.FX,-b.WY,.48),100,'STRIP','front'),
      ('FRONT_ARCH_GRAZING_ISOLATED',(2.65,-3.4,.95),(b.FX,-b.WY,.48),100,'GRAZING','front'),
      ('REAR_ARCH_BROAD_ISOLATED',(-2.55,-3.4,.95),(b.RX,-b.WY,.48),100,'BROAD','rear'),
      ('REAR_ARCH_STRIP_ISOLATED',(-2.55,-3.4,.95),(b.RX,-b.WY,.48),100,'STRIP','rear'),
      ('REAR_ARCH_GRAZING_ISOLATED',(-2.55,-3.4,.95),(b.RX,-b.WY,.48),100,'GRAZING','rear'),
      ('HERO_FRONT_NEARSIDE',(6.2,-7.0,2.75),(.05,0,.66),78,'BROAD','near'),
      ('HERO_REAR_NEARSIDE',(-6.0,-6.8,2.65),(-.10,0,.66),78,'BROAD','near')]
    for lab,loc,tgt,lens,rig,scope in views:
        b.setrig(L,rig);b.world((.012,.012,.012),.16)
        for f in features:f.hide_render=True
        for o in wheel_objs:
            if scope=='front':o.hide_render=(o.location.y>0 or abs(o.location.x-b.FX)>.3)
            elif scope=='rear':o.hide_render=(o.location.y>0 or abs(o.location.x-b.RX)>.3)
            else:o.hide_render=(o.location.y>0)
        for wh in liners:
            if scope=='front':wh.hide_render=('FRONT' not in wh.name or not wh.name.endswith('_R'))
            elif scope=='rear':wh.hide_render=('REAR' not in wh.name or not wh.name.endswith('_R'))
            else:wh.hide_render=(not wh.name.endswith('_R'))
        cam=b.camera('CAM_'+lab,loc,tgt,lens,False,5);bpy.context.scene.camera=cam;p=rd/f'{MODEL}__{lab}.png';b.setup(p,a.samples,a.resolution);bpy.ops.render.render(write_still=True);R.append({'view':lab,'file':str(p),'scope':scope});bpy.data.objects.remove(cam,do_unlink=True)
    h2=r20.shape_hash(source);checks={'source_shape_hash_locked':h0==h1==h2,'source_no_boolean':not any(m.type=='BOOLEAN' for m in source.modifiers),'source_no_subd':not any(m.type=='SUBSURF' for m in source.modifiers),'wheel_hp_package_exact':wheel_exact,'wheelhouse_count_four':len(liners)==4,'render_matrix':len(R)==8}
    q={'schema':'oleander.auto.v0.11.r29a.diag.qa','model':MODEL,'status':'MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL','source_shape_hash':h0,'wheel_hp_package':wheel_records,'checks':checks,'renders':R,'boundary':'Diagnostic-only liners and far-wheel hiding. R29A Source geometry remains hash-locked; no crown/opening/topology variables change.'};(out/'AUTOMOTIVE_V011_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    c={'contract_version':'v0.2','spec_patch':'v0.2.1','job_id':'SYS-MODELING-WORKER-AUTO-M5-v0.11-R29A-DIAG','modeling_stage':'M5','design_state':'REVISE_WITH_DIRECTION_RETAINED','source_authority':{'state':'WORKING_SOURCE_LOCKED_FOR_DIAGNOSTIC','artifact_hash':h0},'revision':{'revision_id':'R29A-WHEELHOUSE-DIAGNOSTIC','source_change':False},'qa':{'construction':['R29A Source hash before == after','exact HP wheel package retained','four derived-only wheelhouse liners','far-side wheels hidden'],'project':['separate cavity artifact from true lip/hood-fender discontinuity','M6/M7/M8 remains blocked']}};(out/'MODELING_CONTRACT.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    raise SystemExit(0 if all(checks.values()) else 5)
if __name__=='__main__':main()
