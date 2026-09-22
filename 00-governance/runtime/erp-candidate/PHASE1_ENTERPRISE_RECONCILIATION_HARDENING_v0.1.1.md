# OLEANDER Enterprise Phase 1 Reconciliation Hardening v0.1.1

Status: **EV2 candidate / non-authoritative / real cases not run**

This successor repairs five defects confirmed by adversarial readback against the merged Phase-1 v0.1 baseline `9c8a9580626cc1505308eec6779dd4f3756e9761`.

## Confirmed defects repaired

1. **EXPLICIT state fact false ALLOW** ? every unconsumed `blocking_semantics=EXPLICIT` state fact now creates a fail-closed blocker.
2. **Cross-carrier contradiction false ALLOW** ? positive/detail state and blocking top-level state for the same subject/family create an explicit contradiction and HOLD.
3. **Direct-only change propagation** ? change impact now follows a declared, bounded, relation-specific policy with cycle protection and smallest-materially-affected scope.
4. **Free-text or receipt-as-authority refs** ? every blocker/action now carries an authority-resolution object. A specific owner is used only when an existing kernel authority binding resolves it; otherwise the required owner remains explicitly unresolved and the authority contract ref is preserved.
5. **Untyped action sets** ? reconciliation now emits typed `action_requests`; legacy `reopen_set / rerun_set / review_set / required_readback_set` are compatibility projections derived only from those actions.

## Typed actions

- `RERUN_WORK` ? target must be a real kernel Work item.
- `REOPEN_REVIEW` ? target must be a Review identity.
- `REVIEW_SUBJECT` ? subject requires bounded review/impact reconciliation.
- `REQUIRE_READBACK` ? subject requires a new/read current readback; requested output class is `READBACK`.
- `REVALIDATE_CONFIGURATION` ? reserved for explicit configuration revalidation rules.

## Impact propagation

The active policy is `OLEANDER_ENTERPRISE_RECONCILIATION_POLICY_v0.1.json`.

Phase-1 automatic propagation is intentionally bounded. Unknown relation types do not propagate automatically. Current declared rules include:

- changed artifact <- `JOB_PRODUCES_ARTIFACT` -> rerun producer Job;
- changed artifact -> `ARTIFACT_REVIEWED_BY` -> reopen Review;
- changed implementation -> `SATISFIES / VERIFIES / VALIDATES / IMPLEMENTS` -> review the affected requirement/subject;
- changed object <- `NONCONFORMANCE_AFFECTS` -> review related NCR and continue one bounded quality-impact step;
- affected NCR <- `CAPA_ADDRESSES` -> review related CAPA effectiveness.

The engine uses a visited-ref/rule boundary and maximum depth from policy. Closed changes do not propagate actions.

## Authority resolution

`blocking_authority_ref` remains only as a compatibility effective ref. The authoritative machine field is `blocking_authority`:

- `RESOLVED_EXISTING_BINDING` ? `owner_ref` must exist in kernel authority bindings;
- `UNRESOLVED_REQUIRED_OWNER` ? no owner is invented; the required owner kind and existing authority-contract path remain visible;
- `DERIVED_COORDINATION_ONLY` ? used only for derived coordination state that has no independent approval authority.

An unresolved required owner never becomes a fabricated owner and contributes to HOLD whenever a blocker/action needs that authority.

## Advance rule

`ALLOW` is legal only when all of the following are empty:

- blocking conditions;
- typed action requests;
- contradictions;
- unresolved authority conflicts;
- unresolved authority requirements.

Additionally, no `EXPLICIT` state fact may escape blocker coverage.

`ALLOW` still means only **Phase-1 coordination clear within observed scope**. It is not Design KEEP, Professional PASS, statutory approval, acceptance or Project Promotion.
