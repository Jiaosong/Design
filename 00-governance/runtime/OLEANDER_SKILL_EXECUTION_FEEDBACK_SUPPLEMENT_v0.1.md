# OLEANDER Skill Execution Feedback Supplement v0.1

Status: **ACTIVE SHARED SUPPLEMENT / ALL ELEVEN CORE SKILL IDENTITIES / NO NEW SKILL**
Decision date: **2026-09-12**
Scope: **real Skill execution → bounded project learning → existing Practice/Skill/regression improvement when evidence supports it**

## 0｜Purpose

Every OLEANDER core Skill identity must be able to learn from real execution without inventing a parallel Skill, knowledge base, state database or promotion path.

This supplement standardizes the feedback layer after actual execution/readback:

`REAL SKILL SELECTION → REAL EXECUTION → NATIVE ARTIFACT → ACTUAL READBACK → OUTCOME → FAILURE/SUCCESS CLASSIFICATION → ROOT CAUSE → REPAIR/RETEST OR HOLD → TRANSFER RULE CANDIDATE → FEEDBACK CLASSIFICATION → REGRESSION DELTA WHEN MATERIAL → CROSS-CONTEXT MATURITY → EXISTING AIG-01 / HUMAN PROMOTION PATH`

It complements, and does not replace:

- each core Skill's own `SKILL.md` / owner-local Practice;
- Current Knowledge / Notion authority;
- `OLEANDER_EXECUTION_RECEIPT_v1.0` as the single execution-instance carrier;
- AIG-01 evaluation/regression and lifecycle promotion governance.

## 1｜Applies to all eleven core identities

This policy applies to the eleven identities in `oleander-skills/SKILL_REGISTRY_v1.1.json`, regardless of whether the identity is installed, candidate, composite-route or candidate-draft.

Applying this policy does **not** change `installation_state`, lifecycle state, owner status or promotion eligibility.

## 2｜Usage provenance is mandatory

Use `PROJECT_USAGE_EVIDENCE` only when direct evidence shows that the exact Skill/version/commit or owner-local extension was actually read/selected before or during the material action and materially influenced the execution.

Post-hoc artifact, diff, commit, screenshot, readback or verdict proves project change. It does **not** by itself prove historical Skill invocation.

When the project learning is real but execution-time Skill provenance is absent, classify it:

`PROJECT_LEARNING_EVIDENCE / SKILL_FEEDBACK_ORPHAN`.

An orphan may still produce bounded learning for an existing owner after readback and root-cause analysis. It must not be rewritten as historical `PROJECT_USAGE_EVIDENCE`.

## 3｜Material feedback trigger

Do not mutate a Skill merely because it ran.

Open `skill_feedback` only when execution/readback exposes a **material reusable delta**, such as:

- a repeatable failure mode not adequately prevented by the existing contract;
- an existing rule whose wording/routing allowed the wrong action;
- a runtime/adapter incompatibility that materially affects legal Skill execution;
- a missing regression that allowed a known failure to recur;
- a bounded reusable success rule with evidence strong enough to test outside the current object.

Do not mutate a Skill when the observation is only:

- project-specific taste/preference;
- one-off content difference;
- no actual artifact;
- no actual readback;
- no causal diagnosis;
- no repair/retest or legitimate HOLD boundary;
- no transferable rule/boundary;
- no material delta from the existing Skill/Practice.

Canonical rule:

`NO MATERIAL SKILL DELTA = NO SKILL MUTATION`.

## 4｜Gap route before feedback action

Classify where the failure actually belongs before editing a Skill:

- `PROJECT_SPECIFIC` — keep local; do not generalize;
- `DESIGN_LAYER_GAP` — upstream design relation/process failed before execution detail;
- `SKILL_CONTRACT_GAP` — the existing Skill lacks or misstates a reusable execution rule;
- `RUNTIME_ADAPTER_GAP` — implementation/runtime compatibility or tool contract is causal;
- `KNOWLEDGE_GAP_ROUTE` — missing Current Knowledge/source authority must be routed to its existing knowledge owner, not copied into the Skill;
- `REGRESSION_GAP` — the rule exists but machine/golden regression did not prevent recurrence.

Fix the causal owner. Do not encode a runtime bug as a design rule or a project-specific exception as universal knowledge.

## 5｜Allowed feedback actions

Reuse the existing owner-local vocabulary:

- `NONE_PROJECT_SPECIFIC`
- `UPDATE_EXISTING_PRACTICE`
- `UPDATE_EXISTING_SKILL`
- `ADD_REGRESSION_RULE`
- `CROSS_CONTEXT_TEST_NEEDED`

Multiple actions may be combined only when each is independently justified by the same evidence chain.

Examples:

- one project exposes a plausible reusable rule, but transfer is unproven → `UPDATE_EXISTING_PRACTICE + CROSS_CONTEXT_TEST_NEEDED`;
- existing Skill wording directly permitted the causal failure and repaired wording can be regression-tested → `UPDATE_EXISTING_SKILL + ADD_REGRESSION_RULE`;
- failure is a Blender/API version mismatch → route `RUNTIME_ADAPTER_GAP`, not an unrelated design-method rewrite;
- missing engineering value is not a Skill failure → `KNOWLEDGE_GAP_ROUTE` / specialist HOLD.

## 6｜Minimum evidence for Skill/Practice mutation

For a material feedback action, preserve:

`SKILL REF + VERSION/COMMIT → RULE/CAPABILITY USED → NATIVE ARTIFACT → ACTUAL READBACK → OUTCOME → GAP ROUTE → ROOT CAUSE OR SUCCESS MECHANISM → REPAIR/RETEST OR HOLD → TRANSFER RULE CANDIDATE → TRANSFER BOUNDARY → FEEDBACK ACTION`.

For a failure-derived rule, root cause and repair/retest are mandatory unless a legitimate external/specialist HOLD prevents retest. A failed tool call without artifact/readback is not enough to rewrite a reusable Skill.

## 7｜Per-run carrier: existing Execution Receipt only

`OLEANDER_EXECUTION_RECEIPT_v1.0` remains the single execution-instance carrier.

When material Skill learning occurs, use its conditional `skill_feedback` section. Do not create a parallel Skill-feedback receipt database or another Project State.

If there is no material Skill delta, omit the section.

## 8｜Regression consequence

When a Skill/Practice rule changes because a real failure escaped the current safeguards, decide whether the same failure can be encoded as a Golden/regression case.

`UPDATE_EXISTING_SKILL` should normally be accompanied by `ADD_REGRESSION_RULE` when the behavior is machine- or corpus-testable.

A regression proves only that the declared case now passes. It does not prove universal maturity, design quality, field truth or promotion.

## 9｜Cross-context maturity and promotion boundary

New reusable learning begins as bounded project/Practice evidence unless stronger authority already exists.

Use materially different contexts to test transfer. Do not manufacture a project or reopen closed work solely to promote a Skill.

Hard separations:

- `EXECUTION SUCCESS ≠ SKILL IMPROVEMENT`
- `ONE PROJECT FAILURE ≠ UNIVERSAL RULE`
- `PROJECT LEARNING ≠ CROSS-CONTEXT MATURITY`
- `CI PASS ≠ SKILL PROMOTION`
- `SKILL SELF-UPDATE ≠ HUMAN PROMOTION`

Candidate/project learning never self-promotes. Promotion continues through existing lifecycle/AIG-01/human authority.

## 10｜Project execution must not be blocked by feedback maturity

Skill feedback is downstream learning from the execution. A project artifact that is otherwise valid does not become invalid merely because the learning remains `NONE_PROJECT_SPECIFIC`, `CROSS_CONTEXT_TEST_NEEDED` or `SKILL_FEEDBACK_ORPHAN`.

Conversely, a successful project artifact does not automatically prove the Skill is improved.

## 11｜Shared trace template

For future real use, the canonical trace is:

`PROJECT_ID / OBJECT_ID → SKILL_REF + VERSION/COMMIT → USAGE_PROVENANCE_STATE → RULE/CAPABILITY_USED → NATIVE ARTIFACT → ACTUAL READBACK → SUCCESS/FAILURE → GAP_ROUTE → ROOT_CAUSE → REPAIR/RETEST or CLEAR HOLD → DOWNSTREAM EFFECT → TRANSFER_RULE_CANDIDATE → TRANSFER_BOUNDARY → FEEDBACK_ACTION → CROSS_CONTEXT_STATUS → REGRESSION_REF / SKILL_CHANGE_REF WHEN MATERIAL`.

## 12｜Does not prove

This supplement does not prove that a Skill was historically used, that a project design passed, that one learning is universal, that a candidate is installable, that CI establishes maturity, or that an updated Skill may self-promote.
