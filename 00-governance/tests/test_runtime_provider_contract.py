from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

from runtime_provider_spikes.provider_adapters import (  # noqa: E402
    DeepSeekHarnessAdapter,
    MicrosoftAgentFrameworkAdapter,
    NativeCosAdapter,
    PydanticTemporalAdapter,
    evaluate_candidate_action_guard_projection,
)


CASES = RUNTIME / "runtime_provider_spikes" / "provider_conformance_cases_v0.1.json"


class RuntimeProviderContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = json.loads(CASES.read_text(encoding="utf-8"))["cases"]
        cls.adapters = [
            NativeCosAdapter(),
            DeepSeekHarnessAdapter(),
            MicrosoftAgentFrameworkAdapter(),
            PydanticTemporalAdapter(),
        ]

    def test_all_four_contract_shims_pass_all_shared_cases(self) -> None:
        for adapter in self.adapters:
            with self.subTest(provider=adapter.provider_id):
                results = [adapter.run_contract_case(case) for case in self.cases]
                self.assertEqual(9, len(results))
                self.assertTrue(all(row["state"] == "PASS" for row in results))

    def test_oleander_deny_wins_before_provider_approval(self) -> None:
        case = next(row for row in self.cases if row["case_id"] == "RPC-04-OLEANDER-DENY-WINS")
        result = NativeCosAdapter().run_contract_case(case)
        self.assertFalse(result["provider_invoked"])
        self.assertEqual("BLOCKED_BY_OLEANDER", result["event"]["outcome"])
        self.assertEqual("ACTION_GUARD_BLOCKED", result["event"]["event_type"])

    def test_provider_can_narrow_but_not_widen(self) -> None:
        case = next(row for row in self.cases if row["case_id"] == "RPC-09-PROVIDER-MAY-NARROW")
        result = NativeCosAdapter().run_contract_case(case)
        self.assertFalse(result["provider_invoked"])
        self.assertEqual("BLOCKED_BY_PROVIDER", result["event"]["outcome"])
        self.assertTrue(result["checks"]["provider_invocation_matches_expected"])

    def test_read_only_sensitive_external_disclosure_is_not_implicitly_allowed(self) -> None:
        case = next(row for row in self.cases if row["case_id"] == "RPC-05-READONLY-DISCLOSURE-DENY")
        decision = evaluate_candidate_action_guard_projection(case["action"])
        self.assertEqual("HOLD", decision["decision"])
        self.assertEqual("EXTERNAL_DISCLOSURE_NOT_AUTHORIZED", decision["reason"])

    def test_provider_authority_payload_is_scrubbed(self) -> None:
        case = next(row for row in self.cases if row["case_id"] == "RPC-08-FORBIDDEN-AUTHORITY-FIELDS-STRIPPED")
        result = NativeCosAdapter().run_contract_case(case)
        payload = result["event"]["provider_payload"]
        self.assertNotIn("project_current", payload)
        self.assertNotIn("design_decision", payload)
        self.assertNotIn("promotion", payload)
        self.assertEqual("preserve me", payload["benign_provider_note"])


if __name__ == "__main__":
    unittest.main()
