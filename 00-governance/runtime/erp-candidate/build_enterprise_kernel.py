from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

PHASE1_MODULES = ("erp", "plm", "bpm", "qms")
DOES_NOT_PROVE = [
    "CURRENT_ADOPTION",
    "ENTERPRISE_COMPLETENESS",
    "DESIGN_KEEP",
    "PROFESSIONAL_PASS",
    "PROJECT_PROMOTION",
    "STATUTORY_APPROVAL",
]
STATE_FAMILY_MAP = {
    "project_design": "PROJECT_DESIGN",
    "job": "JOB",
    "knowledge_integrity": "KNOWLEDGE_INTEGRITY",
    "operational_eligibility": "OPERATIONAL_ELIGIBILITY",
    "design_quality": "DESIGN_QUALITY",
    "professional": "PROFESSIONAL",
    "interface": "INTERFACE",
    "authority": "AUTHORITY",
    "evidence": "EVIDENCE",
    "configuration": "CONFIGURATION",
    "quality": "QUALITY",
    "process": "PROCESS",
    "agent_runtime": "AGENT_RUNTIME",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return text.encode("utf-8")


def canonical_sha256(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest().upper()


def token(value: str) -> str:
    return "".join(ch if ch.isalnum() else "-" for ch in value).strip("-").upper() or "UNRESOLVED"


def state_value(value) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def blocking_semantics(value: str) -> str:
    upper = value.upper()
    explicit = ("HOLD", "BLOCKED", "FAIL", "FAILED", "REJECT", "REVISE", "STALE", "DIVERGED", "MISSING")
    if any(term in upper for term in explicit):
        return "EXPLICIT"
    potential = ("UNKNOWN", "PENDING", "REVIEW", "PARTIAL", "OPEN")
    if any(term in upper for term in potential):
        return "POTENTIAL"
    return "NONE"


def build_kernel(projection: dict, source_ref: str, source_sha256: str, generated_at: str | None = None) -> dict:
    if projection.get("kind") != "OLEANDER_ENTERPRISE_ORCHESTRATION_PROJECTION":
        raise ValueError("source must be OLEANDER_ENTERPRISE_ORCHESTRATION_PROJECTION")
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()

    identities: dict[str, dict] = {}
    authority_bindings: list[dict] = []
    state_facts: list[dict] = []
    relations: list[dict] = []
    work_items: list[dict] = []
    configuration_items: list[dict] = []
    evidence_items: list[dict] = []
    changes: list[dict] = []
    readbacks: list[dict] = []
    receipts: list[dict] = []
    module_refs: dict[str, list[str]] = {name: [] for name in PHASE1_MODULES}

    def ensure_identity(ref: str, identity_class: str = "OTHER", sources: list[str] | None = None) -> str:
        if not ref:
            raise ValueError("kernel identity ref may not be empty")
        iid = f"KID-{token(ref)}"
        if iid not in identities:
            identities[iid] = {
                "identity_id": iid,
                "identity_class": identity_class,
                "canonical_ref": ref,
                "source_refs": sources or [source_ref],
                "projection_only": True,
            }
        elif identities[iid]["identity_class"] == "OTHER" and identity_class != "OTHER":
            identities[iid]["identity_class"] = identity_class
            identities[iid]["source_refs"] = sorted(set(identities[iid]["source_refs"] + (sources or [source_ref])))
        return iid

    def add_state(subject_ref: str, family: str, value, sources: list[str] | None = None, sid_suffix: str | None = None) -> str:
        ensure_identity(subject_ref, sources=sources)
        rendered = state_value(value)
        sid = f"KSTATE-{token(subject_ref)}-{token(family)}"
        if sid_suffix:
            sid += f"-{token(sid_suffix)}"
        state_facts.append({
            "state_fact_id": sid,
            "subject_ref": subject_ref,
            "state_family": family,
            "state_value": rendered,
            "blocking_semantics": blocking_semantics(rendered),
            "source_refs": sources or [source_ref],
            "projection_only": True,
        })
        return sid

    for ref in projection.get("project_axis_refs", []):
        klass = {"P0_PORTFOLIO":"PORTFOLIO","P1_PROGRAM":"PROGRAM","P2_PROJECT":"PROJECT","P3_WORKSTREAM":"WORKSTREAM"}.get(ref.get("axis_level"), "OTHER")
        ensure_identity(ref["canonical_id"], klass)

    for wp in projection.get("work_packages", []):
        ensure_identity(wp["work_package_id"], "WORK_PACKAGE")
        ensure_identity(wp["project_id"], "PROJECT")
        if wp.get("workstream_id"):
            ensure_identity(wp["workstream_id"], "WORKSTREAM")
        for decision in wp.get("decision_object_ids", []):
            ensure_identity(decision, "DECISION_OBJECT")
        for dependency in wp.get("depends_on", []):
            ensure_identity(dependency, sources=[source_ref])
        for output in wp.get("required_native_outputs", []):
            ensure_identity(output, "ARTIFACT", [source_ref])
        work_items.append({
            "work_id": wp["work_package_id"], "work_class":"WORK_PACKAGE", "subject_ref":wp["work_package_id"],
            "work_state":wp["coordination_state"], "depends_on_refs":list(wp.get("depends_on", [])), "owner_refs":[],
            "output_refs":list(wp.get("required_native_outputs", [])), "readback_refs":[], "source_refs":[source_ref], "projection_only":True,
        })
        add_state(wp["work_package_id"], "PROCESS", wp["coordination_state"])

    for job in projection.get("jobs", []):
        ensure_identity(job["job_id"], "JOB")
        ensure_identity(job["work_package_id"], "WORK_PACKAGE")
        for out in job.get("output_refs", []): ensure_identity(out, "ARTIFACT")
        for rb in job.get("readback_refs", []):
            ensure_identity(rb, "READBACK")
            readbacks.append({"readback_id":rb,"subject_ref":job["job_id"],"readback_class":"EXECUTION","readback_state":"OBSERVED","source_refs":[source_ref],"projection_only":True})
        work_items.append({
            "work_id":job["job_id"],"work_class":"JOB","subject_ref":job["job_id"],"work_state":job["job_state"],
            "depends_on_refs":list(job.get("input_refs", [])),"owner_refs":[job["primary_owner_ref"]],"output_refs":list(job.get("output_refs", [])),
            "readback_refs":list(job.get("readback_refs", [])),"source_refs":[source_ref],"projection_only":True,
        })
        add_state(job["job_id"], "JOB", job["job_state"])

    for artifact in projection.get("artifact_refs", []):
        ensure_identity(artifact["artifact_id"], "ARTIFACT")

    for review in projection.get("review_refs", []):
        ensure_identity(review["review_id"], "REVIEW")
        receipt_id = review.get("receipt_ref") or f"RECEIPT-MISSING:{review['review_id']}"
        receipts.append({
            "receipt_id":receipt_id,"subject_ref":review["review_id"],"receipt_class":"REVIEW","result":review["result"],
            "independence_state":review["independence_state"],"source_refs":[source_ref],"projection_only":True,
            "does_not_prove":["DESIGN_KEEP","PROFESSIONAL_PASS","PROJECT_PROMOTION"],
        })
        add_state(review["review_id"], "QUALITY", review["result"], sid_suffix="REVIEW")

    for family_key, rows in projection.get("state_facets", {}).items():
        family = STATE_FAMILY_MAP.get(family_key)
        if not family:
            continue
        for subject_ref, value in rows.items():
            add_state(subject_ref, family, value, sid_suffix="TOP")

    rec = projection.get("reconciliation", {})
    add_state(source_ref, "PROJECTION_FRESHNESS", rec.get("projection_freshness_state", "SOURCE_READBACK_UNKNOWN"), sid_suffix="PROJECTION")
    add_state(source_ref, "ENTERPRISE_READINESS", rec.get("enterprise_readiness_state", "NOT_EVALUATED"), sid_suffix="PROJECTION")

    relation_identity_hints = {
        "JOB_PRODUCES_ARTIFACT": ("JOB", "ARTIFACT"),
        "JOB_EXECUTES_WORK_PACKAGE": ("JOB", "WORK_PACKAGE"),
        "PROJECT_CONTAINS_WORK_PACKAGE": ("PROJECT", "WORK_PACKAGE"),
        "ARTIFACT_REVIEWED_BY": ("ARTIFACT", "REVIEW"),
        "SATISFIES": ("ARTIFACT", "REQUIREMENT"),
        "VERIFIES": ("OTHER", "REQUIREMENT"),
        "VALIDATES": ("OTHER", "REQUIREMENT"),
        "IMPLEMENTS": ("ARTIFACT", "REQUIREMENT"),
        "ALLOCATES_TO": ("REQUIREMENT", "OTHER"),
        "NONCONFORMANCE_AFFECTS": ("QUALITY_ITEM", "ARTIFACT"),
        "CAPA_ADDRESSES": ("QUALITY_ITEM", "QUALITY_ITEM"),
        "AGENT_EXECUTES_JOB": ("OTHER", "JOB"),
    }
    for rel in projection.get("digital_thread", {}).get("relations", []):
        from_class, to_class = relation_identity_hints.get(rel.get("relation_type"), ("OTHER", "OTHER"))
        ensure_identity(rel["from_ref"], from_class, list(rel.get("source_refs", [source_ref])))
        ensure_identity(rel["to_ref"], to_class, list(rel.get("source_refs", [source_ref])))
        relations.append({
            "relation_id":rel["relation_id"],"relation_type":rel["relation_type"],"from_ref":rel["from_ref"],"to_ref":rel["to_ref"],
            "source_refs":list(rel.get("source_refs", [source_ref])),"projection_only":True,"authority_effect":"NONE",
        })
    for unresolved in projection.get("digital_thread", {}).get("unresolved_links", []):
        if unresolved.get("blocking"):
            ensure_identity(unresolved["from_ref"])
            add_state(unresolved["from_ref"], "INTERFACE", f"BLOCKING_RELATION:{unresolved['expected_relation_type']}:{unresolved['reason']}", [source_ref], unresolved["link_id"])

    authority_snapshot = projection.get("authority", {}).get("authority_snapshot_ref") or "PROJECT_AUTHORITY_UNRESOLVED"
    for ref in projection.get("project_axis_refs", []):
        if ref.get("axis_level") == "P2_PROJECT":
            authority_bindings.append({
                "authority_binding_id":f"KAUTH-{token(ref['canonical_id'])}-PROJECT","subject_ref":ref["canonical_id"],
                "authority_owner_ref":authority_snapshot,"authority_scope":"PROJECT","source_refs":[source_ref],"projection_only":True,"authority_gain":False,
            })

    erp = projection["modules"]["erp"]
    for row in erp.get("schedule_records", []):
        ensure_identity(row["subject_ref"], "WORK_PACKAGE", row["source_refs"])
        sid=add_state(row["subject_ref"], "PROCESS", f"ERP_SCHEDULE:{row['schedule_state']}", row["source_refs"], row["schedule_id"])
        module_refs["erp"].append(sid)
    for row in erp.get("resource_demand", []):
        ensure_identity(row["work_package_id"], "WORK_PACKAGE", row["source_refs"])
        rid=add_state(row["work_package_id"], "PROCESS", f"ERP_RESOURCE:{row['demand_state']}:{row['resource_ref']}", row["source_refs"], row["demand_id"])
        module_refs["erp"].append(rid)

    plm = projection["modules"]["plm"]
    baseline_by_member: dict[str,str] = {}
    for base in plm.get("baselines", []):
        for member in base.get("member_refs", []): baseline_by_member[member]=base["baseline_id"]
    for row in plm.get("configuration_items", []):
        ensure_identity(row["canonical_ref"], "ARTIFACT", row["source_refs"])
        cid=f"KCONFIG-{token(row['item_id'])}"
        configuration_items.append({
            "configuration_id":cid,"subject_ref":row["canonical_ref"],"configuration_class":row["item_class"],
            "revision_ref":row["revision_ref"],"configuration_state":row["lifecycle_state"],"baseline_ref":baseline_by_member.get(row["item_id"]),
            "source_refs":row["source_refs"],"projection_only":True,"does_not_prove":list(row.get("does_not_prove", [])),
        })
        add_state(row["canonical_ref"], "CONFIGURATION", row["lifecycle_state"], row["source_refs"], row["item_id"])
        module_refs["plm"].append(cid)
    for row in plm.get("change_records", []):
        ensure_identity(row["change_id"], "CHANGE", row["source_refs"])
        for affected in row.get("affected_refs", []): ensure_identity(affected, sources=row["source_refs"])
        ch={"change_id":row["change_id"],"affected_refs":list(row.get("affected_refs", [])),"change_state":row["disposition"],"reopen_refs":list(row.get("reopen_refs", [])),"required_readback_refs":[],"source_refs":row["source_refs"],"projection_only":True}
        changes.append(ch); module_refs["plm"].append(row["change_id"])
        add_state(row["change_id"], "CONFIGURATION", row["disposition"], row["source_refs"], "CHANGE")

    bpm = projection["modules"]["bpm"]
    for row in bpm.get("process_instances", []):
        ensure_identity(row["process_instance_id"], "PROCESS_INSTANCE", row["source_refs"])
        work_items.append({"work_id":row["process_instance_id"],"work_class":"PROCESS_INSTANCE","subject_ref":row["subject_ref"],"work_state":row["process_state"],"depends_on_refs":[],"owner_refs":["Master Runtime"],"output_refs":[],"readback_refs":[],"source_refs":row["source_refs"],"projection_only":True})
        add_state(row["subject_ref"], "PROCESS", f"BPM:{row['process_state']}", row["source_refs"], row["process_instance_id"])
        module_refs["bpm"].append(row["process_instance_id"])
    for row in bpm.get("handoffs", []):
        hid=row["handoff_id"]; ensure_identity(hid, "PROCESS_INSTANCE", row["source_refs"])
        work_items.append({"work_id":hid,"work_class":"HANDOFF","subject_ref":hid,"work_state":row["handoff_state"],"depends_on_refs":list(row.get("payload_refs", [])),"owner_refs":[row["from_owner_ref"],row["to_owner_ref"]],"output_refs":[],"readback_refs":[row["acceptance_ref"]] if row.get("acceptance_ref") else [],"source_refs":row["source_refs"],"projection_only":True})
        add_state(hid,"PROCESS",f"BPM_HANDOFF:{row['handoff_state']}",row["source_refs"],hid); module_refs["bpm"].append(hid)
    for row in bpm.get("exceptions", []):
        eid=row["exception_id"]; ensure_identity(eid,"PROCESS_INSTANCE",row["source_refs"])
        work_items.append({"work_id":eid,"work_class":"EXCEPTION","subject_ref":row["subject_ref"],"work_state":row["disposition"],"depends_on_refs":[],"owner_refs":["Master Runtime"],"output_refs":[],"readback_refs":[],"source_refs":row["source_refs"],"projection_only":True})
        add_state(row["subject_ref"],"PROCESS",f"BPM_EXCEPTION:{row['exception_class']}:{row['disposition']}",row["source_refs"],eid); module_refs["bpm"].append(eid)

    qms = projection["modules"]["qms"]
    for row in qms.get("nonconformances", []):
        ensure_identity(row["ncr_id"], "QUALITY_ITEM", row["source_refs"]); ensure_identity(row["subject_ref"], sources=row["source_refs"])
        sid=add_state(row["ncr_id"],"QUALITY",f"NCR:{row['severity']}:{row['state']}",row["source_refs"],row["ncr_id"])
        relations.append({"relation_id":f"KREL-{token(row['ncr_id'])}-AFFECTS","relation_type":"NONCONFORMANCE_AFFECTS","from_ref":row["ncr_id"],"to_ref":row["subject_ref"],"source_refs":row["source_refs"],"projection_only":True,"authority_effect":"NONE"})
        module_refs["qms"].append(sid)
    for row in qms.get("capa_records", []):
        ensure_identity(row["capa_id"], "QUALITY_ITEM", row["source_refs"])
        sid=add_state(row["capa_id"],"QUALITY",f"CAPA:{row['state']}:{row['root_cause_state']}",row["source_refs"],row["capa_id"])
        for ncr in row.get("source_ncr_refs", []):
            ensure_identity(ncr,"QUALITY_ITEM",row["source_refs"])
            relations.append({"relation_id":f"KREL-{token(row['capa_id'])}-{token(ncr)}","relation_type":"CAPA_ADDRESSES","from_ref":row["capa_id"],"to_ref":ncr,"source_refs":row["source_refs"],"projection_only":True,"authority_effect":"NONE"})
        if row.get("effectiveness_readback_ref"):
            rb=row["effectiveness_readback_ref"]; ensure_identity(rb,"READBACK",row["source_refs"])
            readbacks.append({"readback_id":rb,"subject_ref":row["capa_id"],"readback_class":"QUALITY_EFFECTIVENESS","readback_state":"OBSERVED","source_refs":row["source_refs"],"projection_only":True})
        module_refs["qms"].append(sid)
    for row in qms.get("inspection_records", []):
        ensure_identity(row["inspection_id"], "REVIEW", row["source_refs"]); ensure_identity(row["subject_ref"], sources=row["source_refs"])
        eid=f"KEVID-{token(row['inspection_id'])}"
        evidence_items.append({"evidence_id":eid,"subject_ref":row["subject_ref"],"evidence_class":"REVIEW","result":row["result"],"evidence_refs":list(row.get("evidence_refs", [])),"source_refs":row["source_refs"],"projection_only":True,"claim_ceiling":"QUALITY_REVIEW_ONLY_NO_PROFESSIONAL_OR_PROMOTION_AUTHORITY"})
        add_state(row["subject_ref"],"QUALITY",f"INSPECTION:{row['result']}",row["source_refs"],row["inspection_id"]); module_refs["qms"].append(eid)

    module_bindings=[]
    for key in PHASE1_MODULES:
        header=projection["modules"][key]["header"]
        module_bindings.append({"module":header["module"],"kernel_object_refs":sorted(set(module_refs[key])),"source_refs":list(header["source_refs"]),"projection_only":True})

    all_identity_refs={row["canonical_ref"] for row in identities.values()}
    referenced=set()
    for row in relations: referenced|={row["from_ref"],row["to_ref"]}
    for row in work_items: referenced.add(row["subject_ref"]); referenced.update(row["depends_on_refs"]); referenced.update(row["output_refs"]); referenced.update(row["readback_refs"])
    for row in configuration_items: referenced.add(row["subject_ref"])
    for row in evidence_items: referenced.add(row["subject_ref"])
    for row in changes: referenced.update(row["affected_refs"]); referenced.update(row["reopen_refs"])
    unresolved=len({r for r in referenced if r and r not in all_identity_refs and not r.startswith("skill:") and not r.startswith("review:")})

    return {
        "schema_version":"0.1-candidate","kind":"OLEANDER_ENTERPRISE_KERNEL","candidate_status":"EVAL_ONLY","generated_at":generated_at,
        "source_projection_ref":source_ref,"source_projection_digest":{"sha256":source_sha256,"hash_semantics":"UTF8_TEXT_LF_CANONICAL_V1"},
        "authority_boundary":{"kernel_is_authority":False,"may_mutate_current":False,"identity_rule":"CANONICAL_REFS_ONLY_NO_AUTHORITY_SYNTHESIS","state_rule":"ORTHOGONAL_STATE_FACTS_NO_FLATTENING","relation_rule":"SOURCE_BOUND_RELATIONS_NO_AUTHORITY_TRANSFER"},
        "identities":sorted(identities.values(),key=lambda x:x["identity_id"]),"authority_bindings":authority_bindings,"state_facts":state_facts,"relations":relations,"work_items":work_items,"configuration_items":configuration_items,"evidence_items":evidence_items,"changes":changes,"readbacks":readbacks,"receipts":receipts,"module_bindings":module_bindings,
        "kernel_metrics":{"identity_count":len(identities),"state_fact_count":len(state_facts),"relation_count":len(relations),"phase1_module_binding_count":4,"unresolved_identity_ref_count":unresolved,"authority_gain_count":0,"projection_rebuildable":True},
        "does_not_prove":DOES_NOT_PROVE,
    }


def main() -> int:
    parser=argparse.ArgumentParser(description="Build OLEANDER Enterprise Kernel v0.1 candidate from an enterprise projection.")
    parser.add_argument("input",type=Path); parser.add_argument("--output",type=Path); parser.add_argument("--generated-at")
    args=parser.parse_args(); projection=load_json(args.input)
    kernel=build_kernel(projection,args.input.as_posix(),canonical_sha256(args.input),args.generated_at)
    payload=(json.dumps(kernel,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        if not args.output.is_file() or args.output.read_bytes()!=payload: args.output.write_bytes(payload)
        print(args.output)
    else: print(payload.decode("utf-8"),end="")
    return 0

if __name__=="__main__": raise SystemExit(main())
