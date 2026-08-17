# Design Crit — OLEANDER-TRN-2026-08-17-UFC

## Engineering / execution gate

- Editable SVG source: PASS.
- CSV source table: PASS.
- 1600×1000 PNG independent render: PASS locally.
- Source/visual boundary: PASS — synthetic calibration data, not project evidence.
- GitHub branch write: PASS.

These do not determine design quality.

## Design Quality Gate

### v1

Verdict: `REVISE`

- First visual threshold: PASS — comparison intent is immediately visible.
- Composition: PASS — reject/keep comparison has a clear two-column read.
- Proportion: PASS.
- Hierarchy: REVISE — evidence provenance is too dependent on small secondary text.
- Typography: REVISE — `walking time / min` collides optically with the final `50` tick.
- Material/spatial realism: N/A.
- Scale: PASS for presentation-scale calibration; not a field scale claim.
- Node readability: N/A.
- Interaction/narrative: PASS — single-value failure → range-first correction → transfer rule.
- Professional finish: REVISE due to the axis collision and weak evidence-state first read.

### v2

Verdict: `KEEP / TRAINING ASSET`

- First visual threshold: PASS — the rejected scalar bars and accepted range-first construction are distinguishable without reading the body copy.
- Composition: PASS.
- Proportion: PASS.
- Hierarchy: PASS — range is primary, recommendation is subordinate, evidence state is visible beside each row.
- Typography: PASS — unit label is separated from terminal tick.
- Truth-state readability: PASS — source-grounded / inferred / assumption are visible and remain semantically separate from probability.
- Accessibility / grayscale hierarchy: PASS for the calibration use because symbol + line pattern do not rely on hue.
- Professional finish: KEEP for training/calibration, not for project evidence publication.

## Failure knowledge

1. `Text exists` is not equivalent to `truth-state is visually encoded`.
2. A clean bar chart can still be false precision if the input is provisional.
3. Styling evidence provenance with a visual channel is dangerous unless the legend states what the channel means; provenance must not be mistaken for likelihood.
4. If uncertainty is large enough to destroy a comparison, do not force ranking through chart polish.

## Reusable repair

`Plausible range → recommended point → evidence provenance → confidence/quality → FIELD correction state`

Use this order whenever a provisional estimate advances design but has not become a measured fact.
