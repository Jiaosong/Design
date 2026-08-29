# 2026-08-30 Effect System Source Digestion

Status: **TRAINING DIGESTION / SOURCE-BOUNDED / NO AUTOMATIC PROMOTION**

Owner target: `oleander-motion`; browser co-route: `oleander-web-ui`.

## Problem

OLEANDER already had a Motion Effect Atlas and a web runtime route, but externally studied effect libraries could still be consumed as named presets or ad-hoc page code. The training objective was to extract transferable mechanisms and write them back into existing owners rather than create a new Effect Skill.

## Existing-first decision

Internal coverage exceeded the threshold for reuse:

- `oleander-motion` already owns Motion Role, timing/easing, interruption/re-entry, Reduced Motion and AR-S10;
- `MOTION_LIBRARY_EFFECT_ATLAS.md` already owns library/effect selection;
- `oleander-web-ui` already owns editable DOM/browser integration, responsive behavior, accessibility and real-browser readback;
- governance already requires local `VISUAL_LAYER_BINDING.md` when present for visual-output owners.

Decision: **REUSE / EXTEND EXISTING OWNERS**. No parallel Effect Skill, no new visual taxonomy.

## External sources studied

### gl-transitions/gl-transitions
Transferable: normalized transition progress, source/destination contract, uniform declaration and endpoint-validation discipline.

License boundary observed: repository MIT; repository license explicitly notes individual transitions may declare their own licenses. Therefore interface/validation principles were independently reformulated; copying a specific transition still requires per-file license review.

### paper-design/shaders
Transferable: rendering core separated from framework adapter, effect/parameter definition, preview/editor metadata and runtime lifecycle; pixel/DPR/runtime-budget thinking.

Transfer boundary: architecture and engineering mechanisms only unless a specific code transfer is separately checked.

### martinlaxenaire/curtainsjs
Transferable: DOM-governed layout/media mapped to WebGL planes; WebGL used as visual representation rather than document-layout authority.

### 14islands/r3f-scroll-rig
Transferable: DOM↔3D geometry tracking, shared-canvas thinking, observer/invalidation-based measurement and runtime synchronization.

### theatre-js/theatre
Transferable: coordinated timeline/choreography across Three/DOM/SVG/shader parameters when ordinary motion primitives are insufficient.

Transfer boundary: exact package/license must be checked before dependency adoption; no runtime promotion occurred here.

### codrops/codrops-sketches and individual experiments
Transferable: input signal → normalization/mapping → visual response patterns, including pointer following, velocity-driven deformation and loop/continuity mechanisms.

Transfer boundary: source experiments are provenance/mechanism references; per-repository/file license review is required before copying code.

## Synthesized delta

The new reusable representation is:

`Signal → Normalization → Mapping → Primitive → Renderer → Orchestration → Quality / Fallback`.

Initial primitives retained only where they express reusable relationships:

`PointerFollower`, `TrailStack`, `VelocityDistortion`, `MorphGeometry`, `TransitionShader`, `DOMTexturePlane`, `LoopingTrack`, `TrackedSceneObject`, `ShaderSurface`, `PostProcessPass`, `ChoreographyTimeline`.

The source library name is not the primary OLEANDER object.

## Rejected transfer

Not transferred as OLEANDER defaults:

- visual presets or named showcase styles;
- external brand/design identity;
- fixed shader numbers, timings, easings or quality thresholds;
- component markup/CSS recipes;
- prompt recipes;
- framework-specific architecture where a smaller native route is sufficient;
- continuous GPU rendering as a default;
- smooth scroll, cursor replacement, particles, glow, distortion or post-processing as default page treatment.

## Repository writeback

This digestion is written into existing process through:

- `oleander-motion/EFFECT_SIGNAL_PRIMITIVE_RUNTIME_EXTENSION.md`;
- `oleander-motion/CAPABILITY.json` input/output/gate/implementation-path binding;
- `oleander-motion/VISUAL_LAYER_BINDING.md` execution discovery;
- `oleander-web-ui/VISUAL_LAYER_BINDING.md` browser Requirement Coverage Map and DOM↔WebGL co-routing.

The extension remains Candidate until real project re-application, target-runtime evidence, repair/retest and existing OLEANDER review gates support stronger maturity.
