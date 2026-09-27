from __future__ import annotations

import hashlib
import importlib.util
import json
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

    def test_host_runtime_view_uses_health_and_surface_reliability_not_reachability_shortcut(self) -> None:
        result = self.host.host_runtime_view()
        local = next(row for row in result["hosts"] if row["host_runtime_id"] == "design_system_local_host")
        self.assertEqual("AVAILABLE", local["availability"])
        self.assertEqual("UNKNOWN", local["surface_reliability_status"])
        self.assertFalse(local["capabilities_runtime_verified"])

        original_health = self.host.health
        self.host.health = lambda: {"status": "DEGRADED"}  # type: ignore[method-assign]
        try:
            degraded = self.host.host_runtime_view()
        finally:
            self.host.health = original_health  # type: ignore[method-assign]
        degraded_local = next(row for row in degraded["hosts"] if row["host_runtime_id"] == "design_system_local_host")
        self.assertEqual("DEGRADED", degraded_local["availability"])
        self.assertFalse(degraded_local["capabilities_runtime_verified"])

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

        restricted = self.host.browser_profile(scope="RESTRICTED")
        self.assertEqual("RESTRICTED", restricted["scope"])
        self.assertEqual("UNBOUND", restricted["provider_binding"])
        with self.assertRaisesRegex(ValueError, "INVALID_BROWSER_PROFILE_SCOPE"):
            self.host.browser_profile(scope="INVALID")

    def test_browser_capture_ingress_runs_action_runtime_and_enters_source_inbox(self) -> None:
        data = b"<html><body><h1>Captured reference</h1></body></html>"
        upload = self.host.init_browser_capture({
            "url": "https://example.com/reference",
            "project_id": "C01",
            "scope": "PROJECT",
            "name": "reference.html",
            "size": len(data),
            "type": "text/html",
            "captured_at": "2026-09-27T05:00:00+00:00",
        })
        self.assertEqual("BROWSER_CAPTURE", upload["ingress_kind"])
        self.assertEqual("UNBOUND", upload["browser_profile"]["provider_binding"])
        self.host.put_chunk(upload["upload_id"], 0, data)
        result = self.host.commit_browser_capture({
            "upload_id": upload["upload_id"],
            "chunk_count": 1,
            "client_fingerprint": "sha256:" + hashlib.sha256(data).hexdigest(),
        })
        self.assertEqual("PASS", result["status"])
        self.assertEqual("COMPLETED", result["action_runtime_status"])
        self.assertEqual("ALLOW", result["guard_decision"]["decision"])
        self.assertEqual("READY", result["reliability_preflight"]["status"])
        self.assertEqual("VERIFIED", result["result_reliability"]["status"])
        source = result["source"]
        self.assertEqual("URL", source["source_kind"])
        self.assertEqual("https://example.com/reference", source["original_ref"])
        self.assertEqual("KNOWLEDGE_DRAFT_READY", source["ingestion_state"])
        self.assertEqual("CAPTURE_RECEIPT_NOT_BROWSER_PROVIDER_PROOF", source["browser_capture"]["semantic_class"])
        self.assertEqual("UNBOUND", source["browser_capture"]["provider_binding"])
        self.assertNotIn("knowledge_current", source)
        self.assertIn("BROWSER_PROVIDER_BOUND", result["does_not_prove"])

        readback = self.host.read_knowledge_draft(source["source_id"])
        self.assertEqual("PASS", readback["status"])
        self.assertIn("Captured reference", readback["body"]["sections"][0]["text"])
        self.assertEqual("OPEN", readback["knowledge_draft"]["review_state"])
        self.assertIn("KNOWLEDGE_CURRENT", readback["does_not_prove"])

    def test_browser_capture_invalid_url_fails_before_upload_or_source_persistence(self) -> None:
        before_uploads = {p.name for p in self.host.uploads_root.iterdir()}
        before_sources = {p.name for p in self.host.sources_root.iterdir()}
        with self.assertRaisesRegex(ValueError, "BROWSER_CAPTURE_URL_NOT_ALLOWED"):
            self.host.init_browser_capture({
                "url": "file:///C:/secret.txt",
                "scope": "RESEARCH",
                "name": "capture.html",
                "size": 3,
                "type": "text/html",
            })
        self.assertEqual(before_uploads, {p.name for p in self.host.uploads_root.iterdir()})
        self.assertEqual(before_sources, {p.name for p in self.host.sources_root.iterdir()})

    def test_text_upload_preserves_original_and_builds_knowledge_draft(self) -> None:
        result = self._upload("notes.md", b"# Site\nCourtyard relation to well.\n", "text/markdown")
        self.assertEqual("PASS", result["status"])
        source = result["source"]
        self.assertEqual("TEXT", source["source_kind"])
        self.assertEqual("KNOWLEDGE_DRAFT_READY", source["ingestion_state"])
        self.assertNotIn("knowledge_current", source)
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
        self.assertNotIn("knowledge_current", source)

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

        plan = self.host.transcription_plan(source["source_id"], "auto", "SEGMENT")
        self.assertEqual("TRANSCRIPT_PROVIDER_NOT_BOUND", plan["status"])
        self.assertEqual(source["source_revision"], plan["source_revision"])
        self.assertEqual("media.json", plan["media_ref"])

        request = self.host.create_transcription_request(
            source["source_id"],
            {"language": "auto", "timestamp_requirement": "SEGMENT"},
        )
        self.assertEqual("TRANSCRIPT_PROVIDER_NOT_BOUND", request["status"])
        self.assertEqual("COMPLETED", request["action_runtime_status"])
        self.assertEqual("ALLOW", request["guard_decision"]["decision"])
        self.assertEqual("BOUNDED_EXECUTION_POLICY_ONLY", request["guard_decision"]["authority_ceiling"])
        self.assertIn("KNOWLEDGE_CURRENT", request["guard_decision"]["does_not_prove"])
        self.assertEqual("READY", request["reliability_preflight"]["status"])
        self.assertEqual("VERIFIED", request["result_reliability"]["status"])
        self.assertEqual("TRANSCRIPT_PROVIDER_NOT_BOUND", request["transcription_request"]["state"])
        ledger_path = self.data_root / "runtime" / "execution.jsonl"
        self.assertTrue(ledger_path.is_file())
        ledger_before_reuse = ledger_path.read_bytes()
        self.assertFalse((self.host.sources_root / source["source_id"] / "transcript.json").exists())

        global_view = self.host.current_execution_view()["view"]
        local = next(row for row in global_view["surfaces"] if row["surface_id"] == "design_system_local_host")
        self.assertEqual("UNKNOWN", local["reliability_preflight"]["status"])

        reused = self.host.create_transcription_request(
            source["source_id"],
            {"language": "auto", "timestamp_requirement": "SEGMENT"},
        )
        self.assertEqual("TRANSCRIPT_PROVIDER_NOT_BOUND", reused["status"])
        self.assertEqual("REUSED_VERIFIED", reused["action_runtime_status"])
        self.assertEqual("PASS", reused["reuse_readback"]["status"])
        self.assertEqual(
            request["transcription_request"]["requested_at"],
            reused["transcription_request"]["requested_at"],
        )
        self.assertEqual(
            request["request_receipt"]["request_revision"],
            reused["request_receipt"]["request_revision"],
        )
        self.assertEqual("NOT_APPLICABLE_NO_NEW_EXECUTION", reused["result_reliability"]["status"])
        self.assertEqual(ledger_before_reuse, ledger_path.read_bytes())

        restarted = host_module.DesignSystemHost(self.data_root)
        persisted = restarted.list_transcription_requests(source["source_id"])
        self.assertEqual("PASS", persisted["status"])
        self.assertEqual(1, persisted["count"])
        self.assertEqual(request["transcription_request"]["request_id"], persisted["requests"][0]["request_id"])
        self.assertEqual("TRANSCRIPT_PROVIDER_NOT_BOUND", persisted["requests"][0]["state"])

        request_id = request["transcription_request"]["request_id"]
        request_path = self.host.sources_root / source["source_id"] / "transcription" / "requests" / f"{request_id}.json"
        receipt_path = request_path.with_suffix(".receipt.json")
        receipt_original_bytes = receipt_path.read_bytes()
        tampered_receipt = json.loads(receipt_original_bytes.decode("utf-8"))
        tampered_receipt["action_guard_decision_ref"] = "action-guard:tampered"
        receipt_path.write_text(json.dumps(tampered_receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tampered_receipt_bytes = receipt_path.read_bytes()
        retry_after_receipt_tamper = self.host.create_transcription_request(
            source["source_id"],
            {"language": "auto", "timestamp_requirement": "SEGMENT"},
        )
        self.assertEqual("HOLD_EXISTING_REQUEST_CHANGED", retry_after_receipt_tamper["status"])
        self.assertIn("REQUEST_RECEIPT_ACTION_GUARD_MISMATCH", retry_after_receipt_tamper["readback_errors"])
        self.assertEqual(tampered_receipt_bytes, receipt_path.read_bytes())
        self.assertEqual(ledger_before_reuse, ledger_path.read_bytes())
        receipt_path.write_bytes(receipt_original_bytes)

        tampered = json.loads(request_path.read_text(encoding="utf-8"))
        tampered["language"] = "tampered"
        request_path.write_text(json.dumps(tampered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tampered_bytes = request_path.read_bytes()
        tampered_readback = self.host.list_transcription_requests(source["source_id"])
        self.assertEqual("HOLD_REQUEST_CHANGED", tampered_readback["status"])
        self.assertIn("REQUEST_RECEIPT_DIGEST_MISMATCH", tampered_readback["requests"][0]["errors"])

        retry_after_tamper = self.host.create_transcription_request(
            source["source_id"],
            {"language": "auto", "timestamp_requirement": "SEGMENT"},
        )
        self.assertEqual("HOLD_EXISTING_REQUEST_CHANGED", retry_after_tamper["status"])
        self.assertIn("RETRY_SAFE", retry_after_tamper["does_not_prove"])
        self.assertEqual(tampered_bytes, request_path.read_bytes())
        self.assertEqual(ledger_before_reuse, ledger_path.read_bytes())

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

    def test_derived_body_tamper_holds_readback_without_source_drift(self) -> None:
        uploaded = self._upload("facts.txt", b"Source-bound body", "text/plain")
        source = uploaded["source"]
        source_dir = self.host.sources_root / source["source_id"]
        body_path = source_dir / "body.json"
        body = json.loads(body_path.read_text(encoding="utf-8"))
        body["sections"][0]["text"] = "tampered derived body"
        body_path.write_text(json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        listing = self.host.list_sources()
        row = next(item for item in listing["sources"] if item["source_id"] == source["source_id"])
        self.assertEqual("PASS", row["source_revision_readback"]["status"])
        self.assertEqual("HOLD_DERIVED_CHANGED", row["derived_integrity_readback"]["status"])
        self.assertFalse(row["derived_content_eligible"])
        self.assertFalse(row["body_available"])
        self.assertEqual("HOLD_DERIVED_CHANGED", row["ingestion_readback_state"])

        readback = self.host.read_knowledge_draft(source["source_id"])
        self.assertEqual("HOLD_DERIVED_CHANGED", readback["status"])
        self.assertEqual("PASS", readback["source_revision_readback"]["status"])
        self.assertIsNone(readback["body"])
        self.assertIsNone(readback["knowledge_draft"])
        self.assertIsNone(readback["media"])

    def test_derived_manifest_tamper_holds_readback(self) -> None:
        uploaded = self._upload("facts.txt", b"Source-bound body", "text/plain")
        source = uploaded["source"]
        source_dir = self.host.sources_root / source["source_id"]
        manifest_path = source_dir / host_module.MANIFEST_NAME
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["artifacts"][0]["sha256"] = "sha256:" + ("0" * 64)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        readback = self.host.read_knowledge_draft(source["source_id"])
        self.assertEqual("HOLD_DERIVED_CHANGED", readback["status"])
        self.assertEqual("DERIVED_MANIFEST_DIGEST_MISMATCH", readback["derived_integrity_readback"]["reason"])

    def test_transcription_contract_plan_is_source_bound_without_provider(self) -> None:
        source = {
            "source_id": "SRC-" + ("1" * 32),
            "source_revision": "sha256:" + ("2" * 64),
            "source_kind": "VIDEO",
        }
        media = {
            "status": "MEDIA_SUPPORT_READY",
            "source_id": source["source_id"],
            "source_revision": source["source_revision"],
            "media_ref": "media.json",
            "duration_seconds": 30.0,
        }
        plan = host_module.build_transcription_plan(
            source=source,
            media=media,
            provider=None,
            language="auto",
            timestamp_requirement="SEGMENT",
        )
        self.assertEqual("TRANSCRIPT_PROVIDER_NOT_BOUND", plan["status"])
        self.assertEqual(source["source_revision"], plan["source_revision"])
        self.assertEqual("media.json", plan["media_ref"])
        request = host_module.build_persistent_transcription_request(plan, requested_at="2026-09-27T00:00:00+00:00")
        self.assertEqual("TRANSCRIPT_PROVIDER_NOT_BOUND", request["state"])
        self.assertIn("PROVIDER_BOUND", request["does_not_prove"])

    def test_project_discovery_reads_bound_independent_projects_without_promoting_current(self) -> None:
        result = host_module.discover_project_candidates()
        names = {row["directory_name"] for row in result["projects"]}
        self.assertTrue({"c01-yimai-guangdu", "c02-daylily", "c03-the-light-collection", "c04-qingjiang-stone-book"}.issubset(names))
        rows = {row["directory_name"]: row for row in result["projects"]}
        expected_ids = {
            "c01-yimai-guangdu": "PRJ-C01-YIMAI-GUANGDU",
            "c02-daylily": "PRJ-C02-DAYLILY",
            "c03-the-light-collection": "PRJ-C03-LIGHT-COLLECTION",
            "c04-qingjiang-stone-book": "PRJ-C04-QINGJIANG-SHISHU",
        }
        for slug, project_id in expected_ids.items():
            row = rows[slug]
            self.assertEqual("BOUND", row["project_locator_status"])
            self.assertEqual(project_id, row["project_id"])
            self.assertEqual("PROJECT_LOCATOR_BOUND", row["state"])
            self.assertEqual("PROJECT_LOCATOR_BOUND_NOT_PROJECT_CURRENT", row["semantic_class"])
            self.assertEqual("BOUND", row["materialization_binding_status"])
            self.assertNotEqual("UNRESOLVED", row["artifact_store_binding"])
            self.assertNotEqual("UNRESOLVED", row["knowledge_mount_binding"])
            self.assertIn(row["migration_state"], {"NOT_SPLIT", "SPLIT_BRANCH_READY"})
            self.assertTrue(str(row["migration_branch"]).startswith("migration/"))
            self.assertTrue(row["local_repository_ready"])
            self.assertEqual("main", row["local_repository_branch"])
            self.assertEqual(["origin"], row["local_repository_remotes"])
        c04 = rows["c04-qingjiang-stone-book"]
        self.assertEqual("file:C04_CURRENT.md", c04["project_state_ref"])
        self.assertEqual("file:C04_CURRENT.md", c04["authority_ref"])
        for slug in ("c01-yimai-guangdu", "c02-daylily", "c03-the-light-collection"):
            self.assertEqual("file:README.md", rows[slug]["project_state_ref"])
            self.assertTrue(str(rows[slug]["authority_ref"]).startswith("platform-file:"))
        for row in result["projects"]:
            self.assertIn(row["migration_state"], {"NOT_SPLIT", "SPLIT_BRANCH_READY"})
            self.assertIn("PROJECT_CURRENT", result["does_not_prove"])


if __name__ == "__main__":
    unittest.main()
