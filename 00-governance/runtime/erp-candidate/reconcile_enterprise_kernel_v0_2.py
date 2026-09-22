from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from reconcile_enterprise_kernel import (
    blocker_authority_spec,
    canonical_sha256,
    effective_authority_ref,
    load_json,
    reconcile as reconcile_phase1,
    resolve_authority,
    token,
)


ROOT = Path(__file__).resolve().parent
POLICY_PATH = ROOT / "OLEANDER_ENTERPRISE_RECONCILIATION_POLICY_v0.2.json"
POLICY_REF = "00-governance/runtime/erp-candidate/OLEANDER_ENTERPRISE_RECONCILIATION_POLICY_v0.2.json"


def reconcile_v0_2(kernel: dict, kernel_ref: str, kernel_sha256: str, generated_at: str | None = None) -> dict:
    if kernel.get("schema_version") != "0.2-candidate":
        raise ValueError("Phase-2 reconciliation requires Enterprise Kernel v0.2")
    policy = load_json(POLICY_PATH)
    decision = reconcile_phase1(
        kernel,
        kernel_ref,
        kernel_sha256,
        generated_at,
        policy=policy,
        policy_ref=POLICY_REF,
        policy_sha256=canonical_sha256(POLICY_PATH),
    )
    decision["schema_version"] = "0.2-candidate"

    identities = {row["canonical_ref"]: row["identity_class"] for row in kernel.get("identities", [])}
    blockers = {row["blocker_id"]: row for row in decision.get("blocking_conditions", [])}
    actions = {(row["action_type"], row["subject_ref"]): row for row in decision.get("action_requests", [])}
    reason_codes = set(decision.get("reason_codes", []))
    unresolved_map: dict[tuple[str, str, str, str], dict] = {}
    for row in decision.get("unresolved_authority_requirements", []):
        key = (row["subject_ref"], row["required_owner_kind"], row["authority_contract_ref"], row["scope"])
        unresolved_map[key] = dict(row)

    def register_unresolved(authority: dict, subject_ref: str, trigger_ref: str) -> None:
        if authority.get("resolution_state") != "UNRESOLVED_REQUIRED_OWNER":
            return
        key = (subject_ref, authority["required_owner_kind"], authority["authority_contract_ref"], authority["scope"])
        rid = f"AUTHREQ-{token(subject_ref)}-{token(authority['required_owner_kind'])}-{token(authority['authority_contract_ref'])}-{token(authority['scope'])}"
        row = unresolved_map.get(key, {
            "requirement_id": rid,
            "subject_ref": subject_ref,
            "required_owner_kind": authority["required_owner_kind"],
            "authority_contract_ref": authority["authority_contract_ref"],
            "scope": authority["scope"],
            "trigger_ref": trigger_ref,
            "trigger_refs": [],
        })
        row["trigger_refs"] = sorted(set(row.get("trigger_refs", []) + [trigger_ref]))
        row["trigger_ref"] = row["trigger_refs"][0]
        unresolved_map[key] = row

    def add_blocker(blocker_class: str, subject_ref: str, observed_state: str, source_refs: list[str], claim_ceiling: str, state_fact_ref: str | None = None) -> str:
        spec = blocker_authority_spec(policy, blocker_class)
        authority = resolve_authority(kernel, spec)
        bid = f"BLOCK-{token(blocker_class)}-{token(subject_ref)}-{token(observed_state)}"
        if state_fact_ref:
            bid += f"-{token(state_fact_ref)}"
        blockers[bid] = {
            "blocker_id": bid,
            "blocker_class": blocker_class,
            "subject_ref": subject_ref,
            "observed_state": observed_state,
            "blocking_authority_ref": effective_authority_ref(authority),
            "blocking_authority": authority,
            "source_refs": sorted(set(source_refs or [kernel_ref])),
            "claim_ceiling": claim_ceiling,
            "state_fact_ref": state_fact_ref,
        }
        register_unresolved(authority, subject_ref, bid)
        reason_codes.add(blocker_class)
        return bid

    def add_action(action_type: str, subject_ref: str, trigger_ref: str, reason_code: str, source_refs: list[str], requested_output_class: str | None = None) -> str:
        key = (action_type, subject_ref)
        spec = policy["action_authority"][action_type]
        authority = resolve_authority(kernel, spec)
        aid = f"ACTION-{token(action_type)}-{token(subject_ref)}"
        if key not in actions:
            actions[key] = {
                "action_id": aid,
                "action_type": action_type,
                "subject_ref": subject_ref,
                "subject_identity_class": identities.get(subject_ref, "UNRESOLVED"),
                "trigger_refs": [],
                "reason_codes": [],
                "authority": authority,
                "source_refs": [],
                "relation_paths": [[]],
                "requested_output_class": requested_output_class,
                "claim_ceiling": "COORDINATION_ACTION_REQUIRED_ONLY_NO_AUTOMATIC_ACCEPTANCE_OR_PROMOTION",
            }
        row = actions[key]
        row["trigger_refs"] = sorted(set(row["trigger_refs"] + [trigger_ref]))
        row["reason_codes"] = sorted(set(row["reason_codes"] + [reason_code]))
        row["source_refs"] = sorted(set(row["source_refs"] + (source_refs or [kernel_ref])))
        if requested_output_class and not row.get("requested_output_class"):
            row["requested_output_class"] = requested_output_class
        register_unresolved(authority, subject_ref, aid)
        reason_codes.add(reason_code)
        return aid

    observed_readbacks = {
        row["readback_id"]
        for row in kernel.get("readbacks", [])
        if row.get("readback_state") == "OBSERVED"
    }

    # MES COMPLETE is not coordination-clear unless every declared actual readback is observed.
    for work in kernel.get("work_items", []):
        if work.get("work_class") != "OPERATION" or str(work.get("work_state", "")).upper() != "COMPLETE":
            continue
        declared = list(work.get("readback_refs", []))
        missing = [ref for ref in declared if ref not in observed_readbacks]
        if not declared or missing:
            state = "COMPLETE_WITHOUT_OBSERVED_READBACK:" + (",".join(missing) if missing else "NONE_DECLARED")
            bid = add_blocker("MES_READBACK_MISSING", work["work_id"], state, list(work.get("source_refs", [])), "MES_COMPLETE_REQUIRES_ACTUAL_OBSERVED_READBACK")
            if missing:
                for ref in missing:
                    add_action("REQUIRE_READBACK", ref, bid, "MES_COMPLETE_REQUIRES_READBACK", list(work.get("source_refs", [])), "READBACK")
            else:
                add_action("REQUIRE_READBACK", work["work_id"], bid, "MES_COMPLETE_REQUIRES_READBACK", list(work.get("source_refs", [])), "READBACK")

    # MBSE Verification and Validation are separate gates and remain fail-closed when a record is not PASS.
    for fact in kernel.get("state_facts", []):
        if fact.get("state_family") != "VALIDATION" or not str(fact.get("claim_scope", "")).startswith("MBSE_VV:"):
            continue
        vv_class = fact["claim_scope"].split(":", 1)[1]
        result = str(fact.get("state_value", "")).split(":", 1)[-1].upper()
        if result == "PASS":
            continue
        blocker_class = "MBSE_VERIFICATION_INCOMPLETE" if vv_class == "VERIFICATION" else "MBSE_VALIDATION_INCOMPLETE"
        bid = add_blocker(blocker_class, fact["subject_ref"], fact["state_value"], list(fact.get("source_refs", [])), f"MBSE_{vv_class}_MUST_PASS_WITH_EVIDENCE_BEFORE_ADVANCE", fact.get("state_fact_id"))
        add_action("REVIEW_SUBJECT", fact["subject_ref"], bid, f"MBSE_{vv_class}_REQUIRES_REVIEW", list(fact.get("source_refs", [])))

    # Agent success cannot clear uncertain side effects; lease conflicts are independent blockers.
    for fact in kernel.get("state_facts", []):
        if fact.get("state_family") != "AGENT_RUNTIME":
            continue
        value = str(fact.get("state_value", "")).upper()
        scope = str(fact.get("claim_scope", ""))
        if scope == "AGENT_ACTION" and "OBSERVED_UNCERTAIN" in value:
            bid = add_blocker("AGENT_SIDE_EFFECT_UNCERTAIN", fact["subject_ref"], fact["state_value"], list(fact.get("source_refs", [])), "UNCERTAIN_AGENT_SIDE_EFFECT_REQUIRES_RECOVERY_READBACK", fact.get("state_fact_id"))
            add_action("REQUIRE_READBACK", fact["subject_ref"], bid, "AGENT_UNCERTAIN_SIDE_EFFECT_REQUIRES_READBACK", list(fact.get("source_refs", [])), "READBACK")
        if scope == "AGENT_LEASE" and "LEASE:CONFLICT" in value:
            bid = add_blocker("AGENT_LEASE_CONFLICT", fact["subject_ref"], fact["state_value"], list(fact.get("source_refs", [])), "AGENT_LEASE_CONFLICT_MUST_BE_RESOLVED_BEFORE_MUTATION")
            add_action("REVIEW_SUBJECT", fact["subject_ref"], bid, "AGENT_LEASE_CONFLICT_REQUIRES_RESOLUTION", list(fact.get("source_refs", [])))

    decision["blocking_conditions"] = sorted(blockers.values(), key=lambda row: row["blocker_id"])
    decision["action_requests"] = sorted(actions.values(), key=lambda row: row["action_id"])
    decision["unresolved_authority_requirements"] = sorted(unresolved_map.values(), key=lambda row: row["requirement_id"])
    decision["reason_codes"] = sorted(reason_codes)
    decision["reopen_set"] = sorted({a["subject_ref"] for a in decision["action_requests"] if a["action_type"] == "REOPEN_REVIEW"})
    decision["rerun_set"] = sorted({a["subject_ref"] for a in decision["action_requests"] if a["action_type"] == "RERUN_WORK"})
    decision["review_set"] = sorted({a["subject_ref"] for a in decision["action_requests"] if a["action_type"] == "REVIEW_SUBJECT"})
    decision["required_readback_set"] = sorted({a["subject_ref"] for a in decision["action_requests"] if a["action_type"] == "REQUIRE_READBACK"})
    can_advance = not decision["blocking_conditions"] and not decision["action_requests"] and not decision["contradictions"] and not decision["unresolved_authority_conflicts"] and not decision["unresolved_authority_requirements"]
    decision["advance_decision"] = "ALLOW" if can_advance else "HOLD"
    decision["claim_ceiling"] = (
        "PHASE2_COORDINATION_CLEAR_WITHIN_OBSERVED_SCOPE_ONLY_NO_DESIGN_PROFESSIONAL_OR_PROMOTION_AUTHORITY"
        if can_advance
        else "PHASE2_COORDINATION_HOLD_NO_DESIGN_PROFESSIONAL_OR_PROMOTION_AUTHORITY"
    )
    decision["does_not_prove"] = sorted(set(decision["does_not_prove"] + [
        "PHYSICAL_EXECUTION_ACCEPTANCE", "SYSTEMS_ENGINEERING_CURRENT", "KNOWLEDGE_CURRENT", "AGENT_MUTATION_AUTHORITY"
    ]))
    return decision


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconcile OLEANDER Enterprise Kernel v0.2 across all eight modules.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--generated-at")
    args = parser.parse_args()
    kernel = load_json(args.input)
    decision = reconcile_v0_2(kernel, args.input.as_posix(), canonical_sha256(args.input), args.generated_at)
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
