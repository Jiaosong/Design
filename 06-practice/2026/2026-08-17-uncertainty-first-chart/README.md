# OLEANDER Training — Uncertainty-first Scenario Chart

Training ID: `OLEANDER-TRN-2026-08-17-UFC`

## Why this training exists

Recent OLEANDER projects require remote/provisional design values to advance as `recommended value + reasonable range + basis + sensitivity + FIELD correction item`. The current `oleander-data-viz` skill covered reproducibility, axes, labels, export and source integrity, but did not explicitly prevent provisional estimates from being presented as precise scalar bars or large numerals.

This practice isolates that gap. It does not reuse the immediately preceding technical-drawing hierarchy exercise.

## Internal evidence / reused system

- Reused the existing `oleander-data-viz` workflow rather than creating a new chart skill.
- Preserved OLEANDER truth-state separation: source-grounded / inferred / assumption and FIELD OPEN.
- Preserved editable SVG + CSV source and explicit export dimensions.

## External calibration

- UK Office for National Statistics, `Showing uncertainty in charts`: show ranges when uncertainty materially changes interpretation; range-oriented forms such as shaded bands or dot plots with ranges are preferred.
- Government Analysis Function, `Communicating quality, uncertainty and change`: uncertainty and quality limitations should be made visible and explained in context.

These references are used as design calibration, not as a claim that the synthetic practice data are statistical confidence intervals.

## Practice data boundary

The four walking-time segments are synthetic calibration data. They are **not C04 project evidence** and must not be copied into a project dataset as factual values.

Fields:

- `recommended_min`
- `low_min`
- `high_min`
- `evidence`
- `confidence`

## Iteration

### v1 — REVISE

The first generated board already contrasted a single-value bar chart with a range-first chart, but visual reopen exposed two defects:

1. the right-axis unit label collided with the terminal `50` tick;
2. evidence class existed only as small text, so it was weak at first-read scale.

### v2 — KEEP training asset

Repairs:

- separated the unit label from the terminal tick;
- made evidence class visible with symbol + line style;
- explicitly stated that line style encodes evidence provenance, not probability;
- kept plausible range as the dominant mark and the recommended value as a subordinate point.

## Transfer rule

`RECOMMENDED VALUE != MEASURED VALUE`

When uncertainty could change a comparison or design decision, the chart must show the range. Evidence class, confidence, unit and FIELD correction state stay adjacent to the visual instead of being relegated to a distant note.

## Does not prove

- no field measurement;
- no statistical confidence interval;
- no engineering capacity verification;
- no C04 route-time evidence;
- no promotion of an assumption into source-grounded fact.
