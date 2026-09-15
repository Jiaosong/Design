#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
REGISTRY = RUNTIME / "OLEANDER_TYPED_SYSTEM_VALIDATOR_RULE_REGISTRY_v0.1.json"
EVALS = RUNTIME / "OLEANDER_TYPED_SYSTEM_REGRESSION_EVALS_v0.1.json"

ORDER = ["P0","P1","P2","P3","P4","P5","P6","P7","P8","P9","P10","P11","INT"]
PLANES = {"KNOWLEDGE","PROJECT","RUNTIME_CONTROL"}
OUTCOMES = {"PASS","FAIL","HOLD","REVIEW_SIGNAL","NOT_APPLICABLE","NOT_EVALUATED"}
CLOSED = {"PASS","ACCEPTED","OUTSIDE_CLAIM","NOT_APPLICABLE"}
HIGH_BADGES = {"PASS","VERIFIED","CURRENT_VERIFIED","PROFESSIONAL_PASS","KEEP_MAIN"}

@dataclass
class Finding:
    rule_id: str
    outcome: str
    severity: str
    object_id: str | None
    message: str
    basis: dict[str, Any] | None = None

def die(msg: str) -> None:
    raise SystemExit(f"typed-system validation failed: {msg}")

def load(path: Path) -> Any:
    if not path.is_file():
        die(f"missing {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        die(f"invalid JSON {path.relative_to(ROOT)}: {exc}")

def oid(obj: dict[str, Any]) -> str | None:
    v = obj.get("id") or obj.get("object_id")
    return None if v is None else str(v)

def sort_key(f: Finding) -> tuple[int,str]:
    ns = f.rule_id.split("/",1)[0]
    return ((ORDER.index(ns) if ns in ORDER else len(ORDER)), f.rule_id)

def contract_checks() -> list[Finding]:
    reg = load(REGISTRY)
    ev = load(EVALS)
    out: list[Finding] = []

    if reg.get("evaluation_order") != ORDER:
        out.append(Finding("INT/REGISTRY-001","FAIL","S3_MAJOR",None,"evaluation order must remain P0→P11→INT"))

    seen: set[str] = set()
    dup: set[str] = set()
    for ns, rules in reg.get("rules", {}).items():
        if ns not in ORDER:
            out.append(Finding("INT/REGISTRY-002","FAIL","S2_MATERIAL",None,f"unknown namespace {ns}"))
        for rid in rules:
            if rid in seen:
                dup.add(rid)
            seen.add(rid)
            if "/" not in rid:
                out.append(Finding("INT/REGISTRY-003","FAIL","S2_MATERIAL",None,f"rule not namespaced: {rid}"))
    if dup:
        out.append(Finding("INT/REGISTRY-004","FAIL","S3_MAJOR",None,"duplicate rule ids",{"duplicates":sorted(dup)}))

    missing = sorted(set(reg.get("replay_derived_rules", {})) - seen)
    if missing:
        out.append(Finding("INT/REGISTRY-005","FAIL","S2_MATERIAL",None,"replay-derived rules absent from namespace lists",{"missing":missing}))

    cases = ev.get("cases", [])
    ids = [c.get("id") for c in cases]
    dups = sorted({x for x in ids if x and ids.count(x) > 1})
    if dups:
        out.append(Finding("INT/EVAL-001","FAIL","S2_MATERIAL",None,"duplicate regression IDs",{"duplicates":dups}))
    for c in cases:
        if not c.get("id") or not c.get("priority") or not c.get("input") or not c.get("expected"):
            out.append(Finding("INT/EVAL-002","FAIL","S2_MATERIAL",c.get("id"),"regression case missing required fields"))

    if not out:
        out.append(Finding("INT/CONTRACTS-000","PASS","S0_INFO",None,f"registry/evals structurally valid; rules={len(seen)} cases={len(cases)}"))
    return out

def snapshot_checks(s: dict[str, Any]) -> list[Finding]:
    out: list[Finding] = []
    if s.get("schema") != "OLEANDER_TYPED_SNAPSHOT_v0.1":
        return [Finding("P0/SNAPSHOT-001","FAIL","S3_MAJOR",None,"invalid snapshot schema",{"actual":s.get("schema")})]

    objects = s.get("objects", [])

    current_groups: dict[tuple[str,str], list[str|None]] = {}
    for o in objects:
        if o.get("plane") not in PLANES:
            out.append(Finding("P0/PLANE-001","FAIL","S3_MAJOR",oid(o),"object must resolve one primary plane",{"plane":o.get("plane")}))
        if o.get("is_current") and o.get("semantic_key"):
            key = (str(o["semantic_key"]), str(o.get("scope_key","GLOBAL")))
            current_groups.setdefault(key, []).append(oid(o))
    for (key, scope), ids in current_groups.items():
        if len(ids) > 1:
            out.append(Finding("P0/ID-002","FAIL","S4_CRITICAL",None,"multiple Current owners for same semantic responsibility/scope",{"semantic_key":key,"scope_key":scope,"object_ids":ids}))

    for o in objects:
        if o.get("semantic_class") == "ASSURANCE_DECISION" and o.get("scope_kind") == "SUPPORT_ONLY":
            grants = o.get("granted_ceilings", {})
            bad = {k:v for k,v in grants.items() if k in {"design_quality","professional","field_operational","source_authority"} and v not in {None,"UNASSESSED","OPEN","NOT_FIELD","UNCHANGED"}}
            if bad:
                out.append(Finding("P1/CLAIM-RP01","FAIL","S3_MAJOR",oid(o),"support-only evidence cannot raise design/professional/field/source-authority ceilings",{"forbidden_grants":bad}))

    for o in objects:
        if o.get("migration_state") in {"INCOMPLETE","LEGACY_UNMIGRATED"} and o.get("project_failure_reason") == "MISSING_NEW_TYPED_FIELDS_ONLY":
            out.append(Finding("P3/MIG-RP01","FAIL","S2_MATERIAL",oid(o),"migration incompleteness alone cannot be rewritten as project failure"))

    for o in objects:
        if o.get("semantic_class") == "INTERFACE" and o.get("disposition") == "CLOSED":
            dims = o.get("acceptance_dimensions", {})
            unresolved = {k:v for k,v in dims.items() if v not in CLOSED}
            if unresolved:
                out.append(Finding("P4/IFC-RP01","FAIL","S3_MAJOR",oid(o),"interface has unresolved material acceptance dimensions",{"unresolved_dimensions":unresolved}))

    for o in objects:
        if o.get("semantic_class") == "CHANGE" and o.get("change_scope") == "SUPPORT_DERIVATIVE_ONLY" and o.get("upstream_source_changed") is False:
            if "UPSTREAM_SOURCE_CONFIGURATION" in set(o.get("stale_effects", [])):
                out.append(Finding("P5/CHG-RP01","FAIL","S3_MAJOR",oid(o),"support-only change cannot stale unchanged upstream source configuration"))

    for o in objects:
        if o.get("semantic_class") in {"ASSURANCE_ACTIVITY","ASSURANCE_DECISION"}:
            tr = o.get("target_results", {})
            if isinstance(tr, dict) and len(set(tr.values())) > 1 and o.get("summary_result") in {"PASS","FAIL"} and not o.get("aggregation_policy"):
                out.append(Finding("P6/ASR-RP02","FAIL","S3_MAJOR",oid(o),"mixed target results require explicit aggregation policy",{"target_results":tr,"summary_result":o.get("summary_result")}))

    for o in objects:
        if o.get("migration_origin_state") == "OPEN_UNCLASSIFIED" and o.get("semantic_class") in {"RISK","ISSUE","ASSUMPTION","UNKNOWN"} and not o.get("classification_basis"):
            out.append(Finding("P7/OPEN-RP01","FAIL","S2_MATERIAL",oid(o),"OPEN state force-classified without semantic basis"))

    census = s.get("corpus_census")
    if census is not None:
        missing = [k for k in ("as_of","scope","enumeration_basis","counts") if not census.get(k)]
        if missing or census.get("hard_ceiling") is True:
            out.append(Finding("P9/CORPUS-RP01","FAIL","S2_MATERIAL",None,"corpus census must be scoped/as-of and cannot be a hard ceiling",{"missing":missing,"hard_ceiling":census.get("hard_ceiling")}))
    for o in objects:
        if o.get("review_evidence_class") in {"GRAPH_ONLY","LINEAGE_ONLY"} and o.get("content_state") == "PASS":
            out.append(Finding("P9/TERM-RP01","FAIL","S2_MATERIAL",oid(o),"graph/lineage-only review evidence cannot grant Content PASS"))
        if o.get("full_body_integrity") == "PASS" and any(o.get(k) == "PASS_BY_READBACK_ONLY" for k in ("content_state","bilingual_state","independent_review_state")):
            out.append(Finding("P9/BODY-RP01","FAIL","S2_MATERIAL",oid(o),"full-body integrity/readback cannot self-grant content/bilingual/IR PASS"))

    assets = s.get("presentation_assets", [])
    source_ids = [a.get("semantic_source_id") for a in assets if a.get("semantic_source_id")]
    declared = s.get("presentation_metrics", {}).get("independent_source_count")
    if declared is not None and declared > len(set(source_ids)):
        out.append(Finding("P10/ASSET-RP01","FAIL","S2_MATERIAL",None,"derivative instances inflate independent semantic visual-source count",{"declared":declared,"unique_sources":len(set(source_ids))}))
    for a in assets:
        aid = a.get("presentation_asset_id")
        if a.get("is_derivative") and not a.get("semantic_source_id"):
            out.append(Finding("P10/ASSET-RP01","FAIL","S2_MATERIAL",aid,"presentation derivative missing semantic_source_id"))
        if a.get("source_role") in {"SUPPORT","PROCESS_SUPPORT","REFERENCE_ONLY"} and a.get("semantic_role") == "PRIMARY_MAIN" and not a.get("authorized_role_change"):
            out.append(Finding("P10/ROLE-RP02","FAIL","S3_MAJOR",aid,"display size/treatment cannot promote support/reference source to PRIMARY_MAIN"))
        if a.get("truth_risk") == "E3" and a.get("semantic_role") in {"PRIMARY_EVIDENCE","FIELD_EVIDENCE","SOURCE_TRUTH"}:
            out.append(Finding("P10/TRUTH-RP03","FAIL","S4_CRITICAL",aid,"E3 synthetic/reference asset cannot occupy evidentiary source role"))
    release = s.get("presentation_release")
    if release and release.get("global_status") == "PASS":
        unresolved = {k:v for k,v in release.get("medium_readback", {}).items() if v not in {"PASS","NOT_APPLICABLE"}}
        if unresolved:
            out.append(Finding("P10/MED-RP01","FAIL","S2_MATERIAL",release.get("id"),"global PASS hides unresolved medium-specific readback",{"unresolved_media":unresolved}))

    for o in objects:
        if o.get("retrieval_space") == "CURRENT" and o.get("professional_state") in {"NOT_PROVEN_PROFESSIONAL_PASS","OPEN","REVISE","HOLD"} and o.get("summary_badge") in HIGH_BADGES:
            out.append(Finding("P11/BADGE-RP02","FAIL","S2_MATERIAL",oid(o),"CURRENT retrieval badge implies unsupported professional/content completion"))

    if not out:
        out.append(Finding("INT/SNAPSHOT-000","PASS","S0_INFO",None,"no implemented invariant violations detected"))
    return sorted(out, key=sort_key)

def self_test() -> list[Finding]:
    snap = {
        "schema":"OLEANDER_TYPED_SNAPSHOT_v0.1",
        "objects":[
            {"id":"A","plane":"PROJECT","semantic_class":"ASSURANCE_DECISION","scope_kind":"SUPPORT_ONLY","granted_ceilings":{"design_quality":"KEEP_MAIN"}},
            {"id":"I","plane":"PROJECT","semantic_class":"INTERFACE","disposition":"CLOSED","acceptance_dimensions":{"GEOMETRY":"PASS","OPERATIONAL":"OPEN"}},
            {"id":"C","plane":"PROJECT","semantic_class":"CHANGE","change_scope":"SUPPORT_DERIVATIVE_ONLY","upstream_source_changed":False,"stale_effects":["UPSTREAM_SOURCE_CONFIGURATION"]},
            {"id":"M","plane":"PROJECT","semantic_class":"ASSURANCE_DECISION","target_results":{"G1":"REVISE","G4":"PASS"},"summary_result":"PASS"},
            {"id":"K","plane":"KNOWLEDGE","semantic_class":"METHOD","retrieval_space":"CURRENT","professional_state":"NOT_PROVEN_PROFESSIONAL_PASS","summary_badge":"CURRENT_VERIFIED"}
        ],
        "corpus_census":{"counts":{"TOTAL":1215},"hard_ceiling":True},
        "presentation_assets":[
            {"presentation_asset_id":"D1","is_derivative":True},
            {"presentation_asset_id":"AI","semantic_source_id":"SRC-AI","truth_risk":"E3","source_role":"REFERENCE_ONLY","semantic_role":"FIELD_EVIDENCE"}
        ],
        "presentation_metrics":{"independent_source_count":3},
        "presentation_release":{"id":"R","global_status":"PASS","medium_readback":{"PDF_PRINT":"PASS","DESKTOP_BROWSER":"WAIT"}}
    }
    findings = snapshot_checks(snap)
    expected = {"P1/CLAIM-RP01","P4/IFC-RP01","P5/CHG-RP01","P6/ASR-RP02","P9/CORPUS-RP01","P10/ASSET-RP01","P10/TRUTH-RP03","P10/MED-RP01","P11/BADGE-RP02"}
    got = {f.rule_id for f in findings}
    missing = sorted(expected - got)
    if missing:
        die(f"self-test missing expected findings {missing}")
    return findings

def emit(findings: list[Finding], source: str, as_json: bool) -> None:
    counts: dict[str,int] = {}
    for f in findings:
        counts[f.outcome] = counts.get(f.outcome,0) + 1
    receipt = {"schema":"OLEANDER_TYPED_VALIDATION_RECEIPT_v0.1","source":source,"evaluation_order":ORDER,"counts":counts,"findings":[asdict(f) for f in findings]}
    if as_json:
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"typed-system validator: {source}")
        print(" ".join(f"{k}={v}" for k,v in sorted(counts.items())))
        for f in findings:
            target = f" [{f.object_id}]" if f.object_id else ""
            print(f"- {f.outcome:<15} {f.rule_id}{target}: {f.message}")

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", type=Path)
    ap.add_argument("--contracts-only", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    findings: list[Finding] = []
    src: list[str] = []
    if args.self_test:
        findings += self_test()
        src.append("self-test")
    if args.contracts_only or (not args.snapshot and not args.self_test):
        findings += contract_checks()
        src.append("contracts")
    if args.snapshot:
        findings += snapshot_checks(load(args.snapshot))
        src.append(str(args.snapshot))

    findings = sorted(findings, key=sort_key)
    emit(findings, "+".join(src) or "none", args.json)
    if any(f.outcome == "FAIL" for f in findings):
        sys.exit(1)

if __name__ == "__main__":
    main()
