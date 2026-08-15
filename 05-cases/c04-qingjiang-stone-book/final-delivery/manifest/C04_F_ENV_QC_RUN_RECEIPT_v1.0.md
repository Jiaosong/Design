# C04 F Environment Freeze + Export QC Run Receipt v1.0

Project: `PRJ-C04-QINGJIANG-SHISHU`  
Lane: `F / Final Integration`  
State: `READY / TECHNICAL EXPORT QC PASS / FIELD OPEN / NO_PROMOTION`

## Actual toolchain

- Python 3.13.5 / Pillow 12.3.0 / ReportLab 4.4.9.
- Poppler 25.06.0 + Ghostscript 10.05.1.
- FFmpeg / ffprobe 7.1.5.
- Inkscape 1.4 / CairoSVG 2.8.2 / ImageMagick 7.1.2-1.
- WeasyPrint 68.0 = current HTML/CSS -> PDF fallback.
- Chromium 144 binary exists, but current headless PDF smoke timed out with DBus/zygote errors and emitted no PDF; it is **not** counted as an available current PDF-print path.
- `qpdf` and `rsvg-convert` absent and non-blocking; no install/wait performed.
- Blender/native 3D is not an F delivery dependency; F consumes upstream GLB/PNG/sections/model bridge when materialized.

## Reproducible entrypoints

```bash
./work/export_reproducible.sh
./work/qc_delivery.sh
```

The default video export is a no-quality-loss FFmpeg stream-copy remux of the already accepted F v0.2 master. `C04_REENCODE_VIDEO=1` activates the D v1.1 motion + F ASS + accepted F audio layer rebuild path. Silent output is permitted only as an explicitly named technical fallback and may not replace the submission film.

## Actual rerun result

- A1 primary PDF: `3 pages / A1 landscape`; full Poppler render PASS; Ghostscript stderr `0`.
- 20-screen primary PDF: `20 pages`; full Poppler render PASS; Ghostscript stderr `0`.
- Visual regression vs pre-freeze accepted PDF: A1 `0/3 changed`; 20-screen `0/20 changed` at 36 dpi.
- During the first rerun, PAGE-11 and PAGE-20 revealed stale generator output. The accepted downstream edits were recovered from the pre-freeze PDF and locked as F presentation-state overrides before the final rerun; no upstream Evidence/Spatial/Model authority was changed.
- WeasyPrint fallback: A1 `3 pages`; 20-screen `20 pages`; structural open PASS.
- 86 s film: `86.000 s / 1920x1080 / 24 fps / H.264 yuv420p + AAC 48 kHz mono`.
- FFmpeg full-stream decode stderr: **0 bytes**.

## Current SHA-256

- A1 PDF: `a32f45040140eb32b61c5419036a71a73968f66937591e93b5ae1249c22c3fc5`
- 20-screen PDF: `859012b416fdccad61885ceb5921ee3072ec654768c500728987bd0b1aff53d7`
- 86 s reproducible film: `0e74bd7d69781495a6db6f3ddc3a26b03b692b6a6f1f00d399c61dc5aef5ae61`
- F audio master: `0eb90e5173c2adbd6e9069d7c7162e614d1c62bc74a0131c38308e185e5e9748`
- Local environment/QC handoff ZIP: `2b8c8ee2e26562a3627138f018d0f61acaf9aaeabe46fd86a15168b747d18feb`

## Web/QC handoff

`F_DELIVERY_BLOCKER = NONE`.

Only open F replacement dependency: `MODEL-BRIDGE-PACKAGE` for `SLOT-3D-HERO`; expected GLB/PNG/section/camera/source-hash bridge. Its absence does not block the current A1/PDF/video/web delivery and must not trigger reflow or redesign.

Project-wide field/expert gaps remain source-boundary HOLDs, not technical export blockers.

Hard state remains: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.

`EXECUTED / BUILD / RENDER / ENCODE / DECODE PASS` does not equal Design PASS, Field PASS, compliance, implementation readiness, or Promotion.
