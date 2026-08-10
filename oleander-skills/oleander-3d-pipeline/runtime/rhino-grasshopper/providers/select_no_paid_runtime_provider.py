#!/usr/bin/env python3
"""Select an OLEANDER Rhino/Grasshopper runtime provider under strict no-paid policy.

This selector does not execute Rhino and is not runtime evidence. It distinguishes:
1. execution-ready providers;
2. technically supported candidates blocked by explicit human/install/license authority;
3. hard-rejected providers that violate platform, cost, service, or workstation policy.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

EXECUTION_READY_STATES = {"AVAILABLE"}
AUTHORITY_BLOCKED_STATES = {
    "INSTALLER_AND_LICENSE_REQUIRED",
    "HUMAN_AUTHORITY_REQUIRED",
    "RUNTIME_INSTALLED_LICENSE_UNKNOWN",
}


def staged_gate(state: str | None) -> tuple[str, str]:
    if state == "HUMAN_AUTHORITY_REQUIRED":
        return "HUMAN_AUTHORITY", "HOLD_FOR_HUMAN_AUTHORITY"
    if state == "RUNTIME_INSTALLED_LICENSE_UNKNOWN":
        return "LICENSE_VALIDATION_AUTHORITY", "HOLD_FOR_INSTALLER_AND_LICENSE"
    return "INSTALLER_AND_LICENSE_AUTHORITY", "HOLD_FOR_INSTALLER_AND_LICENSE"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()

    registry_path = Path(args.registry)
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    policy = data.get("policy") or {}
    providers = data.get("providers") or []

    if policy.get("paid_runtime_allowed") is not False:
        raise SystemExit("Registry violates selector invariant: paid_runtime_allowed must be false")
    if policy.get("user_workstation_allowed") is not False:
        raise SystemExit("Registry violates selector invariant: user_workstation_allowed must be false")
    if policy.get("surrogate_may_promote_cp2") is not False:
        raise SystemExit("Registry violates selector invariant: surrogate_may_promote_cp2 must be false")
    if policy.get("headless_may_close_cp4") is not False:
        raise SystemExit("Registry violates selector invariant: headless_may_close_cp4 must be false")

    execution_ready = []
    staged_candidates = []
    rejected = []

    for provider in providers:
        provider_id = provider.get("provider_id")
        state = provider.get("current_state")
        user_workstation = provider.get("user_workstation") is True
        explicitly_eligible = provider.get("eligible") is True
        probe_allowed = provider.get("probe_allowed") is True

        if explicitly_eligible and not user_workstation and state in EXECUTION_READY_STATES:
            execution_ready.append(provider_id)
            continue

        if not user_workstation and probe_allowed and state in AUTHORITY_BLOCKED_STATES:
            next_gate, next_action = staged_gate(state)
            staged_candidates.append({
                "provider_id": provider_id,
                "state": state,
                "execution_engine": provider.get("execution_engine"),
                "next_gate": next_gate,
                "next_action": next_action,
                "reason": provider.get("selector_reason"),
            })
            continue

        rejected.append({
            "provider_id": provider_id,
            "state": state,
            "reason": provider.get("selector_reason"),
        })

    if len(execution_ready) == 1:
        status = "ONE_EXECUTION_READY_PROVIDER"
        selected = execution_ready[0]
        best_candidate = selected
        next_action = "RUN_PROVIDER_PREFLIGHT"
    elif len(execution_ready) > 1:
        status = "MULTIPLE_EXECUTION_READY_PROVIDERS_TIEBREAK_REQUIRED"
        selected = None
        best_candidate = None
        next_action = "HOLD_FOR_TIEBREAK"
    elif staged_candidates:
        status = "NO_EXECUTION_READY_NO_PAID_PROVIDER"
        selected = None
        best_candidate = staged_candidates[0]["provider_id"]
        next_action = staged_candidates[0]["next_action"]
    else:
        status = "NO_ELIGIBLE_NO_PAID_PROVIDER"
        selected = None
        best_candidate = None
        next_action = "HOLD_CP2_PRESERVE_CP4_OPEN"

    receipt = {
        "selector_id": "OLEANDER-NO-PAID-RUNTIME-PROVIDER-SELECTOR-v0.3",
        "registry_id": data.get("registry_id"),
        "status": status,
        "selected_provider": selected,
        "best_current_candidate": best_candidate,
        "execution_ready_providers": execution_ready,
        "staged_candidates": staged_candidates,
        "rejected_providers": rejected,
        "next_action": next_action,
        "evidence_level": "CONTROL_PLANE_SELECTION_ONLY",
        "runtime_evidence": False,
        "cp2": "OPEN",
        "cp4": "OPEN",
    }

    receipt_path = Path(args.receipt)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "status": status,
        "selected_provider": selected,
        "best_current_candidate": best_candidate,
        "execution_ready_count": len(execution_ready),
        "staged_candidate_count": len(staged_candidates),
        "next_action": next_action,
        "runtime_evidence": False,
        "cp2": "OPEN",
        "cp4": "OPEN",
        "evidence_level": "CONTROL_PLANE_SELECTION_ONLY",
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
