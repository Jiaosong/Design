# 2026-08-28｜DESIGN / Process / L5｜Evidence → Finding → Design Consequence Causal Relation Spine

Status: **PRACTICE_EVIDENCE / TRAINING_MODE / NO PROJECT RE-APPLICATION / NO ACTIVE PROMOTION**

## GAP

`oleander-design-process` Candidate explicitly owns `Research → Finding → Design Consequence`, analysis diagrams and relation maps, but current evidence does not yet prove that the chain remains causal under evidence deletion or adverse-condition attacks.

Failure risk: an equal-card diagram can show Evidence, Finding and Consequence as adjacent boxes while the selected design move is actually independent of the evidence.

## SOURCE

Existing-first:
- `oleander-skills/oleander-design-process/SKILL.md` on `main`.
- Current Candidate sequence: `E/I/A/D → analysis → design consequence → options → editable artifact → readback → crit → repair`.
- Recent evidence: `06-practice/2026/2026-08-27-baojiajie-claim-to-form/README.md`, which already demonstrated semantic-dimension-to-form decomposition and a deletion test in Brand/POP.

No project object is owned in this run. Priority Queue is empty and no ACCEPT Handoff was found, so this remains Practice-only.

## DESIGN QUESTION / INPUTS / CONSTRAINTS / E-I-A-D

Question:
How can an analysis diagram prove that a Design Consequence depends on specific evidence and constraints rather than merely appearing after them?

Synthetic training input:
- `E1`: movement crosses a threshold;
- `E2`: reading requires dwell;
- `E3`: Return continuity must remain visible and unbroken.

E-I-A-D:
- Evidence: E1 / E2 are synthetic relation inputs.
- Inference: movement and dwell occupy the same threshold.
- Finding: a threshold conflict exists because moving and stationary behaviors overlap spatially.
- Decision / Consequence: move dwell laterally into a bay while preserving the movement/Return spine.
- Constraint: E3 controls the consequence; no solution may block Return continuity.

No site, field, service-capacity, accessibility or dimensional truth is claimed.

## ARTIFACT

Editable vector board:
- `OLEANDER_CAUSAL_RELATION_SPINE_R01.svg`
- rendered PNG;
- 50% grayscale PNG.

The board contains three controlled conditions:

### A / REJECT — Equal-card grammar
Evidence / Finding / Consequence use equal cards and generic arrows.

Failure:
deleting E2 does not visually invalidate D; causal dependence is only implied by layout.

### B / KEEP candidate — Causal relation spine
Objects and relations are drawn first:
- movement spine;
- dwell demand;
- threshold;
- Return continuity.

Evidence attaches to the relation it supports.
Finding names the exact conflicting relation.
The consequence points to an explicit `DESIGN LEVER` rather than a generic solution card.

### C / ATTACK + RETEST

`ATTACK 01 / DELETE E2`
- remove dwell demand;
- expected: Finding disappears;
- retest result: lateral dwell bay downgrades to HOLD.

`ATTACK 02 / RETURN BLOCKED`
- break E3 Return continuity;
- expected: previously selected consequence cannot remain SELECT;
- retest result: restore/replace Return first, then re-evaluate dwell placement.

## ACTUAL READBACK

Full-size PNG and 50% grayscale PNG were reopened and visually inspected.

Readback:
- first read is relation geometry, not equal-card dashboard;
- finding and design lever remain distinguishable without relying on hue;
- E1/E2/E3 attach to different functional relations rather than becoming decorative badges;
- deletion attack changes the finding at the same causal link;
- adverse-condition attack changes the consequence, not only the explanatory text;
- no visible clipping, missing glyphs or panel overflow observed.

Hashes:
- SVG `794b645b73541a59be6817337d29728b593420ad91fa70dc999b95eea54c62f0`
- PNG `651b4167b427bfdae5905d38e07bcdb5e68907791190335179651ce9a2c427a4`
- Gray50 `0d932e568d555e6cb53a3d3c38c2cbd2af32243d575585a607cc7c6f4715645a`

## PROFESSIONAL CRIT

### Evidence / execution
**PASS FOR PRACTICE EVIDENCE**
- editable artifact exists;
- no AI-generated imagery;
- vector text remains editable;
- truth boundary is explicit;
- no Project Current or production frontier is modified.

### Design quality
**PRODUCER PRACTICE READBACK / NOT INDEPENDENT KEEP**
- First visual: PASS — relation field dominates KEEP.
- Composition: PASS — one causal field plus bounded attacks; not a repeated card matrix.
- Proportion: PASS — relation geometry > finding > lever > metadata.
- Hierarchy: PASS — Evidence supports relation; Finding synthesizes; Consequence changes a lever.
- Typography: PASS at training-board scale.
- Spatial/service realism: semantic only; no field realism claimed.
- Scale: NTS; no physical dimensional proof.
- Node readability: PASS — E1/E2/E3 roles remain distinct.
- Interaction/narrative: PASS as static causal sequence and attack logic.
- Professional finish: sufficient for Practice; not presentation/MAIN.

Independent Professional Design Review remains OPEN.

## FAILURE / ROOT CAUSE

Failure:
`Evidence cards + arrows + consequence card` can remain visually coherent after critical evidence is removed.

Root cause:
**equal-card grammar flattens dependency into co-occurrence.**
The diagram shows that things are related, not which relation is supported by which evidence or which design variable must change.

## REPAIR / RETEST

Repair:
`OBJECTS / RELATIONS → EVIDENCE HOOKS → FINDING ON THE RELATION → DESIGN LEVER → CONSEQUENCE`

Retest:
1. Delete one critical evidence item.
2. Break one governing constraint.
3. The finding/consequence must change at the same causal link.
4. If it does not, the chain is descriptive rather than causal.

## TRANSFER RULE

**A Design Consequence may be presented as evidence-driven only when removing the evidence or breaking the governing constraint changes the same explicit design lever.**

Useful transfer:
- site / route / service analysis;
- circulation / threshold / dwell relations;
- user-flow and IA/state design;
- product requirement → function → component-role reasoning;
- system-dependency diagrams;
- Evidence → Spatial Finding → Design Consequence boards.

## BOUNDARY

Do not force this grammar onto:
- exploratory ideation where causal authority is intentionally unresolved;
- multi-objective comparisons where several co-equal criteria are the actual subject;
- evidence collections whose purpose is provenance/archive rather than design consequence;
- technical validation where engineering models own the causal proof;
- project application without a queued/explicit Object ID.

## STATUS

`PRACTICE_EVIDENCE`

This round does **not**:
- modify Project Current;
- claim Project Usage Evidence;
- promote `oleander-design-process` to Installed/Active;
- modify the Candidate Skill itself;
- create a Validation or Presentation Handoff, because no owned project object exists.

## NEXT PROMOTION GAP

Test the same causal-dependency rule in a second materially different design context with real authority — preferably product requirement→part role or IA/user-flow state — and require the same deletion/adverse-condition behavior before considering `CROSS_CONTEXT_EVIDENCE`.
