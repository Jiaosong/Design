# OLEANDER Professional Domain Process Contract v1.0

**Status:** CURRENT GOVERNANCE CONTRACT
**Authority position:** subordinate to `complex-project-master-runtime-v1.0.md` and the Current OLEANDER Authority / Knowledge Architecture.
**Purpose:** define the reusable envelope that every authentic professional-domain design/development process must satisfy without replacing that profession's own semantics.
**Applies to:** Architecture, Structural Engineering, Building Services / MEP, Interior Design, Landscape Architecture, Lighting Design, Digital Product / HCD, Systems Engineering and any other materially triggered professional domain.

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

### 3.1 Process Definition｜知识 / 方法层

A reusable domain-process definition states how a profession develops and validates work in a bounded scope.

Example:

```text
Architecture Design Development Process v1.0
ADD-00 ... ADD-17
```

The definition belongs in the existing Knowledge Plane as a METHOD / process definition or equivalent current carrier. It does not create a new Knowledge level.

### 3.2 Domain Process Instance｜项目层

A project activates a process definition as a project-specific instance.

Example:

```text
KH_LY46
→ Architecture Design Development Process v1.0
→ project-specific Architecture process instance
```

The instance records project identity, baseline, current stages, active interfaces, professional verdict, open items, receipts and claim ceiling. It is not reusable knowledge merely because it exists.

### 3.3 Domain Stage Instance｜运行层

A process stage may execute repeatedly across cycles and baselines.

Example:

```text
Architecture ADD-07 definition
→ KH_LY46 ADD-07 instance
→ cycle N / baseline Rxx / task-claim knowledge mounts / active interface refs / current readback / reopen state
```

Stage instances record runtime execution state. They do not become new canonical Knowledge Objects by default.

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
entry_conditions[]
required_inputs[]
knowledge_inputs[]
knowledge_mount_requirement
required_dd_dimensions[]
required_native_outputs[]
interface_requirements[]
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

`does_not_prove[]` is mandatory and non-empty for a Current professional-stage definition. A professional stage may make a bounded claim, but it may not leave its authority ceiling implicit.

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

The professional process **references** interface state. It does not redefine Cross-Disciplinary Integration maturity, disposition, coupling, criticality or Acceptance Contract semantics.

There is deliberately **no process-level numeric/scalar enter/close maturity truth** in the Current machine contract. Actual enter/close maturity is owned per interface binding / Acceptance Contract by Cross-Disciplinary Integration. `interface_maturity_policy` may only state the rule for resolving those per-interface requirements; it cannot override them with a profession-wide scalar.

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

---

## 6｜Stage binding to content, presentation and projection

Professional design decisions often fail because a correct underlying decision is projected through an incomplete or misleading artifact. Therefore each stage may declare projection requirements using the shared Design Quality specification.

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
execution_state
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

`professional_verdict` is the bounded professional judgment that compiles to the Master Runtime's existing `professional_processes[].verdict`. `execution_state` and `professional_verdict` are independent fields.

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
execution_state
review_verdict
claim_ceiling
inputs[]
outputs[]
consequential_knowledge_mount_required
knowledge_mount_refs[]
interface_refs[]
evidence_refs[]
review_refs[]
open_items[]
stale_scope[]
reopen_events[]
exit_condition_state
actual_readback_refs[]
last_updated
```

`knowledge_mount_refs[]` point to the Current task/claim-scoped mount records governed by `knowledge-integrity-and-operational-mount-v1.0.md`. The stage instance does not reissue KI/OE judgments.

The stage instance is a runtime carrier, not a Knowledge level and not an automatic separate page/file.

One process stage may have multiple cycles. A new cycle does not erase prior valid evidence; prior cycle evidence becomes superseded/stale only at the affected scope.

---

## 9A｜Decision-object / claim / output execution granularity

A professional **stage is a responsibility and professional-context container, not the smallest execution unit**. Material execution must be resolvable below stage level without inventing a second professional taxonomy.

Canonical runtime join:

```text
DOMAIN PROCESS INSTANCE
→ DOMAIN STAGE INSTANCE
→ DECISION OBJECT
→ CLAIM
→ TASK/CLAIM KNOWLEDGE MOUNT
→ REQUIRED NATIVE OUTPUT
→ REQUIRED CAPABILITY ROLES
→ MINIMUM SUFFICIENT SKILL / EXECUTION OWNER SET
→ TOOL / ADAPTER ROUTE WHEN REQUIRED
→ NATIVE ARTIFACT
→ ACTUAL READBACK
→ PROFESSIONAL / INTEGRATION / DESIGN / EVIDENCE FINDING
```

The join uses existing OLEANDER objects and owners:

- **Decision Object** is the smallest materially independent design/system object being decided or changed. It is the primary horizontal join key across R-C / R-D / R-E / R-F / R-G / R-H / R-I when that precision is required.
- **Claim** states what the current decision/output is allowed to prove. Claims may be narrower than the stage claim ceiling.
- **Knowledge Mount** remains owned by R-B and is bound to the task/claim, not to a Skill name or tool.
- **Required Native Output** is the bridge from professional semantics into execution. Knowledge does not route directly to a Skill.
- **Required Capability Roles** describe what executable ability the output needs. They are runtime requirements, not a new knowledge taxonomy and not a fixed one-capability/one-Skill mapping.
- **Skill / Execution Owner Set** is resolved dynamically by the Current Skill Resolver as the minimum sufficient owner set.
- **Tool / Adapter** is selected only after capability resolution and runtime availability. A professional stage must not hardcode vendor/software inventory.
- **Artifact + Actual Readback** prove what was actually produced/observed; execution success does not prove professional validity.

For prospective material stage instances, use `granularity_binding_state = DECISION_OBJECT_BOUND` and record:

```text
decision_object_refs[]
claim_refs[]
output_execution_bindings[]:
  binding_id
  decision_object_ref
  claim_refs[]
  knowledge_mount_refs[]
  output_requirement_ref
  required_native_output
  required_capability_roles[]
  tool_adapter_required
  owner_set_ref
  adapter_route_ref
  artifact_refs[]
  readback_refs[]
  resolution_state
  stale_if[]
  does_not_prove[]
```

`LEGACY_STAGE_ONLY` remains valid for historical/provenance instances and bounded stage-level records. It must not be silently treated as decision-object/claim-level execution evidence when a new claim requires the finer binding.

### Granularity invariants

```text
STAGE ≠ EXECUTION UNIT
KNOWLEDGE ROLE ≠ EXECUTION GRANULARITY
KNOWLEDGE MOUNT ≠ SKILL ROUTE
REQUIRED OUTPUT PRECEDES CAPABILITY RESOLUTION
CAPABILITY ≠ SKILL
SKILL ≠ TOOL
TOOL ROUTE ≠ PROFESSIONAL PASS
ARTIFACT EXISTS ≠ ACTUAL READBACK
ACTUAL READBACK ≠ DESIGN KEEP
```

Shared DD responsibilities and Cross-Disciplinary Interfaces remain **overlays bound to the same decision object / claim**; they are not inserted as extra universal stages.

Change propagation follows the smallest materially affected scope:

```text
changed authority / shared variable / artifact
→ affected decision object(s)
→ affected claim(s)
→ affected knowledge/output/interface bindings
→ affected readback/review
→ widen reopen only when dependency analysis requires it
```

This section refines execution granularity only. It creates no new Runtime Layer, Knowledge level, Primary Role, professional stage namespace, Capability taxonomy, Skill family or Tool family.

---

## 10｜State and verdict separation

Runtime state and professional judgment remain separate.

Recommended shared runtime state vocabulary for the generic instance carrier:

```text
NOT_STARTED
READY
IN_PROGRESS
BLOCKED
CURRENT
STALE
CLOSED
SUPERSEDED
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

Domains may have richer internal states, but the compiled Master summary must remain compatible with its existing `state / verdict / claim_ceiling` envelope.

`CURRENT` describes runtime currency. `PASS` describes a bounded professional verdict. Neither is Design KEEP.

`CLOSED` means the represented execution cycle is terminal at its declared claim ceiling; it does **not** mean `PASS`. A domain-authentic terminal `REJECT` remains legal when it is backed by actual readback/review evidence. Generic machine validation must not outlaw legitimate domain terminal semantics merely to simplify orchestration. Conversely, `CLOSED + NOT_RUN` and `CLOSED + HOLD` are structurally contradictory and fail closed.

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

---

## 14｜Assurance and independence

Where independence is required, producer self-check cannot satisfy independent review.

The process definition must state:

- which checks may be deterministic / producer-side;
- which checks require a distinct professional reviewer;
- which checks require an Integration readback;
- which checks require technical / evidence / statutory / field authority outside the process.

Professional review must state its `does_not_prove` boundary.

Examples:

```text
ARCHITECTURE DEVELOPMENT PASS ≠ FIRE PASS
ARCHITECTURE DEVELOPMENT PASS ≠ ACCESSIBILITY CERTIFICATION
STRUCTURAL COORDINATION ≠ STRUCTURAL ENGINEERING APPROVAL
MEP SPACE RESERVE ≠ COMMISSIONED SYSTEM PERFORMANCE
INTERIOR DESIGN KEEP ≠ FIRE / ACCESSIBILITY COMPLIANCE
LANDSCAPE DESIGN KEEP ≠ DRAINAGE / CIVIL APPROVAL
```

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
DOMAIN_PROCESS_INSTANCE.execution_state
→ Master professional_processes[].state mapping

DOMAIN_PROCESS_INSTANCE.professional_verdict
→ Master professional_processes[].verdict

current professional receipt ref
→ Master professional_processes[].receipt_id
```

The Master summary is intentionally thin. It is not the source of stage semantics.

A `CLOSED` process instance must have at least one stage instance and a professional receipt. A `CURRENT/CLOSED + PASS` process cannot compile promotion-relevant PASS without the current professional receipt required by the Master. This closure evidence rule is structural only; the machine still does not award the professional verdict.

No additional Master fields are required merely because this contract exists.

---

## 17｜Machine-verifiable vs professional judgment

Machine validation may verify:

- schema structure;
- required references;
- stage identity uniqueness within an instance;
- baseline / cycle fields;
- Knowledge Operational Mount refs are present when the stage declares consequential mounted knowledge is required;
- interface reference presence without re-awarding interface maturity;
- stale/open/reopen fields;
- receipt linkage;
- state/verdict compatibility;
- closure evidence presence (`outputs / review refs / actual readback / receipt refs` as applicable);
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
CLOSED ≠ PASS
TERMINAL REJECT REMAINS LEGAL WHEN DOMAIN-AUTHENTIC AND EVIDENCED
NO LOSS / NO COMPRESSION
NO AUTOMATIC DESIGN OR PROMOTION INFERENCE
```
