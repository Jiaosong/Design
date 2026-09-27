from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
sys.path.insert(0, str(RUNTIME))

from oleander_design_system_runtime import (  # noqa: E402
    admit_source,
    browser_capture_source,
    content_fingerprint,
    next_ingestion_state,
    validate_project_workspace_binding,
    validate_source_revision,
)


class DesignSystemRuntimeV01Tests(unittest.TestCase):
    def test_project_binding_accepts_one_primary_repo_and_runtime_workspace(self) -> None:
        result = validate_project_workspace_binding({
            "project_id": "C01",
            "project_state_ref": "owner-native:c01@R18",
            "authority_ref": "authority:c01",
            "repositories": [
                {"repository_ref": "github:Jiaosong/c01-yimai-guangdu", "role": "PRIMARY", "remote_identity": "github:Jiaosong"}
            ],
            "workspaces": [
                {"workspace_ref": "local:c01/r18", "workspace_class": "DESIGN_DIRECTION", "repository_ref": "github:Jiaosong/c01-yimai-guangdu", "observed_revision": "abc123"}
            ],
        })
        self.assertEqual("PASS", result["status"])
        self.assertIn("PROJECT_CURRENT", result["does_not_prove"])

    def test_project_binding_rejects_git_materialization_claiming_project_current(self) -> None:
        result = validate_project_workspace_binding({
            "project_id": "C01",
            "project_state_ref": "owner-native:c01@R18",
            "authority_ref": "authority:c01",
            "repositories": [
                {
                    "repository_ref": "github:Jiaosong/c01-yimai-guangdu",
                    "role": "PRIMARY",
                    "remote_identity": "github:Jiaosong",
                    "project_current": True,
                }
            ],
        })
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any(x.startswith("MATERIALIZATION_AUTHORITY_FIELD") for x in result["errors"]))

    def test_project_binding_requires_exactly_one_primary_when_repos_exist(self) -> None:
        result = validate_project_workspace_binding({
            "project_id": "KH46",
            "project_state_ref": "owner-native:kh46@R5",
            "authority_ref": "authority:kh46",
            "repositories": [
                {"repository_ref": "github:a", "role": "SATELLITE", "remote_identity": "github:user"},
                {"repository_ref": "github:b", "role": "SATELLITE", "remote_identity": "github:user"},
            ],
        })
        self.assertEqual("FAIL", result["status"])
        self.assertIn("EXACTLY_ONE_PRIMARY_REPOSITORY_REQUIRED_WHEN_REPOSITORIES_EXIST", result["errors"])

    def test_source_admission_preserves_draft_only_boundary(self) -> None:
        result = admit_source({
            "source_id": "SRC-001",
            "source_kind": "PDF",
            "original_ref": "file:reference.pdf",
            "fingerprint": "sha256:abc",
            "source_revision": "sha256:abc",
            "provenance": {"origin": "user-drop"},
        })
        self.assertEqual("ADMITTED", result["status"])
        self.assertFalse(result["source"]["knowledge_current"])
        self.assertEqual("PRESERVE_ORIGINAL", result["next_action"])

    def test_source_admission_rejects_authority_injection(self) -> None:
        result = admit_source({
            "source_id": "SRC-002",
            "source_kind": "PDF",
            "original_ref": "file:reference.pdf",
            "fingerprint": "sha256:def",
            "source_revision": "sha256:def",
            "provenance": {"origin": "user-drop"},
            "knowledge_current": True,
        })
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any(x.startswith("FORBIDDEN_AUTHORITY_FIELD") for x in result["errors"]))

    def test_ingestion_state_cannot_skip_review_and_ki(self) -> None:
        result = next_ingestion_state("CITATION_BOUND", "KI_GRADED")
        self.assertEqual("HOLD_INVALID_TRANSITION", result["status"])
        self.assertEqual("KNOWLEDGE_DRAFT_READY", result["allowed_next"])

    def test_changed_source_revision_holds_derived_body(self) -> None:
        result = validate_source_revision({"source_revision": "sha256:old"}, "sha256:new")
        self.assertEqual("HOLD_SOURCE_CHANGED", result["status"])
        self.assertFalse(result["derived_body_may_remain_eligible"])

    def test_browser_capture_enters_source_inbox_not_knowledge_current(self) -> None:
        result = browser_capture_source(
            source_id="WEB-1",
            url="https://example.com/article",
            capture_ref="capture:web-1",
            capture_digest="sha256:web1",
            captured_at="2026-09-27T02:30:00+09:00",
            provenance={"captured_by": "design-browser"},
        )
        self.assertEqual("ADMITTED", result["status"])
        self.assertEqual("URL", result["source"]["source_kind"])
        self.assertFalse(result["source"]["knowledge_current"])

    def test_content_fingerprint_is_stable(self) -> None:
        self.assertEqual(content_fingerprint(b"abc"), content_fingerprint(b"abc"))
        self.assertNotEqual(content_fingerprint(b"abc"), content_fingerprint(b"abcd"))


if __name__ == "__main__":
    unittest.main()
