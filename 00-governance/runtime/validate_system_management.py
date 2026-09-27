#!/usr/bin/env python3
from __future__ import annotations

import json

from oleander_system_gateway import run_self_test, validate_system_manifest
from oleander_system_linter import run_lint


def main() -> None:
    manifest = validate_system_manifest()
    self_test = run_self_test() if manifest["status"] == "PASS" else {"status": "SKIPPED"}
    architecture_lint = run_lint() if manifest["status"] == "PASS" else {"status": "SKIPPED"}
    status = "PASS" if manifest["status"] == "PASS" and self_test["status"] == "PASS" and architecture_lint["status"] == "PASS" else "FAIL"
    print(json.dumps({
        "status": status,
        "manifest": manifest,
        "gateway_self_test": self_test,
        "architecture_lint": architecture_lint
    }, ensure_ascii=False, indent=2))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
