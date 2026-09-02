# OLEANDER Universal Production Environment v1.0

Status: **ACTIVE CURRENT**  
Implementation revision: **1.0.4**  
Scope: **ALL OLEANDER projects / all lanes / all conversations / all media**

## 0｜Core correction

OLEANDER does not use a single application as its production environment.

**Figma is not the default OLEANDER environment.** It is an optional specialist adapter only when a project explicitly needs Figma-native editable delivery or a verified Figma connector materially helps the work.

**Blender is already a shared OLEANDER runtime.** The existing `OLEANDER_BLENDER_RUNTIME_v1.0` remains the Blender authority. This document does not replace it.

Current invariant:

> **Authority → Sticky Constraint Preflight → Existing Skill → Required native output → Capability probe → Best-fit allowed adapter → Execution → Readback → Evidence / Design Review → Flow Completion Gate**

Tool choice follows the project and active user constraints. The project never follows the tool.

## 1｜Sticky constraint preflight

Before probing or selecting any tool, adapter or execution environment, resolve active constraints through `OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2` implementation revision `1.2.2`.

Hard rules:

- an explicit `NO_IMAGE_GENERATION` blocks image-generation tools and generative-image adapters;
- an explicit `NO_NEW_SKILL / NO_NEW_METHOD / NO_NEW_FRAMEWORK` blocks gap-driven creation of those objects;
- generic follow-ups such as “继续 / 优化 / 再做” do not revoke active constraints;
- only a later explicit user instruction that changes the named constraint can release it;
- if a denied capability is genuinely required and no compliant fallback preserves the requested native output, mark that step `HOLD` rather than silently violating the constraint.

This preflight happens **before** tool choice. A capability being convenient or visually attractive cannot override the lock.

## 2｜Full-flow completion rule

When a task is OLEANDER production/mutation/training/state-changing review work, or explicitly requires the full OLEANDER process, the environment may not report “complete” at an intermediate technical milestone.

The following are not closure on their own:

- plan written;
- method explained;
- artifact/file created;
- export succeeded;
- PR opened;
- CI green;
- producer self-check passed;
- render passed;
- regression passed.

The Current Execution Receipt Flow Completion Gate must pass after all applicable phases are closed.

**Full flow does not mean all Skills.** The Minimum Sufficient Owner Set still applies.

## 3｜What “all conversations can use Blender” means

Every OLEANDER conversation must know and prefer the same Blender resolution contract when 3D, geometry, CMF, render, animation, AOV or model inspection is required **and not prohibited by an active constraint**:

1. use the runtime-provided `$OLEANDER_BLENDER_BIN` when present;
2. otherwise use `blender` on `PATH`;
3. otherwise use the managed ChatGPT fallback defined by `OLEANDER_BLENDER_RUNTIME_v1.0` when that execution surface exposes it;
4. if the shared interface is active but this job has no materialized binary, use the runtime-owned rematerialization route;
5. if the current conversation surface cannot host the binary directly but an approved shared runner is available, route the job to the shared runner;
6. project code should invoke the shared runtime/runner contract rather than hard-code or install a project-specific Blender environment.

A conversation must still probe the current execution surface before writing `EXECUTED`. A repository contract proves that a route exists; it does not prove that the route executed in that turn.

### 3A｜Shared runtime interface ≠ current-job materialization

This distinction applies to **all shared OLEANDER runtimes and runners**, not only Blender.

A repository-wide runtime may be `ACTIVE` while a newly created job/container does not yet contain the executable bytes. Therefore:

- `SHARED_RUNTIME_AVAILABLE` describes the Current OLEANDER capability/interface;
- a missing executable in one job describes only that job's binding/materialization state;
- a job-local missing path must not be promoted into a global statement such as “OLEANDER has no stable environment”;
- before declaring the capability `UNAVAILABLE`, the task must attempt the Current runtime resolver, runtime-owned rematerialization when defined, and an allowed shared runner when defined;
- projects must not respond to job-local materialization failure by creating parallel installations, project-specific environment frameworks, duplicated download logic, or a new Skill/METHOD/Gate;
- the project declares its required native output and bounded project script/input/output contract; shared runtime bootstrap remains owned by the existing OLEANDER runtime layer.

Correct failure scope:

`ACTIVE_SHARED_RUNTIME + JOB_BINARY_NOT_MATERIALIZED → REMATERIALIZE_OR_SHARED_RUNNER_RESOLUTION`

not:

`JOB_BINARY_NOT_MATERIALIZED → GLOBAL_ENVIRONMENT_MISSING → PROJECT_BUILDS_NEW_ENVIRONMENT`.

## 4｜Universal capability states

Every production round resolves each needed capability to one of:

- `NATIVE_AVAILABLE`
- `CONNECTOR_AVAILABLE`
- `SHARED_RUNTIME_AVAILABLE`
- `RUNNER_AVAILABLE`
- `FALLBACK_AVAILABLE`
- `PENDING_VERIFICATION`
- `UNAVAILABLE`

A capability that is available but actively denied by the user is **not eligible for selection**.

Do not turn one unavailable or denied adapter into a whole-project blocker when another adapter can preserve the required native information. If none can, return the specific step as `HOLD`.

## 5｜Tool Resolver

Before production, every OLEANDER conversation performs this resolver:

1. Read Current Authority / Source Authority / Current Task.
2. Resolve sticky execution constraints.
3. Enforce active tool/output/creation/process locks.
4. Resolve an existing OLEANDER Skill before inventing a method.
5. Define the required native output and fidelity.
6. If reference reconstruction applies, resolve `OLEANDER_REFERENCE_MATERIALIZATION_GATE_v1.0`.
7. Probe only capabilities needed for the required output.
8. Resolve the Current shared runtime/interface before interpreting a job-local binary/path result.
9. Prefer existing shared OLEANDER runtime/runner and runtime-owned rematerialization over project-specific installation logic.
10. Select the best-fit adapter **within the active constraint set**.
11. Use an equivalent fallback when no information is lost.
12. Mark only the genuinely unavailable/denied non-replaceable step pending or HOLD.
13. Open/render/read back the resulting artifact.
14. Verify the Flow Completion Gate before any complete/closed claim.

## 6｜Reference materialization / 1:1 reconstruction

For reference-reconstruction work, use:

- `00-governance/runtime/OLEANDER_REFERENCE_MATERIALIZATION_GATE_v1.0.md`
- `00-governance/runtime/OLEANDER_REFERENCE_MATERIALIZATION_GATE_v1.0.json`
- `90-shared/toolchains/reference-materialization/materialize_reference.py`

Required sequence:

`SOURCE_AUTHORITY_FOUND → SOURCE_BYTES_MATERIALIZED → SOURCE_HASHED → REFERENCE_FRAME_EXTRACTED → REFERENCE_SCALE_LOCKED → COMPARISON_RUNTIME_VERIFIED → INDEPENDENT_ONE_TO_ONE_RECONSTRUCTION → PIXEL_LEVEL_COMPARISON → MISMATCH_REPAIR → RETEST`

`BROWSER_VISIBLE ≠ LOCAL_SOURCE_BYTES_AVAILABLE`.

`REPRODUCTION / RECONSTRUCTION / 复现 / 复刻 / 1:1 / 一模一样 / 按原图做` defaults to pixel-level fidelity. A visually similar result without pixel-level comparison cannot receive `REPRODUCTION PASS`.

If source bytes or exact reference frame cannot be obtained, mark `REFERENCE MATERIALIZATION GATE = HOLD`. If pixel-level comparison cannot be executed or material pixel mismatch remains, keep `FIDELITY HOLD / REVISE`.

Direct source copying/re-export does not count as reconstruction evidence.

## 7｜Production lanes and adapters

### Research / knowledge / source evidence
Preferred adapters: Web, official archives, PDFs, Notion, GitHub, Google Drive.

### Deterministic data / GIS / calculation
Preferred adapters: Python and verified deterministic libraries; GDAL / GeoPandas / QGIS only when actually available.

### 2D vector / information / layout
Preferred adapters: SVG, HTML/CSS, PDF/vector tooling and other verified editable vector environments. Figma remains optional, not required and not default.

### 3D / spatial / product / geometry
Default open shared backend: OLEANDER Blender Runtime where suitable. Rhino / Grasshopper / CAD / BIM / FreeCAD remain valid specialist adapters when required and verified.

### Materials / CMF / rendering
Blender/Cycles is the preferred shared open renderer when suitable. Render PASS ≠ material/engineering PASS.

### Motion / video
Use Blender animation/compositor, FFmpeg, browser motion or another verified native tool according to media authority and active constraints.

### Web / interactive
Use HTML/CSS/JS and a real browser runtime; static export is not browser PASS.

### Visual QA
Any visual conclusion requires actual final pixels or rendered pages. Minimum review is first-read plus detail/near-read, with medium-specific paired views as required.

## 8｜Figma policy

Figma is an optional specialist adapter, not an OLEANDER dependency.

Do not route every 2D exercise to Figma, block work because Figma is absent, treat Figma node count/export existence as design evidence, or let Figma become Source Authority unless the project explicitly defines it as such.

## 9｜Blender policy

The existing runtime remains authoritative:

- `00-governance/runtime/OLEANDER_BLENDER_RUNTIME_v1.0.json`
- `00-governance/runtime/OLEANDER_BLENDER_RUNTIME_v1.0.md`
- `tools/oleander-runtime/activate-blender.sh` (Legacy compatibility adapter; not the Current runtime implementation namespace)
- `tools/oleander-runtime/blender.sh` (Legacy compatibility adapter; not the Current runtime implementation namespace)
- `90-shared/toolchains/blender-runtime/ensure-blender-5.2.sh`
- `.github/workflows/oleander-shared-blender-runner.yml`
- `.github/workflows/oleander-blender-runtime-contract.yml`

Current runtime implementation belongs to `90-shared/toolchains/` and the approved shared runner. The frozen Legacy `tools/` root may remain referenced only by existing compatibility adapters; it must not receive new runtime implementation or bootstrap logic.

Do not fork a separate Blender installation path or Blender bootstrap workflow inside each project. A project workflow may call the shared runner with project-specific script/output parameters; the project does not own Blender installation or version recovery.

## 10｜Execution Receipt

Current contract:

- `00-governance/runtime/OLEANDER_EXECUTION_RECEIPT_v1.0.json`
- policy revision `1.1`

Every new material execution receipt records the normal authority/output/owner/artifact/execution/readback/regression/review/closure fields **plus**:

- `constraint_lock`
- `flow_completion`

Only the explicitly allowlisted pre-policy receipts may omit those sections.

`EXECUTED`, `TRACEABLE` and `REPRODUCIBLE` are process states. They cannot be converted into `Design PASS`, `Professional Finish`, `MAIN KEEP` or full-flow closure without the required downstream gates.

## 11｜No-compression / no-loss environment rule

Changing tools must not delete design information. If one adapter cannot preserve a layer, geometry, text, dimension, material relation, interaction state or Source Authority, do not use apparent simplicity to justify information loss.

**NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS** applies to the production environment itself, while Minimum Sufficient Owner Set prevents unnecessary full-stack execution.
