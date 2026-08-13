#!/usr/bin/env python3
"""OLEANDER Project Control Plane v0.3 orchestration layer.

This module orchestrates external-provider receipts, promotion readiness, and
cross-system contradiction scans. It is subordinate to the v0.2 executable
compiler/router and never mutates Notion, GitHub, Drive, File Library, or project
registries by itself.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from control_plane import load_json, run_check, select_gate_profile  # noqa: E402

PROVIDER_ORDER = ["current_authority", "github", "drive", "file_library", "runtime"]
PROVIDER_STATUSES = {"FOUND", "NOT_FOUND", "UNAVAILABLE", "BLOCKED", "ERROR"}
GATE_RESULTS = {"PASS", "FAIL", "BLOCKED", "NOT_RUN", "N_A"}
REQUIRED_SYNC_SYSTEMS = ["notion", "github", "drive"]


def _provider_receipts(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    receipts = snapshot.get("providers", [])
    if not isinstance(receipts, list):
        raise ValueError("providers must be an array")
    return receipts


def evaluate_provider_chain(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Fail-closed external provider chain.

    Lower-priority hits cannot silently override an unavailable higher-priority
    source. UNLOCATED / E0 eligibility is granted only when every provider in the
    canonical chain was attempted and returned NOT_FOUND. A successful hit may
    stop the chain once every higher-priority provider has been resolved.
    """
    receipts = _provider_receipts(snapshot)
    findings: list[dict[str, str]] = []

    by_provider: dict[str, dict[str, Any]] = {}
    observed_order: list[str] = []
    for i, receipt in enumerate(receipts):
        if not isinstance(receipt, dict):
            findings.append({"level": "ERROR", "code": "PROVIDER_RECEIPT_TYPE", "message": f"providers[{i}] must be an object"})
            continue
        provider = receipt.get("provider")
        if provider not in PROVIDER_ORDER:
            findings.append({"level": "ERROR", "code": "PROVIDER_NAME", "message": f"providers[{i}].provider invalid"})
            continue
        if provider in by_provider:
            findings.append({"level": "ERROR", "code": "PROVIDER_DUPLICATE", "message": f"duplicate provider receipt: {provider}"})
            continue
        observed_order.append(provider)
        by_provider[provider] = receipt

        if receipt.get("attempted") is not True:
            findings.append({"level": "ERROR", "code": "PROVIDER_NOT_ATTEMPTED", "message": f"{provider} must explicitly record attempted=true"})
        status = receipt.get("status")
        if status not in PROVIDER_STATUSES:
            findings.append({"level": "ERROR", "code": "PROVIDER_STATUS", "message": f"{provider} status invalid"})
        hits = receipt.get("hits", [])
        if not isinstance(hits, list):
            findings.append({"level": "ERROR", "code": "PROVIDER_HITS", "message": f"{provider}.hits must be an array"})
        elif status == "FOUND" and not hits:
            findings.append({"level": "ERROR", "code": "PROVIDER_FOUND_WITHOUT_HIT", "message": f"{provider} FOUND requires at least one hit"})
        elif status != "FOUND" and hits:
            findings.append({"level": "ERROR", "code": "PROVIDER_HITS_STATUS_CONFLICT", "message": f"{provider} has hits but status is {status}"})

    if observed_order != [p for p in PROVIDER_ORDER if p in by_provider]:
        findings.append({"level": "ERROR", "code": "PROVIDER_ORDER", "message": "provider receipts must preserve canonical authority order"})

    if any(f["level"] == "ERROR" for f in findings):
        return {
            "status": "BLOCKED",
            "code": "CB-03_PROVIDER_CHAIN_INVALID",
            "query": snapshot.get("query"),
            "findings": findings,
            "selected_provider": None,
            "hits": [],
            "e0_eligible": False,
        }

    first_found_index = None
    first_found_provider = None
    for idx, provider in enumerate(PROVIDER_ORDER):
        if provider in by_provider and by_provider[provider]["status"] == "FOUND":
            first_found_index = idx
            first_found_provider = provider
            break

    if first_found_provider is not None:
        higher = PROVIDER_ORDER[:first_found_index]
        missing_higher = [p for p in higher if p not in by_provider]
        gaps = [p for p in higher if p in by_provider and by_provider[p]["status"] in {"UNAVAILABLE", "BLOCKED", "ERROR"}]
        unresolved_higher = missing_higher + gaps
        if unresolved_higher:
            return {
                "status": "BLOCKED",
                "code": "CB-03_HIGHER_AUTHORITY_GAP",
                "query": snapshot.get("query"),
                "findings": [{
                    "level": "ERROR",
                    "code": "HIGHER_AUTHORITY_UNRESOLVED",
                    "message": f"lower-priority hit exists at {first_found_provider}, but higher-priority providers are unresolved: {', '.join(unresolved_higher)}",
                }],
                "selected_provider": None,
                "hits": [],
                "e0_eligible": False,
            }
        return {
            "status": "FOUND",
            "code": "CB-03_RESOLVED",
            "query": snapshot.get("query"),
            "findings": [],
            "selected_provider": first_found_provider,
            "hits": by_provider[first_found_provider]["hits"],
            "e0_eligible": False,
        }

    missing = [p for p in PROVIDER_ORDER if p not in by_provider]
    if missing:
        return {
            "status": "BLOCKED",
            "code": "CB-03_PROVIDER_CHAIN_INCOMPLETE",
            "query": snapshot.get("query"),
            "findings": [{
                "level": "ERROR",
                "code": "PROVIDER_CHAIN_INCOMPLETE",
                "message": f"cannot declare UNLOCATED / E0 before all providers are attempted: {', '.join(missing)}",
            }],
            "selected_provider": None,
            "hits": [],
            "e0_eligible": False,
        }

    unresolved = [p for p in PROVIDER_ORDER if by_provider[p]["status"] in {"UNAVAILABLE", "BLOCKED", "ERROR"}]
    if unresolved:
        return {
            "status": "BLOCKED",
            "code": "CB-03_PROVIDER_UNAVAILABLE",
            "query": snapshot.get("query"),
            "findings": [{
                "level": "ERROR",
                "code": "PROVIDER_UNRESOLVED",
                "message": f"cannot declare UNLOCATED / E0 while providers are unresolved: {', '.join(unresolved)}",
            }],
            "selected_provider": None,
            "hits": [],
            "e0_eligible": False,
        }

    return {
        "status": "UNLOCATED",
        "code": "CB-03_E0_ELIGIBLE",
        "query": snapshot.get("query"),
        "findings": [],
        "selected_provider": None,
        "hits": [],
        "e0_eligible": True,
    }


def evaluate_promotion(card: dict[str, Any], gate_results: dict[str, Any]) -> dict[str, Any]:
    """Compile promotion prerequisites without making the human promotion decision."""
    check = run_check(card)
    if check["status"] != "PASS":
        return {
            "status": "BLOCKED",
            "code": "PROMOTION_CONTROL_CARD_BLOCKED",
            "control_check": check,
            "missing_or_failed_gates": [],
            "post_promotion_actions": [],
        }

    if card.get("mode") != "AUTHORITY":
        return {
            "status": "NOT_READY",
            "code": "PROMOTION_REQUIRES_AUTHORITY_MODE",
            "control_check": check,
            "missing_or_failed_gates": [],
            "post_promotion_actions": [],
        }

    if not isinstance(gate_results, dict):
        return {
            "status": "BLOCKED",
            "code": "PROMOTION_GATE_RESULTS_INVALID",
            "control_check": check,
            "missing_or_failed_gates": ["gate_results must be an object"],
            "post_promotion_actions": [],
        }

    profile = select_gate_profile(card)
    required = list(profile.base_qa) + list(profile.specialist_gates)
    missing_or_failed: list[dict[str, str]] = []
    for gate in required:
        result = gate_results.get(gate, "NOT_RUN")
        if result not in GATE_RESULTS:
            missing_or_failed.append({"gate": gate, "result": str(result), "reason": "invalid result"})
        elif result != "PASS":
            missing_or_failed.append({"gate": gate, "result": result, "reason": "required gate must PASS before promotion"})

    if missing_or_failed:
        return {
            "status": "BLOCKED",
            "code": "PROMOTION_GATES_OPEN",
            "control_check": check,
            "gate_profile": asdict(profile),
            "missing_or_failed_gates": missing_or_failed,
            "post_promotion_actions": [],
        }

    actions = ["ARTIFACT_REGISTER"]
    sync = card.get("sync_persistence_trigger")
    if sync == "RECEIPT":
        actions.append("RECEIPT_SYNC")
    if sync == "PAP":
        actions.append("PERSISTENCE_RECEIPT_SYNC")
    if sync == "FULL_SYNC":
        actions.extend(["NOTION_GITHUB_DRIVE_FULL_SYNC", "CONTRADICTION_SCAN"])

    return {
        "status": "READY_FOR_HUMAN_DECISION",
        "code": "PROMOTION_MACHINE_PREREQUISITES_PASS",
        "control_check": check,
        "gate_profile": asdict(profile),
        "missing_or_failed_gates": [],
        "post_promotion_actions": actions,
        "human_decision_required": True,
    }


def scan_contradictions(manifest: dict[str, Any]) -> dict[str, Any]:
    """Compare system snapshots to one explicit expected canonical state."""
    expected = manifest.get("expected")
    systems = manifest.get("systems")
    findings: list[dict[str, Any]] = []

    if not isinstance(expected, dict) or not expected:
        findings.append({"level": "ERROR", "code": "EXPECTED_STATE_MISSING", "message": "expected must be a non-empty object"})
    if not isinstance(systems, dict):
        findings.append({"level": "ERROR", "code": "SYSTEM_SNAPSHOTS_MISSING", "message": "systems must be an object"})
        systems = {}

    for system in REQUIRED_SYNC_SYSTEMS:
        snapshot = systems.get(system)
        if not isinstance(snapshot, dict):
            findings.append({"level": "ERROR", "code": "SYSTEM_MISSING", "system": system, "message": f"missing {system} snapshot"})
            continue
        status = snapshot.get("status")
        if status != "FOUND":
            findings.append({"level": "ERROR", "code": "SYSTEM_NOT_FOUND", "system": system, "message": f"{system} status must be FOUND, got {status}"})
            continue
        fields = snapshot.get("fields")
        if not isinstance(fields, dict):
            findings.append({"level": "ERROR", "code": "SYSTEM_FIELDS_MISSING", "system": system, "message": f"{system}.fields must be an object"})
            continue
        if isinstance(expected, dict):
            for key, expected_value in expected.items():
                if key not in fields:
                    findings.append({
                        "level": "ERROR",
                        "code": "FIELD_MISSING",
                        "system": system,
                        "field": key,
                        "message": f"{system} missing expected field {key}",
                    })
                elif fields[key] != expected_value:
                    findings.append({
                        "level": "ERROR",
                        "code": "CONTRADICTION",
                        "system": system,
                        "field": key,
                        "expected": expected_value,
                        "actual": fields[key],
                        "message": f"{system}.{key} contradicts expected canonical state",
                    })

    status = "PASS" if not findings else "BLOCKED"
    return {
        "status": status,
        "code": "CONTRADICTION_SCAN_PASS" if status == "PASS" else "CONTRADICTION_SCAN_BLOCKED",
        "object_id": manifest.get("object_id"),
        "findings": findings,
        "systems_checked": REQUIRED_SYNC_SYSTEMS,
    }


def _print(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OLEANDER Project Control Plane v0.3 orchestration")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("providers")
    p.add_argument("snapshot")

    p = sub.add_parser("promotion")
    p.add_argument("card")
    p.add_argument("gate_results")

    p = sub.add_parser("contradictions")
    p.add_argument("manifest")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "providers":
        result = evaluate_provider_chain(load_json(args.snapshot))
        _print(result)
        return 0 if result["status"] in {"FOUND", "UNLOCATED"} else 6

    if args.command == "promotion":
        result = evaluate_promotion(load_json(args.card), load_json(args.gate_results))
        _print(result)
        return 0 if result["status"] == "READY_FOR_HUMAN_DECISION" else 7

    if args.command == "contradictions":
        result = scan_contradictions(load_json(args.manifest))
        _print(result)
        return 0 if result["status"] == "PASS" else 8

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
