from __future__ import annotations

import hashlib
import json
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent
A_PATH = ROOT / "A_generic_ocg.pdf"
B_PATH = ROOT / "B_processing_metadata.pdf"
RESULT_PATH = ROOT / "readback.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_fixture(path: Path, with_test_metadata: bool) -> None:
    doc = fitz.open()
    page = doc.new_page(width=300, height=200)
    ocg_xref = doc.add_ocg("Test Processing Step")
    shape = page.new_shape()
    shape.draw_line((30, 100), (270, 100))
    shape.finish(color=(1, 0, 0), width=1, oc=ocg_xref)
    shape.commit()
    page.insert_text((30, 40), "EXERCISE ASSUMPTION / DESIGN TEST", fontsize=9)

    if with_test_metadata:
        # TEST FIXTURE ONLY. Field names are informed by a public third-party
        # implementation example. This is not a normative ISO writer and does
        # not establish ISO 19593 conformance.
        doc.xref_set_key(
            ocg_xref,
            "GTS_Metadata",
            "<</GTS_ProcStepsType/Cutting/GTS_ProcStepsGroup/Structural>>",
        )

    doc.save(path)
    doc.close()


def inspect_fixture(path: Path) -> dict:
    doc = fitz.open(path)
    ocgs = doc.get_ocgs()
    rows = []
    for xref, info in ocgs.items():
        raw = doc.xref_object(xref, compressed=False)
        rows.append(
            {
                "xref": xref,
                "info": info,
                "raw_object": raw,
                "has_GTS_Metadata": "/GTS_Metadata" in raw,
                "has_type_cutting": "/GTS_ProcStepsType /Cutting" in raw,
                "has_group_structural": "/GTS_ProcStepsGroup /Structural" in raw,
            }
        )
    catalog_raw = doc.xref_object(doc.pdf_catalog(), compressed=False)
    doc.close()
    return {
        "sha256": sha256(path),
        "ocg_count": len(ocgs),
        "ocgs": rows,
        "catalog_has_OCProperties": "/OCProperties" in catalog_raw,
    }


if __name__ == "__main__":
    build_fixture(A_PATH, False)
    build_fixture(B_PATH, True)
    result = {
        "runtime": {"pymupdf": fitz.VersionBind, "mupdf": fitz.VersionFitz},
        "fixture_note": (
            "B metadata field names are a bounded TEST FIXTURE informed by a public "
            "third-party implementation example; not normative ISO syntax proof."
        ),
        "A_generic_ocg": inspect_fixture(A_PATH),
        "B_metadata_ocg": inspect_fixture(B_PATH),
    }
    result["assertions"] = {
        "A_has_generic_ocg": result["A_generic_ocg"]["ocg_count"] == 1,
        "A_has_no_gts_metadata": not result["A_generic_ocg"]["ocgs"][0]["has_GTS_Metadata"],
        "B_gts_metadata_survives_reopen": result["B_metadata_ocg"]["ocgs"][0]["has_GTS_Metadata"],
        "B_cutting_and_structural_terms_survive": (
            result["B_metadata_ocg"]["ocgs"][0]["has_type_cutting"]
            and result["B_metadata_ocg"]["ocgs"][0]["has_group_structural"]
        ),
        "iso_19593_conformance_proven": False,
        "gwg_suite_pass_proven": False,
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
