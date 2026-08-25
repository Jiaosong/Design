# XJ01 PRO-04.2｜OLEANDER Actual Preview Design Crit

Date: 2026-08-18
Scope: desktop only — 1920×1080 primary, 1440×900 secondary
Mode: CANDIDATE
Decision Question: without section labels, does first-read move from direction → material evidence → interface / environment / lifecycle evidence, rather than title/card/status chrome?

## Authority / review basis
- OLEANDER Artifact Review System v1.1 — Gate 1 Compliance + Gate 2 Professional Design
- OLEANDER Project Control Plane v0.3 — Machine / Visual / Project QA split
- Editorial / Portfolio L5 — page role must change dominant mass, density, whitespace and reading time
- Web UI L5 — earned attention; supporting chrome must recede
- XJ01 Professional CMF Standard — Hero cannot substitute visual evidence

## Gate 1｜Compliance / Machine
- Latest compact-matrix candidate head reviewed: `36cb5747948f970dcc83084982f93c9c0eada06d`.
- AI Governance Evals: PASS for the reviewed candidate.
- Website Quality / e1-static: PASS.
- XJ01 Chromium desktop tests: PASS, including editorial binding, 1920/1440 actual-preview capture, no horizontal overflow, and VE06/VE07 evidence-matrix semantics.
- Repository-wide E2 remains RED because of unrelated non-XJ01 Firefox / Daylily accessibility failures. These are not counted as XJ01 desktop failures.

Final actual-preview run: `32107817739` (Website Quality #136)
Artifact: `9313824606` / `xj01-viewport-review`
Artifact SHA256: `4d7b616c3ae2bd0cd1fba79dd490716fb211ab4f81759de9fef3bc4e4c141654`

## Gate 2｜Professional Design — Actual Preview

### P00｜Hero — KEEP
Claim: two retained CMF territories share one product architecture.
Why KEEP:
- Product presence and D02/D03 comparison are visible within the first viewport.
- Internal status chips were removed after Deletion Test; review chrome no longer competes with the product proposition.
- Black render fields are constrained inside two product windows rather than dominating the whole page.
Warning: source renders remain review-grade; source-resolution / render-artifact caution remains.

### P01｜Direction DNA — KEEP
Previous state: REVISE.
Previous root cause: direction copy was bottom-aligned, creating two large empty colour fields before semantic content.
Revision: direction card content moved to the top / first-read zone.
Why KEEP:
- D02 and D03 names, perceptual promises, material behaviour and risks enter the same first viewport as the product pair.
- The directions read as two CMF territories rather than hue-only A/B swatches.
- Page role is editorial/comparative rather than a repeated report template.

### P02｜Colour × Material × Geometry — KEEP
Why KEEP:
- D02/D03 material review imagery precedes swatches and supporting text.
- Colour is read on product geometry/material rather than as detached palette decoration.
- Evidence-first hierarchy survived the later revisions without regression.
Warning: review-grade source-resolution boundary remains.

### P03｜Where materials meet — KEEP
Previous state: REVISE.
Previous root cause: the dominant field was an operation/sleeve image while the page claim concerned material interfaces.
Revision: matched D02/D03 material-interface views became the dominant field; operation moved to secondary context.
Why KEEP:
- Dominant visual corresponds to the decision question.
- D02/D03 adjacency can be compared before reading the operation-context panel.
- Operation remains available without outranking interface evidence.
Warning: retained mid views are not supplier-grade macro/interface photography.

### P04｜Reflection Environment Adaptation — KEEP EVIDENCE
Previous states: HOLD / SUPPORT → REVISE → KEEP EVIDENCE.
Root-cause chain:
1. retained VE06 frames were not durably Web-bound;
2. first binary binding produced a corrupted/black JPEG and failed AR-G07 Open & Integrity;
3. verified WebP derivative was created with local Git-blob SHA = GitHub blob SHA;
4. first correct visual binding still showed only the upper D02 row in the first viewport;
5. page scale/rhythm was compacted and explicit row/column keys were added.
Final actual-preview result:
- complete 2×3 matrix is visible in the 1920×1080 first viewport;
- D02 / TOP and D03 / BOTTOM are simultaneously visible;
- Neutral Studio / Soft Interior / Wet-zone columns are explicit and aligned;
- interpretation stays secondary to the matrix;
- no physical colour/process approval is implied.
Decision: KEEP as digital environment evidence, not Hero imagery.

### P05｜Lifecycle — KEEP EVIDENCE / SOURCE-RESOLUTION CAUTION
Previous states: HOLD / SUPPORT → REVISE → KEEP EVIDENCE.
Root-cause chain:
1. retained VE07 frames were not durably Web-bound;
2. first JPEG binding was visibly corrupted/tearing and failed AR-G07;
3. verified WebP derivative was created with local Git-blob SHA = GitHub blob SHA;
4. row/column semantics and full-matrix first-read were then repaired.
Final actual-preview result:
- complete 2×3 matrix is visible in the 1440×900 first viewport;
- D02 / TOP and D03 / BOTTOM are simultaneously visible;
- Day 0 / Dirty-wiped / PU Aged columns are explicit;
- risk ownership is readable beside the matrix;
- lifecycle visual differences remain deliberately subtle and scope-bounded as O/H-D2 relative-risk evidence.
Caution:
- current WebP is a review derivative and does not support publication/supplier-review image-quality claims;
- Dirty-wiped / PU-aged constructions do not predict real material ageing.
Decision: KEEP as internal digital evidence; not a primary brand-publication image.

### P06｜Evidence Appendix — KEEP SUPPORT
- Boundary is explicit and subordinate to the design story.
- Physical samples / interaction remain OUT_OF_SCOPE by current project decision.
- Not promoted as a primary portfolio scene.

## Current Design State
- P00 Hero: KEEP
- P01 Direction DNA: KEEP
- P02 CMF System: KEEP
- P03 Interfaces: KEEP
- P04 Environment: KEEP EVIDENCE
- P05 Lifecycle: KEEP EVIDENCE / SOURCE-RESOLUTION CAUTION
- P06 Appendix: KEEP SUPPORT
- XJ01 desktop Machine Gate: PASS
- XJ01 Professional Design Gate: PASS FOR INTERNAL DIGITAL CMF PRESENTATION
- Presentation readiness: `PRESENTATION_READY_INTERNAL`
- Public / publication readiness: `FALSE / NOT_PUBLIC_RELEASE`
- Winner: NONE
- Physical validation: OUT_OF_SCOPE

## Remaining boundary — not an internal presentation blocker
- source-resolution upgrade remains required for publication/supplier-review image quality;
- no physical / measured production colour / supplier process / engineering approval claims;
- D02 and D03 remain retained without a winner.

## Final verdict
`OLEANDER COMPLIANCE PASS + PROFESSIONAL DESIGN PASS → KEEP FOR INTERNAL DIGITAL CMF PRESENTATION`

This verdict does not promote the project to public release, production approval, physical validation or engineering handoff.
