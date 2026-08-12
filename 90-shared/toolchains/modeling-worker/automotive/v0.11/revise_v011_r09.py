#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R09 — Cabin Package Rearward Controlled Variant.

Controlled comparison against R08:
LOCKED: overall L/W/H, wheelbase, track, wheel OD, axle positions, body-side widths.
OPEN: cowl/A/roof/C longitudinal stations only.
Goal: test whether rearward cabin placement removes the remaining single-bubble proportion.
"""
from __future__ import annotations
import importlib.util,bpy,json
from pathlib import Path

BASE="/tmp/revise_v011_r08.py"
spec=importlib.util.spec_from_file_location("r08",BASE)
r08=importlib.util.module_from_spec(spec);spec.loader.exec_module(r08)
b=r08.b

MODEL="OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R09"
r08.MODEL=MODEL;r08.r.MODEL=MODEL;b.MODEL=MODEL

b.HP["cowl_x_m"]=.72;b.HP["cowl_z_m"]=.90;b.HP["roof_peak_x_m"]=-.24;b.HP["roof_peak_z_m"]=1.45
b.SECTIONS=[
 ( 2.325,.51,.24,.52,.31,.46,.40,.34,.45,.23,.36,.15,.30),( 2.22 ,.56,.34,.56,.42,.50,.51,.37,.57,.22,.46,.15,.37),
 ( 2.02 ,.64,.50,.63,.57,.56,.67,.40,.73,.205,.60,.145,.48),( 1.72 ,.72,.62,.70,.68,.63,.81,.43,.87,.19,.76,.14,.61),
 ( 1.465,.77,.66,.75,.74,.67,.90,.45,.92,.18,.83,.14,.67),( 1.20 ,.80,.67,.78,.77,.69,.92,.46,.93,.18,.85,.14,.69),
 ( .96  ,.83,.67,.81,.78,.71,.92,.47,.93,.18,.86,.14,.70),( .78  ,.86,.66,.83,.79,.72,.92,.48,.93,.18,.86,.14,.70),
 ( .72  ,.90,.64,.85,.79,.73,.92,.48,.93,.18,.86,.14,.70),( .52  ,1.09,.53,.86,.80,.74,.915,.48,.925,.18,.86,.14,.70),
 ( .28  ,1.29,.52,.86,.81,.75,.91,.48,.92,.18,.86,.14,.70),( .02  ,1.41,.54,.86,.81,.755,.91,.48,.92,.18,.86,.14,.70),
 (-.24  ,1.45,.56,.86,.81,.755,.91,.48,.92,.18,.86,.14,.70),(-.52  ,1.43,.55,.855,.81,.75,.91,.48,.92,.18,.86,.14,.70),
 (-.78  ,1.37,.52,.85,.80,.745,.91,.48,.92,.18,.86,.14,.70),(-1.02  ,1.27,.48,.84,.79,.73,.905,.47,.915,.18,.85,.14,.69),
 (-1.20  ,1.12,.50,.825,.78,.71,.90,.46,.91,.18,.84,.14,.68),(-1.355 ,.99,.58,.81,.77,.69,.90,.45,.91,.18,.83,.14,.67),
 (-1.62  ,.87,.63,.79,.75,.67,.88,.44,.90,.19,.80,.145,.64),(-1.88  ,.79,.60,.75,.70,.63,.83,.42,.86,.20,.73,.15,.58),
 (-2.10  ,.69,.49,.66,.59,.57,.70,.39,.75,.215,.60,.155,.47),(-2.325 ,.55,.27,.55,.35,.48,.45,.34,.50,.24,.40,.16,.32)]

def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);b.clear();M=b.materials();rows=b.controls_resampled()
    source,ids,verts=r08.r.full_source_grid(rows,M);h0=r08.source_hash(source);derived=r08.build_closed_derived(rows,M);h1=r08.source_hash(source)
    b.wheels(M);G=b.guides(rows,M);b.ground(M);L=b.rigs();b.world((.012,.012,.012),.16)
    scene=bpy.context.scene;scene["OLEANDER_MODEL"]=MODEL;scene["OLEANDER_STAGE"]="M5";scene["OLEANDER_HARD_POINTS"]=json.dumps(b.HP)
    r08.r.b.write_contract(out);cp=out/"MODELING_CONTRACT.json";c=json.loads(cp.read_text())
    c["job_id"]="SYS-MODELING-WORKER-AUTO-M1M5-v0.11-R09";c["decision_question"]="With overall package and wheel hard points locked, does moving only the cabin longitudinal control package rearward improve hood/cowl/cabin proportion and remove the remaining single-bubble reading?"
    c["source_authority"]["editable_source"]=f"{MODEL}.blend";c["source_authority"]["derived_models"]=["DERIVED_CLOSED_BODY"]
    c["sections"]["items"]=[{"id":f"SEC-{i:02d}","role":"transverse control station","station":s[0],"plane":"YZ","continuity_target":"R09 controlled cabin-position variant","depends_on":["HP-WHEELBASE","HP-TRACK"],"status":"OPEN"} for i,s in enumerate(b.SECTIONS)]
    c["primary_geometry"][0]["source_sections"]=[f"SEC-{i:02d}" for i in range(len(b.SECTIONS))]
    c["locks"].append({"target":"overall L/W/H + wheelbase/track/wheel OD + body-side width system","state":"LOCKED","reason":"controlled R08→R09 cabin-position comparison","unlock_trigger":None})
    c["revision"]={"revision_id":"R09-CABIN-REARWARD","semantic_targets":["HP-COWL","HP-ROOF","PG-UNIFIED-GRID"],"parameters":{"cowl_x":{"before":.93,"after":.72},"roof_peak_x":{"before":-.12,"after":-.24}},"expected_affected_components":["COMP-PRIMARY-GRID"],"affected_view_policy":"HYBRID"}
    c["qa"]["project"]=["compare R08 vs R09 at Side / Hero 3Q / Front / Top","no wheel/package hard point changed","if cabin shift improves Side but damages Front/Top, REJECT"];c["resource_budget"]["max_render_views"]=9
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n")
    blend=out/f"{MODEL}.blend";bpy.ops.wm.save_as_mainfile(filepath=str(blend));R=r08.render_r08(out,a.samples,a.resolution,M,L,G,source,derived)
    mn,mx=b.bbox(source);checks={"source_hash_locked":h0==h1,"source_quad_only":all(len(p.vertices)==4 for p in source.data.polygons),"derived_manifold":r08.manifold(derived)==0,"length":4.60<=mx.x-mn.x<=4.70,"width":1.80<=mx.y-mn.y<=1.92,"height":1.42<=mx.z<=1.47,"wheelbase":abs(b.FX-b.RX-2.82)<1e-8,"track":abs(2*b.WY-1.59)<1e-8,"section_count":len(b.SECTIONS)==22,"render_matrix":len(R)==9}
    q={"schema":"oleander.auto.v0.11.r09.qa","model":MODEL,"status":"MACHINE_PASS_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL","source_hash_before":h0,"source_hash_after":h1,"derived_nonmanifold_edges":r08.manifold(derived),"bounds":{"min":list(mn),"max":list(mx),"dimensions":[mx.x-mn.x,mx.y-mn.y,mx.z-mn.z]},"checks":checks,"renders":R,"boundary":"R09 is a controlled cabin-position design variant. No promotion unless comparative Visual QA beats R08."}
    (out/"AUTOMOTIVE_V011_QA.json").write_text(json.dumps(q,ensure_ascii=False,indent=2)+"\n");rec={"schema":"oleander.auto.v0.11.r09.receipt","model":MODEL,"blender_version":bpy.app.version_string,"build_hash":bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),"renderer":"Cycles CPU","samples":a.samples,"resolution":[a.resolution,a.resolution],"status":"EXECUTED_"+q["status"],"blend":str(blend),"qa":str(out/"AUTOMOTIVE_V011_QA.json"),"renders":R};(out/"AUTOMOTIVE_V011_RECEIPT.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n");print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if all(checks.values()) else 5)
if __name__=="__main__":main()
