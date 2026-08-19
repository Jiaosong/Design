#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, json, re
from jsonschema import Draft202012Validator

PH = re.compile(r"^\s*<[^>]*(REQUIRED|SET|ENTER|DEFINE|PROJECT|RUN)[^>]*>\s*$", re.I)
STAGE = {f"M{i}": i for i in range(11)}

def real(v):
    return isinstance(v,str) and bool(v.strip()) and not PH.match(v)

def ids(c):
    return {
      "hard_points":[x.get("id") for x in c.get("hard_points",{}).get("items",[])],
      "envelopes":[x.get("id") for x in c.get("envelopes",{}).get("items",[])],
      "sections":[x.get("id") for x in c.get("sections",{}).get("items",[])],
      "primary_geometry":[x.get("id") for x in c.get("primary_geometry",[])],
      "semantic_components":[x.get("id") for x in c.get("semantic_components",[])],
    }

def semantic(c, mode):
    strict=mode=="strict"; e=[]; w=[]
    if strict:
        for k in ("job_id","decision_question","exit_condition"):
            if not real(c.get(k)): e.append(f"{k}:required_real_value")
    for k in ("hard_points","envelopes","sections"):
        b=c.get(k,{})
        if strict and b.get("applicable") is True and not b.get("items"): e.append(f"{k}:applicable_but_empty")
        if strict and b.get("applicable") is False and not real(b.get("not_applicable_reason")): e.append(f"{k}:not_applicable_requires_reason")
    a=c.get("source_authority",{})
    if strict and a.get("state")!="NONE" and not real(a.get("editable_source")): e.append("source_authority:editable_source_required_when_authority_exists")
    n=STAGE.get(c.get("modeling_stage"),-1)
    if strict and n>=4 and not c.get("primary_geometry"): e.append("primary_geometry:required_at_M4_plus")
    if strict and n>=6 and not c.get("semantic_components"): e.append("semantic_components:required_at_M6_plus")
    if strict and n>=9 and not c.get("material_bindings"): e.append("material_bindings:required_at_M9_plus")
    recommended={"F0_PREFLIGHT":range(0,4),"F1_DESIGN_VALIDATION":range(4,7),"F2_PROMOTION":range(5,11),"F3_PRESENTATION":range(9,11)}
    f=c.get("fidelity")
    if strict and f in recommended and n not in recommended[f]: w.append(f"fidelity_stage_review:{f}/{c.get('modeling_stage')}")
    b=ids(c); flat=[]
    for k,v in b.items():
        r=[x for x in v if isinstance(x,str)]
        if len(r)!=len(set(r)): e.append(f"{k}:duplicate_id")
        flat+=r
    if len(flat)!=len(set(flat)): e.append("global_semantic_ids:not_unique")
    known=set(flat); sec_ids=set(b["sections"]); comp_ids=set(b["semantic_components"])
    for s in c.get("sections",{}).get("items",[]):
        for d in s.get("depends_on",[]):
            if d not in known: e.append(f"section:{s.get('id')}:unknown_dependency:{d}")
    for p in c.get("primary_geometry",[]):
        for s in p.get("source_sections",[]):
            if s not in sec_ids: e.append(f"primary_geometry:{p.get('id')}:unknown_source_section:{s}")
    for x in c.get("semantic_components",[]):
        p=x.get("parent")
        if p is not None and p not in comp_ids: e.append(f"component:{x.get('id')}:unknown_parent:{p}")
    for d in c.get("dependencies",[]):
        if d.get("from") not in known: e.append(f"dependency:unknown_from:{d.get('from')}")
        if d.get("to") not in known: e.append(f"dependency:unknown_to:{d.get('to')}")
    for m in c.get("material_bindings",[]):
        if m.get("target_component") not in comp_ids: e.append(f"material_binding:unknown_target_component:{m.get('target_component')}")
    if strict:
        q=c.get("qa",{})
        for k in ("integrity","construction","design_geometry","project"):
            if not q.get(k): e.append(f"qa:{k}:empty")
        if c.get("cache",{}).get("enabled") is True and not c.get("cache",{}).get("key_inputs"): e.append("cache:enabled_requires_key_inputs")
        if c.get("promotion",{}).get("decision") is None: e.append("promotion:decision_required")
    if c.get("promotion",{}).get("worker_may_mutate_source_authority") is not False: e.append("promotion:worker_may_mutate_source_authority_must_be_false")
    if c.get("persistence",{}).get("policy")=="PROMOTION_ONLY" and c.get("persistence",{}).get("artifact_registry") is not True: e.append("persistence:promotion_only_requires_artifact_registry")
    return e,w

def main():
    p=argparse.ArgumentParser(); p.add_argument("contract"); p.add_argument("--mode",choices=["strict","template"],default="strict"); p.add_argument("--schema",default=None); a=p.parse_args()
    cp=Path(a.contract); c=json.loads(cp.read_text(encoding="utf-8"))
    sp=Path(a.schema) if a.schema else Path(__file__).with_name("OLEANDER_Modeling_Contract_v0.2.schema.json")
    s=json.loads(sp.read_text(encoding="utf-8")); structural=[]
    for x in sorted(Draft202012Validator(s).iter_errors(c),key=lambda x:list(x.absolute_path)):
        loc=".".join(str(i) for i in x.absolute_path) or "$"; structural.append(f"{loc}:{x.message}")
    sem,w=semantic(c,a.mode); errors=structural+sem
    out={"schema":"oleander.modeling-contract.validation.v0.2.1","contract_version":c.get("contract_version"),"spec_patch":"v0.2.1","mode":a.mode,"status":"PASS" if not errors else "FAIL","structural_errors":structural,"semantic_errors":sem,"warnings":w}
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if not errors else 4

if __name__=="__main__": raise SystemExit(main())
