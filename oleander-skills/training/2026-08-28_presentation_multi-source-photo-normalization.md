# PRESENTATION Practice Evidence — Multi-source Photo Normalization

Status: `PRACTICE_EVIDENCE / REAL-PHOTO MULTI-SOURCE / NO PROJECT WRITE / NOT ACTIVE`
Mode: `TRAINING_MODE`

## GAP
Different-source photographs often need to appear as one presentation sequence, but there are two common failures: each frame is independently beautified until the series drifts, or one brand LUT/tint is imposed on every source and erases native light, skin, sky, and material color.

## SOURCE
Professional calibration: Aperture magazine design refresh / A2/SW/HK. Aperture's own design discussion identifies flow, rhythm, image juxtaposition and sequencing as key design concerns, and explicitly notes that established guidelines may be abandoned when the work requires it. Transfer only the sequencing principle; do not copy its styling.

Training material: three real, non-generated photographs with different native light/color conditions (`skimage.data.coffee()`, `rocket()`, `astronaut()`). No compositing, no generative fill.

## ARTIFACT
Editable HTML/CSS + source-bound derivatives + real Chromium desktop/mobile readback + thumbnail/contact sheet + grayscale + tonal readback.

## A/B
- A — each frame optimized independently; family drifts.
- B1 — one warm LUT applied to all; creates false unity and pushes skin/sky/materials toward one cast.
- B2 — bounded luminance normalization only; native white balance / hue family remains source-specific.

## READBACK
A reads as three separately art-directed images. B1 is visually coherent but materially false: the same warm cast becomes the dominant family cue. B2 keeps the warm material image, cool night exterior, and skin/white-suit image visibly distinct while narrowing only tonal discontinuity. Desktop/mobile and grayscale preserve the three-image sequence without forcing equal color identity.

## FAILURE / ROOT CAUSE
Consistency was mistaken first for per-image polish and then for one global chromatic style. Both approaches treat source truth as subordinate to presentation identity.

## REPAIR / RETEST
Normalize only what can safely be shared: bounded exposure / black-floor continuity. Preserve source-native color relationships when they carry material, place, skin or light truth. Reopen as a contact sheet, grayscale sequence and responsive page rather than approving frames one by one.

## TRANSFER RULE
`LOCK SOURCE TRUTH → HARMONIZE ONLY SHARED TONAL BOUNDS → PRESERVE NATIVE COLOR/LIGHT → RETEST AS SEQUENCE`

`MULTI-SOURCE CONSISTENCY ≠ ONE LUT / ONE WHITE BALANCE`

## BOUNDARY
- Training sources are not project evidence.
- Project material/site/skin/product colors remain authoritative.
- No crop may delete claim-bearing evidence.
- No compositing or generative fill may fabricate continuity.
- Exposure/black-floor adjustment must remain bounded and may not convert day/night, material class, skin tone, or site color into a house style.
- This evidence does not promote `oleander-image-art-direction` or `oleander-visual-design` from Candidate status and does not create project authority.
