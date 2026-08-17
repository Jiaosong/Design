---
name: oleander-delivery-qc
description: Perform final technical, visual, metadata, dependency, licensing, and package checks for Oleander deliverables. Use whenever the user mentions Oleander final checks, delivery review, preflight, missing fonts or links, PDF inspection, image DPI/ICC, video codec/frame-rate/color/audio checks, model texture dependencies, file naming, archive completeness, MediaInfo, ExifTool, Ghostscript, FFmpeg, or release sign-off.
compatibility: Uses MediaInfo 26.05, ExifTool 13.59, Ghostscript 10.07.1, FFmpeg, ImageMagick, PDF tools, and the Oleander Python environment.
---

# Oleander Delivery QC

Treat QC as a reproducible release gate. Inspect without modifying masters unless the user explicitly requests a repair; write corrected derivatives separately.

## Gate 1: package integrity

- Expected folders and deliverables exist.
- Names, versions, dates, and status markers follow the project convention.
- No temporary, autosave, cache, proxy, or obsolete final files are mixed into delivery.
- Checksums are produced for final immutable files when appropriate.

## Gate 2: research and rights

- Important claims link to approved evidence.
- Credits, licenses, model releases, font rights, music rights, and stock licenses are present.
- Confidential or personal information is not unintentionally included.

## Gate 3: images and boards

Check dimensions, effective DPI, aspect ratio, ICC profile, alpha, bit depth, compression, missing links, missing fonts, overset text, bleed, trim, and safe margins. Render PDFs to images for visual comparison when needed.

## Gate 4: video and audio

Use MediaInfo, FFmpeg/ffprobe, and ExifTool to check container, codec, duration, dimensions, pixel aspect, frame rate, scan type, bitrate, chroma, bit depth, color primaries/transfer/matrix, audio codec, sample rate, channels, subtitles, and metadata.

Compare the result with the delivery specification. Detect black frames, silence, clipping, missing audio, unexpected variable frame rate, and duration mismatch where practical.

## Gate 5: 3D and interactive

- Open the exchange file in a clean context when possible.
- Check scale, origin, axis, geometry count, materials, textures, caches, plugins, cameras, animation range, and relative paths.
- Confirm preview/thumbnail and manifest match the packaged asset.
- For websites or interactive charts, check local assets, responsive layout, keyboard access, missing links, and offline behavior if required.

### Gate 5.1: interaction state legibility

For websites, mini-programs, interactive charts, prototypes and component libraries, do not reduce keyboard access to a binary functional check. Inspect the visible and semantic state model.

- Compare `default / hover / focus / pressed-or-selected / disabled / error` where those states exist. They must not collapse into near-identical appearances when the distinction affects use.
- Keyboard focus must remain visibly locatable. Do not accept `outline: none` unless a clearly visible author-supplied focus indicator replaces it.
- Use the WCAG 2.2 Focus Appearance geometry as a strong calibration target: a visible indicator at least comparable to a 2 CSS px perimeter, with sufficient state contrast. Record this as a calibration check unless the complete interface has actually been tested for conformance.
- Pointer targets must satisfy the applicable product/accessibility requirement. As an OLEANDER practice default for primary controls, aim for at least `44 × 44 CSS px`; never describe this practice default as the WCAG 2.5.8 minimum, whose baseline is `24 × 24 CSS px` subject to its exceptions.
- State meaning must not depend on motion alone. A static frame should still distinguish important states.
- Disabled controls must look unavailable without becoming illegible; selected/pressed controls must remain distinguishable from hover.
- Preserve native semantics when practical (`button`, `aria-pressed`, labels, disabled state) instead of rebuilding controls as visually styled generic containers.
- Separate visual proof from runtime proof. A design board or screenshot may verify state differentiation, but cannot prove focus order, keyboard operation, screen-reader naming, responsive behavior or full WCAG conformance.

A technically clickable interface is `REVISE` when state hierarchy is visually ambiguous, focus is invisible, or the design claims accessibility without runtime evidence.

## Report format

Use:

1. Release candidate and specification
2. Pass/fail summary
3. Blocking defects
4. Non-blocking warnings
5. File-by-file evidence
6. Required fixes and owner
7. Recheck results
8. Final sign-off status

Never mark a deliverable approved while blocking defects remain.
