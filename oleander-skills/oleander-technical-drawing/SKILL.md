---
name: oleander-technical-drawing
description: Create, deepen, edit, and audit OLEANDER technical drawings as evidence-bound professional design documents. Use whenever the user mentions plans, sections, elevations, construction details, nodes, exploded/assembly drawings, fabrication drawings, dimensional drawings, lineweight, projection, section cuts, callouts, tolerances, material/CMF schedules, title blocks, SVG/DXF/PDF drawing output, Illustrator/CAD drafting, or asks to make a drawing more professional rather than merely more detailed.
compatibility: Works with CAD/vector tools, Blender or other geometry-authoring tools, Illustrator/Inkscape, SVG/DXF/PDF workflows, and OLEANDER review/delivery-QC conventions.
---

# OLEANDER Technical Drawing

A technical drawing is a design-and-communication instrument, not a decorated screenshot. Preserve authoritative geometry and truth state first; then make spatial, constructive, dimensional and visual relationships readable enough that the intended reader does not need to guess.

This skill is independent from `oleander-3d-pipeline`, `oleander-story-and-board`, and `oleander-delivery-qc`:

- 3D pipeline owns model/exchange authority and derived axonometric geometry.
- Technical drawing owns 2D/2.5D drawing logic, dimensional communication, detail hierarchy and drawing-specific review.
- Story/board owns placement of approved drawings inside presentation surfaces.
- Delivery QC owns release-package preflight; it does not grant drawing-design approval.

`ARTIFACT EXISTS ≠ DRAWING PASS ≠ ENGINEERING PASS ≠ FIELD PASS ≠ MAIN KEEP`.

## 1. Declare drawing status before drawing

Every sheet/view must declare one of these states:

1. `DESIGN STUDY` — explores geometry, proportion, relation or assembly logic; not fabrication/construction authority.
2. `TECHNICAL EXPLANATION` — communicates how a design is intended to work using source-grounded or explicitly provisional information.
3. `COORDINATION` — coordinates interfaces between systems/disciplines; unresolved interfaces remain open.
4. `FABRICATION` — may drive making only when dimensions, tolerances, materials, finishes, interfaces and responsible authority are resolved for that scope.
5. `CONSTRUCTION` — may drive site construction only when required field/engineering/code approvals and project authority are resolved.

Never visually imitate a fabrication/construction drawing while the truth state is only study or explanation. Use explicit markers such as `NTS`, `PROVISIONAL`, `FIELD OPEN`, `VERIFY`, `ENGINEERING REVIEW REQUIRED`, or `NOT FOR CONSTRUCTION` where applicable.

## 2. Resolve source authority

Before editing geometry, create a compact authority table:

| Information | Current authority | Revision/date | Allowed use | Open conflict |
|---|---|---|---|---|
| geometry | CAD/BIM/model/survey/etc. | ... | derive views only / editable | ... |
| dimensions | measured/locked/design-recommended | ... | verified / provisional | ... |
| material/finish | CMF schedule/spec | ... | approved / candidate | ... |
| structure/connection | engineer/detail/reference | ... | explanatory / approved | ... |
| site/context | survey/map/field/source | ... | observed / inferred | ... |

Authority order is project-specific; do not invent a universal hierarchy. A render, AI image, presentation diagram or raster screenshot does not become dimensional authority merely because it looks resolved. If a derived view conflicts with the authoritative geometry, the authority wins until a documented design revision changes it.

## 3. Build a drawing set, not an isolated picture

Choose only the views needed to answer the drawing's decision question. Typical set logic:

- `GA / GENERAL ARRANGEMENT`: overall location, orientation and principal relations.
- `PLAN`: horizontal organization, clearances, interfaces and movement.
- `ELEVATION`: vertical relation, envelope, alignment and finish boundaries.
- `SECTION`: cut relation, depth, level, support, ground/water/build-up and human scale.
- `DETAIL / NODE`: local interface, fixing, edge, joint, drainage, safety or maintenance condition.
- `EXPLODED / ASSEMBLY`: part identity and assembly order; not a substitute for exact interface detail.
- `PART / FABRICATION`: manufacturable geometry, dimensions, tolerance and finish for one part/scope.
- `CMF / MATERIAL MAP`: material ID, boundary, direction, finish and schedule linkage.

A detail must have a traceable parent view. A parent view must show where the detail comes from. Do not let an attractive exploded axon replace plan/section information needed to resolve interfaces.

## 4. Projection and view coherence

For orthographic work:

- declare projection method when relevant;
- keep plan/elevation/section geometry aligned to the same locked source;
- identify section/cut direction explicitly;
- use consistent datums, levels, grids or local reference axes;
- do not silently change camera, crop, orientation or scale between comparison views;
- use hidden lines only when they add decision-relevant information;
- use local enlargements for dense interfaces rather than forcing all detail into the parent view.

For axonometric/exploded views, lock camera/projection and derive geometry from the authoritative model where possible. Labels and explanatory graphics remain separate vector layers from the geometry source.

## 5. Dimensioning is a design test

Dimensions must communicate design intent, not merely fill empty space.

Before adding a dimension, classify it as:

- `AUTHORITY / VERIFIED` — measured or locked by the approved source;
- `DESIGN RECOMMENDATION` — selected design value with rationale;
- `RECOMMENDED RANGE` — bounded design range where a single number is not yet authoritative;
- `REFERENCE` — informational only, not controlling;
- `FIELD VERIFY` — cannot be closed remotely/currently;
- `TBD` — unresolved and not safe to guess.

Rules:

1. Dimension from stable datums/interfaces instead of arbitrary visible edges when function depends on datum relationships.
2. Prefer the minimum controlling dimension set; avoid redundant or contradictory closed chains.
3. Show critical clearances, gaps, offsets, thicknesses, radii/chamfers, hole/slot position and interface heights where they affect fit, safety, assembly, drainage, access, maintenance or visual intent.
4. Tolerance only what has a functional/manufacturing reason and an appropriate authority basis. Do not invent precision to make a sheet look professional.
5. Keep nominal size, tolerance, field uncertainty and design range conceptually separate.
6. If a dimension is source-derived by calculation or image/geometry measurement, record method, units and uncertainty outside or alongside the drawing record.

Mechanical GD&T may use ASME Y14.5 or the project's designated GPS standard when applicable, but this skill does not imply GD&T competence or compliance by default. Discipline-specific engineering review remains required.

## 6. Draw the construction/assembly logic that matters

A professional node drawing should let a qualified reader identify the intended relation without reconstructing it from prose.

When applicable, graphically resolve:

- primary load/support path or mounting logic;
- interfaces between parts/materials;
- plate/profile/member orientation;
- fastener/anchor/adhesive/weld location as evidence permits;
- edge treatment, joint, seam and tolerance/clearance condition;
- base/foundation/support relationship;
- drainage, water-shedding and corrosion-isolation intent;
- slip/trip/fall/safety edge condition;
- removal/replacement and maintenance access;
- assembly/disassembly order if it changes design feasibility.

Text does not substitute for visible geometry. Conversely, visible geometry does not prove engineering adequacy. If structural sizing, anchorage, foundation, fire, waterproofing, electrical or other specialist design is unresolved, show the relationship needed for design coordination and mark the specialist scope open.

## 7. Graphic hierarchy: first-read to near-read

Technical completeness cannot compensate for a flat drawing.

Default reading order:

`CUT / PRIMARY FORM → PRIMARY STRUCTURE OR SPATIAL RELATION → SECONDARY CONSTRUCTION / EDGE / INTERFACE → DIMENSION / LEADER / NOTE / HUMAN / MAINTENANCE SUPPORT`

Use the fewest distinct graphic classes that reliably create this order at the actual delivery size. Lineweight values are output- and scale-dependent; do not treat one screen-pixel recipe as universal.

Hard rules:

- section cuts/primary profiles must read before annotations;
- secondary construction must remain visible at near-read without competing with the primary claim;
- dimensions and leaders must terminate unambiguously and must not float as decorative graphics;
- humans, furniture, vegetation and maintenance figures establish use/scale only and never overpower the technical subject;
- hatch/material fills must distinguish states without burying linework;
- if a note competes with the object it describes, move/shorten/reduce the note before making all geometry heavier;
- adding more dimensions or notes is not a valid fix for poor hierarchy.

Review both `FIRST READ` and `NEAR READ`. A clean thumbnail that loses construction evidence at print/detail scale remains `REVISE`.

## 8. Annotation and vector integrity

Text, dimensions, leaders, symbols, title blocks, legends and core technical linework must remain vector in the editable source and vector-capable delivery formats whenever the format supports it.

- Do not rasterize labels merely to preserve appearance.
- Do not use AI-generated pseudo-text, pseudo-dimensions or image-rendered annotation as technical content.
- Raster imagery may appear as a referenced/context layer, but must not replace authoritative linework or dimensional information.
- Keep annotation on separable named layers/classes.
- Establish typography hierarchy for title, view title, dimension, note, qualifier and source/state label.
- Check collisions, overset/clipping, leader crossings and minimum readable size at the target print/view scale.

## 9. Material / CMF communication

Where material or finish affects the drawing, use stable IDs linked to a schedule. Show, as applicable:

- material/finish ID and approved/candidate state;
- finish boundary and transition;
- grain/brushing/weave/lay direction when function or appearance depends on it;
- coating/plating/anodizing/paint/texture/gloss specification only when source-grounded;
- substrate versus finish as separate concepts;
- edge/return/back-face treatment where visible or manufacturable.

Do not infer a hidden build-up solely from a render.

## 10. Sheet and document control

Every controlled drawing set should expose enough document metadata to identify exactly what is being reviewed:

- project/object ID;
- drawing/sheet ID and title;
- revision/status;
- date;
- author/owner and reviewer where required;
- scale or `NTS` per view;
- units;
- projection/orientation when relevant;
- source/authority revision;
- truth/status boundary;
- superseded/current state.

Use project title-block conventions; ISO 7200 is a reference for document-header field logic, not an automatic claim of full compliance.

## 11. OLEANDER Drawing Gates

A drawing must pass these gates independently. Do not collapse them into one score.

### `TD-G0 / INTENT & STATUS`
PASS when drawing purpose, audience, truth state and allowed use are explicit.

Blockers: unlabeled study presented as construction/fabrication authority; stale/superseded state shown as current.

### `TD-G1 / SOURCE AUTHORITY`
PASS when geometry, dimensions, materials and specialist assumptions trace to current authority or are explicitly provisional/open.

Blockers: invented dimensions; render/AI image treated as geometry authority; unresolved source conflict silently reconciled.

### `TD-G2 / GEOMETRY & PROJECTION`
PASS when views agree with the same source, datum/orientation is coherent and cut/detail parentage is traceable.

Blockers: plan/section mismatch; impossible assembly created by presentation edits; untraceable section/detail.

### `TD-G3 / DIMENSIONAL INTENT`
PASS when controlling dimensions are sufficient, non-contradictory and correctly truth-labeled.

Blockers: missing critical interface dimension for claimed fabrication/construction scope; false precision; conflicting chains.

### `TD-G4 / CONSTRUCTION & ASSEMBLY LOGIC`
PASS when the required interfaces and maintenance/assembly conditions are graphically understandable for the declared scope.

Blockers: prose-only critical connection; physically impossible access/assembly; specialist design presented as resolved without authority.

### `TD-G5 / DESIGN QUALITY & READABILITY`
PASS when first-read and near-read hierarchy are both professional at target scale.

Blockers: equal-weight visual noise; annotations dominate geometry; illegible detail; diagrammatic black cuts; missing technical evidence hidden by visual simplification.

### `TD-G6 / VECTOR & ANNOTATION INTEGRITY`
PASS when vector text/dimensions/linework survive export and annotations target the intended geometry without collision or ambiguity.

Blockers: rasterized technical text where vector output is required; broken fonts; pseudo-text; orphan callouts; clipped content.

### `TD-G7 / OUTPUT & ROUND-TRIP`
PASS when editable source and delivery derivatives open independently, scales/units remain correct, and the exported PDF/SVG/DXF reproduces the approved drawing state.

Blockers: wrong scale/units; missing links/fonts; stale export; non-recoverable source; export differs materially from reviewed source.

### `TD-G8 / INDEPENDENT REVIEW & PROMOTION`
Production author may supply evidence but must not self-promote the drawing to `MAIN KEEP`, `FABRICATION APPROVED`, or `CONSTRUCTION APPROVED`. Use the current OLEANDER review path / responsible independent reviewer and keep engineering/field approval separate.

A CI/export PASS, checksum, artifact existence or owner claim cannot override `TD-G1`–`TD-G6`.

## 12. Required review sequence

Use this order before adding new content:

1. Open the actual editable/source drawing and exported derivative.
2. Confirm status and source authority.
3. Check cross-view geometry/projection.
4. Check the dimension set and unresolved critical interfaces.
5. Check construction/assembly/maintenance logic for the declared scope.
6. Review at intended print/display size for first-read hierarchy.
7. Zoom to near-read/detail scale for line, callout, dimension and material clarity.
8. Inspect vector/text/export integrity.
9. Produce `KEEP / REVISE / REJECT / HOLD` with concrete blockers and evidence.
10. Repair the highest-order blocker first; do not add decorative complexity as a substitute.

## 13. Required output contract

For a substantial drawing task, return or create:

- editable authoritative/derived source (`DWG/DXF/SVG/AI` or project-native equivalent as applicable);
- vector PDF/SVG/DXF derivative where applicable;
- preview PNG only as a review convenience, never as sole technical authority;
- `DRAWING_MANIFEST` containing IDs, revision, units, scales, source authority, truth state and dependencies;
- `DIMENSION_REGISTER` for critical dimensions/ranges/field-open items when complexity warrants it;
- `DETAIL/CALLOUT_REGISTER` linking parent views and node IDs where complexity warrants it;
- `DRAWING_QA` with TD-G0…TD-G8 status and blockers;
- revision log that records material design changes rather than cosmetic file churn.

## 14. Standards reference boundary

Use current discipline/project standards when required. As a cross-discipline professional anchor, this skill is informed by the scopes of:

- ISO 128-1:2020 — fundamental requirements for technical drawing representation;
- ISO 128-2:2022 — line, leader and reference-line conventions;
- ISO 128-3:2022 — views, sections and cuts;
- ISO 129-1:2018 + Amd 1:2020 — presentation of dimensions and associated tolerances (not the full meaning/application of tolerances);
- ISO 5455:1979 — drawing scales;
- ISO 5456-2:1996 — orthographic representation;
- ISO 7200:2004 — title-block/document-header data fields;
- ASME Y14.5-2018 (R2024) — GD&T when that standard is the project authority.

These references define professional convention domains, not automatic compliance. If a task requires code/standard compliance, verify the applicable current edition, jurisdiction, discipline and purchased/full normative requirements before claiming compliance.
