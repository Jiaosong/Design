#!/usr/bin/env python3
from __future__ import annotations

import json

from oleander_system_gateway import run_self_test, validate_system_manifest


def main() -> None:
    manifest = validate_system_manifest()
    self_test = run_self_test() if manifest["status"] == "PASS" else {"status": "SKIPPED"}
    status = "PASS" if manifest["status"] == "PASS" and self_test["status"] == "PASS" else "FAIL"
    print(json.dumps({
        "status": status,
        "manifest": manifest,
        "gateway_self_test": self_test
    }, ensure_ascii=False, indent=2))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
