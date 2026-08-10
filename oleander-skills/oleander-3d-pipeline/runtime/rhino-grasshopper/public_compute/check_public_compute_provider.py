#!/usr/bin/env python3
"""Lightweight availability preflight for the historical McNeel public Rhino.Compute endpoint.

This probe is intentionally cheaper than submitting a Grasshopper definition.
It never reads or permits RHINO_TOKEN / Core-Hour billing credentials.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import ssl
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_URL = "https://compute.rhino3d.com/"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def scrub(text: str, token: str | None) -> str:
    if token:
        text = text.replace(token, "[REDACTED]")
        text = text.replace("Bearer " + token, "Bearer [REDACTED]")
        text = text.replace("bearer " + token, "bearer [REDACTED]")
    return text


def classify(http_status: int | None, body: str, error_kind: str | None) -> str:
    lower = body.lower()
    if "this server has been turned off" in lower:
        return "PUBLIC_SERVICE_DISABLED"
    if error_kind == "NETWORK":
        return "NETWORK_BLOCKED"
    if http_status in (401, 403) or "unauthor" in lower or "authorization" in lower or "sign in" in lower:
        return "AUTH_REQUIRED"
    if http_status == 402 or "core-hour" in lower or "billing" in lower or "payment" in lower:
        return "PAID_PATH_REJECTED"
    if http_status is not None and 200 <= http_status < 300:
        return "AVAILABLE"
    if http_status is not None and http_status >= 400:
        return "UNAVAILABLE"
    return "UNKNOWN"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--out-dir", default="runtime-state/public-compute")
    args = parser.parse_args()

    if os.environ.get("RHINO_TOKEN"):
        raise SystemExit("FREE_PUBLIC_COMPUTE preflight refuses RHINO_TOKEN / Core-Hour billing")

    auth_token = os.environ.get("RHINO_COMPUTE_TOKEN") or None
    auth_mode = "RHINO_ACCOUNTS_BEARER_PRESENT" if auth_token else "ANONYMOUS"
    endpoint = args.url.rstrip("/") + "/healthcheck"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "OLEANDER-FREE-PUBLIC-COMPUTE-PREFLIGHT/0.1",
    }
    if auth_token:
        headers["Authorization"] = "Bearer " + auth_token

    started = utc_now()
    http_status = None
    raw_body = ""
    error_kind = None
    error_message = None
    try:
        request = urllib.request.Request(endpoint, headers=headers, method="GET")
        with urllib.request.urlopen(request, timeout=20, context=ssl.create_default_context()) as response:
            http_status = int(response.status)
            raw_body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        http_status = int(exc.code)
        raw_body = exc.read().decode("utf-8", errors="replace")
        error_kind = "HTTP"
        error_message = str(exc)
    except Exception as exc:
        error_kind = "NETWORK"
        error_message = f"{type(exc).__name__}: {exc}"
    finished = utc_now()

    safe_body = scrub(raw_body, auth_token)
    state = classify(http_status, safe_body, error_kind)
    action = "ALLOW_SP02_SUBMISSION" if state == "AVAILABLE" else "SKIP_SP02_PRESERVE_OPEN"

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    receipt = {
        "probe_id": "OLEANDER-FREE-PUBLIC-COMPUTE-PREFLIGHT-v0.1",
        "runtime_mode": "FREE_PUBLIC_COMPUTE",
        "cost_policy": "NO_PAID_RUNTIME",
        "provider": "MCNEEL_PUBLIC_LEGACY",
        "server": args.url,
        "endpoint": "/healthcheck",
        "started_at": started,
        "finished_at": finished,
        "auth": {
            "mode": auth_mode,
            "rhino_token_core_hour_allowed": False,
            "token_value_logged": False,
        },
        "transport": {
            "http_status": http_status,
            "error_kind": error_kind,
            "error_message": scrub(error_message or "", auth_token) or None,
            "response_body": safe_body[:2000],
        },
        "provider_state": state,
        "selector_action": action,
        "cp2": {
            "status_if_skipped": "OPEN",
            "promotion_allowed": state == "AVAILABLE",
            "note": "Provider availability is not Grasshopper runtime evidence.",
        },
        "cp4": {
            "status": "OPEN",
            "blocker": "HEADLESS_NO_GRASSHOPPER_GUI",
        },
    }
    path = out_dir / "provider_preflight_receipt.json"
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({
        "provider_state": state,
        "selector_action": action,
        "http_status": http_status,
        "auth_mode": auth_mode,
        "receipt": str(path),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
