---
name: oleander-technical-drawing
description: Produce and validate Oleander technical drawings, dimensions, line hierarchy, DXF/SVG/PDF drawing sets, exploded/section/detail communication, and handoff-ready drawing evidence without overstating engineering or field truth.
compatibility: Candidate reusable skill. Dimension and geometry authority come before software convenience. Use editable SVG/DXF/PDF/CAD-capable workflows when actually available; Pro Design Toolchain CAD/DXF runtime remains Candidate until explicit promotion.
---

# Oleander Technical Drawing

Create technically readable, editable drawings that preserve authoritative geometry, dimension status, units and construction/product relationships.

## Lifecycle role

- Primary: `VALIDATION`
- Secondary: `DESIGN`, `PRESENTATION`
- Status: `CANDIDATE`
- Upstream: `oleander-design-process`, `oleander-3d-pipeline`
- Downstream: `oleander-delivery-qc`, return-to-`oleander-design-process`

## Required sequence

`SOURCE / DIMENSION AUTHORITY → REQUIRED DRAWING TYPE → UNITS / SCALE / NTS STATE → AUTHORITATIVE GEOMETRY → EDITABLE DRAWING → DIMENSION / ANNOTATION HIERARCHY → REOPEN / ROUNDTRIP → WHOLE + DETAIL READBACK → REPAIR → RETEST`

## Drawing hierarchy

Use the medium-appropriate hierarchy for:
- cut / profile / near / far lines;
- primary / secondary geometry;
- dimensions, leaders and notes;
- grids/axes/reference levels;
- materials/components/assemblies;
- exploded relationships;
- callouts and detail references;
- human/usage scale where relevant;
- field-open or assumption markers.

## Dimension authority

1. Exact dimensions must come from verified source geometry, technical source, measured/observed data, or an explicitly governed design estimate.
2. A governed estimate should preserve recommended value + reasonable range + basis + sensitivity + FIELD correction item when material.
3. Render, AI image, screenshot, presentation diagram or visually inferred proportion is not dimension authority.
4. If FIELD=0 or engineering proof is absent, mark the drawing accordingly; professional graphic quality must not convert provisional geometry into measured fact.

## Exchange and runtime

- Preserve units, layer/entity identity, scale/NTS state and source object IDs.
- DXF/STEP/FCStd or other CAD exchange is used only through an actually probed surface and within its lifecycle state.
- Reopen or roundtrip the target format when the drawing is being claimed as technically valid.
- A readable SVG/PDF derivative does not prove the CAD/native master is healthy, and a valid DXF does not grant engineering approval.

## Review

Check whole/detail readability, lineweight hierarchy, dimension collision, annotation density, units, consistent scales, geometry regression, callout clarity and whether the drawing explains relationships graphically rather than merely listing them in prose.

## Hard boundary

`TECHNICAL DRAWING PASS ≠ FIELD MEASURED ≠ ENGINEERING SIGN-OFF ≠ FOR CONSTRUCTION`.
Do not promote NTS/concept/preliminary drawings into construction authority without the required evidence and owner.

## Required output

Return drawing/master identity, geometry/dimension authority, units/scale, editable format, derivative formats, reopen/readback evidence, assumptions/FIELD items, visual/technical issues repaired, and residual HOLD.

## Candidate boundary

This skill remains Candidate pending real project validation, golden-case regression and explicit promotion. It cannot self-grant ACTIVE or Independent KEEP.