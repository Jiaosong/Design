# OLEANDER Training — Exploration Behavior Grammar

## Trigger
Recent Qingjiang digital review found that motion remained dominated by `fade / reveal / glow / withdraw` and had not yet become a coherent exploration behavior language.

## Existing-first
This round extends `oleander-motion`; it does not create a parallel motion or game-UI framework. The current motion Skill already owns state transitions, spatial continuity, interactive motion, Reduced Motion and runtime QA. The missing piece was the behavioral contract that makes an exploratory interface more than a set of effects.

## Practice
Same synthetic R06-like world relation, no project geometry.

- **A / effect-first — REJECT**: hover → glow → click → fade card. Visual change exists, but no persistent selected relation, retreat semantics, or behavioral memory exists.
- **B / state-first — KEEP FOR TRAINING**: `IDLE → SCOUT → COMMIT → REVEAL → RETREAT / RETURN`. Explanation appears after commitment and stays tied to a selected world relation.

Candidate rule:

`INTENT → SCOUT → COMMIT → REVEAL → RETREAT / RETURN`

## Design Crit
- First visual: KEEP for the state-first specimen; world/route remains primary before explanation.
- Composition/hierarchy: KEEP; one relation owns primary attention only after commit.
- Typography: KEEP for calibration; state labels remain supporting.
- Spatial truth: bounded; synthetic relation only, no C04 geometry claim.
- Interaction grammar: KEEP as designed state model.
- Runtime: HOLD. System Chromium did not complete headless startup in the current environment, so browser execution, keyboard behavior, rapid-switch behavior and Reduced Motion are not promoted to runtime PASS.
- Professional finish: KEEP for training artifact only.

## Failure knowledge
1. Hover/glow/reveal does not constitute an exploration grammar.
2. Commit without retreat traps hierarchy.
3. Reveal without persistent world anchor becomes a detached overlay.
4. RETURN must reset exploration state, not merely navigate elsewhere.
5. Reduced Motion must preserve state meaning even when interpolation disappears.

## Boundary
Synthetic training relation only. No C04 route, geometry, safety, closure, FIELD state, comprehension, accessibility conformance, game-feel, or production-readiness claim.
