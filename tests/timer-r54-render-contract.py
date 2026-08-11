#!/usr/bin/env python3
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "website/practice/timer-light-basin-v3/rendering/R54_RENDER_SPEC.json"
ADAPTER = ROOT / "website/practice/timer-light-basin-v3/rendering/timer_r54_blender52_cycles_adapter.py"
DOC = ROOT / "website/practice/timer-light-basin-v3/rendering/R54_PRODUCT_RENDERING_REBUILD.md"
CANONICAL = "900e02510ab6b2b5176aa3723dba7981700dc79b5f217dbe481844a534ed7c66"

m = json.loads(SPEC.read_text())
assert m["schema"] == "oleander.timer.r54.render-spec.v1"
assert m["status"] == "STANDARD_BUILT_PRODUCTION_RENDER_PENDING"
assert m["canonical"]["sha256"] == CANONICAL
assert m["canonical"]["mesh_count"] == 21
assert m["canonical"]["source_attributes"] == ["POSITION", "NORMAL"]
assert m["canonical"]["texcoord_0_present"] is False
assert m["canonical"]["tangent_present"] is False
assert m["canonical"]["source_units_to_render_meters"] == 0.001
assert m["canonical"]["source_bytes_must_remain_unchanged"] is True
assert len(m["qa_gates"]) == 7
assert m["output"]["primary_adapter"] == "Blender 5.2 LTS / Cycles"
assert m["execution"]["current_runtime"]["blender"] == "5.2.0 LTS fbe6228777e7"
assert m["execution"]["current_runtime"]["cycles"] == "CPU_PATH_TRACING_SMOKE_PASS"
assert m["execution"]["current_runtime"]["gpu_acceleration"] == "UNAVAILABLE_IN_CURRENT_CONTAINER"
assert m["execution"]["smoke_test"]["canonical_sha_verified"] is True
assert m["execution"]["smoke_test"]["canonical_meshes_loaded"] == 21
assert m["execution"]["smoke_test"]["multilayer_exr"] == "PASS"
assert m["execution"]["smoke_test"]["beauty_exr"] == "PASS"
assert m["execution"]["smoke_test"]["classification"] == "RUNTIME_COMPATIBILITY_ONLY_NOT_PRODUCTION_QUALITY"
assert m["execution"]["production_path_traced_render"] == "NOT_RUN"
assert m["execution"]["authority_impact"] == "NONE"
assert m["execution"]["posterlock_authority"] == "UNCHANGED"
assert m["execution"]["posterlock_manifest_authority"] == "PR_33_MERGED"

adapter = ADAPTER.read_text()
ast.parse(adapter)
for token in [
    CANONICAL,
    "SOURCE_UNITS_TO_METERS = 0.001",
    "Blender 5.2 LTS",
    "Khronos PBR Neutral",
    "AgX",
    "OPEN_EXR_MULTILAYER",
    "CompositorNodeOutputFile",
    "file_output_items",
]:
    assert token in adapter, f"adapter missing locked token: {token}"

doc = DOC.read_text()
for token in ["TEXCOORD_0", "TANGENT", "reflection design", "R54-G6", "POSTERLOCK remains authority"]:
    assert token in doc, f"documentation missing boundary: {token}"

print("Timer R54 product rendering contract: PASS")
