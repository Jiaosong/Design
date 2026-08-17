# OLEANDER Data Viz Hierarchy Network Practice

Date: 2026-08-17  
Practice ID: `PRAC-DV-2026-08-17-HIERARCHY-NETWORK`  
Status: `EXECUTED / SELF-CHECKED / REVIEW PENDING`  
Promotion: `NO SELF-KEEP`

## Why this exercise exists

Recent C04 work exposed a recurring gap: route/network diagrams can be logically correct and source-bounded yet still read like technical reports because nodes, lines, labels and status elements have nearly equal visual weight.

This exercise does **not** replace C22 authority. It is a transfer variant that tests the revised `oleander-data-viz` skill against a real OLEANDER failure mode:

- route/service/return must read before optional content;
- optional reading must remain visible without becoming a checklist;
- return must be visibly available without fabricating a single itinerary;
- relational geometry must not be mistaken for survey or georeferenced mapping;
- Evidence -> Spatial Finding -> Design Consequence must be readable as one analytical argument, not six equal cards.

## Inputs

- `05-cases/c04-qingjiang-stone-book/QJ-C22-SPATIAL-DRAWING/QJ_C_SPATIAL_DRAWING_DATA_v3.0.json`
- `05-cases/c04-qingjiang-stone-book/QJ-C22-SPATIAL-DRAWING/README.md`
- revised `oleander-skills/oleander-data-viz/SKILL.md`
- external reference research recorded in `oleander-skills/oleander-data-viz/REFERENCE_RESEARCH_2026-08-17.md`

## Artifacts

- `OLEANDER_DV_HIERARCHY_NETWORK_v0.1.svg` — editable 1920x1080 vector artifact.
- `NETWORK_DATA_v0.1.json` — truth/role/topology contract.
- `VISUAL_CONTRACT_v0.1.json` — claim, analytical grammar, hierarchy, grid and intended-size contract.
- `REVIEW_REQUEST.md` — independent OLEANDER design review request.

Local render check before repository upload:

- SVG bytes: `12491`
- SVG SHA256: `af197bad2d47ba723c5b804fe439596346962d52d2661a101ebcfe49f853c901`
- PNG preview: `1920x1080`
- PNG bytes: `342658`
- PNG SHA256: `618c7631bf5cf003d53df3a1557218b4c10472dcf0aa8d9e9c4b3c2532ccb55d`

The local raster preview is an execution/readback aid only. SVG remains the editable practice authority.

## Visual changes tested

1. one dominant analytical field rather than equal cards;
2. role-based line weights: route > return > optional branch > annotation;
3. role-based node weights: service/return anchors > optional reading > companion;
4. position/size/whitespace establish hierarchy before color;
5. one coherent asymmetric grid across the 16:9 surface;
6. direct boundary labels: `SOURCE-TRACED RELATION / DIAGRAMMATIC PLACEHOLDER / FIELD-SURVEY OPEN`;
7. explicit `RELATIONAL BACKBONE / NOT ROUTE ORDER` label;
8. return spine is visible in the figure itself, not only in prose;
9. narrow Evidence -> Spatial Finding -> Design Consequence strip;
10. all text remains editable SVG text rather than rasterized image text.

## Truth boundary

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / RELATIONAL / NTS / NOT GEOREFERENCED`

This artifact does not prove exact route geometry, distance, slope, accessibility, capacity, safety, construction or live operation.

## Review state

Producer status is limited to `EXECUTED / SELF-CHECKED / REVIEW PENDING` under `OLEANDER_INDEPENDENT_DESIGN_VERDICT_POLICY_v1.0.md`.

Artifact existence, clean export and this README do not establish `PIXEL KEEP`, `MAIN KEEP` or `PROFESSIONAL FINISH PASS`.
