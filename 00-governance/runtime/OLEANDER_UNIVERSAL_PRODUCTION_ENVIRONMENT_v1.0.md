# OLEANDER Universal Production Environment v1.0

Status: **ACTIVE CURRENT**  
Scope: **ALL OLEANDER projects / all lanes / all conversations / all media**

## 0｜Core correction

OLEANDER does not use a single application as its production environment.

**Figma is not the default OLEANDER environment.** It is an optional specialist adapter only when a project explicitly needs Figma-native editable delivery or a verified Figma connector materially helps the work.

**Blender is already a shared OLEANDER runtime.** The existing `OLEANDER_BLENDER_RUNTIME_v1.0` remains the Blender authority. This document does not replace it; it places Blender inside a wider capability-routing environment shared by every OLEANDER conversation.

The invariant is:

> **Authority → Project Flow / State → Existing Mature Design → Existing Skill → Required native output → Capability probe → Best-fit adapter → Real Execution → Readback → Evidence Gate + Design Quality Gate → Gap Diagnosis**

Tool choice follows the project. The project never follows the tool.

**Skill optimization follows execution evidence. Execution does not wait for speculative Skill optimization.**

For reference-reconstruction work, add one mandatory preflight before production:

> **Source Authority → Source Bytes Materialized → Reference Frame Locked → Reconstruction Runtime → 1:1 Fidelity Review**

`BROWSER_VISIBLE ≠ LOCAL_SOURCE_BYTES_AVAILABLE`.

---

## 1｜What “all conversations can use Blender” means

Every OLEANDER conversation must know and prefer the same Blender resolution contract when 3D, geometry, CMF, render, animation, AOV or model inspection is required:

1. use the runtime-provided `$OLEANDER_BLENDER_BIN` when present;
2. otherwise use `blender` on `PATH`;
3. otherwise use the managed ChatGPT fallback defined by `OLEANDER_BLENDER_RUNTIME_v1.0` when that execution surface exposes it;
4. project code should invoke `bash tools/oleander-runtime/blender.sh ...` rather than hard-code a project-specific Blender path.

This gives all OLEANDER projects one Blender interface without coupling them to Timer, C04, Automotive or any other individual project.

However, a conversation must still probe the current execution surface before writing `EXECUTED`. A repository contract proves that a shared route exists; it does not prove that every UI surface has exposed command execution in that exact turn. If invocation is unavailable, mark only that Blender operation `PENDING_VERIFICATION` or route it to a verified OLEANDER runner. Do not pretend it ran.

---

## 2｜Universal capability states

Every production round resolves each needed capability to one of:

- `NATIVE_AVAILABLE` — directly callable in the current execution surface;
- `CONNECTOR_AVAILABLE` — available through a connected service/API;
- `SHARED_RUNTIME_AVAILABLE` — available through an OLEANDER shared runtime such as Blender;
- `RUNNER_AVAILABLE` — executable through a verified workstation/CI/runner;
- `FALLBACK_AVAILABLE` — an equivalent method preserves the required information and fidelity;
- `PENDING_VERIFICATION` — expected route exists but has not been verified in this run;
- `UNAVAILABLE` — no valid execution route exists.

Do not turn one unavailable adapter into a whole-project blocker when another adapter can preserve the required native information.

---

## 3｜Process-first / Skill-gap discipline

Every OLEANDER project, training run, redesign, deepening task and restarted conversation must execute the **current OLEANDER process and current installed Skills first**. Skill creation or Skill optimization is downstream of real execution evidence.

Canonical sequence:

`CURRENT AUTHORITY / PROJECT FLOW → EXISTING MATURE DESIGN / DESIGN SOURCE → CURRENT PROJECT STATE / CURRENT DELTA → EXISTING SKILL RESOLVER → INVOKE EXISTING SKILL(S) → REQUIRED NATIVE OUTPUT → RUNTIME / ADAPTER PROBE → REAL EXECUTION → ACTUAL READBACK → EVIDENCE GATE + DESIGN QUALITY GATE → GAP DIAGNOSIS → OPTIMIZE EXISTING SKILL ONLY IF NEEDED → REGRESSION / GOLDEN CASE → RE-RUN → NEW SKILL ONLY IF NO EXISTING SKILL CAN REASONABLY OWN THE GAP`

Before changing a Skill, the run must record:

- which existing Skill(s) were actually invoked;
- the exact step or decision that proved insufficient;
- the observable consequence in the real artifact, runtime or visual readback;
- why a project-level correction alone is insufficient or why the failure recurs across tasks;
- why the change belongs inside the owning Skill rather than a parallel Skill.

Illegal shortcuts:

- optimizing a Skill before attempting the real task with the current Skill;
- creating a Skill because a case/reference is interesting, a task is newly named, or a cleaner framework can be written;
- treating documentation, commit, PR, CI, eval schema or artifact existence as Skill validation;
- allowing a training artifact or Skill Candidate to become project Authority without explicit binding;
- creating a parallel Skill when an existing Skill reasonably owns the capability.

If the existing Skill is insufficient, **extend or repair that Skill first**. A changed Skill remains Candidate until the same or equivalent task is re-run and actual readback shows that the gap was closed without regressions. New Skill creation is the final option, not the starting point.

---

## 4｜Tool Resolver

Before production, every OLEANDER conversation performs this resolver:

1. Read Current Authority / Source Authority / current Project Flow / Project State / Current Delta.
2. Locate and open relevant Existing Mature Design / Design Source when it exists.
3. Resolve and actually invoke the current installed OLEANDER Skill(s) before inventing or changing a method.
4. Define the required **native output**: geometry, editable vector, HTML, dataset, render, video, PDF, etc.
5. If the task is reference reconstruction, resolve `OLEANDER_REFERENCE_MATERIALIZATION_GATE_v1.0` before any fidelity claim.
6. Probe only the capabilities needed for that output.
7. Prefer an existing shared OLEANDER runtime or runner over project-specific installation logic.
8. Select the adapter that best preserves editability, truth and fidelity.
9. If the preferred adapter is absent, use an equivalent fallback when no information is lost.
10. Execute the real task; do not stop at method description when production is possible.
11. Open/render/read back the actual output and run Evidence Gate + Design Quality Gate independently.
12. Only after a concrete gap is observed may the owning Skill be optimized; then run regression/golden cases and re-run the task.
13. Create a new Skill only if no current Skill can reasonably own the proven gap.
14. Mark only the genuinely unavailable step `PENDING`; continue all other executable work.

---

## 5｜Production lanes and adapters

### Research / knowledge / source evidence

Preferred adapters: Web, official archives, PDFs, Notion, GitHub, Google Drive. These establish evidence and provenance; they do not establish visual quality.

### Reference materialization / 1:1 reconstruction

Canonical contract:

- `00-governance/runtime/OLEANDER_REFERENCE_MATERIALIZATION_GATE_v1.0.md`
- `00-governance/runtime/OLEANDER_REFERENCE_MATERIALIZATION_GATE_v1.0.json`

Preferred deterministic adapter:

- `tools/oleander-runtime/materialize_reference.py`

Required sequence:

`SOURCE_AUTHORITY_FOUND → SOURCE_BYTES_MATERIALIZED → SOURCE_HASHED → REFERENCE_FRAME_EXTRACTED → REFERENCE_SCALE_LOCKED → COMPARISON_RUNTIME_VERIFIED`

Use the first valid source-byte route that preserves the original file: mounted upload, public direct URL, connector-native materialization/download, or exact GitHub/Drive file retrieval. A browser view, citation ref, screenshot handle or preview is not a local byte source.

If source bytes or an exact reference frame cannot be obtained, mark `REFERENCE MATERIALIZATION GATE = HOLD`. Continue only as `STRUCTURAL RECONSTRUCTION / METHOD STUDY / REFERENCE-BOUND STUDY`; do not claim `REPRODUCTION PASS`.

After materialization, use matched-scale side-by-side plus overlay/flicker/difference where technically meaningful. Hashing and rendering source bytes prove reproducibility only; they do not prove fidelity or design quality.

### Deterministic data / GIS / calculation

Preferred adapters: Python and verified deterministic libraries; GDAL / GeoPandas / QGIS only when actually available in the run. Machine-specific paths in old skills are workstation configuration, not universal runtime truth.

### 2D vector / information / layout

Preferred adapters: SVG, HTML/CSS, PDF/vector tooling and other verified editable vector environments. Figma may be used when genuinely useful, but is **not required and not default**. A project must not stop because Figma is absent.

### 3D / spatial / product / geometry

Default open shared backend: **OLEANDER Blender Runtime** where suitable. Rhino / Grasshopper / CAD / BIM / FreeCAD remain valid specialist adapters when the project's geometry authority or deliverable requires them and the runtime is verified.

Derived mesh, render or screenshot never silently replaces authoritative source geometry.

### Materials / CMF / rendering

Blender/Cycles is the preferred shared open renderer when suitable. Material truth still requires measured/reference data, channel logic, scale and project-specific evidence. Render PASS ≠ material/engineering PASS.

### Motion / video

Use Blender animation/compositor, FFmpeg, browser motion or another verified native tool according to the media authority. Encoding success ≠ motion Design PASS.

### Web / interactive

Use HTML/CSS/JS and a real browser runtime. Playwright/Chromium/browser readback is used when verified. Static export is allowed as evidence when browser execution is unavailable, but must be labeled `STATIC EXPORT EVIDENCE ≠ BROWSER PASS`.

### Visual QA

Any visual conclusion requires actual final pixels or rendered pages. Minimum review is:

- First-read / thumbnail / distance view;
- Detail / near-read.

Add desktop/mobile for web, far/near for boards, overall/detail for drawings, overall/scale-detail for models and renders.

---

## 6｜Figma policy

Figma is an **optional specialist adapter**, not an OLEANDER dependency.

Use it only when:
- editable Figma-native delivery is explicitly required;
- the connector is actually available;
- its component/interface workflow is the best-fit tool;
- visual screenshot/readback can be verified when the result is being judged visually.

Do not:
- route every 2D exercise to Figma;
- block training or project work because Figma is unavailable;
- treat Figma node count, successful generation or export existence as visual evidence;
- let Figma become Source Authority unless the project explicitly defines it as such.

---

## 7｜Blender policy

The existing runtime remains authoritative:

- `00-governance/runtime/OLEANDER_BLENDER_RUNTIME_v1.0.json`
- `00-governance/runtime/OLEANDER_BLENDER_RUNTIME_v1.0.md`
- `tools/oleander-runtime/activate-blender.sh`
- `tools/oleander-runtime/blender.sh`
- `.github/workflows/oleander-blender-runtime-contract.yml`

Use Blender across product, spatial, CMF, motion, model inspection, geometry conversion and AOV/render QA when it is the correct adapter.

Do not fork a separate Blender installation path inside each project.

---

## 8｜Execution receipt

Any meaningful production run should be able to report:

`TASK / AUTHORITY / PROJECT_FLOW_STATE / EXISTING_DESIGN_READBACK / SKILL_RESOLVED / SKILL_ACTUALLY_INVOKED / REQUIRED_OUTPUT / CAPABILITY_STATE / ADAPTER_SELECTED / VERIFIED_VERSION_OR_PATH / EXECUTED_OR_PENDING / READBACK_STATE / EVIDENCE_GATE / DESIGN_QUALITY_GATE / GAP_OBSERVED / SKILL_CHANGE_IF_ANY / REGRESSION_STATE / RERUN_STATE / DOES_NOT_PROVE`

Reference-reconstruction runs additionally report:

`SOURCE_LOCATOR / SOURCE_BYTES_STATE / SOURCE_SHA256 / REFERENCE_FRAME_STATE / PAGE_OR_FRAME / SCALE_OR_DPI / RENDERER / REFERENCE_FRAME_SHA256 / COMPARISON_RUNTIME / FIDELITY_GATE`

`EXECUTED`, `TRACEABLE` and `REPRODUCIBLE` are process states. They cannot be converted into `Design PASS`, `Professional Finish` or `MAIN KEEP` without independent design review.

---

## 9｜No-compression / no-loss environment rule

Changing tools must not delete design information. If one adapter cannot preserve a layer, geometry, text, dimension, material relation, interaction state or source authority, do not use the apparent simplicity of the tool change as justification for information loss.

**NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS** applies to the production environment itself.
