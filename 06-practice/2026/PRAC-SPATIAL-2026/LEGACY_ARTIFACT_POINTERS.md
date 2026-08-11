# Legacy Artifact Pointers｜PRAC-SPATIAL-2026

These pointers preserve historical technical provenance. They do **not** define the P0–P4 project hierarchy.

## WS-01｜SP01

Current merged lineage:
- PR #58 — `Rebase SP01-R02 GIS Reality Gate with PAP rescue and current CI governance`
- source branch: `practice/sp01-r02-gis-pap-rebase-20260811`

Retained historical branches:
- `practice/2026-08-08-sp01-gis-density`
- `practice/2026-08-11-sp01-r02-gis-reality-gate`

Authority boundary:
`QGIS Runtime VERIFIED / Persistence PASS / Project CRS OPEN / Project Data OPEN / Candidate Promotion NO`.

## WS-02｜SP02

Current handoff lineage:
- `practice/2026-08-11-sp02-r03-runtime-closure`

Retained historical branches:
- `practice/2026-08-09-sp02-grasshopper-data-tree`
- `practice/2026-08-10-sp02-grasshopper-data-tree-rerun01`
- `practice/2026-08-10-sp02-grasshopper-data-tree-rerun02`
- `practice/2026-08-10-sp02-grasshopper-data-tree-rerun02-check`
- `practice/2026-08-10-sp02-grasshopper-data-tree-rerun02-tmp`

The Rerun branches are version/failure history only. They are not P2/P3 project objects.

Current boundary:
`STATIC HANDOFF PASS / REAL RHINO RUNTIME NOT EXECUTED / CP2 OPEN / CP4 OPEN / NO_PURCHASE=TRUE`.

## WS-03｜SP03

Current validation lineage:
- `practice/2026-08-11-sp03-r02-light-performance-interface`
- final real Radiance Actions run: `31457344868`
- final artifact: `9088638622`
- digest: `sha256:abe1512e849c17054fd8b92d89c8044f70b891a40da0dd04267a052328b02436`

Current boundary:
`PERFORMANCE INTERFACE VERIFIED ON SYNTHETIC TEST CELL / PROJECT REALITY OPEN`.

## WS-04｜SP04

Current closure lineage:
- `practice/2026-08-11-sp04-r08j1-p0-evidence-closure`

Retained earlier branches:
- `practice/2026-08-10-sp04-revit-wall-opening`
- `practice/2026-08-10-sp04-software-neutral-opening-qa`
- `practice/2026-08-11-sp04-r08h2-orthogonal-review`

Current boundary:
`PRACTICE CLOSED / ARCHIVED AS TRAINING PROTOTYPE / RG-01—RG-04 OPEN / PROJECT ISSUE BLOCKED`.

## Migration rule

- Do not rename old branches to match the new project IDs.
- Do not rewrite historical PR titles, run IDs, artifact IDs, or source filenames.
- Do not allow a later PASS to overwrite an earlier FAIL/SUPERSEDED state.
- New structural references should use `PRAC-SPATIAL-2026-*`; historical evidence keeps its original identity.
