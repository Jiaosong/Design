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
RECON_SCHEMA = ROOT / "OLEANDER_ENTERPRISE_RECONCILIATION_DECISION_v0.1.schema.json"
RICH_PROJECTION = ROOT / "example_enterprise_projection_v0.3.1.json"
RICH_KERNEL = ROOT / "example_enterprise_kernel_v0.1.json"
RICH_RECON = ROOT / "example_enterprise_reconciliation_v0.1.json"
MASTER_PROJECTION = ROOT / "eval-output" / "example-master-runtime.enterprise.v0.3.1.json"
MASTER_KERNEL = ROOT / "eval-output" / "example-master-runtime.enterprise-kernel.v0.1.json"
MASTER_RECON = ROOT / "eval-output" / "example-master-runtime.reconciliation.v0.1.json"
PHASE1_MODULES = {"ERP", "PLM", "BPM", "QMS"}
KERNEL_PRIMITIVES = {"IDENTITY", "AUTHORITY_BINDING", "STATE_FACT", "RELATION", "WORK", "CONFIGURATION", "EVIDENCE", "CHANGE", "READBACK", "RECEIPT", "RECONCILIATION"}
OWNER_MAP = ROOT / "OLEANDER_ENTERPRISE_KERNEL_OWNER_MAPPING_v0.1.json"
PHASE1_CANDIDATE = ROOT / "OLEANDER_ENTERPRISE_PHASE1_CANDIDATE_v0.1.json"
PHASE1_RECEIPT = ROOT / "ERP_PHASE1_KERNEL_EVAL_RECEIPT_v0.1_20260922.json"
PHASE1_MANIFEST = ROOT / "ENTERPRISE_PHASE1_MANIFEST_v0.1.json"
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
    "OTHER",
}


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
    schema_validate(RECON_SCHEMA, decision, "reconciliation")
    require(decision.get("kind") == "OLEANDER_ENTERPRISE_RECONCILIATION_DECISION", "reconciliation kind drift")
    require(decision.get("candidate_status") in {"EV2_CANDIDATE", "EVAL_ONLY"}, "reconciliation must remain candidate")
    require(decision.get("kernel_digest", {}).get("sha256") == sha(kernel_path), "reconciliation kernel digest mismatch")
    boundary = decision.get("authority_boundary", {})
    require(boundary.get("decision_is_authority") is False, "reconciliation may not become authority")
    require(boundary.get("may_mutate_current") is False, "reconciliation may not mutate Current")

    blockers = decision.get("blocking_conditions", [])
    require(len({x["blocker_id"] for x in blockers}) == len(blockers), "duplicate reconciliation blockers")
    for blocker in blockers:
        require(blocker.get("blocker_class") in BLOCKING_CLASSES, "unknown blocker class")
        require(bool(blocker.get("blocking_authority_ref")), "blocker missing blocking authority")
        require(bool(blocker.get("source_refs")), "blocker missing source_refs")
        require(bool(blocker.get("claim_ceiling")), "blocker missing claim ceiling")

    sets = [
        decision.get("reopen_set", []),
        decision.get("rerun_set", []),
        decision.get("review_set", []),
        decision.get("required_readback_set", []),
        decision.get("unresolved_authority_conflicts", []),
    ]
    any_required = any(bool(x) for x in sets)
    if decision.get("advance_decision") == "ALLOW":
        require(not blockers and not any_required, "ALLOW requires zero blockers/reopen/rerun/review/readback/conflicts")
        require("CLEAR_WITHIN_OBSERVED_SCOPE" in decision.get("claim_ceiling", ""), "ALLOW claim ceiling must remain bounded")
    elif decision.get("advance_decision") == "HOLD":
        require(bool(blockers) or any_required, "HOLD requires a concrete blocker or required action")
    else:
        require(decision.get("advance_decision") == "NOT_EVALUATED", "invalid reconciliation decision")
    require("PROJECT_PROMOTION" in set(decision.get("does_not_prove", [])), "reconciliation promotion boundary incomplete")


def validate_phase1_support() -> None:
    owner = load(OWNER_MAP)
    require(owner.get("status") == "PHASE1_EV2_CANDIDATE_NON_AUTHORITATIVE", "kernel owner mapping status drift")
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
    require(commit == "179ed4a5f342e0c66babce7b1f129f557fc68918", "Phase-1 candidate exact baseline drift")
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
    require(receipt.get("status") in {"LOCAL_VALIDATION_PASS_ANTI_POLLUTION_PENDING", "VALIDATED_ANTI_POLLUTION_PASS"}, "Phase-1 receipt status invalid")
    require(receipt.get("phase1_modules") == ["ERP", "PLM", "BPM", "QMS"], "Phase-1 receipt module ordering/scope drift")
    require(receipt.get("promotion", {}).get("eligible") is False, "Phase-1 receipt may not claim promotion eligibility")
    require(receipt.get("real_case_evaluation") == {"C01":"NOT_RUN","C04":"NOT_RUN","FALLINGWATER_3D":"NOT_RUN"}, "Phase-1 receipt may not claim unrun real cases")
    check_map = {x.get("check"): x.get("result") for x in receipt.get("checks", [])}
    for required_check in [
        "phase1_validator",
        "v031_candidate_validator",
        "clear_chain",
        "stale_source_fail_closed",
        "qms_open_fail_closed",
        "bpm_blocked_fail_closed",
        "plm_readback_pending_fail_closed",
        "cross_system_false_clear_prevention",
        "control_plane_tests",
        "execution_contract_validator",
        "architecture_control_validator",
    ]:
        require(check_map.get(required_check) == "PASS", f"Phase-1 receipt missing PASS: {required_check}")

    manifest = load(PHASE1_MANIFEST)
    require(manifest.get("status") == "PHASE1_EV2_ACTIVE_CANDIDATE_PACKAGE", "Phase-1 manifest status drift")
    require(manifest.get("baseline_main_commit") == "179ed4a5f342e0c66babce7b1f129f557fc68918", "Phase-1 manifest baseline drift")
    require(manifest.get("hash_semantics") == "UTF8_TEXT_LF_CANONICAL_V1", "Phase-1 manifest hash semantics drift")
    rows = manifest.get("active_files_excluding_this_manifest", [])
    require(len(rows) >= 13, "Phase-1 manifest active-file coverage incomplete")
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
    for row in d["modules"]["plm"].get("change_records", []):
        row["disposition"] = "CLOSED"
        row["reopen_refs"] = []
    for row in d.get("digital_thread", {}).get("unresolved_links", []):
        row["blocking"] = False
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
    print("PHASE1 POSITIVE stored kernel/reconciliation fixtures: PASS")

    rich_classes = {x["blocker_class"] for x in rich_recon["blocking_conditions"]}
    require({"DESIGN_REVIEW", "QUALITY_REVIEW", "CHANGE_READBACK_PENDING", "UNRESOLVED_BLOCKING_RELATION"}.issubset(rich_classes), "rich fixture missing expected blockers")
    require(rich_recon["advance_decision"] == "HOLD", "rich fixture must HOLD")
    require("CHANGE-DEMO-01" in rich_recon["required_readback_set"], "pending PLM change must require readback")
    require("REVIEW-DEMO-01" in rich_recon["reopen_set"], "pending PLM change must preserve reopen set")
    print("PHASE1 HOLD chain: PASS")

    clear_projection = make_clear_projection(load(RICH_PROJECTION))
    clear_kernel, clear_decision = phase1_decision_from_projection(clear_projection, "PHASE1-CLEAR")
    validate_kernel_in_memory(clear_kernel)
    validate_reconciliation_in_memory(clear_decision)
    require(clear_decision["advance_decision"] == "ALLOW", f"clear Phase-1 scenario should ALLOW, got {clear_decision['advance_decision']}")
    print("PHASE1 CLEAR chain: PASS")

    stale = copy.deepcopy(clear_kernel)
    for fact in stale["state_facts"]:
        if fact["state_family"] == "PROJECTION_FRESHNESS":
            fact["state_value"] = "SOURCE_READBACK_STALE"
            fact["blocking_semantics"] = "EXPLICIT"
    stale_payload = (json.dumps(stale, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    stale_decision = reconcile(stale, "fixture:stale-kernel", hashlib.sha256(stale_payload).hexdigest().upper(), "2026-09-22T13:15:00+08:00")
    validate_reconciliation_in_memory(stale_decision)
    require(stale_decision["advance_decision"] == "HOLD", "stale source must HOLD")
    require("SOURCE_STALE" in {x["blocker_class"] for x in stale_decision["blocking_conditions"]}, "stale source blocker missing")
    print("PHASE1 stale-source fail-closed: PASS")

    qms_open = make_clear_projection(load(RICH_PROJECTION))
    qms_open["modules"]["qms"]["nonconformances"][0]["state"] = "OPEN"
    _, qms_decision = phase1_decision_from_projection(qms_open, "PHASE1-QMS-OPEN")
    validate_reconciliation_in_memory(qms_decision)
    require(qms_decision["advance_decision"] == "HOLD", "open NCR must HOLD")
    require("QUALITY_NONCONFORMANCE" in {x["blocker_class"] for x in qms_decision["blocking_conditions"]}, "QMS blocker missing")
    print("PHASE1 QMS fail-closed: PASS")

    bpm_blocked = make_clear_projection(load(RICH_PROJECTION))
    bpm_blocked["modules"]["bpm"]["process_instances"][0]["process_state"] = "BLOCKED"
    _, bpm_decision = phase1_decision_from_projection(bpm_blocked, "PHASE1-BPM-BLOCKED")
    validate_reconciliation_in_memory(bpm_decision)
    require(bpm_decision["advance_decision"] == "HOLD", "blocked BPM process must HOLD")
    require("PROCESS_BLOCKED" in {x["blocker_class"] for x in bpm_decision["blocking_conditions"]}, "BPM blocker missing")
    print("PHASE1 BPM fail-closed: PASS")

    plm_pending = make_clear_projection(load(RICH_PROJECTION))
    plm_pending["modules"]["plm"]["change_records"][0]["disposition"] = "IMPLEMENTED_READBACK_PENDING"
    _, plm_decision = phase1_decision_from_projection(plm_pending, "PHASE1-PLM-PENDING")
    validate_reconciliation_in_memory(plm_decision)
    require(plm_decision["advance_decision"] == "HOLD", "pending PLM readback must HOLD")
    require("CHANGE-DEMO-01" in plm_decision["required_readback_set"], "PLM pending readback set missing")
    print("PHASE1 PLM readback fail-closed: PASS")

    false_clear = make_clear_projection(load(RICH_PROJECTION))
    false_clear["review_refs"][0]["result"] = "REVISE"
    false_clear["modules"]["bpm"]["process_instances"][0]["process_state"] = "COMPLETED"
    false_clear["modules"]["plm"]["configuration_items"][0]["lifecycle_state"] = "RELEASED"
    _, false_decision = phase1_decision_from_projection(false_clear, "PHASE1-FALSE-CLEAR")
    validate_reconciliation_in_memory(false_decision)
    require(false_decision["advance_decision"] == "HOLD", "PLM release/BPM complete must not override Design REVISE")
    require("DESIGN_REVIEW" in {x["blocker_class"] for x in false_decision["blocking_conditions"]}, "Design review blocker missing")
    print("PHASE1 cross-system false-clear prevention: PASS")

    stamp = "2026-09-22T13:15:00+08:00"
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
    print("PHASE1 deterministic kernel/reconciliation: PASS")
    print("ENTERPRISE_PHASE1_VALIDATION: PASS")
    return 0


def validate_kernel_in_memory(kernel: dict) -> None:
    schema_validate(KERNEL_SCHEMA, kernel, "kernel-memory")
    require(kernel.get("kernel_metrics", {}).get("unresolved_identity_ref_count") == 0, "in-memory kernel unresolved identities")
    require(kernel.get("kernel_metrics", {}).get("authority_gain_count") == 0, "in-memory kernel authority gain")
    require({x["module"] for x in kernel.get("module_bindings", [])} == PHASE1_MODULES, "in-memory phase1 module bindings drift")


def validate_reconciliation_in_memory(decision: dict) -> None:
    schema_validate(RECON_SCHEMA, decision, "reconciliation-memory")
    blockers = decision.get("blocking_conditions", [])
    required = any(bool(decision.get(k, [])) for k in ["reopen_set", "rerun_set", "review_set", "required_readback_set", "unresolved_authority_conflicts"])
    if decision["advance_decision"] == "ALLOW":
        require(not blockers and not required, "in-memory ALLOW has blockers/actions")
    if decision["advance_decision"] == "HOLD":
        require(bool(blockers) or required, "in-memory HOLD lacks concrete reason")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(f"ENTERPRISE_PHASE1_VALIDATION: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
