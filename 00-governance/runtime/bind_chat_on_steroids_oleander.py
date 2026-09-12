#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path


BINDING_REVISION = "OLEANDER_CHAT_RESOLVER_BINDING_v1.0"
RESOLVER_REVISION = "1.2.5"
BEGIN = f"[[{BINDING_REVISION}:BEGIN]]"
END = f"[[{BINDING_REVISION}:END]]"
MAX_MCP_INSTRUCTIONS_CHARS = 4_000
MAX_GOAL_SYSTEM_PROMPT_CHARS = 20_000

MAIN_CHAT_BINDING = f"""{BEGIN}
For OLEANDER-scoped work, Chat On Steroids is an execution adapter only. Before a generic continue/execute/repair/optimize mutation or any completion claim, consume the existing OLEANDER resolver instead of inferring execution state from chat text.

Use `00-governance/runtime/oleander_chat_resolver_adapter.py`, which binds `OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2` implementation revision {RESOLVER_REVISION}. Feed it Current authority/frontier/checkpoint/constraint/flow evidence; its result is transient and never becomes Project State.

Run the preflight through the normal CoS command surface so its structured JSON result is recorded as an actual tool call/readback. Hard rules: transcript, handoff and summary are not checkpoint authority; generic continue resumes the verified `next_allowed_action`; a CLOSED checkpoint is not reopened; sticky constraints remain active until a later explicit user revocation; checkpoint sequence must be current before mutation; ready nodes auto-advance while legal; ambiguous frontier or authority/sequence drift revalidates or HOLDs; completion is allowed only after the Flow Completion Gate returns PASS. Never create a second framework, Control Plane, Project State or checkpoint database to compensate for missing runtime state.
{END}"""

GOAL_BINDING = f"""{BEGIN}
OLEANDER override for Goal/Objective/Loop decisions: do not decide continue or stop from the transcript, an assistant completion claim, or a compaction handoff alone. Those are not checkpoint authority.

The latest OLEANDER execution turn must be grounded in the recorded tool result from `00-governance/runtime/oleander_chat_resolver_adapter.py` (existing Resolver v1.2 implementation revision {RESOLVER_REVISION}). `goal.includeToolCalls` is enabled by this binding so the decision context can consume that readback directly. If no current machine result is present, continue only by instructing ChatGPT to run the existing resolver preflight and follow its `conversation_directive`; do not invent a new task, plan, framework or state carrier.

Interpret directives strictly: `EXECUTE_NEXT_ALLOWED_ACTION` / `AUTO_ADVANCE_NEXT_READY_NODE` means continue that target; `REVALIDATE_*`, `REFRESH_FRONTIER_BEFORE_MUTATION` or `HOLD_*` means request only that bounded revalidation/HOLD action; `STOP_CLOSED_TASK` or `STOP_FLOW_COMPLETION_GATE_PASS` means the OLEANDER task is finished for generic continuation and no optional polish may be invented. In Goal/Objective mode return stop/NO_REPLY. In Loop mode this OLEANDER rule overrides the generic instruction to keep raising the bar: return stop rather than manufacturing more work. If the host refuses a Loop stop, fail closed and send no reopening follow-up.
{END}"""


def _default_config() -> Path:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        raise SystemExit("APPDATA is unavailable; pass --config explicitly")
    return Path(appdata) / "chat-on-steroids" / "config.json"


def _replace_binding(text: str, binding: str) -> str:
    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.DOTALL)
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
