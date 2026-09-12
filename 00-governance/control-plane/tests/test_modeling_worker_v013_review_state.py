from __future__ import annotations
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
V013 = ROOT / '90-shared/toolchains/modeling-worker/v0.13'

class ModelingWorkerV013ReviewState(unittest.TestCase):
    def test_review_state_is_pass_but_promotion_is_not_run(self):
        receipt = json.loads((V013/'V013_REVIEW_STATE_RECEIPT.json').read_text(encoding='utf-8'))
        patch = json.loads((V013/'V013_REVIEW_CARD_PATCH.json').read_text(encoding='utf-8'))
        self.assertEqual(receipt['design_state'], 'EXPLORE')
        self.assertEqual(receipt['authority_state'], 'WORKING_SOURCE')
        for key in ('machine','visual','project','candidate_review'):
            self.assertEqual(receipt[key], 'PASS')
            self.assertEqual(patch['evidence_state'][key], 'PASS')
        self.assertEqual(receipt['candidate_promotion'], 'NOT_RUN')
        self.assertEqual(patch['candidate_promotion'], 'NOT_RUN')
        self.assertEqual(patch['mode'], 'EXPLORE')
        self.assertEqual(patch['authority_state'], 'WORKING_SOURCE')

if __name__ == '__main__':
    unittest.main()
