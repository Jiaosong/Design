#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R11 — Transverse Section Tension Variant.

LOCKED from R09/R10:
- L/W/H, wheelbase, track, wheel OD, axle positions
- longitudinal cowl/A/roof/C stations
OPEN:
- transverse shoulder/mid/rocker widths and shoulder height only
Goal:
- establish shoulder crown + side undercut + rocker hierarchy.
"""
from __future__ import annotations
import importlib.util,bpy,json
from pathlib import Path

BASE="/tmp/revise_v011_r10.py"
spec=importlib.util.spec_from_file_location("r10",BASE)
r10=importlib.util.module_from_spec(spec);spec.loader.exec_module(r10)
r09=r10.r09;r08=r10.r08;b=r10.b

MODEL="OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R11"
r10.MODEL=MODEL;r09.MODEL=MODEL;r08.MODEL=MODEL;r08.r.MODEL=MODEL;b.MODEL=MODEL

def tune(s):
    x,tz,te,bz,bw,sz,sw,mz,mw,rz,rw,uz,uw=s
    if -1.70 <= x <= 1.70:
        sw=min(sw+.010,.93);sz+=.012;mw=max(mw-.030,.86);rw=max(rw-.020,.78)
    if abs(x-b.FX)<.08 or abs(x-b.RX)<.08:
        sw=max(sw,.92);mw=max(mw,.895);rw=max(rw,.82)
    return (x,tz,te,bz,bw,sz,sw,mz,mw,rz,rw,uz,uw)

b.SECTIONS=[tune(s) for s in b.SECTIONS]

def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);b.clear();M=b.materials();rows=b.controls_resampled()
    source,ids,verts=r08.r.full_source_grid(rows,M);h0=r08.source_hash(source);derived=r08.build_closed_derived(rows,M);h1=r08.source_hash(source)
    glass=r10.semantic_glass_material();glass_faces=r10.assign_glazing_zone(derived,glass)
    b.wheels(M);G=b.guides(rows,M);b.ground(M);L=b.rigs();b.world((.012,.012,.012),.16)
    scene=bpy.context.scene;scene["OLEANDER_MODEL"]=MODEL;scene["OLEANDER_STAGE"]="M5";scene["OLEANDER_HARD_POINTS"]=json.dumps(b.HP)
    r08.r.b.write_contract(out);cp=out/"MODELING_CONTRACT.json";c=json.loads(cp.read_text())
    c["job_id"]="SYS-MODELING-WORKER-AUTO-M1M5-v0.11-R11";c["decision_question"]="With R09 longitudinal package locked, does a controlled transverse shoulder/mid/rocker tension revision improve body-side hierarchy without destabilizing front/top/package proportions?"
    c["source_authority"]["editable_source"]=f"{MODEL}.blend";c["source_authority"]["derived_models"]=["DERIVED_CLOSED_BODY","MAT_SEMANTIC_GLAZING_DIAG"]
    c["sections"]["items"]=[{"id":f"SEC-{i:02d}","role":"R11 transverse-tension station","station":s[0],"plane":"YZ","continuity_target":"longitudinal positions locked / transverse tension revised","depends_on":["HP-WHEELBASE","HP-TRACK"],"status":"OPEN"} for i,s in enumerate(b.SECTIONS)]
    c["primary_geometry"][0]["source_sections"]=[f"SEC-{i:02d}" for i in range(len(b.SECTIONS))]
    c["locks"].append({"target":"R09 longitudinal cowl/A/roof/C package + all wheel/package hard points","state":"LOCKED","reason":"R11 isolates transverse section tension","unlock_trigger":None})
    c["revision"]={"revision_id":"R11-TRANSVERSE-TENSION","semantic_targets":["PG-UNIFIED-GRID"],"parameters":{"shoulder":"~+10mm/side +12mm z in main body","mid_body":"~30mm/side inward","rocker":"~20mm/side inward"},"expected_affected_components":["COMP-PRIMARY-GRID"],"affected_view_policy":"HYBRID"}
    c["qa"]["project"]=["compare R10 vs R11 Front / 3Q / Strip / Top","shoulder must gain hierarchy without pinching","no longitudinal package change","semantic glazing remains diagnostic only"];c["resource_budget"]["max_render_views"]=9;cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n")
    blend=out/f"{MODEL}.blend";bpy.ops.wm.save_as_mainfile(filepath=str(blend));R=r10.render_r10(out,a.samples,a.resolution,M,L,G,source,derived)
    mn,mx=b.bbox(source);checks={"source_hash_locked":h0==h1,"source_quad_only":all(len(p.vertices)==4 for p in source.data.polygons),"derived_manifold":r08.manifold(derived)==0,"glazing_zone_faces":glass_faces>100,"length":4.60<=mx.x-mn.x<=4.70,"width":1.80<=mx.y-mn.y<=1.94,"height":1.42<=mx.z<=1.47,"wheelbase":abs(b.FX-b.RX-2.82)<1e-8,"track":abs(2*b.WY-1.59)<1e-8,"section_count":len(b.SECTIONS)==22,"render_matrix":len(R)==9}
    q={"schema":"oleander.auto.v0.11.r11.qa","model":MODEL,"status":"MACHINE_PASS_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL","source_hash_before":h0,"source_hash_after":h1,"derived_nonmanifold_edges":r08.manifold(derived),"glazing_zone_face_count":glass_faces,"bounds":{"min":list(mn),"max":list(mx),"dimensions":[mx.x-mn.x,mx.y-mn.y,mx.z-mn.z]},"checks":checks,"renders":R,"boundary":"R11 changes only transverse section tension. Semantic glazing and wheel openings remain derived diagnostics; no M6/M7 authority."}
    (out/"AUTOMOTIVE_V011_QA.json").write_text(json.dumps(q,ensure_ascii=False,indent=2)+"\n");rec={"schema":"oleander.auto.v0.11.r11.receipt","model":MODEL,"blender_version":bpy.app.version_string,"build_hash":bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),"renderer":"Cycles CPU","samples":a.samples,"resolution":[a.resolution,a.resolution],"status":"EXECUTED_"+q["status"],"blend":str(blend),"qa":str(out/"AUTOMOTIVE_V011_QA.json"),"renders":R};(out/"AUTOMOTIVE_V011_RECEIPT.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n");print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if all(checks.values()) else 5)
if __name__=="__main__":main()
