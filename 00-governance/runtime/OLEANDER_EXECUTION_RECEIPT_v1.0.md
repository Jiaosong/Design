# OLEANDER Execution Receipt v1.0

Status: **ACTIVE CURRENT**  
Policy revision: **1.1**  
Decision date: **2026-08-18**  
Scope: **one material execution unit**

## 0｜Purpose

Use one receipt to record the execution instance of the Current resolver/contracts. The receipt is not a new Project State, review framework or Skill.

Policy revision 1.1 adds two mandatory runtime sections for all new receipts:

1. **Constraint Lock**
2. **Flow Completion**

The three pre-policy receipts explicitly allowlisted in the machine contract remain immutable provenance; all future receipts must use the new sections.

## 1｜Identity

- `receipt_id`
- `status = WORKING / REVIEW_PENDING / HOLD / CLOSED`
- `execution_type = PROJECT / TRAINING / SKILL_VALIDATION / GOVERNANCE_RUNTIME`
- `task_id`

## 2｜Authority snapshot

Record Current Root, project/scope authority, Source Authority, Design Authority, relevant Canonical IDs, Current GitHub resolver and actual commit/ref.

The receipt does not replace Project State.

## 3｜Constraint Lock

Resolve before tool/owner selection and record:

- `resolved_from`
- `inheritance_state`
- `active_constraints`
- `revocations`
- `tool_deny`
- `output_deny`
- `creation_deny`
- `required_behaviors`

Each active constraint records:

`constraint_id / constraint_type / normalized_rule / source / scope / status / revocation_rule`.

Supported normalized rules include:

`NO_IMAGE_GENERATION / NO_NEW_SKILL / NO_NEW_METHOD / NO_NEW_FRAMEWORK / USE_EXISTING_OLEANDER_METHODS_AND_SKILLS / FULL_OLEANDER_FLOW_REQUIRED / NO_PRODUCER_SELF_PROMOTION`.

A generic “继续 / 优化 / 再做” does not revoke anything. Only a later explicit user instruction that directly changes the named constraint can release it.

If `NO_IMAGE_GENERATION` is active, image-generation tools and generative-image adapters are forbidden. If `NO_NEW_SKILL / METHOD / FRAMEWORK` is active, gap diagnosis cannot silently authorize creation.

## 4｜Required native output

Record:

`artifact_class / native_format / editable_required / target_runtime / derived_formats`.

A preview, screenshot or chat explanation cannot replace a required editable/native master.

## 5｜Minimum sufficient owner set / DAG

Record `PRIMARY_OWNER` and only supporting nodes actually needed.

Node roles:

`PRIMARY_OWNER / SUPPORTING_OWNER / READ_ONLY_CONSUMER / VALIDATOR / INDEPENDENT_REVIEWER`.

`NO COMPRESSION / NO LOSS` does not mean every Skill must run.

## 6｜Flow Completion

For production/mutation/training/state-changing review work, and whenever `FULL_OLEANDER_FLOW_REQUIRED` is active, record:

- `mode = READ_ONLY_QUERY / MINIMUM_EXECUTION / FULL_OLEANDER_FLOW`
- `required_phases`
- `phase_results`
- `incomplete_required_phases`
- `completion_gate = PASS / FAIL / HOLD`
- `completion_claim_allowed`

Canonical phases:

1. `AUTHORITY_PREFLIGHT`
2. `STICKY_CONSTRAINT_RESOLUTION`
3. `EXISTING_KNOWLEDGE_METHOD_SKILL_RESOLUTION`
4. `REQUIRED_NATIVE_OUTPUT_DEFINITION`
5. `CAPABILITY_AND_MINIMUM_OWNER_SET`
6. `REAL_EXECUTION`
7. `NATIVE_ARTIFACT_AND_TYPED_HANDOFF_RECORD`
8. `ACTUAL_READBACK`
9. `REGRESSION_AS_APPLICABLE`
10. `INDEPENDENT_REVIEW_AS_APPLICABLE`
11. `SYNC_RECEIPT_AND_DRIFT_AS_APPLICABLE`

For full-flow work, Authority, Constraint Resolution, Existing Knowledge/Skill Resolution, Native Output, Minimum Owner Set, Real Execution and Actual Readback cannot be skipped.

Optional phases may be `NOT_APPLICABLE` only with a real reason.

### Closure rule

`status=CLOSED` requires:

- `completion_gate=PASS`
- `incomplete_required_phases=[]`
- no required phase in `FAIL/HOLD`

A plan, method explanation, generated/exported file, PR, CI green, self-check, render pass or regression pass is not enough to close a full-flow task.

## 7｜Native artifacts and handoffs

Every material handoff records the Native Artifact Contract fields, including:

`artifact_id / artifact_role / producer_owner / authority_source / authority_state / native_format / editable_state / semantic_layers / provenance_state / dependencies / hashes_or_commit / runtime / renderer / permission / current_state / does_not_prove`.

Material derivatives receive a new artifact ID.

## 8｜TOOL adapter section

Only when a TOOL is actually used, record:

`adapter_id / canonical_tool_id / implemented_revision / implementation_commit / operator_role / minimum_sufficient_operator_set / effect_budget / fallback / regression_baseline`.

An active Tool Deny is checked before adapter selection.

## 9｜Real execution

Record actual runtime/tool action, result, failures, repairs and re-execution state.

Do not infer EXECUTED from a promise, plan, prompt, path, PR or CI state.

## 10｜Actual readback

Record actual target/runtime, observed result, blockers, warnings and verdict.

`Artifact existence ≠ actual readback`.

## 11｜Four-layer regression

Record each applicable layer independently:

- `STRUCTURAL`
- `SEMANTIC`
- `VISUAL_ROI`
- `RUNTIME`

Each uses `PASS / FAIL / HOLD / NOT_APPLICABLE`.

Regression PASS does not grant Design KEEP and does not independently close the flow.

## 12｜Independent review

Record:

`producer_id / reviewer_id / review_input_artifact_id / review_input_hash_or_commit / reviewer_independence_state / evidence_gate / design_quality_gate / promotion_authority`.

Producer self-check is not an independent verdict.

## 13｜Notion ↔ GitHub drift

Required when a Current cross-platform pointer or implementation changes.

Use `GITHUB_STATIC_CHECK` or `LIVE_CROSS_PLATFORM_CHECK`.

A repository-only check cannot report live Notion `CURRENT`.

## 14｜Closure

Record:

`material_delta / branch / commits / pull_request / ci_state / merge_commit / main_readback / notion_writeback / remaining_blockers / final_state`.

Closure is allowed only after the Flow Completion Gate passes.

## 15｜Does not prove

A complete receipt does not prove Project State, Design PASS, field/engineering truth, user validation, rights clearance or promotion unless the appropriate independent authority separately establishes it.
