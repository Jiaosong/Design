# UI Interaction Visual Layer Binding

Status: **BINDING ONLY / STATE FIRST**

This Skill owns interaction state and transition logic, not independent visual styling.

## Existing sources to inherit

1. `oleander-ui-visual-composition` for static hierarchy, typography, imagery, depth and visual state treatment.
2. `oleander-motion` + `MOTION_LIBRARY_EFFECT_ATLAS.md` for temporal feedback and transition mechanisms.
3. Existing responsive recomposition practice `06-practice/2026/2026-08-18-responsive-recomposition/` when breakpoint changes alter interaction priority.
4. Notion `OLEANDER Artifact Review System v1.1｜合规门 × 专业设计门`.

## Existing ownership boundary

Use this order already established by the Skill:

`input → intent → state transition → UI update → motion/feedback`

Define state before animation. Selection/focus/available/unknown/closed/error states must remain semantically correct before any visual treatment is chosen. Visual effects cannot repair an invalid or contradictory state machine.

## Review inheritance

Static appearance defects route to `oleander-ui-visual-composition`; temporal defects route to `oleander-motion`; state/interrupt/re-entry defects remain here. Final design verdict remains independent.
