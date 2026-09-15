# OLEANDER TP5 Configuration / Change Stress Replay — Git + GitHub Protected Branch / Merge Queue — 2026-09-15

Status: **DRAFT EXTERNAL REPLAY / NOT CURRENT / SOURCE-BOUNDED**.

Purpose: stress-test P5 `Baseline / Change / Staleness / Carry-forward / Concurrency / Rollback` using publicly documented Git/GitHub behavior rather than an invented project scenario.

This replay maps official Git/GitHub semantics into OLEANDER configuration-management concepts. It does not claim that Git/GitHub's terminology is identical to OLEANDER governance terminology.

---

## 1. Official source facts used

Primary source facts, with explicit official bindings verified 2026-09-15:

1. GitHub protected branches can require status checks before merging and can require the branch to be up to date with the base branch.
   - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
2. Required checks must pass on the latest commit SHA; successful checks on earlier commits do not satisfy the latest-head requirement.
   - https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks
3. GitHub merge queues test a temporary `merge_group` configuration that combines the pull request with the latest base branch and, where relevant, pull requests ahead of it in the queue.
   - https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue
4. The merge-group SHA differs from the pull-request SHA and required CI must report against that merge-group context.
5. A queued pull request can be removed when the merged-group configuration fails required checks or conflicts with the base branch.
6. `git revert` records new commit(s) that reverse effects of earlier commits; it preserves the historical commits being reversed.
   - https://git-scm.com/docs/git-revert
7. GitHub reverting a merged pull request creates a new pull request that reverts the original merge commit.
   - https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/reverting-a-pull-request
8. `git reset` moves `HEAD`/branch tip to another commit; hard reset can also make working tree/index match the target and can discard local state.
   - https://git-scm.com/docs/git-reset
9. Git records `ORIG_HEAD` for operations that move HEAD drastically, including reset, merge and rebase.
   - https://git-scm.com/docs/gitrevisions

Source boundary:

- exact Git/GitHub behavior above = source-supported;
- OLEANDER Baseline/Change/Evidence mapping below = analytical replay;
- this replay does not assert that GitHub branch protection is a complete substitute for engineering configuration management.

---

# 2. OLEANDER analytical mapping

Minimum mapping:

```text
protected target branch / accepted target revision
    ≈ controlled promotion target / Current baseline pointer

pull-request head SHA
    ≈ candidate configuration revision

required status checks on head SHA
    ≈ configuration-bound assurance evidence

merge-group SHA
    ≈ derived integration configuration

merge to target branch
    ≈ authorized promotion / new Current configuration

revert commit / revert PR
    ≈ compensating Change producing a new descendant configuration

reset of branch pointer
    ≈ pointer rewrite / historical re-selection, not a compensating Change
```

The mapping is bounded: Git objects are used here because their revision semantics are exact and auditable, not because every OLEANDER project must use Git as its configuration system.

---

# 3. Exact revision identity versus semantic equivalence

A status check can be valid for one exact commit SHA and invalid for a later SHA even when many files are unchanged.

This exposes two different configuration identities:

```text
EXACT_REVISION_IDENTITY
= exact immutable revision/fingerprint being evaluated

SEMANTIC_PROPERTY_EQUIVALENCE
= declared protected properties are proven unchanged/equivalent across two revisions
```

They must not be conflated.

A later revision cannot inherit exact-SHA evidence automatically. It may inherit a bounded result only if OLEANDER explicitly proves applicability/equivalence for the relevant properties and claim.

### Replay result

`UNDERMODELED → EXPLICIT CONFIGURATION IDENTITY MODE REQUIRED`.

### Replay rule

`P5/CFG-RP05 EXACT_REVISION_IDENTITY_AND_SCOPED_SEMANTIC_EQUIVALENCE_ARE_DISTINCT; EVIDENCE_BOUND_TO_EXACT_REVISION_CANNOT_AUTO_CARRY_TO_A_NEW_REVISION`.

Suggested field:

```yaml
configuration_identity_mode:
  EXACT_REVISION
  SCOPED_SEMANTIC_EQUIVALENCE
  DERIVED_INTEGRATION_CONFIGURATION
  HISTORICAL_REFERENCE
```

---

# 4. Required-check evidence is configuration-bound

GitHub explicitly requires required checks to succeed against the latest commit SHA. Earlier-success evidence does not satisfy a later head.

OLEANDER consequence:

`Evidence PASS` must bind not only to method/criterion but also to the configuration identity actually tested.

Minimum applicability record:

```yaml
evidence_applies_to:
  configuration_ref:
  configuration_identity_mode:
  property_scope:
  criterion_version:
  environment_or_condition_ref:
```

### Replay result

`CONFIRMED / STRENGTHENED`.

### Replay rule

`P5/CARRY-RP04 CONFIGURATION_BOUND_ASSURANCE_REQUIRES_EXPLICIT_TARGET_REVISION_OR_PROVEN_EQUIVALENCE_SCOPE; EARLIER_REVISION_PASS_IS_NOT_CURRENT_PASS`.

This is stronger than simply checking artifact timestamps.

---

# 5. Merge queue proves concurrent composition needs new assurance

A pull request can pass CI individually and still require new checks after being placed into a merge queue because the queue tests it together with:

- latest target branch state; and
- changes from pull requests ahead of it.

Therefore two individually verified changes do not imply their composition is verified.

Analytical model:

```text
BASE B0
  ├─ Change A → Candidate A → PASS(A)
  └─ Change B → Candidate B → PASS(B)

queued composition:
B0 + A + B → Integration Configuration M1
                 ↓
             requires PASS(M1)
```

### Replay result

`CONCURRENCY REPLAY CONFIRMED`.

### Replay rule

`P5/CONC-RP03 INDIVIDUALLY_ASSURED_CONCURRENT_CHANGES_REQUIRE_REASSURANCE_ON_THE_ACTUAL_COMPOSED_INTEGRATION_CONFIGURATION_WHEN_THEIR_TARGET_BASE_OR_INTERACTION_CONTEXT_CHANGES`.

This applies far beyond software: coordinated geometry, content+code releases, product+firmware, exhibition+AV, etc.

---

# 6. Candidate branch versus Current baseline

A PR head can be highly reviewed and fully passing while still not being the protected target branch Current state.

OLEANDER consequence:

```text
CANDIDATE PASS ≠ CURRENT PROMOTION
```

Promotion additionally requires target authority/policy satisfaction.

### Replay result

`CONFIRMED`.

### Replay rule

`P5/PROM-RP05 CANDIDATE_CONFIGURATION_ASSURANCE_PASS_DOES_NOT_MOVE_CURRENT_BASELINE_POINTER_WITHOUT_AUTHORIZED_PROMOTION_EVENT`.

This reinforces P1 promotion authority and P5 baseline pointer separation.

---

# 7. Revert is not identity restoration

`git revert` creates a new commit that reverses earlier changes. It does not move history back to the old commit.

Even if resulting content resembles a previous state, the new revision has:

- different history;
- different revision identity;
- potentially different surrounding/base context;
- potentially different environment/dependencies.

Therefore OLEANDER must distinguish:

```text
EXACT_REVERSION
= the controlled system is genuinely restored to the prior configuration identity and conditions

REIMPLEMENT_PRIOR_INTENT
= a new configuration attempts to reproduce prior behavior/content
```

A Git revert is normally the second kind from the viewpoint of revision identity.

### Replay result

`ROLLBACK DISTINCTION CONFIRMED`.

### Replay rule

`P5/ROLL-RP04 COMPENSATING_CHANGE_OR_REVERT_CREATES_A_NEW_CONFIGURATION_IDENTITY; IT_MUST_NOT_BE_TREATED_AS_AUTOMATIC_REACTIVATION_OF_PRIOR_EVIDENCE_OR_BASELINE_IDENTITY`.

---

# 8. Reset / pointer rewrite is a different operation

Git reset can move HEAD/branch tip to another commit; hard reset can additionally rewrite index/working-tree state. This is fundamentally different from revert.

OLEANDER consequence:

- pointer rewrite/reselection must be modeled separately from compensating Change;
- historical lineage must not be silently deleted in governance records;
- on shared/protected Current authority, destructive pointer rewrite should require explicit exceptional authority and lineage handling rather than being treated as ordinary rollback.

### Replay result

`CONFIRMED_WITH GOVERNANCE DELTA`.

### Replay rule

`P5/ROLL-RP05 POINTER_REWRITE_AND_COMPENSATING_CHANGE_ARE_DISTINCT_ROLLBACK_MECHANISMS; SHARED_CURRENT_POINTER_REWRITE_REQUIRES_EXPLICIT_EXCEPTION_AUTHORITY_AND_LINEAGE_PRESERVATION`.

Suggested rollback mechanism field:

```yaml
rollback_mechanism:
  COMPENSATING_CHANGE
  POINTER_RESELECTION
  EXACT_RESTORE_FROM_CONTROLLED_BASELINE
  REIMPLEMENT_PRIOR_INTENT
  ROLLBACK_REJECTED
```

---

# 9. Revert does not guarantee evidence carry-forward

Suppose:

```text
B0 passed assurance E0
B1 changed behavior
B2 reverts B1's patch
```

Even if B2's source content for a protected property matches B0, OLEANDER cannot infer that all B0 evidence is Current because:

- integration context may differ;
- requirements may have changed;
- environment/inputs may have changed;
- other concurrent changes may be present;
- the evidence may have depended on properties outside the reverted patch.

Therefore rollback needs a post-rollback applicability decision.

### Replay result

`CONFIRMED`.

### Replay rule

`P5/CARRY-RP05 ROLLBACK_OR_REVERT_REQUIRES_POST_ROLLBACK_EVIDENCE_APPLICABILITY_REVIEW; CONTENT_SIMILARITY_ALONE_CANNOT_REACTIVATE_HISTORICAL_ASSURANCE`.

---

# 10. Base update creates staleness without changing the candidate's own patch

A PR's patch may remain unchanged while the base branch changes underneath it. GitHub can require the branch to be up to date, and merge queue explicitly retests against latest base.

This is a crucial configuration lesson:

`object-local bytes unchanged` does not imply `integration configuration unchanged`.

### Replay result

`UNDERMODELED → CONTEXTUAL STALENESS REQUIRED`.

### Replay rule

`P5/STALE-RP05 DEPENDENCY_OR_BASELINE_CONTEXT_CHANGE_CAN_STALE_INTEGRATION_ASSURANCE_EVEN_WHEN_THE_LOCAL_CHANGESET_BYTES_ARE_UNCHANGED`.

This complements the opposite rule already learned from KH46:

- derivative/support hash change must not automatically stale unchanged upstream source;
- but upstream/base context change **can** stale an unchanged local candidate's integration evidence.

The two rules are not contradictory because staleness follows dependency scope, not file recency.

---

# 11. Merge-group configuration is ephemeral but assurance-significant

A merge-group branch/SHA may be temporary and never become a long-lived named baseline, yet its successful checks are material to promotion.

Therefore OLEANDER configuration control needs a category for:

`DERIVED_INTEGRATION_CONFIGURATION`.

Such a configuration:

- may be temporary;
- still requires stable identity while evaluated;
- may own assurance evidence;
- may be superseded immediately after queue/base changes;
- does not need to become a permanent canonical Project object if audit receipts preserve lineage.

### Replay result

`CONFIRMED`.

### Replay rule

`P5/CFG-RP06 EPHEMERAL_DERIVED_INTEGRATION_CONFIGURATION_MAY_BE_ASSURANCE_SIGNIFICANT_WITHOUT_BECOMING_LONG_LIVED_CURRENT_BASELINE`.

This also limits over-objectification.

---

# 12. Configuration status accounting needs evidence-head binding

A useful configuration accounting row must separate:

```yaml
candidate_revision:
base_revision:
integration_revision:
required_checks:
check_target_revision:
check_result:
promotion_target:
promotion_state:
```

Without this, a dashboard can mistakenly show a green check from an old head as if it applied to the latest candidate.

### Replay result

`CONFIRMED`.

### Replay rule

`P5/CSA-RP02 CONFIGURATION_STATUS_ACCOUNTING_MUST_BIND_ASSURANCE_RESULT_TO_THE_EXACT_OR_DECLARED_EQUIVALENT_CONFIGURATION_IT_EVALUATED`.

---

# 13. Concurrent change collision has two classes

GitHub merge queue reveals two different failure modes:

### A. Syntactic/structural collision

Changes cannot compose cleanly (merge conflict).

### B. Semantic/integration collision

Changes compose mechanically but combined checks fail.

OLEANDER must preserve both.

### Replay result

`UNDERMODELED → COLLISION TYPE REQUIRED`.

Suggested field:

```yaml
change_collision_type:
  NONE
  STRUCTURAL_CONFLICT
  SHARED_VARIABLE_CONFLICT
  INTERFACE_CONFLICT
  REQUIREMENT_CONFLICT
  SEMANTIC_INTEGRATION_FAILURE
  AUTHORITY_CONFLICT
  UNKNOWN
```

### Replay rule

`P5/CONC-RP04 SUCCESSFUL_MECHANICAL_MERGE_DOES_NOT_PROVE_SEMANTIC_OR_INTEGRATION_COMPATIBILITY; COLLISION_TYPE_MUST_DISTINGUISH_STRUCTURAL_AND_SEMANTIC_FAILURE`.

---

# 14. Stress-replay result against current P5 OPEN items

Previously open P5 replay gaps now resolve as follows:

- `rollback_replay_state`: **CONFIRMED_EXTERNAL_REPLAY_WITH_DISTINCTION**;
- `concurrency_replay_state`: **CONFIRMED_EXTERNAL_REPLAY**;
- evidence carry-forward: **CONFIRMED_REQUIRES_EXACT_REVISION_OR_SCOPED_EQUIVALENCE**;
- branch/variant baseline: **CONFIRMED**;
- promotion-breaking versus derivative-only change: already supported by KH46 + this replay;
- contextual staleness from changing base: **NEW CONFIRMED DELTA**.

---

# 15. Required P5 machine refinements

Add:

1. `configuration_identity_mode`;
2. `rollback_mechanism`;
3. `change_collision_type`;
4. assurance-to-configuration binding fields;
5. explicit base/integration revision in configuration status accounting;
6. contextual staleness from changed dependencies/base;
7. `DERIVED_INTEGRATION_CONFIGURATION` as assurance-significant but optionally ephemeral.

No new top-level Object Class is required.

---

# 16. Replay-derived rules

- `P5/CFG-RP05`
- `P5/CARRY-RP04`
- `P5/CONC-RP03`
- `P5/PROM-RP05`
- `P5/ROLL-RP04`
- `P5/ROLL-RP05`
- `P5/CARRY-RP05`
- `P5/STALE-RP05`
- `P5/CFG-RP06`
- `P5/CSA-RP02`
- `P5/CONC-RP04`

---

# 17. TP5 disposition

`TP5 CONFIGURATION / CHANGE STRESS REPLAY = COMPLETE_WITH_DELTAS`.

The replay confirms that P5 must reason over **configuration identity + dependency context + promotion authority + evidence applicability**, not filenames or timestamps.

No Current promotion is authorized.
