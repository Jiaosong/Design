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

## Optical construction of the smaller carrier

`MECHANICAL SCALE ≠ OPTICAL SCALE`.

When the smaller carrier is an optical variant rather than a mechanically scaled master, preserve the **identity skeleton** first:
- dominant silhouette;
- topology / principal part relation;
- distinctive negative space;
- primary directional gesture;
- locked wordmark/brand relationship when that relationship still belongs to the carrier.

At each actual target size, classify secondary details as:
`SURVIVES / CHATTERS / DISAPPEARS / MERGES`.

Only then allow bounded optical compensation such as:
- limited stroke-weight compensation;
- aperture/counter opening;
- focal-dot or critical terminal enlargement;
- spacing compensation;
- removal of nonessential secondary traces;
- simplified detail whose exit is already permitted by the handoff register.

Rules:
1. Do not restyle the mark merely to make a visibly different “small version”. Every optical change must answer a target-size failure.
2. Do not use blur, glow, extra contrast or added color to rescue structurally weak small geometry.
3. When monochrome support is part of the identity, the optical carrier must remain recognisable in mono/grayscale.
4. Review symbol and wordmark separately. A mark may survive at icon scale while a complete bilingual/signature lockup does not; do not force unreadable text into the smaller carrier.
5. Keep display/master and optical-small assets explicitly named and bounded. The simplified carrier must not silently replace the master at larger sizes.
6. Reopen both the native-size raster and an enlarged nearest-neighbour/pixel diagnostic. The diagnostic locates chatter; the native-size specimen decides recognition.
7. If optical compensation changes the identity silhouette enough to read as a different mark, REJECT unless the new silhouette is explicitly approved by Brand Authority.

Candidate optical sequence:
`IDENTITY SKELETON → TARGET PIXEL SIZE → SURVIVING DETAIL → OPTICAL COMPENSATION → NATIVE RASTER REOPEN → HANDOFF PAIR`.

## Required attack tests

Run all applicable tests on the actual exported assets, not only on enlarged vector diagrams:

- `NATIVE_PIXEL`: render at the actual claimed pixel size with no browser/CSS upscaling;
- `TARGET_MATRIX`: inspect every claimed operational size/range, not only one threshold specimen;
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
- a correct numeric threshold is used to excuse an illegible specimen;
- a mechanically scaled master is accepted despite visible chatter/merge/disappearance;
- optical compensation is decorative rather than failure-driven.

## Promotion test

`A minimum-size page is incomplete unless it also shows the asset handoff that preserves recognition on both sides of the threshold.`

`Correct number ≠ correct carrier.`

`Mechanical scale ≠ optical scale.`

## C04 training trigger / 2026-08-18

CH14-P03 v7.0 currently states `Primary 180px / Mark 48px current minimum`, with `Micro 24–32px` still Candidate. The existing VI manual production extension already requires minimum-size specimens, but it did not explicitly require a transition ladder or recognition-continuity test between Primary → Mark → Optical/Micro.

The earlier small-mark optical-size training lineage (PR #224) demonstrated that mechanically scaled 24/32 px carriers can chatter or become optically light while bounded optical compensation can preserve the identity skeleton. Its reusable rule is consolidated here; its training mark remains provenance only.

The training artifact `OLEANDER_VI_OPTICAL_ASSET_HANDOFF_R01.svg` uses a synthetic proxy mark only. It does not alter or replace C04 Stone Seal Geometry Authority.
