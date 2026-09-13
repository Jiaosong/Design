#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENDPOINT = (
    "https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev"
    "/v1/execution-live-status"
)
WORKER_DEV_VARS = (
    ROOT
    / "90-shared"
    / "oleander-core-framework"
    / "runtime"
    / "notion_canonical_knowledge"
    / ".dev.vars"
)
ALLOWED_STATUS = {"WORKING", "REVIEW_PENDING", "HOLD", "CLOSED"}


def _clean_string(value: object, max_len: int) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value[:max_len] if value else None


def projection_from_receipt(receipt: dict) -> dict:
    checkpoint = receipt.get("continuation_checkpoint") or {}
    flow = receipt.get("flow_completion") or {}
    readback = receipt.get("readback") or {}

    task_id = _clean_string(receipt.get("task_id"), 200)
    executor_id = _clean_string(checkpoint.get("executor_id"), 200)
    sequence = checkpoint.get("checkpoint_sequence")
    status = _clean_string(receipt.get("status"), 40)
    if not task_id:
        raise ValueError("receipt task_id is required")
    if not executor_id:
        raise ValueError("continuation_checkpoint.executor_id is required")
    if not isinstance(sequence, int) or sequence < 0:
        raise ValueError("continuation_checkpoint.checkpoint_sequence must be a non-negative integer")
    if status not in ALLOWED_STATUS:
        raise ValueError(f"receipt status must be one of {sorted(ALLOWED_STATUS)}")

    payload: dict[str, object] = {
        "task_id": task_id,
        "executor_id": executor_id,
        "checkpoint_sequence": sequence,
        "status": status,
    }
    optional = {
        "current_node": _clean_string(checkpoint.get("current_node"), 500),
        "next_allowed_action": _clean_string(checkpoint.get("next_allowed_action"), 1000),
        "receipt_id": _clean_string(receipt.get("receipt_id"), 500),
        "readback_verdict": _clean_string(readback.get("verdict"), 500),
        "flow_completion_gate": _clean_string(flow.get("completion_gate"), 200),
    }
    payload.update({key: value for key, value in optional.items() if value})
    return payload


def projection_from_direct(payload: dict) -> dict:
    required = {
        "task_id": _clean_string(payload.get("task_id"), 200),
        "executor_id": _clean_string(payload.get("executor_id"), 200),
        "checkpoint_sequence": payload.get("checkpoint_sequence"),
        "status": _clean_string(payload.get("status"), 40),
    }
    if not required["task_id"]:
        raise ValueError("task_id is required")
    if not required["executor_id"]:
        raise ValueError("executor_id is required")
    if not isinstance(required["checkpoint_sequence"], int) or required["checkpoint_sequence"] < 0:
        raise ValueError("checkpoint_sequence must be a non-negative integer")
    if required["status"] not in ALLOWED_STATUS:
        raise ValueError(f"status must be one of {sorted(ALLOWED_STATUS)}")
    result: dict[str, object] = dict(required)
    for key, max_len in (
        ("current_node", 500),
        ("next_allowed_action", 1000),
        ("receipt_id", 500),
        ("readback_verdict", 500),
        ("flow_completion_gate", 200),
        ("note", 2000),
    ):
        value = _clean_string(payload.get(key), max_len)
        if value:
            result[key] = value
    return result


def _load_dev_var(path: Path, key: str) -> str | None:
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith(f"{key}="):
            continue
        value = line.split("=", 1)[1].strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        return value or None
    return None


def _token() -> str:
    direct = os.environ.get("OLEANDER_KNOWLEDGE_READER_TOKEN", "").strip()
    if direct:
        return direct
    direct = os.environ.get("OLEANDER_API_TOKEN", "").strip()
    if direct:
        return direct
    token_file = os.environ.get("OLEANDER_KNOWLEDGE_READER_TOKEN_FILE", "").strip()
    if token_file:
        value = Path(token_file).read_text(encoding="utf-8").strip()
        if value:
            return value
    local = _load_dev_var(WORKER_DEV_VARS, "OLEANDER_API_TOKEN")
    if local:
        return local
    raise RuntimeError(
        "No execution-live-status credential is configured. Set OLEANDER_KNOWLEDGE_READER_TOKEN, "
        "OLEANDER_API_TOKEN, or OLEANDER_KNOWLEDGE_READER_TOKEN_FILE."
    )


def publish(payload: dict, endpoint: str, timeout: float = 6.0) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {_token()}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            parsed = json.loads(response.read().decode("utf-8"))
            return {
                "publisher": "OLEANDER_EXECUTION_LIVE_STATUS_PROJECTION",
                "authority_ceiling": "OBSERVABILITY_ONLY",
                "http_status": response.status,
                "response": parsed,
            }
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"execution live-status publish failed HTTP {exc.code}: {detail[:1200]}") from exc


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
        description="Publish one latest-only OLEANDER execution status projection to the existing Cloudflare runtime."
    )
    parser.add_argument("input", nargs="?", help="JSON input or receipt path; omit/use '-' for stdin")
    parser.add_argument("--receipt", action="store_true", help="Interpret input as OLEANDER Execution Receipt v1")
    parser.add_argument("--dry-run", action="store_true", help="Validate/extract payload without network mutation")
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("OLEANDER_KNOWLEDGE_READER_EXECUTION_STATUS_ENDPOINT", DEFAULT_ENDPOINT),
    )
    args = parser.parse_args()
    try:
        source = _load_input(args.input)
        payload = projection_from_receipt(source) if args.receipt else projection_from_direct(source)
        if args.dry_run:
            result = {
                "publisher": "OLEANDER_EXECUTION_LIVE_STATUS_PROJECTION",
                "authority_ceiling": "OBSERVABILITY_ONLY",
                "dry_run": True,
                "payload": payload,
            }
        else:
            result = publish(payload, args.endpoint)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(json.dumps({
            "publisher": "OLEANDER_EXECUTION_LIVE_STATUS_PROJECTION",
            "authority_ceiling": "OBSERVABILITY_ONLY",
            "error": str(exc),
        }, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2) from exc
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
