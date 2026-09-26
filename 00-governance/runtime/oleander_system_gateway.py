#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from oleander_chat_runtime_bridge import run_bridge


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "00-governance" / "runtime" / "OLEANDER_SYSTEM_MANIFEST_v0.1.json"
COS_ADAPTER_PATH = ROOT / "00-governance" / "runtime" / "OLEANDER_COS_HARNESS_ADAPTER_v0.1.json"
STATIC_SURFACES_PATH = ROOT / "00-governance" / "runtime" / "OLEANDER_SHARED_EXECUTION_SURFACES_v0.1.json"
SYSTEM_CONTEXT_SCHEMA = "oleander.system-context-envelope.v0.1"
AUTHORITY_CEILING = "RESOLUTION_CONTEXT_ONLY"
LOCAL_RUNTIME_MAX_AGE_HOURS = 24


def _workspace_root() -> Path:
    if ROOT.parent.name == ".worktrees":
        return ROOT.parent.parent
    return ROOT


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return data


def _repo_rel_exists(ref: str) -> bool:
    if ref.startswith(".mcp-runtime/"):
        return (_workspace_root() / ref).exists()
    candidate = (ROOT / ref).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return False
    return candidate.exists()


def _git(*args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def validate_system_manifest() -> dict[str, Any]:
    manifest = _load_json(MANIFEST_PATH)
    adapter = _load_json(COS_ADAPTER_PATH)
    refs: set[str] = set()

    def collect(value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key in {
                    "root_governance",
                    "master_runtime",
                    "current_architecture_map",
                    "control_graph",
                    "runtime_layer_interface",
                    "implementation",
                    "mcp_server",
                    "provider_contract",
                    "cos_adapter",
                    "static_environment_contract",
                    "static_surface_registry",
                    "system_context_envelope",
                    "runtime_layer",
                    "skill_capability",
                    "tool_adapter",
                    "native_artifact",
                    "execution_receipt",
                    "runtime_provider",
                    "cross_platform_sync",
                } and isinstance(item, str) and ("/" in item or item.startswith(".")):
                    refs.add(item)
                elif key == "owners" and isinstance(item, list):
                    refs.update(x for x in item if isinstance(x, str))
                else:
                    collect(item)
        elif isinstance(value, list):
            for item in value:
                collect(item)

    collect(manifest)
    refs.add(str(COS_ADAPTER_PATH.relative_to(ROOT)).replace("\\", "/"))
    refs.add("00-governance/runtime/OLEANDER_SYSTEM_CONTEXT_ENVELOPE_v0.1.schema.json")
    missing = sorted(ref for ref in refs if not _repo_rel_exists(ref))

    forbidden = {
        "project_state",
        "project_current",
        "source_authority",
        "knowledge_authority",
        "design_decision",
        "design_keep",
        "professional_pass",
        "artifact_current",
        "promotion",
        "release_authority",
    }
    adapter_owns = {str(x).lower() for x in adapter.get("owns") or []}
    forbidden_ownership = sorted(adapter_owns & forbidden)
    runtime_layers = list((manifest.get("architecture") or {}).get("counting_rule", {}).get("runtime_layer_ids") or [])
    expected_layers = [f"R-{chr(code)}" for code in range(ord("A"), ord("K") + 1)]
    checks = {
        "manifest_status_candidate": manifest.get("status") == "CANDIDATE_NON_AUTHORITY",
        "manifest_authority_ceiling": manifest.get("authority_ceiling") == "REFERENCE_AND_RESOLUTION_ONLY",
        "one_architecture": (manifest.get("architecture") or {}).get("counting_rule", {}).get("current_system_architecture") == 1,
        "one_master_runtime": (manifest.get("architecture") or {}).get("counting_rule", {}).get("complex_project_master_runtime") == 1,
        "runtime_layers_exact": runtime_layers == expected_layers,
        "all_canonical_refs_resolve": not missing,
        "cos_authority_ceiling": adapter.get("authority_ceiling") == "EXECUTION_CAPABILITY_AND_OBSERVABILITY_ONLY",
        "cos_forbidden_ownership_absent": not forbidden_ownership,
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "missing_refs": missing,
        "forbidden_cos_ownership": forbidden_ownership,
        "manifest_ref": str(MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/"),
        "cos_adapter_ref": str(COS_ADAPTER_PATH.relative_to(ROOT)).replace("\\", "/"),
    }


def _parse_snapshot_time(raw: Any) -> datetime | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        value = raw.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def environment_snapshot() -> dict[str, Any]:
    static = _load_json(STATIC_SURFACES_PATH)
    local_path = _workspace_root() / ".mcp-runtime" / "registry" / "OLEANDER_INTEGRATION_REGISTRY_CURRENT.json"
    local: dict[str, Any] | None = None
    local_state = "MISSING"
    age_hours: float | None = None
    if local_path.is_file():
        local = _load_json(local_path)
        observed = _parse_snapshot_time(local.get("snapshot_at"))
        if observed is None:
            local_state = "INVALID_TIMESTAMP"
        else:
            age_hours = max(0.0, (datetime.now(timezone.utc) - observed).total_seconds() / 3600.0)
            local_state = "FRESH" if age_hours <= LOCAL_RUNTIME_MAX_AGE_HOURS else "STALE"

    local_surface_summary: list[dict[str, Any]] = []
    if local is not None:
        for row in local.get("cos_mcp_registry") or []:
            if not isinstance(row, dict):
                continue
            local_surface_summary.append({
                "name": row.get("name"),
                "enabled": row.get("enabled"),
                "status": row.get("status"),
                "version": row.get("version"),
                "tool_count": row.get("tool_count"),
            })

    return {
        "semantic_class": "EXECUTION_ENVIRONMENT_OBSERVATION_NOT_AUTHORITY",
        "static_registry_ref": str(STATIC_SURFACES_PATH.relative_to(ROOT)).replace("\\", "/"),
        "static_registry_status": static.get("status"),
        "static_registry_revision": static.get("implementation_revision"),
        "machine_local_runtime_ref": str(local_path),
        "machine_local_runtime_state": local_state,
        "machine_local_snapshot_at": None if local is None else local.get("snapshot_at"),
        "machine_local_age_hours": None if age_hours is None else round(age_hours, 2),
        "machine_local_authority_ceiling": None if local is None else (local.get("registry_identity") or {}).get("authority_ceiling"),
        "machine_local_inventory_summary": {} if local is None else local.get("inventory_summary", {}),
        "machine_local_cos_surfaces": local_surface_summary,
        "selection_rule": "CANONICAL_STATIC_REGISTRY_PLUS_CURRENT_LIVE_PROBE",
        "stale_snapshot_rule": "STALE_MACHINE_LOCAL_READBACK_MAY_INFORM_REPROBE_BUT_MAY_NOT_OVERRIDE_CANONICAL_REGISTRY_OR_PROJECT_AUTHORITY",
    }


def _knowledge_mount_records(payload: dict[str, Any]) -> list[dict[str, Any]]:
    direct = payload.get("knowledge_mount_records")
    if isinstance(direct, list):
        return [x for x in direct if isinstance(x, dict)]
    stage = payload.get("professional_stage_execution")
    if isinstance(stage, dict) and isinstance(stage.get("knowledge_mount_records"), list):
        return [x for x in stage["knowledge_mount_records"] if isinstance(x, dict)]
    return []


def _authority_fingerprint(payload: dict[str, Any]) -> Any:
    direct = payload.get("current_authority_fingerprint")
    if direct is not None:
        return direct
    checkpoint = payload.get("checkpoint")
    return checkpoint.get("authority_fingerprint") if isinstance(checkpoint, dict) else None


def build_system_context(payload: dict[str, Any]) -> dict[str, Any]:
    manifest = _load_json(MANIFEST_PATH)
    environment = environment_snapshot()
    repo_head = _git("rev-parse", "HEAD")
    repo_branch = _git("branch", "--show-current")
    authority = {
        "root_authority_ref": payload.get("root_authority_ref"),
        "project_authority_ref": payload.get("project_authority_ref"),
        "source_authority_ref": payload.get("source_authority_ref"),
        "authority_fingerprint": _authority_fingerprint(payload),
        "resolution_rule": "MISSING_AUTHORITY_FIELDS_REMAIN_UNRESOLVED_AND_MUST_NOT_BE_INFERRED_FROM_CHAT_OR_FILE_LOCATION",
    }
    project = {
        "project_id": payload.get("project_id"),
        "project_state_ref": payload.get("project_state_ref"),
        "current_task_ref": payload.get("current_task_ref"),
        "task_id": payload.get("task_id"),
        "decision_object_id": payload.get("decision_object_id"),
        "state_owner_rule": "OWNER_NATIVE_PROJECT_STATE_ONLY",
    }
    required_native_output = payload.get("required_native_output")
    receipt = payload.get("execution_receipt")
    if required_native_output is None and isinstance(receipt, dict):
        required_native_output = receipt.get("required_native_output")
    artifact = {
        "target_ref": payload.get("target_ref"),
        "required_native_output": required_native_output,
        "native_artifact_contract": manifest["system_interfaces"]["native_artifact"],
        "artifact_existence_is_design_quality": False,
    }
    runtime_provider_id = str(payload.get("runtime_provider_id") or "native_cos")
    return {
        "schema": SYSTEM_CONTEXT_SCHEMA,
        "authority_ceiling": AUTHORITY_CEILING,
        "architecture": {
            "manifest_ref": str(MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/"),
            "current_architecture_map": manifest["architecture"]["current_architecture_map"],
            "master_runtime": manifest["architecture"]["master_runtime"],
            "repo_head": repo_head,
            "repo_branch": repo_branch,
        },
        "authority": authority,
        "project": project,
        "knowledge": {
            "canonical_mount_ref": "00-governance/runtime/OLEANDER_EXISTING_KNOWLEDGE_MOUNT_v1.0.json",
            "mount_records": _knowledge_mount_records(payload),
            "runtime_memory_is_knowledge_authority": False,
        },
        "interfaces": dict(manifest.get("system_interfaces") or {}),
        "environment": environment,
        "runtime": {
            "provider_id": runtime_provider_id,
            "provider_contract": manifest["runtime_providers"]["provider_contract"],
            "cos_adapter": manifest["runtime_providers"]["cos_adapter"] if runtime_provider_id == "native_cos" else None,
            "provider_session_is_project_state": False,
            "provider_event_log_is_project_state": False,
        },
        "artifact": artifact,
        "observability": {
            "authority_ceiling": "OBSERVABILITY_ONLY",
            "local_execution_surface_snapshot_state": environment["machine_local_runtime_state"],
            "execution_receipt_ref": manifest["system_interfaces"]["execution_receipt"],
        },
        "does_not_prove": [
            "project_current",
            "knowledge_correctness",
            "design_decision",
            "artifact_current",
            "design_keep",
            "professional_pass",
            "promotion",
        ],
    }


def run_gateway(payload: dict[str, Any], *, publish_live: bool = True) -> dict[str, Any]:
    validation = validate_system_manifest()
    if validation["status"] != "PASS":
        return {
            "gateway": {
                "status": "HOLD",
                "reason": "SYSTEM_MANIFEST_INVALID",
                "authority_ceiling": AUTHORITY_CEILING,
            },
            "manifest_validation": validation,
        }
    context = build_system_context(payload)
    bridge = run_bridge(payload, publish_live=publish_live)
    return {
        "gateway": {
            "status": "PASS",
            "gateway_id": "oleander_system_gateway_v0.1",
            "authority_ceiling": AUTHORITY_CEILING,
            "changes_project_state": False,
            "changes_knowledge_authority": False,
            "changes_promotion_authority": False,
        },
        "system_context": context,
        "runtime_bridge": bridge,
    }


def run_self_test() -> dict[str, Any]:
    validation = validate_system_manifest()
    if validation["status"] != "PASS":
        raise RuntimeError(f"manifest validation failed: {validation}")
    payload = {
        "intent": "CONTINUE",
        "task_id": "system-gateway-self-test",
        "status": "WORKING",
        "current_authority_fingerprint": "AUTH-SYSTEM-GATEWAY-1",
        "checkpoint": {
            "checkpoint_state": "RESUMABLE",
            "authority_fingerprint": "AUTH-SYSTEM-GATEWAY-1",
            "last_verified_artifact": {
                "artifact_id": "ART-SYSTEM-GATEWAY-1",
                "hash_or_commit": "gateway111",
                "readback_verdict": "PASS"
            },
            "stale_reasons": [],
            "current_node": "ACTUAL_READBACK",
            "resume_from": "ACTUAL_READBACK",
            "next_allowed_action": "NEXT_NODE",
            "checkpoint_sequence": 4,
            "checkpoint_updated_at": "2026-09-26T00:00:00Z",
            "expected_checkpoint_sequence": 4,
            "executor_id": "COS-GATEWAY-SELFTEST",
            "execution_lease_state": "NONE",
            "lease_acquired_at": "NOT_APPLICABLE"
        }
    }
    result = run_gateway(payload, publish_live=False)
    context = result["system_context"]
    if context["project"]["project_id"] is not None:
        raise RuntimeError("gateway self-test: project identity was invented")
    if context["runtime"]["provider_id"] != "native_cos":
        raise RuntimeError("gateway self-test: native_cos default provider missing")
    if context["runtime"]["provider_session_is_project_state"] is not False:
        raise RuntimeError("gateway self-test: provider/session boundary drifted")
    preflight = result["runtime_bridge"]["preflight"]
    if preflight["conversation_directive"]["action"] != "EXECUTE_NEXT_ALLOWED_ACTION":
        raise RuntimeError("gateway self-test: existing resolver decision drifted")
    return {
        "status": "PASS",
        "checks": [
            "SYSTEM_MANIFEST_VALID",
            "NO_PROJECT_ID_INVENTION",
            "COS_SESSION_NOT_PROJECT_STATE",
            "EXISTING_RESOLVER_DECISION_PRESERVED",
            "ENVIRONMENT_READBACK_IS_NON_AUTHORITY"
        ],
        "environment_snapshot_state": context["environment"]["machine_local_runtime_state"]
    }


def _read_payload(path: str | None) -> dict[str, Any]:
    if not path or path == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("input must be one JSON object")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="OLEANDER unified system-management and CoS execution gateway.")
    parser.add_argument("operation", choices=["manifest", "context", "environment", "preflight", "self-test"])
    parser.add_argument("input", nargs="?", help="JSON input file for context/preflight; omit/use '-' for stdin")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--no-publish", action="store_true", help="Disable live observability publication for preflight")
    args = parser.parse_args()

    try:
        if args.operation == "manifest":
            result = {
                "manifest": _load_json(MANIFEST_PATH),
                "validation": validate_system_manifest()
            }
        elif args.operation == "environment":
            result = environment_snapshot()
        elif args.operation == "self-test":
            result = run_self_test()
        elif args.operation == "context":
            result = build_system_context(_read_payload(args.input))
        else:
            result = run_gateway(_read_payload(args.input), publish_live=not args.no_publish)
    except (OSError, ValueError, KeyError, json.JSONDecodeError, RuntimeError) as exc:
        print(json.dumps({"error": "OLEANDER_SYSTEM_GATEWAY_ERROR", "detail": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2) from exc

    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=args.pretty))


if __name__ == "__main__":
    main()
