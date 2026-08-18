# OLEANDER Default Skill Resolver v1.0

Status: **ACTIVE CURRENT**  
Decision date: **2026-08-18**  
Scope: **ALL OLEANDER projects / conversations / agents / media**  
Knowledge authority: **Notion OLEANDER Design Knowledge Base**  
Execution implementation: **GitHub `Jiaosong/Design`**

## 0｜Purpose

This contract resolves one recurring ambiguity: **OLEANDER capability is larger than the GitHub installed-skill list.**

Notion is the knowledge/method authority. GitHub carries executable reusable skills, candidate specialist skills, validators, runtimes and versioned implementations. Neither side replaces the other.

The default invariant is:

> **CURRENT AUTHORITY → KNOWLEDGE DOMAIN / L0–L7 → NOTION METHOD / THEORY / SOURCE / CASE / EVIDENCE / PRACTICE → EXISTING MATURE DESIGN / DESIGN SOURCE → GITHUB EXECUTABLE SKILL → REQUIRED NATIVE OUTPUT → CAPABILITY PROBE → REAL EXECUTION → ACTUAL READBACK → EVIDENCE GATE + INDEPENDENT DESIGN QUALITY GATE → GAP DIAGNOSIS → OPTIMIZE EXISTING SKILL ONLY IF NEEDED**

This resolver supplements the active Universal Production Environment. It does not create a parallel project-state system, parallel method registry or parallel review framework.

## 1｜Authority separation

### Notion = knowledge / method authority

Use the current OLEANDER Design Knowledge Base and `50｜Methods & Design Intelligence` to resolve task-relevant knowledge objects before production.

The current note registry distinguishes:

- `METHOD`
- `THEORY`
- `SOURCE`
- `CASE`
- `EVIDENCE`
- `TOOL`
- `PRACTICE`

Preserve the object's Domain / L0–L7 position, method state, governance state, evidence state, migration maturity and current/legacy boundary.

Canonical Notion resolver object:

`KN-METHOD-OLEANDER-SKILL-RESOLVER-001｜OLEANDER Skill Resolver｜知识方法优先的默认能力路由`

Notion URL:

`https://app.notion.com/p/3c0b86be5c478162993df939a1c2bf03`

### GitHub = executable implementation authority

GitHub contains reusable skill contracts, candidate specialist skills, validators, runtime adapters, regression fixtures and version history.

A GitHub skill file being present, merged or CI-green does not mean the underlying design method is the whole OLEANDER knowledge system, nor does it prove project Design PASS.

## 2｜Current capability layers

### Layer A — Installed reusable execution skills

The current installed list remains owned by `oleander-skills/REVIEW.md`:

1. `oleander-research`
2. `oleander-data-viz`
3. `oleander-3d-pipeline`
4. `oleander-story-and-board`
5. `oleander-delivery-qc`
6. `oleander-motion`

These are the formal reusable execution skills currently registered in the installed-skill review. They are **not** the complete OLEANDER design knowledge inventory.

### Layer B — Candidate specialist execution skills on main

Current candidate UI specialists:

- `oleander-game-ui`
- `oleander-mobile-game-ui`
- `oleander-ui-visual-composition`
- `oleander-route-wayfinding-ui`
- `oleander-ui-interaction`

`oleander-game-ui-stack` is a routing / Golden Cases / change-impact aggregation layer and is not counted as an additional independent specialist skill.

Candidate status must remain explicit. Merge or file existence does not silently promote a candidate to installed/validated.

### Layer C — Candidate / draft specialist development

Technical Drawing is currently a candidate knowledge/skill body, with implementation work carried by PR #172. Until explicit independent promotion, it must not be reported as an installed reusable skill.

### Layer D — Notion method intelligence

The Notion METHOD registry is the broader reusable design-intelligence layer. As-of 2026-08-18, it contains substantially more method objects than the six installed GitHub skills, including research, synthesis, strategy, generation, prototyping, analysis/modeling, evaluation, design translation, delivery/governance and AI collaboration methods.

The count is a snapshot, not a fixed invariant. Future routing queries the live registry rather than hard-coding a number.

## 3｜Default GPT / Agent behavior

When the user says any equivalent of:

- “按 OLEANDER 做”
- “继续项目”
- “用已有 Skill”
- “审查”
- “训练”
- “做成实际成果”
- “不要重新发明方法”

GPT / Agent defaults to the following sequence:

1. Read current OLEANDER Authority / Project State / Source Authority / Current Task when applicable.
2. Resolve the task's Domain, L0–L7 context and Decision Question.
3. Retrieve relevant current Notion METHOD / THEORY / SOURCE / CASE / EVIDENCE / PRACTICE objects.
4. Reuse existing mature design, design source and current project assets before inventing replacements.
5. Resolve an existing GitHub reusable skill or candidate specialist that reasonably owns the execution capability.
6. Define the required native output: editable vector, native geometry, HTML/CSS/JS, data, PDF, model, video, etc.
7. Probe the current execution surface and select the best-fit real production adapter.
8. Produce the actual artifact instead of stopping at a method description when the task is a production/design task.
9. Open/render/run the actual result and perform real readback.
10. Keep Evidence Gate and independent Design Quality Gate separate.
11. Diagnose the root cause of any failure.
12. Optimize an existing Skill only when real execution/readback proves a material reusable capability gap.
13. Create a new Skill only when no existing Skill can reasonably own the capability.
14. Synchronize material delta into current authority; preserve superseded/history objects as provenance.

## 4｜Existing-first rule

Canonical rule:

`CURRENT AUTHORITY / PROJECT FLOW → EXISTING MATURE DESIGN / DESIGN SOURCE → CURRENT PROJECT DELTA → NOTION METHOD RESOLVER → EXISTING GITHUB SKILL RESOLVER → REQUIRED NATIVE OUTPUT → REAL EXECUTION → ACTUAL READBACK → GAP DIAGNOSIS → OPTIMIZE EXISTING SKILL IF NEEDED → NEW SKILL ONLY IF NO EXISTING OWNER EXISTS`

Forbidden reasons for creating a new Skill by themselves:

- a case is interesting;
- a new name sounds useful;
- a training note exists;
- a PR or file can be created;
- CI is green;
- a one-off visual problem occurred before trying an existing owner;
- a candidate specialization can be represented as a submodule of an existing skill.

## 5｜Production-first rule

Design tasks default to **real production**, not AI-image substitution or documentation-only output.

- UI / web / interaction: real editable interface implementation first.
- Spatial / architecture / landscape: real geometry, vector drawings, plans/sections/axonometric or model assets first.
- Product / CMF: real form/material/process assets and editable specifications first.
- Data / information: source-bound data structures and editable vector/interactive outputs first.
- Motion: real state/motion implementation and runtime readback first.

AI-generated images are supplementary visualizations only when appropriate. They do not replace design authority, geometry, technical dimensions, editable text or real production assets. Any generated technical/spatial visualization must respect evidence and reality boundaries.

## 6｜Review default

OLEANDER Artifact Review remains the review authority:

`Gate 1｜Compliance + Gate 2｜Professional Design`

Hard separations:

- `Artifact existence ≠ Design quality`
- `Traceability ≠ Professional finish`
- `Evidence correctness ≠ Visual excellence`
- `Process PASS ≠ MAIN KEEP`
- `Render PASS ≠ Design PASS`
- `Prototype PASS ≠ Field PASS`

A producer/runtime may report execution and self-check evidence, but cannot self-promote its own artifact to a KEEP-class project verdict where independent review is required.

## 7｜No-loss default

`NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS`

Reorder, split, expand, reweight and change visual rhythm when needed. Do not delete valid design systems, evidence, audience depth, physical/sensory content, memory/IP, technical proof, return logic or other valid content merely to make a project look simpler.

## 8｜Truth and source boundary

Keep these roles distinct:

- Current Authority
- Source Authority
- Design Authority
- Native Source
- Derived Asset
- Diagnostic Asset
- Render / Preview
- Prototype
- Field Evidence
- Promotion State

Derived diagrams, render meshes, websites, videos and previews cannot silently replace source, geometry or design authority.

## 9｜Synchronization rule

For a material resolver change:

1. update the canonical Notion METHOD object;
2. update the Notion current Authority / Methods index pointer when the default changes;
3. update GitHub executable resolver/runtime/review implementation through branch → commit → PR → CI/readback;
4. keep only one CURRENT default resolver;
5. mark older wording as superseded/history where it conflicts;
6. do not treat chat summaries as Project State or authority.

## 10｜Does not prove

This resolver being ACTIVE does not promote every Notion method or GitHub candidate skill. It establishes **how OLEANDER GPT / Agents resolve and use capability by default**. Individual method validation, project evidence, independent design review, engineering/field truth and release/promotion remain separate gates.
