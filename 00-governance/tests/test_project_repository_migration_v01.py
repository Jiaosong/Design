from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"


class ProjectRepositoryMigrationV01Tests(unittest.TestCase):
    def test_four_projects_have_verified_local_split_repositories(self) -> None:
        inventory = json.loads((RUNTIME / "OLEANDER_PROJECT_REPOSITORY_MIGRATION_INVENTORY_20260927.json").read_text(encoding="utf-8"))
        self.assertEqual("LOCAL_REPOSITORIES_READY", inventory["status"])
        projects = inventory["projects"]
        self.assertEqual({"C01", "C02", "C03", "C04"}, {row["project_candidate_id"] for row in projects})
        for row in projects:
            self.assertEqual("SPLIT_BRANCH_READY", row["migration_state"])
            self.assertTrue(row["split_is_subdirectory_rooted"])
            self.assertTrue(row["local_repository_ready"])
            self.assertTrue(row["local_repository_contains_split_history"])
            self.assertEqual("main", row["local_repository_branch"])
            self.assertEqual([], row["local_repository_remotes"])
            self.assertTrue(row["old_duplicate_retained"])
        by_id = {row["project_candidate_id"]: row for row in projects}
        for project_id in ("C01", "C02", "C03"):
            row = by_id[project_id]
            self.assertIsNone(row["project_state_ref"])
            self.assertEqual("EVIDENCE_ONLY_NOT_PROJECT_STATE", row["project_state_evidence"]["status"])
            self.assertFalse(row["project_state_evidence"]["owner_native_project_state_verified"])
            self.assertEqual("NOT_ELIGIBLE_PROJECT_STATE_UNRESOLVED", row["bootstrap_manifest"]["status"])

        c04 = by_id["C04"]
        self.assertEqual("file:C04_CURRENT.md", c04["project_state_ref"])
        self.assertEqual("file:C04_CURRENT.md", c04["authority_ref"])
        self.assertEqual("VERIFIED_OWNER_NATIVE_PROJECT_STATE", c04["project_state_evidence"]["status"])
        self.assertTrue(c04["project_state_evidence"]["owner_native_project_state_verified"])
        self.assertIn(c04["bootstrap_manifest"]["status"], {"MISSING", "VERIFIED_LOCATOR_ONLY"})

    def test_migration_readback_never_claims_remote_or_project_authority(self) -> None:
        inventory = json.loads((RUNTIME / "OLEANDER_PROJECT_REPOSITORY_MIGRATION_INVENTORY_20260927.json").read_text(encoding="utf-8"))
        self.assertEqual("MIGRATION_READBACK_ONLY", inventory["authority_ceiling"])
        self.assertIn("PROJECT_CURRENT", inventory["does_not_prove"])
        self.assertIn("REMOTE_REPOSITORY_CREATED", inventory["does_not_prove"])
        for row in inventory["projects"]:
            self.assertIsNone(row["remote_repo_created"])
            self.assertIsNone(row["remote_repo_pushed"])
            self.assertEqual("UNVERIFIED", row["remote_repository_verification"])
            self.assertEqual("UNVERIFIED", row["remote_history_verification"])
            self.assertIn("VERIFY_TARGET_REMOTE_EXISTENCE_AND_HISTORY", row["next_actions"])
            self.assertEqual("UNRESOLVED", row["artifact_store_binding"])
            self.assertEqual("UNRESOLVED", row["knowledge_mount_binding"])

    def test_public_status_is_not_promoted_to_project_state_and_locator_remains_non_authority(self) -> None:
        inventory = json.loads((RUNTIME / "OLEANDER_PROJECT_REPOSITORY_MIGRATION_INVENTORY_20260927.json").read_text(encoding="utf-8"))
        self.assertIn("PUBLIC_STATUS_SUMMARY_NE_OWNER_NATIVE_PROJECT_STATE", inventory["hard_invariants"])
        self.assertIn("BOOTSTRAP_MANIFEST_IS_LOCATOR_ONLY_NOT_PROJECT_STATE", inventory["hard_invariants"])
        self.assertEqual(1, inventory["binding_progress"]["owner_native_project_state_verified"])
        self.assertEqual(3, inventory["binding_progress"]["project_state_unresolved"])
        for row in inventory["projects"]:
            bootstrap = row["bootstrap_manifest"]
            if bootstrap.get("locator_only_verified"):
                self.assertEqual("LOCATOR_ONLY", bootstrap["authority_ceiling"])


if __name__ == "__main__":
    unittest.main()
