# OLEANDER AIG-03｜AI Runtime Evidence v0.1

Status: ACTIVE measurement protocol when present on `main` / scope-limited evidence only / not evidence of model reliability
Canonical method source: Notion `AIG-03｜AI Runtime Evidence Protocol v0.1｜真实运行证据`

## Namespace rule
`AIG-03` is the current runtime-evidence identifier. `P2` is reserved by the project axis for `Project`. Historical event IDs such as `P2-E011` remain immutable audit identifiers only; new runtime events use the `AIG3-E###` namespace.

## Purpose
AIG-01 governs whether AI may be used and whether a changed configuration may be promoted. AIG-02 governs runtime failure, trust calibration and provenance. AIG-03 measures whether those controls improve real OLEANDER work.

AIG-03 does not create more AI authority. It creates operational evidence about AI collaboration quality.

## Core rule
Never report a zero rate when no eligible denominator exists. Use `N/A — insufficient eligible evidence`.

Every metric must be segmented by scope. Governance-infrastructure evidence cannot be silently presented as product, architecture, brand or website runtime performance.

## Evidence scopes
- `GOVERNANCE-INFRA`
- `DESIGN-RUNTIME`
- `PRODUCT`
- `SPATIAL-ARCH`
- `WEBSITE`
- `BRAND`
- `DATA-VIZ`
- `KNOWLEDGE`

## AIG-03 metrics
### M1 | F1–F3 Failure Records
Count confirmed AIG-02 failures with evidence URL, category, escalation, containment and outcome.

### M2 | Human Override Rate
`qualified human overrides / AI recommendations that reached a human decision gate`

### M3 | Recommendation → Reality-test Survival Rate
`recommendations retained after a qualifying reality test / recommendations that completed a qualifying reality test`

### M4 | Blocker Escape Rate
`confirmed blockers first detected after release / confirmed blockers with an explicit release opportunity`

### M5 | Asset Provenance Coverage
`eligible assets with complete required provenance manifest / all eligible assets in the audited release set`

### M6 | Retrieval Miss / Wrong-Authority Rate
For qualified retrieval audit runs:
- `retrieval misses / audited queries`
- `wrong-authority selections / audited queries`

## Minimum runtime event record
- Event ID
- Date/time
- Scope
- Event type
- Project/object/version
- AIG-02 failure category when applicable
- Escalation level when applicable
- Evidence URL / immutable reference
- Detection stage
- Release opportunity
- Confirmed status
- Metric eligibility
- Human override flag
- Recommendation ID
- Reality-test status/outcome when applicable
- Blocker escaped flag when applicable
- Numerator/denominator payload for audit events
- Containment / correction / re-test
- Residue / next regression case

## Evidence quality
- `CONFIRMED`
- `PROVISIONAL`
- `REJECTED`

Only `CONFIRMED` + `metric_eligible=true` events enter reported rates.

## Anti-Goodhart rules
- Do not optimize failure count downward by detecting less.
- Do not optimize Human Override toward zero.
- Do not optimize Reality Survival upward by weakening tests.
- Do not improve Retrieval metrics by shrinking the query set to easy cases.
- Do not improve Provenance Coverage by redefining eligible assets after seeing results.
- Every denominator definition is fixed before rate calculation and remains visible.

## Historical baseline boundary
Existing `P2-*` runtime records remain preserved as audit history and are not renumbered. They are not current project-axis identifiers. Current AIG-03 reporting may consume those historical records where their evidence remains valid, while all new events use `AIG3-*` IDs.

## Collection sequence
`AI Recommendation / AI Run → AIG-02 record → Evidence URL → AIG-03 eligibility check → Runtime event → Metric aggregation → Human review → Regression case / process change`

## Review cadence
- Per blocker: record immediately.
- Per release / project gate: calculate scope-specific metrics.
- Monthly or after >=10 eligible events: review trends.
- Any F2/F3 or post-release blocker: immediate review.

## Decision use
AIG-03 metrics may justify adding/changing a Golden Case, narrowing AI permission, changing a prompt/skill/tool, requiring more reality testing, changing retrieval authority rules, improving provenance workflow, or forcing AIG-01 `HOLD` / `ROLLBACK`.

AIG-03 metrics cannot automatically approve a design, close a rights/safety gate, or replace professional and reality evidence.
