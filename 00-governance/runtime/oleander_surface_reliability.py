#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "00-governance" / "runtime" / "OLEANDER_SURFACE_RELIABILITY_BOUNDARY_v0.1.json"

PREFLIGHT_STAGES = ("R1_ADMISSION", "R2_IDENTITY", "R3_CAPABILITY", "R4_EXECUTION")
POST_EXECUTION_STAGE = "R5_RESULT"
TERMINAL_BLOCKING_FACTS = {"FAIL", "BLOCKED", "STALE"}
PASS_FACTS = {"PASS", "NOT_APPLICABLE"}
MAX_OBSERVATION_AGE = timedelta(hours=24)
MAX_FUTURE_SKEW = timedelta(minutes=5)


def _load_contract() -> dict[str, Any]:
    value = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("surface reliability contract must contain one object")
    return value


def _parse_observed_at(raw: Any) -> datetime | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _timestamp_freshness(raw: Any) -> tuple[str, float | None]:
    observed = _parse_observed_at(raw)
    if observed is None:
        return "INVALID", None
    now = datetime.now(timezone.utc)
    delta = now - observed
    if delta < -MAX_FUTURE_SKEW:
        return "FUTURE", round(delta.total_seconds() / 3600.0, 3)
    if delta > MAX_OBSERVATION_AGE:
        return "STALE", round(delta.total_seconds() / 3600.0, 3)
    return "FRESH", round(max(0.0, delta.total_seconds()) / 3600.0, 3)


def validate_reliability_observation(observation: dict[str, Any]) -> list[str]:
    contract = _load_contract()
    schema = contract.get("observation_schema") or {}
    errors: list[str] = []
    for field in schema.get("required") or []:
        if observation.get(field) in (None, ""):
            errors.append(f"MISSING:{field}")

    stage = str(observation.get("stage") or "")
    dimension = str(observation.get("dimension") or "")
    stages = contract.get("stages") or {}
    if stage not in stages:
        errors.append("UNKNOWN_STAGE")
    elif dimension not in set((stages.get(stage) or {}).get("required_dimensions") or []):
        errors.append("UNKNOWN_DIMENSION_FOR_STAGE")

    if str(observation.get("source_kind") or "") not in set(schema.get("source_kinds") or []):
        errors.append("UNKNOWN_SOURCE_KIND")
    if str(observation.get("fact") or "") not in set(schema.get("fact_values") or []):
        errors.append("UNKNOWN_FACT")
    freshness, _age_hours = _timestamp_freshness(observation.get("observed_at"))
    if freshness == "INVALID":
        errors.append("INVALID_OBSERVED_AT")
    elif freshness == "FUTURE":
        errors.append("FUTURE_OBSERVATION")
    elif freshness == "STALE":
        errors.append("STALE_OBSERVATION")
    return errors


def _strict_stage_state(stage: str, observations: list[dict[str, Any]]) -> dict[str, Any]:
    contract = _load_contract()
    stage_contract = (contract.get("stages") or {}).get(stage) or {}
    required = [str(x) for x in stage_contract.get("required_dimensions") or []]
    by_dimension: dict[str, dict[str, Any]] = {}
    invalid: list[dict[str, Any]] = []

    for observation in observations:
        if str(observation.get("stage") or "") != stage:
            continue
        errors = validate_reliability_observation(observation)
        if errors:
            invalid.append({"observation_id": observation.get("observation_id"), "errors": errors})
            continue
        by_dimension[str(observation["dimension"])] = observation

    missing = [dimension for dimension in required if dimension not in by_dimension]
    facts = {dimension: str(row.get("fact") or "UNKNOWN") for dimension, row in by_dimension.items()}
    if invalid:
        state = "INVALID"
    elif any(fact in TERMINAL_BLOCKING_FACTS for fact in facts.values()):
        state = "BLOCKED"
    elif missing:
        state = "UNKNOWN"
    elif all(fact in PASS_FACTS for fact in facts.values()):
        state = "PASS"
    elif stage == "R4_EXECUTION" and all(fact in PASS_FACTS | {"DEGRADED"} for fact in facts.values()):
        state = "DEGRADED"
    else:
        state = "UNKNOWN"
    return {
        "stage": stage,
        "state": state,
        "required_dimensions": required,
        "facts": facts,
        "missing_dimensions": missing,
        "invalid_observations": invalid,
        "observation_refs": [str(x.get("observation_id")) for x in by_dimension.values()],
    }


def _compatibility_preflight(surface: dict[str, Any]) -> dict[str, Any] | None:
    """Bridge Phase-2 current probes until every surface emits R1-R4 observations.

    This bridge never produces VERIFIED and never fabricates R5. It requires a
    current runtime observation (`availability` plus `observed_at`) and remains
    explicitly marked as compatibility evidence so callers can migrate to the
    strict vector without breaking the existing resolver in one step.
    """
    availability = str(surface.get("availability") or "UNKNOWN").upper()
    observed_at = surface.get("observed_at")
    source = str(surface.get("observation_source") or "")
    if availability not in {"AVAILABLE", "DEGRADED"} or not observed_at:
        return None
    if source in {"STATIC_CANONICAL_REGISTRY_NOT_LIVENESS", ""}:
        return None
    freshness, age_hours = _timestamp_freshness(observed_at)
    if freshness != "FRESH":
        return {
            "status": "STALE" if freshness == "STALE" else "UNKNOWN",
            "strict_vector": False,
            "source": source,
            "observed_at": observed_at,
            "observation_freshness": freshness,
            "observation_age_hours": age_hours,
            "stages": {},
            "missing_stages": list(PREFLIGHT_STAGES),
            "rule": "COMPATIBILITY_EVIDENCE_MUST_BE_CURRENT_BEFORE_ROUTING",
            "does_not_prove": ["R5_RESULT", "PROJECT_CURRENT", "DESIGN_KEEP", "KNOWLEDGE_CURRENT", "PROMOTION"],
        }
    return {
        "status": "COMPATIBILITY_READY" if availability == "AVAILABLE" else "COMPATIBILITY_DEGRADED",
        "strict_vector": False,
        "source": source,
        "observed_at": observed_at,
        "observation_freshness": freshness,
        "observation_age_hours": age_hours,
        "stages": {},
        "missing_stages": list(PREFLIGHT_STAGES),
        "rule": "CURRENT_PHASE2_PROBE_BRIDGE_ONLY_MIGRATE_TO_R1_R4_OBSERVATIONS",
        "does_not_prove": ["R5_RESULT", "PROJECT_CURRENT", "DESIGN_KEEP", "KNOWLEDGE_CURRENT", "PROMOTION"],
    }


def build_preflight_reliability(surface: dict[str, Any]) -> dict[str, Any]:
    observations = [x for x in surface.get("reliability_observations") or [] if isinstance(x, dict)]
    if not observations:
        compatibility = _compatibility_preflight(surface)
        if compatibility is not None:
            return compatibility
        return {
            "status": "UNKNOWN",
            "strict_vector": False,
            "stages": {},
            "missing_stages": list(PREFLIGHT_STAGES),
            "does_not_prove": ["R5_RESULT", "PROJECT_CURRENT", "DESIGN_KEEP", "KNOWLEDGE_CURRENT", "PROMOTION"],
        }

    stages = {stage: _strict_stage_state(stage, observations) for stage in PREFLIGHT_STAGES}
    states = {stage: row["state"] for stage, row in stages.items()}
    if any(state in {"BLOCKED", "INVALID"} for state in states.values()):
        status = "BLOCKED"
    elif all(states[stage] == "PASS" for stage in ("R1_ADMISSION", "R2_IDENTITY", "R3_CAPABILITY")) and states["R4_EXECUTION"] in {"PASS", "DEGRADED"}:
        status = "READY" if states["R4_EXECUTION"] == "PASS" else "DEGRADED_READY"
    else:
        status = "UNKNOWN"
    return {
        "status": status,
        "strict_vector": True,
        "stages": stages,
        "missing_stages": [stage for stage, row in stages.items() if row["state"] == "UNKNOWN"],
        "does_not_prove": ["R5_RESULT", "PROJECT_CURRENT", "DESIGN_KEEP", "KNOWLEDGE_CURRENT", "PROMOTION"],
    }


def assess_result_reliability(observations: list[dict[str, Any]], *, material_mutation: bool = True) -> dict[str, Any]:
    rows = [x for x in observations if isinstance(x, dict)]
    stage = _strict_stage_state(POST_EXECUTION_STAGE, rows)
    status = "VERIFIED" if stage["state"] == "PASS" else ("BLOCKED" if stage["state"] in {"BLOCKED", "INVALID"} else "PARTIAL")
    if material_mutation and stage["state"] != "PASS":
        status = "PARTIAL"
    return {
        "status": status,
        "stage": stage,
        "material_mutation": material_mutation,
        "authority_ceiling": "EXECUTION_RELIABILITY_EVIDENCE_ONLY",
        "does_not_prove": ["PROJECT_CURRENT", "DESIGN_KEEP", "KNOWLEDGE_CURRENT", "PROFESSIONAL_PASS", "PROMOTION"],
    }


def identity_revision_changed(previous: dict[str, Any], current: dict[str, Any]) -> bool:
    return (
        str(previous.get("surface_identity_id") or "") != str(current.get("surface_identity_id") or "")
        or str(previous.get("identity_revision") or "") != str(current.get("identity_revision") or "")
    )


def routing_allowed(preflight: dict[str, Any]) -> bool:
    return str(preflight.get("status") or "") in {
        "READY",
        "DEGRADED_READY",
        "COMPATIBILITY_READY",
        "COMPATIBILITY_DEGRADED",
    }
