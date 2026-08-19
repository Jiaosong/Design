import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / 'oleander-skills/oleander-3d-pipeline/tools/validate_regression_promotion.py'
spec = importlib.util.spec_from_file_location('regression_validator', TOOL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def base_receipt():
    return {
        'schema': 'oleander.3d.reference-regression-promotion-receipt.v1',
        'baseline_revision': 'V20',
        'candidate_revision': 'V23',
        'edit_scope': ['FRONT_CROSS_SECTION'],
        'target_metric_delta': {
            'metric_id': 'FRONT_HALF_PROJECTED_PROFILE_RMSE',
            'baseline': 0.15,
            'candidate': 0.08,
            'direction': 'LOWER_IS_BETTER',
            'improved': True,
        },
        'regression_locks': [
            {'id': 'SIDE_UPPER', 'baseline': 0.03, 'candidate': 0.03, 'limit': 0.04, 'status': 'PASS', 'evidence_source': 'projection'},
            {'id': 'SIDE_LOWER', 'baseline': 0.06, 'candidate': 0.06, 'limit': 0.07, 'status': 'PASS', 'evidence_source': 'projection'},
        ],
        'measurement_method_ids': ['FINAL_EVALUATED_MESH_XZ', 'FINAL_EVALUATED_MESH_YZ'],
        'measurement_comparability': 'COMPARABLE',
        'promotion_decision': 'PROMOTE_OVER_LKG',
        'visual_review_state': 'KEEP',
        'independent_visual_review': {
            'independent': True,
            'owner_is_reviewer': False,
            'reviewer_role': 'OLEANDER_INDEPENDENT_DESIGN_CRIT',
            'evidence_source': 'independent-reference-comparison-receipt.json',
        },
        'does_not_prove': ['manufacturer CAD'],
    }


def base_receipt_v2():
    d = base_receipt()
    d['schema'] = 'oleander.3d.reference-regression-promotion-receipt.v2'
    d['best_known_gate_baselines'] = {
        'SIDE_UPPER': {'revision': 'V23', 'value': 0.03, 'evidence_source': 'projection'},
        'SIDE_LOWER': {'revision': 'V23', 'value': 0.06, 'evidence_source': 'projection'},
    }
    for lock in d['regression_locks']:
        lock['baseline_revision'] = 'V23'
    return d


class RegressionPromotionValidatorTests(unittest.TestCase):
    def test_valid_promotion_requires_independent_visual_keep(self):
        self.assertEqual(mod.validate(base_receipt())['promotion_decision'], 'PROMOTE_OVER_LKG')

    def test_regression_blocks_promotion(self):
        d = base_receipt(); d['regression_locks'][0]['status'] = 'REGRESSED'
        with self.assertRaises(ValueError): mod.validate(d)

    def test_unimproved_target_blocks_promotion(self):
        d = base_receipt(); d['target_metric_delta']['improved'] = False
        with self.assertRaises(ValueError): mod.validate(d)

    def test_visual_reject_blocks_promotion(self):
        d = base_receipt(); d['visual_review_state'] = 'REJECT'
        with self.assertRaises(ValueError): mod.validate(d)

    def test_visual_hold_blocks_promotion(self):
        d = base_receipt(); d['visual_review_state'] = 'HOLD'
        with self.assertRaises(ValueError): mod.validate(d)

    def test_visual_not_run_blocks_promotion(self):
        d = base_receipt(); d['visual_review_state'] = 'NOT_RUN'
        with self.assertRaises(ValueError): mod.validate(d)

    def test_missing_independent_review_blocks_promotion(self):
        d = base_receipt(); d.pop('independent_visual_review')
        with self.assertRaises(ValueError): mod.validate(d)

    def test_owner_self_review_blocks_promotion(self):
        d = base_receipt(); d['independent_visual_review']['owner_is_reviewer'] = True
        with self.assertRaises(ValueError): mod.validate(d)

    def test_non_independent_review_blocks_promotion(self):
        d = base_receipt(); d['independent_visual_review']['independent'] = False
        with self.assertRaises(ValueError): mod.validate(d)

    def test_incomparable_requires_hold_or_rebase(self):
        d = base_receipt(); d['measurement_comparability'] = 'NOT_COMPARABLE'; d['promotion_decision'] = 'KEEP_LKG_HOLD_EXPERIMENT'; d['visual_review_state'] = 'HOLD'
        self.assertEqual(mod.validate(d)['promotion_decision'], 'KEEP_LKG_HOLD_EXPERIMENT')

    def test_rejected_experiment_can_validate_as_evidence(self):
        d = base_receipt(); d['regression_locks'][0]['status'] = 'REGRESSED'; d['promotion_decision'] = 'KEEP_LKG_REJECT_EXPERIMENT'; d['visual_review_state'] = 'REJECT'
        self.assertEqual(mod.validate(d)['promotion_decision'], 'KEEP_LKG_REJECT_EXPERIMENT')

    def test_valid_v2_best_known_baselines(self):
        self.assertEqual(mod.validate(base_receipt_v2())['schema'], 'oleander.3d.reference-regression-promotion-receipt.v2')

    def test_v2_weaker_baseline_revision_fails(self):
        d = base_receipt_v2(); d['regression_locks'][0]['baseline_revision'] = 'V20'
        with self.assertRaises(ValueError): mod.validate(d)

    def test_v2_weaker_baseline_value_fails(self):
        d = base_receipt_v2(); d['regression_locks'][0]['baseline'] = 0.04
        with self.assertRaises(ValueError): mod.validate(d)

    def test_v2_wrong_best_known_evidence_fails(self):
        d = base_receipt_v2(); d['best_known_gate_baselines']['SIDE_UPPER']['evidence_source'] = 'old_projection'
        with self.assertRaises(ValueError): mod.validate(d)


if __name__ == '__main__':
    unittest.main()
