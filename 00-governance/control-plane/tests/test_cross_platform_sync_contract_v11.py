from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GOV = ROOT / "00-governance"


class CrossPlatformSyncContractV11(unittest.TestCase):
    def setUp(self):
        self.v10 = (GOV / "cross-platform-sync-contract-v1.0.md").read_text(encoding="utf-8")
        self.v11 = (GOV / "cross-platform-sync-contract-v1.1.md").read_text(encoding="utf-8")

    def test_exactly_one_current_sync_contract(self):
        self.assertIn("Status: SUPERSEDED / HISTORY", self.v10)
        self.assertIn("Superseded by: `cross-platform-sync-contract-v1.1.md`", self.v10)
        self.assertIn("Status: CURRENT / ACTIVE", self.v11)
        self.assertEqual(sum("Status: CURRENT / ACTIVE" in x for x in (self.v10, self.v11)), 1)

    def test_v11_binds_governance_source(self):
        self.assertIn("Source SHA-256: `82b02e0f01606ff31f45df3c12d66643b500f01bff80ddd11c8548a6b2b92cdf`", self.v11)
        for field in ("object", "source", "revision", "time", "hash", "state", "does-not-prove"):
            self.assertIn(f"`{field}`", self.v11)

    def test_material_delta_and_state_separation(self):
        self.assertIn("MATERIAL DELTA = NO", self.v11)
        self.assertIn("do not write, do not commit, do not open a PR", self.v11)
        self.assertIn("Artifact ≠ Commit ≠ PR ≠ Validated ≠ Merged ≠ Promoted", self.v11)
        self.assertIn("UNSYNCED", self.v11)
        self.assertIn("PARTIAL", self.v11)

    def test_owner_and_f_crossline_readback_are_required(self):
        self.assertIn("Owner Receipt / Run Manifest first", self.v11)
        self.assertIn("F cross-line readback", self.v11)
        self.assertIn("F_READBACK_FAIL", self.v11)
        self.assertIn("No F readback, no cross-line closure", self.v11)

    def test_binary_persistence_contract(self):
        for required in (
            "exact byte size",
            "SHA-256",
            "dependencies and linked assets required to reopen/rebuild",
            "independent retrieval result",
            "independent open / unzip / parse / load result",
        ):
            self.assertIn(required, self.v11)
        self.assertIn("PAP-G0—PAP-G6", self.v11)

    def test_dynamic_state_is_receipt_only_and_boundaries_retained(self):
        self.assertIn("Project State / Current Task RECEIPT ONLY", self.v11)
        self.assertIn("FIELD OBSERVED = 0", self.v11)
        self.assertIn("FIELD MEASURED = 0", self.v11)
        self.assertIn("G1F = HOLD", self.v11)
        self.assertIn("NO_PROMOTION", self.v11)


if __name__ == "__main__":
    unittest.main()
