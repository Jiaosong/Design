import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL = ROOT / 'oleander-skills/oleander-3d-pipeline/reference-reproduction/REGRESSION_BASELINE_PROMOTION_PROTOCOL_v1.md'


class RegressionBaselineProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = PROTOCOL.read_text(encoding='utf-8')

    def test_protocol_exists_and_declares_last_known_good(self):
        self.assertIn('LAST_KNOWN_GOOD', self.text)
        self.assertIn('Newer revision ≠ Better candidate', self.text)

    def test_regression_lock_is_fail_closed(self):
        self.assertIn('REJECT_REGRESSION_LOCK_BROKEN', self.text)
        self.assertIn('regression lock', self.text.lower())
        self.assertIn('threshold', self.text)

    def test_rejected_experiment_cannot_become_baseline(self):
        self.assertIn('KEEP_LKG_REJECT_EXPERIMENT', self.text)
        self.assertIn('FAIL_REJECTED_EXPERIMENT_BECAME_BASELINE', self.text)

    def test_measurement_tool_change_cannot_drive_geometry_edit(self):
        self.assertIn('DIAGNOSTIC_TOOL_CHANGE', self.text)
        self.assertIn('FAIL_MEASUREMENT_TOOL_MUTATED_GEOMETRY', self.text)
        self.assertIn('HOLD_MEASUREMENT_METHOD_NOT_VALIDATED', self.text)

    def test_promotion_requires_regression_free_candidate(self):
        self.assertIn('REGRESSION_PROMOTION_RECEIPT', self.text)
        self.assertIn('target_metric_delta', self.text)
        self.assertIn('measurement_method_ids', self.text)
        self.assertIn('visual_review_state', self.text)


if __name__ == '__main__':
    unittest.main()
