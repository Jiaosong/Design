#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAMING = ROOT / "00-governance" / "naming-status.md"
CASE_MAP = ROOT / "00-governance" / "case-map.md"
AUTHORITY = ROOT / "00-governance" / "legacy-authority-registry.md"
CLAIM_SCHEMA = ROOT / "00-governance" / "schemas" / "claim-id.schema.json"
C01_SCHEMA = ROOT / "00-governance" / "schemas" / "c01-evidence-manifest.v1.schema.json"
C01_TEMPLATE = ROOT / "00-governance" / "schemas" / "c01-evidence-manifest.template.json"


def fail(message):
    raise AssertionError(message)


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing governance file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def require_text(path, terms):
    if not path.exists():
        fail(f"missing governance file: {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    missing = [term for term in terms if term not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing required authority terms: {missing}")
    return text


def main():
    try:
        naming = require_text(NAMING, [
            "C01", "C02", "C03", "C04", "CLM-[Scope]-[NNN]",
            "CLM-C01-001", "CLM-C04-001", "bare `Cnn`", "migration failure",
            "Project axis namespace", "Application Mapping namespace",
            "Priority-0", "Domain / exact L0–L7 level",
        ])
        require_text(CASE_MAP, [
            "C01 / 一脉广渡", "C02 / 忘也 Daylily", "C03 / The Light Collection",
            "C04 / 清江石书", "CLM-C01-NNN", "CLM-C04-NNN",
            "Case Axis root IDs only", "Application Mapping",
        ])
        require_text(AUTHORITY, [
            "SUPERSEDED MACHINE SCHEMA", "HISTORICAL ERROR", "RESOLVED HISTORICAL FAILURE",
            "CASE_GD_Public_Claim_Matrix.csv", "CLM-C01-001", "CLM-C01-005",
        ])

        if re.search(r"Claim(?: ID)?[^\n]*\bC\d{2}\b", naming, re.IGNORECASE):
            for line in naming.splitlines():
                if re.search(r"Claim(?: ID)?[^\n]*\bC\d{2}\b", line, re.IGNORECASE) and not any(k in line.lower() for k in ("histor", "legacy", "must not", "invalid")):
                    fail(f"unqualified bare case ID appears in Claim context: {line}")

        if "Cnn` is reserved" not in naming and "Cnn` values MUST NOT be used as Project IDs" not in naming:
            fail("naming authority must explicitly prevent bare Cnn from becoming a Project ID")

        claim_schema = load_json(CLAIM_SCHEMA)
        claim_encoded = json.dumps(claim_schema, ensure_ascii=False)
        if "CLM-C" not in claim_encoded or "^C\\\\d{2}$" not in claim_encoded:
            fail("claim-id schema must accept CLM-Cnn-NNN and explicitly reject bare Cnn")

        c01_schema = load_json(C01_SCHEMA)
        c01_encoded = json.dumps(c01_schema, ensure_ascii=False)
        if c01_schema.get("properties", {}).get("case", {}).get("properties", {}).get("id", {}).get("const") != "C01":
            fail("C01 schema case.id must be const C01")
        responsibility = c01_schema.get("properties", {}).get("responsibility", {}).get("properties", {})
        if responsibility.get("practiceOwner", {}).get("const") != "刘旋 / Liu Xuan":
            fail("C01 schema practiceOwner must be 刘旋 / Liu Xuan")
        if "P01_evidence_manifest.v0.2.schema.json" not in c01_encoded:
            fail("C01 schema must record superseded P01 schema")
        current_case_id = c01_schema.get("properties", {}).get("case", {}).get("properties", {}).get("id", {}).get("const")
        if current_case_id == "P01":
            fail("canonical C01 schema must not use P01 as a current case identifier")

        template = load_json(C01_TEMPLATE)
        if template.get("case", {}).get("id") != "C01":
            fail("C01 template must use case.id C01")
        claims = template.get("claims", [])
        if not claims or not re.fullmatch(r"CLM-C01-\d{3}", claims[0].get("claimId", "")):
            fail("C01 template must seed canonical CLM-C01-NNN claim IDs")
        if template.get("responsibility", {}).get("practiceOwner") != "刘旋 / Liu Xuan":
            fail("C01 template must use current responsibility identity")

    except AssertionError as exc:
        print(f"OLEANDER NAMESPACE GOVERNANCE: FAIL\n{exc}", file=sys.stderr)
        return 1

    print("OLEANDER NAMESPACE GOVERNANCE: PASS")
    print("- case roots locked: C01 / C02 / C03 / C04")
    print("- bare Cnn cannot substitute for Project ID")
    print("- Application Mapping separated from Domain/L0-L7 and Project Axis")
    print("- delivery priority uses Priority-* namespace")
    print("- claim namespace locked: CLM-[Scope]-[NNN]")
    print("- legacy P01 / CASE-GD authority explicitly superseded")
    print("- canonical C01 schema/template validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
