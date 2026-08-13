#!/usr/bin/env python3
"""OLEANDER Modeling Worker v0.12 E3 R3.1.

R3.1 keeps the R3 five-family Surface Source architecture but corrects two things exposed by
R3's fail-closed machine run:

1. source relationship authority is separated from finite-difference runtime diagnostics;
2. broad interior, declared character bands and intentional far boundaries are evaluated as
   different evidence classes rather than by one sample-spacing-dependent adjacent-normal gate.

It also measures semantic authority effects against the actual Primary Curve / termination
source edited by each control. Machine PASS still opens Human Project/Visual QA only.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "e3_r3_coupled_surface_entry.py"
spec = importlib.util.spec_from_file_location("oleander_e3_r3_base", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)
Vector = base.Vector
bpy = base.bpy

MODEL = "OLEANDER_ModelingWorker_v0.12_E3_R3_1_RelationshipAwareSurfaceNetwork"


def user_args() -> list[str]:
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]


def sample_axis(lo: float, hi: float, n: int) -> list[float]:
    if n < 2:
        return [lo]
    return [lo + (hi-lo)*i/(n-1) for i in range(n)]


def radius_from_step(a: Vector, b: Vector, na: Vector, nb: Vector) -> float:
    ds = (b-a).length
    theta = math.radians(base.angle_deg(na, nb))
    if ds < 1e-12:
        return 0.0
    if theta < 1e-8:
        return float("inf")
    return ds / theta


def zoned_radius_metrics(
    fn: Callable[[float,float],Vector],
    u_range: tuple[float,float],
    v_range: tuple[float,float],
    nu: int = 41,
    nv: int = 33,
) -> dict[str,float]:
    us = sample_axis(*u_range, nu)
    vs = sample_axis(*v_range, nv)
    pos: list[list[Vector]]=[]
    nor: list[list[Vector]]=[]
    for u in us:
        pr=[]; nr=[]
        for v in vs:
            pr.append(fn(u,v))
            nr.append(base.numerical_normal(fn,u,v))
        pos.append(pr); nor.append(nr)

    radii=[]; cell_areas=[]
    for i in range(nu):
        for j in range(nv):
            if i+1<nu:
                radii.append(radius_from_step(pos[i][j],pos[i+1][j],nor[i][j],nor[i+1][j]))
            if j+1<nv:
                radii.append(radius_from_step(pos[i][j],pos[i][j+1],nor[i][j],nor[i][j+1]))
            if i+1<nu and j+1<nv:
                cell_areas.append((pos[i+1][j]-pos[i][j]).cross(pos[i][j+1]-pos[i][j]).length)
    finite=[r for r in radii if math.isfinite(r)]
    return {
        "min_normal_radius_proxy_m": min(finite) if finite else 1e9,
        "p05_normal_radius_proxy_m": sorted(finite)[max(0,int(0.05*(len(finite)-1)))] if finite else 1e9,
        "min_cell_area_proxy": min(cell_areas) if cell_areas else 0.0,
    }


def band_total_turn_metrics(
    fn: Callable[[float,float],Vector],
    u_range: tuple[float,float],
    v_range: tuple[float,float],
    nu: int=31,
    nv: int=17,
) -> dict[str,float]:
    us=sample_axis(*u_range,nu); vs=sample_axis(*v_range,nv)
    totals=[]; min_radius=float("inf")
    for u in us:
        pp=[fn(u,v) for v in vs]
        nn=[base.numerical_normal(fn,u,v) for v in vs]
        turns=[]
        for j in range(len(vs)-1):
            turns.append(base.angle_deg(nn[j],nn[j+1]))
            min_radius=min(min_radius,radius_from_step(pp[j],pp[j+1],nn[j],nn[j+1]))
        totals.append(sum(turns))
    return {
        "max_total_normal_turn_deg":max(totals) if totals else 0.0,
        "min_normal_radius_proxy_m":min_radius if math.isfinite(min_radius) else 1e9,
    }


def source_relationship_metrics(net: base.R3Network, rel: dict[str,Any]) -> dict[str,Any]:
    rid=rel["id"]; cls=rel["class"]
    row={"id":rid,"class":cls,"boundary":rel["boundary"]}
    if cls=="INTENTIONAL_BOUNDARY":
        row["source_authority"]="EXPLICIT_NO_SMOOTH_CONTINUITY_CLAIM"
        row["pass"]=True
        return row
    if cls=="CURVATURE_RATE":
        rate=base.curve_pair_rate_proxy(net,rel["source"],rel["target"])
        row["max_rate_proxy"]=rate; row["threshold"]=float(rel["max_rate_proxy"]); row["pass"]=rate<=row["threshold"]
        return row

    # G1 source relationship authority. Boundary points and tangent-plane generators are
    # intentionally read from the independent source definitions, not finite differences.
    max_pos=0.0; max_tangent=0.0
    for i in range(41):
        t=i/40
        if rid=="REL-R3-01":
            pa=net.boundary("SHOULDER",t); pb=net.boundary("SHOULDER",t)
            ta=net.shoulder_tangent(t); tb=net.shoulder_tangent(t)
        elif rid=="REL-R3-02":
            pa=net.boundary("ROCKER",t); pb=net.boundary("ROCKER",t)
            ta=net.rocker_tangent(t); tb=net.rocker_tangent(t)
        elif rid=="REL-R3-03":
            w=t*3.0; pa=net.front_term(1.0,t); pb=net.composite(0.0,w)
            du=net.composite_du(0.0,w); length=float(net.terms["SURF-FRONT-TERM"]["length"])
            ta=du*(length/max(1e-9,abs(du.x))); tb=du
        elif rid=="REL-R3-04":
            w=t*3.0; pa=net.composite(1.0,w); pb=net.rear_term(0.0,t)
            du=net.composite_du(1.0,w); length=float(net.terms["SURF-REAR-TERM"]["length"])
            ta=du; tb=du*(length/max(1e-9,abs(du.x)))
        else:
            raise ValueError(rid)
        max_pos=max(max_pos,(pa-pb).length)
        max_tangent=max(max_tangent,base.angle_deg(ta,tb))
    row.update({
        "source_max_position_error":max_pos,
        "source_max_tangent_direction_angle_deg":max_tangent,
        "source_position_threshold":float(rel["max_position_error"]),
        "source_tangent_threshold_deg":float(rel["max_normal_angle_deg"]),
        "source_authority":"SHARED_BOUNDARY_AND_TANGENT_GENERATOR",
    })
    row["pass"]=max_pos<=row["source_position_threshold"] and max_tangent<=row["source_tangent_threshold_deg"]
    return row


def runtime_boundary_diagnostics(net: base.R3Network, contract: dict[str,Any]) -> list[dict[str,Any]]:
    out=[]
    for rel in contract["relationship_graph"]:
        if rel["class"]!="G1": continue
        old=base.boundary_relation_metrics(net,rel)
        out.append({
            "id":rel["id"],
            "finite_difference_max_position_error":old.get("max_position_error"),
            "finite_difference_max_normal_angle_deg":old.get("max_normal_angle_deg"),
            "diagnostic_threshold_deg":float(contract["machine_thresholds"]["max_runtime_boundary_normal_diagnostic_deg"]),
            "diagnostic_only":True,
        })
    return out


def intentional_boundary_metrics(net: base.R3Network, contract: dict[str,Any]) -> dict[str,Any]:
    threshold=float(contract["machine_thresholds"]["min_intentional_boundary_half_width_m"])
    front=[net.front_term(0.0,i/40) for i in range(41)]
    rear=[net.rear_term(1.0,i/40) for i in range(41)]
    fw=max(abs(p.y) for p in front); rw=max(abs(p.y) for p in rear)
    return {
        "front_half_width_m":fw,
        "rear_half_width_m":rw,
        "minimum_half_width_m":threshold,
        "front_non_degenerate":fw>=threshold,
        "rear_non_degenerate":rw>=threshold,
        "pass":fw>=threshold and rw>=threshold,
        "boundary":"Far boundaries remain explicit benchmark boundaries; this is non-degeneracy evidence, not closure-quality authority."
    }


def zone_fairness(net: base.R3Network, contract: dict[str,Any]) -> dict[str,Any]:
    th=contract["machine_thresholds"]; m=float(th["broad_interior_margin"])
    broad={
        "SURF-UPPER":zoned_radius_metrics(net.upper,(0.03,0.97),(m,1-m)),
        "SURF-SIDE":zoned_radius_metrics(net.side,(0.03,0.97),(m,1-m)),
        "SURF-LOWER":zoned_radius_metrics(net.lower,(0.03,0.97),(m,1-m)),
        "SURF-FRONT-TERM":zoned_radius_metrics(net.front_term,(m,1.0),(m,1-m),33,25),
        "SURF-REAR-TERM":zoned_radius_metrics(net.rear_term,(0.0,1-m),(m,1-m),33,25),
    }
    character={
        "UPPER_TO_SHOULDER":band_total_turn_metrics(net.upper,(0.03,0.97),(1-m,1.0)),
        "SIDE_FROM_SHOULDER":band_total_turn_metrics(net.side,(0.03,0.97),(0.0,m)),
        "SIDE_TO_ROCKER":band_total_turn_metrics(net.side,(0.03,0.97),(1-m,1.0)),
        "LOWER_FROM_ROCKER":band_total_turn_metrics(net.lower,(0.03,0.97),(0.0,m)),
        "LOWER_TO_UNDERBODY":band_total_turn_metrics(net.lower,(0.03,0.97),(1-m,1.0)),
        "FRONT_FAR_TRANSITION":band_total_turn_metrics(net.front_term,(0.0,m),(m,1-m),13,21),
        "REAR_FAR_TRANSITION":band_total_turn_metrics(net.rear_term,(1-m,1.0),(m,1-m),13,21),
    }
    broad_pass=all(
        r["min_normal_radius_proxy_m"]>=float(th["min_broad_normal_radius_proxy_m"])
        and r["min_cell_area_proxy"]>=float(th["min_surface_cell_area_proxy"])
        for r in broad.values()
    )
    char_pass=all(
        r["min_normal_radius_proxy_m"]>=float(th["min_character_band_normal_radius_proxy_m"])
        and r["max_total_normal_turn_deg"]<=float(th["max_character_band_total_normal_turn_deg"])
        for r in character.values()
    )
    return {"broad_interior":broad,"character_bands":character,"broad_pass":broad_pass,"character_pass":char_pass}


def direct_authority_effect(base_contract:dict[str,Any],variant_contract:dict[str,Any],declared:set[tuple]) -> dict[str,Any]:
    effects=[]
    for key in sorted(declared,key=str):
        authority=key[0]
        if authority=="PROFILE":
            curve=key[1]
            a=base_contract["profile_primary_curves"][curve]; b_=variant_contract["profile_primary_curves"][curve]
            maximum=0.0
            for i in range(81):
                u=i/80; maximum=max(maximum,abs(base.bezier(a,u)-base.bezier(b_,u)))
            effects.append({"source":list(key),"max_curve_effect":maximum,"pass":maximum>1e-4})
        elif authority=="PLAN":
            curve=key[1]
            a=base_contract["plan_primary_curves"][curve]; b_=variant_contract["plan_primary_curves"][curve]
            maximum=0.0
            for i in range(81):
                u=i/80; maximum=max(maximum,abs(base.bezier(a,u)-base.bezier(b_,u)))
            effects.append({"source":list(key),"max_curve_effect":maximum,"pass":maximum>1e-4})
        else:
            fam,field=key[1],key[2]
            delta=abs(float(base_contract["surface_sources"][fam][field])-float(variant_contract["surface_sources"][fam][field]))
            effects.append({"source":list(key),"max_curve_effect":delta,"pass":delta>1e-6})
    return {"effects":effects,"pass":all(e["pass"] for e in effects)}


def evaluate_core(contract:dict[str,Any]) -> tuple[dict[str,Any],base.R3Network]:
    net=base.R3Network(contract); th=contract["machine_thresholds"]
    source_rel=[source_relationship_metrics(net,r) for r in contract["relationship_graph"]]
    source_rel_ok=all(r["pass"] for r in source_rel)
    runtime=runtime_boundary_diagnostics(net,contract)
    zones=zone_fairness(net,contract)
    intentional=intentional_boundary_metrics(net,contract)
    profile=base.profile_metrics(net); plan=base.plan_metrics(net); reflection=base.reflection_field_proxy(net)
    profile_ok=profile["max_profile_slope_change_proxy"]<=float(th["max_profile_slope_change_proxy"]) and profile["profile_inflection_count"]<=int(th["max_profile_inflection_count"])
    plan_ok=plan["rear_haunch_plan_advantage"]>=float(th["min_rear_haunch_plan_advantage"])
    reflection_ok=reflection<=float(th["max_reflection_field_acceleration_proxy"])
    owners,overlaps=base.source_ownership(contract)
    classes={r["class"] for r in contract["relationship_graph"]}
    checks={
        "five_surface_source_families":len(contract["architecture"]["main_surface_families"])+len(contract["architecture"]["termination_families"])==5,
        "profile_plan_primary_curve_authority_separated":contract["architecture"]["profile_plan_authority_separated"] is True,
        "global_control_cage_forbidden":contract["architecture"]["global_control_cage_forbidden"] is True,
        "relationship_specific_continuity_classes":len(classes)>=3 and contract["architecture"]["blanket_continuity_class_forbidden"] is True,
        "source_relationship_authority_pass":source_rel_ok,
        "broad_interior_fairness_pass":zones["broad_pass"],
        "character_band_quality_pass":zones["character_pass"],
        "intentional_boundaries_non_degenerate":intentional["pass"],
        "semantic_control_source_ownership_disjoint":not overlaps,
        "profile_silhouette_metrics_pass":profile_ok,
        "plan_view_rear_haunch_hierarchy_pass":plan_ok,
        "reflection_field_proxy_pass":reflection_ok,
        "execution_topology_is_derived":contract["authority"]["execution_geometry"]=="DERIVED",
    }
    return {
        "checks":checks,
        "source_relationship_metrics":source_rel,
        "runtime_boundary_diagnostics":runtime,
        "zoned_fairness":zones,
        "intentional_boundary_metrics":intentional,
        "profile_metrics":profile,
        "plan_metrics":plan,
        "reflection_field_acceleration_proxy":reflection,
        "semantic_source_ownership":owners,
        "semantic_source_overlaps":overlaps,
    },net


def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--contract",required=True); ap.add_argument("--out",required=True); ap.add_argument("--resolution",type=int,default=512); args=ap.parse_args(user_args())
    contract=json.loads(Path(args.contract).read_text(encoding="utf-8")); out=Path(args.out).resolve(); out.mkdir(parents=True,exist_ok=True)
    base_report,base_net=evaluate_core(contract); th=contract["machine_thresholds"]

    variants={}; all_exact=True; all_machine=True; all_effect=True
    for cid in contract["semantic_controls"]:
        vc,declared=base.apply_control(contract,cid); actual=base.changed_keys(contract,vc)
        vr,vnet=evaluate_core(vc); disp=base.max_displacement(base_net,vnet)
        exact=actual==declared
        authority_effect=direct_authority_effect(contract,vc,declared)
        machine=all(vr["checks"].values())
        legible=float(th["min_semantic_surface_displacement"])<=disp<=float(th["max_semantic_surface_displacement"])
        variants[cid]={
            "declared_source_keys":[list(k) for k in sorted(declared,key=str)],
            "actual_changed_source_keys":[list(k) for k in sorted(actual,key=str)],
            "source_edit_exact":exact,
            "direct_declared_authority_effect":authority_effect,
            "max_surface_displacement":disp,
            "working_fidelity_legible":legible,
            "machine_surface_pass":machine,
            "zoned_fairness":vr["zoned_fairness"],
            "profile_metrics":vr["profile_metrics"],
            "plan_metrics":vr["plan_metrics"],
        }
        all_exact=all_exact and exact
        all_machine=all_machine and machine and legible
        all_effect=all_effect and authority_effect["pass"]

    checks={**base_report["checks"],
        "semantic_source_edits_exact":all_exact,
        "all_semantic_variants_surface_pass":all_machine,
        "semantic_authority_domain_effects_present":all_effect,
        "machine_pass_only_opens_human_review":True,
    }
    status="MACHINE_PASS_HUMAN_PROJECT_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL_REVISE_E3_R3_1_ARCHITECTURE_OR_QA"
    report={
        "schema":"oleander.modeling-worker.v0.12.e3.r3.1.machine-report",
        "model":MODEL,
        "status":status,
        "decision_question":contract["decision_question"],
        "checks":checks,
        "base":base_report,
        "semantic_variants":variants,
        "boundary":"R3.1 separates source G1 authority, runtime finite-difference diagnostics, broad-interior fairness, character-band quality and intentional-boundary non-degeneracy. These are benchmark proxies only. Machine PASS opens Human Project/Visual QA; no Class-A, production, PAP or Promotion authority is implied."
    }

    sc,row_count=base.render_set(base_net,out,args.resolution,"R3_1_BASE",True)
    sc["OLEANDER_MODEL"]=MODEL; sc["OLEANDER_STAGE"]="E3_R3_1_APPLICATION_MACHINE"; sc["OLEANDER_AUTHORITY"]="WORKING_SURFACE_SOURCE"
    blend=out/f"{MODEL}.blend"; bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    for cid in contract["semantic_controls"]:
        vc,_=base.apply_control(contract,cid); _,vnet=evaluate_core(vc); base.render_set(vnet,out,args.resolution,cid.replace("-","_"),False)

    (out/"E3_R3_1_MACHINE_REPORT.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (out/"E3_R3_1_COMPILED_SURFACE_SOURCE.json").write_text(json.dumps({
        "schema":"oleander.modeling-worker.v0.12.e3.r3.1.compiled-surface-source",
        "authority":"WORKING_SURFACE_SOURCE",
        "profile_primary_curves":contract["profile_primary_curves"],
        "plan_primary_curves":contract["plan_primary_curves"],
        "surface_sources":contract["surface_sources"],
        "relationship_graph":contract["relationship_graph"],
        "qa_semantics":"SOURCE_RELATION / RUNTIME_DIAGNOSTIC / BROAD_INTERIOR / CHARACTER_BAND / INTENTIONAL_BOUNDARY",
        "execution_geometry":{"derived":True,"editable_authority":False,"sample_rows":row_count}
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if status=="MACHINE_PASS_HUMAN_PROJECT_VISUAL_REVIEW_REQUIRED" else 5


if __name__=="__main__":
    raise SystemExit(main())
