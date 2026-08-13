#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R24 — Integrated Local Wheel-Arch Topology.

R23 diagnostic proved the front/rear black wedges are genuine Source wheel-zone failures.
R24 replaces the R16/R17/R22 global row deformation model.

Locked:
- R09 cabin/wheel hard points
- R11 transverse tension outside wheel zones
- R12 PCHIP longitudinal interpolation
- R15 local front/rear taper
- R18 structured termination + R20 termination winding

R24 source construction:
- upper grid CENTER_TOP -> SHOULDER remains shared;
- outside wheel zones, MID/ROCKER/UNDER grid remains unchanged;
- inside each wheel zone, lower body is replaced by an integrated local quad patch:
  SHOULDER(shared) -> B1 -> B2 -> INNER_ARCH;
- at wheel-zone endpoints B1/B2/INNER directly reuse the existing MID/ROCKER/UNDER
  vertices, eliminating duplicate patch endpoints and T-junctions;
- inner arch and blend loops use C1 cosine-squared interpolation;
- no Source Boolean/SubD/ngon.
"""
from __future__ import annotations
import importlib.util,bpy,json,math,hashlib
from pathlib import Path

BASE='/tmp/revise_v011_r20.py'
spec=importlib.util.spec_from_file_location('r20',BASE)
r20=importlib.util.module_from_spec(spec);spec.loader.exec_module(r20)
r18=r20.r18;r16=r20.r16;r14=r20.r14;b=r20.b

MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R24'
r20.MODEL=MODEL;r18.MODEL=MODEL;r16.MODEL=MODEL;r16.r15.MODEL=MODEL
r14.MODEL=MODEL;r14.r12.MODEL=MODEL;r14.r11.MODEL=MODEL;r14.r10.MODEL=MODEL
r14.r09.MODEL=MODEL;r14.r08.MODEL;r14.r08.r.MODEL=MODEL;b.MODEL=MODEL

ZONE=.500
ARCH_TOP_Z=.755
ANGLES=[math.radians(v) for v in range(0,181,6)]

def weight(x,wx):
    u=(x-wx)/ZONE
    if abs(u)>=1:return 0.0
    return math.cos(math.pi*u/2.0)**2

def union_xs(rows):
    xs={round(p[0],9) for p in rows[0]}
    for wx in (b.FX,b.RX):
        xs.add(round(wx-ZONE,9));xs.add(round(wx+ZONE,9))
        for a in ANGLES:xs.add(round(wx+ZONE*math.cos(a),9))
    return sorted(xs,reverse=True)

def interp_rows(rows,x):
    return [r14.interp_row(row,x) for row in rows]

def build_source(rows,M,glass):
    xs=union_xs(rows);cols=[interp_rows(rows,x) for x in xs]
    mb=r14.MB()
    def K(i,row,side):return f'X{i}:R{row}:S{side:+d}'
    def V(i,row,side):
        p=cols[i][row]
        if row==4:
            w=max(weight(p[0],b.FX),weight(p[0],b.RX));p=(p[0],p[1]+.012*w,p[2]+.018*w)
        if row==3:
            w=max(weight(p[0],b.FX),weight(p[0],b.RX));p=(p[0],p[1]+.003*w,p[2]+.005*w)
        if row==0:return mb.v(K(i,row,0),(p[0],0,p[2]))
        return mb.v(K(i,row,side),(p[0],side*p[1],p[2]))

    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        for side in (1,-1):
            for arow,brow in ((0,1),(1,2),(2,3),(3,4)):
                a0=V(i,arow,side if arow else 0);a1=V(i+1,arow,side if arow else 0);b1=V(i+1,brow,side);b0=V(i,brow,side)
                ids=(a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1);glass_band=(arow,brow) in ((1,2),(2,3)) and -1.22<=cx<=.72;mb.f(ids,1 if glass_band else 0)

    def interval_in_zone(cx):return any(abs(cx-wx)<ZONE-1e-8 for wx in (b.FX,b.RX))
    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        if interval_in_zone(cx):continue
        for side in (1,-1):
            for arow,brow in ((4,5),(5,6),(6,7)):
                a0=V(i,arow,side);a1=V(i+1,arow,side);b1=V(i+1,brow,side);b0=V(i,brow,side);mb.f((a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1),0)
        mb.f((V(i,7,1),V(i+1,7,1),V(i+1,7,-1),V(i,7,-1)),0)

    arch_meta=[];endpoint_reuse=0
    for wx,wname in ((b.FX,'F'),(b.RX,'R')):
        zone_indices=sorted([i for i,x in enumerate(xs) if abs(x-wx)<=ZONE+1e-8])
        for side in (1,-1):
            sname='L' if side>0 else 'R';crown=[];b1s=[];b2s=[];inner=[]
            for jj,gi in enumerate(zone_indices):
                x=xs[gi];w=weight(x,wx);base=cols[gi];crown.append(V(gi,4,side))
                if jj==0 or jj==len(zone_indices)-1:
                    b1s.append(V(gi,5,side));b2s.append(V(gi,6,side));inner.append(V(gi,7,side));endpoint_reuse+=3;continue
                shoulder=base[4];mid=base[5];rock=base[6];under=base[7]
                inner_z=under[2]+w*(ARCH_TOP_Z-under[2]);inner_y=under[1]+w*((shoulder[1]-.016)-under[1])
                b2_z=rock[2]+w*((inner_z+.045)-rock[2]);b2_y=rock[1]+w*((shoulder[1]-.010)-rock[1])
                b1_z=mid[2]+w*((inner_z+.095)-mid[2]);b1_y=mid[1]+w*((shoulder[1]-.004)-mid[1])
                b1s.append(mb.v(f'ARCH:{wname}:{sname}:B1:{jj}',(x,side*b1_y,b1_z)))
                b2s.append(mb.v(f'ARCH:{wname}:{sname}:B2:{jj}',(x,side*b2_y,b2_z)))
                inner.append(mb.v(f'ARCH:{wname}:{sname}:INNER:{jj}',(x,side*inner_y,inner_z)))
            for j in range(len(zone_indices)-1):
                for A,B in ((crown,b1s),(b1s,b2s),(b2s,inner)):
                    ids=(A[j],A[j+1],B[j+1],B[j]);mb.f(ids if side>0 else tuple(reversed(ids)),0)
            arch_meta.append((wname,sname,crown,inner))

    for i,label,sign,offs in ((0,'FRONT',1,r18.FRONT_OFF),(len(xs)-1,'REAR',-1,r18.REAR_OFF)):
        right=[V(i,r,1) for r in range(1,8)];left=[V(i,r,-1) for r in range(1,8)];center_top=V(i,0,0);centers=[]
        for j in range(7):
            rv=mb.verts[right[j]];lv=mb.verts[left[j]];centers.append(mb.v(f'TERM:{label}:C{j}',(xs[i]+sign*offs[j],0,(rv[2]+lv[2])*.5)))
        t1=(center_top,right[0],centers[0]);t2=(center_top,centers[0],left[0])
        if label=='REAR':t1=tuple(reversed(t1));t2=tuple(reversed(t2))
        mb.f(t1);mb.f(t2)
        for j in range(6):
            rq=(centers[j],right[j],right[j+1],centers[j+1]);lq=(centers[j],centers[j+1],left[j+1],left[j])
            if label=='REAR':rq=tuple(reversed(rq));lq=tuple(reversed(lq))
            mb.f(rq);mb.f(lq)

    me=bpy.data.meshes.new('PRIMARY_LOCAL_ARCH_SOURCE_MESH');me.from_pydata(mb.verts,[],mb.faces);me.update();o=bpy.data.objects.new('PRIMARY_LOCAL_ARCH_SOURCE',me);bpy.context.collection.objects.link(o);o.data.materials.append(M['CLAY']);o.data.materials.append(glass)
    for p,mi in zip(o.data.polygons,mb.face_mat):p.use_smooth=True;p.material_index=mi
    o['OLEANDER_AUTHORITY']='WORKING_SOURCE';o['OLEANDER_TOPOLOGY']='R24_SHARED_ENDPOINT_LOCAL_ARCH';return o,xs,cols,arch_meta,endpoint_reuse

def feature_guides(source,xs,cols,arch_meta,M):
    FM={'arch':r14.feature_mat('MAT_FEATURE_ARCH_R24',(1,.55,.02,1)),'crown':r14.feature_mat('MAT_FEATURE_CROWN_R24',(1,.06,.32,1))};objs=[]
    for wname,sname,crown,inner in arch_meta:
        objs.append(r14.curve(f'FEATURE_FENDER_CROWN_{wname}{sname}',[source.data.vertices[i].co[:] for i in crown],FM['crown'],.006));objs.append(r14.curve(f'FEATURE_WHEEL_ARCH_{wname}{sname}',[source.data.vertices[i].co[:] for i in inner],FM['arch'],.006))
    return objs

def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);b.clear();M=b.materials();glass=r14.diagnostic_glass();rows=b.controls_resampled();source,xs,cols,arch_meta,reuse=build_source(rows,M,glass);h0=r20.shape_hash(source)
    features=feature_guides(source,xs,cols,arch_meta,M);b.wheels(M);b.ground(M);L=b.rigs();b.world((.012,.012,.012),.16);wire=r14.wire_overlay(source,M);stats=r14.topology_stats(source);islands=r16.island_count(source);h1=r20.shape_hash(source)
    scene=bpy.context.scene;scene['OLEANDER_MODEL']=MODEL;scene['OLEANDER_STAGE']='M5';scene['OLEANDER_REVISION']='R24 shared-endpoint local wheel arch topology'
    r14.write_contract(out,source,stats,len(features));cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text());c['job_id']='SYS-MODELING-WORKER-AUTO-M3M5-v0.11-R24';c['decision_question']='Does replacing the global row-deformation wheel zone with a single-mesh local quad patch that shares SHOULDER and reuses MID/ROCKER/UNDER endpoint vertices eliminate the R23 black wedges and scalloped arch transitions?';c['source_authority']['editable_source']=f'{MODEL}.blend';c['source_authority']['artifact_hash']=h0;c['primary_geometry'][0]['id']='PG-LOCAL-ARCH-SOURCE';c['primary_geometry'][0]['role']='integrated primary source with shared-endpoint local wheel-arch patches';c['semantic_components'][1]['id']='COMP-LOCAL-ARCH-SOURCE';c['semantic_components'][1]['role']='R24 editable primary source';c['semantic_components'][1]['source_ref']='PG-LOCAL-ARCH-SOURCE';c['revision']={'revision_id':'R24-SHARED-ENDPOINT-LOCAL-ARCH','semantic_targets':['front/rear wheel zones'],'parameters':{'zone_radius_m':ZONE,'weight':'cos(pi*u/2)^2','arch_top_z_m':ARCH_TOP_Z,'endpoint_reuse':'MID/ROCKER/UNDER','source_boolean':False,'source_subd':False},'expected_affected_components':['wheel-zone primary source topology only'],'affected_view_policy':'HYBRID'};c['qa']['construction']=['one connected source mesh','wheel-zone patch shares SHOULDER vertices','B1/B2/INNER endpoints reuse MID/ROCKER/UNDER vertices','source n-gon=0','no Source Boolean/SubD','R18-style structured terminations retained'];c['qa']['project']=['R23 front black wedge must close','rear arch endpoint must close','outer arch silhouette must stop scalloping materially','M6/M7/M8 remains blocked'];c['resource_budget']['max_render_views']=9;cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    blend=out/f'{MODEL}.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend));rd=out/'renders';rd.mkdir(parents=True,exist_ok=True);records=[]
    V=[('SIDE_SILHOUETTE',(0,-8.8,1.14),(0,0,.64),85,True,5.25,'BROAD','sil'),('PACKAGE_SIDE',(0,-8.8,1.14),(0,0,.64),85,True,5.25,'BROAD','normal'),('HERO_FRONT_3Q',(6.2,-7.0,2.75),(.05,0,.66),78,False,5,'BROAD','normal'),('HERO_REAR_3Q',(-6.0,6.8,2.65),(-.10,0,.66),78,False,5,'BROAD','normal'),('CLAY_STRIP',(6.2,-7.0,2.75),(.05,0,.66),78,False,5,'STRIP','normal'),('CLAY_GRAZING',(6.2,-7.0,2.75),(.05,0,.66),78,False,5,'GRAZING','normal'),('FRONT_ARCH_DETAIL',(2.65,-3.4,.95),(b.FX,-b.WY,.48),100,False,5,'STRIP','normal'),('REAR_ARCH_DETAIL',(-2.55,-3.4,.95),(b.RX,-b.WY,.48),100,False,5,'STRIP','normal'),('SOURCE_WIREFRAME',(5.8,-6.4,2.8),(0,0,.66),80,False,5,'BROAD','wire')]
    for lab,loc,t,lens,ortho,scale,rig,mode in V:
        b.setrig(L,rig);wire.hide_render=(mode!='wire');source.hide_render=(mode=='wire');[setattr(o,'hide_render',True) for o in features];b.world((1,1,1),.75) if mode=='sil' else b.world((.012,.012,.012),.16);bpy.context.view_layer.material_override=M['BLACK'] if mode=='sil' else None;cam=b.camera('CAM_'+lab,loc,t,lens,ortho,scale);bpy.context.scene.camera=cam;p=rd/f'{MODEL}__{lab}.png';b.setup(p,a.samples,a.resolution);bpy.ops.render.render(write_still=True);records.append({'view':lab,'file':str(p),'mode':mode});bpy.data.objects.remove(cam,do_unlink=True)
    bpy.context.view_layer.material_override=None;source.hide_render=False;mods=[m.type for m in source.modifiers];checks={'source_hash_stable_during_diagnostics':h0==h1,'source_island_count_one':islands==1,'source_ngon_zero':stats['ngon']==0,'termination_triangles_four':stats['tri']==4,'source_no_boolean':'BOOLEAN' not in mods,'source_no_subd':'SUBSURF' not in mods,'arch_endpoint_vertex_reuse_24':reuse==24,'four_arch_boundaries':len([o for o in features if 'FEATURE_WHEEL_ARCH_' in o.name])==4,'render_matrix':len(records)==9};q={'schema':'oleander.auto.v0.11.r24.qa','model':MODEL,'status':'MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL','source_hash':h0,'topology':stats,'source_island_count':islands,'endpoint_reuse_count':reuse,'checks':checks,'renders':records,'boundary':'R24 changes wheel-zone Source topology only. M5 Visual QA required; M6/M7/M8 blocked.'};(out/'AUTOMOTIVE_V011_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');rec={'schema':'oleander.auto.v0.11.r24.receipt','model':MODEL,'blender_version':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),'renderer':'Cycles CPU','samples':a.samples,'resolution':[a.resolution,a.resolution],'status':'EXECUTED_'+q['status'],'blend':str(blend),'qa':str(out/'AUTOMOTIVE_V011_QA.json'),'renders':records};(out/'AUTOMOTIVE_V011_RECEIPT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if all(checks.values()) else 5)

if __name__=='__main__':main()
