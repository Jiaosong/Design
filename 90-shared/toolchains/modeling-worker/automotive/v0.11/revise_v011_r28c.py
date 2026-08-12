#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R28C — Zero-Bulge Radial Fender Patch.

R28B proved the corrected 0.70 m wheel package fits under an inset crown with 30 mm
lateral cover, but Human M5 still showed the R28A folded/ridged local fender surface.
R28C keeps every R28B package and topology decision and removes only the artificial
intermediate radial-layer bulge (+18 mm Y / +10 mm Z in R28A).

Decision question: is the remaining fold caused by radial-layer overshoot, or by the
U-boundary-to-polar-boundary parameter mapping itself?
"""
from __future__ import annotations
import importlib.util,bpy,bmesh,json,math
from pathlib import Path

BASE='/tmp/revise_v011_r28b.py'
spec=importlib.util.spec_from_file_location('r28b',BASE)
r28b=importlib.util.module_from_spec(spec);spec.loader.exec_module(r28b)
r28a=r28b.r28a;r25=r28b.r25;r24=r28b.r24;r20=r28b.r20;r18=r28b.r18;r16=r28b.r16;r14=r28b.r14;b=r28b.b

MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R28C'
for m in (r28b,r28a,r25,r24,r20,r18,r16,r16.r15,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):
    m.MODEL=MODEL


def build_source_r28c(rows,M,glass):
    xs=r28a.union_xs(rows)
    cols=[[r14.interp_row(row,x) for row in rows] for x in xs]
    xmap={round(x,9):i for i,x in enumerate(xs)}
    mb=r14.MB()
    def I(x):return xmap[round(x,9)]
    def K(i,row,side):return f'X{i}:R{row}:S{side:+d}'
    def V(i,row,side):
        p=cols[i][row]
        if row==0:return mb.v(K(i,row,0),(p[0],0,p[2]))
        return mb.v(K(i,row,side),(p[0],side*p[1],p[2]))

    # Upper body through shoulder stays exactly as R28A/B.
    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        for side in (1,-1):
            for arow,brow in ((0,1),(1,2),(2,3),(3,4)):
                a0=V(i,arow,side if arow else 0);a1=V(i+1,arow,side if arow else 0);b1=V(i+1,brow,side);b0=V(i,brow,side)
                ids=(a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1)
                glass_band=(arow,brow) in ((1,2),(2,3)) and -1.22<=cx<=.72
                mb.f(ids,1 if glass_band else 0)

    def in_window(cx):return any(abs(cx-wx)<r28a.WINDOW-1e-8 for wx in (b.FX,b.RX))
    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        if in_window(cx):continue
        for side in (1,-1):
            for arow,brow in ((4,5),(5,6),(6,7)):
                a0=V(i,arow,side);a1=V(i+1,arow,side);b1=V(i+1,brow,side);b0=V(i,brow,side)
                mb.f((a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1),0)
        mb.f((V(i,7,1),V(i+1,7,1),V(i+1,7,-1),V(i,7,-1)),0)

    arch_meta=[];boundary_reuse=0
    for wx,wname in ((b.FX,'F'),(b.RX,'R')):
        for side in (1,-1):
            sname='L' if side>0 else 'R';outer=[];xl=wx-r28a.WINDOW;xr=wx+r28a.WINDOW
            for row in (7,6,5,4):outer.append(V(I(xl),row,side))
            for i in range(1,r28a.TOP_SAMPLES-1):
                x=xl+2*r28a.WINDOW*i/(r28a.TOP_SAMPLES-1);outer.append(V(I(x),4,side))
            for row in (4,5,6,7):
                vi=V(I(xr),row,side)
                if not outer or vi!=outer[-1]:outer.append(vi)
            boundary_reuse+=len(outer)

            coords=[mb.verts[v] for v in outer];cum=[0.0]
            for a,c in zip(coords[:-1],coords[1:]):cum.append(cum[-1]+math.dist(a,c))
            total=max(cum[-1],1e-9);inner=[]
            for j,(ov,d) in enumerate(zip(outer,cum)):
                t=d/total;theta=math.pi*(1.0-t);s=max(0.0,math.sin(theta));w=s*s
                x=wx+r28a.INNER_RX*math.cos(theta);base=r14.interp_row(rows[7],x);shoulder=r14.interp_row(rows[4],x)
                z=r28a.lerp(base[2],r28a.ZC+r28a.INNER_RZ*s,w)
                y=r28a.lerp(base[1],shoulder[1]+r28a.LIP_Y,w)
                inner.append(mb.v(f'R28C:{wname}:{sname}:INNER:{j}',(x,side*y,z)))

            # R28C difference: no artificial y/z bulge. Pure monotonic smoothstep bridge.
            layers=[inner]
            for li in range(1,r28a.RADIAL_LAYERS-1):
                u=li/(r28a.RADIAL_LAYERS-1);q=r28a.smoothstep(u);layer=[]
                for j,(iv,ov) in enumerate(zip(inner,outer)):
                    pi=mb.verts[iv];po=mb.verts[ov]
                    p=(r28a.lerp(pi[0],po[0],q),r28a.lerp(abs(pi[1]),abs(po[1]),q),r28a.lerp(pi[2],po[2],q))
                    layer.append(mb.v(f'R28C:{wname}:{sname}:L{li}:{j}',(p[0],side*p[1],p[2])))
                layers.append(layer)
            layers.append(outer)
            for li in range(r28a.RADIAL_LAYERS-1):
                A=layers[li];B=layers[li+1]
                for j in range(len(outer)-1):
                    ids=(A[j],A[j+1],B[j+1],B[j]);mb.f(ids if side>0 else tuple(reversed(ids)),0)
            arch_meta.append((wname,sname,layers[-2],inner))

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

    me=bpy.data.meshes.new('PRIMARY_LOCAL_FENDER_PATCH_R28C_MESH');me.from_pydata(mb.verts,[],mb.faces);me.update()
    o=bpy.data.objects.new('PRIMARY_LOCAL_FENDER_PATCH_R28C',me);bpy.context.collection.objects.link(o);o.data.materials.append(M['CLAY']);o.data.materials.append(glass)
    for p,mi in zip(o.data.polygons,mb.face_mat):p.use_smooth=True;p.material_index=mi
    bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
    o['OLEANDER_AUTHORITY']='WORKING_SOURCE';o['OLEANDER_TOPOLOGY']='R28C_R28A_PATCH_ZERO_RADIAL_BULGE';o['R28_WINDOW_HALF_M']=r28a.WINDOW;o['R28_RADIAL_LAYERS']=r28a.RADIAL_LAYERS;o['R28_BOUNDARY_REUSE_COUNT']=boundary_reuse
    return o,xs,cols,arch_meta,boundary_reuse

r25.build_source_raw=build_source_r28c


def patch_outputs(out:Path):
    cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text())
    c['job_id']='SYS-MODELING-WORKER-AUTO-M4M5-v0.11-R28C'
    c['decision_question']='With R28B package correction and inset crown locked, does removing the R28A artificial intermediate radial-layer bulge eliminate the folded/ridged fender surface?'
    c['source_authority']['editable_source']=f'{MODEL}.blend'
    c['revision']['revision_id']='R28C-ZERO-RADIAL-BULGE';c['revision']['semantic_targets']=['front/rear local fender radial interpolation only'];c['revision']['parameters']['radial_bulge_y_m']=0.0;c['revision']['parameters']['radial_bulge_z_m']=0.0;c['revision']['parameters']['r28b_package_and_crown_locked']=True
    c['locks'].append({'target':'R28B wheel HP normalization + crown inset + R28A topology/U boundary/opening x-z','state':'LOCKED','reason':'R28C isolates intermediate radial overshoot only','unlock_trigger':None})
    c['qa']['project']=['R28B folded/ridged fender highlight must reduce materially','no new self-overlap from zero-bulge bridge','package clearance remains >=15 mm','M6/M7/M8 remains blocked']
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')

    qp=out/'AUTOMOTIVE_V011_QA.json';q=json.loads(qp.read_text());q['schema']='oleander.auto.v0.11.r28c.qa';q['model']=MODEL;q['checks']['zero_radial_bulge_active']=True;q['boundary']='R28C retains R28B corrected wheel package, inset crown and R28A topology. Intermediate radial y/z bulge is zero. Human M5 required; M6/M7/M8 blocked.';q['status']='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(q['checks'].values()) else 'MACHINE_FAIL';qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    rp=out/'AUTOMOTIVE_V011_RECEIPT.json';r=json.loads(rp.read_text());r['schema']='oleander.auto.v0.11.r28c.receipt';r['model']=MODEL;r['status']='EXECUTED_'+q['status'];rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    tp=out/'R28_PATCH_CONTRACT.json';t=json.loads(tp.read_text());t['model']=MODEL;t['revision']='R28C';t['status']=q['status'];t['topology']='R28A_LOCAL_PATCH_R28B_PACKAGE_ZERO_RADIAL_BULGE';t['radial_bulge_y_m']=0.0;t['radial_bulge_z_m']=0.0;tp.write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n')
    return q


def main():
    code=0
    try:r28b.main()
    except SystemExit as e:code=int(e.code or 0)
    a=b.parse();out=Path(a.out).resolve();q=patch_outputs(out)
    raise SystemExit(0 if q['status']=='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' else (code or 5))

if __name__=='__main__':main()
