---
name: oleander-3d-pipeline
description: Plan, build, exchange, render, and audit Oleander 3D assets. Use whenever the user mentions Oleander 3D models, Rhino, Grasshopper, RhinoCode, Rhino.Compute, Blender, Maya, Houdini, Unreal, D5, KeyShot, VRED, geometry nodes, procedural studies, axonometric drawings, exploded views, material libraries, cameras, animation, FBX, glTF, USD, texture paths, or render handoff.
compatibility: Works with installed Rhino/Grasshopper execution nodes when explicitly connected, plus installed Blender, Maya, Houdini, Cinema 4D, Unreal/Epic, D5, KeyShot, VRED, Adobe tools, and FFmpeg.
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

## Rhino + Grasshopper real-runtime rule

When a task requires a real Rhino or Grasshopper result, first determine whether a live runtime is actually connected.

- `rhino3dm`, generic Python geometry, DXF generation, SVG, GLB, or an offline Grasshopper-like data structure are **surrogate outputs**, not Rhino/Grasshopper runtime evidence.
- A real desktop Practice run requires a live Rhino process plus Grasshopper SDK execution, preferably through the governed `runtime/rhino-grasshopper` adapter.
- For GUI-dependent evidence such as Parameter Viewer or viewport comparison, preserve the real `.gh`, Grasshopper canvas capture, Rhino viewport capture, runtime manifest and receipt.
- Rhino.Compute may be used for real headless Grasshopper solving and batch evaluation, but must not be used to claim GUI evidence that Compute did not render.
- Keep `UNKNOWN`, `OPEN` and `HOLD` states intact when the runtime or evidence is missing.
- Do not promote a successful script dispatch or zero exit code into design, engineering, safety or acceptance approval.

## Required output

Return a model manifest, exchange report, render settings, asset dependency list, known limitations, and review images alongside the requested model/render. For real Rhino/Grasshopper tasks, additionally return the runtime manifest, job receipt, `.gh` or source definition, tree/parameter report as applicable, and real canvas/viewport evidence.
