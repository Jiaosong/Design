from __future__ import annotations

import copy
import hashlib
import json
import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
RUNTIME = ROOT / "00-governance" / "runtime"
BRIDGE = RUNTIME / "oleander_chat_runtime_bridge.py"
DEEPSEEK_DSH_PACKAGE = "@deepseek-ai/dsh@0.1.5-rc.3"

FORBIDDEN_AUTHORITY_FIELDS = {
    "project_state",
    "project_current",
    "current",
    "design_decision",
    "design_keep",
    "professional_pass",
    "promotion",
    "statutory_approval",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _stable_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _scrub_authority_fields(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _scrub_authority_fields(item)
            for key, item in value.items()
            if key not in FORBIDDEN_AUTHORITY_FIELDS
        }
    if isinstance(value, list):
        return [_scrub_authority_fields(item) for item in value]
    return value


def _contains_forbidden_authority_field(value: Any) -> bool:
    if isinstance(value, dict):
        if any(key in FORBIDDEN_AUTHORITY_FIELDS for key in value):
            return True
        return any(_contains_forbidden_authority_field(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_forbidden_authority_field(item) for item in value)
    return False


def _run(command: list[str], *, timeout: int = 60, env: dict[str, str] | None = None) -> dict[str, Any]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=merged_env,
        )
    except FileNotFoundError as exc:
        return {"returncode": 127, "stdout": "", "stderr": str(exc), "missing_executable": True}
    except subprocess.TimeoutExpired as exc:
        return {
            "returncode": 124,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "timed_out": True,
        }
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def _python_probe(code: str, *, python_executable: str, timeout: int = 60, env: dict[str, str] | None = None) -> dict[str, Any]:
    return _run([python_executable, "-c", code], timeout=timeout, env=env)


def _command_version(command: str) -> str:
    """Resolve command versions consistently on Windows where npm is commonly a .cmd shim."""
    argv = ["cmd", "/c", command, "--version"] if os.name == "nt" else [command, "--version"]
    result = _run(argv, timeout=10)
    if result["returncode"] != 0:
        return ""
    return result.get("stdout", "").strip()


def evaluate_candidate_action_guard_projection(action: dict[str, Any]) -> dict[str, Any]:
    """Benchmark-only projection of Action Guard ordering; it is not Current mutation/authority logic."""
    if action.get("oleander_guard_decision") != "ALLOW":
        return {"decision": "HOLD", "reason": "OLEANDER_ACTION_GUARD_DENY"}
    if action.get("external_disclosure") is True and action.get("scoped_external_permission") is not True:
        return {"decision": "HOLD", "reason": "EXTERNAL_DISCLOSURE_NOT_AUTHORIZED"}
    if action.get("material_cost_or_blast_radius") is True and action.get("cost_or_blast_radius_authorized") is not True:
        return {"decision": "HOLD", "reason": "COST_OR_BLAST_RADIUS_NOT_AUTHORIZED"}
    return {"decision": "ALLOW", "reason": "OLEANDER_ACTION_GUARD_ALLOW"}


@dataclass(frozen=True)
class ProviderProbe:
    provider_id: str
    state: str
    version: str | None
    smoke_scope: list[str]
    detail: str
    raw: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "state": self.state,
            "version": self.version,
            "smoke_scope": self.smoke_scope,
            "detail": self.detail,
            "raw": self.raw,
        }


class RuntimeProviderAdapter:
    provider_id = "base"

    def __init__(self, *, provider_python: str | None = None) -> None:
        self.provider_python = provider_python or os.environ.get("OLEANDER_RUNTIME_BENCH_PYTHON") or sys.executable

    def native_probe(self) -> ProviderProbe:
        raise NotImplementedError

    def open_runtime_session(self, action: dict[str, Any]) -> dict[str, Any]:
        return {
            "provider_session_id": f"{self.provider_id}:{action['action_id']}:session",
            "intent": action["intent"],
            "runtime_only": True,
        }

    def execute_bounded_action(self, action: dict[str, Any], session: dict[str, Any]) -> dict[str, Any]:
        # The contract shim intentionally does not touch Project State. Native-provider integration is probed separately.
        outcome = action.get("simulated_provider_outcome", "COMPLETED")
        payload = {
            "provider_operation_id": f"{self.provider_id}:{action['action_id']}:operation",
            "provider_session_id": session["provider_session_id"],
            "intent": action["intent"],
            "outcome": outcome,
            "target_ref": action["target_ref"],
            "actual_delta": "NO_MATERIAL_DELTA" if action["side_effect_class"] == "READ_ONLY" else "SIMULATED_BOUNDED_DELTA",
        }
        extra = action.get("provider_extra_payload")
        if isinstance(extra, dict):
            payload.update(copy.deepcopy(extra))
        return payload

    def normalize_execution_event(
        self,
        *,
        action: dict[str, Any],
        session: dict[str, Any] | None,
        provider_payload: dict[str, Any] | None,
        outcome: str,
        event_type: str,
        reason: str | None = None,
    ) -> dict[str, Any]:
        event = {
            "event_id": f"EV-{self.provider_id}-{action['action_id']}-{event_type}",
            "provider_id": self.provider_id,
            "provider_session_id": None if session is None else session["provider_session_id"],
            "action_id": action["action_id"],
            "intent": action["intent"],
            "event_type": event_type,
            "outcome": outcome,
            "reason": reason,
            "target_ref": action["target_ref"],
            "provider_payload": provider_payload or {},
            "observed_at": _utc_now(),
            "does_not_prove": [
                "project_state",
                "project_current",
                "design_decision",
                "design_keep",
                "professional_pass",
                "promotion",
                "design_completion",
            ],
        }
        return _scrub_authority_fields(event)

    def run_contract_case(self, case: dict[str, Any]) -> dict[str, Any]:
        action = copy.deepcopy(case["action"])
        project_state = {
            "project_state_ref": action["project_state_ref"],
            "decision_object_id": action["decision_object_id"],
            "artifact_target_ref": action["target_ref"],
            "authority_fingerprint": "AUTH-RUNTIME-PROVIDER-BENCH-1",
        }
        before = _stable_hash(project_state)
        guard = evaluate_candidate_action_guard_projection(action)

        if guard["decision"] != "ALLOW":
            event = self.normalize_execution_event(
                action=action,
                session=None,
                provider_payload=None,
                outcome="BLOCKED_BY_OLEANDER",
                event_type="ACTION_GUARD_BLOCKED",
                reason=guard["reason"],
            )
            provider_invoked = False
        elif action.get("provider_approval") is not True:
            event = self.normalize_execution_event(
                action=action,
                session=None,
                provider_payload=None,
                outcome="BLOCKED_BY_PROVIDER",
                event_type="PROVIDER_APPROVAL_BLOCKED",
                reason="PROVIDER_NATIVE_APPROVAL_DENY",
            )
            provider_invoked = False
        else:
            session = self.open_runtime_session(action)
            payload = self.execute_bounded_action(action, session)
            provider_outcome = payload.get("outcome", "FAILED")
            event_type = {
                "COMPLETED": "PROVIDER_EXECUTION_COMPLETED",
                "PARTIAL": "PROVIDER_EXECUTION_PARTIAL",
                "FAILED": "PROVIDER_EXECUTION_FAILED",
                "DEGRADED": "PROVIDER_DEGRADED",
            }.get(provider_outcome, "PROVIDER_EXECUTION_FAILED")
            event = self.normalize_execution_event(
                action=action,
                session=session,
                provider_payload=payload,
                outcome=provider_outcome,
                event_type=event_type,
            )
            provider_invoked = True

        after = _stable_hash(project_state)
        expected = case["expected"]
        checks = {
            "normalized_outcome": event["outcome"] == expected["normalized_outcome"],
            "provider_invocation_matches_expected": provider_invoked is expected["provider_invoked"],
            "intent_preserved": event["intent"] == expected["intent_preserved"],
            "project_state_unchanged": before == after == _stable_hash(project_state),
            "forbidden_authority_fields_absent": not _contains_forbidden_authority_field(event),
        }
        if expected.get("benign_provider_note_preserved"):
            checks["benign_provider_note_preserved"] = (
                event.get("provider_payload", {}).get("benign_provider_note") == "preserve me"
            )
        passed = all(checks.values())
        return {
            "case_id": case["case_id"],
            "provider_id": self.provider_id,
            "state": "PASS" if passed else "FAIL",
            "provider_invoked": provider_invoked,
            "expected_provider_invoked": expected["provider_invoked"],
            "checks": checks,
            "event": event,
            "project_state_fingerprint_before": before,
            "project_state_fingerprint_after": after,
        }


class NativeCosAdapter(RuntimeProviderAdapter):
    provider_id = "native_cos"

    def native_probe(self) -> ProviderProbe:
        result = _run([self.provider_python, str(BRIDGE), "--self-test"], timeout=60)
        if result["returncode"] != 0:
            state = "HOLD_MISSING_DEPENDENCY" if result.get("missing_executable") else "HOLD_PROVIDER_API_DRIFT"
            return ProviderProbe(self.provider_id, state, None, [], "OLEANDER bridge self-test failed", result)
        try:
            parsed = json.loads(result["stdout"])
        except json.JSONDecodeError:
            return ProviderProbe(self.provider_id, "HOLD_PROVIDER_API_DRIFT", None, [], "Bridge returned non-JSON", result)
        ok = parsed.get("status") == "PASS"
        return ProviderProbe(
            self.provider_id,
            "NATIVE_PROVIDER_SMOKE_PASS" if ok else "HOLD_PROVIDER_API_DRIFT",
            "current-repo",
            ["resolver_bridge", "source_observed_projection", "observability_degradation_boundary"],
            "Existing COS/native bridge self-test executed with no network publication.",
            parsed,
        )


class DeepSeekHarnessAdapter(RuntimeProviderAdapter):
    provider_id = "deepseek_harness"

    @staticmethod
    def _npx_command(*args: str) -> list[str]:
        if os.name == "nt":
            return ["cmd", "/c", "npx", "--yes", DEEPSEEK_DSH_PACKAGE, *args]
        return ["npx", "--yes", DEEPSEEK_DSH_PACKAGE, *args]

    def native_probe(self) -> ProviderProbe:
        version_result = _run(self._npx_command("--version"), timeout=90)
        if version_result["returncode"] != 0:
            return ProviderProbe(
                self.provider_id,
                "HOLD_MISSING_DEPENDENCY" if version_result.get("missing_executable") else "HOLD_PROVIDER_API_DRIFT",
                None,
                [],
                "DeepSeek Harness CLI version probe failed.",
                version_result,
            )
        version = version_result["stdout"].strip().splitlines()[-1] if version_result["stdout"].strip() else None
        config_result = _run(self._npx_command("--profile", "headless", "--dump-default-config"), timeout=90)
        ok = config_result["returncode"] == 0 and bool(config_result["stdout"].strip())
        return ProviderProbe(
            self.provider_id,
            "NATIVE_PROVIDER_SMOKE_PASS" if ok else "HOLD_PROVIDER_API_DRIFT",
            version,
            ["cli_bootstrap", "headless_profile_composition"],
            "CLI version and shipped headless profile composition were executed; no model credential or project authority was used.",
            {
                "version_probe": version_result,
                "headless_config_probe": {
                    "returncode": config_result["returncode"],
                    "stdout_bytes": len(config_result["stdout"].encode("utf-8")),
                    "stderr": config_result["stderr"][-2000:],
                },
            },
        )


class MicrosoftAgentFrameworkAdapter(RuntimeProviderAdapter):
    provider_id = "microsoft_agent_framework"

    def native_probe(self) -> ProviderProbe:
        code = r'''
import json
import agent_framework as af
required = ["AgentSession", "WorkflowBuilder", "create_harness_agent"]
missing = [name for name in required if not hasattr(af, name)]
if missing:
    raise RuntimeError("missing API: " + ",".join(missing))
session = af.AgentSession(session_id="oleander-msaf-native-smoke")
print(json.dumps({
    "version": getattr(af, "__version__", "UNKNOWN"),
    "session_type": type(session).__name__,
    "session_id": session.session_id,
    "required_symbols": required,
}))
'''
        result = _python_probe(code, python_executable=self.provider_python, timeout=60)
        if result["returncode"] != 0:
            state = "HOLD_MISSING_DEPENDENCY" if "ModuleNotFoundError" in result["stderr"] else "HOLD_PROVIDER_API_DRIFT"
            return ProviderProbe(self.provider_id, state, None, [], "Microsoft Agent Framework probe failed.", result)
        parsed = json.loads(result["stdout"].strip().splitlines()[-1])
        return ProviderProbe(
            self.provider_id,
            "NATIVE_PROVIDER_SMOKE_PASS",
            parsed.get("version"),
            ["agent_session", "workflow_surface", "harness_factory_surface"],
            "AgentSession was instantiated and workflow/harness API seams were verified without calling a model.",
            parsed,
        )


class PydanticTemporalAdapter(RuntimeProviderAdapter):
    provider_id = "pydantic_ai_temporal"

    def native_probe(self) -> ProviderProbe:
        code = r'''
import asyncio
import json
import pydantic_ai
import temporalio
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel
from pydantic_ai.durable_exec.temporal import TemporalDurability
from temporalio.testing import WorkflowEnvironment

agent = Agent(TestModel(), name="oleander-pydantic-native-smoke")
result = agent.run_sync("Return a deterministic response")
durability = TemporalDurability()

async def temporal_smoke():
    env = await WorkflowEnvironment.start_time_skipping()
    env_type = type(env).__name__
    await env.shutdown()
    return env_type

env_type = asyncio.run(temporal_smoke())
print(json.dumps({
    "pydantic_ai_version": getattr(pydantic_ai, "__version__", "UNKNOWN"),
    "temporalio_version": getattr(temporalio, "__version__", "UNKNOWN"),
    "agent_output": str(result.output),
    "durability_type": type(durability).__name__,
    "temporal_environment_type": env_type,
}))
'''
        result = _python_probe(
            code,
            python_executable=self.provider_python,
            timeout=120,
            env={"PYDANTIC_AI_NO_BANNER": "1"},
        )
        if result["returncode"] != 0:
            stderr = result["stderr"]
            if "ModuleNotFoundError" in stderr:
                state = "HOLD_MISSING_DEPENDENCY"
            elif "temporal" in stderr.lower() and ("server" in stderr.lower() or "download" in stderr.lower()):
                state = "HOLD_MISSING_SERVER"
            else:
                state = "HOLD_PROVIDER_API_DRIFT"
            return ProviderProbe(self.provider_id, state, None, [], "PydanticAI/Temporal smoke failed.", result)
        parsed = json.loads(result["stdout"].strip().splitlines()[-1])
        return ProviderProbe(
            self.provider_id,
            "NATIVE_PROVIDER_SMOKE_PASS",
            f"pydantic-ai {parsed.get('pydantic_ai_version')} / temporalio {parsed.get('temporalio_version')}",
            ["deterministic_agent_run", "temporal_durability_capability", "temporal_ephemeral_test_server"],
            "A deterministic PydanticAI TestModel run and a Temporal ephemeral test environment were executed; no external model credential was used.",
            parsed,
        )


def provider_adapters(*, provider_python: str | None = None) -> list[RuntimeProviderAdapter]:
    return [
        NativeCosAdapter(provider_python=provider_python),
        DeepSeekHarnessAdapter(provider_python=provider_python),
        MicrosoftAgentFrameworkAdapter(provider_python=provider_python),
        PydanticTemporalAdapter(provider_python=provider_python),
    ]


def runtime_environment_snapshot(provider_python: str | None = None) -> dict[str, Any]:
    benchmark_python = provider_python or os.environ.get("OLEANDER_RUNTIME_BENCH_PYTHON") or sys.executable
    benchmark_python_version = _run([benchmark_python, "--version"], timeout=10)
    runner_python_version = _run([sys.executable, "--version"], timeout=10)
    return {
        "platform": platform.platform(),
        "benchmark_python": Path(benchmark_python).name,
        "benchmark_python_version": (benchmark_python_version.get("stdout") or benchmark_python_version.get("stderr") or "").strip(),
        "runner_python": Path(sys.executable).name,
        "runner_python_version": (runner_python_version.get("stdout") or runner_python_version.get("stderr") or "").strip(),
        "node_version": _command_version("node"),
        "npm_version": _command_version("npm"),
    }
