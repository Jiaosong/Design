# OLEANDER VI Optical Asset Handoff Gate

Status: ACTIVE SUBROUTINE / CHILD OF `oleander-story-and-board` VI MANUAL PRODUCTION / NO NEW SKILL OWNER

Use this gate when a VI manual defines more than one identity carrier across scale: Primary lockup, Compact, Mark-only, Optical Small, Micro, favicon, service mark, print/emboss variant, or equivalent.

This subroutine extends the existing `VI_MANUAL_PRODUCTION_EXTENSION.md`. It does not create a parallel Brand Identity method and does not change Brand Identity authority.

## Why this gate exists

A minimum-size number is not sufficient when the identity uses multiple assets. A manual can correctly say `Primary ≥ 180 px` and `Mark ≥ 48 px` while still failing operationally if it never shows when the user must stop scaling Primary and switch to Mark.

The design question is therefore not only `HOW SMALL?` but `WHICH ASSET AT THIS SCALE, AND WHAT RECOGNITION MUST SURVIVE THE SWITCH?`

## Required handoff ladder

For every scale-dependent identity family, show a visible ladder:

`LARGER CARRIER → HANDOFF POINT → SMALLER CARRIER → LIMIT / HOLD`

At each handoff, record:

- `FROM_ASSET`
- `TO_ASSET`
- `SWITCHPOINT`
- `UNIT`
- `RECOGNITION_INVARIANTS`
- `DETAILS_ALLOWED_TO_EXIT`
- `BACKGROUND / CONTRAST CONDITION`
- `STATUS = CURRENT / CANDIDATE / HOLD`
- `DOES_NOT_PROVE`

A handoff point may be a single threshold or a bounded overlap range. Do not invent a switchpoint merely to make the ladder look complete.

## Recognition continuity gate

The smaller asset may simplify detail, but it must preserve the identity relations that the current Brand Identity source treats as essential.

Before approval, compare the two assets side by side at the handoff and verify:

1. the mark remains identifiable as the same identity;
2. the primary negative-space relation survives;
3. no small carrier inherits wordmark, texture, linework, aperture, counter, stroke, or bilingual detail that no longer resolves;
4. the smaller carrier does not introduce a new silhouette merely for optical convenience unless that variant is explicitly authoritative;
5. a candidate micro asset remains visually marked as Candidate/HOLD until separately reviewed.

## Required attack tests

Run all applicable tests on the actual exported assets, not only on enlarged vector diagrams:

- `NATIVE_PIXEL`: render at the actual claimed pixel size with no browser/CSS upscaling;
- `ONE_STEP_BELOW`: show at least one below-threshold specimen;
- `HANDOFF_PAIR`: show the last valid larger carrier beside the first valid smaller carrier;
- `GRAY / MONO`: confirm recognition does not depend on decorative color separation;
- `LIGHT / DARK`: test approved background modes;
- `DENSE_CONTEXT`: test against realistic neighboring text/UI/image density when digital use is claimed;
- `PRINT_PROOF_HOLD`: keep physical millimetre thresholds provisional until real proof when print/emboss is involved.

## Invalid patterns

REVISE / REJECT when:

- one Primary lockup is simply scaled down through every size;
- the manual lists multiple minimum values but does not show the asset-switch rule;
- the 48 px/32 px specimen is displayed enlarged, hiding real native-pixel failure;
- the handoff changes silhouette or negative-space logic without authority;
- Micro/Favicon is visually presented as approved while its status is Candidate/HOLD;
- decorative texture survives into a carrier whose geometry no longer resolves;
- a correct numeric threshold is used to excuse an illegible specimen.

## Promotion test

`A minimum-size page is incomplete unless it also shows the asset handoff that preserves recognition on both sides of the threshold.`

`Correct number ≠ correct carrier.`

## C04 training trigger / 2026-08-18

CH14-P03 v7.0 currently states `Primary 180px / Mark 48px current minimum`, with `Micro 24–32px` still Candidate. The existing VI manual production extension already requires minimum-size specimens, but it did not explicitly require a transition ladder or recognition-continuity test between Primary → Mark → Optical/Micro.

The training artifact `OLEANDER_VI_OPTICAL_ASSET_HANDOFF_R01.svg` demonstrates the delta using a synthetic proxy mark only. It does not alter or replace C04 Stone Seal Geometry Authority.
