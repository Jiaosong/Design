from __future__ import annotations

from pathlib import Path

from ev3_common import base_projection, finish_projection, header, load_json


LOCAL_ROOT = Path(r"D:\Desgin")
SOURCE_SPECS = [
    ("EV3SRC:FW:NATIVE_INTEGRITY", LOCAL_ROOT / r".mcp-runtime\diagnostics\OLEANDER_V06_FINAL_MATRIX_20260914\FINAL_NATIVE_SAVE_REOPEN_INTEGRITY.json", "LOCAL_DIAGNOSTIC_EXACT", "UTF8_TEXT_LF_CANONICAL_V1"),
    ("EV3SRC:FW:FURNITURE", LOCAL_ROOT / r".mcp-runtime\diagnostics\OLEANDER_V06_FINAL_MATRIX_20260914\FINAL_FURNITURE_USE_AUDIT.json", "LOCAL_DIAGNOSTIC_EXACT", "UTF8_TEXT_LF_CANONICAL_V1"),
    ("EV3SRC:FW:ARCH_TARGETS", LOCAL_ROOT / r".mcp-runtime\diagnostics\FALLINGWATER_V06_ARCH_TARGET_AUDIT.json", "LOCAL_DIAGNOSTIC_EXACT", "UTF8_TEXT_LF_CANONICAL_V1"),
    ("EV3SRC:FW:CONNECTIONS", LOCAL_ROOT / r".mcp-runtime\diagnostics\FALLINGWATER_V06_CONNECTION_REVIEW\V06_CONNECTION_WIRE_MANIFEST.json", "LOCAL_DIAGNOSTIC_EXACT", "UTF8_TEXT_LF_CANONICAL_V1"),
    ("EV3SRC:FW:NATIVE_BLEND", LOCAL_ROOT / r".mcp-runtime\diagnostics\FALLINGWATER_HABS_COMPLEX_V06_ARCH_SPATIAL_CONSTRUCTIVE_20260913.blend", "LOCAL_DIAGNOSTIC_EXACT", "RAW_BYTES_V1"),
]


def build_projection(source_rows: list[dict], template_path: Path) -> dict:
    native = load_json(SOURCE_SPECS[0][1])
    furniture = load_json(SOURCE_SPECS[1][1])
    arch = load_json(SOURCE_SPECS[2][1])
    connections = load_json(SOURCE_SPECS[3][1])
    assert native["status"] == "PASS" and all(native["checks"].values())
    recorded_native_sha = native["final_saved_reopened_sha256"]
    current_native_sha = source_rows[4]["sha256"]
    native_readback_current = recorded_native_sha == current_native_sha
    assert furniture["blend_sha256"] == recorded_native_sha
    assert furniture["all_edit011_invariants_pass"] is True
    assert len(arch["targets"]) == 44 and len(connections["items"]) == 8
    open_targets = [
        target
        for target in arch["targets"]
        if str(target.get("dimension_state", "")).startswith("OPEN")
        or target.get("authority") is None
    ]
    assert open_targets

    d = base_projection(template_path, "FALLINGWATER", source_rows)
    sr = [row["ref"] for row in source_rows]
    artifact = "ARTIFACT-FW-V06-NATIVE-BLEND"
    review = "REVIEW-FW-V06-INDEPENDENT-DESIGN"
    req = "REQ-FW-V06-ENGINEERING-AUTHORITY"
    d["authority"]["master_runtime_ref"] = "NOT_AVAILABLE:FALLINGWATER:MASTER_RUNTIME"
    d["authority"]["authority_snapshot_ref"] = "UNRESOLVED:FALLINGWATER:P2_PROJECT_AUTHORITY"
    d["case_refs"] = [{"canonical_case_id": "FALLINGWATER-HABS-V06", "canonical_ref": "local-diagnostic:FALLINGWATER-HABS-V06", "project_binding_state": "UNRESOLVED", "does_not_prove": ["P2_PROJECT_ID"]}]
    d["project_axis_refs"] = []
    d["work_packages"] = []
    d["jobs"] = []
    d["artifact_refs"] = [{"artifact_id": artifact, "canonical_ref": str(SOURCE_SPECS[4][1]), "native_format": "blend", "editable_state": "EDITABLE", "hash_or_commit": current_native_sha, "readback_refs": ["EV3SRC:FW:NATIVE_INTEGRITY", "EV3SRC:FW:FURNITURE"]}]
    d["review_refs"] = [{"review_id": review, "review_class": "DESIGN", "receipt_ref": "NOT_AVAILABLE:FALLINGWATER:INDEPENDENT-DESIGN", "result": "HOLD", "independence_state": "UNKNOWN"}]

    d["modules"] = {
        "erp": {"header": header("ERP", "NOT_TRIGGERED", sr, ["PROJECT_PROMOTION", "BUDGET_TRUTH", "PROFESSIONAL_PASS"]), "demand_records": [], "schedule_records": [], "resource_demand": []},
        "plm": {"header": header("PLM", "TRIGGERED", sr, ["TECHNICAL_CORRECTNESS", "DESIGN_KEEP", "PROJECT_PROMOTION"]), "configuration_items": [{"item_id": "CI-FW-V06-BLEND", "item_class": "MODEL", "canonical_ref": artifact, "revision_ref": current_native_sha, "lifecycle_state": "HOLD", "source_refs": sr, "does_not_prove": ["TECHNICAL_CORRECTNESS", "DESIGN_KEEP", "PROJECT_PROMOTION"]}], "baselines": [{"baseline_id": "BASELINE-FW-V06-NATIVE", "member_refs": ["CI-FW-V06-BLEND", req], "baseline_state": "HOLD", "authority_ref": "UNRESOLVED:FALLINGWATER:P2_PROJECT_AUTHORITY", "source_refs": sr}], "change_records": []},
        "mes": {"header": header("MES", "PARTIAL", sr, ["PHYSICAL_EXECUTION", "FIELD_TRUTH", "ACCEPTANCE"]), "operation_records": [], "material_equipment_refs": [{"canonical_ref": str(SOURCE_SPECS[4][1]), "source_refs": sr, "authority_owner": "Local native artifact only", "projection_only": True}], "execution_readbacks": [{"canonical_ref": "EV3SRC:FW:NATIVE_INTEGRITY", "source_refs": sr, "authority_owner": "Actual Readback", "projection_only": True}]},
        "bpm": {"header": header("BPM", "NOT_TRIGGERED", sr, ["PROFESSIONAL_STAGE_PASS", "DESIGN_KEEP", "PROJECT_PROMOTION"]), "process_instances": [], "handoffs": [], "exceptions": []},
        "qms": {"header": header("QMS", "HOLD", sr, ["PROFESSIONAL_PASS", "STATUTORY_APPROVAL", "DESIGN_KEEP"]), "quality_plans": [], "nonconformances": [], "capa_records": [], "inspection_records": [{"inspection_id": "INSP-FW-NATIVE-INTEGRITY", "subject_ref": artifact, "inspection_class": "ARTIFACT", "result": "HOLD" if not native_readback_current else "PASS", "evidence_refs": ["EV3SRC:FW:NATIVE_INTEGRITY", "EV3SRC:FW:NATIVE_BLEND"], "source_refs": sr}, {"inspection_id": "INSP-FW-FURNITURE-USE", "subject_ref": artifact, "inspection_class": "QUALITY", "result": "HOLD" if not native_readback_current else "PASS", "evidence_refs": ["EV3SRC:FW:FURNITURE", "EV3SRC:FW:NATIVE_BLEND"], "source_refs": sr}, {"inspection_id": "INSP-FW-ENGINEERING", "subject_ref": artifact, "inspection_class": "TECHNICAL", "result": "HOLD", "evidence_refs": ["EV3SRC:FW:ARCH_TARGETS", "EV3SRC:FW:CONNECTIONS"], "source_refs": sr}]},
        "mbse": {"header": header("MBSE", "HOLD", sr, ["SYSTEMS_ENGINEERING_CURRENT", "VALIDATION_PASS", "PROJECT_ACCEPTANCE"]), "requirements": [{"requirement_id": req, "requirement_class": "CONSTRAINT", "statement_ref": "FALLINGWATER:OPEN_DIMENSIONS+ENGINEERING+P2_BINDING", "status": "HOLD", "allocated_to_refs": [artifact], "verification_method": "REVIEW", "source_refs": sr, "does_not_prove": ["VALIDATION_PASS", "PROJECT_ACCEPTANCE"]}], "system_elements": [{"element_id": "SYS-FW-V06-MODEL", "element_class": "WORK_PRODUCT", "canonical_ref": artifact, "source_refs": sr}], "interfaces": [{"interface_id": "IF-FW-ENGINEERING", "from_ref": req, "to_ref": artifact, "interface_state": "HOLD", "verification_refs": ["VV-FW-ENGINEERING"], "source_refs": sr}], "verification_validation": [{"vv_id": "VV-FW-ENGINEERING", "subject_ref": req, "vv_class": "VALIDATION", "method": "QUALIFIED_ENGINEERING_REVIEW", "result": "NOT_RUN", "evidence_refs": [], "independent_review_ref": None, "source_refs": sr}], "configuration_baselines": ["BASELINE-FW-V06-NATIVE"]},
        "knowledge_graph": {"header": header("KNOWLEDGE_GRAPH", "TRIGGERED", sr, ["KNOWLEDGE_CURRENT", "OE3", "CLAIM_TRUTH"]), "nodes": [{"node_id": "KG-FW-CASE", "node_class": "EVIDENCE", "canonical_ref": "FALLINGWATER-HABS-V06", "source_refs": sr, "authority_gain": False}, {"node_id": "KG-FW-ART", "node_class": "ARTIFACT", "canonical_ref": artifact, "source_refs": sr, "authority_gain": False}, {"node_id": "KG-FW-REQ", "node_class": "REQUIREMENT", "canonical_ref": req, "source_refs": sr, "authority_gain": False}], "edges": [{"edge_id": "KG-FW-PROV", "predicate": "PROVENANCE_DERIVED_FROM", "from_ref": artifact, "to_ref": "EV3SRC:FW:ARCH_TARGETS", "source_refs": sr, "projection_only": True, "authority_effect": "NONE"}], "provenance_records": [{"provenance_id": "PROV-FW-V06", "entity_ref": artifact, "derived_from_refs": ["EV3SRC:FW:ARCH_TARGETS", "EV3SRC:FW:NATIVE_INTEGRITY"], "generated_by_ref": "LOCAL_BLENDER_EXECUTION_PROVENANCE_ONLY", "attributed_to_refs": ["LOCAL_DIAGNOSTIC_PRODUCER"], "source_refs": sr}], "query_policies": [{"policy_id": "KG-FW-EV3", "query_scope": "TASK_CLAIM_SCOPED_ONLY", "eligibility_rule_ref": "OE-policy", "claim_ceiling_rule_ref": "claim-ceiling-policy", "source_refs": sr}]},
        "agent_runtime": {"header": header("AGENT_RUNTIME", "NOT_TRIGGERED", sr, ["AUTHORITY", "DESIGN_KEEP", "PROJECT_PROMOTION"]), "sessions": [], "leases": [], "actions": [], "handoffs": []},
    }
    d["digital_thread"]["relations"] = [
        {"relation_id": "REL-FW-ART-REV", "relation_type": "ARTIFACT_REVIEWED_BY", "from_ref": artifact, "to_ref": review, "projection_only": True, "source_refs": sr},
        {"relation_id": "REL-FW-ART-REQ", "relation_type": "IMPLEMENTS", "from_ref": artifact, "to_ref": req, "projection_only": True, "source_refs": sr},
        {"relation_id": "REL-FW-PROV", "relation_type": "PROVENANCE_DERIVED_FROM", "from_ref": artifact, "to_ref": "EV3SRC:FW:ARCH_TARGETS", "projection_only": True, "source_refs": sr},
    ]
    d["digital_thread"]["unresolved_links"] = [
        {"link_id": "UNRES-FW-NATIVE-READBACK-DRIFT", "from_ref": artifact, "expected_relation_type": "VERIFIES", "reason": f"Recorded native integrity SHA {recorded_native_sha} does not match current native SHA {current_native_sha}.", "blocking": not native_readback_current},
        {"link_id": "UNRES-FW-P2-PROJECT", "from_ref": artifact, "expected_relation_type": "BOUND_TO_DECISION_OBJECT", "reason": "No canonical P2 Project/Master Runtime binding found; Case/native diagnostic identity cannot synthesize project authority.", "blocking": True},
        {"link_id": "UNRES-FW-ENGINEERING", "from_ref": artifact, "expected_relation_type": "VALIDATES", "reason": f"{len(open_targets)} audited targets have open/approximate dimension or authority state; engineering remains OPEN.", "blocking": True},
    ]
    d["state_facets"].update({
        "project_design": {"FALLINGWATER-HABS-V06": "CANDIDATE"}, "job": {}, "knowledge_integrity": {"EV3:FW:SOURCE_MANIFEST": "SOURCE_BOUND"},
        "operational_eligibility": {artifact: "HOLD_PROJECT_BINDING_UNRESOLVED"}, "design_quality": {artifact: "HOLD_INDEPENDENT_DESIGN_REVIEW_NOT_AVAILABLE"},
        "professional": {artifact: "HOLD_ENGINEERING_OPEN"}, "interface": {req: "HOLD_OPEN_DIMENSION_AND_ENGINEERING_AUTHORITY"},
        "authority": {artifact: "HOLD_P2_PROJECT_AUTHORITY_UNRESOLVED"}, "evidence": {artifact: "STALE_NATIVE_READBACK_DIVERGED" if not native_readback_current else "NATIVE_INTEGRITY_PASS_FURNITURE_USE_PASS"},
        "configuration": {artifact: "REVIEW"}, "quality": {artifact: "HOLD_ENGINEERING_AND_DESIGN_KEEP_NOT_PROVEN"},
        "process": {"FALLINGWATER-HABS-V06": "NOT_EVALUATED_NO_MASTER_RUNTIME"}, "agent_runtime": {"FALLINGWATER-HABS-V06": "NOT_TRIGGERED"},
    })
    d = finish_projection(d)
    if not native_readback_current:
        d["reconciliation"]["drift_state"] = "DIVERGED"
        d["reconciliation"]["projection_freshness_state"] = "SOURCE_READBACK_STALE"
        d["reconciliation"]["enterprise_readiness_state"] = "HOLD"
        d["reconciliation"]["advance_allowed"] = False
        d["reconciliation"]["reconciliation_actions"] = [
            "REFRESH_NATIVE_SAVE_REOPEN_INTEGRITY_AGAINST_CURRENT_BLEND",
            "REFRESH_FURNITURE_USE_READBACK_AGAINST_CURRENT_BLEND",
            "RESOLVE_P2_PROJECT_AUTHORITY_OR_KEEP_CASE_ONLY",
            "QUALIFIED_ENGINEERING_REVIEW_REQUIRED",
        ]
    return d
