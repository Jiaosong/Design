#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from oleander_surface_reliability import build_preflight_reliability, routing_allowed


ROOT = Path(__file__).resolve().parents[2]
STATIC_SURFACES_PATH = ROOT / "00-governance" / "runtime" / "OLEANDER_SHARED_EXECUTION_SURFACES_v0.1.json"
LOCAL_RUNTIME_MAX_AGE_HOURS = 24
AUTHORITY_CEILING = "EXECUTION_CAPABILITY_ONLY"

SIDE_EFFECT_RANK = {
    "READ_ONLY": 0,
    "LOCAL_MUTATION": 1,
    "REMOTE_MUTATION": 2,
    "AUTHORITY_MUTATION": 3,
    "RELEASE_MUTATION": 4,
}

CAPABILITY_HINTS: dict[str, set[str]] = {
    "AUTHORITY_READ_WRITE": {"github_connector", "notion_connector"},
    "REPO_SOURCE_MUTATION": {"github_connector"},
    "ASSET_ARCHIVE_DELIVERY": {"google_drive_connector"},
    "NATIVE_PRODUCTION": {
        "blender_shared_runtime",
        "html_css_js_svg_browser_native",
        "drawio_native_diagram_execution",
        "xmind_native_mindmap_execution",
        "oleander_pro_design_toolchain",
        "figma_connector",
    },
    "RUNTIME_READBACK": {
        "chat_on_steroids_local_execution_bridge",
        "html_css_js_svg_browser_native",
        "three_d_viewer",
    },
    "DEPLOYMENT": {"vercel_connector"},
    "HEAVY_EXECUTION": {"chat_on_steroids_local_execution_bridge"},
}


def _workspace_root() -> Path:
    if ROOT.parent.name == ".worktrees":
        return ROOT.parent.parent
    return ROOT


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def _parse_time(raw: Any) -> datetime | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
    except ValueError:
        return None


def _snapshot_state(snapshot: dict[str, Any] | None) -> tuple[str, float | None]:
    if snapshot is None:
        return "MISSING", None
    observed = _parse_time(snapshot.get("snapshot_at"))
    if observed is None:
        return "INVALID_TIMESTAMP", None
    age = max(0.0, (datetime.now(timezone.utc) - observed).total_seconds() / 3600.0)
    return ("FRESH" if age <= LOCAL_RUNTIME_MAX_AGE_HOURS else "STALE"), round(age, 2)


def _provider_id(surface_id: str, row: dict[str, Any]) -> str:
    if surface_id == "chat_on_steroids_local_execution_bridge":
        return "native_cos"
    if surface_id.endswith("_connector"):
        return surface_id.removesuffix("_connector")
    if "runtime" in surface_id:
        return surface_id
    runtime = row.get("runtime")
    if isinstance(runtime, str) and runtime:
        return runtime.split()[0].lower()
    return surface_id


def _native_outputs(row: dict[str, Any]) -> list[str]:
    outputs = row.get("native_outputs")
    if isinstance(outputs, list):
        return [str(x) for x in outputs]
    return []


def _capability_roles(surface_id: str, row: dict[str, Any]) -> list[str]:
    roles: set[str] = set()
    role = row.get("role")
    if isinstance(role, str) and role:
        roles.add(role)
    for capability_role, surface_ids in CAPABILITY_HINTS.items():
        if surface_id in surface_ids:
            roles.add(capability_role)
    for capability in row.get("validated_candidate_capabilities") or []:
        roles.add(str(capability))
    return sorted(roles)


def _mutation_classes(surface_id: str, row: dict[str, Any]) -> list[str]:
    classes = ["READ_ONLY"]
    text = " ".join(
        str(row.get(key) or "")
        for key in ("class", "role", "source_mutation", "runtime")
    ).upper()
    if row.get("machine_local") or "LOCAL" in text or "SHARED_REPO_RUNTIME" in text:
        classes.append("LOCAL_MUTATION")
    if surface_id.endswith("_connector") or "REMOTE" in text or "DEPLOY" in text:
        classes.append("REMOTE_MUTATION")
    # These classes describe transport capability, not authority ownership.
    # The resolver separately requires owner-native gate evidence before it can
    # route an authority/release mutation through these surfaces.
    if surface_id in {"github_connector", "notion_connector"}:
        classes.append("AUTHORITY_MUTATION")
    if surface_id in {"github_connector", "vercel_connector"}:
        classes.append("RELEASE_MUTATION")
    return sorted(set(classes), key=lambda value: SIDE_EFFECT_RANK[value])


def normalize_static_surfaces(static: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    static = static or _load_json(STATIC_SURFACES_PATH)
    result: dict[str, dict[str, Any]] = {}
    for surface_id, raw in (static.get("surfaces") or {}).items():
        if not isinstance(raw, dict):
            continue
        result[surface_id] = {
            "surface_id": surface_id,
            "provider_id": _provider_id(surface_id, raw),
            "surface_class": str(raw.get("class") or "UNCLASSIFIED"),
            "capability_roles": _capability_roles(surface_id, raw),
            "availability": "UNKNOWN",
            "authority_ceiling": AUTHORITY_CEILING,
            "mutation_classes": _mutation_classes(surface_id, raw),
            "external_disclosure": bool(surface_id.endswith("_connector") or "REMOTE" in str(raw.get("class") or "").upper()),
            "native_outputs": _native_outputs(raw),
            "readback_support": str(raw.get("runtime_readback") or "DECLARED_BY_OWNER_OR_RUNTIME_PROBE"),
            "reliability": "UNKNOWN_UNTIL_CURRENT_PROBE",
            "fallback_surface": None,
            "version": str(raw.get("version")) if raw.get("version") is not None else None,
            "observed_at": None,
            "default_production_eligible": bool(raw.get("default_production_eligible", False)),
            "canonical_registry_entry": True,
            "observation_source": "STATIC_CANONICAL_REGISTRY_NOT_LIVENESS",
            "runtime_probe_required": bool(raw.get("runtime_probe_required_per_run", False)),
            "lifecycle_state": raw.get("lifecycle_state"),
            "does_not_prove": ["PROJECT_AUTHORITY", "DESIGN_AUTHORITY", "KNOWLEDGE_AUTHORITY", "PROMOTION"],
        }
    return result


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"


def machine_local_observations(snapshot: dict[str, Any] | None = None) -> dict[str, Any]:
    local_path = _workspace_root() / ".mcp-runtime" / "registry" / "OLEANDER_INTEGRATION_REGISTRY_CURRENT.json"
    if snapshot is None and local_path.is_file():
        snapshot = _load_json(local_path)
    state, age_hours = _snapshot_state(snapshot)
    authority_ceiling = None if snapshot is None else (snapshot.get("registry_identity") or {}).get("authority_ceiling")
    surfaces: list[dict[str, Any]] = []
    if snapshot:
        for row in snapshot.get("cos_mcp_registry") or []:
            if not isinstance(row, dict):
                continue
            ready = bool(row.get("enabled")) and str(row.get("status") or "").lower() == "ready"
            availability = "AVAILABLE" if state == "FRESH" and ready else ("UNAVAILABLE" if state == "FRESH" and not ready else "UNKNOWN")
            name = str(row.get("name") or "unnamed")
            surfaces.append({
                "surface_id": f"cos_mcp:{_slug(name)}",
                "provider_id": "native_cos",
                "surface_class": "DISCOVERED_COS_MCP_SURFACE",
                "capability_roles": ["MCP_TOOL_EXECUTION"],
                "availability": availability,
                "authority_ceiling": AUTHORITY_CEILING,
                "mutation_classes": ["READ_ONLY", "LOCAL_MUTATION", "REMOTE_MUTATION"],
                "external_disclosure": str(row.get("source_kind") or "").lower() == "remote",
                "native_outputs": [],
                "readback_support": "PROVIDER_DECLARED_OR_TOOL_SPECIFIC",
                "reliability": "STALE_OBSERVATION" if state != "FRESH" else "CURRENT_SNAPSHOT_OBSERVATION",
                "fallback_surface": None,
                "version": row.get("version"),
                "observed_at": snapshot.get("snapshot_at"),
                "default_production_eligible": False,
                "canonical_registry_entry": False,
                "observation_source": "MACHINE_LOCAL_RUNTIME_READBACK",
                "tool_count": row.get("tool_count"),
                "does_not_prove": ["CANONICAL_SURFACE_REGISTRATION", "PROJECT_AUTHORITY", "DESIGN_AUTHORITY", "PROMOTION"],
            })
    return {
        "state": state,
        "age_hours": age_hours,
        "snapshot_at": None if snapshot is None else snapshot.get("snapshot_at"),
        "authority_ceiling": authority_ceiling,
        "path": str(local_path),
        "surfaces": surfaces,
    }


def probe_local_baseline() -> dict[str, dict[str, Any]]:
    probes: dict[str, dict[str, Any]] = {}
    for executable in ("git", "python", "node", "npm"):
        resolved = shutil.which(executable)
        probes[executable] = {
            "capability": executable,
            "availability": "AVAILABLE" if resolved else "UNAVAILABLE",
            "resolved_path": resolved,
            "authority_ceiling": AUTHORITY_CEILING,
            "observation_source": "LIVE_LOCAL_PATH_PROBE",
        }
    return probes


def build_current_execution_view(
    *,
    live_observations: dict[str, dict[str, Any]] | None = None,
    local_snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    canonical = normalize_static_surfaces()
    local = machine_local_observations(local_snapshot)
    explicit = live_observations or {}
    for surface_id, observation in explicit.items():
        if surface_id not in canonical:
            canonical[surface_id] = {
                "surface_id": surface_id,
                "provider_id": str(observation.get("provider_id") or "ephemeral"),
                "surface_class": "EPHEMERAL_CURRENT_SURFACE",
                "capability_roles": list(observation.get("capability_roles") or []),
                "authority_ceiling": AUTHORITY_CEILING,
                "mutation_classes": list(observation.get("mutation_classes") or ["READ_ONLY"]),
                "external_disclosure": bool(observation.get("external_disclosure", False)),
                "native_outputs": list(observation.get("native_outputs") or []),
                "readback_support": str(observation.get("readback_support") or "UNKNOWN"),
                "default_production_eligible": False,
                "canonical_registry_entry": False,
                "does_not_prove": ["CANONICAL_SURFACE_REGISTRATION", "PROJECT_AUTHORITY", "PROMOTION"],
            }
        canonical[surface_id].update({
            "availability": str(observation.get("availability") or "UNKNOWN").upper(),
            "version": observation.get("version", canonical[surface_id].get("version")),
            # An explicit live_observations row is itself a current probe
            # generation. Preserve a caller timestamp when supplied; otherwise
            # stamp this observation at admission time for Phase-2 callers.
            "observed_at": observation.get("observed_at") or datetime.now(timezone.utc).isoformat(),
            "reliability": str(observation.get("reliability") or "CURRENT_LIVE_OBSERVATION"),
            "observation_source": str(observation.get("observation_source") or "EXPLICIT_LIVE_PROBE"),
            "reliability_observations": list(observation.get("reliability_observations") or []),
        })

    all_surfaces = list(canonical.values()) + local["surfaces"]
    for surface in all_surfaces:
        surface["reliability_preflight"] = build_preflight_reliability(surface)

    return {
        "schema": "oleander.current-execution-view.v0.1",
        "semantic_class": "CURRENT_EXECUTION_CAPABILITY_VIEW_NOT_PROJECT_AUTHORITY",
        "authority_ceiling": AUTHORITY_CEILING,
        "canonical_registry_ref": str(STATIC_SURFACES_PATH.relative_to(ROOT)).replace("\\", "/"),
        "local_snapshot": local,
        "baseline_live_probe": probe_local_baseline(),
        "surfaces": all_surfaces,
        "selection_rule": "AUTHORITY_SECURITY_THEN_CAPABILITY_DATA_NATIVE_FORMAT_READBACK_THEN_SURFACE_RELIABILITY_THEN_COST_CONVENIENCE",
        "does_not_prove": ["PROJECT_CURRENT", "KNOWLEDGE_AUTHORITY", "DESIGN_KEEP", "PROFESSIONAL_PASS", "PROMOTION"],
    }


def _surface_supports_request(surface: dict[str, Any], request: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    required_roles = {str(x).upper() for x in request.get("required_capability_roles") or []}
    surface_roles = {str(x).upper() for x in surface.get("capability_roles") or []}
    if required_roles and not required_roles.issubset(surface_roles):
        return False, ["CAPABILITY_ROLE_MISMATCH"]

    required_output = request.get("required_native_output")
    native_outputs = {str(x).lower() for x in surface.get("native_outputs") or []}
    if required_output and native_outputs and str(required_output).lower() not in native_outputs:
        return False, ["NATIVE_OUTPUT_MISMATCH"]

    side_effect = str(request.get("side_effect_class") or "READ_ONLY").upper()
    if side_effect not in set(surface.get("mutation_classes") or []):
        return False, ["SIDE_EFFECT_CLASS_UNSUPPORTED"]
    if side_effect == "AUTHORITY_MUTATION" and request.get("authority_transition_authorized") is not True:
        return False, ["AUTHORITY_GATE_NOT_VERIFIED"]
    if side_effect == "RELEASE_MUTATION" and request.get("release_authority_verified") is not True:
        return False, ["RELEASE_AUTHORITY_NOT_VERIFIED"]

    if bool(request.get("require_readback", True)) and str(surface.get("readback_support") or "").upper() in {"", "NONE", "UNSUPPORTED"}:
        return False, ["READBACK_UNSUPPORTED"]
    reasons.append("CAPABILITY_AND_SIDE_EFFECT_MATCH")
    return True, reasons


def resolve_execution_surface(request: dict[str, Any], view: dict[str, Any]) -> dict[str, Any]:
    preferred = [str(x) for x in request.get("candidate_surface_ids") or []]
    required_roles = [str(x) for x in request.get("required_capability_roles") or []]
    if not required_roles and request.get("required_native_output") is None and not preferred:
        return {
            "status": "HOLD_INVALID_CAPABILITY_REQUEST",
            "selected_surface": None,
            "candidate_summary": [],
            "authority_ceiling": AUTHORITY_CEILING,
            "route_is_ephemeral": True,
            "reason": "CAPABILITY_REQUIREMENT_REQUIRED",
            "does_not_prove": ["MUTATION_PERMISSION", "PROJECT_AUTHORITY", "DESIGN_AUTHORITY", "PROMOTION"],
        }
    all_surfaces = [x for x in view.get("surfaces") or [] if isinstance(x, dict)]
    if preferred:
        index = {str(x.get("surface_id")): x for x in all_surfaces}
        all_surfaces = [index[x] for x in preferred if x in index]

    candidates: list[dict[str, Any]] = []
    for surface in all_surfaces:
        supported, reasons = _surface_supports_request(surface, request)
        if not supported:
            continue
        preflight = surface.get("reliability_preflight") or build_preflight_reliability(surface)
        if not routing_allowed(preflight):
            continue
        availability = str(surface.get("availability") or "UNKNOWN").upper()
        score = 0
        if availability == "AVAILABLE":
            score += 100
        elif availability == "DEGRADED":
            score += 50
        elif availability == "UNKNOWN":
            score += 10
        if surface.get("default_production_eligible"):
            score += 20
        side_effect = str(request.get("side_effect_class") or "READ_ONLY").upper()
        score -= SIDE_EFFECT_RANK.get(side_effect, 9)
        if str(surface.get("readback_support") or "").upper() not in {"", "UNKNOWN", "UNSUPPORTED"}:
            score += 5
        if str(preflight.get("status") or "") == "READY":
            score += 15
        elif str(preflight.get("status") or "") == "DEGRADED_READY":
            score += 5
        candidates.append({"surface": surface, "score": score, "reasons": reasons, "reliability_preflight": preflight})

    candidates.sort(key=lambda x: (-x["score"], str(x["surface"].get("surface_id"))))
    verified = [
        x for x in candidates
        if str(x["surface"].get("availability")).upper() in {"AVAILABLE", "DEGRADED"}
        and routing_allowed(x.get("reliability_preflight") or {})
    ]
    selected = verified[0] if verified else None
    return {
        "status": "ROUTED" if selected else "HOLD_NO_VERIFIED_SURFACE",
        "selected_surface": None if selected is None else selected["surface"],
        "candidate_summary": [
            {
                "surface_id": row["surface"].get("surface_id"),
                "availability": row["surface"].get("availability"),
                "reliability_status": (row.get("reliability_preflight") or {}).get("status"),
                "score": row["score"],
                "reasons": row["reasons"],
            }
            for row in candidates
        ],
        "authority_ceiling": AUTHORITY_CEILING,
        "route_is_ephemeral": True,
        "does_not_prove": ["MUTATION_PERMISSION", "PROJECT_AUTHORITY", "DESIGN_AUTHORITY", "PROMOTION"],
    }
