# 2026-08-17｜Wayfinding / Environmental Information｜Decision Priority Before Graphic Equality

Status: **CANDIDATE / POST-REVIEW PASS FOR PRACTICE**

## Problem
At a real movement decision point, giving every destination, arrow, status and explanatory layer equal visual weight slows first-read and can bury the highest-priority action.

## Learning object
Otl Aicher and collaborators, Munich 1972 visual communication / pictogram system. HfG-Archiv / Museum Ulm preserves Aicher's estate and records that he was appointed design commissioner for the Munich Olympics in 1968; its archive notes that the pictograms developed from 1968 rapidly became an international image-sign system. MoMA holds multiple München 1972 works by Aicher in Architecture and Design.

## Visible Facts
- The Munich 1972 system uses a disciplined family of arrows, pictograms, typography and color rather than independently styled signs.
- Directional arrows and image signs are visually compact enough to be read before long explanatory text.
- The system is applied across a large event environment, so consistency must survive many destinations and services.

## Design Inference
Wayfinding is not a catalogue layout. At a decision point, the graphic hierarchy should follow the visitor's decision priority and movement urgency. Consistency is necessary, but equal weight is not.

## Candidate Transfer Rule
`DECISION PRIORITY -> GRAPHIC PRIORITY`

For OLEANDER wayfinding, first-read order should reflect the project's actual experience hierarchy. For C04 this means that Service / Return and route safety can outrank optional interpretation. Optional content remains visible but cannot compete with the action required to keep the journey legible and safe.

## Technique
1. Keep the information set fixed.
2. Identify the primary movement decision.
3. Give its arrow + destination the largest combined mass and shortest reading path.
4. Group secondary route / observation choices below or beside it with lower weight.
5. Keep optional interpretation visible but tertiary.
6. Preserve states and truth boundaries; do not use hierarchy to hide CLOSED / UNKNOWN / safety information.

## Parameters / Conditions
- Exercise canvas: 1600x1000 SVG.
- Variable under test: visual hierarchy only.
- Content held constant: Return, R06 observation, Thirteen Imprints reading, state/support text.
- CJK font verified in runtime: Noto Sans CJK SC.
- No C04 site distance, direction, geometry or opening-state fact is asserted.

## A/B Result
### Before
Three destination bands use near-equal arrow, title and supporting-text weight. At distance read, no single movement action dominates.

### After
`RETURN` becomes the primary sign event; `R06 / observation` is secondary; optional Thirteen Imprints reading is tertiary. At distance read, the primary action is identifiable substantially earlier while all original information remains available at near read.

## Failure / Revision Evidence
The first render failed visual readback because the default font stack did not render Chinese glyphs, producing missing-glyph boxes. This is a **POST-REVIEW FAIL** even though SVG export succeeded. The files were revised to use a verified `Noto Sans CJK SC` runtime font and re-rendered before retaining the result.

## Counterexample
A very large arrow or RETURN label is not automatically correct. If project authority says another action is more urgent at that exact decision point, or CLOSED / UNKNOWN / hazard information must override normal routing, the hierarchy must change. Visual dominance must follow actual decision priority, not a reusable visual preset.

## Transfer Boundary
- Does not copy Munich 1972 colors, pictograms, typography or trade dress.
- Does not convert C04 into an Olympic-style sign system.
- Does not invent site directions or measured distances.
- Does not allow schematic simplicity to hide safety, accessibility, degraded-state or field-open information.

## OLEANDER Application Mapping
Immediate candidate: C04 Qingjiang physical/digital wayfinding and Return layer.

C04 permanent design invariants require `REAL QINGJIANG FIRST`, `Landscape First`, physical/digital complementarity, optional Thirteen Imprints, credible body-space relations and an independent Return closure. The exercise therefore tests only priority mapping: `RETURN -> ROUTE / OBSERVATION -> OPTIONAL EXPLANATION` for a synthetic decision point.

## Verification
- Editable SVG produced: YES.
- Raster render produced: YES.
- First-read / distance read: EXECUTED.
- Detail / near-read: EXECUTED.
- Initial font failure detected and repaired: YES.
- Real C04 current asset application: NOT YET EXECUTED.

## Gates
- Evidence Gate: **PASS FOR LEARNING OBJECT**.
- Design Quality Gate: **POST-REVIEW PASS FOR PRACTICE / CANDIDATE**.
- C04 project Design PASS: **NOT CLAIMED**.

## Skill Reuse
No new reusable Skill is promoted. Existing `oleander-story-and-board` covers claim/hierarchy logic and `oleander-data-viz` covers deterministic editable output patterns; this remains a Visual Judgment / Wayfinding sub-rule until validated on a real OLEANDER project artifact.
