#!/usr/bin/env python3
import hashlib, json, pathlib, subprocess, fitz

MM = 72 / 25.4
OUT = pathlib.Path(__file__).resolve().parent / "out"
OUT.mkdir(exist_ok=True)
TRIM_W_MM, TRIM_H_MM = 100, 150
BLEED_MM = 3  # EXERCISE ASSUMPTION / DESIGN TEST, not a supplier or industry standard.

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def make_pdf(path, explicit_boxes):
    tw, th, b = TRIM_W_MM * MM, TRIM_H_MM * MM, BLEED_MM * MM
    mw, mh = tw + 2*b, th + 2*b
    doc = fitz.open()
    page = doc.new_page(width=mw, height=mh)
    page.insert_text((20, 30), "B EXPLICIT TRIM + BLEED" if explicit_boxes else "A MEDIA ONLY")
    if explicit_boxes:
        doc.xref_set_key(page.xref, "TrimBox", f"[{b} {b} {b+tw} {b+th}]")
        doc.xref_set_key(page.xref, "BleedBox", f"[0 0 {mw} {mh}]")
    doc.save(path)
    doc.close()

def inspect(path):
    doc = fitz.open(path)
    page = doc[0]
    keys = set(doc.xref_get_keys(page.xref))
    raw = {k: doc.xref_get_key(page.xref, k) for k in ("MediaBox", "TrimBox", "BleedBox")}
    doc.close()
    p = subprocess.run(["pdfinfo", "-box", str(path)], capture_output=True, text=True, check=True)
    return {
        "artifact": path.name,
        "sha256": sha256(path),
        "explicit_TrimBox": "TrimBox" in keys,
        "explicit_BleedBox": "BleedBox" in keys,
        "raw": raw,
        "pdfinfo": p.stdout,
    }

a = OUT / "A_media_only.pdf"
b = OUT / "B_explicit_boxes.pdf"
make_pdf(a, False)
make_pdf(b, True)
A, B = inspect(a), inspect(b)
assert A["explicit_TrimBox"] is False and A["explicit_BleedBox"] is False
assert B["explicit_TrimBox"] is True and B["explicit_BleedBox"] is True

result = {
    "schema_version": "1.0",
    "mode": "TRAINING_MODE",
    "gap": "PDF page-box semantics: explicit TrimBox/BleedBox vs MediaBox-only fallback",
    "exercise_assumption": {"trim_mm": [100, 150], "bleed_mm": 3},
    "A": A,
    "B": B,
    "verdict": {
        "A": "HOLD_FOR_PREPRESS_PAGE_BOX_AUTHORITY",
        "B": "PASS_FOR_BOUNDED_PAGE_BOX_SEMANTICS",
        "transfer_rule": "Effective page-box values reported by a consumer do not prove explicit TrimBox/BleedBox metadata exists; inspect the PDF page dictionary when the delivery contract requires explicit page-box authority.",
        "not_proven": ["PDF/X conformance", "supplier bleed requirement", "printer/RIP behavior", "crop marks", "spot colors/overprint/trapping", "press approval"]
    }
}
(OUT / "validation_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
