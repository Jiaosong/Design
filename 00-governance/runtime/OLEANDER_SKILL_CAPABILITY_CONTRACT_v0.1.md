# OLEANDER Skill Capability Contract v0.1

Status: **CANDIDATE_FOR_CURRENT**  
Decision date: **2026-08-18**  
Scope: **GitHub execution owners only**  
Upstream authority: **Notion Current Root Authority + live Registry + `OLEANDER_DEFAULT_SKILL_RESOLVER_v1.1` + `OLEANDER_NOTION_TO_GITHUB_EXECUTION_OWNER_MAP_v1.0`**

## 0｜Purpose

This contract standardizes how every OLEANDER execution owner declares capability. It does not create a new Skill, Notion Domain, METHOD, TOOL or review authority.

A Skill capability declaration must be machine-readable and must not rely only on prose in `SKILL.md`.

Required fields:

`skill_id / lifecycle_state / routing_state / accepts / produces / owns_authority / does_not_own / required_tools / optional_tools / runtime / fallback / gates / handoff_schema / implementation_paths / last_verified / does_not_prove`

## 1｜Lifecycle and routing are separate

Lifecycle values:

`EXPERIMENTAL → CANDIDATE → VALIDATED → INSTALLED → DEPRECATED → LEGACY`

Routing-state values remain compatible with the Current Execution Owner Map:

`INSTALLED_OWNER / CANDIDATE_OWNER / CANDIDATE_BODY / RUNTIME_TOOL_ADAPTER / NO_DEDICATED_OWNER`.

A file existing on `main`, a successful CI run, or repeated project use does not silently advance lifecycle state.

## 2｜Authority declaration

Every execution owner must declare what it owns and what it must not overwrite.

Examples:
- `oleander-research` may own evidence acquisition/synthesis artifacts, but does not own downstream geometry, final design verdict or field truth.
- `oleander-data-viz` may own chart/map encoding, but does not own upstream source values or route/source geometry.
- `oleander-motion` owns temporal behavior, not the underlying static state semantics.
- `oleander-delivery-qc` owns release/export inspection, not Design Review, user validation or design authoring.

## 3｜Accepts / produces

`accepts` and `produces` are typed by Native Artifact Contract rather than free-text filenames.

An owner may consume an artifact in one of four permissions:

`READ_ONLY / DERIVE / MUTATE_PRESENTATION_ONLY / MUTATE_AUTHORIZED_SOURCE`.

Default is `READ_ONLY` unless the upstream handoff explicitly grants more.

## 4｜Tool declaration

`required_tools` are mandatory for the owner to execute its declared native output.  
`optional_tools` are replaceable adapters.  
A tool capability never becomes a hidden execution owner merely because many Skills reuse it.

Shared TOOLs such as `T-VISUAL-IMAGE-OPS-001` provide operators/adapters only and do not own final artifacts.

## 5｜Fallback

Fallback must preserve truth and native-output intent. A fallback may lower implementation fidelity or medium capability, but must declare what is lost.

Forbidden fallback behavior:
- replacing a native geometry requirement with a screenshot;
- replacing interactive behavior with a static mock and calling it runtime PASS;
- replacing field evidence with a render;
- replacing a vector/text master with a raster-only derivative when editability is required.

## 6｜Gates

Every capability declaration references applicable gates, including as relevant:
- Evidence / Source boundary;
- Professional Design Gate;
- runtime/readback gate;
- Native Artifact Contract;
- Execution Regression Contract;
- independent reviewer requirement;
- project-specific gates.

## 7｜Lifecycle promotion requirements

Minimum lifecycle semantics:

- `EXPERIMENTAL`: exploratory implementation; may be discarded.
- `CANDIDATE`: bounded reusable capability exists; promotion evidence incomplete.
- `VALIDATED`: repeated real executions + regression evidence + no blocking governance defect.
- `INSTALLED`: entered the formal installed reusable execution registry and maintained under AIG-01/evals.
- `DEPRECATED`: no new routing unless explicit compatibility need.
- `LEGACY`: provenance only; not a Current execution route.

Promotion must record `from_state / to_state / evidence_refs / reviewer_id / decision_ref / effective_commit`.

## 8｜Dedupe / merge / retire gate

At any capability change, check:
1. another owner already owns the same native output and authority;
2. the new implementation is only a parameterized recipe under an existing TOOL/Skill;
3. a router has accumulated final-artifact ownership and is becoming a hidden Skill;
4. a candidate can be merged back into an installed owner;
5. a superseded implementation should become DEPRECATED/LEGACY.

Duplicate ownership is a governance defect unless one owner is explicitly PRIMARY and the other is a bounded specialist/support role.

## 9｜Minimum sufficient execution

This contract does not require every Skill to run on every task. Owner selection remains governed by the Multi-Skill Execution DAG Contract and must prefer the minimum sufficient owner set for the required native output.

## 10｜Does not prove

A complete capability contract proves only that the owner boundary is declared. It does not prove Skill quality, project Design PASS, field truth, user validation, engineering validity or release readiness.
