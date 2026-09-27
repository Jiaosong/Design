#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from typing import Any


TIMESTAMP_REQUIREMENTS = {"NONE", "CHUNK_INTERVAL", "SEGMENT", "WORD"}
PROVIDER_LOCATIONS = {"HOST_LOCAL", "CLOUD"}


def validate_transcription_provider(provider: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "provider_id",
        "location",
        "languages",
        "max_audio_seconds",
        "timestamp_capabilities",
        "preparation_state",
        "authority_ceiling",
    }
    for field in sorted(required):
        if provider.get(field) in (None, ""):
            errors.append(f"MISSING:{field}")
    if provider.get("location") not in PROVIDER_LOCATIONS:
        errors.append("INVALID_PROVIDER_LOCATION")
    if provider.get("authority_ceiling") != "EXECUTION_CAPABILITY_ONLY":
        errors.append("INVALID_PROVIDER_AUTHORITY_CEILING")
    timestamp_caps = {str(x) for x in provider.get("timestamp_capabilities") or []}
    if not timestamp_caps or not timestamp_caps.issubset(TIMESTAMP_REQUIREMENTS):
        errors.append("INVALID_TIMESTAMP_CAPABILITIES")
    try:
        max_audio_seconds = float(provider.get("max_audio_seconds"))
    except (TypeError, ValueError):
        max_audio_seconds = 0.0
    if max_audio_seconds <= 0:
        errors.append("INVALID_MAX_AUDIO_SECONDS")
    return sorted(set(errors))


def build_transcription_plan(
    *,
    source: dict[str, Any],
    media: dict[str, Any] | None,
    provider: dict[str, Any] | None,
    language: str = "auto",
    timestamp_requirement: str = "CHUNK_INTERVAL",
) -> dict[str, Any]:
    source_id = str(source.get("source_id") or "")
    source_revision = str(source.get("source_revision") or "")
    if source.get("source_kind") not in {"VIDEO", "AUDIO"}:
        return {"status": "BLOCKED", "reason": "SOURCE_KIND_NOT_TRANSCRIBABLE"}
    if not media or media.get("status") != "MEDIA_SUPPORT_READY":
        return {"status": "BLOCKED", "reason": "MEDIA_SUPPORT_NOT_READY"}
    if media.get("source_id") not in {None, source_id} or media.get("source_revision") not in {None, source_revision}:
        return {"status": "HOLD_SOURCE_CHANGED", "reason": "MEDIA_SOURCE_BINDING_MISMATCH"}
    requested = str(timestamp_requirement or "CHUNK_INTERVAL")
    if requested not in TIMESTAMP_REQUIREMENTS:
        return {"status": "BLOCKED", "reason": "INVALID_TIMESTAMP_REQUIREMENT"}
    media_ref = str(media.get("media_ref") or "media.json")
    request_id = "TRQ-" + hashlib.sha256(f"{source_id}:{source_revision}:{media_ref}:{language}:{requested}".encode("utf-8")).hexdigest()[:24]
    if provider is None:
        return {
            "status": "TRANSCRIPT_PROVIDER_NOT_BOUND",
            "request_id": request_id,
            "source_id": source_id,
            "source_revision": source_revision,
            "media_ref": media_ref,
            "language": language,
            "timestamp_requirement": requested,
            "does_not_prove": ["TRANSCRIPT_AVAILABLE", "KNOWLEDGE_CURRENT", "CLAIM_CORRECTNESS"],
        }

    provider_errors = validate_transcription_provider(provider)
    if provider_errors:
        return {
            "status": "BLOCKED",
            "reason": "INVALID_TRANSCRIPTION_PROVIDER",
            "provider_errors": provider_errors,
            "request_id": request_id,
        }
    if str(provider.get("preparation_state") or "") != "READY":
        return {
            "status": "PROVIDER_PREPARATION_REQUIRED",
            "request_id": request_id,
            "source_id": source_id,
            "source_revision": source_revision,
            "media_ref": media_ref,
            "provider_id": provider.get("provider_id"),
            "provider_location": provider.get("location"),
            "language": language,
            "timestamp_requirement": requested,
            "does_not_prove": ["TRANSCRIPT_AVAILABLE", "KNOWLEDGE_CURRENT", "CLAIM_CORRECTNESS"],
        }

    try:
        duration = float(media.get("duration_seconds")) if media.get("duration_seconds") is not None else None
        max_audio_seconds = float(provider.get("max_audio_seconds"))
    except (TypeError, ValueError):
        duration = None
        max_audio_seconds = 0.0
    if duration is not None and max_audio_seconds > 0 and duration > max_audio_seconds:
        return {
            "status": "BLOCKED",
            "reason": "SOURCE_DURATION_EXCEEDS_PROVIDER_LIMIT",
            "request_id": request_id,
            "duration_seconds": duration,
            "max_audio_seconds": max_audio_seconds,
        }

    timestamp_caps = {str(x) for x in provider.get("timestamp_capabilities") or []}
    if requested not in timestamp_caps:
        if "CHUNK_INTERVAL" not in timestamp_caps:
            return {
                "status": "BLOCKED",
                "reason": "PROVIDER_TIMESTAMP_REQUIREMENT_UNSATISFIED",
                "request_id": request_id,
            }
        requested = "CHUNK_INTERVAL"
    return {
        "status": "READY",
        "request_id": request_id,
        "source_id": source_id,
        "source_revision": source_revision,
        "media_ref": media_ref,
        "provider_id": provider.get("provider_id"),
        "provider_location": provider.get("location"),
        "language": language,
        "timestamp_requirement": requested,
        "max_audio_seconds": provider.get("max_audio_seconds"),
        "rule": "SOURCE_REVISION_RECHECK_REQUIRED_BEFORE_AUDIO_PREPARATION_AND_TRANSCRIPT_COMMIT",
        "does_not_prove": ["TRANSCRIPT_AVAILABLE", "KNOWLEDGE_CURRENT", "CLAIM_CORRECTNESS"],
    }


def build_persistent_transcription_request(plan: dict[str, Any], *, requested_at: str) -> dict[str, Any]:
    state = str(plan.get("status") or "")
    if state not in {"TRANSCRIPT_PROVIDER_NOT_BOUND", "PROVIDER_PREPARATION_REQUIRED", "READY"}:
        raise ValueError("TRANSCRIPTION_PLAN_NOT_PERSISTABLE")
    required = ("request_id", "source_id", "source_revision", "media_ref", "language", "timestamp_requirement")
    missing = [field for field in required if plan.get(field) in (None, "")]
    if missing:
        raise ValueError("TRANSCRIPTION_PLAN_MISSING:" + ",".join(missing))
    request = {
        "schema": "oleander.source-transcription-request.v0.1",
        "request_id": plan["request_id"],
        "source_id": plan["source_id"],
        "source_revision": plan["source_revision"],
        "media_ref": plan["media_ref"],
        "language": plan["language"],
        "timestamp_requirement": plan["timestamp_requirement"],
        "state": state,
        "requested_at": requested_at,
        "provider_id": plan.get("provider_id"),
        "provider_location": plan.get("provider_location"),
        "authority_ceiling": "SOURCE_TRANSCRIPTION_DERIVATIVE_ONLY",
        "semantic_class": "PERSISTENT_SOURCE_TRANSCRIPTION_REQUEST_NOT_TRANSCRIPT",
        "does_not_prove": ["PROVIDER_BOUND", "TRANSCRIPT_AVAILABLE", "KNOWLEDGE_CURRENT", "CLAIM_CORRECTNESS"],
    }
    return request


def validate_persistent_transcription_request(request: dict[str, Any], source: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = ("request_id", "source_id", "source_revision", "media_ref", "language", "timestamp_requirement", "state", "requested_at")
    for field in required:
        if request.get(field) in (None, ""):
            errors.append(f"MISSING:{field}")
    if request.get("source_id") != source.get("source_id"):
        errors.append("SOURCE_ID_MISMATCH")
    if request.get("source_revision") != source.get("source_revision"):
        errors.append("SOURCE_REVISION_MISMATCH")
    if request.get("timestamp_requirement") not in TIMESTAMP_REQUIREMENTS:
        errors.append("INVALID_TIMESTAMP_REQUIREMENT")
    if request.get("authority_ceiling") != "SOURCE_TRANSCRIPTION_DERIVATIVE_ONLY":
        errors.append("INVALID_AUTHORITY_CEILING")
    if request.get("state") not in {"TRANSCRIPT_PROVIDER_NOT_BOUND", "PROVIDER_PREPARATION_REQUIRED", "READY"}:
        errors.append("INVALID_REQUEST_STATE")
    return sorted(set(errors))
