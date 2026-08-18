# 2026-08-18｜Data Viz / L5｜Small-Multiple Comparability

## Trigger
C04 CH02 / ENV-05 now uses summer / equinox / winter small multiples. Current source-bound relative solar means are `0.93 / 0.77 / 0.49`. Existing `oleander-data-viz` already protects source values, geometry authority, route-state semantics, and animated-frame scale stability, but its static visual binding lacked an explicit comparability gate for small multiples.

Recent training already covered Attention-State Composition, Shared Container Continuity, Exploration Motion Grammar, Same-source Paired View and World-Viewport Framing. This round therefore does not repeat hierarchy, motion, paired-view geometry, or route framing.

## Reused current methods
- `oleander-data-viz`
- `T-DATAVIZ-OLEANDER-001 / Chart Spec v0.2`
- `OLEANDER Artifact Review System v1.1`
- C04 CH02 current truth boundary and current ENV figure IDs

## Practice artifact
`OLEANDER_SMALL_MULTIPLE_COMPARABILITY_R01.svg` — 1920×1080 editable vector comparison board.

The left side intentionally demonstrates the failure: each seasonal value is locally normalized to a narrow panel-specific domain, causing all three marks to read near-full despite materially different values. The right side locks a shared `0.00–1.00` domain, identical baseline and mark geometry, with direct values and deltas.

Source-bound values only. No generated imagery. The artifact does not prove solar physics, site exposure, field conditions, or C04 ENV-05 Design PASS.

## Design Crit
Compliance gate: `PASS FOR TRAINING`.

Professional design gate: `KEEP FOR TRAINING` on frozen criteria, with independent-review provenance still `HOLD` because the current tool surface cannot prove a second human/model reviewer identity.

Checks:
- First visual: PASS — local-normalized similarity versus shared-scale decay reads before explanatory text.
- Composition: PASS — reject/keep halves are balanced and comparable.
- Proportion: PASS — right-side mark lengths are source-consistent on one 0–1 domain.
- Hierarchy: PASS — title → comparison condition → marks → metadata.
- Typography: PASS — vector text remains readable in the 1920×1080 preview.
- Material/spatial realism: N/A; this is a data-visualization exercise, not spatial evidence.
- Scale: PASS for analytical scale semantics; target physical display scale remains outside this artifact.
- Node readability: N/A.
- Interaction/narrative: PASS for static compare-before/after narrative; no runtime interaction claimed.
- Professional finish: KEEP FOR TRAINING; not a C04 MAIN asset.

## Failure knowledge
1. Local auto-normalization is not neutral layout polish. It can invert the perceived magnitude relationship.
2. Writing exact numbers under misleading marks does not repair the visual lie; if the comparison becomes truthful only after reading numbers, the encoding has failed.
3. Shared color alone is insufficient. Domain, baseline, mark geometry, unit and legend semantics must also be locked.
4. Missing/HOLD panels must not disappear if omission makes the set appear complete.

## Skill delta
Modified existing `oleander-data-viz/VISUAL_LAYER_BINDING.md`; no new Skill created.

Added `Small-multiple comparability gate`:
- lock shared domain for same question + same unit by default;
- forbid undisclosed local normalization;
- require explicit disclosure when different scale is analytically necessary;
- lock panel/plot geometry where it encodes comparison;
- keep HOLD/UNKNOWN slots explicit;
- require target-size + 50% comparability readback;
- add hard failures and promotion test.

Promotion test: `If the comparison only becomes truthful after reading the numbers, the small-multiple visual encoding has failed.`

## Cross-project transfer
Applicable to C04 environmental/seasonal panels, route-state comparison, capacity scenarios, risk matrices, XJ01 CMF/performance comparisons, product dashboards, research charts, board small multiples and motion keyframe summaries.

Do not apply mechanically when panels intentionally use different units/questions, logarithmic domains are analytically necessary, normalized shape comparison is the explicit analytical task, or the purpose is within-panel pattern reading rather than magnitude comparison. In those cases the scale difference must be explicit and the composition must not imply one-to-one magnitude equivalence.

## Truth boundary
`TRAINING ONLY / SOURCE-BOUND VALUES / NO IMAGE GENERATION / FIELD OBSERVED=0 / FIELD MEASURED=0 / NO C04 PROMOTION`.
