# C04 CH16 v1.1｜OLEANDER Skill-routed Detail Development

Current authoring range: `CH16-P01...P07 / 088–094`.

## Execution routing

Resolved through Current `KN-METHOD-OLEANDER-SKILL-RESOLVER-001`.

Minimum sufficient execution DAG:
- `oleander-story-and-board` — installed; chapter/board hierarchy, existing-evidence-first, same-source presentation.
- `oleander-data-viz` — installed; geometry/source authority separation, semantic diagram, vector/readback workflow.
- Technical Drawing Current Method / candidate body — **not installed / not promoted**; used for spatial translation, structural lineweight and parent→child detail registration only.

No new Skill was created.

## Material delta from v1.0

1. One shared `R06-SUPPORT-CONCEPT` geometry master now drives P01/P03/P04/P05/P06/P07.
2. P02 no longer resembles an invented site plan. Source carrier remains insufficient for exact location, therefore `LOCATION OPEN` and relationship-only spatial model are explicit.
3. P03 becomes registered parent view `CH16-P03-SEC-A`.
4. P05 is child detail `D01`, registered to P03; orientation / ordering / sidedness are preserved while component and fixing information is added.
5. P04 and P06 bind material / failure claims to component IDs `C01–C05`.
6. P07 places the Open Register beside the registered parent→child chain and includes a label-off return test.

## Shared concept geometry

`R06-SUPPORT-CONCEPT`
- width: 1200 mm
- depth: 160 mm
- top height: 975 mm

These are `DESIGNER ESTIMATE / CONCEPT INTERFACE / NTS / FIELD OPEN`, not field measurements.

Components:
- `C01 CONTACT`
- `C02 SUPPORT`
- `C03 BUFFER`
- `C04 CLAMP / FASTENER`
- `C05 EXISTING BASE`

## Readback

Executed locally on the production package:
- 7 × 1920×1080 SVG/PNG pages
- grayscale attacks
- 50% compact attacks
- Web readback 1920×1080: no overflow, 7/7 images loaded, 0 page errors
- Web readback 390×844: no overflow, 7/7 images loaded, 0 page errors

Production ZIP SHA-256: `76bf2ee19d52fe3242ad266d70aec9ea0b0cd16e7da3d30857a4f37fa7be2492`

## Boundaries

- CH16 remains Design Detail Development; CH17 owns technical/model/engineering proof.
- R06 experience remains frozen / no reopen.
- A1 support remains `NOT LOCATED`.
- No survey geometry, structure capacity, anchor/foundation capacity, wet-slip performance or approval claim.
- No image generation used.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`

`ARTIFACT EXISTS != DRAWING PASS != ENGINEERING PASS != FIELD PASS != MAIN KEEP`

Independent Professional Design Gate remains `PENDING`.