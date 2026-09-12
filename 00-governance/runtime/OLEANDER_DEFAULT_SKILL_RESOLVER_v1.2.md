# OLEANDER Default Skill Resolver v1.2

Status: **ACTIVE CURRENT**  
Implementation revision: **1.2.5**  
Decision date: **2026-08-19**  
Runtime extension: **2026-09-09 — Cross-Context Frontier Recovery / Executable Frontier Resolution / Capability-Role Routing / Optimistic Checkpoint Concurrency / Verify-Before-Retry / Continuous Auto-Advance**  
Scope: **ALL OLEANDER projects / conversations / agents / media**  
Notion Current Authority: **OLEANDER｜设计知识库（Design） v1.1.1**  
Execution implementation: **GitHub `Jiaosong/Design`**

## 0｜Purpose

v1.2.5 keeps the existing knowledge-first execution architecture and extends the v1.2.4 Chat-first continuation baseline without adding a new state system, lock service or Agent framework:

1. **Sticky Execution Constraint Lock** — explicit negative user constraints are resolved before owner/tool selection and remain active until explicitly revoked.
2. **Flow Completion Gate** — a task that requires the full OLEANDER flow cannot be called complete until every applicable phase is actually closed.
3. **Existing Visual Authority + Image Consumption Gate** — visual work must first preserve mature/current design artifacts and must check whether a semantic content image has already been reserved or consumed before binding it to another surface.
4. **Verified Continuation / Resume Checkpoint** — a same-task follow-up such as “继续 / 推进 / 优化 / 修一下” resumes from the last verified checkpoint instead of re-planning from zero, but only while Current Authority and the execution frontier remain valid.
5. **Cross-Context Frontier Discovery** — when a new Chat or compressed context does not carry a reliable local task pointer, recover the active execution frontier from existing Project State / Control Card / active Receipt using stable project/object/authority keys rather than chat memory.
6. **Executable Frontier Resolution** — the Current validator contains a deterministic pure resolver that filters existing `WORKING/HOLD` candidates, matches stable keys, detects ambiguity/Authority drift, and selects the highest valid checkpoint sequence.
7. **Optimistic Checkpoint Concurrency** — before remote/authority/release mutation, re-read the checkpoint carrier and require `observed_checkpoint_sequence == expected_checkpoint_sequence`; sequence mismatch blocks stale execution and forces `REVALIDATE_CONCURRENT_ADVANCE`.
8. **Verify-Before-Retry** — uncertain remote mutation outcomes are read back against an expected postcondition before retry. Duplicate create-like side effects are forbidden.
9. **Continuous Ready-Node Auto-Advance** — after a node is actually executed and read back, continue through further ready nodes in the current execution turn while authority, constraints, checkpoint sequence, side-effect ceiling and stop conditions remain valid; do not stop after one node without a real reason.
10. **Capability-Role Adapter Routing** — TOOL/plugin/connector selection follows the existing Tool Adapter Contract by capability role, required native output, authority, side-effect class, readback coverage and current verified availability, not by vendor name.

This is not a new Skill, METHOD, taxonomy, Agent framework, state database, checkpoint database, lock database or parallel process. It hardens the existing Resolver / Project Control Card / Receipt / DAG / Tool Adapter / CI chain.

Current invariant:

> **CURRENT ROOT → CURRENT TASK / SOURCE AUTHORITY → FRONTIER DISCOVERY WHEN LOCAL POINTER IS MISSING → CONTINUATION CHECKPOINT / AUTHORITY REVALIDATION WHEN APPLICABLE → STICKY CONSTRAINT LOCK → LIVE REGISTRY / CURRENT KNOWLEDGE → EXISTING METHOD + SKILL READBACK → EXISTING MATURE DESIGN / CURRENT VISUAL AUTHORITY → IMAGE CONSUMPTION LOOKUP → REQUIRED NATIVE OUTPUT → MINIMUM SUFFICIENT OWNER SET / DAG → CAPABILITY-ROLE TOOL ADAPTER ROUTING → CHECKPOINT-SEQUENCE GUARD BEFORE MUTATION → VERIFY UNCERTAIN REMOTE POSTCONDITION BEFORE RETRY → REAL EXECUTION → NATIVE ARTIFACT / HANDOFF → REGRESSION → ACTUAL READBACK → CHECKPOINT UPDATE WHEN APPLICABLE → AUTO-ADVANCE NEXT READY NODE WHILE ALLOWED → EVIDENCE + INDEPENDENT DESIGN REVIEW → FLOW COMPLETION GATE → EXECUTION RECEIPT → DRIFT / SYNC AS APPLICABLE**

## 1｜Notion current architecture remains upstream

Before historical navigation, method indexes or Skill files, read the Current Root Authority, live Registry and applicable Project State / Source Authority / Current Task.

Notion owns Current knowledge identity, Canonical ID, Domain, L0–L7, hierarchy, dedicated relations and project identity. GitHub owns executable Skill/runtime implementation. Old `00–70` navigation remains provenance/discovery only.

## 2｜Sticky Execution Constraint Lock

Before selecting any execution owner, runtime, TOOL adapter or generation capability, resolve explicit constraints from:

1. latest explicit user instruction;
2. Current Task explicit constraints;
3. active Execution Receipt for the same task;
4. Current Project Authority / recorded user decisions.

Normalize applicable constraints into one of:

- `TOOL_DENY`
- `OUTPUT_DENY`
- `CREATION_DENY`
- `OWNER_REQUIRE`
- `PROCESS_REQUIRE`
- `REVIEW_REQUIRE`

Current normalized rules include:

- `NO_IMAGE_GENERATION`
- `NO_NEW_SKILL`
- `NO_NEW_METHOD`
- `NO_NEW_FRAMEWORK`
- `USE_EXISTING_OLEANDER_METHODS_AND_SKILLS`
- `FULL_OLEANDER_FLOW_REQUIRED`
- `NO_PRODUCER_SELF_PROMOTION`

### Sticky means sticky

An active constraint survives ordinary follow-ups such as:

- “继续”
- “优化”
- “再做一下”
- “修一下”
- “按 OLEANDER 做”

These phrases do **not** revoke a prohibition.

A constraint can be released only by a later explicit instruction that directly changes that named constraint, for example “现在可以生图” releases `NO_IMAGE_GENERATION` only; it does not release `NO_NEW_SKILL` or `FULL_OLEANDER_FLOW_REQUIRED`.

### Hard effects

`NO_IMAGE_GENERATION` means:

- do not call an image-generation tool;
- do not route through a generative-image adapter;
- use existing source imagery, native vector, HTML/CSS/SVG, 3D, CAD, layout or other non-generative production when suitable;
- if the requested native output truly cannot be produced without generation, return **HOLD** rather than silently generate.

`NO_NEW_SKILL / NO_NEW_METHOD / NO_NEW_FRAMEWORK` means:

- do not create a sidecar Skill, METHOD, router, framework or parallel schema simply because a gap appears;
- compose existing owners, use a bounded fallback, record the gap, or HOLD;
- creation becomes eligible only after the user explicitly releases the creation deny and the existing-first gap diagnosis independently supports it.

`USE_EXISTING_OLEANDER_METHODS_AND_SKILLS` means the relevant Current METHOD / Skill / `CAPABILITY.json` / runtime material must actually be read. Saying “我会用 OLEANDER” is not execution evidence.

## 2A｜Verified Continuation / Resume Checkpoint

A generic follow-up that does not materially redefine the task, object, constraints or requested output is interpreted as **same-task continuation**, not a request to restart planning.

Continuation intents include:

- “继续”
- “推进”
- “优化”
- “再修” / “修一下”
- equivalent same-object follow-ups that preserve task identity.

Resolve an existing continuation state in this order:

1. active Execution Receipt for the same task;
2. Current Project Control Card;
3. Current Task / Project State only when no stronger runtime checkpoint exists.

The checkpoint records only runtime continuity:

`checkpoint_state / current_node / last_verified_artifact / resume_from / next_allowed_action / authority_fingerprint / stale_reasons / checkpoint_sequence / checkpoint_updated_at / expected_checkpoint_sequence / executor_id / execution_lease_state / lease_acquired_at`.

It does **not** create another Project State or another owner taxonomy.

### Cross-context frontier discovery

When a new Chat, context compression or other conversation boundary does not carry a reliable local `task_id`, do not use chat history or a summary as execution authority. Discover the existing frontier in this order:

1. stable project / task / object keys explicitly present in the current request;
2. Current Project State or Current Task pointer;
3. Current Project Control Card;
4. active `WORKING / HOLD` Execution Receipts.

Match with stable keys when available:

`PROJECT_ID_OR_SCOPE_ID / TASK_ID / LOGICAL_OBJECT_OR_CANONICAL_IDS / CURRENT_NATIVE_MASTER_OR_REF / AUTHORITY_FINGERPRINT`.

Title similarity or a chat summary alone is insufficient.

If multiple checkpoints belong to the same task/object and match Current Authority, use the highest `checkpoint_sequence`, then the latest `checkpoint_updated_at`; older checkpoints remain provenance.

If multiple **distinct** active frontiers remain and Current Authority does not identify one active task, return `HOLD_AMBIGUOUS_FRONTIER` instead of guessing, merging projects, or creating another Current.

### Executable frontier resolver

The Current runtime validator contains `resolve_continuation_frontier(...)` as a side-effect-free deterministic function. It must:

- filter to existing active `WORKING/HOLD` frontier records;
- match exact stable project/task/object/native-ref keys when supplied;
- prefer Authority-fingerprint matches;
- return `REVALIDATE_AUTHORITY_BEFORE_MUTATION` when no candidate matches Current Authority;
- detect multiple distinct unresolved tasks and return `HOLD_AMBIGUOUS_FRONTIER`;
- choose the highest checkpoint sequence, then latest checkpoint time, among legal same-task matches.

Regression must invoke this function against machine cases. Presence of policy strings alone is not sufficient proof.

### Chat / Chat On Steroids entry enforcement

Conversation surfaces do not receive a second executor or a second state owner. The stateless adapter
`00-governance/runtime/oleander_chat_resolver_adapter.py` composes the existing executable Resolver functions over caller-supplied Current evidence and returns a transient `conversation_directive`.

For OLEANDER-scoped continuation, mutation, auto-advance or completion decisions, Chat/CoS must consume that machine result before relying on transcript inference. The adapter has `EXECUTION_ADAPTER_ONLY` authority ceiling, persists no state, and cannot replace Project State, the Project Control Plane, Execution Receipts or the Flow Completion Gate.

The machine binding must preserve these boundaries:

- `summary / handoff / assistant claim != checkpoint authority`;
- generic continue resumes the verified `next_allowed_action` rather than replanning;
- raw Execution Receipt checkpoint fields are consumed directly, without an adapter-side shadow checkpoint schema;
- `CLOSED` never reopens from generic continuation;
- sticky constraints resolve before tool or creation routing;
- checkpoint sequence mismatch blocks mutation;
- legal ready nodes auto-advance until an existing stop condition;
- only Flow Completion Gate `PASS` permits a complete/stop claim.

`00-governance/runtime/bind_chat_on_steroids_oleander.py` is an idempotent machine-local settings binder for the existing CoS `mcp.instructions` and Goal/Objective/Loop prompt extension surfaces. It appends a marked binding block, preserves the user's existing prompt text, Goal enabled state and Goal mode, and enables the existing `goal.includeToolCalls` option so Goal/Loop can consume the resolver CLI's recorded tool readback instead of relying on an assistant paraphrase. It is not a runtime authority carrier. Direct config persistence does not claim hot reload of an already-running CoS process.

### Authority fingerprint

Direct resume requires a stable fingerprint of the applicable Current execution frontier. Inputs are:

`CURRENT_ROOT_VERSION / PROJECT_OR_SCOPE_AUTHORITY / SOURCE_AUTHORITY / DESIGN_AUTHORITY / CURRENT_TASK_ID / CURRENT_NATIVE_MASTER_OR_REF / ACTIVE_CONSTRAINT_LOCK`.

A matching fingerprint means only that the recorded execution frontier is still eligible for resume. It does not prove the artifact is correct or complete.

### Direct resume rule

Resume from `next_allowed_action` without replaying already verified completed nodes only when all are true:

- same `task_id` and same logical object;
- authority fingerprint matches Current;
- `last_verified_artifact` has real Actual Readback evidence;
- no dependency/handoff is stale or marked `RETEST_REQUIRED / REGEN_REQUIRED / HOLD`;
- `checkpoint_state=RESUMABLE`.

Canonical behavior:

`DISCOVER / RESTORE VERIFIED CHECKPOINT → CONFIRM CURRENT AUTHORITY FINGERPRINT → RESTORE ACTIVE CONSTRAINTS → SKIP VERIFIED COMPLETED NODES → GUARD EXPECTED CHECKPOINT SEQUENCE → EXECUTE NEXT ALLOWED ACTION → READBACK → UPDATE EXISTING CHECKPOINT`.

Do not regenerate a plan merely because the conversation changed, context was compressed, or a new Chat surface is being used.

### Mandatory revalidation

Do **not** direct-resume from the checkpoint when any of the following is true:

- project or task changed;
- authority fingerprint no longer matches;
- Source Authority or Design Authority changed;
- Current native master / canonical write frontier moved externally;
- a consumed dependency became stale or requires regeneration/re-test;
- the checkpoint is missing/corrupt;
- the last artifact was never actually opened/rendered/run and read back;
- another executor advanced the checkpoint sequence.

In those cases set runtime state to `REVALIDATE`, refresh the applicable Current Authority, then either repair the checkpoint or re-route from the first invalid node. Do not throw away valid upstream work.

### BLOCKED behavior

If the checkpoint is `BLOCKED`, generic continuation does not mean blindly repeat the failed mutation. Re-check only the declared release condition if it is currently observable or actionable.

No new evidence / no released capability / no changed authority → keep the same bounded blocker. Do not create another side page, retry loop, new Skill, new framework or duplicate Receipt merely to restate the blocker.

### CLOSED behavior

A generic “继续” does not reopen a `CLOSED` task. Reopen only through an explicit scope change, explicit reopen decision or a new material task that reuses the existing project/object identity.

### Context switch is not authority change

A different conversation, context compression or ordinary summarization is not by itself grounds to invalidate a checkpoint. The checkpoint is invalidated by **execution/authority drift**, not by conversation packaging.

### Persistence throttle

Reuse existing Control Card fields already present where applicable:

- `run_id`
- `execution_integrity.readback`
- `execution_integrity.baseline.rollback_ref`
- `next_allowed_action`
- `task_id`
- `current_node`
- `last_verified_artifact`
- `resume_from`
- `authority_fingerprint`
- `checkpoint_sequence`
- `expected_checkpoint_sequence`
- `executor_id`
- `execution_lease_state`
- `lease_acquired_at`
- `checkpoint_updated_at`

Do not duplicate them into a second state object.

Write/update a continuation checkpoint only after:

- actual readback of a material execution result;
- a genuine HOLD after a legal repair attempt reaches its real boundary;
- a typed handoff becomes ready/accepted.

**NO MATERIAL DELTA = NO NEW RECEIPT / PROJECT STATE JUST FOR ANOTHER CHAT TURN.**

## 2B｜Optimistic checkpoint concurrency

Concurrent Chat / Automation / Work / runtime executors must not rely on last-writer-wins.

Before `REMOTE_MUTATION / AUTHORITY_MUTATION / RELEASE_MUTATION` and before persisting an advanced checkpoint:

`READ EXPECTED CHECKPOINT SEQUENCE → RE-READ CURRENT CARRIER → OBSERVED == EXPECTED ? PROCEED : BLOCK + REVALIDATE_CONCURRENT_ADVANCE`.

Runtime fields:

`expected_checkpoint_sequence / executor_id / execution_lease_state / lease_acquired_at`.

Lease states are `NONE / ACTIVE / STALE / CONFLICTED`, but lease metadata is advisory only. The checkpoint sequence is the concurrency truth. A stale `ACTIVE` lease cannot override a newer checkpoint sequence. Lease metadata grants no mutation Authority.

After material execution + readback, a new persisted checkpoint must advance to a sequence greater than the prior sequence using the source adapter's native concurrency mechanism when available.

No global lock service, lock database or second Project State is introduced.

## 2C｜Continuous ready-node auto-advance

For `继续 / 推进 / 执行 / 修复 / 优化` and equivalent execution intents, do not stop after one successful node merely because one tool call or one sub-step completed.

After each material node:

`EXECUTE READY NODE → SELECTIVE READBACK → REPAIR + RETEST WHEN LEGAL AND NEEDED → UPDATE EXISTING CHECKPOINT WHEN TRIGGERED → RESOLVE NEXT READY NODE → CONTINUE WHILE ALLOWED`.

Advance to the next node only when:

- the previous node was actually executed;
- applicable Actual Readback passed or a typed handoff was accepted;
- the next node is ready under the existing DAG;
- the Authority fingerprint still matches;
- active constraints are unchanged or explicitly re-resolved;
- the next action stays within the already authorized side-effect ceiling;
- `expected_checkpoint_sequence` still matches the current carrier before mutation;
- no stop condition is active.

Stop only on a real boundary:

- Flow Completion Gate passed;
- genuine blocker;
- Authority conflict or ambiguous active frontier;
- concurrent checkpoint advance;
- user design/scope decision is genuinely required;
- irreversible or higher-side-effect action is not already authorized;
- unrecoverable source is missing;
- a future condition/external wait is required;
- required independent review is unavailable;
- actual tool/runtime hard limit.

A forced stop must report the exact `current_node`, `next_allowed_action` or blocker. It must not promise background work.

Continuous execution is **current-turn orchestration**, not background execution. It does not assume a generic child-agent spawn capability. Independent DAG nodes may be parallelized only when the execution surface safely supports it; otherwise serialize them.

## 3｜Execution contract layer

The Current execution contract layer remains:

- `OLEANDER_SKILL_CAPABILITY_CONTRACT_v0.1`
- `OLEANDER_MULTI_SKILL_EXECUTION_DAG_CONTRACT_v0.1`
- `OLEANDER_TOOL_ADAPTER_CONTRACT_v0.1`
- `OLEANDER_NATIVE_ARTIFACT_CONTRACT_v0.1`
- `OLEANDER_EXECUTION_REGRESSION_CONTRACT_v0.1`
- `OLEANDER_NOTION_GITHUB_DRIFT_CHECK_v0.1`
- `OLEANDER_EXECUTION_RECEIPT_v1.0`
- `OLEANDER_IMAGE_CONSUMPTION_REGISTER_v1.0` — allocation/register extension for semantic content images.

The constraint lock precedes tool/owner mutation. Continuation checkpoint resolution may restore the same task state before that lock is re-resolved, but it cannot override a newer explicit user constraint or newer Current Authority.

### Capability-role TOOL/plugin routing

When more than one connector/runtime/plugin can perform a task, route through the existing `OLEANDER_TOOL_ADAPTER_CONTRACT_v0.1` instead of building vendor-specific project logic.

Selection precedence is:

`CURRENT AUTHORITY + OWNER BOUNDARY → REQUIRED NATIVE OUTPUT + MUTATION CAPABILITY → ACTIVE CONSTRAINTS + PERMISSION → LOWEST SUFFICIENT SIDE EFFECT → ACTUAL READBACK COVERAGE → CURRENT VERIFIED AVAILABILITY / RELIABILITY → LOWER EXECUTION OVERHEAD → DECLARED FALLBACK`.

Only probe the selected surface or a needed fallback. Do not inventory-probe every connected plugin. A currently exposed connector may be used ephemerally when its capability role and authority boundary fit the task, but one-off use does not create a new registry entry, TOOL, Skill, Method, Framework or Project State.

Prefer a distinct readback surface when practical. If the same surface must both mutate and read back because no alternative exists, declare the evidence `NOT_INDEPENDENT`; do not silently upgrade it to independent review.

Heavy executors remain `ESCALATION_ONLY`. If a lighter current connector can perform the required mutation with adequate readback, do not escalate merely because a heavier executor is available.

### Verify-before-retry

For remote/authority/release writes, define/use the Tool Adapter Contract's operation fingerprint and expected postcondition before create-like or otherwise nontrivial writes whenever practical.

`UNCERTAIN OUTCOME → VERIFY POSTCONDITION BEFORE RETRY`.

If the postcondition exists, normalize to confirmed success and do not retry. If absence is proven, retry only when the operation is idempotent or provider-keyed and bounded retry remains. Otherwise HOLD rather than risk duplicate PR/page/deployment/upload/message or other side effect.

A timeout or connector ambiguity is not evidence that the write failed and does not authorize replay.

## 4｜Minimum sufficient owner set

`NO COMPRESSION / NO LOSS` protects information. It does not require every Skill to run.

For each task, use the smallest owner set that can produce the required native output and applicable validation/review. Multi-owner work must use explicit DAG roles and typed handoffs.

**Full OLEANDER flow ≠ full Skill stack.**

## 5｜Flow Completion Gate

For OLEANDER production, mutation, training, state-changing review work, or any task explicitly marked `FULL_OLEANDER_FLOW_REQUIRED`, build an applicable-phase checklist before production.

Canonical phases:

1. `AUTHORITY_PREFLIGHT`
2. `STICKY_CONSTRAINT_RESOLUTION`
3. `EXISTING_KNOWLEDGE_METHOD_SKILL_RESOLUTION`
4. `EXISTING_VISUAL_AUTHORITY_AND_IMAGE_CONSUMPTION_CHECK` when visual content images are involved
5. `REQUIRED_NATIVE_OUTPUT_DEFINITION`
6. `CAPABILITY_AND_MINIMUM_OWNER_SET`
7. `REAL_EXECUTION`
8. `NATIVE_ARTIFACT_AND_TYPED_HANDOFF_RECORD`
9. `ACTUAL_READBACK`
10. `REGRESSION_AS_APPLICABLE`
11. `INDEPENDENT_REVIEW_AS_APPLICABLE`
12. `SYNC_RECEIPT_AND_DRIFT_AS_APPLICABLE`

For full-flow work, the following core phases cannot be skipped:

- Authority preflight
- Sticky constraint resolution
- Existing knowledge / METHOD / Skill resolution
- Existing visual authority + image-consumption check when visual content imagery is involved
- Required native output definition
- Capability + minimum owner set
- Real execution
- Actual readback

Other phases may be `NOT_APPLICABLE`, but only with a concrete reason.

### No early completion

The following are intermediate states only and cannot independently justify “完成 / CLOSED / 已闭环”:

- plan written;
- method explained;
- artifact created;
- file exported;
- PR opened;
- CI green;
- producer self-check passed;
- render passed;
- regression passed.

If any required applicable phase is missing, `FAIL` or `HOLD`, the task state is **HOLD / INCOMPLETE**, not complete.

## 6｜Default GPT / Agent behavior

1. Read Current Root Authority + applicable Project State / Source Authority / Current Task.
2. If the current context does not carry a reliable task pointer for a continuation intent, discover the active frontier from the existing Current Project/Task → Control Card → active Receipt chain using stable project/object/authority keys.
3. Run the executable frontier resolver; if multiple distinct active frontiers remain and Current Authority cannot identify one, return `HOLD_AMBIGUOUS_FRONTIER`; do not guess.
4. If the user intent is a same-task follow-up, resolve the latest valid continuation checkpoint.
5. If the checkpoint requires revalidation, refresh Current Authority before mutation; if it is valid, retain the verified completed-node frontier.
6. Resolve sticky execution constraints before any owner/tool selection; a checkpoint never overrides a newer explicit constraint.
7. Enforce tool/output/creation/process locks.
8. Resolve live Registry identity and Current knowledge context.
9. Retrieve relevant Current METHOD / THEORY / SOURCE / CASE / EVIDENCE / TOOL / PRACTICE.
10. Reuse mature design/current assets and actually read required existing Skill/capability material.
11. For visual work, identify the strongest current board / design object / native figure before designing the presentation carrier.
12. Before binding any semantic content image, query the project Image Consumption Ledger/Register by source hash / parent source / child figure / semantic identity.
13. If that `semantic_image_id` is already `RESERVED / CONSUMED / LEGACY_MULTI_CONSUMED / REJECTED_NOT_ELIGIBLE` for another consumer, stop and select another image; crop/recolor/mask/contour/screenshot derivatives do not reset identity.
14. Reserve an available image to the current consumer unit before layout production.
15. Define the required native output.
16. Build the applicable Flow Completion checklist.
17. Resolve Execution Owner Map and Skill Capability Contract.
18. Select the Minimum Sufficient Owner Set; build DAG only when necessary.
19. Resolve TOOL/plugin/runtime adapters through capability-role routing; probe only the selected/needed surfaces.
20. If resuming, skip already verified completed nodes and restore the first `next_allowed_action`; otherwise execute the normal first ready node.
21. Re-read the current checkpoint carrier and enforce `observed_checkpoint_sequence == expected_checkpoint_sequence` before Remote/Authority/Release mutation.
22. If a previous remote mutation outcome is uncertain, verify its expected postcondition before any retry.
23. Execute the real native/editable artifact.
24. Emit Native Artifact records / typed handoffs as applicable.
25. Run `STRUCTURAL / SEMANTIC / VISUAL_ROI / RUNTIME` regression as applicable.
26. Open/render/run the actual result and perform readback.
27. Update the existing continuation checkpoint when the conditional trigger is met; advance checkpoint sequence monotonically; do not create a no-delta receipt solely for chat continuity.
28. If another node is ready and no stop condition is active, continue execution in the same turn; do not stop merely because one node passed.
29. Run Evidence Gate and independent Professional Design Gate separately where applicable.
30. Verify the Flow Completion Gate.
31. Emit/update an Execution Receipt containing the active constraint lock, flow-completion state, continuation/frontier evidence when applicable, concurrency guard when applicable, material adapter route decision when applicable, remote-mutation idempotency evidence when applicable, continuous-execution evidence when applicable and image-consumption section when applicable.
32. Run Notion↔GitHub drift check where cross-platform pointers changed.
33. Only after failed execution/readback may reusable Skill gaps be diagnosed; active creation denies still take precedence.
34. Sync material delta and preserve provenance.

## 7｜Existing-first / Source Gravity / Visual Authority

Existing-first is not satisfied by merely locating an old asset and then re-authoring it into a new weaker carrier.

For visual production the default order is:

`CURRENT SOURCE / MATURE DESIGN / CURRENT BOARD OR NATIVE ARTIFACT → IMAGE CONSUMPTION CHECK → REUSE DIRECT WHEN AVAILABLE → PRESENTATION ADAPTATION → NEW VISUAL ONLY WHEN A REAL GAP REMAINS`.

Hard rules:

- `OBJECT INTEGRITY → FRAME / LAYOUT`.
- A page, board or screen adapts to the design object; the object is not cropped, simplified or re-authored merely to fill a predetermined ratio.
- If a mature current board/artifact already proves the required object, use its valid figure directly before inventing another Hero or explanatory substitute.
- If that valid figure has already been consumed by another independent consumer unit, it is unavailable; choose another unused mature figure or create a genuinely new evidence-bounded visual only when necessary and permitted.
- Presentation carrier authority never reverses into Source or Design Authority.

New Skill creation remains unauthorized by a new project, interesting case, new name, repeated local use, file existence, PR creation, CI success or a missing convenience helper.

If an active `NO_NEW_SKILL / NO_NEW_METHOD / NO_NEW_FRAMEWORK` constraint exists, new creation is blocked even if a gap is real. The correct output is existing-owner composition, fallback, or HOLD until the user explicitly changes the constraint.

`NO_DEDICATED_OWNER` remains a valid state and does not automatically authorize creation.

## 8｜Image Consumption / Uniqueness Gate

Current allocation rule:

`ONE SEMANTIC CONTENT IMAGE → ONE CONSUMER UNIT`.

States:

- `AVAILABLE`
- `RESERVED`
- `CONSUMED`
- `RELEASED`
- `REJECTED_NOT_ELIGIBLE`
- `LEGACY_MULTI_CONSUMED`

`RESERVED / CONSUMED / LEGACY_MULTI_CONSUMED / REJECTED_NOT_ELIGIBLE` block another independent consumer from using the image.

### Derivative laundering forbidden

Crop, resize, recolor, mask, opacity, blend, screenshot, frame extraction, monochrome conversion, contour trace, background removal, blur, texture, typographic overlay or Web derivative inherit the same `semantic_image_id`.

A multi-image board may register genuinely independent child figures only with `parent_source_id + figure/crop bounds + child hash + semantic role`. Fragmenting one subject view does not create new image identities.

### SYSTEM_REUSABLE exception

Only explicitly classified logo / wordmark / UI icon / operational state symbol / navigation-service symbol / brand base pattern / design token / non-content system motif may repeat. A chapter Hero, evidence photo, landscape image, rendering, product image or key-scene image cannot be reclassified to bypass uniqueness.

### Same-source paired view

Same-source paired views may share a source only inside one declared paired `consumer_unit_id`. The pair receives one consumption lock and does not authorize reuse elsewhere.

### Release

An image becomes reusable only after explicit project authority records `REJECT / NOT ENTER PROJECT / SUPERSEDED AND RELEASED`. Ordinary layout revision, downstream supersession or crop change does not release it.

Machine/register definition: `OLEANDER_IMAGE_CONSUMPTION_REGISTER_v1.0.md/.json`.

## 9｜Image-generation boundary

AI imagery remains supplementary when permitted. It never replaces Source Authority, Design Authority, authoritative geometry, technical dimensions, editable text or field truth.

When `NO_IMAGE_GENERATION` is active, the permitted/forbidden distinction becomes simpler: **no image-generation tool or generative-image adapter is called at all.**

The presence of an image-related output requirement does not override the lock.

## 10｜Readback, regression and review

- `Artifact existence ≠ Design quality`
- `Traceability ≠ Professional finish`
- `Evidence correctness ≠ Visual excellence`
- `Process PASS ≠ MAIN KEEP`
- `Render PASS ≠ Design PASS`
- `Prototype PASS ≠ Field PASS`
- `Regression PASS ≠ Design KEEP`

Producer self-check may accompany an artifact but cannot become independent Design Review where independence is required.

For visual artifacts, duplicate-image conflict, derivative identity laundering, image binding without ledger lookup, weaker re-authoring of a mature current artifact, or layout crop that breaks object integrity are direct `REVISE / BLOCK` triggers.

A continuation checkpoint may only advance from actual readback, a genuine repair-boundary HOLD, or typed handoff state. It may not use a plan, chat summary or producer assertion as the last verified artifact.

Dependent mutations in continuous execution require readback between nodes. Auto-advance is not evidence promotion and does not let a producer skip an independent review gate.

Before Remote/Authority/Release mutation, the current checkpoint sequence must be re-read. An uncertain remote side effect must be verified against its expected postcondition before retry.

## 11｜Execution Receipt

The Current `OLEANDER_EXECUTION_RECEIPT_v1.0` remains the single instance carrier. Its current policy requires all new execution receipts to record:

- active / inherited / revoked constraints;
- denied tools / outputs / creation actions;
- required behavior locks;
- applicable flow phases;
- phase results;
- incomplete required phases;
- final completion-gate verdict;
- continuation checkpoint when the same material task must continue across turns/handoffs while `WORKING/HOLD`;
- cross-context frontier discovery evidence only when such discovery was materially used;
- concurrency guard only when a resumable checkpoint drives a material Remote/Authority/Release mutation;
- adapter route decision only when a material execution evaluated multiple surfaces or used an ephemeral connected surface;
- remote-mutation idempotency evidence only when a remote outcome is uncertain or retry is considered;
- continuous execution evidence when multiple ready nodes were executed in one material run or auto-advance stopped before completion;
- `image_consumption` when semantic content imagery is involved, including lookup, reservation/consumption, conflicts, blocked assets, releases and verdict;
- `branch_ref_disposition` when a material execution used a Git work branch / PR and reaches closure: delete the merged ref after ref→SHA provenance capture unless an open PR head/base, active worktree, or explicit keep reason blocks deletion. Unmerged refs are never deleted by age alone.

Older receipts remain immutable provenance. These runtime extensions are prospective and conditional; they do not retroactively rewrite historical receipts or make every chat turn a new material execution unit.

## 12｜Synchronization

A material runtime change still follows:

`Current Authority readback → GitHub branch → commit → PR → CI → main readback → dependency-aware branch-ref disposition/readback → minimal Notion Current pointer/fact update when required → live drift check`.

This branch-ref step belongs to the existing Resolver closure/cleanup responsibility. It reuses `00-governance/runtime/github_branch_governance.py` and the Execution Receipt extension; it does not create a new Router, cleanup framework, or parallel branch authority.

A green CI run proves the declared machine checks passed; it does not by itself close a design or project task.

A chat/session boundary alone is not a cross-platform Current change and therefore does not trigger Notion writeback or drift mutation. Frontier discovery, liveness probes, idempotency verification and no-delta route decisions likewise remain ephemeral unless an existing persistence trigger applies.

## 13｜Does not prove

Resolver v1.2.5 being Current does not prove project design quality, field truth, engineering validity, user validation, rights clearance or candidate promotion. A discovered or valid continuation checkpoint proves only that an existing execution frontier can be resumed under unchanged authority. A concurrency guard proves only that the observed sequence still matches the executor's expected frontier at the guarded mutation boundary. Capability-role routing proves only that a bounded execution surface was selected under the declared constraints. An idempotency decision proves only the bounded retry/no-retry condition for that remote mutation. Continuous auto-advance proves only that successive nodes were eligible to execute in the current turn; none of these mechanisms independently prove Design PASS, Current, promotion or closure.
