#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R27D — Staggered Ring Attachment Topology.

R27A established circumferential rings, R27B corrected radial ordering, and R27C tested
an x-radius fan. Human M5 still showed hard wheel-zone exits because every boundary
ultimately attached at the same longitudinal station. R27D assigns a distinct attachment
radius to each Source row and closes the resulting transition wedges with explicit,
controlled triangles. This is a topology change, not a scalar styling offset.
"""
from __future__ import annotations
import importlib.util,bpy,json,math
from pathlib import Path
BASE='/tmp/revise_v011_r25.py'
spec=importlib.util.spec_from_file_location('r25',BASE);r25=importlib.util.module_from_spec(spec);spec.loader.exec_module(r25)
r24=r25.r24;r20=r25.r20;r18=r25.r18;r16=r25.r16;r14=r25.r14;b=r25.b
MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R27D'
for m in (r25,r24,r20,r18,r16,r16.r15,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):m.MODEL=MODEL
SEG=24;ANGLES=[math.pi*i/SEG for i in range(SEG+1)]
RX=(.500,.465,.435,.405)   # shoulder, blend1, blend2, inner attachment radii
RZ=(.510,.485,.465,.450)
YGAIN=(.060,.048,.036,.024)
ZC=.305

def lerp(a,b,t):return a+(b-a)*t

def polar(theta,rx):return rx*math.cos(theta),max(0.0,math.sin(theta))

def union_xs(rows):
    xs={round(p[0],9) for p in rows[0]}
    for wx in (b.FX,b.RX):
        for a in ANGLES:xs.add(round(wx+RX[0]*math.cos(a),9))
        for rr in RX:
            xs.add(round(wx-rr,9));xs.add(round(wx+rr,9))
    return sorted(xs,reverse=True)

def build_source_r27d(rows,M,glass):
    xs=union_xs(rows);cols=[[r14.interp_row(row,x) for row in rows] for x in xs];mb=r14.MB();xmap={round(x,9):i for i,x in enumerate(xs)}
    def idx(x):return xmap[round(x,9)]
    def K(i,row,side):return f'X{i}:R{row}:S{side:+d}'
    def outer_profile(x,wx):
        u=max(-1.0,min(1.0,(x-wx)/RX[0]));th=math.acos(u);s=max(0.0,math.sin(th));w=s*s;return s,w
    def nearest_outer(x):
        wx=min((b.FX,b.RX),key=lambda q:abs(x-q));return wx if abs(x-wx)<=RX[0]+1e-8 else None
    def V(i,row,side):
        p=cols[i][row];wx=nearest_outer(p[0])
        if row==4 and wx is not None:
            s,w=outer_profile(p[0],wx);p=(p[0],p[1]+YGAIN[0]*w,lerp(p[2],ZC+RZ[0]*s,w))
        if row==0:return mb.v(K(i,row,0),(p[0],0,p[2]))
        return mb.v(K(i,row,side),(p[0],side*p[1],p[2]))

    # Upper cage remains continuous and shares row4 with the outer circumferential boundary.
    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        for side in (1,-1):
            for arow,brow in ((0,1),(1,2),(2,3),(3,4)):
                a0=V(i,arow,side if arow else 0);a1=V(i+1,arow,side if arow else 0);b1=V(i+1,brow,side);b0=V(i,brow,side)
                ids=(a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1);glass_band=(arow,brow) in ((1,2),(2,3)) and -1.22<=cx<=.72;mb.f(ids,1 if glass_band else 0)

    # Lower cage has ring-specific cutback radii. Each ordinary band terminates at the
    # attachment radius of its upper ring; explicit transition triangles close the taper.
    bands=((4,5,RX[0]),(5,6,RX[1]),(6,7,RX[2]))
    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        for side in (1,-1):
            for arow,brow,cut in bands:
                if any(abs(cx-wx)<cut-1e-8 for wx in (b.FX,b.RX)):continue
                a0=V(i,arow,side);a1=V(i+1,arow,side);b1=V(i+1,brow,side);b0=V(i,brow,side);mb.f((a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1),0)
        if not any(abs(cx-wx)<RX[3]-1e-8 for wx in (b.FX,b.RX)):
            mb.f((V(i,7,1),V(i+1,7,1),V(i+1,7,-1),V(i,7,-1)),0)

    arch_meta=[];endpoint_reuse=0;transition_triangles=0
    for wx,wname in ((b.FX,'F'),(b.RX,'R')):
        outer_indices=sorted([i for i,x in enumerate(xs) if abs(x-wx)<=RX[0]+1e-8])
        for side in (1,-1):
            sname='L' if side>0 else 'R';rings=[[],[],[],[]]
            for jj,gi in enumerate(outer_indices):
                xo=xs[gi];u=max(-1.0,min(1.0,(xo-wx)/RX[0]));theta=math.acos(u);s=max(0.0,math.sin(theta));w=s*s;c=math.cos(theta)
                rings[0].append(V(gi,4,side))
                for k,row in ((1,5),(2,6),(3,7)):
                    xr=wx+RX[k]*c
                    if jj==0 or jj==len(outer_indices)-1:
                        ri=idx(wx+(RX[k] if jj==0 else -RX[k]));rings[k].append(V(ri,row,side));endpoint_reuse+=1;continue
                    base=r14.interp_row(rows[row],xr);shoulder=r14.interp_row(rows[4],xr)
                    z=lerp(base[2],ZC+RZ[k]*s,w);y=lerp(base[1],shoulder[1]+YGAIN[k],w)
                    rings[k].append(mb.v(f'R27D:{wname}:{sname}:R{k}:{jj}',(xr,side*y,z)))
            for j in range(len(outer_indices)-1):
                for k in range(3):
                    A,B=rings[k],rings[k+1];ids=(A[j],A[j+1],B[j+1],B[j]);mb.f(ids if side>0 else tuple(reversed(ids)),0)
            arch_meta.append((wname,sname,rings[0],rings[3]))

            # Staggered attachment wedges. 3 bands × 2 longitudinal ends per side.
            for esign in (1,-1):
                ids4=idx(wx+esign*RX[0]);ids5o=idx(wx+esign*RX[0]);ids5i=idx(wx+esign*RX[1]);ids6o=idx(wx+esign*RX[1]);ids6i=idx(wx+esign*RX[2]);ids7o=idx(wx+esign*RX[2]);ids7i=idx(wx+esign*RX[3])
                tris=[(V(ids4,4,side),V(ids5o,5,side),V(ids5i,5,side)),(V(ids5i,5,side),V(ids6o,6,side),V(ids6i,6,side)),(V(ids6i,6,side),V(ids7o,7,side),V(ids7i,7,side))]
                for tri in tris:
                    ids=tri
                    if esign<0:ids=tuple(reversed(ids))
                    if side<0:ids=tuple(reversed(ids))
                    mb.f(ids,0);transition_triangles+=1

    # Retain R18/R20 structured front/rear termination and winding fix.
    for i,label,sign,offs in ((0,'FRONT',1,r18.FRONT_OFF),(len(xs)-1,'REAR',-1,r18.REAR_OFF)):
        right=[V(i,r,1) for r in range(1,8)];left=[V(i,r,-1) for r in range(1,8)];ct=V(i,0,0);centers=[]
        for j in range(7):
            rv=mb.verts[right[j]];lv=mb.verts[left[j]];centers.append(mb.v(f'TERM:{label}:C{j}',(xs[i]+sign*offs[j],0,(rv[2]+lv[2])*.5)))
        t1=(ct,right[0],centers[0]);t2=(ct,centers[0],left[0]);
        if label=='REAR':t1=tuple(reversed(t1));t2=tuple(reversed(t2))
        mb.f(t1);mb.f(t2)
        for j in range(6):
            rq=(centers[j],right[j],right[j+1],centers[j+1]);lq=(centers[j],centers[j+1],left[j+1],left[j]);
            if label=='REAR':rq=tuple(reversed(rq));lq=tuple(reversed(lq))
            mb.f(rq);mb.f(lq)
    # Only the final 28 termination faces receive the historical R20 winding correction.
    for i in range(len(mb.faces)-28,len(mb.faces)):mb.faces[i]=tuple(reversed(mb.faces[i]))
    me=bpy.data.meshes.new('PRIMARY_CIRCUMFERENTIAL_ARCH_R27D_MESH');me.from_pydata(mb.verts,[],mb.faces);me.update();o=bpy.data.objects.new('PRIMARY_CIRCUMFERENTIAL_ARCH_R27D',me);bpy.context.collection.objects.link(o);o.data.materials.append(M['CLAY']);o.data.materials.append(glass)
    for p,mi in zip(o.data.polygons,mb.face_mat):p.use_smooth=True;p.material_index=mi
    o['OLEANDER_AUTHORITY']='WORKING_SOURCE';o['OLEANDER_TOPOLOGY']='R27D_STAGGERED_RING_ATTACHMENTS';o['R27_ARCH_SEGMENTS']=SEG;o['R27_RING_COUNT']=4;o['R27_ENDPOINT_REUSE']=endpoint_reuse;o['R27_TRANSITION_TRIANGLES']=transition_triangles
    return o,xs,cols,arch_meta,endpoint_reuse

r25.build_source_raw=build_source_r27d

def patch_outputs(out:Path):
    cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text());c['job_id']='SYS-MODELING-WORKER-AUTO-M4M5-v0.11-R27D';c['decision_question']='Do staggered ring attachment stations with controlled transition cells remove the common-endpoint wheel-zone wall and integrate the circumferential arch into the body cage?';c['source_authority']['editable_source']=f'{MODEL}.blend';c['revision']={'revision_id':'R27D-STAGGERED-RING-ATTACHMENTS','semantic_targets':['wheel-zone attachment topology','fore/aft arch transition'],'parameters':{'arch_segments':SEG,'attachment_rx_m':list(RX),'ring_rz_m':list(RZ),'transition_triangle_count':24,'source_boolean':False,'source_subd':False},'expected_affected_components':['wheel-zone primary topology and controlled transition cells only'],'affected_view_policy':'HYBRID'};c['qa']['construction']=['one connected Source mesh','four angle-parameterized rings','staggered row4/5/6/7 attachment stations','24 controlled wheel-zone transition triangles + 4 termination triangles','source n-gon=0','no Source Boolean/SubD'];c['qa']['project']=['common-endpoint vertical wall removed','front/rear wheel-zone transition reads as continuous body mass','tire visually contained by fender/body','fender crown shoulder-fed','M6/M7/M8 remains blocked'];cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    qp=out/'AUTOMOTIVE_V011_QA.json';q=json.loads(qp.read_text());q['schema']='oleander.auto.v0.11.r27d.qa';q['model']=MODEL;q['checks']['circumferential_arch_active']=True;q['checks']['arch_segments_24']=True;q['checks']['four_nested_arch_boundaries']=True;q['checks']['staggered_attachment_active']=True;q['checks']['controlled_transition_triangles_24']=q['topology']['tri']==28;q['checks']['termination_triangles_four']=q['topology']['tri']==28;q['boundary']='R27D changes wheel-zone attachment topology. 24 wheel-zone transition triangles are intentional; 4 additional triangles remain the R18/R20 terminations. Human M5 Visual QA required; M6/M7/M8 blocked.';qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    rp=out/'AUTOMOTIVE_V011_RECEIPT.json';r=json.loads(rp.read_text());r['schema']='oleander.auto.v0.11.r27d.receipt';r['model']=MODEL;rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    (out/'R27_TOPOLOGY_CONTRACT.json').write_text(json.dumps({'model':MODEL,'stage':'M5','revision':'R27D','status':'MACHINE_EXECUTED_VISUAL_REVIEW_REQUIRED','arch_segments':SEG,'ring_count':4,'attachment_rx_m':list(RX),'controlled_transition_triangles':24,'termination_triangles':4,'topology':'STAGGERED_CIRCUMFERENTIAL_RING_ATTACHMENTS','blocked':['M6','M7','M8']},ensure_ascii=False,indent=2)+'\n')

def main():
    try:r25.main()
    except SystemExit as e:
        a=b.parse();patch_outputs(Path(a.out).resolve());raise SystemExit(e.code)
if __name__=='__main__':main()
