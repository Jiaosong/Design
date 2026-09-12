# OLEANDER VALIDATION EVIDENCE — PDF Font Embedding

Status: PRACTICE_EVIDENCE / TRAINING_MODE / NO_PROMOTION.

## GAP
A PDF can open and render text while still depending on an unembedded font. Export success or visual readback on the producer machine therefore does not prove portable print/view fidelity.

## EXTERNAL CURRENT BASIS
- Adobe Acrobat, updated 2025-09-23: font embedding includes font data in the PDF so the intended font is available for viewing/printing; embedding prevents substitution, subject to font vendor embedding permissions.
- Adobe Acrobat PDF settings, current 2025: font embedding is required for PDF/X compliance.
- Ghostscript current Vector Devices documentation: `EmbedAllFonts` behavior depends on input type and substitute-font handling; an export option is not sufficient proof of the resulting PDF font state.
- PDF Association: PDF/X core requirements include embedding all fonts; PDF/A validation similarly treats embedded fonts as a core condition except narrow non-rendered cases.

These sources prove why embedding state must be inspected. They do not prove this fixture is PDF/X, press-approved, rights-cleared for arbitrary third-party font distribution, or visually identical across every RIP/viewer.

## TOOL / VERSION / RIGHTS
Actual execution surface:
- Ghostscript `10.05.1` — used only to generate the deliberately unembedded fixture.
- Poppler `pdffonts 25.06.0` — used as the independent font-resource inspector.
- ReportLab `4.4.9` — used to generate the embedded TrueType subset fixture.
- Lato Medium from the execution environment — TRAINING fixture only; it is not a project font authority and is not committed as a font binary.

No font file is redistributed in this Practice evidence. Generator code references an environment path only. External documentation is linked/cited rather than copied.

## TEST DESIGN
Two PDFs contain the same test sentence:

A — `A_unembedded.pdf`: PostScript uses Helvetica, Ghostscript writes PDF with embedding disabled.
B — `B_embedded.pdf`: ReportLab registers Lato Medium and writes an embedded TrueType subset.

Validator: `validate_pdf_font_embedding.py` reopens both PDFs using `pdffonts`, parses each font resource, and requires A=`all_embedded=false`, B=`all_embedded=true`.

## ACTUAL READBACK
Observed locally:
- A: `Helvetica / Type 1 / embedded=no / subset=no`.
- B: `AAAAAA+Lato-Medium / TrueType / embedded=yes / subset=yes`.
- Validator exit = PASS for the fixture contract.

Local SHA256 at execution time:
- A PDF: `6940d058a4c1a715822dcdefa1848b44a242226c96479a857f1c5af9a6cbc7c6`
- B PDF: `a296ba24e00fddcf9edc4c757821875d7f8ded2191363afce241f1fcc78ff4bd`
- validator: `bd064f8e0788ce6f99af92ff2a1c2d840b7141c6472c81a14668da2218d44ff9`

The PDF binaries are not committed by this connector run; the reproducible generators, validator and readback are committed. Therefore GitHub persistence proves reproducibility/evidence text, not remote binary identity.

## ROOT CAUSE → REPAIR → RETEST
Root cause: relying on successful PDF generation or appearance on the producer system conflates rendering availability with embedded-font portability.

Repair rule: run a PDF font-resource inspector after export; if any required rendered font is not embedded, return REVISE/HOLD for print-portable delivery unless the authoritative delivery specification explicitly allows otherwise.

Retest: A correctly fails the embedding condition; B correctly passes the bounded embedding condition.

## PROVEN
- A PDF may render while a font resource remains unembedded.
- `pdffonts` can distinguish the fixture's unembedded versus embedded/subset font resources after reopening the actual PDFs.
- Export-parameter intent is weaker evidence than final-PDF resource readback.

## NOT PROVEN
- PDF/X conformance.
- PDF/A conformance.
- Output Intent / ICC correctness.
- font licensing beyond this bounded training use.
- glyph completeness for arbitrary CJK or variable fonts.
- RIP/printer behavior, trapping, overprint, transparency, bleed/trim, or press approval.
- Design Quality KEEP.

## TRANSFER RULE
`PDF EXPORT SUCCESS → REOPEN PDF → INSPECT FONT RESOURCES → EMBEDDED / SUBSET / UNEMBEDDED → DELIVERY SPEC COMPARISON → PASS|REVISE|HOLD`

Do not equate `looks correct here` with `font portable`. For PDF/X-oriented or vendor print workflows, font embedding is a technical delivery check; final conformance still requires the appropriate dedicated preflight/standard validator.

## MATURITY
`PRACTICE_EVIDENCE` only. Next material delta requires a materially different context: e.g. CJK/variable-font subset behavior, a dedicated PDF/X validator such as veraPDF/callas-equivalent where applicable, or a real project/vendor print requirement. Repeating Latin-font A/B generation is not new evidence.
