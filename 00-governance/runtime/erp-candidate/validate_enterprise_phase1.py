from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from build_enterprise_kernel import build_kernel, canonical_sha256 as projection_sha256
from reconcile_enterprise_kernel import reconcile

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[2]
KERNEL_SCHEMA = ROOT / "OLEANDER_ENTERPRISE_KERNEL_v0.1.schema.json"
RECON_SCHEMA = ROOT / "OLEANDER_ENTERPRISE_RECONCILIATION_DECISION_v0.1.2.schema.json"
RECON_POLICY = ROOT / "OLEANDER_ENTERPRISE_RECONCILIATION_POLICY_v0.1.json"
RICH_PROJECTION = ROOT / "example_enterprise_projection_v0.3.1.json"
RICH_KERNEL = ROOT / "example_enterprise_kernel_v0.1.2.json"
RICH_RECON = ROOT / "example_enterprise_reconciliation_v0.1.2.json"
MASTER_PROJECTION = ROOT / "eval-output" / "example-master-runtime.enterprise.v0.3.1.json"
MASTER_KERNEL = ROOT / "eval-output" / "example-master-runtime.enterprise-kernel.v0.1.2.json"
MASTER_RECON = ROOT / "eval-output" / "example-master-runtime.reconciliation.v0.1.2.json"
PHASE1_MODULES = {"ERP", "PLM", "BPM", "QMS"}
KERNEL_PRIMITIVES = {"IDENTITY", "AUTHORITY_BINDING", "STATE_FACT", "RELATION", "WORK", "CONFIGURATION", "EVIDENCE", "CHANGE", "READBACK", "RECEIPT", "RECONCILIATION"}
OWNER_MAP = ROOT / "OLEANDER_ENTERPRISE_KERNEL_OWNER_MAPPING_v0.1.1.json"
PHASE1_CANDIDATE = ROOT / "OLEANDER_ENTERPRISE_PHASE1_CANDIDATE_v0.1.2.json"
PHASE1_RECEIPT = ROOT / "ERP_PHASE1_KERNEL_EVAL_RECEIPT_v0.1.2_20260922.json"
PHASE1_MANIFEST = ROOT / "ENTERPRISE_PHASE1_MANIFEST_v0.1.2.json"
BLOCKING_CLASSES = {
    "SOURCE_STALE",
    "WORK_BLOCKED",
    "PROCESS_BLOCKED",
    "DESIGN_REVIEW",
    "QUALITY_NONCONFORMANCE",
    "QUALITY_REVIEW",
    "CHANGE_READBACK_PENDING",
    "AUTHORITY_CONFLICT",
    "UNRESOLVED_BLOCKING_RELATION",
    "STATE_FACET_BLOCKER",
    "CROSS_CARRIER_CONTRADICTION",
    "IMPACT_PROPAGATION_PENDING",
    "BLOCKING_AUTHORITY_UNRESOLVED",
    "OTHER",
}
ACTION_TYPES = {"RERUN_WORK", "REOPEN_REVIEW", "REVIEW_SUBJECT", "REQUIRE_READBACK", "REVALIDATE_CONFIGURATION"}


class ValidationError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return text.encode("utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest().upper()


def git_path_exists_at_commit(commit: str, rel: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}:{rel}"],
        cwd=REPO_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def authority_contract_ref_exists(rel: str) -> bool:
    if (REPO_ROOT / rel).is_file():
        return True
    if not PHASE1_CANDIDATE.is_file():
        return False
    candidate = load(PHASE1_CANDIDATE)
    commit = candidate.get("baseline", {}).get("commit")
    return bool(commit) and git_path_exists_at_commit(commit, rel)


def schema_validate(schema_path: Path, doc: dict, label: str) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return
    schema = load(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(doc), key=lambda e: list(e.path))
    if errors:
        first = errors[0]
        path = ".".join(str(x) for x in first.path) or "<root>"
        raise ValidationError(f"{label} jsonschema {path}: {first.message}")


def kernel_object_ids(kernel: dict) -> set[str]:
    ids = set()
    for key, field in [
        ("identities", "identity_id"),
        ("authority_bindings", "authority_binding_id"),
        ("state_facts", "state_fact_id"),
        ("relations", "relation_id"),
        ("work_items", "work_id"),
        ("configuration_items", "configuration_id"),
        ("evidence_items", "evidence_id"),
        ("changes", "change_id"),
        ("readbacks", "readback_id"),
        ("receipts", "receipt_id"),
    ]:
        for row in kernel.get(key, []):
            ids.add(row[field])
    return ids


def validate_kernel(kernel: dict, source_projection_path: Path) -> None:
    schema_validate(KERNEL_SCHEMA, kernel, "kernel")
    require(kernel.get("schema_version") == "0.1-candidate", "kernel schema revision drift")
    require(kernel.get("kind") == "OLEANDER_ENTERPRISE_KERNEL", "kernel kind drift")
    require(kernel.get("candidate_status") in {"EV2_CANDIDATE", "EVAL_ONLY"}, "kernel must remain candidate")
    boundary = kernel.get("authority_boundary", {})
    require(boundary.get("kernel_is_authority") is False, "kernel may not become authority")
    require(boundary.get("may_mutate_current") is False, "kernel may not mutate Current")
    require(kernel.get("source_projection_digest", {}).get("sha256") == sha(source_projection_path), "kernel source projection digest mismatch")

    identities = kernel.get("identities", [])
    canonical_refs = [x["canonical_ref"] for x in identities]
    identity_ids = [x["identity_id"] for x in identities]
    require(len(canonical_refs) == len(set(canonical_refs)), "kernel canonical identity duplication")
    require(len(identity_ids) == len(set(identity_ids)), "kernel identity_id duplication")
    canonical_set = set(canonical_refs)

    for row in kernel.get("authority_bindings", []):
        require(row.get("authority_gain") is False, "kernel authority binding may not gain authority")
        require(bool(row.get("source_refs")), "authority binding missing source_refs")
    for row in kernel.get("state_facts", []):
        require(row.get("subject_ref") in canonical_set, f"state fact subject unresolved: {row.get('subject_ref')}")
        require(row.get("projection_only") is True, "state fact must be projection-only")
        require(bool(row.get("source_refs")), "state fact missing source_refs")
    for row in kernel.get("relations", []):
        require(row.get("from_ref") in canonical_set, f"relation from_ref unresolved: {row.get('from_ref')}")
        require(row.get("to_ref") in canonical_set, f"relation to_ref unresolved: {row.get('to_ref')}")
        require(row.get("authority_effect") == "NONE", "kernel relation may not transfer authority")
    for row in kernel.get("configuration_items", []):
        require(row.get("subject_ref") in canonical_set, "configuration subject unresolved")
        require("PROJECT_PROMOTION" in set(row.get("does_not_prove", [])), "configuration release boundary incomplete")
    for row in kernel.get("evidence_items", []):
        require(row.get("subject_ref") in canonical_set, "evidence subject unresolved")
        require(bool(row.get("claim_ceiling")), "evidence claim ceiling missing")
    for row in kernel.get("changes", []):
        for ref in row.get("affected_refs", []):
            require(ref in canonical_set, f"change affected ref unresolved: {ref}")
    for row in kernel.get("readbacks", []):
        require(row.get("projection_only") is True, "readback must remain projection-only")
    for row in kernel.get("receipts", []):
        require(row.get("projection_only") is True, "receipt must remain projection-only")
        require("PROJECT_PROMOTION" in set(row.get("does_not_prove", [])), "receipt authority boundary incomplete")

    bindings = kernel.get("module_bindings", [])
    require({x["module"] for x in bindings} == PHASE1_MODULES, "Phase-1 module binding set must be exactly ERP/PLM/BPM/QMS")
    all_object_ids = kernel_object_ids(kernel)
    for binding in bindings:
        require(binding.get("projection_only") is True, "module binding must remain projection-only")
        require(bool(binding.get("source_refs")), "module binding missing source_refs")
        for ref in binding.get("kernel_object_refs", []):
            require(ref in all_object_ids, f"module binding references missing kernel object: {ref}")

    metrics = kernel.get("kernel_metrics", {})
    require(metrics.get("identity_count") == len(identities), "kernel identity metric mismatch")
    require(metrics.get("state_fact_count") == len(kernel.get("state_facts", [])), "kernel state metric mismatch")
    require(metrics.get("relation_count") == len(kernel.get("relations", [])), "kernel relation metric mismatch")
    require(metrics.get("phase1_module_binding_count") == 4, "Phase-1 module count drift")
    require(metrics.get("unresolved_identity_ref_count") == 0, "kernel unresolved identity refs must be zero")
    require(metrics.get("authority_gain_count") == 0, "kernel authority gain must remain zero")
    require(metrics.get("projection_rebuildable") is True, "kernel must remain rebuildable")


def validate_reconciliation(decision: dict, kernel_path: Path) -> None:
    kernel = load(kernel_path)
    validate_reconciliation_common(decision, kernel, expected_kernel_sha=sha(kernel_path))


def validate_authority_resolution(authority: dict, kernel: dict, context: str) -> None:
    state = authority.get("resolution_state")
    require(state in {"RESOLVED_EXISTING_BINDING", "UNRESOLVED_REQUIRED_OWNER", "DERIVED_COORDINATION_ONLY"}, f"{context} invalid authority resolution state")
    contract = authority.get("authority_contract_ref")
    require(bool(contract), f"{context} missing authority contract ref")
    if contract.startswith("00-governance/"):
        require(authority_contract_ref_exists(contract), f"{context} authority contract ref missing in checkout and bound baseline: {contract}")
    owners = {row.get("authority_owner_ref") for row in kernel.get("authority_bindings", [])}
    if state == "RESOLVED_EXISTING_BINDING":
        require(bool(authority.get("owner_ref")), f"{context} resolved authority missing owner_ref")
        require(authority.get("owner_ref") in owners, f"{context} owner_ref not present in kernel authority bindings")
    else:
        require(authority.get("owner_ref") is None, f"{context} unresolved/derived authority may not invent owner_ref")


def validate_reconciliation_common(decision: dict, kernel: dict, expected_kernel_sha: str | None = None) -> None:
    schema_validate(RECON_SCHEMA, decision, "reconciliation")
    require(decision.get("schema_version") == "0.1.2-candidate", "reconciliation schema revision drift")
    require(decision.get("kind") == "OLEANDER_ENTERPRISE_RECONCILIATION_DECISION", "reconciliation kind drift")
    require(decision.get("candidate_status") in {"EV2_CANDIDATE", "EVAL_ONLY"}, "reconciliation must remain candidate")
    if expected_kernel_sha:
        require(decision.get("kernel_digest", {}).get("sha256") == expected_kernel_sha, "reconciliation kernel digest mismatch")
    require(decision.get("policy_ref") == "00-governance/runtime/erp-candidate/OLEANDER_ENTERPRISE_RECONCILIATION_POLICY_v0.1.json", "reconciliation policy ref drift")
    require(decision.get("policy_digest", {}).get("sha256") == sha(RECON_POLICY), "reconciliation policy digest mismatch")
    boundary = decision.get("authority_boundary", {})
    require(boundary.get("decision_is_authority") is False, "reconciliation may not become authority")
    require(boundary.get("may_mutate_current") is False, "reconciliation may not mutate Current")
    require(boundary.get("advance_rule") == "ALLOW_ONLY_WHEN_NO_BLOCKERS_NO_TYPED_ACTIONS_NO_CONTRADICTIONS_NO_UNRESOLVED_AUTHORITY_REQUIREMENTS", "reconciliation advance rule drift")

    identity_class = {row["canonical_ref"]: row["identity_class"] for row in kernel.get("identities", [])}
    work_ids = {row["work_id"] for row in kernel.get("work_items", [])}
    authority_requirement_ids = {row["requirement_id"] for row in decision.get("unresolved_authority_requirements", [])}
    unresolved_lookup = {(row["subject_ref"], row["required_owner_kind"], row["authority_contract_ref"], row["scope"]) for row in decision.get("unresolved_authority_requirements", [])}

    blockers = decision.get("blocking_conditions", [])
    require(len({x["blocker_id"] for x in blockers}) == len(blockers), "duplicate reconciliation blockers")
    covered_explicit_facts = set()
    for blocker in blockers:
        require(blocker.get("blocker_class") in BLOCKING_CLASSES, "unknown blocker class")
        require(bool(blocker.get("blocking_authority_ref")), "blocker missing compatibility authority ref")
        require(bool(blocker.get("source_refs")), "blocker missing source_refs")
        require(bool(blocker.get("claim_ceiling")), "blocker missing claim ceiling")
        authority = blocker.get("blocking_authority", {})
        validate_authority_resolution(authority, kernel, f"blocker {blocker.get('blocker_id')}")
        expected_effective = authority.get("owner_ref") or authority.get("authority_contract_ref")
        require(blocker.get("blocking_authority_ref") == expected_effective, "blocker compatibility authority ref must equal resolved owner or authority contract")
        if authority.get("resolution_state") == "UNRESOLVED_REQUIRED_OWNER":
            key = (blocker["subject_ref"], authority["required_owner_kind"], authority["authority_contract_ref"], authority["scope"])
            require(key in unresolved_lookup, f"blocker unresolved authority requirement not materialized: {blocker['blocker_id']}")
        if blocker.get("state_fact_ref"):
            covered_explicit_facts.add(blocker["state_fact_ref"])

    explicit_fact_ids = {row["state_fact_id"] for row in kernel.get("state_facts", []) if row.get("blocking_semantics") == "EXPLICIT"}
    require(explicit_fact_ids.issubset(covered_explicit_facts), f"EXPLICIT state facts escaped reconciliation: {sorted(explicit_fact_ids-covered_explicit_facts)}")

    actions = decision.get("action_requests", [])
    require(len({x["action_id"] for x in actions}) == len(actions), "duplicate typed action requests")
    relation_ids = {row["relation_id"] for row in kernel.get("relations", [])}
    action_ids = {row["action_id"] for row in actions}
    for action in actions:
        require(action.get("action_type") in ACTION_TYPES, "unknown action type")
        require(action.get("subject_ref") in identity_class, f"typed action subject unresolved: {action.get('subject_ref')}")
        require(action.get("subject_identity_class") == identity_class[action["subject_ref"]], f"typed action identity class mismatch: {action['action_id']}")
        require(bool(action.get("trigger_refs")) and bool(action.get("reason_codes")) and bool(action.get("source_refs")), f"typed action provenance incomplete: {action['action_id']}")
        validate_authority_resolution(action.get("authority", {}), kernel, f"action {action.get('action_id')}")
        authority = action["authority"]
        if authority.get("resolution_state") == "UNRESOLVED_REQUIRED_OWNER":
            key = (action["subject_ref"], authority["required_owner_kind"], authority["authority_contract_ref"], authority["scope"])
            require(key in unresolved_lookup, f"action unresolved authority requirement not materialized: {action['action_id']}")
        if action["action_type"] == "RERUN_WORK":
            require(action["subject_ref"] in work_ids, f"RERUN_WORK target must be a work item: {action['subject_ref']}")
        if action["action_type"] == "REOPEN_REVIEW":
            require(identity_class[action["subject_ref"]] == "REVIEW", f"REOPEN_REVIEW target must be REVIEW: {action['subject_ref']}")
        if action["action_type"] == "REQUIRE_READBACK":
            require(action.get("requested_output_class") == "READBACK", "REQUIRE_READBACK must request READBACK output")
        for path in action.get("relation_paths", []):
            require(all(rel in relation_ids for rel in path), f"typed action relation path contains unknown relation: {action['action_id']}")

    legacy_reopen = sorted({a["subject_ref"] for a in actions if a["action_type"] == "REOPEN_REVIEW"})
    legacy_rerun = sorted({a["subject_ref"] for a in actions if a["action_type"] == "RERUN_WORK"})
    legacy_review = sorted({a["subject_ref"] for a in actions if a["action_type"] == "REVIEW_SUBJECT"})
    legacy_readback = sorted({a["subject_ref"] for a in actions if a["action_type"] == "REQUIRE_READBACK"})
    require(decision.get("reopen_set", []) == legacy_reopen, "legacy reopen_set is not a strict projection of typed actions")
    require(decision.get("rerun_set", []) == legacy_rerun, "legacy rerun_set is not a strict projection of typed actions")
    require(decision.get("review_set", []) == legacy_review, "legacy review_set is not a strict projection of typed actions")
    require(decision.get("required_readback_set", []) == legacy_readback, "legacy required_readback_set is not a strict projection of typed actions")

    contradictions = decision.get("contradictions", [])
    require(len({x["contradiction_id"] for x in contradictions}) == len(contradictions), "duplicate contradictions")
    fact_map = {row["state_fact_id"]: row for row in kernel.get("state_facts", [])}
    for contradiction in contradictions:
        require(contradiction.get("blocking") is True, "contradiction must be blocking")
        refs = contradiction.get("state_fact_refs", [])
        require(all(ref in fact_map for ref in refs), "contradiction references unknown state fact")
        require(any(fact_map[ref].get("blocking_semantics") == "EXPLICIT" for ref in refs), "contradiction must include explicit blocking fact")
        scopes = {fact_map[ref].get("claim_scope") or "LEGACY_UNSCOPED" for ref in refs}
        require(len(scopes) == 1, "contradiction may not mix claim scopes")
        require(contradiction.get("claim_scope") in scopes, "contradiction claim_scope mismatch")

    for trace in decision.get("impact_traces", []):
        require(all(rel in relation_ids for rel in trace.get("relation_path", [])), "impact trace contains unknown relation")
        require(all(action_id in action_ids for action_id in trace.get("action_request_ids", [])), "impact trace references unknown action request")
        require(trace.get("depth", 0) <= load(RECON_POLICY).get("propagation_limits", {}).get("max_depth", 4), "impact trace exceeded policy max depth")

    requirements = decision.get("unresolved_authority_requirements", [])
    require(len(authority_requirement_ids) == len(requirements), "duplicate unresolved authority requirement IDs")
    root_keys = [(row["subject_ref"], row["required_owner_kind"], row["authority_contract_ref"], row["scope"]) for row in requirements]
    require(len(root_keys) == len(set(root_keys)), "unresolved authority requirements not root-cause deduplicated")
    for row in requirements:
        require(row.get("trigger_refs") == sorted(set(row.get("trigger_refs", []))), "authority trigger_refs must be sorted/unique")
        require(bool(row.get("trigger_refs")), "authority requirement missing trigger_refs")
        require(row.get("trigger_ref") == row["trigger_refs"][0], "authority trigger_ref must be deterministic first trigger")
    sets = [
        blockers,
        actions,
        contradictions,
        decision.get("unresolved_authority_conflicts", []),
        decision.get("unresolved_authority_requirements", []),
    ]
    any_required = any(bool(x) for x in sets)
    if decision.get("advance_decision") == "ALLOW":
        require(not any_required, "ALLOW requires zero blockers/actions/contradictions/authority issues")
        require(not explicit_fact_ids, "ALLOW may not coexist with EXPLICIT state fact")
        require("CLEAR_WITHIN_OBSERVED_SCOPE" in decision.get("claim_ceiling", ""), "ALLOW claim ceiling must remain bounded")
    elif decision.get("advance_decision") == "HOLD":
        require(any_required, "HOLD requires concrete blockers/actions/contradictions/authority requirements")
    else:
        require(decision.get("advance_decision") == "NOT_EVALUATED", "invalid reconciliation decision")
    require("PROJECT_PROMOTION" in set(decision.get("does_not_prove", [])), "reconciliation promotion boundary incomplete")

def validate_phase1_support() -> None:
    owner = load(OWNER_MAP)
    require(owner.get("status") == "PHASE1_EV2_CANDIDATE_HARDENED_NON_AUTHORITATIVE", "kernel owner mapping status drift")
    require({x.get("primitive") for x in owner.get("primitives", [])} == KERNEL_PRIMITIVES, "kernel primitive owner mapping incomplete")
    require(set(owner.get("phase1_module_bindings", {}).keys()) == PHASE1_MODULES, "kernel Phase-1 module owner mapping drift")
    for row in owner.get("primitives", []):
        require(bool(row.get("canonical_owners")), f"kernel primitive {row.get('primitive')} missing canonical owner")
        require(row.get("mutation_permission") == "NONE_IN_CANDIDATE", f"kernel primitive {row.get('primitive')} may not mutate in candidate")
        require(bool(row.get("boundary")), f"kernel primitive {row.get('primitive')} missing boundary")

    candidate = load(PHASE1_CANDIDATE)
    require(candidate.get("state") == "EV2_EVAL_READY", "Phase-1 candidate state drift")
    require(set(candidate.get("phase1_modules", [])) == PHASE1_MODULES, "Phase-1 candidate module set drift")
    require(set(candidate.get("phase1_kernel_primitives", [])) == KERNEL_PRIMITIVES, "Phase-1 candidate primitive set drift")
    require(candidate.get("mutation_scope", {}).get("current_files_modified") is False, "Phase-1 candidate may not modify Current authority")
    require(candidate.get("mutation_scope", {}).get("new_runtime_layer") is False, "Phase-1 candidate may not add a runtime layer")
    require(candidate.get("mutation_scope", {}).get("new_authority") is False, "Phase-1 candidate may not add authority")
    require(candidate.get("promotion", {}).get("eligible") is False, "Phase-1 candidate must remain promotion-ineligible")
    baseline = candidate.get("baseline", {})
    commit = baseline.get("commit")
    require(commit == "ab83fde14d0b341f373098e789be93cd527465ef", "Phase-1 candidate exact baseline drift")
    require(baseline.get("hash_semantics") == "SHA256_OF_GIT_CANONICAL_BLOB_CONTENT_AT_EXACT_COMMIT", "Phase-1 baseline hash semantics drift")
    for rel, expected in baseline.get("source_sha256", {}).items():
        try:
            blob = subprocess.check_output(["git", "show", f"{commit}:{rel}"], cwd=REPO_ROOT)
        except subprocess.CalledProcessError as exc:
            raise ValidationError(f"Phase-1 baseline source unavailable: {rel}") from exc
        actual = hashlib.sha256(blob).hexdigest().upper()
        require(actual == expected, f"Phase-1 baseline hash drift: {rel}")
    for rel in candidate.get("evaluation", {}).get("eval_refs", []):
        require((REPO_ROOT / rel).is_file(), f"Phase-1 eval ref missing: {rel}")

    receipt = load(PHASE1_RECEIPT)
    require(receipt.get("candidate_ref") == candidate.get("candidate_id"), "Phase-1 receipt candidate binding drift")
    require(receipt.get("status") in {"PREVALIDATION_PENDING_FULL_REGRESSION", "VALIDATED_ANTI_POLLUTION_PASS"}, "Phase-1 receipt status invalid")
    require(receipt.get("phase1_modules") == ["ERP", "PLM", "BPM", "QMS"], "Phase-1 receipt module ordering/scope drift")
    require(receipt.get("promotion", {}).get("eligible") is False, "Phase-1 receipt may not claim promotion eligibility")
    require(receipt.get("real_case_evaluation") == {
        "C01":"STRESS_TEST_HOLD_CORRECT",
        "C04":"STRESS_TEST_HOLD_CORRECT",
        "FALLINGWATER_3D":"SOURCE_DIVERGED_HOLD_REFRESH_REQUIRED",
    }, "Phase-1 real-case stress readback drift")
    if receipt.get("status") == "VALIDATED_ANTI_POLLUTION_PASS":
        check_map = {x.get("check"): x.get("result") for x in receipt.get("checks", [])}
        for required_check in [
            "phase1_validator_v012",
            "v031_candidate_validator",
            "true_clear_chain",
            "explicit_state_fail_closed",
            "scoped_contradiction_gate",
            "authority_requirement_root_dedup",
            "typed_change_impact_closure",
            "canonical_authority_resolution",
            "typed_action_projection",
            "control_plane_tests",
            "execution_contract_validator",
            "architecture_control_validator",
            "anti_pollution",
        ]:
            require(check_map.get(required_check) == "PASS", f"Phase-1 receipt missing PASS: {required_check}")

    manifest = load(PHASE1_MANIFEST)
    require(manifest.get("status") == "PHASE1_EV2_ACTIVE_CANDIDATE_PACKAGE", "Phase-1 manifest status drift")
    require(manifest.get("baseline_main_commit") == "ab83fde14d0b341f373098e789be93cd527465ef", "Phase-1 manifest baseline drift")
    require(manifest.get("hash_semantics") == "UTF8_TEXT_LF_CANONICAL_V1", "Phase-1 manifest hash semantics drift")
    rows = manifest.get("active_files_excluding_this_manifest", [])
    require(len(rows) >= 17, "Phase-1 manifest active-file coverage incomplete")
    seen = set()
    for row in rows:
        rel = row.get("path")
        require(rel and rel not in seen, "Phase-1 manifest duplicate/missing path")
        seen.add(rel)
        path = ROOT / rel
        require(path.is_file(), f"Phase-1 manifest file missing: {rel}")
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
        canonical = text.encode("utf-8")
        require(row.get("hash_semantics") == "UTF8_TEXT_LF_CANONICAL_V1", f"Phase-1 manifest row hash semantics drift: {rel}")
        require(row.get("bytes") == len(canonical), f"Phase-1 manifest byte count drift: {rel}")
        require(row.get("sha256") == hashlib.sha256(canonical).hexdigest().upper(), f"Phase-1 manifest sha256 drift: {rel}")


def make_clear_projection(source: dict) -> dict:
    d = copy.deepcopy(source)
    for review in d.get("review_refs", []):
        if review.get("review_class") == "DESIGN":
            review["result"] = "KEEP"
    for row in d["modules"]["qms"].get("inspection_records", []):
        row["result"] = "PASS"
        if not row.get("evidence_refs"):
            row["evidence_refs"] = ["EVIDENCE:PHASE1-CLEAR"]
    for row in d["modules"]["qms"].get("nonconformances", []):
        row["state"] = "CLOSED"
    for row in d["modules"]["qms"].get("capa_records", []):
        row["state"] = "CLOSED"
        row["root_cause_state"] = "SUPPORTED"
        if not row.get("effectiveness_readback_ref"):
            row["effectiveness_readback_ref"] = "READBACK:PHASE1-CAPA-CLEAR"
    for row in d["modules"]["plm"].get("change_records", []):
        row["disposition"] = "CLOSED"
        row["reopen_refs"] = []
    for row in d["modules"]["bpm"].get("process_instances", []):
        row["process_state"] = "ACTIVE"
    for row in d["modules"]["bpm"].get("exceptions", []):
        row["disposition"] = "CLOSED"
    for row in d.get("digital_thread", {}).get("unresolved_links", []):
        row["blocking"] = False
    # Clear all top-level carriers too. A clear fixture must not contradict its module/detail carriers.
    d["state_facets"]["quality"] = {"ARTIFACT-DEMO-01": "PASS"}
    d["state_facets"]["process"] = {"WP-DEMO-001": "ACTIVE"}
    d["state_facets"]["professional"] = {}
    d["state_facets"]["interface"] = {"IF-DEMO-01": "VERIFIED"}
    d["reconciliation"]["enterprise_readiness_state"] = "READY_FOR_EVALUATION"
    d["reconciliation"]["advance_allowed"] = False
    return d

def phase1_decision_from_projection(projection: dict, label: str) -> tuple[dict, dict]:
    stamp = "2026-09-22T13:15:00+08:00"
    projection_payload = (json.dumps(projection, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    projection_digest = hashlib.sha256(projection_payload).hexdigest().upper()
    kernel = build_kernel(projection, f"fixture:{label}", projection_digest, stamp)
    kernel_payload = (json.dumps(kernel, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    kernel_digest = hashlib.sha256(kernel_payload).hexdigest().upper()
    decision = reconcile(kernel, f"fixture:{label}:kernel", kernel_digest, stamp)
    return kernel, decision


def main() -> int:
    validate_phase1_support()
    rich_kernel = load(RICH_KERNEL)
    rich_recon = load(RICH_RECON)
    master_kernel = load(MASTER_KERNEL)
    master_recon = load(MASTER_RECON)
    validate_kernel(rich_kernel, RICH_PROJECTION)
    validate_reconciliation(rich_recon, RICH_KERNEL)
    validate_kernel(master_kernel, MASTER_PROJECTION)
    validate_reconciliation(master_recon, MASTER_KERNEL)
    print("PHASE1 v0.1.2 stored kernel/reconciliation fixtures: PASS")

    rich_classes = {x["blocker_class"] for x in rich_recon["blocking_conditions"]}
    require({"DESIGN_REVIEW", "QUALITY_REVIEW", "CHANGE_READBACK_PENDING", "UNRESOLVED_BLOCKING_RELATION"}.issubset(rich_classes), "rich fixture missing expected blockers")
    require(rich_recon["advance_decision"] == "HOLD", "rich fixture must HOLD")
    require("CHANGE-DEMO-01" in rich_recon["required_readback_set"], "pending PLM change must require readback")
    require("REVIEW-DEMO-01" in rich_recon["reopen_set"], "pending PLM change must preserve reopen set")
    print("PHASE1 HOLD chain: PASS")

    clear_projection = make_clear_projection(load(RICH_PROJECTION))
    clear_kernel, clear_decision = phase1_decision_from_projection(clear_projection, "PHASE1-CLEAR")
    validate_kernel_in_memory(clear_kernel)
    validate_reconciliation_in_memory(clear_decision, clear_kernel)
    require(clear_decision["advance_decision"] == "ALLOW", f"clear Phase-1 scenario should ALLOW, got {clear_decision['advance_decision']}")
    require(not [f for f in clear_kernel["state_facts"] if f["blocking_semantics"] == "EXPLICIT"], "clear fixture may not contain EXPLICIT state facts")
    print("PHASE1 TRUE CLEAR chain: PASS")

    stale = copy.deepcopy(clear_kernel)
    for fact in stale["state_facts"]:
        if fact["state_family"] == "PROJECTION_FRESHNESS":
            fact["state_value"] = "SOURCE_READBACK_STALE"
            fact["blocking_semantics"] = "EXPLICIT"
    stale_payload = (json.dumps(stale, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    stale_decision = reconcile(stale, "fixture:stale-kernel", hashlib.sha256(stale_payload).hexdigest().upper(), "2026-09-22T14:40:00+08:00")
    validate_reconciliation_in_memory(stale_decision, stale)
    require(stale_decision["advance_decision"] == "HOLD", "stale source must HOLD")
    require("SOURCE_STALE" in {x["blocker_class"] for x in stale_decision["blocking_conditions"]}, "stale source blocker missing")
    print("PHASE1 stale-source fail-closed: PASS")

    qms_open = make_clear_projection(load(RICH_PROJECTION))
    qms_open["modules"]["qms"]["nonconformances"][0]["state"] = "OPEN"
    qms_kernel, qms_decision = phase1_decision_from_projection(qms_open, "PHASE1-QMS-OPEN")
    validate_reconciliation_in_memory(qms_decision, qms_kernel)
    require(qms_decision["advance_decision"] == "HOLD", "open NCR must HOLD")
    require("QUALITY_NONCONFORMANCE" in {x["blocker_class"] for x in qms_decision["blocking_conditions"]}, "QMS blocker missing")
    print("PHASE1 QMS fail-closed: PASS")

    bpm_blocked = make_clear_projection(load(RICH_PROJECTION))
    bpm_blocked["modules"]["bpm"]["process_instances"][0]["process_state"] = "BLOCKED"
    bpm_kernel, bpm_decision = phase1_decision_from_projection(bpm_blocked, "PHASE1-BPM-BLOCKED")
    validate_reconciliation_in_memory(bpm_decision, bpm_kernel)
    require(bpm_decision["advance_decision"] == "HOLD", "blocked BPM process must HOLD")
    require("PROCESS_BLOCKED" in {x["blocker_class"] for x in bpm_decision["blocking_conditions"]}, "BPM blocker missing")
    print("PHASE1 BPM fail-closed: PASS")

    plm_pending = make_clear_projection(load(RICH_PROJECTION))
    plm_pending["modules"]["plm"]["change_records"][0]["disposition"] = "IMPLEMENTED_READBACK_PENDING"
    plm_kernel, plm_decision = phase1_decision_from_projection(plm_pending, "PHASE1-PLM-PENDING")
    validate_reconciliation_in_memory(plm_decision, plm_kernel)
    require(plm_decision["advance_decision"] == "HOLD", "pending PLM readback must HOLD")
    require("CHANGE-DEMO-01" in plm_decision["required_readback_set"], "PLM pending readback set missing")
    print("PHASE1 PLM readback fail-closed: PASS")

    false_clear = make_clear_projection(load(RICH_PROJECTION))
    false_clear["review_refs"][0]["result"] = "REVISE"
    false_clear["modules"]["bpm"]["process_instances"][0]["process_state"] = "COMPLETED"
    false_clear["modules"]["plm"]["configuration_items"][0]["lifecycle_state"] = "RELEASED"
    false_kernel, false_decision = phase1_decision_from_projection(false_clear, "PHASE1-FALSE-CLEAR")
    validate_reconciliation_in_memory(false_decision, false_kernel)
    require(false_decision["advance_decision"] == "HOLD", "PLM release/BPM complete must not override Design REVISE")
    require("DESIGN_REVIEW" in {x["blocker_class"] for x in false_decision["blocking_conditions"]}, "Design review blocker missing")
    print("PHASE1 cross-system false-clear prevention: PASS")

    # Every top-level EXPLICIT state family must independently prevent ALLOW.
    explicit_cases = []
    d = make_clear_projection(load(RICH_PROJECTION)); d["state_facets"]["quality"] = {"ARTIFACT-DEMO-01": "REVISE"}; explicit_cases.append(("QUALITY", d))
    d = make_clear_projection(load(RICH_PROJECTION)); d["state_facets"]["process"] = {"WP-DEMO-001": "BLOCKED"}; explicit_cases.append(("PROCESS", d))
    d = make_clear_projection(load(RICH_PROJECTION)); d["state_facets"]["professional"] = {"ARCH-DEMO": {"state":"HOLD","verdict":"HOLD"}}; explicit_cases.append(("PROFESSIONAL", d))
    d = make_clear_projection(load(RICH_PROJECTION)); d["state_facets"]["interface"] = {"IF-DEMO-01": {"state":"BLOCKED","unresolved_authority_conflicts":0}}; explicit_cases.append(("INTERFACE", d))
    d = make_clear_projection(load(RICH_PROJECTION)); d["reconciliation"]["enterprise_readiness_state"] = "HOLD"; explicit_cases.append(("ENTERPRISE_READINESS", d))
    for label, projection in explicit_cases:
        kernel, decision = phase1_decision_from_projection(projection, f"EXPLICIT-{label}")
        validate_reconciliation_in_memory(decision, kernel)
        require(decision["advance_decision"] == "HOLD", f"EXPLICIT {label} state escaped reconciliation")
        explicit_ids = {f["state_fact_id"] for f in kernel["state_facts"] if f["blocking_semantics"] == "EXPLICIT"}
        covered = {b["state_fact_ref"] for b in decision["blocking_conditions"] if b.get("state_fact_ref")}
        require(explicit_ids.issubset(covered), f"EXPLICIT {label} state fact missing blocker coverage")
    print("PHASE1 all EXPLICIT state facts fail-closed: PASS")

    # Different claim scopes may legitimately disagree (e.g. machine PASS vs professional HOLD).
    scoped_projection = make_clear_projection(load(RICH_PROJECTION))
    scoped_projection["state_facets"]["quality"] = {"ARTIFACT-DEMO-01": "HOLD_PROFESSIONAL_GATE"}
    scoped_kernel, scoped_decision = phase1_decision_from_projection(scoped_projection, "CROSS-SCOPE-NON-CONTRADICTION")
    validate_reconciliation_in_memory(scoped_decision, scoped_kernel)
    require(not scoped_decision["contradictions"], "different claim scopes created false contradiction")

    # Same-subject/same-family/same-claim-scope PASS vs REVISE is a real contradiction.
    contradiction_projection = make_clear_projection(load(RICH_PROJECTION))
    contradiction_projection["modules"]["qms"]["inspection_records"].append({
        "inspection_id":"INSP-DEMO-CONTRADICTION",
        "subject_ref":"ARTIFACT-DEMO-01",
        "inspection_class":"REVIEW_READBACK",
        "result":"REVISE",
        "evidence_refs":["REVIEW-DEMO-01"],
        "source_refs":["fixture:contradiction"]
    })
    contradiction_kernel, contradiction_decision = phase1_decision_from_projection(contradiction_projection, "SAME-SCOPE-CONTRADICTION")
    validate_reconciliation_in_memory(contradiction_decision, contradiction_kernel)
    require(contradiction_decision["contradictions"], "cross-carrier contradiction was not materialized")
    require("CROSS_CARRIER_CONTRADICTION" in {b["blocker_class"] for b in contradiction_decision["blocking_conditions"]}, "cross-carrier contradiction blocker missing")
    require({c["claim_scope"] for c in contradiction_decision["contradictions"]} == {"QMS_INSPECTION:REVIEW_READBACK"}, "contradiction scope classification drift")
    print("PHASE1 scoped contradiction gate: PASS")

    # Relation-bounded impact closure: artifact change must reach producer job, requirement and review without reclassifying artifact as work.
    impact_projection = make_clear_projection(load(RICH_PROJECTION))
    impact_projection["modules"]["plm"]["change_records"] = [{
        "change_id":"CHANGE-IMPACT-01","change_class":"REVISION","affected_refs":["ARTIFACT-DEMO-01"],
        "disposition":"IMPLEMENTED_READBACK_PENDING","reopen_refs":[],"source_refs":["fixture:impact"]
    }]
    impact_projection["digital_thread"]["relations"].append({
        "relation_id":"REL-IMPACT-REVIEW","relation_type":"ARTIFACT_REVIEWED_BY","from_ref":"ARTIFACT-DEMO-01","to_ref":"REVIEW-DEMO-01","projection_only":True,"source_refs":["fixture:impact"]
    })
    impact_kernel, impact_decision = phase1_decision_from_projection(impact_projection, "IMPACT-CLOSURE")
    validate_reconciliation_in_memory(impact_decision, impact_kernel)
    action_pairs = {(a["action_type"], a["subject_ref"]) for a in impact_decision["action_requests"]}
    require(("RERUN_WORK", "JOB-DEMO-001") in action_pairs, "artifact change did not reach producer job")
    require(("REVIEW_SUBJECT", "REQ-DEMO-01") in action_pairs, "artifact change did not reach requirement satisfaction review")
    require(("REOPEN_REVIEW", "REVIEW-DEMO-01") in action_pairs, "artifact change did not reopen artifact review")
    require("ARTIFACT-DEMO-01" not in impact_decision["rerun_set"], "artifact ref may not masquerade as rerunnable work")
    require(impact_decision["impact_traces"], "impact traces missing")
    print("PHASE1 typed change-impact closure: PASS")

    # Closed change must not propagate actions.
    closed_projection = make_clear_projection(load(RICH_PROJECTION))
    closed_projection["modules"]["plm"]["change_records"] = [{
        "change_id":"CHANGE-CLOSED-01","change_class":"REVISION","affected_refs":["ARTIFACT-DEMO-01"],
        "disposition":"CLOSED","reopen_refs":[],"source_refs":["fixture:closed"]
    }]
    closed_kernel, closed_decision = phase1_decision_from_projection(closed_projection, "CHANGE-CLOSED")
    validate_reconciliation_in_memory(closed_decision, closed_kernel)
    require(closed_decision["advance_decision"] == "ALLOW", "closed change created false HOLD")
    require(not closed_decision["action_requests"] and not closed_decision["impact_traces"], "closed change created false propagation")
    print("PHASE1 closed-change no-propagation: PASS")

    # Multiple changes may share one action request, but each change blocker/readback trigger remains visible.
    multi_projection = make_clear_projection(load(RICH_PROJECTION))
    multi_projection["modules"]["plm"]["change_records"] = [
        {"change_id":"CHANGE-DUP-01","change_class":"REVISION","affected_refs":["ARTIFACT-DEMO-01"],"disposition":"IMPLEMENTED_READBACK_PENDING","reopen_refs":["REVIEW-DEMO-01"],"source_refs":["fixture:dup"]},
        {"change_id":"CHANGE-DUP-02","change_class":"REVISION","affected_refs":["ARTIFACT-DEMO-01"],"disposition":"IMPLEMENTED_READBACK_PENDING","reopen_refs":["REVIEW-DEMO-01"],"source_refs":["fixture:dup"]},
    ]
    multi_kernel, multi_decision = phase1_decision_from_projection(multi_projection, "MULTI-CHANGE")
    validate_reconciliation_in_memory(multi_decision, multi_kernel)
    direct_review = [a for a in multi_decision["action_requests"] if a["action_type"] == "REVIEW_SUBJECT" and a["subject_ref"] == "ARTIFACT-DEMO-01"]
    require(len(direct_review) == 1 and set(direct_review[0]["trigger_refs"]) == {"CHANGE-DUP-01","CHANGE-DUP-02"}, "multi-change action dedup/provenance failed")
    require({b["subject_ref"] for b in multi_decision["blocking_conditions"] if b["blocker_class"] == "CHANGE_READBACK_PENDING"} == {"CHANGE-DUP-01","CHANGE-DUP-02"}, "multi-change blockers were collapsed")
    print("PHASE1 multi-change dedup with provenance preservation: PASS")

    # Authority references must be canonical owner bindings or canonical authority-contract refs, never receipt/free text owner claims.
    for decision, kernel in [(rich_recon, rich_kernel), (master_recon, master_kernel), (impact_decision, impact_kernel)]:
        for blocker in decision["blocking_conditions"]:
            authority = blocker["blocking_authority"]
            effective = authority.get("owner_ref") or authority["authority_contract_ref"]
            require(blocker["blocking_authority_ref"] == effective, "blocker authority compatibility ref drift")
            require(not blocker["blocking_authority_ref"].startswith("DESIGN_REVIEW_RECEIPT:"), "receipt ID may not masquerade as authority owner")
    print("PHASE1 canonical blocker authority resolution: PASS")

    stamp = "2026-09-22T14:40:00+08:00"
    source = load(RICH_PROJECTION)
    source_payload = (json.dumps(source, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    source_digest = hashlib.sha256(source_payload).hexdigest().upper()
    a = build_kernel(source, "fixture:deterministic", source_digest, stamp)
    b = build_kernel(source, "fixture:deterministic", source_digest, stamp)
    require(json.dumps(a, ensure_ascii=False, sort_keys=True) == json.dumps(b, ensure_ascii=False, sort_keys=True), "kernel build is not deterministic")
    ap = (json.dumps(a, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    ad = hashlib.sha256(ap).hexdigest().upper()
    ra = reconcile(a, "fixture:deterministic:kernel", ad, stamp)
    rb = reconcile(a, "fixture:deterministic:kernel", ad, stamp)
    require(json.dumps(ra, ensure_ascii=False, sort_keys=True) == json.dumps(rb, ensure_ascii=False, sort_keys=True), "reconciliation is not deterministic")
    validate_reconciliation_in_memory(ra, a)
    print("PHASE1 deterministic kernel/reconciliation: PASS")
    print("ENTERPRISE_PHASE1_VALIDATION: PASS")
    return 0

def validate_kernel_in_memory(kernel: dict) -> None:
    schema_validate(KERNEL_SCHEMA, kernel, "kernel-memory")
    require(kernel.get("kernel_metrics", {}).get("unresolved_identity_ref_count") == 0, "in-memory kernel unresolved identities")
    require(kernel.get("kernel_metrics", {}).get("authority_gain_count") == 0, "in-memory kernel authority gain")
    require({x["module"] for x in kernel.get("module_bindings", [])} == PHASE1_MODULES, "in-memory phase1 module bindings drift")


def validate_reconciliation_in_memory(decision: dict, kernel: dict) -> None:
    payload = (json.dumps(kernel, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    validate_reconciliation_common(decision, kernel, expected_kernel_sha=hashlib.sha256(payload).hexdigest().upper())


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(f"ENTERPRISE_PHASE1_VALIDATION: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
