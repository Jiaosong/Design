from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_POLICY_PATH = ROOT / "OLEANDER_ENTERPRISE_RECONCILIATION_POLICY_v0.1.json"
DEFAULT_POLICY_REF = "00-governance/runtime/erp-candidate/OLEANDER_ENTERPRISE_RECONCILIATION_POLICY_v0.1.json"

BLOCKING_REVIEW_RESULTS = {"REVISE", "REJECT", "HOLD", "FAIL", "FAILED"}
BLOCKING_WORK_STATES = {"BLOCKED", "HOLD", "FAILED", "REJECTED"}
BLOCKING_CHANGE_STATES = {"OPEN", "HOLD", "IMPLEMENTED_READBACK_PENDING"}
POSITIVE_STATE_TOKENS = {"PASS", "KEEP", "CLOSED", "VERIFIED", "ACTIVE", "CURRENT", "RELEASED", "READY", "COMPLETE", "COMPLETED", "SUCCEEDED"}


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


def parse_json_maybe(value: str):
    try:
        return json.loads(value)
    except Exception:
        return None


def authority_bindings_by_scope(kernel: dict) -> dict[str, list[dict]]:
    result: dict[str, list[dict]] = defaultdict(list)
    for row in kernel.get("authority_bindings", []):
        result[str(row.get("authority_scope", ""))].append(row)
    return result


def resolve_authority(kernel: dict, spec: dict) -> dict:
    scope = str(spec.get("scope", "PROJECT"))
    contract = str(spec.get("authority_contract_ref", "AUTHORITY_CONTRACT_UNRESOLVED"))
    owner_kind = str(spec.get("required_owner_kind", "OWNER_UNRESOLVED"))
    if owner_kind == "DERIVED_COORDINATION_ONLY":
        return {
            "resolution_state": "DERIVED_COORDINATION_ONLY",
            "owner_ref": None,
            "authority_contract_ref": contract,
            "required_owner_kind": owner_kind,
            "scope": scope,
        }
    bindings = authority_bindings_by_scope(kernel).get(scope, [])
    if bindings:
        return {
            "resolution_state": "RESOLVED_EXISTING_BINDING",
            "owner_ref": bindings[0]["authority_owner_ref"],
            "authority_contract_ref": contract,
            "required_owner_kind": owner_kind,
            "scope": scope,
        }
    return {
        "resolution_state": "UNRESOLVED_REQUIRED_OWNER",
        "owner_ref": None,
        "authority_contract_ref": contract,
        "required_owner_kind": owner_kind,
        "scope": scope,
    }


def effective_authority_ref(authority: dict) -> str:
    return authority.get("owner_ref") or authority["authority_contract_ref"]


def state_has_positive_signal(value: str) -> bool:
    upper = value.upper()
    tokens = set(re.findall(r"[A-Z_]+", upper))
    if tokens & {"HOLD", "BLOCKED", "FAIL", "FAILED", "REJECT", "REVISE", "STALE", "DIVERGED", "MISSING"}:
        return False
    return bool(tokens & POSITIVE_STATE_TOKENS)


def state_authority_spec(policy: dict, family: str) -> dict:
    return policy.get("state_family_authority", {}).get(
        family,
        {
            "scope": "PROJECT",
            "authority_contract_ref": "00-governance/complex-project-master-runtime-v1.0.md",
            "required_owner_kind": "STATE_FAMILY_OWNER",
        },
    )


def blocker_authority_spec(policy: dict, blocker_class: str, family: str | None = None) -> dict:
    if blocker_class == "STATE_FACET_BLOCKER" and family:
        return state_authority_spec(policy, family)
    specific = policy.get("specific_blocker_authority", {}).get(blocker_class)
    if specific:
        return specific
    if family:
        return state_authority_spec(policy, family)
    return {
        "scope": "PROJECT",
        "authority_contract_ref": "00-governance/complex-project-master-runtime-v1.0.md",
        "required_owner_kind": "PROJECT_AUTHORITY",
    }


def reconcile(
    kernel: dict,
    kernel_ref: str,
    kernel_sha256: str,
    generated_at: str | None = None,
    *,
    policy: dict | None = None,
    policy_ref: str = DEFAULT_POLICY_REF,
    policy_sha256: str | None = None,
) -> dict:
    if kernel.get("kind") != "OLEANDER_ENTERPRISE_KERNEL":
        raise ValueError("input must be OLEANDER_ENTERPRISE_KERNEL")
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()
    policy = policy or load_json(DEFAULT_POLICY_PATH)
    policy_sha256 = policy_sha256 or canonical_sha256(DEFAULT_POLICY_PATH)
    subject = project_subject(kernel)

    identities = {row["canonical_ref"]: row for row in kernel.get("identities", [])}
    work_ids = {row["work_id"] for row in kernel.get("work_items", [])}
    blockers: list[dict] = []
    contradictions: list[dict] = []
    action_map: dict[tuple[str, str], dict] = {}
    impact_traces: list[dict] = []
    authority_conflicts: set[str] = set()
    unresolved_authority_requirements: dict[str, dict] = {}
    reasons: set[str] = set()
    consumed_state_facts: set[str] = set()

    def register_unresolved_authority(authority: dict, subject_ref: str, trigger_ref: str) -> None:
        if authority.get("resolution_state") != "UNRESOLVED_REQUIRED_OWNER":
            return
        key = f"{authority['scope']}:{authority['required_owner_kind']}:{subject_ref}:{trigger_ref}"
        rid = f"AUTHREQ-{token(key)}"
        unresolved_authority_requirements[rid] = {
            "requirement_id": rid,
            "subject_ref": subject_ref,
            "required_owner_kind": authority["required_owner_kind"],
            "authority_contract_ref": authority["authority_contract_ref"],
            "scope": authority["scope"],
            "trigger_ref": trigger_ref,
        }

    def add_blocker(
        blocker_class: str,
        subject_ref: str,
        observed_state: str,
        source_refs: list[str],
        claim_ceiling: str,
        *,
        authority_spec: dict | None = None,
        family: str | None = None,
        state_fact_ref: str | None = None,
        suffix: str = "",
    ) -> str:
        authority = resolve_authority(kernel, authority_spec or blocker_authority_spec(policy, blocker_class, family))
        key = f"{blocker_class}:{subject_ref}:{observed_state}:{state_fact_ref or ''}:{suffix}"
        bid = f"BLOCK-{token(key)}"
        blockers.append({
            "blocker_id": bid,
            "blocker_class": blocker_class,
            "subject_ref": subject_ref,
            "observed_state": observed_state,
            "blocking_authority_ref": effective_authority_ref(authority),
            "blocking_authority": authority,
            "source_refs": sorted(set(source_refs or [kernel_ref])),
            "claim_ceiling": claim_ceiling,
            "state_fact_ref": state_fact_ref,
        })
        register_unresolved_authority(authority, subject_ref, bid)
        reasons.add(blocker_class)
        if state_fact_ref:
            consumed_state_facts.add(state_fact_ref)
        return bid

    def add_action(
        action_type: str,
        subject_ref: str,
        trigger_ref: str,
        reason_code: str,
        source_refs: list[str],
        relation_path: list[str] | None = None,
        requested_output_class: str | None = None,
    ) -> str:
        key = (action_type, subject_ref)
        spec = policy.get("action_authority", {}).get(action_type, blocker_authority_spec(policy, "STATE_FACET_BLOCKER"))
        authority = resolve_authority(kernel, spec)
        action_id = f"ACTION-{token(action_type)}-{token(subject_ref)}"
        if key not in action_map:
            action_map[key] = {
                "action_id": action_id,
                "action_type": action_type,
                "subject_ref": subject_ref,
                "subject_identity_class": identities.get(subject_ref, {}).get("identity_class", "UNRESOLVED"),
                "trigger_refs": [],
                "reason_codes": [],
                "authority": authority,
                "source_refs": [],
                "relation_paths": [],
                "requested_output_class": requested_output_class,
                "claim_ceiling": "COORDINATION_ACTION_REQUIRED_ONLY_NO_AUTOMATIC_ACCEPTANCE_OR_PROMOTION",
            }
        row = action_map[key]
        row["trigger_refs"] = sorted(set(row["trigger_refs"] + [trigger_ref]))
        row["reason_codes"] = sorted(set(row["reason_codes"] + [reason_code]))
        row["source_refs"] = sorted(set(row["source_refs"] + (source_refs or [kernel_ref])))
        path = relation_path or []
        if path not in row["relation_paths"]:
            row["relation_paths"].append(path)
        if requested_output_class and not row.get("requested_output_class"):
            row["requested_output_class"] = requested_output_class
        register_unresolved_authority(authority, subject_ref, action_id)
        reasons.add(reason_code)
        return action_id

    # 1) Consume specific state facts and preserve the state-fact source identity.
    for fact in kernel.get("state_facts", []):
        family = fact.get("state_family")
        value = str(fact.get("state_value", ""))
        upper = value.upper()
        sources = list(fact.get("source_refs", []))
        fact_id = fact.get("state_fact_id")
        if family == "PROJECTION_FRESHNESS" and value != "SOURCE_READBACK_CURRENT":
            add_blocker("SOURCE_STALE", fact["subject_ref"], value, sources, "SOURCE_FRESHNESS_HOLD_NO_ADVANCE", family=family, state_fact_ref=fact_id)
        if family == "INTERFACE" and value.startswith("BLOCKING_RELATION:"):
            add_blocker("UNRESOLVED_BLOCKING_RELATION", fact["subject_ref"], value, sources, "INTERFACE_HOLD_NO_ADVANCE", family=family, state_fact_ref=fact_id)
            add_action("REVIEW_SUBJECT", fact["subject_ref"], fact_id, "UNRESOLVED_BLOCKING_RELATION_REQUIRES_REVIEW", sources)
        if family == "INTERFACE":
            parsed = parse_json_maybe(value)
            if isinstance(parsed, dict) and int(parsed.get("unresolved_authority_conflicts", 0) or 0) > 0:
                authority_conflicts.add(fact["subject_ref"])
                add_blocker("AUTHORITY_CONFLICT", fact["subject_ref"], value, sources, "AUTHORITY_CONFLICT_HOLD_NO_ADVANCE", family=family, state_fact_ref=fact_id)
        if family == "QUALITY" and upper.startswith("NCR:") and not upper.endswith(":CLOSED"):
            add_blocker("QUALITY_NONCONFORMANCE", fact["subject_ref"], value, sources, "QUALITY_HOLD_NO_PROFESSIONAL_OR_PROMOTION_INFERENCE", family=family, state_fact_ref=fact_id)
            add_action("REVIEW_SUBJECT", fact["subject_ref"], fact_id, "OPEN_NCR_REQUIRES_REVIEW", sources)
        if family == "QUALITY" and upper.startswith("CAPA:") and ":CLOSED:" not in upper:
            add_blocker("QUALITY_NONCONFORMANCE", fact["subject_ref"], value, sources, "CAPA_OPEN_NO_QUALITY_CLOSURE", family=family, state_fact_ref=fact_id)
            add_action("REVIEW_SUBJECT", fact["subject_ref"], fact_id, "OPEN_CAPA_REQUIRES_REVIEW", sources)

    # 2) Detect contradictions before generic blocking-state consumption.
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for fact in kernel.get("state_facts", []):
        grouped[(fact["subject_ref"], fact["state_family"])].append(fact)
    for (subject_ref, family), facts in grouped.items():
        blocking = [f for f in facts if f.get("blocking_semantics") == "EXPLICIT"]
        positive = [f for f in facts if f.get("blocking_semantics") != "EXPLICIT" and state_has_positive_signal(str(f.get("state_value", "")))]
        if blocking and positive:
            fact_refs = sorted({f["state_fact_id"] for f in blocking + positive})
            observed = sorted({str(f["state_value"]) for f in blocking + positive})
            sources = sorted({src for f in blocking + positive for src in f.get("source_refs", [])})
            cid = f"CONTRA-{token(subject_ref)}-{token(family)}"
            contradictions.append({
                "contradiction_id": cid,
                "subject_ref": subject_ref,
                "state_family": family,
                "state_fact_refs": fact_refs,
                "observed_values": observed,
                "blocking": True,
                "source_refs": sources or [kernel_ref],
            })
            add_blocker("CROSS_CARRIER_CONTRADICTION", subject_ref, " | ".join(observed), sources, "CONTRADICTORY_CURRENT_STATE_HOLD_NO_ADVANCE", family=family, suffix=cid)

    # 3) Every unconsumed EXPLICIT state fact must block. This is the fail-closed floor.
    for fact in kernel.get("state_facts", []):
        fact_id = fact.get("state_fact_id")
        if fact.get("blocking_semantics") == "EXPLICIT" and fact_id not in consumed_state_facts:
            add_blocker(
                "STATE_FACET_BLOCKER",
                fact["subject_ref"],
                str(fact["state_value"]),
                list(fact.get("source_refs", [])),
                "EXPLICIT_STATE_FACT_HOLD_NO_ADVANCE",
                family=fact.get("state_family"),
                state_fact_ref=fact_id,
            )

    # 4) Work/process carrier checks.
    for item in kernel.get("work_items", []):
        state = str(item.get("work_state", "")).upper()
        if state in BLOCKING_WORK_STATES:
            cls = "PROCESS_BLOCKED" if item.get("work_class") in {"PROCESS_INSTANCE", "HANDOFF", "EXCEPTION"} else "WORK_BLOCKED"
            add_blocker(cls, item["subject_ref"], state, list(item.get("source_refs", [])), "WORK_OR_PROCESS_HOLD_NO_ADVANCE", suffix=item["work_id"])
            add_action("RERUN_WORK", item["work_id"], item["work_id"], "BLOCKED_WORK_REQUIRES_RERUN_OR_RESOLUTION", list(item.get("source_refs", [])))
        if item.get("work_class") == "EXCEPTION" and state not in {"CLOSED", "CONTAINED"}:
            add_blocker("PROCESS_BLOCKED", item["subject_ref"], f"EXCEPTION:{state}", list(item.get("source_refs", [])), "OPEN_EXCEPTION_HOLD_NO_ADVANCE", suffix=item["work_id"])
            add_action("RERUN_WORK", item["work_id"], item["work_id"], "OPEN_EXCEPTION_REQUIRES_PROCESS_RESOLUTION", list(item.get("source_refs", [])))

    # 5) Receipt/evidence checks use review/quality authority contracts, never receipt IDs as authority owners.
    for receipt in kernel.get("receipts", []):
        result = str(receipt.get("result", "")).upper()
        if receipt.get("receipt_class") == "REVIEW" and result in BLOCKING_REVIEW_RESULTS:
            add_blocker("DESIGN_REVIEW", receipt["subject_ref"], result, list(receipt.get("source_refs", [])), "REVIEW_HOLD_NO_DESIGN_KEEP_OR_PROMOTION")
            add_action("REOPEN_REVIEW", receipt["subject_ref"], receipt["receipt_id"], "BLOCKING_DESIGN_REVIEW_REQUIRES_REOPEN", list(receipt.get("source_refs", [])))
    for evidence in kernel.get("evidence_items", []):
        result = str(evidence.get("result", "")).upper()
        if evidence.get("evidence_class") == "REVIEW" and result in BLOCKING_REVIEW_RESULTS:
            add_blocker("QUALITY_REVIEW", evidence["subject_ref"], result, list(evidence.get("source_refs", [])), evidence.get("claim_ceiling") or "QUALITY_REVIEW_HOLD")
            add_action("REVIEW_SUBJECT", evidence["subject_ref"], evidence["evidence_id"], "BLOCKING_QUALITY_REVIEW_REQUIRES_REVIEW", list(evidence.get("source_refs", [])))

    # 6) Change propagation: direct seed actions + bounded relation-specific impact closure.
    observed_readbacks = {row.get("readback_id") for row in kernel.get("readbacks", []) if row.get("readback_state") == "OBSERVED"}
    relations = kernel.get("relations", [])
    rules_by_relation: dict[str, list[dict]] = defaultdict(list)
    for rule in policy.get("impact_rules", []):
        rules_by_relation[rule["relation_type"]].append(rule)
    max_depth = int(policy.get("propagation_limits", {}).get("max_depth", 4))

    for change in kernel.get("changes", []):
        state = str(change.get("change_state", "")).upper()
        if state not in BLOCKING_CHANGE_STATES:
            continue
        change_id = change["change_id"]
        sources = list(change.get("source_refs", []))
        add_blocker("CHANGE_READBACK_PENDING", change_id, state, sources, "CHANGE_NOT_CLOSED_NO_ADVANCE")
        for ref in sorted(set(change.get("reopen_refs", []))):
            add_action("REOPEN_REVIEW", ref, change_id, "DECLARED_CHANGE_REOPEN_REF", sources)
        if state == "IMPLEMENTED_READBACK_PENDING":
            explicit = sorted(set(change.get("required_readback_refs", [])))
            missing = [ref for ref in explicit if ref not in observed_readbacks]
            if explicit:
                for ref in missing:
                    add_action("REQUIRE_READBACK", ref, change_id, "DECLARED_CHANGE_REQUIRES_READBACK", sources, requested_output_class="READBACK")
            else:
                add_action("REQUIRE_READBACK", change_id, change_id, "CHANGE_IMPLEMENTED_REQUIRES_NEW_READBACK", sources, requested_output_class="READBACK")

        seeds = sorted(set(change.get("affected_refs", [])))
        queue: deque[tuple[str, int, list[str], str]] = deque((seed, 0, [], seed) for seed in seeds)
        visited: set[str] = set()
        for seed in seeds:
            if seed in work_ids:
                add_action("RERUN_WORK", seed, change_id, "DIRECT_CHANGE_AFFECTS_WORK", sources)
            else:
                add_action("REVIEW_SUBJECT", seed, change_id, "DIRECT_CHANGE_AFFECTED_REF_REQUIRES_REVIEW", sources)
        while queue:
            current, depth, path, seed = queue.popleft()
            if current in visited or depth > max_depth:
                continue
            visited.add(current)
            for rel in relations:
                rel_type = rel.get("relation_type")
                for rule in rules_by_relation.get(rel_type, []):
                    trigger_ref = rel["to_ref"] if rule["trigger_side"] == "TO" else rel["from_ref"]
                    if trigger_ref != current:
                        continue
                    target_ref = rel["from_ref"] if rule["action_target_side"] == "FROM" else rel["to_ref"]
                    next_path = path + [rel["relation_id"]]
                    action_id = add_action(rule["action_type"], target_ref, change_id, rule["reason_code"], list(rel.get("source_refs", [])), next_path)
                    impact_traces.append({
                        "change_id": change_id,
                        "seed_ref": seed,
                        "reached_ref": target_ref,
                        "depth": depth + 1,
                        "relation_path": next_path,
                        "action_request_ids": [action_id],
                    })
                    if rule.get("continue_impact") and depth + 1 < max_depth and target_ref not in visited:
                        queue.append((target_ref, depth + 1, next_path, seed))

    blockers_by_id = {row["blocker_id"]: row for row in blockers}
    blockers = sorted(blockers_by_id.values(), key=lambda row: row["blocker_id"])
    contradictions_by_id = {row["contradiction_id"]: row for row in contradictions}
    contradictions = sorted(contradictions_by_id.values(), key=lambda row: row["contradiction_id"])
    actions = sorted(action_map.values(), key=lambda row: row["action_id"])
    for action in actions:
        action["relation_paths"] = sorted(action["relation_paths"])

    # Compatibility projections are derived from typed actions only.
    reopen_set = sorted({a["subject_ref"] for a in actions if a["action_type"] == "REOPEN_REVIEW"})
    rerun_set = sorted({a["subject_ref"] for a in actions if a["action_type"] == "RERUN_WORK"})
    review_set = sorted({a["subject_ref"] for a in actions if a["action_type"] == "REVIEW_SUBJECT"})
    readback_set = sorted({a["subject_ref"] for a in actions if a["action_type"] == "REQUIRE_READBACK"})
    conflicts = sorted(x for x in authority_conflicts if x)
    unresolved = sorted(unresolved_authority_requirements.values(), key=lambda row: row["requirement_id"])

    can_advance = not blockers and not actions and not contradictions and not conflicts and not unresolved
    advance = "ALLOW" if can_advance else "HOLD"
    claim_ceiling = (
        "PHASE1_COORDINATION_CLEAR_WITHIN_OBSERVED_SCOPE_ONLY_NO_DESIGN_PROFESSIONAL_OR_PROMOTION_AUTHORITY"
        if can_advance
        else "PHASE1_COORDINATION_HOLD_NO_DESIGN_PROFESSIONAL_OR_PROMOTION_AUTHORITY"
    )
    if can_advance:
        reasons.add("NO_PHASE1_BLOCKERS_OR_TYPED_ACTIONS_OBSERVED")

    return {
        "schema_version": "0.1.1-candidate",
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
        "policy_ref": policy_ref,
        "policy_digest": {"sha256": policy_sha256, "hash_semantics": "UTF8_TEXT_LF_CANONICAL_V1"},
        "action_requests": actions,
        "impact_traces": sorted(impact_traces, key=lambda row: (row["change_id"], row["seed_ref"], row["depth"], row["reached_ref"], row["relation_path"])),
        "contradictions": contradictions,
        "unresolved_authority_requirements": unresolved,
        "claim_ceiling": claim_ceiling,
        "reason_codes": sorted(reasons),
        "source_refs": [kernel_ref],
        "authority_boundary": {
            "decision_is_authority": False,
            "may_mutate_current": False,
            "advance_rule": "ALLOW_ONLY_WHEN_NO_BLOCKERS_NO_TYPED_ACTIONS_NO_CONTRADICTIONS_NO_UNRESOLVED_AUTHORITY_REQUIREMENTS",
        },
        "does_not_prove": ["CURRENT_ADOPTION", "DESIGN_KEEP", "PROFESSIONAL_PASS", "PROJECT_PROMOTION", "STATUTORY_APPROVAL", "REAL_CASE_GENERALIZATION"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconcile an OLEANDER Enterprise Kernel candidate with typed actions and bounded impact propagation.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--generated-at")
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH)
    args = parser.parse_args()
    kernel = load_json(args.input)
    policy = load_json(args.policy)
    decision = reconcile(
        kernel,
        args.input.as_posix(),
        canonical_sha256(args.input),
        args.generated_at,
        policy=policy,
        policy_ref=DEFAULT_POLICY_REF if args.policy.resolve() == DEFAULT_POLICY_PATH.resolve() else args.policy.as_posix(),
        policy_sha256=canonical_sha256(args.policy),
    )
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
