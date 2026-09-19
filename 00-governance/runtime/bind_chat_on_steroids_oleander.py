#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path


BINDING_REVISION = "OLEANDER_CHAT_RESOLVER_BINDING_v1.4"
RESOLVER_REVISION = "1.2.5"
ADAPTER_REVISION = "1.2"
BEGIN = f"[[{BINDING_REVISION}:BEGIN]]"
END = f"[[{BINDING_REVISION}:END]]"
MAX_MCP_INSTRUCTIONS_CHARS = 4_000
MAX_GOAL_SYSTEM_PROMPT_CHARS = 20_000

MAIN_CHAT_BINDING = f"""{BEGIN}
For OLEANDER-scoped work, Chat On Steroids is an execution adapter only. Before a generic continue/execute/repair/optimize mutation or any KEEP/complete/stop claim, consume the existing OLEANDER resolver instead of inferring execution state from chat text.

Use `00-governance/runtime/oleander_chat_runtime_bridge.py`, which delegates to side-effect-free `oleander_chat_resolver_adapter.py` acceptance revision {ADAPTER_REVISION}, bound to `OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2` implementation revision {RESOLVER_REVISION}. Feed it Current authority/frontier/checkpoint/constraint/flow evidence; its result is transient and never becomes Project State.

Hard rules: transcript, handoff and summary are not checkpoint authority; generic continue resumes the verified `next_allowed_action`; CLOSED does not reopen; sticky constraints survive until explicit revocation; checkpoint sequence must be current before mutation; ready nodes auto-advance while legal; ambiguous frontier or authority/sequence drift revalidates or HOLDs.

Closure is stricter than Flow PASS. Whenever Flow Completion reaches PASS or a KEEP/complete/finalize claim is attempted, the bridge payload must also include `skill_consumption` and `quality_acceptance`. `skill_consumption` must name the minimum sufficient owner set and record the exact Current repo-relative canonical `SKILL.md` paths actually read; a same-named worktree/duplicate path or verbal claim is not evidence, and a Candidate remains Candidate. `quality_acceptance` must list task-derived required professional dimensions, actual gate evidence, scope coverage, and independent review when professional dimensions apply. Structure/persistence/page/object/reaction counts, hashes, CI green, file existence or render existence cannot satisfy visual, interaction, icon, motion, spatial-use, overall-form, constructive-connection or CMF quality gates. A producer cannot self-promote its result to professional KEEP. Missing or failing acceptance evidence must return HOLD/REVISE even when Flow Completion says PASS.

For professional-domain execution, also include `professional_stage_execution` whenever a professional process/stage is materially active. Treat the only top-level professional-stage order as `Stage → Professional Question / Decision Object → Knowledge Inputs → Operational Knowledge Mount → Required Capability Roles → Current Execution Owners / Skills → Native Outputs → Actual Readback → Independent Review → Stage Closure`. Pass the exact registered `process_ref`, `stage_id`, active supporting capability roles, explicit omission reasons for inactive supporting roles, and any Current project/specialist or independent-review owner bindings. Also pass task/claim-scoped `knowledge_mount_records` covering each active declared `knowledge_inputs` item; any omitted declared knowledge input needs an explicit N/A/not-triggered reason. Each mount must preserve operational eligibility, eligibility scope, claim ceiling, applicability, conditions, unresolved items, freshness/revalidation, `does_not_prove`, review basis and the stage knowledge input(s) it satisfies. Missing, uncovered, OE1/not-eligible or stale/revalidation-required mounts HOLD. For Candidate professional processes, also pass `candidate_evaluation_mode=BOUNDED_NON_CURRENT_PROJECT_EXERCISE`. Consume `professional_stage_composition` and its `canonical_stage_execution_readback` before execution/closure: unresolved knowledge/specialist/reviewer/callability roles HOLD; Candidate Skills and Candidate Bodies are not Current callable owners; multiple resolved Current owners require an actually materialized existing Multi-Skill DAG and typed handoffs. For a closure/KEEP/finalize attempt, also pass the existing stage-instance readback facts (`decision_object_refs`, `outputs`, `output_execution_bindings`, `actual_readback_refs`, `review_refs`, `review_verdict`, `exit_condition_state`); `stage_closure_gate` must PASS. Tool/Adapter, Claim, DD and Interface data are subordinate bindings, not extra top-level steps. A pre-release HOLD may create an evaluation receipt and continuation checkpoint, but `successor_receipt_ref` must remain null until the release condition is actually satisfied and a selective affected-binding retest executes.

For live Reader observability, invoke the same runtime bridge again with the refreshed source-observed checkpoint after each material verified checkpoint/node transition. When `task_id`, raw `status` and the existing checkpoint/receipt fields are present, the bridge may publish bounded latest-only telemetry; publish failure grants no authority and cannot change the resolver decision. Never create a second framework, Control Plane, Project State, checkpoint database or quality-state store to compensate for missing evidence.
{END}"""

GOAL_BINDING = f"""{BEGIN}
OLEANDER override for Goal/Objective/Loop decisions: do not decide continue or stop from transcript text, an assistant completion claim, compaction handoff, artifact counts, CI, hash, render existence or persistence evidence alone. Those are not completion authority.

The latest OLEANDER turn must be grounded in the recorded tool result from `00-governance/runtime/oleander_chat_runtime_bridge.py`; its preflight comes from Resolver v1.2 implementation revision {RESOLVER_REVISION} plus Chat acceptance revision {ADAPTER_REVISION}. `goal.includeToolCalls` is enabled so Goal/Loop can consume that readback directly. If no current machine result exists, instruct ChatGPT to run the existing bridge; do not invent a new task, plan, framework or state carrier.

Interpret directives strictly. `EXECUTE_NEXT_ALLOWED_ACTION` / `AUTO_ADVANCE_NEXT_READY_NODE` means continue that target. `REVALIDATE_*`, `REFRESH_FRONTIER_BEFORE_MUTATION`, `HOLD_*` or `REVISE_*` means continue only with that bounded repair/revalidation; do not stop. `STOP_CLOSED_TASK` or `STOP_FLOW_COMPLETION_GATE_PASS` means stop only when the same preflight also shows required `skill_consumption.gate=PASS` and `quality_acceptance.gate=PASS` (or explicit quality NOT_APPLICABLE with reason). Flow PASS without those gates is not a valid stop. In Loop mode this rule overrides generic polish loops: stop on verified closure, but never manufacture KEEP from structural evidence.
{END}"""


def _default_config() -> Path:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        raise SystemExit("APPDATA is unavailable; pass --config explicitly")
    return Path(appdata) / "chat-on-steroids" / "config.json"


def _replace_binding(text: str, binding: str) -> str:
    pattern = re.compile(
        r"\[\[OLEANDER_CHAT_RESOLVER_BINDING_v1\.[0-9]+:BEGIN\]\].*?"
        r"\[\[OLEANDER_CHAT_RESOLVER_BINDING_v1\.[0-9]+:END\]\]",
        re.DOTALL,
    )
    cleaned = pattern.sub("", text).strip()
    return f"{cleaned}\n\n{binding}".strip() if cleaned else binding


def _load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("CoS config root must be an object")
    return data


def _bound_config(data: dict) -> dict:
    next_data = json.loads(json.dumps(data, ensure_ascii=False))
    goal = next_data.setdefault("goal", {})
    mcp = next_data.setdefault("mcp", {})

    mcp["instructions"] = _replace_binding(str(mcp.get("instructions") or ""), MAIN_CHAT_BINDING)
    goal["includeToolCalls"] = True
    for field in ("prompt", "objectivePrompt", "loopPrompt"):
        current = goal.get(field)
        if not isinstance(current, str) or not current.strip():
            raise ValueError(f"goal.{field} is missing; refuse to replace the app's built-in prompt implicitly")
        goal[field] = _replace_binding(current, GOAL_BINDING)

    if len(mcp["instructions"]) > MAX_MCP_INSTRUCTIONS_CHARS:
        raise ValueError("mcp.instructions would exceed the current CoS 4,000-character limit")
    for field in ("prompt", "objectivePrompt", "loopPrompt"):
        if len(goal[field]) > MAX_GOAL_SYSTEM_PROMPT_CHARS:
            raise ValueError(f"goal.{field} would exceed the current CoS 20,000-character limit")
    return next_data


def _report(path: Path, data: dict) -> dict:
    goal = data.get("goal") or {}
    mcp = data.get("mcp") or {}
    return {
        "binding_revision": BINDING_REVISION,
        "resolver_implementation_revision": RESOLVER_REVISION,
        "adapter_acceptance_revision": ADAPTER_REVISION,
        "config": str(path),
        "goal_enabled_preserved": goal.get("enabled"),
        "goal_mode_preserved": goal.get("mode"),
        "goal_include_tool_calls": goal.get("includeToolCalls"),
        "mcp_bound": BEGIN in str(mcp.get("instructions") or "") and END in str(mcp.get("instructions") or ""),
        "goal_prompt_bound": BEGIN in str(goal.get("prompt") or ""),
        "goal_objective_prompt_bound": BEGIN in str(goal.get("objectivePrompt") or ""),
        "goal_loop_prompt_bound": BEGIN in str(goal.get("loopPrompt") or ""),
        "prompt_lengths": {
            "mcp.instructions": len(str(mcp.get("instructions") or "")),
            "goal.prompt": len(str(goal.get("prompt") or "")),
            "goal.objectivePrompt": len(str(goal.get("objectivePrompt") or "")),
            "goal.loopPrompt": len(str(goal.get("loopPrompt") or "")),
        },
        "runtime_reload_performed": False,
        "note": "Config persistence is verified here. A running CoS process keeps its in-memory config until its own settings save/reload path runs or the app is naturally restarted.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Persist the OLEANDER Resolver binding into existing Chat On Steroids settings.")
    parser.add_argument("--config", type=Path, default=None, help="Override the CoS config.json path")
    parser.add_argument("--apply", action="store_true", help="Write the binding after creating a UTF-8-safe backup")
    parser.add_argument("--verify", action="store_true", help="Read back the persisted binding")
    args = parser.parse_args()

    path = args.config or _default_config()
    data = _load(path)

    if args.apply:
        next_data = _bound_config(data)
        stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        backup = path.with_name(f"config.before-{BINDING_REVISION}-{stamp}.json")
        shutil.copy2(path, backup)
        tmp = path.with_suffix(path.suffix + ".oleander.tmp")
        tmp.write_text(json.dumps(next_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tmp.replace(path)
        data = _load(path)
        report = _report(path, data)
        report["backup"] = str(backup)
        report["persisted"] = True
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    if args.verify:
        print(json.dumps(_report(path, data), ensure_ascii=False, indent=2))
        return

    preview = _bound_config(data)
    report = _report(path, preview)
    report["persisted"] = False
    report["note"] = "Dry run only; pass --apply to persist. " + report["note"]
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
