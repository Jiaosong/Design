# CH08-S01 v1.3｜Producer Actual-Pixel Readback

State: `PRODUCER CANDIDATE / NO SELF-KEEP / INDEPENDENT PROFESSIONAL DESIGN REVIEW PENDING / NO_PROMOTION`.

## Skill-driven material delta from v1.2
- `oleander-story-and-board`: real Qingjiang is given more visual authority; title scale is reduced; decorative vertical TRACE is removed; WASH no longer obscures as much of the main karst; mobile landscape-first share increases from 48svh to 52svh.
- `oleander-delivery-qc`: rerendered target desktop/mobile and all operation-off attack states after the last visual edit.
- Image Ops remains the non-generative downstream method: `WASH-TONAL → WASH-MASK → INK-EDGE`.

## Current source
`SRC05 / 5pszhdcxjz.jpg` — SHA256 `da94acea1ae3d7961919a390f9f0ef27ceee2b06bdaf5dd897ee63fb95897f4b` — semantic slot `CH08-S01-MAIN` — generation `OFF`.

## Runtime readback
Desktop `1920×1080`: overflow `0` / broken images `0` / recorded errors `0` / photo rect `{x:530.078125,y:191.5,width:1323.921875,height:648}`.

Mobile `390×844`: overflow `0` / broken images `0` / recorded errors `0` / full scrollHeight `1299` / photo rect `{x:0,y:64,width:390,height:438.875}`.

Operation attack deltas vs current desktop:
- ALL FX off mean abs RGB `9.6632`; changed ratio `0.4136`.
- TONAL off mean abs RGB `3.769`.
- WASH off mean abs RGB `9.6565`.
- EDGE off mean abs RGB `0.7261`; changed ratio `0.232931`.

All reported Image Ops changed-pixel bboxes remain inside the photograph carrier. Producer does not issue `KEEP / MAIN KEEP / Professional Design PASS`.

Open independent questions: first-read portfolio strength, source-resolution acceptability at desktop scale, and whether the wash/edge treatment adds material project specificity rather than styling only.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`
