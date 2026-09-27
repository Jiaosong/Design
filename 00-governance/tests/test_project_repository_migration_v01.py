from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"


class ProjectRepositoryMigrationV01Tests(unittest.TestCase):
    def test_four_projects_have_verified_local_split_repositories(self) -> None:
        inventory = json.loads((RUNTIME / "OLEANDER_PROJECT_REPOSITORY_MIGRATION_INVENTORY_20260927.json").read_text(encoding="utf-8"))
        self.assertEqual("MIGRATION_COMPLETE_COMPATIBILITY_MOUNT", inventory["status"])
        projects = inventory["projects"]
        self.assertEqual({"C01", "C02", "C03", "C04"}, {row["project_candidate_id"] for row in projects})
        for row in projects:
            self.assertEqual("SPLIT_BRANCH_READY", row["migration_state"])
            self.assertTrue(row["split_is_subdirectory_rooted"])
            self.assertTrue(row["local_repository_ready"])
            self.assertTrue(row["local_repository_contains_split_history"])
            self.assertEqual("main", row["local_repository_branch"])
            self.assertEqual(["origin"], row["local_repository_remotes"])
            self.assertTrue(row["old_duplicate_retained"])
            self.assertEqual("COMPATIBILITY_MOUNT", row["old_source_role"])
            self.assertGreater(row["compatibility_reference_count"], 0)
            self.assertTrue(row["migration_binding_closed"])
            self.assertTrue(row["remote_repo_created"])
            self.assertTrue(row["remote_repo_pushed"])
            self.assertEqual("VERIFIED", row["remote_repository_verification"])
            self.assertEqual("VERIFIED_HEAD_MATCH", row["remote_history_verification"])
            self.assertEqual("VERIFIED_LOCATOR_ONLY", row["bootstrap_manifest"]["status"])
            self.assertEqual("VERIFIED_MATERIALIZATION_BINDINGS", row["materialization_bindings"]["status"])
            self.assertEqual("VERIFIED_LOCAL_PATHS", row["artifact_store_binding"])
            self.assertNotEqual("UNRESOLVED", row["knowledge_mount_binding"])
        by_id = {row["project_candidate_id"]: row for row in projects}
        for project_id in ("C01", "C02", "C03"):
            row = by_id[project_id]
            self.assertEqual("file:README.md", row["project_state_ref"])
            self.assertEqual("PUBLIC_PROJECT_STATE", row["project_state_evidence"]["project_state_kind"])
            self.assertEqual("VERIFIED_OWNER_NATIVE_PROJECT_STATE", row["project_state_evidence"]["status"])
            self.assertTrue(row["project_state_evidence"]["owner_native_project_state_verified"])
            self.assertTrue(str(row["authority_ref"]).startswith("platform-file:"))

        c04 = by_id["C04"]
        self.assertEqual("file:C04_CURRENT.md", c04["project_state_ref"])
        self.assertEqual("file:C04_CURRENT.md", c04["authority_ref"])
        self.assertEqual("VERIFIED_OWNER_NATIVE_PROJECT_STATE", c04["project_state_evidence"]["status"])
        self.assertTrue(c04["project_state_evidence"]["owner_native_project_state_verified"])
        self.assertEqual("CURRENT_EXECUTION_AUTHORITY", c04["project_state_evidence"]["project_state_kind"])
        self.assertEqual("VERIFIED_LOCATOR_ONLY", c04["bootstrap_manifest"]["status"])

    def test_migration_readback_never_claims_remote_or_project_authority(self) -> None:
        inventory = json.loads((RUNTIME / "OLEANDER_PROJECT_REPOSITORY_MIGRATION_INVENTORY_20260927.json").read_text(encoding="utf-8"))
        self.assertEqual("MIGRATION_READBACK_ONLY", inventory["authority_ceiling"])
        self.assertIn("PROJECT_CURRENT", inventory["does_not_prove"])
        for row in inventory["projects"]:
            self.assertTrue(row["remote_repo_created"])
            self.assertTrue(row["remote_repo_pushed"])
            self.assertEqual(row["local_repository_revision"], row["remote_main_revision"])
            self.assertNotIn("VERIFY_TARGET_REMOTE_EXISTENCE_AND_HISTORY", row["next_actions"])
            self.assertNotIn("VERIFY_ARTIFACT_AND_KNOWLEDGE_BINDINGS", row["next_actions"])
            self.assertIn("RETAIN_COMPATIBILITY_MOUNT_UNTIL_PLATFORM_REFERENCE_REWRITE", row["next_actions"])

    def test_public_status_is_not_promoted_to_project_state_and_locator_remains_non_authority(self) -> None:
        inventory = json.loads((RUNTIME / "OLEANDER_PROJECT_REPOSITORY_MIGRATION_INVENTORY_20260927.json").read_text(encoding="utf-8"))
        self.assertIn("PROJECT_STATE_REF_NE_PROJECT_CURRENT", inventory["hard_invariants"])
        self.assertIn("PUBLIC_PROJECT_STATE_NE_PROJECT_CURRENT", inventory["hard_invariants"])
        self.assertIn("BOOTSTRAP_MANIFEST_IS_LOCATOR_ONLY_NOT_PROJECT_STATE", inventory["hard_invariants"])
        self.assertIn("COMPATIBILITY_MOUNT_NE_PROJECT_AUTHORITY", inventory["hard_invariants"])
        self.assertEqual(4, inventory["binding_progress"]["owner_native_project_state_verified"])
        self.assertEqual(0, inventory["binding_progress"]["project_state_unresolved"])
        self.assertEqual(4, inventory["binding_progress"]["bootstrap_locator_verified"])
        self.assertEqual(4, inventory["binding_progress"]["materialization_bindings_verified"])
        self.assertEqual(4, inventory["binding_progress"]["remote_history_verified"])
        self.assertEqual(0, inventory["binding_progress"]["artifact_store_unresolved"])
        self.assertEqual(0, inventory["binding_progress"]["knowledge_mount_unresolved"])
        for row in inventory["projects"]:
            bootstrap = row["bootstrap_manifest"]
            if bootstrap.get("locator_only_verified"):
                self.assertEqual("LOCATOR_ONLY", bootstrap["authority_ceiling"])


if __name__ == "__main__":
    unittest.main()
