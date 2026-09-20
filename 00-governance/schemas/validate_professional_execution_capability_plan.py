#!/usr/bin/env python3
"""Fail-closed semantic validation for OLEANDER professional execution capability plans."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / "professional-execution-capability-plan.v1.schema.json"

EXECUTABLE_MODES = {
    "AGENT_EXECUTABLE",
    "SHARED_RUNTIME_EXECUTABLE",
    "PROJECT_SPECIALIST_BOUND",
}
VALID_AUTHORITIES = {
    "CURRENT_OWNER",
    "PROJECT_AUTHORIZED_SPECIALIST",
}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return data


def schema_errors(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    schema = load_json(SCHEMA)
    for key in schema.get("required", []):
        if key not in payload:
            errors.append(f"missing required field: {key}")
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return errors
    validator = jsonschema.Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(payload), key=lambda e: list(e.path)):
        where = ".".join(str(x) for x in error.path) or "$"
        errors.append(f"schema {where}: {error.message}")
    return errors


def validate_payload(payload: dict[str, Any]) -> list[str]:
    errors = schema_errors(payload)
    rows = payload.get("capabilities") or []
    seen: set[str] = set()
    blocking = set(payload.get("blocking_capability_ids") or [])

    for row in rows:
        if not isinstance(row, dict):
            errors.append("capabilities entries must be objects")
            continue
        cid = row.get("capability_id")
        if isinstance(cid, str):
            if cid in seen:
                errors.append(f"duplicate capability_id: {cid}")
            seen.add(cid)

        if not row.get("in_claim"):
            continue

        mode = row.get("execution_mode")
        authority = row.get("authority_state")
        availability = row.get("availability_state")

        if mode in {"AGENT_EXECUTABLE", "SHARED_RUNTIME_EXECUTABLE"}:
            if authority != "CURRENT_OWNER":
                errors.append(f"{cid}: executable runtime requires CURRENT_OWNER")
            if availability not in {"AVAILABLE", "DEGRADED"}:
                errors.append(f"{cid}: executable runtime requires observed AVAILABLE/DEGRADED availability")
            if not row.get("selected_owner_ref"):
                errors.append(f"{cid}: executable runtime requires selected_owner_ref")
            if not row.get("execution_surface_ref"):
                errors.append(f"{cid}: executable runtime requires execution_surface_ref")
            if not row.get("actual_readback_method"):
                errors.append(f"{cid}: executable runtime requires actual_readback_method")

        if mode == "PROJECT_SPECIALIST_BOUND":
            if authority != "PROJECT_AUTHORIZED_SPECIALIST":
                errors.append(f"{cid}: specialist-bound execution requires PROJECT_AUTHORIZED_SPECIALIST")
            if availability not in {"AVAILABLE", "DEGRADED"}:
                errors.append(f"{cid}: specialist-bound execution requires AVAILABLE/DEGRADED binding")
            if not row.get("selected_owner_ref"):
                errors.append(f"{cid}: specialist-bound execution requires selected_owner_ref")
            if not row.get("specialist_binding_ref"):
                errors.append(f"{cid}: specialist-bound execution requires current PROJECT_SPECIALIST_OWNER_BINDING ref")
            if not row.get("actual_readback_method"):
                errors.append(f"{cid}: specialist-bound execution requires actual_readback_method")

        if mode == "CANDIDATE_ONLY" and authority != "CANDIDATE_OWNER":
            errors.append(f"{cid}: CANDIDATE_ONLY must declare CANDIDATE_OWNER")
        if mode == "CAPABILITY_HOLD" and authority in VALID_AUTHORITIES and availability == "AVAILABLE":
            errors.append(f"{cid}: CAPABILITY_HOLD contradicts an available authorized owner; resolve mode")

        if row.get("independent_review_required") and not row.get("independent_review_owner_ref"):
            # The plan may still be PARTIAL/HOLD, but an EXECUTABLE plan cannot hide this.
            if payload.get("plan_verdict") == "EXECUTABLE":
                errors.append(f"{cid}: EXECUTABLE plan requires independent_review_owner_ref when review is required")

    unknown_blockers = blocking - seen
    if unknown_blockers:
        errors.append(f"blocking_capability_ids reference unknown IDs: {sorted(unknown_blockers)}")

    if payload.get("plan_verdict") == "EXECUTABLE":
        if payload.get("stale"):
            errors.append("EXECUTABLE plan cannot be stale")
        if blocking:
            errors.append("EXECUTABLE plan requires empty blocking_capability_ids")
        for row in rows:
            if not isinstance(row, dict) or not row.get("in_claim"):
                continue
            if row.get("execution_mode") not in EXECUTABLE_MODES:
                errors.append(
                    f"{row.get('capability_id')}: EXECUTABLE plan contains non-executable in-claim mode "
                    f"{row.get('execution_mode')!r}"
                )
            if row.get("authority_state") not in VALID_AUTHORITIES:
                errors.append(
                    f"{row.get('capability_id')}: EXECUTABLE plan lacks Current/specialist authority"
                )

    if payload.get("plan_verdict") == "HOLD" and not blocking:
        errors.append("HOLD plan requires at least one blocking_capability_id")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_professional_execution_capability_plan.py PLAN.json", file=sys.stderr)
        return 2
    payload = load_json(Path(sys.argv[1]))
    errors = validate_payload(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
