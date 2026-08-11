# XJ01 R54 / R02 × OLEANDER Blender Surface System

Status: `SURFACE v1.15 C TRACK RENDERED ACTIVE / R02-00 PASS (response-equivalence migrated) / R02-01 PASS + A_MID SELECTED / R02-02A OPEN / HUE-CHROMA-FINISH-TEXTURE CLOSED`

## Six-role binding

- `MAT_PP_PRIMARY_FIELD` -> `PP_INJECTION_FINE_MATTE` + `NT_PP_FINE_MATTE`
- `MAT_PP_SECONDARY` -> same PP family
- `MAT_PP_UI` -> same PP family; no project-local UI roughness offset during R02
- `MAT_PU_CONTACT` -> TPE/PU soft-matte optical method; **OVERMOLDING is not adopted as an XJ01 process fact**
- `MAT_IRON_VISIBLE` -> coated-steel / powder-coat visual baseline candidate; actual XJ01 coating remains pending and powder microtexture stays disabled
- `MAT_METAL_HARDWARE` -> generic conductor fallback; exact hardware finish/process unknown

## Surface v1.15 authority

The active authority is the user-uploaded `OLEANDER_Blender_Surface_System_v1.15_C_Track_Rendered.zip`. The package records Blender 5.2 rendered diagnostic PASS evidence for C01/C03/C04/C05/C06/C07/C08/C09. Heavy `.blend` and rendered evidence stays in Drive; GitHub stores the executable contracts, semantic checks and project bindings.

C Track validates procedural mechanisms. It does **not** prove a manufacturing texture or physical finish for XJ01, so automatic C Track application to project materials is disabled.

## Semantic update policy

Surface updates are split into two signatures:

- `render_response_signature`: invalidates an existing controlled R02 color gate only when the material/recipe/project-binding semantics that affect the rendered stimulus change.
- `diagnostic_capability_signature`: changes in C Track or diagnostic capability require a local/detail diagnostic review but do not force a whole-product color rerender when render response is unchanged.

The v1.6 -> v1.15 audit found the XJ01 render-response signature unchanged (`44a462645344c996872c5d3cf80b73e2d9a448d26d34356e8918fb60951642ac`). Therefore the existing Whole Product R02 color evidence can migrate to v1.15 while Local Detail / C Track diagnostics are rerun under v1.15.

## R02-01 multi-scale decision

Whole Product + dedicated `D02_ROD_PP_JOINT` review resolves the Anchor corridor:

- A_LIGHT (`#B8BCC0`): structural spine collapses too far into the shallow PP field.
- A_DEEP (`#5B5F62`): whole-product credibility is strong, but the rod-to-PP joint creates an overly hard dark/light breakpoint and increases tool-like weight.
- **A_MID (`#888C8F`): SELECTED / DIGITAL ANCHOR.** It retains the longitudinal structural spine while preserving better local continuity.

This is a Blender/Cycles digital visual calibration decision, not physical CMF or user-preference validation.

## Local Surface review

- D01 top UI: local geometry/edge hierarchy readable; physical finish not inferred.
- D02 rod/PP joint: PASS; A_MID selected.
- D04 lower UI/hardware: assembly hierarchy readable; hardware finish remains unknown.
- D03C PP Beauty Macro: `READABILITY HOLD`; do not increase procedural amplitude merely to make grain visible.
- D05B PU Beauty Macro: `READABILITY HOLD`; improve reflection-design imaging before changing surface parameters.
- C Track emission diagnostics on the actual XJ01 geometry confirm PP meso/micro/final-roughness and PU macro/micro/final-roughness signals are present. Low Beauty Macro visibility is not node failure.

## Next gate

`R02-02A Field Lightness` is now open with `Anchor=A_MID` locked. Geometry, camera, lighting, exposure, background, scale and Surface v1.15 render-response signature remain locked. `R02-02B Hue`, `R02-02C Chroma`, Finish and Texture remain closed.

## Evidence boundary

All current results are digital Blender 5.2 / Cycles visual calibration. They do not validate physical roughness, coating process, wet/dirty/aged states, touch, manufacturing tolerance or user preference.
