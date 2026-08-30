# VALIDATION PRACTICE EVIDENCE — Keyboard focus obscuration under sticky overlay

Mode: TRAINING_MODE
Maturity: PRACTICE_EVIDENCE
Owner: existing `oleander-delivery-qc`; Web/UI behavior remains bounded to existing Web/UI specialist route.
Project Current mutation: NONE
Promotion: NONE

## GAP
A real browser can report a focusable element as focused while author-created sticky content completely hides the component and its focus indicator. Generic browser/render success therefore does not prove keyboard focus visibility or Focus Not Obscured behavior.

## Existing validator / standard
- OLEANDER `oleander-delivery-qc` remains VALIDATION owner.
- WCAG 2.2 SC 2.4.11 Focus Not Obscured (Minimum): a component receiving keyboard focus must not be entirely hidden due to author-created content.
- WCAG 2.2 SC 2.4.7 Focus Visible: keyboard focus indication must be visible.
- W3C Understanding guidance explicitly names sticky headers/footers and scroll padding as a relevant failure/repair class.

References:
- https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
- https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html

## Required Native Output / Test
Editable HTML fixtures plus a Playwright/Chromium validator. Test both desktop 1280×720 and mobile 390×844. Send one real `Tab` key, verify the active element, compare the focused component bounding box against the author-created sticky header, and preserve screenshot hashes.

## ARTIFACT / A-B attack
A / REJECT: fixed 96px header, main content begins at 20px. The first tabbable button is focused but lies at y=20..64 and is entirely behind the header ending at y=96.

B / REPAIR: main content begins at 112px and the page adds `scroll-padding-top:112px` plus `scroll-margin-top:112px`; focus-visible outline remains explicit.

## Actual readback
Chromium executable: `/usr/bin/chromium`.
Playwright Python available and executed.
`file://` navigation was blocked by runtime administration; validator was repaired to use `page.set_content()` with the exact same HTML source. This runtime restriction is recorded and is not misreported as a browser failure of the fixture.

A desktop: active=`target`; target y=20..64; sticky header bottom=96; fully hidden=true.
A mobile: active=`target`; target y=20..64; sticky header bottom=96; fully hidden=true.
B desktop: active=`target`; target y=112..156; sticky header bottom=96; fully hidden=false.
B mobile: active=`target`; target y=112..156; sticky header bottom=96; fully hidden=false.

The focus outline is present in both A and B (`4px solid`), proving a useful distinction: a focus style may exist in computed CSS while the focused component and indicator are still visually unavailable because another author-created layer covers them.

## Root cause → repair → retest
Root cause: layout reserves no physical viewport territory for the fixed header. Focus semantics and CSS outline exist, but the first focus target occupies the same visual territory as the overlay.

Repair: reserve content offset beyond the sticky header and add scroll padding/margin for subsequent focused elements.

Retest: same Tab action and bounding-box test pass at both viewports; assertions require A to fail and B to pass.

## PROVEN
- `document.activeElement` / keyboard focus success does not prove visible focus.
- A computed focus outline does not prove the focus indicator is actually visible when an overlay covers the component.
- Sticky-overlay geometry must be included in browser validation.
- The bounded repair removes total obscuration in the tested desktop/mobile states.

## NOT PROVEN
- Full WCAG 2.2 conformance or accessibility certification.
- Focus Appearance (2.4.13) metrics, contrast across arbitrary themes, zoom/text-reflow states, screen-reader semantics, complex dialogs, all responsive breakpoints, or production-site behavior.
- The exact 112px offset as a universal design value; it is fixture-specific (`96px header + 16px clearance`).

## Transfer rule
`FOCUSABLE / ACTIVE ≠ VISIBLE FOCUS`.
For pages with sticky/fixed author-created layers, browser QA should include:
`KEYBOARD FOCUS → ACTIVE ELEMENT → COMPONENT BBOX → OVERLAY BBOX → VISIBLE/OBSCURED → REPAIR → RETEST`, at representative native viewports.

## Status
PASS_FOR_BOUNDED_FOCUS_OBSCURATION_VALIDATION / PRACTICE_EVIDENCE / NO_PROMOTION.
Next material evidence: apply the same test to a materially different overlay pattern (persistent bottom banner, drawer/non-modal disclosure) or a real queued/explicit project page; do not repeat another top-header fixture only.
