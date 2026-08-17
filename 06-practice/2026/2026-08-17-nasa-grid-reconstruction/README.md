# 2026-08-17 NASA Grid 5.14 Reconstruction Fidelity Calibration

## Learning object

NASA *Graphics Standards Manual* (NHB 1430.2, January 1976), p. 5.14 `The Grid—What it is`.

Primary source: NASA official PDF.

## Current OLEANDER rule

This practice is governed by `oleander-skills/REVIEW.md` → `Reference Reconstruction Fidelity Gate`.

A visually similar study is not a reproduction. Claimed reproduction requires:

`ORIGINAL → 1:1 RECONSTRUCTION → MATCHED COMPARISON / OVERLAY → REPAIR → METHOD EXTRACTION → TRANSFER`

## Actual execution

- Reconstructed the page at the matched 1048×1478 reference screenshot frame.
- Preserved the three-zone top band, narrow left instructional measure, fixed right-hand double-spread frame, red grid overlay and Step-3 blocked content demonstration.
- Used the PDF text layer for copy and line-break fidelity.
- Used editable SVG as the native output; rendered PNG for first-read and near-read review.

## Fidelity verdict

`HOLD / REFERENCE-BOUND RECONSTRUCTION`

Macro geometry, text measure, line breaks, diagram placement and instructional progression are closely matched, but the current execution surface does not expose the official NASA page screenshot/PDF page as local comparison bytes. Therefore overlay/flicker/pixel-difference verification could not be executed, and the result must not be called `REPRODUCTION PASS`.

## Failure / learning increment

`LOOKS CLOSE ≠ REPRODUCTION PASS`.

A future reconstruction round must check **source-byte comparability before production**. If the original cannot be retained in a form that supports matched overlay/difference, the round is labeled `REFERENCE-BOUND STUDY / FIDELITY HOLD` from the start and cannot supply Candidate-promotion evidence.

## Visible fact

The NASA page teaches the grid by keeping one spatial frame stable while adding one organizational layer at each step:

1. publication frame;
2. grid;
3. content blocked into the same grid.

## Transfer boundary

The transferable observation is `STABLE FRAME → ONE NEW ORGANIZATIONAL LAYER PER STEP`. The NASA page and this reconstruction remain study/calibration material and are not OLEANDER original authorship or public/commercial deliverables.

## Gates

- Evidence Gate: `PASS FOR SOURCE AUTHENTICITY / LEARNING OBJECT`
- Reconstruction Fidelity Gate: `HOLD`
- Design Quality Gate: `VISUALLY COHERENT STUDY / NOT REPRODUCTION PASS`
- Skill status: `OBSERVATION / FIDELITY-GATE CALIBRATION`

## Environment

- Web / official PDF: EXECUTED
- Editable SVG / CairoSVG: EXECUTED
- Reconstruction pixel readback: EXECUTED
- Source-byte overlay / pixel diff: PENDING / unavailable on this execution surface
- Figma: not used
- Blender: not applicable
