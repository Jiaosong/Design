from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


DOES_NOT_PROVE = [
    "DESIGN_KEEP",
    "PROFESSIONAL_PASS",
    "PROJECT_PROMOTION",
    "STATUTORY_APPROVAL",
    "KNOWLEDGE_CURRENT",
    "FIELD_TRUTH",
]

MODULE_BOUNDARIES = {
    "ERP": ["PROJECT_PROMOTION", "BUDGET_TRUTH", "PROFESSIONAL_PASS"],
    "PLM": ["TECHNICAL_CORRECTNESS", "DESIGN_KEEP", "PROJECT_PROMOTION"],
    "MES": ["PHYSICAL_EXECUTION", "FIELD_TRUTH", "ACCEPTANCE"],
    "BPM": ["PROFESSIONAL_STAGE_PASS", "DESIGN_KEEP", "PROJECT_PROMOTION"],
    "QMS": ["PROFESSIONAL_PASS", "STATUTORY_APPROVAL", "DESIGN_KEEP"],
    "MBSE": ["SYSTEMS_ENGINEERING_CURRENT", "VALIDATION_PASS", "PROJECT_ACCEPTANCE"],
    "KNOWLEDGE_GRAPH": ["KNOWLEDGE_CURRENT", "OE3", "CLAIM_TRUTH"],
    "AGENT_RUNTIME": ["AUTHORITY", "DESIGN_KEEP", "PROJECT_PROMOTION"],
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def canonical_text_sha256(path: Path) -> str:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest().upper()


def safe_token(value: str) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").upper()
    return token or "UNRESOLVED"


def module_header(module: str, source_ref: str, scope_state: str) -> dict:
    return {
        "module": module,
        "scope_state": scope_state,
        "authority_mode": "PROJECTION_ONLY",
        "source_refs": [source_ref],
        "does_not_prove": MODULE_BOUNDARIES[module],
    }


def work_package_state(master: dict) -> str:
    if master.get("open_blockers"):
        return "BLOCKED"
    dependency_states = {item.get("state") for item in master.get("dependencies", [])}
    if dependency_states & {"STALE", "REOPEN_REQUIRED", "HOLD"}:
        return "BLOCKED"
    if any(item.get("triggered") for item in master.get("reviews", [])):
        return "REVIEW"
    return "IN_PROGRESS"


def review_refs(master: dict, decision_object_id: str) -> list[dict]:
    rows: list[dict] = []
    for index, review in enumerate(master.get("reviews", []), start=1):
        independence = "NOT_REQUIRED" if not review.get("triggered") else "UNKNOWN"
        rows.append(
            {
                "review_id": f"ERP-REVIEW-{safe_token(decision_object_id)}-{index:02d}",
                "review_class": review["review_type"],
                "receipt_ref": review.get("receipt_ref"),
                "result": review["result"],
                "independence_state": independence,
            }
        )
    return rows


def change_disposition(change: dict) -> str:
    state = str(change.get("propagation_state", "")).upper()
    if state in {"APPLIED", "IMPLEMENTED"}:
        return "IMPLEMENTED_READBACK_PENDING"
    if state in {"CLOSED", "VERIFIED"}:
        return "CLOSED"
    if state in {"REJECTED"}:
        return "REJECTED"
    if state in {"HOLD", "BLOCKED"}:
        return "HOLD"
    return "OPEN"


def module_scope_counts(modules: dict) -> dict[str, int]:
    states = {"TRIGGERED": 0, "PARTIAL": 0, "NOT_TRIGGERED": 0, "HOLD": 0}
    for module in modules.values():
        scope_state = module.get("header", {}).get("scope_state")
        if scope_state not in states:
            raise ValueError(f"unsupported module scope_state: {scope_state}")
        states[scope_state] += 1
    return states


def enterprise_readiness_state(
    *,
    blocked: bool,
    modules: dict,
    unresolved_links: list[dict],
    reviews: list[dict],
) -> str:
    counts = module_scope_counts(modules)
    design_results = {
        item.get("result")
        for item in reviews
        if item.get("review_class") == "DESIGN"
    }
    if (
        blocked
        or counts["HOLD"] > 0
        or any(item.get("blocking") for item in unresolved_links)
        or bool(design_results & {"REVISE", "REJECT", "HOLD", "FAIL"})
    ):
        return "HOLD"
    if counts["PARTIAL"] > 0 or counts["NOT_TRIGGERED"] > 0:
        return "PARTIAL"
    return "READY_FOR_EVALUATION"


def build_projection(
    master: dict,
    source_ref: str,
    generated_at: str | None = None,
    source_sha256: str | None = None,
) -> dict:
    if master.get("kind") != "MASTER_RUNTIME_STATE":
        raise ValueError("input must be kind=MASTER_RUNTIME_STATE")

    project_id = master["project_id"]
    workstream_id = master.get("workstream_id")
    decision_object_id = master["decision_object_id"]
    wp_id = f"WP-{safe_token(project_id)}-{safe_token(decision_object_id)}"
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()

    project_axis_refs = [
        {
            "axis_level": "P2_PROJECT",
            "canonical_id": project_id,
            "canonical_ref": f"MASTER_RUNTIME_STATE:{project_id}",
        }
    ]
    if workstream_id:
        project_axis_refs.append(
            {
                "axis_level": "P3_WORKSTREAM",
                "canonical_id": workstream_id,
                "canonical_ref": f"MASTER_RUNTIME_STATE:{project_id}/{workstream_id}",
            }
        )

    reviews = review_refs(master, decision_object_id)
    review_ids = [r["review_id"] for r in reviews]
    dependencies = [item["object_id"] for item in master.get("dependencies", [])]

    work_package = {
        "work_package_id": wp_id,
        "project_id": project_id,
        "workstream_id": workstream_id,
        "decision_object_ids": [decision_object_id],
        "coordination_state": work_package_state(master),
        "required_native_outputs": [],
        "required_capability_roles": [],
        "depends_on": dependencies,
        "open_blockers": list(master.get("open_blockers", [])),
        "does_not_prove": ["PROJECT_PROMOTION", "DESIGN_KEEP", "PROFESSIONAL_PASS"],
    }

    relations = [
        {
            "relation_id": f"ENT-REL-{safe_token(decision_object_id)}-PROJECT-WP",
            "relation_type": "PROJECT_CONTAINS_WORK_PACKAGE",
            "from_ref": project_id,
            "to_ref": wp_id,
            "projection_only": True,
            "source_refs": [source_ref],
        },
        {
            "relation_id": f"ENT-REL-{safe_token(decision_object_id)}-WP-DECISION",
            "relation_type": "BOUND_TO_DECISION_OBJECT",
            "from_ref": wp_id,
            "to_ref": decision_object_id,
            "projection_only": True,
            "source_refs": [source_ref],
        },
        {
            "relation_id": f"ENT-REL-{safe_token(decision_object_id)}-WP-KNOWLEDGE",
            "relation_type": "SUPPORTED_BY_KNOWLEDGE",
            "from_ref": wp_id,
            "to_ref": master["knowledge_snapshot_ref"],
            "projection_only": True,
            "source_refs": [source_ref],
        },
        {
            "relation_id": f"ENT-REL-{safe_token(decision_object_id)}-CONFIGURES",
            "relation_type": "CONFIGURES",
            "from_ref": f"CI-{safe_token(decision_object_id)}",
            "to_ref": decision_object_id,
            "projection_only": True,
            "source_refs": [source_ref],
        },
    ]

    observations = []
    for change in master.get("change_events", []):
        observations.append(
            {
                "observation_id": f"ENT-OBS-{safe_token(change['change_id'])}",
                "observed_at": generated_at,
                "observation_type": "CONFIGURATION_OBSERVED",
                "subject_ref": change["change_id"],
                "source_refs": [source_ref],
                "projection_only": True,
                "rebuildable": True,
                "authority_effect": "NONE",
            }
        )

    blocked = bool(master.get("open_blockers")) or any(
        item.get("state") in {"STALE", "REOPEN_REQUIRED", "HOLD"}
        for item in master.get("dependencies", [])
    )

    professional_facet = {
        item["domain"]: {
            "state": item["state"],
            "verdict": item["verdict"],
            "claim_ceiling": item["claim_ceiling"],
        }
        for item in master.get("professional_processes", [])
    }

    qms_inspections = [
        {
            "inspection_id": f"QMS-{r['review_id']}",
            "subject_ref": decision_object_id,
            "inspection_class": "REVIEW_READBACK",
            "result": r["result"] if r["result"] in {"PASS", "KEEP", "REVISE", "REJECT", "HOLD", "FAIL", "NOT_RUN"} else "HOLD",
            "evidence_refs": [r["receipt_ref"]] if r.get("receipt_ref") else [],
            "source_refs": [source_ref],
        }
        for r in reviews
    ]

    kg_nodes = [
        {"node_id": f"KG-PROJECT-{safe_token(project_id)}", "node_class": "PROJECT", "canonical_ref": project_id, "source_refs": [source_ref], "authority_gain": False},
        {"node_id": f"KG-DECISION-{safe_token(decision_object_id)}", "node_class": "DECISION", "canonical_ref": decision_object_id, "source_refs": [source_ref], "authority_gain": False},
        {"node_id": f"KG-KNOWLEDGE-{safe_token(master['knowledge_snapshot_ref'])}", "node_class": "KNOWLEDGE", "canonical_ref": master["knowledge_snapshot_ref"], "source_refs": [source_ref], "authority_gain": False},
    ]
    kg_edges = [
        {"edge_id": f"KG-EDGE-{safe_token(decision_object_id)}-KNOWLEDGE", "predicate": "SUPPORTED_BY_KNOWLEDGE", "from_ref": decision_object_id, "to_ref": master["knowledge_snapshot_ref"], "source_refs": [source_ref], "projection_only": True, "authority_effect": "NONE"}
    ]

    modules = {
        "erp": {
            "header": module_header("ERP", source_ref, "TRIGGERED"),
            "demand_records": [
                {"demand_id": f"DEMAND-{safe_token(wp_id)}", "demand_class": "WORK", "subject_ref": wp_id, "quantity_state": "BOUNDED", "source_refs": [source_ref], "does_not_prove": ["BUDGET_TRUTH", "PROJECT_PROMOTION"]}
            ],
            "schedule_records": [
                {"schedule_id": f"SCHEDULE-{safe_token(wp_id)}", "subject_ref": wp_id, "schedule_state": "BLOCKED" if blocked else "ACTIVE", "depends_on": dependencies, "source_refs": [source_ref]}
            ],
            "resource_demand": [],
        },
        "plm": {
            "header": module_header("PLM", source_ref, "TRIGGERED"),
            "configuration_items": [
                {"item_id": f"CI-{safe_token(decision_object_id)}", "item_class": "DECISION_OBJECT", "canonical_ref": decision_object_id, "revision_ref": master["authority_snapshot_ref"], "lifecycle_state": "HOLD" if blocked else "WORKING", "source_refs": [source_ref], "does_not_prove": ["TECHNICAL_CORRECTNESS", "DESIGN_KEEP", "PROJECT_PROMOTION"]}
            ],
            "baselines": [
                {"baseline_id": f"BASELINE-{safe_token(decision_object_id)}", "member_refs": [decision_object_id], "baseline_state": "PROPOSED", "authority_ref": master["authority_snapshot_ref"], "source_refs": [source_ref]}
            ],
            "change_records": [
                {"change_id": c["change_id"], "change_class": "REVISION", "affected_refs": list(c.get("affected_refs", [])), "disposition": change_disposition(c), "reopen_refs": [], "source_refs": [source_ref]}
                for c in master.get("change_events", [])
            ],
        },
        "mes": {
            "header": module_header("MES", source_ref, "NOT_TRIGGERED"),
            "operation_records": [], "material_equipment_refs": [], "execution_readbacks": [],
        },
        "bpm": {
            "header": module_header("BPM", source_ref, "TRIGGERED"),
            "process_instances": [
                {"process_instance_id": f"PROC-{safe_token(project_id)}-{safe_token(decision_object_id)}", "process_ref": "00-governance/complex-project-master-runtime-v1.0.md", "subject_ref": decision_object_id, "process_state": "BLOCKED" if blocked else "ACTIVE", "current_node_ref": decision_object_id, "source_refs": [source_ref], "does_not_prove": ["PROFESSIONAL_STAGE_PASS", "DESIGN_KEEP", "PROJECT_PROMOTION"]}
            ],
            "handoffs": [],
            "exceptions": [
                {"exception_id": f"EXC-{safe_token(b)}", "subject_ref": wp_id, "exception_class": "BLOCKER", "disposition": "OPEN", "source_refs": [source_ref]}
                for b in master.get("open_blockers", [])
            ],
        },
        "qms": {
            "header": module_header("QMS", source_ref, "TRIGGERED" if reviews else "NOT_TRIGGERED"),
            "quality_plans": [
                {"quality_plan_id": f"QPLAN-{safe_token(decision_object_id)}", "subject_ref": decision_object_id, "acceptance_criteria_refs": [], "review_refs": review_ids, "source_refs": [source_ref]}
            ] if reviews else [],
            "nonconformances": [], "capa_records": [], "inspection_records": qms_inspections,
        },
        "mbse": {
            "header": module_header("MBSE", source_ref, "PARTIAL"),
            "requirements": [],
            "system_elements": [
                {"element_id": f"SYS-ELEM-{safe_token(decision_object_id)}", "element_class": "DECISION_OBJECT", "canonical_ref": decision_object_id, "source_refs": [source_ref]}
            ],
            "interfaces": [], "verification_validation": [],
            "configuration_baselines": [f"BASELINE-{safe_token(decision_object_id)}"],
        },
        "knowledge_graph": {
            "header": module_header("KNOWLEDGE_GRAPH", source_ref, "TRIGGERED"),
            "nodes": kg_nodes, "edges": kg_edges,
            "provenance_records": [
                {"provenance_id": f"PROV-{safe_token(decision_object_id)}", "entity_ref": decision_object_id, "derived_from_refs": [master["knowledge_snapshot_ref"], master["authority_snapshot_ref"]], "generated_by_ref": source_ref, "attributed_to_refs": [], "source_refs": [source_ref]}
            ],
            "query_policies": [
                {"policy_id": "KG-POLICY-TASK-CLAIM", "query_scope": "TASK_CLAIM_SCOPED_ONLY", "eligibility_rule_ref": "00-governance/runtime/OLEANDER_EXISTING_KNOWLEDGE_MOUNT_v1.0.json", "claim_ceiling_rule_ref": "00-governance/runtime/OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json", "source_refs": [source_ref]}
            ],
        },
        "agent_runtime": {
            "header": module_header("AGENT_RUNTIME", source_ref, "NOT_TRIGGERED"),
            "sessions": [], "leases": [], "actions": [], "handoffs": [],
        },
    }

    unresolved_links = []
    if not master.get("professional_processes"):
        unresolved_links.append({"link_id": f"UNRES-{safe_token(decision_object_id)}-PROFESSIONAL", "from_ref": decision_object_id, "expected_relation_type": "VERIFIES", "reason": "No professional process instance is present in the source master runtime snapshot.", "blocking": False})

    counts = module_scope_counts(modules)
    module_count = len(modules)
    source_bound_count = sum(
        1 for module in modules.values() if module.get("header", {}).get("source_refs")
    )
    readiness = enterprise_readiness_state(
        blocked=blocked,
        modules=modules,
        unresolved_links=unresolved_links,
        reviews=reviews,
    )

    return {
        "schema_version": "0.3.1-candidate",
        "kind": "OLEANDER_ENTERPRISE_ORCHESTRATION_PROJECTION",
        "candidate_status": "EVAL_ONLY",
        "generated_at": generated_at,
        "authority": {
            "architecture_ref": "00-governance/runtime/OLEANDER_CURRENT_ARCHITECTURE_MAP_v2.1.md",
            "master_runtime_ref": source_ref,
            "authority_snapshot_ref": master["authority_snapshot_ref"],
            "knowledge_snapshot_ref": master["knowledge_snapshot_ref"],
            "source_binding_refs": [source_ref],
            "source_binding_digests": [
                {
                    "ref": source_ref,
                    "sha256": source_sha256 or "0" * 64,
                    "hash_semantics": "UTF8_TEXT_LF_CANONICAL_V1",
                }
            ],
            "source_binding_hash_semantics": "SOURCE_SPECIFIC_EXACT_REVISION_DIGESTS_WHEN_AVAILABLE",
            "projection_only": True,
            "may_mutate_current": False,
        },
        "architecture_contract": {
            "integration_model": "FEDERATED_PROJECTION_ENVELOPE",
            "module_count": 8,
            "no_new_runtime_layer": True,
            "state_policy": "ORTHOGONAL_STATE_FAMILIES_NO_FLATTENING",
            "identity_policy": "CANONICAL_REF_REQUIRED_NO_ID_SYNTHESIS_AS_AUTHORITY",
            "write_policy": "READ_ONLY_CANDIDATE_EXISTING_AUTHORIZED_PATHS_ONLY_AFTER_ADOPTION",
            "transaction_policy": "NO_DISTRIBUTED_TRANSACTION_MANAGER_RECONCILE_PARTIAL_SIDE_EFFECTS",
            "digital_thread_policy": "TYPED_SOURCE_BOUND_LINKS_DO_NOT_TRANSFER_AUTHORITY",
        },
        "case_refs": [],
        "project_axis_refs": project_axis_refs,
        "work_packages": [work_package],
        "jobs": [],
        "resource_refs": [],
        "artifact_refs": [],
        "review_refs": reviews,
        "modules": modules,
        "digital_thread": {
            "relations": relations,
            "trace_queries": [
                {"query_id": f"TRACE-{safe_token(decision_object_id)}-KNOWLEDGE", "question": "Can the decision object be traced to its current knowledge and authority snapshots?", "required_relation_types": ["SUPPORTED_BY_KNOWLEDGE", "CONFIGURES"], "result_state": "PARTIAL", "source_refs": [source_ref]}
            ],
            "unresolved_links": unresolved_links,
        },
        "state_facets": {
            "project_design": {}, "job": {}, "knowledge_integrity": {}, "operational_eligibility": {},
            "design_quality": {decision_object_id: {"state": master["design_quality_development"]["state"], "verdict": master["design_quality_development"]["verdict"], "maturity": master["design_quality_development"]["maturity"], "claim_ceiling": master["design_quality_development"]["claim_ceiling"]}},
            "professional": professional_facet,
            "interface": {decision_object_id: {"state": master["integration"]["state"], "verdict": master["integration"]["verdict"], "open_major_critical_interfaces": master["integration"]["open_major_critical_interfaces"], "unresolved_authority_conflicts": master["integration"]["unresolved_authority_conflicts"]}},
            "authority": {decision_object_id: {"authority_snapshot_ref": master["authority_snapshot_ref"]}},
            "evidence": {},
            "configuration": {decision_object_id: "HOLD" if blocked else "WORKING"},
            "quality": {decision_object_id: "REVIEW" if reviews else "NOT_TRIGGERED"},
            "process": {decision_object_id: "BLOCKED" if blocked else "ACTIVE"},
            "agent_runtime": {},
        },
        "activity_observations": observations,
        "reconciliation": {
            "projection_freshness_state": "SOURCE_READBACK_CURRENT",
            "enterprise_readiness_state": readiness,
            "drift_state": "UNKNOWN",
            "source_readback_refs": [source_ref],
            "partial_side_effect_state": "NONE",
            "reconciliation_actions": [],
            "advance_allowed": False,
        },
        "control_metrics": {
            "authority_duplication_count": 0,
            "state_family_flattening_count": 0,
            "untraceable_relation_count": 0,
            "unresolved_blocking_link_count": sum(1 for x in unresolved_links if x["blocking"]),
            "module_source_binding_coverage": source_bound_count / module_count,
            "module_triggered_coverage": counts["TRIGGERED"] / module_count,
            "module_scope_counts": counts,
            "projection_rebuildable": True,
        },
        "does_not_prove": DOES_NOT_PROVE,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a read-only OLEANDER enterprise orchestration candidate projection from MASTER_RUNTIME_STATE.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--generated-at", type=str, help="Optional fixed timestamp for deterministic evaluation output.")
    args = parser.parse_args()

    master = load_json(args.input)
    projection = build_projection(
        master,
        args.input.as_posix(),
        generated_at=args.generated_at,
        source_sha256=canonical_text_sha256(args.input),
    )
    payload = (json.dumps(projection, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

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
