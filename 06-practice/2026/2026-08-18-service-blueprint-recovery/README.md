# OLEANDER Training｜Service Blueprint Recovery｜2026-08-18

## Trigger

Current C04 v0.2 adds `CH09-P06｜Service Blueprint｜游客看不见的后台怎样支撑Return` and explicitly requires Frontstage / Backstage / Support / Failure / Recovery without inventing SLA when operator/field data are absent.

Notion canonical method reused first: `FW-SERVICE-DESIGN-001｜服务设计｜主体—旅程—前后台—能力—责任—恢复`.

No new parallel service-design framework is created.

## Practice question

When does a Service Blueprint actually prove operational support rather than merely display clean swimlanes?

Candidate rule:

`ACTOR / TASK → FRONTSTAGE STATE → BACKSTAGE CONFIRMATION → SUPPORT / OWNER → FAILURE INJECTION → RECOVERY → FEEDBACK`

## Real practice

The same C04 Return / no-phone service concept was redrawn three times as an editable SVG training asset.

### v1 — REJECT

A visually clean success-path blueprint. It contains Visitor / Frontstage / Backstage / Support lanes, but assumes status, handoff, ownership and capacity will succeed. `NO NETWORK / UNKNOWN / FATIGUE / MISSED HANDOFF` sit outside the model.

Failure knowledge: a complete lane layout is not operational completeness.

### v2 — REVISE

Failure/recovery cards are added, but only as a detached inventory strip. The diagram still does not prove where each failure occurs or what backstage confirmation/owner causes recovery.

Failure knowledge: failure inventory is not recovery design.

### v3 — KEEP FOR TRAINING

Failures are injected in their stage columns. `NO NETWORK / UNKNOWN STATE / MISSED HANDOFF` are connected to the backstage stage that must detect/confirm them. The recovery chain stays visible as `INFORM → MANUAL SUPPORT → RETURN / EXIT`. Unknown operator owner/capacity remain explicitly `OPEN / TBD`; no SLA is invented.

## Independent Design Crit

- First visual: KEEP — actor journey remains the primary horizontal read.
- Composition: KEEP — five stages are readable before lane detail.
- Proportion/hierarchy: KEEP — Visitor/Frontstage lead; Backstage/Support are near-read; Failure/Recovery is distinct but subordinate.
- Typography: KEEP for training — stage, lane, action and truth-boundary levels remain distinguishable.
- Material/spatial realism: N/A; this is a service-system diagram, not spatial evidence.
- Scale: 1800×1120 master plus 600px distance derivative.
- Node/relationship legibility: KEEP after v3 — high-risk failures are stage-bound instead of floating.
- Interaction: N/A.
- Narrative: KEEP — Return remains the service spine; optional content can suspend without breaking exit/return logic.
- Professional completeness: KEEP FOR TRAINING only.

Operational truth remains HOLD: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION`. No staffing, transport capacity, response time, operator ownership or real-time state is asserted.

## Skill delta

Existing Skill modified: `oleander-skills/oleander-data-viz/SKILL.md`.

Added `Service-blueprint causality and recovery gate` because the prior Skill could visualize diagrams but did not distinguish a success-only swimlane from a causally complete failure/recovery blueprint.

The gate adds:

- actor/task first, not fixed-lane-first;
- stage-bound failure injection;
- frontstage state ↔ backstage confirmation binding;
- explicit support/owner/capacity gaps;
- no invented SLA/capacity;
- non-digital recovery proof where the journey requires it;
- whole-system and stage-level reviews;
- separate diagram-quality and operational-truth verdicts.

## Transfer

Applicable to service blueprints, route/return services, museum/visitor operations, retail/service journeys, product-service systems, onboarding/support systems and digital+physical handoffs.

Not sufficient for engineering, staffing plans, emergency procedures, accessibility compliance, legal SLA, real-time operations, or field validation.

## Source boundary

- C04 v0.2 `CH09-P06` authoring candidate.
- Notion `FW-SERVICE-DESIGN-001` canonical service-design framework.
- Training-only SVG. No C04 route or geometry authority changed.
