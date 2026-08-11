# OLEANDER Blender Surface System｜v1.19.0｜Evidence Acquisition & Parameter Promotion Gate

Status: REVIEW / STACKED ON v1.18.0 / NOT MERGED
Primary: IP03
Supporting: SP03

## Purpose
Obtain project-specific evidence before activating physical material/process parameters.

## First-pass result
- 4 project-definition promotions to `P2 PROJECT_DEFINED`.
- 0 physical parameter promotions.
- 6 Evidence Acquisition Requests.

Promoted only as project definition:
1. XJ01 PP Main Field material family = PP.
2. XJ01 PP Main Field process = injection molding.
3. XJ01 PU Contact material family = PU.
4. XJ01 Iron Tube substrate identity = iron tube.

Held:
- XJ01 PP roughness / feature-size hierarchy remains `VISUALIZATION_LOCKED`.
- XJ01 powder coating remains `BLOCKED` / sample hypothesis.
- Timer Housing / Knob / Diffuser remain `VISUALIZATION_LOCKED` for physical identity/process/optics.

## Promotion ladder
`P0 UNKNOWN_OR_BLOCKED → P1 VISUALIZATION_LOCKED → P2 PROJECT_DEFINED → P3 SUPPLIER_DOCUMENTED → P4 SAMPLE_CALIBRATED → P5 PRODUCTION_VALIDATED`

## Evidence policy
External manufacturer/industry references are `REFERENCE_ONLY` unless the project identifies the exact supplier/product/grade/process. Blender render parameters remain representation controls and are never relabeled as physical measurements.

## Acquisition priority
P0:
- XJ01 exact PP grade / supplier / mold-finish sample.
- XJ01 exact PU system / supplier / process.
- XJ01 iron-tube coating chemistry / TDS / coupon.
- Timer diffuser exact polymer / grade / thickness / transmittance / haze.

P1:
- Timer housing exact material grade / finish / molded sample.
- Timer knob alloy / brush / anodize designation / sample.

Reality boundary: no new measured CMF, coating, optical, manufacturing or user claims are introduced by this PR.
