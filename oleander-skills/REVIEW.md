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

This file is the current repository-state source for the installed reusable skills list. Installed-skill existence does **not** prove that a skill, prompt, or model version has passed regression evaluation; promotion remains governed by P0 and `evals/`.

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

## P0 AI governance checks

The skill review is no longer sufficient by itself. Every reusable skill is governed by `90-shared/OLEANDER_AI_Governance_P0_v0.1.md` and the repository `evals/` harness.

Before using or promoting a changed skill:

1. Run the AI Necessity Gate; do not use AI where deterministic, expert, or physical methods are more appropriate.
2. Execute or review the relevant Golden Cases in `evals/golden/skills.jsonl`.
3. If the task depends on workspace knowledge, check retrieval authority against `evals/retrieval/golden_queries.jsonl`.
4. Record model / tool / prompt / skill version and input object version.
5. Compare the candidate against the approved baseline.
6. Do not promote a candidate that introduces blocker regressions, unsupported claims, stale-source acceptance, truth-state collapse, rights/safety overreach, or non-reconstructable output.
7. Keep a rollback point.

### Minimum coverage

Each installed skill must have at least two maintained Golden Cases. CI validates case structure and P0 coverage; actual AI run results require explicit versioned evidence and human approval before `PROMOTE`.
