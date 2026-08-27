# OLEANDER Project Environment Card v0.1

Status: **TEMPLATE / RUNTIME INPUT**  
Parent: `OLEANDER_CLOUD_FREE_PROJECT_PROFILE_v1.0` — ACTIVE CURRENT / GLOBAL OLEANDER DEFAULT unless explicitly overridden.  
Execution routing binding: `OLEANDER_CLOUD_FREE_EXECUTION_ROUTING_BINDING_v0.1.json`.  
Design production contract: `OLEANDER_DESIGN_ENVIRONMENT_PRODUCTION_CONTRACT_v1.0.json` — subordinate production contract; no new Method / Skill / Gate / authority.  
Professional toolchain candidate: `OLEANDER_PRO_DESIGN_TOOLCHAIN_RUNTIME_v0.1.json` → `90-shared/toolchains/pro-design` — runtime smoke validated Candidate only; not default production eligible until existing review/promotion requirements are satisfied.

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
- Current Editable Master Object ID:
- Current Editable Master Path / Locator:
- Current Editable Master Format:
- Design / Geometry Authority when different from presentation master:
- Master Version / Commit / Revision:

## Required Output
- Required Native Output(s):
- Required Fidelity:
- Editable source required?:
- Text / annotation editability required?:
- Unit system when applicable:
- Real-size / scale basis when applicable:
- Dimension Authority when applicable:
- Geometry Authority when applicable:
- Delivery Target:
- Required Derived Formats:
- Readback Matrix:
- AI-generated visual role: `NONE` by default; otherwise `SUPPLEMENTAL_EFFECT_RENDER / REFERENCE_VISUAL / CONCEPT_EXPLORATION / DIAGRAM_SUPPORT` only

## Execution
- Minimum Sufficient Owner Set:
- Browser Runtime:
- Required Software: `BROWSER_ONLY` by default
- Required Plugins: `NONE` by default
- Free-tier Boundary:
- Source / Asset Location:
- Editable Source Format:
- Preview / Derivative Format:
- Current semantic production zones mapped onto project folders:

## Source / Master / Derivative split｜mandatory for material design production
Do not collapse source, editable master, generated supplement and delivery derivative into one undifferentiated folder or file identity.

| Role | Current object / path | Format | Authority / editability | Can become Current silently? |
|---|---|---|---|---|
| SOURCE_AUTHORITY | | | factual / geometric / project constraint | NO |
| EDITABLE_MASTER | | | reconstructable Current design source | N/A — this is the Current master |
| WORKING_DERIVATIVE | | | bounded intermediate | NO |
| REFERENCE | | | read-only | NO |
| GENERATED_SUPPLEMENT | | | synthetic supplemental visualization only | NO |
| DERIVED_EXPORT | | | review / publish / delivery output | NO |
| DELIVERY | | | package surface | NO |
| ARCHIVE_OR_SUPERSEDED | | | provenance only | NO |

Rules:
- One logical design object has one identified Current editable master.
- PNG / JPG / screenshot / render / deployment / preview is not the editable master.
- A derivative becomes a master only through an explicit identity + authority update; filename drift is not promotion.
- Semantic roles above map onto the project's existing folder architecture. Do **not** create a parallel directory tree just to match these labels.
- TEMP / autosave / cache / proxy / obsolete-final files do not enter delivery.

## Software Selection Preflight｜skill owner first, software second
Do **not** choose software first. Resolve in this sequence:

`CURRENT OLEANDER SKILL / OWNER → REQUIRED NATIVE OUTPUT + FIDELITY → AGENT_EXECUTABLE CURRENT CONNECTOR OR NATIVE SOURCE TOOL → SHARED_REPO_RUNTIME (ACTIVE ONLY) → FREE/INCLUDED CLOUD WHEN ACTUALLY EXPOSED → USER_WEB_MANUAL → CAPABILITY_HOLD`

Rules:
- Familiar software does not override the Current Skill or Required Native Output.
- Adapter-specific activation gates precede connector availability; a connector being exposed does not mean it should be probed.
- Generic `UI / UX / interface / prototype / component / design system` requests do **not** activate Figma.
- Agent-executable connector or ACTIVE shared runtime precedes a manual web tool when both preserve the same native output and the adapter's activation gate has passed.
- A Candidate shared runtime is validation / training / support only unless explicitly labeled as bounded project reapplication.
- Existing editable project files/pages are reused before new SaaS files are created.
- Low-file/page-limit software must not become Global Current.
- `TOOL DOCUMENTED ≠ TOOL CALLABLE`; `CONNECTOR EXPOSED ≠ ADAPTER ACTIVATED ≠ UNLIMITED PLAN CAPACITY`; manual web execution never counts as agent execution.
- Tool convenience never authorizes loss of text editability, component structure, dimensions, geometry, coordinate systems, source identity or evidence state.

### Current software role matrix
| Need | Preferred execution | Optional / fallback | Hard boundary |
|---|---|---|---|
| Web/UI implementation | HTML/CSS/JS/SVG + real browser | Figma **explicit-only exception** after activation gate; Penpot manual only when a separate design workspace is genuinely required | Generic UI does not probe/recommend/create Figma; browser implementation evidence remains required |
| UI/vector design handoff | Editable repo-native SVG/HTML first | Figma only for explicit Figma delivery or existing authoritative Figma continuation/repair after capacity check | Figma is not a generic UI workspace; components/variables/Auto Layout/text stay native when Figma is explicitly required |
| Graphic / brand / packaging / POP | Editable vector/layout source | Figma for explicit handoff only; Illustrator/InDesign or equivalent only when already available or externally operated | Flattened raster is derivative; dieline/bleed/trim/text remain separable when applicable |
| Raster/image treatment | Agent-executable deterministic source transform when sufficient | **Candidate Pro Design Toolchain** deterministic raster for validation/support; Candidate Image Lab; Photopea manual fallback; Photoshop-equivalent only when already available | Candidate runtime ≠ Active; source authority remains unchanged; original source identity and pixel/color intent preserved; high-end subjective retouch remains specialist/HOLD when required |
| 3D/spatial/product/CMF | **Blender ACTIVE shared runtime** when callable and fit | **Candidate Pro Design Toolchain** for validated OpenBIM IFC / parametric solid CAD / bounded CAM validation; Candidate Spatial Lab; SketchUp Web manual fallback | Candidate IFC/STEP/CAM evidence does not unlock proprietary BIM/RVT, engineering approval, machine safety, Class-A or manufacturing approval; units and geometry authority remain explicit |
| Technical/vector drawing | Verified source dimensions + editable SVG/PDF-native chain | **Candidate Pro Design Toolchain** for validated DXF generation/readback; Candidate Technical SVG Lab; Figma only for explicit Figma handoff | AI/raster imagery has zero dimension authority; editable annotations retained; DXF generation does not prove GD&T/engineering/supplier approval |
| Data/GIS | Governed data + oleander-data-viz + SVG/HTML; QGIS/GDAL/GeoPandas when verified | bounded specialist adapter | Dataset/CRS/units remain authority, not decorative pixels |
| Motion | Browser motion or Blender ACTIVE runtime, depending output | **Candidate Pro Design Toolchain** FFmpeg deterministic post for validation/support; specialist video/motion software only when already available or externally operated | Candidate FFmpeg runtime ≠ specialist NLE/color finishing; actual state/frame readback required; rendered video does not prove editable source health |
| Deploy/share | Vercel connector when exposed and free/existing plan fits; GitHub Pages / Cloudflare Pages Free | manual deploy only if needed | Deploy PASS ≠ Browser PASS ≠ Design PASS |

### Figma explicit-only gate + capacity rule
Figma is an **explicit-request-only / existing-Figma-source handoff adapter**. It is not part of the generic UI routing path and must not be probed merely because the task concerns UI, UX, interfaces, prototypes, components or a design system.

Figma activation gate — at least one must already be true before probing the connector:
1. The user or Project Authority explicitly requires a Figma deliverable / editable Figma handoff; **or**
2. An existing authoritative Figma file/project must be continued, repaired or handed off.

Only after the activation gate passes:
1. Can the existing project file/page be reused instead of creating a new file?
2. Is current file/team capacity available without paid upgrade or deletion pressure?
3. Is recoverable repo/open-native source preserved outside Figma or is a recoverable handoff strategy recorded?

If the activation gate is not satisfied → **do not probe, recommend or create Figma**; route to repo-native production, another verified execution surface, or HOLD.

When Figma is explicitly required, keep components, variants, variables, Auto Layout and text native. A screenshot, flattened export or node-count receipt does not prove native editability or design quality.

Current connector/plugin check 2026-08-27:
- Figma connector: **installed / agent-executable when exposed, but explicit-gated and not probed for generic UI**.
- Penpot ChatGPT plugin: **not found**.
- Photopea ChatGPT plugin: **not found**.
- SketchUp ChatGPT plugin: **not found**.

## Real dimensions / geometry authority｜when physical scale matters
Required for spatial, architecture, landscape, interior, product, packaging structure, technical drawing and fabrication communication.

- Unit system:
- Scale / real-size basis:
- Dimension Authority source:
- Geometry Authority source:
- Origin / axis / coordinate reference when applicable:
- FIELD / Engineering / Manufacturing validation state when applicable:
- Recommended value + reasonable range + basis + sensitivity + FIELD check used where exact field data is unavailable?:

Hard rules:
- AI-generated imagery has **zero dimensional authority**.
- A perspective render has no hidden dimensional authority unless bound to verified geometry.
- A scale figure does not replace actual dimension data.
- Unknown field conditions stay OPEN; do not invent exact dimensions to make a drawing look finished.

## Text / vector editability contract
- UI labels, body copy, marketing copy, dimensions and annotations remain editable text or vector text in the master when editability is required.
- AI-rendered text is never a final text asset.
- Rasterized or outlined text is a derivative unless the production specification explicitly requires outlines.
- When production artwork requires outlined text, preserve the editable text source plus type specification / font provenance separately.

## AI-generated visual boundary
Default: **NONE / do not use unless active constraints allow it and it materially improves the required result**.

Allowed only as:
- supplemental effect render;
- reference visual;
- concept exploration;
- diagram support.

Never use as:
- Source Authority;
- dimension / engineering evidence;
- native editable master;
- final UI/system text;
- design-system component source;
- factual site/product proof without independent evidence.

If generated pixels conflict with verified source geometry, dimensions or facts, the verified source wins. Final text, labels, dimensions, components and system geometry must be rebuilt as real editable assets.

## Cross-software handoff ledger｜required for material tool / format transitions
| Object ID | Upstream master | Downstream tool/runtime | Exchange format | Units / scale / axis or canvas | Color / font / dependency policy | Editable information preserved | Known losses / bakes | Round-trip / reopen result | Hash / commit |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

Handoff FAIL conditions:
- undeclared unit / scale / axis / coordinate change;
- missing linked assets, fonts or texture dependencies;
- text, components or annotations flattened when editability is required;
- derivative replaces the master without explicit authority update;
- known information loss is hidden or unrecorded.

## Cloud-Free Studio Preflight｜after native output + owner set, before manual SaaS
Resolve each required capability in this order:

`AGENT_EXECUTABLE → CURRENT OLEANDER SKILL → SHARED_REPO_RUNTIME → FREE/INCLUDED CLOUD WHEN ACTUALLY EXPOSED → USER_WEB_MANUAL → CAPABILITY_HOLD`

Interpretation: the Current OLEANDER Skill / Owner is resolved **before this execution-surface list is applied**. The `SHARED_REPO_RUNTIME` production slot means **ACTIVE shared runtime only**. Adapter-specific activation gates are checked before an exposed connector may enter this list.

Current Cloud-Free repo surfaces are **CANDIDATE**, not default production runtimes:
- Responsive / visual staging → `browser-design-workbench/workbench.html`
- Bounded raster treatment / composition A-B → `browser-image-lab/image-lab.html`
- Concept spatial proxy / camera / scale → `browser-spatial-lab/spatial-lab.html`
- Technical vector / packaging / POP preflight → `browser-technical-svg-lab/technical-svg-lab.html`
- Professional OpenBIM IFC / parametric solid CAD / DXF / bounded CAM postprocess / deterministic raster / FFmpeg validation → `90-shared/toolchains/pro-design` — **runtime-smoke validated Candidate**, evidence: GitHub Actions run `33047483244` / run #16 / commit `16672434ec9798324b6419d37b4b5101d07d8767`; machine safety, engineering approval, proprietary BIM/RVT and Class-A remain HOLD.

Candidate surface rule: `VALIDATION / TRAINING / SUPPORT / BOUNDED PROJECT REAPPLICATION WITH EXPLICIT CANDIDATE LABEL` only. A Candidate surface must **not** become `DEFAULT_PRODUCTION_OWNER`, `SOLE_FINAL_NATIVE_OUTPUT_AUTHORITY`, or an unlabeled Current production route. Default production routing requires an **ACTIVE** runtime.

Do **not** route first to Penpot / Photopea / SketchUp Web merely because they are familiar. They are manual fallbacks when Current Skill + agent-executable surface + ACTIVE shared runtime cannot preserve the Required Native Output. Figma is not a generic fallback: it is only considered after its explicit-delivery / existing-Figma-source activation gate has already passed.

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
| OpenBIM / IFC | | | | | | | |
| Parametric solid CAD / STEP | | | | | | | |
| CAM / postprocessor / G-code | | | | | | | |
| 3D viewing | | | | | | | |
| Technical/vector / DXF preflight | | | | | | | |
| Build / compute | | | | | | | |
| Deploy / share | | | | | | | |

A conversation cannot write `EXECUTED` unless that surface was actually probed and used in that run.

## Capability State
- Browser-native capability:
- Current OLEANDER Skill capability:
- Agent-executable connector capability:
- ACTIVE shared repository runtime capability:
- Candidate shared repository runtime capability:
- Validated Candidate runtime evidence / run / commit:
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
- Input / upstream master:
- Output format:
- Editable information preserved?:
- Known loss / bake:
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
- Actual browser / pixel / interaction / model readback:
- Master-source reopen / editability readback:
- Cross-software handoff readback:
- Evidence Gate:
- Design Quality Gate:
- Runtime / Browser Gate:
- Engineering / Manufacturing / Field boundary:
- Does not prove:

`SOURCE READBACK / CI / VALIDATOR PASS ≠ BROWSER PASS ≠ DESIGN PASS`.  
`INTERNAL CRIT ≠ INDEPENDENT REVIEW`.  
`DERIVATIVE LOOKS CORRECT ≠ NATIVE MASTER HEALTHY`.

## Transaction Policy｜minimum sufficient process
Default for one logical object: **one Production PR** carries:

`IMPLEMENTATION → ACTUAL READBACK → INTERNAL CRIT → ROOT CAUSE → REPAIR → RETEST`

Independent Review should be a PR Review or isolated review record bound to the exact artifact hash. A separate review-only PR is **not** the default and is used only when explicit organizational/regulatory separation requires it.

`NO COMPRESSION / NO LOSS` protects information and evidence, not process length.

## Design-environment Definition of Done
A production transaction cannot claim its design environment is closed until all applicable items are resolved:

- [ ] Current editable master identified and reopenable.
- [ ] Source Authority bound to the master / design decision chain.
- [ ] Native master and delivery derivatives are explicitly separated.
- [ ] Unit / scale / dimension / geometry authority recorded when physical scale matters.
- [ ] Text, annotations, tokens/components and system assets remain editable when required.
- [ ] Software role + execution surface + lifecycle + capacity boundary recorded.
- [ ] Material cross-software transitions have a typed handoff record and known-loss statement.
- [ ] Any AI-generated visual is supplemental, traceable and non-authoritative.
- [ ] Actual visual/runtime/model/physical readback executed as applicable.
- [ ] Blocking review defects are repaired or explicitly HOLD.
- [ ] Recoverable Current master + required derivatives are persisted.
- [ ] No parallel competing Current master was created.