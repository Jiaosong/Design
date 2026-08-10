---
name: oleander-3d-pipeline
description: Plan, build, exchange, render, and audit Oleander 3D assets. Use whenever the user mentions Oleander 3D models, Blender, Maya, Houdini, Unreal, D5, KeyShot, VRED, Rhino, Grasshopper, geometry nodes, procedural studies, axonometric drawings, exploded views, material libraries, cameras, animation, FBX, glTF, USD, texture paths, or render handoff.
compatibility: Works with available installed or connected 3D runtimes. Rhino/Grasshopper evidence must follow the runtime adapter under runtime/rhino-grasshopper; offline geometry libraries are surrogate-only.
---

# Oleander 3D Pipeline

Keep one authoritative model per asset and treat downstream scene files as derived outputs. Avoid silent scale, coordinate, material, or texture changes.

## Before modeling

Record:

- asset/scene purpose;
- authoring application and version;
- unit system and real-world scale;
- world origin and north/up axis;
- coordinate reference or survey benchmark when spatial;
- required LOD and final camera distance;
- target render and exchange formats.

## Naming and folders

Use stable ASCII identifiers for machine-facing names:

`OLE_[zone]_[discipline]_[asset]_[variant]_[lod]_v###`

Keep geometry, textures, references, caches, cameras, lighting, exports, renders, and review files separate. Use relative texture paths inside the project package.

## Rhino + Grasshopper runtime hierarchy

When Rhino or Grasshopper is part of a task, distinguish four execution modes:

1. `FREE_PUBLIC_COMPUTE` — no-user-workstation, no-paid fallback; may provide real headless evidence only when the public service actually returns a Grasshopper solve.
2. `PRIVATE_COMPUTE` — private/self-hosted headless runtime; cost/credentials require explicit Human Authority.
3. `DESKTOP_RHINO` — desktop runtime capable of GUI/canvas/viewport evidence; optional, never assumed connected.
4. `SURROGATE_OFFLINE` — Python, rhino3dm, DXF, SVG or equivalent prechecks only.

Evidence rules:

- code existing in GitHub is not runtime evidence;
- CI success is not a Rhino/Grasshopper solve unless the runtime receipt proves the solve;
- headless runtime may support data/tree/geometry results but cannot close GUI-specific checkpoints;
- offline/surrogate output never upgrades directly to `REAL_HEADLESS_GRASSHOPPER_EVIDENCE` or desktop evidence;
- preserve service/auth/network/definition failures as blockers rather than hiding them with a fallback;
- never silently activate a paid `RHINO_TOKEN` path from `FREE_PUBLIC_COMPUTE`.

Current FREE_PUBLIC_COMPUTE evidence (2026-08-10): actual GitHub-hosted request to McNeel public `/grasshopper` returned HTTP 404 with `This server has been turned off`; SP02 CP2 remains OPEN with `PUBLIC_SERVICE_DISABLED`, and CP4 remains OPEN because headless mode has no Parameter Viewer GUI evidence.

## Exchange strategy

- USD: complex scene interchange and variants when supported.
- glTF/GLB: real-time review and lightweight delivery.
- FBX: animation or compatibility bridge.
- OBJ: static geometry fallback.
- Alembic: baked geometry animation/cache.
- EXR: high-dynamic-range render passes.

Run a round-trip test before committing a full scene.

## Axonometric and analysis output

1. Lock camera type, orientation, scale, crop, and north reference.
2. Separate layers by analytical meaning.
3. Export clean linework/vector geometry when possible.
4. Export render passes for color, shadow, depth, object/material ID, and ambient occlusion as needed.
5. Keep labels and explanatory graphics outside the 3D master unless they are spatial objects.

## Handoff checklist

- Units and bounding box are plausible.
- Normals, transforms, pivots, instancing, and modifiers are resolved intentionally.
- No missing or absolute-path textures.
- Material names are unique and meaningful.
- Cameras, frame rate, frame range, and color management are documented.
- External plugins and licenses are listed.
- A low-resolution review file and thumbnail are included.
- Runtime mode and evidence level are explicit.
- Any UNKNOWN / HOLD / blocker survives handoff.

## Required output

Return a model manifest, exchange report, render settings, asset dependency list, known limitations, runtime/evidence status, and review images alongside the requested model/render.
