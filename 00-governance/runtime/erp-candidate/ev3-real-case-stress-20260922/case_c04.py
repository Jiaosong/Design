from __future__ import annotations

from pathlib import Path

from ev3_common import base_projection, finish_projection, header, load_json


REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_SPECS = [
    ("EV3SRC:C04:CURRENT", REPO_ROOT / r"05-cases\c04-qingjiang-stone-book\C04_CURRENT.md", "GIT_MAIN_EXACT", "GIT_CANONICAL_BLOB_SHA256"),
    ("EV3SRC:C04:PROJECT_CONTROL", REPO_ROOT / r"05-cases\c04-qingjiang-stone-book\project-control\v0.1\C04_PROJECT_CONTROL_READBACK_v0.1.json", "GIT_MAIN_EXACT", "GIT_CANONICAL_BLOB_SHA256"),
    ("EV3SRC:C04:CLOSURE", REPO_ROOT / r"05-cases\c04-qingjiang-stone-book\project-control\v0.1\C04_PROJECT_CLOSURE_COMPILATION_READBACK_v0.1.json", "GIT_MAIN_EXACT", "GIT_CANONICAL_BLOB_SHA256"),
    ("EV3SRC:C04:OPERATIONAL", REPO_ROOT / r"05-cases\c04-qingjiang-stone-book\project-control\v0.1\C04_PROJECT_OPERATIONAL_ACCEPTANCE_COMPILATION_v0.1.json", "GIT_MAIN_EXACT", "GIT_CANONICAL_BLOB_SHA256"),
    ("EV3SRC:C04:TD_BINDING", REPO_ROOT / r"05-cases\c04-qingjiang-stone-book\project-control\v0.1\C04_TECHNICAL_DRAWING_SPECIALIST_BINDING_v0.1.json", "GIT_MAIN_EXACT", "GIT_CANONICAL_BLOB_SHA256"),
]


def build_projection(source_rows: list[dict], template_path: Path) -> dict:
    control = load_json(SOURCE_SPECS[1][1])
    closure = load_json(SOURCE_SPECS[2][1])
    ops = load_json(SOURCE_SPECS[3][1])
    td = load_json(SOURCE_SPECS[4][1])
    assert control["project_id"] == "PRJ-C04-QINGJIANG-SHISHU"
    assert control["overall_project_promotion"] == "HOLD"
    assert control["control_results"]["configuration_change"].startswith("PASS")
    assert control["control_results"]["risk_hazard"].startswith("PASS")
    assert control["control_results"]["operational_acceptance"] == "HOLD"
    assert control["control_results"]["technical_drawing_specialist_binding"] == "HOLD"
    assert closure["source_integrity_state"] == "PASS"
    assert closure["schema_validation_state"] == "PASS"
    assert closure["pass_readiness"] == "NOT_REQUESTED"
    assert ops["status"] == "HOLD" and ops["operational_verdict"] == "HOLD"
    assert not ops["operational_readback_refs"]
    assert td["status"] == "HOLD" and td["owner_kind"] == "NOT_ASSIGNED"
    assert td["authorization_state"] == "NOT_ASSIGNED" and td["binding_verdict"] == "HOLD"

    d = base_projection(template_path, "C04", source_rows)
    sr = [row["ref"] for row in source_rows]
    pid = "PRJ-C04-QINGJIANG-SHISHU"
    ws = "C04-PROJECT-CONTROL"
    wp = "WP-PRJ-C04-QINGJIANG-SHISHU-CLOSURE"
    job = "JOB-C04-PROJECT-CONTROL-READBACK"
    artifact = "ARTIFACT-C04-PROJECT-CONTROL-READBACK"
    review = "REVIEW-C04-PROJECT-CLOSURE"
    req = "REQ-C04-OPERATIONAL-TD-CLOSURE"

    d["case_refs"] = [{"canonical_case_id": "C04", "canonical_ref": "05-cases/c04-qingjiang-stone-book", "project_binding_state": "BOUND", "does_not_prove": ["P2_PROJECT_ID"]}]
    d["project_axis_refs"] = [
        {"axis_level": "P2_PROJECT", "canonical_id": pid, "canonical_ref": "05-cases/c04-qingjiang-stone-book/C04_CURRENT.md"},
        {"axis_level": "P3_WORKSTREAM", "canonical_id": ws, "canonical_ref": "05-cases/c04-qingjiang-stone-book/project-control/v0.1"},
    ]
    d["work_packages"] = [{
        "work_package_id": wp, "project_id": pid, "workstream_id": ws, "decision_object_ids": ["C04-PROJECT-CLOSURE"], "coordination_state": "BLOCKED",
        "required_native_outputs": list(td["required_native_outputs"]), "required_capability_roles": ["PROJECT_CONTROL", "TECHNICAL_DRAWING_SPECIALIST", "OPERATIONAL_ACCEPTANCE"],
        "depends_on": [req], "open_blockers": ["FIELD_OBSERVED_0", "FIELD_MEASURED_0", "OPERATIONAL_ACCEPTANCE_HOLD", "TECHNICAL_DRAWING_OWNER_NOT_ASSIGNED"],
        "does_not_prove": ["PROJECT_PROMOTION", "DESIGN_KEEP", "PROFESSIONAL_PASS"],
    }]
    d["jobs"] = [{
        "job_id": job, "work_package_id": wp, "job_state": "SUCCEEDED", "primary_owner_ref": "project-control:compiler",
        "capability_refs": ["capability:PROJECT_CONTROL_READBACK"], "tool_adapter_refs": [], "input_refs": [req], "output_refs": [artifact],
        "readback_refs": ["EV3SRC:C04:PROJECT_CONTROL", "EV3SRC:C04:CLOSURE"], "claim_ceiling": control["claim_ceiling"],
        "does_not_prove": ["DESIGN_KEEP", "PROFESSIONAL_PASS", "PROJECT_PROMOTION"],
    }]
    d["artifact_refs"] = [{"artifact_id": artifact, "canonical_ref": "05-cases/c04-qingjiang-stone-book/project-control/v0.1/C04_PROJECT_CONTROL_READBACK_v0.1.json", "native_format": "json", "editable_state": "EDITABLE", "hash_or_commit": source_rows[1]["sha256"], "readback_refs": ["EV3SRC:C04:PROJECT_CONTROL"]}]
    d["review_refs"] = [{"review_id": review, "review_class": "DESIGN", "receipt_ref": "C04_PROJECT_CONTROL_READBACK_v0.1", "result": "HOLD", "independence_state": "UNKNOWN"}]

    d["modules"] = {
        "erp": {"header": header("ERP", "PARTIAL", sr, ["PROJECT_PROMOTION", "BUDGET_TRUTH", "PROFESSIONAL_PASS"]), "demand_records": [], "schedule_records": [], "resource_demand": []},
        "plm": {"header": header("PLM", "TRIGGERED", sr, ["TECHNICAL_CORRECTNESS", "DESIGN_KEEP", "PROJECT_PROMOTION"]), "configuration_items": [{"item_id": "CI-C04-CONTROL", "item_class": "ARTIFACT", "canonical_ref": artifact, "revision_ref": source_rows[1]["sha256"], "lifecycle_state": "RELEASED", "source_refs": sr, "does_not_prove": ["TECHNICAL_CORRECTNESS", "DESIGN_KEEP", "PROJECT_PROMOTION"]}], "baselines": [{"baseline_id": "BASELINE-C04-CONTROL", "member_refs": ["CI-C04-CONTROL", req], "baseline_state": "RELEASED", "authority_ref": "EV3SRC:C04:CURRENT", "source_refs": sr}], "change_records": []},
        "mes": {"header": header("MES", "NOT_TRIGGERED", sr, ["PHYSICAL_EXECUTION", "FIELD_TRUTH", "ACCEPTANCE"]), "operation_records": [], "material_equipment_refs": [], "execution_readbacks": []},
        "bpm": {"header": header("BPM", "HOLD", sr, ["PROFESSIONAL_STAGE_PASS", "DESIGN_KEEP", "PROJECT_PROMOTION"]), "process_instances": [{"process_instance_id": "PROC-C04-CLOSURE", "process_ref": "00-governance/complex-project-master-runtime-v1.0.md", "subject_ref": wp, "process_state": "HOLD", "current_node_ref": review, "source_refs": sr, "does_not_prove": ["PROFESSIONAL_STAGE_PASS", "DESIGN_KEEP", "PROJECT_PROMOTION"]}], "handoffs": [], "exceptions": []},
        "qms": {"header": header("QMS", "HOLD", sr, ["PROFESSIONAL_PASS", "STATUTORY_APPROVAL", "DESIGN_KEEP"]), "quality_plans": [{"quality_plan_id": "QPLAN-C04-CLOSURE", "subject_ref": wp, "acceptance_criteria_refs": [req], "review_refs": [review], "source_refs": sr}], "nonconformances": [{"ncr_id": "NCR-C04-OP-CLOSEOUT", "subject_ref": artifact, "severity": "HIGH", "state": "OPEN", "containment_ref": "EV3SRC:C04:OPERATIONAL", "disposition_ref": "OWNER_NOT_ASSIGNED", "source_refs": sr}], "capa_records": [], "inspection_records": [{"inspection_id": "INSP-C04-CONFIG", "subject_ref": artifact, "inspection_class": "REVIEW_READBACK", "result": "PASS", "evidence_refs": ["EV3SRC:C04:PROJECT_CONTROL"], "source_refs": sr}, {"inspection_id": "INSP-C04-OPERATIONAL", "subject_ref": artifact, "inspection_class": "COMMISSIONING", "result": "HOLD", "evidence_refs": ["EV3SRC:C04:OPERATIONAL"], "source_refs": sr}, {"inspection_id": "INSP-C04-TD-BINDING", "subject_ref": artifact, "inspection_class": "TECHNICAL", "result": "HOLD", "evidence_refs": ["EV3SRC:C04:TD_BINDING"], "source_refs": sr}]},
        "mbse": {"header": header("MBSE", "PARTIAL", sr, ["SYSTEMS_ENGINEERING_CURRENT", "VALIDATION_PASS", "PROJECT_ACCEPTANCE"]), "requirements": [{"requirement_id": req, "requirement_class": "ACCEPTANCE_CRITERION", "statement_ref": "C04:FIELD+OPERATIONAL+TD:CLOSURE", "status": "HOLD", "allocated_to_refs": [artifact], "verification_method": "REVIEW", "source_refs": sr, "does_not_prove": ["VALIDATION_PASS", "PROJECT_ACCEPTANCE"]}], "system_elements": [{"element_id": "SYS-C04-CLOSURE", "element_class": "WORK_PRODUCT", "canonical_ref": artifact, "source_refs": sr}], "interfaces": [{"interface_id": "IF-C04-OP-TD", "from_ref": req, "to_ref": artifact, "interface_state": "HOLD", "verification_refs": ["VV-C04-OP", "VV-C04-TD"], "source_refs": sr}], "verification_validation": [{"vv_id": "VV-C04-OP", "subject_ref": req, "vv_class": "VALIDATION", "method": "FIELD_COMMISSIONING", "result": "NOT_RUN", "evidence_refs": [], "independent_review_ref": None, "source_refs": sr}, {"vv_id": "VV-C04-TD", "subject_ref": req, "vv_class": "VERIFICATION", "method": "SPECIALIST_OWNER_BINDING", "result": "HOLD", "evidence_refs": ["EV3SRC:C04:TD_BINDING"], "independent_review_ref": None, "source_refs": sr}], "configuration_baselines": ["BASELINE-C04-CONTROL"]},
        "knowledge_graph": {"header": header("KNOWLEDGE_GRAPH", "TRIGGERED", sr, ["KNOWLEDGE_CURRENT", "OE3", "CLAIM_TRUTH"]), "nodes": [{"node_id": "KG-C04-PROJECT", "node_class": "PROJECT", "canonical_ref": pid, "source_refs": sr, "authority_gain": False}, {"node_id": "KG-C04-REQ", "node_class": "REQUIREMENT", "canonical_ref": req, "source_refs": sr, "authority_gain": False}, {"node_id": "KG-C04-ART", "node_class": "ARTIFACT", "canonical_ref": artifact, "source_refs": sr, "authority_gain": False}], "edges": [{"edge_id": "KG-C04-IMPLEMENTS", "predicate": "IMPLEMENTS", "from_ref": artifact, "to_ref": req, "source_refs": sr, "projection_only": True, "authority_effect": "NONE"}], "provenance_records": [{"provenance_id": "PROV-C04-CONTROL", "entity_ref": artifact, "derived_from_refs": [req], "generated_by_ref": job, "attributed_to_refs": ["project-control:compiler"], "source_refs": sr}], "query_policies": [{"policy_id": "KG-C04-EV3", "query_scope": "TASK_CLAIM_SCOPED_ONLY", "eligibility_rule_ref": "OE-policy", "claim_ceiling_rule_ref": "claim-ceiling-policy", "source_refs": sr}]},
        "agent_runtime": {"header": header("AGENT_RUNTIME", "NOT_TRIGGERED", sr, ["AUTHORITY", "DESIGN_KEEP", "PROJECT_PROMOTION"]), "sessions": [], "leases": [], "actions": [], "handoffs": []},
    }
    d["digital_thread"]["relations"] = [
        {"relation_id": "REL-C04-PROJECT-WP", "relation_type": "PROJECT_CONTAINS_WORK_PACKAGE", "from_ref": pid, "to_ref": wp, "projection_only": True, "source_refs": sr},
        {"relation_id": "REL-C04-JOB-WP", "relation_type": "JOB_EXECUTES_WORK_PACKAGE", "from_ref": job, "to_ref": wp, "projection_only": True, "source_refs": sr},
        {"relation_id": "REL-C04-JOB-ART", "relation_type": "JOB_PRODUCES_ARTIFACT", "from_ref": job, "to_ref": artifact, "projection_only": True, "source_refs": sr},
        {"relation_id": "REL-C04-ART-REV", "relation_type": "ARTIFACT_REVIEWED_BY", "from_ref": artifact, "to_ref": review, "projection_only": True, "source_refs": sr},
        {"relation_id": "REL-C04-ART-REQ", "relation_type": "IMPLEMENTS", "from_ref": artifact, "to_ref": req, "projection_only": True, "source_refs": sr},
    ]
    d["digital_thread"]["unresolved_links"] = [
        {"link_id": "UNRES-C04-OP-OWNER", "from_ref": artifact, "expected_relation_type": "HANDOFF_TO", "reason": "Operational/implementation owner not assigned; commissioning and field readback are deferred.", "blocking": True},
        {"link_id": "UNRES-C04-TD-OWNER", "from_ref": artifact, "expected_relation_type": "HANDOFF_TO", "reason": "Technical Drawing specialist owner and authorization are NOT_ASSIGNED.", "blocking": True},
    ]
    d["state_facets"].update({
        "project_design": {pid: "EXPLORE_G3"}, "job": {job: "SUCCEEDED"}, "knowledge_integrity": {"EV3:C04:SOURCE_MANIFEST": "SOURCE_BOUND"}, "operational_eligibility": {pid: "HOLD_G1F_FIELD_OBSERVED_0_MEASURED_0"},
        "design_quality": {artifact: "HOLD_PROJECT_CLOSURE"}, "professional": {pid: "HOLD_OPERATIONAL_AND_TD"}, "interface": {req: "HOLD_OWNER_AND_FIELD_READBACK_OPEN"},
        "authority": {req: "HOLD_TECHNICAL_DRAWING_OWNER_NOT_ASSIGNED"}, "evidence": {artifact: "CONFIG_AND_RISK_BOUNDED_PASS"}, "configuration": {artifact: "RELEASED_AT_CONFIGURATION_CLAIM_ONLY"},
        "quality": {artifact: "HOLD_OPERATIONAL_ACCEPTANCE"}, "process": {wp: "HOLD"}, "agent_runtime": {pid: "NOT_TRIGGERED"},
    })
    return finish_projection(d)
