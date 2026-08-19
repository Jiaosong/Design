#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
RESOLVER = RUNTIME / "OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json"
REGISTER = RUNTIME / "OLEANDER_IMAGE_CONSUMPTION_REGISTER_v1.0.json"
CASES = ROOT / "evals" / "runtime" / "image_consumption_cases.jsonl"
C04_LEDGER = ROOT / "05-cases" / "c04-qingjiang-stone-book" / "orchestration" / "C04_IMAGE_CONSUMPTION_LEDGER_v1_0.json"


def fail(msg: str) -> None:
    raise SystemExit(f"image-consumption validation failed: {msg}")


def load_json(path: Path) -> dict:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON {path.relative_to(ROOT)}: {exc}")


def load_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    rows: list[dict] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except Exception as exc:
            fail(f"invalid JSONL {path.relative_to(ROOT)}:{lineno}: {exc}")
    return rows


def validate_resolver() -> dict:
    r = load_json(RESOLVER)
    if r.get("version") != "1.2" or r.get("implementation_revision") != "1.2.2":
        fail("Current resolver must be v1.2 implementation revision 1.2.2")
    pointer = r.get("execution_contract_layer", {}).get("image_consumption_register")
    if pointer != "00-governance/runtime/OLEANDER_IMAGE_CONSUMPTION_REGISTER_v1.0.json":
        fail("resolver must bind the Current image-consumption register")
    gate = r.get("image_consumption_gate", {})
    if gate.get("core_rule") != "ONE_SEMANTIC_CONTENT_IMAGE_ONE_CONSUMER_UNIT":
        fail("resolver image-consumption core rule missing")
    if gate.get("check_before_layout_and_image_binding") is not True:
        fail("image-consumption lookup must precede layout/image binding")
    required_hard = {
        "EXISTING_VISUAL_AUTHORITY_FIRST_FOR_VISUAL_PRODUCTION",
        "OBJECT_INTEGRITY_PRECEDES_FRAME_AND_LAYOUT",
        "ONE_SEMANTIC_CONTENT_IMAGE_ONE_CONSUMER_UNIT",
        "IMAGE_CONSUMPTION_LOOKUP_PRECEDES_CONTENT_IMAGE_BINDING",
        "DERIVATIVE_PRESENTATION_DOES_NOT_RESET_SEMANTIC_IMAGE_IDENTITY",
    }
    if not required_hard.issubset(set(r.get("hard_rules", []))):
        fail("resolver hard rules incomplete")
    return r


def validate_register() -> dict:
    reg = load_json(REGISTER)
    if reg.get("version") != "1.0":
        fail("image-consumption register must be v1.0")
    if reg.get("core_rule") != "ONE_SEMANTIC_CONTENT_IMAGE_ONE_CONSUMER_UNIT":
        fail("register core rule mismatch")
    states = set(reg.get("states", []))
    expected_states = {
        "AVAILABLE",
        "RESERVED",
        "CONSUMED",
        "RELEASED",
        "REJECTED_NOT_ELIGIBLE",
        "LEGACY_MULTI_CONSUMED",
    }
    if not expected_states.issubset(states):
        fail(f"register states incomplete: {sorted(expected_states - states)}")
    blocking = set(reg.get("blocking_states_for_other_consumers", []))
    expected_blocking = {"RESERVED", "CONSUMED", "REJECTED_NOT_ELIGIBLE", "LEGACY_MULTI_CONSUMED"}
    if not expected_blocking.issubset(blocking):
        fail("blocking states incomplete")
    ops = set(reg.get("derivative_operations_inherit_semantic_identity", []))
    for op in ["CROP", "RECOLOR", "MASK", "SCREENSHOT", "CONTOUR_TRACE"]:
        if op not in ops:
            fail(f"derivative identity inheritance missing {op}")
    if reg.get("fragmentation_for_identity_evasion_forbidden") is not True:
        fail("figure fragmentation laundering must be forbidden")
    if reg.get("conflict_verdict") != "BLOCK_SELECT_ANOTHER_IMAGE":
        fail("conflict must block and select another image")
    return reg


def decide(case: dict, blocking: set[str]) -> str:
    if case.get("system_reusable"):
        return "ALLOW"
    if case.get("existing_state") == "RELEASED" and case.get("explicit_release"):
        return "ALLOW"
    if case.get("existing_consumer_unit") == case.get("requested_consumer_unit"):
        return "ALLOW"
    if case.get("existing_state") in blocking:
        return "BLOCK"
    return "ALLOW"


def validate_cases(reg: dict) -> None:
    rows = load_jsonl(CASES)
    if len(rows) < 6:
        fail("image-consumption regression corpus must have at least six cases")
    required_ids = {
        "IMG-001-DUPLICATE-CONSUMER-BLOCK",
        "IMG-002-CROP-LAUNDERING-BLOCK",
        "IMG-003-SAME-CONSUMER-PAIRED-ALLOW",
        "IMG-004-SYSTEM-REUSABLE-ALLOW",
        "IMG-005-EXPLICIT-RELEASE-ALLOW",
        "IMG-006-REJECTED-IMAGE-BLOCK",
    }
    ids = {r.get("case_id") for r in rows}
    if not required_ids.issubset(ids):
        fail(f"missing cases {sorted(required_ids - ids)}")
    blocking = set(reg.get("blocking_states_for_other_consumers", []))
    for case in rows:
        actual = decide(case, blocking)
        if actual != case.get("expected"):
            fail(f"case {case.get('case_id')} expected {case.get('expected')} got {actual}")


def validate_ledger(path: Path, reg: dict) -> dict:
    ledger = load_json(path)
    if ledger.get("global_rule") != reg.get("core_rule"):
        fail(f"{path.name} global rule mismatch")
    records = ledger.get("records")
    if not isinstance(records, list) or not records:
        fail(f"{path.name} must contain records")

    seen_child_hash: dict[str, str] = {}
    seen_asset_ids: set[str] = set()
    allowed_states = set(reg.get("states", []))

    for rec in records:
        for field in ["asset_id", "semantic_image_id", "source_file", "source_hash", "state", "reuse_lock"]:
            if rec.get(field) in (None, ""):
                fail(f"{path.name}:{rec.get('asset_id')} missing {field}")
        if rec["asset_id"] in seen_asset_ids:
            fail(f"{path.name} duplicate asset_id {rec['asset_id']}")
        seen_asset_ids.add(rec["asset_id"])
        if rec["state"] not in allowed_states:
            fail(f"{path.name}:{rec['asset_id']} invalid state {rec['state']}")

        child_hash = rec.get("child_hash")
        if child_hash:
            prior = seen_child_hash.get(child_hash)
            if prior and prior != rec["semantic_image_id"]:
                fail(f"same child_hash assigned to different semantic identities: {prior} vs {rec['semantic_image_id']}")
            seen_child_hash[child_hash] = rec["semantic_image_id"]

        if rec["state"] in {"RESERVED", "CONSUMED"}:
            if not (rec.get("consumer_unit_id") or rec.get("consumers")):
                fail(f"{path.name}:{rec['asset_id']} {rec['state']} requires consumer identity")
        if rec["state"] == "LEGACY_MULTI_CONSUMED" and len(rec.get("consumers", [])) < 2:
            fail(f"{path.name}:{rec['asset_id']} legacy multi-consumed requires 2+ consumers")
        if rec["state"] == "REJECTED_NOT_ELIGIBLE" and "DO_NOT_REUSE" not in rec["reuse_lock"]:
            fail(f"{path.name}:{rec['asset_id']} rejected image must be do-not-reuse")
    return ledger


def validate_c04(ledger: dict) -> None:
    by_id = {r["asset_id"]: r for r in ledger["records"]}
    required = {"IMG-C04-D-HERO-01", "IMG-C04-F01-SCENIC-01", "IMG-C04-PHYS-RECOVERY-TECH-01"}
    if not required.issubset(by_id):
        fail(f"C04 seed ledger missing {sorted(required - set(by_id))}")

    hero = by_id["IMG-C04-D-HERO-01"]
    if hero.get("state") != "LEGACY_MULTI_CONSUMED" or hero.get("reuse_lock") != "LOCKED_NO_FURTHER_USE":
        fail("C04 D Hero must be legacy-multi-consumed and locked from further use")

    scenic = by_id["IMG-C04-F01-SCENIC-01"]
    if scenic.get("state") != "REJECTED_NOT_ELIGIBLE" or scenic.get("reuse_lock") != "DO_NOT_REUSE":
        fail("C04 F01 scenic image must be rejected/not eligible")

    tech = by_id["IMG-C04-PHYS-RECOVERY-TECH-01"]
    if tech.get("state") != "RESERVED" or tech.get("consumer_unit_id") != "CH13-01":
        fail("C04 Physical Recovery technical figure must be reserved to CH13-01")


def main() -> None:
    validate_resolver()
    reg = validate_register()
    validate_cases(reg)
    c04 = validate_ledger(C04_LEDGER, reg)
    validate_c04(c04)
    print("image-consumption validation: PASS")
    print("existing visual authority: ENFORCED")
    print("semantic image uniqueness: ENFORCED")
    print("derivative identity inheritance: ENFORCED")
    print("C04 ledger: PASS")


if __name__ == "__main__":
    main()
