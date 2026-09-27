# OLEANDER Runtime Contracts

This directory contains cross-project runtime and capability-routing contracts. It does not replace Notion Current Authority or Project State.

Cross-module complex-project orchestration is governed by `../complex-project-master-runtime-v1.0.md` and compiled through the existing Control Plane `MASTER_RUNTIME_STATE`; runtime contracts in this directory remain capability/execution owners beneath that Master rather than a parallel Master system.

`OLEANDER_CURRENT_ARCHITECTURE_MAP_v2.1.md` is the Current architecture **classification + executable control view** for the whole OLEANDER operating-system architecture. Its canonical count is `1 Current system architecture / 1 Complex Project Master Runtime / 11 stable Runtime Layers (R-A...R-K)`. Contracts, professional processes, state families, Reviews/Gates, Skills, tools and artifacts are object classes inside that architecture rather than additional top-level architectures.
The executable companion is `OLEANDER_ARCHITECTURE_CONTROL_GRAPH_v2.1.json`, validated by `validate_architecture_control_graph.py`. It compiles owner resolution, dependency/reopen routing, six cross-cutting operational planes, File & Artifact Management, AI File Handling/Knowledge Reader, failure recovery, compatibility and Controlled Evolution. `OLEANDER_EVOLUTION_CANDIDATE_CONTRACT_v1.0.json` is the machine contract for proposed system improvements; candidate/eval state never self-promotes Current. `OLEANDER_RUNTIME_LAYER_INTERFACE_CONTRACT_v1.0.json` defines the internal I/O, entry/exit, write-authority, readback, failure, plane-binding, handoff, persistence and claim-boundary contract for every R-A...R-K layer. `OLEANDER_OBSERVABILITY_RECOVERY_CONTRACT_v1.0.json` defines non-authoritative observability events plus blast-radius-scoped recovery incidents and closure/readback semantics without creating another Project State or incident authority database.


`OLEANDER_INTEGRATED_RUNTIME_STRUCTURE_v1.0.md` is the Current operator/integration view under that Master. It expands the path through Design Intelligence ? Shared Design Quality & Design Development ? authentic Professional Domain Process ? Integration when coupled ? Skill/Tool execution ? native artifact ? actual readback ? independent reviews, without creating another orchestration authority.

## Candidate provider-neutral runtime spike｜2026-09-26

`OLEANDER_RUNTIME_PROVIDER_CONTRACT_v0.1.md/.json` is a **candidate, non-authority** Runtime Provider Contract below the existing R-G/R-H capability/execution boundary. It does not create another Runtime Layer, Project State, Current, Control Plane, Skill ontology, professional process or Promotion path.

The executable spike lives in `runtime_provider_spikes/` and runs the same contract fixtures against:

- existing COS/native bridge;
- pinned DeepSeek Harness;
- Microsoft Agent Framework;
- PydanticAI + Temporal.

The first machine/readable benchmark is `runtime_provider_spikes/results/OLEANDER_RUNTIME_PROVIDER_BENCHMARK_20260926.json` with a human review companion `.md`. It intentionally stays outside `runtime/receipts/` because it is candidate benchmark evidence, not an Execution Receipt. `PASS_CANDIDATE_SPIKE` means only that the provider-neutral seam + bounded native smokes passed. It does **not** select/promote a provider or prove real artifact parity.

## Candidate unified system-management gateway｜Phase 2｜2026-09-27

`OLEANDER_SYSTEM_MANIFEST_v0.2.json` is the **candidate, non-authority** successor management entry over the existing Current architecture. It keeps the canonical count at `1 Current system architecture / 1 Complex Project Master Runtime / 11 stable Runtime Layers`; it does not create another Project State, Knowledge Registry, Control Plane, professional process, runtime-layer family or Promotion path. `OLEANDER_SYSTEM_COMPONENT_DISPOSITION_v0.2.json` records the explicit `KEEP / REFINE / MERGE / DECOUPLE / REPLACE / REMOVE` disposition of major system responsibilities without changing their owner-native authority.

`OLEANDER_SYSTEM_MANAGEMENT_ARCHITECTURE_v0.2.md` adds a G0–G11 **management view**, not a new runtime-layer family. It makes Governance/Authority, Project/Decision, Knowledge/Evidence, professional design, contracts, Master Runtime, Execution Fabric, Environment/Capability resolution, execution surfaces, artifacts/persistence, observability/recovery and evolution/designer development legible as one system while retaining the existing R-A...R-K owners.

`OLEANDER_CORE_INTERFACE_PRIMITIVES_v0.1.json` is the G4 interface vocabulary for `AuthorityRef / ProjectRef / KnowledgeMount / DecisionObject / ProfessionalStageRef / ActionRequest / ExecutionRoute / ArtifactRef / ReadbackResult / ReviewResult / PersistenceReceipt / LearningCandidate`. These are reference/handoff envelopes over existing owner-native contracts, not a new Project/Knowledge/Artifact store.

`oleander_system_gateway.py` composes a disposable `oleander.system-context-envelope.v0.1` and still delegates continuation/mutation/closure policy to the existing `oleander_chat_runtime_bridge.py` / Resolver. `oleander_system_mcp.py` now exposes seven MCP tools (`manifest`, `context`, `environment`, `capabilities`, `resolve`, `preflight`, `self-test`) so CoS or another compliant harness can consume one stable entrypoint. Capability resolution is read-only routing evidence; a selected execution surface still does not grant mutation or design authority.

`OLEANDER_COS_HARNESS_ADAPTER_v0.2.json` keeps CoS as `EXECUTION_HARNESS_AND_LOCAL_TOOL_SURFACE` with authority ceiling `EXECUTION_CAPABILITY_AND_OBSERVABILITY_ONLY`. CoS Session / Compact & Resume / workers / Goal-Loop / plugins / MCP remain provider-runtime facilities and never become Project State, Knowledge Authority, Design Decision, Artifact Current, Design KEEP, professional PASS or Promotion.

`OLEANDER_EXECUTION_RUNTIME_PRIMITIVES_v0.1.json` + `oleander_execution_runtime.py` implement three provider-neutral primitives: append-only `ExecutionLedger`, typed `ActionRuntime`, and execution-only `DurableJob`. `ActionRuntime` enforces `OLEANDER Action Guard > provider approval`; provider approval may narrow but never widen permission, and material mutation without actual readback is `PARTIAL`, not complete. `OLEANDER_RUNTIME_PROVIDER_CONTRACT_v0.2.json` binds these primitives while preserving the v0.1 contract/benchmark as historical conformance evidence rather than silently relabeling that benchmark as v0.2 proof.

The environment path now uses `OLEANDER_SHARED_EXECUTION_SURFACES_v0.1.json` as canonical static surface policy plus `oleander_environment_resolver.py` for normalized `ExecutionSurface` and current capability resolution. `.mcp-runtime/registry/OLEANDER_INTEGRATION_REGISTRY_CURRENT.json` remains machine-local runtime observation only. A stale snapshot can trigger reprobe, but it cannot produce an `AVAILABLE` route, override the canonical registry or change project authority. Connector access to an owner-native Current source is transport, not connector-owned Current.

Validation:

- `python 00-governance/runtime/validate_system_management.py`
- `python -m unittest 00-governance.tests.test_execution_runtime_primitives 00-governance.tests.test_environment_capability_resolver 00-governance.tests.test_system_management_v02 00-governance.tests.test_system_management_gateway 00-governance.tests.test_system_mcp_gateway 00-governance.tests.test_cos_system_gateway_binding`

Passing this candidate validation proves the management seam, runtime primitive invariants, stale-environment handling and authority separation only. It does not prove all historical runtime code migrated, make the gateway a second Current architecture, promote a runtime provider, or prove design/professional quality.

## Candidate OLEANDER Design System successor｜2026-09-27

`OLEANDER_DESIGN_SYSTEM_ARCHITECTURE_v0.1.md` defines the next Human-facing product shell above the Phase-2 system-management/runtime work. The product center becomes Projects / Design / Knowledge / Sources / Browser / Integrations / Review rather than Chat or CoS runtime mechanics. CoS is retained as `COS_NATIVE`; DeepSeek Harness is treated as a Host Runtime reference/candidate, not Project/Knowledge/Design authority.

`OLEANDER_DESIGN_SYSTEM_OBJECT_MODEL_v0.1.json` defines the six ownership kernels (`Authority / Project / Design / Knowledge / Surface / Execution`) and hard-separates `Project ≠ Repository ≠ Runtime Workspace ≠ Artifact Store ≠ Knowledge Store`. Git remains versioned materialization: branch/merge/clean state does not become Design Direction/KEEP/validity. Source Inbox preserves original files and creates structured, citation-bound Knowledge Drafts; vector indexes remain retrieval indexes rather than Knowledge bodies.

`OLEANDER_SURFACE_RELIABILITY_BOUNDARY_v0.1.json` makes surface reliability first-class across R1 Admission, R2 Identity, R3 Capability, R4 Execution and R5 Result. `oleander_surface_reliability.py` provides the reference evaluator. R1-R4 may route an execution; R5 exists only after execution and material mutation cannot close as verified without actual readback. Observation, interpretation, derived reliability and authority state are separate semantic levels. `Enabled / Connected / Loaded / Ready / Executed / Verified` are not synonyms.

`OLEANDER_PROJECT_WORKSPACE_BINDING_v0.1.json` + `oleander_design_system_runtime.py` implement the first Project materialization boundary: one owner-native Project may bind a primary repository, satellite repositories and multiple runtime workspaces, but Git/worktree fields are rejected if they claim Project Current, Design KEEP, professional PASS or Promotion. `.oleander/project.json` is only a bootstrap locator.

`generate_project_repository_migration_inventory.py` reads actual history-preserving `migration/<project>` split branches for the legacy `05-cases` monorepo layout and emits `OLEANDER_PROJECT_REPOSITORY_MIGRATION_INVENTORY_20260927.json`. The inventory records split commit/history/tree readback while keeping external repository existence/history explicitly `UNVERIFIED`, `project_state_ref=null` and `old_duplicate_retained=true`. An empty local `git remote` list proves only local configuration, never remote absence; target existence/history must be read back before any CREATE/PUSH decision.

`OLEANDER_SOURCE_INGESTION_PIPELINE_v0.1.json` defines Source Inbox progression from source identity/fingerprint through original preservation, native extraction, structured body, citation binding, Knowledge Draft, Content Review, KI, OE and mount eligibility. Browser captures enter the same Source Inbox. The reference runtime rejects authority injection, source-version drift and skipped ingestion states.

The Design System uses explicit `SurfaceDefinition / SurfaceInstance / SurfaceIdentity / CapabilityCatalog / ProviderPool / RoutingPolicy / SurfaceView` objects. DSH capability seams, durability barriers, projection-cache discipline, plugin/browser lifecycle and upload transport are implementation references. `dsh-agy-link` is a reference for provider-pool/identity/catalog/quota/retry reliability patterns; neither reference owns OLEANDER state.

`OLEANDER_SURFACE_VIEW_CONTRACT_v0.1.json` + `oleander_surface_view.py` make `SurfaceView` an explicit UI projection over the Current Execution View. Unavailable integrations remain visible, but the projection may not invent availability or reliability. `BrowserProfile` is likewise a project/research context projection whose downloads and persistent captures enter Source Inbox; it is not Project State and does not prove that a browser provider is currently bound.

`oleander_host_runtime_probe.py` performs current host-runtime discovery without promoting historical evidence. DSH stays `UNAVAILABLE` until a real binary/version probe succeeds. COS_NATIVE consumes the machine-local runtime readback only when it is fresh; a stale snapshot is reported as `STALE/UNKNOWN` and requires reprobe rather than being treated as current capability.

Additional validation:

- `python -m unittest 00-governance.tests.test_surface_reliability_boundary 00-governance.tests.test_design_system_architecture_v01 00-governance.tests.test_design_system_runtime_v01`

## Current default capability resolution

Use:

- `OLEANDER_CURRENT_ARCHITECTURE_MAP_v2.1.md`
- `OLEANDER_ARCHITECTURE_CONTROL_GRAPH_v2.1.json`
- `OLEANDER_EVOLUTION_CANDIDATE_CONTRACT_v1.0.json`
- `OLEANDER_RUNTIME_LAYER_INTERFACE_CONTRACT_v1.0.json`
- `OLEANDER_OBSERVABILITY_RECOVERY_CONTRACT_v1.0.json`
- `OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.md`
- `OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json` — Current implementation revision `1.2.5`
- `OLEANDER_NOTION_CURRENT_ARCHITECTURE_BINDING_v1.0.md/.json`
- `OLEANDER_NOTION_TO_GITHUB_EXECUTION_OWNER_MAP_v1.0.md/.json`
- `OLEANDER_EXECUTION_RECEIPT_v1.0.md`
- `OLEANDER_EXECUTION_RECEIPT_v1.0.json` — Current policy revision `1.1` + image-consumption extension when applicable
- `OLEANDER_IMAGE_CONSUMPTION_REGISTER_v1.0.md/.json`

Canonical default:

`CURRENT NOTION ROOT AUTHORITY → CURRENT TASK / SOURCE AUTHORITY → MASTER RUNTIME CONTEXT → STICKY CONSTRAINT LOCK → LIVE REGISTRY → CURRENT DOMAIN / L0–L7 / ROLE / FRAMEWORK TYPE WHEN L4 / CANONICAL ID → CURRENT METHOD / THEORY / SOURCE / CASE / EVIDENCE / TOOL / PRACTICE → TRAINING ASSIMILATION SNAPSHOT → ACTUAL EXISTING METHOD / SKILL READBACK → EXISTING MATURE DESIGN / CURRENT VISUAL AUTHORITY → IMAGE CONSUMPTION LOOKUP → REQUIRED NATIVE OUTPUT → FLOW COMPLETION CHECKLIST → GITHUB EXECUTION OWNER MAP → SKILL CAPABILITY CONTRACT → MINIMUM SUFFICIENT OWNER SET / DAG → ALLOWED TOOL ADAPTER WHEN REQUIRED → REAL NATIVE ARTIFACT → TYPED HANDOFF → STRUCTURAL + SEMANTIC + VISUAL_ROI + RUNTIME REGRESSION → ACTUAL READBACK → EVIDENCE GATE + INDEPENDENT DESIGN QUALITY GATE → MASTER STATE PROPAGATION / INTEGRATION READBACK WHEN TRIGGERED → LEARNING FEEDBACK → FLOW COMPLETION GATE → EXECUTION RECEIPT → DRIFT CHECK WHEN CROSS-PLATFORM POINTERS CHANGE`

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

`OLEANDER_DEFAULT_SKILL_RESOLVER_v1.1.md/.json` is superseded implementation provenance. Current execution uses v1.2 implementation revision 1.2.5; the runtime hardening compiles existing Resolver/Practice/Naming/Persistence rules and does not create a parallel METHOD or Skill.

Chat / Chat On Steroids entry enforcement now has a candidate unified entry above the existing bridge: `oleander_system_gateway.py` resolves the non-authoritative System Context Envelope, then delegates the actual continuation/mutation/closure decision to `oleander_chat_runtime_bridge.py` ? side-effect-free `oleander_chat_resolver_adapter.py`. The bridge remains the compatibility/execution-policy owner beneath the gateway and still owns no Project State, checkpoint database, Method, Skill or Control Plane. `oleander_system_mcp.py` exposes the candidate gateway to harnesses; `bind_chat_on_steroids_oleander.py` can persist the corresponding CoS runtime-context binding while preserving existing prompts and Goal enabled/mode state.

For material professional-domain work, adapter acceptance revision 1.2 also resolves `professional_stage_execution` through the existing professional machine definition + Execution Owner Map. Five OPEN Candidate process machines carry stage execution requirements directly; already-Current Architecture/Structural/MEP machines remain unchanged and use the exact-revision non-authority `OLEANDER_PROFESSIONAL_STAGE_EXECUTION_PROJECTION_v0.1.json` runtime carrier. The transient `professional_stage_composition` requires both task/claim Knowledge Mount coverage and legal Current execution-owner coverage. Missing/uncovered/OE1/stale knowledge HOLDs; Candidate Skills and Candidate Bodies do not count as Current callable owners; missing project/specialist/reviewer bindings HOLD. Owner identities are deduplicated only after complete capability coverage, and multiple Current owners require an actually materialized existing Multi-Skill DAG/typed handoff path before execution/closure. Candidate professional processes require explicit `BOUNDED_NON_CURRENT_PROJECT_EXERCISE` and retain `current_process_ref=null` until authorized adoption.

The canonical professional-stage execution spine is exactly: `Stage → Professional Question / Decision Object → Knowledge Inputs → Operational Knowledge Mount → Required Capability Roles → Current Execution Owners / Skills → Native Outputs → Actual Readback → Independent Review → Stage Closure`. The adapter emits this exact order in `canonical_stage_execution_chain` and a per-step `canonical_stage_execution_readback`. Tool/Adapter, Claim, DD responsibility and Interface bindings remain subordinate details and do not insert extra top-level stage steps. When closure is requested, `stage_instance_readback` reuses the existing Domain Stage Instance fields; decision-object-bound native outputs must be `READBACK_COMPLETE`, Actual Readback must exist, Independent Review must PASS with a distinct reviewer binding, and exit conditions must be `SATISFIED` before `stage_closure_gate=PASS`.

`compile_project_receipts.py` is the bounded receipt compiler/readback adapter for the same R-E facts. It currently derives Structural Engineering and Building Services / MEP candidate receipts from `DOMAIN_PROCESS_INSTANCE` records and can hash/validate existing Project Plane closure objects. The compiler uses `project-receipt-compiler.v1.schema.json`, pins the process-instance SHA, reports unresolved/stale source references, validates the emitted receipt against the existing receipt validator, and writes a separate compilation readback. Hash identity is checkout-stable: known UTF-8 text is hashed as `UTF8_TEXT_LF_CANONICAL_V1` (BOM-free UTF-8 with all line endings normalized to LF) while binary/unknown formats use `RAW_BYTES_V1`; every persisted digest carries its hash semantics. It is explicitly **non-authority**: a requested professional `PASS` is emitted as `HOLD`; the readback may only say `READY_FOR_AUTHORIZED_REVIEW` when every machine gate needed by the candidate PASS is otherwise satisfied.

`publish_execution_live_status.py` is the bounded live-observability publisher used by that wrapper. After a material verified checkpoint/node transition, rerunning `oleander_chat_runtime_bridge.py` with the refreshed source-observed checkpoint automatically attempts to project the `task_id`, `executor_id`, raw receipt status, current node, next allowed action and monotonic checkpoint sequence into the existing Cloudflare `runtime_state`. No status is inferred from resolver directives or checkpoint state. The projection is latest-only telemetry for Reader polling: it is not Project State, does not resolve owners, does not replace `OLEANDER_EXECUTION_RECEIPT_v1.0`, and cannot turn observed `CLOSED` into authoritative completion without the existing Flow Completion/readback contract. A publish failure therefore degrades observability only and must not alter the Resolver decision or mutation authority.

When the publisher is explicitly given an existing Execution Receipt through `--receipt`, it may additionally copy that receipt's already-resolved `authority.canonical_ids`, `required_native_output`, and minimum-sufficient `owner_set` into a bounded `execution_context` projection. This is a readback transport, not a second owner resolver: the receipt must carry the required owner-routing Flow phases as PASS, exactly one `PRIMARY_OWNER` matching `owner_set.primary_owner`, valid typed owner nodes, checkpoint provenance and non-stale authority evidence. Direct/raw live telemetry is deliberately unable to inject `execution_context`. Reader may consume this context only for an explicit matching `task_id` + exact Canonical ID; missing, stale, malformed, mismatched or ambiguous context remains unresolved. D1 is therefore only a derivative carrier of an existing Execution Receipt result and never gains owner, lifecycle or completion authority.

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
- `python 00-governance/runtime/validate_runtime_provider_contract.py` — candidate provider-neutral seam only; no Current promotion.
- `python -m unittest 00-governance/tests/test_runtime_provider_contract.py`

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
