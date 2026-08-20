# C04 CH01 v1.4｜Actual Pixel Readback

Role: `MACHINE / RUNTIME / PRODUCER PRE-REVIEW EVIDENCE`; not an independent Design verdict.

## Exact source
- `index.html` — 14,682 bytes — SHA256 `290ab5dcb5f68e700e13083535518ebc1aeb360066f0fa1b5bf76c3dda96de8a`
- `style.css` — 17,560 bytes — SHA256 `cb4c415ba24a3e1264c02743c912cc5c9d509ee1614aeea9a9c38967e3015a5d`

## Chromium readback
Desktop:
- `6/6` surfaces at `1920×1080`
- `scrollWidth = 1920`
- raster `<img>` count = `0`
- browser console/page errors = `0`

Mobile:
- `6/6` surfaces at `390×844`
- `scrollWidth = 390`
- raster `<img>` count = `0`
- browser console/page errors = `0`

Review derivatives:
- desktop contact SHA256 `d12a99d184fc2322aee5ff87bdd3ba2d1671ef61e6ca2a7639bbe949f06e878c`
- mobile contact SHA256 `19351f94b3f55a109ffd28ba32f8afab25aa3a756bd07d93ef63e626c1b3e9b4`
- grayscale contact SHA256 `db9fca9fc1c94dbf130958be8c15d98ea429ca26492272995b735c4dbd3b7583`
- 50% far-read SHA256 `c2092e682825d42df90f87157231a4ba3c40117f1938f0a2d2e3dbdc5aa0d6b2`

## Authority checks
- six PR #294 CH01 units preserved; no compression.
- P02 route line = exact excerpt from locked ROUTE-03 source; no geometry mutation.
- P01 relation field = presentation metaphor, explicitly not route geometry.
- P05 aperture field = service-gap metaphor, no route line / fake location.
- Brand color is not used to assert operational state.

## Gate state
`RUNTIME / SOURCE-BOUNDARY PRECHECK = COMPLETE`
`INDEPENDENT PROFESSIONAL DESIGN REVIEW = UNAVAILABLE / HOLD`
`CURRENT / PROMOTION = UNCHANGED`
