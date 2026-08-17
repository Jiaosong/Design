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

For route, travel, spatial exploration, museum/exhibition, game-like discovery, or other multi-step experiences, do not review each transition as an isolated visual effect. Establish a **behavior grammar** first.

Use:

`Journey / Task State → Behavioral Verb → Persistent World/Object → Relationship Change → Motion Mechanism → Reverse/Recovery → Reduced Motion`

Rules:
- derive behavioral verbs from the actual task or journey; do not impose a universal vocabulary when the experience requires different verbs;
- examples such as `approach → confirm → enter → orient → return` are a pattern, not a mandatory sequence;
- every transition must clarify at least one source/destination, causal, spatial, hierarchy, or task relationship;
- preserve a persistent world, object, route, or anchor across adjacent states when continuity is part of the experience; replacing the whole scene with another overlay is not continuity merely because it fades smoothly;
- forward and backward navigation should normally use the same reversible spatial/causal grammar; introduce a different exit effect only when the state semantics actually change;
- fade, glow, reveal, blur, light sweep and similar effects may reinforce a behavioral transition but cannot substitute for the transition relationship itself;
- evaluate the grammar across the sequence: individually polished screens can still fail if the temporal verbs change arbitrarily from screen to screen;
- for landscape-first or world-first experiences, move or reframe the relationship to the world before adding a dominant UI overlay; motion must not turn an environmental experience into an overlay-first map/dashboard without a task reason;
- Reduced Motion must preserve the same behavioral state, route continuity, action hierarchy and return logic through static structure, explicit state change, or near-instant transitions;
- run forward, reverse/back, rapid-repeat and small-screen tests. A desktop sequence that clips anchors, labels, return cues or state meaning on mobile is `REVISE` even when its desktop motion is strong.

Reject by default when a sequence can be described only as `fade / reveal / glow / withdraw` and those effects do not explain why the state changed, where the viewer is going, or how to return.

This gate extends MOT-03 Spatial Continuity and Narrative; it does not create a separate motion framework.

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
