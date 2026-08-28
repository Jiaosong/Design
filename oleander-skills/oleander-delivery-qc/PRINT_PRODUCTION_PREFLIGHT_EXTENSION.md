# OLEANDER Print Production & Preflight Extension

Status: `CANDIDATE EXTENSION / VISUAL-DESIGN + DELIVERY-QC`

Use when a graphic, board, poster, brochure, packaging/POP item, booklet or other visual artifact is intended for commercial print or a named production process.

## Core distinction

`VISUALLY FINISHED ARTWORK ≠ PRINT-PRODUCTION MASTER ≠ PRESS-READY PDF ≠ PHYSICAL PROOF ≠ APPROVED PRINT RUN`.

Print readiness is specification-bound. Do not apply a generic bleed, color profile, PDF preset, ink limit, minimum rule weight or image-resolution threshold as if it were universal.

## Production specification first

Before declaring an artifact print-ready, resolve the current production specification when available:

- finished / trim dimensions and orientation;
- substrate / stock / surface and print method;
- printer/vendor specification and named PDF standard;
- bleed, safe/quiet area, trim/fold/cut/crease requirements;
- color space, ICC/output intent, spot-color and special-ink requirements;
- total area coverage / ink-limit requirements when relevant;
- transparency/flattening requirements;
- mark/page-box requirements;
- image-resolution expectations at final placed size/viewing condition;
- font/text policy;
- overprint/knockout policy;
- proof type and approval process;
- dieline / finishing / white ink / varnish / foil / emboss / cut layers where applicable.

If the printer/vendor spec is unavailable, retain `PENDING PRINTER CONFIRMATION` for affected production claims. A reasonable working assumption can support design development but cannot be silently upgraded to press approval.

## Master / derivative contract

Keep these roles explicit:

1. **Current editable design master** — authoritative live text/vector/image placement and visual system.
2. **Production master / prepress source** — may contain production layers, dielines, separations or finishing instructions while preserving traceability to the design master.
3. **Press-ready derivative** — exported PDF/X or other vendor-required format.
4. **Soft proof / raster proof** — visual evidence only within its color-management limits.
5. **Hard/contract proof** — physical process evidence when required.
6. **Printed run** — field/production result, not inferred from PDF validation.

Do not let a flattened press PDF become the only recoverable editable design source.

## Geometry / page-box checks

Verify against the named job specification:

- MediaBox / TrimBox / BleedBox / CropBox or equivalent page geometry where relevant;
- artwork actually extends through required bleed regions rather than being enlarged after layout;
- critical text/logos/dimensions remain inside required safe/quiet zones;
- folds, cuts, creases, perforations, glue zones and finishing layers use the correct authority and do not visually masquerade as final artwork;
- imposed marks are present only when the printer/workflow requires them.

`ARTWORK SCALED TO FAKE BLEED` is a production defect because it changes composition and effective resolution.

## Image / resolution checks

Judge raster resolution at **effective placed size**, not merely source-file metadata.

Record at minimum:

- source pixel dimensions;
- placed dimensions / scale;
- effective PPI/DPI at final output size;
- intended viewing distance/process requirement;
- any interpolation/upscaling performed and its limitation.

A source image labelled “300 DPI” can still be insufficient after enlargement. Conversely, large-format work may use a lower effective resolution when the actual viewing/process specification permits it.

## Color / separation checks

When production requires managed color, inspect:

- source and output color spaces;
- intended ICC/output profile;
- RGB/CMYK/spot object policy;
- spot-color naming and consistency;
- rich-black versus single-channel black usage according to printer/process requirements;
- total area coverage / ink-limit risk;
- overprint and knockout behavior, especially white/light objects and thin text/rules;
- transparency/blend interaction with separations;
- whether conversion changes material/product/brand color claims materially.

Do not use a generic CMYK build or profile when the printer/substrate/process specifies another condition.

## Font / vector / linework checks

- Preserve the editable type source and font provenance even when a production derivative embeds or outlines fonts.
- Verify font embedding/substitution status in the delivered file.
- Check minimum type/rule/detail limits against the actual printer/process specification.
- Verify fine vector lines, reversed text and registration-sensitive elements at target output scale.

`OUTLINED PRODUCTION TEXT ≠ EDITABLE TYPOGRAPHY MASTER`.

## PDF/X and export validation

When the printer requires PDF/X or another standard, verify the actual file rather than trusting an export-preset name:

- declared PDF/X conformance/version;
- output intent/profile;
- page boxes and bleed;
- fonts;
- image effective resolution;
- transparency/flattening state where required;
- spot colors/separations;
- overprint settings;
- missing links are already resolved upstream;
- no unintended RGB/Device-dependent objects when disallowed by the spec.

`EXPORT PRESET SELECTED ≠ PDF CONFORMANCE VERIFIED`.

## Proof class separation

Keep these separate:

`PDF STRUCTURE PASS ≠ SOFT-PROOF COLOR PASS ≠ HARD-PROOF PASS ≠ PRESS REGISTRATION PASS ≠ FULL RUN APPROVAL`.

For color-critical or finish-critical work, define the proof plan before final approval. A monitor preview cannot prove paper, ink, varnish, foil, emboss, substrate texture, registration or drying behavior.

## Packaging / POP boundary

When dielines or finishing geometry exist:

- use the Current technical/dieline authority rather than redrawing it for layout convenience;
- keep cut/fold/crease/finish layers separable and named;
- do not distort locked dielines to improve visual composition;
- route dimensional/manufacturing approval to Technical Drawing / vendor / engineering authority as appropriate;
- require a physical/sample proof when the production risk justifies it.

## Preflight record

Return or persist:

- job/printer/process specification and unresolved items;
- Current editable design master identity;
- production-master and press-derivative identities;
- trim/bleed/safe/page-box findings;
- effective-resolution findings at placed size;
- color profile/output-intent/separation findings;
- overprint/knockout/TAC findings when relevant;
- font/vector/detail findings;
- actual PDF/preflight checks executed;
- soft/hard proof status;
- printer-confirmation / production HOLD items;
- final status for each proof class.

## Candidate boundary

This extension improves print-production preparation and QC. It does not replace the printer's current specification, a prepress operator, a contract proof, packaging engineering or physical production approval.