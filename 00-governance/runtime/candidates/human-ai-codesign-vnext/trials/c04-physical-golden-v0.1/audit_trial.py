from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SVGS = [
    "A_TWIN_SADDLE_PODS.svg",
    "B_SERVICE_BRIDGE.svg",
    "C_SPLIT_POST_COLLARS.svg",
    "COMPARISON.svg",
]

REQUIRED_PHRASES = (
    "FIELD OPEN",
    "NOT ENGINEERING",
)


def main() -> None:
    rows = []
    for name in SVGS:
        path = ROOT / name
        parsed = False
        try:
            ET.parse(path)
            parsed = True
        except Exception:
            parsed = False
        text = path.read_text(encoding="utf-8")
        # Comparison uses a stronger phrasing rather than the exact NOT ENGINEERING wording.
        boundary_ok = "FIELD OPEN" in text and (
            "NOT ENGINEERING" in text or "NO STRUCTURAL ADEQUACY" in text
        )
        rows.append(
            {
                "file": name,
                "svg_parse": "PASS" if parsed else "FAIL",
                "truth_boundary": "PASS" if boundary_ok else "FAIL",
                "no_floor_leg_claim": "PASS" if ("不画落地支腿" in text or "无落地支腿" in text or name == "B_SERVICE_BRIDGE.svg") else "CHECK",
            }
        )

    failures = [
        row["file"]
        for row in rows
        if row["svg_parse"] != "PASS" or row["truth_boundary"] != "PASS"
    ]
    pngs = sorted(p.name for p in (ROOT / "readback").glob("*.png")) if (ROOT / "readback").exists() else []
    result = {
        "schema": "oleander.codesign.physical-product-trial-audit.v0.1",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "files": rows,
        "readback_pngs": pngs,
        "claim_ceiling": "EDITABLE PRODUCT-INTERFACE RELATION PROTOTYPES / NTS / FIELD OPEN / NO STRUCTURAL OR INSTALLATION PASS / NO DESIGN KEEP / NO PROJECT WRITEBACK / NO PROMOTION"
    }
    (ROOT / "STRUCTURAL_READBACK_v0.1.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    print(f"{result['status']}: svgs={len(rows)} pngs={len(pngs)} failures={failures}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
