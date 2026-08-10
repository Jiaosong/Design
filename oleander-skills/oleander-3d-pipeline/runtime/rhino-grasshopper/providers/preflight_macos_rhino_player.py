#!/usr/bin/env python3
"""Environment-only preflight for a possible free macOS Intel Rhino + GrasshopperPlayer path.

This script deliberately does NOT download, install, launch, license, or authenticate Rhino.
It only records whether the GitHub-hosted macOS environment satisfies the platform side
of the contract. Therefore its output is control-plane evidence, never CP2 runtime evidence.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
from pathlib import Path


def run_text(*cmd: str) -> str:
    try:
        result = subprocess.run(cmd, check=False, text=True, capture_output=True)
        text = (result.stdout or result.stderr or "").strip()
        return text
    except Exception as exc:
        return f"ERROR:{type(exc).__name__}:{exc}"


def disk_free_gb(path: str = "/") -> float:
    usage = shutil.disk_usage(path)
    return round(usage.free / (1024 ** 3), 2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()

    if os.environ.get("RHINO_TOKEN"):
        raise SystemExit("macOS free-runtime preflight refuses RHINO_TOKEN / Core-Hour billing")

    machine = platform.machine()
    mac_version = platform.mac_ver()[0]
    rhino_app = Path("/Applications/Rhino 8.app")
    rhinocode = Path("/Applications/Rhino 8.app/Contents/Resources/bin/rhinocode")
    free_gb = disk_free_gb("/")

    platform_supported = machine in {"x86_64", "AMD64"} and bool(mac_version)
    rhino_installed = rhino_app.exists()
    rhinocode_installed = rhinocode.exists()

    if not platform_supported:
        state = "UNSUPPORTED_ARCHITECTURE"
        action = "HOLD_CP2_PRESERVE_CP4_OPEN"
    elif rhino_installed and rhinocode_installed:
        state = "RUNTIME_INSTALLED_LICENSE_UNKNOWN"
        action = "HOLD_FOR_INSTALLER_AND_LICENSE"
    else:
        state = "INSTALLER_AND_LICENSE_REQUIRED"
        action = "HOLD_FOR_INSTALLER_AND_LICENSE"

    receipt = {
        "preflight_id": "OLEANDER-GITHUB-MACOS-X64-RHINO-PLAYER-PREFLIGHT-v0.1",
        "provider_id": "GITHUB_MACOS_X64_STANDARD",
        "runtime_mode": "FREE_HOSTED_CANDIDATE",
        "execution_engine": "RHINO_DESKTOP_GRASSHOPPER_PLAYER",
        "cost_policy": "NO_PAID_RUNTIME",
        "user_workstation": False,
        "environment": {
            "runner_os": os.environ.get("RUNNER_OS"),
            "runner_arch": os.environ.get("RUNNER_ARCH"),
            "platform_machine": machine,
            "macos_version": mac_version,
            "kernel": platform.platform(),
            "hardware_brand": run_text("sysctl", "-n", "machdep.cpu.brand_string"),
            "free_disk_gb": free_gb,
            "github_repository": os.environ.get("GITHUB_REPOSITORY"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "github_run_number": os.environ.get("GITHUB_RUN_NUMBER"),
        },
        "platform_contract": {
            "required_architecture": "x64 / Intel",
            "required_os_family": "macOS supported by Rhino 8",
            "platform_supported_candidate": platform_supported,
            "rhino_system_requirement_disk_gb": 10,
            "disk_requirement_observed": free_gb >= 10,
        },
        "runtime_presence": {
            "rhino_8_app_present": rhino_installed,
            "rhinocode_present": rhinocode_installed,
            "rhino_app_path": str(rhino_app),
            "rhinocode_path": str(rhinocode),
        },
        "provider_state": state,
        "selector_action": action,
        "licensing": {
            "attempted": False,
            "license_present": None,
            "rhino_account_login_attempted": False,
            "evaluation_requested": False,
            "core_hour_token_allowed": False,
            "note": "No license/account secret was requested or used. A future execution path needs explicit authorization and a supported licensing method before Rhino may be launched."
        },
        "grasshopper_capability_target": {
            "mechanism": "GrasshopperPlayer / rhinocode inside Rhino 8 for Mac",
            "runtime_test_attempted": False,
            "cp2_promotion_possible_only_after_real_execution": True,
            "cp4_closable_by_this_headless_path": False,
        },
        "evidence_level": "ENVIRONMENT_PREFLIGHT_ONLY",
        "runtime_evidence": False,
        "cp2": "OPEN",
        "cp4": "OPEN"
    }

    out = Path(args.receipt)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({
        "provider_state": state,
        "selector_action": action,
        "platform_machine": machine,
        "macos_version": mac_version,
        "free_disk_gb": free_gb,
        "rhino_installed": rhino_installed,
        "rhinocode_installed": rhinocode_installed,
        "runtime_evidence": False,
        "cp2": "OPEN",
        "cp4": "OPEN"
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
