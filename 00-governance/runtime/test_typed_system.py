#!/usr/bin/env python3
from __future__ import annotations

from validate_typed_system import self_test

EXPECTED = {
    "P1/CLAIM-RP01",
    "P4/IFC-RP01",
    "P5/CHG-RP01",
    "P6/ASR-RP02",
    "P9/CORPUS-RP01",
    "P10/ASSET-RP01",
    "P10/TRUTH-RP03",
    "P10/MED-RP01",
    "P11/BADGE-RP02",
}


def main() -> None:
    findings = self_test()
    actual = {f.rule_id for f in findings}
    missing = sorted(EXPECTED - actual)
    if missing:
        raise SystemExit(f"typed-system engine self-test failed: missing {missing}")
    print(f"typed-system engine self-test PASS: {len(findings)} expected findings emitted")


if __name__ == "__main__":
    main()
