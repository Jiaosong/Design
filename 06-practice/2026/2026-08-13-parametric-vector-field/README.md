# OLEANDER Digital Design Training — 2026-08-13

## Knowledge position
- Domain: General Design Knowledge / Computational & Visual Systems
- Level: L5 Practice Method Candidate
- Role: PRACTICE / TOOL METHOD
- Evidence: deterministic SVG + browser-readable HTML generated in this run; no external project data.

## Application Mapping
- IP03: PRIMARY — information/visual system prototyping
- B04: SUPPORTING — AI-assisted reproducible workflow
- Business/Culture/Spatial otherwise: N/A for this exercise

## Exercise
Relation-Weighted Vector Field: one topology, three hierarchy weights (0.35 / 0.65 / 1.00). Parameters are EXERCISE ASSUMPTIONS, not project data.

## Review
- AR-G01–G09: PASS by static inspection.
- AR-G10: PARTIAL — hierarchy, boundary, clearance, scale/proportion, view consistency checked; no target-app export round-trip.
- AR-S04 Code/Parametric: PASS — explicit parameters, deterministic output, reproducible structure.
- AR-S06 Visual: PASS — three hierarchy states remain distinguishable without changing topology.
- AR-S09 Release Package: PENDING.

Status: NEEDS REVISION / DESIGN-READY FOR RUNTIME REVIEW.

## Keep / Reduce / Remove
- KEEP relation-driven geometry and explicit weight parameters.
- REDUCE stroke-contrast range when applied to dense diagrams.
- REMOVE curvature that does not encode a relation.

## Runtime boundary
The HTML/SVG were generated and statically inspected in the execution environment. No Illustrator/Inkscape/Figma round-trip or real browser interaction test is claimed.
