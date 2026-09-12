# OLEANDER Execution Receipt v1.0

Status: **ACTIVE CURRENT**  
Policy revision: **1.2**
Decision date: **2026-08-18**  
Current extensions: **2026-08-19 — Existing Visual Authority + Image Consumption; 2026-09-09 — Continuation Resume Checkpoint / Frontier / Concurrency / Adapter Route / Auto-Advance; 2026-09-12 — Shared Skill Execution Feedback + Git Branch Ref Disposition at Closure**
Scope: **one material execution unit**

## 0｜Purpose

Use one receipt to record the execution instance of the Current resolver/contracts. The receipt is not a new Project State, review framework or Skill.

Policy revision 1.1 requires two mandatory runtime sections for all new receipts:

1. **Constraint Lock**
2. **Flow Completion**

Current visual extension additionally requires **Image Consumption** whenever the execution binds semantic content imagery.

The 2026-09-09 runtime extensions additionally support:

- **Continuation Resume Checkpoint** when the same material task continues across chat turns, context compression, handoffs or other execution interruptions;
- **Cross-Context Frontier Discovery** when a continuation must recover the active frontier from existing state because the current Chat does not carry a reliable local task pointer;
- **Concurrency Guard** when a resumable checkpoint is about to drive Remote/Authority/Release mutation;
- **Adapter Route Decision** when a material execution evaluates multiple surfaces or uses a currently exposed ephemeral connector;
- **Remote Mutation Idempotency** when a remote write outcome is uncertain or retry is considered;
- **Continuous Execution** when multiple ready nodes execute in one material run or auto-advance stops before Flow Completion.

The 2026-09-12 extension additionally supports **Skill Feedback** only when real execution plus Actual Readback produces material reusable learning. No material Skill delta means the section is omitted and no Skill mutation is created.

The same 2026-09-12 runtime also supports **Branch Ref Disposition** at actual closure when a material execution used a Git work branch/PR: merged refs are deleted only after ref→SHA provenance capture and dependency checks; open PR heads/bases, active worktrees and explicit keep refs remain protected, and unmerged refs are never deleted by age alone.

These are conditional runtime sections inside the existing Receipt. They do not create a new Project State, METHOD, Skill, framework, Agent taxonomy, plugin database, state database, checkpoint database or lock service.

The three pre-policy receipts explicitly allowlisted in the machine contract remain immutable provenance; all future receipts use only the sections applicable to the material execution. New fields are prospective and conditional.

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

## 3A｜Continuation Resume Checkpoint｜when applicable

Use this section when the same `task_id` / logical object is still active and execution is expected to continue across turns, handoffs or interruption while Receipt status remains `WORKING` or `HOLD`.

Record:

- `checkpoint_state = RESUMABLE / REVALIDATE / BLOCKED / CLOSED`
- `current_node`
- `last_verified_artifact`
- `resume_from`
- `next_allowed_action`
- `authority_fingerprint`
- `stale_reasons`
- `checkpoint_sequence`
- `checkpoint_updated_at`
- `expected_checkpoint_sequence`
- `executor_id`
- `execution_lease_state = NONE / ACTIVE / STALE / CONFLICTED`
- `lease_acquired_at`

`last_verified_artifact` records at minimum:

`artifact_id / hash_or_commit / readback_verdict`.

The `authority_fingerprint` is a deterministic digest or stable composite over the applicable Current state:

`CURRENT_ROOT_VERSION / PROJECT_OR_SCOPE_AUTHORITY / SOURCE_AUTHORITY / DESIGN_AUTHORITY / CURRENT_TASK_ID / CURRENT_NATIVE_MASTER_OR_REF / ACTIVE_CONSTRAINT_LOCK`.

### Cross-context frontier discovery

When a new Chat or compressed context does not carry a reliable local task pointer, recover the existing frontier from:

1. project/task/object keys explicitly present in the current request;
2. Current Project State or Current Task pointer;
3. Current Project Control Card;
4. active `WORKING / HOLD` Execution Receipts.

Match on stable keys when available:

`PROJECT_ID_OR_SCOPE_ID / TASK_ID / LOGICAL_OBJECT_OR_CANONICAL_IDS / CURRENT_NATIVE_MASTER_OR_REF / AUTHORITY_FINGERPRINT`.

Do not use title similarity, chat history or a summary as checkpoint authority.

When frontier discovery is materially used, record:

`discovery_trigger / project_or_scope_key / task_key / object_or_canonical_ids / candidate_frontiers / selected_frontier / selection_basis / ambiguity_state`.

If several checkpoints represent the same task/object under matching Current Authority, select the highest `checkpoint_sequence`, then the latest `checkpoint_updated_at`. Older checkpoints remain provenance.

If multiple **distinct** active frontiers remain and Current Authority cannot identify one active task, use `HOLD_AMBIGUOUS_FRONTIER` instead of guessing or merging states.

### Direct resume

A generic same-task follow-up such as “继续 / 推进 / 优化 / 修一下” resumes `next_allowed_action` instead of re-planning from zero only when all are true:

- same task and same logical object;
- authority fingerprint still matches Current;
- the recorded last artifact has actual readback evidence;
- no dependency/handoff is stale or marked for re-test;
- checkpoint state is `RESUMABLE`.

Already verified completed nodes are not replayed merely because the conversation changed or context was compressed.

### Revalidation

Set `checkpoint_state=REVALIDATE` and re-read Current Authority before mutation when any of the following is true:

- project or task switched;
- authority fingerprint changed;
- Source Authority or Design Authority changed;
- Current native master / canonical write frontier changed externally;
- a consumed dependency became stale or requires re-test;
- the checkpoint is missing, corrupt, or its last artifact was never actually read back;
- another executor advanced the checkpoint sequence.

A chat switch, model context compression or reopening the same conversation is **not by itself** an authority change.

### BLOCKED behavior

A `BLOCKED` checkpoint does not authorize blind retry. Re-check only the declared release condition when it is actually checkable. Without new evidence or released capability, do not repeat the same failed mutation, spin another retry loop, or create a side page merely to re-register the same blocker.

### CLOSED behavior

A generic “继续” does not silently reopen a `CLOSED` execution unit. Reopening requires a new explicit scope, an explicit reopen decision, or a new material task bound to the existing project/object identity.

### Persistence boundary

Checkpointing reuses the existing Receipt / Control Card state. It must not create a new Receipt or Project State solely because another chat turn occurred.

Write/update a continuation checkpoint only through an existing persistence trigger after one of:

- actual readback following material execution;
- a genuine HOLD reached after the legal repair path was attempted;
- a typed handoff becoming ready/accepted.

`NO MATERIAL DELTA = NO NEW RECEIPT JUST FOR CHECKPOINTING`.

## 3B｜Concurrency Guard｜when applicable

Use before `REMOTE_MUTATION / AUTHORITY_MUTATION / RELEASE_MUTATION` when execution is driven by a resumable checkpoint.

Record:

`expected_checkpoint_sequence / observed_checkpoint_sequence / executor_id / execution_lease_state / lease_acquired_at / guard_verdict`.

The concurrency truth is the checkpoint sequence, not the lease metadata.

Canonical guard:

`READ EXPECTED SEQUENCE → RE-READ CURRENT CARRIER BEFORE MUTATION → OBSERVED == EXPECTED = PASS_SEQUENCE_MATCH → OBSERVED != EXPECTED = REVALIDATE_CONCURRENT_ADVANCE / BLOCK MUTATION`.

A stale `ACTIVE` lease cannot override a newer sequence. `executor_id` and lease fields are runtime diagnostics only and grant no mutation authority. No global lock service or lock database is introduced.

## 3C｜Continuous Execution｜when applicable

Use this section when more than one ready node is executed in one material run, or when auto-advance stops before Flow Completion.

Record:

- `auto_advance_enabled`
- `nodes_executed_in_order`
- `node_readback_verdicts`
- `stop_reason`
- `final_current_node`
- `next_allowed_action`

Dependent mutations require Actual Readback between nodes. A successful tool call alone is not enough to advance a dependent write frontier.

Do not stop after one node solely because a tool call returned. Continue while the next node is ready, Authority/constraints remain valid, the expected checkpoint sequence is still current, the side-effect class stays within the existing authorized ceiling and no real stop condition is active.

Allowed stop reasons include:

`FLOW_COMPLETION_GATE_PASS / GENUINE_BLOCKER / AUTHORITY_CONFLICT_OR_AMBIGUOUS_FRONTIER / CONCURRENT_CHECKPOINT_ADVANCE / USER_DESIGN_OR_SCOPE_DECISION_REQUIRED / SIDE_EFFECT_ESCALATION_NOT_AUTHORIZED / MISSING_UNRECOVERABLE_SOURCE / FUTURE_CONDITION_OR_EXTERNAL_WAIT_REQUIRED / REQUIRED_INDEPENDENT_REVIEW_UNAVAILABLE / TOOL_OR_RUNTIME_HARD_LIMIT`.

Continuous execution is current-turn orchestration. It is not background execution and does not justify promising future work after the turn ends.

`NO MATERIAL DELTA = NO NEW RECEIPT JUST TO RECORD AUTO-ADVANCE`.

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
4. `EXISTING_VISUAL_AUTHORITY_AND_IMAGE_CONSUMPTION_CHECK` — required when semantic content imagery is bound
5. `REQUIRED_NATIVE_OUTPUT_DEFINITION`
6. `CAPABILITY_AND_MINIMUM_OWNER_SET`
7. `REAL_EXECUTION`
8. `NATIVE_ARTIFACT_AND_TYPED_HANDOFF_RECORD`
9. `ACTUAL_READBACK`
10. `REGRESSION_AS_APPLICABLE`
11. `INDEPENDENT_REVIEW_AS_APPLICABLE`
12. `SYNC_RECEIPT_AND_DRIFT_AS_APPLICABLE`

For full-flow work, Authority, Constraint Resolution, Existing Knowledge/Skill Resolution, Native Output, Minimum Owner Set, Real Execution and Actual Readback cannot be skipped. The Existing Visual/Image Consumption phase is additionally mandatory when semantic content imagery is involved.

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

Material derivatives receive a new artifact ID. A new artifact ID does **not** automatically create a new semantic-image identity.

## 7A｜Image Consumption｜when applicable

Required whenever a visual execution binds a semantic content image. Record:

- `register_path_or_authority`
- `lookup_performed`
- `reservations_or_consumptions`
- `conflicts`
- `blocked_assets`
- `release_actions`
- `verdict`

The authoritative semantics are in `OLEANDER_IMAGE_CONSUMPTION_REGISTER_v1.0.md/.json`.

Rules:

- lookup and reservation happen **before** image binding / layout production;
- one `semantic_image_id` may belong to one independent consumer unit only;
- `RESERVED / CONSUMED / LEGACY_MULTI_CONSUMED / REJECTED_NOT_ELIGIBLE` blocks another consumer;
- crop / recolor / mask / screenshot / contour / other presentation derivatives inherit the same semantic identity;
- only explicitly classified `SYSTEM_REUSABLE` assets may repeat;
- `NOT_APPLICABLE` is allowed only when no content imagery is used or the run uses `SYSTEM_REUSABLE` assets only, with the reason recorded;
- a conflict verdict is `BLOCK / SELECT ANOTHER IMAGE`, not “make another crop.”

## 8｜TOOL adapter section

Only when a TOOL is actually used, record:

`adapter_id / canonical_tool_id / implemented_revision / implementation_commit / operator_role / minimum_sufficient_operator_set / effect_budget / fallback / regression_baseline`.

An active Tool Deny is checked before adapter selection.

## 8A｜Adapter Route Decision｜when applicable

Use this section only when a **material execution** evaluates multiple candidate surfaces or uses a currently exposed ephemeral connected surface.

Record:

`required_capability_roles / candidate_surfaces / selected_surface / selection_reasons / availability_state / authority_ceiling / side_effect_class / readback_surface / fallback_surface`.

The selection reason must be capability/authority/readback based, not “because vendor X is available.”

Unused candidates and liveness probes remain ephemeral. The selected surface does not gain Project/Source/Design Authority. If the same surface must mutate and read back because no alternative exists, declare the readback `NOT_INDEPENDENT`.

`NO MATERIAL DELTA = NO NEW RECEIPT JUST TO RECORD ROUTING`.

## 8B｜Remote Mutation Idempotency｜when applicable

Use when a Remote/Authority/Release mutation returns `UNCERTAIN`, or a retry is being considered.

Record:

`operation_fingerprint / expected_postcondition / outcome_state / verification_surface / retry_decision`.

`outcome_state = CONFIRMED_SUCCESS / CONFIRMED_FAILURE / UNCERTAIN`.

Canonical rule:

`UNCERTAIN → VERIFY POSTCONDITION BEFORE RETRY`.

If the expected postcondition is found, normalize to `CONFIRMED_SUCCESS` and do not retry. If absence is proven, retry only when the operation is idempotent or provider-keyed and the bounded retry budget remains. Otherwise HOLD rather than risk a duplicate side effect.

Timeout or connector ambiguity is never sufficient evidence to replay a create-like mutation.

`NO MATERIAL DELTA = NO NEW RECEIPT JUST TO RECORD IDEMPOTENCY PROBES`.

## 9｜Real execution

Record actual runtime/tool action, result, failures, repairs and re-execution state.

Do not infer EXECUTED from a promise, plan, prompt, path, PR or CI state.

## 10｜Actual readback

Record actual target/runtime, observed result, blockers, warnings and verdict.

`Artifact existence ≠ actual readback`.

For a continuing task, a successful readback is the preferred checkpoint boundary. Record the verified artifact identity before advancing `next_allowed_action`.

For continuous execution, readback is also the dependency boundary between successive material mutations.

For uncertain remote outcomes, readback is additionally the verification boundary that decides whether a retry is legal. For cross-system state changes, it is part of reconciliation evidence.

## 10A｜Skill Feedback｜when applicable

Use only when real execution plus Actual Readback establishes a material reusable Skill/Practice/regression delta. The authoritative shared policy is `OLEANDER_SKILL_EXECUTION_FEEDBACK_SUPPLEMENT_v0.1.md/.json`.

Record:

`skill_id / skill_version_or_commit / usage_provenance_state / rule_or_capability_used / artifact_refs / actual_readback / outcome / gap_route / failure_class / root_cause / repair_retest_or_hold / transfer_rule_candidate / transfer_boundary / feedback_action / cross_context_status / regression_case_required / skill_change_ref / promotion_boundary`.

Usage provenance states:

- `PROJECT_USAGE_EVIDENCE` — only with direct pre-execution/in-action exact Skill/version/extension evidence that materially influenced the action;
- `PROJECT_LEARNING_EVIDENCE_SKILL_FEEDBACK_ORPHAN` — project learning is real but historical Skill-use provenance is not established.

Allowed feedback actions remain:

`NONE_PROJECT_SPECIFIC / UPDATE_EXISTING_PRACTICE / UPDATE_EXISTING_SKILL / ADD_REGRESSION_RULE / CROSS_CONTEXT_TEST_NEEDED`.

Failure-derived Skill changes require root cause and repair/retest, or a legitimate bounded HOLD. Post-hoc artifact/diff/commit/readback cannot be used to manufacture historical Skill usage.

`NO MATERIAL SKILL DELTA = OMIT skill_feedback + NO SKILL MUTATION`.

The section never changes installation/lifecycle state and never self-promotes a Skill.

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

A route to a different technical surface is not automatically an independent design review. Independence remains governed by the existing reviewer identity contract.

## 13｜Notion ↔ GitHub drift

Required when a Current cross-platform pointer or implementation changes.

Use `GITHUB_STATIC_CHECK` or `LIVE_CROSS_PLATFORM_CHECK`.

A repository-only check cannot report live Notion `CURRENT`.

A chat/session boundary, frontier discovery, liveness probe, idempotency verification or no-delta route decision does not by itself create a Current pointer mutation.

## 14｜Closure

Record:

`material_delta / branch / commits / pull_request / ci_state / merge_commit / main_readback / notion_writeback / remaining_blockers / final_state`.

For material executions that use a Git work branch or pull request and reach closure, new receipts also record `branch_ref_disposition` prospectively:

`branch / disposition / reason / dependency_checks / audit_receipt / readback`.

After merge, the default is `DELETE_AFTER_MERGE` once ref→SHA provenance has been captured and the branch is not an open PR head, open PR base, active worktree, or explicit retained provenance/stack ref. An unmerged branch may not be deleted by age alone. Historical receipts are immutable and are not backfilled merely to satisfy this extension.

Closure is allowed only after the Flow Completion Gate passes.

A `CLOSED` checkpoint is a runtime consequence of valid closure; it does not itself prove closure.

## 15｜Does not prove

A complete receipt, valid continuation checkpoint, concurrency guard, idempotency decision, discovered frontier, adapter route decision, continuous-execution record or Skill-feedback section does not prove Project State, Design PASS, field/engineering truth, user validation, rights clearance, historical Skill usage without execution-time provenance, universal transfer or promotion unless the appropriate independent authority separately establishes it.
