# Temporal Handoff Gate

Status: **CANDIDATE**  
Parent skill: `oleander-motion`  
Coverage: MOT-02 State Transition + MOT-03 Spatial Continuity + hierarchy handoff

## Problem
A state transition can be smooth, technically correct, and still fail visual judgment when the outgoing and incoming states both retain full first-read weight during the transition.

## Trigger
Use when one state, claim, panel, scene, object, route condition, or information layer yields attention priority to another.

## Inputs
- before state and after state;
- declared primary visual/claim in each state;
- continuity anchor that persists across states;
- runtime timing/easing or reduced-motion behavior;
- project Source Authority and task priority.

## Visible symptoms
- two simultaneous first-read centers at 25–75% transition progress;
- old headline/hero stays at full weight while a new full-weight panel arrives;
- user must wait until animation completion to know what is primary;
- unrelated crossfade makes state origin/destination ambiguous;
- reduced-motion mode deletes the continuity relation.

## Cause
Motion is treated as two complete compositions overlapping in time instead of an explicit transfer of hierarchy.

## Technique
`OLD PRIMARY → CONTINUITY ANCHOR → OLD PRIMARY DOWNWEIGHT → NEW PRIMARY ACQUIRE → OLD STATE SUPPORT`

Preserve the smallest persistent element that explains continuity. Lower the outgoing state's visual weight before or while the incoming state acquires first-read priority. Do not force the entire previous state to disappear when spatial/context continuity is useful.

## Parameters / conditions
- inspect at minimum 0%, 25–50%, 75%, and 100%;
- one first-read center should be unambiguous through the middle of the transition;
- overlap is allowed only when one layer is visibly subordinate;
- preserve task-critical information in Reduced Motion;
- duration/easing remain governed by MOT-01 and AR-S10 rather than this gate;
- no requirement for a specific library or visual style.

## Aesthetic judgment
The transition should feel like a transfer of authorship: the old state explains where the new state came from, then yields visual authority without visual dead time or dual-focus noise.

## Verification
1. no-motion baseline;
2. candidate transition in real runtime;
3. capture intermediate frames, not only before/after;
4. first-read review at intermediate frames;
5. near-read for overlap/occlusion;
6. Reduced Motion equivalence;
7. interruption/reversal attack under parent `oleander-motion` AR-S10.

## Failure condition
REVISE when outgoing and incoming states both preserve full first-read weight for a material portion of the transition, when hierarchy is only legible after completion, or when Reduced Motion removes required continuity.

## Counterexample
A polished crossfade with correct easing and no jank can still fail if the old hero headline and the new decision panel are both equally dominant in the middle frames.

## Transfer boundary
This gate governs temporal hierarchy only. It does not prove comprehension, accessibility conformance, field truth, operational state, product performance, engineering safety, or release approval.

## Applicable domains
Web/UI, spatial route interfaces, dashboards, brand motion, product state changes, 3D exploded/assembly transitions, data-state transitions, presentation/video sequences.

## Application mapping
Current calibration: C04 `Landscape First → Relation Reveal`, with no change to R06 geometry, route facts, FIELD state, or Source Authority.

## Evidence Gate
PASS only when precedent facts, project state mapping, and runtime behavior are traceable.

## Design Quality Gate
Requires actual intermediate-frame visual readback. Browser/video existence, CI, export, or frame-rate success cannot substitute.

Version: `0.1-candidate`  
Status: `CANDIDATE / broader project validation pending`
