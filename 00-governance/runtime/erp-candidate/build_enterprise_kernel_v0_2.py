from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from build_enterprise_kernel import (
    build_kernel as build_phase1_kernel,
    canonical_sha256,
    load_json,
    token,
)


PHASE2_MODULES = ("mes", "mbse", "knowledge_graph", "agent_runtime")
ALL_MODULES = ("erp", "plm", "bpm", "qms") + PHASE2_MODULES


def _blocking(value: str) -> str:
    upper = value.upper()
    if any(term in upper for term in ("HOLD", "BLOCKED", "FAIL", "FAILED", "REJECT", "REVISE", "STALE", "DIVERGED", "MISSING", "CONFLICT", "UNCERTAIN")):
        return "EXPLICIT"
    if any(term in upper for term in ("UNKNOWN", "PENDING", "REVIEW", "PARTIAL", "OPEN", "NOT_RUN")):
        return "POTENTIAL"
    return "NONE"


def build_kernel_v0_2(projection: dict, source_ref: str, source_sha256: str, generated_at: str | None = None) -> dict:
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()
    kernel = build_phase1_kernel(projection, source_ref, source_sha256, generated_at)
    kernel["schema_version"] = "0.2-candidate"

    identities = {row["identity_id"]: row for row in kernel["identities"]}
    state_facts = kernel["state_facts"]
    relations = kernel["relations"]
    work_items = kernel["work_items"]
    evidence_items = kernel["evidence_items"]
    readbacks = kernel["readbacks"]
    module_refs: dict[str, list[str]] = {name: [] for name in PHASE2_MODULES}

    def ensure_identity(ref: str, identity_class: str = "OTHER", sources: list[str] | None = None) -> str:
        if not ref:
            raise ValueError("Phase-2 kernel identity ref may not be empty")
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

    def add_state(subject_ref: str, family: str, value: str, sources: list[str], suffix: str, claim_scope: str, force_blocking: str | None = None) -> str:
        ensure_identity(subject_ref, sources=sources)
        sid = f"KSTATE-{token(subject_ref)}-{token(family)}-{token(suffix)}"
        state_facts.append({
            "state_fact_id": sid,
            "subject_ref": subject_ref,
            "state_family": family,
            "state_value": value,
            "claim_scope": claim_scope,
            "blocking_semantics": force_blocking or _blocking(value),
            "source_refs": sources,
            "projection_only": True,
        })
        return sid

    def add_relation(relation_id: str, relation_type: str, from_ref: str, to_ref: str, sources: list[str], from_class: str = "OTHER", to_class: str = "OTHER") -> str:
        ensure_identity(from_ref, from_class, sources)
        ensure_identity(to_ref, to_class, sources)
        relations.append({
            "relation_id": relation_id,
            "relation_type": relation_type,
            "from_ref": from_ref,
            "to_ref": to_ref,
            "source_refs": sources,
            "projection_only": True,
            "authority_effect": "NONE",
        })
        return relation_id

    def add_readback(readback_id: str, subject_ref: str, readback_class: str, sources: list[str], state: str = "OBSERVED") -> str:
        ensure_identity(readback_id, "READBACK", sources)
        if not any(row["readback_id"] == readback_id for row in readbacks):
            readbacks.append({
                "readback_id": readback_id,
                "subject_ref": subject_ref,
                "readback_class": readback_class,
                "readback_state": state,
                "source_refs": sources,
                "projection_only": True,
            })
        return readback_id

    # MES -> operation work + execution state + actual readback.
    mes = projection["modules"]["mes"]
    for row in mes.get("operation_records", []):
        sources = list(row["source_refs"])
        op = row["operation_id"]
        ensure_identity(op, "OPERATION", sources)
        ensure_identity(row["work_package_id"], "WORK_PACKAGE", sources)
        for ref in row.get("resource_refs", []):
            ensure_identity(ref, "RESOURCE", sources)
            module_refs["mes"].append(add_relation(f"KREL-{token(op)}-USES-{token(ref)}", "USES_RESOURCE", op, ref, sources, "OPERATION", "RESOURCE"))
        for ref in row.get("input_refs", []):
            ensure_identity(ref, sources=sources)
            module_refs["mes"].append(add_relation(f"KREL-{token(op)}-CONSUMES-{token(ref)}", "CONSUMES", op, ref, sources, "OPERATION"))
        for ref in row.get("output_refs", []):
            ensure_identity(ref, "ARTIFACT", sources)
            module_refs["mes"].append(add_relation(f"KREL-{token(op)}-PRODUCES-{token(ref)}", "OPERATION_PRODUCES_ARTIFACT", op, ref, sources, "OPERATION", "ARTIFACT"))
        module_refs["mes"].append(add_relation(f"KREL-{token(op)}-WP", "OPERATION_EXECUTES_WORK_PACKAGE", op, row["work_package_id"], sources, "OPERATION", "WORK_PACKAGE"))
        actual = []
        for ref in row.get("actual_readback_refs", []):
            actual.append(add_readback(ref, op, "MES_EXECUTION", sources))
            module_refs["mes"].append(add_relation(f"KREL-{token(op)}-RB-{token(ref)}", "OPERATION_HAS_READBACK", op, ref, sources, "OPERATION", "READBACK"))
        work_items.append({
            "work_id": op,
            "work_class": "OPERATION",
            "subject_ref": op,
            "work_state": row["execution_state"],
            "depends_on_refs": list(row.get("input_refs", [])) + list(row.get("resource_refs", [])),
            "owner_refs": [],
            "output_refs": list(row.get("output_refs", [])),
            "readback_refs": actual,
            "source_refs": sources,
            "projection_only": True,
        })
        module_refs["mes"].append(op)
        module_refs["mes"].append(add_state(op, "EXECUTION", f"MES:{row['operation_class']}:{row['execution_state']}", sources, op, f"MES_OPERATION:{row['operation_class']}"))
    for row in mes.get("material_equipment_refs", []):
        module_refs["mes"].append(ensure_identity(row["canonical_ref"], "RESOURCE", list(row["source_refs"])))
    for row in mes.get("execution_readbacks", []):
        module_refs["mes"].append(add_readback(row["canonical_ref"], row["canonical_ref"], "MES_EXECUTION", list(row["source_refs"])))

    # MBSE -> requirement / interface / V&V remain distinct claim scopes.
    mbse = projection["modules"]["mbse"]
    for row in mbse.get("requirements", []):
        sources = list(row["source_refs"])
        req = row["requirement_id"]
        module_refs["mbse"].append(ensure_identity(req, "REQUIREMENT", sources))
        module_refs["mbse"].append(add_state(req, "REQUIREMENT", f"REQUIREMENT:{row['status']}", sources, req, f"MBSE_REQUIREMENT:{row['requirement_class']}"))
        for target in row.get("allocated_to_refs", []):
            module_refs["mbse"].append(add_relation(f"KREL-{token(req)}-ALLOC-{token(target)}", "ALLOCATES_TO", req, target, sources, "REQUIREMENT"))
    for row in mbse.get("system_elements", []):
        sources = list(row["source_refs"])
        module_refs["mbse"].append(ensure_identity(row["element_id"], "SYSTEM_ELEMENT", sources))
        ensure_identity(row["canonical_ref"], "ARTIFACT" if row["element_class"] == "WORK_PRODUCT" else "OTHER", sources)
        module_refs["mbse"].append(add_relation(f"KREL-{token(row['element_id'])}-REPRESENTS", "SYSTEM_ELEMENT_REPRESENTS", row["element_id"], row["canonical_ref"], sources, "SYSTEM_ELEMENT"))
    for row in mbse.get("interfaces", []):
        sources = list(row["source_refs"])
        interface = row["interface_id"]
        module_refs["mbse"].append(ensure_identity(interface, "INTERFACE", sources))
        module_refs["mbse"].append(add_relation(f"KREL-{token(interface)}-FROM", "INTERFACE_FROM", interface, row["from_ref"], sources, "INTERFACE"))
        module_refs["mbse"].append(add_relation(f"KREL-{token(interface)}-TO", "INTERFACE_TO", interface, row["to_ref"], sources, "INTERFACE"))
        module_refs["mbse"].append(add_state(interface, "INTERFACE", f"MBSE_INTERFACE:{row['interface_state']}", sources, interface, "MBSE_INTERFACE"))
    for row in mbse.get("verification_validation", []):
        sources = list(row["source_refs"])
        vv = row["vv_id"]
        ensure_identity(vv, "REVIEW", sources)
        ensure_identity(row["subject_ref"], "REQUIREMENT", sources)
        for ref in row.get("evidence_refs", []):
            ensure_identity(ref, sources=sources)
        eid = f"KEVID-{token(vv)}"
        evidence_items.append({
            "evidence_id": eid,
            "subject_ref": row["subject_ref"],
            "evidence_class": row["vv_class"],
            "result": row["result"],
            "evidence_refs": list(row.get("evidence_refs", [])),
            "source_refs": sources,
            "projection_only": True,
            "claim_ceiling": f"MBSE_{row['vv_class']}_ONLY_NO_PROJECT_ACCEPTANCE_OR_PROMOTION",
        })
        force = "EXPLICIT" if row["result"] in {"FAIL", "HOLD", "NOT_RUN", "PARTIAL"} else None
        module_refs["mbse"].append(eid)
        module_refs["mbse"].append(add_state(row["subject_ref"], "VALIDATION", f"{row['vv_class']}:{row['result']}", sources, vv, f"MBSE_VV:{row['vv_class']}", force))
        relation_type = "VERIFIES" if row["vv_class"] == "VERIFICATION" else "VALIDATES"
        module_refs["mbse"].append(add_relation(f"KREL-{token(vv)}-{relation_type}", relation_type, vv, row["subject_ref"], sources, "REVIEW", "REQUIREMENT"))
        if row.get("independent_review_ref"):
            module_refs["mbse"].append(add_relation(f"KREL-{token(vv)}-INDEPENDENT", "REVIEWED_BY", vv, row["independent_review_ref"], sources, "REVIEW", "REVIEW"))
    for ref in mbse.get("configuration_baselines", []):
        module_refs["mbse"].append(ensure_identity(ref, "OTHER", list(mbse["header"]["source_refs"])))

    # Knowledge Graph -> source-bound identities/relations/provenance only; never authority.
    kg = projection["modules"]["knowledge_graph"]
    node_class_map = {
        "PROJECT": "PROJECT", "WORKSTREAM": "WORKSTREAM", "ARTIFACT": "ARTIFACT", "REVIEW": "REVIEW",
        "RECEIPT": "RECEIPT", "REQUIREMENT": "REQUIREMENT", "AGENT_SESSION": "AGENT_SESSION",
    }
    for row in kg.get("nodes", []):
        module_refs["knowledge_graph"].append(ensure_identity(row["canonical_ref"], node_class_map.get(row["node_class"], "KNOWLEDGE_NODE"), list(row["source_refs"])))
    for row in kg.get("edges", []):
        module_refs["knowledge_graph"].append(add_relation(row["edge_id"], row["predicate"], row["from_ref"], row["to_ref"], list(row["source_refs"])))
    for row in kg.get("provenance_records", []):
        sources = list(row["source_refs"])
        entity = row["entity_ref"]
        ensure_identity(entity, sources=sources)
        eid = f"KEVID-{token(row['provenance_id'])}"
        evidence_items.append({
            "evidence_id": eid,
            "subject_ref": entity,
            "evidence_class": "KNOWLEDGE_PROVENANCE",
            "result": "SOURCE_BOUND",
            "evidence_refs": list(row.get("derived_from_refs", [])),
            "source_refs": sources,
            "projection_only": True,
            "claim_ceiling": "PROVENANCE_ONLY_NO_CANONICAL_TRUTH_OR_AUTHORITY_GAIN",
        })
        module_refs["knowledge_graph"].append(eid)
        module_refs["knowledge_graph"].append(add_state(entity, "KNOWLEDGE_PROVENANCE", "SOURCE_BOUND", sources, row["provenance_id"], "KG_PROVENANCE"))
        for ref in row.get("derived_from_refs", []):
            module_refs["knowledge_graph"].append(add_relation(f"KREL-{token(row['provenance_id'])}-DERIVED-{token(ref)}", "PROVENANCE_DERIVED_FROM", entity, ref, sources))
        if row.get("generated_by_ref"):
            module_refs["knowledge_graph"].append(add_relation(f"KREL-{token(row['provenance_id'])}-GENERATED", "PROVENANCE_GENERATED_BY", entity, row["generated_by_ref"], sources))
        for ref in row.get("attributed_to_refs", []):
            module_refs["knowledge_graph"].append(add_relation(f"KREL-{token(row['provenance_id'])}-ATTR-{token(ref)}", "PROVENANCE_ATTRIBUTED_TO", entity, ref, sources))
    for row in kg.get("query_policies", []):
        module_refs["knowledge_graph"].append(ensure_identity(row["policy_id"], "QUERY_POLICY", list(row["source_refs"])))

    # Agent Runtime -> session/lease/action/handoff + side-effect readback.
    agent = projection["modules"]["agent_runtime"]
    for row in agent.get("sessions", []):
        sources = list(row["source_refs"])
        session = row["session_id"]
        ensure_identity(session, "AGENT_SESSION", sources)
        ensure_identity(row["task_ref"], "JOB", sources)
        ensure_identity(row["authority_ref"], "OTHER", sources)
        ensure_identity(row["checkpoint_ref"], "READBACK", sources)
        work_items.append({
            "work_id": session, "work_class": "AGENT_SESSION", "subject_ref": session, "work_state": row["session_state"],
            "depends_on_refs": [row["task_ref"], row["checkpoint_ref"]], "owner_refs": [row["agent_ref"]], "output_refs": [], "readback_refs": [],
            "source_refs": sources, "projection_only": True,
        })
        module_refs["agent_runtime"].append(session)
        module_refs["agent_runtime"].append(add_state(session, "AGENT_RUNTIME", f"SESSION:{row['session_state']}", sources, session, "AGENT_SESSION"))
        module_refs["agent_runtime"].append(add_relation(f"KREL-{token(session)}-TASK", "AGENT_EXECUTES_JOB", session, row["task_ref"], sources, "AGENT_SESSION", "JOB"))
    for row in agent.get("leases", []):
        sources = list(row["source_refs"])
        lease = row["lease_id"]
        ensure_identity(lease, "AGENT_LEASE", sources)
        ensure_identity(row["subject_ref"], sources=sources)
        force = "EXPLICIT" if row["lease_state"] == "CONFLICT" else None
        module_refs["agent_runtime"].append(lease)
        module_refs["agent_runtime"].append(add_state(lease, "AGENT_RUNTIME", f"LEASE:{row['lease_state']}", sources, lease, "AGENT_LEASE", force))
        module_refs["agent_runtime"].append(add_relation(f"KREL-{token(lease)}-SUBJECT", "LEASE_CONTROLS_SUBJECT", lease, row["subject_ref"], sources, "AGENT_LEASE"))
    for row in agent.get("actions", []):
        sources = list(row["source_refs"])
        action = row["action_id"]
        ensure_identity(action, "AGENT_ACTION", sources)
        ensure_identity(row["session_id"], "AGENT_SESSION", sources)
        ensure_identity(row["subject_ref"], sources=sources)
        readback_refs = []
        for ref in row.get("readback_refs", []):
            readback_refs.append(add_readback(ref, action, "AGENT_SIDE_EFFECT", sources))
        work_items.append({
            "work_id": action, "work_class": "AGENT_ACTION", "subject_ref": action, "work_state": row["side_effect_state"],
            "depends_on_refs": [row["session_id"], row["authorization_ref"]], "owner_refs": [], "output_refs": [row["subject_ref"]],
            "readback_refs": readback_refs, "source_refs": sources, "projection_only": True,
        })
        force = "EXPLICIT" if row["side_effect_state"] == "OBSERVED_UNCERTAIN" else None
        module_refs["agent_runtime"].append(action)
        module_refs["agent_runtime"].append(add_state(action, "AGENT_RUNTIME", f"ACTION:{row['action_class']}:{row['side_effect_state']}", sources, action, "AGENT_ACTION", force))
        module_refs["agent_runtime"].append(add_relation(f"KREL-{token(row['session_id'])}-{token(action)}", "AGENT_SESSION_HAS_ACTION", row["session_id"], action, sources, "AGENT_SESSION", "AGENT_ACTION"))
        module_refs["agent_runtime"].append(add_relation(f"KREL-{token(action)}-SUBJECT", "AGENT_ACTION_AFFECTS", action, row["subject_ref"], sources, "AGENT_ACTION"))
    for row in agent.get("handoffs", []):
        sources = list(row["source_refs"])
        handoff = row["handoff_id"]
        ensure_identity(handoff, "AGENT_HANDOFF", sources)
        ensure_identity(row["from_session_ref"], "AGENT_SESSION", sources)
        work_items.append({
            "work_id": handoff, "work_class": "AGENT_HANDOFF", "subject_ref": handoff, "work_state": row["state"],
            "depends_on_refs": list(row.get("payload_refs", [])), "owner_refs": [row["from_session_ref"], row["to_agent_or_owner_ref"]],
            "output_refs": [], "readback_refs": [], "source_refs": sources, "projection_only": True,
        })
        module_refs["agent_runtime"].append(handoff)
        module_refs["agent_runtime"].append(add_state(handoff, "AGENT_RUNTIME", f"HANDOFF:{row['state']}", sources, handoff, "AGENT_HANDOFF"))

    # Extend module binding set without changing Phase-1 rows.
    existing_modules = {row["module"] for row in kernel["module_bindings"]}
    for key in PHASE2_MODULES:
        header = projection["modules"][key]["header"]
        if header["module"] not in existing_modules:
            kernel["module_bindings"].append({
                "module": header["module"],
                "kernel_object_refs": sorted(set(module_refs[key])),
                "source_refs": list(header["source_refs"]),
                "projection_only": True,
            })

    kernel["identities"] = sorted(identities.values(), key=lambda row: row["identity_id"])
    # Phase-2 identity closure includes every evidence carrier referenced by Phase-1 or Phase-2 evidence rows.
    # This preserves source identity without claiming that the evidence itself is authoritative.
    for row in evidence_items:
        for ref in row.get("evidence_refs", []):
            ensure_identity(ref, "EVIDENCE", list(row.get("source_refs", [source_ref])))
    kernel["identities"] = sorted(identities.values(), key=lambda row: row["identity_id"])
    all_identity_refs = {row["canonical_ref"] for row in kernel["identities"]}
    referenced: set[str] = set()
    for row in relations:
        referenced |= {row["from_ref"], row["to_ref"]}
    for row in work_items:
        referenced.add(row["subject_ref"]); referenced.update(row["depends_on_refs"]); referenced.update(row["output_refs"]); referenced.update(row["readback_refs"])
    for row in evidence_items:
        referenced.add(row["subject_ref"]); referenced.update(row.get("evidence_refs", []))
    unresolved = len({ref for ref in referenced if ref and ref not in all_identity_refs and not ref.startswith("skill:") and not ref.startswith("review:") and not ref.startswith("agent:")})
    kernel["kernel_metrics"].update({
        "identity_count": len(kernel["identities"]),
        "state_fact_count": len(state_facts),
        "relation_count": len(relations),
        "phase2_module_binding_count": 4,
        "enterprise_module_binding_count": 8,
        "unresolved_identity_ref_count": unresolved,
    })
    return kernel


def main() -> int:
    parser = argparse.ArgumentParser(description="Build OLEANDER Enterprise Kernel v0.2 candidate with all eight enterprise modules.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--generated-at")
    args = parser.parse_args()
    projection = load_json(args.input)
    kernel = build_kernel_v0_2(projection, args.input.as_posix(), canonical_sha256(args.input), args.generated_at)
    payload = (json.dumps(kernel, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if not args.output.is_file() or args.output.read_bytes() != payload:
            args.output.write_bytes(payload)
        print(args.output)
    else:
        print(payload.decode("utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
