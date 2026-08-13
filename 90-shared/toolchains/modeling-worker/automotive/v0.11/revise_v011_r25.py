#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R25 — Rounded Wheel-Opening Profile.

R24 Machine Gate passed, but human M5 Visual QA failed:
- front/rear opening still reads as a V/triangular wedge;
- wheel/tire visibly pierces the body envelope in arch detail;
- fender crown reads as an isolated cap rather than a shoulder-fed local surface.

R25 reopens only wheel-zone M4 geometry. R09/R11/R12 package and the non-wheel source remain locked.
The R24 single-mesh/shared-endpoint topology concept is retained; only the local arch profile law and
nested B1/B2/crown shaping are revised.
"""
from __future__ import annotations
import importlib.util,bpy,json,math
from pathlib import Path

BASE='/tmp/revise_v011_r24.py'
spec=importlib.util.spec_from_file_location('r24',BASE)
r24=importlib.util.module_from_spec(spec);spec.loader.exec_module(r24)
r20=r24.r20;r18=r24.r18;r16=r24.r16;r14=r24.r14;b=r24.b

MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R25'
r24.MODEL=MODEL;r20.MODEL=MODEL;r18.MODEL=MODEL;r16.MODEL=MODEL;r16.r15.MODEL=MODEL
r14.MODEL=MODEL;r14.r12.MODEL=MODEL;r14.r11.MODEL=MODEL;r14.r10.MODEL=MODEL
r14.r09.MODEL=MODEL;r14.r08.MODEL=MODEL;r14.r08.r.MODEL=MODEL;b.MODEL=MODEL

ZONE=.435
ARCH_TOP_Z=.755
ARCH_POWER=.42
CROWN_Y=.018
CROWN_Z=.030
ANGLES=[math.radians(v) for v in range(0,181,5)]

def arch_shape(x,wx):
    u=abs((x-wx)/ZONE)
    if u>=1.0:return 0.0
    return max(0.0,1.0-u*u)**ARCH_POWER

def union_xs(rows):
    xs={round(p[0],9) for p in rows[0]}
    for wx in (b.FX,b.RX):
        xs.add(round(wx-ZONE,9));xs.add(round(wx+ZONE,9))
        for a in ANGLES:xs.add(round(wx+ZONE*math.cos(a),9))
    return sorted(xs,reverse=True)

def interp_rows(rows,x):
    return [r14.interp_row(row,x) for row in rows]

def build_source_raw(rows,M,glass):
    xs=union_xs(rows);cols=[interp_rows(rows,x) for x in xs]
    mb=r14.MB()
    def K(i,row,side):return f'X{i}:R{row}:S{side:+d}'
    def local_s(x):return max(arch_shape(x,b.FX),arch_shape(x,b.RX))
    def V(i,row,side):
        p=cols[i][row];s=local_s(p[0])
        if row==4:p=(p[0],p[1]+CROWN_Y*s,p[2]+CROWN_Z*s)
        if row==3:p=(p[0],p[1]+.004*s,p[2]+.008*s)
        if row==0:return mb.v(K(i,row,0),(p[0],0,p[2]))
        return mb.v(K(i,row,side),(p[0],side*p[1],p[2]))

    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        for side in (1,-1):
            for arow,brow in ((0,1),(1,2),(2,3),(3,4)):
                a0=V(i,arow,side if arow else 0);a1=V(i+1,arow,side if arow else 0);b1=V(i+1,brow,side);b0=V(i,brow,side)
                ids=(a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1);glass_band=(arow,brow) in ((1,2),(2,3)) and -1.22<=cx<=.72
                mb.f(ids,1 if glass_band else 0)

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
                x=xs[gi];s=arch_shape(x,wx);base=cols[gi];crown.append(V(gi,4,side))
                if jj==0 or jj==len(zone_indices)-1:
                    b1s.append(V(gi,5,side));b2s.append(V(gi,6,side));inner.append(V(gi,7,side));endpoint_reuse+=3;continue
                shoulder=base[4];mid=base[5];rock=base[6];under=base[7]
                inner_z=under[2]+s*(ARCH_TOP_Z-under[2]);inner_y=under[1]+s*((shoulder[1]-.024)-under[1])
                b2_z=rock[2]+s*((inner_z+.035)-rock[2]);b2_y=rock[1]+s*((shoulder[1]-.014)-rock[1])
                b1_z=mid[2]+s*((inner_z+.072)-mid[2]);b1_y=mid[1]+s*((shoulder[1]-.006)-mid[1])
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

    for i in range(len(mb.faces)-28,len(mb.faces)):mb.faces[i]=tuple(reversed(mb.faces[i]))
    me=bpy.data.meshes.new('PRIMARY_ROUNDED_ARCH_SOURCE_MESH');me.from_pydata(mb.verts,[],mb.faces);me.update();o=bpy.data.objects.new('PRIMARY_ROUNDED_ARCH_SOURCE',me);bpy.context.collection.objects.link(o)
    o.data.materials.append(M['CLAY']);o.data.materials.append(glass)
    for p,mi in zip(o.data.polygons,mb.face_mat):p.use_smooth=True;p.material_index=mi
    o['OLEANDER_AUTHORITY']='WORKING_SOURCE';o['OLEANDER_TOPOLOGY']='R25_ROUNDED_SHARED_ENDPOINT_LOCAL_ARCH_R20_WINDING'
    return o,xs,cols,arch_meta,endpoint_reuse

def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);b.clear();M=b.materials();glass=r14.diagnostic_glass();rows=b.controls_resampled();source,xs,cols,arch_meta,reuse=build_source_raw(rows,M,glass);h0=r20.shape_hash(source)
    features=r24.feature_guides(source,xs,cols,arch_meta,M);b.wheels(M);b.ground(M);L=b.rigs();b.world((.012,.012,.012),.16);wire=r14.wire_overlay(source,M);stats=r14.topology_stats(source);islands=r16.island_count(source);h1=r20.shape_hash(source)
    scene=bpy.context.scene;scene['OLEANDER_MODEL']=MODEL;scene['OLEANDER_STAGE']='M5';scene['OLEANDER_REVISION']='R25 rounded wheel-opening profile; R24 topology concept retained'
    r14.write_contract(out,source,stats,len(features));cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text())
    c['job_id']='SYS-MODELING-WORKER-AUTO-M4M5-v0.11-R25';c['decision_question']='Does replacing the R24 cosine-squared wheel-opening height law with a broader superellipse-like local profile remove the V-shaped wheel wedges and tire/body penetration while retaining the R24 single-mesh shared-endpoint topology?';c['source_authority']['editable_source']=f'{MODEL}.blend';c['source_authority']['artifact_hash']=h0
    c['primary_geometry'][0]['id']='PG-ROUNDED-LOCAL-ARCH-SOURCE';c['primary_geometry'][0]['role']='integrated primary source with rounded shared-endpoint local wheel-arch patches';c['semantic_components'][1]['id']='COMP-ROUNDED-LOCAL-ARCH-SOURCE';c['semantic_components'][1]['role']='R25 editable primary source';c['semantic_components'][1]['source_ref']='PG-ROUNDED-LOCAL-ARCH-SOURCE'
    c['locks'].append({'target':'R09/R11/R12 package + all non-wheel source geometry','state':'LOCKED','reason':'R25 reopens wheel-zone M4 only after R24 visual QA failure','unlock_trigger':None})
    c['revision']={'revision_id':'R25-ROUNDED-WHEEL-OPENING','semantic_targets':['front/rear wheel opening','fender crown local blend'],'parameters':{'zone_radius_m':ZONE,'arch_top_z_m':ARCH_TOP_Z,'arch_profile':'(1-u^2)^0.42','crown_y_m':CROWN_Y,'crown_z_m':CROWN_Z,'endpoint_reuse':'MID/ROCKER/UNDER','source_boolean':False,'source_subd':False},'expected_affected_components':['wheel-zone primary source coordinates/topology sampling only'],'affected_view_policy':'HYBRID'}
    c['qa']['construction']=['one connected source mesh','R24 shared SHOULDER and endpoint-reuse topology retained','source n-gon=0','no Source Boolean/SubD','R20 terminal winding retained'];c['qa']['project']=['R24 V-shaped front/rear wheel wedges must close','tire must not visibly pierce body envelope in arch detail','fender crown must read as shoulder-fed rather than isolated cap','M6/M7/M8 remains blocked'];c['resource_budget']['max_render_views']=9;cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    blend=out/f'{MODEL}.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend));rd=out/'renders';rd.mkdir(parents=True,exist_ok=True);records=[]
    V=[('SIDE_SILHOUETTE',(0,-8.8,1.14),(0,0,.64),85,True,5.25,'BROAD','sil'),('PACKAGE_SIDE',(0,-8.8,1.14),(0,0,.64),85,True,5.25,'BROAD','normal'),('HERO_FRONT_3Q',(6.2,-7.0,2.75),(.05,0,.66),78,False,5,'BROAD','normal'),('HERO_REAR_3Q',(-6.0,6.8,2.65),(-.10,0,.66),78,False,5,'BROAD','normal'),('CLAY_STRIP',(6.2,-7.0,2.75),(.05,0,.66),78,False,5,'STRIP','normal'),('CLAY_GRAZING',(6.2,-7.0,2.75),(.05,0,.66),78,False,5,'GRAZING','normal'),('FRONT_ARCH_DETAIL',(2.65,-3.4,.95),(b.FX,-b.WY,.48),100,False,5,'STRIP','normal'),('REAR_ARCH_DETAIL',(-2.55,-3.4,.95),(b.RX,-b.WY,.48),100,False,5,'STRIP','normal'),('SOURCE_WIREFRAME',(5.8,-6.4,2.8),(0,0,.66),80,False,5,'BROAD','wire')]
    for lab,loc,t,lens,ortho,scale,rig,mode in V:
        b.setrig(L,rig);wire.hide_render=(mode!='wire');source.hide_render=(mode=='wire')
        for o in features:o.hide_render=True
        b.world((1,1,1),.75) if mode=='sil' else b.world((.012,.012,.012),.16);bpy.context.view_layer.material_override=M['BLACK'] if mode=='sil' else None;cam=b.camera('CAM_'+lab,loc,t,lens,ortho,scale);bpy.context.scene.camera=cam;p=rd/f'{MODEL}__{lab}.png';b.setup(p,a.samples,a.resolution);bpy.ops.render.render(write_still=True);records.append({'view':lab,'file':str(p),'mode':mode});bpy.data.objects.remove(cam,do_unlink=True)
    bpy.context.view_layer.material_override=None;source.hide_render=False;mods=[m.type for m in source.modifiers]
    checks={'source_hash_stable_during_diagnostics':h0==h1,'source_island_count_one':islands==1,'source_ngon_zero':stats['ngon']==0,'termination_triangles_four':stats['tri']==4,'source_no_boolean':'BOOLEAN' not in mods,'source_no_subd':'SUBSURF' not in mods,'arch_endpoint_vertex_reuse_24':reuse==24,'four_arch_boundaries':len([o for o in features if 'FEATURE_WHEEL_ARCH_' in o.name])==4,'rounded_profile_active':ARCH_POWER<.5 and ZONE<.45,'render_matrix':len(records)==9}
    q={'schema':'oleander.auto.v0.11.r25.qa','model':MODEL,'status':'MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL','source_hash':h0,'topology':stats,'source_island_count':islands,'endpoint_reuse_count':reuse,'checks':checks,'renders':records,'boundary':'R25 reopens wheel-zone M4 only. R09/R11/R12 and non-wheel source remain locked. M5 Visual QA required; M6/M7/M8 blocked.'};(out/'AUTOMOTIVE_V011_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    rec={'schema':'oleander.auto.v0.11.r25.receipt','model':MODEL,'blender_version':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),'renderer':'Cycles CPU','samples':a.samples,'resolution':[a.resolution,a.resolution],'status':'EXECUTED_'+q['status'],'blend':str(blend),'qa':str(out/'AUTOMOTIVE_V011_QA.json'),'renders':records};(out/'AUTOMOTIVE_V011_RECEIPT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if all(checks.values()) else 5)

if __name__=='__main__':main()
