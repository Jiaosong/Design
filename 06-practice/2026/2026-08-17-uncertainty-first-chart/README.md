# OLEANDER Training — Uncertainty-first Scenario Chart

Training ID: `OLEANDER-TRN-2026-08-17-UFC`

Status: **PRACTICE / SELF-CHECKED TRAINING CANDIDATE / INDEPENDENT DESIGN VERDICT OPEN / NO_PROMOTION**

## Why this training exists

Recent OLEANDER projects require remote/provisional design values to advance as `recommended value + reasonable range + basis + sensitivity + FIELD correction item`. The current `oleander-data-viz` skill covered reproducibility, axes, labels, export and source integrity, but did not explicitly prevent provisional estimates from being presented as precise scalar bars or large numerals.

This practice isolates that gap. It does not create a new chart Skill.

## Internal evidence / reused system

- Reused the existing `oleander-data-viz` workflow rather than creating a new chart skill.
- Preserved OLEANDER truth-state separation: source-grounded / inferred / assumption and FIELD OPEN.
- Preserved editable SVG + CSV source and explicit export dimensions.

## External calibration

- UK Office for National Statistics, `Showing uncertainty in charts`: uncertainty ranges are used as design calibration when uncertainty materially changes interpretation.
- Government Analysis Function, `Communicating quality, uncertainty and change`: uncertainty and quality limitations should be visible and explained in context.

These references are calibration provenance only. This Practice does **not** claim that the synthetic ranges are statistical confidence intervals or that the external sources define OLEANDER project truth states.

## Practice data boundary

The four walking-time segments are synthetic calibration data. They are **not C04 project evidence** and must not be copied into a project dataset as factual values.

Fields:

- `recommended_min`
- `low_min`
- `high_min`
- `evidence`
- `confidence`

The row labels `SOURCE-GROUNDED / INFERRED / ASSUMPTION` are synthetic example classes used to test visual semantics. `SOURCE-GROUNDED` inside this specimen does not mean that the row is grounded in a real C04 source.

## Iteration

### v1 — producer REVISE

The first generated board already contrasted a single-value bar chart with a range-first chart, but visual self-check exposed two defects:

1. the right-axis unit label collided with the terminal `50` tick;
2. evidence class existed only as small text, so it was weak at first-read scale.

### v2 — self-checked training candidate

Repairs:

- separated the unit label from the terminal tick;
- made evidence class visible with symbol + line style;
- explicitly stated that line style encodes evidence provenance, not probability;
- kept plausible range as the dominant mark and the recommended value as a subordinate point.

The repository contains the editable SVG and CSV, but this PR does not contain an independent reviewer verdict. Therefore v2 is **not** `KEEP / Professional Design PASS`; it remains `SELF-CHECKED TRAINING CANDIDATE / INDEPENDENT REVIEW REQUIRED`.

## Transfer rule

`RECOMMENDED VALUE != MEASURED VALUE`

When uncertainty could change a comparison or design decision, the chart should show the range rather than let a recommendation masquerade as a measured scalar. Evidence class, confidence/quality, unit and FIELD correction state remain adjacent to the visual rather than being relegated to a distant note.

## Does not prove

- independent Design KEEP;
- field measurement;
- statistical confidence interval;
- engineering capacity verification;
- C04 route-time evidence;
- promotion of an assumption or synthetic example class into source-grounded project fact.
