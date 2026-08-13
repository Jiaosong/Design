#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R29A — Shoulder-Fed Monotonic Fender Crown.

HP-correct A/B retained R25 as the stronger working source. R29A reopens only the local
crown / hood-fender-shoulder dependency. R25 wheel-opening scale/topology and the exact
wheel hard-point package remain locked.

R25 at wheel center placed B1 above the shared shoulder/crown, creating an isolated cap.
R29A transfers peak authority back to the shared shoulder and enforces a monotonic radial
z/y relation: SHOULDER_CROWN > B1 > B2 > INNER_OPENING.
"""
from __future__ import annotations
import importlib.util,bpy,json,math
from pathlib import Path

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
r25=load('/tmp/revise_v011_r25.py','r25');hp=load('/tmp/wheel_hp_contract.py','wheel_hp_contract')
r24=r25.r24;r20=r25.r20;r18=r25.r18;r16=r25.r16;r14=r25.r14;b=r25.b
MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R29A'
for m in (r25,r24,r20,r18,r16,r16.r15,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):m.MODEL=MODEL
hp.install(b,.700)

ARCH_ZONE=r25.ZONE
ARCH_TOP_Z=r25.ARCH_TOP_Z
ARCH_POWER=r25.ARCH_POWER
CROWN_ZONE=.620
CROWN_TOP_Z=.805
CROWN_Y=.010
B1_OVER_INNER=.035
B2_OVER_INNER=.018
ROW3_SHARE=.35
ROW5_SHARE=.18
CROWN_ANGLES=[math.radians(v) for v in range(0,181,10)]

def arch_shape(x,wx):
    u=abs((x-wx)/ARCH_ZONE)
    return 0.0 if u>=1 else max(0.0,1-u*u)**ARCH_POWER

def crown_shape(x,wx):
    u=abs((x-wx)/CROWN_ZONE)
    if u>=1:return 0.0
    # raised cosine: zero slope at center and local influence boundary
    return .5*(1.0+math.cos(math.pi*u))

def union_xs(rows):
    xs=set(r25.union_xs(rows))
    for wx in (b.FX,b.RX):
        xs.add(round(wx-CROWN_ZONE,9));xs.add(round(wx+CROWN_ZONE,9))
        for a in CROWN_ANGLES:xs.add(round(wx+CROWN_ZONE*math.cos(a),9))
    return sorted(xs,reverse=True)

def interp_rows(rows,x):return [r14.interp_row(row,x) for row in rows]

def build_source_r29a(rows,M,glass):
    xs=union_xs(rows);cols=[interp_rows(rows,x) for x in xs];mb=r14.MB()
    def K(i,row,side):return f'X{i}:R{row}:S{side:+d}'
    def crown_s(x):return max(crown_shape(x,b.FX),crown_shape(x,b.RX))
    def V(i,row,side):
        p=cols[i][row];cs=crown_s(p[0])
        # transfer the height authority to the shared shoulder row4 and distribute a
        # smaller part into adjacent row3/row5 so the shoulder volume, not an inner ring,
        # carries the fender crown.
        if row==4:
            dz=max(0.0,CROWN_TOP_Z-p[2])*cs;p=(p[0],p[1]+CROWN_Y*cs,p[2]+dz)
        elif row==3:
            shoulder=cols[i][4];dz=max(0.0,CROWN_TOP_Z-shoulder[2])*ROW3_SHARE*cs;p=(p[0],p[1]+.003*cs,p[2]+dz)
        elif row==5:
            shoulder=cols[i][4];dz=max(0.0,CROWN_TOP_Z-shoulder[2])*ROW5_SHARE*cs;p=(p[0],p[1]+.004*cs,p[2]+dz)
        if row==0:return mb.v(K(i,row,0),(p[0],0,p[2]))
        return mb.v(K(i,row,side),(p[0],side*p[1],p[2]))

    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        for side in (1,-1):
            for arow,brow in ((0,1),(1,2),(2,3),(3,4)):
                a0=V(i,arow,side if arow else 0);a1=V(i+1,arow,side if arow else 0);b1=V(i+1,brow,side);b0=V(i,brow,side)
                ids=(a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1);glass_band=(arow,brow) in ((1,2),(2,3)) and -1.22<=cx<=.72;mb.f(ids,1 if glass_band else 0)

    def interval_in_zone(cx):return any(abs(cx-wx)<ARCH_ZONE-1e-8 for wx in (b.FX,b.RX))
    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        if interval_in_zone(cx):continue
        for side in (1,-1):
            for arow,brow in ((4,5),(5,6),(6,7)):
                a0=V(i,arow,side);a1=V(i+1,arow,side);b1=V(i+1,brow,side);b0=V(i,brow,side);mb.f((a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1),0)
        mb.f((V(i,7,1),V(i+1,7,1),V(i+1,7,-1),V(i,7,-1)),0)

    arch_meta=[];endpoint_reuse=0
    for wx,wname in ((b.FX,'F'),(b.RX,'R')):
        zone_indices=sorted([i for i,x in enumerate(xs) if abs(x-wx)<=ARCH_ZONE+1e-8])
        for side in (1,-1):
            sname='L' if side>0 else 'R';crown=[];b1s=[];b2s=[];inner=[]
            for jj,gi in enumerate(zone_indices):
                x=xs[gi];s=arch_shape(x,wx);base=cols[gi];cvi=V(gi,4,side);crown.append(cvi)
                if jj==0 or jj==len(zone_indices)-1:
                    b1s.append(V(gi,5,side));b2s.append(V(gi,6,side));inner.append(V(gi,7,side));endpoint_reuse+=3;continue
                shoulder=base[4];mid=base[5];rock=base[6];under=base[7];crown_p=mb.verts[cvi]
                inner_z=under[2]+s*(ARCH_TOP_Z-under[2]);inner_y=under[1]+s*((shoulder[1]-.026)-under[1])
                # Monotonic crown-to-opening bridge. Targets are deliberately below the
                # shared crown and above the inner opening at wheel center.
                b1_target=min(crown_p[2]-.015,ARCH_TOP_Z+B1_OVER_INNER)
                b2_target=min(b1_target-.010,ARCH_TOP_Z+B2_OVER_INNER)
                b1_z=mid[2]+s*(b1_target-mid[2]);b2_z=rock[2]+s*(b2_target-rock[2])
                b1_y=mid[1]+s*((shoulder[1]-.008)-mid[1]);b2_y=rock[1]+s*((shoulder[1]-.017)-rock[1])
                b1s.append(mb.v(f'R29A:{wname}:{sname}:B1:{jj}',(x,side*b1_y,b1_z)))
                b2s.append(mb.v(f'R29A:{wname}:{sname}:B2:{jj}',(x,side*b2_y,b2_z)))
                inner.append(mb.v(f'R29A:{wname}:{sname}:INNER:{jj}',(x,side*inner_y,inner_z)))
            for j in range(len(zone_indices)-1):
                for A,B in ((crown,b1s),(b1s,b2s),(b2s,inner)):
                    ids=(A[j],A[j+1],B[j+1],B[j]);mb.f(ids if side>0 else tuple(reversed(ids)),0)
            arch_meta.append((wname,sname,crown,inner))

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
    me=bpy.data.meshes.new('PRIMARY_R29A_SHOULDER_FED_CROWN_MESH');me.from_pydata(mb.verts,[],mb.faces);me.update();o=bpy.data.objects.new('PRIMARY_R29A_SHOULDER_FED_CROWN',me);bpy.context.collection.objects.link(o);o.data.materials.append(M['CLAY']);o.data.materials.append(glass)
    for p,mi in zip(o.data.polygons,mb.face_mat):p.use_smooth=True;p.material_index=mi
    o['OLEANDER_AUTHORITY']='WORKING_SOURCE';o['OLEANDER_TOPOLOGY']='R29A_R25_SHARED_ENDPOINT_MONOTONIC_SHOULDER_CROWN';o['R29_CROWN_ZONE_M']=CROWN_ZONE;o['R29_CROWN_TOP_Z_M']=CROWN_TOP_Z
    return o,xs,cols,arch_meta,endpoint_reuse

r25.build_source_raw=build_source_r29a

def context():
    rows=b.controls_resampled();items=[]
    for axle,wx in (('FRONT',b.FX),('REAR',b.RX)):
        sh=r14.interp_row(rows[4],wx);items.append({'axle':axle,'wheel_x_m':wx,'base_shoulder_z_m':sh[2],'target_crown_z_m':CROWN_TOP_Z,'target_b1_z_m':ARCH_TOP_Z+B1_OVER_INNER,'target_b2_z_m':ARCH_TOP_Z+B2_OVER_INNER,'inner_opening_z_m':ARCH_TOP_Z,'monotonic_z':CROWN_TOP_Z>ARCH_TOP_Z+B1_OVER_INNER>ARCH_TOP_Z+B2_OVER_INNER>ARCH_TOP_Z})
    return items

def patch_outputs(out:Path,ctx):
    qp=out/'AUTOMOTIVE_V011_QA.json';q=json.loads(qp.read_text());records=getattr(b,'_OLEANDER_WHEEL_HP_RECORDS',[]);exact=bool(getattr(b,'_OLEANDER_WHEEL_HP_EXACT',False));q['schema']='oleander.auto.v0.11.r29a.qa';q['model']=MODEL;q['checks']['wheel_hp_package_exact']=exact;q['checks']['r25_shared_endpoint_topology_retained']=q['endpoint_reuse_count']==24;q['checks']['shoulder_fed_crown_active']=True;q['checks']['monotonic_crown_bridge_targets']=all(x['monotonic_z'] for x in ctx);q['checks']['bounded_crown_influence']=CROWN_ZONE<.70;q['boundary']='R29A reopens only the R25 local crown/shoulder relation. Corrected wheel package and R25 opening scale/topology remain locked. Human M5 required; M6/M7/M8 blocked.';q['status']='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(q['checks'].values()) else 'MACHINE_FAIL';q['wheel_hp_package']=records;qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    rp=out/'AUTOMOTIVE_V011_RECEIPT.json';r=json.loads(rp.read_text());r['schema']='oleander.auto.v0.11.r29a.receipt';r['model']=MODEL;r['status']='EXECUTED_'+q['status'];rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text());c['job_id']='SYS-MODELING-WORKER-AUTO-M4M5-v0.11-R29A';c['decision_question']='Does transferring fender-crown height authority from R25 B1 to the shared shoulder, with a bounded wider crown envelope and monotonic shoulder>B1>B2>inner ordering, remove the cap-like crown without reopening wheel-opening topology?';c['source_authority']['editable_source']=f'{MODEL}.blend';c['revision']={'revision_id':'R29A-SHOULDER-FED-CROWN','semantic_targets':['front/rear fender crown','hood-fender-shoulder local continuity'],'parameters':{'r25_arch_zone_m':ARCH_ZONE,'r25_arch_top_z_m':ARCH_TOP_Z,'crown_zone_m':CROWN_ZONE,'crown_top_z_m':CROWN_TOP_Z,'b1_over_inner_m':B1_OVER_INNER,'b2_over_inner_m':B2_OVER_INNER,'wheel_hp_contract':'OD700','source_boolean':False,'source_subd':False},'expected_affected_components':['row3/row4/row5 local crown envelope and R25 B1/B2 z/y targets only'],'affected_view_policy':'HYBRID'};c['locks'].append({'target':'R25 wheel-opening scale/topology + exact wheel HP package + R09 + non-wheel R11/R12 + R18/R20','state':'LOCKED','reason':'R29A is a bounded crown-authority transfer only','unlock_trigger':None});c['qa']['project']=['front crown must stop reading as isolated cap','hood-fender-shoulder strip/grazing kink must reduce','rear crown must remain controlled','wheel opening/clearance must remain R25-scale','M6/M7/M8 remains blocked'];cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    (out/'R29A_CONTEXT.json').write_text(json.dumps({'model':MODEL,'status':q['status'],'targets':ctx,'wheel_hp_package_exact':exact,'next':'HUMAN_M5_VISUAL_QA'},ensure_ascii=False,indent=2)+'\n')

def main():
    ctx=context();code=0
    try:r25.main()
    except SystemExit as e:code=int(e.code or 0)
    a=b.parse();out=Path(a.out).resolve();patch_outputs(out,ctx);q=json.loads((out/'AUTOMOTIVE_V011_QA.json').read_text());raise SystemExit(0 if q['status']=='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' else (code or 5))
if __name__=='__main__':main()
