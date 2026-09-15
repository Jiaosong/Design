#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "00-governance" / "runtime" / "OLEANDER_ARCHITECTURE_CONTROL_GRAPH_v2.1.json"
LAYER_INTERFACE = ROOT / "00-governance" / "runtime" / "OLEANDER_RUNTIME_LAYER_INTERFACE_CONTRACT_v1.0.json"
OBSERVABILITY_RECOVERY = ROOT / "00-governance" / "runtime" / "OLEANDER_OBSERVABILITY_RECOVERY_CONTRACT_v1.0.json"
EXPECTED_LAYERS = ["R-A", "R-B", "R-C", "R-D", "R-E", "R-F", "R-G", "R-H", "R-I", "R-J", "R-K"]
EXPECTED_PLANES = {"CONTROL_PLANE", "STATE_PLANE", "ACQUISITION_READER_PLANE", "EXECUTION_PLANE", "OBSERVABILITY_PLANE", "EVOLUTION_PLANE"}
EXPECTED_MATURITY = {
    "M0_DECLARED",
    "M1_DEFINED",
    "M2_FORMALIZED",
    "M3_MACHINE_BOUND",
    "M4_PROJECT_EXERCISED",
    "M5_INDEPENDENTLY_READBACK",
}
REQUIRED_OBSERVABILITY = {
    "project_or_scope_id",
    "current_task_id",
    "current_decision_object",
    "active_runtime_layer",
    "active_owner",
    "authority_fingerprint",
    "current_state",
    "stale_or_reopen_refs",
    "open_blockers",
    "last_verified_artifact_ref",
    "last_readback_ref",
    "current_receipt_refs",
    "dependency_health",
    "next_allowed_action",
    "observed_at",
}
REQUIRED_MACHINE_DENIES = {
    "AWARD_DESIGN_KEEP",
    "AWARD_DQ3_DQ5",
    "PROMOTE_CURRENT_AUTHORITY",
    "GRANT_STATUTORY_APPROVAL",
}
REQUIRED_RECOVERY_STEPS = {
    "DETECT",
    "IDENTIFY_OWNER_AND_BLAST_RADIUS",
    "PRESERVE_LAST_VERIFIED_STATE",
    "ACTUAL_READBACK",
    "RERUN_AFFECTED_REVIEWS",
}
REQUIRED_COMPAT_CLASSES = {
    "DOC_CLARIFICATION",
    "BACKWARD_COMPATIBLE_EXTENSION",
    "SEMANTIC_OWNER_CHANGE",
    "STATE_CONTRACT_CHANGE",
    "SCHEMA_BREAKING_CHANGE",
    "PROFESSIONAL_PROCESS_REVISION",
    "AUTHORITY_REPLACEMENT",
}
REQUIRED_TRIGGER_STATES = {
    "NOT_EVALUATED",
    "TRIGGERED",
    "NOT_REQUIRED",
    "UNRESOLVED",
}
REQUIRED_NOTION_GITHUB_REFERENCE_DRIFT_STATES = {
    "CURRENT",
    "STALE",
    "MISSING",
    "DIVERGED",
    "ORPHANED_IMPLEMENTATION",
    "NOT_REQUIRED",
    "UNKNOWN",
}


def fail(message: str) -> None:
    raise SystemExit(f"ARCHITECTURE CONTROL VALIDATION: FAIL: {message}")


def load_graph() -> dict:
    try:
        return json.loads(GRAPH.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot load {GRAPH.relative_to(ROOT)}: {exc}")


def check_ref(ref: str) -> None:
    path = ROOT / ref
    if not path.exists():
        fail(f"referenced local carrier does not exist: {ref}")


def validate_dag(layers_by_id: dict[str, dict]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            fail(f"primary dependency cycle detected at {node}; feedback must use feedback_edges")
        if node in visited:
            return
        visiting.add(node)
        for dep in layers_by_id[node].get("dependencies", []):
            visit(dep)
        visiting.remove(node)
        visited.add(node)

    for layer_id in EXPECTED_LAYERS:
        visit(layer_id)


def validate_layer_interface_contract(graph: dict, layers_by_id: dict[str, dict], plane_ids: set[str]) -> None:
    import re

    ref = graph.get("runtime_layer_interface_contract_ref")
    expected_ref = "00-governance/runtime/OLEANDER_RUNTIME_LAYER_INTERFACE_CONTRACT_v1.0.json"
    if ref != expected_ref:
        fail("runtime layer interface contract pointer drift")
    check_ref(ref)

    try:
        contract = json.loads(LAYER_INTERFACE.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot load runtime layer interface contract: {exc}")

    if contract.get("schema") != "oleander.runtime-layer-interface-contract.v1":
        fail("runtime layer interface schema drift")
    if contract.get("version") != "1.0":
        fail("runtime layer interface contract must be v1.0")
    if contract.get("status") != "ACTIVE_CURRENT_CONTRACT":
        fail("runtime layer interface contract must be ACTIVE_CURRENT_CONTRACT")
    if contract.get("architecture_ref") != graph.get("canonical_markdown_ref"):
        fail("runtime layer interface architecture pointer drift")
    if contract.get("control_graph_ref") != "00-governance/runtime/OLEANDER_ARCHITECTURE_CONTROL_GRAPH_v2.1.json":
        fail("runtime layer interface control-graph pointer drift")

    common = contract.get("common", {})
    required_fields = set(common.get("required_interface_fields", []))
    expected_required = {
        "external_inputs", "inputs", "outputs", "entry_conditions", "exit_conditions",
        "write_authority", "required_readback", "failure_codes", "plane_bindings",
        "handoff_targets", "persistence_policy", "claim_boundary",
    }
    if required_fields != expected_required:
        fail("runtime layer interface required-field set drift")
    if common.get("no_universal_layer_progress_state") is not True:
        fail("runtime layer interface must not create a universal layer progress state")

    handoff_fields = set(common.get("handoff_envelope_fields", []))
    for field in {
        "handoff_id", "from_layer", "to_layer", "project_or_scope_id", "decision_object_id",
        "authority_fingerprint", "source_revision", "object_refs", "claim_boundary", "open_blockers",
        "stale_if", "readback_refs", "handoff_state", "observed_at", "does_not_prove",
    }:
        if field not in handoff_fields:
            fail(f"handoff envelope missing field {field}")
    if set(common.get("handoff_state_values", [])) != {"UNRESOLVED", "READY", "ACCEPTED", "HOLD", "STALE", "SUPERSEDED"}:
        fail("handoff state vocabulary drift")
    for rule in {
        "PRODUCER_MAY_EMIT_READY_BUT_MAY_NOT_SELF_AWARD_ACCEPTED",
        "CONSUMER_ACCEPTS_ONLY_AFTER_REQUIRED_OBJECT_AND_READBACK_CHECK",
        "HANDOFF_ACCEPTED_DOES_NOT_PROVE_DOWNSTREAM_PASS",
        "FEEDBACK_EDGE_IS_NOT_A_DEPENDENCY_HANDOFF",
    }:
        if rule not in set(common.get("handoff_rules", [])):
            fail(f"handoff rule missing: {rule}")

    intersections = contract.get("plane_intersections", [])
    expected_intersections = {"CONTROL_STATE", "CONTROL_OBSERVABILITY", "ACQUISITION_STATE", "ACQUISITION_EXECUTION", "EXECUTION_OBSERVABILITY", "EVOLUTION_CONTROL", "EVOLUTION_STATE"}
    if {row.get("id") for row in intersections} != expected_intersections:
        fail("operational-plane intersection set drift")
    for row in intersections:
        if row.get("from_plane") not in plane_ids or row.get("to_plane") not in plane_ids:
            fail(f"plane intersection {row.get('id')} references unknown plane")
        if not row.get("allowed_flow") or not row.get("forbidden_inference"):
            fail(f"plane intersection {row.get('id')} missing allowed/forbidden semantics")

    interfaces = contract.get("layers", {})
    if list(interfaces.keys()) != EXPECTED_LAYERS:
        fail("runtime layer interface contract must contain R-A..R-K exactly once in canonical order")

    consumers: dict[str, list[str]] = {layer_id: [] for layer_id in EXPECTED_LAYERS}
    for target_id, layer in layers_by_id.items():
        for source_id in layer.get("dependencies", []) + layer.get("conditional_dependencies", []):
            consumers[source_id].append(target_id)

    failure_pattern = re.compile(r"^[A-Z][A-Z0-9_]+$")
    for layer_id in EXPECTED_LAYERS:
        interface = interfaces[layer_id]
        if interface.get("name") != layers_by_id[layer_id].get("name"):
            fail(f"{layer_id} interface name drift")
        for key in expected_required:
            if key not in interface:
                fail(f"{layer_id} interface missing {key}")
        for key in ("external_inputs", "outputs", "entry_conditions", "exit_conditions", "write_authority", "required_readback", "failure_codes", "plane_bindings"):
            if not isinstance(interface.get(key), list) or not interface[key]:
                fail(f"{layer_id} interface {key} must be a non-empty list")
        if not isinstance(interface.get("inputs"), list):
            fail(f"{layer_id} interface inputs must be a list")
        if layer_id != "R-A" and not interface["inputs"]:
            fail(f"{layer_id} must declare dependency inputs")
        if layer_id == "R-A" and interface["inputs"]:
            fail("R-A must not pretend to consume another runtime layer")

        input_sources = {item.split(":", 1)[0] for item in interface["inputs"] if ":" in item}
        expected_sources = set(layers_by_id[layer_id].get("dependencies", []) + layers_by_id[layer_id].get("conditional_dependencies", []))
        if input_sources != expected_sources:
            fail(f"{layer_id} dependency input coverage drift: expected {sorted(expected_sources)}, got {sorted(input_sources)}")
        for item in interface["inputs"]:
            if ":" not in item:
                fail(f"{layer_id} dependency input must use SOURCE_LAYER:OUTPUT_TOKEN: {item}")
            source_id, output_token = item.split(":", 1)
            source_interface = interfaces.get(source_id, {})
            if output_token not in set(source_interface.get("outputs", [])):
                fail(f"{layer_id} input {item} is not declared by upstream {source_id} outputs")

        if interface.get("handoff_targets") != consumers[layer_id]:
            fail(f"{layer_id} handoff_targets drift from dependency graph")
        if not set(interface.get("plane_bindings", [])).issubset(plane_ids):
            fail(f"{layer_id} binds unknown operational plane")
        if len(interface["failure_codes"]) != len(set(interface["failure_codes"])):
            fail(f"{layer_id} duplicate failure code")
        for code in interface["failure_codes"]:
            if not failure_pattern.fullmatch(code):
                fail(f"{layer_id} invalid failure code {code}")
        if not isinstance(interface.get("persistence_policy"), str) or not interface["persistence_policy"].strip():
            fail(f"{layer_id} persistence policy missing")
        if not isinstance(interface.get("claim_boundary"), str) or not interface["claim_boundary"].strip():
            fail(f"{layer_id} claim boundary missing")

    rk = interfaces["R-K"]
    if rk.get("feedback_targets") != ["R-B"]:
        fail("R-K feedback target must remain bounded to R-B")
    if "R-B" in rk.get("handoff_targets", []):
        fail("R-K feedback may not be represented as a dependency handoff")


def validate_observability_recovery_contract(graph: dict, layers_by_id: dict[str, dict]) -> None:
    ref = graph.get("observability_recovery_contract_ref")
    expected_ref = "00-governance/runtime/OLEANDER_OBSERVABILITY_RECOVERY_CONTRACT_v1.0.json"
    if ref != expected_ref:
        fail("observability/recovery contract pointer drift")
    check_ref(ref)
    try:
        contract = json.loads(OBSERVABILITY_RECOVERY.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot load observability/recovery contract: {exc}")

    if contract.get("schema") != "oleander.observability-recovery-contract.v1":
        fail("observability/recovery schema drift")
    if contract.get("version") != "1.0" or contract.get("status") != "ACTIVE_CURRENT_CONTRACT":
        fail("observability/recovery contract must be ACTIVE_CURRENT_CONTRACT v1.0")
    if contract.get("architecture_ref") != graph.get("canonical_markdown_ref"):
        fail("observability/recovery architecture pointer drift")
    if contract.get("control_graph_ref") != "00-governance/runtime/OLEANDER_ARCHITECTURE_CONTROL_GRAPH_v2.1.json":
        fail("observability/recovery control-graph pointer drift")
    if contract.get("layer_interface_ref") != graph.get("runtime_layer_interface_contract_ref"):
        fail("observability/recovery layer-interface pointer drift")
    if contract.get("execution_receipt_ref") != "00-governance/runtime/OLEANDER_EXECUTION_RECEIPT_v1.0.json":
        fail("observability/recovery execution-receipt pointer drift")
    check_ref(contract["execution_receipt_ref"])

    observability = contract.get("observability", {})
    if observability.get("semantic_class") != "READ_ONLY_OR_RECEIPT_BACKED_PROJECTION":
        fail("observability event must remain a read-only or receipt-backed projection")
    if observability.get("authority_ceiling") != "OBSERVABILITY_ONLY":
        fail("observability authority ceiling must remain OBSERVABILITY_ONLY")
    if set(observability.get("snapshot_required_fields", [])) != REQUIRED_OBSERVABILITY:
        fail("observability/recovery snapshot fields drift from architecture observability contract")
    event_fields = set(observability.get("event_core_required_fields", []))
    for required in {
        "event_id", "event_type", "project_or_scope_id", "decision_object_id", "owner_ref",
        "authority_fingerprint", "source_revision", "source_ref", "object_refs", "observed_at", "does_not_prove",
    }:
        if required not in event_fields:
            fail(f"observability event core field missing: {required}")
    if observability.get("event_type_is_state_family") is not False:
        fail("observability event type may not become a state family")
    conditional = observability.get("event_conditional_fields", {})
    for required in {"current_task_id", "runtime_layer_id", "checkpoint_sequence", "handoff_refs", "incident_ref", "readback_refs", "failure_class", "failure_code"}:
        if required not in conditional:
            fail(f"observability conditional event field missing: {required}")
    if observability.get("authority_resolution_rule") != "AN_OBSERVABILITY_EVENT_MAY_POINT_TO_OWNER_NATIVE_EVIDENCE_BUT_NEVER_OUTRANK_OR_REPLACE_THAT_OWNER_NATIVE_SOURCE":
        fail("observability event may not outrank owner-native authority")
    live = observability.get("live_projection", {})
    if live.get("version") != "oleander-execution-live-status/v1":
        fail("execution live-status projection version drift")
    check_ref(live.get("publisher_ref"))
    if set(live.get("required_fields", [])) != {"version", "task_id", "executor_id", "checkpoint_sequence", "status"}:
        fail("execution live-status required-field contract drift")
    if set(live.get("allowed_status_values", [])) != {"WORKING", "REVIEW_PENDING", "HOLD", "CLOSED"}:
        fail("execution live-status status vocabulary drift")
    if live.get("projection_is_project_state") is not False or live.get("projection_is_authority") is not False:
        fail("execution live-status must remain non-authoritative observability")
    if live.get("durable_event_or_incident_store") is not False or live.get("event_history_must_not_be_added_to_runtime_state") is not True:
        fail("runtime_state may not become a durable event/incident authority store")
    if live.get("newer_checkpoint_sequence_wins") is not True or live.get("same_sequence_requires_identical_stable_payload") is not True:
        fail("execution live-status checkpoint concurrency guard drift")

    incident = contract.get("recovery_incident", {})
    if incident.get("semantic_class") != "BOUNDED_INCIDENT_LIFECYCLE_NOT_PROJECT_STATE_FAMILY":
        fail("recovery incident must remain bounded and separate from Project State")
    if incident.get("lifecycle_scope") != "INCIDENT_LOCAL_ONLY":
        fail("recovery incident lifecycle must remain incident-local")
    if incident.get("owning_layer_values") != EXPECTED_LAYERS:
        fail("recovery incident owning-layer vocabulary must be exactly R-A..R-K")
    incident_fields = set(incident.get("required_fields", []))
    for required in {
        "incident_id", "failure_class", "failure_owner_ref", "owning_layer",
        "project_or_scope_id", "current_task_id", "decision_object_id", "authority_fingerprint",
        "source_revision", "trigger_source_ref", "blast_radius", "preserved_state", "containment",
        "recovery", "closure", "incident_state", "remaining_blockers", "next_allowed_action", "does_not_prove",
    }:
        if required not in incident_fields:
            fail(f"recovery incident required field missing: {required}")
    incident_conditional = incident.get("conditional_fields", {})
    if set(incident_conditional) != {"failure_code", "trigger_event_ref"}:
        fail("recovery incident conditional-field contract drift")
    recovery = graph.get("recovery", {})
    if set(incident.get("failure_classes", [])) != set(recovery.get("failure_classes", {}).keys()):
        fail("recovery incident failure-class vocabulary drift from architecture recovery owner")
    if incident.get("failure_class_actions") != recovery.get("failure_classes"):
        fail("recovery incident failure actions drift from architecture recovery owner")
    if incident.get("recovery_sequence", []) != recovery.get("sequence", []):
        fail("recovery incident sequence drift from architecture recovery owner")
    if not {"affected_layer_ids", "affected_handoff_refs", "affected_consumer_refs", "affected_claim_refs", "unaffected_verified_refs"}.issubset(set(incident.get("blast_radius_required_fields", []))):
        fail("recovery blast-radius contract incomplete")
    if "last_verified_state_refs" not in set(incident.get("preserved_state_required_fields", [])):
        fail("recovery must preserve last verified state refs")
    if not {"unsafe_or_duplicate_mutation_stopped", "containment_evidence_refs", "containment_complete"}.issubset(set(incident.get("containment_required_fields", []))):
        fail("recovery containment contract incomplete")
    if not {"selected_smallest_valid_action", "required_postcondition", "required_readback", "affected_review_rerun_refs", "affected_handoff_reacceptance_refs"}.issubset(set(incident.get("recovery_required_fields", []))):
        fail("recovery action/readback contract incomplete")
    if not {"recovery_readback_ref", "closure_evidence_refs", "resume_condition", "resume_decision_owner_ref"}.issubset(set(incident.get("closure_required_fields", []))):
        fail("recovery closure/resume contract incomplete")
    if incident.get("allowed_transitions", {}).get("CLOSED") != []:
        fail("closed incident must be terminal until an explicit reopen condition creates a new material incident/reopen decision")
    if incident.get("closed_incident_reentry_rule") != "A_NEW_MATERIAL_FAILURE_OR_CONTRADICTION_AFTER_CLOSURE_CREATES_A_SUCCESSOR_INCIDENT_OR_AN_EXPLICIT_OWNER_REOPEN_RECORD_WITH_PROVENANCE; THE_CLOSED_RECORD_IS_NOT_SILENTLY_REWRITTEN":
        fail("closed recovery incident may not be silently rewritten")
    incident_rules = set(incident.get("hard_rules", []))
    for required in {
        "INCIDENT_STATE_IS_NOT_PROJECT_STATE_JOB_STATE_REVIEW_STATE_OR_HANDOFF_STATE",
        "FAILURE_DOES_NOT_ERASE_UNRELATED_VERIFIED_STATE",
        "RECOVERY_SCOPE_IS_SMALLEST_VALID_BLAST_RADIUS",
        "CLOSED_REQUIRES_POST_RECOVERY_READBACK",
        "RECOVERY_MAY_REACCEPT_AFFECTED_HANDOFFS_ONLY_AFTER_REQUIRED_READBACK",
        "UNRELATED_HANDOFFS_AND_REVIEWS_ARE_NOT_REOPENED_BY_DEFAULT",
        "REMOTE_UNCERTAINTY_USES_VERIFY_BEFORE_RETRY",
    }:
        if required not in incident_rules:
            fail(f"recovery incident hard rule missing: {required}")

    binding = contract.get("execution_receipt_binding", {})
    if binding.get("prospective_only") is not True or binding.get("historical_receipts_immutable") is not True:
        fail("recovery incident receipt binding must remain prospective and preserve history")
    if binding.get("receipt_field") != "recovery_incident":
        fail("recovery incident receipt field drift")
    if binding.get("telemetry_only_event_must_not_create_receipt") is not True:
        fail("telemetry-only events may not create execution receipts")
    if binding.get("existing_receipt_remains_execution_truth_carrier") is not True:
        fail("recovery contract may not replace the Execution Receipt truth carrier")


def main() -> None:
    graph = load_graph()

    if graph.get("schema") != "oleander.architecture-control-graph.v2.1":
        fail("unexpected schema id")
    if graph.get("logical_object_id") != "OLEANDER-CURRENT-ARCHITECTURE-CONTROL":
        fail("logical object identity drift")
    if graph.get("version") != "2.1":
        fail("control graph must be v2.1")
    if graph.get("system_architecture_count") != 1:
        fail("OLEANDER must declare exactly one Current system architecture")
    if graph.get("master_runtime_count") != 1:
        fail("OLEANDER must declare exactly one Master Runtime")

    canonical = graph.get("canonical_markdown_ref")
    if canonical != "00-governance/runtime/OLEANDER_CURRENT_ARCHITECTURE_MAP_v2.1.md":
        fail("canonical markdown pointer drift")
    check_ref(canonical)

    master = graph.get("master_runtime", {})
    if master.get("ref") != "00-governance/complex-project-master-runtime-v1.0.md":
        fail("Master Runtime pointer drift")
    check_ref(master["ref"])

    order = graph.get("runtime_layer_order")
    if order != EXPECTED_LAYERS:
        fail(f"runtime layer order must be exactly {EXPECTED_LAYERS}")

    vocabulary = set(graph.get("maturity_vocabulary", []))
    if vocabulary != EXPECTED_MATURITY:
        fail("architecture-module maturity vocabulary drift")

    obs = set(graph.get("observability_required_fields", []))
    if obs != REQUIRED_OBSERVABILITY:
        fail("minimum observability field contract drift")

    planes = graph.get("planes", [])
    plane_ids = {p.get("id") for p in planes}
    if plane_ids != EXPECTED_PLANES:
        fail("cross-cutting plane set must be CONTROL/STATE/ACQUISITION_READER/EXECUTION/OBSERVABILITY/EVOLUTION")
    for plane in planes:
        if not plane.get("owns") or not plane.get("refs") or not plane.get("does_not_prove"):
            fail(f"incomplete plane contract: {plane.get('id')}")
        for ref in plane["refs"]:
            check_ref(ref)

    layers = graph.get("layers", [])
    ids = [layer.get("id") for layer in layers]
    if ids != EXPECTED_LAYERS:
        fail("layers array must contain each R-A..R-K exactly once in canonical order")
    if len(set(ids)) != 11:
        fail("duplicate runtime layer id")
    layers_by_id = {layer["id"]: layer for layer in layers}

    for layer in layers:
        layer_id = layer["id"]
        if not layer.get("name"):
            fail(f"{layer_id} missing name")
        if not layer.get("owner_refs"):
            fail(f"{layer_id} missing canonical owner_refs")
        for ref in layer["owner_refs"]:
            check_ref(ref)
        if layer.get("maturity") not in EXPECTED_MATURITY:
            fail(f"{layer_id} invalid maturity")
        if not layer.get("state_objects"):
            fail(f"{layer_id} missing state_objects")
        if not layer.get("control_actions"):
            fail(f"{layer_id} missing control_actions")
        if not layer.get("reopen_rule"):
            fail(f"{layer_id} missing reopen_rule")
        if not layer.get("observability"):
            fail(f"{layer_id} missing observability projection")
        if not layer.get("machine_cannot_award"):
            fail(f"{layer_id} missing machine authority boundary")

        for key in ("dependencies", "conditional_dependencies", "reopen_targets", "conditional_reopen_targets", "feedback_targets"):
            for target in layer.get(key, []):
                if target not in layers_by_id:
                    fail(f"{layer_id} {key} references unknown layer {target}")
                if key in {"dependencies", "conditional_dependencies"} and target == layer_id:
                    fail(f"{layer_id} may not depend on itself")

    validate_dag(layers_by_id)
    validate_layer_interface_contract(graph, layers_by_id, plane_ids)
    validate_observability_recovery_contract(graph, layers_by_id)

    feedback = graph.get("feedback_edges", [])
    if not feedback:
        fail("bounded feedback edge must be explicit")
    for edge in feedback:
        if edge.get("from") not in layers_by_id or edge.get("to") not in layers_by_id:
            fail("feedback edge references unknown layer")
        if edge.get("automatic_promotion") is not False:
            fail("G9 feedback may not auto-promote knowledge")

    professional = graph.get("professional_domain_process_state", [])
    by_domain = {row.get("domain"): row for row in professional}
    architecture = by_domain.get("Architecture")
    if not architecture:
        fail("Architecture process state missing")
    if architecture.get("state") != "FORMALIZED_PROJECT_EXERCISED":
        fail("Architecture reference-process state drift")
    check_ref(architecture.get("current_process_ref"))
    check_ref(architecture.get("machine_schema_ref"))
    if architecture.get("project_exercised_claim") is not True:
        fail("Architecture project-exercised reference claim drift")
    for domain in ("Structural Engineering", "Building Services / MEP"):
        row = by_domain.get(domain)
        if not row or row.get("state") != "FORMALIZED_MACHINE_BOUND":
            fail(f"{domain} must resolve as FORMALIZED_MACHINE_BOUND on the current main baseline")
        if row.get("project_exercised_claim") is not False:
            fail(f"{domain} may not infer project-exercised maturity from Current schema/document status")
        check_ref(row.get("current_process_ref"))
        check_ref(row.get("machine_schema_ref"))

    for domain, row in by_domain.items():
        if domain in {"Architecture", "Structural Engineering", "Building Services / MEP"}:
            continue
        if row.get("state") != "CONTRACT_ENVELOPE_AVAILABLE_PROCESS_OPEN":
            fail(f"{domain} must not be auto-promoted beyond current evidence")
        if row.get("current_process_ref") is not None:
            fail(f"{domain} declares a process ref while state remains PROCESS_OPEN")

    rights = graph.get("decision_rights", {})
    machine_denies = set(rights.get("machine_may_not", []))
    if not REQUIRED_MACHINE_DENIES.issubset(machine_denies):
        fail("machine/human authority firewall incomplete")
    if "HUMAN_PROMOTION_DECISION" not in set(rights.get("project_authority", [])):
        fail("human promotion authority missing")
    if "STATUTORY_OR_LICENSED_APPROVAL_WHERE_APPLICABLE" not in set(rights.get("external_authority", [])):
        fail("external statutory authority boundary missing")

    control_domains = graph.get("control_domains", {})
    file_domain = control_domains.get("FILE_ARTIFACT_MANAGEMENT", {})
    reader_domain = control_domains.get("AI_FILE_AND_READER", {})
    if file_domain.get("artifact_invariant") != "ONE_LOGICAL_ARTIFACT_ONE_CURRENT_REVISION_N_REPRESENTATIONS":
        fail("file/artifact logical identity invariant missing")
    if set(file_domain.get("representation_roles", [])) != {"SOURCE", "NATIVE", "CANONICAL", "PREVIEW", "PACKAGE"}:
        fail("file/artifact representation-role set drift")
    if file_domain.get("location_integrity_required") is not True or file_domain.get("blind_age_delete_forbidden") is not True:
        fail("file location/deletion safety boundary incomplete")
    for ref in file_domain.get("owner_refs", []):
        check_ref(ref)

    expected_read_ops = {"LIST", "SEARCH", "FIND", "READ", "MATERIALIZE", "PARSE_RENDER", "READBACK"}
    if set(reader_domain.get("read_operations", [])) != expected_read_ops:
        fail("AI file/Reader read-depth contract drift")
    if reader_domain.get("minimum_sufficient_access") is not True:
        fail("AI file handling must use minimum sufficient access")
    if reader_domain.get("canonical_derivative_separation_required") is not True:
        fail("Reader canonical/derivative separation must remain required")
    if reader_domain.get("partial_or_stale_readback_fails_closed") is not True:
        fail("partial/stale Reader readback must fail closed")
    required_firewall = {"CAN_READ_NOT_CAN_EDIT", "CAN_MATERIALIZE_NOT_CAN_OVERWRITE", "CAN_DERIVE_NOT_CAN_PROMOTE", "DERIVATIVE_INDEX_NOT_CANONICAL_AUTHORITY"}
    if not required_firewall.issubset(set(reader_domain.get("mutation_firewall", []))):
        fail("AI file/Reader mutation firewall incomplete")
    for ref in reader_domain.get("owner_refs", []):
        check_ref(ref)

    evolution = graph.get("evolution", {})
    evolution_contract = evolution.get("contract_ref")
    if evolution_contract != "00-governance/runtime/OLEANDER_EVOLUTION_CANDIDATE_CONTRACT_v1.0.json":
        fail("controlled evolution candidate contract pointer drift")
    check_ref(evolution_contract)
    if evolution.get("mode") != "CONTROLLED_EVOLUTION_NO_DIRECT_SELF_PROMOTION":
        fail("evolution mode must forbid direct self-promotion")
    if evolution.get("candidate_may_modify_live_baseline_during_eval") is not False:
        fail("evolution candidate may not modify its live evaluation baseline")
    if evolution.get("human_promotion_required") is not True:
        fail("evolution adoption requires human promotion")
    if evolution.get("rollback_required") is not True or evolution.get("migration_provenance_required") is not True:
        fail("evolution requires rollback and migration provenance")
    if evolution.get("one_success_may_universalize_rule") is not False:
        fail("one project success may not universalize an OLEANDER rule")
    required_evolution_steps = {"FREEZE_CURRENT_BASELINE", "GENERATE_ISOLATED_VARIANTS", "RUN_TARGET_SPECIFIC_EVALS", "RUN_CONSTRAINT_AND_REGRESSION_GATES", "INDEPENDENT_REVIEW", "HUMAN_PROMOTION_DECISION", "ACTUAL_READBACK", "POST_ADOPTION_MONITORING"}
    if not required_evolution_steps.issubset(set(evolution.get("loop", []))):
        fail("controlled evolution loop incomplete")
    protected = set(evolution.get("protected_targets", []))
    for required in {"CURRENT_AUTHORITY_IDENTITY", "ACTIVE_USER_CONSTRAINTS", "HUMAN_PROMOTION_RIGHT", "STATUTORY_LICENSED_AUTHORITY"}:
        if required not in protected:
            fail(f"evolution protected target missing: {required}")

    recovery = graph.get("recovery", {})
    if not REQUIRED_RECOVERY_STEPS.issubset(set(recovery.get("sequence", []))):
        fail("recovery sequence does not preserve bounded verified state/readback")
    if len(recovery.get("failure_classes", {})) < 8:
        fail("failure/recovery coverage too thin")

    compatibility = graph.get("compatibility", {})
    if set(compatibility.get("change_classes", [])) != REQUIRED_COMPAT_CLASSES:
        fail("architecture compatibility change classes drift")
    if "OLD_RECEIPT_NOT_SILENTLY_REINTERPRETED" not in set(compatibility.get("invariants", [])):
        fail("receipt compatibility boundary missing")

    trigger = graph.get("trigger_applicability_contract", {})
    if trigger.get("semantic_class") != "CONTROL_DECISION_RESULT_NOT_STATE_FAMILY":
        fail("trigger/applicability results must not create a new state family")
    if trigger.get("projection_only_not_replacement_schema") is not True or trigger.get("owner_native_trigger_fields_remain_authoritative") is not True:
        fail("trigger/applicability control must remain a projection over owner-native fields")
    if set(trigger.get("results", [])) != REQUIRED_TRIGGER_STATES:
        fail("trigger/applicability result contract drift")
    trigger_fields = set(trigger.get("required_fields", []))
    for required in {
        "decision_object_id",
        "scope",
        "trigger_owner",
        "applicability_result",
        "authority_fingerprint",
        "owner_native_basis_ref_or_fields",
    }:
        if required not in trigger_fields:
            fail(f"trigger/applicability required field missing: {required}")
    if trigger.get("not_required_requires_explicit_owner_native_basis") is not True:
        fail("NOT_REQUIRED trigger decision must remain traceable to owner-native non-trigger basis")
    if trigger.get("free_text_reason_field_not_universally_required") is not True:
        fail("architecture projection must not force a duplicate universal free-text reason field")
    if trigger.get("omission_is_not_not_required") is not True:
        fail("omission may not be treated as NOT_REQUIRED")
    if trigger.get("trigger_decision_does_not_award_pass") is not True:
        fail("trigger resolution may not award triggered owner PASS")
    if trigger.get("unresolved_material_trigger_fails_closed") is not True:
        fail("material unresolved trigger must fail closed")
    if trigger.get("unresolved_blocker_code") != "TRIGGER_APPLICABILITY_UNRESOLVED":
        fail("unresolved trigger must use a blocker code rather than a new runtime state")
    if set(trigger.get("unresolved_runtime_outcomes", [])) != {"BLOCKED", "RECONCILIATION_REQUIRED"}:
        fail("unresolved trigger must reuse existing Master Runtime outcomes")
    trigger_mapping = trigger.get("current_master_runtime_mapping", {})
    if trigger_mapping.get("triggered_true") != "TRIGGERED":
        fail("trigger projection must preserve current Master Runtime triggered=true semantics")
    if trigger_mapping.get("triggered_false_plus_explicit_native_not_required_or_na") != "NOT_REQUIRED":
        fail("trigger projection must preserve current Master Runtime non-trigger semantics")

    ceiling = graph.get("claim_ceiling_contract", {})
    if ceiling.get("projection_only_not_second_claim_ledger") is not True or ceiling.get("owner_native_claim_fields_remain_authoritative") is not True:
        fail("claim-ceiling compilation must not create a second claim ledger or steal owner authority")
    ceiling_fields = set(ceiling.get("input_required_fields", []))
    for required in {
        "owner",
        "claim_family_or_id",
        "scope",
        "ceiling_statement",
        "basis_refs",
        "blocking_or_limiting_conditions",
        "valid_until_or_revalidate_on",
        "authority_fingerprint",
    }:
        if required not in ceiling_fields:
            fail(f"claim-ceiling input field missing: {required}")
    if ceiling.get("universal_numeric_order_forbidden") is not True:
        fail("claim ceilings may not collapse into a universal numeric order")
    if set(ceiling.get("current_machine_compilation", [])) != {"claim_ceiling_inputs", "claim_ceiling_rule"}:
        fail("claim-ceiling projection must match current Master Runtime machine compilation floor")
    if ceiling.get("current_machine_rule") != "LOWEST_APPLICABLE_VALID_CLAIM_GOVERNS; MACHINE_DOES_NOT_RANK_DOMAIN_SPECIFIC_CLAIM_TEXT":
        fail("claim-ceiling projection must preserve current Master Runtime opaque-text boundary")
    if ceiling.get("richer_effective_envelope_requires_comparable_owner_semantics_or_authorized_human_judgment") is not True:
        fail("richer claim envelope must require comparable owner semantics or authorized judgment")
    if ceiling.get("machine_may_not_infer_semantic_conflict_by_ranking_opaque_claim_text") is not True:
        fail("machine may not infer semantic claim conflicts by ranking opaque claim strings")
    if ceiling.get("conflict_blocker_code") != "CLAIM_CEILING_CONFLICT":
        fail("claim-ceiling conflict must be represented as a blocker code")
    if set(ceiling.get("conflict_runtime_outcomes", [])) != {"BLOCKED", "RECONCILIATION_REQUIRED"}:
        fail("claim-ceiling conflict must reuse existing Master Runtime outcomes")
    if ceiling.get("stronger_unrelated_owner_cannot_widen_weaker_consumed_boundary") is not True:
        fail("unrelated stronger claim ceiling may not widen a weaker consumed boundary")
    if ceiling.get("promotion_must_bind_effective_envelope") is not True:
        fail("promotion must bind the effective claim envelope")

    frontier = graph.get("execution_frontier_concurrency", {})
    for ref in frontier.get("owner_refs", []):
        check_ref(ref)
    if frontier.get("mode") != "OPTIMISTIC_CHECKPOINT_SEQUENCE":
        fail("execution frontier concurrency mode drift")
    if frontier.get("sequence_is_authoritative") is not True:
        fail("checkpoint sequence must remain concurrency truth")
    if frontier.get("lease_metadata_is_advisory_only") is not True or frontier.get("lease_does_not_grant_authority") is not True:
        fail("execution lease metadata must remain advisory and non-authoritative")
    if frontier.get("global_lock_service_forbidden") is not True:
        fail("architecture must not introduce a global lock service")
    if frontier.get("blind_last_writer_wins_forbidden") is not True:
        fail("blind last-writer-wins must remain forbidden")
    if frontier.get("chat_summary_is_not_checkpoint_authority") is not True:
        fail("chat summary may not become checkpoint authority")
    if frontier.get("sequence_mismatch_state") != "REVALIDATE_CONCURRENT_ADVANCE":
        fail("checkpoint sequence mismatch must force concurrent revalidation")
    if frontier.get("uncertain_remote_mutation_rule") != "VERIFY_EXPECTED_POSTCONDITION_BEFORE_RETRY":
        fail("uncertain remote mutation must use verify-before-retry")
    if frontier.get("blind_duplicate_create_retry_forbidden") is not True:
        fail("blind duplicate create retry must remain forbidden")
    if frontier.get("parallel_convergence_requires_current_readback") is not True:
        fail("parallel convergence must require Current readback")
    if frontier.get("background_execution_implied") is not False:
        fail("continuous/current-turn execution must not imply background execution")

    drift = graph.get("current_drift_reconciliation", {})
    if drift.get("projection_only_not_replacement_state_machine") is not True or drift.get("surface_native_drift_or_sync_owner_remains_authoritative") is not True:
        fail("drift reconciliation must remain a projection over existing surface owners")
    if drift.get("reference_state_owner") != "OLEANDER_NOTION_GITHUB_DRIFT_CHECK_v0.1":
        fail("drift reference vocabulary owner must remain the current Notion↔GitHub drift contract")
    if drift.get("other_surface_states_not_forced") is not True:
        fail("Notion↔GitHub drift states may not be forced onto other surface-native state machines")
    for ref in drift.get("owner_refs", []):
        check_ref(ref)
    if set(drift.get("notion_github_reference_states", [])) != REQUIRED_NOTION_GITHUB_REFERENCE_DRIFT_STATES:
        fail("Notion↔GitHub reference drift-state vocabulary drift")
    if drift.get("newest_timestamp_is_not_authority") is not True:
        fail("drift reconciliation may not use newest timestamp as authority")
    if drift.get("diverged_requires_explicit_reconciliation") is not True:
        fail("DIVERGED state must require explicit reconciliation")
    if drift.get("missing_does_not_authorize_parallel_owner_creation") is not True:
        fail("MISSING drift may not authorize parallel owner creation")
    if drift.get("unknown_fails_closed_when_claim_depends_on_cross_surface_certainty") is not True:
        fail("UNKNOWN drift must fail closed for dependent cross-surface claims")
    if drift.get("static_repo_check_cannot_claim_live_cross_platform_current") is not True:
        fail("static repository check may not claim live cross-platform CURRENT")
    if drift.get("sync_requires_target_platform_readback") is not True:
        fail("sync must require target-platform readback")
    if drift.get("preserve_last_verified_state_and_provenance") is not True:
        fail("drift repair must preserve last verified state and provenance")

    invariants = set(graph.get("hard_invariants", []))
    for invariant in {
        "ONE_SYSTEM_ARCHITECTURE",
        "ONE_MASTER_RUNTIME",
        "EXACTLY_11_RUNTIME_LAYERS",
        "NO_MACHINE_DESIGN_PROMOTION",
        "PRESERVE_VALID_STATE_DURING_RECOVERY",
        "READ_SURFACE_IS_NOT_AUTHORITY",
        "ONE_LOGICAL_ARTIFACT_ONE_CURRENT_REVISION_N_REPRESENTATIONS",
        "EVOLUTION_CANDIDATE_NO_SELF_PROMOTION",
        "EVOLUTION_REQUIRES_FROZEN_BASELINE_EVAL_REVIEW_HUMAN_PROMOTION",
        "EVOLUTION_REQUIRES_ROLLBACK_AND_PROVENANCE",
        "CONDITIONAL_RESPONSIBILITY_REQUIRES_EXPLICIT_APPLICABILITY_RESULT",
        "OMISSION_IS_NOT_NOT_REQUIRED",
        "CLAIM_CEILING_NO_UNIVERSAL_NUMERIC_COLLAPSE",
        "CLAIM_CEILING_CONFLICT_FAILS_CLOSED",
        "CHECKPOINT_SEQUENCE_GUARDS_MATERIAL_MUTATION",
        "BLIND_LAST_WRITER_WINS_FORBIDDEN",
        "VERIFY_REMOTE_POSTCONDITION_BEFORE_RETRY",
        "STATIC_REPO_CHECK_NOT_LIVE_CROSS_PLATFORM_CURRENT",
        "DRIFT_RECONCILIATION_PRESERVES_CANONICAL_OWNER",
        "RUNTIME_LAYER_INTERFACE_CONTRACT_REQUIRED",
        "PRODUCER_CANNOT_SELF_ACCEPT_HANDOFF",
        "HANDOFF_ACCEPTED_DOES_NOT_PROVE_DOWNSTREAM_PASS",
        "NO_UNIVERSAL_LAYER_PROGRESS_STATE",
        "OBSERVABILITY_EVENT_NOT_AUTHORITY",
        "RECOVERY_INCIDENT_NOT_PROJECT_STATE",
        "RECOVERY_BLAST_RADIUS_PRESERVES_UNAFFECTED_VALID_STATE",
        "RECOVERY_CLOSURE_REQUIRES_ACTUAL_READBACK",
        "INCIDENT_CLOSED_DOES_NOT_PROVE_DESIGN_PROFESSIONAL_OR_PROMOTION_PASS",
        "RECOVERY_REACCEPTS_ONLY_AFFECTED_HANDOFFS_AFTER_REQUIRED_READBACK",
        "LIVE_STATUS_REMAINS_OBSERVABILITY_ONLY",
    }:
        if invariant not in invariants:
            fail(f"missing hard invariant {invariant}")

    print("ARCHITECTURE CONTROL VALIDATION: PASS")
    print("system_architecture_count=1")
    print("master_runtime_count=1")
    print("runtime_layers=11")
    print("professional_reference_process=Architecture")
    print("control_graph_version=2.1")
    print("operational_planes=6")
    print("file_artifact_control=PASS")
    print("knowledge_reader_control=PASS")
    print("controlled_evolution=PASS")
    print("trigger_applicability_projection_definition=PASS")
    print("claim_ceiling_projection_definition=PASS")
    print("execution_frontier_concurrency=PASS")
    print("current_drift_reconciliation_projection=PASS")
    print("runtime_layer_interfaces=PASS")
    print("observability_recovery_contract=PASS")


if __name__ == "__main__":
    main()
