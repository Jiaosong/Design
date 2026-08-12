#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R27B — Monotonic Radial Bridge.

R27A established angle-parameterized circumferential topology and passed Machine M5,
but Human M5 showed a new failure: intermediate rings overshot the shared shoulder
transition and read as a floating wheel-brow / bridge. R27B retains R27 topology and
reorders ring coordinates monotonically from body shoulder transition to inner opening.
"""
from __future__ import annotations
import importlib.util,bpy,json
from pathlib import Path

BASE='/tmp/revise_v011_r27.py'
spec=importlib.util.spec_from_file_location('r27',BASE)
r27=importlib.util.module_from_spec(spec);spec.loader.exec_module(r27)
r25=r27.r25;r24=r27.r24;r20=r27.r20;r18=r27.r18;r16=r27.r16;r14=r27.r14;b=r27.b
MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R27B'
for m in (r27,r25,r24,r20,r18,r16,r16.r15,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):m.MODEL=MODEL

ZONE=r27.ZONE;ARCH_SEGMENTS=r27.ARCH_SEGMENTS;Z_CENTER=.305;RZ_INNER=.450
OUTER_RZ=.505;OUTER_Y_GAIN=.060;INNER_Y_GAIN=.025

def lerp(a,b,t):return a+(b-a)*t

def build_source_r27b(rows,M,glass):
    xs=r27.union_xs(rows);cols=[r27.interp_rows(rows,x) for x in xs];mb=r14.MB()
    def K(i,row,side):return f'X{i}:R{row}:S{side:+d}'
    def nearest_wheel(x):
        wx=min((b.FX,b.RX),key=lambda q:abs(x-q))
        return wx if abs(x-wx)<=ZONE+1e-8 else None
    def V(i,row,side):
        p=cols[i][row];wx=nearest_wheel(p[0])
        if row==4 and wx is not None:
            _,s,w=r27.arch_angle(p[0],wx)
            # The shared shoulder transition is the outermost ring and must stay
            # outside / above every nested ring. Blend to locked row4 at zone exits.
            outer_z_target=Z_CENTER+OUTER_RZ*s
            p=(p[0],p[1]+OUTER_Y_GAIN*w,lerp(p[2],outer_z_target,w))
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

    arch_meta=[];endpoint_reuse=0;ring_vertex_count=0
    for wx,wname in ((b.FX,'F'),(b.RX,'R')):
        zone_indices=sorted([i for i,x in enumerate(xs) if abs(x-wx)<=ZONE+1e-8])
        for side in (1,-1):
            sname='L' if side>0 else 'R';outer=[];blend1=[];blend2=[];inner=[]
            for jj,gi in enumerate(zone_indices):
                x=xs[gi];base=cols[gi];outer_idx=V(gi,4,side);outer.append(outer_idx)
                if jj==0 or jj==len(zone_indices)-1:
                    blend1.append(V(gi,5,side));blend2.append(V(gi,6,side));inner.append(V(gi,7,side));endpoint_reuse+=3;continue
                _,s,w=r27.arch_angle(x,wx);shoulder,under=base[4],base[7]
                ov=mb.verts[outer_idx];outer_y=abs(ov[1]);outer_z=ov[2]
                inner_z=lerp(under[2],Z_CENTER+RZ_INNER*s,w)
                inner_y=lerp(under[1],shoulder[1]+INNER_Y_GAIN,w)
                # Radial bridge is strictly bounded by outer and inner coordinates:
                # no intermediate ring may rise above / outside the shared shoulder ring.
                b1_z=lerp(outer_z,inner_z,.34);b2_z=lerp(outer_z,inner_z,.67)
                b1_y=lerp(outer_y,inner_y,.34);b2_y=lerp(outer_y,inner_y,.67)
                blend1.append(mb.v(f'R27B:{wname}:{sname}:BLEND1:{jj}',(x,side*b1_y,b1_z)))
                blend2.append(mb.v(f'R27B:{wname}:{sname}:BLEND2:{jj}',(x,side*b2_y,b2_z)))
                inner.append(mb.v(f'R27B:{wname}:{sname}:INNER:{jj}',(x,side*inner_y,inner_z)));ring_vertex_count+=3
            for j in range(len(zone_indices)-1):
                for A,B in ((outer,blend1),(blend1,blend2),(blend2,inner)):
                    ids=(A[j],A[j+1],B[j+1],B[j]);mb.f(ids if side>0 else tuple(reversed(ids)),0)
            arch_meta.append((wname,sname,outer,inner))

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

    me=bpy.data.meshes.new('PRIMARY_CIRCUMFERENTIAL_ARCH_R27B_MESH');me.from_pydata(mb.verts,[],mb.faces);me.update();o=bpy.data.objects.new('PRIMARY_CIRCUMFERENTIAL_ARCH_R27B',me);bpy.context.collection.objects.link(o)
    o.data.materials.append(M['CLAY']);o.data.materials.append(glass)
    for p,mi in zip(o.data.polygons,mb.face_mat):p.use_smooth=True;p.material_index=mi
    o['OLEANDER_AUTHORITY']='WORKING_SOURCE';o['OLEANDER_TOPOLOGY']='R27B_MONOTONIC_CIRCUMFERENTIAL_RADIAL_BRIDGE';o['R27_ARCH_SEGMENTS']=ARCH_SEGMENTS;o['R27_RING_COUNT']=4;o['R27_ENDPOINT_REUSE']=endpoint_reuse;o['R27_RING_VERTEX_COUNT']=ring_vertex_count
    return o,xs,cols,arch_meta,endpoint_reuse

r25.build_source_raw=build_source_r27b

def patch_outputs(out:Path):
    cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text());c['job_id']='SYS-MODELING-WORKER-AUTO-M4M5-v0.11-R27B';c['decision_question']='Does monotonic radial ordering of the R27 circumferential rings remove the floating wheel-brow/bridge while preserving tire containment and shoulder continuity?';c['source_authority']['editable_source']=f'{MODEL}.blend';c['revision']={'revision_id':'R27B-MONOTONIC-RADIAL-BRIDGE','semantic_targets':['circumferential arch radial ordering','shoulder-to-inner opening bridge'],'parameters':{'arch_segments':ARCH_SEGMENTS,'ring_count':4,'outer_rz_m':OUTER_RZ,'inner_rz_m':RZ_INNER,'outer_y_gain_m':OUTER_Y_GAIN,'inner_y_gain_m':INNER_Y_GAIN,'monotonic_bridge':True},'expected_affected_components':['wheel-zone R27 ring coordinates only'],'affected_view_policy':'HYBRID'};c['qa']['construction']=['R27 circumferential topology retained','outer-to-inner z/y ordering monotonic','one connected Source mesh','source n-gon=0','no Source Boolean/SubD','zone-exit vertex reuse retained'];c['qa']['project']=['floating wheel-brow/bridge from R27A must disappear','tire visually contained by body volume','fender crown grows from shoulder','front/rear arch continuity acceptable','M6/M7/M8 remains blocked'];cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    qp=out/'AUTOMOTIVE_V011_QA.json';q=json.loads(qp.read_text());q['schema']='oleander.auto.v0.11.r27b.qa';q['model']=MODEL;q['checks']['circumferential_arch_active']=True;q['checks']['arch_segments_24']=ARCH_SEGMENTS==24;q['checks']['four_nested_arch_boundaries']=True;q['checks']['monotonic_radial_bridge_active']=True;q['boundary']='R27B retains R27 topology and corrects ring ordering only. Human M5 Visual QA required; M6/M7/M8 blocked.';qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    rp=out/'AUTOMOTIVE_V011_RECEIPT.json';r=json.loads(rp.read_text());r['schema']='oleander.auto.v0.11.r27b.receipt';r['model']=MODEL;rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    (out/'R27_TOPOLOGY_CONTRACT.json').write_text(json.dumps({'model':MODEL,'stage':'M5','revision':'R27B','status':'MACHINE_EXECUTED_VISUAL_REVIEW_REQUIRED','arch_segments':ARCH_SEGMENTS,'ring_count':4,'topology':'SHARED_SHOULDER_TRANSITION -> BLEND1 -> BLEND2 -> INNER_OPENING','radial_order':'MONOTONIC_OUTER_TO_INNER','blocked':['M6','M7','M8']},ensure_ascii=False,indent=2)+'\n')

def main():
    try:r25.main()
    except SystemExit as e:
        a=b.parse();patch_outputs(Path(a.out).resolve());raise SystemExit(e.code)
if __name__=='__main__':main()
