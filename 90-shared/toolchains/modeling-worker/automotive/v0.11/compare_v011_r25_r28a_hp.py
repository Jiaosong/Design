#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 — hard-point-correct R25 vs R28A visual rebaseline.

Source-locked A/B diagnostic. No candidate geometry is revised.
Both candidates use the same corrected wheel package and identical evidence matrix.
"""
from __future__ import annotations
import argparse,importlib.util,bpy,json,math,sys
from pathlib import Path

def cli():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--variant',choices=['R25','R28A'],required=True);p.add_argument('--samples',type=int,default=8);p.add_argument('--resolution',type=int,default=640);return p.parse_args(argv)
def load(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def bounds(pts):
    mn=[min(p[i] for p in pts) for i in range(3)];mx=[max(p[i] for p in pts) for i in range(3)];return {'min':mn,'max':mx,'dimensions':[mx[i]-mn[i] for i in range(3)],'center':[(mn[i]+mx[i])*.5 for i in range(3)]}
def raw_wb(o):return bounds([o.matrix_world@v.co for v in o.data.vertices])
def eval_wb(o):
    dg=bpy.context.evaluated_depsgraph_get();oe=o.evaluated_get(dg);me=oe.to_mesh()
    try:return bounds([oe.matrix_world@v.co for v in me.vertices])
    finally:oe.to_mesh_clear()
def near(a,b,t=1e-5):return abs(a-b)<t

def normalize_wheels(b,M,target_od=.700):
    b.wheels(M);records=[]
    for o in [x for x in bpy.context.scene.objects if x.type=='MESH' and x.name.startswith('WHEEL_')]:
        before=raw_wb(o);code=o.name.split('_')[1];x=b.FX if code.startswith('F') else b.RX;y=b.WY if code.endswith('L') else -b.WY;z=b.WZ;target=[float(x),float(y),float(z)];cx,cy,cz=before['center'];dx,dy,dz=before['dimensions'];fx=target_od/dx;fz=target_od/dz;inv=o.matrix_world.inverted()
        for v in o.data.vertices:
            p=o.matrix_world@v.co;p.x=target[0]+(p.x-cx)*fx;p.y=target[1]+(p.y-cy);p.z=target[2]+(p.z-cz)*fz;v.co=inv@p
        o.data.update();bpy.context.view_layer.update();after=eval_wb(o);records.append({'name':o.name,'wheel_code':code,'target_center':target,'before_raw':before,'after_evaluated':after,'y_thickness_target':dy})
    ok=len(records)==4 and all(near(r['after_evaluated']['dimensions'][0],target_od) and near(r['after_evaluated']['dimensions'][2],target_od) and near(r['after_evaluated']['dimensions'][1],r['y_thickness_target']) and all(near(r['after_evaluated']['center'][i],r['target_center'][i]) for i in range(3)) for r in records)
    side_ok=all((r['target_center'][1]>0)==r['wheel_code'].endswith('L') for r in records)
    return records,ok and side_ok

def diag_mat(b):return b.mat('MAT_WHEELHOUSE_DIAGNOSTIC',(.055,.060,.065,1),.58)
def wheelhouse(b,name,wx,side,ma):
    r=.418;angles=[math.radians(v) for v in range(12,169,6)];y0=side*.655;y1=side*.515;verts=[];faces=[]
    for a in angles:
        x=wx+r*math.cos(a);z=b.WZ+r*math.sin(a);verts.extend([(x,y0,z),(x,y1,z)])
    for i in range(len(angles)-1):
        k=2*i;f=(k,k+2,k+3,k+1);faces.append(f if side>0 else tuple(reversed(f)))
    me=bpy.data.meshes.new(name+'_M');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(ma)
    for p in me.polygons:p.use_smooth=True
    o['OLEANDER_AUTHORITY']='NONE';o['OLEANDER_ROLE']='DERIVED_DIAGNOSTIC_WHEELHOUSE';return o

def main():
    a=cli();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
    if a.variant=='R25':
        mod=load('/tmp/revise_v011_r25.py','candidate_r25');b=mod.b;r14=mod.r14;r20=mod.r20;r16=mod.r16;r24=mod.r24;builder=mod.build_source_raw;model='OLEANDER_Automotive_v0.11_R25_HP_REBASELINE'
    else:
        mod=load('/tmp/revise_v011_r28a.py','candidate_r28a');b=mod.b;r14=mod.r14;r20=mod.r20;r16=mod.r16;r24=mod.r24;builder=mod.build_source_r28a;model='OLEANDER_Automotive_v0.11_R28A_HP_REBASELINE'
    b.clear();M=b.materials();glass=r14.diagnostic_glass();rows=b.controls_resampled();source,xs,cols,arch_meta,reuse=builder(rows,M,glass);h0=r20.shape_hash(source);stats=r14.topology_stats(source);islands=r16.island_count(source)
    features=r24.feature_guides(source,xs,cols,arch_meta,M);wheel_records,wheel_ok=normalize_wheels(b,M);whm=diag_mat(b);liners=[]
    for wx,wname in ((b.FX,'FRONT'),(b.RX,'REAR')):
        for side,sname in ((1,'L'),(-1,'R')):liners.append(wheelhouse(b,f'DIAG_WHEELHOUSE_{wname}_{sname}',wx,side,whm))
    b.ground(M);L=b.rigs();b.world((.012,.012,.012),.16);wire=r14.wire_overlay(source,M);h1=r20.shape_hash(source)
    rd=out/'renders';rd.mkdir(parents=True,exist_ok=True);R=[];wheel_objs=[o for o in bpy.context.scene.objects if o.name.startswith('WHEEL_')]
    views=[('SIDE_SILHOUETTE_HP',(0,-8.8,1.14),(0,0,.64),85,True,5.25,'BROAD','sil','near'),('PACKAGE_SIDE_NEARSIDE',(0,-8.8,1.14),(0,0,.64),85,True,5.25,'BROAD','normal','near'),('HERO_FRONT_NEARSIDE',(6.2,-7.0,2.75),(.05,0,.66),78,False,5,'BROAD','normal','near'),('HERO_REAR_NEARSIDE',(-6.0,-6.8,2.65),(-.10,0,.66),78,False,5,'BROAD','normal','near'),('CLAY_STRIP_NEARSIDE',(6.2,-7.0,2.75),(.05,0,.66),78,False,5,'STRIP','normal','near'),('CLAY_GRAZING_NEARSIDE',(6.2,-7.0,2.75),(.05,0,.66),78,False,5,'GRAZING','normal','near'),('FRONT_ARCH_ISOLATED',(2.65,-3.4,.95),(b.FX,-b.WY,.48),100,False,5,'STRIP','normal','front'),('REAR_ARCH_ISOLATED',(-2.55,-3.4,.95),(b.RX,-b.WY,.48),100,False,5,'STRIP','normal','rear'),('SOURCE_WIREFRAME',(5.8,-6.4,2.8),(0,0,.66),80,False,5,'BROAD','wire','near')]
    for lab,loc,tgt,lens,ortho,scale,rig,mode,scope in views:
        b.setrig(L,rig);wire.hide_render=(mode!='wire');source.hide_render=(mode=='wire')
        for f in features:f.hide_render=True
        for o in wheel_objs:
            if scope=='front':o.hide_render=(o.location.y>0 or abs(o.location.x-b.FX)>.3)
            elif scope=='rear':o.hide_render=(o.location.y>0 or abs(o.location.x-b.RX)>.3)
            else:o.hide_render=(o.location.y>0)
        for wh in liners:
            if mode in ('wire','sil'):wh.hide_render=True
            elif scope=='front':wh.hide_render=('FRONT' not in wh.name or not wh.name.endswith('_R'))
            elif scope=='rear':wh.hide_render=('REAR' not in wh.name or not wh.name.endswith('_R'))
            else:wh.hide_render=(not wh.name.endswith('_R'))
        if mode=='sil':b.world((1,1,1),.75);bpy.context.view_layer.material_override=M['BLACK']
        else:b.world((.012,.012,.012),.16);bpy.context.view_layer.material_override=None
        cam=b.camera('CAM_'+lab,loc,tgt,lens,ortho,scale);bpy.context.scene.camera=cam;p=rd/f'{model}__{lab}.png';b.setup(p,a.samples,a.resolution);bpy.ops.render.render(write_still=True);R.append({'view':lab,'file':str(p),'scope':scope,'mode':mode});bpy.data.objects.remove(cam,do_unlink=True)
    bpy.context.view_layer.material_override=None;source.hide_render=False;h2=r20.shape_hash(source);mods=[m.type for m in source.modifiers];blend=out/f'{model}.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    checks={'source_shape_hash_locked':h0==h1==h2,'source_island_count_one':islands==1,'source_ngon_zero':stats['ngon']==0,'termination_triangles_four':stats['tri']==4,'source_no_boolean':'BOOLEAN' not in mods,'source_no_subd':'SUBSURF' not in mods,'wheel_hp_package_exact':wheel_ok,'wheel_left_right_mapping_exact':all((r['after_evaluated']['center'][1]>0)==r['wheel_code'].endswith('L') for r in wheel_records),'wheelhouse_count_four':len(liners)==4,'render_matrix':len(R)==9}
    q={'schema':'oleander.auto.v0.11.hp-rebaseline.v2.qa','variant':a.variant,'model':model,'status':'MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL','source_hash':h0,'topology':stats,'source_island_count':islands,'source_boundary_reuse_or_endpoint_count':reuse,'wheel_package':wheel_records,'checks':checks,'renders':R,'boundary':'Source candidate locked. A/B enforces OD=0.70 and exact current FX/RX, +/-WY, WZ with FL/RL on +Y and FR/RR on -Y; same derived wheelhouse/near-side evidence; no design variable revision.'};(out/'AB_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    c={'contract_version':'v0.2','spec_patch':'v0.2.1','job_id':f'SYS-MODELING-WORKER-AUTO-M1M5-v0.11-{a.variant}-HP-REBASELINE-v2','modeling_stage':'M5','design_state':'REVISE','authority_state':'DIAGNOSTIC_ONLY','source_authority':{'state':'LOCKED_FOR_AB_REBASELINE','artifact_hash':h0},'revision':{'source_change':False,'wheel_package_change':'deterministic implementation correction to exact current M1 hard points','left_right_mapping':'FL/RL +Y; FR/RR -Y','comparison_peer':'R28A' if a.variant=='R25' else 'R25'},'qa':{'project':['compare package, arch containment, shoulder/fender continuity, strip/grazing curvature and wire topology under identical corrected wheel evidence','M6/M7/M8 remains blocked']}};(out/'MODELING_CONTRACT.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'variant':a.variant,'status':q['status'],'source_hash':h0,'topology':stats,'wheel_package_exact':wheel_ok,'renders':len(R)},ensure_ascii=False));raise SystemExit(0 if all(checks.values()) else 5)
if __name__=='__main__':main()
