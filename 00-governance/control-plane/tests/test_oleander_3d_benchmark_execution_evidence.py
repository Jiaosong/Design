from __future__ import annotations
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = ROOT / 'oleander-skills' / 'oleander-3d-pipeline' / 'tools' / 'validate_benchmark_execution_evidence.py'
CONTRACT_PATH = ROOT / 'oleander-skills' / 'oleander-3d-pipeline' / 'contracts' / 'BENCHMARK_EXECUTION_EVIDENCE_CONTRACT_v1.json'

spec = importlib.util.spec_from_file_location('benchmark_execution_validator', VALIDATOR)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
CONTRACT = json.loads(CONTRACT_PATH.read_text(encoding='utf-8'))


def receipt():
    return {
        'schema': 'oleander.3d.benchmark-execution-receipt.v1',
        'benchmark_id': 'PORSCHE_911_V59',
        'source_commit': 'abc123',
        'target_revision': 'V59_SPARSE_FRONT_HOOD_FENDER_RELATION',
        'runtime': {
            'application': 'Blender',
            'version': '5.2.0 LTS',
            'platform': 'linux-x64',
            'runtime_support_state': 'VERIFIED_EXECUTED'
        },
        'invocation': {
            'entrypoint': 'run_reference_repro_v59.py',
            'target_revision_invoked': True,
            'exit_code': 0
        },
        'output_readback': {
            'receipt_path': 'out/V59/PRIMARY_BODY_SURFACE_RECEIPT_V2.json',
            'receipt_exists': True,
            'receipt_target_revision': 'V59_SPARSE_FRONT_HOOD_FENDER_RELATION',
            'artifact_readback': True
        },
        'baseline_comparison': {
            'required': True,
            'baseline_revision': 'V49_FEATURE_ALIGNED_CURVE_NETWORK',
            'candidate_revision': 'V59_SPARSE_FRONT_HOOD_FENDER_RELATION',
            'same_runtime_or_declared_delta': True,
            'comparability': 'CONTROLLED'
        },
        'execution_result': 'PASS_EXECUTED',
        'experiment_result': 'SCREENED',
        'evidence_result': 'HOLD_EVIDENCE_INCOMPLETE',
        'design_result': 'HOLD_NOT_REVIEWED',
        'does_not_prove': ['Reference Fidelity PASS', 'Design KEEP']
    }


class BenchmarkExecutionEvidenceTests(unittest.TestCase):
    def test_valid_executed_benchmark(self):
        self.assertTrue(mod.validate(receipt(), CONTRACT))

    def test_green_workflow_without_target_invocation_cannot_pass(self):
        d = receipt()
        d['invocation']['target_revision_invoked'] = False
        with self.assertRaises(SystemExit) as e:
            mod.validate(d, CONTRACT)
        self.assertIn('FAIL_TARGET_REVISION_NOT_EXECUTED', str(e.exception))

    def test_receipt_revision_must_match_target(self):
        d = receipt()
        d['output_readback']['receipt_target_revision'] = 'V58_V49_SURFACE_RECEIPT_V2'
        with self.assertRaises(SystemExit) as e:
            mod.validate(d, CONTRACT)
        self.assertIn('FAIL_RECEIPT_TARGET_REVISION_MISMATCH', str(e.exception))

    def test_negative_experiment_can_still_be_valid_execution(self):
        d = receipt()
        d['experiment_result'] = 'REJECT_HYPOTHESIS'
        self.assertTrue(mod.validate(d, CONTRACT))

    def test_ab_requires_comparable_runtime(self):
        d = receipt()
        d['baseline_comparison']['same_runtime_or_declared_delta'] = False
        with self.assertRaises(SystemExit) as e:
            mod.validate(d, CONTRACT)
        self.assertIn('HOLD_BENCHMARK_RUNTIME_COMPARABILITY_UNRESOLVED', str(e.exception))

    def test_machine_pass_cannot_self_promote_design(self):
        d = receipt()
        d['design_result'] = 'PASS_INDEPENDENT_DESIGN_REVIEW'
        with self.assertRaises(SystemExit) as e:
            mod.validate(d, CONTRACT)
        self.assertIn('FAIL_MACHINE_EXECUTION_SELF_PROMOTED_TO_DESIGN_PASS', str(e.exception))

    def test_independent_design_receipt_allows_separate_design_pass(self):
        d = receipt()
        d['design_result'] = 'PASS_INDEPENDENT_DESIGN_REVIEW'
        d['independent_design_review_receipt'] = 'ARTIFACT_REVIEW_3D_001'
        self.assertTrue(mod.validate(d, CONTRACT))


if __name__ == '__main__':
    unittest.main()
