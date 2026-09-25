from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


HERE = Path(__file__).resolve().parent
CONTRACT = HERE / "OLEANDER_COS_UPDATE_COMPATIBILITY_CONTRACT_v0.1.json"
BINDER = HERE / "bind_chat_on_steroids_oleander.py"
ENTRY_VALIDATOR = HERE / "validate_chat_entry_runtime.py"
RESOLVER = HERE / "oleander_chat_resolver_adapter.py"
RUNTIME_BRIDGE = HERE / "oleander_chat_runtime_bridge.py"
CHAT_COS_BRIDGE = (
    HERE
    / "candidates"
    / "human-ai-codesign-vnext"
    / "codesign_chat_cos_bridge_v0_1.py"
)
BAIDU_VERIFY = (
    HERE
    / "candidates"
    / "oleander-baidu-storage-app-v0.1"
    / "verify_local_runtime.ps1"
)


@dataclass(frozen=True)
class Check:
    check_id: str
    ok: bool
    scope: str
    detail: str


def _load_python(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"IMPORT_SPEC_UNAVAILABLE:{path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _default_paths() -> tuple[Path, Path, Path]:
    localappdata = os.environ.get("LOCALAPPDATA")
    appdata = os.environ.get("APPDATA")
    if not localappdata or not appdata:
        raise RuntimeError("WINDOWS_APPDATA_ENVIRONMENT_UNAVAILABLE")
    local = Path(localappdata)
    roaming = Path(appdata)
    return (
        local / "Programs" / "Chat On Steroids" / "Chat On Steroids.exe",
        local / "chat-on-steroids-updater" / "installer.exe",
        roaming / "chat-on-steroids" / "config.json",
    )


def _powershell_file_version(path: Path) -> str | None:
    if os.name != "nt" or not path.is_file():
        return None
    escaped = str(path).replace("'", "''")
    command = f"(Get-Item -LiteralPath '{escaped}').VersionInfo.FileVersion"
    completed = subprocess.run(
        ["powershell.exe", "-NoLogo", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=20,
        check=False,
    )
    if completed.returncode != 0:
        return None
    value = completed.stdout.strip()
    return value or None


def _run(command: list[str], *, timeout: int = 180) -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            command,
            cwd=HERE.parents[1],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, f"{type(exc).__name__}:{exc}"
    combined = "\n".join(
        part.strip() for part in (completed.stdout, completed.stderr) if part.strip()
    )
    if len(combined) > 1400:
        combined = combined[-1400:]
    return completed.returncode == 0, combined or f"exit={completed.returncode}"


def _config_bootstrap_checks(config_path: Path, binder, observed_version: str | None) -> list[Check]:
    scope = "COS_CONFIG_BOOTSTRAP"
    if not config_path.is_file():
        return [Check("COS_CONFIG_PRESENT_AND_PARSEABLE", False, scope, f"missing:{config_path}")]
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [Check("COS_CONFIG_PRESENT_AND_PARSEABLE", False, scope, f"{type(exc).__name__}:{exc}")]
    if not isinstance(data, dict):
        return [Check("COS_CONFIG_PRESENT_AND_PARSEABLE", False, scope, "config root is not an object")]

    mcp = data.get("mcp")
    goal = data.get("goal")
    schema_issues: list[str] = []
    if not isinstance(mcp, dict):
        schema_issues.append("mcp:not-object")
    if not isinstance(goal, dict):
        schema_issues.append("goal:not-object")
    if isinstance(mcp, dict) and not isinstance(mcp.get("instructions"), str):
        schema_issues.append("mcp.instructions:not-string")
    if isinstance(goal, dict):
        for field in ("prompt", "objectivePrompt", "loopPrompt"):
            value = goal.get(field)
            if not isinstance(value, str) or not value.strip():
                schema_issues.append(f"goal.{field}:not-nonempty-string")
        if not isinstance(goal.get("includeToolCalls"), bool):
            schema_issues.append("goal.includeToolCalls:not-bool")
    compatible_shape = not schema_issues
    checks = [
        Check(
            "COS_CONFIG_PRESENT_AND_PARSEABLE",
            compatible_shape,
            scope,
            "expected binder-written config field schema present"
            if compatible_shape
            else "incompatible config schema:" + ",".join(schema_issues),
        )
    ]
    if not compatible_shape:
        return checks

    marker_fields = {
        "mcp.instructions": mcp.get("instructions"),
        "goal.prompt": goal.get("prompt"),
        "goal.objectivePrompt": goal.get("objectivePrompt"),
        "goal.loopPrompt": goal.get("loopPrompt"),
    }
    missing = [
        name
        for name, value in marker_fields.items()
        if binder.BEGIN not in str(value or "") or binder.END not in str(value or "")
    ]
    checks.append(
        Check(
            "COS_BOOTSTRAP_MARKER_PRESENT",
            not missing,
            scope,
            "stable bootstrap marker present in mcp + goal surfaces"
            if not missing
            else "missing marker:" + ",".join(missing),
        )
    )

    tool_calls_enabled = goal.get("includeToolCalls") is True
    checks.append(
        Check(
            "COS_TOOL_CALL_FEEDBACK_ENABLED",
            tool_calls_enabled,
            scope,
            "goal.includeToolCalls=true" if tool_calls_enabled else "goal.includeToolCalls is not true",
        )
    )

    main_binding = str(binder.MAIN_CHAT_BINDING)
    bootstrap_text = main_binding + "\n" + str(binder.GOAL_BINDING)
    implementation_pins = [
        token
        for token in ("codesign_chat_cos_bridge_v0_1.py", "oleander-baidu-storage@oleander-personal")
        if token in bootstrap_text
    ]
    dynamic_only = (
        "OLEANDER_CHAT_ENTRY_RUNTIME.md" in main_binding
        and "OLEANDER_CHAT_ENTRY_RUNTIME.md" in str(binder.GOAL_BINDING)
        and not implementation_pins
    )
    checks.append(
        Check(
            "COS_BOOTSTRAP_DYNAMIC_ENTRY_ONLY",
            dynamic_only,
            scope,
            "bootstrap points to dynamic entry without capability implementation pins"
            if dynamic_only
            else "bootstrap implementation pins:" + ",".join(implementation_pins),
        )
    )

    version_pinned = bool(observed_version and observed_version in bootstrap_text)
    checks.append(
        Check(
            "COS_NO_INSTALLED_VERSION_PIN",
            not version_pinned,
            scope,
            "observed CoS version is not encoded as a bootstrap requirement"
            if not version_pinned
            else f"bootstrap contains installed CoS version:{observed_version}",
        )
    )
    return checks


def _repair_bootstrap(config_path: Path) -> tuple[bool, str]:
    return _run([sys.executable, str(BINDER), "--config", str(config_path), "--apply"], timeout=60)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Observe whether the current CoS installation remains compatible with OLEANDER's stable Chat bootstrap."
    )
    parser.add_argument("--repair-bootstrap", action="store_true", help="Explicitly reapply the existing stable bootstrap if compatible CoS config survived but the marker did not.")
    parser.add_argument("--skip-baidu-provider", action="store_true", help="Skip the real installed Baidu stdio acceptance check; core CoS compatibility is still checked.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument("--cos-exe", type=Path, default=None)
    parser.add_argument("--cos-updater", type=Path, default=None)
    parser.add_argument("--cos-config", type=Path, default=None)
    args = parser.parse_args()

    checks: list[Check] = []
    repair = {"requested": bool(args.repair_bootstrap), "attempted": False, "succeeded": False, "detail": None}

    try:
        default_exe, default_updater, default_config = _default_paths()
    except RuntimeError as exc:
        default_exe = default_updater = default_config = Path("<unavailable>")
        checks.append(Check("WINDOWS_APPDATA_ENVIRONMENT", False, "COS_INSTALLATION_SURFACE", str(exc)))

    cos_exe = args.cos_exe or default_exe
    cos_updater = args.cos_updater or default_updater
    cos_config = args.cos_config or default_config

    exe_present = cos_exe.is_file()
    checks.append(Check("COS_EXECUTABLE_PRESENT", exe_present, "COS_INSTALLATION_SURFACE", str(cos_exe)))
    observed_version = _powershell_file_version(cos_exe) if exe_present else None
    checks.append(
        Check(
            "COS_VERSION_OBSERVED",
            bool(observed_version),
            "COS_INSTALLATION_SURFACE",
            observed_version or "file version unavailable",
        )
    )
    checks.append(
        Check(
            "COS_UPDATER_PRESENT",
            cos_updater.is_file(),
            "COS_UPDATE_OBSERVABILITY",
            str(cos_updater),
        )
    )

    try:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        contract_ok = (
            contract.get("authority_effect") == "NONE"
            and contract.get("lifecycle_rule", {}).get("cos_version_pinned_by_oleander") is False
            and contract.get("drift_policy", {}).get("block_cos_update") is False
        )
        checks.append(Check("COMPATIBILITY_CONTRACT_VALID", contract_ok, "OLEANDER_COMPATIBILITY_CONTRACT", contract.get("contract_id", "unknown")))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        checks.append(Check("COMPATIBILITY_CONTRACT_VALID", False, "OLEANDER_COMPATIBILITY_CONTRACT", f"{type(exc).__name__}:{exc}"))

    try:
        binder = _load_python(BINDER, "oleander_cos_update_binder")
        config_checks = _config_bootstrap_checks(cos_config, binder, observed_version)
    except Exception as exc:  # import failure is itself bounded integration drift
        binder = None
        config_checks = [Check("COS_CONFIG_PRESENT_AND_PARSEABLE", False, "COS_CONFIG_BOOTSTRAP", f"binder load failed:{type(exc).__name__}:{exc}")]
    checks.extend(config_checks)

    marker_failed = any(c.check_id == "COS_BOOTSTRAP_MARKER_PRESENT" and not c.ok for c in config_checks)
    shape_ok = any(c.check_id == "COS_CONFIG_PRESENT_AND_PARSEABLE" and c.ok for c in config_checks)
    if args.repair_bootstrap and marker_failed and shape_ok and binder is not None:
        repair["attempted"] = True
        ok, detail = _repair_bootstrap(cos_config)
        repair["succeeded"] = ok
        repair["detail"] = detail
        if ok:
            checks = [c for c in checks if c.scope != "COS_CONFIG_BOOTSTRAP"]
            checks.extend(_config_bootstrap_checks(cos_config, binder, observed_version))

    subprocess_checks = [
        ("CHAT_RUNTIME_ENTRY_VALID", "OLEANDER_RUNTIME_ENTRY", [sys.executable, str(ENTRY_VALIDATOR)], "PASS: Chat runtime entry"),
        ("RESOLVER_ADAPTER_SELF_TEST_PASS", "OLEANDER_RESOLVER_RUNTIME", [sys.executable, str(RESOLVER), "--self-test"], None),
        ("RUNTIME_BRIDGE_SELF_TEST_PASS", "OLEANDER_RESOLVER_RUNTIME", [sys.executable, str(RUNTIME_BRIDGE), "--self-test"], None),
        ("CHAT_COS_BRIDGE_SELF_TEST_PASS", "CHAT_COS_LOCAL_BRIDGE", [sys.executable, str(CHAT_COS_BRIDGE), "--self-test"], '"status": "PASS"'),
    ]
    for check_id, scope, command, expected in subprocess_checks:
        ok, detail = _run(command)
        if expected is not None:
            ok = ok and expected in detail
        checks.append(Check(check_id, ok, scope, detail))

    provider_skipped = bool(args.skip_baidu_provider)
    if provider_skipped:
        checks.append(Check("BAIDU_LOCAL_RUNTIME_SKIPPED", True, "BAIDU_LOCAL_ADAPTER", "SKIPPED_BY_EXPLICIT_FLAG"))
    else:
        ok, detail = _run(
            ["powershell.exe", "-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(BAIDU_VERIFY)],
            timeout=240,
        )
        ok = ok and "PASS_LOCAL_COS_CODEX_BAIDU_STORAGE" in detail
        checks.append(Check("BAIDU_LOCAL_RUNTIME_PASS", ok, "BAIDU_LOCAL_ADAPTER", detail))

    failures = [c for c in checks if not c.ok]
    affected = sorted({c.scope for c in failures})
    if failures:
        status = "HOLD_COS_UPDATE_COMPATIBILITY"
    elif provider_skipped:
        status = "PASS_COS_UPDATE_COMPATIBILITY_CORE_ONLY"
    else:
        status = "PASS_COS_UPDATE_COMPATIBILITY"
    proof_scope = (
        "CURRENT_INSTALLED_COS_CORE_SURFACE_ONLY"
        if provider_skipped and not failures
        else "CURRENT_INSTALLED_AND_OBSERVED_COS_SURFACE_ONLY"
    )
    payload = {
        "status": status,
        "proof_scope": proof_scope,
        "cos_version_observed": observed_version,
        "authority_effect": "NONE",
        "cos_update_policy": "DO_NOT_BLOCK_COS_UPDATE",
        "drift_effect": "NONE" if not failures else "HOLD_AFFECTED_OLEANDER_INTEGRATION_ONLY",
        "affected_integrations": affected,
        "baidu_provider_check": "SKIPPED_BY_EXPLICIT_FLAG" if provider_skipped else "EXECUTED",
        "repair": repair,
        "checks": [c.__dict__ for c in checks],
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(status)
        print(f"cos_version_observed={observed_version or 'UNAVAILABLE'}")
        print(f"proof_scope={proof_scope}")
        print("cos_update_policy=DO_NOT_BLOCK_COS_UPDATE")
        print("authority_effect=NONE")
        if provider_skipped:
            print("baidu_provider_check=SKIPPED_BY_EXPLICIT_FLAG")
        if repair["requested"]:
            print(f"repair_bootstrap_attempted={str(repair['attempted']).lower()}")
            print(f"repair_bootstrap_succeeded={str(repair['succeeded']).lower()}")
        if failures:
            print("affected_integrations=" + ",".join(affected))
            for failure in failures:
                detail = failure.detail.replace("\n", " | ")
                print(f"- {failure.check_id} [{failure.scope}]: {detail}")
        else:
            print(f"checks={len(checks)}/{len(checks)} PASS")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
