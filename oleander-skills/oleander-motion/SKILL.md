---
name: oleander-motion
description: Design, prototype, implement, and review purposeful motion for OLEANDER across brand, interface, product, 3D, spatial, and data contexts. Use whenever a task involves animation, state transitions, motion language, micro-interactions, scroll/gesture motion, Blender animation, procedural motion, animated data, Lottie/Rive, motion accessibility, or motion QA.
compatibility: Prefer Figma, Blender, browser-native CSS/WAAPI/JavaScript/GSAP/Three.js when available; may use Rive, Lottie, After Effects, Framer, or TouchDesigner only when the real toolchain is available. Unavailable runtime steps stay PENDING.
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

- **Figma:** component states, prototype paths, Smart Animate, quick interaction validation.
- **Blender:** product/spatial/brand 3D motion, camera, Graph Editor, Drivers, Geometry Nodes and simulation.
- **Web:** CSS Transitions/Animations, WAAPI, JavaScript/GSAP and Three.js for implemented interactive motion.
- **Rive / Lottie / After Effects / Framer / TouchDesigner:** use only when the actual environment is available and the task benefits from that medium.

Do not claim execution in unavailable software. A storyboard, timeline specification, or code draft is `DESIGNED / NOT RUN` until executed in a real runtime.

## Required practice loop

For a formal motion exercise, produce the same state change as:

`No-motion Baseline → Candidate A → Candidate B or Timing Variant → Reduced Motion → Real Runtime Review → Keep / Reduce / Remove`

Record:
- tool and version;
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
- source ↔ export consistency;
- reopen and reproduction.

Hard FAIL:
- disabling motion deletes required information;
- motion blocks a critical task;
- unsafe flashing or aggressive zoom/parallax is introduced;
- sustained jank changes the task relationship;
- a loop cannot be exited;
- motion occludes required content;
- export behavior materially differs from the reviewed source.

A screen recording, video render, or automated PASS is not a substitute for target-runtime review.

## OLEANDER project applications

Prefer real project questions over generic exercises, including:
- irreversible-revision motion for the OLEANDER symbol system;
- Timer Light Basin remaining-time light/state transitions;
- product exploded/assembly motion;
- website navigation and state continuity;
- spatial route/time transitions;
- GIS and data time-series transitions.

Preserve the OLEANDER evidence boundary: motion prototypes demonstrate a designed temporal behavior; they do not prove user response, implementation, engineering performance, cultural acceptance, or release approval.
