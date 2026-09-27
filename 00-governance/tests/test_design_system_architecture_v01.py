from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"


class DesignSystemArchitectureV01Tests(unittest.TestCase):
    def test_design_system_core_files_exist(self) -> None:
        for name in (
            "OLEANDER_DESIGN_SYSTEM_ARCHITECTURE_v0.1.md",
            "OLEANDER_DESIGN_SYSTEM_OBJECT_MODEL_v0.1.json",
            "OLEANDER_SURFACE_RELIABILITY_BOUNDARY_v0.1.json",
        ):
            self.assertTrue((RUNTIME / name).is_file(), name)

    def test_six_kernel_ownership_model_is_exact(self) -> None:
        model = json.loads((RUNTIME / "OLEANDER_DESIGN_SYSTEM_OBJECT_MODEL_v0.1.json").read_text(encoding="utf-8"))
        self.assertEqual(
            {"AuthorityKernel", "ProjectKernel", "DesignKernel", "KnowledgeKernel", "SurfaceKernel", "ExecutionKernel"},
            set(model["kernels"]),
        )

    def test_project_git_workspace_and_stores_are_not_collapsed(self) -> None:
        model = json.loads((RUNTIME / "OLEANDER_DESIGN_SYSTEM_OBJECT_MODEL_v0.1.json").read_text(encoding="utf-8"))
        rules = set(model["project_model"]["hard_non_equivalences"])
        self.assertTrue({
            "PROJECT_NE_REPOSITORY",
            "PROJECT_NE_RUNTIME_WORKSPACE",
            "PROJECT_NE_ARTIFACT_STORE",
            "PROJECT_NE_KNOWLEDGE_STORE",
            "GIT_BRANCH_NE_DESIGN_DIRECTION",
            "GIT_MERGE_NE_DESIGN_KEEP",
        }.issubset(rules))

    def test_source_body_and_vector_index_remain_distinct(self) -> None:
        model = json.loads((RUNTIME / "OLEANDER_DESIGN_SYSTEM_OBJECT_MODEL_v0.1.json").read_text(encoding="utf-8"))
        rules = set(model["knowledge_model"]["hard_non_equivalences"])
        self.assertIn("VECTOR_INDEX_NE_KNOWLEDGE", rules)
        self.assertIn("ORIGINAL_SOURCE_NE_EXTRACTED_BODY", rules)
        self.assertIn("IMPORTED_NE_KNOWLEDGE_CURRENT", rules)

    def test_surface_view_cannot_bypass_action_runtime(self) -> None:
        model = json.loads((RUNTIME / "OLEANDER_DESIGN_SYSTEM_OBJECT_MODEL_v0.1.json").read_text(encoding="utf-8"))
        rule = model["surface_view_model"]["rule"]
        self.assertIn("PRODUCT_ACTION", rule)
        self.assertIn("ACTION_RUNTIME", rule)


if __name__ == "__main__":
    unittest.main()
