#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "00-governance/runtime/OLEANDER_BLENDER_RUNTIME_v1.0.json"
DOC = ROOT / "00-governance/runtime/OLEANDER_BLENDER_RUNTIME_v1.0.md"
ACTIVATE = ROOT / "tools/oleander-runtime/activate-blender.sh"
WRAPPER = ROOT / "tools/oleander-runtime/blender.sh"

m = json.loads(REGISTRY.read_text())
assert m["schema"] == "oleander.runtime.blender.v1"
assert m["status"] == "ACTIVE_RUNTIME_INTERFACE"
assert m["scope"] == "OLEANDER_ALL_PROJECTS"
assert m["runtime"]["version"] == "5.2.0 LTS"
assert m["runtime"]["build_hash"] == "fbe6228777e7"
assert m["runtime"]["release_archive_sha256"] == "96f6c181a30f4950607839dc84d42a354b250d8a0231b098b59b7bc69c351c48"
assert m["runtime"]["render_engine"] == "CYCLES"
assert m["project_policy"]["project_specific_absolute_blender_paths"] == "FORBIDDEN"
assert m["project_policy"]["vendoring_blender_binary_in_repository"] == "FORBIDDEN"

activate = ACTIVATE.read_text()
wrapper = WRAPPER.read_text()
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
    "OLEANDER ALL PROJECTS",
    "Project files must not hard-code a project-specific Blender path",
    "Evidence boundary",
    "not restricted to Timer Light Basin",
]:
    assert token in doc, f"runtime documentation missing boundary: {token}"

print("OLEANDER Blender shared-runtime contract: PASS")
