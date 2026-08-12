#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R29 — HP-Correct Monotonic Nested Arch.

HP rebaseline A/B showed that the simpler R25 Source is materially cleaner than the
R28A-C full local patch family when both use the correct locked 0.700 m wheel package.
R29 therefore returns to R25 topology and changes only the local nested-arch vertical
ordering.

R25 apex ordering could overshoot:
  CROWN -> B1 (above INNER) -> B2 -> INNER
R29 makes the intended source relation monotonic:
  CROWN -> B1 -> B2 -> INNER
while keeping:
- R25 rounded x-z opening target;
- R25 single-mesh/shared-endpoint longitudinal topology;
- R09/R11/R12/R18/R20 locked outside the wheel-zone revision;
- no Boolean, global SubD or n-gon;
- corrected 0.700 m wheel package in all canonical evidence.
"""
from __future__ import annotations
import importlib.util,bpy,json,math
from pathlib import Path

BASE='/tmp/revise_v011_r25.py'
spec=importlib.util.spec_from_file_location('r25',BASE)
r25=importlib.util.module_from_spec(spec);spec.loader.exec_module(r25)
r24=r25.r24;r20=r25.r20;r18=r25.r18;r16=r25.r16;r14=r25.r14;b=r25.b

MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R29'
for m in (r25,r24,r20,r18,r16,r16.r15,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):
    m.MODEL=MODEL

TARGET_OD=.700
CROWN_Y=.012
CROWN_Z=.020
B1_T=.36
B2_T=.68
APEX_RECORD=[]
WHEEL_FIX=[]

_orig_wheels=b.wheels

def mesh_world_bounds(o):
    pts=[o.matrix_world@v.co for v in o.data.vertices]
    mn=[min(p[i] for p in pts) for i in range(3)]
    mx=[max(p[i] for p in pts) for i in range(3)]
    return {'min':mn,'max':mx,'dimensions':[mx[i]-mn[i] for i in range(3)],'center':[(mn[i]+mx[i])*.5 for i in range(3)]}

def hp_wheels(M):
    res=_orig_wheels(M)
    for o in [x for x in bpy.context.scene.objects if x.type=='MESH' and x.name.startswith('WHEEL_')]:
        before=mesh_world_bounds(o);cx=before['center'][0];cz=before['center'][2]
        fx=TARGET_OD/before['dimensions'][0];fz=TARGET_OD/before['dimensions'][2];inv=o.matrix_world.inverted()
        for v in o.data.vertices:
            p=o.matrix_world@v.co;p.x=cx+(p.x-cx)*fx;p.z=cz+(p.z-cz)*fz;v.co=inv@p
        o.data.update();bpy.context.view_layer.update();after=mesh_world_bounds(o)
        WHEEL_FIX.append({'name':o.name,'before':before,'after':after,'factor_x':fx,'factor_z':fz})
    return res
b.wheels=hp_wheels


def lerp(a,bv,t):return a+(bv-a)*t

def build_source_r29(rows,M,glass):
    xs=r25.union_xs(rows);cols=[r25.interp_rows(rows,x) for x in xs]
    mb=r14.MB()
    def K(i,row,side):return f'X{i}:R{row}:S{side:+d}'
    def local_s(x):return max(r25.arch_shape(x,b.FX),r25.arch_shape(x,b.RX))
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
                ids=(a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1)
                glass_band=(arow,brow) in ((1,2),(2,3)) and -1.22<=cx<=.72
                mb.f(ids,1 if glass_band else 0)

    def interval_in_zone(cx):return any(abs(cx-wx)<r25.ZONE-1e-8 for wx in (b.FX,b.RX))
    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        if interval_in_zone(cx):continue
        for side in (1,-1):
            for arow,brow in ((4,5),(5,6),(6,7)):
                a0=V(i,arow,side);a1=V(i+1,arow,side);b1=V(i+1,brow,side);b0=V(i,brow,side)
                mb.f((a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1),0)
        mb.f((V(i,7,1),V(i+1,7,1),V(i+1,7,-1),V(i,7,-1)),0)

    arch_meta=[];endpoint_reuse=0
    for wx,wname in ((b.FX,'F'),(b.RX,'R')):
        zone_indices=sorted([i for i,x in enumerate(xs) if abs(x-wx)<=r25.ZONE+1e-8])
        for side in (1,-1):
            sname='L' if side>0 else 'R';crown=[];b1s=[];b2s=[];inner=[]
            best=None
            for jj,gi in enumerate(zone_indices):
                x=xs[gi];s=r25.arch_shape(x,wx);base=cols[gi];cvi=V(gi,4,side);crown.append(cvi)
                if jj==0 or jj==len(zone_indices)-1:
                    b1s.append(V(gi,5,side));b2s.append(V(gi,6,side));inner.append(V(gi,7,side));endpoint_reuse+=3;continue
                shoulder=base[4];mid=base[5];rock=base[6];under=base[7]
                inner_z=under[2]+s*(r25.ARCH_TOP_Z-under[2])
                inner_y=under[1]+s*((shoulder[1]-.024)-under[1])
                cp=mb.verts[cvi];crown_y=abs(cp[1]);crown_z=cp[2]

                # Target B1/B2 are ordered samples between crown and inner boundary.
                t1_y=lerp(crown_y,inner_y,B1_T);t1_z=lerp(crown_z,inner_z,B1_T)
                t2_y=lerp(crown_y,inner_y,B2_T);t2_z=lerp(crown_z,inner_z,B2_T)
                # Fade from inherited MID/ROCKER rows into the ordered local targets.
                b1_y=mid[1]+s*(t1_y-mid[1]);b1_z=mid[2]+s*(t1_z-mid[2])
                b2_y=rock[1]+s*(t2_y-rock[1]);b2_z=rock[2]+s*(t2_z-rock[2])
                b1v=mb.v(f'R29:{wname}:{sname}:B1:{jj}',(x,side*b1_y,b1_z))
                b2v=mb.v(f'R29:{wname}:{sname}:B2:{jj}',(x,side*b2_y,b2_z))
                inv=mb.v(f'R29:{wname}:{sname}:INNER:{jj}',(x,side*inner_y,inner_z))
                b1s.append(b1v);b2s.append(b2v);inner.append(inv)
                if best is None or s>best[0]:best=(s,cvi,b1v,b2v,inv,x)
            for j in range(len(zone_indices)-1):
                for A,B in ((crown,b1s),(b1s,b2s),(b2s,inner)):
                    ids=(A[j],A[j+1],B[j+1],B[j]);mb.f(ids if side>0 else tuple(reversed(ids)),0)
            if best:
                _,cv,v1,v2,iv,x=best
                zs=[mb.verts[k][2] for k in (cv,v1,v2,iv)]
                ys=[abs(mb.verts[k][1]) for k in (cv,v1,v2,iv)]
                APEX_RECORD.append({'wheel':wname,'side':sname,'x_m':x,'z_crown_b1_b2_inner':zs,'y_crown_b1_b2_inner':ys,'z_monotonic':zs[0]<=zs[1]<=zs[2]<=zs[3]+1e-9,'y_monotonic_out_to_in':ys[0]>=ys[1]>=ys[2]>=ys[3]-1e-9})
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

    me=bpy.data.meshes.new('PRIMARY_R29_MONOTONIC_ARCH_SOURCE_MESH');me.from_pydata(mb.verts,[],mb.faces);me.update()
    o=bpy.data.objects.new('PRIMARY_R29_MONOTONIC_ARCH_SOURCE',me);bpy.context.collection.objects.link(o)
    o.data.materials.append(M['CLAY']);o.data.materials.append(glass)
    for p,mi in zip(o.data.polygons,mb.face_mat):p.use_smooth=True;p.material_index=mi
    o['OLEANDER_AUTHORITY']='WORKING_SOURCE';o['OLEANDER_TOPOLOGY']='R29_R25_SHARED_ENDPOINT_MONOTONIC_NESTED_ARCH'
    return o,xs,cols,arch_meta,endpoint_reuse

r25.build_source_raw=build_source_r29


def patch_outputs(out:Path):
    cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text())
    c['job_id']='SYS-MODELING-WORKER-AUTO-M4M5-v0.11-R29'
    c['decision_question']='Under the corrected 0.700 m wheel package and retained R25 Source topology, does monotonic CROWN→B1→B2→INNER ordering remove the cap-like overshoot/pinching while preserving the cleaner R25 broad surface?'
    c['source_authority']['editable_source']=f'{MODEL}.blend'
    c['revision']={'revision_id':'R29-HP-CORRECT-MONOTONIC-NESTED-ARCH','semantic_targets':['front/rear wheel-zone nested arch vertical ordering'],'parameters':{'base_architecture':'R25_HP_CORRECT','target_wheel_od_m':TARGET_OD,'crown_y_m':CROWN_Y,'crown_z_m':CROWN_Z,'b1_fraction':B1_T,'b2_fraction':B2_T,'rounded_xz_opening_locked':True,'source_boolean':False,'source_subd':False},'expected_affected_components':['wheel-zone CROWN/B1/B2/INNER coordinates only','wheel display/package meshes'], 'affected_view_policy':'HYBRID'}
    c['locks'].append({'target':'R25 topology + rounded x-z opening + R09/R11/R12/R18/R20 + non-wheel Source','state':'LOCKED','reason':'R29 returns to HP-correct R25 and isolates nested-arch ordering','unlock_trigger':None})
    c['qa']['project']=['R25 cap-like crown must reduce','fore/aft arch pinching must reduce','broad Hero/Strip/Grazing surface must remain cleaner than R28 family','corrected wheel must remain contained without forcing crown outside shoulder','M6/M7/M8 remains blocked']
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')

    qp=out/'AUTOMOTIVE_V011_QA.json';q=json.loads(qp.read_text());q['schema']='oleander.auto.v0.11.r29.qa';q['model']=MODEL
    q['checks']['wheel_hp_package_exact']=len(WHEEL_FIX)==4 and all(abs(x['after']['dimensions'][0]-TARGET_OD)<1e-5 and abs(x['after']['dimensions'][2]-TARGET_OD)<1e-5 for x in WHEEL_FIX)
    q['checks']['wheel_centers_retained']=len(WHEEL_FIX)==4 and all(abs(x['after']['center'][0]-x['before']['center'][0])<1e-6 and abs(x['after']['center'][2]-x['before']['center'][2])<1e-6 for x in WHEEL_FIX)
    q['checks']['wheel_y_thickness_retained']=len(WHEEL_FIX)==4 and all(abs(x['after']['dimensions'][1]-x['before']['dimensions'][1])<1e-6 for x in WHEEL_FIX)
    q['checks']['four_apex_records']=len(APEX_RECORD)==4
    q['checks']['apex_z_monotonic']=len(APEX_RECORD)==4 and all(x['z_monotonic'] for x in APEX_RECORD)
    q['checks']['apex_y_monotonic']=len(APEX_RECORD)==4 and all(x['y_monotonic_out_to_in'] for x in APEX_RECORD)
    q['checks']['r25_hp_correct_baseline_retained']=True
    q['boundary']='R29 returns to the R25 HP-correct Source family and changes only local nested-arch ordering. R28A-C are superseded exploration. Human M5 required; M6/M7/M8 blocked.'
    q['status']='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(q['checks'].values()) else 'MACHINE_FAIL'
    qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')

    rp=out/'AUTOMOTIVE_V011_RECEIPT.json';r=json.loads(rp.read_text());r['schema']='oleander.auto.v0.11.r29.receipt';r['model']=MODEL;r['status']='EXECUTED_'+q['status'];rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    (out/'R29_ARCH_CONTEXT.json').write_text(json.dumps({'schema':'oleander.auto.v0.11.r29.arch-context','model':MODEL,'target_wheel_od_m':TARGET_OD,'base':'R25_HP_CORRECT','apex_records':APEX_RECORD,'wheel_normalization':WHEEL_FIX,'r28_family_status':'SUPERSEDED_AUDIT_ONLY'},ensure_ascii=False,indent=2)+'\n')
    return q


def main():
    code=0
    try:r25.main()
    except SystemExit as e:code=int(e.code or 0)
    a=b.parse();out=Path(a.out).resolve();q=patch_outputs(out)
    raise SystemExit(0 if q['status']=='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' else (code or 5))

if __name__=='__main__':main()
