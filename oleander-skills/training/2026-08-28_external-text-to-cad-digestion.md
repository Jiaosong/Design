# External Skill Digestion — earthtojake/text-to-cad

Date: 2026-08-28
Status: `EXTERNAL REFERENCE DIGESTION / KNOWLEDGE EVIDENCE`
License observed: MIT

## Scope read

Primary external materials reviewed:

- `skills/cad/SKILL.md`
- `skills/cad/references/positioning.md`
- `skills/cad/references/inspection-and-validation.md`
- `skills/cad/references/snapshot-review.md`
- `skills/step-parts/SKILL.md`
- `skills/dfam-check/SKILL.md`

## Material delta accepted

Only general professional mechanisms were independently reformulated into OLEANDER:

1. fit/assembly CAD should preserve a parametric/native source and expose meaningful named parameters;
2. functional assembly placement should be datum/joint/mating driven rather than unexplained visual dragging;
3. STEP/STP can be a strong inspectable exchange for parametric mechanical/product work while remaining distinct from the editable authoring master and engineering approval;
4. geometry validation should separate topology/solidity, specified dimensions, alignment/frame checks and change isolation;
5. a CAD snapshot/view is diagnostic; a visual suspicion must be converted into deterministic geometry evidence before becoming a validation conclusion;
6. named off-the-shelf parts should use traceable real manufacturer/catalog geometry when available before simplified proxies are introduced;
7. mesh/process checks such as DfAM remain a separate manufacturing proof class and do not follow automatically from valid STEP geometry.

## Existing-first mapping

- `oleander-3d-pipeline` owns model/source/exchange integration and now routes parametric CAD work to `PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION.md`.
- Technical Drawing remains the existing Candidate knowledge/body for drawing-specific outputs; no new CAD Core Skill is created.
- `oleander-delivery-qc` remains the downstream release gate for file identity, units, reopen/round-trip and package integrity.
- Manufacturing/DfM/DfAM claims remain separate validation/HOLD unless a real specialist execution surface and process evidence exist.

## Rejected / not imported

- external CLI names, selector syntax, build123d-specific helper classes, viewer implementation, catalog API implementation and scripts are not copied into OLEANDER;
- external default wall/fillet/hole numbers are not adopted as OLEANDER defaults;
- OLEANDER does not assume the external runtime, STEP catalog or dependencies are installed;
- no external Skill is promoted as an OLEANDER execution owner merely because its repository exists.

## New OLEANDER artifact

`oleander-skills/oleander-3d-pipeline/PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION.md`

Key contract:

`DESIGN INTENT → PARAMETRIC SOURCE → DATUM / JOINT RELATION → CAD ARTIFACT → DETERMINISTIC GEOMETRY CHECK → DIAGNOSTIC VISUAL READBACK → REPAIR`

Maturity remains Candidate until real project execution and independent review.