#!/usr/bin/env python3
"""Validate that release workflow defaults match the locked authority manifest."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "website" / "practice" / "timer-light-basin-v3" / "DEPLOYMENT_ARTIFACT_MANIFEST_v3.3.json"
WORKFLOWS = [
    ROOT / ".github" / "workflows" / "timer-v33-integrated-browser.yml",
    ROOT / ".github" / "workflows" / "timer-v33-staged-pages.yml",
]


def validate():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected_tag = manifest["staging_release_tag"]
    expected_asset = manifest["asset_name"]

    failures = []
    for path in WORKFLOWS:
        text = path.read_text(encoding="utf-8")
        if f'default: "{expected_tag}"' not in text:
            failures.append(f"{path.relative_to(ROOT)}: default draft release tag does not match manifest")
        if f'default: "{expected_asset}"' not in text:
            failures.append(f"{path.relative_to(ROOT)}: default asset_name does not match manifest")

    if failures:
        raise AssertionError("\n".join(failures))

    print("WORKFLOW RELEASE DEFAULT AUDIT: PASS")
    print(f"- staging_release_tag: {expected_tag}")
    print(f"- asset_name: {expected_asset}")


def main():
    try:
        validate()
    except (AssertionError, KeyError, json.JSONDecodeError, OSError) as exc:
        print(f"WORKFLOW RELEASE DEFAULT AUDIT: FAIL\n{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
