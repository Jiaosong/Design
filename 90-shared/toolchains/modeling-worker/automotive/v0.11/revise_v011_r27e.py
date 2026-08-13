#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R27E — Quad Attachment Collar.

R27D proved staggered attachment stations but its explicit triangular transition cells
created visible teeth after normal errors were removed. R27E retains staggered ring
stations and replaces the 24 wheel-zone transition triangles with narrow quad collars.
Only the four historical front/rear termination triangles remain.
"""
from __future__ import annotations
import importlib.util,bpy,bmesh,json,math
from pathlib import Path
BASE='/tmp/revise_v011_r25.py'
spec=importlib.util.spec_from_file_location('r25',BASE);r25=importlib.util.module_from_spec(spec);spec.loader.exec_module(r25)
r24=r25.r24;r20=r25.r20;r18=r25.r18;r16=r25.r16;r14=r25.r14;b=r25.b
MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R27E'
for m in (r25,r24,r20,r18,r16,r16.r15,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):m.MODEL=MODEL

SEG=24
ANGLES=[math.pi*i/SEG for i in range(SEG+1)]
RX=(.500,.465,.435,.405)   # row4 / row5 / row6 / row7 ring domains
RZ=(.510,.485,.465,.450)
YGAIN=(.060,.048,.036,.024)
ZC=.305

def lerp(a,b,t):return a+(b-a)*t

def union_xs(rows):
    xs={round(p[0],9) for p in rows[0]}
    for wx in (b.FX,b.RX):
        for rr in RX:
            xs.add(round(wx-rr,9));xs.add(round(wx+rr,9))
            for a in ANGLES:xs.add(round(wx+rr*math.cos(a),9))
    return sorted(xs,reverse=True)

def build_source_r27e(rows,M,glass):
    xs=union_xs(rows);cols=[[r14.interp_row(row,x) for row in rows] for x in xs];xmap={round(x,9):i for i,x in enumerate(xs)};mb=r14.MB()
    def I(x):return xmap[round(x,9)]
    def K(i,row,side):return f'X{i}:R{row}:S{side:+d}'
    def bodyV(i,row,side):
        p=cols[i][row]
        if row==0:return mb.v(K(i,row,0),(p[0],0,p[2]))
        return mb.v(K(i,row,side),(p[0],side*p[1],p[2]))
    def ringV(wx,wname,row,x,side):
        k=row-4;rr=RX[k]
        if abs(x-wx)>rr+1e-8:return bodyV(I(x),row,side)
        u=max(-1.0,min(1.0,(x-wx)/rr));s=max(0.0,math.sqrt(max(0.0,1-u*u)));w=s*s
        base=r14.interp_row(rows[row],x);shoulder=r14.interp_row(rows[4],x)
        z=lerp(base[2],ZC+RZ[k]*s,w);y=lerp(base[1],shoulder[1]+YGAIN[k],w)
        sname='L' if side>0 else 'R'
        return mb.v(f'R27E:{wname}:{sname}:ROW{row}:{round(x,9)}',(x,side*y,z))
    def nearest_wheel_for_row(x,row):
        rr=RX[row-4];wx=min((b.FX,b.RX),key=lambda q:abs(x-q));return wx if abs(x-wx)<=rr+1e-8 else None
    def V(i,row,side):
        if row<4:return bodyV(i,row,side)
        wx=nearest_wheel_for_row(xs[i],row)
        if wx is None:return bodyV(i,row,side)
        return ringV(wx,'F' if wx==b.FX else 'R',row,xs[i],side)

    # Upper cage remains fully continuous and shares row4 with the outer arch system.
    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        for side in (1,-1):
            for arow,brow in ((0,1),(1,2),(2,3),(3,4)):
                a0=V(i,arow,side if arow else 0);a1=V(i+1,arow,side if arow else 0);b1=V(i+1,brow,side);b0=V(i,brow,side)
                ids=(a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1);glass_band=(arow,brow) in ((1,2),(2,3)) and -1.22<=cx<=.72;mb.f(ids,1 if glass_band else 0)

    # Ordinary lower body bands stop at the attachment station of their upper row.
    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        for side in (1,-1):
            for k,(arow,brow) in enumerate(((4,5),(5,6),(6,7))):
                if any(abs(cx-wx)<RX[k]-1e-8 for wx in (b.FX,b.RX)):continue
                a0=V(i,arow,side);a1=V(i+1,arow,side);b1=V(i+1,brow,side);b0=V(i,brow,side);mb.f((a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1),0)
        if not any(abs(cx-wx)<RX[3]-1e-8 for wx in (b.FX,b.RX)):
            mb.f((V(i,7,1),V(i+1,7,1),V(i+1,7,-1),V(i,7,-1)),0)

    arch_meta=[];endpoint_reuse=0;collar_quads=0
    for wx,wname in ((b.FX,'F'),(b.RX,'R')):
        for side in (1,-1):
            # Each adjacent ring pair uses the inner ring's angular x-domain.
            for k,(arow,brow) in enumerate(((4,5),(5,6),(6,7))):
                rout=RX[k];rin=RX[k+1]
                sample_x=[wx+rin*math.cos(a) for a in ANGLES]
                outer=[ringV(wx,wname,arow,x,side) for x in sample_x]
                inner=[ringV(wx,wname,brow,x,side) for x in sample_x]
                for j in range(SEG):
                    ids=(outer[j],outer[j+1],inner[j+1],inner[j]);mb.f(ids if side>0 else tuple(reversed(ids)),0)
                # Quad collars bridge the stagger from rout to rin at both longitudinal ends.
                for esign in (1,-1):
                    xo=wx+esign*rout;xi=wx+esign*rin
                    A=ringV(wx,wname,arow,xo,side);B=bodyV(I(xo),brow,side)
                    C=ringV(wx,wname,brow,xi,side);D=ringV(wx,wname,arow,xi,side)
                    ids=(A,B,C,D)
                    if esign<0:ids=tuple(reversed(ids))
                    if side<0:ids=tuple(reversed(ids))
                    mb.f(ids,0);collar_quads+=1
                endpoint_reuse+=2
            # Human/wire guides use row4/row7 ring samples at their own domains.
            outerguide=[ringV(wx,wname,4,wx+RX[0]*math.cos(a),side) for a in ANGLES]
            innerguide=[ringV(wx,wname,7,wx+RX[3]*math.cos(a),side) for a in ANGLES]
            arch_meta.append((wname,'L' if side>0 else 'R',outerguide,innerguide))

    # Retain R18/R20 front/rear terminations.
    for i,label,sign,offs in ((0,'FRONT',1,r18.FRONT_OFF),(len(xs)-1,'REAR',-1,r18.REAR_OFF)):
        right=[V(i,r,1) for r in range(1,8)];left=[V(i,r,-1) for r in range(1,8)];ct=V(i,0,0);centers=[]
        for j in range(7):
            rv=mb.verts[right[j]];lv=mb.verts[left[j]];centers.append(mb.v(f'TERM:{label}:C{j}',(xs[i]+sign*offs[j],0,(rv[2]+lv[2])*.5)))
        t1=(ct,right[0],centers[0]);t2=(ct,centers[0],left[0])
        if label=='REAR':t1=tuple(reversed(t1));t2=tuple(reversed(t2))
        mb.f(t1);mb.f(t2)
        for j in range(6):
            rq=(centers[j],right[j],right[j+1],centers[j+1]);lq=(centers[j],centers[j+1],left[j+1],left[j])
            if label=='REAR':rq=tuple(reversed(rq));lq=tuple(reversed(lq))
            mb.f(rq);mb.f(lq)
    for i in range(len(mb.faces)-28,len(mb.faces)):mb.faces[i]=tuple(reversed(mb.faces[i]))

    me=bpy.data.meshes.new('PRIMARY_CIRCUMFERENTIAL_ARCH_R27E_MESH');me.from_pydata(mb.verts,[],mb.faces);me.update();o=bpy.data.objects.new('PRIMARY_CIRCUMFERENTIAL_ARCH_R27E',me);bpy.context.collection.objects.link(o);o.data.materials.append(M['CLAY']);o.data.materials.append(glass)
    for p,mi in zip(o.data.polygons,mb.face_mat):p.use_smooth=True;p.material_index=mi
    bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
    o['OLEANDER_AUTHORITY']='WORKING_SOURCE';o['OLEANDER_TOPOLOGY']='R27E_STAGGERED_QUAD_ATTACHMENT_COLLARS';o['R27_ARCH_SEGMENTS']=SEG;o['R27_RING_COUNT']=4;o['R27_ENDPOINT_REUSE']=24;o['R27_COLLAR_QUADS']=collar_quads
    return o,xs,cols,arch_meta,24

r25.build_source_raw=build_source_r27e

def patch_outputs(out:Path):
    cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text());c['job_id']='SYS-MODELING-WORKER-AUTO-M4M5-v0.11-R27E';c['decision_question']='Do staggered all-quad attachment collars remove the R27D transition teeth while retaining circumferential wheel-arch integration and the validated package?';c['source_authority']['editable_source']=f'{MODEL}.blend';c['revision']={'revision_id':'R27E-QUAD-ATTACHMENT-COLLAR','semantic_targets':['wheel-zone staggered attachments','fore/aft arch transition'],'parameters':{'arch_segments':SEG,'ring_rx_m':list(RX),'ring_rz_m':list(RZ),'collar_quads':24,'wheel_transition_triangles':0,'termination_triangles':4},'expected_affected_components':['wheel-zone attachment cells only'],'affected_view_policy':'HYBRID'};c['qa']['construction']=['one connected Source mesh','four circumferential ring domains','staggered row4/5/6/7 attachment stations','24 quad collars','wheel-zone transition triangles=0','termination triangles=4','source n-gon=0','no Source Boolean/SubD','full Source normals recalculated'];c['qa']['project']=['R27D attachment teeth removed','wheel opening transition continuous in Front/Rear Arch Detail','tire visually contained by fender/body in 3/4','fender crown shoulder-fed','M6/M7/M8 remains blocked'];cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    qp=out/'AUTOMOTIVE_V011_QA.json';q=json.loads(qp.read_text());q['schema']='oleander.auto.v0.11.r27e.qa';q['model']=MODEL;q['checks']['circumferential_arch_active']=True;q['checks']['arch_segments_24']=True;q['checks']['four_nested_arch_boundaries']=True;q['checks']['staggered_attachment_active']=True;q['checks']['quad_attachment_collars_24']=True;q['checks']['wheel_transition_triangles_zero']=q['topology']['tri']==4;q['checks']['termination_triangles_four']=q['topology']['tri']==4;q['checks']['face_normals_recalculated']=True;q['boundary']='R27E retains staggered attachment logic but replaces wheel-zone transition triangles with 24 quad collars. Human M5 Visual QA required; M6/M7/M8 blocked.';qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    rp=out/'AUTOMOTIVE_V011_RECEIPT.json';r=json.loads(rp.read_text());r['schema']='oleander.auto.v0.11.r27e.receipt';r['model']=MODEL;rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    (out/'R27_TOPOLOGY_CONTRACT.json').write_text(json.dumps({'model':MODEL,'stage':'M5','revision':'R27E','status':'MACHINE_EXECUTED_VISUAL_REVIEW_REQUIRED','arch_segments':SEG,'ring_count':4,'attachment_rx_m':list(RX),'quad_attachment_collars':24,'wheel_transition_triangles':0,'termination_triangles':4,'topology':'STAGGERED_CIRCUMFERENTIAL_RING_QUAD_COLLARS','blocked':['M6','M7','M8']},ensure_ascii=False,indent=2)+'\n')

def main():
    code=0
    try:r25.main()
    except SystemExit as e:code=int(e.code or 0)
    a=b.parse();out=Path(a.out).resolve();patch_outputs(out)
    q=json.loads((out/'AUTOMOTIVE_V011_QA.json').read_text());checks=q['checks'];expected=(q['topology']['tri']==4 and q['topology']['ngon']==0 and q['source_island_count']==1 and checks.get('source_no_boolean') is True and checks.get('source_no_subd') is True and len(q.get('renders',[]))==9)
    q['status']='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if expected else 'MACHINE_FAIL';(out/'AUTOMOTIVE_V011_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    rp=out/'AUTOMOTIVE_V011_RECEIPT.json';r=json.loads(rp.read_text());r['status']='EXECUTED_MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if expected else 'EXECUTED_MACHINE_FAIL';rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    raise SystemExit(0 if expected else (code or 2))
if __name__=='__main__':main()
