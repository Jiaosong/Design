from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
V013 = ROOT / "90-shared/toolchains/modeling-worker/v0.13"


class ModelingWorkerV013G1Regression(unittest.TestCase):
    def test_control_card_and_full_g1_r2_machine_gate(self) -> None:
        card = V013 / "V013_REENTRY_CONTROL_CARD.json"
        cp = subprocess.run(
            [sys.executable, str(ROOT / "00-governance/control-plane/control_plane.py"), "check", str(card)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)

        with tempfile.TemporaryDirectory() as td:
            run = subprocess.run(
                [
                    sys.executable,
                    str(V013 / "g1_r2_qa.py"),
                    "--source", str(V013 / "G1_PRIMARY_CURVE_SOURCE.json"),
                    "--correction", str(V013 / "G1_R2_RELATION_CORRECTION.json"),
                    "--out", td,
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            report = json.loads((Path(td) / "G1_R2_MACHINE_REPORT.json").read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "MACHINE_PASS_RELATION_REVISION_PASS_VISUAL_REVIEW_REQUIRED")
            self.assertTrue(all(report["checks"].values()))
            self.assertTrue(all(report["baseline"]["checks"].values()))
            self.assertTrue(all(report["revised"]["checks"].values()))
            self.assertTrue(all(report["relation_revision"]["checks"].values()))
            self.assertEqual(report["authority_state"], "WORKING_SOURCE")
            self.assertEqual(report["design_state"], "EXPLORE")

    def test_r1_visual_failure_remains_immutable(self) -> None:
        text = (V013 / "G1_R1_VISUAL_DECISION.md").read_text(encoding="utf-8")
        self.assertIn("VISUAL REVISE", text)
        self.assertIn("PROJECT QA BLOCKED", text)
        self.assertIn("CANDIDATE REVIEW BLOCKED", text)


if __name__ == "__main__":
    unittest.main()
