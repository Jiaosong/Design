#!/usr/bin/env python3
"""OLEANDER Project Control Plane v0.3 hardened orchestration."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from control_plane import load_json, run_check, select_gate_profile  # noqa: E402
from schema_enforcer import load_schema, validate_instance  # noqa: E402

ORCH_SCHEMA = load_schema(HERE / "orchestration.schema.json")
PROVIDER_ORDER = ["current_authority", "github", "drive", "file_library", "runtime"]
MATERIALIZATION_PROVIDERS = ["github", "drive", "file_library", "runtime"]
REQUIRED_SYNC_SYSTEMS = ["notion", "github", "drive"]
MASTER_REVIEW_TYPES = {"ARTIFACT", "TECHNICAL", "EVIDENCE", "DISCIPLINE", "DESIGN", "PERSISTENCE"}
VALID_TRANSITIONS = {
    ("CANDIDATE_PROMOTION", "WORKING_SOURCE", "CANDIDATE_AUTHORITY", "CANDIDATE"),
    ("CANONICAL_PROMOTION", "CANDIDATE_AUTHORITY", "CANONICAL_AUTHORITY", "PROMOTED"),
    ("FREEZE", "CANONICAL_AUTHORITY", "FROZEN_AUTHORITY", "FROZEN"),
    ("RELEASE", "CANONICAL_AUTHORITY", "CANONICAL_AUTHORITY", "RELEASED"),
}
OPEN_EVIDENCE = {"UNKNOWN", "NOT_RUN", "OPEN", "BLOCKED", "FAIL"}


def _schema_findings(value: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {"level": "ERROR", "code": "SCHEMA_VALIDATION", "message": f"{e['path']}: {e['message']}"}
        for e in validate_instance(value, ORCH_SCHEMA)
    ]


def _binding_matches(hit: dict[str, Any], object_id: str, binding: dict[str, Any]) -> bool:
    if hit.get("object_id") != object_id:
        return False
    if hit.get("source_id") != binding.get("source_id"):
        return False
    if hit.get("authority_state") != binding.get("authority_state"):
        return False
    expected_hash = binding.get("sha256")
    return expected_hash in (None, "") or hit.get("sha256") == expected_hash


def evaluate_provider_chain(snapshot: dict[str, Any]) -> dict[str, Any]:
    findings = _schema_findings(snapshot)
    if findings:
        return {
            "status": "BLOCKED", "resolution_status": "INVALID", "actionability": "BLOCKED",
            "code": "CB-03_PROVIDER_SCHEMA_INVALID", "findings": findings,
            "selected_provider": None, "hits": [], "e0_eligible": False,
        }
    if snapshot.get("kind") != "PROVIDER_CHAIN":
        return {
            "status": "BLOCKED", "resolution_status": "INVALID", "actionability": "BLOCKED",
            "code": "CB-03_WRONG_DOCUMENT_KIND", "findings": [], "selected_provider": None,
            "hits": [], "e0_eligible": False,
        }

    providers = snapshot["providers"]
    observed = [r["provider"] for r in providers]
    if len(observed) != len(set(observed)) or observed != [p for p in PROVIDER_ORDER if p in observed]:
        return {
            "status": "BLOCKED", "resolution_status": "INVALID", "actionability": "BLOCKED",
            "code": "CB-03_PROVIDER_ORDER",
            "findings": [{"level": "ERROR", "code": "PROVIDER_ORDER", "message": "provider receipts must be unique and preserve canonical search order"}],
            "selected_provider": None, "hits": [], "e0_eligible": False,
        }
    by_provider = {r["provider"]: r for r in providers}
    for receipt in providers:
        if receipt["status"] == "FOUND" and not receipt["hits"]:
            findings.append({"level": "ERROR", "code": "PROVIDER_FOUND_WITHOUT_HIT", "message": f"{receipt['provider']} FOUND requires hits"})
        if receipt["status"] != "FOUND" and receipt["hits"]:
            findings.append({"level": "ERROR", "code": "PROVIDER_HITS_STATUS_CONFLICT", "message": f"{receipt['provider']} has hits while status={receipt['status']}"})
    if findings:
        return {
            "status": "BLOCKED", "resolution_status": "INVALID", "actionability": "BLOCKED",
            "code": "CB-03_PROVIDER_RECEIPT_INVALID", "findings": findings,
            "selected_provider": None, "hits": [], "e0_eligible": False,
        }

    if snapshot["lookup_mode"] == "DISCOVERY":
        hits = [dict(hit, provider=receipt["provider"]) for receipt in providers if receipt["status"] == "FOUND" for hit in receipt["hits"]]
        if hits:
            return {
                "status": "DISCOVERED", "resolution_status": "COMPLETE",
                "actionability": "BLOCKED_PENDING_AUTHORITY_RESOLUTION",
                "code": "CB-03_DISCOVERY_HITS_NOT_AUTHORITY", "findings": [],
                "selected_provider": None, "hits": hits, "e0_eligible": False,
            }
        missing = [p for p in PROVIDER_ORDER if p not in by_provider]
        unresolved = [p for p, receipt in by_provider.items() if receipt["status"] in {"UNAVAILABLE", "BLOCKED", "ERROR"}]
        if missing or unresolved:
            return {
                "status": "BLOCKED", "resolution_status": "INCOMPLETE", "actionability": "BLOCKED",
                "code": "CB-03_DISCOVERY_INCOMPLETE",
                "findings": [{"level": "ERROR", "code": "PROVIDER_CHAIN_INCOMPLETE", "message": f"missing={missing}; unresolved={unresolved}"}],
                "selected_provider": None, "hits": [], "e0_eligible": False,
            }
        return {
            "status": "UNLOCATED", "resolution_status": "COMPLETE", "actionability": "BLOCKED",
            "code": "CB-03_E0_ELIGIBLE", "findings": [], "selected_provider": None,
            "hits": [], "e0_eligible": True,
        }

    binding = snapshot.get("authority_binding")
    if not isinstance(binding, dict):
        return {
            "status": "BLOCKED", "resolution_status": "INVALID", "actionability": "BLOCKED",
            "code": "CB-03_AUTHORITY_BINDING_REQUIRED", "findings": [], "selected_provider": None,
            "hits": [], "e0_eligible": False,
        }
    authority_receipt = by_provider.get("current_authority")
    if not authority_receipt or authority_receipt["status"] != "FOUND":
        return {
            "status": "BLOCKED", "resolution_status": "INCOMPLETE", "actionability": "BLOCKED",
            "code": "CB-03_AUTHORITY_NOT_RESOLVED", "findings": [], "selected_provider": None,
            "hits": [], "e0_eligible": False,
        }
    exact_authority_hits = [h for h in authority_receipt["hits"] if _binding_matches(h, snapshot["object_id"], binding)]
    if len(exact_authority_hits) != 1:
        return {
            "status": "BLOCKED", "resolution_status": "INVALID", "actionability": "BLOCKED",
            "code": "CB-03_AUTHORITY_BINDING_MISMATCH",
            "findings": [{"level": "ERROR", "code": "AUTHORITY_BINDING_MISMATCH", "message": "Current Authority receipt must contain exactly one exact authority-bound hit"}],
            "selected_provider": None, "hits": [], "e0_eligible": False,
        }

    for provider in MATERIALIZATION_PROVIDERS:
        receipt = by_provider.get(provider)
        if not receipt:
            continue
        if receipt["status"] in {"UNAVAILABLE", "BLOCKED", "ERROR"}:
            return {
                "status": "BLOCKED", "resolution_status": "INCOMPLETE", "actionability": "BLOCKED",
                "code": "CB-03_MATERIALIZATION_PROVIDER_UNRESOLVED",
                "findings": [{"level": "ERROR", "code": "PROVIDER_UNRESOLVED", "message": f"{provider} status={receipt['status']}"}],
                "selected_provider": None, "hits": [], "e0_eligible": False,
            }
        if receipt["status"] == "FOUND":
            exact = [h for h in receipt["hits"] if _binding_matches(h, snapshot["object_id"], binding)]
            if not exact:
                return {
                    "status": "BLOCKED", "resolution_status": "INVALID", "actionability": "BLOCKED",
                    "code": "CB-03_FOUND_NOT_AUTHORITY_BOUND",
                    "findings": [{"level": "ERROR", "code": "FOUND_NOT_AUTHORITY_BOUND", "message": f"{provider} FOUND only non-matching objects"}],
                    "selected_provider": None, "hits": [], "e0_eligible": False,
                }
            return {
                "status": "FOUND", "resolution_status": "COMPLETE", "actionability": "ALLOWED",
                "code": "CB-03_BOUND_MATERIALIZATION_RESOLVED", "findings": [],
                "selected_provider": provider, "hits": exact, "e0_eligible": False,
            }
    missing_materialization = [p for p in MATERIALIZATION_PROVIDERS if p not in by_provider]
    if missing_materialization:
        return {
            "status": "BLOCKED", "resolution_status": "INCOMPLETE", "actionability": "BLOCKED",
            "code": "CB-03_MATERIALIZATION_CHAIN_INCOMPLETE",
            "findings": [{"level": "ERROR", "code": "PROVIDER_CHAIN_INCOMPLETE", "message": f"unattempted materialization providers: {missing_materialization}"}],
            "selected_provider": None, "hits": [], "e0_eligible": False,
        }
    return {
        "status": "UNLOCATED", "resolution_status": "COMPLETE", "actionability": "BLOCKED",
        "code": "CB-03_AUTHORITY_KNOWN_MATERIALIZATION_UNLOCATED", "findings": [],
        "selected_provider": None, "hits": [], "e0_eligible": False,
    }


def _valid_transition(transition: dict[str, Any]) -> bool:
    return (
        transition["kind"], transition["from_authority_state"],
        transition["target_authority_state"], transition["target_design_state"]
    ) in VALID_TRANSITIONS


def evaluate_promotion(card: dict[str, Any], bundle: dict[str, Any]) -> dict[str, Any]:
    check = run_check(card)
    if check["status"] != "PASS":
        return {
            "status": "BLOCKED", "code": "PROMOTION_CONTROL_CARD_BLOCKED", "control_check": check,
            "findings": [], "missing_or_failed_gates": [], "post_promotion_actions": [],
        }
    schema_findings = _schema_findings(bundle)
    if schema_findings or bundle.get("kind") != "GATE_RECEIPTS":
        return {
            "status": "BLOCKED", "code": "PROMOTION_RECEIPT_SCHEMA_INVALID", "control_check": check,
            "findings": schema_findings, "missing_or_failed_gates": [], "post_promotion_actions": [],
        }

    source = card.get("authority_source") or {}
    expected_object = source.get("object_id")
    expected_source = source.get("source_id")
    if not expected_object or not expected_source:
        return {
            "status": "BLOCKED", "code": "PROMOTION_AUTHORITY_IDENTITY_INCOMPLETE", "control_check": check,
            "findings": [{"level": "ERROR", "code": "AUTHORITY_IDENTITY_INCOMPLETE", "message": "Promotion requires distinct authority_source.object_id and authority_source.source_id"}],
            "missing_or_failed_gates": [], "post_promotion_actions": [],
        }
    binding = bundle["authority_binding"]
    if bundle["object_id"] != expected_object or binding.get("source_id") != expected_source or binding.get("authority_state") != source.get("state"):
        return {
            "status": "BLOCKED", "code": "PROMOTION_AUTHORITY_BINDING_MISMATCH", "control_check": check,
            "findings": [{"level": "ERROR", "code": "AUTHORITY_BINDING_MISMATCH", "message": "gate bundle does not bind to the exact Control Card authority object/source"}],
            "missing_or_failed_gates": [], "post_promotion_actions": [],
        }
    expected_hash = source.get("sha256")
    if expected_hash not in (None, "") and binding.get("sha256") != expected_hash:
        return {
            "status": "BLOCKED", "code": "PROMOTION_AUTHORITY_HASH_MISMATCH", "control_check": check,
            "findings": [], "missing_or_failed_gates": [], "post_promotion_actions": [],
        }

    transition = bundle["transition"]
    if transition["from_authority_state"] != source.get("state") or not _valid_transition(transition):
        return {
            "status": "BLOCKED", "code": "PROMOTION_TRANSITION_INVALID", "control_check": check,
            "transition": transition, "findings": [], "missing_or_failed_gates": [], "post_promotion_actions": [],
        }
    required_mode = "CANDIDATE" if transition["target_authority_state"] == "CANDIDATE_AUTHORITY" else "AUTHORITY"
    if card.get("mode") != required_mode:
        return {
            "status": "BLOCKED", "code": "PROMOTION_MODE_TRANSITION_MISMATCH", "control_check": check,
            "transition": transition, "findings": [], "missing_or_failed_gates": [], "post_promotion_actions": [],
        }

    open_evidence = {k: v for k, v in card.get("evidence_state", {}).items() if v in OPEN_EVIDENCE}
    if open_evidence:
        return {
            "status": "BLOCKED", "code": "PROMOTION_EVIDENCE_OPEN", "control_check": check,
            "transition": transition, "open_evidence": open_evidence, "findings": [],
            "missing_or_failed_gates": [], "post_promotion_actions": [],
        }

    receipts = bundle["receipts"]
    execution_mode = bundle["execution_mode"]
    by_gate: dict[str, dict[str, Any]] = {}
    duplicates: list[str] = []
    for receipt in receipts:
        if receipt["gate"] in by_gate:
            duplicates.append(receipt["gate"])
        by_gate[receipt["gate"]] = receipt
    if duplicates:
        return {
            "status": "BLOCKED", "code": "PROMOTION_DUPLICATE_GATE_RECEIPTS", "control_check": check,
            "findings": [{"level": "ERROR", "code": "DUPLICATE_GATE_RECEIPT", "message": ", ".join(sorted(set(duplicates)))}],
            "missing_or_failed_gates": [], "post_promotion_actions": [],
        }

    profile = select_gate_profile(card)
    required = list(profile.base_qa) + list(profile.specialist_gates)
    missing_or_failed: list[dict[str, str]] = []
    replay_mappings: list[dict[str, str]] = []
    for gate in required:
        receipt = by_gate.get(gate)
        if not receipt:
            missing_or_failed.append({"gate": gate, "result": "NOT_RUN", "reason": "missing bound gate receipt"})
            continue
        if receipt["object_id"] != expected_object or receipt["source_id"] != expected_source:
            missing_or_failed.append({"gate": gate, "result": receipt["result"], "reason": "receipt object/source binding mismatch"})
            continue
        if binding.get("sha256") not in (None, "") and receipt["authority_sha256"] != binding["sha256"]:
            missing_or_failed.append({"gate": gate, "result": receipt["result"], "reason": "receipt authority hash mismatch"})
            continue
        if execution_mode == "LIVE" and receipt["basis"] != "DIRECT":
            missing_or_failed.append({"gate": gate, "result": receipt["result"], "reason": "LIVE promotion requires DIRECT gate evidence; replay mapping is not admissible"})
            continue
        if receipt["basis"] == "REPLAY_MAPPING":
            replay_mappings.append({"gate": gate, "historical_evidence_label": receipt.get("historical_evidence_label") or "UNSPECIFIED"})
        if receipt["result"] != "PASS":
            missing_or_failed.append({"gate": gate, "result": receipt["result"], "reason": "required bound gate must PASS"})
    if missing_or_failed:
        return {
            "status": "BLOCKED", "code": "PROMOTION_GATES_OPEN", "control_check": check,
            "gate_profile": asdict(profile), "transition": transition, "execution_mode": execution_mode,
            "findings": [], "missing_or_failed_gates": missing_or_failed, "post_promotion_actions": [],
        }

    simulated_actions = ["ARTIFACT_REGISTER"]
    sync = card.get("sync_persistence_trigger")
    if sync == "RECEIPT":
        simulated_actions.append("RECEIPT_SYNC")
    if sync == "PAP":
        simulated_actions.append("PERSISTENCE_RECEIPT_SYNC")
    if sync == "FULL_SYNC":
        simulated_actions.extend(["NOTION_GITHUB_DRIVE_FULL_SYNC", "CONTRADICTION_SCAN"])

    replay_only = execution_mode == "REPLAY"
    return {
        "status": "READY_FOR_HUMAN_DECISION",
        "code": "PROMOTION_REPLAY_PREREQUISITES_PASS" if replay_only else "PROMOTION_BOUND_PREREQUISITES_PASS",
        "control_check": check, "gate_profile": asdict(profile), "transition": transition,
        "execution_mode": execution_mode, "replay_only": replay_only, "replay_mappings": replay_mappings,
        "missing_or_failed_gates": [],
        "post_promotion_actions": [] if replay_only else simulated_actions,
        "simulated_post_promotion_actions": simulated_actions if replay_only else [],
        "human_decision_required": True,
    }


def _parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def snapshot_payload_hash(snapshot: dict[str, Any]) -> str:
    payload = {
        "object_id": snapshot["object_id"], "revision": snapshot["revision"],
        "fields": snapshot["fields"], "semantic": snapshot["semantic"],
    }
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def scan_contradictions(manifest: dict[str, Any]) -> dict[str, Any]:
    findings = _schema_findings(manifest)
    if findings or manifest.get("kind") != "CONTRADICTION_MANIFEST":
        return {
            "status": "BLOCKED", "code": "CONTRADICTION_SCAN_SCHEMA_BLOCKED",
            "object_id": manifest.get("object_id"), "findings": findings, "systems_checked": [],
        }
    scan_as_of = _parse_time(manifest["scan_as_of"])
    max_age = manifest["max_age_seconds"]
    expected, semantic_expected = manifest["expected"], manifest["semantic_expected"]
    for system in REQUIRED_SYNC_SYSTEMS:
        snap = manifest["systems"][system]
        if snap["status"] != "FOUND":
            findings.append({"level": "ERROR", "code": "SYSTEM_NOT_FOUND", "system": system, "message": f"status={snap['status']}"})
            continue
        if snap["object_id"] != manifest["object_id"]:
            findings.append({"level": "ERROR", "code": "OBJECT_ID_MISMATCH", "system": system, "message": "snapshot object_id mismatch"})
        try:
            observed = _parse_time(snap["observed_at"])
            age = (scan_as_of - observed).total_seconds()
            if age < 0 or age > max_age:
                findings.append({"level": "ERROR", "code": "SNAPSHOT_STALE", "system": system, "message": f"snapshot age {age}s outside 0..{max_age}s"})
        except Exception as exc:
            findings.append({"level": "ERROR", "code": "SNAPSHOT_TIME_INVALID", "system": system, "message": str(exc)})
        calculated = snapshot_payload_hash(snap)
        if calculated != snap["payload_sha256"]:
            findings.append({"level": "ERROR", "code": "SNAPSHOT_PAYLOAD_HASH_MISMATCH", "system": system, "expected": calculated, "actual": snap["payload_sha256"], "message": "snapshot payload hash does not bind fields/semantic/revision"})
        for key, value in expected.items():
            if key not in snap["fields"]:
                findings.append({"level": "ERROR", "code": "FIELD_MISSING", "system": system, "field": key, "message": f"missing field {key}"})
            elif snap["fields"][key] != value:
                findings.append({"level": "ERROR", "code": "CONTRADICTION", "system": system, "field": key, "expected": value, "actual": snap["fields"][key], "message": "field contradicts expected state"})
        for key, value in semantic_expected.items():
            if key not in snap["semantic"]:
                findings.append({"level": "ERROR", "code": "SEMANTIC_ASSERTION_MISSING", "system": system, "field": key, "message": f"missing semantic assertion {key}"})
            elif snap["semantic"][key] != value:
                findings.append({"level": "ERROR", "code": "SEMANTIC_CONTRADICTION", "system": system, "field": key, "expected": value, "actual": snap["semantic"][key], "message": "semantic assertion contradicts expected state"})
    status = "PASS" if not findings else "BLOCKED"
    return {
        "status": status, "code": "CONTRADICTION_SCAN_PASS" if status == "PASS" else "CONTRADICTION_SCAN_BLOCKED",
        "object_id": manifest["object_id"], "findings": findings, "systems_checked": REQUIRED_SYNC_SYSTEMS,
    }


def evaluate_master_runtime(state: dict[str, Any]) -> dict[str, Any]:
    """Evaluate the thin complex-project Master Runtime without self-promoting a project.

    This function compiles existing Design Intelligence, shared design-development,
    professional-process, integration, review, dependency and change-propagation states. It owns no specialist truth and
    never converts machine completeness into Design KEEP or Promotion.
    """
    findings = _schema_findings(state)
    if findings or state.get("kind") != "MASTER_RUNTIME_STATE":
        return {
            "status": "BLOCKED",
            "code": "MASTER_RUNTIME_SCHEMA_BLOCKED",
            "findings": findings,
            "required_actions": [],
            "claim_ceiling_inputs": [],
            "human_decision_required": False,
        }

    required_actions: list[dict[str, str]] = []
    semantic_findings: list[dict[str, str]] = []

    design_intelligence = state["design_intelligence"]
    if design_intelligence["state"] != "CURRENT" or not design_intelligence.get("packet_id"):
        required_actions.append({
            "scope": "DESIGN_INTELLIGENCE",
            "action": "RESOLVE_OR_REFRESH_DESIGN_INTELLIGENCE_PACKET",
            "reason": f"state={design_intelligence['state']}; packet_id={design_intelligence.get('packet_id')!r}",
        })

    design_quality = state["design_quality_development"]
    if design_quality["triggered"]:
        if design_quality["state"] == "NOT_REQUIRED" or design_quality["verdict"] == "N_A" or design_quality["maturity"] == "N_A":
            semantic_findings.append({
                "level": "ERROR", "code": "MASTER_DESIGN_QUALITY_TRIGGER_STATE_CONTRADICTION",
                "message": "triggered design quality/development cannot use NOT_REQUIRED/N_A state",
            })
        if not design_quality.get("receipt_id"):
            required_actions.append({"scope": "DESIGN_QUALITY", "action": "EMIT_DESIGN_QUALITY_DEVELOPMENT_RECEIPT", "reason": "triggered design quality/development has no current receipt_id"})
        if design_quality["state"] != "CURRENT" or design_quality["stale"]:
            scope = "STALE:DESIGN_QUALITY" if design_quality["state"] == "STALE" or design_quality["stale"] else "DESIGN_QUALITY"
            required_actions.append({"scope": scope, "action": "REFRESH_DESIGN_QUALITY_READBACK", "reason": f"state={design_quality['state']}; stale={design_quality['stale']}"})
        if design_quality["verdict"] != "KEEP":
            required_actions.append({"scope": "DESIGN_QUALITY", "action": "RESOLVE_DESIGN_QUALITY_VERDICT", "reason": f"design quality verdict={design_quality['verdict']}"})
    else:
        if design_quality["state"] != "NOT_REQUIRED" or design_quality["verdict"] != "N_A" or design_quality["maturity"] != "N_A" or design_quality["stale"]:
            semantic_findings.append({
                "level": "ERROR", "code": "MASTER_DESIGN_QUALITY_NOT_TRIGGERED_STATE_CONTRADICTION",
                "message": "non-triggered design quality/development must use state=NOT_REQUIRED, verdict=N_A, maturity=N_A, stale=false",
            })
        if design_quality.get("receipt_id"):
            semantic_findings.append({
                "level": "ERROR", "code": "MASTER_DESIGN_QUALITY_NOT_TRIGGERED_RECEIPT_CONTRADICTION",
                "message": "non-triggered design quality/development cannot claim a receipt",
            })

    professional_processes = state["professional_processes"]
    process_keys = [(x["domain"], x["process_id"]) for x in professional_processes]
    duplicates = sorted({x for x in process_keys if process_keys.count(x) > 1})
    if duplicates:
        semantic_findings.append({
            "level": "ERROR", "code": "MASTER_PROFESSIONAL_PROCESS_DUPLICATE",
            "message": f"professional_processes must be unique by domain/process_id; duplicates={duplicates}",
        })
    for process in professional_processes:
        key = f"{process['domain']}:{process['process_id']}"
        if process["triggered"]:
            if process["state"] == "NOT_REQUIRED" or process["verdict"] == "N_A":
                semantic_findings.append({
                    "level": "ERROR", "code": "MASTER_PROFESSIONAL_PROCESS_TRIGGER_STATE_CONTRADICTION",
                    "message": f"{key}: triggered professional process cannot use NOT_REQUIRED/N_A state",
                })
            if not process.get("receipt_id"):
                required_actions.append({"scope": f"PROFESSIONAL_PROCESS:{key}", "action": "EMIT_OR_REFRESH_PROFESSIONAL_PROCESS_RECEIPT", "reason": "triggered professional process has no current receipt_id"})
            if process["state"] != "CURRENT":
                scope = f"STALE:PROFESSIONAL_PROCESS:{key}" if process["state"] == "STALE" else f"PROFESSIONAL_PROCESS:{key}"
                required_actions.append({"scope": scope, "action": "RESOLVE_OR_REFRESH_PROFESSIONAL_PROCESS", "reason": f"state={process['state']}"})
            if process["verdict"] != "PASS":
                required_actions.append({"scope": f"PROFESSIONAL_PROCESS:{key}", "action": "RESOLVE_PROFESSIONAL_PROCESS_VERDICT", "reason": f"verdict={process['verdict']}"})
        else:
            if process["state"] != "NOT_REQUIRED" or process["verdict"] != "N_A" or process.get("receipt_id"):
                semantic_findings.append({
                    "level": "ERROR", "code": "MASTER_PROFESSIONAL_PROCESS_NOT_TRIGGERED_CONTRADICTION",
                    "message": f"{key}: non-triggered process must be NOT_REQUIRED/N_A with no receipt",
                })

    integration = state["integration"]
    if integration["triggered"]:
        if integration["state"] == "NOT_REQUIRED" or integration["verdict"] == "N_A":
            semantic_findings.append({
                "level": "ERROR", "code": "MASTER_INTEGRATION_TRIGGER_STATE_CONTRADICTION",
                "message": "triggered integration cannot use NOT_REQUIRED/N_A state",
            })
        if not integration.get("packet_id"):
            required_actions.append({"scope": "INTEGRATION", "action": "COMPILE_INTEGRATION_PACKET", "reason": "triggered integration has no packet_id"})
        if not integration.get("receipt_id"):
            required_actions.append({"scope": "INTEGRATION", "action": "RUN_INTEGRATION_READBACK", "reason": "triggered integration has no current receipt_id"})
        if integration["state"] != "CURRENT":
            required_actions.append({"scope": "INTEGRATION", "action": "REFRESH_OR_RECONCILE_INTEGRATION", "reason": f"integration state={integration['state']}"})
        if integration["verdict"] != "PASS":
            required_actions.append({"scope": "INTEGRATION", "action": "RESOLVE_INTEGRATION_VERDICT", "reason": f"integration verdict={integration['verdict']}"})
        if integration["open_major_critical_interfaces"] > 0:
            required_actions.append({
                "scope": "INTEGRATION", "action": "CLOSE_MAJOR_CRITICAL_INTERFACES",
                "reason": f"open_major_critical_interfaces={integration['open_major_critical_interfaces']}",
            })
        if integration["unresolved_authority_conflicts"] > 0:
            required_actions.append({
                "scope": "AUTHORITY", "action": "RESOLVE_SHARED_VARIABLE_OR_INTERFACE_AUTHORITY",
                "reason": f"unresolved_authority_conflicts={integration['unresolved_authority_conflicts']}",
            })
    else:
        if integration["state"] != "NOT_REQUIRED" or integration["verdict"] != "N_A":
            semantic_findings.append({
                "level": "ERROR", "code": "MASTER_INTEGRATION_NOT_TRIGGERED_STATE_CONTRADICTION",
                "message": "non-triggered integration must use state=NOT_REQUIRED and verdict=N_A",
            })
        if integration.get("packet_id") or integration.get("receipt_id"):
            semantic_findings.append({
                "level": "ERROR", "code": "MASTER_INTEGRATION_NOT_TRIGGERED_RECEIPT_CONTRADICTION",
                "message": "non-triggered integration cannot claim packet/receipt closure",
            })
        if integration["open_major_critical_interfaces"] or integration["unresolved_authority_conflicts"]:
            semantic_findings.append({
                "level": "ERROR", "code": "MASTER_INTEGRATION_NOT_TRIGGERED_OPEN_STATE",
                "message": "non-triggered integration cannot carry open major/critical interfaces or authority conflicts",
            })

    reviews = state["reviews"]
    observed_types = [r["review_type"] for r in reviews]
    duplicates = sorted({x for x in observed_types if observed_types.count(x) > 1})
    missing = sorted(MASTER_REVIEW_TYPES - set(observed_types))
    extras = sorted(set(observed_types) - MASTER_REVIEW_TYPES)
    if duplicates or missing or extras:
        semantic_findings.append({
            "level": "ERROR", "code": "MASTER_REVIEW_SET_INVALID",
            "message": f"reviews must contain each canonical review class exactly once; missing={missing}; duplicates={duplicates}; extras={extras}",
        })

    for review in reviews:
        kind = review["review_type"]
        triggered = review["triggered"]
        result = review["result"]
        receipt_ref = review.get("receipt_ref")
        if not triggered:
            if result != "N_A" or receipt_ref is not None:
                semantic_findings.append({
                    "level": "ERROR", "code": "MASTER_REVIEW_NOT_TRIGGERED_CONTRADICTION",
                    "message": f"{kind}: non-triggered review must be N_A with no receipt_ref",
                })
            continue
        if result == "N_A":
            semantic_findings.append({
                "level": "ERROR", "code": "MASTER_TRIGGERED_REVIEW_NA",
                "message": f"{kind}: triggered review cannot be N_A",
            })
            continue
        if result != "NOT_RUN" and not receipt_ref:
            semantic_findings.append({
                "level": "ERROR", "code": "MASTER_REVIEW_RECEIPT_REQUIRED",
                "message": f"{kind}: executed review result {result} requires receipt_ref",
            })
        expected = "KEEP" if kind == "DESIGN" else "PASS"
        if result != expected:
            required_actions.append({
                "scope": f"REVIEW:{kind}",
                "action": "RUN_OR_RESOLVE_TRIGGERED_REVIEW" if result == "NOT_RUN" else "REPAIR_AND_REVIEW",
                "reason": f"required promotion result={expected}; current={result}",
            })

    for dep in state["dependencies"]:
        if dep["state"] != "CURRENT":
            required_actions.append({
                "scope": f"DEPENDENCY:{dep['object_id']}",
                "action": "RECONCILE_DEPENDENCY",
                "reason": f"dependency state={dep['state']}",
            })

    for event in state["change_events"]:
        impact = event["impact_class"]
        propagation = event["propagation_state"]
        allowed = {"NOT_REQUIRED", "APPLIED"} if impact == "NON_MATERIAL" else {"APPLIED"}
        if propagation not in allowed:
            required_actions.append({
                "scope": f"CHANGE:{event['change_id']}",
                "action": "PROPAGATE_AND_REOPEN_AFFECTED_STATE",
                "reason": f"impact_class={impact}; propagation_state={propagation}",
            })

    for blocker in state["open_blockers"]:
        required_actions.append({"scope": "BLOCKER", "action": "RESOLVE_BLOCKER", "reason": blocker})

    claim_ceiling_inputs = [
        {"owner": "DESIGN_INTELLIGENCE", "claim_ceiling": design_intelligence["claim_ceiling"]},
    ]
    if design_quality["triggered"]:
        claim_ceiling_inputs.append({"owner": "DESIGN_QUALITY_DEVELOPMENT", "claim_ceiling": design_quality["claim_ceiling"]})
    for process in professional_processes:
        if process["triggered"]:
            claim_ceiling_inputs.append({"owner": f"PROFESSIONAL_PROCESS:{process['domain']}:{process['process_id']}", "claim_ceiling": process["claim_ceiling"]})
    if integration["triggered"]:
        claim_ceiling_inputs.append({"owner": "INTEGRATION", "claim_ceiling": integration["claim_ceiling"]})

    if semantic_findings:
        return {
            "status": "BLOCKED",
            "code": "MASTER_RUNTIME_STATE_CONTRADICTION",
            "findings": semantic_findings,
            "required_actions": required_actions,
            "claim_ceiling_inputs": claim_ceiling_inputs,
            "claim_ceiling_rule": "LOWEST_APPLICABLE_VALID_CLAIM_GOVERNS; MACHINE_DOES_NOT_RANK_DOMAIN-SPECIFIC_CLAIM_TEXT",
            "human_decision_required": False,
        }

    if required_actions:
        return {
            "status": "RECONCILIATION_REQUIRED" if any(a["scope"].startswith(("DEPENDENCY:", "CHANGE:", "STALE:")) or a["scope"] in {"AUTHORITY", "INTEGRATION"} for a in required_actions) else "IN_PROGRESS",
            "code": "MASTER_RUNTIME_OPEN_WORK",
            "findings": [],
            "required_actions": required_actions,
            "claim_ceiling_inputs": claim_ceiling_inputs,
            "claim_ceiling_rule": "LOWEST_APPLICABLE_VALID_CLAIM_GOVERNS; MACHINE_DOES_NOT_RANK_DOMAIN-SPECIFIC_CLAIM_TEXT",
            "human_decision_required": False,
        }

    if state["promotion_requested"]:
        return {
            "status": "READY_FOR_HUMAN_DECISION",
            "code": "MASTER_RUNTIME_PROMOTION_PREREQUISITES_PASS",
            "findings": [],
            "required_actions": [],
            "claim_ceiling_inputs": claim_ceiling_inputs,
            "claim_ceiling_rule": "LOWEST_APPLICABLE_VALID_CLAIM_GOVERNS; MACHINE_DOES_NOT_RANK_DOMAIN-SPECIFIC_CLAIM_TEXT",
            "human_decision_required": True,
        }

    return {
        "status": "RUNNABLE",
        "code": "MASTER_RUNTIME_CURRENT_AND_RUNNABLE",
        "findings": [],
        "required_actions": [],
        "claim_ceiling_inputs": claim_ceiling_inputs,
        "claim_ceiling_rule": "LOWEST_APPLICABLE_VALID_CLAIM_GOVERNS; MACHINE_DOES_NOT_RANK_DOMAIN-SPECIFIC_CLAIM_TEXT",
        "human_decision_required": False,
    }


def _print(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OLEANDER Project Control Plane v0.3 orchestration")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("providers"); p.add_argument("snapshot")
    p = sub.add_parser("promotion"); p.add_argument("card"); p.add_argument("gate_receipts")
    p = sub.add_parser("contradictions"); p.add_argument("manifest")
    p = sub.add_parser("master-runtime"); p.add_argument("state")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "providers":
        result = evaluate_provider_chain(load_json(args.snapshot)); _print(result)
        return 0 if result.get("actionability") == "ALLOWED" else 6
    if args.command == "promotion":
        result = evaluate_promotion(load_json(args.card), load_json(args.gate_receipts)); _print(result)
        return 0 if result["status"] == "READY_FOR_HUMAN_DECISION" else 7
    if args.command == "contradictions":
        result = scan_contradictions(load_json(args.manifest)); _print(result)
        return 0 if result["status"] == "PASS" else 8
    if args.command == "master-runtime":
        result = evaluate_master_runtime(load_json(args.state)); _print(result)
        return 0 if result["status"] in {"RUNNABLE", "READY_FOR_HUMAN_DECISION"} else 9
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
