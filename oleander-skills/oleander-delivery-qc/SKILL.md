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

### Source-independent visual QA fallback

Do not make visual design review depend on a single authoring application's screenshot/export service.

If the native authoring tool cannot provide a visual readback because of quota, connection, plugin, browser, or runtime limits, but the artifact itself is deterministic and faithfully renderable, use an independent renderer/viewer and continue the visual gate.

Required fallback sequence:

`SOURCE ARTIFACT → IDENTITY/DIMENSION CHECK → INDEPENDENT RENDER → REOPEN → DESIGN CRIT → VERDICT`

Examples include SVG → CairoSVG/browser rasterization, HTML → browser screenshot, PDF → independent PDF rasterizer, image → independent image viewer, and video → FFmpeg frame extraction.

The fallback view must preserve the intended canvas/aspect ratio and must be traceable to the source artifact. Record renderer/tool, output dimensions, and checksum when practical.

A source-tool screenshot failure is **not** by itself a reason to mark Professional Design / Visual QA `HOLD` when a faithful independent view can be produced.

Keep `HOLD` when:
- no faithful view can be generated;
- the fallback changes layout, fonts, color, geometry, timing, or state materially;
- the review question depends on authoring-tool-only evidence such as hidden layers, native editability, component structure, interactive state, 3D scene state, or source-specific behavior.

Never use fallback rendering to claim facts it does not prove. A rendered PNG can prove visible composition but cannot prove the health of the native source file.

## Gate 4: video and audio

Use MediaInfo, FFmpeg/ffprobe, and ExifTool to check container, codec, duration, dimensions, pixel aspect, frame rate, scan type, bitrate, chroma, bit depth, color primaries/transfer/matrix, audio codec, sample rate, channels, subtitles, and metadata.

Compare the result with the delivery specification. Detect black frames, silence, clipping, missing audio, unexpected variable frame rate, and duration mismatch where practical.

## Gate 5: 3D and interactive

- Open the exchange file in a clean context when possible.
- Check scale, origin, axis, geometry count, materials, textures, caches, plugins, cameras, animation range, and relative paths.
- Confirm preview/thumbnail and manifest match the packaged asset.
- For websites or interactive charts, check local assets, responsive layout, keyboard access, missing links, and offline behavior if required.

### Gate 5.1: interaction-state legibility

For websites, mini-programs, interactive charts, prototypes and component systems, do not reduce keyboard/accessibility review to a binary “clicks/does not click” check. Inspect both the visible state model and the runtime evidence appropriate to the release claim.

Visible-state review:

- Compare `default / hover / focus / pressed-or-selected / disabled / error` where those states exist. States that change operation or meaning must not collapse into near-identical appearances.
- Keyboard focus must remain visibly locatable. Do not accept removal of the user-agent focus indicator unless a clearly visible author-supplied replacement remains available.
- Selected/pressed state must remain distinguishable from hover. Disabled controls should look unavailable without making necessary labels illegible.
- State meaning must not depend on motion alone when a static visual carrier is needed for comprehension or reduced-motion use.
- Preserve native semantics where practical (`button`, labels, `disabled`, `aria-pressed` or other appropriate state semantics) rather than rebuilding every control as a generic styled container.

WCAG 2.2 calibration boundary:

- SC 2.4.7 Focus Visible is a **Level AA** requirement for a visible keyboard focus indicator mode.
- SC 2.4.13 Focus Appearance is a **Level AAA** calibration target: when visible, an area of the focus indicator is at least as large as the area of a `2 CSS px` perimeter of the unfocused component/sub-component and has at least `3:1` contrast between the same pixels in focused and unfocused states, subject to the criterion's exceptions.
- SC 2.5.8 Target Size (Minimum) is **Level AA** with a baseline `24 × 24 CSS px` target, subject to its spacing/equivalent/inline/user-agent/essential exceptions.
- `44 × 44 CSS px` is associated with SC 2.5.5 Target Size (Enhanced), **Level AAA**, subject to its exceptions. OLEANDER may use 44 px or larger as a product/practice target, but must not call it the SC 2.5.8 minimum or infer AAA conformance from target size alone.

Separate proof classes:

`STATIC VISUAL PROOF ≠ RUNTIME KEYBOARD PROOF ≠ ACCESSIBLE NAME/ROLE/VALUE PROOF ≠ RESPONSIVE/DEVICE PROOF ≠ WCAG CONFORMANCE`.

A screenshot or design board can support visible differentiation, but cannot by itself prove focus order, keyboard activation, accessible naming, screen-reader/assistive-technology behavior, responsive layout, device behavior, or complete WCAG conformance. Record which proof class was actually executed.

Return `REVISE/HOLD` when visible states are ambiguous, focus is not visibly locatable where required, a state distinction depends on unsupported styling/motion alone, or an accessibility/conformance claim exceeds the runtime evidence.

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
