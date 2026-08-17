---
name: oleander-3d-pipeline
description: Plan, build, exchange, render, and audit Oleander 3D assets. Use whenever the user mentions Oleander 3D models, Blender, Maya, Houdini, Unreal, D5, KeyShot, VRED, geometry nodes, procedural studies, axonometric drawings, exploded views, material libraries, cameras, animation, FBX, glTF, USD, texture paths, or render handoff.
compatibility: Works with installed Blender, Maya, Houdini, Cinema 4D, Unreal/Epic, D5, KeyShot, VRED, Adobe tools, and FFmpeg.
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

## Cross-media correspondence gate

Use this gate whenever the same design object is represented in more than one of: plan, section, axonometric, model view, render, diagram, or interactive spatial view.

1. Declare stable correspondence anchors before styling. Use durable IDs for the minimum set of places, joints, edges, route decisions, datum points, or objects that must remain recognisable across media.
2. Separate invariants from reprojectable properties. Anchor identity, order, adjacency, side-of-relation, and design role are invariant; camera, projection, crop, graphic style, and local silhouette may change when the medium requires it.
3. A shared label is not evidence of correspondence by itself. If two views carry the same ID but depict a different order, adjacency, side, elevation relation, or object role, mark the set `REVISE` or `REJECT`.
4. Derived views must not locally redraw geometry to improve composition when that redraw changes the authoritative relationship. Improve camera, crop, hierarchy, linework, annotation, or framing first.
5. When exact survey or field geometry is unavailable, preserve only the relation that the current authority actually supports. Mark synthetic, inferred, provisional, or NTS geometry explicitly and do not turn correspondence into false precision.
6. Where a relation crosses plan/section/model boundaries, provide at least one explicit binding mechanism: shared anchor IDs, section cut IDs, camera IDs, callouts, datum names, object IDs, or a correspondence table.
7. Review correspondence as a set, not file-by-file. Open the plan, section, axon/model, and render together and ask whether a reviewer can follow the same object or sequence without relying on captions alone.
8. Distinguish `MODEL/RENDER QUALITY` from `CORRESPONDENCE QUALITY`. A clean render can still fail if it depicts a different relationship from the plan or section; a technically correct model can still require visual revision.
9. For route or sequence work, verify stable order and branch logic across media. For assemblies/details, verify component identity, joint location, side, and termination logic instead.
10. Promotion requires both correspondence and medium-specific Design Crit. A correspondence PASS does not prove material realism, field accuracy, engineering approval, accessibility, or overall Design PASS.

Default review sequence:

`SOURCE AUTHORITY → SHARED ANCHORS → INVARIANTS → MEDIA TRANSLATION → SIDE-BY-SIDE READ → MEDIUM-SPECIFIC CRIT`

## Handoff checklist

- Units and bounding box are plausible.
- Normals, transforms, pivots, instancing, and modifiers are resolved intentionally.
- No missing or absolute-path textures.
- Material names are unique and meaningful.
- Cameras, frame rate, frame range, and color management are documented.
- External plugins and licenses are listed.
- A low-resolution review file and thumbnail are included.

## Required output

Return a model manifest, exchange report, render settings, asset dependency list, known limitations, and review images alongside the requested model/render.
