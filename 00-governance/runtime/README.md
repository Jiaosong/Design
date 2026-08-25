# OLEANDER Runtime Contracts

This directory contains cross-project runtime and capability-routing contracts. It does not replace Notion Current Authority or Project State.

## Current default capability resolution

Use:

- `OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.md`
- `OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json` — Current implementation revision `1.2.2`
- `OLEANDER_NOTION_CURRENT_ARCHITECTURE_BINDING_v1.0.md/.json`
- `OLEANDER_NOTION_TO_GITHUB_EXECUTION_OWNER_MAP_v1.0.md/.json`
- `OLEANDER_EXECUTION_RECEIPT_v1.0.md`
- `OLEANDER_EXECUTION_RECEIPT_v1.0.json` — Current policy revision `1.1` + image-consumption extension when applicable
- `OLEANDER_IMAGE_CONSUMPTION_REGISTER_v1.0.md/.json`

Canonical default:

`CURRENT NOTION ROOT AUTHORITY → CURRENT TASK / SOURCE AUTHORITY → STICKY CONSTRAINT LOCK → LIVE REGISTRY → CURRENT DOMAIN / L0–L7 / ROLE / CANONICAL ID → CURRENT METHOD / THEORY / SOURCE / CASE / EVIDENCE / TOOL / PRACTICE → TRAINING ASSIMILATION SNAPSHOT → ACTUAL EXISTING METHOD / SKILL READBACK → EXISTING MATURE DESIGN / CURRENT VISUAL AUTHORITY → IMAGE CONSUMPTION LOOKUP → REQUIRED NATIVE OUTPUT → FLOW COMPLETION CHECKLIST → GITHUB EXECUTION OWNER MAP → SKILL CAPABILITY CONTRACT → MINIMUM SUFFICIENT OWNER SET / DAG → ALLOWED TOOL ADAPTER WHEN REQUIRED → REAL NATIVE ARTIFACT → TYPED HANDOFF → STRUCTURAL + SEMANTIC + VISUAL_ROI + RUNTIME REGRESSION → ACTUAL READBACK → EVIDENCE GATE + INDEPENDENT DESIGN QUALITY GATE → LEARNING FEEDBACK → FLOW COMPLETION GATE → EXECUTION RECEIPT → DRIFT CHECK WHEN CROSS-PLATFORM POINTERS CHANGE`

### Sticky execution constraints

Explicit negative user constraints are resolved **before** owner/tool selection and remain active through ordinary follow-ups until explicitly revoked. Current normalized rules include:

- `NO_IMAGE_GENERATION`
- `NO_NEW_SKILL`
- `NO_NEW_METHOD`
- `NO_NEW_FRAMEWORK`
- `USE_EXISTING_OLEANDER_METHODS_AND_SKILLS`
- `FULL_OLEANDER_FLOW_REQUIRED`
- `NO_PRODUCER_SELF_PROMOTION`

“继续 / 优化 / 再做 / 修一下” does not revoke an active constraint. An available capability does not override a deny lock. If no compliant fallback can produce the required native output, return the affected step as `HOLD` rather than violating the constraint.

### Existing visual authority + image consumption

For visual-producing tasks, Existing-first is now an enforceable pre-production gate rather than a preference:

`CURRENT SOURCE / MATURE DESIGN / CURRENT BOARD OR NATIVE ARTIFACT → IMAGE CONSUMPTION LOOKUP → DIRECT REUSE IF AVAILABLE → PRESENTATION ADAPTATION → NEW VISUAL ONLY IF A REAL GAP REMAINS`.

Hard direction: `OBJECT INTEGRITY → FRAME / LAYOUT`.

Project content imagery follows:

`ONE SEMANTIC CONTENT IMAGE → ONE CONSUMER UNIT`.

Before image binding or layout production, the owner must query the project Image Consumption Ledger/Register. `RESERVED / CONSUMED / LEGACY_MULTI_CONSUMED / REJECTED_NOT_ELIGIBLE` blocks reuse by another independent consumer. Crop, resize, recolor, mask, screenshot, contour trace and other presentation derivatives inherit the same `semantic_image_id`; a derivative is not a new image for reuse purposes.

Only explicitly classified `SYSTEM_REUSABLE` assets such as logo/wordmark/icons/state symbols/navigation symbols/base patterns/tokens may repeat. Same-source paired views are allowed only inside one declared paired consumer unit.

Global machine contract: `OLEANDER_IMAGE_CONSUMPTION_REGISTER_v1.0.md/.json`. Project-specific ledgers own actual allocations.

### Full-flow completion

`FULL_OLEANDER_FLOW_REQUIRED` means **all applicable phases must close**, not “run every Skill”. The Minimum Sufficient Owner Set remains mandatory.

For visual executions binding semantic content imagery, `EXISTING_VISUAL_AUTHORITY_AND_IMAGE_CONSUMPTION_CHECK` is an applicable required phase.

Plan, method explanation, artifact existence, export, PR, CI green, self-check, render PASS or regression PASS are intermediate states. A full-flow task cannot be reported `CLOSED / 完成 / 已闭环` until the Current Execution Receipt `flow_completion.completion_gate = PASS` and no required applicable phase remains incomplete.

### Runtime efficiency + verified reading｜2026-08-21 current hardening

The full OLEANDER flow remains mandatory where triggered, but governance work must not displace the native design task. Runtime now uses the following operational compression without information loss:

`ASSIMILATE → READ → TARGET → MAKE → LOOK → JUDGE → LEARN → SAVE`.

This is a compiled operating view of the existing Resolver, not a new framework or Gate.

**Verified source coverage.** When the user explicitly asks for a complete read, the run must enumerate the required source set and record `READ / PARTIAL / UNREAD / FAILED`. `READ COMPLETE` is allowed only when every required item is fully read. `SOURCE READ ONLY` forbids design, summary and advancement until coverage closes.

**Incremental read.** For ordinary continuation, reuse a verified read snapshot only when `source_id + revision/hash/last_edited_time` is unchanged. Read only changed/new material. A later explicit request to “重新完整看一遍” invalidates reuse and requires full coverage again.

**Output-first production.** Production tasks require both one `Decision Question` and one `Concrete Target`. Preflight should terminate as soon as the minimum sufficient authority / source / method / Skill set is resolved; then execute the real native/editable artifact. Method explanation is not a substitute for execution.

**Status truthfulness.** `READING` requires actual source fetch/read evidence. `EXECUTING` requires an actual tool/runtime/native-artifact mutation. `READBACK` requires reopening/running/rendering the actual result. If those events have not occurred, the state remains `NOT_STARTED` or `BLOCKED`; conversational progress language cannot manufacture execution state.

### Training assimilation｜current default

Practice is now an executable input, not an archive. Before relevant production, resolve a **Training Assimilation Snapshot** from Current `PRACTICE / METHOD / existing Skill delta` records. Do not reread the entire training corpus on every run: load only task-relevant active rules plus deltas newer than the previous snapshot.

Assimilated rules preserve their maturity and boundary. `KEEP FOR TRAINING / CANDIDATE` is advisory and may shape execution but cannot override Project / Source / Design Authority or become production KEEP automatically. Repeated project failure can narrow, demote or reject a training rule; project success can strengthen transfer confidence only after actual readback and review.

The current assimilated baseline includes the following families already evidenced in recent Practice records:

- **Visual hierarchy / typography:** Dominant Field and first-read ownership; page-type rhythm instead of one neutral template; bilingual role pairing; semantic occlusion priority; title identity from glyph/relationship rather than decoration.
- **Object / landscape / carrier priority:** object or landscape before explanation; carrier subordination; free-route reading rather than forced checkpoint sequence; full-resource sequential carrier where source integrity must remain visible.
- **Geometry / technical proof:** same-source paired-view geometry identity; experience ↔ technical-proof co-registration; detail-callout registration; negative-space integrity; geometry/annotation correspondence.
- **UI / interaction:** scene-anchored depth; world-viewport framing; responsive media art direction; one meaningful attention transition at a time; brand color and operational-state color remain semantically separated.
- **Data visualization / evidence:** small-multiple comparability on a shared visual scale; variable-to-primitive fit; evidence-state surface grammar; evidence encoding must not become decorative noise.
- **Brand / icon / handoff:** series identity comes from shared grammar rather than shared template; optical normalization across carriers; optical asset handoff; map-derived identity and functional wayfinding keep a semantic firewall.
- **CMF / product / 3D:** role-bound CMF; lifecycle evidence framing; physical-interaction cues escalate only when function requires them; surface/material treatment cannot substitute for geometry or evidence.
- **Landscape / planting:** field structure precedes species scatter; landscape reading remains spatial before informational overlay.

A training rule that conflicts with a more specific Current project source, locked variable, evidence boundary or direct user constraint is suppressed for that task and recorded as `NOT_APPLIED_CONFLICT`, not silently forced.

### Learning feedback

After actual project readback/review, compare the result against the assimilated rules. Only material learning deltas are written back:

- `CONFIRMED_TRANSFER` — project result supports the rule under stated conditions;
- `BOUNDARY_ADDED` — rule works only under narrower conditions;
- `COUNTEREXAMPLE` — project evidence contradicts the rule;
- `DEMOTE / REJECT` — repeated contradiction makes the rule unsafe as a default;
- `NO_DELTA` — do not create another training note merely because the rule was used.

Training therefore runs bidirectionally: `Practice → Project → Readback/Review → Practice correction`.

### File / artifact discipline integration

File discipline is mode-sensitive and must not slow exploration unnecessarily:

- `EXPLORE`: short working filenames are allowed and are non-authoritative.
- `CANDIDATE`: assign stable `artifact_id + revision + status`; the artifact becomes traceable across representations.
- `AUTHORITY / RELEASE`: use the full canonical naming contract and triggered manifest / persistence requirements.

One logical artifact has one Current revision and may have multiple representations: `SOURCE / NATIVE / CANONICAL / PREVIEW / PACKAGE`. A preview never reverses authority into its native source (`PNG ≠ SVG`, `render ≠ .blend`, `screenshot ≠ HTML`, `PDF ≠ CAD`). Representation files do not compete as separate Currents unless they are genuinely different logical artifacts.

Keep physical folders shallow. Identity, relations, revision, status and provenance belong in artifact metadata / manifest rather than deep directory nesting. Production binary persistence still follows PAP when triggered.

The GitHub installed-skill list is the formal reusable execution registry, not the complete OLEANDER design-intelligence inventory. GitHub Skill names are execution identifiers and must not be copied into Notion as a parallel taxonomy.

The execution-owner map is routing only. `NO_DEDICATED_OWNER` is valid and does not authorize automatic creation of a new Skill. An active creation deny is stronger still: it blocks gap-driven creation and requires existing-owner composition, fallback or HOLD.

For execution owners that produce or materially judge visual output, check local `VISUAL_LAYER_BINDING.md` when present. These files are binding-only and do not create a new visual taxonomy, style bible or effect methodology.

Current Notion structural routing uses the live Registry and `Canonical Parent｜层级上位 / Canonical Children｜层级子级`; historical navigation ancestry and legacy hierarchy fields are not Current routing authority.

`OLEANDER_DEFAULT_SKILL_RESOLVER_v1.1.md/.json` is superseded implementation provenance. Current execution uses v1.2 implementation revision 1.2.2 plus this 2026-08-21 runtime hardening; the hardening compiles existing Resolver/Practice/Naming/Persistence rules and does not create a parallel METHOD or Skill.

## Current executable contract layer v0.1

- `OLEANDER_SKILL_CAPABILITY_CONTRACT_v0.1.md/.json`
- `OLEANDER_MULTI_SKILL_EXECUTION_DAG_CONTRACT_v0.1.md/.json`
- `OLEANDER_TOOL_ADAPTER_CONTRACT_v0.1.md/.json`
- `OLEANDER_NATIVE_ARTIFACT_CONTRACT_v0.1.md/.json`
- `OLEANDER_EXECUTION_REGRESSION_CONTRACT_v0.1.md/.json`
- `OLEANDER_NOTION_GITHUB_DRIFT_CHECK_v0.1.md/.json`
- `OLEANDER_IMAGE_CONSUMPTION_REGISTER_v1.0.md/.json` — semantic content-image allocation extension; not a new Skill/METHOD/framework.

Instance carrier:

- `OLEANDER_EXECUTION_RECEIPT_v1.0.md`
- `OLEANDER_EXECUTION_RECEIPT_v1.0.json` — policy revision 1.1; all new receipts record `constraint_lock` + `flow_completion`; visual content-image runs additionally record `image_consumption`.
- `receipts/` — execution receipts. Only the explicitly allowlisted pre-policy receipts may omit policy-1.1 fields.
- `regression-baselines/` — typed four-layer regression baselines.

Validation entrypoints:

- `python 00-governance/runtime/validate_execution_contracts.py`
- `python 00-governance/runtime/validate_execution_locks.py`
- `python 00-governance/runtime/validate_image_consumption.py`

Runtime regression corpus:

- `evals/runtime/sticky_constraints_and_flow.jsonl`
- `evals/runtime/image_consumption_cases.jsonl`

These contracts and validators do not promote candidate Skills or Notion objects.

## Existing active runtime contracts

- `OLEANDER_UNIVERSAL_PRODUCTION_ENVIRONMENT_v1.0.md/.json` — Current implementation revision 1.0.1; constraint preflight now precedes capability routing and tool selection.
- `OLEANDER_BLENDER_RUNTIME_v1.0.md/.json`
- `OLEANDER_REFERENCE_MATERIALIZATION_GATE_v1.0.md/.json`

The Default Skill Resolver supplements the Universal Production Environment; it does not create a parallel tool environment.

## Hard boundary

`Artifact existence ≠ Design quality`  
`Traceability ≠ Professional finish`  
`Evidence correctness ≠ Visual excellence`  
`Process PASS ≠ MAIN KEEP`  
`Regression PASS ≠ Design KEEP`  
`PR / CI PASS ≠ FULL FLOW COMPLETE`  
`ONE SEMANTIC CONTENT IMAGE → ONE CONSUMER UNIT`  
`TRAINING KEEP ≠ PROJECT KEEP`  
`PREVIEW ≠ NATIVE AUTHORITY`

`NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS`

`NO LOSS` protects information; it does not require running every Skill or rereading unchanged material.
