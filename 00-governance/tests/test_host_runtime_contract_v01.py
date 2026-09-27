from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"


class HostRuntimeContractV01Tests(unittest.TestCase):
    def test_host_runtime_never_owns_project_or_design_authority(self) -> None:
        contract = json.loads((RUNTIME / "OLEANDER_HOST_RUNTIME_CONTRACT_v0.1.json").read_text(encoding="utf-8"))
        self.assertEqual("EXECUTION_HOST_AND_SURFACE_LIFECYCLE_ONLY", contract["authority_ceiling"])
        forbidden = set(contract["state_ownership"]["must_not_own"])
        self.assertTrue({"PROJECT_STATE", "PROJECT_CURRENT", "KNOWLEDGE_AUTHORITY", "DESIGN_KEEP", "PROMOTION"}.issubset(forbidden))

    def test_dsh_mapping_preserves_key_non_equivalences(self) -> None:
        adapter = json.loads((RUNTIME / "OLEANDER_DSH_HOST_ADAPTER_v0.1.json").read_text(encoding="utf-8"))
        self.assertEqual("CANDIDATE_REFERENCE_ADAPTER", adapter["status"])
        self.assertEqual("DSH_WORKSPACE_NE_OLEANDER_PROJECT", adapter["mapping"]["workspace_registry"]["boundary"])
        self.assertEqual("SESSION_LOG_NE_PROJECT_STATE", adapter["mapping"]["session_persistence"]["boundary"])
        self.assertIn("NEVER_WIDEN", adapter["mapping"]["approval"]["boundary"])

    def test_agy_link_is_reference_pattern_only(self) -> None:
        adapter = json.loads((RUNTIME / "OLEANDER_DSH_HOST_ADAPTER_v0.1.json").read_text(encoding="utf-8"))
        ref = adapter["third_party_provider_reference"]
        self.assertEqual("amlyczz/dsh-agy-link", ref["repository"])
        self.assertIn("IDENTITY_BOUND_PROVIDER_STATE", ref["borrow_patterns"])
        self.assertIn("NE_OLEANDER_RELIABILITY_OR_AUTHORITY_TRUTH", ref["boundary"])


if __name__ == "__main__":
    unittest.main()
