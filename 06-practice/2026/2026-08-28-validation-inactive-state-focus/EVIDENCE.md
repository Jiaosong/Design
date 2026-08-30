# OLEANDER VALIDATION — Inactive State Focus Isolation

Status: PRACTICE_EVIDENCE / TRAINING_MODE / NO_PROMOTION
Date: 2026-08-28
Owner: oleander-delivery-qc (VALIDATION)

## GAP
A visually inactive/off-screen interface state can remain in the sequential keyboard focus order when it is only moved offscreen, made transparent, pointer-disabled, or marked `aria-hidden`. This creates a ghost-control state: the current view appears settled, but keyboard users can still focus controls belonging to the inactive view.

## Existing validator / standard calibration
- Existing OLEANDER Web/UI review requires real-browser keyboard/state readback; browser PASS does not imply Design KEEP.
- HTML `inert` is used as the bounded browser mechanism for removing an inactive subtree from focus/input participation. `hidden` is used here to make the inactive visual state explicit as well.
- This training artifact does not claim full accessibility conformance or certification.

## Required Native Output / test
Editable HTML A/B + Playwright browser validator + JSON readback.

A / REJECT:
- inactive AXON panel is moved off-screen and opacity=0;
- pointer-events are disabled;
- `aria-hidden=true` is present;
- descendants remain focusable.

B / REPAIR:
- inactive AXON panel is `hidden` and `inert`;
- active/inactive tab state is explicit;
- inactive descendants are removed from the sequential focus order.

## Capability probe
- `/usr/bin/chromium` available.
- Python Playwright available.
- `file://` navigation was blocked by runtime policy, so the same editable HTML source was executed with `page.set_content()`; no false local-file PASS is claimed.

## Actual readback
Tested settled `SECTION` state at 1280×720 and 390×844.

A focus sequence in both viewports contains `a-hotspot` while AXON is visually inactive:
`a-hotspot → b-hotspot → ...`

A inactive AXON readback:
- `aria-hidden=true`
- `opacity=0`
- `left=-10000px`
- `inert=false`
- `ghost_focus_present=true`

B focus sequence in both viewports excludes `a-hotspot` while AXON is inactive.

B inactive AXON readback:
- `hidden=true`
- `inert=true`
- `display=none`
- `ghost_focus_present=false`

## Failure / Root Cause
Failure: visual state isolation was implemented only in the rendering/pointer layer.
Root cause: visibility, pointer interaction, accessibility exposure, and keyboard focus participation were treated as if they were the same state contract.

## Repair / Retest
Repair the inactive state as an interaction-state boundary, not a styling-only state. The bounded repair here uses `hidden + inert` for the inactive panel and retests the actual sequential focus order after the state settles.

Retest result: PASS for this bounded browser behavior at both tested viewports.

## Transfer rule
`VISUAL STATE OFF ≠ INTERACTION STATE OFF`

For tabbed viewers, carousels, model view states, drawers, and multi-state evidence panels, validation should check:
`SETTLED STATE → INACTIVE SUBTREE → TAB ORDER / FOCUS EVENTS → POINTER/AT BOUNDARY → REPAIR → RETEST`.

`aria-hidden`, opacity, offscreen positioning, and pointer-event suppression do not by themselves prove focus isolation.

## PROVEN
- A visually hidden/offscreen inactive subtree can still leak focusable descendants into sequential keyboard navigation.
- In this Chromium/Playwright execution, `hidden + inert` removed the inactive subtree from the tab order in the tested state and viewports.
- State visual completion and keyboard-state completion are separate validation concerns.

## NOT PROVEN
- Full WCAG 2.2 conformance or accessibility certification.
- Screen-reader behavior across browser/AT combinations.
- Correct ARIA tab pattern semantics, roving tabindex, focus restoration policy, or announcement behavior.
- Dialog/modal focus trapping.
- Production-site behavior across all breakpoints and state graphs.
- Design Quality KEEP.

## Maturity
PRACTICE_EVIDENCE. No Skill/runtime/Registry promotion. A future material delta requires a different state container or real project usage, not another equivalent two-panel fixture.
