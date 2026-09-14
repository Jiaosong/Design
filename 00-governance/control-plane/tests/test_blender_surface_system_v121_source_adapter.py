from __future__ import annotations

import importlib.util
import json
import py_compile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
V121 = ROOT / "90-shared/toolchains/blender-surface-system/v1.21.0"
ADAPTER = V121 / "source_authority_adapter.py"
CONTRACT = V121 / "SOURCE_AUTHORITY_ADAPTER_CONTRACT_v1.21.0.json"
V013 = ROOT / "90-shared/toolchains/modeling-worker/v0.13"
BINDING = V013 / "G1_SURFACE_SOURCE_CONTEXT_BINDING_v1.json"


def load_adapter():
    spec = importlib.util.spec_from_file_location("oleander_surface_source_adapter_v121", ADAPTER)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot import v1.21 source adapter")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BlenderSurfaceSystemV121SourceAdapter(unittest.TestCase):
    def test_contract_boundary_and_identity(self):
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(contract["system"], "OLEANDER Blender Surface System")
        self.assertEqual(contract["version"], "v1.21.0")
        self.assertEqual(contract["parent_surface_system"], "v1.20.0")
        self.assertEqual(
            contract["adapter_api"],
            "oleander.blender-surface-system.source-authority-adapter.v1",
        )
        self.assertTrue(contract["source_authority"]["before_after_diagnostic_snapshot_required"])
        self.assertTrue(contract["source_authority"]["source_geometry_mutation_during_diagnostic_forbidden"])
        self.assertTrue(contract["source_authority"]["source_material_mutation_during_diagnostic_forbidden"])
        self.assertFalse(contract["diagnostic_proxy"]["authority"])
        self.assertTrue(contract["diagnostic_proxy"]["diagnostic_material_mutation_allowed_on_proxy_only"])
        self.assertTrue(contract["integration_rule"]["modeling_worker_source_authority_remains_owner"])
        self.assertTrue(contract["integration_rule"]["surface_system_may_read_and_bind_but_not_redefine_source"])
        self.assertEqual(len(contract["source_authority"]["expected_objects"]), 6)

    def test_modeling_worker_v013_binding_consumes_v121_adapter(self):
        adapter = load_adapter()
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        binding = json.loads(BINDING.read_text(encoding="utf-8"))
        identity = adapter.validate_context_binding(binding, contract)
        self.assertEqual(identity["status"], "PASS")
        self.assertTrue(all(identity["checks"].values()))
        self.assertEqual(binding["source_owner"], "MODELING_WORKER_v0.13")
        self.assertEqual(
            binding["surface_system"]["module"],
            "90-shared/toolchains/blender-surface-system/v1.21.0/source_authority_adapter.py",
        )
        self.assertEqual(
            binding["surface_system"]["parent_render_runtime"],
            "90-shared/toolchains/blender-surface-system/v1.20.0/f1_design_validation_runtime.py",
        )
        self.assertIn(
            "termination_cap_pole_curvature_scale",
            binding["source_authority"]["captured_relation_properties"]["LOWER_RETURN_PROFILE"],
        )
        self.assertFalse(binding["source_authority"]["derived_execution_is_authority"])
        self.assertTrue(binding["diagnostic_policy"]["diagnostic_proxy_required"])

    def test_canonical_digest_is_order_stable_and_edit_sensitive(self):
        adapter = load_adapter()
        a = {
            "object": "OL_SRC_THUMB_SIDE_PLAN",
            "points": [[0.0, 0.1, 0.0], [0.1, 0.2, 0.0]],
            "properties": {"b": 2, "a": 1},
        }
        b = {
            "properties": {"a": 1, "b": 2},
            "points": [[0.0, 0.1, 0.0], [0.1, 0.2, 0.0]],
            "object": "OL_SRC_THUMB_SIDE_PLAN",
        }
        changed = {
            "properties": {"a": 1, "b": 2},
            "points": [[0.0, 0.1, 0.0], [0.1, 0.203, 0.0]],
            "object": "OL_SRC_THUMB_SIDE_PLAN",
        }
        self.assertEqual(adapter.canonical_digest(a), adapter.canonical_digest(b))
        self.assertNotEqual(adapter.canonical_digest(a), adapter.canonical_digest(changed))

    def test_source_unchanged_gate_fails_closed(self):
        adapter = load_adapter()
        before = {"source_sha256": "a" * 64}
        after = {"source_sha256": "a" * 64}
        self.assertEqual(adapter.assert_source_unchanged(before, after)["status"], "PASS")
        with self.assertRaises(RuntimeError):
            adapter.assert_source_unchanged(before, {"source_sha256": "b" * 64})
        self.assertTrue(adapter.source_edit_detected(before, {"source_sha256": "b" * 64}))

    def test_adapter_compiles_without_blender_and_proxy_guard_is_explicit(self):
        py_compile.compile(str(ADAPTER), doraise=True)
        text = ADAPTER.read_text(encoding="utf-8")
        self.assertIn('DERIVED_DIAGNOSTIC_ROLE = "DERIVED_DIAGNOSTIC_NOT_AUTHORITY"', text)
        self.assertIn("def snapshot_source_collection(", text)
        self.assertIn("def diagnostic_proxy(", text)
        self.assertIn("def assign_diagnostic_material(", text)
        self.assertIn('proxy["OLEANDER_AUTHORITY"] = "DERIVED_EXECUTION_NOT_AUTHORITY"', text)
        self.assertIn('Refusing material mutation on non-diagnostic object', text)


if __name__ == "__main__":
    unittest.main()
