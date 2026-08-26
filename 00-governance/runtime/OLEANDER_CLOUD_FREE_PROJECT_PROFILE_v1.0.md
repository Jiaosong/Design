# OLEANDER Cloud-Free Project Profile v1.0

Status: **CANDIDATE RUNTIME PROFILE**  
Date: **2026-08-26**  
Parent runtime: `OLEANDER_UNIVERSAL_PRODUCTION_ENVIRONMENT_v1.0`  
Scope: **Project execution when the active user constraints are browser-first / no local install / no new paid dependency**

## 0｜Role

This file is a **runtime profile**, not a new METHOD, Skill, framework, Gate or replacement production environment.

It specializes the existing Universal Production Environment under the active constraints:

- `NO_LOCAL_INSTALL_REQUIRED`
- `NO_NEW_PAID_DEPENDENCY`
- `STOP_AT_FREE_LIMIT`
- `BROWSER_FIRST`

The Universal Production Environment remains authority for capability routing. This profile only narrows eligible adapters when these constraints are active.

## 1｜Hard rules

1. Do not require the user to install Blender, Photoshop, Illustrator, CAD/BIM, Node, Python, FFmpeg or CLI software on their own computer.
2. Do not require a new paid software license, paid plugin, paid render farm, paid cloud VM, paid hosting plan or paid design SaaS for project continuity.
3. Free-quota services must stop at their included quota. Do not enable paid overage as an execution requirement.
4. Tool choice still follows `Required Native Output`; free/browser constraints do **not** authorize lowering the professional requirement or replacing a missing professional output with a fake equivalent.
5. If no browser/free adapter preserves the required information and professional boundary, return only the affected capability as `CAPABILITY_HOLD`.
6. Existing source/model/artifact reuse is preferred over recreating work only because a browser-native authoring tool is unavailable.
7. `BROWSER VISIBLE ≠ NATIVE AUTHORITY`; `FREE TOOL AVAILABLE ≠ CAPABILITY PROVEN`; `DEPLOYED ≠ DESIGN PASS`.

## 2｜Default free/browser stack

| Need | Default adapter | Runtime role | Boundary |
|---|---|---|---|
| Source/code/SVG/JSON editing | GitHub Web + `github.dev` | PRIMARY | browser editing; `github.dev` is not a full compute runtime |
| Build/terminal when actually required | GitHub Codespaces included personal quota | CONDITIONAL | free quota only; stop at quota; prefer 2-core / short-lived sessions |
| Static site deploy/share | GitHub Pages or Cloudflare Pages Free | PRIMARY DEPLOY | static-first; functions only inside free allowance |
| Raster/manual image editing | Photopea Web | PRIMARY MANUAL RASTER | free browser editor; preserve source/derivative boundary |
| Vector / technical communication | editable SVG + browser preview | PRIMARY VECTOR | text, dimensions and annotation remain editable |
| Knowledge / project state | Notion | CURRENT KNOWLEDGE / PROJECT STATE | not sole storage for irreplaceable large binaries |
| Assets / originals / delivery packages | Google Drive | ASSET / ARCHIVE | Canonical Path + version + readback required |
| 3D display / interaction | Three.js / `<model-viewer>` + glTF/GLB | BROWSER VIEWER | viewer does not prove modeling capability |
| Complex new 3D / CAD / BIM authoring | no default browser-free owner | CAPABILITY HOLD | do not pretend viewer/SVG/AI image equals professional geometry authoring |

## 3｜Type → software routing

### Web / UI / interaction

`NOTION TYPE BRIEF → GITHUB SOURCE → github.dev → HTML/CSS/JS/SVG → REAL BROWSER → STATIC/FREE DEPLOY → DESKTOP/MOBILE/STATE READBACK`

Prefer native HTML/CSS/JS. Add libraries only when native browser capability cannot reasonably preserve the required interaction or production fidelity.

### Graphic / brand / packaging / Retail POP

`SOURCE ASSETS → EDITABLE SVG MASTER → BROWSER READBACK → PHOTOPEA ONLY IF RASTER TREATMENT IS NEEDED → SVG/PDF/PNG DERIVATIVES → DRIVE DELIVERY`

Illustrator/Photoshop are optional adapters, never required by this profile. Production layers such as `CUT_DIE / BLEED_WORKING / SAFE_WORKING / ARTWORK / LOCKED_ASSET_SLOT / NONPRINT_NOTES` should remain separately editable where applicable.

### Data Viz / GIS / diagrams

`CSV/JSON/GEOJSON → OLEANDER DATA-VIZ OWNER → SVG/HTML → BROWSER → PNG READBACK`

Use static SVG first. Use JS only for interaction. Geography/CRS/topology/evidence boundaries remain mandatory; browser convenience cannot rewrite data truth.

### Architecture / landscape / interior presentation

Use existing photos, current drawings, source geometry and verified assets first. Compose through SVG/HTML/PDF/browser where that preserves the intended output.

If the task requires genuinely new professional BIM/CAD/complex 3D geometry and no browser/free execution owner is available, return `CAPABILITY_HOLD`. Do not use AI imagery, a viewer, or a diagram as fake BIM/CAD evidence.

### Product / CMF

Use existing product geometry, product photography, browser 3D viewing, parametric/simple geometry and SVG technical communication where sufficient. Complex manufacturing surfaces / Class-A / production CAD remain `CAPABILITY_HOLD` unless a verified browser/free owner exists.

### Technical drawing / construction / engineering diagram

Use editable SVG/PDF for conceptual details, relationships, dimensions, exploded views and lineweight/annotation work where source inputs are sufficient. Real structural approval, signed engineering, supplier submittal and field acceptance remain outside this profile's proof authority.

### Motion

Prefer CSS / Web Animations API / JS / SVG motion when the final medium is Web or browser-native. External motion libraries are optional and must satisfy the plugin policy below.

## 4｜Plugin policy

Default: **NO PLUGIN**.

A plugin/library may be introduced only when all are true:

1. the Required Native Output actually needs it;
2. existing OLEANDER owner + browser native capability cannot reasonably cover the need;
3. it is usable without making paid continuation mandatory;
4. the core artifact remains exportable/recoverable in an open or documented format;
5. it does not become Source Authority merely because it generated an output;
6. version, purpose, owner, free boundary and fallback are recorded;
7. removal of the plugin does not destroy the only recoverable copy of the design.

Minimum plugin record:

`NAME / VERSION / TYPE / PURPOSE / REQUIRED? / FREE_LIMIT / SOURCE / OUTPUT_FORMAT / FALLBACK / LOCK_IN_RISK / STATUS`

## 5｜Free-quota safety

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

### Raster

Photopea is a browser-based raster/vector editor with a free account/basic usage path. It is a manual-editing fallback, not Source Authority and not evidence generation.

Official references:
- https://www.photopea.com/learn/
- https://www.photopea.com/api/accounts

## 6｜Project Environment Card

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
- `FREE_TIER_BOUNDARY`
- `SOURCE_AUTHORITY`
- `ASSET_LOCATION`
- `DELIVERY_TARGET`
- `READBACK_MATRIX`
- `CAPABILITY_HOLD`
- `FALLBACK`

## 7｜Fallback order

`BROWSER_NATIVE → CURRENT_OLEANDER_SKILL → FREE_WEB_TOOL → INCLUDED_FREE_QUOTA_CLOUD_COMPUTE → SIMPLIFY_EXECUTION_WITHOUT_INFORMATION_LOSS → CAPABILITY_HOLD`

Forbidden fallback:

`BUY_PAID_TOOL → ENABLE_PAID_OVERAGE → USE_AI_IMAGE_AS_FAKE_SOURCE → DELETE_PROFESSIONAL_REQUIREMENT → TREAT_PREVIEW_AS_NATIVE_AUTHORITY`

## 8｜Does not prove

This profile proves only that OLEANDER has a **browser-first / no-local-install / no-new-paid-dependency routing policy**.

It does not prove that every design/engineering domain can be completed professionally in a browser, that free tools equal full professional suites, that Three.js equals CAD/BIM, that a static deployment equals browser/design PASS, or that engineering/manufacturing/field approval has occurred.
