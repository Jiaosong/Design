# C04 CH16 v1.2 — OLEANDER Design Review / Repair Note

## State
`REPAIR CANDIDATE / PRODUCER-EXECUTED / INDEPENDENT EXTERNAL DESIGN GATE STILL PENDING`

## Authority preserved
- Current CH16 base authoring = 7 pages, P01–P07.
- R06 experience remains FROZEN / NO REOPEN.
- No new platform, route, railing, node, surveyed terrain, exact field geometry, structural capacity or safety claim is introduced.
- `1200 × 160 × 975 mm` is shown only as `DESIGNER ESTIMATE / CONCEPT INTERFACE / NTS / FIELD OPEN`.

## Skills / methods applied
1. `oleander-story-and-board`: one claim + one dominant technical field per page; evidence/notes subordinate.
2. `oleander-data-viz`: source/presentation separation; vector geometry and semantic component IDs.
3. Technical Drawing Current Method (NOT installed / NOT promoted): line hierarchy, spatial translation, parent-child detail registration.
4. Detail Callout Registration: P03 parent `CH16-P03-SEC-A` → P05 child `D01`, repeated orientation and anchors, no geometry drift.
5. Delivery QC: SVG parse/render + 1920×1080 readback completed. v1.2 headless Chromium browser attempt timed out in the container (D-Bus/zygote); browser PASS is therefore **HOLD**, and v1.1 browser evidence is not inherited as v1.2 proof.

## v1.2 repairs
- Corrected C05 from misleading “field-verified existing substrate” to `EXISTING BASE / FIELD VERIFY REQUIRED`.
- P02 is explicitly relational and cannot be mistaken for a surveyed/site plan.
- P03 uses structural line hierarchy: primary body/path/interface before dimensions/notes.
- P04 uses material roles rather than invented brand-color/material-name claims.
- P05 registers D01 to the parent view and keeps side/orientation/component order stable.
- P06 binds water/slip/maintenance open items to C01–C05 instead of generic risk cards.
- P07 attaches the Open Register to the actual parent/interface and states the next professional input.

## Gate
Artifact existence / clean render / responsive source do not equal professional MAIN KEEP. This package must remain a candidate until an independent reviewer inspects the finished pages.

Truth: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.
