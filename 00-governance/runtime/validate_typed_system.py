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
EXECUTABLE_SNAPSHOT_RULES = {
    "P0/PLANE-001",
    "P0/ID-002",
    "P1/CLAIM-RP01",
    "P3/MIG-RP01",
    "P4/IFC-RP01",
    "P4/VAR-RP09",
    "P4/VAR-RP10",
    "P4/VAR-RP11",
    "P4/AUTH-RP06",
    "P4/VAR-RP12",
    "P4/IFC-RP10",
    "P4/IFC-RP11",
    "P4/IFC-RP12",
    "P4/IFC-RP13",
    "P5/CHG-RP01",
    "P5/CFG-RP05",
    "P5/CARRY-RP04",
    "P5/CONC-RP03",
    "P5/PROM-RP05",
    "P5/ROLL-RP04",
    "P5/ROLL-RP05",
    "P5/CARRY-RP05",
    "P5/STALE-RP05",
    "P5/CSA-RP02",
    "P5/CONC-RP04",
    "P6/ASR-RP02",
    "P6/APP-RP04",
    "P6/ADM-RP04",
    "P6/APP-RP05",
    "P6/TGT-RP01",
    "P6/INDP-RP02",
    "P6/CEIL-RP04",
    "P6/RDY-RP02",
    "P6/CEIL-RP05",
    "P6/TRF-RP01",
    "P6/CONTRA-RP02",
    "P6/UNC-RP02",
    "P6/UNC-RP03",
    "P6/UNC-RP04",
    "P6/DISP-RP02",
    "P6/IND-RP02",
    "P6/INDP-RP03",
    "P6/INDP-RP04",
    "P6/CONTRA-RP03",
    "P6/CEIL-RP06",
    "P7/OPEN-RP01",
    "P9/CORPUS-RP01",
    "P9/TERM-RP01",
    "P9/BODY-RP01",
    "P10/ASSET-RP01",
    "P10/ROLE-RP02",
    "P10/TRUTH-RP03",
    "P10/MED-RP01",
    "P11/BADGE-RP02",
}

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

    unregistered_executable = sorted(EXECUTABLE_SNAPSHOT_RULES - seen)
    if unregistered_executable:
        out.append(Finding(
            "INT/REGISTRY-006","FAIL","S3_MAJOR",None,
            "executable snapshot rule is absent from rule registry",
            {"missing":unregistered_executable},
        ))

    missing = sorted(set(reg.get("replay_derived_rules", {})) - seen)
    if missing:
        out.append(Finding("INT/REGISTRY-005","FAIL","S2_MATERIAL",None,"replay-derived rules absent from namespace lists",{"missing":missing}))

    discovered_replay_rules: dict[str, list[str]] = {}
    discovered_replay_sources: set[str] = set()
    for replay_path in sorted(RUNTIME.glob("OLEANDER_REPLAY_*.json")):
        replay = load(replay_path)
        replay_id = replay.get("replay_id")
        replay_rules = replay.get("replay_derived_rules", [])
        if isinstance(replay_rules, dict):
            replay_rules = list(replay_rules)
        if replay_rules is None:
            replay_rules = []
        if not isinstance(replay_rules, list):
            out.append(Finding(
                "INT/REPLAY-001","FAIL","S2_MATERIAL",None,
                "replay_derived_rules must be a list or object",
                {"file":replay_path.name,"actual_type":type(replay_rules).__name__},
            ))
            continue
        if replay_rules and not replay_id:
            out.append(Finding(
                "INT/REPLAY-002","FAIL","S2_MATERIAL",None,
                "replay with derived rules must declare replay_id",
                {"file":replay_path.name},
            ))
        if replay_id:
            discovered_replay_sources.add(str(replay_id))
        for rule_id in replay_rules:
            if not isinstance(rule_id, str) or "/" not in rule_id:
                out.append(Finding(
                    "INT/REPLAY-003","FAIL","S2_MATERIAL",None,
                    "replay-derived rule must be a namespaced string",
                    {"file":replay_path.name,"rule":rule_id},
                ))
                continue
            discovered_replay_rules.setdefault(rule_id, []).append(str(replay_id or replay_path.name))

    missing_registered = sorted(set(discovered_replay_rules) - seen)
    if missing_registered:
        out.append(Finding(
            "INT/REPLAY-004","FAIL","S3_MAJOR",None,
            "replay-derived rules exist in replay records but are absent from validator namespace registry",
            {"count":len(missing_registered),"missing":missing_registered},
        ))

    defined_replay_rules = set(reg.get("replay_derived_rules", {}))
    missing_definitions = sorted(set(discovered_replay_rules) - defined_replay_rules)
    if missing_definitions:
        out.append(Finding(
            "INT/REPLAY-005","FAIL","S2_MATERIAL",None,
            "replay-derived rules are registered but lack registry definitions",
            {"count":len(missing_definitions),"missing":missing_definitions},
        ))

    registered_sources = set(reg.get("replay_sources", []))
    missing_sources = sorted(discovered_replay_sources - registered_sources)
    if missing_sources:
        out.append(Finding(
            "INT/REPLAY-006","FAIL","S2_MATERIAL",None,
            "replay source IDs are not bound into validator registry",
            {"count":len(missing_sources),"missing":missing_sources},
        ))

    declared_origins = reg.get("replay_rule_origins", {})
    origin_mismatch: dict[str, dict[str, list[str]]] = {}
    for rule_id, source_ids in discovered_replay_rules.items():
        declared = set(declared_origins.get(rule_id, []))
        expected = set(source_ids)
        if not expected.issubset(declared):
            origin_mismatch[rule_id] = {
                "missing_origins": sorted(expected - declared),
                "declared_origins": sorted(declared),
            }
    if origin_mismatch:
        out.append(Finding(
            "INT/REPLAY-007","FAIL","S2_MATERIAL",None,
            "replay rule origin bindings are incomplete",
            {"count":len(origin_mismatch),"mismatch":origin_mismatch},
        ))

    cases = ev.get("cases", [])
    ids = [c.get("id") for c in cases]
    dups = sorted({x for x in ids if x and ids.count(x) > 1})
    if dups:
        out.append(Finding("INT/EVAL-001","FAIL","S2_MATERIAL",None,"duplicate regression IDs",{"duplicates":dups}))
    for c in cases:
        if not c.get("id") or not c.get("priority") or not c.get("input") or not c.get("expected"):
            out.append(Finding("INT/EVAL-002","FAIL","S2_MATERIAL",c.get("id"),"regression case missing required fields"))

    eval_rule_refs: set[str] = set()
    for c in cases:
        for expected in c.get("expected", []):
            if isinstance(expected, str):
                eval_rule_refs.add(expected.split(":", 1)[0])
    uncovered_replay_rules = sorted(set(discovered_replay_rules) - eval_rule_refs)
    if uncovered_replay_rules:
        out.append(Finding(
            "INT/EVAL-003","REVIEW_SIGNAL","S1_REVIEW",None,
            "replay-derived rules without explicit regression-case references remain visible coverage debt",
            {"count":len(uncovered_replay_rules),"rules":uncovered_replay_rules},
        ))

    if not any(f.outcome == "FAIL" for f in out):
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

            required = set(o.get("required_acceptance_dimensions", []))
            missing_required = sorted(required - set(dims))
            unresolved_required = {k:dims.get(k) for k in sorted(required & set(dims)) if dims.get(k) not in CLOSED}
            identity_or_session = {"IDENTITY_CONTINUITY","TRANSACTION_SESSION_CONTINUITY"}
            semantic_outcome = identity_or_session | {"ROUTE_ATTRIBUTION","FARE_OR_RULE_OUTCOME","RECOVERY_CORRECTION","PRIVACY_AUTHORIZED_USE"}
            if dims.get("CREDENTIAL_RECOGNITION") in CLOSED and (
                missing_required or unresolved_required
            ) and required & identity_or_session:
                out.append(Finding(
                    "P4/IFC-RP10","FAIL","S3_MAJOR",oid(o),
                    "local credential/device acceptance cannot close unresolved end-to-end identity or session continuity",
                    {"missing_required":missing_required,"unresolved_required":unresolved_required},
                ))
            if dims.get("CREDENTIAL_RECOGNITION") in CLOSED and (
                missing_required or unresolved_required
            ) and required & semantic_outcome:
                out.append(Finding(
                    "P4/IFC-RP12","FAIL","S3_MAJOR",oid(o),
                    "technical communication/recognition pass cannot close unresolved semantic transaction or service outcome dimensions",
                    {"missing_required":missing_required,"unresolved_required":unresolved_required},
                ))
            if o.get("n_way_model") in {"HUB_INTERFACE","HUB_WITH_SELECTIVE_PAIRWISE_EDGES"} and o.get("pairwise_acceptance_complete") is True and o.get("hub_invariant_result") not in CLOSED:
                out.append(Finding(
                    "P4/IFC-RP11","FAIL","S3_MAJOR",oid(o),
                    "pairwise acceptance cannot prove required hub-level transaction/session coherence",
                    {"hub_invariant_result":o.get("hub_invariant_result")},
                ))
            if o.get("failure_user_consequence_material") is True and o.get("recovery_path_status") not in CLOSED:
                out.append(Finding(
                    "P4/IFC-RP13","FAIL","S3_MAJOR",oid(o),
                    "material service interface cannot close without a defined accepted recovery/exception path",
                    {"recovery_path_status":o.get("recovery_path_status")},
                ))

    for o in objects:
        if o.get("semantic_class") == "CONTROLLED_VARIABLE":
            if o.get("identity_equivalence_material") is True:
                missing_identity = [k for k in ("identity_scope","equivalence_policy") if not o.get(k)]
                if missing_identity:
                    out.append(Finding(
                        "P4/VAR-RP09","FAIL","S3_MAJOR",oid(o),
                        "identity-sensitive controlled variable must declare identity scope and equivalence policy",
                        {"missing":missing_identity},
                    ))
            if o.get("transition_changes_downstream_behavior_or_outcome") is True and o.get("treated_as_material") is False:
                out.append(Finding(
                    "P4/VAR-RP10","FAIL","S3_MAJOR",oid(o),
                    "state variable that changes allowed downstream behavior/outcome cannot be treated as non-material",
                ))
            if o.get("derived_output_active") is True:
                required_inputs = set(o.get("required_input_dimensions", []))
                resolved_inputs = set(o.get("resolved_input_dimensions", []))
                missing_inputs = sorted(required_inputs - resolved_inputs)
                if missing_inputs:
                    out.append(Finding(
                        "P4/VAR-RP11","FAIL","S3_MAJOR",oid(o),
                        "active derived controlled output is missing required non-substitutable input dimensions",
                        {"missing_input_dimensions":missing_inputs},
                    ))
            if o.get("derivation_changes_meaning_or_outcome") is True and not o.get("semantic_interpreter"):
                out.append(Finding(
                    "P4/AUTH-RP06","FAIL","S3_MAJOR",oid(o),
                    "meaning/outcome-changing derivation must name semantic interpreter separately from raw value production",
                ))

        if o.get("semantic_class") == "STATE_EVENT" and o.get("advances_state_machine") is True and not o.get("subject_or_session_ref"):
            out.append(Finding(
                "P4/VAR-RP12","FAIL","S3_MAJOR",oid(o),
                "state-advancing event must bind to the semantic subject/session whose state it advances",
            ))

    for o in objects:
        if o.get("semantic_class") == "CHANGE" and o.get("change_scope") == "SUPPORT_DERIVATIVE_ONLY" and o.get("upstream_source_changed") is False:
            if "UPSTREAM_SOURCE_CONFIGURATION" in set(o.get("stale_effects", [])):
                out.append(Finding("P5/CHG-RP01","FAIL","S3_MAJOR",oid(o),"support-only change cannot stale unchanged upstream source configuration"))

    for o in objects:
        if o.get("semantic_class") in {"ASSURANCE_ACTIVITY","ASSURANCE_DECISION","CONFIGURATION_STATUS"}:
            checked = o.get("check_target_revision")
            used_for = o.get("current_use_revision") or o.get("candidate_revision")
            has_bridge = bool(o.get("equivalence_or_applicability_ref"))
            if checked and used_for and checked != used_for and not has_bridge:
                if o.get("configuration_identity_mode") == "EXACT_REVISION":
                    out.append(Finding(
                        "P5/CFG-RP05","FAIL","S3_MAJOR",oid(o),
                        "exact-revision assurance cannot silently become assurance for a different revision",
                        {"check_target_revision":checked,"current_use_revision":used_for},
                    ))
                out.append(Finding(
                    "P5/CARRY-RP04","FAIL","S3_MAJOR",oid(o),
                    "earlier revision assurance requires explicit equivalence/applicability or re-assurance before carry-forward",
                    {"check_target_revision":checked,"current_use_revision":used_for},
                ))
                out.append(Finding(
                    "P5/CSA-RP02","FAIL","S3_MAJOR",oid(o),
                    "configuration status accounting projects an assurance result beyond the revision it evaluated",
                    {"check_target_revision":checked,"current_use_revision":used_for},
                ))

            if o.get("dependency_or_base_context_changed") is True and o.get("local_changeset_unchanged") is True and o.get("integration_assurance_status") in {"PASS","CURRENT_VALID","VERIFIED"} and not has_bridge:
                out.append(Finding(
                    "P5/STALE-RP05","FAIL","S3_MAJOR",oid(o),
                    "integration assurance cannot remain current solely because local bytes are unchanged when dependency/base context changed",
                ))

        if o.get("semantic_class") == "INTEGRATION_CONFIGURATION":
            composed = o.get("composed_change_refs", [])
            if len(composed) >= 2 and o.get("component_assurance_complete") is True and o.get("base_or_interaction_context_changed") is True and o.get("integration_assurance_status") not in CLOSED:
                out.append(Finding(
                    "P5/CONC-RP03","FAIL","S3_MAJOR",oid(o),
                    "individually assured concurrent changes require assurance on the actual composed integration configuration",
                    {"composed_change_refs":composed,"integration_assurance_status":o.get("integration_assurance_status")},
                ))
            if o.get("mechanical_merge_status") in CLOSED and o.get("semantic_integration_claimed_pass") is True and o.get("semantic_integration_status") not in CLOSED:
                out.append(Finding(
                    "P5/CONC-RP04","FAIL","S3_MAJOR",oid(o),
                    "successful mechanical merge cannot self-grant semantic/integration compatibility",
                    {"mechanical_merge_status":o.get("mechanical_merge_status"),"semantic_integration_status":o.get("semantic_integration_status")},
                ))

        if o.get("semantic_class") in {"CONFIGURATION_PROMOTION","BASELINE"} and o.get("candidate_assurance_status") in CLOSED and o.get("baseline_pointer_moved") is True and not o.get("authorized_promotion_event_ref"):
            out.append(Finding(
                "P5/PROM-RP05","FAIL","S4_CRITICAL",oid(o),
                "candidate assurance PASS cannot move Current/baseline pointer without an authorized promotion event",
            ))

        if o.get("rollback_mechanism") == "COMPENSATING_CHANGE" and o.get("reuses_prior_configuration_identity") is True:
            out.append(Finding(
                "P5/ROLL-RP04","FAIL","S3_MAJOR",oid(o),
                "compensating rollback/revert creates a new configuration identity and cannot reuse the prior identity",
            ))

        if o.get("rollback_mechanism") == "POINTER_RESELECTION" and o.get("baseline_pointer_moved") is True:
            missing = []
            if not o.get("pointer_rewrite_authority_ref"):
                missing.append("pointer_rewrite_authority_ref")
            if o.get("lineage_preserved") is not True:
                missing.append("lineage_preserved")
            if missing:
                out.append(Finding(
                    "P5/ROLL-RP05","FAIL","S4_CRITICAL",oid(o),
                    "shared Current/baseline pointer rewrite requires explicit authority and preserved lineage",
                    {"missing":missing},
                ))

        if o.get("rollback_mechanism") in {"COMPENSATING_CHANGE","POINTER_RESELECTION","EXACT_RESTORE_FROM_CONTROLLED_BASELINE","REIMPLEMENT_PRIOR_INTENT"} and o.get("reactivated_prior_assurance") is True and not o.get("post_rollback_applicability_review_ref"):
            out.append(Finding(
                "P5/CARRY-RP05","FAIL","S3_MAJOR",oid(o),
                "rollback cannot automatically reactivate prior assurance without post-rollback applicability review",
            ))

    for o in objects:
        if o.get("semantic_class") in {"ASSURANCE_ACTIVITY","ASSURANCE_DECISION"}:
            tr = o.get("target_results", {})
            if isinstance(tr, dict) and len(set(tr.values())) > 1 and o.get("summary_result") in {"PASS","FAIL"} and not o.get("aggregation_policy"):
                out.append(Finding("P6/ASR-RP02","FAIL","S3_MAJOR",oid(o),"mixed target results require explicit aggregation policy",{"target_results":tr,"summary_result":o.get("summary_result")}))

            disposition = o.get("disposition") or o.get("summary_result")
            material_dims = set(o.get("material_applicability_dimensions", []))
            resolved_dims = set(o.get("resolved_applicability_dimensions", []))
            missing_dims = sorted(material_dims - resolved_dims)
            if o.get("evidence_acquisition_state") == "ACQUIRED" and o.get("target_admissibility") in {"NOT_EVALUATED","APPLICABILITY_UNRESOLVED","REJECTED"} and disposition == "PASS":
                out.append(Finding(
                    "P6/ADM-RP04","FAIL","S3_MAJOR",oid(o),
                    "acquired evidence cannot be treated as target-admissible by acquisition state alone",
                    {"target_admissibility":o.get("target_admissibility")},
                ))
            if o.get("direct_project_closure_claimed") is True and missing_dims:
                out.append(Finding(
                    "P6/APP-RP04","FAIL","S3_MAJOR",oid(o),
                    "direct project assurance cannot close while material applicability dimensions remain unresolved",
                    {"unresolved_dimensions":missing_dims},
                ))
                if o.get("evidence_source_kind") in {"EXTERNAL_REFERENCE","VENDOR_EVIDENCE","PRECEDENT","STANDARD_REFERENCE"}:
                    out.append(Finding(
                        "P6/APP-RP05","FAIL","S3_MAJOR",oid(o),
                        "external/reference/vendor evidence requires explicit target applicability before direct project closure",
                        {"unresolved_dimensions":missing_dims},
                    ))

            if o.get("assurance_target_id") and o.get("result_reused_for_target_id") and o.get("assurance_target_id") != o.get("result_reused_for_target_id") and not o.get("separate_target_decision_ref"):
                out.append(Finding(
                    "P6/TGT-RP01","FAIL","S4_CRITICAL",oid(o),
                    "assurance PASS cannot be reused across a different target identity without a separate target decision",
                    {"source_target":o.get("assurance_target_id"),"reused_target":o.get("result_reused_for_target_id")},
                ))

            required_independence = o.get("required_independence_level")
            if o.get("review_performer_relationship") in {"PRODUCER","REPAIRER","PRODUCER_OR_REPAIRER"} and required_independence in {"INDEPENDENT_PROJECT_REVIEW","EXTERNAL_SPECIALIST","AUTHORIZED_PROFESSIONAL_OR_BODY"} and (o.get("independent_review_status") == "PASS" or o.get("downstream_active_granted") is True):
                out.append(Finding(
                    "P6/INDP-RP02","FAIL","S4_CRITICAL",oid(o),
                    "producer/repair retest cannot satisfy a required independent review or grant dependent active state",
                    {"required_independence_level":required_independence},
                ))

            if disposition == "PASS" and o.get("promotion_ambiguity_possible") is True:
                missing_boundary_fields = [k for k in ("grants","leaves_unchanged","excludes","does_not_establish") if k not in o]
                if missing_boundary_fields:
                    out.append(Finding(
                        "P6/CEIL-RP04","FAIL","S3_MAJOR",oid(o),
                        "PASS with promotion ambiguity must name granted, unchanged, excluded and non-established boundaries",
                        {"missing":missing_boundary_fields},
                    ))
            if disposition == "PASS" and o.get("adjacent_high_risk_claims") and not o.get("does_not_establish"):
                out.append(Finding(
                    "P6/CEIL-RP05","FAIL","S3_MAJOR",oid(o),
                    "assurance artifact that can be misread as broader proof must state adjacent high-risk claims it does not establish",
                    {"adjacent_high_risk_claims":o.get("adjacent_high_risk_claims")},
                ))
            if o.get("output_role") in {"QUANTITATIVE_READINESS","LIMITED_ACCEPTANCE"} and o.get("source_evidence_quality_upgraded") is True:
                out.append(Finding(
                    "P6/RDY-RP02","FAIL","S3_MAJOR",oid(o),
                    "readiness/limited-acceptance disposition cannot upgrade the quality class of its source evidence",
                ))
            if o.get("evidence_modality") in {"PROTOTYPE","SIMULATION","RENDER","CALIBRATION"} and o.get("claim_target_modality") in {"FIELD_OPERATIONAL","FIELD_MEASURED","REAL_USE_VALIDATION"} and disposition == "PASS" and not o.get("validation_bridge_ref"):
                out.append(Finding(
                    "P6/TRF-RP01","FAIL","S4_CRITICAL",oid(o),
                    "prototype/simulation/render/calibration evidence cannot directly close field/real-use claim without an explicit validation bridge",
                ))
            if o.get("invalid_or_inapplicable_for_target") is True and (o.get("retained_in_current_assurance_basis") is True or not o.get("correction_lineage_ref")):
                out.append(Finding(
                    "P6/CONTRA-RP02","FAIL","S3_MAJOR",oid(o),
                    "invalid/inapplicable evidence must leave the current assurance basis while preserving correction lineage",
                    {"retained_in_current_assurance_basis":o.get("retained_in_current_assurance_basis"),"correction_lineage_ref":o.get("correction_lineage_ref")},
                ))

            if o.get("decision_rule_material") is True:
                if disposition == "PASS" and not o.get("decision_rule_id"):
                    out.append(Finding(
                        "P6/UNC-RP02","FAIL","S3_MAJOR",oid(o),
                        "quantitative conformity PASS cannot be inferred from a point result when the decision rule/uncertainty is material but undefined",
                    ))
                if o.get("decision_rule_changes_acceptance_boundary") is True and o.get("acceptance_zone_declared") is not True:
                    out.append(Finding(
                        "P6/UNC-RP03","FAIL","S3_MAJOR",oid(o),
                        "decision-rule-modified acceptance boundary must be declared separately from the source specification zone",
                    ))
                if o.get("source_requirement_rewritten_by_decision_rule") is True:
                    out.append(Finding(
                        "P6/UNC-RP04","FAIL","S4_CRITICAL",oid(o),
                        "assurance decision rule cannot silently rewrite the source requirement/specification",
                    ))
                if o.get("uncertainty_or_decision_boundary_material") is True and disposition in {"PASS","FAIL","INCONCLUSIVE","ACCEPTED_WITH_LIMITATIONS"} and not o.get("disposition_reason_code"):
                    out.append(Finding(
                        "P6/DISP-RP02","FAIL","S3_MAJOR",oid(o),
                        "quantitative boundary disposition requires an explicit reason code when uncertainty/decision boundary is material",
                    ))

            claimed_independent = o.get("claimed_independent_source_count")
            if claimed_independent is not None:
                groups = {x for x in o.get("source_independence_groups", []) if x}
                if claimed_independent > len(groups):
                    out.append(Finding(
                        "P6/IND-RP02","FAIL","S3_MAJOR",oid(o),
                        "evidence instance count cannot be used as independent-source count when sources share dependence groups",
                        {"claimed_independent_source_count":claimed_independent,"independence_group_count":len(groups)},
                    ))

            if o.get("independence_claimed_satisfied") is True:
                profile = o.get("independence_profile", {})
                required = o.get("required_independence_dimensions", [])
                unsatisfied = {dim:profile.get(dim,"NOT_EVALUATED") for dim in required if profile.get(dim) != "SATISFIED"}
                if unsatisfied:
                    out.append(Finding(
                        "P6/INDP-RP03","FAIL","S3_MAJOR",oid(o),
                        "independent-review claim cannot collapse required technical/managerial/financial dimensions to one boolean",
                        {"unsatisfied_dimensions":unsatisfied},
                    ))
            if o.get("independent_review_status") == "REQUIRED_INDEPENDENCE_NOT_MET" and o.get("underlying_self_check_evidence_status") == "INVALIDATED_BY_INDEPENDENCE_ONLY":
                out.append(Finding(
                    "P6/INDP-RP04","FAIL","S2_MATERIAL",oid(o),
                    "failure to meet independent-review requirement downgrades the independence claim, not automatically the underlying self-check evidence",
                ))

            if o.get("contradictory_evidence_present") is True and o.get("contradiction_adjudication_complete") is not True and disposition in {"PASS","FAIL"}:
                out.append(Finding(
                    "P6/CONTRA-RP03","FAIL","S3_MAJOR",oid(o),
                    "material contradictory evidence requires adjudication across target/configuration/condition/method/uncertainty/dependence before final PASS/FAIL",
                ))

            if disposition == "PASS" and o.get("declared_target_ceiling_dimensions") is not None:
                allowed = set(o.get("declared_target_ceiling_dimensions", []))
                grants = o.get("granted_ceilings", {})
                if isinstance(grants, dict):
                    overreach = {k:v for k,v in grants.items() if k not in allowed and v not in {None,"UNASSESSED","OPEN","UNCHANGED","NOT_FIELD"}}
                    if overreach:
                        out.append(Finding(
                            "P6/CEIL-RP06","FAIL","S4_CRITICAL",oid(o),
                            "quantitative/conformity PASS grants ceiling dimensions outside the declared assurance target",
                            {"overreach":overreach,"declared_target_ceiling_dimensions":sorted(allowed)},
                        ))

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
            {"id":"TFL-I","plane":"PROJECT","semantic_class":"INTERFACE","disposition":"CLOSED","n_way_model":"HUB_WITH_SELECTIVE_PAIRWISE_EDGES","pairwise_acceptance_complete":True,"hub_invariant_result":"OPEN","required_acceptance_dimensions":["CREDENTIAL_RECOGNITION","IDENTITY_CONTINUITY","TRANSACTION_SESSION_CONTINUITY"],"acceptance_dimensions":{"CREDENTIAL_RECOGNITION":"PASS","IDENTITY_CONTINUITY":"OPEN"},"failure_user_consequence_material":True,"recovery_path_status":"OPEN"},
            {"id":"TFL-ID","plane":"PROJECT","semantic_class":"CONTROLLED_VARIABLE","controlled_variable_class":"CONTENT_SEMANTIC","identity_equivalence_material":True},
            {"id":"TFL-STATE","plane":"PROJECT","semantic_class":"CONTROLLED_VARIABLE","controlled_variable_class":"STATE","transition_changes_downstream_behavior_or_outcome":True,"treated_as_material":False},
            {"id":"TFL-FARE","plane":"PROJECT","semantic_class":"CONTROLLED_VARIABLE","derived_output_active":True,"required_input_dimensions":["ORIGIN","DESTINATION","ROUTE_EVIDENCE"],"resolved_input_dimensions":["ORIGIN","DESTINATION"],"derivation_changes_meaning_or_outcome":True},
            {"id":"TFL-EVENT","plane":"PROJECT","semantic_class":"STATE_EVENT","advances_state_machine":True},
            {"id":"C","plane":"PROJECT","semantic_class":"CHANGE","change_scope":"SUPPORT_DERIVATIVE_ONLY","upstream_source_changed":False,"stale_effects":["UPSTREAM_SOURCE_CONFIGURATION"]},
            {"id":"GIT-CHECK","plane":"PROJECT","semantic_class":"ASSURANCE_DECISION","configuration_identity_mode":"EXACT_REVISION","check_target_revision":"sha-old","current_use_revision":"sha-new"},
            {"id":"GIT-MERGE","plane":"PROJECT","semantic_class":"INTEGRATION_CONFIGURATION","composed_change_refs":["PR-1","PR-2"],"component_assurance_complete":True,"base_or_interaction_context_changed":True,"integration_assurance_status":"OPEN","mechanical_merge_status":"PASS","semantic_integration_claimed_pass":True,"semantic_integration_status":"OPEN"},
            {"id":"GIT-PROMOTE","plane":"PROJECT","semantic_class":"CONFIGURATION_PROMOTION","candidate_assurance_status":"PASS","baseline_pointer_moved":True},
            {"id":"GIT-REVERT","plane":"PROJECT","semantic_class":"CHANGE","rollback_mechanism":"COMPENSATING_CHANGE","reuses_prior_configuration_identity":True,"reactivated_prior_assurance":True},
            {"id":"GIT-RESET","plane":"PROJECT","semantic_class":"CHANGE","rollback_mechanism":"POINTER_RESELECTION","baseline_pointer_moved":True,"lineage_preserved":False},
            {"id":"GIT-CONTEXT","plane":"PROJECT","semantic_class":"ASSURANCE_DECISION","dependency_or_base_context_changed":True,"local_changeset_unchanged":True,"integration_assurance_status":"PASS"},
            {"id":"M","plane":"PROJECT","semantic_class":"ASSURANCE_DECISION","target_results":{"G1":"REVISE","G4":"PASS"},"summary_result":"PASS"},
            {"id":"P6-APP","plane":"PROJECT","semantic_class":"ASSURANCE_DECISION","evidence_acquisition_state":"ACQUIRED","target_admissibility":"APPLICABILITY_UNRESOLVED","material_applicability_dimensions":["CONFIGURATION","CONDITION"],"resolved_applicability_dimensions":["CONFIGURATION"],"direct_project_closure_claimed":True,"evidence_source_kind":"EXTERNAL_REFERENCE","disposition":"PASS"},
            {"id":"P6-TARGET","plane":"PROJECT","semantic_class":"ASSURANCE_DECISION","assurance_target_id":"ARTIFACT_QA","result_reused_for_target_id":"TECHNICAL_REQUIREMENT","disposition":"PASS"},
            {"id":"P6-INDEP-PRODUCER","plane":"PROJECT","semantic_class":"ASSURANCE_DECISION","review_performer_relationship":"PRODUCER_OR_REPAIRER","required_independence_level":"INDEPENDENT_PROJECT_REVIEW","independent_review_status":"PASS","downstream_active_granted":True},
            {"id":"P6-BOUNDARY","plane":"PROJECT","semantic_class":"ASSURANCE_DECISION","disposition":"PASS","promotion_ambiguity_possible":True,"adjacent_high_risk_claims":["FIELD_VALIDITY"],"output_role":"QUANTITATIVE_READINESS","source_evidence_quality_upgraded":True},
            {"id":"P6-TRANSFER","plane":"PROJECT","semantic_class":"ASSURANCE_DECISION","evidence_modality":"SIMULATION","claim_target_modality":"FIELD_OPERATIONAL","disposition":"PASS"},
            {"id":"P6-CORRECTION","plane":"PROJECT","semantic_class":"ASSURANCE_DECISION","invalid_or_inapplicable_for_target":True,"retained_in_current_assurance_basis":True},
            {"id":"P6-UNC","plane":"PROJECT","semantic_class":"ASSURANCE_DECISION","decision_rule_material":True,"decision_rule_changes_acceptance_boundary":True,"acceptance_zone_declared":False,"source_requirement_rewritten_by_decision_rule":True,"uncertainty_or_decision_boundary_material":True,"disposition":"PASS"},
            {"id":"P6-GROUPS","plane":"PROJECT","semantic_class":"ASSURANCE_DECISION","claimed_independent_source_count":3,"source_independence_groups":["SHARED-LAB"],"disposition":"PASS"},
            {"id":"P6-INDEP-PROFILE","plane":"PROJECT","semantic_class":"ASSURANCE_DECISION","required_independence_dimensions":["technical","managerial","financial"],"independence_profile":{"technical":"SATISFIED","managerial":"NOT_SATISFIED","financial":"NOT_EVALUATED"},"independence_claimed_satisfied":True,"independent_review_status":"REQUIRED_INDEPENDENCE_NOT_MET","underlying_self_check_evidence_status":"INVALIDATED_BY_INDEPENDENCE_ONLY"},
            {"id":"P6-CONTRA","plane":"PROJECT","semantic_class":"ASSURANCE_DECISION","contradictory_evidence_present":True,"contradiction_adjudication_complete":False,"disposition":"PASS"},
            {"id":"P6-CEILING","plane":"PROJECT","semantic_class":"ASSURANCE_DECISION","disposition":"PASS","declared_target_ceiling_dimensions":["technical_fit"],"granted_ceilings":{"technical_fit":"PASS","field_operational":"PASS"}},
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
    expected = {"P1/CLAIM-RP01","P4/IFC-RP01","P4/VAR-RP09","P4/VAR-RP10","P4/VAR-RP11","P4/AUTH-RP06","P4/VAR-RP12","P4/IFC-RP10","P4/IFC-RP11","P4/IFC-RP12","P4/IFC-RP13","P5/CHG-RP01","P5/CFG-RP05","P5/CARRY-RP04","P5/CONC-RP03","P5/PROM-RP05","P5/ROLL-RP04","P5/ROLL-RP05","P5/CARRY-RP05","P5/STALE-RP05","P5/CSA-RP02","P5/CONC-RP04","P6/ASR-RP02","P6/APP-RP04","P6/ADM-RP04","P6/APP-RP05","P6/TGT-RP01","P6/INDP-RP02","P6/CEIL-RP04","P6/RDY-RP02","P6/CEIL-RP05","P6/TRF-RP01","P6/CONTRA-RP02","P6/UNC-RP02","P6/UNC-RP03","P6/UNC-RP04","P6/DISP-RP02","P6/IND-RP02","P6/INDP-RP03","P6/INDP-RP04","P6/CONTRA-RP03","P6/CEIL-RP06","P9/CORPUS-RP01","P10/ASSET-RP01","P10/TRUTH-RP03","P10/MED-RP01","P11/BADGE-RP02"}
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
