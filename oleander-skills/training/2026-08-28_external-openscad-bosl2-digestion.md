# 2026-08-28｜External Skill Digestion｜OpenSCAD / BOSL2

Status: `DIGESTED / LICENSE UNCLEAR / HIGH-LEVEL MECHANISM ONLY / EXISTING OWNER EXTENDED`

## Source

- Repository: `swh/openscad-skill`
- Skill: `openscad-bosl2/SKILL.md`
- Reviewed repository documentation: root README summary + Skill content.
- Repository license check: root `LICENSE` not found; code search did not establish a repository-level license in the reviewed state.

Rights therefore remain unclear. OLEANDER does not copy BOSL2 code templates, helper tools, printer tables, slicer recipes, house-style defaults or fixed numeric baselines.

## Current comparison

Existing `PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION.md` already owns:

- parametric source authority;
- named parameters/datums;
- deterministic dimension/alignment/topology checks;
- purchased-component provenance;
- source repair/regeneration;
- mesh/STEP derivatives not replacing parametric source;
- manufacturing validity separate from geometry validity.

The residual gap was a native `.scad` fabrication route and explicit fabrication-context separation.

## Material delta accepted

Implemented as:

`oleander-3d-pipeline/OPENSCAD_PARAMETRIC_FABRICATION_EXTENSION.md`.

Accepted mechanisms:

1. `.scad` can be the Current editable parametric authority when it matches Required Native Output.
2. Separate user-facing parameters from derived/internal values and expose only meaningful variation controls.
3. Use stable reference-frame/anchor relations so parameter changes do not create transform drift.
4. Treat boolean robustness workarounds separately from real manufacturing clearance/tolerance.
5. Treat print/build orientation as a design/process decision tied to load, support, critical faces and finish rather than “what lies flat.”
6. Version printer/material/slicer/process context separately from geometry truth.
7. Track `.scad → mesh/3MF/STL → target-tool reopen` lineage while preserving source authority.

## Rejected / not transferred

- BOSL2-first requirement;
- fixed `$fn`, epsilon, layer-height defaults;
- fixed chamfer/roundover sizes;
- specific material hierarchy such as PETG default;
- fixed overhang/bridge/infill/wall/top-bottom/brim/ironing recommendations;
- fixed diagonal print angles;
- fixed printer capability tables;
- mandatory 3MF over STL regardless of the actual toolchain;
- helper binaries/scripts and code skeletons.

## OLEANDER correction

Process numbers come from the Current printer/material/process evidence. A modeling epsilon is not manufacturing clearance. A valid OpenSCAD render or 3MF export does not prove fit, strength, safety or manufacturability.

## Maturity boundary

`CANDIDATE EXTENSION / NOT ACTIVE`. Requires real `.scad` project execution, parameter-change regression and fabrication/tool readback before stronger maturity.