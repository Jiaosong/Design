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

### Project Web image uniqueness check

For every OLEANDER project Web, run a **whole-project** image-source uniqueness audit before release.

- Build/read the Web image-use ledger and group content imagery by `SOURCE_ASSET_ID` and, when available, `SOURCE_SHA256` or another stable upstream source identity.
- The same underlying content-image source may occupy only one semantic Web image slot in the project.
- A second use is blocking even if crop, ratio, resize, color grade, filter, mask, text overlay, frame, or breakpoint presentation differs. These are presentation derivatives, not new source imagery.
- Responsive renders of the same semantic slot are one use, not duplicates.
- Repeated brand marks, functional UI icons, navigation symbols, and system texture tokens are excluded unless used as content imagery.
- If a repeated subject is required, replace the repeated source with a genuinely different photograph/render/evidence asset, or a different medium such as SVG/map/diagram/model/technical drawing/chart.
- For a same-source reveal on Web, bind the base image once and change state/layers in the same semantic component instead of creating separate duplicate image slots.

**Blocking rule:** `same underlying content-image source in 2+ project-Web slots = FAIL / REVISE`.

## Gate 4: video and audio

Use MediaInfo, FFmpeg/ffprobe, and ExifTool to check container, codec, duration, dimensions, pixel aspect, frame rate, scan type, bitrate, chroma, bit depth, color primaries/transfer/matrix, audio codec, sample rate, channels, subtitles, and metadata.

Compare the result with the delivery specification. Detect black frames, silence, clipping, missing audio, unexpected variable frame rate, and duration mismatch where practical.

## Gate 5: 3D and interactive

- Open the exchange file in a clean context when possible.
- Check scale, origin, axis, geometry count, materials, textures, caches, plugins, cameras, animation range, and relative paths.
- Confirm preview/thumbnail and manifest match the packaged asset.
- For websites or interactive charts, check local assets, responsive layout, keyboard access, missing links, and offline behavior if required.
- For project Web, include the final image-use ledger and duplicate-source scan result in the release evidence.

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

