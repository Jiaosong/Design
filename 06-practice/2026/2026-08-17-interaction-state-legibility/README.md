# OLEANDER Practice｜Interaction State Legibility Calibration

Status: **PRACTICE PROVENANCE / ASSET EVIDENCE INCOMPLETE / PRODUCER SELF-CHECK ONLY / RUNTIME + INDEPENDENT DESIGN VERDICT OPEN**

## 2026-08-25 readback correction

The original record stated that a responsive HTML/CSS calibration interface and a static SVG derivative had been built. PR #182, however, contains only this README and the `oleander-delivery-qc` Skill change. The claimed HTML/CSS and SVG artifact bytes are **not present in the PR**, so they cannot be reopened, rendered, inspected, or used as independent Design/Runtime evidence from repository state.

Consequences:

- the historical `KEEP as training asset` wording is withdrawn as a Design verdict;
- any visual observations below are retained as producer-reported Practice provenance only;
- no runtime keyboard/focus/accessibility proof is established;
- no responsive/browser or independent Design PASS is established;
- the reusable Skill delta may be retained only where it is independently supported by Current standards/rules and does not depend on the missing artifact bytes.

## Training question

How should OLEANDER interactive work distinguish `default / hover / focus / selected / disabled` without confusing visual polish with actual accessibility proof?

## Existing gap

`oleander-delivery-qc` previously required keyboard access for websites and interactive charts, but did not define a visible-state differentiation gate. The exercise isolates interaction-state legibility rather than creating another UI hierarchy framework.

## External calibration — current W3C verification 2026-08-25

WCAG 2.2 Current Recommendation was rechecked against W3C:

- **SC 2.4.7 Focus Visible — Level AA**: a keyboard-operable interface has a mode where the keyboard focus indicator is visible.
- **SC 2.4.13 Focus Appearance — Level AAA**: when the focus indicator is visible, an area is at least as large as a `2 CSS px` perimeter of the unfocused component/sub-component and has at least `3:1` contrast between the same focused/unfocused pixels, subject to the criterion's exceptions.
- **SC 2.5.8 Target Size (Minimum) — Level AA**: pointer target size is at least `24 × 24 CSS px`, subject to its spacing/equivalent/inline/user-agent/essential exceptions.
- **SC 2.5.5 Target Size (Enhanced) — Level AAA** uses `44 × 44 CSS px`, subject to its exceptions. OLEANDER may use `44 px` or larger as a practice/product target, but must not call that the SC 2.5.8 minimum or claim AAA conformance without full applicable testing.

These values are calibration references, not a blanket WCAG conformance claim for OLEANDER work.

## Historical reported asset behavior — not repository-reopenable

The original run reported:

- native `<button>` semantics;
- explicit `:focus-visible`;
- 48 px primary control height;
- selected state using `aria-pressed`;
- disabled state;
- responsive two-column-to-one-column behavior;
- a static SVG visual-proof derivative.

Because those HTML/CSS/SVG bytes are absent from PR #182, these remain historical implementation claims rather than inspectable evidence.

## Historical producer Design Crit

Original wording: `KEEP as training asset / runtime conformance HOLD`.

Current governance classification: **`SELF-CHECKED PRACTICE / EVIDENCE INCOMPLETE / INDEPENDENT DESIGN VERDICT NOT RECORDED`**.

Producer-reported observations preserved for derivation:

- reject/correct comparison was intended to make state differentiation first-read visible;
- 48 px controls were intended to remain operable in the calibration layout;
- focus indicator was intended to become the strongest local event only when needed;
- screenshot/static visual proof was correctly treated as insufficient for focus order, keyboard activation, accessible naming or full conformance.

These observations are not upgraded to Design PASS because the visual/runtime artifacts are missing.

## Failure knowledge retained

1. `outline: none` without a visible replacement can remove keyboard orientation and fails the intended focus-visible requirement.
2. Hover and selected/pressed states should not collapse into near-identical appearances when their meanings differ.
3. A screenshot can support visible-state differentiation only; it cannot prove focus order, keyboard operation, accessible naming, responsive behavior, assistive-technology behavior, or full WCAG conformance.
4. A larger target-size practice default must not be misreported as the formal WCAG 2.5.8 minimum.
5. Visual-state quality and runtime accessibility evidence remain separate review axes.

## Skill delta

The transferable delta belongs inside existing `oleander-delivery-qc`: inspect visible interaction states and explicitly separate screenshot/visual proof from runtime accessibility proof. No parallel UI/accessibility Skill is created by this Practice.

## Transfer

Applicable to OLEANDER websites, mini-programs, interactive maps/charts, UI prototypes and component systems. It is not a substitute for usability tests, device testing, assistive-technology testing or a complete accessibility conformance assessment.

## Does not prove

- the missing historical HTML/CSS/SVG assets existed exactly as described;
- independent Design KEEP;
- browser/runtime PASS;
- keyboard focus order or activation;
- accessible name/role/value correctness;
- responsive/device behavior;
- WCAG AA/AAA conformance.
