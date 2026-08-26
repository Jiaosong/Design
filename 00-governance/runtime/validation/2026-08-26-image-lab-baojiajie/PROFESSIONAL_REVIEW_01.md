# Image Lab｜Professional Review 01

Date: 2026-08-27
Surface: `browser_image_lab`
Review method: artifact-first. Reviewed `IMAGE_LAB_BAOJIAJIE_WORKING_DERIVATIVE.png` and the corresponding Before readback before reading runtime code or producer receipt.
Verdict: **REVISE / RETEST REQUIRED / ACTIVE NOT GRANTED**

## Artifact-first verdict
The runtime can produce a technically valid derivative from locked source bytes, but the reviewed derivative does not yet demonstrate professional image-treatment judgment. It reads as a zoomed crop of an existing social-media four-image grid rather than a deliberate retail/brand image composition. Subject hierarchy is weak, important figures/products are clipped by the frame, and the runtime provides no target-carrier, crop-safe/focal, or clipping diagnostics to prevent these failures.

## Findings
### I01｜Critical｜No target output intent or carrier ratio
The runtime is hard-wired to a 1600×1200 / 4:3 canvas. The reviewed Baojiajie derivative therefore has no explicit relation to a real carrier such as POP card, web module, social crop, slide, or product detail slot.

**Root Cause:** canvas size/ratio is implementation default rather than a project input.

**Feedback Action:** make target width/height or ratio explicit and record `output_role / target_px / aspect_ratio` in config. Provide bounded presets only as convenience; project target remains authoritative.

**Retest Evidence:** same source can be reopened into at least two declared target ratios while preserving source SHA and producing distinct, traceable crops.

### I02｜Critical｜No focal anchor / crop-safe system; framing clips subjects and product evidence
The reviewed 4:3 derivative cuts figures and package/product elements at the right and bottom edges and retains gray gutters. Scale/Offset numeric controls alone do not provide a professional first-read or crop-safety workflow.

**Root Cause:** transform is controlled only by canvas-pixel scale/offset; there is no focal anchor, safe-area overlay, visual crop boundary, or cover/contain policy.

**Feedback Action:** add focal-point/crop-anchor controls, visible crop-safe overlay, `cover / contain / manual` fit mode, and drag-to-reframe. Keep all transforms non-destructive and source-relative.

**Retest Evidence:** artifact-first review at target size can identify one deliberate primary subject, no accidental edge cuts of the chosen subject, and no unintended gutters unless explicitly requested.

### I03｜High｜No highlight/shadow clipping diagnostic
Brightness/contrast/saturation can materially change tonal distribution, but the runtime exposes no histogram or clipping warning. The reviewed derivative uses brightness 104 / contrast 118 / saturation 108; external pixel inspection finds non-zero extreme dark clipping, but the runtime itself provides no way to distinguish deliberate density from accidental loss.

**Root Cause:** filter controls have no image-integrity readback layer.

**Feedback Action:** add lightweight luminance diagnostics: shadow-clipped %, highlight-clipped %, and optional overlay/warning. This is a diagnostic, not an automatic correction.

**Retest Evidence:** extreme settings trigger clipping warnings; neutral/reset returns the diagnostic to baseline; ordinary treatment can be reviewed with the warning state visible.

### I04｜High｜Transform is not portable across target sizes
Config records `scale=160, offsetX=100, offsetY=-80` in a fixed 1600×1200 canvas. These values do not define a source-relative crop that can survive a different target ratio or canvas size.

**Root Cause:** framing transform is canvas-pixel based rather than normalized/source-relative.

**Feedback Action:** persist normalized focal coordinates and source-relative scale/crop transform in addition to current human-readable controls.

**Retest Evidence:** reopen config at the same target reproduces the same crop; changing target preserves focal intent without silently reusing invalid pixel offsets.

### I05｜Medium｜A/B review is toggle-only, not comparison-ready
The true-source-fit Before mode is correct, but a toggle forces memory-based comparison. For professional image treatment, the reviewer needs a split/wipe or side-by-side diagnostic to judge crop, contrast, saturation and tonal loss without relying on memory.

**Root Cause:** Before was repaired as a truth function, but not developed into a visual review instrument.

**Feedback Action:** add a bounded `COMPARE` mode (split or side-by-side) that always uses true source fit versus current derivative; export remains derivative-only.

## What is already acceptable
- Source bytes are SHA-locked and read-only.
- Invalid/no source fails closed; empty gray export is blocked.
- Before is true source fit rather than filter-only reset.
- Config records source MIME/bytes/SHA/dimensions and derivative truth boundary.
- Individual filter and transform controls have actual pixel effect.
- No AI generation or source-authority replacement occurs.

These are functional/evidence strengths, not a substitute for professional image-composition quality.

## Decision
`REVISE`.

Do **not** promote Image Lab to ACTIVE. Required next transaction:

`I01–I05 repair → same-source browser A/B → declared target-ratio readback → clipping diagnostic retest → artifact-first professional retest → then reconsider promotion`.

Source Authority remains unchanged and all output remains derivative-only.
