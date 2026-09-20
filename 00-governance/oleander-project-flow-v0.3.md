# OLEANDER Canonical Project Flow｜v0.3

**Status:** ACTIVE / CURRENT EXECUTION-FLOW MODULE
**Application Primary Mapping:** B04｜Metrics & Governance  
**Application Supporting Mapping:** IP03｜Visual & Verbal System / SP04｜Construction & Operation  
**Knowledge Architecture note:** B04 / IP03 / SP04 describe Application Mapping only; knowledge ownership must be resolved separately through `Domain / exact L0–L7 level`.  
**Parent cognitive method:** `01B｜OLEANDER AI 协同设计方法｜读取、反馈与验证`

## 1｜Position

OLEANDER no longer treats AI collaboration, engine-style execution, project management, QA and persistence as parallel workflows.

This file is the canonical execution-flow module under `complex-project-master-runtime-v1.0.md`. The Master Runtime owns cross-module invocation, precedence, stale-state propagation and Promotion readiness; this file owns the execution-flow sequence itself. Neither file replaces the unique OLEANDER Current Authority.

The canonical project structure is:

`Design Intelligence (WHY) → Execution Runtime (HOW) → Evidence & Governance (PROOF)`

The cognitive method remains:

`Read → Frame → Hypothesize → Vary → Construct → Attack → Test → Decide → Archive`

The project flow adds the execution and governance semantics required to use that method across product/CMF, brand, spatial/architecture, digital/interaction and other OLEANDER work. Design Intelligence routing is governed by `design-intelligence-routing-and-review-v1.0.md`: it resolves existing L4/L5 methods/frameworks, L6 source/evidence/case material and relevant L7 practice into a project-runtime Design Intelligence Packet and Design Review Contract without creating a parallel knowledge taxonomy.

This flow is subordinate to already-active fail-closed governance. In particular, `Production Asset Persistence Gate v1.0` remains mandatory before AR-S09 / Promotion whenever its trigger conditions apply. A project- or Practice-specific logging/sync contract also remains binding; this flow does not silently cancel existing Notion/Drive/GitHub obligations.

## 2｜Dual Loop

### Loop A｜Exploration Sandbox

`Design Question → Knowledge Route → Frame / Intent → Sandbox → Variants → Compare → Attack / Test → Reject / Branch / Candidate`

Rules:
- one Decision Question per experiment;
- estimates and low fidelity are allowed;
- branching and rejection are expected;
- comparison is preferred to isolated-output evaluation;
- `FID0/FID1` are the default;
- experiments do not automatically create canonical versions or full three-system synchronization unless an explicit Practice/project contract requires it;
- exit on an acceptable corridor, an answered question, a viable Candidate, or a required reframe.

### Candidate Gate

A Candidate may enter Canonical Production only when:
1. the Decision Question is explicit;
2. the retention reason is explicit;
3. Locked and Open Variables are recorded;
4. it is more valuable to continue than rejected alternatives;
5. the next step requires reproducible/measurable execution;
6. when design-quality promotion is intended, relevant knowledge routes, review lenses, technical/evidence triggers and the current claim ceiling are resolvable through the Design Intelligence Packet;
7. when material project obligations affect the claim, a `PROJECT_REQUIREMENT_ACCEPTANCE_BASELINE` route is resolvable so each obligation has a source/revision, owner, acceptance method, proof class, acceptance criteria, verification owner, evidence route and reopen rule;
8. the applicable shared design-development responsibilities are resolved through `design-quality-and-design-development-specification-v1.0.md`, including whether `PROJECT_DESIGN_DNA`, multi-scale/state readback, comparison, content projection or other DD responsibilities are triggered;
9. when a professional domain process is triggered, its authentic professional stages, required outputs and review/readback obligations are resolvable; architecture uses `architecture-design-development-process-v1.0.md` and `ADD-00—ADD-17` rather than replacing those stages with shared DD identifiers;
10. when multiple disciplines materially couple, the critical interfaces, integration owner, coupling / criticality, shared variables, required maturity, acceptance basis and required integrated readbacks are resolvable under `cross-disciplinary-design-integration-v1.0.md`;
11. every required native output has a Current callable owner or an explicit project-authorized specialist owner. Candidate Skill / Candidate Body presence is not sufficient.

Candidate is not Canonical.

### Loop B｜Canonical Production

`Candidate → Contract Compile → Design Intelligence Resolve → Project Requirement / Acceptance Baseline when triggered → Shared Design Quality & Development Scope Resolve → Professional Domain Process Resolve when triggered → Cross-Disciplinary Integration Resolve when triggered → Authority Resolve → Required Capability Roles / Current Owner Resolve → Native Output Execute → Machine QA → Visual QA → Project QA → Artifact Review → Requirement Verification / Validation Readback → Design Quality Actual Readback → Professional Domain Readback when triggered → Integration Readback when triggered → Specialized Acceptance Gates when triggered → Evidence / Truth Review → Independent Design Decision → Persistence Gate when triggered → Promote / Revise / Reject → Artifact Register → Cross-System Sync`

Execution should be deterministic wherever possible.

When cross-disciplinary integration is triggered, the promotion-relevant `Integration Readback` emits or refreshes the current `CROSS_DISCIPLINARY_INTEGRATION_RECEIPT`. A material interface / system change makes affected receipt conclusions stale until the required reopen scope has been reconciled and read back.

When material project obligations are promotion-relevant, the current `PROJECT_REQUIREMENT_ACCEPTANCE_BASELINE` is compiled under `schemas/project-requirement-acceptance-baseline.v1.schema.json`. It does not replace domain requirements or Systems Engineering; it is the Project Plane compilation that prevents unverified obligations from disappearing between disciplines.

If technical drawing is a required native output and the Current route still resolves only to the Candidate Technical Drawing body, the project remains `CANDIDATE_BODY_HOLD` unless an explicit project-authorized specialist owner is bound. The general design owner may not absorb technical-drawing authority merely to avoid HOLD.

**Hard ordering:** if PAP is triggered, durable upload + independent retrieval + hash/size/open verification must PASS before AR-S09 and before `PROMOTED`. Cross-system registration/synchronization may continue after promotion, but the durable binary gate cannot be deferred until after promotion.

## 3｜Two State Machines

### Job State

`CREATED → RESOLVED → QUEUED → RUNNING → SUCCEEDED / FAILED / CANCELLED / CACHED`

This describes machine execution only.

### Design State

`EXPLORE → CANDIDATE → REVISE / REJECTED → PROMOTED → LOCKED → SUPERSEDED`

Valid example:

`Render Job = SUCCEEDED` + `Material Candidate = REJECTED`

Never infer `Render PASS → Design PASS`.

## 4｜Progressive Authority

`NONE → WORKING_SOURCE → CANDIDATE_AUTHORITY → CANONICAL_AUTHORITY → FROZEN_AUTHORITY`

Authority is object-specific. Geometry, Material Profile, Camera, Lighting, Content, Data and Code may have different authoritative sources.

A derived render mesh must not silently replace CAD/BIM/parametric Geometry Authority.

Authority state also does not overwrite evidence claim state. A project may have a canonical visualization profile while physical/process evidence remains `VISUALIZATION_LOCKED / BLOCKED / UNKNOWN` under the applicable evidence contract.

## 5｜Two Graphs

### Design Semantic Graph

Stores first reading, hierarchy, relationships, roles, locked/open variables, Decision Question and comparison logic.

### Technical Dependency Graph

Stores model/mesh, material, parameter preset, camera, lighting, runtime, worker, source, export and derived artifacts.

Technical dependency never substitutes for design relationship.

## 6｜Comparison-First

Default evaluation unit:

`A / B / C + fixed conditions + open variable → Review Contract → Decision Corridor`

Every comparison records:
- Decision Question;
- Locked Variables;
- Changed Variables;
- Reading Scale;
- Failure Signs;
- Exit Condition.

The design target is often an **Acceptable Corridor**, not a fake global optimum.

## 7｜Shared Fidelity Namespace

Bare `F1–F3` already has an active meaning in the AI runtime-evidence classification governed by `AIG-03`. Historical governance/evidence records may refer to the same lineage as `OLEANDER AI Runtime Evidence P2`; that old `P2` label is Legacy only and must not be reused as Current Authority. To prevent namespace collision, project-flow fidelity uses the explicit `FID` prefix:

- **FID0｜Preflight** — syntax, scene, topology, framing and obvious failures.
- **FID1｜Design Validation** — fast controlled comparison.
- **FID2｜Promotion** — higher fidelity only for retained candidates.
- **FID3｜Presentation** — final portfolio/client/animation output after promotion.

High fidelity is Gate-authorized expenditure, not the default.

## 8｜Execution Runtime

### Rendering

`Scene Compile once → Compiled Scene → Render Matrix`

Do not rebuild unchanged geometry/camera/lighting for every variant.

### Modeling

`Editable Source → Derived Model → Export`

Geometry Authority must be explicit.

### Capability Resolve

Workers may include Blender, Geometry Nodes, Rhino/Grasshopper, Fusion/CAD, GIS and Vector/2D. Software is an execution capability, not a design method.

## 9｜Cache and Review Context

Artifact cache may use:

`Geometry Hash + Material Hash + Parameter Hash + Lighting Hash + Camera Hash + Runtime Hash`

But an Artifact Cache Hit does not automatically reuse a review decision.

Review identity:

`Artifact Hash + Review Contract Hash`

The same image can answer different design questions.

A cache hit also does not prove that a previously qualified durable object is still retrievable; persistence status must use the applicable PAP receipt / retrieval evidence rather than cache existence.

## 10｜Three QA Layers

### Machine QA

Runtime/API errors, missing files, dimensions, normals, non-manifold, transforms, naming, clipping, export integrity, etc.

### Visual QA

Proportion, occlusion, hierarchy, first reading, surface artifacts, grain, reflection, highlight, scale and readability.

### Project QA

Whether the Decision Question was answered, Locked Variables were preserved and the current project/Gate intention is supported.

Review outcome: `PASS / REVISE / REJECT / BLOCKED`.

Machine / Visual / Project QA do not substitute for specialized gates such as rights, field/reality, engineering, human-test or PAP when those are applicable.

Machine / Visual / Project QA also do not substitute for professional design judgment. Triggered design lenses are resolved through `design-intelligence-routing-and-review-v1.0.md`; material design-development work additionally compiles the shared responsibilities in `design-quality-and-design-development-specification-v1.0.md`. Those DD responsibilities are cross-domain contracts, not professional stages. A technically correct, evidence-correct artifact may still receive `DESIGN REVISE / REJECT`.

For complex multidisciplinary work, `cross-disciplinary-design-integration-v1.0.md` governs interfaces, coupling / criticality, shared variables, interface maturity, acceptance contracts, dependency/change propagation, joint decisions and integrated readback. `ALL DISCIPLINES PASS` does not imply system-level Integration PASS, and a stale Integration Receipt cannot support Promotion.

For architecture / building-planning work that makes a material claim about functional zoning, adjacency, circulation, room usability, operational states, service/hygiene/security, life-safety-aware planning or accessibility-aware planning, `architecture-design-development-process-v1.0.md` is mandatory. A program overlay, area balance, no-overlap result, detailed model, render or technical QA PASS cannot replace the ADD chain.

For spatial / architectural / built-environment models that claim complete high-fidelity realism, close constructive completeness, construction-aware, near-as-built or digital-twin-ready representation, the canonical `high-fidelity-built-environment-model-gate-v1.0.md` is the specialized governance Gate. Its 3D execution / receipt implementation is `oleander-skills/oleander-3d-pipeline/BUILT_ASSET_HIGH_FIDELITY_ACCEPTANCE_EXTENSION.md`. It runs after general QA and before Promotion and emits `BUILT_ASSET_FIDELITY_ACCEPTANCE_RECEIPT`. Its `BA0?BA4` namespace describes built-asset representation depth and is independent from this flow's execution/render `FID0?FID3`, external BIM LOD, FIELD state and engineering/code/manufacturing authority.

### Shared Design Quality & Design Development result semantics

When material design-quality promotion is intended, emit a current `DESIGN_QUALITY_DEVELOPMENT_RECEIPT` under `schemas/design-quality-development-receipt.v1.schema.json`.

- `KEEP` means the Design Axis is sufficiently developed at the declared claim ceiling, the actual artifact/experience has been read back at the required size/state/medium, no in-scope Design hard fail remains, and independent design review agrees.
- `REVISE` means a material design relation remains under-developed and the current dominant root cause must be named before the next revision.
- `REJECT` means the current design direction is not viable at the declared intent/claim.
- `HOLD` means a material design decision genuinely depends on missing authority/input that cannot be truthfully resolved inside the current cycle.

Material changes to Design Intent, Project Design DNA, primary content/asset, formal grammar, composition/geometry, material/typography/color identity, target medium/state, professional interface or contradictory evidence make the affected Design Quality receipt stale until actual readback and independent design review are rerun.

### Professional Domain Process result semantics

Each triggered professional process owns its own stage semantics and receipt. Shared DD state never substitutes for professional process closure. Architecture currently emits `ARCHITECTURE_DESIGN_DEVELOPMENT_RECEIPT`; equivalent future domains must bind their own authentic process receipt rather than reuse `ADD-*` or `DD-*` as generic stage IDs.

Current machine receipt bindings now include:

- Architecture → `ARCHITECTURE_DESIGN_DEVELOPMENT_RECEIPT`;
- Structural Engineering → `STRUCTURAL_ENGINEERING_DESIGN_PROCESS_RECEIPT`;
- Building Services / MEP → `BUILDING_SERVICES_MEP_DESIGN_PROCESS_RECEIPT`.

Their domain receipt PASS remains separate from Design KEEP, Integration PASS, statutory approval, field truth and Promotion.

For Architecture, material changes to capacity, program, room location, circulation, major openings, stairs/lifts, public/private boundaries, operational states, structure/MEP/fire/accessibility interfaces, site access or retained fabric make the affected architecture receipt scope stale and require reopen/readback.

## 11｜Revision Boundary

Workers may automatically correct deterministic technical failures such as missing paths, clipping, NaN, naming, non-manifold or export errors.

Design changes must be issued as a **Revision Proposal**. Workers must not autonomously optimize design parameters in an unbounded loop.

A deterministic technical repair must still preserve the governing authority object and evidence boundary; it may not silently reconstruct a missing historical binary under the old identity.

## 12｜Resource Budget

Every execution contract should define limits for resolution/fidelity, samples/solver quality, runtime, variant count, iteration count and parallelism.

Budget controls `FID0/FID1/FID2/FID3` selection.

## 13｜Version Layers

Do not bump the main system version for every lab or preset change.

- **System Version** — architecture/API capability changes.
- **Contract Version** — public interface changes.
- **Asset/Preset Version** — asset content changes.
- **Project Profile Version** — project-locked values change.
- **Experiment/Lab Run ID** — single experiment; does not bump system version.

`v1.0.0` remains reserved for formally confirmed Canonical rules/assets under OLEANDER naming governance.

## 14｜Promotion-Focused Cross-System Sync

Default synchronization policy:

- Sandbox → local/temp by default; explicit Practice/project logging contracts may require Notion/Drive/GitHub records.
- Candidate → receipt/review evidence; if a production binary is being prepared for promotion and PAP is triggered, durable persistence must occur **here, before promotion**.
- PAP-triggered candidate → qualified durable store → independent retrieval → SHA/size/open verification → `PERSISTENCE PASS`.
- **PROMOTED → Artifact Registry → required GitHub / Notion / Google Drive authority/receipt synchronization**.

Therefore:

> `Promotion-focused sync` means full cross-system canonical synchronization is normally concentrated on promoted work. It does **not** mean durable production-binary persistence may wait until after promotion.

Not every execution is synchronized to all three systems, unless an explicit governing contract says otherwise. Explicit project, Practice, governance, rights or release contracts override this default.

## 15｜Artifact Registry

Canonical artifacts record at least:

`Artifact ID / Type / Project / Design State / Authority State / Source Job / Source Hash / Version / QA / Persistence / Dependencies / GitHub / Drive / Notion / Supersedes`

When PAP applies, Persistence records at least:

`PAP Triggered / PAP Status / Durable Store / Durable File ID / Retrieved SHA / Open Test / Receipt`.

GitHub, Notion and Drive are persistence/registry targets with explicit roles, not competing sources of truth. A text receipt in GitHub or Notion is not a substitute for the qualified durable binary object.

## 16｜Stop Conditions

Every experiment has a Decision Question and Exit Condition.

Stop when:
- an acceptable corridor is stable;
- the current question is sufficiently answered;
- additional fidelity no longer changes the design judgment;
- new information requires reframing;
- execution cost exceeds the value of the current question.

“Can still optimize a little” is not an acceptable infinite-loop criterion.

## 17｜Relationship to G0–G9

`G0–G9` is the outer project-governance Gate sequence. It is **not** the `P0–P4` Project Axis, not a Delivery Priority namespace, and not a waterfall schedule.

- G0–G2: Read / Frame / Exploration dominant;
- G3–G4: Exploration and Canonical Production alternate;
- G5–G6: Canonical Production becomes dominant;
- G7–G8: execution / acceptance / release;
- G9: operational feedback re-enters Read.

No G-stage is upgraded merely because a Job State is `SUCCEEDED`, a fidelity level is high, or a persistence gate passed.

## 18｜Canonical Formula

**Read / Route Knowledge ? Frame / Intent ? Explore ? Compare ? Candidate ? Compile Shared Design Development ? Execute Authentic Professional Domain Process ? Integrate when coupled ? Resolve Capability / Tool ? Construct / Execute ? Actual Readback ? Validate Truth + Performance + Design ? Design Crit / Decide ? Persist when required ? Promote ? Deliver ? Observe ? Extract Learning ? Archive / Re-enter**

Exploration may branch. Candidate Gate separates exploration from production. Workers construct/execute. Validation is Machine + Visual + Project QA plus any applicable specialized gates. Human design judgment owns Decide. When PAP applies, persistence closes before Promotion. Promotion establishes Canonical Authority and triggers default canonical cross-system synchronization. G9 can reopen a locked conclusion into the next Read cycle.
