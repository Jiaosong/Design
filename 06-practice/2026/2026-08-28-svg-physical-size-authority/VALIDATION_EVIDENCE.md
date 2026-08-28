# SVG Physical-Size Authority Validation

Status: PRACTICE_EVIDENCE / TRAINING_MODE / NO_PROJECT_MUTATION / NO_PROMOTION

## GAP
Current validation already covers DXF unit semantics and STL external unit contracts, but SVG technical/vector delivery still has a distinct physical-size risk: a valid `viewBox` and matching numeric width/height can reopen/render correctly while failing to carry the intended millimetre print size.

## TEST / SOURCE
Two matched SVG fixtures use the same geometry and `viewBox="0 0 120 60"`.

- A: `width="120" height="60"` (unitless CSS length; effectively px in normal SVG/CSS interpretation).
- B: `width="120mm" height="60mm"` (explicit physical unit).

Validation surface used CairoSVG 2.8.2 to produce PDF and pypdf to reopen/read the PDF MediaBox. Local capability probe also found Chromium available, but the deterministic SVG→PDF readback was sufficient for this bounded physical-size test.

## ARTIFACT / READBACK
Local executed readback:

- A unitless → PDF MediaBox `90 × 45 pt` = `31.75 × 15.875 mm` → `HOLD_PHYSICAL_SIZE_AUTHORITY_NOT_EXPLICIT`.
- B explicit mm → PDF MediaBox `340.15748 × 170.07874 pt` = approximately `120 × 60 mm` → `PASS_FOR_BOUNDED_PHYSICAL_SIZE_SEMANTICS`.

Both fixtures retain the same 120×60 viewBox geometry. Therefore numeric geometry agreement alone does not establish physical print size.

## FAILURE / ROOT CAUSE
Failure mode: treating SVG `viewBox`, or unitless `width/height`, as a millimetre Dimension Authority. Unitless SVG/CSS lengths are not equivalent to explicit `mm` dimensions; downstream PDF/export size can be materially different while the artwork still looks geometrically correct on screen.

## REPAIR / RETEST
Repair: preserve the same geometry but make physical units explicit in the authoritative SVG (`120mm × 60mm`). Retest by converting to PDF and reopening the PDF page size; result returns approximately `120 × 60 mm`.

## PROVEN
- `viewBox` defines an internal coordinate system, not the intended millimetre print size by itself.
- Unitless numeric SVG width/height can produce a physically smaller PDF while retaining identical internal geometry.
- Explicit `mm` width/height can survive this bounded SVG→PDF readback at the intended physical size.

## NOT PROVEN
- printer/plotter driver scaling;
- vendor RIP interpretation;
- bleed, trim, safe-zone or dieline compliance;
- PDF/X conformance, output intent or spot-color semantics;
- stroke scaling policy under arbitrary downstream editing;
- engineering/manufacturing approval.

## TRANSFER RULE
`SVG GEOMETRY / VIEWBOX PASS ≠ PHYSICAL DIMENSION PASS.` For size-authoritative technical, packaging or print SVG, require explicit physical units or an equivalent authoritative output contract, then verify the downstream PDF/print derivative by reopened physical page size.

## MATURITY
`PRACTICE_EVIDENCE`. A materially different downstream consumer or real source-authoritative project drawing is required before claiming broader cross-context validation.
