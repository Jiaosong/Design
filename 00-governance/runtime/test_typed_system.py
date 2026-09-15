#!/usr/bin/env python3
from __future__ import annotations

from validate_typed_system import self_test

EXPECTED = {
    "P1/CLAIM-RP01",
    "P4/IFC-RP01",
    "P4/VAR-RP09",
    "P4/VAR-RP10",
    "P4/VAR-RP11",
    "P4/AUTH-RP06",
    "P4/VAR-RP12",
    "P4/IFC-RP10",
    "P4/IFC-RP11",
    "P4/IFC-RP12",
    "P4/IFC-RP13",
    "P5/CHG-RP01",
    "P5/CFG-RP05",
    "P5/CARRY-RP04",
    "P5/CONC-RP03",
    "P5/PROM-RP05",
    "P5/ROLL-RP04",
    "P5/ROLL-RP05",
    "P5/CARRY-RP05",
    "P5/STALE-RP05",
    "P5/CSA-RP02",
    "P5/CONC-RP04",
    "P6/ASR-RP02",
    "P6/APP-RP04",
    "P6/ADM-RP04",
    "P6/APP-RP05",
    "P6/TGT-RP01",
    "P6/INDP-RP02",
    "P6/CEIL-RP04",
    "P6/RDY-RP02",
    "P6/CEIL-RP05",
    "P6/TRF-RP01",
    "P6/CONTRA-RP02",
    "P6/UNC-RP02",
    "P6/UNC-RP03",
    "P6/UNC-RP04",
    "P6/DISP-RP02",
    "P6/IND-RP02",
    "P6/INDP-RP03",
    "P6/INDP-RP04",
    "P6/CONTRA-RP03",
    "P6/CEIL-RP06",
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
