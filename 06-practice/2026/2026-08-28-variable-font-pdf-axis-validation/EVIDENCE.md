# Variable Font → PDF Axis Validation

Status: `PRACTICE_EVIDENCE / NO_PROMOTION`  
Mode: `TRAINING_MODE`  
Verdict: `PASS_FOR_VISUAL_OUTPUT / HOLD_FOR_EDITABLE_VARIABLE_FONT_AUTHORITY`

## Gap
Previous PDF font-embedding validation proved embedded vs unembedded resources, but did not prove that a variable-font axis selection remains recoverable after browser PDF export.

## Current external basis
- Microsoft OpenType 1.9.1 Font Variations documentation: variable-font axes and ranges are defined in `fvar`; `STAT` participates in style/instance semantics.
- fontTools current `varLib.instancer`: pinning all axes produces a static instance and removes `fvar`.
- ReportLab current docs document ordinary TrueType embedding; they are not evidence that arbitrary OpenType variation-axis semantics survive PDF export.

These sources define the technical question; they do not predetermine the test result.

## Capability probe
Actual execution surface:
- Chromium PDF producer: `Skia/PDF m144`
- Poppler `pdffonts 25.06.0`
- fontTools `4.63.0`
- fixture: system `Cantarell-VF.otf`, `wght=100..800`, SIL OFL 1.1.

The font itself is not committed to this repository.

## Actual A/B
Same text, same viewport, same source variable font:
- A: CSS `font-variation-settings: "wght" 400`
- B: CSS `font-variation-settings: "wght" 700`

Browser readback confirmed distinct computed axis settings and different text widths (`511.921875 px` vs `526.40625 px`). Both pages were exported to PDF, reopened with Poppler and rasterized independently.

## Readback
Both PDFs:
- contain embedded subset Unicode font resources;
- extract the original text;
- are reported by `pdffonts` as `AAAAAA+Cantarell-Regular / Type 3`.

The two rasterized PDFs differ over `9832` pixels, so the selected weight materially survives as final visual output. However, the PDF font-resource identity does not expose the original `wght=400` versus `wght=700` coordinate.

## PROVEN
1. Chromium used materially different variable-font weight states before export.
2. The two exported PDFs preserve materially different glyph appearance.
3. Both output PDFs embed subset resources and preserve Unicode text extraction.
4. In this tested output path, font embedding alone does not preserve a recoverable variable-axis coordinate/authoring identity.

## NOT PROVEN
- recovery of original variable-font axes/coordinates from the PDF;
- roundtrip back to editable variable-font authoring;
- cross-browser equivalence;
- PDF/X/PDF/A conformance;
- RIP/press behavior or print approval.

## Transfer rule
`VARIABLE FONT VISUAL OUTPUT PASS ≠ EDITABLE VARIABLE FONT AUTHORITY PASS`.

When a delivery only requires fixed final pixels/vectors, a browser PDF can be visually valid after explicit readback. When downstream editing must preserve the font's axis identity, retain the authoritative variable-font source plus explicit axis coordinates outside the PDF, or use a workflow whose native format demonstrably preserves those semantics.

## Next material evidence
A valid next step is a materially different downstream consumer/authoring format that claims to preserve variable-font axes, followed by actual reopen/roundtrip. Repeating Chromium PDF with another weight alone is not a new training delta.
