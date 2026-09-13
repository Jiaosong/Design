#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Callable

from oleander_chat_resolver_adapter import run_preflight
from publish_execution_live_status import (
    DEFAULT_ENDPOINT,
    projection_from_direct,
    projection_from_receipt,
    publish,
)


BRIDGE_ID = "chat_on_steroids_oleander_runtime_bridge"
AUTHORITY_CEILING = "EXECUTION_ADAPTER_PLUS_OBSERVABILITY_ONLY"
ROOT = Path(__file__).resolve().parents[2]


def _workspace_root() -> Path:
    """Resolve the shared workspace root without copying credentials into a worktree."""
    if ROOT.parent.name == ".worktrees":
        return ROOT.parent.parent
    return ROOT


def _default_token_file() -> str | None:
    if os.environ.get("OLEANDER_KNOWLEDGE_READER_TOKEN") or os.environ.get("OLEANDER_API_TOKEN"):
        return None
    configured = os.environ.get("OLEANDER_KNOWLEDGE_READER_TOKEN_FILE", "").strip()
    if configured:
        return configured
    candidate = _workspace_root() / ".mcp-runtime" / "secrets" / "oleander-knowledge-reader.token"
    return str(candidate) if candidate.is_file() else None


def _projection_from_payload(payload: dict) -> dict | None:
    """Extract only caller/source-observed telemetry; never infer execution authority."""
    receipt = payload.get("execution_receipt")
    if isinstance(receipt, dict):
        return projection_from_receipt(receipt)

    direct = payload.get("live_projection")
    if isinstance(direct, dict):
        return projection_from_direct(direct)

    checkpoint = payload.get("checkpoint")
    if not isinstance(checkpoint, dict):
        return None
    task_id = payload.get("task_id")
    status = payload.get("status")
    if not isinstance(task_id, str) or not task_id.strip() or not isinstance(status, str) or not status.strip():
        return None

    projection: dict[str, object] = {
        "task_id": task_id,
        "executor_id": checkpoint.get("executor_id"),
        "checkpoint_sequence": checkpoint.get("checkpoint_sequence"),
        "status": status,
        "current_node": checkpoint.get("current_node"),
        "next_allowed_action": checkpoint.get("next_allowed_action"),
    }
    readback = payload.get("readback")
    if isinstance(readback, dict):
        projection["readback_verdict"] = readback.get("verdict")
    flow = payload.get("flow_completion")
    if isinstance(flow, dict):
        projection["flow_completion_gate"] = flow.get("completion_gate")
    if isinstance(payload.get("receipt_id"), str):
        projection["receipt_id"] = payload.get("receipt_id")
    if isinstance(payload.get("live_note"), str):
        projection["note"] = payload.get("live_note")
    return projection_from_direct(projection)


def run_bridge(
    payload: dict,
    *,
    publish_live: bool = True,
    endpoint: str = DEFAULT_ENDPOINT,
    token_file: str | None = None,
    publisher: Callable[..., dict] = publish,
) -> dict:
    """Run the authoritative resolver adapter, then best-effort derivative telemetry publication."""
    preflight = run_preflight(payload)
    observability: dict[str, object] = {
        "authority_ceiling": "OBSERVABILITY_ONLY",
        "changes_resolver_decision": False,
        "changes_project_state": False,
        "changes_completion_authority": False,
    }

    try:
        projection = _projection_from_payload(payload)
    except (KeyError, TypeError, ValueError) as exc:
        observability.update({
            "state": "DEGRADED",
            "reason": "INVALID_SOURCE_OBSERVED_LIVE_PROJECTION",
            "error": str(exc),
        })
        projection = None

    if projection is None and "state" not in observability:
        observability.update({
            "state": "NOT_PUBLISHED",
            "reason": "SOURCE_OBSERVED_LIVE_FIELDS_NOT_PRESENT",
        })
    elif projection is not None and not publish_live:
        observability.update({
            "state": "DRY_RUN",
            "projection": projection,
        })
    elif projection is not None:
        try:
            result = publisher(
                projection,
                endpoint,
                token_file=token_file if token_file is not None else _default_token_file(),
            )
            observability.update({
                "state": "PUBLISHED",
                "projection": projection,
                "publish_result": result,
            })
        except (OSError, RuntimeError, ValueError) as exc:
            # Live telemetry is intentionally outside the Resolver authority path.
            observability.update({
                "state": "DEGRADED",
                "reason": "LIVE_STATUS_PUBLISH_FAILED",
                "error": str(exc),
                "projection": projection,
            })

    return {
        "bridge": {
            "bridge_id": BRIDGE_ID,
            "authority_ceiling": AUTHORITY_CEILING,
            "resolver_adapter": preflight.get("adapter", {}).get("adapter_id"),
        },
        "preflight": preflight,
        "observability": observability,
    }


def run_self_test() -> dict:
    payload = {
        "intent": "CONTINUE",
        "task_id": "bridge-self-test",
        "status": "WORKING",
        "current_authority_fingerprint": "AUTH-BRIDGE-1",
        "checkpoint": {
            "checkpoint_state": "RESUMABLE",
            "authority_fingerprint": "AUTH-BRIDGE-1",
            "last_verified_artifact": {
                "artifact_id": "ART-BRIDGE-1",
                "hash_or_commit": "bridge111",
                "readback_verdict": "PASS",
            },
            "stale_reasons": [],
            "current_node": "ACTUAL_READBACK",
            "resume_from": "ACTUAL_READBACK",
            "next_allowed_action": "NEXT_NODE",
            "checkpoint_sequence": 7,
            "checkpoint_updated_at": "2026-09-13T00:00:00Z",
            "expected_checkpoint_sequence": 7,
            "executor_id": "CHAT-BRIDGE",
            "execution_lease_state": "NONE",
            "lease_acquired_at": "NOT_APPLICABLE",
        },
    }
    dry = run_bridge(payload, publish_live=False)
    if dry["preflight"]["conversation_directive"]["action"] != "EXECUTE_NEXT_ALLOWED_ACTION":
        raise RuntimeError("bridge self-test: resolver directive drifted")
    projection = dry["observability"].get("projection") or {}
    if projection.get("checkpoint_sequence") != 7 or projection.get("task_id") != "bridge-self-test":
        raise RuntimeError("bridge self-test: source-observed projection extraction failed")

    def fail_publisher(*_args, **_kwargs):
        raise RuntimeError("simulated observability outage")

    degraded = run_bridge(payload, publisher=fail_publisher)
    if degraded["observability"].get("state") != "DEGRADED":
        raise RuntimeError("bridge self-test: publish failure must degrade observability")
    if degraded["preflight"]["conversation_directive"] != dry["preflight"]["conversation_directive"]:
        raise RuntimeError("bridge self-test: publish failure changed resolver decision")
    return {
        "status": "PASS",
        "bridge_id": BRIDGE_ID,
        "checks": [
            "RESOLVER_DECISION_PRESERVED",
            "SOURCE_OBSERVED_PROJECTION_ONLY",
            "PUBLISH_FAILURE_OBSERVABILITY_ONLY",
        ],
    }


def _load_input(path: str | None) -> dict:
    if not path or path == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("input must be one JSON object")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the existing OLEANDER CoS resolver adapter and best-effort Reader live observability projection."
    )
    parser.add_argument("input", nargs="?", help="Resolver JSON input file; omit/use '-' for stdin")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    parser.add_argument("--no-publish", action="store_true", help="Run resolver and projection extraction without network mutation")
    parser.add_argument("--token-file", default=None, help="Optional local bearer token file; secret contents are never printed")
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("OLEANDER_KNOWLEDGE_READER_EXECUTION_STATUS_ENDPOINT", DEFAULT_ENDPOINT),
    )
    parser.add_argument("--self-test", action="store_true", help="Run bridge invariants without network access")
    args = parser.parse_args()

    try:
        if args.self_test:
            print(json.dumps(run_self_test(), ensure_ascii=False, indent=2))
            return
        payload = _load_input(args.input)
        result = run_bridge(
            payload,
            publish_live=not args.no_publish,
            endpoint=args.endpoint,
            token_file=args.token_file,
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": "INVALID_BRIDGE_INPUT", "detail": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2) from exc

    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=args.pretty))


if __name__ == "__main__":
    main()
