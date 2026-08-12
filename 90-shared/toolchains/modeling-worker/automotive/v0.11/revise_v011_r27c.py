#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R27C — Tangential Radial Fan.

R27B fixed radial z/y overshoot but Human M5 still shows hard vertical wheel-zone exits.
R27C retains the four-boundary circumferential Source topology and monotonic z/y bridge,
then fans the inner rings inward in x through the arch while all rings converge C1-ish to
the same body-cage endpoint. This targets fore/aft tangency without detached geometry.
"""
from __future__ import annotations
import importlib.util,bpy,json,math
from pathlib import Path
BASE='/tmp/revise_v011_r27b.py'
spec=importlib.util.spec_from_file_location('r27b',BASE);r27b=importlib.util.module_from_spec(spec);spec.loader.exec_module(r27b)
r27=r27b.r27;r25=r27b.r25;r24=r27b.r24;r20=r27b.r20;r18=r27b.r18;r16=r27b.r16;r14=r27b.r14;b=r27b.b
MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R27C'
for m in (r27b,r27,r25,r24,r20,r18,r16,r16.r15,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):m.MODEL=MODEL
ZONE=.475;Z_CENTER=.305;RZ_INNER=.450;OUTER_RZ=.510
RX_BLEND1=.450;RX_BLEND2=.430;RX_INNER=.405
OUTER_Y_GAIN=.060;INNER_Y_GAIN=.025

def lerp(a,b,t):return a+(b-a)*t

def angle_data(x,wx):
    u=max(-1.0,min(1.0,(x-wx)/ZONE));theta=math.acos(u);s=max(0.0,math.sin(theta));w=s*s
    return theta,s,w,math.cos(theta)

def union_xs(rows):
    xs={round(p[0],9) for p in rows[0]}
    for wx in (b.FX,b.RX):
        xs.add(round(wx-ZONE,9));xs.add(round(wx+ZONE,9))
        for i in range(25):
            a=math.pi*i/24;xs.add(round(wx+ZONE*math.cos(a),9))
    return sorted(xs,reverse=True)

def build_source_r27c(rows,M,glass):
    xs=union_xs(rows);cols=[[r14.interp_row(row,x) for row in rows] for x in xs];mb=r14.MB()
    def K(i,row,side):return f'X{i}:R{row}:S{side:+d}'
    def nearest_wheel(x):
        wx=min((b.FX,b.RX),key=lambda q:abs(x-q));return wx if abs(x-wx)<=ZONE+1e-8 else None
    def V(i,row,side):
        p=cols[i][row];wx=nearest_wheel(p[0])
        if row==4 and wx is not None:
            _,s,w,_=angle_data(p[0],wx);p=(p[0],p[1]+OUTER_Y_GAIN*w,lerp(p[2],Z_CENTER+OUTER_RZ*s,w))
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
            sname='L' if side>0 else 'R';outer=[];b1s=[];b2s=[];inner=[]
            for jj,gi in enumerate(zone_indices):
                x=xs[gi];base=cols[gi];outer_idx=V(gi,4,side);outer.append(outer_idx)
                if jj==0 or jj==len(zone_indices)-1:
                    b1s.append(V(gi,5,side));b2s.append(V(gi,6,side));inner.append(V(gi,7,side));endpoint_reuse+=3;continue
                _,s,w,c=angle_data(x,wx);shoulder,under=base[4],base[7];ov=mb.verts[outer_idx];outer_y=abs(ov[1]);outer_z=ov[2]
                inner_z=lerp(under[2],Z_CENTER+RZ_INNER*s,w);inner_y=lerp(under[1],shoulder[1]+INNER_Y_GAIN,w)
                b1_z=lerp(outer_z,inner_z,.34);b2_z=lerp(outer_z,inner_z,.67);b1_y=lerp(outer_y,inner_y,.34);b2_y=lerp(outer_y,inner_y,.67)
                # Tangential radial fan: all boundaries share the locked endpoint radius,
                # but interior x-radius contracts smoothly toward each nested ring target.
                rx1=lerp(ZONE,RX_BLEND1,w);rx2=lerp(ZONE,RX_BLEND2,w);rxi=lerp(ZONE,RX_INNER,w)
                x1=wx+rx1*c;x2=wx+rx2*c;xi=wx+rxi*c
                b1s.append(mb.v(f'R27C:{wname}:{sname}:BLEND1:{jj}',(x1,side*b1_y,b1_z)))
                b2s.append(mb.v(f'R27C:{wname}:{sname}:BLEND2:{jj}',(x2,side*b2_y,b2_z)))
                inner.append(mb.v(f'R27C:{wname}:{sname}:INNER:{jj}',(xi,side*inner_y,inner_z)))
            for j in range(len(zone_indices)-1):
                for A,B in ((outer,b1s),(b1s,b2s),(b2s,inner)):
                    ids=(A[j],A[j+1],B[j+1],B[j]);mb.f(ids if side>0 else tuple(reversed(ids)),0)
            arch_meta.append((wname,sname,outer,inner))

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
    for i in range(len(mb.faces)-28,len(mb.faces)):mb.faces[i]=tuple(reversed(mb.faces[i]))
    me=bpy.data.meshes.new('PRIMARY_CIRCUMFERENTIAL_ARCH_R27C_MESH');me.from_pydata(mb.verts,[],mb.faces);me.update();o=bpy.data.objects.new('PRIMARY_CIRCUMFERENTIAL_ARCH_R27C',me);bpy.context.collection.objects.link(o);o.data.materials.append(M['CLAY']);o.data.materials.append(glass)
    for p,mi in zip(o.data.polygons,mb.face_mat):p.use_smooth=True;p.material_index=mi
    o['OLEANDER_AUTHORITY']='WORKING_SOURCE';o['OLEANDER_TOPOLOGY']='R27C_TANGENTIAL_RADIAL_FAN';o['R27_ARCH_SEGMENTS']=24;o['R27_RING_COUNT']=4;o['R27_ENDPOINT_REUSE']=endpoint_reuse
    return o,xs,cols,arch_meta,endpoint_reuse

r25.build_source_raw=build_source_r27c

def patch_outputs(out:Path):
    cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text());c['job_id']='SYS-MODELING-WORKER-AUTO-M4M5-v0.11-R27C';c['decision_question']='Does a C1-ish x-radius fan across the R27 circumferential boundaries remove hard vertical wheel-zone exits while retaining monotonic radial ordering and shoulder continuity?';c['source_authority']['editable_source']=f'{MODEL}.blend';c['revision']={'revision_id':'R27C-TANGENTIAL-RADIAL-FAN','semantic_targets':['front/rear arch fore-aft tangency','wheel-zone exit continuity'],'parameters':{'outer_zone_radius_m':ZONE,'blend1_crown_rx_m':RX_BLEND1,'blend2_crown_rx_m':RX_BLEND2,'inner_crown_rx_m':RX_INNER,'endpoint_convergence':'shared outer zone radius','fan_envelope':'sin(theta)^2'},'expected_affected_components':['R27 wheel-zone x coordinates only'],'affected_view_policy':'HYBRID'};c['qa']['construction']=['R27 circumferential topology retained','R27B monotonic z/y bridge retained','nested x-radius fan','shared zone-exit endpoints','one connected Source mesh','source n-gon=0','no Source Boolean/SubD'];c['qa']['project']=['hard vertical wheel-zone exits materially reduced','front/rear arch opening wraps tire coherently in 3/4','fender crown remains shoulder-fed','M6/M7/M8 remains blocked'];cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    qp=out/'AUTOMOTIVE_V011_QA.json';q=json.loads(qp.read_text());q['schema']='oleander.auto.v0.11.r27c.qa';q['model']=MODEL;q['checks']['circumferential_arch_active']=True;q['checks']['arch_segments_24']=True;q['checks']['four_nested_arch_boundaries']=True;q['checks']['monotonic_radial_bridge_active']=True;q['checks']['tangential_radial_fan_active']=True;q['boundary']='R27C retains R27 topology and R27B radial ordering, revising fore/aft ring x-radius only. Human M5 Visual QA required; M6/M7/M8 blocked.';qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    rp=out/'AUTOMOTIVE_V011_RECEIPT.json';r=json.loads(rp.read_text());r['schema']='oleander.auto.v0.11.r27c.receipt';r['model']=MODEL;rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    (out/'R27_TOPOLOGY_CONTRACT.json').write_text(json.dumps({'model':MODEL,'stage':'M5','revision':'R27C','status':'MACHINE_EXECUTED_VISUAL_REVIEW_REQUIRED','arch_segments':24,'ring_count':4,'topology':'CIRCUMFERENTIAL_NESTED_RING_FAN','radial_order':'MONOTONIC_OUTER_TO_INNER','fore_aft_transition':'C1_ISH_SHARED_ENDPOINT_FAN','blocked':['M6','M7','M8']},ensure_ascii=False,indent=2)+'\n')

def main():
    try:r25.main()
    except SystemExit as e:
        a=b.parse();patch_outputs(Path(a.out).resolve());raise SystemExit(e.code)
if __name__=='__main__':main()
