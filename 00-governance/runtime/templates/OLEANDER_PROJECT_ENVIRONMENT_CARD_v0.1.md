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

Current shared repo candidates:
- Responsive / visual staging → `browser-design-workbench/workbench.html`
- Bounded raster treatment / composition A-B → `browser-image-lab/image-lab.html`
- Concept spatial massing / camera / scale → `browser-spatial-lab/spatial-lab.html`
- Technical vector / packaging / POP preflight → `browser-technical-svg-lab/technical-svg-lab.html`

Do **not** route first to Figma / Penpot / Photopea / SketchUp Web merely because they are familiar. They are optional/manual fallbacks when the shared runtime cannot preserve the Required Native Output. A manual web option never counts as agent execution.

## Execution Surface｜must resolve per required capability
Allowed values: `AGENT_EXECUTABLE / SHARED_REPO_RUNTIME / USER_WEB_MANUAL / VIEW_ONLY_OR_REFERENCE / CAPABILITY_HOLD`.

| Capability | Tool / Runtime | Execution Surface Class | Actually probed this run? | Free boundary | Result |
|---|---|---|---|---|---|
| Source / code editing | | | | | |
| Knowledge / project state | | | | | |
| Assets / archive | | | | | |
| Browser implementation | | | | | |
| Raster/image treatment | | | | | |
| UI/prototype workspace | | | | | |
| 3D/spatial authoring | | | | | |
| 3D viewing | | | | | |
| Technical/vector preflight | | | | | |
| Build / compute | | | | | |
| Deploy / share | | | | | |

`TOOL DOCUMENTED ≠ TOOL CALLABLE`. `USER_WEB_MANUAL ≠ AGENT_EXECUTED`. A conversation cannot write `EXECUTED` unless that surface was actually probed and used in that run.

## Capability State
- Browser-native capability:
- Current OLEANDER Skill capability:
- Shared repository runtime capability:
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
- Source / static-validator readback:
- Actual browser / pixel / interaction readback:
- Evidence Gate:
- Design Quality Gate:
- Runtime / Browser Gate:
- Engineering / Manufacturing / Field boundary:
- Does not prove:

`SOURCE READBACK / CI / VALIDATOR PASS ≠ BROWSER PASS ≠ DESIGN PASS`.

## Closure
- Actual Readback:
- Independent Review:
- Root Cause / Feedback:
- Retest:
- Persistence / Remote Readback:
- Current Cleanup:
