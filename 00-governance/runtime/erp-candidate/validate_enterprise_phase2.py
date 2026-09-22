from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

from build_enterprise_kernel_v0_2 import build_kernel_v0_2
from reconcile_enterprise_kernel_v0_2 import reconcile_v0_2
from validate_enterprise_phase1 import make_clear_projection
from validate_erp_candidate import validate_projection


ROOT = Path(__file__).resolve().parent
PROJECTION = ROOT / "example_enterprise_projection_v0.3.1.json"
KERNEL = ROOT / "example_enterprise_kernel_v0.2.json"
RECON = ROOT / "example_enterprise_reconciliation_v0.2.json"
KERNEL_SCHEMA = ROOT / "OLEANDER_ENTERPRISE_KERNEL_v0.2.schema.json"
RECON_SCHEMA = ROOT / "OLEANDER_ENTERPRISE_RECONCILIATION_DECISION_v0.2.schema.json"
PHASE2_CANDIDATE = ROOT / "OLEANDER_ENTERPRISE_PHASE2_CANDIDATE_v0.2_20260922.json"
PHASE2_RECEIPT = ROOT / "ERP_PHASE2_KERNEL_EVAL_RECEIPT_v0.2_20260922.json"
PHASE2_MANIFEST = ROOT / "ENTERPRISE_PHASE2_MANIFEST_v0.2.json"
PHASE2_STRESS_SUMMARY = ROOT / "phase2-real-case-stress-20260922" / "PHASE2_REAL_CASE_STRESS_SUMMARY_20260922.json"
REPO_ROOT = ROOT.parents[2]
BASELINE_MAIN = "69f73a1a0e105d6797affccc0d8c09110febb345"
ALL_MODULES = {"ERP", "PLM", "MES", "BPM", "QMS", "MBSE", "KNOWLEDGE_GRAPH", "AGENT_RUNTIME"}


class ValidationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_validate(schema_path: Path, value: dict, label: str) -> None:
    schema = load(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda e: list(e.absolute_path))
    if errors:
        first = errors[0]
        raise ValidationError(f"{label} schema error at {'/'.join(map(str, first.absolute_path))}: {first.message}")


def canonical_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return text.encode("utf-8")


def validate_phase2_package() -> None:
    candidate = load(PHASE2_CANDIDATE)
    receipt = load(PHASE2_RECEIPT)
    manifest = load(PHASE2_MANIFEST)
    stress = load(PHASE2_STRESS_SUMMARY)

    require(candidate.get("candidate_id") == "OLEANDER_ENTERPRISE_PHASE2_KERNELIZATION_v0.2_20260922", "Phase-2 candidate id drift")
    require(candidate.get("baseline", {}).get("commit") == BASELINE_MAIN, "Phase-2 candidate baseline drift")
    require(candidate.get("evaluation", {}).get("independent_review") == "NOT_RUN", "Phase-2 candidate may not self-grant EV4")
    require(candidate.get("promotion", {}).get("eligible") is False, "Phase-2 candidate may not self-promote")
    require(candidate.get("mutation_scope", {}).get("current_files_modified") is False, "Phase-2 candidate may not mutate Current")
    require(candidate.get("mutation_scope", {}).get("new_runtime_layer") is False, "Phase-2 candidate may not add runtime layer")
    require(candidate.get("mutation_scope", {}).get("new_authority") is False, "Phase-2 candidate may not add authority")

    for rel, expected in candidate.get("baseline", {}).get("source_sha256", {}).items():
        payload = subprocess.check_output(["git", "show", f"{BASELINE_MAIN}:{rel}"], cwd=REPO_ROOT)
        actual = hashlib.sha256(payload).hexdigest().upper()
        require(actual == expected, f"Phase-2 baseline source hash drift: {rel}")

    require(receipt.get("candidate_ref") == candidate.get("candidate_id"), "Phase-2 receipt candidate mismatch")
    require(receipt.get("baseline_main_commit") == BASELINE_MAIN, "Phase-2 receipt baseline drift")
    require(receipt.get("independent_review", {}).get("state") == "NOT_RUN", "Phase-2 receipt may not claim independent review")
    require(receipt.get("promotion", {}).get("eligible") is False, "Phase-2 receipt may not claim promotion eligibility")
    check_map = {row["check"]: row["result"] for row in receipt.get("checks", [])}
    for check in [
        "phase2_validator", "phase1_regression", "v031_candidate_validator", "real_case_c01", "real_case_c04",
        "real_case_fallingwater", "control_plane_tests", "execution_contract_validator", "architecture_control_validator",
        "compileall", "deterministic_repeat",
    ]:
        require(str(check_map.get(check, "")).startswith("PASS"), f"Phase-2 receipt missing PASS: {check}")
    require(check_map.get("anti_pollution") in {"PENDING_COMMIT_DELTA", "PASS"}, "Phase-2 Anti-Pollution receipt state invalid")

    require(manifest.get("baseline_main_commit") == BASELINE_MAIN, "Phase-2 manifest baseline drift")
    require(manifest.get("enterprise_module_binding_count") == 8, "Phase-2 manifest module count drift")
    require(set(manifest.get("phase2_modules", [])) == {"MES", "MBSE", "KNOWLEDGE_GRAPH", "AGENT_RUNTIME"}, "Phase-2 manifest module set drift")
    require(manifest.get("independent_review") == "NOT_RUN", "Phase-2 manifest may not claim EV4")
    require(manifest.get("promotion_eligible") is False, "Phase-2 manifest may not claim promotion")
    rows = manifest.get("active_files_excluding_this_manifest", [])
    require(len({row["path"] for row in rows}) == len(rows), "Phase-2 manifest duplicate path")
    for row in rows:
        rel = row["path"]
        path = ROOT / rel
        require(path.is_file(), f"Phase-2 manifest missing file: {rel}")
        payload = canonical_bytes(path)
        require(row.get("bytes") == len(payload), f"Phase-2 manifest byte drift: {rel}")
        require(row.get("sha256") == hashlib.sha256(payload).hexdigest().upper(), f"Phase-2 manifest SHA drift: {rel}")
        require(row.get("hash_semantics") == "UTF8_TEXT_LF_CANONICAL_V1", f"Phase-2 manifest hash semantics drift: {rel}")

    require(stress.get("baseline_main_commit") == BASELINE_MAIN, "Phase-2 stress baseline drift")
    require(stress.get("authority_gain_count") == 0, "Phase-2 real-case stress authority gain")
    require(stress.get("promotion_eligible") is False, "Phase-2 stress may not claim promotion")
    require(stress.get("independent_review") == "NOT_RUN", "Phase-2 stress may not claim EV4")
    require(set(stress.get("cases", {})) == {"C01", "C04", "FALLINGWATER"}, "Phase-2 stress case set drift")
    for name, row in stress["cases"].items():
        require(row.get("decision") == "HOLD", f"Phase-2 real case unexpectedly advanced: {name}")
        require(row.get("contradiction_count") == 0, f"Phase-2 real case contradiction: {name}")
    print("PHASE2 candidate/receipt/manifest/real-case package: PASS")


def build_decision(projection: dict, label: str) -> tuple[dict, dict]:
    validate_projection(projection)
    stamp = "2026-09-22T17:30:00+08:00"
    projection_bytes = (json.dumps(projection, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    kernel = build_kernel_v0_2(projection, f"fixture:{label}", hashlib.sha256(projection_bytes).hexdigest().upper(), stamp)
    kernel_bytes = (json.dumps(kernel, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    decision = reconcile_v0_2(kernel, f"fixture:{label}:kernel", hashlib.sha256(kernel_bytes).hexdigest().upper(), stamp)
    schema_validate(KERNEL_SCHEMA, kernel, f"{label} kernel")
    schema_validate(RECON_SCHEMA, decision, f"{label} reconciliation")
    require(kernel["kernel_metrics"]["unresolved_identity_ref_count"] == 0, f"{label}: unresolved kernel identity")
    require(kernel["kernel_metrics"]["authority_gain_count"] == 0, f"{label}: authority gain")
    require(kernel["kernel_metrics"]["phase1_module_binding_count"] == 4, f"{label}: Phase-1 binding count drift")
    require(kernel["kernel_metrics"]["phase2_module_binding_count"] == 4, f"{label}: Phase-2 binding count drift")
    require(kernel["kernel_metrics"]["enterprise_module_binding_count"] == 8, f"{label}: enterprise binding count drift")
    require({row["module"] for row in kernel["module_bindings"]} == ALL_MODULES, f"{label}: eight-module binding set drift")
    return kernel, decision


def make_phase2_clear() -> dict:
    d = make_clear_projection(load(PROJECTION))
    # Verification and Validation both require evidence in the clear scenario.
    for row in d["modules"]["mbse"]["verification_validation"]:
        row["result"] = "PASS"
        if not row["evidence_refs"]:
            row["evidence_refs"] = ["READBACK-DEMO-01"]
    d["state_facets"]["agent_runtime"] = {"SESSION-DEMO-01": "SUCCEEDED_READBACK_OBSERVED"}
    d["reconciliation"]["enterprise_readiness_state"] = "READY_FOR_EVALUATION"
    d["reconciliation"]["partial_side_effect_state"] = "NONE"
    unresolved_blocking = sum(1 for row in d["digital_thread"]["unresolved_links"] if row.get("blocking"))
    scope_counts = {state: 0 for state in ["TRIGGERED", "PARTIAL", "NOT_TRIGGERED", "HOLD"]}
    for module in d["modules"].values():
        scope_counts[module["header"]["scope_state"]] += 1
    d["control_metrics"]["unresolved_blocking_link_count"] = unresolved_blocking
    d["control_metrics"]["module_scope_counts"] = scope_counts
    d["control_metrics"]["module_triggered_coverage"] = scope_counts["TRIGGERED"] / 8
    return d


def main() -> int:
    validate_phase2_package()
    stored_kernel = load(KERNEL)
    stored_recon = load(RECON)
    schema_validate(KERNEL_SCHEMA, stored_kernel, "stored kernel")
    schema_validate(RECON_SCHEMA, stored_recon, "stored reconciliation")
    require({row["module"] for row in stored_kernel["module_bindings"]} == ALL_MODULES, "stored kernel missing Phase-2 modules")
    require(stored_kernel["kernel_metrics"]["unresolved_identity_ref_count"] == 0, "stored kernel unresolved identities")
    print("PHASE2 stored eight-module kernel/reconciliation: PASS")

    clear = make_phase2_clear()
    clear_kernel, clear_decision = build_decision(clear, "PHASE2-CLEAR")
    require(clear_decision["advance_decision"] == "ALLOW", "Phase-2 true-clear scenario did not ALLOW")
    require(not clear_decision["blocking_conditions"], "Phase-2 true-clear scenario has blockers")
    print("PHASE2 true-clear eight-module chain: PASS")

    # MES false complete: mutate built kernel after projection validation so reconciliation itself must catch it.
    mes_kernel = copy.deepcopy(clear_kernel)
    operation = next(row for row in mes_kernel["work_items"] if row["work_class"] == "OPERATION")
    for rb in operation["readback_refs"]:
        for row in mes_kernel["readbacks"]:
            if row["readback_id"] == rb:
                row["readback_state"] = "MISSING"
    kb = (json.dumps(mes_kernel, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    mes_decision = reconcile_v0_2(mes_kernel, "fixture:MES-NO-RB:kernel", hashlib.sha256(kb).hexdigest().upper(), "2026-09-22T17:31:00+08:00")
    schema_validate(RECON_SCHEMA, mes_decision, "MES missing readback")
    require(mes_decision["advance_decision"] == "HOLD", "MES COMPLETE without observed readback escaped")
    require("MES_READBACK_MISSING" in {b["blocker_class"] for b in mes_decision["blocking_conditions"]}, "MES specific blocker missing")
    require(operation["readback_refs"][0] in mes_decision["required_readback_set"], "MES readback action missing")
    print("PHASE2 MES actual-readback gate: PASS")

    # Verification PASS must not erase Validation HOLD; they are distinct claim scopes, not contradictions.
    vv = make_phase2_clear()
    validation = next(row for row in vv["modules"]["mbse"]["verification_validation"] if row["vv_class"] == "VALIDATION")
    validation["result"] = "HOLD"
    validation["evidence_refs"] = []
    _, vv_decision = build_decision(vv, "MBSE-V-NE-V")
    require(vv_decision["advance_decision"] == "HOLD", "Validation HOLD escaped")
    require("MBSE_VALIDATION_INCOMPLETE" in {b["blocker_class"] for b in vv_decision["blocking_conditions"]}, "MBSE Validation blocker missing")
    require(not vv_decision["contradictions"], "Verification PASS + Validation HOLD was falsely classified as contradiction")
    print("PHASE2 MBSE verification != validation: PASS")

    # KG must never create authority gain or a new canonical owner.
    kg_kernel, _ = build_decision(make_phase2_clear(), "KG-AUTHORITY")
    kg_relations = [r for r in kg_kernel["relations"] if r["relation_type"].startswith("PROVENANCE_") or r["relation_id"].startswith("KG-")]
    require(kg_relations and all(r["authority_effect"] == "NONE" for r in kg_relations), "KG relation transferred authority")
    require(kg_kernel["kernel_metrics"]["authority_gain_count"] == 0, "KG caused authority gain")
    print("PHASE2 Knowledge Graph provenance-only authority boundary: PASS")

    # Agent session SUCCEEDED cannot clear an uncertain mutation side effect.
    uncertain = make_phase2_clear()
    action = uncertain["modules"]["agent_runtime"]["actions"][0]
    action["side_effect_state"] = "OBSERVED_UNCERTAIN"
    action["readback_refs"] = []
    uncertain["reconciliation"]["enterprise_readiness_state"] = "HOLD"
    uncertain["reconciliation"]["partial_side_effect_state"] = "OBSERVED_OPEN"
    uncertain["reconciliation"]["advance_allowed"] = False
    _, uncertain_decision = build_decision(uncertain, "AGENT-UNCERTAIN")
    require(uncertain_decision["advance_decision"] == "HOLD", "uncertain Agent side effect escaped")
    require("AGENT_SIDE_EFFECT_UNCERTAIN" in {b["blocker_class"] for b in uncertain_decision["blocking_conditions"]}, "Agent uncertainty blocker missing")
    require(action["action_id"] in uncertain_decision["required_readback_set"], "Agent recovery readback action missing")
    print("PHASE2 Agent uncertain-side-effect gate: PASS")

    conflict = make_phase2_clear()
    conflict["modules"]["agent_runtime"]["leases"][0]["lease_state"] = "CONFLICT"
    _, conflict_decision = build_decision(conflict, "AGENT-LEASE-CONFLICT")
    require(conflict_decision["advance_decision"] == "HOLD", "Agent lease conflict escaped")
    require("AGENT_LEASE_CONFLICT" in {b["blocker_class"] for b in conflict_decision["blocking_conditions"]}, "Agent lease conflict blocker missing")
    print("PHASE2 Agent lease-conflict gate: PASS")

    # Deterministic full eight-module build/reconcile.
    source = load(PROJECTION)
    payload = (json.dumps(source, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest().upper()
    a = build_kernel_v0_2(source, "fixture:phase2-deterministic", digest, "2026-09-22T17:32:00+08:00")
    b = build_kernel_v0_2(source, "fixture:phase2-deterministic", digest, "2026-09-22T17:32:00+08:00")
    require(json.dumps(a, ensure_ascii=False, sort_keys=True) == json.dumps(b, ensure_ascii=False, sort_keys=True), "Phase-2 kernel nondeterministic")
    ab = (json.dumps(a, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    ad = hashlib.sha256(ab).hexdigest().upper()
    ra = reconcile_v0_2(a, "fixture:phase2-deterministic:kernel", ad, "2026-09-22T17:32:00+08:00")
    rb = reconcile_v0_2(b, "fixture:phase2-deterministic:kernel", ad, "2026-09-22T17:32:00+08:00")
    require(json.dumps(ra, ensure_ascii=False, sort_keys=True) == json.dumps(rb, ensure_ascii=False, sort_keys=True), "Phase-2 reconciliation nondeterministic")
    print("PHASE2 deterministic eight-module kernel/reconciliation: PASS")
    print("ENTERPRISE_PHASE2_VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(f"ENTERPRISE_PHASE2_VALIDATION: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
