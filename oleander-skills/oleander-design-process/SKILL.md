---
name: oleander-design-process
description: Turn Oleander research, constraints and project questions into editable analysis diagrams, spatial/product/system options, design reasoning, comparison, and validation handoffs. Use for site/user/service analysis, design consequence mapping, massing, form finding, system design, concept-to-detail reasoning, and project design-process artifacts.
compatibility: Candidate reusable skill. Existing Skill First and Required Native Output First. Use SVG/HTML/Blender/data/CAD support only when the current authority and actual execution surface justify them; technical validation remains a separate downstream gate.
---

# Oleander Design Process

Convert evidence and constraints into design decisions through visible, editable, reviewable artifacts rather than prose-only explanation.

## Lifecycle role

- Primary: `DESIGN`
- Secondary: `KNOWLEDGE`, `VALIDATION`
- Status: `CANDIDATE`
- Upstream: `oleander-research`
- Downstream: `oleander-data-viz`, `oleander-3d-pipeline`, `oleander-visual-design`, `oleander-web-ui`, `oleander-technical-drawing`

## Specialist extension routing

Use only the minimum relevant extension:

- `PHYSICAL_PRODUCT_PHASE_GATES_EXTENSION.md` — physical products whose visual form depends on payload/cavity, human interface, mechanism, assembly or CMF sequencing;
- `PRODUCT_FORM_AFFORDANCE_SERVICEABILITY_EXTENSION.md` — physical form whose operation cues, body/contact relation, construction truth, serviceability or repair path need explicit review.

These are complementary. The phase-gate extension controls sequencing/fidelity; the affordance/serviceability extension attacks form/use honesty and lifecycle access. Neither is a manufacturing or ergonomic certification owner.

## Core sequence

`CURRENT PROJECT / SOURCE AUTHORITY → DESIGN QUESTION → EXISTING KNOWLEDGE + SKILL → REQUIREMENT / EVIDENCE COVERAGE MAP WHEN MULTI-PART → EVIDENCE / INFERENCE / ASSUMPTION / DECISION → REFERENCE STRUCTURE DECOMPOSITION WHEN APPLICABLE → ANALYSIS → DESIGN CONSEQUENCE → OPTIONS → EDITABLE DESIGN ARTIFACT → ACTUAL READBACK → DESIGN CRIT → ROOT CAUSE → REPAIR → VALIDATION HANDOFF WHEN NEEDED`

## What this skill owns

- site/context/user/behavior/service/route/system analysis;
- Research → Finding → Design Consequence;
- analysis diagrams, mappings, relation maps and sequence diagrams;
- spatial organization, massing, circulation, section logic and thresholds;
- product need → function → component → proportion → form → structure → material/interaction reasoning;
- information architecture, user flow and state models before final UI polish;
- option generation and deletion tests;
- design models used for reasoning, not merely rendering;
- project-specific transfer rules and Candidate design-method records.

## Requirement / evidence coverage map

Use this when a task contains multiple requested outputs, source assets, interactions, states or review obligations. Before design options are treated as complete, map each material requirement to an accountable object:

`REQUEST / SOURCE → DESIGN CONSEQUENCE → TARGET OBJECT / REGION → REQUIRED STATE OR PROOF → ACCEPTANCE EVIDENCE → STATUS`.

This prevents attractive outputs from silently omitting one source, state or deliverable. Approved omissions must be explicit. The map is a working design-control artifact and should not leak into public-facing design copy.

## Reference decomposition gate

When a user/project supplies a concrete reference, adopted version or mature example, separate **relation** from **style** before generating options. Record the aspects that materially govern the design problem, such as:

- hierarchy and dominant alignment;
- density and whitespace rhythm;
- object/media scale and crop behavior;
- section/sequence order;
- interaction/state relationship;
- repeated visual/spatial grammar;
- motion ownership where temporal behavior matters.

Then translate those relationships into the project's own content, authority and constraints. Do not reproduce third-party identity, proprietary template expression or irrelevant surface decoration.

Use:

`REFERENCE → STRUCTURAL RELATIONS → PROJECT-SPECIFIC CONSEQUENCES → OPTIONS → RENDERED / ARTIFACT DELTA REVIEW`.

## Evidence-density gate

Do not equate more modules with more design depth. If truthful content/evidence is sparse, reduce the number of objects and strengthen the role, scale, sequence and whitespace around the best available proof. Do not invent metrics, testimonials, images, modules or decorative analysis to make the artifact look complete.

`LOW EVIDENCE DENSITY → FEWER STRONGER OBJECTS`, not filler.

## Rules

1. Start from a real project question or genuine capability gap; do not invent exercises merely to use software.
2. Existing Skill First. Do not create a new method/Skill where a current one already covers the problem.
3. Keep evidence, inference, assumption and decision visually and semantically separate.
4. Every substantial round must create at least one editable design artifact. Text explanation alone is not completion.
5. Compare at least two options, an A/B, Before/After or deletion test when alternatives materially affect the decision.
6. Actual Readback is mandatory. Inspect the artifact/model/page itself.
7. Design Quality is independent from evidence correctness and technical validity. A logically correct analysis can still be visually or spatially weak.
8. Existing Mature Design First: do not regress a stronger current artifact merely because a new method is cleaner or more systematic.
9. When exact dimensions or technical facts are unresolved, preserve the uncertainty and generate a Validation Handoff rather than inventing closure.
10. A design artifact cannot certify browser behavior, CAD roundtrip, engineering approval, field truth or machine safety.
11. Do not treat a visual reference as a template license. Extract only the relations relevant to the project problem and keep source/rights boundaries explicit.
12. Do not fill missing evidence with decorative content. Missing proof remains missing proof even when a composition would benefit from more density.
13. For physical-product form, do not let decorative/function-like cues silently imply ventilation, fastening, grip, motion, structure or service access that the object does not actually provide. Route material affordance/serviceability questions through the corresponding extension.

## Semantic-dimension-to-form gate

Use this gate when one project claim, behavior or requirement contains more than one relation type and form generation risks collapsing them into literal decoration.

1. Split the input into semantic dimensions before sketching form: `DISCRETE / CONTINUOUS / DIRECTIONAL / RELATIONAL / HIERARCHICAL / TEMPORAL`.
2. Assign different form roles when dimensions differ. Example: discrete state may use a stepped/notched event while continuous duration may use elongation, span or uninterrupted mass.
3. Generate at least two mappings. One option must attack the most literal translation so its failure is visible rather than silently avoided.
4. Run a deletion test: remove labels, numbering, arrows and decorative color. The selected form should still preserve the intended relation type.
5. Reject literal counting decoration when it only reproduces the number of graphic elements without preserving the relation.
6. If the selected form creates production, structural, ergonomic or safety geometry, stop at the design decision and emit a Validation Handoff.

Promotion test:

`REMOVE LABELS + DECORATIVE COLOR → DOES THE FORM STILL PRESERVE THE RELATION TYPE, NOT MERELY THE NUMBER OF GRAPHIC ELEMENTS?`

Validated training evidence remains Candidate-only and must record the project application and technical HOLD boundary.

## Validation handoff

When technical proof is needed, return:
- Object ID and upstream Current design master;
- Required Native Output;
- expected design behavior/relationship;
- units/scale/axis/canvas/CRS where relevant;
- dimension or geometry authority;
- exchange format;
- known assumptions;
- expected validation;
- residual HOLD boundary.

The returned PASS/REVISE/HOLD must feed back into the design. Do not let validation evidence float separately from the object it changes.

## Skill record

A reusable method becomes a Candidate only after real artifact creation, readback and repair. Record Problem / Trigger / Inputs / Technique / Parameters or Conditions / Expected Result / Failure Symptoms / Counterexample / Transfer Boundary / Applicable Domains / Application Mapping / Status.

## Candidate boundary

This skill is Candidate. It cannot self-promote, self-KEEP, replace technical validation, or claim final presentation quality merely because the reasoning is coherent.