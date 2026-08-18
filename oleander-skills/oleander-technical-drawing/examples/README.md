# Technical Drawing Calibration Fixture

This example preserves the strongest current vector practice asset from `training/2026-08-17-technical-drawing-hierarchy` as a regression/calibration fixture for `oleander-technical-drawing`.

It is **not** a construction detail and must not be used as evidence that a real node is structurally resolved.

## What the fixture tests

- first-read section hierarchy;
- near-read node hierarchy;
- explicit leader targets;
- human scale as relative scale only;
- maintenance notation as support information;
- `NTS / FIELD OPEN / no construction claim` boundaries;
- technical text and annotation remaining native SVG vector elements.

## Reading order under test

`CUT / PRIMARY FORM → STRUCTURE / RELATION → EDGE / CONNECTION → DIMENSION / NOTE`

## Provenance

The fixture derives from the OLEANDER training asset `technical_drawing_hierarchy_calibration.svg` produced on 2026-08-17 after the C04/Qingjiang drawing reviews exposed equal-weight linework, weak node hierarchy, crowded callouts and insufficient distinction between scale evidence and construction evidence.

The earlier `practice/2026-08-16-technical-drawing-lineweight` experiment established the precursor rule that CAD/export defaults must not be mistaken for visual hierarchy. The later fixture added section/node/callout/maintenance reading to that lineweight principle.

## Detail callout registration calibration

The 2026-08-19 training adds a second, non-duplicate calibration axis through `references/DETAIL_CALLOUT_REGISTRATION.md` and the practice asset `06-practice/2026/2026-08-19-detail-callout-registration/OLEANDER_DETAIL_CALLOUT_REGISTRATION_R01.svg`.

This axis does **not** ask whether the child detail merely contains enough lines or notes. It tests whether a parent callout and enlarged child remain the same interface across a scale jump. Required checks include parent/crop traceability, stable anchors, orientation/sidedness, label-off registration and return-to-parent readability.

Core regression boundary:

`ENLARGEMENT ≠ REDRAW`.

A child may reveal fixing, build-up, drainage, maintenance or verification information that cannot be read at parent scale. It may not silently move, mirror, widen, reorder or invent the interface to make the drawing easier to explain.

## Promotion boundary

These fixtures can support skill regression testing for graphic hierarchy, vector annotation and parent→child registration only. They do not prove:

- field-measured geometry;
- structural design;
- anchor/foundation sizing;
- fabrication tolerances;
- code compliance;
- construction approval;
- universal lineweight values.

Any real drawing must still pass its own `TD-G0…TD-G8` gates.