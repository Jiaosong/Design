# Automotive v0.11｜R28 Local Fender Patch Architecture Gate

Status: `INITIALIZED / M4 REOPENED LOCALLY / M6-M8 BLOCKED`

## Evidence trigger

R27A–R27E established that a circumferential wheel-opening principle is preferable to the earlier longitudinal-strip approximation, but every attempt to attach that new ring system directly into the inherited row4–row7 lower-body cage failed Human M5 in a different way:

- R27A: radial overshoot / floating bridge;
- R27B: hard common-endpoint exits;
- R27C: tangential fan still retained the common attachment wall;
- R27D: staggered stations were structurally clearer but transition triangles became visible teeth;
- R27E: all-quad collars removed wheel-zone triangles but converted the same local conflict into radial highlight pinching / curvature teeth.

Therefore the remaining defect is no longer scoped as `wheel-arch attachment`. The local M4 reopening expands to:

`wheel opening + fender crown + shoulder transition + mid-body transition + rocker transition`

as one Primary patch architecture.

## Locked outside the R28 influence window

- R09 wheelbase / track / wheel OD / cabin package;
- R11 transverse section intent outside local fender windows;
- R12 longitudinal interpolation outside local fender windows;
- R18/R20 front/rear termination system;
- R25 wheel-opening proportion target as a starting target, not a mandatory final curve;
- global roof / greenhouse / center body package.

## R28 construction requirements

1. Rebuild each front/rear fender zone as a single local Source patch, not an inserted ring with attachment cells.
2. The patch must include the complete shoulder-to-rocker transition around the wheel opening.
3. Inner wheel opening and outer body boundary must be solved together in the same parameterization.
4. Influence must decay to the locked body cage before leaving the local window.
5. One editable Source authority remains mandatory.
6. No detached wheel-brow authority.
7. Source Boolean = forbidden as the modeling-quality solution.
8. Global SubD = forbidden as the modeling-quality solution.
9. Source n-gon = 0.
10. Any unavoidable extraordinary vertices / controlled triangles must be explicitly counted and visually audited under Strip/Grazing.

## R28A decision question

Can a local polar-to-body fender patch, with the complete shoulder-to-rocker region included inside the same deformation field, remove the R27 attachment seam/pinching while retaining the accepted package and R25 wheel-opening scale?

## Validation matrix

Machine:
- one Source island;
- no n-gon;
- no Boolean / global SubD;
- local influence bounded to front/rear fender windows;
- stable source hash during diagnostics;
- 9 renders.

Human M5:
- wheel opening wraps tire coherently in Side and 3/4;
- no visible attachment seam, teeth, radial collar pinching or vertical strip wall;
- fender crown grows from shoulder/body volume rather than reading as a cap;
- front/rear arch detail has controlled curvature;
- Strip and Grazing highlights cross the patch without severe kinks;
- package / cabin / body proportion remains unchanged outside local windows.

No M6/M7/M8 continuation until Human M5 PASS.
