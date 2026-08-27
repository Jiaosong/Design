# Browser Design Workbench — Professional Review 01

**Date:** 2026-08-27  
**Surface:** `browser_design_workbench` v0.2  
**Binding:** C04 Current responsive contract fixture / readback shell only  
**Review mode:** artifact-first; screenshots before producer receipt/source  
**Verdict:** **REVISE / RETEST REQUIRED / ACTIVE NOT GRANTED**

## What remains valid
- v0.2 fixed the v0.1 false-mobile defect: iframe inner viewport is genuinely 1440×900 / 1024×768 / 768×1024 / 390×844.
- C04 Current breakpoints actually activate inside the iframe.
- preview zoom does not mutate project viewport dimensions.
- grid, grayscale and inspectable-srcdoc outline diagnostics work.
- non-HTTP(S) URL input fails closed.
- Workbench does not mutate C04 Source Authority.
- C04 full finished-pixel PASS remains independently blocked by current #353 asset binding.

## W01 — Actual-pixel readback is visually demoted by default
**Visible fact:** persisted 1440 and 390 readbacks are captured with the Workbench preview at 50%; the 390 viewport is therefore presented at roughly 195 CSS px and the 1440 viewport at roughly 720 CSS px.

**Why this fails:** real viewport dimensions are correct, but a professional finished-pixel review needs an explicit `ACTUAL PIXELS / 100%` mode and must not silently present a scaled-down preview as the default visual evidence. Responsive-contract PASS is not enough for typography, lineweight, image sharpness, clipping, micro-spacing or touch-target near-read.

**Root cause:** preview zoom is treated only as a convenience selector; the UI has no semantic distinction between `ACTUAL_PIXEL_READBACK` and `FIT_PREVIEW`.

**Feedback action:** add explicit readback modes. Default professional review to `100% ACTUAL PIXELS`; add `FIT TO STAGE` only as a clearly labeled overview. Every exported/readback state must record the preview mode and zoom.

**Retest evidence:** 390 and 1440 artifact-first captures at actual pixels plus a separately labeled fit overview; no ambiguity about which one is evidence for near-read.

## W02 — Missing project-surface telemetry
**Visible fact:** Workbench status reports requested viewport but not the loaded project's `scrollWidth / clientWidth / scrollHeight / clientHeight`, horizontal overflow, devicePixelRatio, or current scroll position.

**Why this fails:** a viewport shell can display a page that visually appears plausible while horizontal overflow, clipped long-form content, or wrong scroll-state remains unreported. This is especially important for C04 long-form Web and mobile readback.

**Root cause:** v0.2 validates iframe dimensions, not the loaded document surface contract.

**Feedback action:** for inspectable SRCDOC/same-origin content, add live telemetry and explicit `HORIZONTAL OVERFLOW PASS/HOLD`. Record scroll position and document height. Cross-origin URL mode must state telemetry unavailable rather than infer PASS.

**Retest evidence:** desktop/mobile telemetry values from the actual frame document; an injected overflow fixture must produce HOLD; clean fixture must PASS.

## W03 — Controlled SRCDOC lacks durable source identity
**Visible fact:** `loadHTML(html,{meta})` accepts arbitrary caller metadata. Workbench itself does not hash the loaded HTML bytes or display a durable source identifier.

**Why this fails:** two visually similar fixtures can be loaded into the same viewport with no Workbench-level proof of which exact source bytes were reviewed. `projectMeta` is descriptive metadata, not byte identity.

**Root cause:** source binding was outside v0.2 scope.

**Feedback action:** hash controlled SRCDOC bytes in-browser (SHA-256 with fallback where required) and expose `source_sha256 / bytes / role / baseHref` in status/readback receipt. URL mode records URL only and explicitly remains `REMOTE_CONTENT_IDENTITY_UNVERIFIED` unless an external source hash is provided.

**Retest evidence:** known fixture hash matches independently computed SHA; single-byte source change changes Workbench hash.

## W04 — Readback state is not persistable as a first-class artifact
**Visible fact:** `OleanderWorkbench.getState()` exposes ephemeral JS state, but there is no `Export Readback Receipt` containing viewport, preview mode, diagnostics, source identity, telemetry, scroll state and capability boundaries.

**Why this fails:** screenshots alone do not reconstruct how the review was made, and current automation has to create evidence outside the Workbench.

**Root cause:** v0.2 was a viewport harness, not yet a self-describing review surface.

**Feedback action:** add downloadable JSON readback receipt for the last inspectable state; receipt must remain evidence metadata, not Design PASS.

**Retest evidence:** export JSON → reload/read → fields match current frame state; dirty/source change updates receipt identity.

## W05 — URL mode can overstate successful readback
**Visible fact:** cross-origin `frame.onload` currently reports `URL LOADED / OUTLINE MAY BE CROSS-ORIGIN BLOCKED`. The shell cannot determine whether the iframe contains the intended project, a protection/login/error page, an X-Frame/CSP failure, or the right version.

**Why this fails:** load event ≠ target-content verification.

**Root cause:** URL mode does not separate navigation event from inspectable/verified project readback.

**Feedback action:** URL mode status must be `REMOTE VISUAL LOAD ONLY / CONTENT IDENTITY + DOM TELEMETRY UNVERIFIED` unless same-origin inspection or externally supplied verification evidence exists. Do not emit a Browser/Design PASS from URL load alone.

**Retest evidence:** URL mode truth label is always visible; invalid/protected/cross-origin content cannot become `VERIFIED` without additional evidence.

## Review decision
`RESPONSIVE CONTRACT FUNCTIONAL PASS` remains valid.  
`PROFESSIONAL WORKBENCH READBACK PASS = NOT GRANTED`.  
`INDEPENDENT KEEP = OPEN`.  
`ACTIVE = NOT GRANTED`.

Repair only W01–W05, then reopen actual artifacts before any promotion.