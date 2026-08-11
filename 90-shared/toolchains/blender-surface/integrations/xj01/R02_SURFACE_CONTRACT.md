# XJ01 R54 / R02 × OLEANDER Blender Surface System

Status: `R02-00 SURFACE-v1.6 PREVIEW GATE PASS / R02-01 PAIR RENDERED / R02-02A CLOSED`

## Six-role binding

- `MAT_PP_PRIMARY_FIELD` -> `PP_INJECTION_FINE_MATTE` + `NT_PP_FINE_MATTE`
- `MAT_PP_SECONDARY` -> same PP family
- `MAT_PP_UI` -> same PP family; no project-local UI roughness offset during R02
- `MAT_PU_CONTACT` -> TPE/PU soft-matte optical method; **OVERMOLDING is not adopted as an XJ01 process fact**
- `MAT_IRON_VISIBLE` -> coated-steel / powder-coat visual baseline candidate; actual XJ01 coating remains pending and powder microtexture stays disabled
- `MAT_METAL_HARDWARE` -> generic conductor fallback; exact hardware finish/process unknown

## R02 lock

Surface response is locked across CURRENT_REF / NEUTRAL_DIAG / A_LIGHT / A_DEEP. Geometry, camera, focal length, pose, lighting, exposure, background and scale are also locked. R02 changes color-role variables only; it does not open Finish/Texture.

## Gate invalidation

R02-01 accepts an R02-00 gate only when both the Surface System `resolved_version` and `active_manifest_sha256` match the currently resolved system. Updating the global Surface System therefore forces a controlled rerun instead of silently reusing an old visual decision.

## Current evidence boundary

The current R02-00 pass is a digital preview gate under Blender 5.2 LTS / Cycles. It does not validate physical PP, PU, coated iron, wet/dirty/aged states, production tolerance or user preference.
