# XJ01 PRO-04.2｜OLEANDER Actual Preview Design Crit

Date: 2026-08-18
Scope: desktop only — 1920×1080 primary, 1440×900 secondary
Mode: CANDIDATE
Decision Question: without section labels, does first-read move from direction → material evidence → interface evidence, rather than title/card/status chrome?

## Authority / review basis
- OLEANDER Artifact Review System v1.1 — Gate 1 Compliance + Gate 2 Professional Design
- OLEANDER Project Control Plane v0.3 — Machine / Visual / Project QA split
- Editorial / Portfolio L5 — page role must change dominant mass, density, whitespace and reading time
- Web UI L5 — earned attention; supporting chrome must recede
- XJ01 Professional CMF Standard — Hero cannot substitute visual evidence

## Gate 1｜Compliance / Machine
- AI Governance Evals #1858: PASS
- Website Quality #122 / e1-static: PASS
- XJ01 Chromium desktop tests in e2-browser: PASS
- XJ01 1920/1440 actual-preview capture: PASS
- XJ01 horizontal overflow: PASS after P00 hero min-size root-cause fix
- Repository-wide E2 remains RED because of a non-XJ01 Daylily chromium-mobile colour-contrast failure. Mobile is outside the current XJ01 review scope and is not counted as an XJ01 failure.

Run: 32104838712
Artifact: 9312831782
Artifact SHA256: bf2b96c57784691fe81cb23908326df2437f7c1f25e731fdcabd230fea0c9adb

## Gate 2｜Professional Design — Actual Preview

### P00｜Hero — KEEP
Claim: two retained CMF territories share one product architecture.
Why KEEP:
- Product presence and D02/D03 comparison are visible within the first viewport.
- Internal status chips were removed after Deletion Test; review chrome no longer competes with the product proposition.
- Black render fields are constrained inside two product windows rather than dominating the whole page.
Warning: source renders remain review-grade; minor source-resolution / render-artifact caution remains.

### P01｜Direction DNA — KEEP
Previous state: REVISE.
Previous root cause: direction copy was bottom-aligned, creating two large empty colour fields before semantic content.
Revision: direction card content moved to the top/first-read zone.
Why KEEP:
- D02 and D03 names, perceptual promises, material behaviour and risks now enter the same first viewport as the product pair.
- The directions read as two CMF territories rather than hue-only A/B swatches.
- Page role is recognizably editorial/comparative rather than a repeated report template.

### P02｜Colour × Material × Geometry — KEEP
Why KEEP:
- D02/D03 material review imagery precedes swatches and supporting text.
- Colour is read on product geometry/material rather than as detached palette decoration.
- Evidence-first hierarchy survived the latest revision without regression.
Warning: review-grade source-resolution boundary remains.

### P03｜Where materials meet — KEEP
Previous state: REVISE.
Previous root cause: the dominant field was an operation/sleeve image while the page claim concerned material interfaces.
Revision: matched D02/D03 material-interface views became the dominant field; operation moved to secondary context.
Why KEEP:
- Dominant visual now corresponds to the decision question.
- D02/D03 adjacency can be compared before reading the operation-context panel.
- Operation remains available without outranking interface evidence.
Warning: the current retained mid views are not supplier-grade macro/interface photography; close diagnostic evidence remains a lower-level review asset.

### P04｜Reflection Environment Adaptation — HOLD / SUPPORT
Root cause: retained VE06 image frames are not yet durably bound into the Web asset set.
Status:
- Text summary and evidence states are valid.
- It must not be promoted as visual proof or MAIN while the actual retained VE06 frames are absent from durable Web binding.
- This is an Evidence binding HOLD, not a design failure of the VE06 study itself.

### P05｜Lifecycle — HOLD / SUPPORT
Root cause: retained VE07 visual frames are not yet durably bound into the Web asset set.
Status:
- Relative-risk narrative is valid and scope-bounded.
- Historical 06D proxy stays collapsed/diagnostic and cannot substitute for retained VE07 review frames.
- No physical ageing prediction is claimed.

### P06｜Evidence Appendix — KEEP SUPPORT
- Boundary is explicit and subordinate to the design story.
- Physical samples / interaction remain OUT_OF_SCOPE by current project decision.
- Not promoted as a primary portfolio scene.

## Current Design State
- Core MAIN presentation spine P00–P03: KEEP
- P04 Environment: HOLD / SUPPORT
- P05 Lifecycle: HOLD / SUPPORT
- P06 Appendix: KEEP SUPPORT
- XJ01 desktop Machine Gate: PASS
- XJ01 core Professional Design Gate: PASS FOR P00–P03
- Overall PRO-04.2 Presentation Ready: FALSE
- Winner: NONE
- Physical validation: OUT_OF_SCOPE

## Remaining blocker
`VE06 / VE07 retained visual frames → durable Web asset binding → actual-preview recheck`

Source-resolution caution remains non-blocking for internal design review but blocks any claim of publication/supplier-review image quality.
