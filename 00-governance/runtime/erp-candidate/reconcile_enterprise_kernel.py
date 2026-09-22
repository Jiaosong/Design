from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BLOCKING_REVIEW_RESULTS = {"REVISE", "REJECT", "HOLD", "FAIL", "FAILED"}
BLOCKING_WORK_STATES = {"BLOCKED", "HOLD", "FAILED", "REJECTED"}
BLOCKING_CHANGE_STATES = {"OPEN", "HOLD", "IMPLEMENTED_READBACK_PENDING"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return text.encode("utf-8")


def canonical_sha256(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest().upper()


def token(value: str) -> str:
    return "".join(ch if ch.isalnum() else "-" for ch in value).strip("-").upper() or "UNRESOLVED"


def project_subject(kernel: dict) -> str:
    for row in kernel.get("identities", []):
        if row.get("identity_class") == "PROJECT":
            return row["canonical_ref"]
    return kernel.get("source_projection_ref", "ENTERPRISE_KERNEL_SUBJECT_UNRESOLVED")


def authority_for_scope(kernel: dict, scope: str, default: str) -> str:
    for row in kernel.get("authority_bindings", []):
        if row.get("authority_scope") == scope:
            return row["authority_owner_ref"]
    return default


def parse_json_maybe(value: str):
    try:
        return json.loads(value)
    except Exception:
        return None


def reconcile(kernel: dict, kernel_ref: str, kernel_sha256: str, generated_at: str | None = None) -> dict:
    if kernel.get("kind") != "OLEANDER_ENTERPRISE_KERNEL":
        raise ValueError("input must be OLEANDER_ENTERPRISE_KERNEL")
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()
    subject = project_subject(kernel)
    project_authority = authority_for_scope(kernel, "PROJECT", "Project Authority / Project State")

    blockers: list[dict] = []
    reopen: set[str] = set()
    rerun: set[str] = set()
    review: set[str] = set()
    readback: set[str] = set()
    authority_conflicts: set[str] = set()
    reasons: set[str] = set()

    def add_blocker(blocker_class: str, subject_ref: str, observed_state: str, authority_ref: str, source_refs: list[str], claim_ceiling: str, suffix: str = "") -> None:
        key = f"{blocker_class}:{subject_ref}:{observed_state}:{suffix}"
        blockers.append({
            "blocker_id": f"BLOCK-{token(key)}",
            "blocker_class": blocker_class,
            "subject_ref": subject_ref,
            "observed_state": observed_state,
            "blocking_authority_ref": authority_ref,
            "source_refs": source_refs or [kernel_ref],
            "claim_ceiling": claim_ceiling,
        })
        reasons.add(blocker_class)

    for fact in kernel.get("state_facts", []):
        family = fact.get("state_family")
        value = str(fact.get("state_value", ""))
        upper = value.upper()
        sources = list(fact.get("source_refs", []))
        if family == "PROJECTION_FRESHNESS" and value != "SOURCE_READBACK_CURRENT":
            add_blocker("SOURCE_STALE", fact["subject_ref"], value, "Source Projection / Readback Owner", sources, "SOURCE_FRESHNESS_HOLD_NO_ADVANCE")
        if family == "INTERFACE" and value.startswith("BLOCKING_RELATION:"):
            add_blocker("UNRESOLVED_BLOCKING_RELATION", fact["subject_ref"], value, project_authority, sources, "INTERFACE_HOLD_NO_ADVANCE")
            review.add(fact["subject_ref"])
        if family == "INTERFACE":
            parsed = parse_json_maybe(value)
            if isinstance(parsed, dict) and int(parsed.get("unresolved_authority_conflicts", 0) or 0) > 0:
                authority_conflicts.add(fact["subject_ref"])
                add_blocker("AUTHORITY_CONFLICT", fact["subject_ref"], value, project_authority, sources, "AUTHORITY_CONFLICT_HOLD_NO_ADVANCE")
        if family == "QUALITY" and upper.startswith("NCR:") and not upper.endswith(":CLOSED"):
            add_blocker("QUALITY_NONCONFORMANCE", fact["subject_ref"], value, "Review owners / domain specialist acceptance owner", sources, "QUALITY_HOLD_NO_PROFESSIONAL_OR_PROMOTION_INFERENCE")
            review.add(fact["subject_ref"])
        if family == "QUALITY" and upper.startswith("CAPA:") and ":CLOSED:" not in upper:
            add_blocker("QUALITY_NONCONFORMANCE", fact["subject_ref"], value, "Review owners / domain specialist acceptance owner", sources, "CAPA_OPEN_NO_QUALITY_CLOSURE")
            review.add(fact["subject_ref"])

    for item in kernel.get("work_items", []):
        state = str(item.get("work_state", "")).upper()
        if state in BLOCKING_WORK_STATES:
            cls = "PROCESS_BLOCKED" if item.get("work_class") in {"PROCESS_INSTANCE", "HANDOFF", "EXCEPTION"} else "WORK_BLOCKED"
            authority = "Master Runtime" if cls == "PROCESS_BLOCKED" else project_authority
            add_blocker(cls, item["subject_ref"], state, authority, list(item.get("source_refs", [])), "WORK_OR_PROCESS_HOLD_NO_ADVANCE", item["work_id"])
            rerun.add(item["work_id"])
        if item.get("work_class") == "EXCEPTION" and state not in {"CLOSED", "CONTAINED"}:
            add_blocker("PROCESS_BLOCKED", item["subject_ref"], f"EXCEPTION:{state}", "Master Runtime", list(item.get("source_refs", [])), "OPEN_EXCEPTION_HOLD_NO_ADVANCE", item["work_id"])
            rerun.add(item["work_id"])

    for receipt in kernel.get("receipts", []):
        result = str(receipt.get("result", "")).upper()
        if receipt.get("receipt_class") == "REVIEW" and result in BLOCKING_REVIEW_RESULTS:
            add_blocker("DESIGN_REVIEW", receipt["subject_ref"], result, receipt.get("receipt_id") or "Independent Review boundary", list(receipt.get("source_refs", [])), "REVIEW_HOLD_NO_DESIGN_KEEP_OR_PROMOTION")
            review.add(receipt["subject_ref"])

    for evidence in kernel.get("evidence_items", []):
        result = str(evidence.get("result", "")).upper()
        if evidence.get("evidence_class") == "REVIEW" and result in BLOCKING_REVIEW_RESULTS:
            add_blocker("QUALITY_REVIEW", evidence["subject_ref"], result, "Review owners / domain specialist acceptance owner", list(evidence.get("source_refs", [])), evidence.get("claim_ceiling") or "QUALITY_REVIEW_HOLD")
            review.add(evidence["subject_ref"])

    observed_readbacks = {row.get("readback_id") for row in kernel.get("readbacks", []) if row.get("readback_state") == "OBSERVED"}
    for change in kernel.get("changes", []):
        state = str(change.get("change_state", "")).upper()
        reopen.update(change.get("reopen_refs", []))
        if state in BLOCKING_CHANGE_STATES:
            add_blocker("CHANGE_READBACK_PENDING", change["change_id"], state, "Project Configuration / Change Register", list(change.get("source_refs", [])), "CHANGE_NOT_CLOSED_NO_ADVANCE")
            if state == "IMPLEMENTED_READBACK_PENDING":
                explicit = set(change.get("required_readback_refs", []))
                if explicit:
                    readback.update(explicit - observed_readbacks)
                else:
                    readback.add(change["change_id"])
            rerun.update(change.get("affected_refs", []))

    blockers_by_id = {row["blocker_id"]: row for row in blockers}
    blockers = sorted(blockers_by_id.values(), key=lambda row: row["blocker_id"])
    reopen_set = sorted(x for x in reopen if x)
    rerun_set = sorted(x for x in rerun if x)
    review_set = sorted(x for x in review if x)
    readback_set = sorted(x for x in readback if x)
    conflicts = sorted(x for x in authority_conflicts if x)

    can_advance = not blockers and not reopen_set and not rerun_set and not review_set and not readback_set and not conflicts
    advance = "ALLOW" if can_advance else "HOLD"
    claim_ceiling = (
        "PHASE1_COORDINATION_CLEAR_WITHIN_OBSERVED_SCOPE_ONLY_NO_DESIGN_PROFESSIONAL_OR_PROMOTION_AUTHORITY"
        if can_advance
        else "PHASE1_COORDINATION_HOLD_NO_DESIGN_PROFESSIONAL_OR_PROMOTION_AUTHORITY"
    )
    if can_advance:
        reasons.add("NO_PHASE1_BLOCKERS_OBSERVED")

    return {
        "schema_version": "0.1-candidate",
        "kind": "OLEANDER_ENTERPRISE_RECONCILIATION_DECISION",
        "candidate_status": "EVAL_ONLY",
        "generated_at": generated_at,
        "kernel_ref": kernel_ref,
        "kernel_digest": {"sha256": kernel_sha256, "hash_semantics": "UTF8_TEXT_LF_CANONICAL_V1"},
        "subject_ref": subject,
        "advance_decision": advance,
        "blocking_conditions": blockers,
        "reopen_set": reopen_set,
        "rerun_set": rerun_set,
        "review_set": review_set,
        "required_readback_set": readback_set,
        "unresolved_authority_conflicts": conflicts,
        "claim_ceiling": claim_ceiling,
        "reason_codes": sorted(reasons),
        "source_refs": [kernel_ref],
        "authority_boundary": {"decision_is_authority": False, "may_mutate_current": False, "advance_rule": "ALLOW_ONLY_WHEN_NO_BLOCKERS_AND_NO_REQUIRED_REOPEN_RERUN_REVIEW_READBACK"},
        "does_not_prove": ["CURRENT_ADOPTION", "DESIGN_KEEP", "PROFESSIONAL_PASS", "PROJECT_PROMOTION", "STATUTORY_APPROVAL", "REAL_CASE_GENERALIZATION"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconcile an OLEANDER Enterprise Kernel v0.1 candidate.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--generated-at")
    args = parser.parse_args()
    kernel = load_json(args.input)
    decision = reconcile(kernel, args.input.as_posix(), canonical_sha256(args.input), args.generated_at)
    payload = (json.dumps(decision, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if not args.output.is_file() or args.output.read_bytes() != payload:
            args.output.write_bytes(payload)
        print(args.output)
    else:
        print(payload.decode("utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
