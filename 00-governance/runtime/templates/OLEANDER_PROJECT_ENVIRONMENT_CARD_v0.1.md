# OLEANDER Project Environment Card v0.1

Status: **TEMPLATE / RUNTIME INPUT**  
Parent: `OLEANDER_CLOUD_FREE_PROJECT_PROFILE_v1.0` — ACTIVE CURRENT / GLOBAL OLEANDER DEFAULT unless explicitly overridden.  
Execution routing binding: `OLEANDER_CLOUD_FREE_EXECUTION_ROUTING_BINDING_v0.1.json`.

## Identity
- Project ID:
- Project Name:
- Primary Design / Engineering Type:
- Supporting Types:
- Stage / Purpose:
- Viewer / User / Operator Task:

## Authority
- Current Project Authority:
- Source Authority:
- Current Type Brief / METHOD:
- Current Design Source / Existing Mature Design:

## Required Output
- Required Native Output(s):
- Required Fidelity:
- Delivery Target:
- Readback Matrix:

## Execution
- Minimum Sufficient Owner Set:
- Browser Runtime:
- Required Software: `BROWSER_ONLY` by default
- Required Plugins: `NONE` by default
- Free-tier Boundary:
- Source / Asset Location:
- Editable Source Format:
- Preview / Derivative Format:

## Cloud-Free Studio Preflight｜after native output + owner set, before manual SaaS
Resolve each required capability in this order:

`AGENT_EXECUTABLE → CURRENT OLEANDER SKILL → SHARED_REPO_RUNTIME → FREE/INCLUDED CLOUD WHEN ACTUALLY EXPOSED → USER_WEB_MANUAL → CAPABILITY_HOLD`

**Lifecycle semantics:** the `SHARED_REPO_RUNTIME` production slot means **ACTIVE shared runtime only**. A Candidate shared runtime is not default-production eligible.

Current Cloud-Free repo surfaces are **CANDIDATE**, not default production runtimes:
- Responsive / visual staging → `browser-design-workbench/workbench.html`
- Bounded raster treatment / composition A-B → `browser-image-lab/image-lab.html`
- Concept spatial massing / camera / scale → `browser-spatial-lab/spatial-lab.html`
- Technical vector / packaging / POP preflight → `browser-technical-svg-lab/technical-svg-lab.html`

Candidate surface rule: `VALIDATION / TRAINING / SUPPORT / BOUNDED PROJECT REAPPLICATION WITH EXPLICIT CANDIDATE LABEL` only. A Candidate surface must **not** become `DEFAULT_PRODUCTION_OWNER`, `SOLE_FINAL_NATIVE_OUTPUT_AUTHORITY`, or an unlabeled Current production route. Default production routing requires an **ACTIVE** runtime.

Do **not** route first to Figma / Penpot / Photopea / SketchUp Web merely because they are familiar. They are optional/manual fallbacks when the Current Skill and an ACTIVE shared runtime cannot preserve the Required Native Output. A manual web option never counts as agent execution.

## Execution Surface｜must resolve per required capability
Allowed values: `AGENT_EXECUTABLE / SHARED_REPO_RUNTIME / USER_WEB_MANUAL / VIEW_ONLY_OR_REFERENCE / CAPABILITY_HOLD`.

| Capability | Tool / Runtime | Execution Surface Class | Lifecycle | Default production eligible? | Actually probed this run? | Free boundary | Result |
|---|---|---|---|---|---|---|---|
| Source / code editing | | | | | | | |
| Knowledge / project state | | | | | | | |
| Assets / archive | | | | | | | |
| Browser implementation | | | | | | | |
| Raster/image treatment | | | | | | | |
| UI/prototype workspace | | | | | | | |
| 3D/spatial authoring | | | | | | | |
| 3D viewing | | | | | | | |
| Technical/vector preflight | | | | | | | |
| Build / compute | | | | | | | |
| Deploy / share | | | | | | | |

`TOOL DOCUMENTED ≠ TOOL CALLABLE`. `USER_WEB_MANUAL ≠ AGENT_EXECUTED`. `CANDIDATE_RUNTIME ≠ DEFAULT_PRODUCTION_ELIGIBLE`. A conversation cannot write `EXECUTED` unless that surface was actually probed and used in that run.

## Capability State
- Browser-native capability:
- Current OLEANDER Skill capability:
- Shared repository runtime capability:
- Runtime lifecycle: `ACTIVE / CANDIDATE / SUPPORT / HOLD`
- Default production eligible?:
- Agent-executable connector capability:
- Free Web manual capability:
- Included free-quota cloud capability:
- Capability HOLD:
- Fallback:

## Plugin Record｜only if actually required
- Name:
- Version:
- Type:
- Purpose:
- Required?:
- Execution Surface Class:
- Free limit:
- Source:
- Output format:
- Fallback:
- Lock-in risk:
- Status:

## Review Boundary
### Internal artifact-first professional crit
May be performed in the producer context. It may return `REVISE / HOLD` and drive Root Cause → Repair → Retest, but it **cannot grant Independent KEEP**.

### Independent review
Required fields when Independent Review is applicable:
- producer_id
- reviewer_id
- review_input_artifact_id
- review_input_hash
- reviewer_independence_state
- review_verdict
- promotion_authority

`reviewer_independence_state=INDEPENDENT` requires `reviewer_id != producer_id`. A title such as “Professional Review” is not independence evidence. A review record missing the identity fields above is treated as `INTERNAL_ARTIFACT_FIRST_PROFESSIONAL_CRIT`, not Independent Review.

- Source / static-validator readback:
- Actual browser / pixel / interaction readback:
- Evidence Gate:
- Design Quality Gate:
- Runtime / Browser Gate:
- Engineering / Manufacturing / Field boundary:
- Does not prove:

`SOURCE READBACK / CI / VALIDATOR PASS ≠ BROWSER PASS ≠ DESIGN PASS`.  
`INTERNAL CRIT ≠ INDEPENDENT REVIEW`.

## Transaction Policy｜minimum sufficient process
Default for one logical object: **one Production PR** carries:

`IMPLEMENTATION → ACTUAL READBACK → INTERNAL CRIT → ROOT CAUSE → REPAIR → RETEST`

Independent Review should be a PR Review or isolated review record bound to the exact artifact hash. A separate review-only PR is **not** the default and is used only when explicit organizational/regulatory separation requires it.

`NO COMPRESSION / NO LOSS` protects information and evidence, not process length.

## Closure
- Actual Readback:
- Internal Crit:
- Root Cause / Feedback:
- Repair:
- Retest:
- Independent Review:
- Persistence / Remote Readback:
- Current Cleanup:

`TRANSACTION CLOSED` = this mutation/repair transaction is persisted.  
`OLEANDER FLOW CLOSED` = every required applicable phase is complete, including Independent Review when required, with no unresolved FAIL/HOLD.
