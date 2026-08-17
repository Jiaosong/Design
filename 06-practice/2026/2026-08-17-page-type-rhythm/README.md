# 2026-08-17 Editorial / Portfolio — Page-Type Rhythm

Status: **CANDIDATE / project transfer practice complete / broader validation pending**

## Existing-first
This round does not create a new reusable Skill. It reuses:
- `oleander-story-and-board` for page role, hierarchy, narrative sequence and distance readability;
- `oleander-delivery-qc` for final-pixel readback;
- C04 Project Architecture v3.0 page-type grammar.

## Learning object
Irma Boom, *SHV Think Book 1996–1896* (1996).

MoMA records a 2,136-page book presented in reverse chronological order. Page numbers, contents and index were omitted to encourage nonlinear exploration. Typography, layout, materials and printing are all treated as part of the reading experience.

## Transfer rule
`PAGE ROLE → DOMINANT MASS → DENSITY → WHITESPACE → READING TIME`

Different page roles must create perceptibly different visual tempos. A page-type label alone is not enough.

## C04 transfer
The same eight role set is compared in A/B:
- PROJECT
- ANALYSIS
- PRINCIPLE
- SYSTEM
- SCENE
- DETAIL
- TECHNICAL
- CLOSURE

A uses one repeated template for all roles.

B changes only editorial tempo:
- PROJECT / SCENE = fast first-read / visual mass;
- ANALYSIS / DETAIL / TECHNICAL = slower near-read density;
- PRINCIPLE / CLOSURE = deliberate pause;
- SYSTEM = relation/orientation diagram.

No C04 source pixels or geometry are replaced.

## Readback
- editable SVG: executed;
- CairoSVG: `NATIVE_AVAILABLE`;
- 1800×1100 near-read: executed and reopened;
- 491×300 distance-read: executed and reopened;
- Design Quality Gate: `POST-READBACK PASS FOR PRACTICE`.

## Failure condition / counterexample
A portfolio can be consistent, aligned and technically clean yet still require **REVISE** if ANALYSIS, SCENE, DETAIL and CLOSURE all create the same reading speed.

`COMPONENT CONSISTENCY != EDITORIAL RHYTHM`

## Transfer boundary
Do not copy SHV typography, page designs, materials or nonlinear navigation as a style preset. Transfer only the principle that content role should produce a visible change in reading tempo.

## Gates
- Evidence Gate: PASS for the learning-object facts and current C04 architecture mapping.
- Design Quality Gate: POST-READBACK PASS for this calibration artifact only.
- C04 Web / PDF / Boards: PENDING actual production binding + finished-output review.
- Skill status: CANDIDATE, not VALIDATED / ACTIVE.
