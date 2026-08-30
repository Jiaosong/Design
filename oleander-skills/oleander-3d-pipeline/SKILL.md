---
name: oleander-3d-pipeline
description: Plan, build, exchange, render, and audit Oleander 3D assets. Use whenever the user mentions Oleander 3D models, Blender, Rhino, Grasshopper, Maya, 3ds Max, SketchUp, Houdini, Unreal, D5, KeyShot, VRED, geometry nodes, procedural studies, polygon/SubD/NURBS modeling, retopology, UV/baking, material nodes, texture processing, technical art, plugins, axonometric drawings, exploded views, material libraries, cameras, animation, FBX, glTF, USD, texture paths, or render handoff.
compatibility: Capability-first and per-run probed. Blender ACTIVE shared runtime is preferred when callable and fit; other 3D/CAD/render tools such as Rhino/Grasshopper, Maya, 3ds Max, SketchUp, Houdini, Cinema 4D, Unreal/Epic, D5, KeyShot, VRED, Adobe tools, FFmpeg, or specialist CAD/BIM tools may be used only when the actual execution environment is available and preserves the Required Native Output. No local installation or installed-software state is assumed globally.
---

# Oleander 3D Pipeline

Inherit `00-governance/runtime/OLEANDER_DESIGN_ENVIRONMENT_PRODUCTION_CONTRACT_v1.0.json` for master/derivative separation, software handoff, dimension authority, text editability and AI-generated-visual boundaries. This Skill does not create a second environment policy.

Keep one authoritative editable model per asset and treat downstream scene files, exchange files, renders, screenshots and viewers as typed derivatives unless Project Authority explicitly promotes another source. Avoid silent scale, coordinate, material, texture, unit, axis or authority changes.

## 3D production knowledge route

For any modeling, surfacing, procedural, texturing, lighting, rendering, technical-art, runtime or plugin task, read:

`oleander-skills/oleander-3d-pipeline/3D_PRODUCTION_KNOWLEDGE_ROUTING.md`

For spline/NURBS structure, half-edge/Euler topology, UV parameterization/distortion, smoothing/fairing, robust Boolean/intersection, or Subdivision limit-surface diagnosis, also read:

`oleander-skills/oleander-3d-pipeline/MODELING_ESSENCE_DEEP_DIAGNOSTICS.md`

Its Current Notion owner is:

`FW-CG-3D-PRODUCTION-001｜3D Production Knowledge Stack｜建模—程序化—表面—材质—渲染—技术美术`.

Required routing behavior:

- choose the representation/modeling paradigm before choosing a software worker;
- resolve `KN-THEORY-3D-MODELING-ESSENCE-001` before treating a modeling command or software worker as the method;
- use `KN-METHOD-OLEANDER-3D-MODELING-001` for the default evidence-first/coarse-to-fine modeling sequence;
- route spline/NURBS basis, degree/CV/knot/multiplicity/weight issues through the deep modeling diagnostics rather than equating control density with accuracy;
- route connectivity edits, UV parameterization, fairing/smoothing, Boolean robustness and SubD limit-surface issues through their deep modeling diagnostics before software-specific fixes;
- route Rhino/NURBS/industrial surface work to the Rhino surface method + surface-continuity evidence;
- route Blender native/GN, Maya, 3ds Max, SketchUp, Houdini and Grasshopper work to their corresponding Current method/evidence objects;
- route sculpt/retopo/UV/bake/displacement/decal work to Surface Detail Production;
- route shader nodes/texture selection/processing/Substance work to Shading & Texturing plus the applicable CG BSDF/color evidence;
- route lighting/rendering to Rendering & Lighting Production plus radiometry/transport/color evidence;
- route LOD/instances/shader cost/runtime/export/profiling to 3D Technical Art;
- route addon/plugin choices through Plugin & Toolchain Governance, and never infer that a REVIEW plugin candidate is installed or approved;
- preserve software-specific version/runtime uncertainty; documentation synthesis alone is not M6 PRACTICED.

Stable principle: **software is a Worker, not the design method or authority**.

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

## Computer graphics quality route

For any task that makes a retained claim about 3D form, surface quality, material appearance, lighting, render quality, or cross-renderer visual fidelity, read:

`oleander-skills/oleander-3d-pipeline/COMPUTER_GRAPHICS_QUALITY_LAYER.md`

Apply its causality order and **CG-Q01—CG-Q10** before treating a render as quality evidence.

Required behavior:

- diagnose `geometry/silhouette/section → curvature/normals → BSDF/material → lighting/transport → sampling/denoise → color/display` in causal order;
- keep source-control density, evaluated-surface density, surface fairness, and design quality separate;
- use silhouette, neutral diffuse, and reflective/grazing diagnostic carriers when the form/surface claim requires them;
- treat lighting as a surface-measurement rig before hero lighting becomes an aesthetic tool;
- treat roughness, metalness, IOR, coat, transmission and other shader controls as representation parameters unless backed by physical/sample evidence;
- separate color textures from non-color/data maps and verify target-renderer channel/tangent semantics;
- do not use fixed universal sample counts or one "premium material" preset; diagnose the actual light paths and target viewing distance;
- lock working/view/display/exposure in controlled A/B comparisons;
- compare noisy vs denoised output when denoise could erase the feature under review;
- perform representative cross-renderer calibration/readback when appearance must survive export.

Hard boundary: `CG QUALITY PASS ≠ PHYSICAL MATERIAL TRUTH ≠ ENGINEERING / MANUFACTURING PASS ≠ DESIGN KEEP`.

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
- For form/surface claims, the applicable CG-Q01—CG-Q10 checks and diagnostic carriers have been executed rather than replaced by a hero render.
- Material class/BSDF semantics, texture color-vs-data encoding, light rig, sample/denoise policy, and color pipeline are explicit when they materially affect appearance.
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

When the computer-graphics quality route is triggered, also return or retain the applicable CG-Q01—CG-Q10 status, diagnostic-carrier identities, material/texture semantic notes, sampling/denoise policy, color-pipeline lock, and target-renderer readback status.

For parametric CAD/assembly work, also return the named parameter/datum contract, deterministic geometry checks actually executed, purchased-component provenance or proxy boundary, diagnostic visual readback, source repair/retest record, and remaining manufacturing/engineering HOLD.

For OpenSCAD/fabrication work, also return the `.scad` source identity, user-parameter contract, derived/reference-frame logic, process/orientation context, fabrication derivative identities, target-tool reopen when available, and physical fit/strength/finish HOLD.