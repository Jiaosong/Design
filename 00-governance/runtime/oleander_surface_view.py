#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "00-governance" / "runtime" / "OLEANDER_SURFACE_VIEW_CONTRACT_v0.1.json"


def _contract() -> dict[str, Any]:
    value = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("surface view contract must contain one object")
    return value


def _definition_index() -> dict[str, dict[str, Any]]:
    return {
        str(row["surface_definition_id"]): row
        for row in _contract().get("definitions") or []
        if isinstance(row, dict) and row.get("surface_definition_id")
    }


def build_surface_views(current_execution_view: dict[str, Any]) -> dict[str, Any]:
    contract = _contract()
    definitions = _definition_index()
    runtime_rows = {
        str(row.get("surface_id")): row
        for row in current_execution_view.get("surfaces") or []
        if isinstance(row, dict) and row.get("surface_id")
    }

    rows: list[dict[str, Any]] = []
    for surface_id, definition in definitions.items():
        runtime = runtime_rows.get(surface_id)
        rows.append({
            "surface_view_id": f"surface-view:{surface_id}",
            "surface_definition_id": surface_id,
            "display_name": definition["display_name"],
            "view_kind": definition["view_kind"],
            "availability": str((runtime or {}).get("availability") or "UNREGISTERED").upper(),
            "reliability_preflight": (runtime or {}).get("reliability_preflight") or {
                "status": "UNKNOWN",
                "strict_vector": False,
                "stages": {},
                "missing_stages": ["R1_ADMISSION", "R2_IDENTITY", "R3_CAPABILITY", "R4_EXECUTION"],
            },
            "observation_source": (runtime or {}).get("observation_source") or "NO_CURRENT_SURFACE_OBSERVATION",
            "observed_at": (runtime or {}).get("observed_at"),
            "provider_id": (runtime or {}).get("provider_id"),
            "product_actions": list(definition.get("product_actions") or []),
            "authority_ceiling": "UI_PROJECTION_ONLY",
            "runtime_surface_ref": surface_id if runtime is not None else None,
            "does_not_prove": ["SURFACE_READINESS", "PROJECT_CURRENT", "KNOWLEDGE_CURRENT", "DESIGN_KEEP", "PROMOTION"],
        })

    # Runtime-discovered surfaces that do not yet have a curated product view
    # remain visible as generic projections rather than disappearing.
    for surface_id in sorted(set(runtime_rows) - set(definitions)):
        runtime = runtime_rows[surface_id]
        rows.append({
            "surface_view_id": f"surface-view:{surface_id}",
            "surface_definition_id": surface_id,
            "display_name": surface_id,
            "view_kind": "GENERIC_INTEGRATION",
            "availability": str(runtime.get("availability") or "UNKNOWN").upper(),
            "reliability_preflight": runtime.get("reliability_preflight") or {},
            "observation_source": runtime.get("observation_source") or "UNKNOWN_SOURCE",
            "observed_at": runtime.get("observed_at"),
            "provider_id": runtime.get("provider_id"),
            "product_actions": ["OBSERVE"],
            "authority_ceiling": "UI_PROJECTION_ONLY",
            "runtime_surface_ref": surface_id,
            "does_not_prove": ["SURFACE_READINESS", "PROJECT_CURRENT", "KNOWLEDGE_CURRENT", "DESIGN_KEEP", "PROMOTION"],
        })

    return {
        "schema": "oleander.surface-view-projection.v0.1",
        "semantic_class": "CURRENT_UI_PROJECTION_NOT_SURFACE_REGISTRY",
        "authority_ceiling": contract["authority_ceiling"],
        "surface_views": rows,
        "count": len(rows),
        "does_not_prove": contract["does_not_prove"],
    }


def project_browser_profile(*, project_id: str | None = None) -> dict[str, Any]:
    scope = "PROJECT" if project_id else "RESEARCH"
    suffix = project_id or "unbound-research"
    return {
        "browser_profile_id": f"browser-profile:{suffix}",
        "scope": scope,
        "project_id": project_id,
        "credential_boundary": "PROFILE_SCOPED_NOT_PROJECT_AUTHORITY",
        "download_target": "SOURCE_INBOX",
        "capture_target": "SOURCE_INBOX",
        "status": "UNBOUND_PROVIDER",
        "semantic_class": "BROWSER_CONTEXT_PROJECTION_NOT_PROJECT_STATE",
        "does_not_prove": ["PROJECT_STATE", "SOURCE_CAPTURED", "KNOWLEDGE_CURRENT"],
    }
