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
IMAGE_RECEIPT = RUNTIME / "validation" / "2026-08-26-image-lab-baojiajie" / "VALIDATION_RECEIPT_v0.1.json"
SPATIAL_RECEIPT = RUNTIME / "validation" / "2026-08-26-spatial-lab-timer" / "VALIDATION_RECEIPT_v0.1.json"
WORKBENCH_RECEIPT = RUNTIME / "validation" / "2026-08-26-design-workbench-c04" / "VALIDATION_RECEIPT_v0.1.json"
WORKBENCH_RESULTS = RUNTIME / "validation" / "2026-08-26-design-workbench-c04" / "BROWSER_TEST_RESULTS_v0.2.json"


def fail(msg: str) -> None:
    raise SystemExit(f"CLOUD_FREE_CAPABILITY_VALIDATION_FAIL: {msg}")


def require(text: str, tokens: list[str], label: str) -> None:
    missing = [t for t in tokens if t not in text]
    if missing:
        fail(f"{label} missing tokens: {missing}")


def main() -> None:
    required_files = [PACK, REGISTRY, ROUTING, CARD, STUDIO, IMAGE_RECEIPT, SPATIAL_RECEIPT, WORKBENCH_RECEIPT, WORKBENCH_RESULTS]
    if any(not p.exists() for p in required_files):
        fail("pack / registry / routing / project card / studio / validation receipt or result missing")

    pack = json.loads(PACK.read_text(encoding="utf-8"))
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    routing = json.loads(ROUTING.read_text(encoding="utf-8"))
    image_receipt = json.loads(IMAGE_RECEIPT.read_text(encoding="utf-8"))
    spatial_receipt = json.loads(SPATIAL_RECEIPT.read_text(encoding="utf-8"))
    workbench_receipt = json.loads(WORKBENCH_RECEIPT.read_text(encoding="utf-8"))
    workbench_results = json.loads(WORKBENCH_RESULTS.read_text(encoding="utf-8"))

    if pack.get("status") != "CANDIDATE_SHARED_REPO_RUNTIME":
        fail("capability pack must remain candidate until independent review and promotion evidence exist")
    if pack.get("routing_binding") != "00-governance/runtime/OLEANDER_CLOUD_FREE_EXECUTION_ROUTING_BINDING_v0.1.json":
        fail("capability pack is not bound to current Cloud-Free execution routing")
    rb = pack.get("readback_state_2026_08_26", {})
    if rb.get("browser_pass") != "OPEN_NOT_CLAIMED":
        fail("whole-pack browser PASS must remain open")

    required_holds = {
        "NEW_PROFESSIONAL_BIM_CAD", "CLASS_A_MANUFACTURING_CAD",
        "FROM_ZERO_HIGH_END_ARCHVIZ_CGI", "SUPPLIER_PREPRESS_PROOF",
        "ENGINEERING_APPROVAL", "FIELD_ACCEPTANCE",
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
    truth = routing.get("execution_truth", {})
    if truth.get("validator_or_ci_pass") != "DOES_NOT_EQUAL_BROWSER_PASS_OR_DESIGN_PASS":
        fail("routing binding lost CI/browser/design truth separation")
    if not truth.get("real_readback_required"):
        fail("routing binding must require real readback")

    surfaces = pack.get("surfaces", {})
    expected = {"browser_design_workbench", "browser_image_lab", "browser_spatial_lab", "browser_technical_svg_lab"}
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
        if spec.get("source_mutation") != "AGENT_EXECUTABLE_WHEN_GITHUB_CONNECTOR_EXPOSED":
            fail(f"{name} source mutation boundary missing")
        if spec.get("runtime_readback") != "REAL_BROWSER_REQUIRED":
            fail(f"{name} runtime readback boundary missing")

    workbench_spec = surfaces["browser_design_workbench"]
    if workbench_spec.get("validation_state") != "FUNCTIONAL_BROWSER_READBACK_PASS_PERSISTENCE_REMOTE_READBACK_PASS_INDEPENDENT_REVIEW_OPEN":
        fail("design workbench validation state drifted or was prematurely promoted")
    if workbench_spec.get("validation_receipt") != "00-governance/runtime/validation/2026-08-26-design-workbench-c04/VALIDATION_RECEIPT_v0.1.json":
        fail("design workbench validation receipt pointer missing")
    if workbench_spec.get("full_project_readback") != "C04_FINISHED_PIXEL_BLOCKED_BY_PR353_ASSET_BINDING":
        fail("design workbench must preserve current C04 finished-pixel blocker")
    require(files["browser_design_workbench"], [
        "<iframe", "id=\"projectFrame\"", "data-w=\"390\" data-h=\"844\"",
        "--viewport-width", "--viewport-height", "loadHTML", "loadURL",
        "PREVIEW ZOOM ONLY", "URL BLOCKED / HTTP(S) REQUIRED",
        "OUTLINE BLOCKED / CROSS-ORIGIN OR NON-INSPECTABLE",
    ], "design workbench")
    if "--frame-width" in files["browser_design_workbench"] or "id=\"design-root\"" in files["browser_design_workbench"]:
        fail("design workbench regressed to same-document false viewport mechanism")
    if workbench_receipt.get("status") != "FUNCTIONAL_BROWSER_READBACK_PASS_PERSISTENCE_REMOTE_READBACK_PASS_INDEPENDENT_REVIEW_OPEN":
        fail("design workbench receipt status invalid")
    wb_review = workbench_receipt.get("review", {})
    if wb_review.get("independent_professional_design_review") != "OPEN" or wb_review.get("active_promotion") != "NOT_GRANTED":
        fail("design workbench cannot self-grant independent review or ACTIVE promotion")
    if wb_review.get("full_c04_finished_pixel_review") != "BLOCKED_BY_CURRENT_ASSET_BINDING":
        fail("design workbench receipt lost C04 asset-binding blocker")
    if workbench_receipt.get("persistent_readback", {}).get("library_folder") != "/Oleander/90_Archive/Runtime-Validation/2026-08-26/Design-Workbench":
        fail("design workbench persistent readback location drifted")
    if workbench_receipt.get("project_binding", {}).get("source_css_blob_sha") != "6841f1241dddaed7a84f0c46e0bccabdb358f312":
        fail("design workbench C04 responsive source identity drifted")
    if workbench_results.get("page_errors") != []:
        fail("design workbench browser test has page errors")
    cases = workbench_results.get("viewport_cases", [])
    if [c.get("inner") for c in cases] != [1440, 1024, 768, 390]:
        fail("design workbench iframe inner viewport matrix invalid")
    if len(cases) != 4 or cases[0].get("nav") != "flex" or cases[1].get("nav") != "none" or cases[2].get("nav") != "none" or cases[3].get("nav") != "none":
        fail("design workbench C04 responsive nav contract failed")
    if cases[3].get("cols") != "354px" or cases[2].get("cols") != "732px":
        fail("design workbench mobile/tablet single-column contract failed")
    if workbench_results.get("zoom_invariant", {}).get("inner") != 390:
        fail("design workbench preview zoom changed project viewport")
    if workbench_results.get("grid", {}).get("pixel_surface_changed") is not True:
        fail("design workbench grid diagnostic has no pixel readback evidence")
    if workbench_results.get("grayscale", {}).get("filter") != "grayscale(1)":
        fail("design workbench grayscale diagnostic failed")
    if workbench_results.get("outline", {}).get("stylePresent") is not True:
        fail("design workbench srcdoc outline diagnostic failed")
    if workbench_results.get("invalid_url_return") is not False:
        fail("design workbench invalid URL protocol did not fail closed")

    image_spec = surfaces["browser_image_lab"]
    if image_spec.get("validation_state") != "FUNCTIONAL_BROWSER_READBACK_PASS_PERSISTENCE_REMOTE_READBACK_PASS_INDEPENDENT_REVIEW_OPEN":
        fail("image lab validation state drifted or was prematurely promoted")
    if image_spec.get("validation_receipt") != "00-governance/runtime/validation/2026-08-26-image-lab-baojiajie/VALIDATION_RECEIPT_v0.1.json":
        fail("image lab validation receipt pointer missing")
    require(files["browser_image_lab"], [
        "<canvas", "Export PNG derivative", "Export Config JSON",
        "Before view · true source fit", "SOURCE_BYTES_READ_ONLY",
        "sha256", "IMAGE MIME REQUIRED / SOURCE CLEARED",
        "EXPORT BLOCKED / SOURCE REQUIRED", "DERIVATIVE_NOT_SOURCE_AUTHORITY",
    ], "image lab")
    if image_receipt.get("status") != "FUNCTIONAL_BROWSER_READBACK_PASS_PERSISTENCE_REMOTE_READBACK_PASS_INDEPENDENT_REVIEW_OPEN":
        fail("image validation receipt status invalid")
    if image_receipt.get("review", {}).get("independent_design_review") != "OPEN":
        fail("image lab cannot self-grant independent review")
    if image_receipt.get("persistent_readback", {}).get("library_folder") != "/Oleander/90_Archive/Runtime-Validation/2026-08-26/Image-Lab":
        fail("image lab persistent readback location drifted")
    if image_receipt.get("project_binding", {}).get("source_sha256") != "e1d7fde5f7ac18b0a49b140e53d7dde95ee0e7295af56a3f0feb506bf3bc34b4":
        fail("image lab source identity drifted")

    spatial_spec = surfaces["browser_spatial_lab"]
    if spatial_spec.get("validation_state") != "FUNCTIONAL_BROWSER_READBACK_PASS_PERSISTENCE_REMOTE_READBACK_PASS_INDEPENDENT_REVIEW_OPEN":
        fail("spatial lab validation state drifted or was prematurely promoted")
    if spatial_spec.get("validation_receipt") != "00-governance/runtime/validation/2026-08-26-spatial-lab-timer/VALIDATION_RECEIPT_v0.1.json":
        fail("spatial lab validation receipt pointer missing")
    require(files["browser_spatial_lab"], [
        "<canvas", "oleander.spatial-proxy-scene.v0.2", "PROXY_DERIVED",
        "PROXY_ONLY_NOT_SOURCE_GEOMETRY", "ORTHOGRAPHIC_PROPORTION_READBACK",
        "PERSPECTIVE_CAMERA_READBACK", "geometryEquivalent=false",
        "units must be one of mm / cm / m", "type unsupported",
        "SCENE DIRTY / VALIDATE + APPLY REQUIRED / EXPORT BLOCKED",
        "EXPORT BLOCKED / VALIDATE + APPLY CURRENT SCENE FIRST",
        "Export Valid Scene JSON", "Fit Scene", "pointerdown",
    ], "spatial lab")
    if "https://" in files["browser_spatial_lab"] or "http://" in files["browser_spatial_lab"] or "import " in files["browser_spatial_lab"]:
        fail("spatial lab must remain zero external runtime dependency")
    if spatial_receipt.get("status") != "FUNCTIONAL_BROWSER_READBACK_PASS_PERSISTENCE_REMOTE_READBACK_PASS_INDEPENDENT_REVIEW_OPEN":
        fail("spatial validation receipt status invalid")
    if spatial_receipt.get("review", {}).get("independent_design_review") != "OPEN":
        fail("spatial lab cannot self-grant independent review")
    if spatial_receipt.get("project_binding", {}).get("canonical_glb_sha256") != "900e02510ab6b2b5176aa3723dba7981700dc79b5f217dbe481844a534ed7c66":
        fail("spatial lab canonical source identity drifted")
    proxy = spatial_receipt.get("proxy_derivation", {})
    if proxy.get("geometry_equivalent") is not False or proxy.get("all_proxy_bounds_match_source_aabb") is not True:
        fail("spatial proxy truth/derivation boundary invalid")
    if spatial_receipt.get("persistent_readback", {}).get("library_folder") != "/Oleander/90_Archive/Runtime-Validation/2026-08-26/Spatial-Lab":
        fail("spatial lab persistent readback location drifted")
    bt = spatial_receipt.get("browser_tests", {})
    if bt.get("front_orthographic_depth_invariance") != "PASS":
        fail("spatial lab orthographic depth-invariance evidence missing")
    if bt.get("invalid_json_export_blocked") != "PASS" or bt.get("dirty_scene_export_blocked") != "PASS":
        fail("spatial lab fail-closed export evidence missing")

    require(files["browser_technical_svg_lab"], ["id=\"CUT\"", "id=\"BLEED\"", "id=\"SAFE\"", "id=\"ARTWORK\"", "id=\"DIMENSIONS\"", "Export SVG", "VENDOR CONFIRM"], "technical SVG lab")

    studio = STUDIO.read_text(encoding="utf-8")
    require(studio, ["browser-design-workbench/workbench.html", "browser-image-lab/image-lab.html", "browser-spatial-lab/spatial-lab.html", "browser-technical-svg-lab/technical-svg-lab.html", "CAPABILITY HOLD REMAINS"], "Cloud-Free Studio")

    card = CARD.read_text(encoding="utf-8")
    require(card, ["Cloud-Free Studio Preflight", "AGENT_EXECUTABLE → CURRENT OLEANDER SKILL → SHARED_REPO_RUNTIME", "USER_WEB_MANUAL", "CAPABILITY_HOLD", "SOURCE READBACK / CI / VALIDATOR PASS ≠ BROWSER PASS ≠ DESIGN PASS"], "Project Environment Card")
    if card.find("SHARED_REPO_RUNTIME") > card.find("USER_WEB_MANUAL"):
        fail("project card must prefer shared repo runtime before manual web tools")

    registry_surfaces = reg.get("surfaces", {})
    for key in ("oleander_browser_design_workbench", "oleander_browser_image_lab", "oleander_browser_spatial_lab", "oleander_browser_technical_svg_lab"):
        if registry_surfaces.get(key, {}).get("class") != "SHARED_REPO_RUNTIME":
            fail(f"registry missing shared surface {key}")
    wb_reg = registry_surfaces.get("oleander_browser_design_workbench", {})
    if wb_reg.get("role") != "REAL_RESPONSIVE_IFRAME_READBACK_SHELL" or wb_reg.get("project_source_mutation") is not False:
        fail("design workbench registry role/source-mutation boundary invalid")

    print("CLOUD_FREE_CAPABILITY_VALIDATION_PASS")
    print("surfaces=4")
    print("design_workbench_functional_browser_readback=PASS")
    print("design_workbench_persistence_remote_readback=PASS")
    print("design_workbench_full_c04_finished_pixel=BLOCKED_BY_PR353_ASSET_BINDING")
    print("design_workbench_independent_review=OPEN")
    print("image_lab_functional_browser_readback=PASS")
    print("image_lab_persistence_remote_readback=PASS")
    print("image_lab_independent_review=OPEN")
    print("spatial_lab_functional_browser_readback=PASS")
    print("spatial_lab_persistence_remote_readback=PASS")
    print("spatial_lab_independent_review=OPEN")
    print("spatial_external_dependencies=0")
    print("browser_pass=OPEN_NOT_CLAIMED")


if __name__ == "__main__":
    main()
