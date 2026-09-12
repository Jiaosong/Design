# CH08-S01 v0.9｜Producer Actual-Pixel Readback

State: `PRODUCER CANDIDATE / NO SELF-KEEP / INDEPENDENT PROFESSIONAL DESIGN REVIEW PENDING / NO_PROMOTION`

## Current source allocation
- underlying source: `SRC05 / 5pszhdcxjz.jpg`
- source SHA256: `da94acea1ae3d7961919a390f9f0ef27ceee2b06bdaf5dd897ee63fb95897f4b`
- semantic slot: `CH08-S01-MAIN`
- generation: `OFF`
- source identity unchanged from v0.8. This revision does not create a second Web image slot.

## Material visual delta
- removes the hard 32% full-height editorial split from v0.8;
- real Qingjiang source now occupies the entire desktop viewport;
- paper color becomes a left-side reading wash over the same scene rather than a separate panel;
- the claim remains one sentence: `先看见清江，系统才有资格出现。`;
- mobile remains image-first, then copy; it is a responsive variant of the same semantic slot.

## Chromium readback
Desktop `1920×1080`: scrollWidth 1920 / clientWidth 1920 / horizontal overflow 0 / broken images 0 / recorded console+page errors 0.

Mobile `390×844`: scrollWidth 390 / clientWidth 390 / full scrollHeight 944 / horizontal overflow 0 / broken images 0 / recorded console+page errors 0.

Direct file navigation remains runtime-blocked; exact authored HTML/CSS was executed through `page.set_content` with the exact source image bytes encoded as data URI for readback. This is actual pixel evidence, not live-navigation PASS.

## Review boundary
No producer `KEEP / MAIN KEEP / Professional Design PASS`. Independent review must inspect native desktop/mobile pixels, grayscale hierarchy, source softness at 1920, Qingjiang specificity, typography, deletion test and portfolio worthiness.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`
