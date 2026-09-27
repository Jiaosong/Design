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
            self.assertTrue(row["local_repository_matches_split"])
            self.assertEqual("main", row["local_repository_branch"])
            self.assertEqual([], row["local_repository_remotes"])
            self.assertTrue(row["old_duplicate_retained"])
            self.assertIsNone(row["project_state_ref"])

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


if __name__ == "__main__":
    unittest.main()
