# 2026-08-18｜VI Manual / L5｜Optical Asset Handoff

## Training question
How should a VI manual represent the transition between Primary / Mark / Optical / Micro assets so that minimum-size rules remain visually truthful rather than becoming isolated numbers?

## Real project trigger
C04 CH14-P03 v7.0 is currently rebuilding the Stone Seal VI Manual. Its current public rule states `Primary 180px / Mark 48px current minimum`, while `Micro 24–32px` remains Candidate. The page correctly stops treating minimum size as prose-only, but the reusable Skill did not yet require the transition logic between those carriers to be shown or tested.

Recent OLEANDER training already covered Same-source Paired View, World-Viewport Framing, Small-Multiple Comparability, Exploration Motion Grammar, Cross-Screen Family Grammar, Experience↔Technical Proof Co-registration, and Prompt↔Media Semantic Binding. This round therefore avoids those topics and focuses on optical identity continuity across asset switches.

## Existing Skill reused
- `oleander-story-and-board/SKILL.md`
- `oleander-story-and-board/VI_MANUAL_PRODUCTION_EXTENSION.md`

Existing rule retained: `Text rule ≠ visual specification.` Existing minimum-size gate already requires concrete threshold specimens and below-threshold/failure samples.

## Gap found
The old rule could still allow a manual to show several correct minimum-size numbers without explaining **which carrier must replace which carrier at the transition**. A correct numeric threshold can therefore coexist with an operationally wrong identity system.

## Actual exercise
Editable 1920×1080 SVG: `OLEANDER_VI_OPTICAL_ASSET_HANDOFF_R01.svg`.

The plate compares:
- REJECT: one Primary bilingual lockup scaled continuously to 180 / 64 / 48 / 32 px;
- KEEP: an explicit `Primary → Mark → Optical → Micro Candidate` handoff ladder;
- current C04 values are used only as project-triggered labels: Primary 180px, Mark 48px, Micro 24–32px Candidate;
- the mark drawn in the exercise is a synthetic proxy and has no Stone Seal geometry authority.

No image generation was used. All text remains live SVG text.

## Actual pixel readback and repair
First rendered readback failed for design reasons even though export succeeded:
1. the Primary specimen overflowed its card and clipped the bilingual line;
2. the Handoff 2 / Micro status labels collided.

Repair:
- reduced the Primary proxy scale within the specimen card;
- separated handoff labels and shortened the Micro HOLD label;
- re-rendered the final PNG and reopened it.

This confirms again: `SVG/export success ≠ finished-pixel design success`.

## Design Crit
### Execution / compliance gate
PASS FOR TRAINING EXECUTION.
- editable vector source exists;
- no generated image is used;
- current C04 thresholds are labeled as current decisions/candidate status, not physical proof;
- proxy mark is explicitly non-authoritative.

### Producer frozen-criteria design finding
KEEP-FOR-TRAINING CANDIDATE after repair.
- First visual: REJECT vs KEEP is immediately legible.
- Composition: two large comparison fields, no dashboard-like equal micro-panels.
- Proportion: large Primary → smaller Mark/Optical/Micro reads as a scale system.
- Hierarchy: title → comparison logic → specimens → handoff labels → promotion test.
- Typography: Chinese and English render cleanly after final readback.
- Material/spatial realism: not applicable beyond truthful flat identity representation.
- Scale: digital pixel thresholds are shown as project decisions; physical millimetre proof remains OPEN.
- Node/readability: each handoff point and candidate state is legible.
- Interaction/narrative: static sequence is sufficient; no runtime behavior is claimed.
- Professional finish: training-level KEEP candidate; not a C04 production asset.

### Independent Professional Design Gate
HOLD / REVIEW REQUIRED.
No reviewer identity independent from the producer is available in the current tool surface. Producer readback is not promoted into an independent KEEP.

## Failure knowledge
- Minimum size is not a single scalar when multiple identity carriers exist.
- `Correct number ≠ correct carrier`.
- Shrinking Primary below its legibility range while keeping the numeric label correct is still a design failure.
- Enlarging a 32px or 48px specimen for a manual screenshot hides native-pixel failure.
- A smaller optical variant may simplify detail, but cannot silently invent a new silhouette or negative-space grammar.
- Candidate Micro/Favicon cannot be visually presented as approved merely because it occupies the smallest slot in the ladder.

## Skill delta
Added `oleander-skills/oleander-story-and-board/VI_OPTICAL_ASSET_HANDOFF_GATE.md` as an active subroutine of the existing VI Manual production capability. No new Skill owner or Brand Identity framework was created.

New required fields: `FROM_ASSET / TO_ASSET / SWITCHPOINT / UNIT / RECOGNITION_INVARIANTS / DETAILS_ALLOWED_TO_EXIT / BACKGROUND-CONTRAST / STATUS / DOES_NOT_PROVE`.

New attack tests: `NATIVE_PIXEL / ONE_STEP_BELOW / HANDOFF_PAIR / GRAY-MONO / LIGHT-DARK / DENSE_CONTEXT / PRINT_PROOF_HOLD`.

Promotion test: `A minimum-size page is incomplete unless it also shows the asset handoff that preserves recognition on both sides of the threshold.`

## Cross-project transfer
Applicable to:
- C04 Stone Seal and future Brand Manual pages;
- mobile/web app marks, service icons and favicons;
- product-brand lockups and packaging marks;
- signage/wayfinding identity families;
- exhibition graphics and small-format print;
- any OLEANDER identity system with responsive/optical asset variants.

Not directly applicable when:
- only one single-scale identity asset exists;
- a platform mandates a different official app icon asset with separate authority;
- physical emboss/print minimums have not yet been proofed: keep those thresholds provisional;
- a genuinely different sub-brand is being compared rather than an optical variant of the same identity.

## Project truth boundary
`TRAINING ONLY / NO IMAGE GENERATION / C04 STONE SEAL GEOMETRY UNCHANGED / PHYSICAL PROOF OPEN / FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION`.
