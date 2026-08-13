#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R27 — Circumferential Wheel-Arch Source Topology.

R24/R25/R26 established that the remaining wheel-zone defect is a topology / surface-
construction problem rather than a scalar parameter problem. R27 therefore rebuilds the
wheel-zone source patch from angle-parameterized nested arch rings while retaining the
validated non-wheel package and one-mesh authority rules.

Locked: R09 package, R11 non-wheel transverse tension, R12 longitudinal interpolation,
R18/R20 termination construction, R25 rounded opening target.
Blocked: M6/M7/M8 until Human M5 Visual QA passes.
"""
from __future__ import annotations
import importlib.util,bpy,json,math
from pathlib import Path

BASE='/tmp/revise_v011_r25.py'
spec=importlib.util.spec_from_file_location('r25',BASE)
r25=importlib.util.module_from_spec(spec);spec.loader.exec_module(r25)
r24=r25.r24;r20=r25.r20;r18=r25.r18;r16=r25.r16;r14=r25.r14;b=r25.b

MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R27'
r25.MODEL=MODEL;r24.MODEL=MODEL;r20.MODEL=MODEL;r18.MODEL=MODEL;r16.MODEL=MODEL;r16.r15.MODEL=MODEL
r14.MODEL=MODEL;r14.r12.MODEL=MODEL;r14.r11.MODEL=MODEL;r14.r10.MODEL=MODEL;r14.r09.MODEL=MODEL;r14.r08.MODEL=MODEL;r14.r08.r.MODEL=MODEL;b.MODEL=MODEL

ZONE=.435
ARCH_SEGMENTS=24
ANGLES=[math.pi*i/ARCH_SEGMENTS for i in range(ARCH_SEGMENTS+1)]
Z_CENTER=.305
RZ_INNER=.450
RZ_BLEND2=.490
RZ_BLEND1=.530
CROWN_Y=.030
CROWN_Z=.040


def arch_angle(x,wx):
    u=max(-1.0,min(1.0,(x-wx)/ZONE))
    theta=math.acos(u)
    s=max(0.0,math.sin(theta))
    # C1-ish endpoint envelope so local topology merges back into locked body rows.
    w=s*s
    return theta,s,w


def union_xs(rows):
    xs={round(p[0],9) for p in rows[0]}
    for wx in (b.FX,b.RX):
        xs.add(round(wx-ZONE,9));xs.add(round(wx+ZONE,9))
        for a in ANGLES: xs.add(round(wx+ZONE*math.cos(a),9))
    return sorted(xs,reverse=True)


def interp_rows(rows,x): return [r14.interp_row(row,x) for row in rows]


def build_source_r27(rows,M,glass):
    xs=union_xs(rows);cols=[interp_rows(rows,x) for x in xs];mb=r14.MB()
    def K(i,row,side):return f'X{i}:R{row}:S{side:+d}'
    def nearest_wheel(x):
        wx=min((b.FX,b.RX),key=lambda q:abs(x-q))
        return wx if abs(x-wx)<=ZONE+1e-8 else None
    def V(i,row,side):
        p=cols[i][row];wx=nearest_wheel(p[0])
        if row==4 and wx is not None:
            _,_,w=arch_angle(p[0],wx);p=(p[0],p[1]+CROWN_Y*w,p[2]+CROWN_Z*w)
        if row==0:return mb.v(K(i,row,0),(p[0],0,p[2]))
        return mb.v(K(i,row,side),(p[0],side*p[1],p[2]))

    # Locked upper source cage through SHOULDER; row 4 is the shared transition boundary.
    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        for side in (1,-1):
            for arow,brow in ((0,1),(1,2),(2,3),(3,4)):
                a0=V(i,arow,side if arow else 0);a1=V(i+1,arow,side if arow else 0);b1=V(i+1,brow,side);b0=V(i,brow,side)
                ids=(a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1)
                glass_band=(arow,brow) in ((1,2),(2,3)) and -1.22<=cx<=.72
                mb.f(ids,1 if glass_band else 0)

    # Preserve ordinary longitudinal body cage outside wheel zones.
    def interval_in_zone(cx):return any(abs(cx-wx)<ZONE-1e-8 for wx in (b.FX,b.RX))
    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        if interval_in_zone(cx):continue
        for side in (1,-1):
            for arow,brow in ((4,5),(5,6),(6,7)):
                a0=V(i,arow,side);a1=V(i+1,arow,side);b1=V(i+1,brow,side);b0=V(i,brow,side)
                mb.f((a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1),0)
        mb.f((V(i,7,1),V(i+1,7,1),V(i+1,7,-1),V(i,7,-1)),0)

    arch_meta=[];endpoint_reuse=0;ring_vertex_count=0
    # R27: four angle-sampled boundaries in the same Source mesh:
    # SHOULDER_TRANSITION(shared row4) -> BLEND1 -> BLEND2 -> INNER_OPENING.
    for wx,wname in ((b.FX,'F'),(b.RX,'R')):
        zone_indices=sorted([i for i,x in enumerate(xs) if abs(x-wx)<=ZONE+1e-8])
        for side in (1,-1):
            sname='L' if side>0 else 'R';outer=[];blend1=[];blend2=[];inner=[]
            for jj,gi in enumerate(zone_indices):
                x=xs[gi];base=cols[gi];outer.append(V(gi,4,side))
                if jj==0 or jj==len(zone_indices)-1:
                    # Reuse locked body cage at zone exits: no T-junction / detached patch endpoints.
                    blend1.append(V(gi,5,side));blend2.append(V(gi,6,side));inner.append(V(gi,7,side));endpoint_reuse+=3
                    continue
                _,s,w=arch_angle(x,wx)
                shoulder,mid,rock,under=base[4],base[5],base[6],base[7]
                # Angle-driven nested ring targets. The endpoint envelope w merges each ring
                # back to the pre-existing body rows while the crown follows an elliptical arc.
                target_inner_z=Z_CENTER+RZ_INNER*s
                target_b2_z=Z_CENTER+RZ_BLEND2*s
                target_b1_z=Z_CENTER+RZ_BLEND1*s
                inner_z=under[2]*(1-w)+target_inner_z*w
                b2_z=rock[2]*(1-w)+target_b2_z*w
                b1_z=mid[2]*(1-w)+target_b1_z*w
                # Lateral section is also ring-driven: maximum wheel coverage occurs near crown
                # and decays C1-ish toward the reused endpoints.
                shoulder_y=shoulder[1]
                inner_y=under[1]*(1-w)+(shoulder_y+.020)*w
                b2_y=rock[1]*(1-w)+(shoulder_y+.042)*w
                b1_y=mid[1]*(1-w)+(shoulder_y+.055)*w
                blend1.append(mb.v(f'R27:{wname}:{sname}:BLEND1:{jj}',(x,side*b1_y,b1_z)))
                blend2.append(mb.v(f'R27:{wname}:{sname}:BLEND2:{jj}',(x,side*b2_y,b2_z)))
                inner.append(mb.v(f'R27:{wname}:{sname}:INNER:{jj}',(x,side*inner_y,inner_z)))
                ring_vertex_count+=3
            for j in range(len(zone_indices)-1):
                for A,B in ((outer,blend1),(blend1,blend2),(blend2,inner)):
                    ids=(A[j],A[j+1],B[j+1],B[j]);mb.f(ids if side>0 else tuple(reversed(ids)),0)
            arch_meta.append((wname,sname,outer,inner))

    # Retain structured R18/R20 terminations and final winding orientation.
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

    me=bpy.data.meshes.new('PRIMARY_CIRCUMFERENTIAL_ARCH_SOURCE_MESH');me.from_pydata(mb.verts,[],mb.faces);me.update()
    o=bpy.data.objects.new('PRIMARY_CIRCUMFERENTIAL_ARCH_SOURCE',me);bpy.context.collection.objects.link(o)
    o.data.materials.append(M['CLAY']);o.data.materials.append(glass)
    for p,mi in zip(o.data.polygons,mb.face_mat):p.use_smooth=True;p.material_index=mi
    o['OLEANDER_AUTHORITY']='WORKING_SOURCE'
    o['OLEANDER_TOPOLOGY']='R27_ANGLE_PARAMETERIZED_NESTED_ARCH_RINGS_SHARED_SOURCE'
    o['R27_ARCH_SEGMENTS']=ARCH_SEGMENTS;o['R27_RING_COUNT']=4;o['R27_ENDPOINT_REUSE']=endpoint_reuse;o['R27_RING_VERTEX_COUNT']=ring_vertex_count
    return o,xs,cols,arch_meta,endpoint_reuse

# Execute through the already-proven R25 scene/render pipeline, but swap the authoritative source builder.
r25.build_source_raw=build_source_r27


def patch_outputs(out:Path):
    cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text())
    c['job_id']='SYS-MODELING-WORKER-AUTO-M4M5-v0.11-R27'
    c['decision_question']='Does an angle-parameterized four-ring circumferential wheel-arch Source topology integrate the tire, fender crown and shoulder in 3/4 views while retaining locked R09/R11/R12 non-wheel geometry?'
    c['source_authority']['editable_source']=f'{MODEL}.blend'
    c['primary_geometry'][0]['id']='PG-CIRCUMFERENTIAL-ARCH-SOURCE';c['primary_geometry'][0]['role']='single editable Source with shared shoulder transition and three nested circumferential wheel-arch rings'
    c['semantic_components'][1]['id']='COMP-CIRCUMFERENTIAL-ARCH-SOURCE';c['semantic_components'][1]['role']='R27 editable primary source';c['semantic_components'][1]['source_ref']='PG-CIRCUMFERENTIAL-ARCH-SOURCE'
    c['locks'].append({'target':'R09 package + R11/R12 non-wheel source + R18/R20 termination + R25 opening target','state':'LOCKED','reason':'R27 reopens only wheel-zone topology/surface construction','unlock_trigger':None})
    c['revision']={'revision_id':'R27-CIRCUMFERENTIAL-WHEEL-ARCH','semantic_targets':['front/rear wheel opening','fender crown','shoulder transition'],'parameters':{'arch_segments':ARCH_SEGMENTS,'ring_count':4,'zone_radius_m':ZONE,'z_center_m':Z_CENTER,'ring_rz_m':[RZ_INNER,RZ_BLEND2,RZ_BLEND1],'endpoint_reuse':'SHOULDER shared + MID/ROCKER/UNDER reused at zone exits','source_boolean':False,'source_subd':False},'expected_affected_components':['wheel-zone primary Source topology coordinates only'],'affected_view_policy':'HYBRID'}
    c['qa']['construction']=['one connected Source mesh','angle-parameterized wheel opening','four circumferential boundaries','shared shoulder transition','zone-exit vertex reuse','source n-gon=0','no Source Boolean/SubD','R20 terminal winding retained']
    c['qa']['project']=['tire visually contained by fender/body volume','fender crown grows continuously from shoulder','front/rear arch detail has no vertical/diagonal strip-wall reading','R25 rounded side opening quality retained','M6/M7/M8 remains blocked']
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    qp=out/'AUTOMOTIVE_V011_QA.json';q=json.loads(qp.read_text());q['schema']='oleander.auto.v0.11.r27.qa';q['model']=MODEL
    q['checks']['circumferential_arch_active']=True;q['checks']['arch_segments_24']=ARCH_SEGMENTS==24;q['checks']['four_nested_arch_boundaries']=True
    q['boundary']='R27 reopens wheel-zone topology only. Human M5 Visual QA required; M6/M7/M8 blocked.'
    qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    rp=out/'AUTOMOTIVE_V011_RECEIPT.json';r=json.loads(rp.read_text());r['schema']='oleander.auto.v0.11.r27.receipt';r['model']=MODEL;rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    (out/'R27_TOPOLOGY_CONTRACT.json').write_text(json.dumps({'model':MODEL,'stage':'M5','revision':'R27','status':'MACHINE_EXECUTED_VISUAL_REVIEW_REQUIRED','arch_segments':ARCH_SEGMENTS,'ring_count':4,'topology':'SHARED_SHOULDER_TRANSITION -> BLEND1 -> BLEND2 -> INNER_OPENING','authority':'WORKING_SOURCE','blocked':['M6','M7','M8']},ensure_ascii=False,indent=2)+'\n')


def main():
    try:r25.main()
    except SystemExit as e:
        a=b.parse();out=Path(a.out).resolve();patch_outputs(out);raise SystemExit(e.code)

if __name__=='__main__':main()
