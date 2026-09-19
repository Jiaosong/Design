#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"

CONTRACT_FILES = {
    "capability": RUNTIME / "OLEANDER_SKILL_CAPABILITY_CONTRACT_v0.1.json",
    "dag": RUNTIME / "OLEANDER_MULTI_SKILL_EXECUTION_DAG_CONTRACT_v0.1.json",
    "tool": RUNTIME / "OLEANDER_TOOL_ADAPTER_CONTRACT_v0.1.json",
    "artifact": RUNTIME / "OLEANDER_NATIVE_ARTIFACT_CONTRACT_v0.1.json",
    "regression": RUNTIME / "OLEANDER_EXECUTION_REGRESSION_CONTRACT_v0.1.json",
    "drift": RUNTIME / "OLEANDER_NOTION_GITHUB_DRIFT_CHECK_v0.1.json",
}
EXPECTED_IDS = {
    "capability": "OLEANDER_SKILL_CAPABILITY_CONTRACT",
    "dag": "OLEANDER_MULTI_SKILL_EXECUTION_DAG_CONTRACT",
    "tool": "OLEANDER_TOOL_ADAPTER_CONTRACT",
    "artifact": "OLEANDER_NATIVE_ARTIFACT_CONTRACT",
    "regression": "OLEANDER_EXECUTION_REGRESSION_CONTRACT",
    "drift": "OLEANDER_NOTION_GITHUB_DRIFT_CHECK",
}
RESOLVER_CURRENT = RUNTIME / "OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json"
RESOLVER_PREVIOUS = RUNTIME / "OLEANDER_DEFAULT_SKILL_RESOLVER_v1.1.json"
OWNER_MAP = RUNTIME / "OLEANDER_NOTION_TO_GITHUB_EXECUTION_OWNER_MAP_v1.0.json"
CONTROL_GRAPH = RUNTIME / "OLEANDER_ARCHITECTURE_CONTROL_GRAPH_v2.1.json"
RECEIPT_CONTRACT = RUNTIME / "OLEANDER_EXECUTION_RECEIPT_v1.0.json"
RECEIPT_DIR = RUNTIME / "receipts"
LIFECYCLE_BASELINE = RUNTIME / "skill-lifecycle" / "BASELINE_ADOPTION_2026-08-18.json"
LIFECYCLE_DIR = RUNTIME / "skill-lifecycle"
REVIEW = ROOT / "oleander-skills" / "REVIEW.md"
GOLDEN_SKILLS = ROOT / "evals" / "golden" / "skills.jsonl"
UI_CANDIDATE_GOLDEN = ROOT / "evals" / "golden" / "ui_candidate_stack.jsonl"
GAME_STACK = ROOT / "skills" / "oleander-game-ui-stack" / "README.md"
README = RUNTIME / "README.md"


def fail(msg: str) -> None:
    raise SystemExit(f"execution-contract validation failed: {msg}")


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


def require_fields(obj: dict, fields: list[str] | set[str], context: str) -> None:
    missing = [f for f in fields if f not in obj or obj[f] in (None, "", [])]
    if missing:
        fail(f"{context} missing required fields {sorted(missing)}")


def require_present_fields(obj: dict, fields: list[str] | set[str], context: str) -> None:
    missing = [f for f in fields if f not in obj or obj[f] in (None, "")]
    if missing:
        fail(f"{context} missing required fields {sorted(missing)}")


def installed_from_review() -> set[str]:
    text = REVIEW.read_text(encoding="utf-8")
    if "## Installed skills" not in text:
        fail("oleander-skills/REVIEW.md missing Installed skills section")
    section = text.split("## Installed skills", 1)[1].split("## Retrieval alias", 1)[0]
    ids = set(re.findall(r"^- `([^`]+)`:", section, flags=re.M))
    if not ids:
        fail("could not parse installed skills from REVIEW.md")
    return ids


def validate_current_resolver_and_pointers() -> tuple[dict, dict]:
    current = load_json(RESOLVER_CURRENT)
    previous = load_json(RESOLVER_PREVIOUS)
    if current.get("version") != "1.2" or current.get("status") != "ACTIVE_CURRENT":
        fail("resolver v1.2 must be the sole ACTIVE_CURRENT resolver")
    if previous.get("status") != "SUPERSEDED":
        fail("resolver v1.1 must be SUPERSEDED after v1.2")
    if previous.get("superseded_by") != str(RESOLVER_CURRENT.relative_to(ROOT)).replace("\\", "/"):
        fail("resolver v1.1 superseded_by pointer mismatch")

    owner_map = load_json(OWNER_MAP)
    expected_pointer = str(RESOLVER_CURRENT.relative_to(ROOT)).replace("\\", "/")
    if owner_map.get("authority", {}).get("default_skill_resolver") != expected_pointer:
        fail("Execution Owner Map does not point to resolver v1.2")

    readme = README.read_text(encoding="utf-8")
    for name in [
        "OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.md",
        "OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json",
        "OLEANDER_EXECUTION_RECEIPT_v1.0.md",
        "OLEANDER_EXECUTION_RECEIPT_v1.0.json",
    ]:
        if name not in readme:
            fail(f"runtime README missing Current pointer {name}")
    if "v1.1.md/.json` is superseded" not in readme:
        fail("runtime README must explicitly mark resolver v1.1 superseded")

    order = current.get("default_resolution_order", [])
    closure_cleanup = current.get("closure_cleanup", {})
    require_fields(
        closure_cleanup,
        [
            "git_branch_ref_disposition",
            "contract",
            "local_tool",
            "run_after_main_readback_when_merge_occurred",
            "protect",
            "bulk_delete_requires_ref_sha_audit",
            "unmerged_age_only_delete_forbidden",
            "delete_branch_on_merge_global_switch_not_required",
            "does_not_create",
        ],
        "resolver-v1.2:closure-cleanup",
    )
    if closure_cleanup.get("local_tool") != "00-governance/runtime/github_branch_governance.py":
        fail("resolver closure cleanup must use the canonical Git branch governance tool")
    if not {"OPEN_PR_HEAD", "OPEN_PR_BASE", "ACTIVE_WORKTREE", "EXPLICIT_KEEP"}.issubset(set(closure_cleanup.get("protect", []))):
        fail("resolver closure cleanup branch dependency protections incomplete")
    if closure_cleanup.get("bulk_delete_requires_ref_sha_audit") is not True or closure_cleanup.get("unmerged_age_only_delete_forbidden") is not True:
        fail("resolver closure cleanup must preserve ref audit and forbid age-only unmerged deletion")
    required_order = [
        "RESOLVE_PROFESSIONAL_PROCESS_CURRENT_OR_BOUNDED_CANDIDATE_EVALUATION_MODE",
        "PROFESSIONAL_STAGE",
        "PROFESSIONAL_QUESTION_OR_DECISION_OBJECT",
        "KNOWLEDGE_INPUTS",
        "OPERATIONAL_KNOWLEDGE_MOUNT",
        "REQUIRED_CAPABILITY_ROLES",
        "CURRENT_EXECUTION_OWNERS_OR_SKILLS",
        "RESOLVE_EXECUTION_OWNER_MAP",
        "LOAD_SKILL_CAPABILITY_CONTRACT",
        "SELECT_MINIMUM_SUFFICIENT_EXECUTION_OWNER_SET",
        "RESOLVE_TOOL_ADAPTERS_WHEN_REQUIRED",
        "NATIVE_OUTPUTS",
        "DEFINE_REQUIRED_NATIVE_OUTPUT",
        "EXECUTE_ACTUAL_NATIVE_ARTIFACT",
        "EMIT_NATIVE_ARTIFACT_RECORDS_AND_TYPED_HANDOFFS",
        "RUN_STRUCTURAL_SEMANTIC_VISUAL_ROI_RUNTIME_REGRESSION_AS_APPLICABLE",
        "ACTUAL_READBACK",
        "READ_BACK_CAPABILITY_COVERAGE_BEFORE_STAGE_CLOSURE",
        "INDEPENDENT_REVIEW",
        "EVIDENCE_GATE",
        "INDEPENDENT_DESIGN_QUALITY_GATE",
        "STAGE_CLOSURE",
        "EMIT_EXECUTION_RECEIPT",
    ]
    positions = []
    for token in required_order:
        if token not in order:
            fail(f"resolver v1.2 missing execution-order token {token}")
        positions.append(order.index(token))
    if positions != sorted(positions):
        fail("resolver v1.2 execution-contract order is inconsistent")

    canonical_chain = current.get("canonical_professional_stage_execution_chain", {})
    require_fields(
        canonical_chain,
        [
            "chain",
            "is_single_canonical_stage_spine",
            "ordering_rule",
            "auxiliary_bindings_do_not_insert_new_top_level_steps",
            "auxiliary_substeps",
            "closure_rule",
            "does_not_create",
        ],
        "resolver-v1.2:canonical-professional-stage-execution-chain",
    )
    expected_chain = [
        "PROFESSIONAL_STAGE",
        "PROFESSIONAL_QUESTION_OR_DECISION_OBJECT",
        "KNOWLEDGE_INPUTS",
        "OPERATIONAL_KNOWLEDGE_MOUNT",
        "REQUIRED_CAPABILITY_ROLES",
        "CURRENT_EXECUTION_OWNERS_OR_SKILLS",
        "NATIVE_OUTPUTS",
        "ACTUAL_READBACK",
        "INDEPENDENT_REVIEW",
        "STAGE_CLOSURE",
    ]
    if canonical_chain.get("chain") != expected_chain:
        fail("canonical professional-stage execution chain order drift")
    if canonical_chain.get("is_single_canonical_stage_spine") is not True:
        fail("professional-stage execution chain must remain the single canonical stage spine")
    top_positions = [order.index(token) for token in expected_chain]
    if top_positions != sorted(top_positions):
        fail("default resolver order violates canonical professional-stage execution chain")

    stage_comp = current.get("stage_composition_policy", {})
    require_fields(
        stage_comp,
        [
            "purpose",
            "minimum_sufficient_means",
            "minimum_sufficient_does_not_mean",
            "resolve_sequence",
            "recompute_on",
            "stage_transition_rule",
            "multi_skill_required_when",
            "single_owner_allowed_when",
            "selective_reroute_rule",
            "forbidden_compressions",
            "does_not_create",
        ],
        "resolver-v1.2:stage-composition",
    )
    if stage_comp.get("minimum_sufficient_does_not_mean") != "MINIMUM_SKILL_COUNT":
        fail("resolver stage composition must explicitly reject minimum-skill-count interpretation")
    for token in [
        "READ_PROFESSIONAL_STAGE_AND_PROFESSIONAL_QUESTION_OR_DECISION_OBJECT",
        "RESOLVE_ACTIVE_PROFESSIONAL_STAGE_KNOWLEDGE_INPUTS",
        "BIND_AND_VALIDATE_OPERATIONAL_KNOWLEDGE_MOUNT",
        "RESOLVE_REQUIRED_CAPABILITY_ROLES",
        "SELECT_CURRENT_EXECUTION_OWNERS_OR_SKILLS",
        "HOLD_CANDIDATE_SKILL_OR_CANDIDATE_BODY_AS_NON_CURRENT_UNLESS_EXPLICIT_LEGAL_PROJECT_SPECIALIST_OVERRIDE",
        "DEDUPE_ONLY_AFTER_CAPABILITY_COVERAGE_IS_PROVEN",
        "BIND_AND_EXECUTE_REQUIRED_NATIVE_OUTPUTS",
        "ACTUAL_READBACK",
        "INDEPENDENT_REVIEW_WHEN_TRIGGERED",
        "STAGE_CLOSURE_GATE",
    ]:
        if token not in stage_comp.get("resolve_sequence", []):
            fail(f"resolver stage composition missing resolve token {token}")
    for token in [
        "PROFESSIONAL_STAGE_CHANGE",
        "REQUIRED_NATIVE_OUTPUT_OR_READBACK_CHANGE",
        "HOLD_RELEASE_CONDITION_ACTIVATES_NEW_VERIFICATION_PATH",
        "ACTUAL_READBACK_PROVES_CAPABILITY_GAP",
    ]:
        if token not in stage_comp.get("recompute_on", []):
            fail(f"resolver stage composition missing recompute trigger {token}")

    knowledge_policy = current.get("professional_stage_knowledge_mount_policy", {})
    require_fields(
        knowledge_policy,
        [
            "purpose",
            "contract_ref",
            "active_input_rule",
            "required_mount_record_fields",
            "eligible_states",
            "accepted_freshness_states",
            "fail_closed_when",
            "does_not_prove",
        ],
        "resolver-v1.2:professional-stage-knowledge-mount",
    )
    if knowledge_policy.get("contract_ref") != "00-governance/knowledge-integrity-and-operational-mount-v1.0.md":
        fail("professional-stage Knowledge Mount policy must bind the Current Knowledge Integrity / Operational Mount owner")
    required_mount_fields = {
        "knowledge_ref",
        "use_role",
        "operational_eligibility",
        "eligibility_scope",
        "claim_ceiling",
        "applicability",
        "conditions",
        "unresolved_items",
        "freshness_state",
        "freshness_or_revalidation_trigger",
        "does_not_prove",
        "review_basis",
        "satisfies_knowledge_inputs",
    }
    if set(knowledge_policy.get("required_mount_record_fields", [])) != required_mount_fields:
        fail("professional-stage Knowledge Mount required record fields drift")
    if not {"OE2", "OE3", "OE2_CONDITIONAL", "OE3_ELIGIBLE"}.issubset(
        set(knowledge_policy.get("eligible_states", []))
    ):
        fail("professional-stage Knowledge Mount eligible states incomplete")
    if set(knowledge_policy.get("accepted_freshness_states", [])) != {"CURRENT", "REVALIDATED_CURRENT"}:
        fail("professional-stage Knowledge Mount freshness states must fail closed outside Current/revalidated Current")
    for token in {
        "ACTIVE_KNOWLEDGE_INPUT_HAS_NO_USABLE_MOUNT",
        "MOUNT_IS_OE1_OR_NOT_ELIGIBLE",
        "MOUNT_IS_STALE_UNKNOWN_OR_REVALIDATION_REQUIRED",
        "OMITTED_KNOWLEDGE_INPUT_HAS_NO_EXPLICIT_REASON",
    }:
        if token not in knowledge_policy.get("fail_closed_when", []):
            fail(f"professional-stage Knowledge Mount policy missing fail-closed token {token}")

    candidate_policy = current.get("candidate_professional_process_evaluation_policy", {})
    require_fields(
        candidate_policy,
        [
            "purpose",
            "eligible_graph_state",
            "requires_candidate_refs",
            "evaluation_mode",
            "authority_rule",
            "exact_binding_required",
            "entry_requires",
            "exercise_sequence",
            "problem_record_requires",
            "hold_release_rule",
            "stage_recomposition_evidence_required",
            "candidate_result_never_means",
            "does_not_create",
        ],
        "resolver-v1.2:candidate-professional-process-evaluation",
    )
    if candidate_policy.get("eligible_graph_state") != "CONTRACT_ENVELOPE_AVAILABLE_PROCESS_OPEN":
        fail("candidate professional-process evaluation must bind PROCESS_OPEN graph state")
    if candidate_policy.get("evaluation_mode") != "BOUNDED_NON_CURRENT_PROJECT_EXERCISE":
        fail("candidate professional-process evaluation mode drift")
    if "CURRENT_PROCESS_REF_REMAINS_NULL" not in candidate_policy.get("authority_rule", ""):
        fail("candidate professional-process evaluation must keep current_process_ref null")
    if candidate_policy.get("stage_recomposition_evidence_required") is not True:
        fail("candidate professional-process evaluation must require stage recomposition evidence")
    for token in {
        "RESOLVE_ACTIVE_KNOWLEDGE_INPUTS",
        "BIND_AND_VALIDATE_TASK_CLAIM_KNOWLEDGE_MOUNTS",
        "HOLD_NON_CURRENT_CANDIDATE_SKILL_OWNERS",
        "RECORD_HOLD_REVISE_REJECT_OR_PASS_WITH_CLAIM_CEILING",
        "PERSIST_CONTINUATION_CHECKPOINT_WHEN_TRIGGERED",
        "SELECTIVE_RETEST_AFTER_RELEASE_CONDITION",
        "EMIT_SUCCESSOR_RECEIPT_ONLY_AFTER_MATERIAL_RETEST_EXECUTES",
    }:
        if token not in candidate_policy.get("exercise_sequence", []):
            fail(f"candidate professional-process exercise sequence missing {token}")
    for token in {
        "RELEASE_CONDITION",
        "CONTINUATION_CHECKPOINT_REF",
        "AFFECTED_CAPABILITY_OUTPUT_BINDINGS",
        "UNAFFECTED_VERIFIED_BINDINGS",
        "SELECTIVE_RETEST_PLAN",
        "EVALUATION_RECEIPT_REF",
    }:
        if token not in candidate_policy.get("problem_record_requires", []):
            fail(f"candidate professional-process problem record missing {token}")
    return current, owner_map


def validate_contract_headers() -> dict[str, dict]:
    data: dict[str, dict] = {}
    for name, path in CONTRACT_FILES.items():
        obj = load_json(path)
        if obj.get("contract_id") != EXPECTED_IDS[name]:
            fail(f"{path.name} contract_id mismatch")
        if obj.get("version") != "0.1":
            fail(f"{path.name} version must remain 0.1")
        if obj.get("status") != "ACTIVE_CURRENT":
            fail(f"{path.name} must be ACTIVE_CURRENT, got {obj.get('status')}")
        data[name] = obj
    return data


def local_capability_path(owner: dict) -> Path | None:
    state = owner.get("routing_state")
    skill_id = owner.get("skill_id")
    if state == "INSTALLED_OWNER":
        return ROOT / "oleander-skills" / skill_id / "CAPABILITY.json"
    if state == "CANDIDATE_OWNER":
        return ROOT / "skills" / skill_id / "CAPABILITY.json"
    return None


def validate_owner_consistency(capability: dict, resolver: dict, owner_map: dict) -> None:
    owners = capability.get("owners", [])
    required = set(capability.get("required_fields", []))
    installed_resolver_declared = set(resolver.get("capability_layers", {}).get("installed_reusable_execution_skills", []))
    candidate_resolver_declared = set(resolver.get("capability_layers", {}).get("candidate_ui_specialists_on_main", []))
    expected_owner_count = len(installed_resolver_declared) + len(candidate_resolver_declared) + 1
    if len(owners) != expected_owner_count:
        fail(f"capability declaration count must match installed + candidate owners + Technical Drawing body: expected {expected_owner_count}, got {len(owners)}")
    ids = [o.get("skill_id") for o in owners]
    if len(ids) != len(set(ids)):
        fail("duplicate skill_id in capability declarations")

    governed_fields = sorted(required)
    for owner in owners:
        context = f"capability:{owner.get('skill_id')}"
        require_fields(owner, required - {"implementation_paths"}, context)
        require_present_fields(owner, {"implementation_paths"}, context)
        routing_state = owner.get("routing_state")
        implementation_paths = owner.get("implementation_paths", [])

        if routing_state in {"INSTALLED_OWNER", "CANDIDATE_OWNER"}:
            if not implementation_paths:
                fail(f"{context} implemented owner must declare implementation_paths")
            for rel in implementation_paths:
                if not (ROOT / rel).exists():
                    fail(f"{context} missing implementation path {rel}")
            local_path = local_capability_path(owner)
            if not local_path or not local_path.is_file():
                fail(f"{context} missing local CAPABILITY.json")
            local = load_json(local_path)
            if local.get("schema") != "OLEANDER_SKILL_CAPABILITY_CONTRACT_v0.1":
                fail(f"{context} local CAPABILITY schema mismatch")
            for field in governed_fields:
                if local.get(field) != owner.get(field):
                    fail(f"{context} local/aggregate drift in field {field}")
        elif routing_state == "CANDIDATE_BODY":
            if owner.get("skill_id") != "OLEANDER Technical Drawing":
                fail(f"{context} unexpected central-only candidate body")
            if implementation_paths:
                fail("Technical Drawing CANDIDATE_BODY must not claim a main implementation path")
            if owner.get("implementation_state") != "NOT_ON_MAIN":
                fail("Technical Drawing must declare implementation_state=NOT_ON_MAIN")
            refs = owner.get("implementation_refs", [])
            if not any("PR #172" in ref for ref in refs):
                fail("Technical Drawing non-main implementation must reference Draft PR #172")
        else:
            fail(f"{context} unsupported owner routing state in current owner registry: {routing_state}")

    installed_review = installed_from_review()
    installed_cap = {o["skill_id"] for o in owners if o.get("lifecycle_state") == "INSTALLED" and o.get("routing_state") == "INSTALLED_OWNER"}
    installed_resolver = installed_resolver_declared
    installed_map = {k for k, v in owner_map.get("owners", {}).items() if v.get("state") == "INSTALLED"}
    if not (installed_review == installed_cap == installed_resolver == installed_map):
        fail(f"installed owner drift REVIEW={sorted(installed_review)} capability={sorted(installed_cap)} resolver={sorted(installed_resolver)} map={sorted(installed_map)}")

    candidates_cap = {o["skill_id"] for o in owners if o.get("routing_state") == "CANDIDATE_OWNER"}
    candidates_resolver = candidate_resolver_declared
    candidates_map = {k for k, v in owner_map.get("owners", {}).items() if v.get("state") == "CANDIDATE"}
    if not (candidates_cap == candidates_resolver == candidates_map):
        fail(f"candidate owner drift capability={sorted(candidates_cap)} resolver={sorted(candidates_resolver)} map={sorted(candidates_map)}")

    tech = next((o for o in owners if o.get("skill_id") == "OLEANDER Technical Drawing"), None)
    if not tech or tech.get("routing_state") != "CANDIDATE_BODY":
        fail("Technical Drawing must remain CANDIDATE_BODY")
    if owner_map.get("owners", {}).get("OLEANDER Technical Drawing", {}).get("state") != "CANDIDATE_BODY":
        fail("Owner Map Technical Drawing state drift")


def _professional_role_matches_rule(role: str, rule: dict) -> bool:
    match = rule.get("match") or {}
    if match.get("fallback") is True:
        return True
    if role in {str(x) for x in match.get("exact_any") or []}:
        return True
    if any(role.startswith(str(prefix)) for prefix in match.get("starts_with_any") or []):
        return True
    if any(str(token) in role for token in match.get("contains_any") or []):
        return True
    return False


def _professional_stage_exec_for(
    *,
    row: dict,
    process_ref: str,
    process: dict,
    stage: dict,
    owner_map: dict,
) -> tuple[dict, str]:
    direct = stage.get("stage_execution_requirements")
    if isinstance(direct, dict):
        if row.get("state") in {"FORMALIZED_PROJECT_EXERCISED", "FORMALIZED_MACHINE_BOUND"}:
            fail(
                f"{row.get('domain')}:{stage.get('stage_id')} mutates a Current professional machine in place "
                "with stage_execution_requirements"
            )
        return direct, "CANDIDATE_PROCESS_DEFINITION"

    if row.get("state") not in {"FORMALIZED_PROJECT_EXERCISED", "FORMALIZED_MACHINE_BOUND"}:
        fail(f"{row.get('domain')}:{stage.get('stage_id')} Candidate stage lacks stage_execution_requirements")

    projection_ref = owner_map.get("current_professional_stage_execution_projection_ref")
    if not projection_ref:
        fail("Execution Owner Map missing Current professional-stage execution projection ref")
    projection_path = ROOT / projection_ref
    if not projection_path.is_file():
        fail("Current professional-stage execution projection ref is unreadable")
    projection = load_json(projection_path)
    require_fields(
        projection,
        ["purpose", "semantic_class", "authority_rule", "migration_rule", "does_not_create", "processes"],
        "execution-owner-map:current-professional-stage-execution-projection",
    )
    if projection.get("semantic_class") != "NON_AUTHORITY_RUNTIME_COMPATIBILITY_PROJECTION":
        fail("Current professional stage execution projection must remain non-authority runtime compatibility only")
    entry = next(
        (
            item
            for item in projection.get("processes", [])
            if item.get("current_machine_ref") == process_ref
        ),
        None,
    )
    if not entry:
        fail(f"{row.get('domain')} Current professional machine lacks exact-revision execution projection")
    path = ROOT / process_ref
    actual_sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
    actual_blob = subprocess.check_output(["git", "hash-object", process_ref], cwd=ROOT, text=True).strip()
    if entry.get("current_machine_sha256") != actual_sha256:
        fail(f"{row.get('domain')} Current stage execution projection SHA256 is stale")
    if entry.get("current_machine_blob") != actual_blob:
        fail(f"{row.get('domain')} Current stage execution projection blob is stale")
    stage_exec = (entry.get("stages") or {}).get(stage.get("stage_id"))
    if not isinstance(stage_exec, dict):
        fail(f"{row.get('domain')}:{stage.get('stage_id')} missing exact-revision execution projection")
    return stage_exec, "CURRENT_EXACT_REVISION_RUNTIME_PROJECTION"


def validate_professional_stage_capability_routing(owner_map: dict, capability: dict) -> tuple[int, int, int]:
    routing = owner_map.get("professional_stage_capability_routing", {})
    require_fields(
        routing,
        [
            "purpose",
            "is_routing_extension_not_taxonomy",
            "resolution_inputs",
            "valid_resolution_classes",
            "ordered_first_match",
            "rules",
            "composition_rule",
            "single_owner_rule",
            "no_owner_rule",
            "recompute_rule",
            "candidate_owner_rule",
            "candidate_body_rule",
        ],
        "execution-owner-map:professional-stage-capability-routing",
    )
    if routing.get("is_routing_extension_not_taxonomy") is not True:
        fail("professional-stage capability routing must remain an owner-map extension, not a new taxonomy")
    if routing.get("ordered_first_match") is not True:
        fail("professional-stage capability routing must use deterministic ordered-first-match semantics")
    if "NOT_CURRENT_CALLABLE_EXECUTION_AUTHORITY" not in routing.get("candidate_owner_rule", ""):
        fail("Candidate Skill routing must explicitly remain non-Current execution authority")
    if "NOT_CURRENT_CALLABLE_EXECUTION_AUTHORITY" not in routing.get("candidate_body_rule", ""):
        fail("Candidate Body routing must explicitly remain non-Current execution authority")

    rules = routing.get("rules", [])
    rule_ids = [str(rule.get("rule_id") or "") for rule in rules]
    if len(rule_ids) != len(set(rule_ids)) or any(not rule_id for rule_id in rule_ids):
        fail("professional-stage capability routing rule ids must be unique and non-empty")
    required_rule_ids = {
        "PSC-INDEPENDENT-REVIEW",
        "PSC-PROFESSIONAL-SPECIALIST-GUARD",
        "PSC-TECHNICAL-DRAWING",
        "PSC-RESEARCH-EVIDENCE",
        "PSC-DATA-GIS",
        "PSC-3D-GEOMETRY",
        "PSC-DESIGN-PROCESS",
        "PSC-UNOWNED-PROFESSIONAL-CAPABILITY",
    }
    if not required_rule_ids.issubset(set(rule_ids)):
        fail("professional-stage capability routing is missing required semantic guards")
    fallback_rules = [rule for rule in rules if (rule.get("match") or {}).get("fallback") is True]
    if len(fallback_rules) != 1 or rules[-1] is not fallback_rules[0]:
        fail("professional-stage capability routing must have exactly one final fallback rule")
    if fallback_rules[0].get("resolution_class") != "PROJECT_OR_SPECIALIST_OWNER_REQUIRED":
        fail("professional-stage fallback must fail closed to project/specialist owner required")

    valid_classes = set(routing.get("valid_resolution_classes", []))
    owner_contracts = {str(owner.get("skill_id")): owner for owner in capability.get("owners", [])}
    for rule in rules:
        resolution_class = rule.get("resolution_class")
        if resolution_class not in valid_classes:
            fail(f"professional-stage rule {rule.get('rule_id')} uses undeclared resolution class {resolution_class}")
        for owner_id in rule.get("owner_refs", []):
            if owner_id not in owner_contracts:
                fail(f"professional-stage rule {rule.get('rule_id')} references unknown owner {owner_id}")
            routing_state = owner_contracts[owner_id].get("routing_state")
            if resolution_class == "EXISTING_OWNER" and routing_state != "INSTALLED_OWNER":
                fail(f"professional-stage existing-owner rule points to non-installed owner {owner_id}")
            if resolution_class == "CANDIDATE_OWNER" and routing_state != "CANDIDATE_OWNER":
                fail(f"professional-stage candidate-owner rule points to non-candidate owner {owner_id}")
            if resolution_class == "CANDIDATE_BODY_REQUIRES_CALLABILITY" and routing_state != "CANDIDATE_BODY":
                fail(f"professional-stage candidate-body rule points to wrong owner state {owner_id}")

    specialist_rule = next(rule for rule in rules if rule.get("rule_id") == "PSC-PROFESSIONAL-SPECIALIST-GUARD")
    design_rule = next(rule for rule in rules if rule.get("rule_id") == "PSC-DESIGN-PROCESS")
    if rules.index(specialist_rule) > rules.index(design_rule):
        fail("professional specialist guard must precede generic design-process routing")

    graph = load_json(CONTROL_GRAPH)
    stage_count = 0
    knowledge_bound_stage_count = 0
    unique_roles: set[str] = set()
    fallback_roles: set[str] = set()
    design_roles: set[str] = set()
    process_rows = graph.get("professional_domain_process_state", [])
    if not process_rows:
        fail("control graph has no professional-domain process state")
    for row in process_rows:
        ref = row.get("machine_schema_ref") or row.get("candidate_machine_schema_ref")
        if not ref:
            fail(f"professional domain {row.get('domain')} has no machine process ref for capability routing")
        process = load_json(ROOT / ref)
        if process.get("kind") != "PROFESSIONAL_DOMAIN_PROCESS_DEFINITION":
            fail(f"professional domain {row.get('domain')} machine ref is not a process definition: {ref}")
        for stage in process.get("stages", []):
            stage_count += 1
            if not stage.get("knowledge_inputs"):
                fail(f"{row.get('domain')}:{stage.get('stage_id')} has no declared knowledge_inputs")
            if not str(stage.get("knowledge_mount_requirement") or "").strip():
                fail(f"{row.get('domain')}:{stage.get('stage_id')} has no knowledge_mount_requirement")
            knowledge_bound_stage_count += 1
            stage_exec, _ = _professional_stage_exec_for(
                row=row,
                process_ref=ref,
                process=process,
                stage=stage,
                owner_map=owner_map,
            )
            roles = list(stage_exec.get("required_capability_roles", []))
            roles += list(stage_exec.get("supporting_capability_roles", []))
            if not roles:
                fail(f"{row.get('domain')}:{stage.get('stage_id')} has no stage capability roles")
            for role in roles:
                role = str(role)
                unique_roles.add(role)
                matched = next((rule for rule in rules if _professional_role_matches_rule(role, rule)), None)
                if matched is None:
                    fail(f"professional capability role has no owner-map classification: {role}")
                if matched.get("rule_id") == "PSC-UNOWNED-PROFESSIONAL-CAPABILITY":
                    fallback_roles.add(role)
                if matched.get("rule_id") == "PSC-DESIGN-PROCESS":
                    design_roles.add(role)

    if fallback_roles:
        fail(
            "professional capability roles may not rely on unnamed fallback; classify them explicitly: "
            + ", ".join(sorted(fallback_roles))
        )
    wrongly_generic = sorted(
        role for role in design_roles if _professional_role_matches_rule(role, specialist_rule)
    )
    if wrongly_generic:
        fail(
            "professional specialist roles were swallowed by generic design-process routing: "
            + ", ".join(wrongly_generic)
        )
    return stage_count, len(unique_roles), knowledge_bound_stage_count


def validate_dag(data: dict) -> None:
    if not data.get("minimum_sufficient_owner_set"):
        fail("DAG must enforce minimum_sufficient_owner_set")
    if data.get("default_handoff_permission") != "READ_ONLY":
        fail("DAG default handoff permission must be READ_ONLY")
    required_roles = {"PRIMARY_OWNER", "SUPPORTING_OWNER", "READ_ONLY_CONSUMER", "VALIDATOR", "INDEPENDENT_REVIEWER"}
    if not required_roles.issubset(set(data.get("node_roles", []))):
        fail("DAG node roles incomplete")
    required_dag_fields = set(data.get("required_dag_fields", []))
    for token in {"stage_or_decision_scope", "required_capability_roles", "capability_coverage", "reroute_triggers"}:
        if token not in required_dag_fields:
            fail(f"DAG required fields missing stage-composition field {token}")
    if "NOT_MINIMUM_SKILL_COUNT" not in data.get("minimum_sufficient_definition", ""):
        fail("DAG minimum_sufficient_definition must reject minimum-skill-count interpretation")
    for token in {
        "SUPPORTING_OWNER_IS_NOT_OPTIONAL_WHEN_ITS_CAPABILITY_IS_MATERIAL_TO_THE_CLAIM",
        "INDEPENDENT_REVIEWER_CANNOT_BE_COLLAPSED_INTO_PRODUCER_FOR_COUNT_MINIMIZATION",
        "SELECTIVE_REOPEN_REROUTES_ONLY_AFFECTED_CAPABILITY_OUTPUT_BINDINGS",
    }:
        if token not in data.get("composition_rules", []):
            fail(f"DAG composition rules missing {token}")
    if "minimum_sufficient_does_not_mean_minimum_skill_count" not in data.get("hard_guards", []):
        fail("DAG must reject minimum-skill-count interpretation")
    if "stage_specific_capability_composition_required_for_material_professional_work" not in data.get("hard_guards", []):
        fail("DAG must require stage-specific capability composition for material professional work")


def validate_tool(data: dict) -> None:
    if "final_project_artifact" not in data.get("shared_tool_must_not_own", []):
        fail("Tool Adapter must forbid final project artifact ownership")
    required = set(data.get("required_fields", []))
    adapters = data.get("current_adapters", [])
    image_ops = next((a for a in adapters if a.get("canonical_tool_id") == "T-VISUAL-IMAGE-OPS-001"), None)
    if not image_ops:
        fail("missing Current Image Ops adapter")
    require_fields(image_ops, required, "Image Ops adapter")
    consumers = image_ops.get("consumers", [])
    if len(consumers) != 11 or len(set(consumers)) != 11:
        fail("Image Ops adapter must have exactly 11 unique consumers")
    expected_paths = {
        "oleander-research": "oleander-skills/oleander-research/VISUAL_LAYER_BINDING.md",
        "oleander-data-viz": "oleander-skills/oleander-data-viz/VISUAL_LAYER_BINDING.md",
        "oleander-3d-pipeline": "oleander-skills/oleander-3d-pipeline/VISUAL_LAYER_BINDING.md",
        "oleander-story-and-board": "oleander-skills/oleander-story-and-board/VISUAL_LAYER_BINDING.md",
        "oleander-motion": "oleander-skills/oleander-motion/VISUAL_LAYER_BINDING.md",
        "oleander-delivery-qc": "oleander-skills/oleander-delivery-qc/VISUAL_LAYER_BINDING.md",
        "oleander-ui-visual-composition": "skills/oleander-ui-visual-composition/VISUAL_LAYER_BINDING.md",
        "oleander-ui-interaction": "skills/oleander-ui-interaction/VISUAL_LAYER_BINDING.md",
        "oleander-route-wayfinding-ui": "skills/oleander-route-wayfinding-ui/VISUAL_LAYER_BINDING.md",
        "oleander-game-ui": "skills/oleander-game-ui/VISUAL_LAYER_BINDING.md",
        "oleander-mobile-game-ui": "skills/oleander-mobile-game-ui/VISUAL_LAYER_BINDING.md",
    }
    for consumer in consumers:
        rel = expected_paths.get(consumer)
        if not rel or not (ROOT / rel).is_file():
            fail(f"missing Image Ops binding for {consumer}: {rel}")
    baseline = ROOT / image_ops["regression_baseline"]
    b = load_json(baseline)
    if b.get("baseline_id") != "RB-IMAGE-OPS-ADAPTER-SEED-v0.1":
        fail("Image Ops regression baseline id mismatch")
    for layer in ["STRUCTURAL", "SEMANTIC", "VISUAL_ROI", "RUNTIME"]:
        if layer not in b.get("layer_results", {}):
            fail(f"Image Ops baseline missing layer {layer}")


def validate_artifact(data: dict) -> None:
    vocab = data.get("provenance_vocabulary", [])
    if len(vocab) != len(set(vocab)):
        fail("duplicate provenance vocabulary")
    required_vocab = {"SOURCE_VISIBLE", "SOURCE_EXPLICIT", "REFERENCE_DERIVED_GEOMETRY", "INFERRED_FROM_MARK", "VISUAL_PROXY", "ASSUMED_FOR_PROTOTYPE", "UNREADABLE", "UNKNOWN", "FIELD_OPEN"}
    if not required_vocab.issubset(set(vocab)):
        fail("Native Artifact provenance vocabulary incomplete")
    if data.get("default_permission") != "READ_ONLY":
        fail("Native Artifact default permission must be READ_ONLY")

    source_integrity = data.get("source_integrity_extension", {})
    require_fields(
        source_integrity,
        [
            "prospective_only",
            "historical_artifacts_immutable",
            "required_when",
            "fields",
            "modes",
            "mode_semantics",
            "path_is_not_identity",
            "source_identity_requires",
            "declared_transform_boundary_required",
            "missing_or_unperformed_verification_must_not_equal_pass",
            "verification_result_carrier",
            "does_not_prove",
        ],
        "native-artifact:source-integrity-extension",
    )
    expected_modes = {"EVIDENCE_ONLY", "DETERMINISTIC_TRANSFORM", "NORMALIZED_RASTER_EXACT", "BYTE_EXACT"}
    if set(source_integrity.get("modes", [])) != expected_modes:
        fail("Native Artifact source integrity mode vocabulary drift")
    if set(source_integrity.get("mode_semantics", {})) != expected_modes:
        fail("Native Artifact source integrity semantics incomplete")
    if source_integrity.get("prospective_only") is not True or source_integrity.get("historical_artifacts_immutable") is not True:
        fail("Native Artifact source integrity extension must be prospective")
    if source_integrity.get("path_is_not_identity") is not True:
        fail("Native Artifact source integrity must reject path-only identity")
    if source_integrity.get("missing_or_unperformed_verification_must_not_equal_pass") is not True:
        fail("Native Artifact missing integrity verification may not equal PASS")

    delivery = data.get("delivery_eligibility_extension", {})
    require_fields(
        delivery,
        [
            "prospective_only",
            "historical_artifacts_immutable",
            "required_when",
            "fields",
            "states",
            "generative_output_default",
            "deterministic_or_native_output_may_still_require_gates",
            "intermediate_cannot_satisfy_final_native_output",
            "flattened_derivative_cannot_replace_editable_master_when_editability_is_required",
            "current_or_superseded_is_independent_from_delivery_eligibility",
            "delivery_eligibility_does_not_grant_promotion",
            "gate_rule",
        ],
        "native-artifact:delivery-eligibility-extension",
    )
    expected_delivery_states = {"INTERMEDIATE_ONLY", "CANDIDATE_ONLY", "ELIGIBLE_AFTER_REQUIRED_GATES", "DELIVERY_DERIVATIVE"}
    if set(delivery.get("states", [])) != expected_delivery_states:
        fail("Native Artifact delivery eligibility vocabulary drift")
    if delivery.get("generative_output_default") != "INTERMEDIATE_ONLY":
        fail("Generative artifact default must remain INTERMEDIATE_ONLY")
    if delivery.get("intermediate_cannot_satisfy_final_native_output") is not True:
        fail("Intermediate artifact may not satisfy final native output")
    if delivery.get("delivery_eligibility_does_not_grant_promotion") is not True:
        fail("Delivery eligibility may not grant promotion")

    dependency_identity = data.get("dependency_identity_extension", {})
    require_fields(
        dependency_identity,
        [
            "prospective_only",
            "historical_artifacts_immutable",
            "required_when",
            "fields",
            "requiredness_values",
            "fallback_policy_values",
            "silent_fallback_forbidden",
            "missing_required_dependency_blocks_delivery_eligibility",
            "declared_equivalent_requires_explicit_identity_and_readback",
            "nonfinal_preview_fallback_cannot_satisfy_final_native_output",
            "required_dependency_verification_result_carrier",
            "does_not_prove",
        ],
        "native-artifact:dependency-identity-extension",
    )
    expected_requiredness = {"REQUIRED_FOR_REPRODUCTION", "REQUIRED_FOR_SEMANTIC_FIDELITY", "OPTIONAL"}
    expected_fallback = {"FORBID", "ALLOW_DECLARED_EQUIVALENT", "ALLOW_NONFINAL_PREVIEW"}
    if set(dependency_identity.get("requiredness_values", [])) != expected_requiredness:
        fail("Native Artifact dependency requiredness vocabulary drift")
    if set(dependency_identity.get("fallback_policy_values", [])) != expected_fallback:
        fail("Native Artifact dependency fallback vocabulary drift")
    if dependency_identity.get("prospective_only") is not True or dependency_identity.get("historical_artifacts_immutable") is not True:
        fail("Native Artifact dependency identity extension must be prospective")
    if dependency_identity.get("silent_fallback_forbidden") is not True:
        fail("Native Artifact must forbid silent dependency fallback")
    if dependency_identity.get("missing_required_dependency_blocks_delivery_eligibility") is not True:
        fail("Missing required dependency must block delivery eligibility")
    if dependency_identity.get("declared_equivalent_requires_explicit_identity_and_readback") is not True:
        fail("Declared dependency equivalent must require identity + readback")
    if dependency_identity.get("nonfinal_preview_fallback_cannot_satisfy_final_native_output") is not True:
        fail("Nonfinal preview dependency fallback may not satisfy final native output")


def validate_regression(data: dict) -> None:
    if data.get("layers") != ["STRUCTURAL", "SEMANTIC", "VISUAL_ROI", "RUNTIME"]:
        fail("Regression layers must be STRUCTURAL, SEMANTIC, VISUAL_ROI, RUNTIME")
    if data.get("design_review_boundary") != "regression_pass_does_not_equal_design_keep":
        fail("Regression must preserve Design Review boundary")


def validate_drift(data: dict) -> None:
    required = set(data.get("required_fields", []))
    states = set(data.get("drift_states", []))
    expected_states = {"CURRENT", "STALE", "MISSING", "DIVERGED", "ORPHANED_IMPLEMENTATION", "NOT_REQUIRED", "UNKNOWN"}
    if not expected_states.issubset(states):
        fail("Drift Check state vocabulary incomplete")
    modes = data.get("modes", {})
    if "LIVE_CROSS_PLATFORM_CHECK" not in modes or "GITHUB_STATIC_CHECK" not in modes:
        fail("Drift Check must separate static/live modes")
    seeds = data.get("seed_mappings", [])
    if len(seeds) < 2:
        fail("Drift Check requires resolver and Image Ops seed mappings")
    for seed in seeds:
        require_fields(seed, required, f"drift:{seed.get('mapping_id')}")
        if seed.get("drift_state") == "CURRENT" and seed.get("notion_last_verified") in (None, ""):
            fail(f"drift:{seed.get('mapping_id')} CURRENT requires live Notion verification")


def validate_receipts() -> None:
    schema = load_json(RECEIPT_CONTRACT)
    if schema.get("status") != "ACTIVE_CURRENT" or schema.get("version") != "1.0":
        fail("Execution Receipt v1.0 must be ACTIVE_CURRENT")
    expected_stage_chain = [
        "PROFESSIONAL_STAGE",
        "PROFESSIONAL_QUESTION_OR_DECISION_OBJECT",
        "KNOWLEDGE_INPUTS",
        "OPERATIONAL_KNOWLEDGE_MOUNT",
        "REQUIRED_CAPABILITY_ROLES",
        "CURRENT_EXECUTION_OWNERS_OR_SKILLS",
        "NATIVE_OUTPUTS",
        "ACTUAL_READBACK",
        "INDEPENDENT_REVIEW",
        "STAGE_CLOSURE",
    ]
    if schema.get("professional_stage_canonical_execution_chain") != expected_stage_chain:
        fail("Execution Receipt professional-stage canonical execution chain drift")
    if "MUST_NOT_BE_USED_TO_REORDER" not in str(schema.get("professional_stage_flow_binding_rule") or ""):
        fail("Execution Receipt generic flow phases must remain subordinate to professional-stage spine")

    typed_validation = schema.get("typed_validation_extension", {})
    require_fields(
        typed_validation,
        [
            "prospective_only",
            "historical_receipts_immutable",
            "required_when",
            "fields",
            "result_values",
            "result_semantics",
            "only_pass_satisfies_required_check",
            "not_applicable_requires_reason",
            "not_run_or_unverified_cannot_be_normalized_to_pass",
            "missing_evidence_cannot_default_to_pass",
            "missing_source_integrity_comparison_result",
            "producer_self_check_does_not_equal_independent_review",
            "technical_pass_does_not_equal_design_keep",
            "process_pass_does_not_equal_promotion",
        ],
        "execution-receipt:typed-validation-extension",
    )
    expected_validation_results = {"PASS", "FAIL", "HOLD", "NOT_RUN", "UNVERIFIED", "NOT_APPLICABLE"}
    if set(schema.get("validation_result_values", [])) != expected_validation_results:
        fail("Execution Receipt validation result vocabulary drift")
    if set(typed_validation.get("result_values", [])) != expected_validation_results:
        fail("Execution Receipt typed validation result vocabulary drift")
    if set(typed_validation.get("result_semantics", {})) != expected_validation_results:
        fail("Execution Receipt typed validation semantics incomplete")
    if set(schema.get("phase_result_values", [])) != expected_validation_results:
        fail("Execution Receipt phase result vocabulary must preserve typed validation states")
    if set(schema.get("regression_layer_result_values", [])) != expected_validation_results:
        fail("Execution Receipt regression result vocabulary must preserve typed validation states")
    if typed_validation.get("only_pass_satisfies_required_check") is not True:
        fail("Execution Receipt required validation checks must require PASS")
    if typed_validation.get("not_run_or_unverified_cannot_be_normalized_to_pass") is not True:
        fail("NOT_RUN/UNVERIFIED may not normalize to PASS")
    if typed_validation.get("missing_evidence_cannot_default_to_pass") is not True:
        fail("Missing evidence may not default to PASS")
    if typed_validation.get("missing_source_integrity_comparison_result") != "UNVERIFIED":
        fail("Missing source-integrity comparison must be UNVERIFIED")
    if typed_validation.get("prospective_only") is not True or typed_validation.get("historical_receipts_immutable") is not True:
        fail("Typed validation extension must be prospective")

    exception_boundary = schema.get("required_check_exception_boundary_extension", {})
    require_fields(
        exception_boundary,
        [
            "prospective_only",
            "historical_receipts_immutable",
            "required_when",
            "fields",
            "exception_effect_values",
            "generic_waiver_state_forbidden",
            "exception_does_not_mutate_prior_validation_result",
            "fail_hold_not_run_unverified_cannot_be_waived_to_pass",
            "authorized_exception_requires_decision_rights_basis",
            "changed_criterion_or_claim_requires_fresh_validation",
            "not_applicable_requires_reason_and_authority_basis",
            "exception_cannot_grant_design_keep_professional_pass_or_promotion",
            "does_not_prove",
        ],
        "execution-receipt:required-check-exception-boundary",
    )
    expected_exception_effects = {"CRITERION_CHANGED", "CLAIM_BOUNDARY_NARROWED", "CHECK_DECLARED_NOT_APPLICABLE_BY_AUTHORITY"}
    if set(exception_boundary.get("exception_effect_values", [])) != expected_exception_effects:
        fail("Execution Receipt exception-effect vocabulary drift")
    for required_true in (
        "prospective_only",
        "historical_receipts_immutable",
        "generic_waiver_state_forbidden",
        "exception_does_not_mutate_prior_validation_result",
        "fail_hold_not_run_unverified_cannot_be_waived_to_pass",
        "authorized_exception_requires_decision_rights_basis",
        "changed_criterion_or_claim_requires_fresh_validation",
        "not_applicable_requires_reason_and_authority_basis",
        "exception_cannot_grant_design_keep_professional_pass_or_promotion",
    ):
        if exception_boundary.get(required_true) is not True:
            fail(f"Execution Receipt exception boundary missing {required_true}")
    forbidden_validation_tokens = {"WAIVED_PASS", "PASS_WITH_WAIVER", "PASS_BY_EXCEPTION"}
    if forbidden_validation_tokens & set(schema.get("validation_result_values", [])):
        fail("Execution Receipt may not add waiver-derived PASS states")

    receipts = sorted(RECEIPT_DIR.glob("*.json"))
    if len(receipts) < 2:
        fail("at least two real execution receipts are required")
    core = set(schema.get("required_core_fields", []))
    artifact_fields = set(schema.get("artifact_required_fields", []))
    review_fields = set(schema.get("review_required_fields", []))
    closure_fields = set(schema.get("closure_required_fields", []))
    handoff_ext = schema.get("runtime_layer_handoff_extension", {})
    require_fields(
        handoff_ext,
        [
            "required_when",
            "prospective_only",
            "historical_receipts_immutable",
            "contract_ref",
            "fields",
            "handoff_state_values",
            "producer_max_state",
            "consumer_accepts_after_required_readback",
            "accepted_does_not_prove_downstream_pass",
            "authority_or_source_change_marks_affected_handoff_stale",
            "hold_preserves_last_verified_upstream_state",
            "feedback_edge_not_dependency_handoff",
            "no_material_delta_no_new_receipt",
        ],
        "execution-receipt:runtime-layer-handoff-extension",
    )
    expected_handoff_fields = {
        "handoff_id", "from_layer", "to_layer", "project_or_scope_id", "decision_object_id",
        "authority_fingerprint", "source_revision", "object_refs", "claim_boundary", "open_blockers",
        "stale_if", "readback_refs", "handoff_state", "observed_at", "does_not_prove",
    }
    if set(handoff_ext.get("fields", [])) != expected_handoff_fields:
        fail("runtime-layer handoff extension fields drift")
    if set(handoff_ext.get("handoff_state_values", [])) != {"UNRESOLVED", "READY", "ACCEPTED", "HOLD", "STALE", "SUPERSEDED"}:
        fail("runtime-layer handoff state vocabulary drift")
    if handoff_ext.get("producer_max_state") != "READY" or handoff_ext.get("consumer_accepts_after_required_readback") is not True:
        fail("runtime-layer handoff producer/consumer acceptance boundary invalid")
    if handoff_ext.get("accepted_does_not_prove_downstream_pass") is not True:
        fail("runtime-layer handoff acceptance may not equal downstream PASS")
    if handoff_ext.get("feedback_edge_not_dependency_handoff") != "R-K_TO_R-B":
        fail("R-K to R-B must remain feedback, not dependency handoff")
    if handoff_ext.get("prospective_only") is not True or handoff_ext.get("historical_receipts_immutable") is not True:
        fail("runtime-layer handoff extension must be prospective and preserve historical receipts")
    contract_path = ROOT / handoff_ext.get("contract_ref", "")
    if not contract_path.is_file():
        fail("runtime-layer handoff contract ref missing")

    partial_commit = schema.get("partial_commit_reconciliation_extension", {})
    require_fields(
        partial_commit,
        [
            "required_when",
            "prospective_only",
            "historical_receipts_immutable",
            "contract_ref",
            "runtime_implementation_ref",
            "fields",
            "leg_fields",
            "leg_observation_values",
            "reconciliation_results",
            "result_is_ephemeral_runtime_fact_not_project_state",
            "uncertain_leg_action",
            "absent_safe_leg_action",
            "unsafe_missing_with_legal_compensation_action",
            "unsafe_unreconciled_action",
            "all_legs_confirmed_action",
            "dependent_handoff_ready_requires_coherent_commit",
            "dependent_handoff_acceptance_requires_coherent_commit",
            "dag_advance_requires_coherent_commit",
            "compensation_requires_existing_legal_authorized_path",
            "distributed_transaction_manager_forbidden",
            "persistent_transaction_ledger_forbidden",
            "no_material_delta_no_new_receipt",
        ],
        "execution-receipt:partial-commit-reconciliation-extension",
    )
    expected_partial_fields = {
        "project_or_scope_id", "task_id", "decision_object_id", "authority_fingerprint",
        "mutation_scope", "legs", "reconciliation_result", "reconciliation_action", "advance_allowed",
        "readback_refs", "observed_at", "does_not_prove",
    }
    if set(partial_commit.get("fields", [])) != expected_partial_fields:
        fail("partial-commit reconciliation receipt fields drift")
    expected_partial_leg_fields = {
        "surface_id", "side_effect_class", "operation_fingerprint", "expected_postcondition",
        "state", "retry_safe", "idempotent_or_provider_keyed", "compensation_legal", "readback_ref",
    }
    if set(partial_commit.get("leg_fields", [])) != expected_partial_leg_fields:
        fail("partial-commit reconciliation leg fields drift")
    if set(partial_commit.get("leg_observation_values", [])) != {"CONFIRMED", "ABSENT", "UNCERTAIN"}:
        fail("partial-commit reconciliation leg observation vocabulary drift")
    if set(partial_commit.get("reconciliation_results", [])) != {"COHERENT_COMMIT", "PARTIAL_COMMIT", "HOLD"}:
        fail("partial-commit reconciliation result vocabulary drift")
    expected_partial_actions = {
        "uncertain_leg_action": "VERIFY_UNCERTAIN_LEGS_BEFORE_ADVANCE",
        "absent_safe_leg_action": "RECONCILE_MISSING_LEGS_BEFORE_ADVANCE",
        "unsafe_missing_with_legal_compensation_action": "COMPENSATE_CONFIRMED_LEGS_BEFORE_ADVANCE",
        "unsafe_unreconciled_action": "HOLD_PARTIAL_COMMIT_UNRECONCILED",
        "all_legs_confirmed_action": "ADVANCE_AFTER_COHERENT_COMMIT",
    }
    for key, expected in expected_partial_actions.items():
        if partial_commit.get(key) != expected:
            fail(f"partial-commit reconciliation action drift: {key}")
    for required_true in {
        "prospective_only",
        "historical_receipts_immutable",
        "result_is_ephemeral_runtime_fact_not_project_state",
        "dependent_handoff_ready_requires_coherent_commit",
        "dependent_handoff_acceptance_requires_coherent_commit",
        "dag_advance_requires_coherent_commit",
        "compensation_requires_existing_legal_authorized_path",
        "distributed_transaction_manager_forbidden",
        "persistent_transaction_ledger_forbidden",
        "no_material_delta_no_new_receipt",
    }:
        if partial_commit.get(required_true) is not True:
            fail(f"partial-commit reconciliation boundary missing {required_true}")
    for pointer in ("contract_ref", "runtime_implementation_ref"):
        if not (ROOT / partial_commit[pointer]).is_file():
            fail(f"partial-commit reconciliation {pointer} missing")

    recovery_ext = schema.get("recovery_incident_extension", {})
    require_fields(
        recovery_ext,
        [
            "required_when",
            "prospective_only",
            "historical_receipts_immutable",
            "contract_ref",
            "fields",
            "required_fields",
            "conditional_fields",
            "incident_state_is_local_only",
            "closed_requires_actual_recovery_readback",
            "unaffected_verified_state_preserved",
            "reaccept_only_affected_handoffs_after_readback",
            "owner_refs_do_not_grant_authority",
            "consequential_resume_requires_resolvable_authorization_basis",
            "telemetry_only_event_no_new_receipt",
            "no_material_delta_no_new_receipt",
        ],
        "execution-receipt:recovery-incident-extension",
    )
    expected_recovery_fields = {
        "incident_id", "failure_class", "failure_code", "failure_owner_ref", "detected_at", "owning_layer",
        "project_or_scope_id", "current_task_id", "decision_object_id", "authority_fingerprint", "source_revision",
        "trigger_source_ref", "trigger_event_ref", "blast_radius", "preserved_state", "containment", "recovery", "closure",
        "incident_state", "remaining_blockers", "next_allowed_action", "observed_at", "does_not_prove",
    }
    if set(recovery_ext.get("fields", [])) != expected_recovery_fields:
        fail("recovery-incident extension fields drift")
    expected_recovery_required_fields = expected_recovery_fields - {"failure_code", "trigger_event_ref"}
    if set(recovery_ext.get("required_fields", [])) != expected_recovery_required_fields:
        fail("recovery-incident required fields drift")
    if set(recovery_ext.get("conditional_fields", {})) != {"failure_code", "trigger_event_ref"}:
        fail("recovery-incident conditional fields drift")
    if recovery_ext.get("prospective_only") is not True or recovery_ext.get("historical_receipts_immutable") is not True:
        fail("recovery-incident extension must be prospective and preserve historical receipts")
    if recovery_ext.get("incident_state_is_local_only") is not True:
        fail("recovery incident state must remain incident-local")
    if recovery_ext.get("closed_requires_actual_recovery_readback") is not True:
        fail("recovery incident closure must require actual readback")
    if recovery_ext.get("unaffected_verified_state_preserved") is not True:
        fail("recovery incident must preserve unaffected verified state")
    if recovery_ext.get("reaccept_only_affected_handoffs_after_readback") is not True:
        fail("recovery may only reaccept affected handoffs after readback")
    if recovery_ext.get("owner_refs_do_not_grant_authority") is not True:
        fail("recovery incident owner refs may not grant authority")
    if recovery_ext.get("consequential_resume_requires_resolvable_authorization_basis") is not True:
        fail("recovery incident consequential resume requires current authorization basis")
    if recovery_ext.get("telemetry_only_event_no_new_receipt") is not True or recovery_ext.get("no_material_delta_no_new_receipt") is not True:
        fail("telemetry/no-delta recovery observations may not create a new receipt")
    recovery_contract_path = ROOT / recovery_ext.get("contract_ref", "")
    if not recovery_contract_path.is_file():
        fail("recovery-incident contract ref missing")

    branch_ref = schema.get("branch_ref_disposition_extension", {})
    require_fields(
        branch_ref,
        [
            "required_when",
            "prospective_only",
            "historical_receipts_immutable",
            "fields",
            "disposition_values",
            "dependency_checks",
            "merged_default",
            "unmerged_age_only_delete_forbidden",
            "bulk_cleanup_requires_ref_sha_audit",
            "branch_ref_is_not_current_authority",
        ],
        "execution-receipt:branch-ref-disposition-extension",
    )
    if branch_ref.get("prospective_only") is not True or branch_ref.get("historical_receipts_immutable") is not True:
        fail("branch-ref disposition extension must remain prospective and preserve historical receipts")
    if branch_ref.get("unmerged_age_only_delete_forbidden") is not True:
        fail("branch-ref disposition must forbid age-only deletion of unmerged refs")
    if branch_ref.get("bulk_cleanup_requires_ref_sha_audit") is not True:
        fail("branch-ref bulk cleanup must preserve ref->SHA audit evidence")
    if branch_ref.get("branch_ref_is_not_current_authority") is not True:
        fail("branch refs must not become Current authority")
    required_branch_dependencies = {"OPEN_PR_HEAD", "OPEN_PR_BASE", "ACTIVE_WORKTREE", "EXPLICIT_KEEP"}
    if not required_branch_dependencies.issubset(set(branch_ref.get("dependency_checks", []))):
        fail("branch-ref disposition dependency checks are incomplete")
    for path in receipts:
        r = load_json(path)
        require_fields(r, core, f"receipt:{path.name}")
        require_fields(r.get("authority", {}), schema.get("authority_required_fields", []), f"receipt:{path.name}:authority")
        require_present_fields(r.get("required_native_output", {}), schema.get("required_native_output_fields", []), f"receipt:{path.name}:native-output")
        require_fields(r.get("owner_set", {}), schema.get("owner_set_required_fields", []), f"receipt:{path.name}:owner-set")
        for art in r.get("artifacts", []):
            require_fields(art, artifact_fields, f"receipt:{path.name}:artifact:{art.get('artifact_id')}")
        reg = r.get("regression", {})
        for layer in schema.get("regression_layers", []):
            if layer not in reg or reg[layer].get("result") not in schema.get("regression_layer_result_values", []):
                fail(f"receipt:{path.name} invalid regression layer {layer}")
        review = r.get("review", {})
        require_fields(review, review_fields, f"receipt:{path.name}:review")
        if review.get("reviewer_independence_state") == "INDEPENDENT" and review.get("producer_id") == review.get("reviewer_id"):
            fail(f"receipt:{path.name} independent reviewer cannot equal producer")
        require_fields(r.get("closure", {}), closure_fields, f"receipt:{path.name}:closure")
        if "recovery_incident" in r:
            incident = r["recovery_incident"]
            require_present_fields(incident, expected_recovery_required_fields, f"receipt:{path.name}:recovery-incident")
            for field in {"failure_code", "trigger_event_ref"}:
                if field in incident and incident[field] in (None, ""):
                    fail(f"receipt:{path.name}:recovery-incident conditional field {field} may not be empty when present")


def validate_lifecycle_baseline(capability: dict) -> None:
    b = load_json(LIFECYCLE_BASELINE)
    installed = {r["skill_id"] for r in b.get("installed_pre_contract_baseline", [])}
    candidates = {r["skill_id"] for r in b.get("candidate_baseline", [])}
    required_transition_fields = set(b.get("future_transition_required_fields", [])) | {"skill_id"}
    valid_lifecycle_states = set(capability.get("lifecycle_states", []))

    for path in sorted(LIFECYCLE_DIR.glob("PROMOTION_*.json")):
        transition = load_json(path)
        if transition.get("status") not in {"ACTIVE_TRANSITION", "APPLIED"}:
            continue
        require_fields(transition, required_transition_fields, f"lifecycle:{path.name}")
        skill_id = transition["skill_id"]
        from_state = transition["from_state"]
        to_state = transition["to_state"]
        if from_state not in valid_lifecycle_states or to_state not in valid_lifecycle_states:
            fail(f"lifecycle:{path.name} uses unsupported lifecycle state {from_state}->{to_state}")

        current_state = "INSTALLED" if skill_id in installed else "CANDIDATE" if skill_id in candidates else None
        if current_state is not None and current_state != from_state:
            fail(f"lifecycle:{path.name} from_state mismatch: expected {current_state}, got {from_state}")
        if current_state is None and from_state != "CANDIDATE":
            fail(f"lifecycle:{path.name} source skill is not baseline-tracked and must enter from CANDIDATE, got {from_state}")

        installed.discard(skill_id)
        candidates.discard(skill_id)
        if to_state == "INSTALLED":
            installed.add(skill_id)
        elif to_state == "CANDIDATE":
            candidates.add(skill_id)
        else:
            fail(f"lifecycle:{path.name} transition target {to_state} is not represented by the current capability aggregate")

    cap_installed = {o["skill_id"] for o in capability.get("owners", []) if o.get("lifecycle_state") == "INSTALLED"}
    cap_noninstalled = {o["skill_id"] for o in capability.get("owners", []) if o.get("lifecycle_state") == "CANDIDATE"}
    if installed != cap_installed:
        fail(f"lifecycle baseline + promotions installed set does not match capability contract: lifecycle={sorted(installed)} capability={sorted(cap_installed)}")
    if candidates != cap_noninstalled:
        fail(f"lifecycle baseline + promotions candidate set does not match capability contract: lifecycle={sorted(candidates)} capability={sorted(cap_noninstalled)}")


def validate_golden_coverage(installed_skills: set[str], candidate_skills: set[str]) -> None:
    rows = load_jsonl(GOLDEN_SKILLS)
    counts = Counter(r.get("skill") for r in rows)
    missing = {s: counts[s] for s in installed_skills if counts[s] < 2}
    if missing:
        fail(f"installed Skill Golden Case coverage <2: {missing}")
    if counts["oleander-motion"] < 2:
        fail("oleander-motion must have at least two Golden Cases")

    candidate_rows = load_jsonl(UI_CANDIDATE_GOLDEN)
    ccounts: Counter[str] = Counter()
    for row in candidate_rows:
        require_fields(row, ["case_id", "candidate_skills", "task", "required_outputs", "blockers", "pass_rule"], f"candidate-golden:{row.get('case_id')}")
        for skill in row.get("candidate_skills", []):
            ccounts[skill] += 1
    under = {s: ccounts[s] for s in candidate_skills if ccounts[s] < 2}
    if under:
        fail(f"candidate Skill machine Golden coverage <2: {under}")


def validate_game_router() -> None:
    text = GAME_STACK.read_text(encoding="utf-8")
    for token in ["MINIMUM SUFFICIENT OWNER SET", "Do **not** automatically run", "default = `READ_ONLY`"]:
        if token not in text:
            fail(f"Game UI router missing Current DAG rule: {token}")


def main() -> None:
    resolver, owner_map = validate_current_resolver_and_pointers()
    contracts = validate_contract_headers()
    validate_owner_consistency(contracts["capability"], resolver, owner_map)
    professional_stage_count, professional_role_count, knowledge_bound_stage_count = validate_professional_stage_capability_routing(
        owner_map, contracts["capability"]
    )
    validate_dag(contracts["dag"])
    validate_tool(contracts["tool"])
    validate_artifact(contracts["artifact"])
    validate_regression(contracts["regression"])
    validate_drift(contracts["drift"])
    validate_receipts()
    validate_lifecycle_baseline(contracts["capability"])

    installed = installed_from_review()
    candidates = set(resolver.get("capability_layers", {}).get("candidate_ui_specialists_on_main", []))
    validate_golden_coverage(installed, candidates)
    validate_game_router()

    print("execution-contract validation: PASS")
    print(f"installed owners consistent: {len(installed)}")
    print(f"candidate UI owners consistent: {len(candidates)}")
    print(f"lifecycle promotion records applied: {len(list(LIFECYCLE_DIR.glob('PROMOTION_*.json')))}")
    print(f"real execution receipts: {len(list(RECEIPT_DIR.glob('*.json')))}")
    print(f"professional stage capability routing: {professional_stage_count} stages / {professional_role_count} unique roles / unnamed fallback=0")
    print(f"professional stage knowledge binding: {knowledge_bound_stage_count}/{professional_stage_count} stages declare knowledge inputs + mount requirement")
    print("resolver v1.2 / owner map / local+aggregate capability / adapter / artifact / regression / drift / eval coverage: CONSISTENT")


if __name__ == "__main__":
    main()
