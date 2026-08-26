#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
PACK = RUNTIME / "OLEANDER_CLOUD_FREE_CAPABILITY_PACK_v0.1.json"
REGISTRY = RUNTIME / "OLEANDER_SHARED_EXECUTION_SURFACES_v0.1.json"
ROUTING = RUNTIME / "OLEANDER_CLOUD_FREE_EXECUTION_ROUTING_BINDING_v0.1.json"
CARD = RUNTIME / "templates" / "OLEANDER_PROJECT_ENVIRONMENT_CARD_v0.1.md"
STUDIO = RUNTIME / "cloud-free-studio" / "index.html"


def fail(msg: str) -> None:
    raise SystemExit(f"CLOUD_FREE_CAPABILITY_VALIDATION_FAIL: {msg}")


def require(text: str, tokens: list[str], label: str) -> None:
    missing = [t for t in tokens if t not in text]
    if missing:
        fail(f"{label} missing tokens: {missing}")


def main() -> None:
    required_files = [PACK, REGISTRY, ROUTING, CARD, STUDIO]
    if any(not p.exists() for p in required_files):
        fail("pack / registry / routing / project card / studio missing")

    pack = json.loads(PACK.read_text(encoding="utf-8"))
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    routing = json.loads(ROUTING.read_text(encoding="utf-8"))

    if pack.get("status") != "CANDIDATE_SHARED_REPO_RUNTIME":
        fail("capability pack must remain candidate before real project browser readback")
    if pack.get("routing_binding") != "00-governance/runtime/OLEANDER_CLOUD_FREE_EXECUTION_ROUTING_BINDING_v0.1.json":
        fail("capability pack is not bound to current Cloud-Free execution routing")
    rb = pack.get("readback_state_2026_08_26", {})
    if rb.get("browser_pass") != "OPEN_NOT_CLAIMED":
        fail("browser PASS must remain open until real browser evidence exists")

    required_holds = {
        "NEW_PROFESSIONAL_BIM_CAD",
        "CLASS_A_MANUFACTURING_CAD",
        "FROM_ZERO_HIGH_END_ARCHVIZ_CGI",
        "SUPPLIER_PREPRESS_PROOF",
        "ENGINEERING_APPROVAL",
        "FIELD_ACCEPTANCE",
    }
    if not required_holds.issubset(set(pack.get("hard_holds_preserved", []))):
        fail("professional capability HOLD set was weakened")
    if not required_holds.issubset(set(routing.get("hard_holds", []))):
        fail("routing binding weakened professional capability HOLD set")

    expected_order = [
        "AGENT_EXECUTABLE_CURRENT_CONNECTOR",
        "CURRENT_OLEANDER_SKILL_WITH_NATIVE_OUTPUT",
        "SHARED_REPO_RUNTIME_MATCH",
        "FREE_OR_INCLUDED_QUOTA_CLOUD_EXECUTION_WHEN_ACTUALLY_EXPOSED",
        "USER_WEB_MANUAL_ONLY_IF_SHARED_RUNTIME_CANNOT_PRESERVE_REQUIRED_NATIVE_OUTPUT",
        "CAPABILITY_HOLD",
    ]
    if routing.get("routing_order") != expected_order:
        fail("Cloud-Free default routing order drifted")
    if routing.get("role") != "ROUTING_BINDING_NOT_NEW_METHOD_SKILL_GATE_OR_FRAMEWORK":
        fail("routing binding role boundary drifted")
    truth = routing.get("execution_truth", {})
    if truth.get("validator_or_ci_pass") != "DOES_NOT_EQUAL_BROWSER_PASS_OR_DESIGN_PASS":
        fail("routing binding lost CI/browser/design truth separation")
    if not truth.get("real_readback_required"):
        fail("routing binding must require real readback")

    surfaces = pack.get("surfaces", {})
    expected = {"browser_image_lab", "browser_spatial_lab", "browser_technical_svg_lab"}
    if set(surfaces) != expected:
        fail(f"unexpected capability surface set: {set(surfaces)}")

    files: dict[str, str] = {}
    for name, spec in surfaces.items():
        p = ROOT / spec["path"]
        if not p.exists():
            fail(f"{name} path missing: {p}")
        files[name] = p.read_text(encoding="utf-8")
        if spec.get("class") != "SHARED_REPO_RUNTIME":
            fail(f"{name} must be SHARED_REPO_RUNTIME")
        if "AGENT_EXECUTABLE_WHEN_GITHUB_CONNECTOR_EXPOSED" != spec.get("source_mutation"):
            fail(f"{name} source mutation boundary missing")
        if "REAL_BROWSER_REQUIRED" != spec.get("runtime_readback"):
            fail(f"{name} runtime readback boundary missing")

    require(files["browser_image_lab"], ["<canvas", "exportPng", "exportJson", "brightness", "contrast", "saturation", "grayscale", "Before view"], "image lab")
    require(files["browser_spatial_lab"], ["<canvas", "Scene JSON", "Camera preset", "yaw", "pitch", "distance", "pointerdown", "cylinder", "wire", "grid"], "spatial lab")
    if "https://" in files["browser_spatial_lab"] or "http://" in files["browser_spatial_lab"] or "import " in files["browser_spatial_lab"]:
        fail("spatial lab must remain zero external runtime dependency")
    require(files["browser_technical_svg_lab"], ["id=\"CUT\"", "id=\"BLEED\"", "id=\"SAFE\"", "id=\"ARTWORK\"", "id=\"DIMENSIONS\"", "Export SVG", "VENDOR CONFIRM"], "technical SVG lab")

    studio = STUDIO.read_text(encoding="utf-8")
    require(studio, ["browser-design-workbench/workbench.html", "browser-image-lab/image-lab.html", "browser-spatial-lab/spatial-lab.html", "browser-technical-svg-lab/technical-svg-lab.html", "CAPABILITY HOLD REMAINS"], "Cloud-Free Studio")

    card = CARD.read_text(encoding="utf-8")
    require(card, [
        "Cloud-Free Studio Preflight",
        "AGENT_EXECUTABLE → CURRENT OLEANDER SKILL → SHARED_REPO_RUNTIME",
        "USER_WEB_MANUAL",
        "CAPABILITY_HOLD",
        "SOURCE READBACK / CI / VALIDATOR PASS ≠ BROWSER PASS ≠ DESIGN PASS",
    ], "Project Environment Card")
    if card.find("SHARED_REPO_RUNTIME") > card.find("USER_WEB_MANUAL"):
        fail("project card must prefer shared repo runtime before manual web tools")

    registry_surfaces = reg.get("surfaces", {})
    for key in ("oleander_browser_image_lab", "oleander_browser_spatial_lab", "oleander_browser_technical_svg_lab"):
        if registry_surfaces.get(key, {}).get("class") != "SHARED_REPO_RUNTIME":
            fail(f"registry missing shared surface {key}")

    print("CLOUD_FREE_CAPABILITY_VALIDATION_PASS")
    print("surfaces=3")
    print("routing_binding=ACTIVE")
    print("shared_runtime_precedes_manual_saas=PASS")
    print("spatial_external_dependencies=0")
    print("browser_pass=OPEN_NOT_CLAIMED")


if __name__ == "__main__":
    main()
