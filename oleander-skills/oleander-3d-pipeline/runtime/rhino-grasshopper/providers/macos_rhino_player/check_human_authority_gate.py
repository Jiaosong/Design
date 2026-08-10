#!/usr/bin/env python3
"""Evaluate whether the Rhino 8 Mac execution path has explicit human authority.

This checker never downloads, installs, licenses, authenticates, or starts Rhino.
It records only boolean presence / selected mode. Secret values are never emitted.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

ALLOWED_LICENSE_MODES = {
    "CLOUD_ZOO_AUTHORIZED_BUNDLE",
    "LAN_ZOO_AUTHORIZED_BUNDLE",
    "STANDALONE_EXPLICITLY_AUTHORIZED",
}


def is_true(value: str | None) -> bool:
    return (value or "").strip().lower() == "true"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()

    eula_accepted = is_true(os.environ.get("OLEANDER_RHINO8_EULA_ACCEPTED"))
    installer_present = bool((os.environ.get("RHINO_MAC_INSTALLER_URL") or "").strip())
    license_mode = (os.environ.get("OLEANDER_RHINO8_LICENSE_MODE") or "").strip()
    license_mode_allowed = license_mode in ALLOWED_LICENSE_MODES
    bundle_present = bool((os.environ.get("RHINO_MAC_LICENSE_BUNDLE_B64") or "").strip())

    blockers: list[str] = []
    if not eula_accepted:
        blockers.append("EULA_AUTHORITY_NOT_GRANTED")
    if not installer_present:
        blockers.append("INSTALLER_SOURCE_NOT_PROVIDED")
    if not license_mode_allowed:
        blockers.append("LICENSE_MODE_NOT_AUTHORIZED")
    if license_mode in {"CLOUD_ZOO_AUTHORIZED_BUNDLE", "LAN_ZOO_AUTHORIZED_BUNDLE"} and not bundle_present:
        blockers.append("LICENSE_BUNDLE_NOT_PROVIDED")
    if license_mode == "STANDALONE_EXPLICITLY_AUTHORIZED":
        blockers.append("STANDALONE_EPHEMERAL_VALIDATION_NOT_IMPLEMENTED")

    all_gates_pass = not blockers
    result = {
        "gate_id": "OLEANDER-RHINO8-MAC-HUMAN-AUTHORITY-GATE-v0.1",
        "provider_id": "GITHUB_MACOS_X64_STANDARD",
        "evaluated_inputs": {
            "eula_accepted": eula_accepted,
            "installer_source_present": installer_present,
            "license_mode": license_mode or None,
            "license_mode_allowed": license_mode_allowed,
            "license_bundle_present": bundle_present,
            "secret_values_logged": False,
        },
        "blockers": blockers,
        "all_gates_pass": all_gates_pass,
        "status": "AUTHORITY_READY_FOR_PREP" if all_gates_pass else "HUMAN_AUTHORITY_REQUIRED",
        "selector_action": "ALLOW_INSTALLER_AND_LICENSE_PREP" if all_gates_pass else "HOLD_FOR_HUMAN_AUTHORITY",
        "installer_downloaded": False,
        "rhino_installed": False,
        "licensing_attempted": False,
        "rhino_started": False,
        "grasshopper_executed": False,
        "runtime_evidence": False,
        "cp2": "OPEN",
        "cp4": "OPEN",
        "evidence_level": "HUMAN_AUTHORITY_GATE_ONLY"
    }

    out = Path(args.receipt)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "selector_action": result["selector_action"],
        "blocker_count": len(blockers),
        "blockers": blockers,
        "secret_values_logged": False,
        "runtime_evidence": False,
        "cp2": "OPEN",
        "cp4": "OPEN"
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
