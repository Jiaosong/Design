# OLEANDER Practice｜Interaction State Legibility Calibration

## Training question

How should OLEANDER interactive work distinguish `default / hover / focus / selected / disabled` without confusing visual polish with actual accessibility proof?

## Existing gap

`oleander-delivery-qc` previously required keyboard access for websites and interactive charts, but did not define a visible-state differentiation gate. Recent practice already covers earned-attention UI hierarchy, so this exercise deliberately avoids another hierarchy study and isolates interaction-state legibility.

## External calibration

- WCAG 2.2 SC 2.4.7 requires keyboard focus to be visible.
- WCAG 2.2 SC 2.4.13 describes a stronger Focus Appearance calibration: indicator area comparable to a 2 CSS px perimeter and at least 3:1 change of contrast for the same pixels; this is Level AAA and is used here as a calibration target, not a blanket conformance claim.
- WCAG 2.2 SC 2.5.8 Target Size (Minimum) is 24 × 24 CSS px subject to exceptions. This practice uses 44 px minimum height for primary controls as an OLEANDER practice target, not as the WCAG 2.5.8 minimum.

## Actual asset

A responsive HTML/CSS calibration interface was built with native `<button>` semantics, explicit `:focus-visible`, 48 px primary control height, selected state using `aria-pressed`, disabled state, and responsive two-column-to-one-column behavior.

A static SVG visual-proof derivative was also generated to support independent Design Crit. The derivative does not replace browser/runtime testing.

## Design Crit

**Verdict: KEEP as training asset / runtime conformance HOLD.**

- First visual gate: PASS — reject/keep contrast is immediately readable.
- Composition: PASS — two-panel comparison supports direct state comparison.
- Proportion: PASS — 48 px controls remain clearly operable in the calibration layout.
- Hierarchy: PASS — state label is subordinate to the control; focus indicator becomes the strongest local event only when needed.
- Typography: PASS — neutral sans-serif avoids decorative interference.
- Material/spatial reality: N/A.
- Scale: PASS within CSS-interface scope.
- Node readability: N/A.
- Interaction narrative: PASS as a state model; full runtime evidence remains HOLD because the container browser could not produce a reliable screenshot during this run.
- Professional completion: KEEP for reusable calibration/training, not a finished product UI.

## Failure knowledge

1. `outline: none` without a replacement is not a visual-cleanliness improvement; it removes orientation for keyboard users.
2. Hover and selected states cannot rely on nearly identical pale fills when their meanings differ.
3. A screenshot can prove visible differentiation but cannot prove focus order, keyboard activation, screen-reader naming or full WCAG conformance.
4. A larger OLEANDER target-size practice default must not be misreported as the formal WCAG minimum.

## Skill delta

Updated `oleander-skills/oleander-delivery-qc/SKILL.md` with `Gate 5.1: interaction state legibility` rather than creating a parallel UI skill.

## Transfer

Applicable to OLEANDER websites, mini-programs, interactive maps/charts, UI prototypes and component systems. Not a substitute for usability tests, device testing, assistive-technology testing or full accessibility conformance assessment.
