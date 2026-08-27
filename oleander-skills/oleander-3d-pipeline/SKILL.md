---
name: oleander-3d-pipeline
description: Plan, build, exchange, render, and audit Oleander 3D assets. Use whenever the user mentions Oleander 3D models, Blender, Maya, Houdini, Unreal, D5, KeyShot, VRED, geometry nodes, procedural studies, axonometric drawings, exploded views, material libraries, cameras, animation, FBX, glTF, USD, texture paths, or render handoff.
compatibility: Capability-first and per-run probed. Blender ACTIVE shared runtime is preferred when callable and fit; other 3D/CAD/render tools such as Maya, Houdini, Cinema 4D, Unreal/Epic, D5, KeyShot, VRED, Adobe tools, FFmpeg, or specialist CAD/BIM tools may be used only when the actual execution environment is available and preserves the Required Native Output. No local installation or installed-software state is assumed globally.
---

# Oleander 3D Pipeline

Inherit `00-governance/runtime/OLEANDER_DESIGN_ENVIRONMENT_PRODUCTION_CONTRACT_v1.0.json` for master/derivative separation, software handoff, dimension authority, text editability and AI-generated-visual boundaries. This Skill does not create a second environment policy.

Keep one authoritative editable model per asset and treat downstream scene files, exchange files, renders, screenshots and viewers as typed derivatives unless Project Authority explicitly promotes another source. Avoid silent scale, coordinate, material, texture, unit, axis or authority changes.

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

## Exchange strategy

- USD: complex scene interchange and variants when supported.
- glTF/GLB: real-time review and lightweight delivery.
- FBX: animation or compatibility bridge.
- OBJ: static geometry fallback.
- Alembic: baked geometry animation/cache.
- EXR: high-dynamic-range render passes.

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
- No missing or absolute-path textures.
- Material names are unique and meaningful.
- Cameras, frame rate, frame range, and color management are documented.
- External plugins and licenses are listed.
- Cross-software exchange records known losses/bakes and passes reopen/round-trip when applicable.
- A low-resolution review file and thumbnail are included.
- Renders/viewers/AI supplements are clearly derivatives, not master replacements.

## Required output

Return a model manifest, Current-master identity, dimension/geometry authority record, exchange report, typed cross-software handoff record when applicable, render settings, asset dependency list, known limitations, and review images alongside the requested model/render.