# OLEANDER Effect Signal / Primitive / Runtime Extension

Status: **CANDIDATE OWNER-LOCAL EXTENSION / EXISTING-FIRST / PROJECT RUNTIME VALIDATION REQUIRED**

Parent owner: `oleander-motion`

Purpose: integrate externally studied web/motion effect mechanisms into the existing OLEANDER motion owner without creating a parallel Effect Skill, style catalogue, visual-effects taxonomy, or new authority layer.

This extension deepens `MOTION_LIBRARY_EFFECT_ATLAS.md`. The Atlas continues to decide **whether** a motion/effect mechanism is justified; this extension defines how non-trivial interactive, shader, DOM↔WebGL and multi-renderer effects are represented, implemented, degraded and reviewed once justified.

`EFFECT EXTENSION ≠ EFFECT STYLE LIBRARY`

`SOURCE DIGESTION ≠ PROJECT PASS`

## 1 | Routing position

Use only after Current Authority, Required Native Output, state/information model and Motion Role have been resolved.

Required sequence:

`CURRENT AUTHORITY → REQUIRED NATIVE OUTPUT → STATE / INFORMATION CHANGE → MOTION ROLE → NO-MOTION BASELINE → EFFECT NEED → SIGNAL CONTRACT → MAPPING → PRIMITIVE → RENDERER → ORCHESTRATION WHEN NEEDED → QUALITY TIER / FALLBACK → REAL RUNTIME → AR-S10 → REPAIR / RETEST → PROJECT RE-APPLICATION`

Do not reverse this into:

`LIBRARY / DEMO → COOL EFFECT → FIND A PLACE TO USE IT`.

For browser work, co-route through `oleander-web-ui` for DOM, responsive, accessibility and real-browser authority. For 3D authoring, co-route to `oleander-3d-pipeline` when source geometry/camera/material authority is material. For final release proof, hand technical defects to `oleander-delivery-qc`.

## 2 | Unified effect model

Represent a non-trivial effect as:

`Signal → Normalization → Mapping → Primitive → Renderer → Orchestration → Quality / Fallback`

### Signal

Prefer shared, explicit inputs rather than each component inventing its own listeners and hidden state.

Core signals include as applicable:

- `time`;
- `progress` (`0..1` where meaningful);
- `pointerX / pointerY`;
- `pointerVelocity`;
- `scrollProgress`;
- `scrollVelocity`;
- `elementProgress`;
- `viewport` / observed element bounds;
- `DPR`;
- `visibility`;
- `reducedMotion`;
- `qualityTier`.

Signals are not automatically design variables. Only expose a signal when it carries a real interaction, state, spatial or narrative relationship.

### Mapping

Keep the response function explicit and reusable. Common mapping operators include:

`clamp`, `mapRange`, `lerp`, `damp`, `spring`, `ease`, `stagger`, `decay`, `velocity`, `distance`, `direction`, `threshold`, `step`, `quantize`, `noise`, `oscillation`, `envelope`.

A mapping should be inspectable independently of the renderer. Avoid burying interaction logic inside a shader, component render loop or page-specific callback when the same relation can be represented as a reusable mapping.

### Primitive

Prefer structural primitives over named visual presets. Initial owner-local primitive vocabulary:

- `PointerFollower` — lagged positional following;
- `TrailStack` — one signal distributed across layers with temporal separation;
- `VelocityDistortion` — input velocity mapped to deformation amplitude/direction;
- `MorphGeometry` — continuous geometry/path state interpolation where endpoints remain valid;
- `TransitionShader` — source texture → normalized progress → destination texture;
- `DOMTexturePlane` — DOM-governed media represented by a WebGL plane;
- `LoopingTrack` — seamless repeated content/scene track with continuity constraints;
- `TrackedSceneObject` — DOM geometry synchronized with Three/WebGL scene geometry;
- `ShaderSurface` — renderer-independent mount contract for a parameterized shader surface;
- `PostProcessPass` — bounded post-processing stage;
- `ChoreographyTimeline` — coordinated multi-object / multi-renderer temporal sequence.

A new named primitive is justified only when it introduces a materially different reusable relationship. A new visual preset alone does not justify a new primitive.

## 3 | Transition shader contract

For texture/view transitions, prefer a stable contract inspired by the transferable interface logic studied in GL Transitions rather than copying visual presets.

Required semantics when applicable:

- explicit source and destination inputs (`from`, `to` or equivalent semantic identities);
- normalized `progress`;
- aspect/ratio handling when image geometry can differ;
- declared custom uniforms/parameters;
- deterministic endpoint behavior: `progress=0` preserves the source state and `progress=1` preserves the destination state unless Current Authority explicitly defines another boundary condition;
- no hidden time-based drift that makes endpoint verification impossible;
- parameter defaults and legal ranges documented;
- transition can be disabled or replaced without deleting required information.

Validation should attack compilation/runtime errors, endpoint contamination, invalid/missing uniforms, aspect/crop failure, rapid reversal/re-entry, repeated invocation and fallback behavior.

## 4 | DOM ↔ WebGL contract

For browser work, DOM remains the authority for document flow, responsive layout, semantic text, accessibility, selection, focus and interaction semantics unless a more specific Current source overrides it.

Use WebGL/Three as a visual proxy or spatial renderer, not as an excuse to rebuild ordinary page layout inside Canvas.

Preferred relation:

`REAL DOM / SVG → measured semantic object → visual proxy plane/object → effect renderer`

Rules:

1. Required readable text remains live DOM/SVG/vector. Shader text may be a visual proxy but not the sole information carrier.
2. DOM geometry is measured/cached deliberately; avoid uncontrolled synchronous layout reads each frame.
3. Use `ResizeObserver`, `IntersectionObserver` or equivalent event-driven invalidation where appropriate.
4. Prefer one shared Canvas/context when several DOM-bound effects can coexist without violating isolation, layering or lifecycle requirements.
5. Preserve stable semantic IDs between DOM objects, scene proxies and QA evidence.
6. Responsive recomposition remains a design decision; do not merely scale WebGL coordinates proportionally.
7. Canvas failure, WebGL unavailability or reduced-motion mode must leave a valid page baseline.

## 5 | Runtime / quality tiers

Effect quality is part of the design contract, not a late optimization pass.

Use project-specific thresholds, but structure runtime choices as:

- `Q0` — DOM/SVG/static/no-WebGL baseline;
- `Q1` — reduced GPU path, low DPR/sample/pass count;
- `Q2` — standard target implementation;
- `Q3` — high-cost FBO/multi-pass/post-processing path only when justified and verified.

Every material effect should record when applicable:

- `preferredQuality`;
- `minimumQuality`;
- `mobileQuality`;
- `reducedMotionQuality`;
- `fallback`;
- DPR cap / pixel budget;
- sample/pass count;
- mount / resize / dispose lifecycle;
- context-loss/reopen behavior;
- bundle/runtime dependency cost.

Do not install one global device heuristic as an OLEANDER design truth. Choose quality based on actual project content, renderer cost and target-runtime evidence.

## 6 | Parameter contract

Separate runtime parameters from authoring/editor metadata.

Runtime parameters may include values such as intensity, scale, frequency, displacement, colors, seed, speed, progress, origin or direction.

Authoring metadata may include:

- semantic label and group;
- default;
- min / max / step or enum where meaningful;
- preset only when project-specific and traceable;
- description and design duty;
- quality implications;
- fallback/reduced-motion behavior.

Translate low-level implementation parameters into project design variables where possible. Do not expose arbitrary shader numbers as if they were a design system.

## 7 | Orchestration boundary

Use the smallest adequate layer:

- CSS / WAAPI / native scroll/view transitions for simple DOM effects;
- Motion / GSAP / Anime as already routed by the parent Skill;
- a choreography timeline only when multiple independent systems need coordinated temporal control;
- Theatre.js is a studied candidate mechanism for coordinated Three/DOM/SVG/shader parameter sequencing, not an automatic dependency or new OLEANDER authority.

Do not introduce a timeline editor merely because an effect is visually complex. The criterion is coordination complexity, interruption/re-entry need, authoring reproducibility and project handoff value.

## 8 | Effect-specific AR-S10 additions

When this extension is active, AR-S10 additionally checks as applicable:

- signal source and semantic duty are explicit;
- mapping is inspectable and not hidden accidental behavior;
- primitive selection is smaller than or equal to the problem;
- transition endpoint exactness / contamination;
- DOM↔WebGL geometry synchronization after resize/reflow;
- text/semantic information remains available without the visual proxy;
- DPR/pixel budget/sample/pass cost;
- shared-canvas/context lifecycle where relevant;
- mount / resize / dispose / remount correctness;
- context loss/reopen behavior where testable;
- mobile/touch fallback;
- Reduced Motion information equivalence;
- no-motion/Q0 baseline;
- native scroll, keyboard, focus and pointer behavior after effect infrastructure;
- actual target-browser/runtime playback, not a vendor demo;
- final design purpose after the effect is stripped of source-library visual identity.

Hard FAIL additions:

- an effect is the only carrier of required readable information;
- `progress=0/1` or defined transition endpoints visibly contaminate the source/destination without an authorized reason;
- DOM/scene proxies drift materially after resize/reflow;
- hidden continuous rendering causes material runtime cost when the scene is visually/static state-wise idle;
- unmount/remount leaks or duplicates rendering/interaction layers;
- WebGL failure leaves the page/task unusable when a valid baseline is required;
- source-library visual identity is copied as the project design language without project-specific reconstruction.

`RUNTIME PASS ≠ DESIGN KEEP` remains in force.

## 9 | Requirement coverage binding

For web/project use, material effects enter the Requirement Coverage Map as first-class implementation objects rather than polish notes.

Recommended row shape:

`REQUEST / SOURCE → TARGET OBJECT / REGION → STATE / INFORMATION DUTY → SIGNAL → MAPPING → PRIMITIVE → RENDERER → QUALITY / FALLBACK → ACCEPTANCE EVIDENCE → STATUS`

Example form only:

`hero media continuity → hero-media → reveal spatial relation → scrollProgress → damp → DOMTexturePlane → WebGL → Q2 / Q0 → desktop+mobile browser readback → PENDING`

The example does not authorize that effect for any project.

## 10 | Existing-first external study provenance

The following sources informed this independently reformulated extension. They remain provenance, not OLEANDER authority and not automatic dependencies:

- `gl-transitions/gl-transitions` — transferable contract ideas around normalized transition progress, uniforms and endpoint validation. Repository license: MIT; individual transitions may declare their own license and must be checked before code transfer.
- `paper-design/shaders` — transferable architecture ideas around separating rendering core, framework adapter, parameter definitions, preview/authoring metadata and runtime lifecycle. Use only independently reformulated architecture unless a specific code transfer is separately license-checked.
- `martinlaxenaire/curtainsjs` — transferable DOM-governed layout → WebGL plane relation and media-as-texture integration concepts.
- `14islands/r3f-scroll-rig` — transferable DOM/3D tracking, shared-canvas and measurement invalidation concepts.
- `theatre-js/theatre` — transferable multi-system choreography/timeline concept; package/license boundaries must be checked for the exact component used.
- `codrops/codrops-sketches` and individual Codrops experiments — transferable input-signal → mapping → visual-response patterns. Per-repository/file license must be checked before copying code.

Also studied as mechanism/catalog references: Motion, Anime.js, Lenis, OGL, Three/postprocessing, Magic UI, Animata, React Bits and related source libraries already covered by the parent Atlas or Existing-First research.

Transfer rule:

`OBSERVE SOURCE → EXTRACT MECHANISM → REMOVE SOURCE VISUAL IDENTITY → REFORMULATE CONTRACT → PROJECT RE-APPLICATION → REAL RUNTIME REVIEW`.

Do not import external prompt recipes, component markup, CSS values, shader presets, fixed timings, brand tokens, visual signatures or runtime assumptions as OLEANDER defaults.

## 11 | Maturity boundary

This file is an owner-local Candidate extension under the installed `oleander-motion` owner. It does not create a new installed Skill and does not promote any external runtime/library.

The mechanism model may be used as a routing/implementation contract, but stronger maturity claims require real project re-application, target-runtime evidence, repair/retest and independent review under the existing OLEANDER lifecycle.

`DOCUMENTED ≠ EXECUTED ≠ VALIDATED ≠ PROJECT KEEP`.
