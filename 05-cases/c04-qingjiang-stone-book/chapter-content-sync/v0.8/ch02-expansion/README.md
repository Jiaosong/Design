# C04 CH02 Expansion v0.8

Project: `PRJ-C04-QINGJIANG-SHISHU`
Chapter: `CH02｜场地与山水分析`
Status: `EXECUTED / PRODUCER ACTUAL-PREVIEW COMPLETE / INDEPENDENT PROFESSIONAL DESIGN REVIEW REQUIRED / NO_PROMOTION`

## Scope
This change preserves the current `CH02-P01–P05` authoring units and adds four independent page units under the existing NO COMPRESSION / NO LOSS rule:

- `CH02-P06｜Climate + Visibility`
- `CH02-P07｜Rain–Flood–Geohazard Coupling`
- `CH02-P08｜Analytical Raster Frontier`
- `CH02-P09｜Environment → Experience Matrix`

No existing route geometry, R06 decision, R13 body-first/Return decision, or project truth boundary is modified.

## Data / truth boundary
- `ROUTE-03 = LOCKED CURRENT` remains the single current route carrier.
- `ENV-03 WorldCover` and `ENV-04 JRC Global Surface Water` remain `SOURCE VERIFIED / AOI UNBOUND / HOLD / NO MAIN PROMOTION`.
- A textual location reference can place 红花峰林 on the Qingjiang south bank in 新塘乡保水溪村巴漏雨组 and reports an area of about `5.96 km²`, but this is **not** a surveyed or GIS polygon and is not used to guess an analytical AOI.
- Required raster closure path remains: `REAL RASTER BYTES → CRS / DATUM / NoData readback → TRUSTWORTHY AOI BINDING → AOI crop → derivation/statistics → actual preview → independent review`.

## Production
- `image_generation_used = false`.
- Native authoring format: editable `1920×1080 SVG` with live vector text.
- Local rendered preview set: `4 × PNG + contact sheet`.
- Producer actual-preview found and repaired one P09 footer/matrix collision before final local packaging.
- Producer preview is execution evidence only; it does not issue an independent `KEEP / MAIN / Design PASS`.

## Local canonical export receipt
Package: `C04_CH02_EXPANSION_v0.8.zip`
Bytes: `1,226,241`
SHA256: `c8f32a13de2218adffd1c65af852391c9265808e4ad57d9d2c7d6897ba51d2bc`

Local SVG SHA256:
- P06 `c20c71eedcb4d6892be3ba032a33bdc8f0e86ecb6fe708e4f02cc318b1e8fc9f`
- P07 `2f68f2a86dda05ddb58621f41791eda8fd6699e5b6087aff80d30534e9b7b680`
- P08 `3f004abade643d18cb6faa11d5424554cae6f664b8d0517522419386132b95ad`
- P09 `d31d1a0c9b3d03ef006299b2fec0662f6efaa7b1923318f6b29ea7c9a1fa9ce3`

## Repository serialization note
P07 is byte-equivalent to the local SVG (`Git blob 1a1fa10ff8a13cab0afb5a71b4bb2ca0e303a026`). P06/P08/P09 are repository-side vector serializations of the same authored page content but are **not claimed byte-equivalent** to the locally packaged SVG bytes; therefore the local package hashes above must not be used as GitHub blob hashes. This is explicitly recorded rather than silently claiming persistence equivalence.

## Gates
`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS`

`Artifact existence ≠ Design quality`  
`Traceability ≠ Professional finish`  
`Evidence correctness ≠ Visual excellence`  
`Process PASS ≠ MAIN KEEP`
