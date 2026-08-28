# PDF Page-Box Semantics Validation Evidence

Status: `PRACTICE_EVIDENCE / TRAINING_MODE / NO_PROMOTION`

## Knowledge read state

- Notion Current Root Authority = `OLEANDER｜设计知识库（Design）`.
- Knowledge lifecycle = `OLEANDER Knowledge Retrieval & Lifecycle｜知识库机制 v1.0`.
- Default retrieval stayed `CURRENT + DEFAULT`; no K06 / Legacy / chronology source was used as Current Authority.
- GitHub Current owner = `oleander-delivery-qc` for VALIDATION; `oleander-technical-drawing` remains `CANDIDATE_DRAFT`.
- Priority Queue current object is owned by PRESENTATION, so this run did not enter Project Current.

## GAP

A PDF can look physically sized correctly while lacking explicit `TrimBox` / `BleedBox` metadata. A validator that reads only effective page-box values from a PDF consumer may silently accept fallback values and overstate prepress readiness.

## External Current sources / version check

1. Adobe Acrobat desktop, page-box documentation, updated December 2025: `TrimBox` is the final page size after trimming; `BleedBox` is the region outside the trim used for professional printing. Source: https://helpx.adobe.com/de/acrobat/desktop/edit-documents/organize-pages/crop-pages.html
2. Ghostscript 10.08.0 Vector Devices documentation: PDF/X requires Trim/Art page-box entries; `BleedBox` identifies the area to which output may extend and contains the `TrimBox`. Source: https://ghostscript.readthedocs.io/en/latest/VectorDevices.html
3. Poppler official release index confirms `25.06.0` release dated 2025-06-03. Source: https://poppler.freedesktop.org/releases.html
4. MuPDF official releases page states the open-source MuPDF line is AGPL with commercial licensing available. Source: https://mupdf.com/releases

External-source role: these sources define page-box semantics, current tool/version context and license boundary. They do **not** establish any supplier-specific bleed dimension or production approval.

## Rights / license boundary

- Adobe / Ghostscript documentation is cited as technical reference; no third-party code is copied.
- Poppler `pdfinfo` is used as an installed inspection tool only; this Practice does not redistribute Poppler binaries or source, and makes no new claim about Poppler redistribution rights.
- PyMuPDF / MuPDF is used only on the current execution surface to construct and reopen training fixtures. MuPDF's official release page identifies the open-source line as AGPL; this Practice neither embeds nor redistributes MuPDF as a deliverable.
- No external validator code is copied into OLEANDER; `validate_pdf_pageboxes.py` is a small OLEANDER wrapper around the installed inspection APIs/CLI.

## Required Native Output / Test Artifact

Reproducible validator: `validate_pdf_pageboxes.py`.

Fixture geometry is explicitly `EXERCISE ASSUMPTION / DESIGN TEST`:
- trim = `100 × 150 mm`;
- bleed offset = `3 mm`;
- these values are not claimed as an industry or supplier standard.

A = MediaBox-only PDF.
B = same physical outer page, but with explicit TrimBox and BleedBox entries.

Actual execution surface:
- Poppler `pdfinfo 25.06.0`;
- PyMuPDF `1.26.7` / MuPDF `1.26.12`.

## Actual readback

A raw page dictionary:
- `MediaBox` exists;
- `TrimBox` = absent;
- `BleedBox` = absent.

Yet `pdfinfo -box` reports effective `TrimBox` and `BleedBox` equal to the MediaBox. Therefore consumer-reported effective values alone do not prove explicit page-box metadata exists.

B raw page dictionary:
- explicit `TrimBox = [8.503937 8.503937 291.9685 433.70079]`;
- explicit `BleedBox = [0 0 300.47245 442.2047]`;
- reopen via `pdfinfo -box` reports the expected explicit trim relationship.

Local fixture hashes from the executed test:
- A SHA256 = `8be1ac8f9d6431fd239e4e59234ec13c55287fcff5b06f982ed8c7d9d82c0614`;
- B SHA256 = `573b2344d5e3adc402268e938dc87c0d0d185e39c8a572fb159ebfd5c4b7f7c1`.

## Verdict

A = `HOLD_FOR_PREPRESS_PAGE_BOX_AUTHORITY`.

B = `PASS_FOR_BOUNDED_PAGE_BOX_SEMANTICS`.

### PROVEN

- Correct-looking MediaBox/page size does not prove explicit TrimBox/BleedBox entries exist.
- `pdfinfo -box` may show effective fallback boxes for a MediaBox-only PDF.
- When a delivery requirement depends on explicit Trim/Bleed authority, validation must inspect the PDF page dictionary or an equivalent source that distinguishes explicit metadata from fallback semantics.

### NOT PROVEN

- PDF/X conformance;
- supplier-specific bleed requirement;
- crop-mark correctness;
- printer/RIP behavior;
- spot color / overprint / trapping;
- press approval.

## Transfer boundary

Candidate validation rule:

`PDF OPEN/PAGE SIZE PASS → PAGE-DICTIONARY BOX EXISTENCE → BOX RELATIONSHIP → CONSUMER READBACK → DELIVERY-SPEC COMPARISON`.

Do not promote this single training result to a universal Current Rule. KNOWLEDGE owns later Migration Closure / Relation Closure.
