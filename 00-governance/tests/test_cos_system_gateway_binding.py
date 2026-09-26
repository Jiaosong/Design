from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BINDER = ROOT / "00-governance" / "runtime" / "bind_chat_on_steroids_oleander.py"
spec = importlib.util.spec_from_file_location("oleander_cos_binder", BINDER)
assert spec and spec.loader
binder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(binder)


def base_config() -> dict:
    old = "[[OLEANDER_CHAT_RESOLVER_BINDING_v1.6:BEGIN]]\nold bootstrap\n[[OLEANDER_CHAT_RESOLVER_BINDING_v1.6:END]]"
    return {
        "goal": {
            "enabled": False,
            "mode": "goal",
            "includeToolCalls": False,
            "prompt": "base prompt\n\n" + old,
            "objectivePrompt": "objective\n\n" + old,
            "loopPrompt": "loop\n\n" + old,
        },
        "mcp": {"instructions": "user prefix\n\n" + old},
    }


class CosSystemGatewayBindingTests(unittest.TestCase):
    def test_v17_supersedes_v16_without_losing_user_text(self) -> None:
        result = binder._bound_config(base_config())
        self.assertIn("user prefix", result["mcp"]["instructions"])
        self.assertNotIn("v1.6", result["mcp"]["instructions"])
        self.assertIn("OLEANDER_CHAT_RESOLVER_BINDING_v1.7", result["mcp"]["instructions"])
        self.assertNotIn("old bootstrap", result["goal"]["prompt"])
        self.assertIn("base prompt", result["goal"]["prompt"])

    def test_runtime_context_is_structured_and_goal_state_is_preserved(self) -> None:
        data = base_config()
        result = binder._bound_config(data)
        self.assertEqual(False, result["goal"]["enabled"])
        self.assertEqual("goal", result["goal"]["mode"])
        self.assertTrue(result["goal"]["includeToolCalls"])
        self.assertEqual(
            {
                "label": "OLEANDER System Gateway",
                "entrypoint": "00-governance/runtime/oleander_system_mcp.py",
                "authorityCeiling": "execution_and_observability",
            },
            result["mcp"]["runtimeContext"],
        )

    def test_bound_prompts_stay_inside_cos_limits(self) -> None:
        result = binder._bound_config(base_config())
        self.assertLessEqual(len(result["mcp"]["instructions"]), binder.MAX_MCP_INSTRUCTIONS_CHARS)
        for field in ("prompt", "objectivePrompt", "loopPrompt"):
            self.assertLessEqual(len(result["goal"][field]), binder.MAX_GOAL_SYSTEM_PROMPT_CHARS)


if __name__ == "__main__":
    unittest.main()
