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

## Material identity gate

A shader name, texture slot, successful render, or visually different base color does not by itself prove material identity or professional CMF separation.

Before a material family is accepted for a main render, product/spatial visualization, CMF board, or reusable library:

1. Review materials under one controlled lighting/camera condition before comparing artistic lighting variants.
2. Separate the material channels conceptually: base color, metallic/conductor vs dielectric behavior, roughness/specular response width, normal or relief character, occlusion, texture scale/direction, and edge behavior. The exact renderer may expose different controls, but these roles must not collapse into hue alone.
3. For metallic-roughness workflows, keep the physical meaning of metalness and roughness distinct. Do not make a dielectric material appear metallic only by tinting it, and do not use orange/brown hue alone as proof of weathering steel.
4. Texture frequency and grain direction must be plausible at the modeled object scale and intended camera distance. A visible tile/repeat, arbitrary procedural pattern, or wrong grain scale is a Design REVISE even when the texture technically loads.
5. Material identity should remain reasonably legible when color is reduced or neutralized. Use a grayscale/desaturation check when hue may be carrying too much of the distinction.
6. Edge response is part of material reading: sharp, chipped, rounded, laminated, oxidized, cut, end-grain, polished, or weathered edges must agree with the intended material and fabrication logic. Do not add edge wear as generic decoration.
7. Avoid `gray model + color labels` as a finished material system. If different named materials share nearly identical roughness response, texture scale, highlight behavior, and edges, default to `REVISE` even if the palette is attractive.
8. Review at two scales: first-read silhouette/material family and near-read surface behavior. Microtexture that only works in a close crop must not be used to claim material realism in a distant hero view.
9. Keep truth boundaries explicit. A render or calibration image can demonstrate visual material separation; it does not prove measured reflectance, real sample approval, weathering life, fire/slip performance, structural suitability, fabrication quality, or field installation.
10. If the renderer/runtime is unavailable, a deterministic calibration board may test material hierarchy and response logic, but it cannot substitute for the final PBR/runtime material validation when that validation is required by the deliverable.

Reference implementation note: glTF 2.0 metallic-roughness separates base color, metallic factor, roughness factor, normal and occlusion textures. Use these categories as a compatibility model where relevant, not as a claim that every OLEANDER renderer or real material must reduce to one shader model.

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
