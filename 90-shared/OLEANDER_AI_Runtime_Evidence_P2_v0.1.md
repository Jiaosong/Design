# OLEANDER AI Runtime Evidence P2 v0.1

Status: DRAFT for review
Canonical method source: Notion `01B-8｜AI Runtime Evidence Protocol v0.1｜P2 真实运行证据`

## Purpose
P0 governs whether AI may be used and whether a changed configuration may be promoted. P1 governs runtime failure, trust calibration and provenance. P2 measures whether those controls improve real OLEANDER work.

P2 does not create more AI authority. It creates operational evidence about AI collaboration quality.

## Core rule
Never report a zero rate when no eligible denominator exists. Use `N/A — insufficient eligible evidence`.

Every metric must be segmented by scope. Governance-infrastructure evidence cannot be silently presented as product, architecture, brand or website runtime performance.

## Evidence scopes
- `GOVERNANCE-INFRA`: protocols, CI, eval corpus, repository controls.
- `DESIGN-RUNTIME`: cross-domain real design work.
- `PRODUCT`
- `SPATIAL-ARCH`
- `WEBSITE`
- `BRAND`
- `DATA-VIZ`
- `KNOWLEDGE`

## P2 metrics

### M1 | F1–F3 Failure Records
Count confirmed P1 failures with evidence URL, category, escalation, containment and outcome.

### M2 | Human Override Rate
`qualified human overrides / AI recommendations that reached a human decision gate`

An override means the human rejects or materially changes an AI recommendation after reviewing its evidence. AI self-correction does not count as a human override.

### M3 | Recommendation → Reality-test Survival Rate
`recommendations retained after a qualifying reality test / recommendations that completed a qualifying reality test`

Reality tests include physical prototype, site measurement, user test, browser/device test, production sample or qualified professional simulation/inspection where applicable. Pure AI critique is not a reality test.

### M4 | Blocker Escape Rate
`confirmed blockers first detected after release / all confirmed blockers with a release opportunity`

A blocker caught by CI or review before `main`/publication is a prevention success, not an escape.

### M5 | Asset Provenance Coverage
`eligible assets with complete required provenance manifest / all eligible assets in the audited release set`

Do not calculate until an explicit asset inventory defines the denominator.

### M6 | Retrieval Miss / Wrong-Authority Rate
For qualified retrieval audit runs:
- `retrieval misses / audited queries`
- `wrong-authority selections / audited queries`

Golden-query corpus errors are governance-corpus failures; they are not automatically counted as live retrieval misses.

## Minimum runtime event record
- Event ID
- Date/time
- Scope
- Event type
- Project/object/version
- P1 failure category when applicable
- Escalation level when applicable
- Evidence URL / immutable reference
- Detection stage: PRE-RELEASE / POST-RELEASE / RUNTIME / N-A
- Confirmed status
- Metric eligibility
- Human override flag
- Reality-test status/outcome when applicable
- Blocker escaped flag when applicable
- Numerator/denominator payload for audit events
- Containment / correction / re-test
- Residue / next regression case

## Evidence quality
- `CONFIRMED`: supported by repository record, CI log, signed-off test, measured observation or equivalent traceable evidence.
- `PROVISIONAL`: event is plausible but evidence or denominator is incomplete.
- `REJECTED`: should not enter metrics.

Only `CONFIRMED` + `metric_eligible=true` events enter reported rates.

## First baseline boundary — 2026-08-10
The initial dataset may include verified P0/P1 implementation incidents from PR #20 and #21 under `GOVERNANCE-INFRA` only.

It must not claim:
- human override rate until qualified AI Recommendation Cards reach a human gate;
- recommendation survival rate until a real-world test exists;
- retrieval miss rate from a Golden Query authoring error;
- provenance coverage until an explicit eligible asset inventory is audited;
- model reliability from static CI.

## Collection sequence
`AI Recommendation / AI Run → P1 record → Evidence URL → P2 eligibility check → Runtime event → Metric aggregation → Human review → Regression case / process change`

## Review cadence
- Per blocker: record immediately.
- Per release / project gate: calculate scope-specific metrics.
- Monthly or after >=10 eligible events: review trends, not just cumulative totals.
- Any F2/F3 or post-release blocker: immediate review regardless of sample size.

## Decision use
P2 metrics may justify:
- adding or changing a Golden Case;
- narrowing AI permission;
- changing a prompt/skill/tool;
- requiring more reality testing;
- changing retrieval authority rules;
- improving provenance workflow;
- P0 `HOLD` or `ROLLBACK`.

P2 metrics cannot automatically approve a design, close a rights/safety gate, or replace professional and reality evidence.
