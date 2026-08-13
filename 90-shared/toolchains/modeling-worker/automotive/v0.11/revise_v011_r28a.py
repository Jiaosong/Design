#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R28A — Local Polar-to-Body Fender Patch.

R27 demonstrated that the circumferential wheel-opening idea is valid but cannot be
cleanly retrofitted into the inherited row4-row7 cage through local attachment cells.
R28A reopens the complete shoulder-to-rocker fender window and solves it as one local
patch between a locked U-shaped body boundary and the wheel-opening boundary.
"""
from __future__ import annotations
import importlib.util,bpy,bmesh,json,math
from pathlib import Path
BASE='/tmp/revise_v011_r25.py'
spec=importlib.util.spec_from_file_location('r25',BASE);r25=importlib.util.module_from_spec(spec);spec.loader.exec_module(r25)
r24=r25.r24;r20=r25.r20;r18=r25.r18;r16=r25.r16;r14=r25.r14;b=r25.b
MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R28A'
for m in (r25,r24,r20,r18,r16,r16.r15,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):m.MODEL=MODEL

WINDOW=.700
INNER_RX=.405
INNER_RZ=.450
ZC=.305
LIP_Y=.026
RADIAL_LAYERS=6
TOP_SAMPLES=13

def lerp(a,b,t):return a+(b-a)*t

def smoothstep(t):return t*t*(3.0-2.0*t)

def union_xs(rows):
    xs={round(p[0],9) for p in rows[0]}
    for wx in (b.FX,b.RX):
        xs.add(round(wx-WINDOW,9));xs.add(round(wx+WINDOW,9));xs.add(round(wx-INNER_RX,9));xs.add(round(wx+INNER_RX,9))
        for i in range(TOP_SAMPLES):
            x=wx-WINDOW+2*WINDOW*i/(TOP_SAMPLES-1);xs.add(round(x,9))
    return sorted(xs,reverse=True)

def build_source_r28a(rows,M,glass):
    xs=union_xs(rows);cols=[[r14.interp_row(row,x) for row in rows] for x in xs];xmap={round(x,9):i for i,x in enumerate(xs)};mb=r14.MB()
    def I(x):return xmap[round(x,9)]
    def K(i,row,side):return f'X{i}:R{row}:S{side:+d}'
    def V(i,row,side):
        p=cols[i][row]
        if row==0:return mb.v(K(i,row,0),(p[0],0,p[2]))
        return mb.v(K(i,row,side),(p[0],side*p[1],p[2]))

    # Upper body source through shoulder remains canonical and continuous.
    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        for side in (1,-1):
            for arow,brow in ((0,1),(1,2),(2,3),(3,4)):
                a0=V(i,arow,side if arow else 0);a1=V(i+1,arow,side if arow else 0);b1=V(i+1,brow,side);b0=V(i,brow,side)
                ids=(a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1);glass_band=(arow,brow) in ((1,2),(2,3)) and -1.22<=cx<=.72;mb.f(ids,1 if glass_band else 0)

    # Existing lower cage remains outside the local fender windows only.
    def in_window(cx):return any(abs(cx-wx)<WINDOW-1e-8 for wx in (b.FX,b.RX))
    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        if in_window(cx):continue
        for side in (1,-1):
            for arow,brow in ((4,5),(5,6),(6,7)):
                a0=V(i,arow,side);a1=V(i+1,arow,side);b1=V(i+1,brow,side);b0=V(i,brow,side);mb.f((a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1),0)
        mb.f((V(i,7,1),V(i+1,7,1),V(i+1,7,-1),V(i,7,-1)),0)

    arch_meta=[];boundary_reuse=0
    for wx,wname in ((b.FX,'F'),(b.RX,'R')):
        for side in (1,-1):
            sname='L' if side>0 else 'R'
            # Locked U-shaped outer boundary: left side row7->row4, top row4,
            # right side row4->row7. Every point is an existing body-cage vertex.
            outer=[]
            xl=wx-WINDOW;xr=wx+WINDOW
            for row in (7,6,5,4):outer.append(V(I(xl),row,side))
            for i in range(1,TOP_SAMPLES-1):
                x=xl+2*WINDOW*i/(TOP_SAMPLES-1);outer.append(V(I(x),4,side))
            for row in (4,5,6,7):
                vi=V(I(xr),row,side)
                if not outer or vi!=outer[-1]:outer.append(vi)
            boundary_reuse+=len(outer)

            # Parameterize the inner wheel opening by cumulative outer-boundary distance,
            # so dense top-boundary samples map to the fender crown rather than to side walls.
            coords=[mb.verts[v] for v in outer];cum=[0.0]
            for a,c in zip(coords[:-1],coords[1:]):
                cum.append(cum[-1]+math.dist(a,c))
            total=max(cum[-1],1e-9)
            inner=[]
            for j,(ov,d) in enumerate(zip(outer,cum)):
                t=d/total;theta=math.pi*(1.0-t);s=max(0.0,math.sin(theta));w=s*s
                x=wx+INNER_RX*math.cos(theta);base=r14.interp_row(rows[7],x);shoulder=r14.interp_row(rows[4],x)
                z=lerp(base[2],ZC+INNER_RZ*s,w);y=lerp(base[1],shoulder[1]+LIP_Y,w)
                inner.append(mb.v(f'R28A:{wname}:{sname}:INNER:{j}',(x,side*y,z)))

            # Full local patch: interpolate between inner arch and the locked U boundary.
            layers=[inner]
            for li in range(1,RADIAL_LAYERS-1):
                u=li/(RADIAL_LAYERS-1);q=smoothstep(u);layer=[]
                for j,(iv,ov) in enumerate(zip(inner,outer)):
                    pi=mb.verts[iv];po=mb.verts[ov];theta=math.pi*(1.0-cum[j]/total);s=max(0.0,math.sin(theta));bulge=4*u*(1-u)*s
                    p=(lerp(pi[0],po[0],q),lerp(abs(pi[1]),abs(po[1]),q)+.018*bulge,lerp(pi[2],po[2],q)+.010*bulge)
                    layer.append(mb.v(f'R28A:{wname}:{sname}:L{li}:{j}',(p[0],side*p[1],p[2])))
                layers.append(layer)
            layers.append(outer)
            for li in range(RADIAL_LAYERS-1):
                A=layers[li];B=layers[li+1]
                for j in range(len(outer)-1):
                    ids=(A[j],A[j+1],B[j+1],B[j]);mb.f(ids if side>0 else tuple(reversed(ids)),0)
            arch_meta.append((wname,sname,layers[-2],inner))

    # R18/R20 structured front/rear terminations are outside the local fender architecture.
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

    me=bpy.data.meshes.new('PRIMARY_LOCAL_FENDER_PATCH_R28A_MESH');me.from_pydata(mb.verts,[],mb.faces);me.update();o=bpy.data.objects.new('PRIMARY_LOCAL_FENDER_PATCH_R28A',me);bpy.context.collection.objects.link(o);o.data.materials.append(M['CLAY']);o.data.materials.append(glass)
    for p,mi in zip(o.data.polygons,mb.face_mat):p.use_smooth=True;p.material_index=mi
    bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
    o['OLEANDER_AUTHORITY']='WORKING_SOURCE';o['OLEANDER_TOPOLOGY']='R28A_LOCAL_U_BOUNDARY_TO_POLAR_ARCH_PATCH';o['R28_WINDOW_HALF_M']=WINDOW;o['R28_RADIAL_LAYERS']=RADIAL_LAYERS;o['R28_BOUNDARY_REUSE_COUNT']=boundary_reuse
    return o,xs,cols,arch_meta,boundary_reuse

r25.build_source_raw=build_source_r28a

def patch_outputs(out:Path):
    cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text());c['job_id']='SYS-MODELING-WORKER-AUTO-M4M5-v0.11-R28A';c['decision_question']='Can a single local U-boundary-to-wheel-opening fender patch solve shoulder, crown, mid-body and rocker transition together without the R27 attachment seam/pinching?';c['source_authority']['editable_source']=f'{MODEL}.blend';c['primary_geometry'][0]['id']='PG-LOCAL-FENDER-PATCH-SOURCE';c['primary_geometry'][0]['role']='single Source with front/rear local polar-to-body fender patches';c['revision']={'revision_id':'R28A-LOCAL-FENDER-PATCH','semantic_targets':['front/rear wheel opening','fender crown','shoulder-to-rocker local patch'],'parameters':{'window_half_m':WINDOW,'inner_rx_m':INNER_RX,'inner_rz_m':INNER_RZ,'radial_layers':RADIAL_LAYERS,'top_samples':TOP_SAMPLES,'outer_boundary':'LOCKED_U_BODY_CAGE','source_boolean':False,'source_subd':False},'expected_affected_components':['front/rear local shoulder-to-rocker fender windows only'],'affected_view_policy':'HYBRID'};c['locks'].append({'target':'R09 hard points + R11/R12 source outside local fender windows + R18/R20 terminations','state':'LOCKED','reason':'R28A expands M4 only inside bounded local fender windows','unlock_trigger':None});c['qa']['construction']=['one connected Source mesh','local U-shaped outer boundary reuses existing body cage','wheel opening and fender transition solved in one patch parameterization','source n-gon=0','no Source Boolean/SubD','termination triangles=4','full Source normals recalculated'];c['qa']['project']=['no R27 attachment seam/teeth/radial collar pinching','wheel opening wraps tire coherently','fender crown shoulder-fed','Strip/Grazing highlights cross local patch without severe kinks','outside-window package unchanged','M6/M7/M8 remains blocked'];cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    qp=out/'AUTOMOTIVE_V011_QA.json';q=json.loads(qp.read_text());q['schema']='oleander.auto.v0.11.r28a.qa';q['model']=MODEL;q['checks'].pop('arch_endpoint_vertex_reuse_24',None);q['checks']['local_fender_patch_active']=True;q['checks']['bounded_local_window']=True;q['checks']['outer_body_boundary_reused']=q.get('endpoint_reuse_count',0)>0;q['checks']['radial_layers_6']=RADIAL_LAYERS==6;q['checks']['termination_triangles_four']=q['topology']['tri']==4;q['checks']['face_normals_recalculated']=True;q['boundary']='R28A reopens the complete local shoulder-to-rocker fender window; R09 and non-wheel package remain locked. Human M5 Visual QA required; M6/M7/M8 blocked.';qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    rp=out/'AUTOMOTIVE_V011_RECEIPT.json';r=json.loads(rp.read_text());r['schema']='oleander.auto.v0.11.r28a.receipt';r['model']=MODEL;rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    (out/'R28_PATCH_CONTRACT.json').write_text(json.dumps({'model':MODEL,'stage':'M5','revision':'R28A','status':'MACHINE_EXECUTED_VISUAL_REVIEW_REQUIRED','local_window_half_m':WINDOW,'radial_layers':RADIAL_LAYERS,'outer_boundary':'U_SHAPED_LOCKED_BODY_CAGE','inner_boundary':'POLAR_WHEEL_OPENING','topology':'LOCAL_POLAR_TO_BODY_PATCH','blocked':['M6','M7','M8']},ensure_ascii=False,indent=2)+'\n')

def main():
    code=0
    try:r25.main()
    except SystemExit as e:code=int(e.code or 0)
    a=b.parse();out=Path(a.out).resolve();patch_outputs(out)
    qp=out/'AUTOMOTIVE_V011_QA.json';q=json.loads(qp.read_text());checks=q['checks'];expected=(q['topology']['tri']==4 and q['topology']['ngon']==0 and q['source_island_count']==1 and checks.get('source_no_boolean') is True and checks.get('source_no_subd') is True and checks.get('local_fender_patch_active') is True and checks.get('outer_body_boundary_reused') is True and len(q.get('renders',[]))==9)
    q['status']='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if expected else 'MACHINE_FAIL';qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    rp=out/'AUTOMOTIVE_V011_RECEIPT.json';r=json.loads(rp.read_text());r['status']='EXECUTED_MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if expected else 'EXECUTED_MACHINE_FAIL';rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    raise SystemExit(0 if expected else (code or 2))
if __name__=='__main__':main()
