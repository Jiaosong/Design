---
name: oleander-motion
description: Design, prototype, implement, and review purposeful motion for OLEANDER across brand, interface, product, 3D, spatial, and data contexts. Use whenever a task involves animation, state transitions, motion language, micro-interactions, scroll/gesture motion, Blender animation, procedural motion, animated data, motion libraries, Lottie/Rive, motion accessibility, or motion QA.
compatibility: Native-first. Prefer CSS/WAAPI/View Transitions/Scroll-driven Animations when sufficient; route React/UI to Motion, complex timelines/FLIP/scroll to GSAP, expressive SVG to Anime.js, interactive vector state machines to Rive, vector delivery to Lottie, web 3D to Three.js, and dense GPU 2D/shader work to PixiJS. Figma and Blender remain primary authoring/prototyping routes where applicable. Unavailable runtime steps stay PENDING.
---

# OLEANDER Motion

Treat motion as a temporal relationship system, not decoration. The primary question is always: **what state, hierarchy, causality, spatial continuity, or information change becomes clearer because this motion exists?**

## Canonical method

`State Change → Motion Role → No-motion Baseline → Candidate Motion → Timing/Easing Variants → Reduced-motion Alternative → Runtime Attack → Human Decision → Archive`

Motion roles:
- `Feedback` — input, waiting, success, failure;
- `Continuity` — where an object/state comes from and where it goes;
- `Hierarchy` — enter/exit, expand/collapse, group/split;
- `Attention` — necessary change or risk only;
- `Brand Motion` — repeatable temporal identity;
- `Narrative` — sequence, reveal, comparison, temporal argument.

If no role is identifiable, remove the animation.

## Skill matrix

1. `MOT-01 Timing & Easing` — duration, velocity, pause, delay, rhythm, frequency.
2. `MOT-02 State Transition` — state machines, interruption, reversal, recovery.
3. `MOT-03 Spatial Continuity` — position, camera, parallax, depth and continuity.
4. `MOT-04 Brand Motion` — symbol/type/graphic motion grammar; no generic logo reveal.
5. `MOT-05 3D / Procedural Motion` — Blender keyframes, Graph Editor, Drivers, Constraints, Geometry Nodes/Simulation, lighting/material change.
6. `MOT-06 Data / Information Motion` — sorting, filtering, time, update, transition, uncertainty.
7. `MOT-07 Interactive Motion` — hover, press, drag, scroll, gesture, component feedback.
8. `MOT-08 Motion Accessibility` — reduced motion, flashing/zoom/parallax risk, equivalent information.
9. `MOT-09 Delivery` — Figma prototype, Rive/Lottie, CSS/WAAPI/JS, Three.js/GLB animation, video/sequence output.
10. `MOT-10 Motion QA` — frame pacing, latency, looping, interruption, occlusion, cross-device consistency and reopen/reproduction.

## Tool routing

- **Native Web:** CSS transitions/animations, Web Animations API, CSS Scroll-driven Animations and View Transitions are the first check for DOM/view motion.
- **Motion:** React/UI state, layout/shared-element continuity, gestures and scroll-linked UI.
- **GSAP:** complex timeline orchestration, ScrollTrigger narratives and Flip/FLIP transitions.
- **Anime.js:** expressive DOM/SVG work including morphing, line drawing, motion paths, staggering and draggable behavior.
- **Rive:** interactive vector assets whose behavior belongs in an explicit state machine.
- **Lottie:** vector animation delivery/playback where the authored motion is primarily packaged as an animation asset rather than a product state machine.
- **Three.js:** web 3D animation, camera/material/morph motion and controlled post-processing.
- **PixiJS:** dense GPU 2D scenes, filters, displacement/noise and shader-driven visual systems.
- **Lenis / Barba:** selective infrastructure only. Lenis is scroll transport/synchronisation; Barba manages page-transition lifecycle and requires a separate animation mechanism. Check native scrolling/View Transitions first.
- **Figma:** component states, prototype paths, Smart Animate and quick interaction validation.
- **Blender:** product/spatial/brand 3D motion, camera, Graph Editor, Drivers, Geometry Nodes and simulation.
- **After Effects / Framer / TouchDesigner and other specialist tools:** use only when the actual environment is available and the task benefits from that medium.

Do not claim execution in unavailable software. A storyboard, timeline specification, effect reference, or code draft is `DESIGNED / NOT RUN` until executed in a real runtime.

## Library and effect selection gate

Read `MOTION_LIBRARY_EFFECT_ATLAS.md` before introducing a new animation dependency or reference effect.

Use this order:

`State / Information Change → Structural Effect → Native Capability Check → Library → Reduced Motion → Runtime Cost → AR-S10 → Keep / Remove`

Do **not** use:
`Library → Cool Effect → Find a place to use it`.

Prefer reusable structural mechanisms such as shared-element/FLIP continuity, mask/clip reveal, SVG path trace, topology-safe morph, structured stagger, scroll progress, explode/assemble, temporal light/material parameters, data reorder/time interpolation and view transitions.

Treat aurora/glow trails, infinite floating, generic logo reveals, heavy cursor followers, excessive magnetic motion, scroll-jacking, gratuitous glitch/displacement, full-screen zoom transitions and similar showcase effects as `AVOID BY DEFAULT` unless a concrete state/relationship justifies them.

Component/effect libraries and galleries are mechanism references only. Strip their visual identity before any OLEANDER use.

## Exploration behavior grammar gate

Use this gate for route, travel, spatial exploration, museum/exhibition, inspection, world-linked explanation, or game-like discovery. Do not judge isolated glow/fade/reveal effects first. Establish the **behavior grammar and persistent relationship** before choosing render mechanisms.

Base contract:

`Journey / Task State → Behavioral Verb → Persistent World/Object → Relationship Change → Motion Mechanism → Reverse/Recovery → Reduced Motion`

Rules:
- derive behavioral verbs from the actual task or journey; do not impose one universal vocabulary;
- each transition must clarify at least one source/destination, causal, spatial, hierarchy, or task relationship;
- preserve a persistent world, object, route, or anchor across adjacent states when continuity is part of the experience;
- forward/back navigation should normally use the same reversible causal/spatial grammar unless the exit semantics genuinely differ;
- fade, glow, pulse, reveal, blur, mask, scale, parallax, camera movement, light sweep and card appearance are **motion/render mechanisms**, not behavioral states;
- a sequence that can only be described as `fade / reveal / glow / withdraw` without explaining why state changed, where the viewer is going, what remained selected, or how to return is a default `REVISE`;
- evaluate the grammar across the full sequence, not as individually polished frames;
- for landscape/world-first experiences, preserve world/object/route first-read before a dominant UI overlay; motion must not convert a world-first experience into an overlay-first dashboard without a task reason;
- Reduced Motion must preserve the same state, route continuity, action hierarchy and Return meaning through static structure, explicit state change, or near-instant transitions;
- run forward, reverse/back, rapid-repeat, interruption/re-entry, target-switch and narrow-screen tests.

### Committed exploration specialization

When the experience specifically contains preview → selection → explanation behavior, use the bounded specialization:

`INTENT → SCOUT → COMMIT → REVEAL → RETREAT / RETURN`

This is **not a mandatory universal sequence**. Use it only when the Current interaction claim actually contains these roles.

1. `SCOUT` is a reversible preview. It may increase local salience but must not silently create a persistent selection or replace route/world first-read.
2. `COMMIT` records the selected relation/object. The committed identity must remain stable through later mechanisms.
3. `REVEAL` may expose explanation, detail, memory, or relation after commitment when that ordering is part of the experience claim. A reveal with no selected world/object anchor defaults to `REVISE`.
4. `RETREAT` moves backward without destroying underlying world/route context. `RETURN` clears optional exploration state and restores the defined route/service baseline.
5. Selected relations require persistent state memory. Rapid switching, interruption, or re-entry must not orphan an explanation panel, leader, world anchor, focus state, or previous selection.
6. Required states cannot depend on hover alone. Pointer, keyboard, touch, switch/accessibility input and focus behavior must preserve the same state meaning even when gestures differ.
7. Safety, route, closure, service and Return remain outside optional interpretation. A committed explanatory state cannot hide or disable them.

Hard FAIL:
- a reveal appears with no persistent selected object/relation when selection is required by the interaction claim;
- commit cannot be reversed or cleared;
- Return changes location but leaves stale exploration state;
- switching targets leaves panel/leader/focus bound to the previous target;
- keyboard/touch cannot reach a required state available to pointer users;
- Reduced Motion removes required state information;
- optional exploration blocks route, safety, closure, service recovery or Return;
- mobile/narrow carriers clip or detach the world anchor, selected relation, state label or Return cue.

This gate extends MOT-02 State Transition and MOT-03 Spatial Continuity. It does not create a separate motion/game-UI framework. It proves a designed temporal/interaction relationship only; it does not prove comprehension, delight, game feel, accessibility conformance, spatial truth, field usability, implementation quality or production readiness without the corresponding tests.

## Required practice loop

For a formal motion exercise, produce the same state change as:

`No-motion Baseline → Candidate A → Candidate B or Timing Variant → Reduced Motion → Real Runtime Review → Keep / Reduce / Remove`

Record:
- tool and version;
- library/runtime and version when applicable;
- device/canvas/browser and refresh conditions;
- state diagram and trigger;
- key durations/curves or physics parameters;
- source and export files;
- actual playback/runtime evidence;
- failure modes;
- keep/reduce/remove decision.

Do not claim improved comprehension, efficiency, comfort, or accessibility without an appropriate real test.

## AR-S10 Motion review

Run OLEANDER Common Review plus this motion-specific gate.

Check separately:
- Motion Role and no-motion baseline;
- state before/after and causal legibility;
- timing/easing versus distance, task frequency and information load;
- attention cost and unnecessary waiting;
- loop / interrupt / reverse / rapid repeat behavior;
- occlusion, clearance, hierarchy and path conflicts;
- actual frame rate, jank, input latency and first-load blocking;
- Reduced Motion information equivalence;
- cross-device/browser/refresh-rate behavior;
- dependency/bundle/GPU cost when a library or shader is introduced;
- native scrolling, keyboard, focus and pointer behavior after motion infrastructure is added;
- source ↔ export consistency;
- reopen and reproduction.

Hard FAIL:
- disabling motion deletes required information;
- motion blocks a critical task;
- unsafe flashing or aggressive zoom/parallax is introduced;
- sustained jank changes the task relationship;
- a loop cannot be exited;
- motion occludes required content;
- a scroll or cursor layer breaks expected native control without a justified fallback;
- export behavior materially differs from the reviewed source.

A screen recording, video render, vendor demo, component gallery, or automated PASS is not a substitute for target-runtime review.

## OLEANDER project applications

Prefer real project questions over generic exercises, including:
- irreversible-revision motion for the OLEANDER symbol system;
- Timer Light Basin remaining-time light/state transitions;
- product exploded/assembly motion;
- website navigation and state continuity;
- spatial route/time transitions;
- GIS and data time-series transitions.

Preserve the OLEANDER evidence boundary: motion prototypes demonstrate a designed temporal behavior; they do not prove user response, implementation, engineering performance, cultural acceptance, or release approval.
