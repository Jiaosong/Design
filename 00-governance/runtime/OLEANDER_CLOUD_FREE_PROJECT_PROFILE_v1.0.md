# OLEANDER Cloud-Free Project Profile v1.0

Status: **ACTIVE CURRENT / GLOBAL OLEANDER DEFAULT**  
Date: **2026-08-26**  
Parent runtime: `OLEANDER_UNIVERSAL_PRODUCTION_ENVIRONMENT_v1.0`  
Scope: **ALL OLEANDER conversations and projects unless an explicit later project/user override changes the named constraints**

## 0｜Role

This file is a **runtime profile**, not a new METHOD, Skill, framework, Gate or replacement production environment.

It specializes the existing Universal Production Environment under the standing user constraints:

- `NO_LOCAL_INSTALL_REQUIRED`
- `NO_NEW_PAID_DEPENDENCY`
- `STOP_AT_FREE_LIMIT`
- `BROWSER_FIRST`

The Universal Production Environment remains authority for capability routing. This profile narrows eligible adapters while these constraints remain active.

### 0A｜Global activation / cross-conversation rule

The user explicitly activated this profile for **all OLEANDER conversations** on 2026-08-26.

Every OLEANDER conversation therefore resolves this profile after Current Authority / Source Authority and sticky constraints, before selecting production software or plugins. A generic follow-up such as `继续 / 优化 / 再做` does not deactivate it. Only an explicit later instruction allowing local installation, a new paid dependency or another named execution policy can override the affected constraint.

This activation makes the **routing policy and shared repository runtime** cross-conversation. It does **not** create a permanently running private workstation inside ChatGPT and it does not make every third-party website directly controllable by the agent. Every conversation must still probe whether a connector/runtime is actually exposed before claiming `EXECUTED`.

## 1｜Hard rules

1. Do not require the user to install Blender, Photoshop, Illustrator, CAD/BIM, Node, Python, FFmpeg or CLI software on their own computer.
2. Do not require a new paid software license, paid plugin, paid render farm, paid cloud VM, paid hosting plan or paid design SaaS for project continuity.
3. Free-quota services must stop at their included quota. Do not enable paid overage as an execution requirement.
4. Tool choice still follows `Required Native Output`; free/browser constraints do **not** authorize lowering the professional requirement or replacing a missing professional output with a fake equivalent.
5. If no browser/free adapter preserves the required information and professional boundary, return only the affected capability as `CAPABILITY_HOLD`.
6. Existing source/model/artifact reuse is preferred over recreating work only because a browser-native authoring tool is unavailable.
7. `BROWSER VISIBLE ≠ NATIVE AUTHORITY`; `FREE TOOL AVAILABLE ≠ CAPABILITY PROVEN`; `DEPLOYED ≠ DESIGN PASS`.
8. `TOOL DOCUMENTED ≠ TOOL CALLABLE IN THIS CONVERSATION`; actual connector/runtime availability must be probed per run.

## 2｜Execution-surface classes

Every software/plugin/runtime candidate must be classified before use:

- `AGENT_EXECUTABLE` — the current ChatGPT conversation exposes a connector/tool that can directly read/write/execute the target service or artifact.
- `SHARED_REPO_RUNTIME` — the capability is implemented as reusable GitHub source/runtime and can be consumed by OLEANDER conversations through the shared repository when the connector/runtime is exposed.
- `USER_WEB_MANUAL` — the service is free/browser-based, but the agent cannot directly operate that third-party UI; it may be recommended or used by the user without local installation.
- `VIEW_ONLY_OR_REFERENCE` — useful for viewing/reference, not authoritative authoring.
- `CAPABILITY_HOLD` — no verified free/no-local route preserves the required professional native output.

A documented free web app must never be promoted from `USER_WEB_MANUAL` to `AGENT_EXECUTABLE` without a real connector/tool probe.

## 3｜Default free/browser stack

| Need | Default adapter | Execution surface | Boundary |
|---|---|---|---|
| Source/code/SVG/JSON editing | GitHub connector + GitHub Web / `github.dev` | `AGENT_EXECUTABLE` when GitHub connector is exposed; otherwise browser manual | `github.dev` is not a full compute runtime |
| Knowledge / project state | Notion connector | `AGENT_EXECUTABLE` when exposed | Not sole storage for irreplaceable large binaries |
| Assets / originals / delivery packages | Google Drive connector | `AGENT_EXECUTABLE` when exposed | Canonical Path + version + readback required |
| Build/terminal when actually required | GitHub Actions / Codespaces included quota | `SHARED_REPO_RUNTIME` / conditional | free quota only; stop at quota |
| Static site deploy/share | GitHub Pages; Cloudflare/Vercel free route when verified | `SHARED_REPO_RUNTIME` or connector-conditional | static-first; no paid overage |
| Browser-native UI implementation | HTML/CSS/JS/SVG | `SHARED_REPO_RUNTIME` | real browser readback required |
| Raster/manual image editing | Photopea Web | `USER_WEB_MANUAL` | free browser editor; preserve source/derivative boundary |
| Visual UI design/prototyping | Penpot Cloud Professional free | `USER_WEB_MANUAL` unless a future verified connector exists | design/prototype workspace; exported/native recoverability required |
| Vector / technical communication | editable SVG + browser preview | `AGENT_EXECUTABLE` / `SHARED_REPO_RUNTIME` | text, dimensions and annotation remain editable |
| 3D concept authoring | SketchUp for Web free | `USER_WEB_MANUAL` | browser model authoring; free/subscription feature boundary must be respected |
| 3D display / interaction | Three.js / `<model-viewer>` + glTF/GLB | `SHARED_REPO_RUNTIME` | viewer does not prove modeling capability |
| Complex new 3D / CAD / BIM authoring | no default verified agent-executable free owner | `CAPABILITY_HOLD` | do not pretend viewer/SVG/AI image equals professional geometry authoring |

Current plugin discovery on 2026-08-26 found no installable ChatGPT plugin for Penpot or SketchUp. Therefore both remain `USER_WEB_MANUAL` rather than agent-executable adapters until a connector is actually available and verified.

## 4｜Type → software routing

### Web / UI / interaction

Agent-executable default:

`NOTION TYPE BRIEF → GITHUB SOURCE → HTML/CSS/JS/SVG → REAL BROWSER → STATIC/FREE DEPLOY → DESKTOP/MOBILE/STATE READBACK`

Optional visual design workspace:

`PENPOT (USER_WEB_MANUAL) → exported/open design source → GITHUB IMPLEMENTATION → REAL BROWSER READBACK`

Penpot does not become required and does not replace browser implementation evidence.

### Graphic / brand / packaging / Retail POP

`SOURCE ASSETS → EDITABLE SVG MASTER → BROWSER READBACK → PHOTOPEA USER_WEB_MANUAL ONLY IF RASTER TREATMENT IS NEEDED → SVG/PDF/PNG DERIVATIVES → DRIVE DELIVERY`

Illustrator/Photoshop are optional adapters, never required by this profile. Production layers such as `CUT_DIE / BLEED_WORKING / SAFE_WORKING / ARTWORK / LOCKED_ASSET_SLOT / NONPRINT_NOTES` should remain separately editable where applicable.

### Data Viz / GIS / diagrams

`CSV/JSON/GEOJSON → OLEANDER DATA-VIZ OWNER → SVG/HTML → BROWSER → PNG READBACK`

Use static SVG first. Use JS only for interaction. Geography/CRS/topology/evidence boundaries remain mandatory; browser convenience cannot rewrite data truth.

### Architecture / landscape / interior presentation

Agent-executable default uses existing photos, current drawings, source geometry and verified assets first, composed through SVG/HTML/PDF/browser where the required output is preserved.

For browser concept massing/spatial authoring, `SketchUp for Web` is a verified free browser option but remains `USER_WEB_MANUAL` because no direct ChatGPT connector is currently available. Its free mode does not authorize claims about paid-only features, BIM, production CAD or high-end visualization.

If genuinely new professional BIM/CAD/complex 3D geometry is required and no verified free agent-executable/shared runtime owner is available, return `CAPABILITY_HOLD`. Do not use AI imagery, a viewer, or a diagram as fake BIM/CAD evidence.

### Architecture visualization

Use real source imagery, existing verified geometry/renders and non-generative image treatment first. Browser/SVG/HTML composition can execute framing, sequencing, typography and presentation. From-zero high-end CGI remains `CAPABILITY_PARTIAL/HOLD` when the required lighting/material/render pipeline cannot be executed within this profile.

### Product / CMF

Use existing product geometry, product photography, browser 3D viewing, parametric/simple geometry and SVG technical communication where sufficient. Complex manufacturing surfaces / Class-A / production CAD remain `CAPABILITY_HOLD` unless a verified free agent-executable owner exists.

### Technical drawing / construction / engineering diagram

Use editable SVG/PDF for conceptual details, relationships, dimensions, exploded views and lineweight/annotation work where source inputs are sufficient. Real structural approval, signed engineering, supplier submittal and field acceptance remain outside this profile's proof authority.

### Motion

Prefer CSS / Web Animations API / JS / SVG motion when the final medium is Web or browser-native. External motion libraries are optional and must satisfy the plugin policy below.

## 5｜Plugin policy

Default: **NO PLUGIN**.

A plugin/library may be introduced only when all are true:

1. the Required Native Output actually needs it;
2. existing OLEANDER owner + browser native capability cannot reasonably cover the need;
3. it is usable without making paid continuation mandatory;
4. the core artifact remains exportable/recoverable in an open or documented format;
5. it does not become Source Authority merely because it generated an output;
6. version, purpose, owner, free boundary and fallback are recorded;
7. removal of the plugin does not destroy the only recoverable copy of the design;
8. `execution_surface_class` is recorded so another conversation knows whether it can actually call the plugin/service.

Minimum plugin record:

`NAME / VERSION / TYPE / PURPOSE / REQUIRED? / EXECUTION_SURFACE_CLASS / FREE_LIMIT / SOURCE / OUTPUT_FORMAT / FALLBACK / LOCK_IN_RISK / STATUS`

## 6｜Free-quota safety

### GitHub

- `github.dev` is the zero-compute default editor.
- Codespaces is burst compute only, not a permanent workstation.
- Current GitHub documentation (verified 2026-08-26) states personal GitHub Free accounts include **120 core-hours/month** and **15 GB-month storage** for Codespaces.
- If there is no payment method, GitHub blocks billable Codespaces use after the included quota is exhausted; this profile treats that state as `COMPUTE_HOLD`.
- Prefer low-core sessions and stop/delete inactive environments to conserve included usage.

Official references:
- https://docs.github.com/en/codespaces/the-githubdev-web-based-editor
- https://docs.github.com/en/billing/concepts/product-billing/github-codespaces

### Hosting

Static-first deployment is preferred.

Current Cloudflare documentation (verified 2026-08-26) states Pages static asset requests are free/unlimited on Free and paid plans; Free currently includes 500 builds/month and a 20,000-file site limit. Pages Functions share Workers Free-plan request limits.

Official references:
- https://developers.cloudflare.com/pages/functions/pricing/
- https://developers.cloudflare.com/pages/platform/limits/

GitHub Pages remains a valid zero-cost static-hosting option for eligible repositories under GitHub Free.

### UI design / prototyping

Penpot official pricing (verified 2026-08-26) lists the hosted Professional plan at `$0 / user / month`, with plugins, unlimited design files within storage capacity, up to 8 team members and up to 10 GB storage. Penpot remains `USER_WEB_MANUAL` until a connector is actually available.

Official reference:
- https://penpot.app/pricing

### Spatial concept modeling

SketchUp official documentation (verified 2026-08-26) states SketchUp for Web can be used without a subscription and can create/edit models in a browser with a Trimble ID; subscription unlocks additional features. SketchUp for Web remains `USER_WEB_MANUAL` until a connector is actually available.

Official references:
- https://help.sketchup.com/en/sketchup-web/sketchup-web
- https://help.sketchup.com/en/sketchup-web/web-features

### Raster

Photopea is a browser-based raster/vector editor with a free account/basic usage path. It is a manual-editing fallback, not Source Authority and not evidence generation.

Official references:
- https://www.photopea.com/learn/
- https://www.photopea.com/api/accounts

## 7｜Project Environment Card

Each P2 project should resolve only the fields it actually needs:

- `PROJECT_ID`
- `PRIMARY_DESIGN_OR_ENGINEERING_TYPE`
- `SUPPORTING_TYPES`
- `REQUIRED_NATIVE_OUTPUTS`
- `CURRENT_TYPE_BRIEF_OR_METHOD`
- `EXECUTION_OWNER_SET`
- `BROWSER_RUNTIME`
- `REQUIRED_SOFTWARE` — default `BROWSER_ONLY`
- `REQUIRED_PLUGINS` — default `NONE`
- `EXECUTION_SURFACE_CLASS`
- `FREE_TIER_BOUNDARY`
- `SOURCE_AUTHORITY`
- `ASSET_LOCATION`
- `DELIVERY_TARGET`
- `READBACK_MATRIX`
- `CAPABILITY_HOLD`
- `FALLBACK`

## 8｜Fallback order

`AGENT_EXECUTABLE_BROWSER_NATIVE → SHARED_REPO_RUNTIME → CURRENT_OLEANDER_SKILL → VERIFIED_FREE_WEB_TOOL → INCLUDED_FREE_QUOTA_CLOUD_COMPUTE → USER_WEB_MANUAL_OPTION → SIMPLIFY_EXECUTION_WITHOUT_INFORMATION_LOSS → CAPABILITY_HOLD`

Forbidden fallback:

`BUY_PAID_TOOL → ENABLE_PAID_OVERAGE → REQUIRE_USER_LOCAL_INSTALL → CLAIM_MANUAL_WEB_TOOL_AS_AGENT_EXECUTED → USE_AI_IMAGE_AS_FAKE_SOURCE → DELETE_PROFESSIONAL_REQUIREMENT → TREAT_PREVIEW_AS_NATIVE_AUTHORITY`

## 9｜Does not prove

This profile proves that OLEANDER has an **ACTIVE cross-conversation browser-first / no-local-install / no-new-paid-dependency routing policy** and a shared machine-readable repository configuration.

It does not prove that ChatGPT has a permanently running private workstation, that every third-party website is agent-controllable, that every design/engineering domain can be completed professionally in a browser, that free tools equal full professional suites, that Three.js equals CAD/BIM, that a static deployment equals browser/design PASS, or that engineering/manufacturing/field approval has occurred.
