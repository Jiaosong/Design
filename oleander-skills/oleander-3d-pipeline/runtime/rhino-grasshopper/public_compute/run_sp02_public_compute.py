#!/usr/bin/env python3
"""Best-effort no-cost probe of McNeel public Rhino.Compute for OLEANDER SP02.

Evidence rules:
- never reads RHINO_TOKEN (Core-Hour billing token);
- optionally reads RHINO_COMPUTE_TOKEN only as a Rhino Accounts bearer token;
- CP2 upgrades only when a real headless Grasshopper response contains the exact OLEANDER report;
- CP4 is always OPEN in this headless mode.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import re
import ssl
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_URL = "https://compute.rhino3d.com/"
MARKER = "OLEANDER_SP02_REPORT::"
EXPECTED = {
    "BASE": {"branch_count": 4, "item_count": 24, "items_per_branch": [6, 6, 6, 6]},
    "GRAFT": {"branch_count": 24, "item_count": 24, "items_per_branch": [1] * 24},
    "FLATTEN": {"branch_count": 1, "item_count": 24, "items_per_branch": [24]},
    "TRANSPOSE_BY_ITEM": {"branch_count": 6, "item_count": 24, "items_per_branch": [4, 4, 4, 4, 4, 4]},
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scrub(text: str, token: str | None) -> str:
    if token:
        text = text.replace(token, "[REDACTED]")
        text = text.replace("Bearer " + token, "Bearer [REDACTED]")
        text = text.replace("bearer " + token, "bearer [REDACTED]")
    return text


def walk_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)


def extract_report(parsed: Any) -> dict | None:
    for text in walk_strings(parsed):
        if MARKER not in text:
            continue
        tail = text.split(MARKER, 1)[1].strip()
        # Standard-output data can contain surrounding quotes or additional newlines.
        candidates = [tail]
        match = re.search(r"(\{.*\})", tail, flags=re.S)
        if match:
            candidates.append(match.group(1))
        for candidate in candidates:
            try:
                obj = json.loads(candidate)
                if isinstance(obj, dict):
                    return obj
            except json.JSONDecodeError:
                pass
    return None


def exact_cp2(report: dict | None) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not report:
        return False, ["OLEANDER runtime report marker not found in response"]
    if report.get("marker_version") != "OLEANDER-SP02-HEADLESS-REPORT-v1":
        errors.append("unexpected report marker version")
    states = report.get("states") or {}
    for key, expected in EXPECTED.items():
        state = states.get(key)
        if not isinstance(state, dict):
            errors.append(f"{key}: state missing")
            continue
        for field in ("branch_count", "item_count", "items_per_branch"):
            if state.get(field) != expected[field]:
                errors.append(f"{key}.{field}: expected {expected[field]!r}, got {state.get(field)!r}")
    checks = report.get("checks") or {}
    if not all(checks.get(k) is True for k in EXPECTED):
        errors.append("runtime checks are not all true")
    return len(errors) == 0, errors


def classify(http_status: int | None, body: str, error_kind: str | None) -> str:
    lower = body.lower()
    if error_kind == "NETWORK":
        return "NETWORK_BLOCKED"
    if http_status in (401, 403) or "unauthor" in lower or "authorization" in lower or "sign in" in lower:
        return "AUTH_REQUIRED"
    if http_status == 402 or "core-hour" in lower or "billing" in lower or "payment" in lower:
        return "PAID_PATH_REJECTED"
    if http_status is not None and http_status >= 400:
        return "SERVER_REJECTED"
    return "DEFINITION_OR_REPORT_ERROR"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--definition", required=True)
    parser.add_argument("--out-dir", default="runtime-state/public-compute")
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()

    definition = Path(args.definition)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Important: FREE_PUBLIC_COMPUTE must never activate Core-Hour billing.
    if os.environ.get("RHINO_TOKEN"):
        raise SystemExit("FREE_PUBLIC_COMPUTE refuses to run when RHINO_TOKEN is present")

    auth_token = os.environ.get("RHINO_COMPUTE_TOKEN") or None
    auth_mode = "RHINO_ACCOUNTS_BEARER_PRESENT" if auth_token else "ANONYMOUS"
    endpoint = args.url.rstrip("/") + "/grasshopper"

    payload = {
        "algo": base64.b64encode(definition.read_bytes()).decode("ascii"),
        "pointer": None,
        "values": [],
    }
    request_body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "OLEANDER-FREE-PUBLIC-COMPUTE/0.1",
    }
    if auth_token:
        headers["Authorization"] = "Bearer " + auth_token

    http_status = None
    raw_body = ""
    error_kind = None
    error_message = None
    started = utc_now()
    try:
        req = urllib.request.Request(endpoint, data=request_body, headers=headers, method="POST")
        context = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=90, context=context) as response:
            http_status = int(response.status)
            raw_body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        http_status = int(exc.code)
        raw_body = exc.read().decode("utf-8", errors="replace")
        error_kind = "HTTP"
        error_message = str(exc)
    except Exception as exc:  # network/DNS/TLS/timeout are preserved, not hidden.
        error_kind = "NETWORK"
        error_message = f"{type(exc).__name__}: {exc}"
    finished = utc_now()

    safe_body = scrub(raw_body, auth_token)
    (out_dir / "public_compute_response.txt").write_text(safe_body, encoding="utf-8")

    parsed = None
    if raw_body:
        try:
            parsed = json.loads(raw_body)
            (out_dir / "public_compute_response.json").write_text(
                json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except json.JSONDecodeError:
            pass

    report = extract_report(parsed) if parsed is not None else None
    cp2_ok, validation_errors = exact_cp2(report)

    if cp2_ok and http_status is not None and 200 <= http_status < 300:
        blocker = None
        cp2_status = "REAL_HEADLESS_GRASSHOPPER_EVIDENCE"
        evidence_level = "REAL_RHINO_COMPUTE_GRASSHOPPER_HEADLESS"
    else:
        blocker = classify(http_status, safe_body, error_kind)
        cp2_status = "OPEN"
        evidence_level = "ATTEMPT_EVIDENCE_ONLY"

    receipt = {
        "run_id": "OLEANDER-SP02-FREE-PUBLIC-COMPUTE-001",
        "runtime_mode": "FREE_PUBLIC_COMPUTE",
        "cost_policy": "NO_PAID_RUNTIME",
        "server": args.url,
        "endpoint": "/grasshopper",
        "started_at": started,
        "finished_at": finished,
        "definition": {
            "path": str(definition),
            "sha256": sha256(definition),
        },
        "auth": {
            "mode": auth_mode,
            "rhino_compute_token_value_logged": False,
            "rhino_token_core_hour_allowed": False,
        },
        "transport": {
            "http_status": http_status,
            "error_kind": error_kind,
            "error_message": scrub(error_message or "", auth_token) or None,
        },
        "evidence": {
            "level": evidence_level,
            "runtime_report_found": report is not None,
            "runtime_report": report,
            "validation_errors": validation_errors,
        },
        "cp2": {
            "status": cp2_status,
            "blocker": blocker,
            "promotion_rule": "Only exact report from real public Rhino.Compute / Grasshopper response may promote CP2.",
        },
        "cp4": {
            "status": "OPEN",
            "blocker": "HEADLESS_NO_GRASSHOPPER_GUI",
            "note": "FREE_PUBLIC_COMPUTE never closes CP4; no Parameter Viewer / canvas GUI evidence exists in headless mode.",
        },
    }
    (out_dir / "public_compute_receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(json.dumps({
        "http_status": http_status,
        "auth_mode": auth_mode,
        "cp2": cp2_status,
        "cp2_blocker": blocker,
        "cp4": "OPEN",
        "evidence_level": evidence_level,
        "receipt": str(out_dir / "public_compute_receipt.json"),
    }, ensure_ascii=False))

    # Always return zero once an auditable receipt exists. Public service availability/auth
    # is evidence, not CI infrastructure failure.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
