# CH08-S01 v1.5｜Producer Actual-Pixel Readback

State: `PRODUCER CANDIDATE / CH14 CORRECTION / NO SELF-KEEP / INDEPENDENT PROFESSIONAL DESIGN REVIEW PENDING / NO_PROMOTION`.

## Material delta from rejected v1.4
- removes v1.4 monochrome/teal watercolour-like takeover;
- restores real Qingjiang photography as first-read;
- removes faux paper scanline texture and page-level pseudo-ink atmosphere;
- image becomes a restrained contemporary editorial print plate: narrow Bone Mist carrier + hairline boundary + no drop-shadow/card float;
- CH14 P08 presence reduced to TRACE; no new Seal/LINE/TRACE geometry is introduced;
- Image Ops remain deterministic and reversible but visually subordinate to the source.

## Source lock
- `SRC05 / 5pszhdcxjz.jpg`
- source SHA256: `da94acea1ae3d7961919a390f9f0ef27ceee2b06bdaf5dd897ee63fb95897f4b`
- semantic slot: `CH08-S01-MAIN`
- source natural size: `1080×608`
- generation: `OFF`

## Chromium readback
Desktop 1920×1080: horizontal overflow `0` / broken images `0` / recorded errors `0`.

Mobile 390×844: horizontal overflow `0` / broken images `0` / recorded errors `0` / scrollHeight `1316`.

Small 320×700 attack exists. Grayscale and print-mono readbacks exist. Source / tonal / wash / final stage readbacks exist.

Image-stage pixel deltas (desktop page):
- source→tonal mean abs RGB `2.2423`
- tonal→wash `0.2528`
- wash→final `0.188`
- source→final `2.2465`

This readback proves execution/render integrity only. It does not prove Professional Design KEEP, source-resolution sufficiency for every downstream scale, field truth or release approval.
