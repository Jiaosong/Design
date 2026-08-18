# OLEANDER Default Skill Resolver v1.2

Status: **ACTIVE CURRENT**  
Implementation revision: **1.2.1**  
Decision date: **2026-08-18**  
Scope: **ALL OLEANDER projects / conversations / agents / media**  
Notion Current Authority: **OLEANDER｜设计知识库（Design） v1.1.1**  
Execution implementation: **GitHub `Jiaosong/Design`**

## 0｜Purpose

v1.2.1 keeps the existing knowledge-first execution architecture and adds two runtime hard gates directly into the Current Resolver:

1. **Sticky Execution Constraint Lock** — explicit negative user constraints are resolved before owner/tool selection and remain active until explicitly revoked.
2. **Flow Completion Gate** — a task that requires the full OLEANDER flow cannot be called complete until every applicable phase is actually closed.

This is not a new Skill, METHOD, taxonomy or parallel process framework. It hardens the existing Resolver / Receipt / CI chain.

Current invariant:

> **CURRENT ROOT → CURRENT TASK / SOURCE AUTHORITY → STICKY CONSTRAINT LOCK → LIVE REGISTRY / CURRENT KNOWLEDGE → EXISTING METHOD + SKILL READBACK → REQUIRED NATIVE OUTPUT → MINIMUM SUFFICIENT OWNER SET / DAG → REAL EXECUTION → NATIVE ARTIFACT / HANDOFF → REGRESSION → ACTUAL READBACK → EVIDENCE + INDEPENDENT DESIGN REVIEW → FLOW COMPLETION GATE → EXECUTION RECEIPT → DRIFT / SYNC AS APPLICABLE**

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

## 3｜Execution contract layer

The Current execution contract layer remains:

- `OLEANDER_SKILL_CAPABILITY_CONTRACT_v0.1`
- `OLEANDER_MULTI_SKILL_EXECUTION_DAG_CONTRACT_v0.1`
- `OLEANDER_TOOL_ADAPTER_CONTRACT_v0.1`
- `OLEANDER_NATIVE_ARTIFACT_CONTRACT_v0.1`
- `OLEANDER_EXECUTION_REGRESSION_CONTRACT_v0.1`
- `OLEANDER_NOTION_GITHUB_DRIFT_CHECK_v0.1`
- `OLEANDER_EXECUTION_RECEIPT_v1.0`

The constraint lock precedes these contracts; it can restrict which owners/tools are eligible, but it cannot rewrite Notion identity or invent a new owner.

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
4. `REQUIRED_NATIVE_OUTPUT_DEFINITION`
5. `CAPABILITY_AND_MINIMUM_OWNER_SET`
6. `REAL_EXECUTION`
7. `NATIVE_ARTIFACT_AND_TYPED_HANDOFF_RECORD`
8. `ACTUAL_READBACK`
9. `REGRESSION_AS_APPLICABLE`
10. `INDEPENDENT_REVIEW_AS_APPLICABLE`
11. `SYNC_RECEIPT_AND_DRIFT_AS_APPLICABLE`

For full-flow work, the following core phases cannot be skipped:

- Authority preflight
- Sticky constraint resolution
- Existing knowledge / METHOD / Skill resolution
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
2. Resolve sticky execution constraints before any owner/tool selection.
3. Enforce tool/output/creation/process locks.
4. Resolve live Registry identity and Current knowledge context.
5. Retrieve relevant Current METHOD / THEORY / SOURCE / CASE / EVIDENCE / TOOL / PRACTICE.
6. Reuse mature design/current assets and actually read required existing Skill/capability material.
7. Define the required native output.
8. Build the applicable Flow Completion checklist.
9. Resolve Execution Owner Map and Skill Capability Contract.
10. Select the Minimum Sufficient Owner Set; build DAG only when necessary.
11. Resolve only allowed TOOL adapters and runtime capabilities.
12. Execute the real native/editable artifact.
13. Emit Native Artifact records / typed handoffs as applicable.
14. Run `STRUCTURAL / SEMANTIC / VISUAL_ROI / RUNTIME` regression as applicable.
15. Open/render/run the actual result and perform readback.
16. Run Evidence Gate and independent Professional Design Gate separately where applicable.
17. Verify the Flow Completion Gate.
18. Emit an Execution Receipt containing the active constraint lock and flow-completion state.
19. Run Notion↔GitHub drift check where cross-platform pointers changed.
20. Only after failed execution/readback may reusable Skill gaps be diagnosed; active creation denies still take precedence.
21. Sync material delta and preserve provenance.

## 7｜Existing-first is now enforceable

New Skill creation is not authorized by:

- a new project;
- an interesting case;
- a new name;
- repeated local use;
- file existence;
- PR creation;
- CI success;
- a missing convenience helper.

If an active `NO_NEW_SKILL / NO_NEW_METHOD / NO_NEW_FRAMEWORK` constraint exists, new creation is blocked even if a gap is real. The correct output is existing-owner composition, fallback, or HOLD until the user explicitly changes the constraint.

`NO_DEDICATED_OWNER` remains a valid state and does not automatically authorize creation.

## 8｜Image-generation boundary

AI imagery remains supplementary when permitted. It never replaces Source Authority, Design Authority, authoritative geometry, technical dimensions, editable text or field truth.

When `NO_IMAGE_GENERATION` is active, the permitted/forbidden distinction becomes simpler: **no image-generation tool or generative-image adapter is called at all.**

The presence of an image-related output requirement does not override the lock.

## 9｜Readback, regression and review

- `Artifact existence ≠ Design quality`
- `Traceability ≠ Professional finish`
- `Evidence correctness ≠ Visual excellence`
- `Process PASS ≠ MAIN KEEP`
- `Render PASS ≠ Design PASS`
- `Prototype PASS ≠ Field PASS`
- `Regression PASS ≠ Design KEEP`

Producer self-check may accompany an artifact but cannot become independent Design Review where independence is required.

## 10｜Execution Receipt

The Current `OLEANDER_EXECUTION_RECEIPT_v1.0` remains the single instance carrier. Its current policy revision requires all new execution receipts to record:

- active / inherited / revoked constraints;
- denied tools / outputs / creation actions;
- required behavior locks;
- applicable flow phases;
- phase results;
- incomplete required phases;
- final completion-gate verdict.

Older receipts that predate this policy remain immutable provenance and are explicitly allowlisted by the Receipt contract/validator; new receipts cannot omit these sections.

## 11｜Synchronization

A material runtime change still follows:

`Current Authority readback → GitHub branch → commit → PR → CI → main readback → minimal Notion Current pointer/fact update when required → live drift check`.

A green CI run proves the declared machine checks passed; it does not by itself close a design or project task.

## 12｜Does not prove

Resolver v1.2.1 being Current does not prove project design quality, field truth, engineering validity, user validation or candidate promotion. It only makes user constraints and flow completeness first-class execution requirements instead of verbal promises.
