# OLEANDER Professional Domain Process Contract v1.0

**Status:** CURRENT GOVERNANCE CONTRACT
**Authority position:** subordinate to `complex-project-master-runtime-v1.0.md` and the Current OLEANDER Authority / Knowledge Architecture.
**Purpose:** define the reusable envelope that every authentic professional-domain design/development process must satisfy without replacing that profession's own semantics.
**Applies to:** Architecture, Structural Engineering, Building Services / MEP, Interior Design, Landscape Architecture, Lighting Design, Digital Product / HCD, Systems Engineering and any other materially triggered professional domain.
**v2.1 architecture placement:** canonical shared envelope for `R-E Professional Domain Execution Process` under `runtime/OLEANDER_CURRENT_ARCHITECTURE_MAP_v2.1.md`; domain stage-body records are runtime locators over canonical knowledge mounts, native outputs and readback, not copied Knowledge bodies and not a universal professional progress state.

---

## 1｜Why this contract exists

OLEANDER needs a common way to invoke, inspect, integrate, reopen and close professional work without pretending that every profession follows the same stage sequence.

The shared object is therefore a **contract envelope**, not a universal design process.

```text
WHAT IS SHARED
= identity + trigger + knowledge binding + interface contract
+ native-output contract + assurance + change/reopen + completion semantics

WHAT REMAINS DOMAIN-SPECIFIC
= professional questions + stage semantics + professional methods
+ native artifact semantics + professional acceptance logic
```

This contract closes a structural gap between:

- the Master Runtime's compact `professional_processes[]` summary;
- authentic domain process definitions such as Architecture `ADD-00 ... ADD-17`;
- the shared `DD-01 ... DD-12` design-development responsibilities;
- Knowledge Integrity / Operational Mount admission;
- Cross-Disciplinary Integration interface state;
- Skill / Capability / Tool execution;
- project-level stage execution and reopen state.

It does **not** create a second Master Runtime, a second Knowledge Architecture, a universal stage prefix, a new Review class or a new Skill family.

---

## 2｜Canonical position in OLEANDER

The canonical relationship remains:

```text
Current Authority
→ Master Runtime
→ Current Knowledge Resolution
→ Knowledge Integrity / Task-Claim Operational Mount
→ Design Intelligence
→ Shared Design Quality & Design Development
→ Authentic Professional Domain Process
→ Cross-Disciplinary Integration when coupled
→ Required Native Output
→ Capability / Skill Resolution
→ Tool / Adapter
→ Native Execution
→ Actual Readback
→ Professional / Artifact / Technical / Evidence / Design review
→ Independent Decision
→ Persistence when triggered
→ Human Promotion
→ Cross-System Sync
→ G9 bounded knowledge return
```

The professional process owns the **discipline's authentic development logic**. It does not own unrelated review, knowledge-integrity, operational-eligibility or integration authority.

Hard boundaries:

```text
CONTENT COMPLETE ≠ KNOWLEDGE CLEAN
KNOWLEDGE CLEAN ≠ OPERATIONALLY ELIGIBLE FOR EVERY CLAIM
OPERATIONAL ELIGIBILITY ≠ PROFESSIONAL STAGE PASS
DD RESPONSIBILITY ≠ PROFESSIONAL STAGE
PROFESSIONAL STAGE ≠ SKILL
SKILL ≠ TOOL
TOOL EXECUTION ≠ PROFESSIONAL PROCESS PASS
PROFESSIONAL PROCESS PASS ≠ DESIGN KEEP
DISCIPLINE PASS ≠ INTEGRATION PASS
INTEGRATION PASS ≠ DESIGN KEEP
READY FOR HUMAN DECISION ≠ PROMOTED
```

---

## 3｜Three separate object layers

Professional work must preserve three distinct object layers.

### 3.1 Process Definition｜R-E professional-definition layer

A reusable domain-process definition states how a profession develops and validates work in a bounded scope.

Example:

```text
Architecture Design Development Process v1.0
ADD-00 ... ADD-17
```

The **executable Current professional-process definition is an R-E owner-native object**. Reusable research or METHOD knowledge that explains or supports the process remains in the existing R-B Knowledge Architecture and is mounted/referenced by the R-E definition; Knowledge lifecycle state does not activate, Current-ize or supersede R-E professional stage semantics by itself. This separation creates neither a new Knowledge level nor a second process authority.

### 3.2 Domain Process Instance｜项目层

A project activates a process definition as a project-specific instance.

Example:

```text
KH_LY46
→ Architecture Design Development Process v1.0
→ project-specific Architecture process instance
```

The instance records project identity, baseline, owner-native domain state, Current-use/supersession binding, current stages, active interface refs, professional verdict, open items, receipts and claim ceiling. It is not reusable knowledge merely because it exists.

### 3.3 Domain Stage Instance｜运行层

A process stage may execute repeatedly across cycles and baselines.

Example:

```text
Architecture ADD-07 definition
→ KH_LY46 ADD-07 instance
→ cycle N / baseline Rxx / task-claim knowledge mounts / active interface refs / current readback / reopen state
```

Stage instances record the domain owner's own stage state plus the existing Current-use/supersession projection needed for runtime consumption. They do not create a universal professional progress state and do not become new canonical Knowledge Objects by default.

Canonical separation:

```text
PROCESS DEFINITION
≠ PROJECT PROCESS INSTANCE
≠ STAGE EXECUTION INSTANCE
≠ MASTER RUNTIME SUMMARY
```

---

## 4｜`PROFESSIONAL_DOMAIN_PROCESS` definition contract

Every Current professional process definition must resolve the following sections. A domain may add stronger or more specific fields; it may not silently omit applicable shared responsibilities.

The machine schema family is prospective. `schema_version = 1.0` remains the exact legacy read branch for earlier definitions that carried inline `interface_bindings[]` and no shared stage-body contract. `schema_version = 1.1` is the Current definition-emission branch: it requires `stage_body_contract` and emits `interface_binding_requirements[]` rather than duplicating R-F-owned interface truth. A v1.0 definition is not rewritten in place merely to satisfy the v1.1 carrier.

### A. Definition

Required identity:

- `process_id`;
- `domain`;
- `version`;
- `title`;
- `purpose`;
- `scope_in[]`;
- `scope_out[]`;
- `authority_position`;
- `current_definition_ref`.

The process ID and stage IDs remain domain-native. OLEANDER does not prescribe `ADD-*`, `STR-*`, `MEP-*` or any other prefix globally.

### B. Trigger

Resolve:

- `project_flow_trigger`;
- `design_question_types[]`;
- `responsibility_triggers[]`;
- `claim_ceiling_rule`;
- `not_triggered_when[]`;
- `mandatory_reopen_triggers[]`.

Triggering a professional process means the project is making a material claim that requires that profession's real development logic. Merely containing an object associated with that profession is insufficient.

### C. Knowledge Binding

Resolve the existing Knowledge Architecture routes needed to run the process:

- `operational_mount_contract_ref` → Current owner is `knowledge-integrity-and-operational-mount-v1.0.md`;
- `consequential_knowledge_rule` → consequential knowledge must be admitted by task/claim-scoped Operational Eligibility before it drives a professional decision;
- `required_methods[]`;
- `theory_routes[]`;
- `source_routes[]`;
- `evidence_routes[]`;
- `standard_code_routes[]` when applicable;
- `precedent_case_routes[]`;
- `practice_routes[]`;
- `tool_knowledge_routes[]` when relevant.

These are references into the existing L0–L7 architecture. They are not a new "Professional Process Knowledge Base".

The process definition does not duplicate `KI0...KI5` or `OE0...OE3`. It declares the mount requirement; the Current Knowledge Integrity & Operational Mount owner resolves canonical knowledge refs, task/claim eligibility, applicability, freshness/revalidation, claim ceiling, conditions and `does_not_prove`. A professional stage instance stores only the mount-record refs needed to prove that admission happened.

For consequential use, a stage must not silently consume a bare knowledge page reference as professional authority. The stage-side mount must preserve the Current contract's minimum semantics:

```text
knowledge_ref
operational_eligibility
eligibility_scope / professional question
claim_ceiling
applicability
conditions / unresolved items
freshness or revalidation trigger
does_not_prove
review basis
```

`KNOWLEDGE MOUNT PASS ≠ PROFESSIONAL STAGE PASS`.

### D. Authentic Professional Stages

Each stage definition records at minimum:

```text
stage_id
stage_name
professional_question
stage_body_contract
entry_conditions[]
required_inputs[]
knowledge_inputs[]
knowledge_mount_requirement
required_dd_dimensions[]
required_native_outputs[]
interface_requirements[]
interface_binding_requirements[]
human_experience_consequences[]
design_language_consequences[]
technical_consequences[]
content_projection_requirements[]
required_readback[]
professional_review_owner
independent_review_requirement
open_items_allowed[]
exit_conditions[]
reopen_triggers[]
claim_ceiling
does_not_prove[]
```

`knowledge_inputs[]` names required knowledge routes/questions. `knowledge_mount_requirement` declares when actual task/claim-scoped mount records are required before consequential decisions or closure. It does not copy Knowledge Integrity fields into the professional process.

`required_dd_dimensions[]` binds shared Design Quality responsibilities into the professional process without renaming the stage.

`content_projection_requirements[]` binds the Design Quality specification's content / body-text / figure / caption / no-loss requirements where a stage produces communicative artifacts. It does not turn presentation into the professional decision itself.

`stage_body_contract` defines how the professional decision is written, located and read back at runtime. It is a shared semantic envelope, not a shared visible heading set. At minimum it resolves:

```text
title rule / identity rule
required semantic section responsibilities
knowledge-mount reference rule
native source rule
actual readback rule
OPEN / failure / does-not-prove rule
bounded verdict / claim ceiling / reopen / next-action rule
```

The body contract must keep the professional stage's own terminology and authentic decision logic. It must not copy canonical Knowledge bodies, create a second knowledge taxonomy, or substitute professional prose for the required native carrier.

`does_not_prove[]` is mandatory and non-empty for a Current professional-stage definition. A professional stage may make a bounded claim, but it may not leave its authority ceiling implicit.

#### D.1｜Professional decision-content floor

A stage definition is not professionally substantive merely because every required field exists. Each material stage must contain enough **domain-native decision content** that a competent downstream professional can understand what is being decided, what controls the decision, what evidence is sufficient to retain it, and what would force it to reopen.

At minimum, resolve where applicable:

- **professional criteria** — the actual performance, safety, usability, spatial, environmental, material, operational or quality criteria governing the stage; when measurable, include the required units/tolerances/acceptance basis through Current owner sources rather than generic adjectives;
- **controlling assumptions and uncertainty** — which loads, demands, users, site conditions, operating states, material properties, source versions or external decisions the stage relies on, and how far the present claim may extend while those inputs remain provisional;
- **professional alternatives / route choice** — when different systems, layouts, details, control strategies, materials or implementation routes materially change the outcome, compare real alternatives under fixed criteria rather than documenting only the selected route;
- **spatial / physical consequence** — room, clearance, geometry, mass, section, support, access, replacement, tolerance, installation, maintenance or human-body consequences where the profession creates or constrains physical space;
- **technical / behavioral consequence** — loads, capacity, flow, energy, environmental response, control behavior, interaction state, failure mode, robustness, serviceability or equivalent system behavior where relevant;
- **material / assembly consequence** — material performance, aging, joints, interfaces, finish, durability, fabrication/installation method or repairability where the stage owns or constrains them;
- **human / operational consequence** — task, posture, reach, accessibility, comfort, supervision, cognition, staffing, maintainability or operating sequence when materially affected;
- **controlled variables issued and consumed** — values/conditions another domain is allowed to rely on, their source-of-truth carrier, maturity requested for the current claim and the consequences of divergence;
- **acceptance evidence** — the actual native calculation/model/drawing/schedule/prototype/test/inspection/measurement/readback needed to support the stage verdict; prose or document presence alone is insufficient;
- **decision threshold** — what observable condition distinguishes `PASS` from `REVISE`, what missing authority/evidence requires `HOLD`, and what result makes the present professional route no longer viable (`REJECT`) at this claim ceiling;
- **handoff payload** — the minimum decision object, controlled variables, assumptions/tolerances, native source refs, readback refs, OPEN limits and recipient needed for the next stage/domain to consume the result safely;
- **reopen semantics** — the specific upstream/input/native/interface change that invalidates the present reasoning, plus whether the expected blast radius is local, interface-material or wider.

Not every profession needs every bullet. A bounded `NOT_APPLICABLE_WITH_REASON` is legitimate where a relation is truly absent. What is not legitimate is a stage whose substantive content can be replaced by “coordinate with X”, “review Y”, “ensure quality”, “meet requirements” or “produce report/model” without specifying the professional relation being designed and judged.

For quantitative criteria, this contract does not impose cross-profession numbers. The domain owner must bind the threshold to the Current code/standard/brief/evidence/model basis and preserve units, applicability and tolerance. For qualitative professional judgment, the stage still needs an observable retention/failure criterion and actual readback at the condition in claim.

`FIELD COMPLETE ≠ PROFESSIONAL CONTENT COMPLETE`.

`DELIVERABLE NAMED ≠ PROFESSIONAL DECISION MADE`.

`COORDINATE / REVIEW / ENSURE ≠ ACCEPTANCE CRITERION`.

### E. Interface Contract

Every materially coupled stage must declare enough information for `cross-disciplinary-design-integration-v1.0.md` to own integration state:

- `inputs_from_domains[]`;
- `outputs_to_domains[]`;
- `shared_variables[]`;
- `interface_refs[]`;
- `controlling_authority_requirements[]`;
- `interface_maturity_policy`;
- `allowed_open_interface_conditions[]`;
- `integration_readback_requirements[]`.

The professional process **requests and references** interface resolution. It does not redefine Cross-Disciplinary Integration maturity, disposition, coupling, criticality or Acceptance Contract semantics.

There is deliberately **no process-level numeric/scalar enter/close maturity truth** in the Current machine contract. Each stage may emit `interface_binding_requirements[]` containing the shared variables, threshold requested for the stage claim, a coupling/criticality **hypothesis** and the required native-source role. `R-F` then instantiates or resolves the actual interface binding / Acceptance Contract and remains the sole owner of actual maturity, disposition, coupling, criticality and current interface source-of-truth. A requirement record is not an interface-state record. `interface_maturity_policy` may only state the rule for resolving those per-interface requirements; it cannot override R-F with a profession-wide scalar.

### F. Execution Binding

Resolve what must actually be produced before capability/tool routing:

- `required_native_outputs[]`;
- `native_source_of_truth_rules[]`;
- `execution_owner_requirements[]`;
- `required_capabilities[]`;
- `tool_adapter_requirements[]`;
- `typed_handoff_contracts[]`;
- `actual_readback_requirements[]`.

Canonical order:

```text
Professional Requirement
→ Required Native Output
→ Required Capability
→ Skill / Execution Owner
→ Tool / Adapter
→ Native Artifact
→ Actual Readback
```

The live Skill Resolver selects the minimum sufficient owner set. A process definition must not hardcode a stale global Skill inventory.

v2.1 file/Reader controls remain cross-cutting here. A professional process may request the source, native output or read depth it requires, but it does not gain a separate file authority or Knowledge Reader authority. Before a material mutation, resolve the logical artifact identity, Current revision, write authority, intended delta, affected consumers, recovery path and required readback. Professional execution should preserve `one logical artifact → one Current revision → N representations`; a derived preview/package may not silently replace its native source.

Consequential professional knowledge continues to enter through R-B task/claim Operational Mount. Direct Reader/search/materialization access may support retrieval or exact-byte processing, but `READABLE ≠ KNOWLEDGE AUTHORITY ≠ OE ELIGIBLE`, and `CAN READ ≠ CAN EDIT`.

### G. Assurance

Resolve:

- `professional_review`;
- `evidence_review`;
- `technical_gates[]` when applicable;
- `independent_review` when required;
- `receipt_contract`;
- `does_not_prove[]`.

Professional assurance may consume the canonical Review classes, but it must not create a parallel review taxonomy solely for the domain.

`does_not_prove[]` must be non-empty. Passing the process contract cannot be used to widen the professional, statutory, engineering, field or Design claim.

### H. Change / Reopen

Resolve:

- `reopen_triggers[]`;
- `stale_scope_rules[]`;
- `upstream_impact_rules[]`;
- `downstream_impact_rules[]`;
- `interface_reopen_rules[]`;
- `receipt_stale_rules[]`.

Changes use the existing Master / Integration impact classes:

```text
NON_MATERIAL
LOCAL_MATERIAL
INTERFACE_MATERIAL
COUPLED_SYSTEM
PROMOTION_BREAKING
```

Do not create domain-specific duplicates unless a domain needs a finer internal classification subordinate to these shared classes.

Where the changed relation is a file/native-artifact mutation, classify semantic impact rather than byte difference alone. Reopen only affected consumers, derivatives, interfaces, reviews and receipts; preserve unrelated verified professional state. A move/rename/export that preserves the governed relation need not reopen the same scope as a geometry, calculation, topology or controlled-variable change.

### I. Completion

Resolve:

- `process_exit_conditions[]`;
- `stage_exit_logic`;
- `open_items_allowed[]`;
- `professional_receipt`;
- `promotion_effect`;
- `claim_ceiling`;
- `does_not_prove[]`.

A professional process closes only at its declared claim ceiling. Unresolved items may remain only if they are explicitly allowed, outside the promoted claim, and do not contradict an in-claim decision.

`does_not_prove[]` must be non-empty. Process closure does not inherit a broader claim from a downstream Design or Promotion decision.

---

## 5｜Stage binding to Shared Design Quality & Design Development

The shared Design Development Kernel (`DD-01 ... DD-12`) is a responsibility overlay.

A professional stage declares which shared responsibilities are materially triggered, for example:

```text
DOMAIN STAGE X
→ professional question
→ DD-02 Concept
→ DD-04 Form / Composition
→ DD-05 Human Relation
→ DD-08 Detail / Craft
→ DD-12 Integration / Coherence
```

The mapping means those design-quality responsibilities must be resolved at that stage's current claim ceiling. It does **not** mean the stage has been renamed or that the DD list becomes a universal project sequence.

### 5.1｜Trigger rule

Map a DD responsibility because the professional stage materially **creates, changes, constrains, tests or accepts** that design relation, not because the DD label appears semantically similar to the stage name.

Typical trigger questions are:

- does this stage create or revise project intent/criteria? → `DD-01`;
- does it choose or materially shape a generative system/option? → `DD-02`;
- does it change user/service/spatial/temporal experience? → `DD-03`;
- does it materially shape form, composition, massing, hierarchy or arrangement? → `DD-04`;
- does it change body/task/access/ergonomic relation? → `DD-05`;
- does it change sensory/environmental response? → `DD-06`;
- does it change a project Design DNA / formal-language relation? → `DD-07`;
- does it develop a detail/interface/constructive craft relation? → `DD-08`;
- does it require a prototype/test/experiment to answer the professional question? → `DD-09`;
- does it define adaptation across states, contexts or lifecycle conditions? → `DD-10`;
- does it materially shape meaning, memory, cultural or interpretive relation? → `DD-11`;
- does it resolve coherence across systems/domains/scales? → `DD-12`.

The process definition stores the triggered IDs in `required_dd_dimensions[]`. The Design Quality owner retains the meaning of those dimensions; the professional process owns how they are expressed through authentic domain work.

### 5.2｜Stage-DD execution relation

For each triggered DD responsibility, a professional stage should be able to resolve:

`stage question → DD responsibility → domain-native criterion → required input/evidence → professional development action → native output → actual readback → bounded professional finding → Design Quality consequence / OPEN item`.

The stage does not need a separate artifact for each DD ID. One native drawing/model/calculation/prototype may carry several coupled responsibilities, provided the body/readback can recover which relation each responsibility refers to.

### 5.3｜Closure and failure boundary

Professional stage closure does not automatically close its mapped DD dimensions. A stage may be professionally `PASS` while a Design Quality question remains `REVISE`, and a strong Design result may coexist with a professional `HOLD` outside the Design owner's authority.

Reopen the mapped DD relation when the professional change alters a material design consequence, such as member depth changing spatial proportion, MEP routing changing ceiling/section hierarchy, accessibility geometry changing circulation/thresholds, controls behavior changing user experience, or fabrication constraints changing detail/form language.

`DD MAPPING ≠ STAGE RENAMING`.

`PROFESSIONAL PASS ≠ DD KEEP`.

`DD KEEP ≠ PROFESSIONAL PASS`.

---

## 6｜Stage binding to content, presentation and projection

Professional design decisions often fail because a correct underlying decision is projected through an incomplete or misleading artifact. Therefore each stage may declare projection requirements using the shared Design Quality specification.

### 6.1｜Professional body before presentation

Projection starts from the **professional stage body**, not from slide, board, web or publication styling. Every materially executed or in-claim stage must remain recoverable as a structured professional body before its information is compressed into a presentation surface.

Minimum semantic responsibilities, expressed through domain-native visible headings where appropriate:

1. `Professional Question / Scope`;
2. `Current Condition / Problem`;
3. `Authority / Canonical Knowledge / Evidence Inputs`;
4. `Professional Criteria / Intent`;
5. `Development / Analysis / Comparison / Mechanism`;
6. `Cross-domain Interfaces` when materially coupled;
7. `Native Output / Source of Truth`;
8. `Actual Readback / Finding`;
9. `Failure / OPEN / does_not_prove`;
10. `Verdict / Claim Ceiling / Reopen / Next Action`.

The stage may combine responsibilities where authentic professional practice does so, or disposition one as `NOT_APPLICABLE_WITH_REASON`. It may not satisfy the contract through an untitled paragraph dump, a decorative heading with no substantive body, or silent omission of a material responsibility.

Generic titles such as `Analysis`, `Concept`, `Design Development`, `Final`, `Planning` or `Review` are incomplete by themselves. The title must identify the actual decision object, professional stage and bounded scope/cycle/baseline as applicable.

Hard boundaries:

```text
PROFESSIONAL BODY STRUCTURE ≠ KNOWLEDGE BODY DUPLICATION
PROFESSIONAL PROSE ≠ NATIVE OUTPUT
NATIVE OUTPUT EXISTS ≠ PROFESSIONAL PASS
MACHINE BODY-COMPLETENESS PASS ≠ PROFESSIONAL JUDGMENT
```

### 6.2｜Knowledge and evidence projection boundary

When the professional body consumes knowledge, it stores **refs plus task/claim-scoped mount state**, not copied reusable content. The stage may summarize the consequence for the current decision, but the canonical Knowledge Object remains the owner of theory, method, source, evidence, case or Practice content.

Where consequential, preserve the mounted decision context:

```text
knowledge_ref
use_role
operational_eligibility
claim_ceiling
applicability
conditions
freshness / revalidation trigger
does_not_prove
review_basis
```

An `OE2` condition remains visible wherever omitting it would widen the professional claim. An `OE1` object may remain as OPEN, excluded input or counterevidence, but it may not support an in-claim stage `PASS`.

### 6.3｜Native carrier and actual readback binding

The stage body identifies the native or authoritative carrier that actually contains the professional decision. Text, screenshots, renders and presentation graphics may explain the decision, but they do not replace geometry, calculations, schedules, simulation models, editable state models, physical test records or other domain-native sources when those are required by the claim.

The body must preserve the distinction:

```text
INTENDED
→ IMPLEMENTED IN NATIVE CARRIER
→ OBSERVED IN ACTUAL READBACK
→ INTERPRETED PROFESSIONAL FINDING
```

Producer intent, implementation state, observed readback and professional interpretation must not be collapsed into a single narrative statement.

### 6.4｜Stage-body runtime record

Where a process receipt is emitted, each materially executed/in-claim stage must be able to point to a compact body record such as:

```yaml
stage_id:
body_ref:
title:
section_coverage:
knowledge_mount_refs:
native_artifact_refs:
readback_refs:
interface_refs:
claim_ceiling:
open_items:
reopen_triggers:
stage_verdict:
```

The runtime record is a locator/index over existing owners. It is not a new Knowledge Object and must not duplicate the full body when the current project carrier already contains it.

#### R-I review consumption boundary

When a stage body is material to closure, `R-I Actual Readback & Review` consumes the stage-body record as a locator. The reviewer must reopen the referenced native output and actual readback and verify that the reviewed identity/revision matches the stage body. Body completeness, professional prose or a producer-side screenshot cannot substitute for that readback.

If the locator is stale, incomplete or points at a superseded native/readback result, the review remains open and the gap routes back to the appropriate R-E/R-H owner. R-I may record the mismatch and bounded review finding; it may not rewrite the professional body, Knowledge mount, domain verdict or native source to close the gap.

`STAGE BODY COMPLETE ≠ NATIVE OUTPUT VERIFIED ≠ PROFESSIONAL PASS`.

### 6.5｜Presentation / projection requirements

Applicable stage outputs should state:

- required body-text role / `DESIGN DEVELOPMENT BODY` coverage;
- mandatory diagrams / drawings / schedules / simulations / prototypes;
- Figure Role (`EVIDENCE / ANALYSIS / EXPLANATION / COMPARISON / TECHNICAL / EXPERIENCE / ORIENTATION / REFERENCE / DECORATIVE`);
- Text–Visual relationship (`DUPLICATE / LABEL / EXPLAIN / EVIDENCE / COMPARE / EXTEND / COUNTERPOINT / NAVIGATE`);
- caption type;
- `MUST_SHOW / MAY_COLLAPSE / MUST_RETAIN / MUST_COLOCATE` constraints;
- reading scale / resolution scale where applicable;
- required actual readback context.

No projection may hide an in-claim blocker, limitation or uncertainty.

Typical co-location requirements remain:

```text
claim ↔ critical limitation
number ↔ unit
requirement ↔ authority
figure ↔ legend
decision ↔ unresolved blocker
status ↔ reason
```

---

## 7｜Cross-disciplinary synchronization rule

Disciplines do **not** synchronize by stage number or nominal stage name.

Incorrect:

```text
Architecture ADD-07
→ Structural STR-07
→ MEP MEP-07
```

Correct runtime question:

> Does the current architecture decision have every required incoming interface at the maturity and authority required for this claim, and have its outgoing controlled variables been issued at the maturity required by consuming domains?

The source-domain stage reference must point to the actual Current domain process/milestone when one exists. Until a domain-native process definition is Current, use the domain's current authoritative input/milestone description; **do not invent a synthetic numbered stage merely to fill the matrix**.

### 7.1｜Interface requirement → R-F binding, not stage matching

Synchronization is performed through the existing Integration owner. An R-E stage emits `interface_binding_requirements[]`; R-F resolves each material requirement into its owner-native interface binding / Acceptance Contract. The stage-side requirement may state:

`requirement_id / source_domain / source_stage_ref / direction / shared_variables / coupling_hypothesis / criticality_hypothesis / required_maturity_to_enter / required_maturity_to_close / allowed_dispositions_on_exit / required_native_source_role / integration_binding_ref when resolved / acceptance_contract_ref when resolved / requested_change_reopen_rule`.

`coupling_hypothesis` and `criticality_hypothesis` are routing/coordination hypotheses only. They may help R-F initialize or inspect the relation; they are not actual interface-state truth. `integration_binding_ref` / `acceptance_contract_ref` point to R-F-owned objects when those objects exist.

The maturity order is:

`IDENTIFIED → DEFINED → COORDINATED → EXERCISED → VERIFIED`.

For one **requirement**, the maturity requested to close may not be lower than the maturity requested to enter. This is a machine-checkable requirement-consistency rule; it does not validate actual interface maturity, does not mean every interface must reach `VERIFIED`, and does not make stage progression globally linear.

### 7.2｜Entry, work and exit behavior

At stage entry, dereference the R-F-owned interface binding / Acceptance Contract and confirm that every in-claim incoming interface has the authority, maturity and source-of-truth required to begin the affected professional decision. During the stage, issue outgoing professional controlled variables and let R-F resolve their interface effect. At exit, compare each material interface against its R-F-owned current binding and the R-E stage requirement.

An `OPEN` interface may remain only when the referenced binding/Acceptance Contract permits it, the open item is visible, the claim ceiling excludes the unresolved consequence, and downstream consumers are not told that the interface is closed. A `BLOCKED` interface prevents the dependent claim from closing. `OUTSIDE_CLAIM` is a bounded disposition, not a way to hide a known in-claim dependency.

### 7.3｜Change and divergence

If two domains issue incompatible values for the same controlled variable, do not select whichever value is newest or easiest to model. Route the conflict to the controlling authority / Integration owner, preserve both source refs, and block the affected dependent claim until a bounded disposition exists.

When a shared variable changes, use the R-F-owned binding / Acceptance Contract plus the existing dependency graph to reopen only actual consumers. The R-E `requested_change_reopen_rule` may inform that route but does not override R-F. A stage-number match, federated-model presence or clash-free result does not prove interface acceptance.

`SAME STAGE NUMBER ≠ SYNCHRONIZED`.

`CLASH-FREE ≠ INTERFACE ACCEPTED`.

`INTERFACE MATURITY ≠ PROFESSIONAL VERDICT`.

---

## 8｜`DOMAIN_PROCESS_INSTANCE`

A project-level process instance minimally records:

```text
instance_id
project_id
workstream_id when applicable
decision_object_refs[]
process_definition_ref
process_id
process_version
domain
owner
current_baseline
domain_state
current_use_state
process_exit_condition_state
professional_verdict
claim_ceiling
stage_instances[]
active_interface_refs[]
open_items[]
professional_receipt_refs[]
integration_receipt_refs[]
stale_scope[]
reopen_events[]
last_updated
```

`domain_state` is owner-native and intentionally not constrained to one cross-profession progress vocabulary. `current_use_state = CURRENT / STALE / SUPERSEDED` is only the existing Current/Supersession projection for this instance. `process_exit_condition_state = NOT_EVALUATED / OPEN / SATISFIED / BLOCKED` records whether the process-level exit contract is currently met. These facts remain independent from `professional_verdict`, which is the bounded professional judgment compiled to the Master Runtime's existing `professional_processes[].verdict`.

The instance may be embedded in the existing project/runtime carrier or persisted as a dedicated runtime artifact when the existing persistence policy triggers. **This contract does not create a mandatory new database.**

The Master Runtime continues to carry only its compact `professional_processes[]` summary for orchestration.

---

## 9｜`DOMAIN_STAGE_INSTANCE`

A stage instance minimally records:

```text
stage_instance_id
stage_definition_ref
stage_id
cycle
baseline_ref
domain_state
current_use_state
review_verdict
claim_ceiling
inputs[]
outputs[]
consequential_knowledge_mount_required
knowledge_mount_refs[]
interface_refs[]
evidence_refs[]
review_refs[]
review_bindings[] when emitted under project-instance schema v1.1 and a PASS review is claimed
open_items[]
in_claim_blocking_open_item_count for project-instance schema v1.1
stale_scope[]
reopen_events[]
exit_condition_state
actual_readback_refs[]
last_updated
```

`knowledge_mount_refs[]` point to the Current task/claim-scoped mount records governed by `knowledge-integrity-and-operational-mount-v1.0.md`. The stage instance does not reissue KI/OE judgments.

For new project/runtime instance emissions, `schema_version = 1.1` is the Current machine contract. Historical `schema_version = 1.0` instances remain immutable/read-compatible evidence and are not rewritten to acquire the v1.1 fields. A v1.1 stage that claims `PASS` must bind each consumed review through `review_bindings[]` with `review_ref / reviewer_id / review_input_artifact_ref / review_input_revision_or_hash`; the referenced artifact must be one of the stage body's native-artifact refs and the review ref must be one of the stage's declared review refs. This proves exact review-input binding only. It does not award reviewer competence, independence, authorization or the review verdict, all of which remain with the applicable R-I/professional review owner.

`in_claim_blocking_open_item_count` is a v1.1 machine projection, not a new professional state family or issue database. A v1.1 stage/process may report OPEN material outside or later than the bounded claim, but `exit_condition_state = SATISFIED` / `process_exit_condition_state = SATISFIED` requires the corresponding in-claim blocking count to be zero. The underlying open-item evidence remains owner-native.

The stage instance is a runtime carrier, not a Knowledge level and not an automatic separate page/file.

One process stage may have multiple cycles. A new cycle does not erase prior valid evidence; prior cycle evidence becomes superseded/stale only at the affected scope.

Where a new cycle or owner-native successor changes the material native output/readback relation, the predecessor stage-body record and professional receipt remain historical evidence under the authority/baseline that produced them. Do not rewrite the predecessor receipt or body record to impersonate the successor state. Reopen only consuming scope, bind the successor/current stage-body locator to the new native/readback refs, rerun the required R-I professional/readback review, and emit successor/revalidation evidence before the new bounded professional claim is treated as Current.

Authority binding remains owned by R-A. A professional stage/receipt may resolve the consumed authority snapshot/fingerprint through its runtime instance, baseline/source revision and typed handoff rather than duplicating a central authority ledger inside the professional schema. A later authority-fingerprint mismatch stops direct Current reuse and revalidates only the affected consumers; it does not justify mutating the historical stage receipt to add or change authority fields.

If owner-native identity analysis shows only a path/location/representation move with no material professional relation change, the prior professional evidence may remain valid after pointer/readback refresh; supersession does not force whole-process invalidation by itself.

`NEW STAGE CYCLE / NATIVE REVISION ≠ OLD PROFESSIONAL RECEIPT REWRITTEN`.

`SUPERSEDED PROFESSIONAL EVIDENCE ≠ FALSE EVIDENCE`.

`HISTORICAL PROFESSIONAL RECEIPT ≠ CURRENT PROFESSIONAL CLAIM BY DEFAULT`.

---

## 10｜Domain state, Current-use binding, closure and verdict separation

Professional state is domain-owned. The shared R-E carrier therefore does **not** define one universal `NOT_STARTED → READY → IN_PROGRESS → CLOSED` professional progress sequence.

Instead it keeps four different facts separate:

```text
domain_state                = owner-native string / domain semantics
current_use_state           = CURRENT / STALE / SUPERSEDED
exit_condition_state        = NOT_EVALUATED / OPEN / SATISFIED / BLOCKED
professional/review verdict = NOT_RUN / N_A / PASS / REVISE / REJECT / HOLD
```

Generic professional stage/process verdict vocabulary:

```text
NOT_RUN
N_A
PASS
REVISE
REJECT
HOLD
```

`current_use_state` reuses the existing R-A Current/Supersession boundary; it is not a new lifecycle authority. `CURRENT` means only that this specific instance is the selected consumable R-E record for the bounded baseline. `SUPERSEDED` preserves history and must not compile as the active Master summary. `STALE` blocks direct Current consequential reuse at the affected scope.

For a process-level `CURRENT + SATISFIED + PASS` compilation, at least one supporting stage must itself be `CURRENT + SATISFIED + PASS`. A `SUPERSEDED` PASS stage remains historical evidence and cannot by itself support the Current process PASS.

`exit_condition_state=SATISFIED` means the bounded stage exit contract is satisfied for that cycle; it does **not** mean `PASS`. A domain-authentic terminal `REJECT` remains legal when backed by actual readback/review evidence. Conversely, `SATISFIED + NOT_RUN` and `SATISFIED + HOLD` are structurally contradictory and fail closed.

`CURRENT USE ≠ EXIT SATISFIED ≠ PROFESSIONAL PASS ≠ DESIGN KEEP`.

---

## 11｜Interface-state compilation

The process instance may reference interface IDs and current interface facts, but the canonical owner of interface semantics remains `cross-disciplinary-design-integration-v1.0.md`.

Existing vocabularies are reused without duplication:

```text
Maturity:
IDENTIFIED / DEFINED / COORDINATED / EXERCISED / VERIFIED

Disposition:
OPEN / BLOCKED / CLOSED / OUTSIDE_CLAIM

Coupling:
INFORMATIVE / DEPENDENT / RECIPROCAL / TIGHTLY_COUPLED

Criticality:
ROUTINE / MATERIAL / MAJOR / CRITICAL
```

A stage may close with an `OPEN` interface only when:

1. the interface's current required maturity for this stage/claim has been met;
2. the remaining work belongs to a later or explicitly outside claim;
3. no unresolved controlling-authority conflict exists;
4. the open item is explicit in the stage/process receipt;
5. the professional claim is not widened beyond the evidence.

An in-claim `MAJOR / CRITICAL` interface below required maturity prevents closure of the dependent professional claim.

The process definition may express `interface_maturity_policy`, but the actual maturity requirement remains a property of each referenced interface / stage binding / Acceptance Contract. The process instance must not become a second interface-state truth source.

---

## 12｜Native artifact and source-of-truth rule

Every stage that changes a design decision must identify its native or authoritative artifact rather than rely on a report-only description.

Examples may include:

- CAD / BIM / native 3D geometry;
- plans / sections / elevations;
- schedules / room data / equipment schedules;
- calculations / simulation models;
- editable diagrams / state models / service blueprints;
- native UI/prototype source;
- structured data / interface registers;
- physical mockup or test records where relevant.

Presentation imagery, screenshots and renders may support readback, but they do not silently replace the native source of truth.

Native-artifact identity follows the v2.1 File & Artifact Management invariant: filename, timestamp, preview or package location is not semantic identity. A retained authority-bearing artifact should remain traceable through stable logical identity, Current revision, representation role, parent/derivation relation, producer owner, readback and persistence/sync state where triggered.

### 12.1｜Choosing the authoritative carrier

The stage definition should select the carrier from the professional claim that must remain editable/checkable, not from presentation convenience. Where several carriers coexist, distinguish their roles, for example:

- calculation/model = governing engineering analysis source;
- BIM/CAD/native geometry = governing spatial/geometry source;
- schedule/database = governing structured parameter/equipment/room source;
- specification = governing textual performance/material requirement source;
- test/commissioning record = governing observed performance evidence;
- issue drawing/PDF = controlled communication/contract representation where that role is owner-authorized.

Do not force one file to own every truth. The process may have several authoritative carriers for different variables, provided controlling authority and interface handoffs are explicit.

### 12.2｜Implementation-readback chain

For any professional claim that depends on an executed design change, preserve:

`INTENDED PROFESSIONAL DECISION → AUTHORIZED NATIVE MUTATION → CURRENT ARTIFACT IDENTITY/REVISION → ACTUAL READBACK → PROFESSIONAL FINDING`.

The stage body/instance stores locators to the native/readback evidence. It does not turn the prose record into a substitute source. When R-I reviews a material stage, the referenced native/readback identity must still match the Current relation under review.

### 12.3｜Failure and fallback

Return `REVISE / HOLD` or the existing runtime failure route when the authoritative source is missing, write authority is unresolved, only a derivative/screenshot can be located, required units/coordinate system/version cannot be resolved, a round-trip changes material semantics, or a new revision invalidates the reviewed relation.

A derivative may remain useful evidence at a bounded claim ceiling. It cannot silently become the new native authority merely because the original tool is unavailable.

`NATIVE FILE EXISTS ≠ NATIVE AUTHORITY RESOLVED`.

`SCREENSHOT MATCHES INTENT ≠ PROFESSIONAL IMPLEMENTATION VERIFIED`.

---

## 13｜Skill / capability binding

Professional stages are many-to-many with Skills and tools.

Example:

```text
Architecture ADD-07
├─ current knowledge resolution
├─ task/claim operational knowledge mount
├─ CAD / plan execution
├─ 3D spatial readback
├─ area / data checks
├─ accessibility-aware review
├─ circulation review
└─ independent design review
```

The Current Default Skill Resolver determines the minimum sufficient owner set from the live registry and actual callable execution surfaces.

Do not create one Skill because one professional stage exists. Do not hardcode a global Skill list inside a professional-process definition.

### 13.1｜Required-output-first routing

Resolve capability in this order:

`professional question → required native output/readback → required capability → eligible execution owner/Skill → callable tool/adapter → execution plan`.

Do not reverse the order to `available software → whatever output it can make → reinterpret as professional evidence`.

The process definition may state `required_capabilities[]`, `tool_adapter_requirements[]`, `typed_handoff_contracts[]` and execution-owner requirements, but the live Resolver decides the minimum sufficient callable owner set at runtime. Registry existence is not callability evidence.

### 13.2｜Fallback and specialist boundary

Fallback execution is permitted only when the substitute route preserves the domain-native source-of-truth, required precision/semantics, interface obligations and readback. If it cannot, use the existing capability gap/HOLD route and preserve the unresolved professional claim.

A general design Skill may help construct/inspect a professional artifact, but it does not inherit licensed/statutory/specialist authority. Conversely, a specialist calculation/tool result does not acquire Design KEEP authority by being technically sophisticated.

### 13.3｜Reopen triggers

Re-resolve the capability route when required output type/format changes, source authority moves to a different native carrier, the selected Skill/tool becomes unavailable or non-callable, an adapter changes semantics/precision, a controlling interface changes exchange requirements, or readback proves that the chosen route cannot support the claimed professional decision.

`SKILL INSTALLED ≠ SKILL SUFFICIENT FOR THIS CLAIM`.

`TOOL EXECUTED ≠ PROFESSIONAL RESULT ACCEPTED`.

---

## 14｜Assurance and independence

Where independence is required, producer self-check cannot satisfy independent review.

The process definition must state:

- which checks may be deterministic / producer-side;
- which checks require a distinct professional reviewer;
- which checks require an Integration readback;
- which checks require technical / evidence / statutory / field authority outside the process.

Professional review must state its `does_not_prove` boundary.

### 14.1｜Assurance classes remain separate

For each stage, distinguish at least the applicable assurance classes:

1. **deterministic / producer QA** — schema, units, references, arithmetic, model/drawing consistency, automated rule checks or other encoded tests;
2. **professional self-review** — producer/domain-team judgment within assigned competence;
3. **independent professional review** — a reviewer with the required independence and competence for the consequential professional claim;
4. **Integration readback** — cross-domain shared-variable/interface acceptance owned by the Integration contract;
5. **technical/evidence/statutory/field authority** — specialist or external authority whose claim cannot be manufactured by the professional process.

Passing one class never substitutes for a triggered class in another column.

### 14.2｜Independence evidence

Where independent review is required, the review must bind the exact artifact/revision or owner-native immutable identity actually reviewed, the reviewer identity, the required independence/competence basis available under the owner contract, the bounded verdict/claim and the `does_not_prove` boundary. A different chat, worker, tool, export surface or producer-side second pass is not independence by itself.

If the reviewed native artifact changes materially after the review, the affected independent review becomes stale for the new use even though the historical review remains valid evidence of what was reviewed then.

### 14.3｜Decision boundary

Machines may verify that required review records/identity/bindings are present and current. They may not invent reviewer competence, independence, licensed authority or a professional verdict. A project authority may decide project progression within its scope but cannot convert an unresolved professional/statutory claim into PASS.

Examples:

```text
ARCHITECTURE DEVELOPMENT PASS ≠ FIRE PASS
ARCHITECTURE DEVELOPMENT PASS ≠ ACCESSIBILITY CERTIFICATION
STRUCTURAL COORDINATION ≠ STRUCTURAL ENGINEERING APPROVAL
MEP SPACE RESERVE ≠ COMMISSIONED SYSTEM PERFORMANCE
INTERIOR DESIGN KEEP ≠ FIRE / ACCESSIBILITY COMPLIANCE
LANDSCAPE DESIGN KEEP ≠ DRAINAGE / CIVIL APPROVAL
```

`PRODUCER SELF-CHECK ≠ INDEPENDENT REVIEW`.

`INDEPENDENT REVIEW PASS ≠ STATUTORY APPROVAL`.

---

## 15｜Change propagation and stale scope

After any accepted material change:

```text
changed professional decision / shared variable
→ consuming stage instances
→ task/claim knowledge mounts when applicability/freshness changes
→ active interfaces
→ native artifacts
→ professional reviews
→ integration readbacks
→ affected receipts
→ promotion dependency
```

Only affected scope becomes stale. Do not invalidate an entire profession merely because one local interface changed, unless dependency analysis shows whole-process consequence.

Likewise, a local valid result must not remain falsely current when a controlling shared variable, mounted source applicability, source version or other governing input changed upstream.

For a superseding body/native/readback relation, reuse the existing `STALE / SUPERSEDED`, reopen-event, receipt-stale and R-I readback mechanisms. Do not introduce a domain-specific version database or second Current registry. Historical receipts remain immutable under their original contract/authority binding; current consumption changes through successor/revalidation evidence rather than in-place history edits.

### 15.1｜Material-change classification

Treat a change as material to a stage when it changes at least one consumed professional relation, including:

- Current authority / source authority / governing code-standard basis;
- task-scoped knowledge applicability or eligibility;
- professional question, criterion, assumption or claim ceiling;
- controlled geometry, load, duty, quantity, performance target, operational state or specification;
- shared variable/interface maturity or controlling authority;
- native source identity/semantics;
- evidence/readback method or acceptance criterion;
- reviewer/assurance condition required for the claim.

Pure storage movement, filename cleanup or representation regeneration may be non-material when stable identity and semantic/readback equivalence are proven. Recency or small file diff does not decide materiality.

### 15.2｜Propagation algorithm

Use the smallest truthful propagation:

`changed relation → identify direct stage/interface consumers → mark only affected current use stale/open → preserve unrelated verified evidence → re-resolve authority/knowledge/interface as required → re-execute affected native work → actual readback → rerun affected assurance → issue successor/revalidation receipt`.

Upstream reopen is required when a downstream failure reveals that the controlling assumption/decision is wrong, not merely because downstream work changed. Downstream reopen is required whenever a changed upstream relation was actually consumed.

### 15.3｜Historical evidence and Current use

Do not rewrite a historical stage/process receipt to show today's status. Keep the original execution/review truth; change whether it is eligible for Current consequential use through stale/supersession/revalidation evidence under the existing v2.1 authority boundary.

`SMALL DIFF ≠ NON-MATERIAL CHANGE`.

`SUPERSEDED RECEIPT ≠ FALSE HISTORY`.

`CHANGE DETECTED ≠ WHOLE PROCESS RESET`.

---

## 16｜Completion and Master compilation

The detailed process instance closes according to the domain definition. It then compiles a compact orchestration summary into the existing Master Runtime:

```text
professional_processes[]
├─ domain
├─ process_id
├─ triggered
├─ receipt_id
├─ state
├─ verdict
└─ claim_ceiling
```

Compilation rule:

```text
DOMAIN_PROCESS_INSTANCE.current_use_state + process_exit_condition_state + selected-current-instance existence
→ Master professional_processes[].state projection

DOMAIN_PROCESS_INSTANCE.professional_verdict
→ Master professional_processes[].verdict

current professional receipt ref
→ Master professional_processes[].receipt_id
```

The Master summary is intentionally thin. It is not the source of stage semantics. The Master `state` vocabulary remains exactly `NOT_REQUIRED / CURRENT / STALE / MISSING / BLOCKED`: it is compiled from current-use/existence/blockage facts, never by copying a domain state string.

A process with `process_exit_condition_state=SATISFIED` must have at least one stage instance and a professional receipt. `current_use_state=CURRENT + process_exit_condition_state=SATISFIED + professional_verdict=PASS` cannot compile promotion-relevant PASS without the current professional receipt required by the Master. This closure evidence rule is structural only; the machine still does not award the professional verdict.

No additional Master fields are required merely because this contract exists.

### 16.1｜Stage closure versus process closure

A stage may reach `exit_condition_state=SATISFIED` with `PASS / REVISE / REJECT` when its domain-authentic exit conditions are actually satisfied and the corresponding outputs/reviews/readbacks exist. `SATISFIED` means the bounded stage exit contract has reached a terminal disposition for that cycle; it does not mean the verdict is PASS.

The process reaches `process_exit_condition_state=SATISFIED` only when the process-level exit contract is met, required in-claim stage/interface/assurance dependencies have terminal dispositions consistent with the process claim, allowed open items are explicitly bounded, and a current professional receipt exists. A terminal `REJECT` remains legal where the domain has evidence to discontinue the candidate/route.

### 16.2｜Compilation rules

Compilation into Master Runtime is loss-minimizing, not semantics-moving. The Master consumes only the current summary fields needed for orchestration; detailed stage questions, body records, interface bindings, native outputs, evidence and assurance stay with the Professional Domain owner.

Before compiling a promotion-relevant professional PASS, confirm structurally:

- process definition/version is Current for the claimed use;
- process/stage Current baseline is resolvable;
- at least one materially executed stage exists;
- consequential knowledge mounts are present where required;
- required native outputs and actual readbacks are present for in-claim stages whose exit condition is `SATISFIED`;
- required review/independence records are present;
- under project-instance schema v1.1, each PASS stage carries an exact reviewer + reviewed native-artifact identity + revision/hash binding, and a `SUPERSEDED` PASS stage is not the sole support for a Current process PASS;
- under project-instance schema v1.1, the process and every satisfied in-claim stage report zero unresolved in-claim blocking open items;
- critical in-claim interface requirements are not hidden by the summary;
- professional receipt ref is current for the claim;
- `does_not_prove` / claim ceiling remains visible.

The machine may reject a structurally incomplete compilation. It may not manufacture professional PASS from structural completeness.

### 16.3｜Post-closure reopen

Process closure is not permanent validity. A material authority/source/interface/native/readback change may reopen only the affected stage/process scope. Preserve the former closed receipt as history and issue successor/revalidation evidence rather than editing the old record in place.

`EXIT SATISFIED ≠ PASS`.

`PROFESSIONAL PASS ≠ PROJECT PROMOTION`.

`MASTER SUMMARY ≠ PROFESSIONAL SOURCE OF TRUTH`.

---

## 17｜Machine-verifiable vs professional judgment

Machine validation may verify:

- schema structure;
- required references;
- stage identity uniqueness within an instance;
- baseline / cycle fields;
- non-empty stage input / native-output / readback / exit / reopen requirements;
- Knowledge Operational Mount refs are present when the stage declares consequential mounted knowledge is required;
- interface reference presence without re-awarding interface maturity;
- per-interface maturity consistency, including `required_maturity_to_close >= required_maturity_to_enter` under the existing maturity order;
- non-empty shared-variable bindings for declared interfaces;
- stale/open/reopen fields;
- receipt linkage;
- state/verdict compatibility;
- closure evidence presence (`outputs / review refs / actual readback / receipt refs` as applicable), including review evidence for a stage `PASS`;
- at least one stage `PASS` behind a process-level `current_use_state=CURRENT + process_exit_condition_state=SATISFIED + PASS` claim;
- claim-ceiling field presence;
- non-empty `does_not_prove` boundaries;
- no duplicate process-instance identity where the carrier requires uniqueness.

Machine validation must not infer:

- `KI4 VERIFIED` or `OE3 ELIGIBLE`;
- professional excellence;
- architectural quality;
- engineering adequacy;
- statutory compliance;
- field validity;
- Design KEEP;
- DQ3–DQ5;
- interface maturity;
- Promotion.

---

## 18｜Implementation requirements for a new domain process

Before a new professional-domain process is treated as Current, verify:

1. authentic professional semantics have been researched rather than copied from Architecture ADD;
2. scope and claim ceiling are explicit;
3. stage questions / entry / exit / reopen conditions exist;
4. consequential knowledge routes through the Current Knowledge Integrity & Operational Mount contract, with task/claim applicability, freshness, claim ceiling and `does_not_prove` preserved by mount refs;
5. shared DD responsibilities are mapped without renaming stages;
6. cross-domain interfaces use the existing Integration owner and vocabulary;
7. interface maturity is owned per interface / Acceptance Contract rather than duplicated as a profession-wide enter/close scalar;
8. required native outputs precede Skill/Tool selection;
9. Current Skill Resolver / live registry is used rather than a hardcoded inventory;
10. actual readback and independent review requirements are explicit;
11. human-experience / design-language / technical / content-projection consequences are present as explicit stage fields even when the domain records a bounded N/A reason;
12. process receipt and non-empty `does_not_prove` boundary exist;
13. project instances do not create a parallel knowledge taxonomy;
14. process instance exposes a professional verdict separately from execution state;
15. Master Runtime receives only the compact summary required for orchestration.
16. a material stage has a domain-native body/title contract before professional closure;
17. the body points to canonical knowledge mounts rather than copying reusable Knowledge bodies;
18. the body points to the required native source and actual readback rather than replacing either with prose;
19. machine completeness checks do not auto-award professional judgment, Design KEEP or Promotion.
20. every material stage passes the §D.1 professional decision-content floor: it contains real domain criteria, controlling assumptions, professional consequences and an observable decision threshold rather than only verbs such as coordinate/review/ensure;
21. at least one representative high-consequence stage demonstrates the complete chain `criterion → professional development action → native carrier → actual readback → bounded verdict → handoff → reopen trigger` before the process is claimed operationally usable;
22. quantitative stage criteria bind values/ranges to source, unit, applicability and tolerance/acceptance method instead of embedding unexplained generic numbers or leaving “meets standard” as the only criterion;
23. material cross-domain handoffs state the controlled variable/decision, Current source, value/range/geometry locator where measurable, assumptions/tolerances, recipient, required interface maturity and reopen rule rather than only naming the neighboring discipline;
24. a new domain process includes explicit hard-fail/mandatory-revise examples drawn from authentic domain failure modes so a professional reviewer can distinguish incomplete documentation from a materially wrong professional decision.

---

## 19｜Canonical invariants

```text
ONE MASTER RUNTIME
ONE EXISTING KNOWLEDGE ARCHITECTURE
CONSEQUENTIAL KNOWLEDGE → TASK/CLAIM OPERATIONAL MOUNT BEFORE PROFESSIONAL DECISION
AUTHENTIC DOMAIN PROCESS SEMANTICS
SHARED CONTRACT ENVELOPE
INTERFACE MATURITY OWNED PER INTERFACE, NOT BY STAGE-NUMBER MATCHING OR PROCESS-WIDE SCALAR
NATIVE OUTPUT BEFORE TOOL SELECTION
ACTUAL READBACK BEFORE PROFESSIONAL CLOSURE
INDEPENDENT REVIEW WHERE REQUIRED
EXIT SATISFIED ≠ PASS
TERMINAL REJECT REMAINS LEGAL WHEN DOMAIN-AUTHENTIC AND EVIDENCED
NO LOSS / NO COMPRESSION
NO AUTOMATIC DESIGN OR PROMOTION INFERENCE
```

---

## 20｜G9 / Knowledge Return boundary

Professional execution may produce observations, failures, successful repairs, retest results and counterexamples that are useful beyond the current stage. Those outputs remain project/professional evidence until the existing `R-K G9 / Knowledge Return` path creates a bounded candidate and routes it to the correct owner.

Keep the routes independent:

```text
PROJECT / PROFESSIONAL OBSERVATION
→ project reopen when the affected project conclusion must change
→ reusable Knowledge candidate when transfer is plausible
→ Evolution candidate when a runtime/process behavior is the proposed target
```

The professional process may state a causal hypothesis and transfer boundary, but neither stage `PASS` nor repeated successful use proves a universal professional rule. G9 candidate intake cannot award `CURRENT` Knowledge, `KI4`, `OE3`, professional-process revision or direct runtime mutation. `R-K → R-B` remains a bounded feedback edge rather than a dependency handoff.

A project may reopen immediately when current evidence requires correction; it does not wait for reusable Knowledge promotion. Conversely, project reopen does not prove that the reusable professional method or Knowledge object should be revised.

`PROFESSIONAL STAGE PASS ≠ REUSABLE KNOWLEDGE`.

`PROJECT REOPEN ≠ KNOWLEDGE PROMOTION`.

`G9 CANDIDATE ≠ KI4 ≠ OE3`.
