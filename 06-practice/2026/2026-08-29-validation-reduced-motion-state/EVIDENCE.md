# OLEANDER VALIDATION Practice Evidence｜Reduced Motion State Equivalence

Status: PRACTICE_EVIDENCE / NOT CURRENT RULE / NO_PROMOTION.
Mode: TRAINING_MODE.
Existing Owner: `oleander-delivery-qc` (VALIDATION); supporting route only: `oleander-web-ui` candidate.
Applicable Domain: Digital / Interaction / Accessibility Validation.
Applicable Project: none in this run. C04 `PRJ-C04-DIGITAL-INTERACTION` remains PRESENTATION-owned in Priority Queue; no project mutation or PASS is claimed.
Trust: EXECUTED_EVIDENCE / CURRENT-KNOWLEDGE-MIGRATION_OPEN.
Freshness: source/version check completed 2026-08-29; re-check on WCAG/WAI technique, browser behavior, or Playwright version change, and before any promotion.
Knowledge Write Handoff: KNOWLEDGE may migrate/relate this evidence only after its normal Current/Support/Provenance and relation-closure process.

## GAP

A common reduced-motion implementation disables CSS animation with `@media (prefers-reduced-motion: reduce)`, while application state completion is still coupled to the `animationend` event. If the animation is removed, the event may not fire and the semantic state can remain stuck even though motion is successfully suppressed.

## External discovery / source-version check

1. W3C WAI, WCAG 2.2 technique SCR40, current page accessed 2026-08-29: JavaScript can evaluate `prefers-reduced-motion` to prevent interaction-triggered motion. This is a sufficient technique related to SC 2.3.3, not the only conforming implementation and not a complete accessibility certification.
   Source: https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR40
2. W3C WAI Understanding SC 2.3.3, page updated 2025-09-16: non-essential motion animation triggered by interaction can be disabled; user-agent/OS reduced-motion preference is one documented approach. SC 2.3.3 is Level AAA.
   Source: https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions
3. MDN `prefers-reduced-motion`, current page accessed 2026-08-29: the media feature detects a user preference to reduce non-essential motion and is widely available.
   Source: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
4. Playwright Python emulation docs, current page accessed 2026-08-29: browser contexts/pages can emulate reduced-motion preference. Actual runtime in this evidence is Playwright Python `1.57.0` with Chromium `144.0.7559.96`.
   Source: https://playwright.dev/python/docs/emulation
5. Playwright repository license checked 2026-08-29: Apache License 2.0.
   Source: https://github.com/microsoft/playwright/blob/main/LICENSE

What these sources prove: reduced-motion is a recognized user preference; WAI documents using it to suppress non-essential motion; Playwright exposes browser emulation for this preference.
What they do NOT prove: that any specific site's state machine is equivalent under reduced motion, that this fixture is a complete WCAG 2.2 conformance test, or that all browsers/assistive technologies behave identically.

## Required Native Output / capability probe

RNO: editable HTML A/B fixtures + deterministic browser validator + structured JSON readback.

Execution surface:
- `/usr/bin/chromium` = `Chromium 144.0.7559.96 built on Debian GNU/Linux 13 (trixie)`;
- Python Playwright = `1.57.0`;
- initial `file://` navigation was blocked by environment administrator policy, so the exact HTML bytes were executed through Playwright `page.set_content()` instead. This environment restriction is not treated as product evidence.

## Test design

A / REJECT:
- CSS suppresses the motion in `prefers-reduced-motion: reduce`.
- JavaScript always waits for `animationend` to change `status=loading` to `status=ready`.

B / REPAIR:
- same CSS and visible end state;
- JavaScript checks `matchMedia('(prefers-reduced-motion: reduce)').matches`;
- when reduce=true, it commits the final semantic state immediately; otherwise it keeps the normal `animationend` path.

The `300ms` animation and `450ms` observation time are EXERCISE ASSUMPTIONS selected only to make the failure deterministic; they are not standards, recommended UI timing, or product requirements.

## Actual readback

A / no-preference: media=false; after 450ms status=`ready`; final transform=identity.
A / reduce: media=true; after 450ms status=`loading`; transform=`none` → state-equivalence failure reproduced.
B / no-preference: media=false; after 450ms status=`ready`.
B / reduce: media=true; after 450ms status=`ready`; transform=`none` → reduced motion plus semantic completion.

Validator assertions all passed and produced:
`PASS_FOR_BOUNDED_REDUCED_MOTION_STATE_EQUIVALENCE`.

## Root cause → repair → retest

Root cause: semantic completion was coupled to the lifecycle of a non-essential visual animation. Removing the animation removed the event that advanced application state.

Repair: decouple final semantic state from the animation event when the user preference requests reduced motion; commit the same final state without motion.

Retest: normal preference and reduced-motion preference both reach the same semantic `ready` state, while reduced-motion keeps the motion removed.

## PROVEN

- In Chromium 144.0.7559.96 under Playwright 1.57.0, a fixture that disables its CSS animation can remain stuck if semantic completion depends only on `animationend`.
- The repaired fixture in this bounded test reaches the same final semantic state for `no-preference` and `reduce`.
- `matchMedia('(prefers-reduced-motion: reduce)')` matched the Playwright-emulated preference in the executed test.

## NOT PROVEN / boundary

- Complete WCAG 2.2 conformance or accessibility certification.
- Cross-browser equivalence across Firefox/WebKit or real OS/device preference propagation.
- Screen-reader behavior, focus management, live-region quality, interruption/re-entry, network-driven state, complex motion choreography, or performance.
- Any C04 project state or Design Quality KEEP; the current C04 object remains owned by PRESENTATION until a valid handoff occurs.

## Transfer rule candidate

`REDUCED MOTION MUST PRESERVE SEMANTIC STATE COMPLETION; DO NOT COUPLE REQUIRED STATE TRANSITIONS SOLELY TO A NON-ESSENTIAL ANIMATION EVENT.`

Candidate only. It may move beyond PRACTICE_EVIDENCE only after materially different contexts or real project usage expose and survive additional failure modes.
