from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ALTERNATIVES = {
    "A_RETURN_RAIL": ROOT / "A_RETURN_RAIL.html",
    "B_CONTEXT_BEACON": ROOT / "B_CONTEXT_BEACON.html",
    "C_RETURN_MODE": ROOT / "C_RETURN_MODE.html",
}

REQUIRED_TEXT = (
    "UNKNOWN / 未确认",
    "data-status=\"UNKNOWN\"",
    "data-no-live-claim",
    "data-digital-off-fallback",
)

FORBIDDEN = (
    "实时开放：正常",
    "当前安全",
    "已验证安全",
    "FIELD VALIDATED",
    "13/13 完成",
)


def main() -> None:
    results = []
    for name, path in ALTERNATIVES.items():
        text = path.read_text(encoding="utf-8")
        missing = [item for item in REQUIRED_TEXT if item not in text]
        forbidden_hits = [item for item in FORBIDDEN if item in text]
        mechanism_specific_marker = name.split("_", 1)[1].replace("_", " ") in text
        results.append(
            {
                "id": name,
                "editable_html_exists": path.exists(),
                "required_boundary_missing": missing,
                "forbidden_claim_hits": forbidden_hits,
                "mechanism_specific_marker": mechanism_specific_marker,
                "status": "PASS" if not missing and not forbidden_hits and mechanism_specific_marker else "FAIL",
            }
        )

    hard_failures = [r["id"] for r in results if r["status"] != "PASS"]
    screenshot_dir = ROOT / "readback"
    screenshots = sorted(p.name for p in screenshot_dir.glob("*.png")) if screenshot_dir.exists() else []
    output = {
        "schema": "oleander.codesign.digital-hcd-trial-audit.v0.1",
        "status": "PASS" if not hard_failures else "FAIL",
        "hard_failures": hard_failures,
        "alternatives": results,
        "browser_screenshots_present": screenshots,
        "claim_ceiling": "LOCAL_BROWSER_AND_STRUCTURE_READBACK_ONLY / NO USER VALIDATION / NO PROFESSIONAL HCD PASS / NO PROJECT WRITEBACK / NO PROMOTION",
    }
    (ROOT / "STRUCTURAL_READBACK_v0.1.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"{output['status']}: alternatives={len(results)} screenshots={len(screenshots)}")
    if hard_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
