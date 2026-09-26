#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path


BINDING_REVISION = "OLEANDER_CHAT_RESOLVER_BINDING_v1.7"
RESOLVER_REVISION = "1.2.5"
ADAPTER_REVISION = "1.2"
SYSTEM_GATEWAY_REVISION = "0.1"
MCP_SERVER_REF = "00-governance/runtime/oleander_system_mcp.py"
BEGIN = f"[[{BINDING_REVISION}:BEGIN]]"
END = f"[[{BINDING_REVISION}:END]]"
MAX_MCP_INSTRUCTIONS_CHARS = 4_000
MAX_GOAL_SYSTEM_PROMPT_CHARS = 20_000

MAIN_CHAT_BINDING = f"""{BEGIN}
For OLEANDER-scoped work, Chat On Steroids is an execution harness only. Resolve system context and execution permission through the OLEANDER System Gateway revision {SYSTEM_GATEWAY_REVISION}. Prefer the exposed OLEANDER System Gateway MCP tools when available; otherwise run `00-governance/runtime/oleander_system_gateway.py`. Do not infer Project State, Current, Knowledge Authority, Design Decision, Artifact Current, professional PASS or Promotion from chat text, CoS sessions, workers, plugins, tool logs, compaction handoffs or local file presence.

Before a material continue/resume/recover/execute/repair/optimize mutation or any KEEP/complete/finalize/stop claim, obtain a current gateway preflight from owner-native authority/frontier/checkpoint/constraint/readback evidence. The gateway composes the System Context Envelope, delegates execution policy to Resolver v1.2 implementation revision {RESOLVER_REVISION} / adapter acceptance revision {ADAPTER_REVISION}, and keeps CoS below the OLEANDER authority boundary.

CoS session continuity, Compact & Resume, workers, Goal/Loop, plugins and MCP tools are provider-runtime facilities only. Provider approval may narrow an OLEANDER allow but may never widen an OLEANDER deny. Plugin installed/ready does not grant capability authority or mutation permission. Missing Project/Knowledge/Authority fields remain unresolved rather than being invented.

Consume the gateway result literally: `system_context` is non-authoritative execution context; `runtime_bridge.preflight.conversation_directive` is the resolver directive. Preserve sticky user constraints, checkpoint sequence, minimum owner set, actual readback, professional-stage knowledge mounts and independent review requirements. Never create a parallel Project State, Knowledge Registry, Control Plane, checkpoint database, quality-state store or Promotion path.
{END}"""

GOAL_BINDING = f"""{BEGIN}
OLEANDER Goal/Objective/Loop decisions must consume the latest recorded OLEANDER System Gateway preflight. Transcript text, assistant completion language, CoS Compact & Resume, worker state, plugin status, artifact counts, CI, hashes, render existence and persistence alone are not completion authority.

If no current gateway result exists, obtain one instead of inventing a task, framework or state carrier. Interpret its existing resolver directive strictly: execute/auto-advance only the named allowed target; revalidate/refresh/HOLD/REVISE only the bounded repair; stop only when the same owner-native flow, skill-consumption, quality/professional and readback gates allow closure. CoS Goal/Loop is a continuation-policy consumer, never Project State or Design KEEP authority.
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
    mcp["runtimeContext"] = {
        "label": "OLEANDER System Gateway",
        "entrypoint": MCP_SERVER_REF,
        "authorityCeiling": "execution_and_observability",
    }
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
        "system_gateway_revision": SYSTEM_GATEWAY_REVISION,
        "resolver_implementation_revision": RESOLVER_REVISION,
        "adapter_acceptance_revision": ADAPTER_REVISION,
        "config": str(path),
        "goal_enabled_preserved": goal.get("enabled"),
        "goal_mode_preserved": goal.get("mode"),
        "goal_include_tool_calls": goal.get("includeToolCalls"),
        "runtime_context": mcp.get("runtimeContext"),
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
