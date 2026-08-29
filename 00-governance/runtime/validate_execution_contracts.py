#!/usr/bin/env python3
from __future__ import annotations

import json
import re
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
    required_order = [
        "DEFINE_REQUIRED_NATIVE_OUTPUT",
        "RESOLVE_EXECUTION_OWNER_MAP",
        "LOAD_SKILL_CAPABILITY_CONTRACT",
        "SELECT_MINIMUM_SUFFICIENT_EXECUTION_OWNER_SET",
        "RESOLVE_TOOL_ADAPTERS_WHEN_REQUIRED",
        "EXECUTE_ACTUAL_NATIVE_ARTIFACT",
        "EMIT_NATIVE_ARTIFACT_RECORDS_AND_TYPED_HANDOFFS",
        "RUN_STRUCTURAL_SEMANTIC_VISUAL_ROI_RUNTIME_REGRESSION_AS_APPLICABLE",
        "ACTUAL_READBACK",
        "EVIDENCE_GATE",
        "INDEPENDENT_DESIGN_QUALITY_GATE",
        "EMIT_EXECUTION_RECEIPT",
    ]
    positions = []
    for token in required_order:
        if token not in order:
            fail(f"resolver v1.2 missing execution-order token {token}")
        positions.append(order.index(token))
    if positions != sorted(positions):
        fail("resolver v1.2 execution-contract order is inconsistent")
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


def validate_dag(data: dict) -> None:
    if not data.get("minimum_sufficient_owner_set"):
        fail("DAG must enforce minimum_sufficient_owner_set")
    if data.get("default_handoff_permission") != "READ_ONLY":
        fail("DAG default handoff permission must be READ_ONLY")
    required_roles = {"PRIMARY_OWNER", "SUPPORTING_OWNER", "READ_ONLY_CONSUMER", "VALIDATOR", "INDEPENDENT_REVIEWER"}
    if not required_roles.issubset(set(data.get("node_roles", []))):
        fail("DAG node roles incomplete")


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
    receipts = sorted(RECEIPT_DIR.glob("*.json"))
    if len(receipts) < 2:
        fail("at least two real execution receipts are required")
    core = set(schema.get("required_core_fields", []))
    artifact_fields = set(schema.get("artifact_required_fields", []))
    review_fields = set(schema.get("review_required_fields", []))
    closure_fields = set(schema.get("closure_required_fields", []))
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
    print("resolver v1.2 / owner map / local+aggregate capability / adapter / artifact / regression / drift / eval coverage: CONSISTENT")


if __name__ == "__main__":
    main()
