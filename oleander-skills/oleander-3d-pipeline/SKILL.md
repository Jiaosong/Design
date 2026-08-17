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

## Camera claim gate

A locked camera is not automatically a correct camera. Treat camera selection as part of the design claim, not only as a framing or rendering setting.

Use this review sequence before promoting a camera-dependent render, model view, spatial image, or technical proof:

`CLAIM → PROJECTION → CAMERA DISTANCE / FOCAL LENGTH → FIRST-READ → ROLE VERDICT`

1. Declare the camera role before tuning it: `EXPERIENCE_HERO`, `RELATION_PROOF`, `TECHNICAL_ORTHO`, `DETAIL`, `SEQUENCE`, or another project-specific role.
2. Record projection type. Perspective and orthographic views are not interchangeable evidence: perspective communicates experiential depth; orthographic deliberately removes perspective size falloff and is often better for technical comparison.
3. For perspective views, record focal length or field of view together with camera position/distance and target. Focal length alone does not describe perspective emphasis.
4. Reject `FIT EVERYTHING` as a sufficient camera rationale. A wider lens or closer camera may include more scene while over-weighting foreground objects and under-weighting the relation the view is meant to prove.
5. When comparing camera candidates, keep the authoritative scene geometry unchanged. Camera tests may change projection, camera position, focal length, target, shift, crop, and framing; they may not redraw geometry to make one camera look better.
6. Check near/mid/far scale relationships and human-scale cues. If foreground expansion, far-context suppression, or depth compression changes the intended claim, mark the view `REVISE` even when the render is visually attractive.
7. Use orthographic/axonometric views when the claim is relational or technical, but do not promote them as experiential evidence merely because they are clearer.
8. Use lens shift or off-axis framing deliberately when vertical/horizontal convergence must be controlled; do not rotate or distort geometry to simulate a camera correction.
9. Review the final camera at the actual delivery crop and size. A camera that works in the viewport but loses its claim after crop, responsive reframing, or board placement is not a Design PASS.
10. Keep camera/render quality separate from field truth. A convincing camera does not prove the real viewpoint, measured visibility, human perception on site, lens calibration, or field-validated geometry unless those inputs are independently established.

Default fail condition: if the reviewer cannot state what the camera proves, why this projection is appropriate, and what spatial emphasis changes because of camera distance/focal length, the camera remains `REVISE`.

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
