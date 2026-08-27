---
name: oleander-web-ui
description: Design, implement, and visually read back Oleander web/UI interfaces as real browser artifacts. Use for responsive pages, interaction states, navigation, component behavior, accessibility, UI presentation, and browser-delivered project experiences.
compatibility: Candidate reusable skill. Generic UI defaults to repo-native HTML/CSS/JS/SVG plus real browser readback. Figma is explicit-only for an explicitly requested editable Figma deliverable or continuation/repair of an existing authoritative Figma source. Commercial tools are never assumed.
---

# Oleander Web UI

Create real, editable browser interfaces whose visual system, information hierarchy, state semantics, and interaction behavior remain coherent across target viewports.

## Lifecycle role

- Primary: `PRESENTATION`
- Secondary: `DESIGN`, `VALIDATION`
- Status: `CANDIDATE`
- Upstream: `oleander-design-process`, `oleander-visual-design`, `oleander-data-viz`
- Downstream: `oleander-motion`, `oleander-delivery-qc`

## Required sequence

`CURRENT AUTHORITY → EXISTING SKILL / MATURE DESIGN → REQUIRED NATIVE OUTPUT → INFORMATION / STATE MODEL → EDITABLE HTML/CSS/JS/SVG → REAL BROWSER → DESKTOP/MOBILE READBACK → VISUAL + INTERACTION CRIT → REPAIR → RETEST`

## Rules

1. Generic UI does not probe, recommend, or create Figma by default.
2. Preserve one Current editable source. Screenshot/PNG/video is evidence or derivative, not the UI master.
3. Define information hierarchy, state semantics, navigation, Return/back behavior, focus/keyboard behavior, loading/error/empty states when applicable before decorative motion.
4. Responsive design is not proportional shrinking. Recompose hierarchy, crop, density, navigation and interaction for target viewports while preserving claim and state meaning.
5. Use real browser readback. Static export is not browser PASS.
6. Design Quality and technical browser validation are separate gates. Browser success cannot grant Design KEEP.
7. Reuse existing components/tokens when they are Current and fit; do not force a component library over a stronger project-specific design.
8. Keep formal text editable. Do not bake UI text into raster imagery when it must remain live or localized.
9. Record external assets, fonts, dependencies, runtime assumptions and known fallback behavior.
10. Any backend, authentication, persistence, payment, security or service claim requires separate evidence; a front-end prototype does not prove production backend correctness.

## Visual readback

At minimum inspect the required target sizes and the highest-risk states. For ordinary responsive work, include desktop and mobile. Check first-read, hierarchy, dominant mass, typography, spacing, image behavior, interactive affordance, state contrast, overflow, clipping, keyboard focus and Return/back behavior.

## Handoff

Return:
- Current editable source path/identity;
- target viewports and states;
- component/token dependencies;
- actual browser evidence;
- visual issues repaired;
- technical issues for `oleander-delivery-qc` or VALIDATION;
- motion states for `oleander-motion` when needed;
- what remains HOLD.

## Candidate boundary

This skill is installed as a Candidate. Real project use, browser readback, regression cases and independent promotion evidence are required before any stronger maturity claim. `BROWSER PASS ≠ DESIGN PASS`; `CANDIDATE ≠ DEFAULT PRODUCTION OWNER`.