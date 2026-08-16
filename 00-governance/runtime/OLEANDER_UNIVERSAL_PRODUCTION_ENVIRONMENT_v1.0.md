# OLEANDER Universal Production Environment v1.0

Status: **CANDIDATE CURRENT**  
Scope: **ALL OLEANDER projects / all lanes / all conversations / all media**

## 0｜Core correction

OLEANDER does not use a single application as its production environment.

**Figma is not the default OLEANDER environment.** It is an optional specialist adapter only when a project explicitly needs Figma-native editable delivery or a verified Figma connector materially helps the work.

**Blender is already a shared OLEANDER runtime.** The existing `OLEANDER_BLENDER_RUNTIME_v1.0` remains the Blender authority. This document does not replace it; it places Blender inside a wider capability-routing environment shared by every OLEANDER conversation.

The invariant is:

> **Authority → Skill → Required native output → Capability probe → Best-fit adapter → Execution → Readback → Evidence Gate + Design Quality Gate**

Tool choice follows the project. The project never follows the tool.

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

## 3｜Tool Resolver

Before production, every OLEANDER conversation performs this resolver:

1. Read Current Authority / Source Authority / current project state.
2. Resolve an existing OLEANDER Skill before inventing a method.
3. Define the required **native output**: geometry, editable vector, HTML, dataset, render, video, PDF, etc.
4. Probe only the capabilities needed for that output.
5. Prefer an existing shared OLEANDER runtime or runner over project-specific installation logic.
6. Select the adapter that best preserves editability, truth and fidelity.
7. If the preferred adapter is absent, use an equivalent fallback when no information is lost.
8. Mark only the genuinely unavailable step `PENDING`; continue all other executable work.
9. Open/render/read back the resulting artifact before a visual Design PASS.

---

## 4｜Production lanes and adapters

### Research / knowledge / source evidence

Preferred adapters: Web, official archives, PDFs, Notion, GitHub, Google Drive. These establish evidence and provenance; they do not establish visual quality.

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

## 5｜Figma policy

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

## 6｜Blender policy

The existing runtime remains authoritative:

- `00-governance/runtime/OLEANDER_BLENDER_RUNTIME_v1.0.json`
- `00-governance/runtime/OLEANDER_BLENDER_RUNTIME_v1.0.md`
- `tools/oleander-runtime/activate-blender.sh`
- `tools/oleander-runtime/blender.sh`
- `.github/workflows/oleander-blender-runtime-contract.yml`

Use Blender across product, spatial, CMF, motion, model inspection, geometry conversion and AOV/render QA when it is the correct adapter.

Do not fork a separate Blender installation path inside each project.

---

## 7｜Execution receipt

Any meaningful production run should be able to report:

`TASK / AUTHORITY / SKILL_RESOLVED / REQUIRED_OUTPUT / CAPABILITY_STATE / ADAPTER_SELECTED / VERIFIED_VERSION_OR_PATH / EXECUTED_OR_PENDING / READBACK_STATE / EVIDENCE_GATE / DESIGN_QUALITY_GATE / DOES_NOT_PROVE`

`EXECUTED`, `TRACEABLE` and `REPRODUCIBLE` are process states. They cannot be converted into `Design PASS`, `Professional Finish` or `MAIN KEEP` without independent design review.

---

## 8｜No-compression / no-loss environment rule

Changing tools must not delete design information. If one adapter cannot preserve a layer, geometry, text, dimension, material relation, interaction state or source authority, do not use the apparent simplicity of the tool change as justification for information loss.

**NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS** applies to the production environment itself.
