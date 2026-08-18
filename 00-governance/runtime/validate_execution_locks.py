#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
RESOLVER = RUNTIME / "OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json"
RECEIPT_CONTRACT = RUNTIME / "OLEANDER_EXECUTION_RECEIPT_v1.0.json"
RECEIPT_DIR = RUNTIME / "receipts"
CASES = ROOT / "evals" / "runtime" / "sticky_constraints_and_flow.jsonl"


def fail(msg: str) -> None:
    raise SystemExit(f"execution-lock validation failed: {msg}")


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


def require_present(obj: dict, fields: list[str], context: str) -> None:
    missing = [f for f in fields if f not in obj or obj[f] in (None, "")]
    if missing:
        fail(f"{context} missing fields {missing}")


def validate_resolver() -> dict:
    data = load_json(RESOLVER)
    if data.get("version") != "1.2" or data.get("implementation_revision") != "1.2.1":
        fail("Current resolver must be v1.2 implementation revision 1.2.1")
    if data.get("status") != "ACTIVE_CURRENT":
        fail("Current resolver must remain ACTIVE_CURRENT")

    sticky = data.get("sticky_execution_constraints", {})
    if not sticky.get("required") or not sticky.get("resolve_before_owner_or_tool_selection"):
        fail("sticky execution constraints must be mandatory and pre-routing")
    required_rules = {
        "NO_IMAGE_GENERATION",
        "NO_NEW_SKILL",
        "NO_NEW_METHOD",
        "NO_NEW_FRAMEWORK",
        "USE_EXISTING_OLEANDER_METHODS_AND_SKILLS",
        "FULL_OLEANDER_FLOW_REQUIRED",
        "NO_PRODUCER_SELF_PROMOTION",
    }
    if not required_rules.issubset(set(sticky.get("normalized_rules", []))):
        fail("resolver sticky normalized rules incomplete")
    if sticky.get("generic_continue_does_not_revoke") is not True:
        fail("generic continue must not revoke constraints")
    if "ONLY_A_LATER_EXPLICIT_USER_INSTRUCTION" not in sticky.get("revocation_rule", ""):
        fail("constraint revocation must require later explicit user instruction")
    hard_effects = sticky.get("hard_effects", {})
    if "BLOCK_IMAGE_GENERATION_TOOLS" not in hard_effects.get("NO_IMAGE_GENERATION", ""):
        fail("NO_IMAGE_GENERATION must hard-block image generation tools")
    if "BLOCK_NEW_SKILL_CREATION" not in hard_effects.get("NO_NEW_SKILL", ""):
        fail("NO_NEW_SKILL must hard-block new Skill creation")

    flow = data.get("flow_completion_gate", {})
    if flow.get("does_not_mean_all_skills") is not True or flow.get("minimum_owner_set_still_applies") is not True:
        fail("full flow must not expand into all-Skill pipeline")
    phases = flow.get("phases", [])
    core = flow.get("core_phases_cannot_be_skipped_for_full_flow", [])
    required_phases = {
        "AUTHORITY_PREFLIGHT",
        "STICKY_CONSTRAINT_RESOLUTION",
        "EXISTING_KNOWLEDGE_METHOD_SKILL_RESOLUTION",
        "REQUIRED_NATIVE_OUTPUT_DEFINITION",
        "CAPABILITY_AND_MINIMUM_OWNER_SET",
        "REAL_EXECUTION",
        "ACTUAL_READBACK",
    }
    if not required_phases.issubset(set(phases)) or not required_phases.issubset(set(core)):
        fail("full-flow core phases incomplete")
    early = set(flow.get("early_stop_states_that_do_not_equal_completion", []))
    if not {"PR_OPENED", "CI_GREEN", "SELF_CHECK_PASS", "ARTIFACT_CREATED", "REGRESSION_PASS"}.issubset(early):
        fail("early-completion denylist incomplete")

    order = data.get("default_resolution_order", [])
    required_order = [
        "READ_APPLICABLE_PROJECT_STATE_SOURCE_AUTHORITY_CURRENT_TASK",
        "RESOLVE_STICKY_EXECUTION_CONSTRAINTS",
        "ENFORCE_TOOL_OUTPUT_CREATION_AND_PROCESS_LOCKS",
        "VERIFY_REQUIRED_EXISTING_METHOD_AND_SKILL_FILES_WERE_ACTUALLY_READ",
        "DEFINE_REQUIRED_NATIVE_OUTPUT",
        "BUILD_APPLICABLE_FLOW_COMPLETION_CHECKLIST",
        "RESOLVE_EXECUTION_OWNER_MAP",
        "EXECUTE_ACTUAL_NATIVE_ARTIFACT",
        "ACTUAL_READBACK",
        "VERIFY_FLOW_COMPLETION_GATE_BEFORE_CLOSURE_OR_COMPLETE_CLAIM",
        "EMIT_EXECUTION_RECEIPT_WITH_CONSTRAINT_LOCK_AND_FLOW_COMPLETION",
    ]
    positions = []
    for token in required_order:
        if token not in order:
            fail(f"resolver order missing {token}")
        positions.append(order.index(token))
    if positions != sorted(positions):
        fail("sticky constraint / full-flow resolver order is invalid")
    return data


def validate_receipt_contract() -> dict:
    data = load_json(RECEIPT_CONTRACT)
    if data.get("version") != "1.0" or data.get("policy_revision") != "1.1":
        fail("Execution Receipt must be v1.0 policy revision 1.1")
    core = set(data.get("required_core_fields", []))
    if not {"constraint_lock", "flow_completion"}.issubset(core):
        fail("new Receipt core must require constraint_lock and flow_completion")
    legacy = set(data.get("legacy_receipts_without_policy_1_1_fields", []))
    expected_legacy = {
        "EXR-20260818-PR246-IMAGE-OPS-ADAPTER",
        "EXR-20260818-PR248-CONTRACT-LAYER",
        "EXR-20260818-SKILL-RUNTIME-CLOSURE-v1.2",
    }
    if legacy != expected_legacy:
        fail("legacy Receipt allowlist must be explicit and exact")
    if data.get("closed_state_rule") != "IF_STATUS_IS_CLOSED_COMPLETION_GATE_MUST_BE_PASS_AND_INCOMPLETE_REQUIRED_PHASES_MUST_BE_EMPTY":
        fail("Receipt CLOSED state rule missing")
    return data


def validate_cases() -> None:
    rows = load_jsonl(CASES)
    if len(rows) < 6:
        fail("sticky/full-flow regression corpus must have at least six cases")
    ids = {r.get("case_id") for r in rows}
    required = {
        "LOCK-001-NO-IMAGE-STICKY",
        "LOCK-002-NO-NEW-SKILL-STICKY",
        "LOCK-003-EXPLICIT-REVOCATION-ONLY",
        "FLOW-001-FULL-FLOW-NO-EARLY-CLOSE",
        "FLOW-002-FULL-FLOW-MINIMUM-OWNERS",
        "FLOW-003-EXISTING-SKILL-READBACK",
    }
    if not required.issubset(ids):
        fail(f"missing runtime cases {sorted(required - ids)}")
    by_id = {r["case_id"]: r for r in rows}
    if "NO_IMAGE_GENERATION" not in by_id["LOCK-001-NO-IMAGE-STICKY"].get("expected_active_constraints", []):
        fail("no-image sticky case does not preserve lock")
    if "CREATE_NEW_SKILL" not in by_id["LOCK-002-NO-NEW-SKILL-STICKY"].get("forbidden_actions", []):
        fail("no-new-skill case must block creation")
    if by_id["FLOW-001-FULL-FLOW-NO-EARLY-CLOSE"].get("expected_completion_gate") != "HOLD":
        fail("PR/CI early close case must HOLD")
    if "AUTOMATICALLY_RUN_MOTION" not in by_id["FLOW-002-FULL-FLOW-MINIMUM-OWNERS"].get("forbidden_actions", []):
        fail("full-flow minimum-owner case must forbid unnecessary Motion")


def validate_new_receipts(contract: dict) -> int:
    legacy = set(contract.get("legacy_receipts_without_policy_1_1_fields", []))
    constraint_fields = contract.get("constraint_lock_required_fields", [])
    flow_fields = contract.get("flow_completion_required_fields", [])
    constraint_record_fields = contract.get("constraint_record_required_fields", [])
    phase_values = set(contract.get("phase_result_values", []))
    current_policy_count = 0

    for path in sorted(RECEIPT_DIR.glob("*.json")):
        r = load_json(path)
        rid = r.get("receipt_id")
        if rid in legacy:
            continue
        current_policy_count += 1
        require_present(r, ["constraint_lock", "flow_completion"], f"receipt:{rid}")
        lock = r["constraint_lock"]
        require_present(lock, constraint_fields, f"receipt:{rid}:constraint_lock")
        for item in lock.get("active_constraints", []):
            require_present(item, constraint_record_fields, f"receipt:{rid}:constraint")
        flow = r["flow_completion"]
        require_present(flow, flow_fields, f"receipt:{rid}:flow_completion")
        for phase, result in flow.get("phase_results", {}).items():
            if result not in phase_values:
                fail(f"receipt:{rid} invalid phase result {phase}={result}")
        if r.get("status") == "CLOSED":
            if flow.get("completion_gate") != "PASS":
                fail(f"receipt:{rid} CLOSED requires completion_gate PASS")
            if flow.get("incomplete_required_phases"):
                fail(f"receipt:{rid} CLOSED cannot have incomplete required phases")
            if flow.get("completion_claim_allowed") is not True:
                fail(f"receipt:{rid} CLOSED requires completion_claim_allowed=true")
    if current_policy_count < 1:
        fail("at least one policy-1.1 execution receipt is required to prove adoption")
    return current_policy_count


def main() -> None:
    validate_resolver()
    contract = validate_receipt_contract()
    validate_cases()
    count = validate_new_receipts(contract)
    print("execution-lock validation: PASS")
    print("sticky negative constraints: ENFORCED")
    print("full-flow completion gate: ENFORCED")
    print(f"policy-1.1 receipts: {count}")


if __name__ == "__main__":
    main()
