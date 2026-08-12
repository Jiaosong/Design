# OLEANDER Canonical Project Flow｜v0.3

**Status:** REVIEW  
**Application Primary Mapping:** B04｜Metrics & Governance  
**Application Supporting Mapping:** IP03｜Visual & Verbal System / SP04｜Construction & Operation  
**Knowledge Architecture note:** B04 / IP03 / SP04 describe Application Mapping only; knowledge ownership must be resolved separately through `Domain / exact L0–L7 level`.  
**Parent cognitive method:** `01B｜OLEANDER AI 协同设计方法｜读取、反馈与验证`

## 1｜Position

OLEANDER no longer treats AI collaboration, engine-style execution, project management, QA and persistence as parallel workflows.

The canonical project structure is:

`Design Intelligence (WHY) → Execution Runtime (HOW) → Evidence & Governance (PROOF)`

The cognitive method remains:

`Read → Frame → Hypothesize → Vary → Construct → Attack → Test → Decide → Archive`

The project flow adds the execution and governance semantics required to use that method across product/CMF, brand, spatial/architecture, digital/interaction and other OLEANDER work.

This flow is subordinate to already-active fail-closed governance. In particular, `Production Asset Persistence Gate v1.0` remains mandatory before AR-S09 / Promotion whenever its trigger conditions apply. A project- or Practice-specific logging/sync contract also remains binding; this flow does not silently cancel existing Notion/Drive/GitHub obligations.

## 2｜Dual Loop

### Loop A｜Exploration Sandbox

`Design Question → Sandbox → Variants → Compare → Reject / Branch / Candidate`

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
5. the next step requires reproducible/measurable execution.

Candidate is not Canonical.

### Loop B｜Canonical Production

`Candidate → Contract Compile → Authority Resolve → Capability Resolve → Execute → Machine QA → Visual QA → Project QA → Persistence Gate when triggered → Promote / Revise / Reject → Artifact Register → Cross-System Sync`

Execution should be deterministic wherever possible.

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

**Read → Frame → Explore → Compare → Candidate → Construct / Execute → Validate → Decide → Persist when required → Promote → Deliver → Observe → Archive → Re-enter**

Exploration may branch. Candidate Gate separates exploration from production. Workers construct/execute. Validation is Machine + Visual + Project QA plus any applicable specialized gates. Human design judgment owns Decide. When PAP applies, persistence closes before Promotion. Promotion establishes Canonical Authority and triggers default canonical cross-system synchronization. G9 can reopen a locked conclusion into the next Read cycle.
