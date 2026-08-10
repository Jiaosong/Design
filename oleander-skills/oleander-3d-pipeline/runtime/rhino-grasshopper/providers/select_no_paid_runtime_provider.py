#!/usr/bin/env python3
"""Select an OLEANDER Rhino/Grasshopper runtime provider under strict no-paid policy.

This selector does not execute Rhino and is not runtime evidence. It evaluates the
provider registry and returns only candidates that already satisfy the hard policy
constraints. Live availability still requires a provider-specific preflight.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ALLOWED_STATES_FOR_SELECTION = {"AVAILABLE"}


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

    eligible = []
    rejected = []
    for provider in providers:
        provider_id = provider.get("provider_id")
        hard_eligible = provider.get("eligible") is True
        state = provider.get("current_state")
        user_workstation = provider.get("user_workstation") is True
        if hard_eligible and not user_workstation and state in ALLOWED_STATES_FOR_SELECTION:
            eligible.append(provider_id)
        else:
            rejected.append({
                "provider_id": provider_id,
                "state": state,
                "reason": provider.get("selector_reason"),
            })

    if len(eligible) == 1:
        status = "ONE_ELIGIBLE_PROVIDER"
        selected = eligible[0]
        next_action = "RUN_PROVIDER_PREFLIGHT"
    elif len(eligible) > 1:
        status = "MULTIPLE_ELIGIBLE_PROVIDERS_HUMAN_OR_POLICY_TIEBREAK_REQUIRED"
        selected = None
        next_action = "HOLD_FOR_TIEBREAK"
    else:
        status = "NO_ELIGIBLE_NO_PAID_PROVIDER"
        selected = None
        next_action = "HOLD_CP2_PRESERVE_CP4_OPEN"

    receipt = {
        "selector_id": "OLEANDER-NO-PAID-RUNTIME-PROVIDER-SELECTOR-v0.1",
        "registry_id": data.get("registry_id"),
        "status": status,
        "selected_provider": selected,
        "eligible_providers": eligible,
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
        "eligible_count": len(eligible),
        "next_action": next_action,
        "cp2": "OPEN",
        "cp4": "OPEN",
        "evidence_level": "CONTROL_PLANE_SELECTION_ONLY",
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
