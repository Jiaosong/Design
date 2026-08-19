# CH14-P06 v2.0｜Map-derived Graphic Language

Status: `EXECUTED / MAP-AUTHORITY-REBOUND / BROWSER READBACK COMPLETE / INDEPENDENT PROFESSIONAL DESIGN GATE PENDING / NO_PROMOTION`

## Why v2 replaces v1
P06 v1 introduced an abstract brand LINE even though C04 already has a single locked current route object. That would create a second route geometry. v1 is therefore `SUPERSEDED / PROVENANCE ONLY`.

## Current authority
- Route object: `ROUTE-03`
- Artifact: `ROUTE_03_QINGJIANG_ROUTE_CURRENTIZED`
- Upstream PR: `#192`
- Upstream commit: `128b9069c686b9a8ab65d6425fa928890f0604dc`
- Locked SVG SHA256: `44bde5dfd82bcc6435b1aa40fb9a61d3fb99b281c93e7d0e41bdf4a38e4aec75`
- Geometry policy: `NO MUTATION / EXCERPT + CROP + STYLING ONLY`

## P06 v2 grammar
`ROUTE-03 → LINE / TRACE / NODE-PAGE RELATION + STONE SEAL IDENTITY`

- LINE = exact ROUTE-03 main path.
- TRACE = the same path at lower visual authority.
- Branch / short loop / Return loop = exact source path data.
- PAGE may attach to a source-bound node but never owns route order. Current example uses 蝴蝶崖 `(517.8, 363.9)`.
- SEAL remains P03 identity authority and does not become a map-node family.
- Wide / Tall / Square are crops of the same geometry; there is no responsive redraw.

## Handoff boundary
- P06 owns route-derived brand grammar, crop hierarchy, PAGE relation and identity anchor.
- P07 owns map legend, icons, signage, information decoding, App/paper-map usability and functional contrast/state semantics.
- P08 owns the final `FULL / LIGHT / TRACE / OFF` presence scale.

## Readback
Actual Chromium readback completed at:
- `1920×1080`
- `390×844`
- desktop full long page
- mobile full long page

No horizontal overflow; 10/10 sections and image loads checked.

## Recoverable local package
`C04_CH14_P06_v2_0_MAP_DERIVED_GRAPHIC_LANGUAGE.zip`

SHA-256: `7a536111e28e4ea49fca6aeec8d2422f0ae7ae981dac236345d4e50fc2e015ab`

## Boundary
`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT GPS`.

Artifact/readback success does not equal independent Design PASS. No image generation used.