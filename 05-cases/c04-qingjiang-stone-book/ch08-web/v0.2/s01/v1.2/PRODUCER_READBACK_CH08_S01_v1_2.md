# CH08-S01 v1.2｜Producer Actual-Pixel Readback

State: `PRODUCER CANDIDATE / NO SELF-KEEP / INDEPENDENT PROFESSIONAL DESIGN REVIEW PENDING / NO_PROMOTION`.

## Material delta from v1.1
- preserves the accepted large composition and copy hierarchy;
- strengthens the Current `T-VISUAL-IMAGE-OPS-001` chain as `WASH-TONAL → WASH-MASK → INK-EDGE`;
- WASH-TONAL now uses a recoverable 8-band tonal overlay plus restrained desaturation/contrast rather than a light photo grade only;
- WASH-MASK replaces the regular left fog/linear wash with asymmetric Bone Mist absorption fields and a bounded paper-print veil;
- INK-EDGE is stronger but spatially bounded to the main karst and selected river/shore relation, not the full image;
- no image generation, source replacement, geometry reconstruction, object insertion or source-byte overwrite.

## Current source allocation
- `SRC05 / 5pszhdcxjz.jpg`
- source SHA256: `da94acea1ae3d7961919a390f9f0ef27ceee2b06bdaf5dd897ee63fb95897f4b`
- semantic slot: `CH08-S01-MAIN`
- generation: `OFF`

## Chromium readback
Desktop `1920×1080`: overflow `0` / broken images `0` / recorded console+page errors `0`.

Mobile `390×844`: overflow `0` / broken images `0` / recorded console+page errors `0` / full scrollHeight `1277`.

Operation attack tests:
- ALL FX off delta mean abs RGB = `11.478`; changed ratio = `0.411415`.
- TONAL off delta mean abs RGB = `3.2661`.
- WASH off delta mean abs RGB = `12.1569`.
- EDGE off delta mean abs RGB = `0.942`; changed ratio = `0.23712`.

The changed-pixel bounding boxes remain inside the photograph region; no copy/metadata/route geometry is produced by Image Ops.

## Producer observation only — not verdict
The treatment now reads materially closer to a printed Qingjiang plate: the photo is less screen-luminous, the left transition is no longer a single digital gradient, and the central karst receives a selective structural second-read. This observation is not a `KEEP / MAIN KEEP / Professional Design PASS`.

Independent review must still judge whether the treatment is materially useful rather than styling-only, whether the source resolution remains acceptable at the display size, and whether the first-read balance is portfolio-worthy.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.
