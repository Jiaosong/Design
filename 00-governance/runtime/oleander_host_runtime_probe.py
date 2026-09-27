#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from oleander_environment_resolver import machine_local_observations


ROOT = Path(__file__).resolve().parents[2]
DSH_ADAPTER_PATH = ROOT / "00-governance" / "runtime" / "OLEANDER_DSH_HOST_ADAPTER_v0.1.json"


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def _probe_version(binary: str) -> tuple[str | None, str | None]:
    try:
        result = subprocess.run(
            [binary, "--version"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return None, f"VERSION_PROBE_FAILED:{type(exc).__name__}"
    output = (result.stdout or result.stderr).strip()
    if result.returncode != 0:
        return None, f"VERSION_PROBE_EXIT:{result.returncode}"
    return output or "UNKNOWN_VERSION", None


def probe_dsh_host(binary_override: str | None = None) -> dict[str, Any]:
    adapter = _load_json(DSH_ADAPTER_PATH)
    requested = binary_override or os.environ.get("OLEANDER_DSH_BIN")
    binary = requested if requested else (shutil.which("dsh") or shutil.which("deepseek-harness"))
    if requested and not Path(requested).is_file() and shutil.which(requested) is None:
        binary = None
    if not binary:
        return {
            "host_runtime_id": "dsh_host",
            "host_class": "DSH_HOST",
            "status": "UNAVAILABLE",
            "availability": "UNAVAILABLE",
            "version": None,
            "resolved_binary": None,
            "capabilities": list(adapter.get("required_adapter_behaviors") or []),
            "capabilities_runtime_verified": False,
            "observation_source": "LIVE_BINARY_DISCOVERY",
            "authority_ceiling": "EXECUTION_HOST_AND_SURFACE_LIFECYCLE_ONLY",
            "reason": "DSH_BINARY_NOT_DISCOVERED",
            "does_not_prove": ["DSH_ADOPTED", "PROJECT_CURRENT", "DESIGN_KEEP", "PROMOTION"],
        }
    version, error = _probe_version(binary)
    return {
        "host_runtime_id": "dsh_host",
        "host_class": "DSH_HOST",
        "status": "AVAILABLE" if not error else "DEGRADED",
        "availability": "AVAILABLE" if not error else "DEGRADED",
        "version": version,
        "resolved_binary": binary,
        "capabilities": list(adapter.get("required_adapter_behaviors") or []),
        "capabilities_runtime_verified": False,
        "observation_source": "LIVE_BINARY_AND_VERSION_PROBE",
        "authority_ceiling": "EXECUTION_HOST_AND_SURFACE_LIFECYCLE_ONLY",
        "reason": error,
        "does_not_prove": ["DSH_ADOPTED", "DSH_PRODUCTION_READY", "PROJECT_CURRENT", "DESIGN_KEEP", "PROMOTION"],
    }


def probe_cos_native(local_snapshot: dict[str, Any] | None = None) -> dict[str, Any]:
    local = machine_local_observations(local_snapshot)
    state = str(local.get("state") or "MISSING")
    surfaces = [row for row in local.get("surfaces") or [] if isinstance(row, dict)]
    available_count = sum(1 for row in surfaces if row.get("availability") == "AVAILABLE")
    declared_ready_count = sum(1 for row in surfaces if row.get("declared_ready") is True)
    if state == "FRESH":
        availability = "UNKNOWN" if declared_ready_count else "UNAVAILABLE"
        status = "DISCOVERED_REPROBE_REQUIRED" if declared_ready_count else "UNAVAILABLE"
        reason = (
            "FRESH_REGISTRY_METADATA_REQUIRES_LIVE_CALLABILITY_PROBE"
            if declared_ready_count
            else "FRESH_REGISTRY_WITHOUT_DECLARED_READY_COS_MCP_SURFACE"
        )
    elif state == "STALE":
        availability = "UNKNOWN"
        status = "STALE"
        reason = "STALE_MACHINE_LOCAL_RUNTIME_READBACK_REPROBE_REQUIRED"
    elif state == "MISSING":
        availability = "UNKNOWN"
        status = "UNKNOWN"
        reason = "NO_MACHINE_LOCAL_RUNTIME_READBACK"
    else:
        availability = "UNKNOWN"
        status = state
        reason = "INVALID_MACHINE_LOCAL_RUNTIME_READBACK"
    return {
        "host_runtime_id": "cos_native",
        "host_class": "COS_NATIVE",
        "status": status,
        "availability": availability,
        "version": None,
        "snapshot_at": local.get("snapshot_at"),
        "snapshot_age_hours": local.get("age_hours"),
        "discovered_surface_count": len(surfaces),
        "available_surface_count": available_count,
        "declared_ready_surface_count": declared_ready_count,
        "capabilities": ["LOCAL_FILES", "LOCAL_PROCESS", "MCP_TRANSPORT", "RUNTIME_READBACK"],
        "capabilities_runtime_verified": False,
        "observation_source": "MACHINE_LOCAL_RUNTIME_READBACK",
        "authority_ceiling": "EXECUTION_HOST_AND_SURFACE_LIFECYCLE_ONLY",
        "reason": reason,
        "does_not_prove": ["PROJECT_STATE", "PROJECT_CURRENT", "DESIGN_KEEP", "PROMOTION"],
    }


def build_host_runtime_view(
    *,
    local_host_ready: bool,
    local_snapshot: dict[str, Any] | None = None,
    dsh_binary_override: str | None = None,
) -> dict[str, Any]:
    local_host = {
        "host_runtime_id": "design_system_local_host",
        "host_class": "DESIGN_SYSTEM_LOCAL_HOST",
        "status": "AVAILABLE" if local_host_ready else "UNAVAILABLE",
        "availability": "AVAILABLE" if local_host_ready else "UNAVAILABLE",
        "version": "v0.1",
        "capabilities": ["PROJECT_DISCOVERY", "SOURCE_INGESTION_TRANSPORT", "SURFACE_VIEW_PROJECTION", "RUNTIME_READBACK"],
        "capabilities_runtime_verified": local_host_ready,
        "observation_source": "IN_PROCESS_LOCAL_HOST",
        "authority_ceiling": "EXECUTION_HOST_AND_SURFACE_LIFECYCLE_ONLY",
        "does_not_prove": ["PROJECT_CURRENT", "KNOWLEDGE_CURRENT", "DESIGN_KEEP", "PROMOTION"],
    }
    rows = [local_host, probe_dsh_host(dsh_binary_override), probe_cos_native(local_snapshot)]
    return {
        "schema": "oleander.host-runtime-view.v0.1",
        "semantic_class": "CURRENT_HOST_RUNTIME_OBSERVATION_NOT_PROJECT_STATE",
        "authority_ceiling": "EXECUTION_HOST_AND_SURFACE_LIFECYCLE_ONLY",
        "hosts": rows,
        "count": len(rows),
        "does_not_prove": ["PROVIDER_SELECTION", "PROJECT_CURRENT", "DESIGN_KEEP", "PROMOTION"],
    }
