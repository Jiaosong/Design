# Motion Visual Layer Binding

Status: **BINDING ONLY / EXISTING EFFECT ATLAS + OWNER-LOCAL RUNTIME EXTENSION**

Do not create another OLEANDER motion/effect catalogue or a parallel Effect Skill. The current visual-effect selection source for this Skill remains:

`MOTION_LIBRARY_EFFECT_ATLAS.md` — OLEANDER Motion Library & Effect Atlas v0.3.

For justified non-trivial interactive, shader, DOM↔WebGL or multi-renderer effects, deepen implementation through:

`EFFECT_SIGNAL_PRIMITIVE_RUNTIME_EXTENSION.md` — owner-local Candidate extension for `Signal → Mapping → Primitive → Renderer → Orchestration → Quality/Fallback` representation and runtime review.

The extension does not replace the Atlas. The Atlas decides whether a motion/effect mechanism belongs; the extension defines how a justified complex effect is represented, degraded and tested.

## Existing sources to inherit

1. Local `MOTION_LIBRARY_EFFECT_ATLAS.md`.
2. Local `EFFECT_SIGNAL_PRIMITIVE_RUNTIME_EXTENSION.md` when its trigger applies.
3. Notion `OLEANDER Artifact Review System v1.1｜合规门 × 专业设计门`.
4. Current Project Design DNA / Visual Bible when motion must inherit a project-specific visual language.
5. Current Notion `T-VISUAL-IMAGE-OPS-001｜OLEANDER Image Processing Operator Standard｜图层—蒙版—透明度—混合—滤镜—非破坏编辑` for preparation and compositing of layered raster/vector assets.

## Existing selection rule

Use the atlas order:

`State / Information Change → Motion Role → Native Capability Check → Library Choice → Effect Mechanism → Reduced Motion → Runtime Cost → AR-S10 → Keep / Reduce / Remove`

When the selected mechanism requires non-trivial input mapping or a shader/scene renderer, continue:

`Signal → Normalization → Mapping → Primitive → Renderer → Orchestration when needed → Quality/Fallback → Real Runtime → AR-S10`.

The atlas already defines core, selective and avoid-by-default mechanisms. Do not start from a fashionable effect and search for somewhere to use it.

## Browser / WebGL binding

When a web effect is DOM-bound, preserve the existing `oleander-web-ui` authority for document flow, semantic HTML/SVG, responsive layout, accessibility and real-browser readback. WebGL/Three may act as a visual proxy or spatial renderer; it must not silently replace live text, keyboard/focus semantics or the no-effect page baseline.

Effects that introduce scroll, pointer, resize, shared-canvas or post-processing infrastructure must declare their signal source, renderer lifecycle, Reduced Motion path, Q0/no-WebGL fallback and project-specific runtime evidence.

## Image-processing operator routing

Use `T-VISUAL-IMAGE-OPS-001` for alpha/mask preparation, layered image assets, opacity/blend setup, Smart Object-style source preservation, frame-level tonal treatment and vector/raster effect preparation. Temporal meaning, sequencing, easing, reduced-motion equivalence and runtime behavior remain owned by Motion. Do not bake a destructive Photoshop/Illustrator effect into the only source when a recoverable layered or vector-safe master can remain available.

## Review inheritance

Actual target-runtime playback remains mandatory. Video/render/demo evidence does not prove runtime behavior or design quality.

For extension-triggering effects, additionally inspect endpoint contamination where applicable, DOM↔scene drift after reflow, DPR/pixel/sample/pass cost, mount/resize/dispose/remount behavior, mobile/touch fallback and whether required information survives Q0 / Reduced Motion.

`RUNTIME PASS ≠ DESIGN KEEP`.
