#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "00-governance/runtime/OLEANDER_BLENDER_RUNTIME_v1.0.json"
DOC = ROOT / "00-governance/runtime/OLEANDER_BLENDER_RUNTIME_v1.0.md"
ACTIVATE = ROOT / "tools/oleander-runtime/activate-blender.sh"
WRAPPER = ROOT / "tools/oleander-runtime/blender.sh"
ENSURE = ROOT / "90-shared/toolchains/blender-runtime/ensure-blender-5.2.sh"
RUNNER = ROOT / ".github/workflows/oleander-shared-blender-runner.yml"

m = json.loads(REGISTRY.read_text())
assert m["schema"] == "oleander.runtime.blender.v1"
assert m["status"] == "ACTIVE_RUNTIME_INTERFACE"
assert m["scope"] == "OLEANDER_ALL_PROJECTS"
assert m["runtime"]["version"] == "5.2.0 LTS"
assert m["runtime"]["build_hash"] == "fbe6228777e7"
assert m["runtime"]["release_archive_sha256"] == "96f6c181a30f4950607839dc84d42a354b250d8a0231b098b59b7bc69c351c48"
assert m["runtime"]["render_engine"] == "CYCLES"
assert m["shared_runtime_state_model"]["hard_rule"] == "JOB_LOCAL_BINARY_ABSENCE_DOES_NOT_MEAN_SHARED_RUNTIME_UNAVAILABLE"
assert m["rematerialization"]["implementation"] == "90-shared/toolchains/blender-runtime/ensure-blender-5.2.sh"
assert m["rematerialization"]["project_ownership"] == "FORBIDDEN"
assert m["shared_runner"]["implementation"] == ".github/workflows/oleander-shared-blender-runner.yml"
assert m["shared_runner"]["role"] == "UNIVERSAL_PRODUCTION_ENVIRONMENT_SUBORDINATE_RUNTIME_ADAPTER_NOT_PROJECT_FRAMEWORK"
assert m["project_policy"]["project_specific_absolute_blender_paths"] == "FORBIDDEN"
assert m["project_policy"]["vendoring_blender_binary_in_repository"] == "FORBIDDEN"
assert m["project_policy"]["project_specific_blender_install_or_download_logic"].startswith("FORBIDDEN")

activate = ACTIVATE.read_text()
wrapper = WRAPPER.read_text()
ensure = ENSURE.read_text()
runner = RUNNER.read_text()
doc = DOC.read_text()

for token in [
    "OLEANDER_BLENDER_BIN",
    "command -v blender",
    "/mnt/data/runtime/blender-5.2.0-lts/blender",
    "OLEANDER_RENDER_ENGINE",
]:
    assert token in activate, f"activate script missing {token}"

for token in ["OLEANDER_BLENDER_BIN", "command -v blender", "exec \"$blender_bin\""]:
    assert token in wrapper, f"wrapper missing {token}"

for token in [
    "ARCHIVE_SHA256",
    "download.blender.org/release/Blender5.2",
    "sha256sum",
    "/mnt/data/runtime/blender-5.2.0-lts/blender",
]:
    assert token in ensure, f"rematerialization script missing {token}"

for token in [
    "workflow_call:",
    "OLEANDER_JOB_OUTPUT_DIR",
    "90-shared/toolchains/blender-runtime/ensure-blender-5.2.sh",
    "--python-exit-code",
]:
    assert token in runner, f"shared runner missing {token}"

for token in [
    "OLEANDER ALL PROJECTS",
    "Project files must not hard-code a project-specific Blender path",
    "Interface state is not job-local binary state",
    "Shared rematerialization",
    "Shared runner",
    "Evidence boundary",
    "not restricted to Timer Light Basin or any other individual project",
]:
    assert token in doc, f"runtime documentation missing boundary: {token}"

print("OLEANDER Blender shared-runtime contract: PASS")
