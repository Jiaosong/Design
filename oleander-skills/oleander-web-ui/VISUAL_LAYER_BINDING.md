# Web UI Visual / Effect Layer Binding

Status: **BINDING ONLY / NO NEW WEB OR EFFECT METHODOLOGY**

This binding connects the existing `oleander-web-ui` composite route to the installed `oleander-motion` owner when browser effects, scroll-linked motion, shader surfaces, DOM↔WebGL proxies or multi-renderer choreography are material.

It does not create a new Effect Skill, does not promote `oleander-web-ui` beyond its Candidate status, and does not make any external library a default dependency.

## Existing sources to inherit

1. Local `SKILL.md` — Current web integration sequence, Requirement Coverage Map, source-asset role pass, responsive/accessibility rules and real-browser readback.
2. `oleander-motion/SKILL.md` — Motion Role, no-motion baseline, runtime and AR-S10 authority.
3. `oleander-motion/MOTION_LIBRARY_EFFECT_ATLAS.md` — effect/library selection and avoid-by-default mechanisms.
4. `oleander-motion/EFFECT_SIGNAL_PRIMITIVE_RUNTIME_EXTENSION.md` when non-trivial signal mapping, shader, DOM↔WebGL, shared-canvas, 3D proxy or post-processing behavior is introduced.
5. Current Project Authority / Design DNA / Visual Bible when project-specific motion or material language exists.
6. Existing accessibility/responsive extensions in this owner when the effect crosses those boundaries.

## Routing rule

Keep the existing web order:

`TASK / IA → WAYFINDING → WITHIN-PAGE LAYOUT → INTERACTION STATE → ACCESSIBILITY CROSS-CHECK → MOTION → REAL BROWSER RETEST`.

When Motion selects a non-trivial effect, continue through:

`STATE / INFORMATION DUTY → SIGNAL → MAPPING → PRIMITIVE → RENDERER → QUALITY / FALLBACK → REAL BROWSER → AR-S10 + WEB READBACK → REPAIR / RETEST`.

Do not start from a library or shader demo and retrofit page meaning around it.

## Requirement Coverage Map binding

Material effects are first-class implementation objects, not polish notes. Extend the existing coverage row as applicable:

`REQUEST / SOURCE → TARGET REGION / COMPONENT → REQUIRED STATE / BEHAVIOR → SIGNAL → MAPPING → PRIMITIVE → RENDERER → QUALITY / FALLBACK → ACCEPTANCE EVIDENCE → STATUS`.

If an effect is non-material decoration, it does not need to be forced into the map; it may instead be removed under the Motion Role / Design Purpose gate.

## DOM ↔ visual proxy rule

For ordinary browser interfaces:

- DOM/SVG owns document flow, semantic text, focus, selection, accessibility and responsive structure;
- WebGL/Three may provide a visual proxy or spatial renderer where justified;
- required text and state meaning cannot exist only inside Canvas;
- proxy geometry must remain synchronized after resize/reflow;
- stable semantic IDs should connect DOM objects, scene objects and QA evidence;
- one shared Canvas/context is preferred when it materially reduces duplicated measurement/render cost and does not create layering/lifecycle conflicts;
- Q0/no-WebGL and Reduced Motion paths must preserve the task and required information.

`CANVAS EFFECT ≠ PAGE AUTHORITY`.

## Runtime readback additions

When the Motion effect extension is active, browser readback additionally attacks as applicable:

- desktop + mobile/touch behavior;
- breakpoint/reflow proxy drift;
- transition endpoint contamination;
- resize/remount/context lifecycle;
- DPR/pixel/sample/pass cost;
- idle continuous rendering;
- scroll/pointer/keyboard/focus regressions;
- Reduced Motion and Q0 equivalence;
- effect removal test: the page hierarchy and information architecture must still make sense without spectacle.

A vendor demo, recorded video, screenshot or shader playground is not browser evidence for the project.

## Project / design boundary

Effects inherit the project design system; they do not establish it. External component libraries, Codrops experiments, shader presets and WebGL demos are mechanism/provenance sources only. Strip source visual identity, rebuild parameters around the project relation, then review the actual rendered project.

`BROWSER PASS ≠ DESIGN KEEP`.
