#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROJECT_BINDING_PATH = ROOT / "00-governance" / "runtime" / "OLEANDER_PROJECT_WORKSPACE_BINDING_v0.1.json"
SOURCE_PIPELINE_PATH = ROOT / "00-governance" / "runtime" / "OLEANDER_SOURCE_INGESTION_PIPELINE_v0.1.json"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one object")
    return value


def _find_forbidden(value: Any, forbidden: set[str], path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            key_lower = str(key).lower()
            child = f"{path}.{key}"
            if key_lower in forbidden:
                hits.append(child)
            hits.extend(_find_forbidden(item, forbidden, child))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hits.extend(_find_forbidden(item, forbidden, f"{path}[{index}]"))
    return hits


def validate_project_workspace_binding(binding: dict[str, Any]) -> dict[str, Any]:
    contract = _load(PROJECT_BINDING_PATH)
    errors: list[str] = []
    for field in contract.get("required_project_fields") or []:
        if binding.get(field) in (None, ""):
            errors.append(f"MISSING:{field}")

    repos = [x for x in binding.get("repositories") or [] if isinstance(x, dict)]
    workspaces = [x for x in binding.get("workspaces") or [] if isinstance(x, dict)]
    repo_refs = [str(x.get("repository_ref") or "") for x in repos]
    if len(repo_refs) != len(set(repo_refs)):
        errors.append("DUPLICATE_REPOSITORY_REF")
    primary_count = sum(1 for x in repos if x.get("role") == "PRIMARY")
    if repos and primary_count != 1:
        errors.append("EXACTLY_ONE_PRIMARY_REPOSITORY_REQUIRED_WHEN_REPOSITORIES_EXIST")

    valid_repo_roles = set(contract.get("repository_roles") or [])
    for row in repos:
        for field in contract.get("repository_binding_required") or []:
            if row.get(field) in (None, ""):
                errors.append(f"REPOSITORY_MISSING:{field}")
        if row.get("role") not in valid_repo_roles:
            errors.append(f"INVALID_REPOSITORY_ROLE:{row.get('role')}")

    valid_workspace_classes = set(contract.get("workspace_classes") or [])
    repo_ref_set = set(repo_refs)
    for row in workspaces:
        for field in contract.get("workspace_binding_required") or []:
            if row.get(field) in (None, ""):
                errors.append(f"WORKSPACE_MISSING:{field}")
        if row.get("workspace_class") not in valid_workspace_classes:
            errors.append(f"INVALID_WORKSPACE_CLASS:{row.get('workspace_class')}")
        if repos and str(row.get("repository_ref") or "") not in repo_ref_set:
            errors.append(f"WORKSPACE_UNKNOWN_REPOSITORY:{row.get('repository_ref')}")

    forbidden = {str(x).lower() for x in contract.get("forbidden_materialization_authority_fields") or []}
    authority_hits = _find_forbidden({"repositories": repos, "workspaces": workspaces}, forbidden)
    if authority_hits:
        errors.extend(f"MATERIALIZATION_AUTHORITY_FIELD:{x}" for x in authority_hits)

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": sorted(set(errors)),
        "project_id": binding.get("project_id"),
        "repository_count": len(repos),
        "workspace_count": len(workspaces),
        "authority_ceiling": contract["authority_ceiling"],
        "does_not_prove": contract["does_not_prove"],
    }


def content_fingerprint(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def admit_source(payload: dict[str, Any]) -> dict[str, Any]:
    contract = _load(SOURCE_PIPELINE_PATH)
    source = dict(payload)
    errors: list[str] = []
    for field in contract.get("admission_required") or []:
        if source.get(field) in (None, ""):
            errors.append(f"MISSING:{field}")
    if source.get("source_kind") not in set(contract.get("source_classes") or []):
        errors.append("UNSUPPORTED_SOURCE_KIND")

    forbidden = {str(x).lower() for x in contract.get("forbidden_output_authority_fields") or []}
    authority_hits = _find_forbidden(source, forbidden)
    if authority_hits:
        errors.extend(f"FORBIDDEN_AUTHORITY_FIELD:{x}" for x in authority_hits)

    if errors:
        return {"status": "FAIL", "errors": sorted(set(errors)), "source": None}
    return {
        "status": "ADMITTED",
        "source": {
            **source,
            "ingestion_state": "ADMITTED",
            "knowledge_current": False,
            "authority_ceiling": contract["authority_ceiling"],
        },
        "next_action": "PRESERVE_ORIGINAL",
        "does_not_prove": contract["does_not_prove"],
    }


def validate_source_revision(source: dict[str, Any], observed_revision: str) -> dict[str, Any]:
    expected = str(source.get("source_revision") or "")
    actual = str(observed_revision or "")
    match = bool(expected) and expected == actual
    return {
        "status": "PASS" if match else "HOLD_SOURCE_CHANGED",
        "expected_revision": expected,
        "observed_revision": actual,
        "derived_body_may_remain_eligible": match,
    }


def next_ingestion_state(current: str, requested: str) -> dict[str, Any]:
    contract = _load(SOURCE_PIPELINE_PATH)
    states = [str(x) for x in contract.get("states") or []]
    if current not in states or requested not in states:
        return {"status": "FAIL", "reason": "UNKNOWN_INGESTION_STATE"}
    current_index = states.index(current)
    requested_index = states.index(requested)
    if requested_index != current_index + 1:
        return {
            "status": "HOLD_INVALID_TRANSITION",
            "reason": "NO_STAGE_SKIPPING_OR_BACKWARD_PROMOTION",
            "allowed_next": states[current_index + 1] if current_index + 1 < len(states) else None,
        }
    return {"status": "PASS", "from": current, "to": requested}


def browser_capture_source(
    *,
    source_id: str,
    url: str,
    capture_ref: str,
    capture_digest: str,
    captured_at: str,
    provenance: dict[str, Any],
) -> dict[str, Any]:
    return admit_source({
        "source_id": source_id,
        "source_kind": "URL",
        "original_ref": url,
        "fingerprint": capture_digest,
        "source_revision": capture_digest,
        "provenance": provenance,
        "capture_ref": capture_ref,
        "captured_at": captured_at,
        "browser_capture": True,
    })
