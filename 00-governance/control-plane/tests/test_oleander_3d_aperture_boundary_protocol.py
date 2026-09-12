import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL = ROOT / 'oleander-skills/oleander-3d-pipeline/reference-reproduction/APERTURE_BACKING_BOUNDARY_OWNERSHIP_PROTOCOL_v1.md'


class ApertureBoundaryProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = PROTOCOL.read_text(encoding='utf-8')

    def test_complete_aperture_stack(self):
        for token in ('HOST_SURFACE','OPENING_BOUNDARY','INTERFACE_SURFACE','INFILL','BACKING_OR_VOID'):
            self.assertIn(token, self.text)

    def test_backing_missing_is_fail_closed(self):
        self.assertIn('FAIL_APERTURE_BACKING_MISSING', self.text)
        self.assertIn('REVISE_BACKING_OCCLUSION_ARCHITECTURE', self.text)

    def test_shared_boundary_has_single_owner(self):
        self.assertIn('exactly one canonical geometric definition', self.text)
        self.assertIn('FAIL_SHARED_BOUNDARY_DIVERGENCE', self.text)
        self.assertIn('REJECT_OVERLAPPING_INTERFACE_PATCHES', self.text)

    def test_profile_pass_cannot_promote_interface_failure(self):
        self.assertIn('PROJECTED_PROFILE_GATE=PASS', self.text)
        self.assertIn('BOUNDARY_CLOSURE_GATE=REJECT', self.text)

    def test_receipt_required(self):
        self.assertIn('APERTURE_INTERFACE_RECEIPT.json', self.text)
        self.assertIn('boundary owner IDs', self.text)
        self.assertIn('backing/occlusion objects', self.text)


if __name__ == '__main__':
    unittest.main()
