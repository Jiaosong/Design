from __future__ import annotations

import importlib.util
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HOST_PATH = ROOT / "apps" / "oleander-design-system" / "host.py"

spec = importlib.util.spec_from_file_location("oleander_design_system_host", HOST_PATH)
assert spec and spec.loader
host_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(host_module)


class DesignSystemLocalHostV01Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.data_root = Path(self.temp.name)
        self.host = host_module.DesignSystemHost(self.data_root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _upload(self, name: str, data: bytes, content_type: str) -> dict:
        upload = self.host.init_upload({"name": name, "size": len(data), "type": content_type})
        if data:
            self.host.put_chunk(upload["upload_id"], 0, data)
            count = 1
        else:
            count = 0
        return self.host.commit_upload({"upload_id": upload["upload_id"], "chunk_count": count})

    def test_health_is_execution_only(self) -> None:
        result = self.host.health()
        self.assertEqual("PASS", result["status"])
        self.assertEqual("EXECUTION_CAPABILITY_AND_OBSERVABILITY_ONLY", result["authority_ceiling"])
        self.assertIn("PROJECT_CURRENT", result["does_not_prove"])

    def test_current_execution_view_uses_strict_r1_r4_observations(self) -> None:
        result = self.host.current_execution_view()
        self.assertEqual("PASS", result["status"])
        surfaces = {row["surface_id"]: row for row in result["view"]["surfaces"]}
        local = surfaces["design_system_local_host"]
        self.assertEqual("UNKNOWN", local["reliability_preflight"]["status"])
        self.assertTrue(local["reliability_preflight"]["strict_vector"])
        self.assertEqual("PASS", local["reliability_preflight"]["stages"]["R1_ADMISSION"]["state"])
        self.assertEqual("UNKNOWN", local["reliability_preflight"]["stages"]["R3_CAPABILITY"]["state"])
        self.assertEqual("UNKNOWN", local["reliability_preflight"]["stages"]["R4_EXECUTION"]["state"])
        self.assertNotIn("R5_RESULT", local["reliability_preflight"]["stages"])
        self.assertIn("PROJECT_CURRENT", result["view"]["does_not_prove"])

    def test_surface_views_are_projection_only_and_keep_unavailable_surfaces_visible(self) -> None:
        result = self.host.surface_views()
        self.assertEqual("UI_PROJECTION_ONLY", result["authority_ceiling"])
        views = {row["surface_definition_id"]: row for row in result["surface_views"]}
        self.assertEqual("AVAILABLE", views["design_system_local_host"]["availability"])
        self.assertEqual("UNKNOWN", views["design_system_local_host"]["reliability_preflight"]["status"])
        self.assertIn("github_connector", views)
        self.assertIn(views["github_connector"]["availability"], {"UNKNOWN", "UNREGISTERED"})
        self.assertEqual("UI_PROJECTION_ONLY", views["github_connector"]["authority_ceiling"])

    def test_browser_profile_is_context_projection_not_project_state(self) -> None:
        unbound = self.host.browser_profile()
        self.assertEqual("RESEARCH", unbound["scope"])
        self.assertIsNone(unbound["project_id"])
        project = self.host.browser_profile("C01")
        self.assertEqual("PROJECT", project["scope"])
        self.assertEqual("C01", project["project_id"])
        self.assertEqual("SOURCE_INBOX", project["capture_target"])
        self.assertIn("PROJECT_STATE", project["does_not_prove"])

    def test_text_upload_preserves_original_and_builds_knowledge_draft(self) -> None:
        result = self._upload("notes.md", b"# Site\nCourtyard relation to well.\n", "text/markdown")
        self.assertEqual("PASS", result["status"])
        source = result["source"]
        self.assertEqual("TEXT", source["source_kind"])
        self.assertEqual("KNOWLEDGE_DRAFT_READY", source["ingestion_state"])
        self.assertFalse(source["knowledge_current"])
        source_dir = self.host.sources_root / source["source_id"]
        self.assertTrue((source_dir / "original" / "notes.md").is_file())
        self.assertTrue((source_dir / "body.json").is_file())
        self.assertTrue((source_dir / "knowledge_draft.json").is_file())
        self.assertEqual("KNOWLEDGE_DRAFT_READY", result["extraction"]["status"])

    def test_video_upload_is_preserved_without_false_absorption_claim(self) -> None:
        result = self._upload("lecture.mp4", b"not-a-real-video-fixture", "video/mp4")
        self.assertEqual("PASS", result["status"])
        source = result["source"]
        self.assertEqual("VIDEO", source["source_kind"])
        self.assertEqual("ORIGINAL_PRESERVED", source["ingestion_state"])
        self.assertEqual("EXTRACTOR_NOT_BOUND", result["extraction"]["status"])
        self.assertFalse(source["knowledge_current"])

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg/ffprobe not available")
    def test_valid_video_gets_metadata_and_keyframes_but_no_false_transcript(self) -> None:
        fixture = self.data_root / "fixture.mp4"
        subprocess.run(
            [
                shutil.which("ffmpeg"),
                "-v", "error",
                "-f", "lavfi",
                "-i", "color=c=black:s=320x180:d=1",
                "-f", "lavfi",
                "-i", "anullsrc=r=16000:cl=mono",
                "-shortest",
                "-c:v", "libx264",
                "-c:a", "aac",
                "-y",
                str(fixture),
            ],
            check=True,
            timeout=30,
        )
        result = self._upload("lecture.mp4", fixture.read_bytes(), "video/mp4")
        source = result["source"]
        self.assertEqual("VIDEO", source["source_kind"])
        self.assertEqual("ORIGINAL_PRESERVED", source["ingestion_state"])
        self.assertEqual("PARTIAL_MEDIA_EXTRACTED", result["extraction"]["status"])
        self.assertEqual("TRANSCRIPT_PROVIDER_NOT_BOUND", result["extraction"]["transcript_status"])
        media = source["media_extraction"]
        self.assertEqual("MEDIA_SUPPORT_READY", media["status"])
        self.assertGreater(media["duration_seconds"], 0)
        self.assertGreaterEqual(media["keyframe_count"], 1)
        self.assertFalse((self.host.sources_root / source["source_id"] / "body.json").exists())

    def test_xlsx_upload_builds_sheet_bound_structured_body(self) -> None:
        from openpyxl import Workbook

        fixture = self.data_root / "fixture.xlsx"
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Program"
        sheet.append(["Space", "Area"])
        sheet.append(["Courtyard", 120])
        workbook.save(fixture)
        workbook.close()
        result = self._upload("program.xlsx", fixture.read_bytes(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.assertEqual("KNOWLEDGE_DRAFT_READY", result["source"]["ingestion_state"])
        self.assertEqual("OPENPYXL_READ_ONLY", result["extraction"]["extractor"])
        body = self.host.read_knowledge_draft(result["source"]["source_id"])["body"]
        self.assertEqual("Program", body["sections"][0]["heading"])
        self.assertIn("Courtyard\t120", body["sections"][0]["text"])

    def test_commit_rejects_missing_chunk(self) -> None:
        upload = self.host.init_upload({"name": "bad.txt", "size": 3, "type": "text/plain"})
        with self.assertRaisesRegex(ValueError, "MISSING_CHUNK"):
            self.host.commit_upload({"upload_id": upload["upload_id"], "chunk_count": 1})

    def test_chunk_size_limit_is_enforced(self) -> None:
        upload = self.host.init_upload({"name": "large.bin", "size": host_module.MAX_CHUNK_BYTES + 1, "type": "application/octet-stream"})
        with self.assertRaisesRegex(ValueError, "CHUNK_TOO_LARGE"):
            self.host.put_chunk(upload["upload_id"], 0, b"x" * (host_module.MAX_CHUNK_BYTES + 1))

    def test_source_list_reads_back_body_without_promoting_current(self) -> None:
        uploaded = self._upload("facts.txt", b"Source-bound body", "text/plain")
        result = self.host.list_sources()
        self.assertEqual(1, result["count"])
        self.assertTrue(result["sources"][0]["body_available"])
        self.assertTrue(result["sources"][0]["knowledge_draft_available"])
        self.assertIn("KNOWLEDGE_CURRENT", result["does_not_prove"])
        body = self.host.read_knowledge_draft(uploaded["source"]["source_id"])
        self.assertIsNotNone(body["body"])
        self.assertEqual("OPEN", body["knowledge_draft"]["review_state"])
        self.assertEqual("UNGRADED", body["knowledge_draft"]["ki_state"])
        self.assertIn("KNOWLEDGE_CURRENT", body["does_not_prove"])

    def test_preserved_original_revision_drift_holds_derived_body_and_draft(self) -> None:
        uploaded = self._upload("facts.txt", b"Source-bound body", "text/plain")
        source = uploaded["source"]
        source_dir = self.host.sources_root / source["source_id"]
        original = source_dir / source["storage_relpath"]
        original.write_bytes(b"externally changed bytes")

        listing = self.host.list_sources()
        row = next(item for item in listing["sources"] if item["source_id"] == source["source_id"])
        self.assertEqual("HOLD_SOURCE_CHANGED", row["source_revision_readback"]["status"])
        self.assertFalse(row["derived_content_eligible"])
        self.assertFalse(row["body_available"])
        self.assertFalse(row["knowledge_draft_available"])
        self.assertTrue(row["body_file_present"])

        readback = self.host.read_knowledge_draft(source["source_id"])
        self.assertEqual("HOLD_SOURCE_CHANGED", readback["status"])
        self.assertIsNone(readback["body"])
        self.assertIsNone(readback["knowledge_draft"])
        self.assertIsNone(readback["media"])

    def test_project_discovery_reports_embedded_cases_as_candidates_only(self) -> None:
        result = host_module.discover_project_candidates()
        names = {row["directory_name"] for row in result["projects"]}
        self.assertTrue({"c01-yimai-guangdu", "c02-daylily", "c03-the-light-collection", "c04-qingjiang-stone-book"}.issubset(names))
        for row in result["projects"]:
            self.assertIsNone(row["project_state_ref"])
            self.assertEqual("DISCOVERED_PROJECT_CANDIDATE_NOT_PROJECT_STATE", row["semantic_class"])
            self.assertIn(row["migration_state"], {"NOT_SPLIT", "SPLIT_BRANCH_READY"})
            self.assertTrue(str(row["migration_branch"]).startswith("migration/"))
            if row["local_repository_ready"]:
                self.assertEqual("LOCAL_REPOSITORY_READY", row["state"])
                self.assertEqual("main", row["local_repository_branch"])
                self.assertEqual([], row["local_repository_remotes"])


if __name__ == "__main__":
    unittest.main()
