# Practice Evidence — Material / Constructive Detail — 2026-09-12

Status: `REAL BLENDER 5.2 PRACTICE / CURRENT SKILL REFINEMENT / NO DESIGN PROMOTION`

## Trigger

A live Blender 5.2 pavilion already contained a freeform canopy, Geometry Nodes, columns, stairs, cables, 133 base objects and 97 modifiers, but user review correctly identified that material and structural/constructive detail were still weak.

This practice demonstrates why scene complexity cannot substitute for constructive/material depth.

## Existing-first execution

The work reused the current `oleander-3d-pipeline` authority/state/readback rules and the active Blender runtime. No new project-level Skill, METHOD, framework or approval gate was created.

The live model was enriched non-destructively in a separate detail collection. Major reviewed objects received stable OLE-style IDs plus semantic class, material-authority state, constructive-detail state and explicit `engineering/manufacturing/field = OPEN` metadata.

## Real model delta

Representative detail added included:

- 32 washers;
- 32 nuts plus visible threaded rod ends;
- 8 column-head plate/cleat groups;
- column-base stiffening representation;
- secondary roof members;
- standing-seam roof representation;
- edge gutters and 4 downpipes;
- 30 stair tread support brackets plus anti-slip/nosing representation;
- an outer stair stringer and landing support frame;
- 24 cable-end socket representations plus anchor plates/pins;
- plaza joint representation.

Nine distinct procedural visual materials were created for steel, galvanized steel, standing-seam aluminum, fasteners, concrete, timber, anti-slip rubber, EPDM/seal and water. All remain visual material models rather than physical material specifications.

## Readback failure and repair

The first real Blender overall render failed the constructive-detail review: standing seams and some roof secondary details floated above and extended beyond the authoritative canopy.

Root cause: those details were generated from an independent approximate roof equation instead of the evaluated authoritative canopy geometry.

The repair rebuilt a BVH from the evaluated canopy, ray-bound seam/purlin points to that host, split detail curves at the real oculus/opening, derived gutter traces from evaluated roof-edge geometry, regenerated downpipes from repaired gutter endpoints, and repeated the overall render.

The close joint readback also showed that the first base stiffener representation was too one-directional, so a perpendicular stiffener orientation was added before the second readback.

## Accepted Skill delta

- host-following procedural detail must bind to evaluated authoritative geometry or an explicitly governed offset;
- detail termination at boundaries/openings is part of geometry QC;
- close-camera constructive review must inspect primary/secondary/interface/fastener/edge/drainage/service layers as relevant;
- visual material model, material identity/process/section authority and physical claim level remain separate;
- readback is a repair-and-retest loop, not only evidence capture;
- `MODEL COMPLEXITY ≠ CONSTRUCTIVE DEPTH`;
- `PBR NODE ≠ MATERIAL TRUTH`;
- `VISIBLE FASTENER ≠ ENGINEERING VALIDATION`.

## Claim ceiling

The practice proves Blender execution, improved constructive representation, evaluated-host binding and closed-loop visual/geometry readback only.

It does not prove structural capacity, final member/plate/fastener sizing, weld/bolt specification, drainage capacity, material grade/coating specification, fabrication feasibility, code compliance, field installation or engineering/manufacturing approval.

Those states remain OPEN.
