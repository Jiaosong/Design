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
ALLOWED_OWNER_NODE_ROLES = {
    "PRIMARY_OWNER",
    "SUPPORTING_OWNER",
    "READ_ONLY_CONSUMER",
    "VALIDATOR",
    "INDEPENDENT_REVIEWER",
}
OWNER_CONTEXT_REQUIRED_FLOW_PHASES = {
    "AUTHORITY_PREFLIGHT",
    "STICKY_CONSTRAINT_RESOLUTION",
    "EXISTING_KNOWLEDGE_METHOD_SKILL_RESOLUTION",
    "REQUIRED_NATIVE_OUTPUT_DEFINITION",
    "CAPABILITY_AND_MINIMUM_OWNER_SET",
}


def _clean_string(value: object, max_len: int) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value[:max_len] if value else None


def _clean_string_list(value: object, *, max_items: int, max_len: int) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    seen: set[str] = set()
    for item in value[:max_items]:
        cleaned = _clean_string(item, max_len)
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
    return result


def _execution_context_from_receipt(receipt: dict) -> dict:
    """Extract only execution-owner context already recorded by Execution Receipt v1.

    This function does not resolve an owner. It refuses to synthesize missing
    owner/output/canonical inputs and therefore cannot become a second owner
    resolver.
    """
    receipt_id = _clean_string(receipt.get("receipt_id"), 500)
    authority = receipt.get("authority")
    native_output = receipt.get("required_native_output")
    owner_set = receipt.get("owner_set")
    checkpoint = receipt.get("continuation_checkpoint")
    flow = receipt.get("flow_completion")
    if not receipt_id:
        raise ValueError("receipt receipt_id is required for execution context projection")
    if not isinstance(authority, dict):
        raise ValueError("receipt authority is required for execution context projection")
    canonical_ids = _clean_string_list(authority.get("canonical_ids"), max_items=64, max_len=500)
    if not canonical_ids:
        raise ValueError("receipt authority.canonical_ids must contain at least one canonical id")
    if not isinstance(native_output, dict):
        raise ValueError("receipt required_native_output is required for execution context projection")
    artifact_class = _clean_string(native_output.get("artifact_class"), 500)
    native_format = _clean_string(native_output.get("native_format"), 500)
    target_runtime = _clean_string(native_output.get("target_runtime"), 1000)
    editable_required = native_output.get("editable_required")
    derived_formats = _clean_string_list(native_output.get("derived_formats"), max_items=32, max_len=500)
    if not artifact_class or not native_format or not target_runtime or not isinstance(editable_required, bool):
        raise ValueError("receipt required_native_output is incomplete")
    if not isinstance(owner_set, dict):
        raise ValueError("receipt owner_set is required for execution context projection")
    minimum_sufficient = owner_set.get("minimum_sufficient_owner_set")
    primary_owner = _clean_string(owner_set.get("primary_owner"), 500)
    omitted_owner_reasoning = _clean_string(owner_set.get("omitted_owner_reasoning"), 2000)
    raw_nodes = owner_set.get("nodes")
    if minimum_sufficient is not True or not primary_owner or not omitted_owner_reasoning or not isinstance(raw_nodes, list):
        raise ValueError("receipt owner_set is incomplete")
    nodes: list[dict[str, str]] = []
    for raw in raw_nodes[:32]:
        if not isinstance(raw, dict):
            continue
        owner_id = _clean_string(raw.get("owner_id"), 500)
        role = _clean_string(raw.get("role"), 200)
        if owner_id and role in ALLOWED_OWNER_NODE_ROLES:
            nodes.append({"owner_id": owner_id, "role": role})
    if not nodes:
        raise ValueError("receipt owner_set.nodes must contain at least one typed owner node")
    primary_nodes = [node for node in nodes if node["role"] == "PRIMARY_OWNER"]
    if len(primary_nodes) != 1 or primary_nodes[0]["owner_id"] != primary_owner:
        raise ValueError("receipt owner_set must contain exactly one PRIMARY_OWNER matching primary_owner")
    if not isinstance(checkpoint, dict):
        raise ValueError("receipt continuation_checkpoint is required for execution context projection")
    checkpoint_state = _clean_string(checkpoint.get("checkpoint_state"), 80)
    authority_fingerprint = _clean_string(checkpoint.get("authority_fingerprint"), 1000)
    stale_reasons = _clean_string_list(checkpoint.get("stale_reasons"), max_items=32, max_len=1000)
    if not checkpoint_state or not authority_fingerprint:
        raise ValueError("receipt continuation_checkpoint provenance is incomplete")
    if not isinstance(flow, dict):
        raise ValueError("receipt flow_completion is required for execution context projection")
    phase_results = flow.get("phase_results")
    if not isinstance(phase_results, dict):
        raise ValueError("receipt flow_completion.phase_results is required for execution context projection")
    missing_pass = sorted(
        phase for phase in OWNER_CONTEXT_REQUIRED_FLOW_PHASES if phase_results.get(phase) != "PASS"
    )
    if missing_pass:
        raise ValueError(f"receipt owner-routing phases are not PASS: {missing_pass}")
    completion_gate = _clean_string(flow.get("completion_gate"), 40)
    completion_claim_allowed = flow.get("completion_claim_allowed")
    incomplete_required_phases = _clean_string_list(
        flow.get("incomplete_required_phases"), max_items=64, max_len=500
    )
    if receipt.get("status") == "CLOSED" and (
        completion_gate != "PASS"
        or completion_claim_allowed is not True
        or incomplete_required_phases
    ):
        raise ValueError("closed receipt does not satisfy the existing Flow Completion Gate")
    return {
        "source": "OLEANDER_EXECUTION_RECEIPT_V1",
        "receipt_id": receipt_id,
        "canonical_ids": canonical_ids,
        "checkpoint_state": checkpoint_state,
        "authority_fingerprint": authority_fingerprint,
        "stale_reasons": stale_reasons,
        "required_native_output": {
            "artifact_class": artifact_class,
            "native_format": native_format,
            "editable_required": editable_required,
            "target_runtime": target_runtime,
            "derived_formats": derived_formats,
        },
        "owner_set": {
            "minimum_sufficient_owner_set": minimum_sufficient,
            "primary_owner": primary_owner,
            "nodes": nodes,
            "omitted_owner_reasoning": omitted_owner_reasoning,
        },
        "flow_completion": {
            "completion_gate": completion_gate,
            "completion_claim_allowed": completion_claim_allowed is True,
            "incomplete_required_phases": incomplete_required_phases,
        },
    }


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
        "execution_context": _execution_context_from_receipt(receipt),
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
    # Direct status input remains observability-only and may not inject owner
    # routing context. Only the Execution Receipt extraction path can carry it.
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


def _token(explicit_token_file: str | None = None) -> str:
    direct = os.environ.get("OLEANDER_KNOWLEDGE_READER_TOKEN", "").strip()
    if direct:
        return direct
    direct = os.environ.get("OLEANDER_API_TOKEN", "").strip()
    if direct:
        return direct
    if explicit_token_file:
        value = Path(explicit_token_file).read_text(encoding="utf-8").strip()
        if value:
            return value
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


def publish(payload: dict, endpoint: str, timeout: float = 6.0, token_file: str | None = None) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {_token(token_file)}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "OLEANDER-Execution-Live-Status/1.0",
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
    parser.add_argument("--token-file", default=None, help="Read the bearer credential from this local file without exporting it through the shell environment")
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
            result = publish(payload, args.endpoint, token_file=args.token_file)
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
