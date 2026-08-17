# Oleander skills review

## Installed skills

- `oleander-research`: Notion-first evidence, precedent, interview, and decision research.
- `oleander-data-viz`: reproducible table, chart, animation, map, and export workflow.
- `oleander-3d-pipeline`: 3D naming, units, exchange, axonometric, render, and archive workflow.
- `oleander-story-and-board`: shared narrative for boards, reports, decks, brand stories, and films.
- `oleander-delivery-qc`: non-destructive release checks for packages, rights, PDFs, images, video, audio, 3D, and interactive outputs.
- `oleander-motion`: purposeful motion design, native-first library routing, state-transition prototyping, 3D/procedural motion, interactive motion, Reduced Motion alternatives, delivery, effect selection and AR-S10 Motion QA.

## Retrieval alias / authority routing

Canonical query: **What are the currently installed OLEANDER reusable skills in GitHub?**

Search aliases: `installed OLEANDER reusable skills`, `current OLEANDER skills`, `GitHub reusable skills`, `oleander skills review`.

This file is the current repository-state source for the installed reusable skills list. Installed-skill existence does **not** prove that a skill, prompt, or model version has passed regression evaluation; promotion remains governed by AIG-01 and `evals/`.

## Review prompts

1. Research: Organize site studies, policies, precedents, and interviews into a traceable Notion research system.
2. Data visualization: Turn quarterly traffic, activity, and dwell-time data into interactive, animated, and editable outputs.
3. 3D pipeline: Hand a Blender scene to Unreal while producing a layered Illustrator-ready exploded axonometric.
4. Story and board: Compile approved findings, analysis diagrams, and renders into two A0 boards and a 12-page deck.
5. Delivery QC: Inspect A0 PDFs, a 4K film, render images, and a GLB model without modifying masters.
6. Motion: Design one state change as a no-motion baseline, candidate variants and Reduced Motion; justify any runtime library through the Motion Library & Effect Atlas and execute in a real runtime when available.

## Acceptance checks

- Research uses Notion rather than Zotero.
- GIS instructions target QGIS 4 and avoid QGIS 3 paths.
- Data work uses `C:\Users\Xianmu\.venvs\oleander`.
- 3D handoffs record units, axes, dependencies, versions, and exchange tests.
- Narrative outputs trace claims back to approved research.
- QC distinguishes blocking defects from warnings and never edits masters without permission.
- Motion identifies a real Motion Role, includes a no-motion baseline and Reduced Motion path, uses native-first library routing, distinguishes `DESIGNED / NOT RUN` from executed runtime evidence, and applies AR-S10 checks for timing, interruption, jank, latency, occlusion, accessibility, dependency/runtime cost and export consistency.

## Reference Reconstruction Fidelity Gate

For OLEANDER aesthetic / design-skill training, the word **reproduction / reconstruction / 复现** is reserved for a strict 1:1 fidelity exercise. A loose reinterpretation, style study, inspired variant, simplified teaching diagram, or principle-only A/B is **not** a reproduction.

Required sequence:

`ORIGINAL REFERENCE → SOURCE BYTES MATERIALIZED → REFERENCE FRAME LOCKED → 1:1 RECONSTRUCTION → SIDE-BY-SIDE / OVERLAY CRIT → FIDELITY REPAIR → METHOD EXTRACTION → TRANSFER VARIANT`

Do not skip the source-byte or 1:1 reconstruction stage when the training claim is that a reference has been reproduced.

### Reference Materialization Preflight

Before drawing, modeling, animating or laying out a claimed reproduction, resolve the current `OLEANDER_REFERENCE_MATERIALIZATION_GATE_v1.0` contract.

`BROWSER_VISIBLE ≠ LOCAL_SOURCE_BYTES_AVAILABLE`.

A browser/PDF view, citation ref, screenshot handle or connector preview does not automatically give Python / SVG / Blender / FFmpeg / diff tooling the original source bytes required for deterministic comparison.

Mandatory preflight:

`SOURCE AUTHORITY FOUND → SOURCE BYTES MATERIALIZED → SOURCE HASHED → REFERENCE FRAME EXTRACTED → REFERENCE SCALE LOCKED → COMPARISON RUNTIME VERIFIED`

Preferred adapter:

`python tools/oleander-runtime/materialize_reference.py ...`

If the source cannot be materialized or the exact reference frame cannot be locked, record `REFERENCE MATERIALIZATION GATE = HOLD`. Continue only as `STRUCTURAL RECONSTRUCTION / METHOD STUDY / REFERENCE-BOUND STUDY`; `REPRODUCTION PASS` is forbidden.

Do not wait until the end of a reconstruction to discover that overlay/difference comparison is impossible.

### Minimum reproduction standard

The reconstruction must aim to be visually indistinguishable from the available reference at the intended viewing scale, with no deliberate redesign before the fidelity gate. Match, as applicable:

- canvas / frame / aspect ratio and crop;
- primary mass, geometry, silhouette and object placement;
- grid, margins, alignment, spacing and whitespace;
- typography family or the closest legally/technically available equivalent, plus size, weight, leading, tracking and line breaks;
- lineweight, stroke hierarchy, icon/pictogram geometry and annotation placement;
- image scale, crop, tonal balance, color relationships and contrast;
- material, lighting, camera, lens/perspective and render relationship for 3D/spatial/product work;
- state timing, easing, path, overlap and key-frame relationships for motion/interaction work.

A result that is only “similar”, “captures the principle”, “has the same hierarchy”, or “looks inspired by the reference” remains `STRUCTURAL STUDY / VISUAL REVISE`, not `REPRODUCTION PASS`.

### Fidelity verification

Every claimed reproduction requires actual visual comparison against the materialized and locked reference:

- side-by-side at matched scale;
- overlay / flicker / difference view where the source medium permits;
- first-read plus near-read/detail review;
- pixel/geometry diff when technically meaningful, while accounting for unavoidable rasterization, antialiasing, color-management or rendering differences;
- explicit mismatch list and another repair cycle until no material visual mismatch remains.

If the source reference is incomplete, too low-resolution, unavailable, ambiguous in version/frame, or cannot support an honest 1:1 comparison, do **not** fabricate missing details and do **not** call the result a reproduction. Label it `STRUCTURAL RECONSTRUCTION`, `METHOD STUDY`, or `REFERENCE-BOUND STUDY` and keep the fidelity gate `HOLD`.

### Training and rights boundary

The 1:1 reconstruction is a study / calibration artifact used to learn professional visual judgment. It must not be presented as OLEANDER original authorship, substituted for the source project, or promoted as a public/commercial project deliverable. The transferable output is the extracted method and the independently designed transfer variant, not the copied reference artifact itself.

Source materialization proves only that a specific byte source and/or frame was acquired for comparison. It does not by itself prove Source Authority, rights clearance, reconstruction fidelity, design quality, or field/engineering truth.

### Skill promotion consequence

A principle extracted from a reference cannot receive a stronger visual-learning status merely because the explanation is correct. If the training task claims reproduction but the Reference Materialization Gate or 1:1 Fidelity Gate fails, record at most `OBSERVATION / STRUCTURAL STUDY`; do not use that failed reproduction as evidence for `CANDIDATE` promotion. Artifact existence, export success, traceability, source hashing and CI cannot override these gates.

## AIG-01 AI governance checks

The skill review is no longer sufficient by itself. Every reusable skill is governed by `90-shared/OLEANDER_AIG-01_Evaluation_Regression_v0.1.md` and the repository `evals/` harness.

Before using or promoting a changed skill:

1. Run the AI Necessity Gate; do not use AI where deterministic, expert, or physical methods are more appropriate.
2. Execute or review the relevant Golden Cases in `evals/golden/skills.jsonl`.
3. If the task depends on workspace knowledge, check retrieval authority against `evals/retrieval/golden_queries.jsonl`.
4. Record model / tool / prompt / skill version and input object version.
5. Compare the candidate against the approved baseline.
6. Do not promote a candidate that introduces blocker regressions, unsupported claims, stale-source acceptance, truth-state collapse, rights/safety overreach, or non-reconstructable output.
7. Keep a rollback point.

### Minimum coverage

Each installed skill must have at least two maintained Golden Cases. CI validates case structure and AIG-01 coverage; actual AI run results require explicit versioned evidence and human approval before `PROMOTE`.
