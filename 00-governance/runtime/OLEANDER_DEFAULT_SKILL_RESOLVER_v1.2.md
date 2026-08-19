# OLEANDER Default Skill Resolver v1.2

Status: **ACTIVE CURRENT**  
Implementation revision: **1.2.2**  
Decision date: **2026-08-19**  
Scope: **ALL OLEANDER projects / conversations / agents / media**  
Notion Current Authority: **OLEANDER｜设计知识库（Design） v1.1.1**  
Execution implementation: **GitHub `Jiaosong/Design`**

## 0｜Purpose

v1.2.2 keeps the existing knowledge-first execution architecture and adds a third runtime hard gate to the v1.2.1 constraint/completion baseline:

1. **Sticky Execution Constraint Lock** — explicit negative user constraints are resolved before owner/tool selection and remain active until explicitly revoked.
2. **Flow Completion Gate** — a task that requires the full OLEANDER flow cannot be called complete until every applicable phase is actually closed.
3. **Existing Visual Authority + Image Consumption Gate** — visual work must first preserve mature/current design artifacts and must check whether a semantic content image has already been reserved or consumed before binding it to another surface.

This is not a new Skill, METHOD, taxonomy or parallel process framework. It hardens the existing Resolver / Image Processing TOOL / Receipt / CI chain.

Current invariant:

> **CURRENT ROOT → CURRENT TASK / SOURCE AUTHORITY → STICKY CONSTRAINT LOCK → LIVE REGISTRY / CURRENT KNOWLEDGE → EXISTING METHOD + SKILL READBACK → EXISTING MATURE DESIGN / CURRENT VISUAL AUTHORITY → IMAGE CONSUMPTION LOOKUP → REQUIRED NATIVE OUTPUT → MINIMUM SUFFICIENT OWNER SET / DAG → REAL EXECUTION → NATIVE ARTIFACT / HANDOFF → REGRESSION → ACTUAL READBACK → EVIDENCE + INDEPENDENT DESIGN REVIEW → FLOW COMPLETION GATE → EXECUTION RECEIPT → DRIFT / SYNC AS APPLICABLE**

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
- `OLEANDER_IMAGE_CONSUMPTION_REGISTER_v1.0` — allocation/register extension for semantic content images.

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
2. Resolve sticky execution constraints before any owner/tool selection.
3. Enforce tool/output/creation/process locks.
4. Resolve live Registry identity and Current knowledge context.
5. Retrieve relevant Current METHOD / THEORY / SOURCE / CASE / EVIDENCE / TOOL / PRACTICE.
6. Reuse mature design/current assets and actually read required existing Skill/capability material.
7. For visual work, identify the strongest current board / design object / native figure before designing the presentation carrier.
8. Before binding any semantic content image, query the project Image Consumption Ledger/Register by source hash / parent source / child figure / semantic identity.
9. If that `semantic_image_id` is already `RESERVED / CONSUMED / LEGACY_MULTI_CONSUMED / REJECTED_NOT_ELIGIBLE` for another consumer, stop and select another image; crop/recolor/mask/contour/screenshot derivatives do not reset identity.
10. Reserve an available image to the current consumer unit before layout production.
11. Define the required native output.
12. Build the applicable Flow Completion checklist.
13. Resolve Execution Owner Map and Skill Capability Contract.
14. Select the Minimum Sufficient Owner Set; build DAG only when necessary.
15. Resolve only allowed TOOL adapters and runtime capabilities.
16. Execute the real native/editable artifact.
17. Emit Native Artifact records / typed handoffs as applicable.
18. Run `STRUCTURAL / SEMANTIC / VISUAL_ROI / RUNTIME` regression as applicable.
19. Open/render/run the actual result and perform readback.
20. Run Evidence Gate and independent Professional Design Gate separately where applicable.
21. Verify the Flow Completion Gate.
22. Emit an Execution Receipt containing the active constraint lock, flow-completion state and image-consumption section when applicable.
23. Run Notion↔GitHub drift check where cross-platform pointers changed.
24. Only after failed execution/readback may reusable Skill gaps be diagnosed; active creation denies still take precedence.
25. Sync material delta and preserve provenance.

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

## 11｜Execution Receipt

The Current `OLEANDER_EXECUTION_RECEIPT_v1.0` remains the single instance carrier. Its current policy requires all new execution receipts to record:

- active / inherited / revoked constraints;
- denied tools / outputs / creation actions;
- required behavior locks;
- applicable flow phases;
- phase results;
- incomplete required phases;
- final completion-gate verdict;
- `image_consumption` when semantic content imagery is involved, including lookup, reservation/consumption, conflicts, blocked assets, releases and verdict.

Older receipts that predate the relevant policy sections remain immutable provenance and are explicitly allowlisted by the Receipt contract/validator; new receipts cannot omit applicable sections.

## 12｜Synchronization

A material runtime change still follows:

`Current Authority readback → GitHub branch → commit → PR → CI → main readback → minimal Notion Current pointer/fact update when required → live drift check`.

A green CI run proves the declared machine checks passed; it does not by itself close a design or project task.

## 13｜Does not prove

Resolver v1.2.2 being Current does not prove project design quality, field truth, engineering validity, user validation, rights clearance or candidate promotion. It makes user constraints, existing visual authority, semantic-image allocation and flow completeness first-class execution requirements instead of verbal promises.
