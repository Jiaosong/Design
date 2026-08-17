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

## Promotion boundary

This fixture can support skill regression testing for graphic hierarchy and vector annotation only. It does not prove:

- field-measured geometry;
- structural design;
- anchor/foundation sizing;
- fabrication tolerances;
- code compliance;
- construction approval;
- universal lineweight values.

Any real drawing must still pass its own `TD-G0…TD-G8` gates.
