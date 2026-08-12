# OLEANDER Modeling Contract｜v0.2

**Spec Patch:** `v0.2.1`  
**Status:** `REVIEW`  
**Parent:** `OLEANDER Canonical Project Flow｜v0.3`  
**Primary:** `B04｜Metrics & Governance`  
**Supporting:** `IP03 / SP04`

> v0.2.1 is a non-breaking validation/governance patch. The contract payload remains `contract_version: v0.2`. M0–M10 and the modeling method are unchanged.

## Canonical modeling sequence

`Decision Question → Hard Points / Proportion Skeleton → Envelope → Section Network → Primary Geometry / Surface → Construction & Surface QA → Component Architecture → Secondary Geometry → Detail / Instances → Material Binding → Multi-Scale QA → Candidate Authority`

## M0–M10

- M0｜Decision Question
- M1｜Hard Points & Proportion Skeleton
- M2｜Envelope / Package
- M3｜Section Network
- M4｜Primary Geometry / Primary Surface
- M5｜Construction & Surface QA
- M6｜Component Architecture
- M7｜Secondary Geometry
- M8｜Detail / Repetition / Instances
- M9｜Material / CMF Binding
- M10｜Multi-Scale Modeling QA

F0 usually covers M0–M3; F1 focuses M4–M6; F2 covers stable M7–M8 plus refined M5/M10; F3 adds material/presentation outputs without changing design authority.

**F1 does not mean a highly detailed model. It means primary geometric relationships are reliable.**

## Modeling-quality QA

Integrity QA covers file/runtime/dimensions/transforms/normals/manifold/export validity.

Construction QA covers SubD topology/pinching, NURBS patch/continuity, CAD feature/datum stability, BIM host/grid/type logic, dependency/instance structure, section traceability and rebuild stability.

Design Geometry QA covers silhouette, proportion, stance, hierarchy, curvature tension, junction logic, component relations, detail density and interaction/use clearances.

Project QA checks the Decision Question, locked variables, dependent zones, exit condition and project intent.

`Manifold PASS ≠ Surface Quality PASS`.

Diagnostics where relevant:
`CLAY_BROAD / CLAY_STRIP / CLAY_GRAZING / SIDE_SILHOUETTE / SECTION_OVERLAY / ZEBRA / CURVATURE / WIREFRAME`.

## Progressive Lock

`OPEN / LOCKED / DEPENDENCY_LOCKED / CONDITIONALLY_UNLOCKABLE / FROZEN`

Dependent relations may reopen through:
`Revision Request → Impact Analysis → Affected Components / Sections / Views → Unlock Decision → Selective Rebuild`.

## Semantic dependency

Use semantic component IDs and assemblies instead of canonical object-name wildcards.

Preferred:
`COMP-WHEEL-SPOKE → ASY-WHEEL → INST-WHEEL-FL/FR/RL/RR`

Legacy evidence:
`*_SPOKE_* → 40 independent mesh targets`

R01 remains valid historical evidence for selective execution; v0.2 changes the source-model architecture and dependency semantics.

## Source / Derived / Export

Every model distinguishes `Editable Source / Derived Model / Export`. Derived/render/export geometry never silently replaces editable-source authority.

## Selective execution

`Revision Contract → Dependency Resolve → Impact Graph → Changed Source Nodes → Derived Components → Affected Views → Selective Rebuild → Selective Render → QA`

Artifact cache key:
`Source Authority Hash + Normalized Contract + Worker Version + Runtime + Dependency Graph Version`.

Cache scope must be explicit: `JOB_LOCAL / PROJECT_LOCAL / PERSISTENT_CROSS_RUN`.

## Worker autonomy boundary

Workers may auto-repair deterministic technical faults. They must not autonomously optimize design variables. Design issues return a `REVISION_PROPOSAL` for design reasoning/human decision.

## v0.2.1 validation fix

The initial v0.2 validator could produce false-positive PASS results. For example, `<REQUIRED...>` placeholders and `applicable=true` blocks with no actual items could pass.

Canonical validation now has two modes:

- `template` — structural/template validation only;
- `strict` — required before Worker execution or promotion.

Strict validation additionally checks:
- placeholders are not accepted as real values;
- applicable Hard Points / Envelopes / Sections contain actual items;
- non-applicable blocks have a real reason;
- Authority other than `NONE` has an editable source;
- M4+ has Primary Geometry;
- M6+ has Semantic Components;
- M9+ has Material Bindings;
- semantic IDs are globally unique;
- Section / Primary Geometry / Component / Dependency references resolve;
- component parents exist;
- Material Binding targets resolve;
- all four QA groups contain actual checks;
- enabled cache has key inputs;
- Promotion-only persistence uses Artifact Registry;
- Workers cannot mutate Source Authority.

The validator executes the JSON Schema first, then OLEANDER semantic validation.

A blank Template is therefore expected to be:
`TEMPLATE MODE = PASS / STRICT MODE = FAIL`.

## Authority and persistence

Authority remains progressive:
`NONE → WORKING_SOURCE → CANDIDATE_AUTHORITY → CANONICAL_AUTHORITY → FROZEN_AUTHORITY`.

An asset can be `EXECUTION BENCHMARK PASS` while still `MODELING QUALITY REVISE`.

Promotion-only persistence remains mandatory:
- Exploration → temp/local
- Candidate → receipt/review evidence
- Promoted → Artifact Registry → Notion / GitHub / Google Drive

## Review boundary

`contract_version=v0.2` remains REVIEW. Before a higher canonical promotion it must be applied to the automotive model from F0→F1 and to at least one second geometry family.