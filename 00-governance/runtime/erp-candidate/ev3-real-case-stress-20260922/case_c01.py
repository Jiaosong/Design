from __future__ import annotations

from pathlib import Path

from ev3_common import base_projection, finish_projection, header, load_json


LOCAL_ROOT = Path(r"D:\Desgin")
SOURCE_SPECS = [
    ("EV3SRC:C01:AUTHORITY", LOCAL_ROOT / r"05-cases\c01-yimai-guangdu\presentation\route-rebuild_v0.1\detail-design-successor-r1.7_v0.1\runtime-v0.1\C01_DD_R17_R-A_AUTHORITY_SNAPSHOT_v0.1.json", "LOCAL_CURRENT_UNTRACKED", "UTF8_TEXT_LF_CANONICAL_V1"),
    ("EV3SRC:C01:CHECKPOINT", LOCAL_ROOT / r"05-cases\c01-yimai-guangdu\presentation\route-rebuild_v0.1\detail-design-successor-r1.7_v0.1\C01_DD_R17_OLEANDER_CHECKPOINT_v0.1.json", "LOCAL_CURRENT_UNTRACKED", "UTF8_TEXT_LF_CANONICAL_V1"),
    ("EV3SRC:C01:FINAL_READBACK", LOCAL_ROOT / r"05-cases\c01-yimai-guangdu\presentation\route-rebuild_v0.1\detail-design-successor-r1.7_v0.1\C01_DD_R17_FINAL_READBACK_v0.4.json", "LOCAL_CURRENT_UNTRACKED", "UTF8_TEXT_LF_CANONICAL_V1"),
    ("EV3SRC:C01:DOWNSTREAM", LOCAL_ROOT / r"05-cases\c01-yimai-guangdu\presentation\route-rebuild_v0.1\presentation-successor-from-upstream_v0.3\C01_DOWNSTREAM_SUCCESSOR_CHECKPOINT_v0.3.json", "LOCAL_CURRENT_UNTRACKED", "UTF8_TEXT_LF_CANONICAL_V1"),
    ("EV3SRC:C01:FREEZE", LOCAL_ROOT / r"05-cases\c01-yimai-guangdu\presentation\route-rebuild_v0.1\presentation-successor-from-upstream_v0.3\C01_SUCCESSOR_FREEZE_READBACK_v0.3.json", "LOCAL_CURRENT_UNTRACKED", "UTF8_TEXT_LF_CANONICAL_V1"),
]


def build_projection(source_rows: list[dict], template_path: Path) -> dict:
    authority = load_json(SOURCE_SPECS[0][1])
    checkpoint = load_json(SOURCE_SPECS[1][1])
    final = load_json(SOURCE_SPECS[2][1])
    downstream = load_json(SOURCE_SPECS[3][1])
    freeze = load_json(SOURCE_SPECS[4][1])
    assert authority["project_id"] == "PRJ-C01-YIMAI-GUANGDU"
    assert authority["authority_decisions"]["no_second_authority"] is True
    assert authority["authority_decisions"]["promotion"] is False
    assert checkpoint["professional_verdict"] == "NOT_RUN"
    assert checkpoint["integration_verdict"] == "NOT_RUN"
    assert checkpoint["design_keep"] is False and checkpoint["promotion"] is False
    assert final["machine_verdict"] == "PASS" and final["promotion"] is False
    assert "FIELD-UNVERIFIED" in final["maturity"]
    assert "DO NOT CONVERT TO KEEP" in final["independent_professional_review"]
    assert downstream["promotion"] is False and downstream["current_pointer_changed"] is False
    assert freeze["verdict"] == "PASS" and freeze["fail_count"] == 0

    d = base_projection(template_path, "C01", source_rows)
    sr = [row["ref"] for row in source_rows]
    pid = "PRJ-C01-YIMAI-GUANGDU"
    ws = "C01-R17-DETAIL-DESIGN"
    wp = "WP-PRJ-C01-YIMAI-GUANGDU-R17-DD"
    job = "JOB-C01-R17-PRODUCER-READBACK"
    artifact = "ARTIFACT-C01-R17-DD-PACKAGE"
    review = "REVIEW-C01-R17-INDEPENDENT-PROFESSIONAL"
    req = "REQ-C01-R17-FIELD-ENGINEERING-GATES"

    d["case_refs"] = [{"canonical_case_id": "C01", "canonical_ref": "05-cases/c01-yimai-guangdu", "project_binding_state": "BOUND", "does_not_prove": ["P2_PROJECT_ID"]}]
    d["project_axis_refs"] = [
        {"axis_level": "P2_PROJECT", "canonical_id": pid, "canonical_ref": "local-current:C01:R-A-authority-snapshot"},
        {"axis_level": "P3_WORKSTREAM", "canonical_id": ws, "canonical_ref": "local-current:C01:R17"},
    ]
    d["work_packages"] = [{
        "work_package_id": wp, "project_id": pid, "workstream_id": ws,
        "decision_object_ids": ["C01-R17-DETAIL-SYSTEM"], "coordination_state": "BLOCKED",
        "required_native_outputs": [artifact],
        "required_capability_roles": ["NATIVE_DETAIL_PRODUCTION", "INDEPENDENT_PROFESSIONAL_REVIEW", "FIELD_VERIFICATION"],
        "depends_on": [req], "open_blockers": list(final["external_gates_not_design_gaps"]),
        "does_not_prove": ["PROJECT_PROMOTION", "DESIGN_KEEP", "PROFESSIONAL_PASS"],
    }]
    d["jobs"] = [{
        "job_id": job, "work_package_id": wp, "job_state": "SUCCEEDED", "primary_owner_ref": "producer:C01-R17",
        "capability_refs": ["capability:NATIVE_DETAIL_PRODUCTION"], "tool_adapter_refs": [], "input_refs": [req], "output_refs": [artifact],
        "readback_refs": ["EV3SRC:C01:FINAL_READBACK"], "claim_ceiling": "MACHINE_READBACK_PASS_FIELD_AND_PROFESSIONAL_GATES_OPEN",
        "does_not_prove": ["DESIGN_KEEP", "PROFESSIONAL_PASS", "PROJECT_PROMOTION"],
    }]
    d["artifact_refs"] = [{
        "artifact_id": artifact, "canonical_ref": "local-current:C01:R17-detail-package", "native_format": "SVG_CSV_JSON_PACKAGE", "editable_state": "EDITABLE",
        "hash_or_commit": source_rows[2]["sha256"], "readback_refs": ["EV3SRC:C01:FINAL_READBACK"],
    }]
    d["review_refs"] = [{"review_id": review, "review_class": "DESIGN", "receipt_ref": "NOT_AVAILABLE:C01:R17:INDEPENDENT_PROFESSIONAL_REVIEW", "result": "HOLD", "independence_state": "UNKNOWN"}]

    d["modules"] = {
        "erp": {"header": header("ERP", "PARTIAL", sr, ["PROJECT_PROMOTION", "BUDGET_TRUTH", "PROFESSIONAL_PASS"]), "demand_records": [], "schedule_records": [], "resource_demand": []},
        "plm": {"header": header("PLM", "TRIGGERED", sr, ["TECHNICAL_CORRECTNESS", "DESIGN_KEEP", "PROJECT_PROMOTION"]), "configuration_items": [{"item_id": "CI-C01-R17-DD", "item_class": "ARTIFACT", "canonical_ref": artifact, "revision_ref": source_rows[2]["sha256"], "lifecycle_state": "REVIEW", "source_refs": sr, "does_not_prove": ["TECHNICAL_CORRECTNESS", "DESIGN_KEEP", "PROJECT_PROMOTION"]}], "baselines": [{"baseline_id": "BASELINE-C01-R17", "member_refs": ["CI-C01-R17-DD", req], "baseline_state": "HOLD", "authority_ref": "EV3SRC:C01:AUTHORITY", "source_refs": sr}], "change_records": []},
        "mes": {"header": header("MES", "TRIGGERED", sr, ["PHYSICAL_EXECUTION", "FIELD_TRUTH", "ACCEPTANCE"]), "operation_records": [{"operation_id": "OP-C01-R17-DIGITAL-NATIVE", "work_package_id": wp, "operation_class": "DIGITAL_NATIVE_EXECUTION", "execution_state": "COMPLETE", "resource_refs": [], "input_refs": [req], "output_refs": [artifact], "actual_readback_refs": ["EV3SRC:C01:FINAL_READBACK"], "source_refs": sr, "does_not_prove": ["PHYSICAL_EXECUTION", "FIELD_TRUTH", "ACCEPTANCE"]}], "material_equipment_refs": [], "execution_readbacks": [{"canonical_ref": "EV3SRC:C01:FINAL_READBACK", "source_refs": sr, "authority_owner": "Actual Readback", "projection_only": True}]},
        "bpm": {"header": header("BPM", "HOLD", sr, ["PROFESSIONAL_STAGE_PASS", "DESIGN_KEEP", "PROJECT_PROMOTION"]), "process_instances": [{"process_instance_id": "PROC-C01-R17", "process_ref": "local-current:C01:R17-runtime", "subject_ref": wp, "process_state": "HOLD", "current_node_ref": review, "source_refs": sr, "does_not_prove": ["PROFESSIONAL_STAGE_PASS", "DESIGN_KEEP", "PROJECT_PROMOTION"]}], "handoffs": [], "exceptions": []},
        "qms": {"header": header("QMS", "HOLD", sr, ["PROFESSIONAL_PASS", "STATUTORY_APPROVAL", "DESIGN_KEEP"]), "quality_plans": [{"quality_plan_id": "QPLAN-C01-R17", "subject_ref": wp, "acceptance_criteria_refs": [req], "review_refs": [review], "source_refs": sr}], "nonconformances": [], "capa_records": [], "inspection_records": [{"inspection_id": "INSP-C01-R17-MACHINE", "subject_ref": artifact, "inspection_class": "REVIEW_READBACK", "result": "PASS", "evidence_refs": ["EV3SRC:C01:FINAL_READBACK", "EV3SRC:C01:FREEZE"], "source_refs": sr}, {"inspection_id": "INSP-C01-R17-PROFESSIONAL", "subject_ref": artifact, "inspection_class": "QUALITY", "result": "HOLD", "evidence_refs": ["EV3SRC:C01:CHECKPOINT"], "source_refs": sr}]},
        "mbse": {"header": header("MBSE", "PARTIAL", sr, ["SYSTEMS_ENGINEERING_CURRENT", "VALIDATION_PASS", "PROJECT_ACCEPTANCE"]), "requirements": [{"requirement_id": req, "requirement_class": "DESIGN_REQUIREMENT", "statement_ref": "C01:R17:external_gates_not_design_gaps", "status": "HOLD", "allocated_to_refs": [artifact], "verification_method": "REVIEW", "source_refs": sr, "does_not_prove": ["VALIDATION_PASS", "PROJECT_ACCEPTANCE"]}], "system_elements": [{"element_id": "SYS-C01-R17-DD", "element_class": "WORK_PRODUCT", "canonical_ref": artifact, "source_refs": sr}], "interfaces": [], "verification_validation": [{"vv_id": "VV-C01-R17-FIELD", "subject_ref": req, "vv_class": "VALIDATION", "method": "FIELD_MEASUREMENT_AND_SPECIALIST_REVIEW", "result": "NOT_RUN", "evidence_refs": [], "independent_review_ref": None, "source_refs": sr}], "configuration_baselines": ["BASELINE-C01-R17"]},
        "knowledge_graph": {"header": header("KNOWLEDGE_GRAPH", "TRIGGERED", sr, ["KNOWLEDGE_CURRENT", "OE3", "CLAIM_TRUTH"]), "nodes": [{"node_id": "KG-C01-PROJECT", "node_class": "PROJECT", "canonical_ref": pid, "source_refs": sr, "authority_gain": False}, {"node_id": "KG-C01-ARTIFACT", "node_class": "ARTIFACT", "canonical_ref": artifact, "source_refs": sr, "authority_gain": False}, {"node_id": "KG-C01-REQ", "node_class": "REQUIREMENT", "canonical_ref": req, "source_refs": sr, "authority_gain": False}], "edges": [{"edge_id": "KG-C01-SATISFIES", "predicate": "SATISFIES", "from_ref": artifact, "to_ref": req, "source_refs": sr, "projection_only": True, "authority_effect": "NONE"}], "provenance_records": [{"provenance_id": "PROV-C01-R17", "entity_ref": artifact, "derived_from_refs": [req], "generated_by_ref": job, "attributed_to_refs": ["producer:C01-R17"], "source_refs": sr}], "query_policies": [{"policy_id": "KG-C01-EV3", "query_scope": "TASK_CLAIM_SCOPED_ONLY", "eligibility_rule_ref": "OE-policy", "claim_ceiling_rule_ref": "claim-ceiling-policy", "source_refs": sr}]},
        "agent_runtime": {"header": header("AGENT_RUNTIME", "NOT_TRIGGERED", sr, ["AUTHORITY", "DESIGN_KEEP", "PROJECT_PROMOTION"]), "sessions": [], "leases": [], "actions": [], "handoffs": []},
    }
    d["digital_thread"]["relations"] = [
        {"relation_id": "REL-C01-PROJECT-WP", "relation_type": "PROJECT_CONTAINS_WORK_PACKAGE", "from_ref": pid, "to_ref": wp, "projection_only": True, "source_refs": sr},
        {"relation_id": "REL-C01-JOB-WP", "relation_type": "JOB_EXECUTES_WORK_PACKAGE", "from_ref": job, "to_ref": wp, "projection_only": True, "source_refs": sr},
        {"relation_id": "REL-C01-JOB-ART", "relation_type": "JOB_PRODUCES_ARTIFACT", "from_ref": job, "to_ref": artifact, "projection_only": True, "source_refs": sr},
        {"relation_id": "REL-C01-ART-REV", "relation_type": "ARTIFACT_REVIEWED_BY", "from_ref": artifact, "to_ref": review, "projection_only": True, "source_refs": sr},
        {"relation_id": "REL-C01-ART-REQ", "relation_type": "SATISFIES", "from_ref": artifact, "to_ref": req, "projection_only": True, "source_refs": sr},
    ]
    d["digital_thread"]["unresolved_links"] = [{"link_id": "UNRES-C01-INDEPENDENT-REVIEW", "from_ref": artifact, "expected_relation_type": "ARTIFACT_REVIEWED_BY", "reason": "Independent professional review is NOT_RUN; machine PASS must not become Design KEEP.", "blocking": True}]
    d["state_facets"].update({
        "project_design": {pid: "CANDIDATE"}, "job": {job: "SUCCEEDED"}, "knowledge_integrity": {"EV3:C01:SOURCE_MANIFEST": "SOURCE_BOUND"}, "operational_eligibility": {req: "OE2_CONDITIONAL"},
        "design_quality": {artifact: "HOLD_INDEPENDENT_REVIEW_NOT_RUN"}, "professional": {"C01-R17": "HOLD_PROFESSIONAL_REVIEW_NOT_RUN"}, "interface": {req: "HOLD_FIELD_ENGINEERING_OPEN"},
        "authority": {artifact: "CURRENT_POINTER_UNCHANGED"}, "evidence": {artifact: "MACHINE_READBACK_PASS"}, "configuration": {artifact: "REVIEW"}, "quality": {artifact: "HOLD_PROFESSIONAL_GATE"}, "process": {wp: "HOLD"}, "agent_runtime": {"C01-R17": "NOT_TRIGGERED"},
    })
    return finish_projection(d)
