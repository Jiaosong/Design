#!/usr/bin/env python3
from __future__ import annotations

import json
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "00-governance" / "runtime" / "OLEANDER_ARCHITECTURE_CONTROL_GRAPH_v2.1.json"
LAYER_INTERFACE = ROOT / "00-governance" / "runtime" / "OLEANDER_RUNTIME_LAYER_INTERFACE_CONTRACT_v1.0.json"
OBSERVABILITY_RECOVERY = ROOT / "00-governance" / "runtime" / "OLEANDER_OBSERVABILITY_RECOVERY_CONTRACT_v1.0.json"
EVOLUTION_CANDIDATE = ROOT / "00-governance" / "runtime" / "OLEANDER_EVOLUTION_CANDIDATE_CONTRACT_v1.0.json"
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


def _git_output(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True, encoding="utf-8").strip()


def _validate_professional_candidate_mutation_manifest(candidate_record: dict, binding: dict) -> dict:
    manifest_ref = binding.get("mutation_manifest_ref")
    manifest_id = binding.get("mutation_manifest_id")
    if not manifest_ref or not manifest_id:
        fail("professional-process Candidate binding missing exact mutation manifest ref/id")
    manifest_path = ROOT / manifest_ref
    if not manifest_path.is_file():
        fail(f"professional-process Candidate mutation manifest missing: {manifest_ref}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("manifest_id") != manifest_id:
        fail("professional-process Candidate mutation manifest id drift")
    baseline = candidate_record.get("baseline", {}).get("source_hash_or_commit")
    if manifest.get("baseline_commit") != baseline:
        fail("professional-process Candidate mutation manifest baseline drift")
    expected_source_revision = f"origin/main@{baseline}+manifest:{manifest_id}"
    if binding.get("source_revision_or_commit") != expected_source_revision:
        fail("professional-process Candidate source_revision_or_commit does not bind the exact mutation manifest")

    entries = manifest.get("material_files", [])
    if not entries or manifest.get("material_delta_count") != len(entries):
        fail("professional-process Candidate mutation manifest material file count drift")
    manifest_paths: list[str] = []
    for entry in entries:
        rel = str(entry.get("path") or "")
        if not rel or rel in manifest_paths:
            fail("professional-process Candidate mutation manifest has empty/duplicate path")
        manifest_paths.append(rel)
        path = ROOT / rel
        if not path.is_file():
            fail(f"professional-process Candidate manifest file missing: {rel}")
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry.get("sha256"):
            fail(f"professional-process Candidate manifest SHA256 stale: {rel}")
        if len(raw) != entry.get("bytes"):
            fail(f"professional-process Candidate manifest byte count stale: {rel}")
        if _git_output("git", "hash-object", rel) != entry.get("git_blob"):
            fail(f"professional-process Candidate manifest Git blob stale: {rel}")

    scope_exclusion_prefixes = manifest.get("scope_exclusion_prefixes", [])
    if not isinstance(scope_exclusion_prefixes, list) or any(
        not isinstance(prefix, str) or not prefix for prefix in scope_exclusion_prefixes
    ):
        fail("professional-process Candidate mutation manifest scope exclusion prefixes malformed")
    allowed_sync_prefix = "00-governance/receipts/OLEANDER_PROFESSIONAL_STAGE_SKILL_COMPOSITION_SYNC_"
    if any(prefix != allowed_sync_prefix for prefix in scope_exclusion_prefixes):
        fail("professional-process Candidate mutation manifest uses an unbounded scope exclusion prefix")

    fingerprint_payload = "\n".join(
        [
            f"baseline={manifest.get('baseline_commit')}",
            f"manifest_id={manifest_id}",
            *[f"scope_exclusion_prefix={prefix}" for prefix in scope_exclusion_prefixes],
        ]
        + [
            f"{entry['path']}|{entry['sha256']}|{entry['git_blob']}|{entry['bytes']}"
            for entry in entries
        ]
    )
    fingerprint = hashlib.sha256(fingerprint_payload.encode("utf-8")).hexdigest()
    if manifest.get("manifest_content_fingerprint_sha256") != fingerprint:
        fail("professional-process Candidate mutation manifest fingerprint drift")

    current_changed = set(
        filter(None, _git_output("git", "diff", "--name-only", baseline, "--").splitlines())
    )
    current_untracked = set(
        filter(None, _git_output("git", "ls-files", "--others", "--exclude-standard").splitlines())
    )
    current_material = (current_changed | current_untracked) - {str(manifest_ref)}
    current_material = {
        rel
        for rel in current_material
        if not any(rel.startswith(prefix) for prefix in scope_exclusion_prefixes)
    }
    if current_material != set(manifest_paths):
        missing = sorted(current_material - set(manifest_paths))
        stale = sorted(set(manifest_paths) - current_material)
        fail(
            "professional-process Candidate mutation manifest scope drift: "
            f"unlisted_current={missing} stale_manifest_entries={stale}"
        )

    for assertion in manifest.get("unchanged_current_professional_machine_assertions", []):
        rel = assertion.get("path")
        if not rel:
            fail("professional-process Candidate manifest has malformed Current-machine assertion")
        base_blob = _git_output("git", "rev-parse", f"{baseline}:{rel}")
        worktree_blob = _git_output("git", "hash-object", rel)
        if assertion.get("base_git_blob") != base_blob or assertion.get("working_tree_git_blob") != worktree_blob:
            fail(f"professional-process Candidate Current-machine assertion stale: {rel}")
        if worktree_blob != base_blob or assertion.get("unchanged") is not True:
            fail(f"professional-process Candidate illegally mutates Current professional machine: {rel}")
    return manifest
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

    transaction = common.get("multi_surface_transaction_projection", {})
    if transaction.get("semantic_class") != "EPHEMERAL_RECONCILIATION_RESULT_NOT_STATE_FAMILY_OR_TRANSACTION_SERVICE":
        fail("runtime layer transaction projection must remain an ephemeral reconciliation result")
    for ref in transaction.get("semantic_owner_refs", []):
        check_ref(ref)
    check_ref(transaction.get("runtime_implementation_ref"))
    expected_transaction_fields = {
        "project_or_scope_id", "task_id", "decision_object_id", "authority_fingerprint",
        "mutation_scope", "legs", "reconciliation_result", "reconciliation_action", "advance_allowed",
        "readback_refs", "observed_at", "does_not_prove",
    }
    if set(transaction.get("projection_fields", [])) != expected_transaction_fields:
        fail("runtime layer transaction projection field set drift")
    expected_leg_fields = {
        "surface_id", "side_effect_class", "operation_fingerprint", "expected_postcondition",
        "state", "retry_safe", "idempotent_or_provider_keyed", "compensation_legal", "readback_ref",
    }
    if set(transaction.get("leg_fields", [])) != expected_leg_fields:
        fail("runtime layer transaction leg field set drift")
    if set(transaction.get("leg_observation_values", [])) != {"CONFIRMED", "ABSENT", "UNCERTAIN"}:
        fail("runtime layer transaction leg observation vocabulary drift")
    if set(transaction.get("reconciliation_results", [])) != {"COHERENT_COMMIT", "PARTIAL_COMMIT", "HOLD"}:
        fail("runtime layer transaction reconciliation result vocabulary drift")
    for required_true in {
        "result_is_ephemeral_runtime_fact_not_project_state",
        "dependent_handoff_ready_requires_coherent_commit",
        "dependent_handoff_acceptance_requires_coherent_commit",
        "dag_advance_requires_coherent_commit",
        "compensation_requires_existing_legal_authorized_path",
        "compensation_is_not_general_rollback_guarantee",
        "distributed_transaction_manager_forbidden",
        "persistent_transaction_ledger_forbidden",
        "global_lock_service_forbidden",
    }:
        if transaction.get(required_true) is not True:
            fail(f"runtime layer transaction boundary missing {required_true}")
    expected_transaction_actions = {
        "uncertain_leg_action": "VERIFY_UNCERTAIN_LEGS_BEFORE_ADVANCE",
        "absent_safe_leg_action": "RECONCILE_MISSING_LEGS_BEFORE_ADVANCE",
        "unsafe_missing_with_legal_compensation_action": "COMPENSATE_CONFIRMED_LEGS_BEFORE_ADVANCE",
        "unsafe_unreconciled_action": "HOLD_PARTIAL_COMMIT_UNRECONCILED",
        "all_legs_confirmed_action": "ADVANCE_AFTER_COHERENT_COMMIT",
    }
    for key, expected in expected_transaction_actions.items():
        if transaction.get(key) != expected:
            fail(f"runtime layer transaction action drift: {key}")

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
    authorization_binding = incident.get("authorization_binding", {})
    for required_true in {
        "failure_owner_ref_is_reference_not_grant",
        "resume_decision_owner_ref_is_reference_not_grant",
        "consequential_resume_requires_current_decision_authorization_projection",
        "unresolved_authorization_fails_closed",
        "authorization_change_revalidates_affected_recovery_decision",
    }:
        if authorization_binding.get(required_true) is not True:
            fail(f"recovery authorization binding missing {required_true}")
    if graph.get("decision_rights", {}).get("authorization_projection", {}).get("owner_native_authority_remains_authoritative") is not True:
        fail("recovery incident owner refs require the current decision-authorization projection")
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
        "INCIDENT_OWNER_REFS_DO_NOT_GRANT_AUTHORITY",
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
    stage_chain = graph.get("professional_stage_canonical_execution_chain", {})
    expected_stage_chain = [
        "PROFESSIONAL_STAGE",
        "PROFESSIONAL_QUESTION_OR_DECISION_OBJECT",
        "KNOWLEDGE_INPUTS",
        "OPERATIONAL_KNOWLEDGE_MOUNT",
        "REQUIRED_CAPABILITY_ROLES",
        "CURRENT_EXECUTION_OWNERS_OR_SKILLS",
        "NATIVE_OUTPUTS",
        "ACTUAL_READBACK",
        "INDEPENDENT_REVIEW",
        "STAGE_CLOSURE",
    ]
    if stage_chain.get("chain") != expected_stage_chain:
        fail("architecture control graph professional-stage canonical execution chain drift")
    if stage_chain.get("authority_rule") != "ONE_CANONICAL_TOP_LEVEL_STAGE_SPINE_ACROSS_ALL_PROFESSIONAL_DOMAINS":
        fail("architecture control graph professional-stage spine authority rule drift")
    if "MUST_NOT_CREATE_AN_EXTRA_TOP_LEVEL_PROFESSIONAL_STAGE_STEP" not in str(
        stage_chain.get("auxiliary_binding_rule") or ""
    ):
        fail("architecture control graph must keep auxiliary bindings subordinate to canonical stage spine")
    if "INDEPENDENT_REVIEW" not in str(stage_chain.get("closure_rule") or ""):
        fail("architecture control graph Stage Closure must require triggered Independent Review")

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
        if row.get("candidate_evaluation_mode") != "BOUNDED_NON_CURRENT_PROJECT_EXERCISE":
            fail(f"{domain} PROCESS_OPEN candidate must use bounded non-Current project exercise mode")
        if row.get("project_exercised_claim") is not False:
            fail(f"{domain} candidate exercise evidence may not become a Current project-exercised claim")
        for candidate_ref_field in (
            "candidate_process_ref",
            "candidate_machine_schema_ref",
            "candidate_evolution_ref",
        ):
            candidate_ref = row.get(candidate_ref_field)
            if not candidate_ref:
                fail(f"{domain} PROCESS_OPEN candidate missing {candidate_ref_field}")
            check_ref(candidate_ref)
        candidate_record = json.loads(
            (ROOT / row["candidate_evolution_ref"]).read_text(encoding="utf-8")
        )
        candidate_contract = json.loads(EVOLUTION_CANDIDATE.read_text(encoding="utf-8"))
        for required in candidate_contract.get("required_candidate_fields", []):
            if required not in candidate_record:
                fail(f"{domain} candidate evolution record missing required field {required}")
        for object_key, contract_field_key in (
            ("baseline", "baseline_required_fields"),
            ("evaluation", "evaluation_required_fields"),
            ("constraints", "constraint_required_fields"),
            ("comparison", "comparison_required_fields"),
            ("independent_review", "independent_review_required_fields"),
            ("promotion", "promotion_required_fields"),
            ("migration", "migration_required_fields"),
            ("rollback", "rollback_required_fields"),
            ("monitoring", "monitoring_required_fields"),
        ):
            payload = candidate_record.get(object_key, {})
            for required in candidate_contract.get(contract_field_key, []):
                if required not in payload:
                    fail(f"{domain} candidate evolution {object_key} missing required field {required}")
        if candidate_record.get("state") not in {
            "EV1_CANDIDATE",
            "EV2_EVAL_READY",
            "EV3_EVAL_PASSED",
            "EV4_INDEPENDENT_REVIEWED",
            "EV5_PROMOTION_READY",
            "EVH_HOLD",
        }:
            fail(f"{domain} candidate evolution state is not legal for bounded evaluation")
        if candidate_record.get("target_class") != "PROFESSIONAL_PROCESS_DEFINITIONS":
            fail(f"{domain} candidate evolution record target_class drift")
        if candidate_record.get("target_ref") != row.get("candidate_machine_schema_ref"):
            fail(f"{domain} candidate evolution target_ref does not match graph machine candidate")
        binding = candidate_record.get("candidate_definition_binding", {})
        if binding.get("prose_ref") != row.get("candidate_process_ref"):
            fail(f"{domain} candidate evolution prose binding does not match graph candidate")
        if binding.get("machine_ref") != row.get("candidate_machine_schema_ref"):
            fail(f"{domain} candidate evolution machine binding does not match graph candidate")
        _validate_professional_candidate_mutation_manifest(candidate_record, binding)
        machine_path = ROOT / row["candidate_machine_schema_ref"]
        actual_machine_sha256 = hashlib.sha256(machine_path.read_bytes()).hexdigest()
        if binding.get("machine_sha256") != actual_machine_sha256:
            fail(f"{domain} candidate evolution machine_sha256 is stale")
        machine_definition = json.loads(machine_path.read_text(encoding="utf-8"))
        machine_stages = machine_definition.get("stages", [])
        if binding.get("stage_count") != len(machine_stages):
            fail(f"{domain} candidate evolution stage_count is stale")
        distinct_profiles = {
            tuple(
                stage.get("stage_execution_requirements", {}).get(
                    "required_capability_roles", []
                )
            )
            for stage in machine_stages
        }
        if any(
            not isinstance(stage.get("stage_execution_requirements"), dict)
            or not stage.get("stage_execution_requirements", {}).get("required_capability_roles")
            for stage in machine_stages
        ):
            fail(f"{domain} Candidate stages must declare non-empty stage_execution_requirements")
        if binding.get("distinct_required_capability_profiles") != len(distinct_profiles):
            fail(f"{domain} candidate evolution capability-profile count is stale")
        runtime_exercise = candidate_record.get("runtime_exercise", {})
        if runtime_exercise.get("current_candidate_revision_exercised") is True:
            real_project_counted = runtime_exercise.get("real_project_exercise_counted") is True
            graph_evidence_state = str(row.get("candidate_project_exercise_evidence_state") or "")
            if real_project_counted and (
                "CURRENT_REVISION" not in graph_evidence_state
                or "NOT_PROJECT_ADOPTION" in graph_evidence_state
            ):
                fail(f"{domain} graph candidate evidence state understates or contradicts counted real-project reapplication")
            if not real_project_counted and "NOT_PROJECT_ADOPTION" not in graph_evidence_state:
                fail(f"{domain} graph must explicitly preserve non-project-adoption ceiling for bounded context reapplication")
            if runtime_exercise.get("current_candidate_stage_composition_owner_resolution_exercised") is not True:
                fail(f"{domain} current-revision exercise must include stage composition owner-resolution readback")
            if runtime_exercise.get("current_candidate_knowledge_mount_gate_exercised") is not True:
                fail(f"{domain} current-revision exercise must execute the task/claim Knowledge Mount gate")
            real_case_refs = candidate_record.get("evaluation", {}).get("real_case_refs", [])
            if not real_case_refs:
                fail(f"{domain} current-revision exercise has no real_case_refs")
            for real_case_ref in real_case_refs:
                check_ref(real_case_ref)
            recovery = candidate_record.get("continuation_recovery", {})
            evaluation_receipt_ref = recovery.get("evaluation_receipt_ref")
            successor_receipt_ref = recovery.get("successor_receipt_ref")
            checkpoint_ref = recovery.get("continuation_checkpoint_ref")
            if not evaluation_receipt_ref or not checkpoint_ref:
                fail(f"{domain} current-revision HOLD evaluation must bind evaluation receipt and continuation checkpoint")
            check_ref(evaluation_receipt_ref)
            check_ref(checkpoint_ref)
            evaluation_receipt = json.loads((ROOT / evaluation_receipt_ref).read_text(encoding="utf-8"))
            checkpoint = json.loads((ROOT / checkpoint_ref).read_text(encoding="utf-8"))
            if evaluation_receipt.get("current_candidate_revision_exercised") is not True:
                fail(f"{domain} evaluation receipt does not prove current candidate revision evaluation")
            if evaluation_receipt.get("stage_composition_owner_resolution_exercised") is not True:
                fail(f"{domain} evaluation receipt lacks stage composition owner-resolution readback")
            if evaluation_receipt.get("knowledge_mount_gate_exercised") is not True:
                fail(f"{domain} evaluation receipt lacks Knowledge Mount gate readback")
            evaluation_binding = evaluation_receipt.get("candidate_binding", {})
            if evaluation_binding.get("machine_ref") != row.get("candidate_machine_schema_ref"):
                fail(f"{domain} evaluation receipt candidate machine ref drift")
            if evaluation_binding.get("machine_sha256") != actual_machine_sha256:
                fail(f"{domain} evaluation receipt candidate machine hash is stale")
            if checkpoint.get("candidate_process_ref") != row.get("candidate_machine_schema_ref"):
                fail(f"{domain} continuation checkpoint candidate process ref drift")
            if checkpoint.get("candidate_machine_sha256") != actual_machine_sha256:
                fail(f"{domain} continuation checkpoint candidate machine hash is stale")
            if checkpoint.get("release_condition_readback") != "UNSATISFIED":
                fail(f"{domain} current HOLD evaluation currently claims a release condition other than evidenced UNSATISFIED")
            if evaluation_receipt.get("hold_release_condition_satisfied") is not False:
                fail(f"{domain} evaluation receipt must not claim HOLD release while release evidence is absent")
            if evaluation_receipt.get("selective_retest_executed") is not False:
                fail(f"{domain} evaluation receipt may not claim selective retest before release")
            if successor_receipt_ref is not None or evaluation_receipt.get("successor_receipt_ref") is not None:
                fail(f"{domain} may not emit a successor receipt before release and actual selective retest")
            stage_evidence = candidate_record.get("stage_composition_evidence", {})
            required_stage_evidence_fields = {
                "stage_scope",
                "canonical_stage_execution_chain",
                "professional_question_or_decision_object_refs",
                "knowledge_inputs",
                "operational_knowledge_mount_refs",
                "required_capability_roles",
                "resolved_owner_set",
                "native_output_refs",
                "multi_skill_dag_ref_or_single_owner_justification",
                "typed_handoff_refs",
                "actual_readback_refs",
                "independent_review_refs",
                "stage_closure_state",
                "omitted_capability_reasoning",
            }
            missing_stage_evidence_fields = sorted(
                required_stage_evidence_fields - set(stage_evidence)
            )
            if missing_stage_evidence_fields:
                fail(
                    f"{domain} stage-composition evidence missing canonical chain fields: "
                    + ", ".join(missing_stage_evidence_fields)
                )
            expected_stage_chain = [
                "PROFESSIONAL_STAGE",
                "PROFESSIONAL_QUESTION_OR_DECISION_OBJECT",
                "KNOWLEDGE_INPUTS",
                "OPERATIONAL_KNOWLEDGE_MOUNT",
                "REQUIRED_CAPABILITY_ROLES",
                "CURRENT_EXECUTION_OWNERS_OR_SKILLS",
                "NATIVE_OUTPUTS",
                "ACTUAL_READBACK",
                "INDEPENDENT_REVIEW",
                "STAGE_CLOSURE",
            ]
            if stage_evidence.get("canonical_stage_execution_chain") != expected_stage_chain:
                fail(f"{domain} stage-composition evidence canonical stage chain order drift")
            for evidence_ref in stage_evidence.get("actual_readback_refs", []):
                check_ref(evidence_ref)
            comparison_ref = candidate_record.get("comparison", {}).get("evidence_ref")
            if not comparison_ref:
                fail(f"{domain} current-revision exercised candidate must bind baseline-vs-candidate comparison evidence")
            check_ref(comparison_ref)
            comparison = json.loads((ROOT / comparison_ref).read_text(encoding="utf-8"))
            if comparison.get("target_class") != "PROFESSIONAL_PROCESS_DEFINITIONS":
                fail(f"{domain} comparison evidence target_class drift")
            if comparison.get("candidate", {}).get("professional_machine_stage_count") != 79:
                fail(f"{domain} comparison evidence professional stage-count drift")
            if comparison.get("candidate", {}).get("unique_required_and_supporting_capability_roles") != 308:
                fail(f"{domain} comparison evidence capability-role count drift")
            if comparison.get("candidate", {}).get("roles_using_unnamed_owner_routing_fallback") != 0:
                fail(f"{domain} comparison evidence must preserve zero unnamed routing fallbacks")
        candidate_state = candidate_record.get("state")
        if candidate_state in {"EV3_EVAL_PASSED", "EV4_INDEPENDENT_REVIEWED", "EV5_PROMOTION_READY"}:
            if candidate_record.get("evaluation", {}).get("result") != "PASS":
                fail(f"{domain} {candidate_state} requires evaluation.result=PASS")
            if runtime_exercise.get("real_project_exercise_counted") is not True:
                fail(f"{domain} {candidate_state} requires at least one authentic real-project exercise")
            stage_evidence = candidate_record.get("stage_composition_evidence", {})
            if stage_evidence.get("knowledge_mount_gate") != "PASS":
                fail(f"{domain} {candidate_state} requires task/claim Knowledge Mount gate PASS")
            if not stage_evidence.get("operational_knowledge_mount_refs"):
                fail(f"{domain} {candidate_state} requires mounted operational knowledge refs")
            if not stage_evidence.get("native_output_refs"):
                fail(f"{domain} {candidate_state} requires native-output evidence in the canonical stage chain")
            if not stage_evidence.get("actual_readback_refs"):
                fail(f"{domain} {candidate_state} requires stage composition actual readback evidence")
            if not stage_evidence.get("independent_review_refs"):
                fail(f"{domain} {candidate_state} requires independent-review evidence before stage closure")
            if stage_evidence.get("stage_closure_state") != "PASS":
                fail(f"{domain} {candidate_state} requires canonical Stage Closure PASS")
        if candidate_state in {"EV4_INDEPENDENT_REVIEWED", "EV5_PROMOTION_READY"}:
            review = candidate_record.get("independent_review", {})
            if review.get("independence_state") != "INDEPENDENT":
                fail(f"{domain} {candidate_state} requires an independent domain-professional reviewer")
            if review.get("reviewer_id") in {None, "", "NOT_ASSIGNED"}:
                fail(f"{domain} {candidate_state} requires a bound reviewer identity")
            if review.get("review_input_revision") != actual_machine_sha256:
                fail(f"{domain} {candidate_state} independent review must bind the exact Candidate machine revision")
            if review.get("verdict") != "PASS":
                fail(f"{domain} {candidate_state} requires independent review verdict PASS")
        if candidate_state == "EV5_PROMOTION_READY":
            recovery = candidate_record.get("continuation_recovery", {})
            if runtime_exercise.get("current_candidate_hold_release_selective_retest_exercised") is not True:
                fail(f"{domain} EV5 requires an actual post-release selective retest")
            if recovery.get("release_condition_readback") != "SATISFIED_ON_CURRENT_CANDIDATE_REVISION":
                fail(f"{domain} EV5 requires release-condition satisfaction readback")
            if recovery.get("selective_retest_readback") != "PASS_AFFECTED_BINDINGS_ONLY":
                fail(f"{domain} EV5 requires affected-binding selective retest PASS readback")
            successor_ref = recovery.get("successor_receipt_ref")
            if not successor_ref:
                fail(f"{domain} EV5 requires a successor receipt bound to the retest result")
            check_ref(successor_ref)
            successor = json.loads((ROOT / successor_ref).read_text(encoding="utf-8"))
            if successor.get("hold_release_condition_satisfied") is not True:
                fail(f"{domain} EV5 successor receipt must bind satisfied release condition")
            if successor.get("selective_retest_executed") is not True:
                fail(f"{domain} EV5 successor receipt must bind actual selective retest")
            stage_evidence = candidate_record.get("stage_composition_evidence", {})
            resolved_owner_set = stage_evidence.get("resolved_owner_set", [])
            dag_ref = stage_evidence.get("multi_skill_dag_ref_or_single_owner_justification")
            typed_handoffs = stage_evidence.get("typed_handoff_refs", [])
            if len(resolved_owner_set) > 1:
                if not dag_ref or str(dag_ref).startswith("NOT_"):
                    fail(f"{domain} EV5 multi-owner stage requires a materialized Multi-Skill DAG ref")
                check_ref(dag_ref)
                if not typed_handoffs:
                    fail(f"{domain} EV5 multi-owner stage requires typed-handoff records")
                for handoff_ref in typed_handoffs:
                    check_ref(handoff_ref)
            if candidate_record.get("adoption_blockers"):
                fail(f"{domain} EV5 may not retain adoption blockers")
        if candidate_record.get("promotion", {}).get("eligible") is True and candidate_state != "EV5_PROMOTION_READY":
            fail(f"{domain} candidate cannot be promotion-eligible before EV5_PROMOTION_READY")
        if candidate_state != "EV5_PROMOTION_READY" and candidate_record.get("promotion", {}).get("eligible") is True:
            fail(f"{domain} non-EV5 candidate may not be promotion eligible")

    rights = graph.get("decision_rights", {})
    machine_denies = set(rights.get("machine_may_not", []))
    if not REQUIRED_MACHINE_DENIES.issubset(machine_denies):
        fail("machine/human authority firewall incomplete")
    if "HUMAN_PROMOTION_DECISION" not in set(rights.get("project_authority", [])):
        fail("human promotion authority missing")
    if "STATUTORY_OR_LICENSED_APPROVAL_WHERE_APPLICABLE" not in set(rights.get("external_authority", [])):
        fail("external statutory authority boundary missing")

    authorization = rights.get("authorization_projection", {})
    if authorization.get("semantic_class") != "CONTROL_PROJECTION_NOT_AUTHORITY_GRANT_OR_DELEGATION_REGISTRY":
        fail("decision authorization must remain a projection rather than a new authority/delegation registry")
    if authorization.get("owner_native_authority_remains_authoritative") is not True:
        fail("decision authorization projection may not replace owner-native authority")
    if authorization.get("central_authority_or_delegation_registry_forbidden") is not True:
        fail("decision authorization projection may not create a central authority/delegation registry")
    for ref in authorization.get("owner_refs", []):
        check_ref(ref)
    required_authorization_fields = {
        "decision_object_id",
        "project_or_scope_id",
        "decision_class",
        "actor_or_authority_ref",
        "authorization_basis_ref_or_fields",
        "authority_scope",
        "claim_boundary",
        "authority_fingerprint",
    }
    if set(authorization.get("required_resolvable_fields", [])) != required_authorization_fields:
        fail("decision authorization required projection fields drift")
    required_conditional_authorization_fields = {
        "competence_basis_ref_or_fields",
        "independence_basis_ref_or_fields",
        "legal_authority_basis_ref_or_fields",
        "validity_or_revalidate_on",
        "decision_readback_ref",
    }
    if set(authorization.get("conditional_resolvable_fields", [])) != required_conditional_authorization_fields:
        fail("decision authorization conditional projection fields drift")
    for required_true in {
        "projection_may_resolve_from_existing_fields_without_duplicate_record",
        "assignment_or_delegation_may_narrow_not_widen_source_rights",
        "identity_alone_does_not_prove_competence_independence_or_legal_authority",
        "professional_judgment_requires_competence_within_scope",
        "independent_review_requires_owner_native_independence_basis",
        "project_authority_cannot_substitute_for_professional_or_statutory_authority",
        "statutory_claim_requires_applicable_legal_authority_basis",
        "recommendation_or_eligibility_report_is_not_decision_transition",
        "material_authorization_change_requires_revalidation_before_consumption",
        "unresolved_material_authorization_fails_closed",
        "machine_may_validate_encoded_binding_not_invent_authority_or_competence",
    }:
        if authorization.get(required_true) is not True:
            fail(f"decision authorization boundary missing {required_true}")
    if set(authorization.get("unresolved_runtime_outcomes", [])) != {"BLOCKED", "RECONCILIATION_REQUIRED"}:
        fail("unresolved material decision authorization must reuse existing runtime outcomes")
    receipt_contract = json.loads(
        (ROOT / "00-governance/runtime/OLEANDER_EXECUTION_RECEIPT_v1.0.json").read_text(encoding="utf-8")
    )
    if "project_or_scope_authority" not in set(receipt_contract.get("authority_required_fields", [])):
        fail("decision authorization projection lost native project/scope authority evidence")
    if not {"reviewer_id", "reviewer_independence_state", "promotion_authority"}.issubset(
        set(receipt_contract.get("review_required_fields", []))
    ):
        fail("decision authorization projection lost native reviewer/promotion authority evidence")

    review_boundary = graph.get("independent_review_boundary", {})
    if review_boundary.get("semantic_class") != "CONTROL_PROJECTION_NOT_REVIEW_AUTHORITY_REGISTRY_STATE_FAMILY_OR_VERDICT_SCHEMA":
        fail("independent review boundary must remain a control projection rather than a review authority/registry/state family/verdict schema")
    if review_boundary.get("projection_only_not_replacement_owner_review_contract") is not True:
        fail("independent review boundary may not replace owner-native review contracts")
    if review_boundary.get("owner_native_review_and_verdict_semantics_remain_authoritative") is not True:
        fail("independent review boundary may not replace owner-native review/verdict semantics")
    if review_boundary.get("central_reviewer_registry_or_review_state_family_forbidden") is not True:
        fail("independent review boundary may not create a central reviewer registry or review state family")
    required_review_sources = {
        "00-governance/complex-project-master-runtime-v1.0.md",
        "00-governance/OLEANDER_INDEPENDENT_DESIGN_VERDICT_POLICY_v1.0.md",
        "00-governance/design-quality-and-design-development-specification-v1.0.md",
        "00-governance/professional-domain-process-contract-v1.0.md",
        "00-governance/cross-disciplinary-design-integration-v1.0.md",
        "00-governance/runtime/OLEANDER_EXECUTION_RECEIPT_v1.0.json",
    }
    if set(review_boundary.get("source_refs", [])) != required_review_sources:
        fail("independent review source-owner projection drift")
    for ref in review_boundary.get("source_refs", []):
        check_ref(ref)
    required_review_binding_fields = {
        "project_or_scope_id",
        "producer_id",
        "reviewer_id",
        "review_input_artifact_id",
        "review_input_hash_or_commit",
        "reviewer_independence_state",
        "review_scope_or_claim_ref",
        "owner_native_verdict_or_gate_ref",
        "does_not_prove",
    }
    if set(review_boundary.get("review_input_required_resolvable_fields", [])) != required_review_binding_fields:
        fail("independent review required input-binding fields drift")
    expected_execution_review_fields = {
        "producer_id",
        "reviewer_id",
        "review_input_artifact_id",
        "review_input_hash_or_commit",
        "reviewer_independence_state",
        "evidence_gate",
        "design_quality_gate",
        "promotion_authority",
    }
    if set(review_boundary.get("owner_native_execution_receipt_fields", [])) != expected_execution_review_fields:
        fail("independent review projection drifted from the declared native Execution Receipt fields")
    if set(receipt_contract.get("review_required_fields", [])) != expected_execution_review_fields:
        fail("Execution Receipt review field contract drift")
    expected_independence_states = {"INDEPENDENT", "PARTIALLY_INDEPENDENT", "NOT_INDEPENDENT", "NOT_REQUIRED"}
    if set(review_boundary.get("reviewer_independence_states", [])) != expected_independence_states:
        fail("independent review projection independence-state vocabulary drift")
    if set(receipt_contract.get("reviewer_independence_states", [])) != expected_independence_states:
        fail("Execution Receipt reviewer-independence state vocabulary drift")
    required_review_classes = {
        "DESIGN_QUALITY",
        "PROFESSIONAL_DOMAIN",
        "INTEGRATION",
        "TECHNICAL_OR_ENGINEERING",
        "EVIDENCE_OR_TRUTH",
        "STATUTORY_OR_LICENSED_WHERE_APPLICABLE",
    }
    if set(review_boundary.get("triggered_review_or_gate_classes", [])) != required_review_classes:
        fail("independent review triggered review/gate class separation drift")
    required_review_revalidation_triggers = {
        "REVIEW_INPUT_IDENTITY_OR_HASH",
        "REVIEW_SCOPE_OR_CLAIM",
        "DECISION_AUTHORIZATION_OR_COMPETENCE_OR_INDEPENDENCE_BASIS",
        "MATERIAL_DEPENDENCY_OR_ACCEPTANCE_BASIS_CONSUMED_BY_REVIEW",
    }
    if set(review_boundary.get("material_review_revalidation_triggers", [])) != required_review_revalidation_triggers:
        fail("independent review material revalidation trigger set drift")
    if set(review_boundary.get("machine_may_validate", [])) != {
        "FIELD_PRESENCE",
        "REFERENCE_RESOLUTION",
        "EXACT_INPUT_HASH_BINDING",
        "ENCODED_PRODUCER_REVIEWER_IDENTITY_DIFFERENCE",
        "ENCODED_STALENESS_TRIGGER",
    }:
        fail("independent review machine-validation boundary drift")
    if set(review_boundary.get("machine_may_not_award", [])) != {
        "OWNER_NATIVE_REVIEW_VERDICT_REQUIRING_HUMAN_JUDGMENT",
        "DESIGN_KEEP",
        "PROFESSIONAL_PASS_WHERE_JUDGMENT_REQUIRED",
        "INTEGRATION_PASS_WHERE_JUDGMENT_REQUIRED",
        "HUMAN_PROMOTION",
        "STATUTORY_OR_LICENSED_APPROVAL",
    }:
        fail("independent review machine verdict firewall drift")
    for required_true in {
        "independent_identity_difference_is_required_but_not_sufficient",
        "producer_self_check_cannot_satisfy_independent_review",
        "different_tool_session_or_surface_does_not_prove_independence",
        "independence_does_not_prove_competence_or_authorization",
        "review_must_bind_exact_input_identity_and_hash_or_commit",
        "review_pass_does_not_auto_apply_to_changed_input",
        "review_domain_pass_cannot_substitute_for_other_triggered_domain",
        "unrelated_file_timestamp_or_nonconsumed_change_does_not_stale_review",
        "reopen_only_affected_review_scope",
        "stale_or_unbound_review_uses_existing_blocker_reconciliation_semantics",
        "review_binding_valid_does_not_prove_verdict_pass",
        "review_result_is_not_promotion",
        "independent_review_is_not_statutory_approval",
        "resolvable_fields_do_not_require_duplicate_central_persistence",
    }:
        if review_boundary.get(required_true) is not True:
            fail(f"independent review boundary missing {required_true}")
    if set(review_boundary.get("unresolved_runtime_outcomes", [])) != {"BLOCKED", "RECONCILIATION_REQUIRED"}:
        fail("stale/unbound independent review must reuse existing blocker/reconciliation outcomes")
    if "producer_self_check_is_not_independent_review" not in set(receipt_contract.get("hard_guards", [])):
        fail("Execution Receipt lost producer-self-check independent-review guard")

    supersession = graph.get("current_supersession_boundary", {})
    if supersession.get("semantic_class") != "CONTROL_PROJECTION_NOT_DUPLICATE_CURRENT_REGISTRY_VERSION_DATABASE_STATE_FAMILY_OR_PROMOTION_AUTHORITY":
        fail("Current/supersession boundary must remain a projection rather than a duplicate registry/version database/state family/promotion authority")
    if supersession.get("projection_only_not_replacement_owner_supersession_contract") is not True:
        fail("Current/supersession projection may not replace owner-native supersession contracts")
    if supersession.get("owner_native_lifecycle_authority_and_current_pointers_remain_authoritative") is not True:
        fail("Current/supersession projection may not replace owner-native lifecycle/authority/current pointers")
    if supersession.get("duplicate_architecture_level_current_registry_or_version_database_forbidden") is not True:
        fail("Current/supersession projection may not create a duplicate architecture-level Current registry/version database")
    required_supersession_sources = {
        "00-governance/complex-project-master-runtime-v1.0.md",
        "00-governance/naming-status.md",
        "00-governance/OLEANDER_ANTI_POLLUTION_PROTOCOL_v1.0.md",
        "00-governance/OLEANDER_ANTI_POLLUTION_CONTRACT_CURRENT.json",
        "00-governance/cross-platform-sync-contract-v1.1.md",
    }
    if set(supersession.get("source_refs", [])) != required_supersession_sources:
        fail("Current/supersession owner-source projection drift")
    for ref in supersession.get("source_refs", []):
        check_ref(ref)
    required_current_identity_fields = {
        "logical_object_id",
        "project_or_scope_id",
        "object_class_or_owner_domain",
        "owner_or_authority_ref",
        "current_ref_or_revision",
        "current_authority_state",
        "authority_fingerprint",
    }
    if set(supersession.get("current_identity_required_resolvable_fields", [])) != required_current_identity_fields:
        fail("Current/supersession current-identity projection fields drift")
    required_successor_transition_fields = {
        "predecessor_ref",
        "successor_ref",
        "adoption_authorization_or_owner_native_transition_ref",
        "supersession_relation",
        "affected_dependency_or_pointer_refs",
        "transition_readback_ref",
        "provenance_ref",
    }
    if set(supersession.get("successor_transition_required_resolvable_fields_when_applicable", [])) != required_successor_transition_fields:
        fail("Current/supersession successor-transition projection fields drift")
    required_successor_sequence = [
        "RESOLVE_LOGICAL_OBJECT_AND_OWNER",
        "RESOLVE_EXISTING_CURRENT_AND_PREDECESSOR",
        "VERIFY_OWNER_NATIVE_ADOPTION_AUTHORIZATION",
        "COMPUTE_AFFECTED_RELATIONS",
        "APPLY_CANONICAL_SUCCESSOR_CURRENT_TRANSITION",
        "DEMOTE_OR_CLOSE_PREDECESSOR_AUTHORITY_IN_SAME_CLOSURE_TRANSACTION",
        "PRESERVE_PREDECESSOR_PROVENANCE_AND_HISTORICAL_RECEIPTS",
        "REFRESH_AFFECTED_POINTERS_INDEXES_AND_DEPENDENCIES",
        "READ_BACK_CANONICAL_AUTHORITY_AND_AFFECTED_SURFACES",
        "HOLD_DEPENDENT_CROSS_PLATFORM_CURRENT_CLAIM_WHERE_MIRROR_STILL_STALE",
    ]
    if supersession.get("successor_adoption_sequence", []) != required_successor_sequence:
        fail("Current/supersession successor-adoption sequence drift")
    for required_true in {
        "one_logical_object_one_current_authority",
        "successor_adoption_requires_predecessor_closure_same_control_transaction",
        "owner_native_adoption_or_authority_transition_required_before_current_claim",
        "recency_filename_branch_pr_merge_or_upload_does_not_select_current",
        "candidate_or_new_revision_may_not_self_promote",
        "supersession_relation_is_not_structural_related_dependency_or_derivation_relation",
        "historical_receipts_immutable_under_original_revision_contract",
        "predecessor_provenance_preserved",
        "superseded_does_not_mean_false_or_delete_authority",
        "deletion_or_ref_cleanup_requires_separate_owner_native_authority",
        "unresolved_competing_current_claims_fail_closed",
        "canonical_transition_may_precede_ordinary_mirror_sync_when_owner_contract_allows",
        "stale_mirror_is_not_coequal_current_authority",
        "mirror_failure_does_not_resurrect_predecessor_canonical_authority",
        "uncertain_canonical_transition_fails_closed",
        "current_or_superseded_lifecycle_disposition_does_not_substitute_for_project_promotion_design_keep_or_statutory_approval",
        "resolvable_fields_do_not_require_duplicate_central_persistence",
    }:
        if supersession.get(required_true) is not True:
            fail(f"Current/supersession boundary missing {required_true}")
    if set(supersession.get("unresolved_runtime_outcomes", [])) != {"BLOCKED", "RECONCILIATION_REQUIRED"}:
        fail("competing/unresolved Current claims must reuse existing blocker/reconciliation outcomes")
    anti_pollution = json.loads(
        (ROOT / "00-governance/OLEANDER_ANTI_POLLUTION_CONTRACT_CURRENT.json").read_text(encoding="utf-8")
    )
    single_current_rules = anti_pollution.get("single_current_rules", {})
    if single_current_rules.get("one_logical_object_one_current") is not True:
        fail("anti-pollution owner lost one-logical-object-one-Current rule")
    if single_current_rules.get("candidate_may_not_self_promote") is not True:
        fail("anti-pollution owner lost candidate self-promotion firewall")
    if anti_pollution.get("git_branch_hygiene", {}).get("branch_ref_is_current_authority") is not False:
        fail("branch ref must remain non-authoritative for Current resolution")
    if "resolve_supersession_and_readback" not in set(anti_pollution.get("mandatory_preflight", [])):
        fail("anti-pollution owner lost supersession/readback preflight")
    naming_text = (ROOT / "00-governance/naming-status.md").read_text(encoding="utf-8")
    if "SUCCESSOR ADOPTION REQUIRES PREDECESSOR CLOSURE" not in naming_text:
        fail("naming/status owner lost successor/predecessor closure invariant")
    if "ONE LOGICAL OBJECT → MAX 1 ACTIVE PRODUCTION FRONTIER + MAX 1 ACTIVE INDEPENDENT REVIEW FRONTIER" not in naming_text:
        fail("naming/status owner lost per-logical-object active-frontier bound")

    authority_binding = graph.get("authority_snapshot_fingerprint_boundary", {})
    if authority_binding.get("semantic_class") != "CONTROL_PROJECTION_NOT_AUTHORITY_REGISTRY_LEDGER_HISTORY_DATABASE_OR_GRANT_MECHANISM":
        fail("authority snapshot/fingerprint boundary must remain a projection rather than an authority registry/ledger/history DB/grant mechanism")
    for required_true in {
        "projection_only_not_replacement_r_a_authority_contract",
        "r_a_owner_native_authority_snapshot_remains_authoritative",
        "fingerprint_is_derived_binding_guard_not_authority_source",
        "fingerprint_match_is_necessary_not_sufficient_for_direct_resume",
        "fingerprint_match_does_not_prove_artifact_review_design_professional_technical_or_statutory_validity",
        "fingerprint_mismatch_requires_re_resolution_not_whole_project_invalidation",
        "changed_constituent_propagates_only_to_actual_consumers",
        "root_version_change_does_not_auto_stale_unaffected_verified_work_after_re_resolution",
        "constraint_change_may_change_execution_permission_without_retroactively_falsifying_unrelated_evidence",
        "context_switch_chat_compression_worker_or_session_change_is_not_authority_change",
        "same_name_filename_or_summary_does_not_prove_same_authority_binding",
        "historical_receipts_immutable_under_consumed_snapshot_fingerprint_and_source_revision",
        "refreshed_snapshot_does_not_rewrite_or_auto_upgrade_historical_receipt",
        "machine_may_validate_binding_not_invent_or_widen_authority",
        "resolvable_bindings_do_not_require_duplicate_central_authority_persistence",
        "central_authority_ledger_registry_or_history_database_forbidden",
    }:
        if authority_binding.get(required_true) is not True:
            fail(f"authority snapshot/fingerprint boundary missing {required_true}")
    if set(authority_binding.get("semantic_owner_refs", [])) != {
        "00-governance/README.md",
        "00-governance/complex-project-master-runtime-v1.0.md",
    }:
        fail("authority snapshot/fingerprint semantic-owner refs drift")
    if set(authority_binding.get("runtime_contract_refs", [])) != {
        "00-governance/runtime/OLEANDER_RUNTIME_LAYER_INTERFACE_CONTRACT_v1.0.json",
        "00-governance/runtime/OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json",
        "00-governance/runtime/OLEANDER_EXECUTION_RECEIPT_v1.0.json",
        "00-governance/control-plane/orchestration.schema.json",
    }:
        fail("authority snapshot/fingerprint runtime-carrier refs drift")
    for ref in authority_binding.get("semantic_owner_refs", []) + authority_binding.get("runtime_contract_refs", []):
        check_ref(ref)
    layer_contract = json.loads(LAYER_INTERFACE.read_text(encoding="utf-8"))
    r_a_interface = layer_contract.get("layers", {}).get("R-A", {})
    if set(authority_binding.get("r_a_external_binding_inputs", [])) != set(r_a_interface.get("external_inputs", [])):
        fail("authority snapshot projection drifted from R-A external binding inputs")
    if set(authority_binding.get("r_a_required_readback", [])) != set(r_a_interface.get("required_readback", [])):
        fail("authority snapshot projection drifted from R-A required readback")
    if set(authority_binding.get("r_a_outputs", [])) != set(r_a_interface.get("outputs", [])):
        fail("authority snapshot projection drifted from R-A outputs")
    resolver = json.loads(
        (ROOT / "00-governance/runtime/OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json").read_text(encoding="utf-8")
    )
    receipt = json.loads(
        (ROOT / "00-governance/runtime/OLEANDER_EXECUTION_RECEIPT_v1.0.json").read_text(encoding="utf-8")
    )
    resolver_checkpoint = resolver.get("continuation_checkpoint_policy", {})
    receipt_checkpoint = receipt.get("continuation_checkpoint_extension", {})
    expected_fingerprint_inputs = [
        "CURRENT_ROOT_VERSION",
        "PROJECT_OR_SCOPE_AUTHORITY",
        "SOURCE_AUTHORITY",
        "DESIGN_AUTHORITY",
        "CURRENT_TASK_ID",
        "CURRENT_NATIVE_MASTER_OR_REF",
        "ACTIVE_CONSTRAINT_LOCK",
    ]
    if authority_binding.get("continuation_fingerprint_inputs", []) != expected_fingerprint_inputs:
        fail("authority snapshot projection continuation fingerprint input order/set drift")
    if resolver_checkpoint.get("authority_fingerprint_inputs", []) != expected_fingerprint_inputs:
        fail("Current Resolver continuation fingerprint inputs drift")
    if receipt_checkpoint.get("authority_fingerprint_inputs", []) != expected_fingerprint_inputs:
        fail("Execution Receipt continuation fingerprint inputs drift")
    expected_direct_resume = {
        "SAME_TASK_AND_OBJECT",
        "AUTHORITY_FINGERPRINT_MATCH",
        "LAST_VERIFIED_ARTIFACT_HAS_ACTUAL_READBACK",
        "NO_STALE_DEPENDENCY_OR_HANDOFF",
        "CHECKPOINT_STATE_RESUMABLE",
    }
    if set(authority_binding.get("direct_resume_requires", [])) != expected_direct_resume:
        fail("authority snapshot projection direct-resume conditions drift")
    if set(resolver_checkpoint.get("direct_resume_requires", [])) != expected_direct_resume:
        fail("Current Resolver direct-resume conditions drift")
    if set(receipt_checkpoint.get("direct_resume_requires", [])) != expected_direct_resume:
        fail("Execution Receipt direct-resume conditions drift")
    expected_revalidate = {
        "PROJECT_OR_TASK_SWITCH",
        "AUTHORITY_FINGERPRINT_MISMATCH",
        "SOURCE_OR_DESIGN_AUTHORITY_CHANGED",
        "CURRENT_NATIVE_MASTER_OR_WRITE_FRONTIER_CHANGED_EXTERNALLY",
        "DEPENDENCY_STALE_OR_RETEST_REQUIRED",
        "CHECKPOINT_MISSING_OR_LAST_ARTIFACT_NOT_READBACK_VERIFIED",
        "CHECKPOINT_SEQUENCE_ADVANCED_BY_ANOTHER_EXECUTOR",
    }
    if set(authority_binding.get("mismatch_revalidation_triggers", [])) != expected_revalidate:
        fail("authority snapshot projection revalidation-trigger set drift")
    if set(resolver_checkpoint.get("revalidate_when", [])) != expected_revalidate:
        fail("Current Resolver continuation revalidation triggers drift")
    if set(receipt_checkpoint.get("revalidate_on", [])) != expected_revalidate:
        fail("Execution Receipt continuation revalidation triggers drift")
    if resolver_checkpoint.get("context_switch_or_compression_is_not_authority_change") is not True:
        fail("Current Resolver lost context-switch/compression authority boundary")
    if receipt_checkpoint.get("context_switch_or_compression_is_not_authority_change") is not True:
        fail("Execution Receipt lost context-switch/compression authority boundary")
    if authority_binding.get("mismatch_action_sequence", []) != [
        "STOP_DIRECT_RESUME_OR_PROTECTED_MUTATION",
        "RE_RESOLVE_CURRENT_OWNER_NATIVE_BINDINGS",
        "IDENTIFY_CHANGED_FINGERPRINT_CONSTITUENTS",
        "COMPUTE_ACTUAL_CONSUMERS_AND_AFFECTED_SCOPE",
        "MARK_ONLY_AFFECTED_DEPENDENCIES_HANDOFFS_REVIEWS_OR_CHECKPOINTS_STALE",
        "PRESERVE_UNAFFECTED_VERIFIED_STATE",
        "REFRESH_REQUIRED_READBACK",
        "RESUME_ONLY_WHEN_EXISTING_RELEASE_CONDITIONS_CLOSE",
    ]:
        fail("authority snapshot/fingerprint mismatch action sequence drift")

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
    required_evolution_steps = {"FREEZE_CURRENT_BASELINE", "GENERATE_ISOLATED_VARIANTS", "RUN_BOUNDED_REAL_PROJECT_EXERCISE_AS_APPLICABLE", "RUN_TARGET_SPECIFIC_EVALS", "VERIFY_STAGE_SPECIFIC_CAPABILITY_RECOMPOSITION_AS_APPLICABLE", "VERIFY_HOLD_RELEASE_SELECTIVE_RETEST_AS_APPLICABLE", "RUN_CONSTRAINT_AND_REGRESSION_GATES", "INDEPENDENT_REVIEW", "HUMAN_PROMOTION_DECISION", "ACTUAL_READBACK", "POST_ADOPTION_MONITORING"}
    if not required_evolution_steps.issubset(set(evolution.get("loop", []))):
        fail("controlled evolution loop incomplete")
    if evolution.get("professional_process_candidate_evaluation_mode") != "BOUNDED_NON_CURRENT_PROJECT_EXERCISE":
        fail("professional-process candidate evaluation mode drift")
    if evolution.get("professional_process_candidate_current_authority_during_eval") != "PROCESS_OPEN_CURRENT_PROCESS_REF_NULL":
        fail("professional-process candidate evaluation must preserve PROCESS_OPEN/current_process_ref=null")
    if evolution.get("professional_process_adoption_requires_stage_recomposition_evidence") is not True:
        fail("professional-process adoption must require stage recomposition evidence")
    if evolution.get("professional_process_adoption_requires_selective_retest_evidence") is not True:
        fail("professional-process adoption must require selective retest evidence")
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

    impact = compatibility.get("impact_projection", {})
    if impact.get("semantic_class") != "CONTROL_PROJECTION_NOT_MIGRATION_STATE_FAMILY_OR_LEDGER":
        fail("compatibility impact must remain a control projection rather than a migration state family/ledger")
    if impact.get("projection_only_not_replacement_migration_schema") is not True or impact.get("owner_native_migration_fields_remain_authoritative") is not True:
        fail("compatibility impact projection may not replace owner-native migration semantics")
    expected_compat_source_refs = {
        "00-governance/runtime/OLEANDER_EVOLUTION_CANDIDATE_CONTRACT_v1.0.json",
        "00-governance/runtime/OLEANDER_RUNTIME_LAYER_INTERFACE_CONTRACT_v1.0.json",
        "00-governance/runtime/OLEANDER_OBSERVABILITY_RECOVERY_CONTRACT_v1.0.json",
        "00-governance/runtime/OLEANDER_EXECUTION_RECEIPT_v1.0.json",
    }
    if set(impact.get("projection_source_refs", [])) != expected_compat_source_refs:
        fail("compatibility impact projection source refs drift")
    for ref in impact.get("projection_source_refs", []):
        check_ref(ref)

    required_migration_projection_fields = {
        "target_ref",
        "target_owner",
        "baseline_current_version_or_revision",
        "compatibility_class",
        "affected_carriers",
        "affected_scope",
        "migration_steps",
        "readback_required",
        "rollback_previous_pointer",
        "rollback_provenance_ref",
    }
    if set(impact.get("migration_required_resolvable_fields", [])) != required_migration_projection_fields:
        fail("compatibility migration projection required fields drift")
    expected_field_map = {
        "target_ref": "evolution_candidate.target_ref",
        "target_owner": "evolution_candidate.target_owner",
        "baseline_current_version_or_revision": "evolution_candidate.baseline.current_version_or_revision",
        "compatibility_class": "evolution_candidate.migration.compatibility_class",
        "affected_carriers": "evolution_candidate.migration.affected_carriers",
        "affected_scope": "evolution_candidate.migration.affected_scope",
        "migration_steps": "evolution_candidate.migration.migration_steps",
        "readback_required": "evolution_candidate.migration.readback_required",
        "rollback_previous_pointer": "evolution_candidate.rollback.previous_pointer",
        "rollback_provenance_ref": "evolution_candidate.rollback.provenance_ref",
    }
    field_map = impact.get("owner_native_field_map", {})
    if field_map != expected_field_map:
        fail("compatibility migration owner-native field map drift")

    impact_scope_fields = {
        "affected_object_refs",
        "affected_handoff_refs",
        "affected_consumer_refs",
        "affected_claim_refs",
        "unaffected_verified_refs",
    }
    if set(impact.get("impact_scope_projection_fields", [])) != impact_scope_fields:
        fail("compatibility impact-scope relation fields drift")
    required_scope_sources = {
        "EXPLICIT_MIGRATION_AFFECTED_CARRIERS_AND_SCOPE",
        "CURRENT_DEPENDENCY_GRAPH",
        "RUNTIME_LAYER_HANDOFF_RELATIONS",
        "CLAIM_CONSUMPTION_RELATIONS",
        "AUTHORITY_BINDINGS",
        "RECOVERY_BLAST_RADIUS_WHEN_AN_ACTUAL_INCIDENT_EXISTS",
    }
    if set(impact.get("impact_scope_sources", [])) != required_scope_sources:
        fail("compatibility impact-scope derivation sources drift")
    if not {"CREATED_BEFORE_CHANGE_ALONE", "SAME_REPOSITORY_ALONE", "FILENAME_PATTERN_ALONE", "SAME_PROJECT_ALONE", "NEWER_TIMESTAMP_ALONE"}.issubset(set(impact.get("affectedness_exclusions", []))):
        fail("compatibility affectedness exclusions are incomplete")

    expected_compat_actions = {
        "PRESERVE_UNAFFECTED_VERIFIED",
        "APPLY_NEW_REQUIREMENT_PROSPECTIVELY",
        "UPDATE_AFFECTED_VALIDATOR_ADAPTER",
        "MARK_AFFECTED_STALE",
        "REOPEN_AFFECTED_CONSUMERS",
        "MIGRATE_AFFECTED_CARRIERS",
        "REFRESH_AUTHORITY_BINDING",
        "RERUN_AFFECTED_READBACK_OR_REVIEW",
        "SUPERSEDE_OLD_POINTER_WHEN_APPLICABLE",
    }
    if impact.get("control_actions_are_not_state_family") is not True or set(impact.get("control_action_vocabulary", [])) != expected_compat_actions:
        fail("compatibility control actions must remain a bounded non-state vocabulary")
    expected_actions_by_class = {
        "DOC_CLARIFICATION": {"PRESERVE_UNAFFECTED_VERIFIED"},
        "BACKWARD_COMPATIBLE_EXTENSION": {"PRESERVE_UNAFFECTED_VERIFIED", "APPLY_NEW_REQUIREMENT_PROSPECTIVELY", "UPDATE_AFFECTED_VALIDATOR_ADAPTER"},
        "SEMANTIC_OWNER_CHANGE": {"MARK_AFFECTED_STALE", "REFRESH_AUTHORITY_BINDING", "REOPEN_AFFECTED_CONSUMERS", "RERUN_AFFECTED_READBACK_OR_REVIEW"},
        "STATE_CONTRACT_CHANGE": {"MARK_AFFECTED_STALE", "MIGRATE_AFFECTED_CARRIERS", "REOPEN_AFFECTED_CONSUMERS", "RERUN_AFFECTED_READBACK_OR_REVIEW"},
        "SCHEMA_BREAKING_CHANGE": {"MARK_AFFECTED_STALE", "MIGRATE_AFFECTED_CARRIERS", "REOPEN_AFFECTED_CONSUMERS", "RERUN_AFFECTED_READBACK_OR_REVIEW"},
        "PROFESSIONAL_PROCESS_REVISION": {"PRESERVE_UNAFFECTED_VERIFIED", "MARK_AFFECTED_STALE", "REOPEN_AFFECTED_CONSUMERS", "RERUN_AFFECTED_READBACK_OR_REVIEW"},
        "AUTHORITY_REPLACEMENT": {"SUPERSEDE_OLD_POINTER_WHEN_APPLICABLE", "REFRESH_AUTHORITY_BINDING", "MARK_AFFECTED_STALE", "REOPEN_AFFECTED_CONSUMERS", "RERUN_AFFECTED_READBACK_OR_REVIEW"},
    }
    actions_by_class = impact.get("minimum_actions_by_change_class", {})
    if set(actions_by_class) != REQUIRED_COMPAT_CLASSES:
        fail("compatibility minimum-action map must cover every change class exactly once")
    for change_class, actions in actions_by_class.items():
        if not actions or not set(actions).issubset(expected_compat_actions):
            fail(f"compatibility action map invalid for {change_class}")
        if set(actions) != expected_actions_by_class[change_class]:
            fail(f"compatibility minimum action boundary drift for {change_class}")

    for required_true in {
        "whole_system_invalidation_forbidden_when_affected_scope_known",
        "relation_scoped_propagation_only",
        "backward_compatible_extension_is_prospective_by_default",
        "canonical_owner_may_explicitly_require_named_existing_carrier_migration",
        "new_field_does_not_auto_upgrade_old_evidence",
        "review_rerun_only_when_review_input_claim_authorization_or_acceptance_dependency_is_affected",
        "change_classification_alone_does_not_open_recovery_incident",
        "actual_failure_or_contradiction_may_use_recovery_incident_contract",
        "post_migration_readback_required_when_declared",
        "rollback_uses_evolution_candidate_pointer_and_provenance",
        "persistent_migration_ledger_forbidden",
    }:
        if impact.get(required_true) is not True:
            fail(f"compatibility impact boundary missing {required_true}")
    if set(impact.get("unresolved_affected_scope_runtime_outcomes", [])) != {"BLOCKED", "RECONCILIATION_REQUIRED"}:
        fail("unresolved compatibility impact must reuse existing runtime outcomes")
    expected_history_rule = "PRESERVE_RAW_RECEIPT_UNDER_ORIGINAL_CONTRACT_AND_RECORD_SUCCESSOR_MIGRATION_OR_REVALIDATION_EVIDENCE; NEVER_REWRITE_HISTORY_TO_LOOK_CURRENT"
    if impact.get("historical_receipt_rule") != expected_history_rule:
        fail("historical receipt migration rule drift")

    try:
        evolution_candidate = json.loads(EVOLUTION_CANDIDATE.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot load evolution candidate contract: {exc}")
    if not {"target_ref", "target_owner", "baseline", "migration", "rollback"}.issubset(set(evolution_candidate.get("required_candidate_fields", []))):
        fail("compatibility projection requires target/baseline/migration/rollback owner-native candidate fields")
    if set(evolution_candidate.get("migration_required_fields", [])) != {"compatibility_class", "affected_carriers", "affected_scope", "migration_steps", "readback_required"}:
        fail("compatibility projection no longer matches owner-native Evolution migration fields")
    if "current_version_or_revision" not in set(evolution_candidate.get("baseline_required_fields", [])):
        fail("compatibility projection requires Evolution baseline current_version_or_revision")
    rollback_fields = set(evolution_candidate.get("rollback_required_fields", []))
    if not {"previous_pointer", "provenance_ref"}.issubset(rollback_fields):
        fail("compatibility rollback projection requires Evolution previous_pointer + provenance_ref")
    if "ADOPTION_DOES_NOT_REINTERPRET_OLD_RECEIPTS" not in set(evolution_candidate.get("invariants", [])):
        fail("Evolution contract must preserve old receipt interpretation boundary")
    professional_policy = evolution_candidate.get("professional_process_candidate_policy", {})
    if professional_policy.get("evaluation_mode") != "BOUNDED_NON_CURRENT_PROJECT_EXERCISE":
        fail("Evolution contract professional-process candidate mode drift")
    if professional_policy.get("current_authority_during_evaluation") != "REMAINS_OPEN_WITH_CURRENT_PROCESS_REF_NULL":
        fail("Evolution contract must preserve PROCESS_OPEN/current_process_ref=null during candidate exercise")
    required_professional_ev5 = {
        "MATERIALLY_DIFFERENT_STAGES_DEMONSTRATE_RECOMPUTED_CAPABILITY_OWNER_SETS",
        "MULTI_OWNER_STAGE_HAS_DAG_AND_TYPED_HANDOFF_EVIDENCE",
        "AT_LEAST_ONE_MATERIAL_HOLD_REOPEN_OR_STAGE_SCOPE_CHANGE_DEMONSTRATES_SELECTIVE_REROUTE",
        "UNAFFECTED_VERIFIED_OUTPUTS_REUSED_RATHER_THAN_FULL_STACK_RESTART",
        "SUCCESSOR_RECEIPT_BINDS_RETEST_RESULT",
    }
    if not required_professional_ev5.issubset(set(professional_policy.get("required_before_ev5", []))):
        fail("Evolution contract professional-process EV5 evidence gate incomplete")
    required_professional_invariants = {
        "PROFESSIONAL_PROCESS_CANDIDATE_EVALUATION_DOES_NOT_CREATE_CURRENT_PROCESS_AUTHORITY",
        "PROFESSIONAL_PROCESS_ADOPTED_DOES_NOT_MEAN_ONE_OR_TWO_SKILLS_REUSED_THROUGH_EVERY_STAGE",
        "MINIMUM_SUFFICIENT_OWNER_SET_DOES_NOT_MEAN_MINIMUM_SKILL_COUNT",
        "HOLD_RELEASE_RETESTS_ONLY_AFFECTED_CAPABILITY_OUTPUT_BINDINGS_UNLESS_DEPENDENCY_ANALYSIS_PROVES_WIDER_STALENESS",
    }
    if not required_professional_invariants.issubset(set(evolution_candidate.get("invariants", []))):
        fail("Evolution contract professional-process adoption invariants incomplete")

    try:
        recovery_contract = json.loads(OBSERVABILITY_RECOVERY.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot load observability/recovery contract for compatibility projection: {exc}")
    recovery_scope = set(recovery_contract.get("recovery_incident", {}).get("blast_radius_required_fields", []))
    if not impact_scope_fields.issubset(recovery_scope):
        fail("compatibility impact projection drift from recovery blast-radius relation fields")

    promotion = graph.get("promotion_persistence_sync_boundary", {})
    if promotion.get("semantic_class") != "CONTROL_PROJECTION_NOT_PROMOTION_STATE_FAMILY_LEDGER_OR_AUTHORITY":
        fail("promotion/persistence/sync boundary must remain a control projection")
    if promotion.get("projection_only_not_replacement_promotion_schema") is not True or promotion.get("owner_native_project_design_authority_states_remain_authoritative") is not True:
        fail("promotion projection may not replace owner-native Project/Design/Authority state owners")
    expected_promotion_owner_refs = {
        "00-governance/complex-project-master-runtime-v1.0.md",
        "00-governance/oleander-project-flow-v0.3.md",
        "00-governance/production-asset-persistence-gate-v1.0.md",
        "00-governance/cross-platform-sync-contract-v1.1.md",
    }
    if set(promotion.get("owner_native_source_refs", [])) != expected_promotion_owner_refs:
        fail("promotion/persistence/sync semantic owner refs drift")
    expected_promotion_runtime_refs = {
        "00-governance/runtime/OLEANDER_RUNTIME_LAYER_INTERFACE_CONTRACT_v1.0.json",
        "00-governance/control-plane/orchestration.schema.json",
        "00-governance/control-plane/orchestrator.py",
    }
    if set(promotion.get("runtime_carrier_or_implementation_refs", [])) != expected_promotion_runtime_refs:
        fail("promotion/persistence/sync runtime implementation refs drift")
    for ref in promotion.get("owner_native_source_refs", []) + promotion.get("runtime_carrier_or_implementation_refs", []):
        check_ref(ref)

    if set(promotion.get("eligibility_required_resolvable_fields", [])) != {
        "project_or_scope_id", "decision_object_id", "authority_fingerprint", "promotion_request_or_intent_ref",
        "claim_boundary", "eligibility_result_ref", "eligibility_evidence_refs", "open_blockers",
    }:
        fail("promotion eligibility projection fields drift")
    if set(promotion.get("triggered_pre_promotion_persistence_fields", [])) != {
        "persistence_trigger_basis_ref_or_fields", "persistence_receipt_ref", "persistence_readback_ref",
    }:
        fail("pre-promotion persistence projection fields drift")
    if set(promotion.get("promotion_transition_required_resolvable_fields", [])) != {
        "human_decision_actor_or_authority_ref", "authorization_basis_ref_or_fields", "human_decision_ref",
        "promotion_transition_owner_ref", "promotion_transition_ref", "authoritative_transition_readback_ref",
    }:
        fail("promotion transition projection fields drift")
    if set(promotion.get("conditional_owner_native_transition_fields", [])) != {
        "transition_kind", "from_authority_state", "target_authority_state", "target_design_state",
    }:
        fail("owner-native promotion transition field projection drift")
    if set(promotion.get("post_promotion_sync_fields", [])) != {
        "required_sync_target_refs", "sync_readback_refs", "cross_line_readback_ref", "drift_or_partial_sync_refs",
    }:
        fail("post-promotion sync projection fields drift")

    expected_promotion_actions = [
        "RESOLVE_PROMOTION_PREREQUISITES_AND_CLAIM_BOUNDARY",
        "CLOSE_TRIGGERED_PRE_PROMOTION_PERSISTENCE",
        "REPORT_ELIGIBILITY_ONLY",
        "RESOLVE_HUMAN_DECISION_AUTHORIZATION",
        "RECORD_AUTHORIZED_HUMAN_DECISION",
        "APPLY_OWNER_NATIVE_PROMOTION_TRANSITION",
        "READBACK_AUTHORITATIVE_PROMOTION_STATE",
        "REGISTER_PROMOTED_ARTIFACT_OR_AUTHORITY_AS_APPLICABLE",
        "PROPAGATE_REQUIRED_POST_PROMOTION_SYNC",
        "READBACK_REQUIRED_SYNC_TARGETS_AND_DRIFT",
    ]
    if promotion.get("control_actions_are_not_state_family") is not True or promotion.get("control_action_sequence") != expected_promotion_actions:
        fail("promotion/persistence/sync control action sequence drift")
    if promotion.get("machine_terminal_before_human_transition") != "READY_FOR_HUMAN_DECISION" or promotion.get("machine_terminal_is_promotion") is not False:
        fail("machine promotion boundary must stop at READY_FOR_HUMAN_DECISION")
    for required_true in {
        "owner_native_pre_promotion_persistence_gate_closes_before_promotion_when_triggered",
        "persistence_pass_does_not_prove_promotion",
        "human_decision_requires_current_decision_authorization",
        "human_decision_record_alone_does_not_prove_transition_unless_same_owner_native_carrier_mutates_and_reads_back_target_state",
        "authoritative_transition_readback_required_for_effective_promotion_claim",
        "full_cross_platform_sync_is_not_universal_pre_promotion_gate",
        "post_promotion_sync_may_follow_confirmed_promotion",
        "post_promotion_mirror_failure_does_not_erase_confirmed_canonical_promotion",
        "post_promotion_mirror_failure_blocks_affected_sync_or_cross_platform_current_claim_only",
        "canonical_authority_transition_uncertainty_blocks_effective_promotion_claim",
        "multi_surface_authority_transition_reuses_partial_commit_reconciliation",
        "ordinary_post_promotion_mirrors_are_not_automatically_transaction_legs",
        "pr_ci_merge_do_not_prove_promotion",
        "sync_success_does_not_prove_promotion",
        "promotion_does_not_prove_release_or_statutory_approval",
        "one_current_per_authority_surface_preserved",
        "resolvable_fields_do_not_require_duplicate_central_persistence",
        "skill_lifecycle_promotion_record_not_project_promotion_schema",
        "persistent_promotion_ledger_forbidden",
    }:
        if promotion.get(required_true) is not True:
            fail(f"promotion/persistence/sync boundary missing {required_true}")
    if set(promotion.get("unresolved_runtime_outcomes", [])) != {"BLOCKED", "RECONCILIATION_REQUIRED"}:
        fail("unresolved promotion transition must reuse existing runtime outcomes")

    master_text = (ROOT / "00-governance/complex-project-master-runtime-v1.0.md").read_text(encoding="utf-8")
    if "READY_FOR_HUMAN_DECISION ≠ PROMOTED" not in master_text:
        fail("Master Runtime promotion readiness/human transition boundary drift")
    project_flow_text = (ROOT / "00-governance/oleander-project-flow-v0.3.md").read_text(encoding="utf-8")
    if "durable persistence must occur **here, before promotion**" not in project_flow_text or "Cross-system registration/synchronization may continue after promotion" not in project_flow_text:
        fail("Project Flow pre-promotion persistence vs post-promotion sync ordering drift")
    pap_text = (ROOT / "00-governance/production-asset-persistence-gate-v1.0.md").read_text(encoding="utf-8")
    if "Promotion / Archive may not begin until PAP-G0—PAP-G6 PASS" not in pap_text or "`PERSISTENCE PASS` concerns durable asset availability only" not in pap_text:
        fail("PAP Promotion prerequisite / does-not-prove boundary drift")
    sync_text = (ROOT / "00-governance/cross-platform-sync-contract-v1.1.md").read_text(encoding="utf-8")
    if "Merge and Promotion remain separate transitions" not in sync_text or "No target-system readback, no sync claim" not in sync_text:
        fail("cross-platform sync merge/promotion/readback boundary drift")

    layer_contract = json.loads(LAYER_INTERFACE.read_text(encoding="utf-8"))
    rj = layer_contract.get("layers", {}).get("R-J", {})
    if set(rj.get("outputs", [])) != {"PERSISTENCE_RECEIPT", "PROMOTION_ELIGIBILITY", "HUMAN_PROMOTION_DECISION_RECORD", "SYNC_READBACK", "DRIFT_STATE"}:
        fail("R-J output contract drift")
    if not {"PERSISTENCE_CLOSED_WHEN_TRIGGERED", "MACHINE_REPORTS_ONLY_ELIGIBILITY_NOT_PROMOTION", "HUMAN_DECISION_RECORDED_WHEN_PROMOTION_OCCURS", "TARGET_PLATFORM_READBACK_CLOSES_SYNC_CLAIM"}.issubset(set(rj.get("exit_conditions", []))):
        fail("R-J exit boundary drift")
    if not {"PERSISTENCE_REQUIRED_BUT_MISSING", "PROMOTION_PREREQUISITE_OPEN", "HUMAN_PROMOTION_DECISION_REQUIRED", "TARGET_SYNC_READBACK_FAILED", "CROSS_PLATFORM_DRIFT", "PROMOTION_CLAIM_BOUNDARY_EXCEEDED"}.issubset(set(rj.get("failure_codes", []))):
        fail("R-J failure boundary drift")

    orchestration_schema = json.loads((ROOT / "00-governance/control-plane/orchestration.schema.json").read_text(encoding="utf-8"))
    transition_props = orchestration_schema.get("$defs", {}).get("transition", {}).get("properties", {})
    if "CANONICAL_PROMOTION" not in set(transition_props.get("kind", {}).get("enum", [])) or "PROMOTED" not in set(transition_props.get("target_design_state", {}).get("enum", [])):
        fail("Control Plane owner-native canonical Promotion transition schema drift")
    orchestrator_text = (ROOT / "00-governance/control-plane/orchestrator.py").read_text(encoding="utf-8")
    if '("CANONICAL_PROMOTION", "CANDIDATE_AUTHORITY", "CANONICAL_AUTHORITY", "PROMOTED")' not in orchestrator_text:
        fail("Control Plane canonical Promotion transition implementation drift")
    if '"status": "READY_FOR_HUMAN_DECISION"' not in orchestrator_text or '"human_decision_required": True' not in orchestrator_text:
        fail("Control Plane evaluator must stop at human decision readiness")

    skill_capability = json.loads((ROOT / "00-governance/runtime/OLEANDER_SKILL_CAPABILITY_CONTRACT_v0.1.json").read_text(encoding="utf-8"))
    if skill_capability.get("scope") != "github_execution_owners":
        fail("Skill Capability promotion record scope drift")

    g9 = graph.get("g9_knowledge_return_boundary", {})
    if g9.get("semantic_class") != "CONTROL_PROJECTION_NOT_KNOWLEDGE_AUTHORITY_STATE_FAMILY_OR_PARALLEL_LEARNING_DATABASE":
        fail("G9 knowledge return must remain a control projection rather than a knowledge authority/state/database")
    for required_true in {
        "projection_only_not_replacement_knowledge_validation_schema",
        "r_b_and_current_knowledge_owner_retain_knowledge_authority",
        "resolvable_fields_do_not_require_duplicate_central_persistence",
        "common_control_actions_are_not_state_family",
        "routes_are_not_mutually_exclusive_but_do_not_inherit_each_others_authority",
        "observation_does_not_prove_causation",
        "repeated_pattern_does_not_prove_universal_rule",
        "one_project_success_does_not_prove_transferability",
        "project_failure_does_not_automatically_invalidate_current_knowledge",
        "transfer_boundary_required_before_reusable_knowledge_route",
        "unsupported_causal_story_cannot_be_promoted_by_g9",
        "counterevidence_and_failed_attempts_preserved_when_material",
        "project_specific_or_unresolved_transfer_may_remain_project_practice_evidence",
        "knowledge_validation_gate_results_owned_by_existing_knowledge_research_contracts",
        "g9_cannot_award_knowledge_research_gate_pass",
        "knowledge_lifecycle_disposition_owned_by_existing_knowledge_authority",
        "knowledge_lifecycle_vocabulary_reused_not_redefined",
        "current_knowledge_does_not_auto_grant_task_scoped_oe3",
        "g9_cannot_award_ki4_or_oe3",
        "project_reopen_does_not_require_prior_reusable_knowledge_promotion",
        "project_reopen_does_not_prove_reusable_knowledge_revision",
        "g9_may_propose_evolution_candidate_but_not_mutate_live_runtime",
        "evolution_target_owner_retains_semantic_authority",
        "parallel_g9_knowledge_tree_forbidden",
        "parallel_persistent_g9_learning_authority_database_forbidden",
        "g9_feedback_edge_to_r_b_is_candidate_feedback_not_dependency_handoff",
    }:
        if g9.get(required_true) is not True:
            fail(f"G9 knowledge return boundary missing {required_true}")
    expected_g9_refs = {
        "00-governance/complex-project-master-runtime-v1.0.md",
        "00-governance/design-intelligence-routing-and-review-v1.0.md",
        "00-governance/design-quality-and-design-development-specification-v1.0.md",
        "00-governance/cross-disciplinary-design-integration-v1.0.md",
        "00-governance/knowledge-integrity-and-operational-mount-v1.0.md",
        "00-governance/runtime/OLEANDER_KNOWLEDGE_CONTENT_REVIEW_LAYER_v1.0.md",
        "oleander-skills/oleander-research/PROFESSIONAL_KNOWLEDGE_CONTENT_RESEARCH_STANDARD_v1.0.json",
        "00-governance/naming-status.md",
        "00-governance/runtime/OLEANDER_RUNTIME_LAYER_INTERFACE_CONTRACT_v1.0.json",
        "00-governance/runtime/OLEANDER_EVOLUTION_CANDIDATE_CONTRACT_v1.0.json",
    }
    if set(g9.get("projection_source_refs", [])) != expected_g9_refs:
        fail("G9 projection source refs drift")
    for ref in g9.get("projection_source_refs", []):
        check_ref(ref)
    if set(g9.get("candidate_required_resolvable_fields", [])) != {
        "project_or_context_scope_ref", "intended_relation_or_baseline_ref", "observed_outcome_ref",
        "difference_or_pattern", "causal_hypothesis_or_uncertainty", "repair_retest_refs",
        "counterexample_refs", "transfer_boundary", "proposed_reusable_form_or_role",
        "target_knowledge_or_evolution_owner_ref", "validation_route_ref", "does_not_prove",
    }:
        fail("G9 candidate projection fields drift")
    if g9.get("common_control_action_sequence") != [
        "CAPTURE_ACTUAL_OBSERVED_OUTCOME",
        "BIND_INTENDED_RELATION_OR_BASELINE",
        "SEPARATE_OBSERVATION_FROM_CAUSAL_HYPOTHESIS",
        "PRESERVE_PROJECT_CONTEXT_UNCERTAINTY_AND_NEGATIVE_EVIDENCE",
        "PRESERVE_REPAIR_RETEST_AND_COUNTEREXAMPLES_WHEN_AVAILABLE",
        "DEFINE_TRANSFER_BOUNDARY",
        "RESOLVE_TARGET_OWNER_AND_VALIDATION_ROUTE",
    ]:
        fail("G9 common control action sequence drift")
    if set(g9.get("bounded_route_actions", [])) != {
        "ROUTE_PROJECT_SPECIFIC_FINDING_TO_PROJECT_PRACTICE_EVIDENCE",
        "ROUTE_MATERIAL_PROJECT_FAILURE_TO_EXISTING_REOPEN_CONTROLS",
        "ROUTE_REUSABLE_LESSON_TO_EXISTING_KNOWLEDGE_VALIDATION",
        "ROUTE_RUNTIME_OR_PROCESS_LESSON_TO_EVOLUTION_CANDIDATE_CONTRACT",
    }:
        fail("G9 bounded route actions drift")

    expected_rk_failure_codes = {
        "CAUSAL_STORY_UNSUPPORTED", "TRANSFER_BOUNDARY_MISSING", "PROJECT_SPECIFIC_ONLY",
        "COUNTEREVIDENCE_UNRESOLVED", "CANDIDATE_OWNER_UNRESOLVED", "AUTO_PROMOTION_ATTEMPT_BLOCKED",
    }
    if set(g9.get("existing_r_k_failure_codes", [])) != expected_rk_failure_codes:
        fail("G9 projection failure-code set drift")
    r_k = layer_contract.get("layers", {}).get("R-K", {})
    if set(r_k.get("failure_codes", [])) != expected_rk_failure_codes:
        fail("R-K owner-native failure codes drift from G9 projection")
    if set(r_k.get("outputs", [])) != {"LESSON_CANDIDATE", "CAUSAL_HYPOTHESIS", "TRANSFER_BOUNDARY", "COUNTEREXAMPLE_SET", "KNOWLEDGE_VALIDATION_ROUTE", "EVOLUTION_CANDIDATE_REF"}:
        fail("R-K owner-native output contract drift")
    if r_k.get("persistence_policy") != "PERSIST_AS_PROJECT_OR_CANDIDATE_UNTIL_VALIDATED; NEVER_AS_CURRENT_KNOWLEDGE_BY_DEFAULT":
        fail("R-K candidate persistence boundary drift")
    if r_k.get("claim_boundary") != "MAY_PROPOSE_BOUNDED_REUSABLE_LEARNING_OR_EVOLUTION_CANDIDATE; DOES_NOT_PROMOTE_CURRENT_KNOWLEDGE_OR_MUTATE_RUNTIME_DIRECTLY":
        fail("R-K claim boundary drift")
    if set(r_k.get("feedback_targets", [])) != {"R-B"} or r_k.get("handoff_targets", []) != []:
        fail("R-K to R-B must remain bounded feedback rather than dependency handoff")

    research_standard = json.loads((ROOT / "oleander-skills/oleander-research/PROFESSIONAL_KNOWLEDGE_CONTENT_RESEARCH_STANDARD_v1.0.json").read_text(encoding="utf-8"))
    expected_current_gates = {
        "AUTHORITY_IDENTITY_PASS", "APPLICABLE_R1_PASS", "APPLICABLE_R2_PASS", "K1_PASS", "K2_PASS",
        "K3_PASS", "K4_PASS", "K5_PASS", "B1_PASS", "APPLICABLE_IR_PASS", "NO_UNRESOLVED_CRITICAL_CONTRADICTION",
    }
    if set(research_standard.get("promotion_rule", {}).get("canonical_current_requires", [])) != expected_current_gates:
        fail("G9 reusable Knowledge promotion projection drift from research standard")
    if not {"KNOWLEDGE_OBJECT_PASS_NE_CANONICAL_CURRENT", "CONTENT_PASS_NE_RESEARCH_PASS"}.issubset(set(research_standard.get("separation_rules", []))):
        fail("Knowledge research separation rules incomplete for G9 projection")

    knowledge_mount_text = (ROOT / "00-governance/knowledge-integrity-and-operational-mount-v1.0.md").read_text(encoding="utf-8")
    if "G9 project outcomes return as lesson candidates and must pass existing knowledge validation before reusable promotion" not in knowledge_mount_text:
        fail("Knowledge Operational Mount G9 validation boundary drift")
    if "derive `OE*` only for a concrete task/claim scope" not in knowledge_mount_text:
        fail("Knowledge Operational Mount task-scoped OE boundary drift")
    content_review_text = (ROOT / "00-governance/runtime/OLEANDER_KNOWLEDGE_CONTENT_REVIEW_LAYER_v1.0.md").read_text(encoding="utf-8")
    if "CONTENT TERMINAL != KNOWLEDGE INTEGRITY VERIFIED != OPERATIONALLY ELIGIBLE" not in content_review_text:
        fail("G9 projection requires Content/KI/OE separation")
    naming_text = (ROOT / "00-governance/naming-status.md").read_text(encoding="utf-8")
    if "WORKING / TEMP → CANDIDATE → CURRENT | SUPPORT | PROVENANCE | SUPERSEDED | REJECTED | DELETE_CANDIDATE" not in naming_text:
        fail("G9 projection must reuse existing Knowledge lifecycle vocabulary")
    evolution = json.loads(EVOLUTION_CANDIDATE.read_text(encoding="utf-8"))
    evolution_invariants = set(evolution.get("invariants", []))
    if not {"ONE_PROJECT_SUCCESS_DOES_NOT_UNIVERSALIZE_RULE", "TARGET_OWNER_RETAINS_SEMANTIC_AUTHORITY", "G9_IS_CANDIDATE_INTAKE_NOT_SUPER_AUTHORITY"}.issubset(evolution_invariants):
        fail("G9 Evolution route boundary drift")

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

    transaction = graph.get("multi_surface_mutation_transaction_boundary", {})
    if transaction.get("semantic_class") != "EPHEMERAL_RECONCILIATION_PROJECTION_NOT_DISTRIBUTED_TRANSACTION_SERVICE":
        fail("multi-surface transaction boundary must remain an ephemeral projection")
    for ref in transaction.get("semantic_owner_refs", []):
        check_ref(ref)
    check_ref(transaction.get("runtime_implementation_ref"))
    if set(transaction.get("leg_observation_values", [])) != {"CONFIRMED", "ABSENT", "UNCERTAIN"}:
        fail("multi-surface transaction leg observation vocabulary drift")
    if set(transaction.get("reconciliation_results", [])) != {"COHERENT_COMMIT", "PARTIAL_COMMIT", "HOLD"}:
        fail("multi-surface transaction reconciliation result vocabulary drift")
    expected_runtime_actions = {
        "ADVANCE_AFTER_COHERENT_COMMIT",
        "VERIFY_UNCERTAIN_LEGS_BEFORE_ADVANCE",
        "RECONCILE_MISSING_LEGS_BEFORE_ADVANCE",
        "COMPENSATE_CONFIRMED_LEGS_BEFORE_ADVANCE",
        "HOLD_PARTIAL_COMMIT_UNRECONCILED",
    }
    if set(transaction.get("current_runtime_actions", [])) != expected_runtime_actions:
        fail("multi-surface transaction actions drift from current P6 runtime")
    for required_true in {
        "result_is_ephemeral_runtime_fact_not_project_state",
        "dependent_handoff_ready_requires_coherent_commit",
        "dependent_handoff_acceptance_requires_coherent_commit",
        "dag_advance_requires_coherent_commit",
        "uncertain_leg_uses_verify_before_retry",
        "retry_requires_idempotent_or_provider_keyed_or_explicit_retry_safe",
        "compensation_requires_existing_legal_authorized_path",
        "compensation_is_not_general_rollback_guarantee",
        "preserve_last_verified_state_on_hold",
        "distributed_transaction_manager_forbidden",
        "persistent_transaction_ledger_forbidden",
        "global_lock_service_forbidden",
    }:
        if transaction.get(required_true) is not True:
            fail(f"multi-surface transaction boundary missing {required_true}")

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
        "MULTI_SURFACE_PARTIAL_COMMIT_BLOCKS_DEPENDENT_HANDOFF_AND_DAG_ADVANCE",
        "TRANSACTION_RECONCILIATION_DOES_NOT_CREATE_DISTRIBUTED_TRANSACTION_AUTHORITY",
        "CONSEQUENTIAL_DECISION_REQUIRES_RESOLVABLE_AUTHORIZATION_BASIS",
        "DELEGATION_OR_ASSIGNMENT_CANNOT_WIDEN_SOURCE_AUTHORITY",
        "UNRESOLVED_MATERIAL_DECISION_AUTHORIZATION_FAILS_CLOSED",
        "MACHINE_CANNOT_INVENT_DECISION_AUTHORITY_OR_COMPETENCE",
        "NO_UNIVERSAL_LAYER_PROGRESS_STATE",
        "OBSERVABILITY_EVENT_NOT_AUTHORITY",
        "RECOVERY_INCIDENT_NOT_PROJECT_STATE",
        "RECOVERY_BLAST_RADIUS_PRESERVES_UNAFFECTED_VALID_STATE",
        "RECOVERY_CLOSURE_REQUIRES_ACTUAL_READBACK",
        "INCIDENT_CLOSED_DOES_NOT_PROVE_DESIGN_PROFESSIONAL_OR_PROMOTION_PASS",
        "RECOVERY_REACCEPTS_ONLY_AFFECTED_HANDOFFS_AFTER_REQUIRED_READBACK",
        "LIVE_STATUS_REMAINS_OBSERVABILITY_ONLY",
        "COMPATIBILITY_IMPACT_IS_RELATION_SCOPED_NOT_GLOBAL_RESET",
        "HISTORICAL_RECEIPTS_IMMUTABLE_ACROSS_MIGRATION",
        "BACKWARD_COMPATIBLE_EXTENSION_PROSPECTIVE_BY_DEFAULT",
        "MIGRATION_ACTIONS_DO_NOT_CREATE_STATE_FAMILY_OR_LEDGER",
        "READY_FOR_HUMAN_DECISION_IS_NOT_PROMOTION",
        "TRIGGERED_PERSISTENCE_CLOSES_BEFORE_PROMOTION",
        "PROMOTION_REQUIRES_AUTHORIZED_OWNER_NATIVE_TRANSITION_AND_READBACK",
        "POST_PROMOTION_SYNC_FAILURE_DOES_NOT_ERASE_CONFIRMED_CANONICAL_PROMOTION",
        "PROMOTION_SYNC_BOUNDARY_DOES_NOT_CREATE_STATE_FAMILY_OR_LEDGER",
        "G9_CANDIDATE_IS_NOT_CURRENT_KNOWLEDGE",
        "G9_OBSERVATION_IS_NOT_CAUSAL_PROOF",
        "G9_REUSABLE_ROUTE_REQUIRES_TRANSFER_BOUNDARY",
        "G9_KNOWLEDGE_LIFECYCLE_DISPOSITION_REMAINS_WITH_KNOWLEDGE_OWNER",
        "CURRENT_KNOWLEDGE_DOES_NOT_AUTO_GRANT_OE3",
        "G9_EVOLUTION_CANDIDATE_CANNOT_MUTATE_LIVE_RUNTIME",
        "PROJECT_REOPEN_AND_REUSABLE_KNOWLEDGE_PROMOTION_REMAIN_SEPARATE",
        "INDEPENDENT_REVIEW_BINDS_EXACT_INPUT_IDENTITY_AND_HASH_OR_COMMIT",
        "PRODUCER_SELF_CHECK_IS_NOT_INDEPENDENT_REVIEW",
        "INDEPENDENCE_DOES_NOT_PROVE_COMPETENCE_OR_AUTHORIZATION",
        "REVIEW_CLASS_PASS_DOES_NOT_SUBSTITUTE_FOR_OTHER_TRIGGERED_REVIEW",
        "MATERIAL_REVIEW_CHANGE_STALES_ONLY_AFFECTED_REVIEW_SCOPE",
        "MACHINE_CANNOT_AWARD_HUMAN_REVIEW_VERDICT",
        "INDEPENDENT_REVIEW_BOUNDARY_DOES_NOT_CREATE_REVIEWER_REGISTRY_OR_STATE_FAMILY",
        "ONE_LOGICAL_OBJECT_ONE_CURRENT_AUTHORITY",
        "SUCCESSOR_ADOPTION_CLOSES_PREDECESSOR_AUTHORITY_IN_SAME_CONTROL_TRANSACTION",
        "RECENCY_BRANCH_PR_MERGE_DO_NOT_SELECT_CURRENT",
        "SUPERSESSION_PRESERVES_PROVENANCE_AND_HISTORICAL_RECEIPTS",
        "SUPERSEDED_IS_NOT_DELETE_AUTHORITY_OR_FALSEHOOD",
        "STALE_MIRROR_IS_NOT_COEQUAL_CURRENT_AUTHORITY",
        "CURRENT_SUPERSESSION_BOUNDARY_DOES_NOT_CREATE_REGISTRY_VERSION_DB_STATE_FAMILY_OR_PROMOTION_AUTHORITY",
        "AUTHORITY_FINGERPRINT_IS_DERIVED_GUARD_NOT_AUTHORITY_SOURCE",
        "AUTHORITY_FINGERPRINT_MATCH_IS_NOT_SUFFICIENT_FOR_DIRECT_RESUME",
        "AUTHORITY_FINGERPRINT_MISMATCH_REQUIRES_RERESOLUTION_NOT_GLOBAL_INVALIDATION",
        "AUTHORITY_CHANGE_REOPENS_ONLY_ACTUAL_BOUND_CONSUMERS",
        "CONTEXT_PACKAGING_CHANGE_IS_NOT_AUTHORITY_CHANGE",
        "HISTORICAL_RECEIPT_RETAINS_CONSUMED_AUTHORITY_BINDING",
        "AUTHORITY_SNAPSHOT_BOUNDARY_DOES_NOT_CREATE_LEDGER_REGISTRY_HISTORY_DB_OR_GRANT_MECHANISM",
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
    print("compatibility_impact_projection=PASS")
    print("promotion_persistence_sync_boundary=PASS")
    print("g9_knowledge_return_boundary=PASS")
    print("independent_review_boundary=PASS")
    print("current_supersession_boundary=PASS")
    print("authority_snapshot_fingerprint_boundary=PASS")
    print("trigger_applicability_projection_definition=PASS")
    print("claim_ceiling_projection_definition=PASS")
    print("execution_frontier_concurrency=PASS")
    print("multi_surface_transaction_boundary=PASS")
    print("decision_authorization_projection=PASS")
    print("current_drift_reconciliation_projection=PASS")
    print("runtime_layer_interfaces=PASS")
    print("observability_recovery_contract=PASS")


if __name__ == "__main__":
    main()
