# 2026-08-18 Motion / Interaction — Temporal Handoff

Status: **CANDIDATE / project-main validation pending**

## Existing-first
Reuses `oleander-motion`; no new parallel Skill. This round narrows MOT-02/MOT-03 to a temporal hierarchy question: whether visual authority is explicitly handed from the outgoing state to the incoming state.

## Learning object
Apple Live Activities / Dynamic Island transition guidance.

Visible facts used:
- preserve as much existing layout as possible during layout changes by moving existing elements to new positions rather than deleting and recreating them;
- avoid transition overlap/collision where appropriate;
- motion should be purposeful and cancellable;
- Reduced Motion must not remove required information.

## Transfer rule
`OLD PRIMARY → CONTINUITY ANCHOR → OLD PRIMARY DOWNWEIGHT → NEW PRIMARY ACQUIRE → OLD STATE SUPPORT`

A transition can be smooth yet still fail when two full-weight first-read centers coexist during the middle frames.

## Real C04 transfer
Calibration only for `Landscape First → Relation Reveal`.

A — dual-focus: Relation enters at full weight while the Landscape headline retains full first-read mass.

B — attention handoff: landscape remains as spatial continuity, its headline downweights, a short relation anchor preserves origin, and the Relation panel becomes the sole first-read center.

No route, R06 geometry, state, FIELD, safety, accessibility or operational fact is changed.

## Runtime / readback
- editable HTML/CSS/JS: executed;
- system Chromium `/usr/bin/chromium`: executed;
- Playwright runtime: executed using system Chromium;
- 0% frame: executed;
- intermediate frame (~220 ms): executed;
- 100% frame: executed;
- Reduced Motion state: executed;
- intermediate-frame Design Crit: A = REVISE, B = KEEP FOR TRAINING;
- Reduced Motion retains the same information relationship.

## Gate
Evidence Gate: PASS for precedent facts, runtime traceability, and bounded C04 mapping.

Design Quality Gate: POST-READBACK PASS for the training artifact only.

## Failure counterexample
A polished crossfade with correct easing and no jank is still REVISE when both outgoing hero and incoming decision panel remain equally dominant through the middle of the transition.

## Boundary
`TRAINING ONLY / NO SOURCE GEOMETRY CHANGE / FIELD OPEN / NO_PROMOTION`.

Browser execution, screenshots, CI and GitHub cannot promote this candidate to VALIDATED/ACTIVE and cannot establish C04 production UI Design PASS, user comprehension, accessibility conformance, or field truth.
