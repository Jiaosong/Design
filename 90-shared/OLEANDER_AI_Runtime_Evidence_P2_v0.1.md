# OLEANDER AI Runtime Evidence P2 v0.1

Status: ACTIVE measurement protocol when present on `main` / scope-limited evidence only / not evidence of model reliability
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

Failure count is diagnostic, not a target to minimize. Better detection may increase the count while reducing escape.

### M2 | Human Override Rate
`qualified human overrides / AI recommendations that reached a human decision gate`

An override means the human rejects or materially changes an AI recommendation after reviewing its evidence. AI self-correction does not count as a human override.

There is no universal target direction. A high rate can indicate weak AI alignment or healthy oversight; a low rate can indicate strong alignment or passive rubber-stamping. Interpret with task class, evidence quality and decision consequences.

### M3 | Recommendation → Reality-test Survival Rate
`recommendations retained after a qualifying reality test / recommendations that completed a qualifying reality test`

Reality tests include physical prototype, site measurement, user test, browser/device test, production sample or qualified professional simulation/inspection where applicable. Pure AI critique is not a reality test.

A high survival rate is not automatically good: it may mean strong recommendations, easy cases or weak tests. Always retain test severity and failure modes.

### M4 | Blocker Escape Rate
`confirmed blockers first detected after release / confirmed blockers with an explicit release opportunity`

Each failure event must record `release_opportunity: true|false`. A blocker that never approached a release/publication/execution gate does not enter this denominator. A blocker caught by CI or review before `main`/publication is a prevention success, not an escape.

Lower escape is desirable only when detection coverage remains stable; do not improve the number by narrowing what gets inspected.

### M5 | Asset Provenance Coverage
`eligible assets with complete required provenance manifest / all eligible assets in the audited release set`

Do not calculate until an explicit asset inventory defines the denominator. Higher coverage is desirable, but coverage does not imply that rights are cleared or provenance claims are cryptographically authentic.

### M6 | Retrieval Miss / Wrong-Authority Rate
For qualified retrieval audit runs:
- `retrieval misses / audited queries`
- `wrong-authority selections / audited queries`

Golden-query corpus errors are governance-corpus failures; they are not automatically counted as live retrieval misses. A metric-eligible retrieval audit must contain at least one audited query.

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
- Release opportunity: true / false
- Confirmed status
- Metric eligibility
- Human override flag
- Recommendation ID for human decisions and reality-test records
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

## Anti-Goodhart rules
- Do not optimize failure count downward by detecting less.
- Do not optimize Human Override toward zero.
- Do not optimize Reality Survival upward by weakening tests.
- Do not improve Retrieval metrics by shrinking the query set to easy cases.
- Do not improve Provenance Coverage by redefining eligible assets after seeing results.
- Every denominator definition is fixed before rate calculation and remains visible in the report.

## First baseline boundary — 2026-08-10
The initial dataset may include verified P0/P1 implementation incidents from PR #20 and #21 under `GOVERNANCE-INFRA` only.

It must not claim:
- human override rate until qualified AI Recommendation Cards reach a human gate;
- recommendation survival rate until a real-world test exists;
- retrieval miss rate from a Golden Query authoring error;
- provenance coverage until an explicit eligible asset inventory is audited;
- model reliability from static CI.

The four initial failures all have explicit `release_opportunity=true` because they were on PR paths approaching `main`, and all were detected pre-release.

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
