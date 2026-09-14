"""OLEANDER validation runner v0.1."""

from datetime import datetime, timezone


def create_receipt(target_id: str, check: str, result: str, evidence=None):
    return {
        "id": f"VAL-{target_id}-{check}",
        "target": target_id,
        "check": check,
        "result": result,
        "evidence": evidence or [],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


def run_basic_checks(ole_object: dict):
    checks = []
    checks.append(create_receipt(
        ole_object["id"],
        "semantic_object_exists",
        "PASS" if ole_object.get("type") else "FAIL"
    ))
    checks.append(create_receipt(
        ole_object["id"],
        "source_binding_exists",
        "PASS" if ole_object.get("source") else "FAIL"
    ))
    return checks
