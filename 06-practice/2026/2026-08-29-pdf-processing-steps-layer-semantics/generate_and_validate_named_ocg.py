from __future__ import annotations

import hashlib
import json
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent
PDF_PATH = ROOT / "A_named_cut_layer_only.pdf"
RESULT_PATH = ROOT / "readback.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_fixture() -> None:
    doc = fitz.open()
    page = doc.new_page(width=300, height=200)
    ocg_xref = doc.add_ocg("Cutting")
    shape = page.new_shape()
    shape.draw_line((30, 100), (270, 100))
    shape.finish(color=(1, 0, 0), width=1, oc=ocg_xref)
    shape.commit()
    page.insert_text(
        (30, 40),
        "EXERCISE ASSUMPTION / DESIGN TEST",
        fontsize=9,
    )
    doc.save(PDF_PATH)
    doc.close()


def inspect_fixture() -> dict:
    doc = fitz.open(PDF_PATH)
    ocgs = doc.get_ocgs()
    raw_ocgs = []
    for xref, info in ocgs.items():
        raw_ocgs.append(
            {
                "xref": xref,
                "info": info,
                "raw_object": doc.xref_object(xref, compressed=False),
            }
        )

    catalog_xref = doc.pdf_catalog()
    catalog_raw = doc.xref_object(catalog_xref, compressed=False)
    raw_pdf = PDF_PATH.read_bytes()
    result = {
        "runtime": {
            "pymupdf": fitz.VersionBind,
            "mupdf": fitz.VersionFitz,
        },
        "artifact": {
            "path": PDF_PATH.name,
            "sha256": sha256(PDF_PATH),
        },
        "reopen": {
            "ocg_count": len(ocgs),
            "ocgs": raw_ocgs,
            "catalog_raw": catalog_raw,
        },
        "bounded_checks": {
            "named_cutting_ocg_present": any(
                info.get("name") == "Cutting" for info in ocgs.values()
            ),
            "generic_ocg_roundtrip_proven": len(ocgs) == 1,
            "additional_processing_step_metadata_proven": False,
            "iso_19593_conformance_proven": False,
        },
        "raw_term_counts": {
            "ProcessingStep": raw_pdf.count(b"ProcessingStep"),
            "Structural": raw_pdf.count(b"Structural"),
            "Cutting": raw_pdf.count(b"Cutting"),
            "DPart": raw_pdf.count(b"DPart"),
            "GTS": raw_pdf.count(b"GTS"),
        },
        "verdict": "NOT_PROVEN_AS_ISO_19593_PROCESSING_STEPS",
        "boundary": (
            "A generic PDF OCG named 'Cutting' survives save/reopen. This does not "
            "establish ISO 19593 Processing Steps conformance. A PASS-capable retest "
            "requires an unmodified official compliant sample/test-suite or an ISO 19593 "
            "writer independently validated against a current conformance suite."
        ),
    }
    doc.close()
    return result


if __name__ == "__main__":
    build_fixture()
    result = inspect_fixture()
    RESULT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
