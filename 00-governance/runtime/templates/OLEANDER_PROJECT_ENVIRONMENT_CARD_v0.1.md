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
- Current OLEANDER Skill / Owner:
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

## Software Selection Preflight｜skill owner first, software second
Do **not** choose software first. Resolve in this sequence:

`CURRENT OLEANDER SKILL / OWNER → REQUIRED NATIVE OUTPUT + FIDELITY → AGENT-EXECUTABLE CONNECTOR OR NATIVE SOURCE TOOL → ACTIVE SHARED RUNTIME → FREE/INCLUDED CLOUD WHEN ACTUALLY EXPOSED → USER_WEB_MANUAL → CAPABILITY_HOLD`

Rules:
- Familiar software does not override the Current Skill or Required Native Output.
- Agent-executable connector or ACTIVE shared runtime precedes a manual web tool when both preserve the same native output.
- A Candidate shared runtime is validation / training / support only unless explicitly labeled as bounded project reapplication.
- Existing editable project files/pages are reused before new SaaS files are created.
- Low-file/page-limit software must not become Global Current.
- `TOOL DOCUMENTED ≠ TOOL CALLABLE`; `CONNECTOR EXPOSED ≠ UNLIMITED PLAN CAPACITY`; `USER_WEB_MANUAL ≠ AGENT_EXECUTED`.

### Current software role matrix
| Need | Preferred execution | Optional / fallback | Hard boundary |
|---|---|---|---|
| Web/UI implementation | HTML/CSS/JS/SVG + real browser | Figma connector only for existing-file or explicit Figma delivery; Penpot manual fallback | Figma/Penpot do not replace browser implementation evidence |
| UI/vector design handoff | Editable repo-native SVG/HTML first | Figma connector if explicit editable Figma handoff and capacity check passes | Figma is OPTIONAL TEMP, not Global Current |
| Raster/image treatment | Agent-executable deterministic source transform when sufficient | Candidate Image Lab for validation/support; Photopea manual fallback | Source authority remains unchanged; high-res quality must be proven |
| 3D/spatial/product/CMF | **Blender ACTIVE shared runtime** when callable and fit | Candidate Spatial Lab for proxy/readback; SketchUp Web manual fallback | No fake BIM/CAD/Class-A/manufacturing geometry |
| Technical/vector drawing | Editable SVG/PDF native | Candidate Technical SVG Lab for validation/support; Figma only for explicit handoff | Supplier/prepress/engineering approval remains OPEN when applicable |
| Motion | Browser motion or Blender ACTIVE runtime, depending output | Manual tool only if native output cannot otherwise be preserved | Actual state/frame readback required |
| Deploy/share | Vercel connector when exposed and free/existing plan fits; GitHub Pages / Cloudflare Pages Free | manual deploy only if needed | Deploy PASS ≠ Browser PASS ≠ Design PASS |

### Figma capacity rule
Figma is now an **agent-executable connector when exposed**, but it remains an **OPTIONAL TEMP adapter** because low shared file/page limits and vendor lock-in disqualify it from Global Current.

Before any new Figma file:
1. Is Figma explicitly required by the deliverable, or does an existing Figma file materially improve the task?
2. Can the existing project file/page be reused instead of creating a new file?
3. Is current file/team capacity available without paid upgrade or deletion pressure?
4. Is recoverable repo/open-native source preserved outside Figma?

If any required answer is NO → do not create a new Figma file; route to repo-native production, another verified execution surface, or HOLD.

Current connector/plugin check 2026-08-27:
- Figma connector: **installed / agent-executable when exposed**.
- Penpot ChatGPT plugin: **not found**.
- Photopea ChatGPT plugin: **not found**.
- SketchUp ChatGPT plugin: **not found**.

## Cloud-Free Studio Preflight｜after native output + owner set, before manual SaaS
Resolve each required capability in this order:

`AGENT_EXECUTABLE → CURRENT OLEANDER SKILL → SHARED_REPO_RUNTIME → FREE/INCLUDED CLOUD WHEN ACTUALLY EXPOSED → USER_WEB_MANUAL → CAPABILITY_HOLD`

Interpretation: the Current OLEANDER Skill / Owner is resolved **before this execution-surface list is applied**. The `SHARED_REPO_RUNTIME` production slot means **ACTIVE shared runtime only**.

Current Cloud-Free repo surfaces are **CANDIDATE**, not default production runtimes:
- Responsive / visual staging → `browser-design-workbench/workbench.html`
- Bounded raster treatment / composition A-B → `browser-image-lab/image-lab.html`
- Concept spatial proxy / camera / scale → `browser-spatial-lab/spatial-lab.html`
- Technical vector / packaging / POP preflight → `browser-technical-svg-lab/technical-svg-lab.html`

Candidate surface rule: `VALIDATION / TRAINING / SUPPORT / BOUNDED PROJECT REAPPLICATION WITH EXPLICIT CANDIDATE LABEL` only. A Candidate surface must **not** become `DEFAULT_PRODUCTION_OWNER`, `SOLE_FINAL_NATIVE_OUTPUT_AUTHORITY`, or an unlabeled Current production route. Default production routing requires an **ACTIVE** runtime.

Do **not** route first to Penpot / Photopea / SketchUp Web merely because they are familiar. They are manual fallbacks when Current Skill + agent-executable surface + ACTIVE shared runtime cannot preserve the Required Native Output. Figma is treated separately as an optional agent-executable TEMP adapter when its connector is exposed and its capacity/explicit-delivery conditions pass.

## Execution Surface｜must resolve per required capability
Allowed values: `AGENT_EXECUTABLE / SHARED_REPO_RUNTIME / USER_WEB_MANUAL / VIEW_ONLY_OR_REFERENCE / CAPABILITY_HOLD`.

| Capability | Tool / Runtime | Execution Surface Class | Lifecycle | Default production eligible? | Actually probed this run? | Free/capacity boundary | Result |
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

A conversation cannot write `EXECUTED` unless that surface was actually probed and used in that run.

## Capability State
- Browser-native capability:
- Current OLEANDER Skill capability:
- Agent-executable connector capability:
- ACTIVE shared repository runtime capability:
- Candidate shared repository runtime capability:
- Runtime lifecycle: `ACTIVE / CANDIDATE / SUPPORT / HOLD`:
- Default production eligible?:
- Free Web manual capability:
- Included free-quota cloud capability:
- Capability HOLD:
- Fallback:

## Software / Plugin Record｜only if actually required
- Name:
- Version:
- Type:
- Purpose:
- Required?:
- Execution Surface Class:
- Lifecycle / Role:
- Free or capacity limit:
- Existing-file reuse checked?:
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
