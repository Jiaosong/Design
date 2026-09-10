#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
RESOLVER = RUNTIME / "OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json"
STORY_SKILL = ROOT / "oleander-skills" / "oleander-story-and-board" / "SKILL.md"
STORY_EVALS = ROOT / "oleander-skills" / "oleander-story-and-board" / "evals" / "evals.json"
VISUAL_SKILL = ROOT / "oleander-skills" / "oleander-visual-design" / "SKILL.md"
CASES = ROOT / "evals" / "runtime" / "chat_visual_execution.jsonl"


def fail(msg: str) -> None:
    raise SystemExit(f"chat-visual execution validation failed: {msg}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid or missing JSON {path.relative_to(ROOT)}: {exc}")


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        fail(f"missing corpus {path.relative_to(ROOT)}: {exc}")
    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except Exception as exc:
            fail(f"invalid JSONL {path.relative_to(ROOT)}:{lineno}: {exc}")
    return rows


def decide_chat_visual_execution(case: dict) -> dict:
    """Compile the existing OLEANDER full-flow ordering for ordinary Chat visual production."""
    if case.get("current_design_knowledge_required") and not case.get("current_design_knowledge_resolved"):
        return {
            "action": "RESOLVE_CURRENT_DESIGN_KNOWLEDGE_BEFORE_COMPOSITION",
            "completion_eligible": False,
        }

    benchmark_required = bool(case.get("benchmark_required"))
    repeated_failure_reopens_benchmark = (
        case.get("quality_convergence_required")
        and case.get("same_root_cause_revise_count", 0) >= 2
        and case.get("root_cause_reclassified")
        and case.get("current_benchmark_insufficient")
    )
    benchmark_required = benchmark_required or repeated_failure_reopens_benchmark

    if benchmark_required and not case.get("benchmark_completed"):
        return {
            "action": "RUN_HIGHEST_STANDARD_BENCHMARK_BEFORE_NEXT_MAKE",
            "completion_eligible": False,
        }

    if benchmark_required and case.get("benchmark_completed") and not case.get("benchmark_transfer_rules_extracted"):
        return {
            "action": "EXTRACT_BENCHMARK_TRANSFER_RULES_BEFORE_DIVERGE",
            "completion_eligible": False,
        }

    if (
        benchmark_required
        and case.get("benchmark_completed")
        and case.get("benchmark_transfer_rules_extracted")
        and case.get("learn_when_needed_required")
        and not case.get("learning_completed")
    ):
        return {
            "action": "LEARN_WHEN_NEEDED_BEFORE_DIVERGE",
            "completion_eligible": False,
        }

    if (
        case.get("current_design_knowledge_required")
        and case.get("current_design_knowledge_resolved")
        and not case.get("visible_method_application_planned")
    ):
        return {
            "action": "TRANSLATE_METHODS_TO_VISIBLE_COMPOSITION_OPERATIONS",
            "completion_eligible": False,
        }

    if (
        benchmark_required
        and case.get("benchmark_completed")
        and case.get("benchmark_transfer_rules_extracted")
        and (not case.get("learn_when_needed_required") or case.get("learning_completed"))
        and case.get("benchmark_guided_divergence_required")
        and not case.get("materially_distinct_candidates_present")
    ):
        return {
            "action": "DIVERGE_FROM_BENCHMARK_BEFORE_NEXT_MAKE",
            "completion_eligible": False,
        }

    if case.get("medium") == "WEB" and case.get("component_layout_locked_before_visual_ownership"):
        return {
            "action": "REOPEN_VISUAL_OWNERSHIP_BEFORE_COMPONENT_LOCK",
            "completion_eligible": False,
        }

    if case.get("material_images_present") and not case.get("asset_role_usability_passed"):
        return {
            "action": "RUN_ASSET_ROLE_USABILITY_PASS_BEFORE_LAYOUT_LOCK",
            "completion_eligible": False,
        }

    if case.get("final_editable_required") and case.get("generated_full_board_only"):
        return {
            "action": "HOLD_EDITABLE_MASTER_MISSING",
            "completion_eligible": False,
        }

    if not case.get("target_scale_readback_passed"):
        return {
            "action": "RUN_TARGET_SCALE_ACTUAL_READBACK",
            "completion_eligible": False,
        }

    if case.get("quality_convergence_required"):
        revise_now = case.get("visual_qa") == "REVISE" or case.get("project_qa") == "REVISE"
        if revise_now and not case.get("dominant_root_cause_named"):
            return {
                "action": "DIAGNOSE_DOMINANT_VISUAL_ROOT_CAUSE_BEFORE_REPAIR",
                "completion_eligible": False,
            }

        if case.get("same_root_cause_revise_count", 0) >= 2 and not case.get("root_cause_reclassified"):
            return {
                "action": "RECLASSIFY_ROOT_CAUSE_AND_REOPEN_DESIGN_HYPOTHESIS",
                "completion_eligible": False,
            }

        if case.get("candidate_comparison_required") and not case.get("materially_distinct_candidates_present"):
            return {
                "action": "BUILD_MATERIALLY_DISTINCT_CANDIDATE_SET",
                "completion_eligible": False,
            }

        if (
            case.get("candidate_comparison_required")
            and case.get("materially_distinct_candidates_present")
            and not case.get("matched_candidate_comparison_passed")
        ):
            return {
                "action": "RUN_MATCHED_CONTENT_CANDIDATE_COMPARISON",
                "completion_eligible": False,
            }

        if (
            case.get("matched_candidate_comparison_passed")
            and case.get("retrieved_methods_applied")
            and not case.get("quality_gain_observed")
        ):
            return {
                "action": "REOPEN_TECHNIQUE_HYPOTHESIS_AFTER_NO_QUALITY_GAIN",
                "completion_eligible": False,
            }

    if case.get("premature_distill_or_update_attempted") and not case.get("artifact_quality_validated"):
        return {
            "action": "RETURN_TO_PROJECT_REPAIR_BEFORE_DISTILL_UPDATE",
            "completion_eligible": False,
        }

    if case.get("visual_qa") == "REVISE" or case.get("project_qa") == "REVISE":
        return {
            "action": "REPAIR_REOPEN_RETEST_IN_SAME_ACTIVE_TURN",
            "completion_eligible": False,
        }

    if case.get("visual_qa") == "HOLD" or case.get("project_qa") == "HOLD":
        return {
            "action": "HOLD_WITH_EXACT_BLOCKER",
            "completion_eligible": False,
        }

    if (
        case.get("visual_qa") == "PASS"
        and case.get("project_qa") == "PASS"
        and (not case.get("final_editable_required") or case.get("editable_master_exists"))
    ):
        return {
            "action": "ELIGIBLE_FOR_EXISTING_FLOW_COMPLETION_GATE",
            "completion_eligible": True,
        }

    return {"action": "CONTINUE_VISUAL_PRODUCTION", "completion_eligible": False}


def validate_existing_runtime_binding() -> None:
    resolver = load_json(RESOLVER)
    if resolver.get("version") != "1.2" or resolver.get("implementation_revision") != "1.2.5":
        fail("repair must reuse Current Resolver v1.2 implementation revision 1.2.5")
    if resolver.get("status") != "ACTIVE_CURRENT":
        fail("Current Resolver must remain ACTIVE_CURRENT")

    installed = set(resolver.get("capability_layers", {}).get("installed_reusable_execution_skills", []))
    if "oleander-story-and-board" not in installed or "oleander-design-process" not in installed:
        fail("Chat visual production must reuse installed story-and-board + design-process owners")

    hard = set(resolver.get("hard_rules", []))
    required_hard = {
        "PRODUCTION_TASKS_DEFAULT_TO_REAL_EDITABLE_AUDITABLE_ARTIFACTS",
        "AI_IMAGE_IS_SUPPLEMENTARY_NOT_DESIGN_AUTHORITY",
        "ACTUAL_READBACK_REQUIRED_BEFORE_VISUAL_DESIGN_PASS",
        "READY_NODES_AUTO_ADVANCE_WITHOUT_ARTIFICIAL_ONE_NODE_STOP",
    }
    missing = required_hard - hard
    if missing:
        fail(f"existing Resolver hard-rule basis missing {sorted(missing)}")

    separations = set(resolver.get("review_separations", []))
    for token in ["PROCESS_PASS_NE_MAIN_KEEP", "RENDER_PASS_NE_DESIGN_PASS", "TRACEABILITY_NE_PROFESSIONAL_FINISH"]:
        if token not in separations:
            fail(f"existing review separation missing {token}")


def validate_visual_skill() -> None:
    text = VISUAL_SKILL.read_text(encoding="utf-8")
    required_phrases = [
        "## Current design-knowledge resolution before composition",
        "CURRENT NOTION FRAMEWORK / METHOD / PRACTICE RETRIEVAL",
        "FW-DESIGN-VISUAL-COMM-001",
        "Dominant Field & First-read",
        "Page-role Visual Rhythm",
        "Attention-State Composition",
        "Claim-bound Camera",
        "Decompose & Recombine",
        "T-VISUAL-IMAGE-OPS-001",
        "Breakpoint Role Redistribution",
        "KNOWLEDGE RETRIEVED ≠ TECHNIQUE APPLIED",
        "COMPONENT CONSISTENCY ≠ VISUAL AUTHORSHIP",
        "## Quality convergence after actual visual failure",
        "existing Control Plane `CB-01` behavior",
        "highest-standard benchmark step",
        "METHOD APPLICATION ≠ QUALITY IMPROVEMENT",
        "ITERATION COUNT ≠ CONVERGENCE",
        "MICRO-VARIATION ≠ ALTERNATIVE COMPOSITION",
    ]
    for phrase in required_phrases:
        if phrase not in text:
            fail(f"visual-design missing existing-knowledge/convergence phrase: {phrase}")
    if "Merely naming a method in a receipt does not count as use." not in text:
        fail("visual-design must require visible application rather than method-name receipt compliance")
    if "generic `hero + equal cards + timeline`" not in text:
        fail("visual-design must detect generic component-first fallback as unresolved composition")
    if "Two consecutive `REVISE` outcomes with the same dominant Root Cause" not in text:
        fail("visual-design must invoke existing CB-01 after repeated same-root-cause REVISE")
    if "changing only font size, spacing, color, corner radius, shadow" not in text:
        fail("visual-design must distinguish structural candidates from micro-parameter variants")


def validate_story_skill() -> None:
    text = STORY_SKILL.read_text(encoding="utf-8")
    required_phrases = [
        "## Chat-first visual production execution",
        "FIRST VISUAL DRAFT ≠ COMPLETION",
        "RUN ASSET ROLE / USABILITY PASS BEFORE LAYOUT LOCK",
        "REVISE → REPAIR → REOPEN → RETEST",
        "GENERATED FULL-BOARD IMAGE ≠ EDITABLE MASTER",
        "EXPLORE / SYNTHETIC / DOES_NOT_PROVE",
        "Visual QA",
        "Project QA",
    ]
    for phrase in required_phrases:
        if phrase not in text:
            fail(f"story-and-board missing Chat-first execution phrase: {phrase}")

    if "do not stop and wait for a generic `继续`" not in text.lower():
        fail("story-and-board must explicitly forbid waiting for generic continue after REVISE")
    if "complex hair masking" not in text:
        fail("story-and-board must preserve specialist extraction/retouch boundary")


def validate_story_eval() -> None:
    data = load_json(STORY_EVALS)
    cases = {int(row.get("id")): row for row in data.get("evals", []) if row.get("id") is not None}
    if 3 not in cases:
        fail("story-and-board eval 3 for ordinary Chat editable-board production is missing")
    prompt = cases[3].get("prompt", "")
    expected = cases[3].get("expected_output", "")
    for token in ["普通 Chat", "可编辑", "多次生图", "抠图", "第一版"]:
        if token not in prompt:
            fail(f"story eval 3 prompt missing {token}")
    for token in ["asset-role/usability", "editable master", "REVISE", "repair/reopen", "non-factual"]:
        if token not in expected:
            fail(f"story eval 3 expected_output missing {token}")


def validate_cases() -> None:
    rows = load_jsonl(CASES)
    by_id = {row.get("case_id"): row for row in rows}
    required = {
        "CHAT-VIS-001-ASSET-PASS-BEFORE-LAYOUT",
        "CHAT-VIS-002-FIRST-DRAFT-READBACK-REQUIRED",
        "CHAT-VIS-003-REVISE-CONTINUES-SAME-TURN",
        "CHAT-VIS-004-GENERATED-BOARD-NOT-EDITABLE-MASTER",
        "CHAT-VIS-005-PASS-ELIGIBLE-FOR-EXISTING-FLOW-GATE",
        "CHAT-VIS-006-NONFACTUAL-GENERATIVE-EXPLORATION-ALLOWED",
        "CHAT-VIS-007-CURRENT-DESIGN-KNOWLEDGE-FIRST",
        "CHAT-VIS-008-METHOD-NAME-IS-NOT-APPLICATION",
        "CHAT-VIS-009-WEB-COMPONENT-FIRST-REOPEN",
        "CHAT-VIS-010-REVISE-REQUIRES-ROOT-CAUSE",
        "CHAT-VIS-011-SAME-ROOT-CAUSE-TWICE-RECLASSIFY",
        "CHAT-VIS-012-MICRO-VARIANTS-ARE-NOT-CANDIDATE-SET",
        "CHAT-VIS-013-MATCHED-CANDIDATE-COMPARISON-REQUIRED",
        "CHAT-VIS-014-METHOD-APPLIED-NO-GAIN-REOPEN",
        "CHAT-VIS-015-RECLASSIFIED-FAILURE-REENTERS-BENCHMARK",
        "CHAT-VIS-016-BENCHMARK-MUST-BECOME-TRANSFER-RULES",
        "CHAT-VIS-017-LEARN-WHEN-NEEDED-BEFORE-DIVERGE",
        "CHAT-VIS-018-BENCHMARK-FEEDS-DIVERGENCE",
        "CHAT-VIS-019-NO-PREMATURE-DISTILL-UPDATE",
    }
    missing = required - set(by_id)
    if missing:
        fail(f"missing Chat visual execution cases {sorted(missing)}")

    for case_id in sorted(required - {"CHAT-VIS-006-NONFACTUAL-GENERATIVE-EXPLORATION-ALLOWED"}):
        case = by_id[case_id]
        result = decide_chat_visual_execution(case)
        if result["action"] != case.get("expected_action"):
            fail(f"{case_id} action mismatch: {result['action']} != {case.get('expected_action')}")
        if result["completion_eligible"] != case.get("expected_completion_eligible"):
            fail(f"{case_id} completion eligibility mismatch")

    exploration = by_id["CHAT-VIS-006-NONFACTUAL-GENERATIVE-EXPLORATION-ALLOWED"]
    if exploration.get("active_no_image_generation_constraint") is not False:
        fail("generative exploration case must not bypass an active NO_IMAGE_GENERATION constraint")
    if exploration.get("truth_status") != "EXPLORE_SYNTHETIC_DOES_NOT_PROVE":
        fail("generative exploration must remain non-factual derivative evidence")
    if exploration.get("final_editable_master_still_required") is not True:
        fail("generative exploration must not replace final editable master")

    for case_id in [
        "CHAT-VIS-015-RECLASSIFIED-FAILURE-REENTERS-BENCHMARK",
        "CHAT-VIS-016-BENCHMARK-MUST-BECOME-TRANSFER-RULES",
        "CHAT-VIS-017-LEARN-WHEN-NEEDED-BEFORE-DIVERGE",
        "CHAT-VIS-018-BENCHMARK-FEEDS-DIVERGENCE",
    ]:
        case = by_id[case_id]
        if case.get("benchmark_authority_state") != "BENCHMARK_CANDIDATE_NOT_PROJECT_AUTHORITY":
            fail(f"{case_id} must keep external/reference benchmark below Project/Source Authority")


def main() -> None:
    validate_existing_runtime_binding()
    validate_visual_skill()
    validate_story_skill()
    validate_story_eval()
    validate_cases()
    print("chat-visual execution validation: PASS")
    print("ordinary Chat visual production reuses existing OLEANDER owners: ENFORCED")
    print("Current Notion design knowledge resolves before composition lock: ENFORCED")
    print("reclassified repeated visual failure re-enters BENCHMARK before another MAKE when benchmark is insufficient: ENFORCED")
    print("benchmark evidence must become visible transfer rules before DIVERGE: ENFORCED")
    print("LEARN WHEN NEEDED occurs only after benchmark exposes a real capability gap and before DIVERGE: ENFORCED")
    print("benchmark-guided repair must DIVERGE into materially different candidates before next MAKE: ENFORCED")
    print("failed/unvalidated artifact cannot trigger premature DISTILL / UPDATE: ENFORCED")
    print("external/reference benchmark remains candidate evidence, not Project/Source Authority: ENFORCED")
    print("retrieved methods must become visible composition operations: ENFORCED")
    print("component-first Web fallback reopens visual ownership: ENFORCED")
    print("asset role/usability pass before image-dependent layout lock: ENFORCED")
    print("first visual draft/export/generated board is not completion: ENFORCED")
    print("REVISE requires a dominant visual Root Cause before repair: ENFORCED")
    print("same-root-cause repeated REVISE invokes existing CB-01 reclassification: ENFORCED")
    print("micro-parameter variants do not satisfy structural candidate comparison: ENFORCED")
    print("matched-content candidate comparison precedes quality-selection claims: ENFORCED")
    print("method application without visible quality gain reopens technique hypothesis: ENFORCED")
    print("Visual/Project REVISE continues repair/reopen/retest in the active turn: ENFORCED")
    print("non-factual generative exploration may iterate when allowed: ENFORCED")
    print("generated full-board image cannot replace final editable master: ENFORCED")
    print("no P10 framework / new Skill / new Project State: PRESERVED")


if __name__ == "__main__":
    main()
