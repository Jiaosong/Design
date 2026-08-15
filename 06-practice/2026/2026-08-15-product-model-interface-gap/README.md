# OLEANDER Digital Design Training — 2026-08-15

## Knowledge Position
- Domain: General Design Knowledge / Product Design / Product Modeling & Interface Geometry
- Level: L5 Practice Method Candidate
- Role: PRACTICE / MODELING METHOD
- Evidence: OpenSCAD executable source, 3 STL outputs, 3 rendered PNG previews.
- Application Mapping: IP03 PRIMARY; B02 SUPPORTING.

## Exercise
Generic compact device enclosure. Same overall geometry, three shell-seam values: 0.2 / 0.6 / 1.2 mm.
All dimensions are exercise assumptions and do not represent project, manufacturing, ergonomic, tolerance, or supplier data.

## Method
Model product as `Core body → split/interface → control/display zones → seam variant`, then inspect whether the interface remains visually legible without becoming the first-reading unit.

## Results
- Variant 1 / 0.2 mm: seam is visually weak at current render scale; interface risks disappearing.
- Variant 2 / 0.6 mm: seam remains legible while body still reads as one volume. KEEP as visual-comparison baseline only.
- Variant 3 / 1.2 mm: seam becomes a strong horizontal band and begins competing with the product volume. REDUCE for this exercise.

These are visual judgments from the generated renders, not manufacturing recommendations.

## Artifact Review
- Common geometry/render open test: PASS.
- OpenSCAD compile/export: PASS for all 3 variants.
- STL generation: PASS for all 3 variants.
- Preview render: PASS via Xvfb/OpenSCAD; PNG reopened and visually inspected.
- Product/manufacturing validity: NOT TESTED.
- Physical assembly/tolerance/warpage/tooling: OPEN.
- AR-S02 Model: PASS for practice geometry, not production geometry.
- AR-S06 Visual: PASS for hierarchy comparison.
- AR-S09 Release Package: pending cross-platform sync closure until GitHub and Drive readback.

## Candidate Rule v0.1
Interface gaps should be modeled as explicit relation variables and reviewed at product-reading scale; neither zero-visibility nor maximum separation should be assumed correct before manufacturing constraints are introduced.

Status: PRACTICE CANDIDATE / NOT PROMOTED.
