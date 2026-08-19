from __future__ import annotations
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[3]
VALIDATOR=ROOT/'oleander-skills'/'oleander-3d-pipeline'/'tools'/'validate_stage_capability_routing.py'
spec=importlib.util.spec_from_file_location('stage_capability_validator',VALIDATOR)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
CONTRACT=mod.json.loads((ROOT/'oleander-skills'/'oleander-3d-pipeline'/'contracts'/'STAGE_CAPABILITY_ROUTING_CONTRACT_v1.json').read_text())


def valid_receipt():
    return {
        'schema':'oleander.3d.stage-capability-routing-receipt.v1',
        'candidate_revision':'TEST_V1',
        'stage':'PRIMARY_FORM_PROXY_APERTURE_HOLD',
        'required_capabilities':['PRIMARY_FORM_PROJECTION','FRONT_GROSS_PROFILE'],
        'available_capabilities':['PRIMARY_FORM_PROJECTION','FRONT_GROSS_PROFILE','GREENHOUSE_VISUAL_PROXY'],
        'held_capabilities':['FINAL_APERTURE_ARCHITECTURE','FINAL_WINDSHIELD_FLANGE'],
        'held_result':'NOT_APPLICABLE_STAGE_HOLD',
        'failed_required_capabilities':[],
        'legacy_name_dependencies_not_required':['REF_WINDSHIELD'],
        'result':'PASS_STAGE_AWARE_ROUTING',
        'does_not_prove':['reference fidelity','design quality']
    }


class StageCapabilityRoutingTest(unittest.TestCase):
    def test_valid_stage_hold_passes(self):
        self.assertTrue(mod.validate(valid_receipt(),CONTRACT))

    def test_required_capability_cannot_be_held(self):
        d=valid_receipt(); d['required_capabilities'].append('FINAL_APERTURE_ARCHITECTURE')
        with self.assertRaises(SystemExit) as e: mod.validate(d,CONTRACT)
        self.assertIn('FAIL_REQUIRED_CAPABILITY_MISCLASSIFIED_AS_HOLD',str(e.exception))

    def test_missing_required_capability_cannot_pass(self):
        d=valid_receipt(); d['required_capabilities'].append('SURFACE_REFLECTION_DIAGNOSTIC')
        with self.assertRaises(SystemExit) as e: mod.validate(d,CONTRACT)
        self.assertIn('FAIL_REQUIRED_CAPABILITY_MISSING',str(e.exception))

    def test_failed_required_capability_blocks_pass(self):
        d=valid_receipt(); d['failed_required_capabilities']=['FRONT_GROSS_PROFILE']
        with self.assertRaises(SystemExit) as e: mod.validate(d,CONTRACT)
        self.assertIn('FAIL_STAGE_PASS_WITH_FAILED_REQUIRED_CAPABILITY',str(e.exception))


if __name__=='__main__':
    unittest.main()
