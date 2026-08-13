#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R12 — Shape-Preserving Hermite Surface Interpolation.

All R11 hard points and 22 transverse sections are LOCKED.
Only longitudinal interpolation changes:
piecewise-linear -> monotone shape-preserving cubic Hermite (PCHIP-like).
No section/control-point changes.
"""
from __future__ import annotations
import importlib.util,bpy,json,math
from pathlib import Path

BASE="/tmp/revise_v011_r11.py"
spec=importlib.util.spec_from_file_location("r11",BASE)
r11=importlib.util.module_from_spec(spec);spec.loader.exec_module(r11)
r10=r11.r10;r09=r11.r09;r08=r11.r08;b=r11.b

MODEL="OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R12"
r11.MODEL=MODEL;r10.MODEL=MODEL;r09.MODEL=MODEL;r08.MODEL=MODEL;r08.r.MODEL=MODEL;b.MODEL=MODEL

def pchip_derivatives(xs,vs):
    n=len(xs)
    if n<2:return [0.0]*n
    h=[xs[i+1]-xs[i] for i in range(n-1)]
    d=[(vs[i+1]-vs[i])/h[i] for i in range(n-1)]
    m=[0.0]*n
    if n==2:return [d[0],d[0]]
    m[0]=((2*h[0]+h[1])*d[0]-h[0]*d[1])/(h[0]+h[1])
    if m[0]*d[0] <= 0:m[0]=0.0
    elif abs(m[0]) > 3*abs(d[0]):m[0]=3*d[0]
    m[-1]=((2*h[-1]+h[-2])*d[-1]-h[-1]*d[-2])/(h[-1]+h[-2])
    if m[-1]*d[-1] <= 0:m[-1]=0.0
    elif abs(m[-1]) > 3*abs(d[-1]):m[-1]=3*d[-1]
    for i in range(1,n-1):
        if d[i-1]==0 or d[i]==0 or d[i-1]*d[i] <= 0:m[i]=0.0
        else:
            w1=2*h[i]+h[i-1];w2=h[i]+2*h[i-1]
            m[i]=(w1+w2)/(w1/d[i-1]+w2/d[i])
    return m

def hermite(x0,x1,v0,v1,m0,m1,x):
    h=x1-x0;t=(x-x0)/h
    h00=2*t**3-3*t**2+1;h10=t**3-2*t**2+t;h01=-2*t**3+3*t**2;h11=t**3-t**2
    return h00*v0+h10*h*m0+h01*v1+h11*h*m1

def pchip_resample(points,steps=4):
    asc=list(reversed(points));xs=[p[0] for p in asc];ys=[p[1] for p in asc];zs=[p[2] for p in asc]
    my=pchip_derivatives(xs,ys);mz=pchip_derivatives(xs,zs);out=[]
    for i in range(len(xs)-1):
        for j in range(steps):
            t=j/steps;x=xs[i]+(xs[i+1]-xs[i])*t
            y=hermite(xs[i],xs[i+1],ys[i],ys[i+1],my[i],my[i+1],x)
            z=hermite(xs[i],xs[i+1],zs[i],zs[i+1],mz[i],mz[i+1],x)
            out.append((x,y,z))
    out.append(asc[-1]);return list(reversed(out))

b.resample_list=pchip_resample

def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);b.clear();M=b.materials();rows=b.controls_resampled()
    source,ids,verts=r08.r.full_source_grid(rows,M);h0=r08.source_hash(source);derived=r08.build_closed_derived(rows,M);h1=r08.source_hash(source)
    glass=r10.semantic_glass_material();glass_faces=r10.assign_glazing_zone(derived,glass)
    b.wheels(M);G=b.guides(rows,M);b.ground(M);L=b.rigs();b.world((.012,.012,.012),.16)
    scene=bpy.context.scene;scene["OLEANDER_MODEL"]=MODEL;scene["OLEANDER_STAGE"]="M5";scene["OLEANDER_HARD_POINTS"]=json.dumps(b.HP)
    r08.r.b.write_contract(out);cp=out/"MODELING_CONTRACT.json";c=json.loads(cp.read_text())
    c["job_id"]="SYS-MODELING-WORKER-AUTO-M1M5-v0.11-R12";c["decision_question"]="With all R11 hard points and transverse section values locked, does shape-preserving Hermite interpolation improve surface flow while preserving the intended cowl/roof/backlight/shoulder control structure?"
    c["source_authority"]["editable_source"]=f"{MODEL}.blend";c["source_authority"]["derived_models"]=["DERIVED_CLOSED_BODY","MAT_SEMANTIC_GLAZING_DIAG"]
    c["sections"]["items"]=[{"id":f"SEC-{i:02d}","role":"R11 locked transverse section","station":s[0],"plane":"YZ","continuity_target":"LOCKED / PCHIP interpolation only","depends_on":["HP-WHEELBASE","HP-TRACK"],"status":"LOCKED"} for i,s in enumerate(b.SECTIONS)]
    c["primary_geometry"][0]["source_sections"]=[f"SEC-{i:02d}" for i in range(len(b.SECTIONS))]
    c["locks"].append({"target":"R11 hard points + all 22 section values","state":"LOCKED","reason":"R12 isolates interpolation/construction quality","unlock_trigger":"R12 visual QA identifies a genuine section failure"})
    c["revision"]={"revision_id":"R12-PCHIP-INTERPOLATION","semantic_targets":["PG-UNIFIED-GRID"],"parameters":{"longitudinal_interpolation":{"before":"piecewise-linear","after":"shape-preserving cubic Hermite/PCHIP-like"}},"expected_affected_components":["COMP-PRIMARY-GRID"],"affected_view_policy":"HYBRID"}
    c["qa"]["construction"]=["source grid remains quad-only","PCHIP is evaluated per longitudinal control row","local extrema force zero/interior-safe tangent and prevent overshoot","no global SubD/Catmull smoothing","wheel-arch body remains derived"]
    c["qa"]["project"]=["compare R11 vs R12 Clay Strip/Grazing/Silhouette","retain R11 proportions if PCHIP only improves flow","if PCHIP rounds away required cowl/backlight control, REJECT"]
    c["resource_budget"]["max_render_views"]=9;cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n")
    blend=out/f"{MODEL}.blend";bpy.ops.wm.save_as_mainfile(filepath=str(blend));R=r10.render_r10(out,a.samples,a.resolution,M,L,G,source,derived)
    mn,mx=b.bbox(source);checks={"source_hash_locked":h0==h1,"source_quad_only":all(len(p.vertices)==4 for p in source.data.polygons),"derived_manifold":r08.manifold(derived)==0,"glazing_zone_faces":glass_faces>100,"length":4.60<=mx.x-mn.x<=4.70,"width":1.80<=mx.y-mn.y<=1.94,"height":1.42<=mx.z<=1.47,"wheelbase":abs(b.FX-b.RX-2.82)<1e-8,"track":abs(2*b.WY-1.59)<1e-8,"section_count":len(b.SECTIONS)==22,"render_matrix":len(R)==9}
    q={"schema":"oleander.auto.v0.11.r12.qa","model":MODEL,"status":"MACHINE_PASS_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL","source_hash_before":h0,"source_hash_after":h1,"derived_nonmanifold_edges":r08.manifold(derived),"glazing_zone_face_count":glass_faces,"interpolation":"shape-preserving cubic Hermite/PCHIP-like","checks":checks,"renders":R,"boundary":"R12 changes interpolation only. R11 hard points/sections are unchanged; semantic glazing and wheel arches remain diagnostic."}
    (out/"AUTOMOTIVE_V011_QA.json").write_text(json.dumps(q,ensure_ascii=False,indent=2)+"\n");rec={"schema":"oleander.auto.v0.11.r12.receipt","model":MODEL,"blender_version":bpy.app.version_string,"build_hash":bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),"renderer":"Cycles CPU","samples":a.samples,"resolution":[a.resolution,a.resolution],"status":"EXECUTED_"+q["status"],"blend":str(blend),"qa":str(out/"AUTOMOTIVE_V011_QA.json"),"renders":R};(out/"AUTOMOTIVE_V011_RECEIPT.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n");print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if all(checks.values()) else 5)
if __name__=="__main__":main()
