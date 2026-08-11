# OLEANDER Motion Library & Effect Atlas v0.3

**Status:** `REFERENCE / ROUTING CONTRACT / RUNTIME VALIDATION PER PROJECT REQUIRED`  
**Verified:** 2026-08-11  
**Parent skill:** `oleander-motion`  

This atlas is not a style catalogue. It maps a motion problem to the smallest adequate runtime/tool and then to an effect mechanism. A library demo, component gallery, recording, or vendor showcase is reference evidence only; it does not prove that the mechanism is appropriate, performant, accessible, or production-ready inside an OLEANDER project.

## 1｜Selection order

`State / Information Change → Motion Role → Native Capability Check → Library Choice → Effect Mechanism → Reduced Motion → Runtime Cost → AR-S10 → Keep / Reduce / Remove`

Hard rule: **do not start from a library or a fashionable effect and search for somewhere to use it.**

### Native-first rule

Prefer browser/platform-native capabilities when they can express the required relationship without losing interruption, accessibility, or reproducibility:

1. CSS transitions / animations;
2. Web Animations API (`Element.animate`, `Animation` controls);
3. CSS Scroll-driven Animations for simple scroll-linked timelines;
4. View Transition API for suitable SPA/MPA view continuity;
5. `prefers-reduced-motion` for non-essential motion reduction/replacement.

Escalate to a library only when the task requires capabilities, authoring ergonomics, state logic, or rendering that the native layer does not provide well enough.

## 2｜Library routing map

| Route | Best-fit problem | Strong mechanisms | OLEANDER default | Main caution |
| --- | --- | --- | --- | --- |
| Native CSS / WAAPI / View Transitions | small/medium DOM state changes, simple scroll/view transitions | keyframes, playback controls, scroll timelines, cross-view continuity | **FIRST CHECK** | browser/runtime support and interruption must still be tested |
| Motion | React/UI state, layout continuity, gestures, shared elements, scroll | layout/layoutId, AnimatePresence, gestures, scroll values, reduced motion | **PREFERRED UI ROUTE** | do not animate every mount/in-view event |
| GSAP + ScrollTrigger + Flip | complex timelines, pinned/scrubbed narrative, FLIP across layout changes | timeline orchestration, scrub/pin/snap, FLIP state capture | **COMPLEX TIMELINE ROUTE** | scroll-jacking, excessive pinning, long blocking sequences |
| Anime.js | expressive lightweight DOM/SVG animation | SVG morph, line draw, motion path, stagger, draggable | **SVG / GRAPHIC ROUTE** | morph topology and stagger can become decorative noise |
| Rive | interactive vector assets with internal behavior | state machines, transitions, inputs/data binding | **INTERACTIVE VECTOR ROUTE** | state-machine complexity and runtime handoff need explicit QA |
| Lottie / lottie-web | authored vector animation delivery/playback | JSON vector animation, markers, SVG/canvas/html playback | **DELIVERY ROUTE** | not a substitute for a rich product state machine; source/export parity matters |
| Three.js | web 3D product/spatial/brand motion | AnimationMixer, clips, morph targets, camera/material animation, post FX | **WEB 3D ROUTE** | GPU cost, device variance, shader/post-processing excess |
| PixiJS | dense GPU 2D, particles, raster/vector-like scene effects | ticker, filters, displacement/noise/blur, shaders | **DENSE 2D / SHADER ROUTE** | filters multiply render cost; effect stacks need profiling |
| Lenis | smooth-scroll transport/synchronisation | smooth wheel/touch interpolation, scroll sync | **SELECTIVE INFRASTRUCTURE** | it is not a motion engine; preserve native usability and nested scrolling |
| Barba.js | custom page lifecycle/transition orchestration | leave/enter hooks, route/namespace transition selection | **SELECTIVE LEGACY/ADVANCED ROUTE** | Barba itself is not an animation engine; native View Transitions should be checked first |
| Figma | component/state concept and quick interaction validation | component variants, Smart Animate, prototype triggers | **PROTOTYPE** | not implementation evidence |
| Blender | 3D/product/spatial/camera/procedural motion | keyframes, Graph Editor, drivers, constraints, geometry nodes/simulation | **3D AUTHORING** | render/video does not prove interactive runtime behavior |

## 3｜Core effect mechanisms｜优先学习与复用

These mechanisms usually have a clear structural role and can transfer across OLEANDER projects.

### EF-01 Shared-element / FLIP continuity
Use when an object changes container, scale, position, or hierarchy but should remain perceptually the same object.

Good for:
- project-card → project-detail continuity;
- filter/reorder states;
- component expansion/collapse;
- before/after layout transitions.

Prefer: native View Transition / Motion layout / GSAP Flip depending on runtime.

### EF-02 Mask / Clip / Aperture reveal
Reveal content by changing a boundary rather than simply fading everything in.

Good for:
- hierarchical entry;
- spatial threshold concepts;
- controlled image/text reveal.

Fail when the mask hides required information too long or becomes a generic cinematic wipe.

### EF-03 SVG line drawing / path trace
Expose route, relation, or construction sequence through a path.

Good for:
- C01 route/evidence diagrams;
- diagram logic;
- brand construction studies.

Do not use path-drawing to imply a route or sequence was observed in reality when it was only designed or inferred.

### EF-04 Topology-safe morph
Morph only between static states that are both valid and independently legible.

Good for:
- Symbol Route 01.2 irreversible revision structures;
- state icon transitions;
- selected information graphics.

Hard rule: motion cannot rescue a weak static symbol. If either endpoint fails static identity/legibility, reject the morph.

### EF-05 Stagger / structured sequence
Use timing offsets to expose hierarchy, order, dependency, or reading sequence.

Good for:
- list/group updates;
- diagram build-up;
- controlled title/data sequencing.

Avoid decorative cascade on every page load.

### EF-06 Scroll progress / scroll-linked state
Bind a state to real document/scene progress rather than using scroll as a trigger for unrelated spectacle.

Good for:
- chapter progress;
- evidence sequence;
- time-series scrub;
- product exploded stages.

Avoid scroll-jacking and avoid making normal navigation depend on long pinned sequences.

### EF-07 Explode / assemble
Express product hierarchy, construction relationship, layer order, or maintenance access.

Good for:
- Timer/product assemblies;
- CMF layer logic;
- architectural component sequences.

Explosion distance, order and collisions must be derived from the object structure, not arbitrary cinematic motion.

### EF-08 Temporal light / material parameter transition
Animate emission, luminance, roughness, reflection, opacity or controlled shader parameters where those variables genuinely carry state.

Good for:
- Timer Light Basin remaining-time state;
- CMF/reflection studies;
- environmental/daylight narratives when clearly simulated.

Do not use glow as a generic quality signal.

### EF-09 Data reorder / filter / time interpolation
Keep object identity visible while data changes state.

Good for:
- ranking/sorting;
- before/after comparison;
- map/time-series filtering;
- state uncertainty changes.

Missing, uncertain or unavailable data must remain visible through the transition; animation must not smooth away discontinuities that matter.

### EF-10 View/page transition
Preserve spatial or semantic context between views.

Good for:
- project list ↔ detail;
- image ↔ evidence detail;
- modal/dialog continuity.

Prefer a direct transition with a stable anchor over full-screen cinematic transitions.

## 4｜Selective effect mechanisms｜条件性使用

Use only when the project relationship justifies them and AR-S10 runtime review supports the decision.

- `EF-11 Spring / inertia / drag` — tactile manipulation and interruptible feedback; reject decorative bouncing.
- `EF-12 Parallax / depth separation` — clarify spatial planes; avoid continuous vestibular-heavy movement.
- `EF-13 Displacement / refraction` — material/field transition or controlled distortion; avoid generic liquid/glitch identity.
- `EF-14 Blur / progressive blur / depth transition` — attention/hierarchy shift; verify text legibility and GPU cost.
- `EF-15 Grain / noise evolution` — material/time atmosphere only; do not use moving grain to fake “cinematic quality”.
- `EF-16 Particle / field` — aggregate, flow or spatial field representation; data-driven when claiming analytical meaning.
- `EF-17 Kinetic type / variable-font axis motion` — semantic emphasis or typographic state; never animate every headline by default.
- `EF-18 Camera orbit / dolly / focus shift` — reveal 3D relation or product structure; avoid constant showroom orbit.
- `EF-19 Cursor-linked / magnetic response` — local affordance or exploratory surface; preserve normal pointer behavior and touch fallback.
- `EF-20 Smooth-scroll transport` — only when it improves synchronization of a justified experience; native scroll remains baseline.

## 5｜Avoid-by-default patterns｜默认否决

These are not forbidden, but they require a concrete semantic/functional case rather than an aesthetic adjective.

- generic logo reveal;
- infinite floating/bobbing cards;
- gratuitous aurora, meteors, glow trails or particle backgrounds;
- constant marquee for ordinary content;
- heavy cursor followers and full-page cursor replacement;
- aggressive magnetic buttons;
- scroll-jacking / forced cinematic scroll;
- excessive 3D tilt on cards;
- full-screen zoom transitions as default navigation;
- long loaders when there is no real wait state;
- glitch/chromatic aberration used merely to signal “technology”;
- liquify/displacement on every hover;
- many simultaneous parallax layers;
- confetti without a meaningful outcome event;
- auto-playing background motion that competes with reading.

## 6｜Reference component/effect libraries｜只研究机制，不复制视觉身份

The following can be used to study implementation mechanisms, composition patterns and failure modes. They are **not OLEANDER design-language sources** and their visual recipes should not be copied wholesale:

- Animate UI;
- Motion Primitives;
- Magic UI;
- React Bits.

For every borrowed mechanism record:
`Reference → Mechanism extracted → Visual identity removed → OLEANDER state/relationship rebuilt → Runtime review`.

## 7｜OLEANDER project mapping

### Symbol Route 01.2
Preferred:
- `EF-04 Topology-safe morph`;
- shared-boundary transition;
- cut → displacement → irreversible residue;
- static endpoint competition before any animation.

Avoid:
- logo draw-on;
- glow reveal;
- rotation/scale reveal that does not arise from the symbol topology.

### Timer Light Basin
Preferred:
- `EF-08 Temporal light/material parameter transition`;
- radius / luminous-area / intensity relationship tied to remaining-time state;
- no-motion and reduced-motion equivalents that preserve state information.

Avoid:
- bounce/pulse unless it represents an actual alert state;
- arbitrary breathing glow during normal timing.

### Website
Preferred:
- `EF-01` shared-element/layout continuity;
- `EF-02` restrained mask reveal;
- `EF-06` progress-linked motion;
- `EF-10` View Transition where compatible;
- small native/WAAPI effects before large libraries.

Avoid:
- every section animating on scroll;
- long pinned hero sequences that block reading;
- smooth scroll as a default requirement.

### Product / CMF
Preferred:
- `EF-07` explode/assemble;
- `EF-08` material/reflection/light parameter change;
- selective shader/displacement only if it reveals a material condition.

### Spatial / C01
Preferred:
- route/path trace;
- time sequence;
- evidence layer appearance/disappearance;
- viewpoint continuity.

Evidence boundary: designed motion may explain a route hypothesis; it cannot promote unobserved site behavior to observed fact.

### Data / GIS
Preferred:
- `EF-05` structured sequencing;
- `EF-09` reorder/filter/time interpolation;
- scroll/time scrub when the time/sequence variable is real.

### Web 3D / dense 2D
- Three.js: 3D clips, morphs, material/camera changes and controlled post-processing.
- PixiJS: high-density 2D, displacement/noise/filter/shader work when DOM/SVG is no longer the right renderer.

## 8｜Library escalation gate

Before adding a runtime dependency answer:

1. What exact state/relationship cannot be expressed adequately with the current stack?
2. Is the dependency solving motion logic, authoring, rendering, scrolling, or delivery?
3. Can interruption/reverse/rapid repeat be handled?
4. How will Reduced Motion preserve the information?
5. What is the bundle/runtime/GPU cost?
6. Does it alter native scroll, focus, keyboard, pointer or navigation behavior?
7. Is the source/export/runtime chain reproducible?
8. What is the rollback/no-motion baseline?

If these questions have no clear answer, do not add the library.

## 9｜Source register｜Primary documentation checked 2026-08-11

- Motion: https://motion.dev/docs/react
- Motion reduced motion: https://motion.dev/docs/react-use-reduced-motion
- GSAP ScrollTrigger: https://gsap.com/docs/v3/Plugins/ScrollTrigger/
- GSAP Flip: https://gsap.com/docs/v3/Plugins/Flip/
- Anime.js SVG: https://animejs.com/documentation/svg/
- Anime.js stagger: https://animejs.com/documentation/utilities/stagger/
- Rive State Machines: https://rive.app/docs/editor/state-machine/state-machine
- Rive Web State Machine Playback: https://rive.app/docs/runtimes/web/state-machines
- Lottie specification: https://lottie.github.io/lottie-spec/1.0/
- lottie-web: https://github.com/airbnb/lottie-web
- Three.js AnimationMixer: https://threejs.org/docs/pages/AnimationMixer.html
- Three.js EffectComposer: https://threejs.org/docs/pages/EffectComposer.html
- PixiJS filters: https://pixijs.com/8.x/guides/components/filters
- PixiJS Ticker: https://pixijs.com/8.x/guides/components/ticker
- Web Animations API: https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API
- CSS Scroll-driven Animations: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations
- View Transition API: https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API
- prefers-reduced-motion: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
- Lenis: https://github.com/darkroomengineering/lenis
- Barba transitions: https://barba.js.org/docs/advanced/transitions/

## 10｜Evidence boundary

This atlas records **verified documentation capabilities and OLEANDER routing judgments**. It does not claim that all libraries are installed, that all effects have been run on OLEANDER artifacts, or that any effect improves user experience. Each actual project implementation remains `DESIGNED / NOT RUN` until executed in its real tool/runtime and reviewed through Common Review + AR-S10.
