---
name: oleander-3d-pipeline
description: Plan, build, exchange, render, and audit Oleander 3D assets. Use whenever the user mentions Oleander 3D models, Blender, Maya, Houdini, Unreal, D5, KeyShot, VRED, geometry nodes, procedural studies, axonometric drawings, exploded views, material libraries, cameras, animation, FBX, glTF, USD, texture paths, or render handoff.
compatibility: Capability-first and per-run probed. Blender ACTIVE shared runtime is preferred when callable and fit; other 3D/CAD/render tools such as Maya, Houdini, Cinema 4D, Unreal/Epic, D5, KeyShot, VRED, Adobe tools, FFmpeg, or specialist CAD/BIM tools may be used only when the actual execution environment is available and preserves the Required Native Output. No local installation or installed-software state is assumed globally.
---

# Oleander 3D Pipeline

Inherit `00-governance/runtime/OLEANDER_DESIGN_ENVIRONMENT_PRODUCTION_CONTRACT_v1.0.json` for master/derivative separation, software handoff, dimension authority, text editability and AI-generated-visual boundaries. This Skill does not create a second environment policy.

Keep one authoritative editable model per asset and treat downstream scene files, exchange files, renders, screenshots and viewers as typed derivatives unless Project Authority explicitly promotes another source. Avoid silent scale, coordinate, material, texture, unit, axis or authority changes.

## Blender Workbench existing-first route

`oleander-3d-pipeline` is the single installed 3D owner. Blender Runtime modules, CAD sidecars, validation scripts and workbench UI are implementation layers under this Skill, not separate Skills or parallel Current authorities.

Before extending or modifying Blender behavior:

1. resolve the active Project/Object Current, Source Authority, Required Native Output and production Blender runtime;
2. read `BLENDER_RUNTIME_CAPABILITY.json`, `PROFESSIONAL_PARITY_STATUS.json`, and, when working on an unmerged runtime branch, `blender_runtime/CANDIDATE_GOVERNANCE.json`;
3. route to an existing implementation module before creating any new module, workflow or abstraction;
4. use specialist CAD/BIM/Class-A/CAE/CAM kernels only when the Required Native Output needs them and runtime probing proves them callable;
5. after any material runtime change, align Skill routing, capability/status records, Workbench extension, Runtime README, Candidate governance and the matching Notion Current control surface in the same closure cycle, then run the smallest applicable real-runtime regression and readback.

Existing module families are reused as follows:

- identity / audit / dependencies / diff -> `properties.py`, `audit.py`, `dependency.py`, `geometry_diff.py`, `review_state.py`;
- direct and non-destructive feature editing -> `direct_model.py`, `feature_stack.py`, `feature_edit.py`;
- dimensions / guides / datum / inference -> `measurement_system.py`, `measurement_atomic.py`, `angular_datum.py`, `precision_inference.py`, `inference_engine.py`;
- relations / one-shot correction / configurations -> `relation_kernel.py`, `relation_apply.py`, `configuration.py`, `configuration_ops.py`;
- governed design-intent mutation / rebuild / procedural state -> `design_intent.py`, `design_intent_apply.py`, `design_intent_batch.py`, `design_intent_rebuild.py`, `procedural.py`;
- mesh clearance / surface diagnostics -> `mesh_clearance.py`, `surface_diagnostics.py`;
- authoritative B-Rep handoff -> `professional_adapter/cad_sidecar.py` plus the approved specialist CAD route. Blender remains a display/review derivative when CAD native geometry is authority.

If an existing module can carry roughly 60% or more of the requirement, extend or compose it. Do not create `oleander-blender-skill`, assembly Skill, CAD Skill, second Runtime Current, parallel Workbench framework, or one-off professional workflow to bypass an existing owner. A new implementation object requires an actual material capability gap plus authority and anti-pollution preflight.

Historical per-stage Blender receipts remain provenance. Current-source compatibility must be re-probed against the production runtime authority before promotion; a Candidate branch does not become installed Current merely because its tests pass.

## Before modeling

Record:

- asset/scene purpose;
- authoritative editable master object ID and path/locator;
- authoring application and version;
- unit system and real-world scale;
- dimension and geometry authority source;
- world origin and north/up axis;
- coordinate reference or survey benchmark when spatial;
- field / engineering / manufacturing validation state when applicable;
- required LOD and final camera distance;
- target render and exchange formats;
- any AI-generated visual role, default `NONE`.

If exact field dimensions are unavailable, do not invent them for visual completeness. Use a recommended value + reasonable range + basis + sensitivity + explicit FIELD verification item where the project allows design estimates.

## Naming and folders

Use stable ASCII identifiers for machine-facing names:

`OLE_[zone]_[discipline]_[asset]_[variant]_[lod]_v###`

Keep geometry, textures, references, caches, cameras, lighting, exports, renders, generated supplements and review files separable within the project's approved folder architecture. Do not create a duplicate folder system merely to satisfy the Skill. Use relative texture paths inside the project package.

There must be one Current master pointer per logical 3D object. A GLB, FBX, OBJ, screenshot or rendered image does not silently become that master.

## Parametric CAD / assembly route

When the Required Native Output includes parametric product/mechanical CAD, STEP/STP, fit-critical geometry, assemblies, mating interfaces, purchased components or technical-drawing geometry, read:

`oleander-skills/oleander-3d-pipeline/PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION.md`

Use the project-fit professional CAD runtime only when actually available. Preserve the editable parametric/native source as authority, expose meaningful parameters/datums, validate specified dimensions and assembly relations deterministically, and use visual CAD snapshots only as diagnostic evidence. A viewer, mesh or manually dragged assembly pose does not certify geometry.

## OpenSCAD / parametric fabrication route

When the Required Native Output is an editable `.scad` source for a parameter-driven fabricated part, read:

`oleander-skills/oleander-3d-pipeline/OPENSCAD_PARAMETRIC_FABRICATION_EXTENSION.md`

Use this route for source-parameter discipline, stable reference-frame/anchor relations, boolean robustness, fabrication-orientation reasoning and mesh/3MF/STL derivative tracking. Keep printer/material/slicer settings as a separate versioned fabrication context. Do not import BOSL2, fixed print parameters or one printer profile as an OLEANDER default.

For fit-critical interfaces, named purchased components or assembly relations, co-route from OpenSCAD to `PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION.md`; OpenSCAD source validity alone does not certify the fit.

## Exchange strategy

- USD: complex scene interchange and variants when supported.
- glTF/GLB: real-time review and lightweight delivery.
- FBX: animation or compatibility bridge.
- OBJ: static geometry fallback.
- Alembic: baked geometry animation/cache.
- EXR: high-dynamic-range render passes.
- STEP/STP: preferred inspectable exchange for parametric mechanical/product CAD when supported by the authoritative CAD route; preserve the native parametric source and do not confuse STEP validity with engineering approval.
- 3MF/STL: mesh/fabrication derivatives when required by the actual fabrication toolchain; preserve the parametric/native source when continuation matters and verify units/metadata/tool reopen as applicable.

Run a round-trip or reopen test before committing a full scene. Every material cross-software handoff records:

- object ID and upstream master;
- upstream/downstream tool or runtime;
- exchange format;
- units, scale, origin/axis or coordinate state;
- linked textures/dependencies;
- material/color-management assumptions;
- editable information preserved;
- known losses, triangulation, modifier baking, animation baking or texture baking;
- reopen/round-trip result;
- hash/commit when material.

An undeclared unit/axis change, missing dependency or hidden bake is a handoff FAIL.

## Dimension and geometry authority

For spatial/product/CMF/technical work:

- real dimensions come from verified geometry, technical sources or explicit governed estimates, not rendered pixels;
- AI-generated imagery has zero dimensional authority;
- a perspective render has no hidden geometry authority unless it is demonstrably bound to the verified model;
- a browser 3D viewer proves viewing only and cannot replace required CAD/BIM/Class-A/manufacturing authoring;
- field, engineering and manufacturing claims remain OPEN unless separately validated.

For parametric CAD, also keep `source intent → named parameters/datums → generated geometry → deterministic measurement/alignment/topology checks` traceable. Visual suspicion must be converted into a geometry check before becoming a validation conclusion.

For OpenSCAD/fabrication, keep public parameters, derived dimensions, reference frames, process orientation and exported mesh derivatives traceable back to the `.scad` source. A boolean workaround/epsilon is a modeling-kernel device, not a manufacturing tolerance.

## AI-generated visual boundary

Default to no generative image use unless active project/user constraints explicitly allow it and it materially helps.

When allowed, AI imagery may be used only as a supplemental effect render, reference visual, concept exploration or diagram-support layer. It must not become:

- model or geometry authority;
- dimension/engineering evidence;
- texture/material specification without independent source evidence;
- final technical annotation or text;
- the only recoverable representation of the design.

If generated pixels conflict with verified model geometry, dimensions or source facts, the verified source wins.

## Axonometric and analysis output

1. Lock camera type, orientation, scale, crop, and north reference.
2. Separate layers by analytical meaning.
3. Export clean linework/vector geometry when possible.
4. Export render passes for color, shadow, depth, object/material ID, and ambient occlusion as needed.
5. Keep labels, dimensions and explanatory graphics outside the 3D master unless they are true spatial objects.
6. Keep final labels, dimensions and explanatory text editable/vector; rasterized or AI-rendered text is not final technical text.

## Handoff checklist

- Current authoritative editable model is identifiable and reopenable.
- Units and bounding box are plausible and bound to the declared dimension authority.
- Normals, transforms, pivots, instancing, and modifiers are resolved intentionally.
- For fit/assembly CAD, local frames, functional datums, mating intent and relevant dimensions are explicit and checked.
- For OpenSCAD/fabrication, public parameters, derived dimensions, stable reference relations and source→mesh/export lineage are explicit.
- Named off-the-shelf components use a traceable real model when available, or a documented envelope/proxy with uncertainty.
- No missing or absolute-path textures.
- Material names are unique and meaningful.
- Cameras, frame rate, frame range, and color management are documented.
- External plugins and licenses are listed.
- Cross-software exchange records known losses/bakes and passes reopen/round-trip when applicable.
- A low-resolution review file and thumbnail are included.
- Renders/viewers/AI supplements are clearly derivatives, not master replacements.

## Required output

Return a model manifest, Current-master identity, dimension/geometry authority record, exchange report, typed cross-software handoff record when applicable, render settings, asset dependency list, known limitations, and review images alongside the requested model/render.

For parametric CAD/assembly work, also return the named parameter/datum contract, deterministic geometry checks actually executed, purchased-component provenance or proxy boundary, diagnostic visual readback, source repair/retest record, and remaining manufacturing/engineering HOLD.

For OpenSCAD/fabrication work, also return the `.scad` source identity, user-parameter contract, derived/reference-frame logic, process/orientation context, fabrication derivative identities, target-tool reopen when available, and physical fit/strength/finish HOLD.