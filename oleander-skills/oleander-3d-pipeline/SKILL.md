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

## Dimension-to-object binding gate

Use this gate whenever a model, axonometric, orthographic, exploded view, or technical presentation contains dimensions that are intended to prove scale, clearance, position, component size, or body relationship.

1. A dimension is not considered visually present merely because its numeric value exists in a register, legend, table, or nearby note. The measured object, interval, edge, datum, or relation must be unambiguous in the intended view.
2. Bind critical dimensions directly to the object using extension lines, witness lines, leaders, aligned dimension lines, section references, or another explicit geometric carrier appropriate to the medium.
3. Separate **CRITICAL ATTACHED DIMENSIONS** from **SECONDARY SCALE / PARAMETER RAILS**. Critical values required for first interpretation stay on-object; repeated or supporting values may move to a near-read rail so they do not bury the silhouette.
4. Dimension graphics must not destroy the first-read model, human-scale figure, joint, route relation, or other primary design evidence. When annotation density competes with the object, revise spacing, projection, crop, leader routing, or page allocation rather than detaching the values again.
5. Human-scale and ergonomic dimensions must identify the body condition they refer to (for example SIT / LEAN / RECLINE) and must not imply percentile, accessibility, or population-standard claims unless the source actually supports them.
6. Nominal/model dimensions, scenario values, measured field dimensions, and engineering tolerances are different evidence classes. Keep the source class and `DOES NOT PROVE` boundary adjacent when misinterpretation would be consequential.
7. Do not convert a scale-test or provisional dimension into apparent site or construction truth by placing it on a polished model sheet. `MODEL SCALE READ =/= FIELD MEASUREMENT =/= ENGINEERING APPROVAL`.
8. Use the source authority for numeric values. Layout/presentation may change leader position, spacing, type hierarchy, and visual weight, but it may not silently change the number, unit, measured interval, or datum.
9. Review at two distances: **FIRST READ** checks whether the model/object remains dominant; **NEAR READ** checks whether each important value can be traced to the exact object or interval it describes.
10. Promotion requires a rendered/reopened target-size proof. Export success, dimension text presence, or a clean parameter table cannot substitute for dimension-to-object legibility.

Default review order:

`SOURCE VALUE → MEASURED OBJECT / INTERVAL → ATTACHMENT CARRIER → FIRST-READ MODEL → NEAR-READ DIMENSION → TRUTH BOUNDARY`

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

