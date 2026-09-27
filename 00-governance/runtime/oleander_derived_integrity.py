#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


MANIFEST_NAME = "derived_manifest.json"


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            while True:
                block = handle.read(1024 * 1024)
                if not block:
                    break
                digest.update(block)
    except OSError:
        return None
    return "sha256:" + digest.hexdigest()


def _artifact_id(kind: str, ref: str) -> str:
    return hashlib.sha256(f"{kind}:{ref}".encode("utf-8")).hexdigest()[:24]


def build_manifest(source_dir: Path, source: dict[str, Any]) -> dict[str, Any]:
    source_id = str(source.get("source_id") or "")
    source_revision = str(source.get("source_revision") or "")
    specs: list[tuple[str, Path]] = []
    fixed = [
        ("STRUCTURED_BODY", source_dir / "body.json"),
        ("KNOWLEDGE_DRAFT", source_dir / "knowledge_draft.json"),
        ("MEDIA_METADATA", source_dir / "media.json"),
        ("TRANSCRIPT", source_dir / "transcript.json"),
    ]
    specs.extend((kind, path) for kind, path in fixed if path.is_file())
    for path in sorted((source_dir / "derived" / "keyframes").glob("*")) if (source_dir / "derived" / "keyframes").is_dir() else []:
        if path.is_file():
            specs.append(("KEYFRAME", path))
    for path in sorted((source_dir / "derived" / "transcription-audio").glob("*.wav")) if (source_dir / "derived" / "transcription-audio").is_dir() else []:
        if path.is_file():
            specs.append(("TRANSCRIPTION_AUDIO", path))

    artifacts: list[dict[str, Any]] = []
    for kind, path in specs:
        digest = sha256_file(path)
        if digest is None:
            continue
        ref = str(path.relative_to(source_dir)).replace("\\", "/")
        artifacts.append({
            "artifact_id": _artifact_id(kind, ref),
            "kind": kind,
            "ref": ref,
            "sha256": digest,
            "source_revision": source_revision,
        })
    return {
        "schema": "oleander.derived-artifact-manifest.v0.1",
        "source_id": source_id,
        "source_revision": source_revision,
        "artifacts": artifacts,
        "semantic_class": "DERIVED_ARTIFACT_INTEGRITY_NOT_KNOWLEDGE_AUTHORITY",
        "does_not_prove": ["KNOWLEDGE_CURRENT", "CLAIM_CORRECTNESS", "KI_PASS", "OE_PASS", "DESIGN_KEEP", "PROMOTION"],
    }


def write_manifest(source_dir: Path, source: dict[str, Any]) -> dict[str, Any]:
    manifest = build_manifest(source_dir, source)
    path = source_dir / MANIFEST_NAME
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    return manifest


def validate_manifest(source_dir: Path, source: dict[str, Any]) -> dict[str, Any]:
    path = source_dir / MANIFEST_NAME
    if not path.is_file():
        return {
            "status": "UNVERIFIED_DERIVED",
            "reason": "DERIVED_MANIFEST_MISSING",
            "derived_content_may_be_exposed": False,
            "artifacts": [],
        }
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            "status": "HOLD_DERIVED_CHANGED",
            "reason": "DERIVED_MANIFEST_INVALID",
            "derived_content_may_be_exposed": False,
            "artifacts": [],
        }
    if not isinstance(manifest, dict):
        return {
            "status": "HOLD_DERIVED_CHANGED",
            "reason": "DERIVED_MANIFEST_INVALID",
            "derived_content_may_be_exposed": False,
            "artifacts": [],
        }
    observed_manifest_revision = sha256_file(path)
    expected_manifest_revision = source.get("derived_manifest_revision")
    if not isinstance(expected_manifest_revision, str) or not expected_manifest_revision:
        return {
            "status": "UNVERIFIED_DERIVED",
            "reason": "DERIVED_MANIFEST_REVISION_NOT_BOUND_TO_SOURCE_METADATA",
            "derived_content_may_be_exposed": False,
            "manifest_revision": observed_manifest_revision,
            "artifacts": [],
        }
    if observed_manifest_revision != expected_manifest_revision:
        return {
            "status": "HOLD_DERIVED_CHANGED",
            "reason": "DERIVED_MANIFEST_DIGEST_MISMATCH",
            "derived_content_may_be_exposed": False,
            "expected_manifest_revision": expected_manifest_revision,
            "observed_manifest_revision": observed_manifest_revision,
            "artifacts": [],
        }
    if manifest.get("source_id") != source.get("source_id") or manifest.get("source_revision") != source.get("source_revision"):
        return {
            "status": "HOLD_DERIVED_CHANGED",
            "reason": "DERIVED_MANIFEST_SOURCE_BINDING_MISMATCH",
            "derived_content_may_be_exposed": False,
            "artifacts": [],
        }

    rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for artifact in manifest.get("artifacts") or []:
        if not isinstance(artifact, dict):
            failures.append({"reason": "INVALID_ARTIFACT_RECORD"})
            continue
        ref = str(artifact.get("ref") or "")
        candidate = (source_dir / ref).resolve()
        try:
            candidate.relative_to(source_dir.resolve())
        except ValueError:
            failures.append({"ref": ref, "reason": "DERIVED_REF_ESCAPES_SOURCE_DIR"})
            continue
        observed = sha256_file(candidate)
        expected = artifact.get("sha256")
        semantic_errors: list[str] = []
        if artifact.get("source_revision") != source.get("source_revision"):
            semantic_errors.append("ARTIFACT_MANIFEST_SOURCE_REVISION_MISMATCH")
        kind = str(artifact.get("kind") or "")
        if kind in {"STRUCTURED_BODY", "KNOWLEDGE_DRAFT", "MEDIA_METADATA", "TRANSCRIPT"} and candidate.is_file():
            try:
                payload = json.loads(candidate.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                semantic_errors.append("DERIVED_JSON_INVALID")
            else:
                if not isinstance(payload, dict):
                    semantic_errors.append("DERIVED_JSON_NOT_OBJECT")
                else:
                    if payload.get("source_id") != source.get("source_id"):
                        semantic_errors.append("DERIVED_SOURCE_ID_MISMATCH")
                    if payload.get("source_revision") != source.get("source_revision"):
                        semantic_errors.append("DERIVED_SOURCE_REVISION_MISMATCH")
        row = {
            "artifact_id": artifact.get("artifact_id"),
            "kind": artifact.get("kind"),
            "ref": ref,
            "expected_sha256": expected,
            "observed_sha256": observed,
            "semantic_errors": semantic_errors,
            "status": "PASS" if observed is not None and observed == expected and not semantic_errors else "FAIL",
        }
        rows.append(row)
        if row["status"] != "PASS":
            failures.append(row)
    status = "PASS" if not failures else "HOLD_DERIVED_CHANGED"
    return {
        "status": status,
        "reason": None if status == "PASS" else "DERIVED_ARTIFACT_DIGEST_MISMATCH_OR_MISSING",
        "derived_content_may_be_exposed": status == "PASS",
        "artifacts": rows,
        "failures": failures,
        "does_not_prove": ["KNOWLEDGE_CURRENT", "CLAIM_CORRECTNESS", "KI_PASS", "OE_PASS", "DESIGN_KEEP", "PROMOTION"],
    }
