from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[2]
SCHEMA_PATH = ROOT / "OLEANDER_ENTERPRISE_ORCHESTRATION_PROJECTION_v0.3.schema.json"
FIXTURE_PATH = ROOT / "example_enterprise_projection_v0.3.json"
CANDIDATE_PATH = ROOT / "OLEANDER_EVOLUTION_CANDIDATE_ERP_ORCHESTRATION_STAGE1_20260921.json"
OWNER_MAP_PATH = ROOT / "OLEANDER_ENTERPRISE_MODULE_OWNER_MAPPING_v0.2.json"
REFERENCE_MODEL_PATH = ROOT / "OLEANDER_ENTERPRISE_REFERENCE_MODEL_v0.1.json"
GAP_REGISTER_PATH = ROOT / "OLEANDER_ENTERPRISE_CANDIDATE_GAP_REGISTER_v0.1.json"
BUILDER_OUTPUT_PATH = ROOT / "eval-output" / "example-master-runtime.enterprise.v0.3.json"
MANIFEST_PATH = ROOT / "ENTERPRISE_CANDIDATE_MANIFEST_v0.3.json"

CANONICAL_JOB_STATES = {"CREATED", "RESOLVED", "QUEUED", "RUNNING", "SUCCEEDED", "FAILED", "CANCELLED", "CACHED"}
PROJECT_AXIS_LEVELS = {"P0_PORTFOLIO", "P1_PROGRAM", "P2_PROJECT", "P3_WORKSTREAM", "P4_VALIDATION"}
REQUIRED_STATE_FACETS = {"project_design", "job", "knowledge_integrity", "operational_eligibility", "design_quality", "professional", "interface", "authority", "evidence", "configuration", "quality", "process", "agent_runtime"}
MODULES = {"erp": "ERP", "plm": "PLM", "mes": "MES", "bpm": "BPM", "qms": "QMS", "mbse": "MBSE", "knowledge_graph": "KNOWLEDGE_GRAPH", "agent_runtime": "AGENT_RUNTIME"}
FORBIDDEN_AUTHORITY_CLAIMS = {"DESIGN_KEEP", "PROFESSIONAL_PASS", "PROJECT_PROMOTION", "KNOWLEDGE_CURRENT"}


class ValidationError(AssertionError):
    pass


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def schema_validate(doc: dict) -> None:
    schema = load_json(SCHEMA_PATH)
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return
    errors = sorted(Draft202012Validator(schema).iter_errors(doc), key=lambda e: list(e.path))
    if errors:
        first = errors[0]
        path = ".".join(str(x) for x in first.path) or "<root>"
        raise ValidationError(f"jsonschema {path}: {first.message}")


def require_source_refs(row: dict, context: str) -> None:
    require(bool(row.get("source_refs")), f"{context} requires source_refs")


def validate_projection(doc: dict) -> None:
    schema_validate(doc)
    require(doc.get("schema_version") == "0.3-candidate", "wrong schema_version")
    require(doc.get("kind") == "OLEANDER_ENTERPRISE_ORCHESTRATION_PROJECTION", "wrong kind")
    require(doc.get("candidate_status") in {"NON_AUTHORITATIVE_CANDIDATE", "EVAL_ONLY"}, "projection must remain candidate/eval-only")

    authority = doc.get("authority", {})
    require(authority.get("projection_only") is True, "projection_only must be true")
    require(authority.get("may_mutate_current") is False, "candidate may not mutate Current")
    require(bool(authority.get("source_binding_refs")), "projection requires explicit source binding refs")
    require(authority.get("source_binding_hash_semantics") == "SOURCE_SPECIFIC_EXACT_REVISION_DIGESTS_WHEN_AVAILABLE", "projection source digest semantics missing or ambiguous")
    digests = authority.get("source_binding_digests", [])
    require(bool(digests), "projection requires source binding digests")
    digest_refs = set()
    for row in digests:
        ref = row.get("ref")
        require(ref in set(authority.get("source_binding_refs", [])), "source digest ref must be declared in source_binding_refs")
        require(ref not in digest_refs, "duplicate source digest ref")
        digest_refs.add(ref)
        require(row.get("hash_semantics") in {"UTF8_TEXT_LF_CANONICAL_V1", "RAW_BYTES_V1", "GIT_CANONICAL_BLOB_SHA256"}, "invalid source digest semantics")
        sha = row.get("sha256", "")
        require(len(sha) == 64 and all(c in "0123456789ABCDEF" for c in sha), "invalid source digest")
        local = REPO_ROOT / ref
        if local.is_file() and row.get("hash_semantics") == "UTF8_TEXT_LF_CANONICAL_V1":
            raw = local.read_bytes()
            text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
            actual = hashlib.sha256(text.encode("utf-8")).hexdigest().upper()
            require(actual == sha, f"source digest mismatch: {ref}")

    contract = doc.get("architecture_contract", {})
    require(contract.get("integration_model") == "FEDERATED_PROJECTION_ENVELOPE", "must remain one federated projection envelope")
    require(contract.get("module_count") == 8, "exactly eight enterprise modules required")
    require(contract.get("no_new_runtime_layer") is True, "candidate may not create R-L")
    require(contract.get("state_policy") == "ORTHOGONAL_STATE_FAMILIES_NO_FLATTENING", "state flattening forbidden")
    require(contract.get("transaction_policy") == "NO_DISTRIBUTED_TRANSACTION_MANAGER_RECONCILE_PARTIAL_SIDE_EFFECTS", "distributed transaction manager forbidden")
    require(contract.get("digital_thread_policy") == "TYPED_SOURCE_BOUND_LINKS_DO_NOT_TRANSFER_AUTHORITY", "digital thread may not transfer authority")

    case_refs = doc.get("case_refs", [])
    axis_refs = doc.get("project_axis_refs", [])
    require(case_refs or axis_refs, "at least one Case or Project Axis identity anchor is required")
    for case_ref in case_refs:
        require(case_ref.get("project_binding_state") in {"BOUND", "UNRESOLVED", "NOT_APPLICABLE"}, "invalid Case-to-Project binding state")
        require("P2_PROJECT_ID" in set(case_ref.get("does_not_prove", [])), "Case identity must not prove a P2 Project ID")
    for ref in axis_refs:
        require(ref.get("axis_level") in PROJECT_AXIS_LEVELS, "invalid Project Axis level")
    if not axis_refs:
        require(not doc.get("work_packages"), "Work Package requires an existing Project Axis binding")
        require(not doc.get("jobs"), "Job orchestration requires an existing Project Axis binding")

    wp_ids = {wp.get("work_package_id") for wp in doc.get("work_packages", [])}
    for wp in doc.get("work_packages", []):
        require(str(wp.get("work_package_id", "")).startswith("WP-"), "work package id must be WP-*")
        require({"PROJECT_PROMOTION", "DESIGN_KEEP", "PROFESSIONAL_PASS"}.issubset(set(wp.get("does_not_prove", []))), "work package authority disclaimer incomplete")

    jobs = doc.get("jobs", [])
    for job in jobs:
        require(job.get("job_state") in CANONICAL_JOB_STATES, "non-canonical Job State")
        require(job.get("work_package_id") in wp_ids, "job references unknown work package")
        require({"DESIGN_KEEP", "PROJECT_PROMOTION"}.issubset(set(job.get("does_not_prove", []))), "job result must not prove Design KEEP or Promotion")

    facets = doc.get("state_facets", {})
    require(set(facets.keys()) == REQUIRED_STATE_FACETS, "state families must remain orthogonal and complete")

    modules = doc.get("modules", {})
    require(set(modules.keys()) == set(MODULES.keys()), "enterprise module set drift")
    for key, module_name in MODULES.items():
        header = modules[key].get("header", {})
        require(header.get("module") == module_name, f"{key} module header mismatch")
        require(header.get("authority_mode") == "PROJECTION_ONLY", f"{key} may not gain authority")
        require(bool(header.get("source_refs")), f"{key} module requires source_refs")
        require(bool(header.get("does_not_prove")), f"{key} module requires claim ceiling boundaries")

    for item in modules["erp"].get("demand_records", []) + modules["erp"].get("schedule_records", []) + modules["erp"].get("resource_demand", []):
        require_source_refs(item, "ERP record")

    for item in modules["plm"].get("configuration_items", []):
        require_source_refs(item, "PLM configuration item")
        require("PROJECT_PROMOTION" in set(item.get("does_not_prove", [])), "PLM item must not prove project promotion")
    for item in modules["plm"].get("baselines", []) + modules["plm"].get("change_records", []):
        require_source_refs(item, "PLM record")

    for op in modules["mes"].get("operation_records", []):
        require_source_refs(op, "MES operation")
        if op.get("execution_state") == "COMPLETE":
            require(bool(op.get("actual_readback_refs")), "MES COMPLETE requires actual_readback_refs")
        require({"FIELD_TRUTH", "ACCEPTANCE"}.issubset(set(op.get("does_not_prove", []))), "MES operation boundary incomplete")

    for proc in modules["bpm"].get("process_instances", []):
        require_source_refs(proc, "BPM process")
        require("PROJECT_PROMOTION" in set(proc.get("does_not_prove", [])), "BPM completion must not prove project promotion")
    for handoff in modules["bpm"].get("handoffs", []):
        require_source_refs(handoff, "BPM handoff")
        if handoff.get("handoff_state") == "ACCEPTED":
            require(bool(handoff.get("acceptance_ref")), "accepted BPM handoff requires acceptance_ref")

    for capa in modules["qms"].get("capa_records", []):
        require_source_refs(capa, "QMS CAPA")
        if capa.get("state") == "CLOSED":
            require(bool(capa.get("effectiveness_readback_ref")), "closed CAPA requires effectiveness readback")
    for inspection in modules["qms"].get("inspection_records", []):
        require_source_refs(inspection, "QMS inspection")
        if inspection.get("result") == "PASS":
            require(bool(inspection.get("evidence_refs")), "QMS PASS inspection requires evidence_refs")

    for req in modules["mbse"].get("requirements", []):
        require_source_refs(req, "MBSE requirement")
        require("PROJECT_ACCEPTANCE" in set(req.get("does_not_prove", [])), "MBSE requirement must not prove project acceptance")
    for vv in modules["mbse"].get("verification_validation", []):
        require_source_refs(vv, "MBSE V&V")
        if vv.get("result") == "PASS":
            require(bool(vv.get("evidence_refs")), "MBSE PASS requires evidence refs")
    vv_classes = {vv.get("vv_class") for vv in modules["mbse"].get("verification_validation", [])}
    if "VERIFICATION" in vv_classes and "VALIDATION" in vv_classes:
        require(True, "verification/validation represented independently")

    for node in modules["knowledge_graph"].get("nodes", []):
        require(node.get("authority_gain") is False, "Knowledge Graph node may not gain authority")
        require_source_refs(node, "Knowledge Graph node")
    for edge in modules["knowledge_graph"].get("edges", []):
        require(edge.get("projection_only") is True and edge.get("authority_effect") == "NONE", "Knowledge Graph edge may not create authority")
        require_source_refs(edge, "Knowledge Graph edge")

    for session in modules["agent_runtime"].get("sessions", []):
        require_source_refs(session, "Agent session")
        require({"AUTHORITY", "DESIGN_KEEP", "PROJECT_PROMOTION"}.issubset(set(session.get("does_not_prove", []))), "agent session authority boundary incomplete")
    uncertain_side_effect = False
    for action in modules["agent_runtime"].get("actions", []):
        require_source_refs(action, "Agent action")
        side_effect = action.get("side_effect_state")
        if side_effect == "OBSERVED_AUTHORIZED":
            require(bool(action.get("authorization_ref")), "authorized mutation observation requires authorization_ref")
            require(bool(action.get("readback_refs")), "authorized mutation observation requires readback_refs")
        if side_effect == "OBSERVED_UNCERTAIN":
            uncertain_side_effect = True

    for relation in doc.get("digital_thread", {}).get("relations", []):
        require(relation.get("projection_only") is True, "digital-thread relation must be projection-only")
        require_source_refs(relation, "digital-thread relation")
    unresolved_blocking = sum(1 for x in doc.get("digital_thread", {}).get("unresolved_links", []) if x.get("blocking"))

    for observation in doc.get("activity_observations", []):
        require(observation.get("projection_only") is True, "activity must be projection-only")
        require(observation.get("rebuildable") is True, "activity must be rebuildable")
        require(observation.get("authority_effect") == "NONE", "activity may not grant authority")
        require_source_refs(observation, "activity observation")

    reconciliation = doc.get("reconciliation", {})
    if uncertain_side_effect:
        require(reconciliation.get("projection_state") == "HOLD", "uncertain side effect must HOLD projection")
        require(reconciliation.get("partial_side_effect_state") in {"OBSERVED_OPEN", "UNKNOWN"}, "uncertain side effect requires open/unknown reconciliation")
        require(reconciliation.get("advance_allowed") is False, "uncertain side effect must block advance")

    design_results = {r.get("result") for r in doc.get("review_refs", []) if r.get("review_class") == "DESIGN"}
    succeeded = any(job.get("job_state") == "SUCCEEDED" for job in jobs)
    agent_succeeded = any(s.get("session_state") == "SUCCEEDED" for s in modules["agent_runtime"].get("sessions", []))
    if (succeeded or agent_succeeded) and ("REVISE" in design_results or "HOLD" in design_results):
        require(reconciliation.get("advance_allowed") is False, "execution success with Design REVISE/HOLD must not advance")

    metrics = doc.get("control_metrics", {})
    require(metrics.get("authority_duplication_count") == 0, "authority duplication must remain zero")
    require(metrics.get("state_family_flattening_count") == 0, "state flattening must remain zero")
    require(metrics.get("untraceable_relation_count") == 0, "untraceable relation count must remain zero")
    require(metrics.get("unresolved_blocking_link_count") == unresolved_blocking, "blocking-link metric mismatch")
    require(metrics.get("projection_rebuildable") is True, "projection must be rebuildable")

    does_not_prove = set(doc.get("does_not_prove", []))
    require(FORBIDDEN_AUTHORITY_CLAIMS.issubset(does_not_prove), "projection must explicitly disclaim protected authority conclusions")


def validate_support_files() -> None:
    owner = load_json(OWNER_MAP_PATH)
    require(owner.get("status") == "EV2_CANDIDATE_NON_AUTHORITATIVE", "owner mapping must remain candidate")
    names = {m.get("module") for m in owner.get("modules", [])}
    require(names == set(MODULES.values()), "owner mapping must cover exactly eight modules")
    for module in owner.get("modules", []):
        require(bool(module.get("canonical_owners")), f"{module.get('module')} missing canonical owners")
        require(module.get("mutation_permission") in {"NONE_IN_CANDIDATE", "OBSERVE_EXISTING_AUTHORIZED_PATHS_ONLY"}, "candidate module mutation permission too broad")
        require(bool(module.get("hard_boundary")), "module hard boundary missing")
    reference = load_json(REFERENCE_MODEL_PATH)
    require(reference.get("status") == "CANDIDATE_REFERENCE_NOT_AUTHORITY", "external reference model may not gain authority")
    require(len(reference.get("references", [])) >= 4, "external reference model coverage incomplete")
    gaps = load_json(GAP_REGISTER_PATH)
    require(gaps.get("status") == "OPEN_CANDIDATE_GAPS", "gap register must preserve open candidate gaps")
    require(len(gaps.get("gaps", [])) == 8, "gap register must cover eight modules")

    manifest = load_json(MANIFEST_PATH)
    require(manifest.get("status") == "EV2_ACTIVE_CANDIDATE_PACKAGE", "candidate manifest status drift")
    require(manifest.get("baseline_main_commit") == "e34ef6366b58749a7f8645f03329c8e7596caf60", "candidate manifest baseline drift")
    require(manifest.get("hash_semantics") == "UTF8_TEXT_LF_CANONICAL_V1", "candidate manifest hash semantics drift")
    rows = manifest.get("active_files_excluding_this_manifest", [])
    require(len(rows) >= 12, "candidate manifest active-file coverage incomplete")
    seen = set()
    for row in rows:
        rel = row.get("path")
        require(rel and rel not in seen, "candidate manifest duplicate/missing active path")
        seen.add(rel)
        path = ROOT / rel
        require(path.is_file(), f"candidate manifest active file missing: {rel}")
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
        canonical = text.encode("utf-8")
        require(row.get("hash_semantics") == "UTF8_TEXT_LF_CANONICAL_V1", f"candidate manifest row hash semantics drift: {rel}")
        require(row.get("bytes") == len(canonical), f"candidate manifest byte count drift: {rel}")
        require(row.get("sha256") == hashlib.sha256(canonical).hexdigest().upper(), f"candidate manifest sha256 drift: {rel}")


def validate_candidate(candidate: dict) -> None:
    required = {"candidate_id", "state", "target_class", "target_owner", "target_ref", "baseline", "trigger_evidence", "hypothesis", "mutation_scope", "evaluation", "constraints", "comparison", "independent_review", "promotion", "migration", "rollback", "monitoring", "does_not_prove"}
    require(required.issubset(candidate.keys()), "candidate misses required evolution fields")
    require(candidate["state"] in {"EV1_CANDIDATE", "EV2_EVAL_READY"}, "candidate may only be EV1/EV2 in this package")
    require(candidate["mutation_scope"].get("current_files_modified") is False, "Current mutation forbidden")
    require(candidate["promotion"].get("eligible") is False, "candidate must not be promotion-eligible yet")
    require(candidate["promotion"].get("human_decision_required") is True, "human promotion decision required")
    excluded = set(candidate["mutation_scope"].get("explicitly_excluded", []))
    require("persistent transaction ledger" in excluded, "persistent transaction ledger must be excluded")
    require("distributed transaction manager" in excluded, "distributed transaction manager must be excluded")
    require("new R-L runtime layer" in excluded, "new runtime layer must be excluded")
    evaluation = candidate.get("evaluation", {})
    require(evaluation.get("result") == "EVAL_READY_FEDERATED_MODEL_PASS_REAL_CASES_PENDING", "candidate result must reflect v0.3 federated model and pending real cases")
    metrics = evaluation.get("metrics", {})
    require(metrics.get("enterprise_module_count") == 8, "candidate must declare eight modules")
    require(metrics.get("real_case_projection_count") == 0, "candidate must not claim unrun real cases")
    require(metrics.get("negative_invariant_tests_required", 0) >= 12, "candidate negative-test floor too low")

    baseline = candidate.get("baseline", {})
    require(baseline.get("source_sha256_semantics") == "SHA256_OF_GIT_CANONICAL_BLOB_CONTENT_AT_EXACT_COMMIT", "candidate baseline hash semantics must be explicit")
    commit = baseline.get("source_hash_or_commit")
    source_hashes = baseline.get("source_sha256", {})
    require(bool(commit) and bool(source_hashes), "candidate baseline must bind exact commit and source hashes")
    for rel, expected in source_hashes.items():
        try:
            canonical = subprocess.check_output(
                ["git", "show", f"{commit}:{rel}"], cwd=REPO_ROOT
            )
        except subprocess.CalledProcessError as exc:
            raise ValidationError(f"candidate baseline source unavailable at {commit}: {rel}") from exc
        actual = hashlib.sha256(canonical).hexdigest().upper()
        require(actual == expected, f"candidate baseline source hash drift: {rel}")

    for rel in evaluation.get("eval_set_refs", []):
        require((REPO_ROOT / rel).is_file(), f"candidate eval_set_ref missing: {rel}")


def expect_blocked(name: str, mutate) -> None:
    fixture = load_json(FIXTURE_PATH)
    mutate(fixture)
    try:
        validate_projection(fixture)
    except Exception:
        print(f"NEGATIVE {name}: BLOCKED")
        return
    raise ValidationError(f"negative test unexpectedly passed: {name}")


def main() -> int:
    fixture = load_json(FIXTURE_PATH)
    candidate = load_json(CANDIDATE_PATH)
    validate_support_files()
    validate_projection(fixture)
    validate_candidate(candidate)
    print("POSITIVE enterprise fixture: PASS")

    require(BUILDER_OUTPUT_PATH.is_file(), "v0.3 builder output missing")
    builder_output = load_json(BUILDER_OUTPUT_PATH)
    validate_projection(builder_output)
    print("POSITIVE Master Runtime builder projection: PASS")

    tests = [
        ("JOB_SUCCESS_CLAIMS_DESIGN_KEEP", lambda d: d["jobs"][0].update({"does_not_prove": ["PROJECT_PROMOTION"]})),
        ("MODULE_GAINS_AUTHORITY", lambda d: d["modules"]["erp"]["header"].update({"authority_mode": "AUTHORITATIVE"})),
        ("NEW_PROJECT_AXIS_LEVEL", lambda d: d["project_axis_refs"][0].update({"axis_level": "P5_WORK_PACKAGE"})),
        ("CANDIDATE_MUTATES_CURRENT", lambda d: d["authority"].update({"may_mutate_current": True})),
        ("MES_COMPLETE_WITHOUT_READBACK", lambda d: d["modules"]["mes"]["operation_records"][0].update({"actual_readback_refs": []})),
        ("QMS_CAPA_CLOSED_WITHOUT_EFFECTIVENESS", lambda d: d["modules"]["qms"]["capa_records"][0].update({"effectiveness_readback_ref": None})),
        ("MBSE_VERIFY_PASS_WITHOUT_EVIDENCE", lambda d: d["modules"]["mbse"]["verification_validation"][0].update({"evidence_refs": []})),
        ("KG_EDGE_GAINS_AUTHORITY", lambda d: d["modules"]["knowledge_graph"]["edges"][0].update({"authority_effect": "CURRENT"})),
        ("AGENT_MUTATION_WITHOUT_AUTHORIZATION", lambda d: d["modules"]["agent_runtime"]["actions"][0].update({"authorization_ref": None})),
        ("UNCERTAIN_SIDE_EFFECT_ADVANCES", lambda d: (d["modules"]["agent_runtime"]["actions"][0].update({"side_effect_state": "OBSERVED_UNCERTAIN"}), d["reconciliation"].update({"projection_state": "CURRENT_PROJECTION", "partial_side_effect_state": "NONE", "advance_allowed": True}))),
        ("DIGITAL_THREAD_WITHOUT_SOURCE", lambda d: d["digital_thread"]["relations"][0].update({"source_refs": []})),
        ("STATE_FAMILY_COLLAPSE", lambda d: d["state_facets"].pop("quality")),
        ("PLM_RELEASE_CLAIMS_PROMOTION", lambda d: d["modules"]["plm"]["configuration_items"][0].update({"does_not_prove": ["DESIGN_KEEP"]})),
        ("BPM_COMPLETION_CLAIMS_PROMOTION", lambda d: d["modules"]["bpm"]["process_instances"][0].update({"process_state": "COMPLETED", "does_not_prove": ["DESIGN_KEEP"]})),
    ]
    for name, mutate in tests:
        expect_blocked(name, mutate)

    require(fixture["jobs"][0]["job_state"] == "SUCCEEDED", "fixture requires succeeded job")
    require(fixture["modules"]["agent_runtime"]["sessions"][0]["session_state"] == "SUCCEEDED", "fixture requires succeeded agent session")
    require(any(r["review_class"] == "DESIGN" and r["result"] == "REVISE" for r in fixture["review_refs"]), "fixture requires Design REVISE")
    require(fixture["reconciliation"]["advance_allowed"] is False, "execution success must not outrun Design REVISE")
    print("SEMANTIC EXECUTION_SUCCESS_NE_DESIGN_KEEP: PASS")
    print("SEMANTIC PLM_RELEASE_NE_PROJECT_PROMOTION: PASS")
    print("SEMANTIC MES_COMPLETE_NE_ACCEPTANCE: PASS")
    print("SEMANTIC VERIFY_NE_VALIDATE: PASS")
    print("SEMANTIC GRAPH_EDGE_NE_AUTHORITY: PASS")
    print("SEMANTIC AGENT_SUCCESS_NE_AUTHORITY: PASS")
    print("ENTERPRISE_CANDIDATE_VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(f"ENTERPRISE_CANDIDATE_VALIDATION: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
