---
name: oleander-mobile-game-ui
description: OLEANDER mobile game UI skill for thumb-zone layout, touch targets, safe areas, one-handed use, gesture discoverability, narrow-screen density, responsive fit, reduced motion, and mobile interaction resilience.
status: candidate
version: 0.1.0
---

# OLEANDER Mobile Game UI

## Purpose
Ensure game-like and immersive interfaces remain readable, operable, discoverable, and calm on actual mobile screens. This skill is a mobile ergonomics and interaction-quality gate, not a styling layer.

## Authority and review discipline
- Read project authority before changing layout or interaction.
- Preserve existing mature design intent; adapt presentation to mobile without deleting product content.
- Mobile simplification must follow `NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS`.
- Runtime success proves operation only, not visual quality.
- Producer may not self-award final Design PASS / MAIN / numeric quality score.

## Core principles
### 1. Thumb-zone priority
Place frequent, reversible actions in comfortable reach. Put low-frequency, destructive, or cognitively heavy actions farther from accidental thumb zones.

For one-handed portrait use:
- lower-center and lower-side zones are easiest for frequent actions;
- upper corners are acceptable for low-frequency or explicit utility controls;
- do not put multiple equally important actions in both upper corners if they force constant grip change.

### 2. Touch targets
Use approximately 44–48 CSS px as the default minimum interactive hit area where practical. Visual glyphs may be smaller, but the hit target must remain comfortable and separated.

Check:
- adjacent node spacing;
- icon-only controls;
- map/route anchors;
- bottom navigation;
- small close/back/Return controls;
- gesture surfaces versus control surfaces.

### 3. Safe areas
Respect `env(safe-area-inset-*)` and device cutouts. Do not let critical controls sit against rounded corners, home indicators, browser chrome, or notches.

### 4. Gesture discoverability
A gesture cannot be the only path to a core action unless the gesture is platform-standard and recoverable.

For drag/pan/route exploration:
- provide visible affordance or partial next/previous context;
- preserve keyboard/button alternatives where web-based;
- do not require exact drag direction or long distance;
- handle cancel/interruption cleanly.

### 5. Progressive density
Do not shrink desktop/full-map information until it fits. Recompose it.

Preferred mobile strategies:
- segment/viewport into a larger world;
- reveal labels on focus/approach;
- prioritize current object and next decision;
- use progressive disclosure;
- maintain a stable Return/escape path;
- retain full information in alternate/detail states rather than deleting it.

### 6. One-handed stability
Do not move primary controls after interaction begins. Avoid reflow that changes the user's muscle memory. Keep bottom navigation and Return stable unless a scene intentionally enters a focused/withdrawn state.

### 7. Motion sensitivity and reduced motion
Reduced Motion is not “same timers with opacity removed.”

When `prefers-reduced-motion: reduce` is active:
- remove decorative and spatially unnecessary animation;
- remove JS delay locks tied only to animation;
- preserve state change, hierarchy, focus, route, and feedback information;
- ensure all actions remain immediate and reversible;
- verify actual running animation count, not just CSS declarations.

## Required test matrix
Minimum for a mobile web/app prototype:

```text
390×844 portrait
430×932 portrait
Reduced Motion at one narrow viewport
Keyboard/focus smoke test where web-based
Touch/pointer interaction path
```

Add landscape/tablet only if Current Task requires it.

## Workflow
1. Inventory all interactive elements and their frequency/criticality.
2. Map primary actions to thumb zones.
3. Measure effective hit areas and separation.
4. Verify safe-area padding and no overlap with browser/device chrome.
5. Check gesture discoverability and alternate paths.
6. Check narrow-screen density using real/long labels.
7. Test interruption: change target mid-transition, press Return, cancel gesture, background/blur if applicable.
8. Test Reduced Motion behavior and confirm no hidden wait locks.
9. Test keyboard/focus if delivered as HTML/web prototype.
10. Capture runtime evidence without converting it into a Design PASS.

## Hard failure conditions
- Core touch target < 40px with no surrounding hit area;
- adjacent small controls cause likely accidental activation;
- essential gesture has no affordance or alternate path;
- Return/escape is outside comfortable reach and no equivalent exists;
- interaction depends on hover;
- full desktop information is merely scaled down until illegible;
- safe-area overlap clips or obstructs a critical control;
- Reduced Motion leaves invisible waits, locks, or unusable state changes;
- keyboard focus lands on invisible elements;
- UI depends on color alone for selected/current/disabled state.

## Review output
```text
VIEWPORTS TESTED:
PRIMARY HAND / THUMB ASSUMPTION:
TARGET-SIZE FINDINGS:
SAFE-AREA FINDINGS:
GESTURE DISCOVERABILITY:
DENSITY / LABEL FIT:
RETURN / ESCAPE:
REDUCED MOTION:
KEYBOARD / FOCUS:
RUNTIME DEFECTS:
INDEPENDENT DESIGN VERDICT REQUIRED: YES
```

## Source lineage
Adapted for OLEANDER from mobile game UI ergonomics practice, Fitts-style target principles, platform guidance for mobile game controls, and OLEANDER's existing Reduced Motion / runtime QA rules. External guidance supports the skill but does not override project authority.