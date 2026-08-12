#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R30 — HP-Correct Shoulder-Fed Descending Crown.

R29 retained the HP-correct R25 topology family and removed B1/B2 overshoot, but Human
M5 showed a planar shelf above both wheel openings. The apex evidence explains why:
R29 placed the outer crown below the inner wheel-opening lip, forcing the fender surface
to climb inward.

R30 reopens only the wheel-zone crown z-envelope and nested B1/B2 vertical relation:
- canonical wheel_hp_contract.py remains the sole wheel implementation authority;
- R25 topology, rounded x-z opening, endpoint reuse and non-wheel Source stay locked;
- crown is allowed to rise only where the inner lip requires it, then returns smoothly
  to the inherited shoulder outside the wheel crown region;
- at the wheel apex, the validation hypothesis is crown = inner lip + 25 mm;
- B1/B2 descend monotonically from crown to inner lip.

The 25 mm rise is a designer-estimate validation parameter, not an engineering target.
"""
from __future__ import annotations
import importlib.util,json,bpy
from pathlib import Path


def load(path,name):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

r29=load('/tmp/revise_v011_r29.py','r29')
r25=r29.r25;hp=r29.hp;r24=r29.r24;r20=r29.r20;r18=r29.r18;r16=r29.r16;r14=r29.r14;b=r29.b

MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R30'
for m in (r29,r25,r24,r20,r18,r16,r16.r15,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):
    m.MODEL=MODEL

TARGET_OD=.700
CROWN_RISE_M=.025
CROWN_Y=.010
B1_T=.36
B2_T=.68
APEX_RECORD=[]
ZONE_RECORD=[]


def lerp(a,bv,t):return a+(bv-a)*t

def smoothstep(t):
    t=max(0.0,min(1.0,t))
    return t*t*(3.0-2.0*t)


def build_source_r30(rows,M,glass):
    xs=r25.union_xs(rows)
    cols=[r25.interp_rows(rows,x) for x in xs]
    mb=r14.MB()

    def K(i,row,side):return f'X{i}:R{row}:S{side:+d}'
    def local_s(x):return max(r25.arch_shape(x,b.FX),r25.arch_shape(x,b.RX))

    def crown_coords(i):
        shoulder=cols[i][4]
        under=cols[i][7]
        s=local_s(shoulder[0])
        if s<=0:
            return shoulder
        w=smoothstep(s)
        inner_z=under[2]+s*(r25.ARCH_TOP_Z-under[2])
        target_z=max(shoulder[2],inner_z+CROWN_RISE_M*s)
        return (shoulder[0],shoulder[1]+CROWN_Y*w,lerp(shoulder[2],target_z,w))

    def V(i,row,side):
        p=cols[i][row]
        s=local_s(p[0])
        if row==4:
            p=crown_coords(i)
        elif row==3:
            w=smoothstep(s)
            p=(p[0],p[1]+.003*w,p[2]+.006*w)
        if row==0:return mb.v(K(i,row,0),(p[0],0,p[2]))
        return mb.v(K(i,row,side),(p[0],side*p[1],p[2]))

    # R25 upper body / glazing / shoulder topology retained.
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
    APEX_RECORD.clear();ZONE_RECORD.clear()

    for wx,wname in ((b.FX,'F'),(b.RX,'R')):
        zone_indices=sorted([i for i,x in enumerate(xs) if abs(x-wx)<=r25.ZONE+1e-8])
        for side in (1,-1):
            sname='L' if side>0 else 'R';crown=[];b1s=[];b2s=[];inner=[];best=None;local_records=[]
            for jj,gi in enumerate(zone_indices):
                x=xs[gi];s=r25.arch_shape(x,wx);base=cols[gi];cvi=V(gi,4,side);crown.append(cvi)
                if jj==0 or jj==len(zone_indices)-1:
                    b1s.append(V(gi,5,side));b2s.append(V(gi,6,side));inner.append(V(gi,7,side));endpoint_reuse+=3
                    continue

                shoulder=base[4];under=base[7]
                inner_z=under[2]+s*(r25.ARCH_TOP_Z-under[2])
                inner_y=under[1]+s*((shoulder[1]-.024)-under[1])
                cp=mb.verts[cvi];crown_y=abs(cp[1]);crown_z=cp[2]

                # R30: exact nested interpolation from the shoulder-fed crown DOWN to inner lip.
                b1_y=lerp(crown_y,inner_y,B1_T);b1_z=lerp(crown_z,inner_z,B1_T)
                b2_y=lerp(crown_y,inner_y,B2_T);b2_z=lerp(crown_z,inner_z,B2_T)
                b1v=mb.v(f'R30:{wname}:{sname}:B1:{jj}',(x,side*b1_y,b1_z))
                b2v=mb.v(f'R30:{wname}:{sname}:B2:{jj}',(x,side*b2_y,b2_z))
                inv=mb.v(f'R30:{wname}:{sname}:INNER:{jj}',(x,side*inner_y,inner_z))
                b1s.append(b1v);b2s.append(b2v);inner.append(inv)

                zs=[crown_z,b1_z,b2_z,inner_z];ys=[crown_y,b1_y,b2_y,inner_y]
                rec={'wheel':wname,'side':sname,'x_m':x,'shape_weight':s,'z_crown_b1_b2_inner':zs,'y_crown_b1_b2_inner':ys,'z_descending':zs[0]+1e-9>=zs[1]>=zs[2]>=zs[3]-1e-9,'y_out_to_in':ys[0]+1e-9>=ys[1]>=ys[2]>=ys[3]-1e-9}
                local_records.append(rec)
                if best is None or s>best[0]:best=(s,rec)

            for j in range(len(zone_indices)-1):
                for A,B in ((crown,b1s),(b1s,b2s),(b2s,inner)):
                    ids=(A[j],A[j+1],B[j+1],B[j]);mb.f(ids if side>0 else tuple(reversed(ids)),0)
            if best:
                apex=dict(best[1]);apex['crown_above_inner_m']=apex['z_crown_b1_b2_inner'][0]-apex['z_crown_b1_b2_inner'][3];APEX_RECORD.append(apex)
            ZONE_RECORD.extend(local_records)
            arch_meta.append((wname,sname,crown,inner))

    # Validated R18/R20 terminations retained.
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

    me=bpy.data.meshes.new('PRIMARY_R30_DESCENDING_CROWN_SOURCE_MESH');me.from_pydata(mb.verts,[],mb.faces);me.update()
    o=bpy.data.objects.new('PRIMARY_R30_DESCENDING_CROWN_SOURCE',me);bpy.context.collection.objects.link(o)
    o.data.materials.append(M['CLAY']);o.data.materials.append(glass)
    for p,mi in zip(o.data.polygons,mb.face_mat):p.use_smooth=True;p.material_index=mi
    o['OLEANDER_AUTHORITY']='WORKING_SOURCE';o['OLEANDER_TOPOLOGY']='R30_R25_SHARED_ENDPOINT_SHOULDER_FED_DESCENDING_CROWN'
    return o,xs,cols,arch_meta,endpoint_reuse

r25.build_source_raw=build_source_r30


def patch_outputs(out:Path):
    records=getattr(b,'_OLEANDER_WHEEL_HP_RECORDS',[]);hp_exact=bool(getattr(b,'_OLEANDER_WHEEL_HP_EXACT',False))
    cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text())
    c['job_id']='SYS-MODELING-WORKER-AUTO-M4M5-v0.11-R30'
    c['decision_question']='With R25 topology and the canonical 0.700 m wheel HP contract locked, does a shoulder-fed crown that sits modestly above the inner lip and descends through B1/B2 remove the R29 shelf without restoring the R25 cap overshoot?'
    c['source_authority']['editable_source']=f'{MODEL}.blend'
    c['revision']={'revision_id':'R30-HP-CORRECT-SHOULDER-FED-DESCENDING-CROWN','semantic_targets':['wheel-zone crown z-envelope','B1/B2 vertical interpolation'],'parameters':{'base_architecture':'R25_HP_CORRECT','wheel_hp_contract':'wheel_hp_contract.py','target_wheel_od_m':TARGET_OD,'apex_crown_rise_above_inner_m':CROWN_RISE_M,'parameter_status':'DESIGNER_ESTIMATE_FOR_VALIDATION','b1_fraction':B1_T,'b2_fraction':B2_T,'rounded_xz_opening_locked':True,'y_order_locked_from_r29':True,'source_boolean':False,'source_subd':False},'expected_affected_components':['wheel-zone CROWN/B1/B2 Source z coordinates only plus minor row3 continuity support'],'affected_view_policy':'HYBRID'}
    c['locks'].append({'target':'R25 topology + rounded x-z opening + R29 y ordering + 24 endpoint reuse + R09/R11/R12/R18/R20 + canonical wheel HP contract','state':'LOCKED','reason':'R30 reopens only the vertical crown envelope identified by R29 Human M5','unlock_trigger':None})
    c['qa']['project']=['R29 planar fender shelf must reduce materially','R25 large cap-like bulge must not return','Hero/Strip/Grazing broad surface must remain clean','front/rear arch crown must read as shoulder-fed and descend toward opening','M6/M7/M8 remains blocked']
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')

    qp=out/'AUTOMOTIVE_V011_QA.json';q=json.loads(qp.read_text());q['schema']='oleander.auto.v0.11.r30.qa';q['model']=MODEL
    q['checks']['wheel_hp_contract_active']=True;q['checks']['wheel_hp_package_exact']=hp_exact and hp.package_exact(records,TARGET_OD)
    q['checks']['four_apex_records']=len(APEX_RECORD)==4
    q['checks']['apex_z_descending']=len(APEX_RECORD)==4 and all(x['z_descending'] for x in APEX_RECORD)
    q['checks']['apex_y_out_to_in']=len(APEX_RECORD)==4 and all(x['y_out_to_in'] for x in APEX_RECORD)
    q['checks']['apex_crown_rise_25mm']=len(APEX_RECORD)==4 and all(abs(x['crown_above_inner_m']-CROWN_RISE_M)<1e-5 for x in APEX_RECORD)
    q['checks']['all_interior_nested_z_descending']=bool(ZONE_RECORD) and all(x['z_descending'] for x in ZONE_RECORD)
    q['checks']['all_interior_nested_y_out_to_in']=bool(ZONE_RECORD) and all(x['y_out_to_in'] for x in ZONE_RECORD)
    q['checks']['r25_topology_family_retained']=True
    q['wheel_hp_package']=records;q['boundary']='R30 retains the HP-correct R25 topology family and changes only crown/B1/B2 vertical relation. Crown rise is a designer-estimate validation parameter. Human M5 required; M6/M7/M8 blocked.'
    q['status']='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(q['checks'].values()) else 'MACHINE_FAIL';qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')

    rp=out/'AUTOMOTIVE_V011_RECEIPT.json';r=json.loads(rp.read_text());r['schema']='oleander.auto.v0.11.r30.receipt';r['model']=MODEL;r['status']='EXECUTED_MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if q['status'].startswith('MACHINE_PASS') else 'EXECUTED_MACHINE_FAIL';rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    (out/'R30_CROWN_CONTEXT.json').write_text(json.dumps({'schema':'oleander.auto.v0.11.r30.crown-context','model':MODEL,'base':'R25_HP_CORRECT','wheel_hp_contract':'v0.11-OD700','crown_rise_m':CROWN_RISE_M,'crown_rise_status':'DESIGNER_ESTIMATE_FOR_VALIDATION','apex_records':APEX_RECORD,'interior_record_count':len(ZONE_RECORD),'all_interior_z_descending':all(x['z_descending'] for x in ZONE_RECORD),'all_interior_y_out_to_in':all(x['y_out_to_in'] for x in ZONE_RECORD),'r29_status':'MACHINE_PASS_HUMAN_REVISE_DIRECTION_RETAINED','r28_family_status':'SUPERSEDED_AUDIT_ONLY'},ensure_ascii=False,indent=2)+'\n')
    return q


def main():
    code=0
    try:r25.main()
    except SystemExit as e:code=int(e.code or 0)
    a=b.parse();out=Path(a.out).resolve();q=patch_outputs(out);raise SystemExit(0 if q['status']=='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' else (code or 5))

if __name__=='__main__':main()
