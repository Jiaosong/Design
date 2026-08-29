---
name: oleander-design-process
description: Turn OLEANDER Current authority, evidence, constraints and design goals into materially different options, right-fidelity editable artifacts, critique/repair loops, controlled specialist handoffs and post-decision readback. Use for site/user/service analysis, design consequence mapping, spatial/product/system reasoning, option-space generation, form finding, concept-to-detail reasoning and project design-process artifacts.
compatibility: Installed reusable skill. Existing Skill First, Current Knowledge First when applicable, and Required Native Output First. This skill owns design reasoning and design-state progression; research authority, specialist technical validation, final presentation quality and release QC remain separate owners.
---

# Oleander Design Process

Convert evidence and constraints into design decisions through visible, editable, reviewable artifacts. The process must expose why a design exists, what remains uncertain, what alternatives were rejected, what was actually tested, and what evidence can reopen the decision.

## Lifecycle role

- Primary: `DESIGN`
- Secondary: `KNOWLEDGE`, `VALIDATION`
- Status: `ACTIVE / INSTALLED`
- Upstream: `oleander-research`
- Downstream: `oleander-data-viz`, `oleander-3d-pipeline`, `oleander-visual-design`, `oleander-web-ui`, `oleander-technical-drawing`, `oleander-story-and-board`, `oleander-image-art-direction`, `oleander-motion`

This skill does **not** replace the OLEANDER Project Control Plane. It compiles into the existing orchestration:

`Resolve → Frame → Execute → Review → Decide → Persist/Sync when triggered`

The design-specific cognitive loop is:

`Resolve → Frame Goal → Map Evidence + Unknowns → Synthesize Relations → Diverge → Converge → Construct → Attack → Readback/Crit → Repair → Validate/Return → Present/Release Handoff → Post-use Readback → Knowledge Return`

This is not a fixed waterfall. Any material failure may reopen the correct earlier layer.

## Current knowledge routing anchors

When applicable, resolve the Current canonical Notion owner before inventing local rules:

- `KN-METHOD-DESIGN-GOAL-CONTRACT-001` — actor/context/outcome/guardrail, Need vs Goal vs Objective vs Requirement vs Criterion;
- `KN-METHOD-DESIGN-TRADE-STUDY-001` — alternatives, hard gates, uncertainty, sensitivity, decision corridor and post-decision validation;
- `KN-METHOD-PRODUCT-PRINCIPLES-001` — repeated conflict, scope, falsifiability, exceptions, precedence and retirement;
- `KN-THEORY-VISUAL-PERCEPTUAL-ORG-001` — perceptual grouping, figure-ground, cue competition and perturbation tests.

These anchors are routing references, not copied authority. Project Current and specialist Source Authority still override generic knowledge where required.

## Specialist extension routing

Use only the minimum relevant extension:

- `PHYSICAL_PRODUCT_PHASE_GATES_EXTENSION.md` — physical products whose visual form depends on payload/cavity, human interface, mechanism, assembly or CMF sequencing;
- `PRODUCT_FORM_AFFORDANCE_SERVICEABILITY_EXTENSION.md` — physical form whose operation cues, body/contact relation, construction truth, serviceability or repair path need explicit review;
- `PACKAGING_STRUCTURE_DIELINE_EXTENSION.md` — packaging where panel logic, cut/crease/glue/lock, opening, assembly, face hierarchy or production geometry materially govern the design;
- `SYSTEM_INTERFACE_COUPLING_EXTENSION.md` — systems where service state, permission, interface coupling, dependency or cross-object change control must become visible design consequences.

Extensions refine the current object. They do not create a second project process and do not replace manufacturing, ergonomics, code, engineering or human-test authority.

## Full process

### 0 — Resolve authority, mode and decision object

Before designing, resolve:

`PROJECT / OBJECT → MODE → CURRENT AUTHORITY → DECISION QUESTION → LOCKED VARIABLES → OPEN VARIABLES → REQUIRED NATIVE OUTPUT → REQUIRED QA`

Use the Control Plane modes `EXPLORE / CANDIDATE / AUTHORITY`.

Rules:
- one substantial round has one primary Decision Question;
- do not design against a Legacy/superseded carrier as if it were Current;
- do not reopen locked variables merely because a new form is attractive;
- if the source cannot be located, route to asset/source recovery before reconstructing from memory.

Use a **Variable Budget** for each substantial round:

`PRIMARY VARIABLE FAMILY + NECESSARY DEPENDENT VARIABLES + LOCKED VARIABLES`

Primary families may include `Parameter / Relation / Geometry / Topology / Material-CMF / Interaction-State / Information-Hierarchy / Narrative-Sequence`. Change one primary family by default. A secondary change is allowed only when it is a necessary consequence of the primary change and is recorded as such.

If several unrelated families change at once, the comparison may still produce a design candidate, but it cannot honestly claim which change caused the improvement. Split the next test.

**Phase exit:** the object, authority, question, allowed design freedom and current Variable Budget are explicit.

### 1 — Frame the design goal before form

Do not start from adjectives such as `高级 / 年轻 / 极简 / 冲击力 / 科技感 / 更好看`.

Frame:

`ACTOR + CONTEXT + CURRENT CONDITION + INTENDED OUTCOME + DESIGN RELATIONSHIP + SUCCESS SIGNAL + GUARDRAIL + HARD CONSTRAINT + UNKNOWN + OWNER + REOPEN TRIGGER`

Separate:
- Need — what problem/gap exists;
- Goal — what outcome should improve/protect;
- Objective — a more specific target state where appropriate;
- Requirement / Hard Constraint — what cannot be traded away;
- Criterion — what can discriminate alternatives;
- Metric / Signal — one observation channel, never the goal itself.

Create a causal hypothesis when the path is not obvious:

`CURRENT CONDITION → RELATION / MECHANISM → ACTOR OR SYSTEM RESPONSE → INTENDED OUTCOME`

Mark critical links as fact/source/inference/hypothesis/unknown according to project conventions.

**Phase exit:** the design question is falsifiable enough that a test could change the decision.

### 2 — Build the requirement, evidence and unknown map

For multi-part work, maintain:

`REQUEST / SOURCE → DESIGN CONSEQUENCE → TARGET OBJECT / REGION → REQUIRED STATE OR PROOF → ACCEPTANCE EVIDENCE → STATUS`

Also identify:
- what is known strongly enough to constrain design;
- what is only an inference or assumption;
- which unknown is most likely to change the design decision;
- which evidence can be deferred without corrupting the current design round.

Use evidence density honestly:

`LOW EVIDENCE DENSITY → FEWER STRONGER OBJECTS`

Never add decorative modules, invented metrics, synthetic testimonials or fabricated analysis to make an artifact look complete.

**Phase exit:** missing proof is visible and the next design move does not depend on pretending it is closed.

### 3 — Synthesize evidence into design relations

The core translation is not `research → moodboard → form`.

Use:

`SOURCE / OBSERVATION → FINDING → RELATION / FAILURE MODE → DESIGN CONSEQUENCE → TESTABLE DESIGN VARIABLE`

Examples:
- program relation → adjacency/separation/flow → massing or section consequence;
- service state → allowed next action → threshold/path/interface consequence;
- maintenance requirement → access/dependency/reassembly → component or spatial serviceability consequence;
- environmental requirement → zone role → envelope openness/protection → section consequence;
- task sequence → purpose/function/sequence → control grouping/order/prominence;
- claim/state distinction → semantic dimension → different form role.

When one input contains multiple relation types, split it before form:
`DISCRETE / CONTINUOUS / DIRECTIONAL / RELATIONAL / HIERARCHICAL / TEMPORAL`.

**Phase exit:** at least one relation can be seen or attacked without relying on explanatory prose.

### 4 — Diverge into a real option space

Generate materially different alternatives before polishing one direction.

A valid option difference should change at least one important:
- functional allocation;
- spatial organization / adjacency / topology;
- interface or permission structure;
- component architecture;
- section / massing relation;
- interaction/state model;
- information hierarchy;
- causal mechanism.

Run the **surface-off test**:

`REMOVE COLOR / MATERIAL / FACADE / DECORATION → DO THE OPTIONS STILL DIFFER IN A DECISION-RELEVANT WAY?`

If not, they are variants of one concept, not a broad option space.

At least two materially different options are required when alternatives genuinely exist. A single route is acceptable only when authority/hard constraints already eliminate alternatives; record why.

Include:
- status quo / no-change when relevant;
- one option that attacks the most literal interpretation;
- at least one adverse-condition or deletion-test candidate where useful.

Run an **Option Space Coverage** check. For each candidate record:

`CONCEPT FAMILY → MATERIAL STRUCTURAL DELTA → MAIN TRADE-OFF → WHAT WOULD FALSIFY IT`

Use the **concept-family test**:

`CAN OPTION A BECOME OPTION B THROUGH SMALL PARAMETER TUNING WITHOUT CHANGING FUNCTIONAL ALLOCATION / TOPOLOGY / INTERFACE PERMISSION / CAUSAL MECHANISM?`

If yes, they are usually variants within one concept family. Do not count parameter spread as architectural diversity. Coverage is sufficient when the option set exposes the material trade-off axes relevant to the Decision Question; no fixed concept count is required.

**Phase exit:** the option set is broad enough to expose the real trade-off, not only stylistic preference, and concept-family duplication is visible.

### 5 — Converge without score theatre

Before selection, separate:
1. hard gates / veto conditions;
2. criteria with traceable sources;
3. uncertainty / unknowns;
4. stakeholder/value conflict;
5. specialist judgments that DESIGN cannot own.

Use the Current Trade Study owner where comparison is non-trivial.

Prefer:
`DOMINANCE CHECK → PARETO / DECISION CORRIDOR → SENSITIVITY / ROBUSTNESS → DISCRIMINATING TEST → DECISION`

Do not:
- invent 1–5 scores for unknown facts;
- tune weights until the preferred option wins;
- count vague synonyms such as `美观 / 高级 / 创新` as separate criteria;
- let a small total-score difference masquerade as objective certainty.

Selection outputs:
`SELECT / KEEP CANDIDATE / REVISE / REJECT / HOLD`, plus rejected alternatives and rationale.

**Phase exit:** the chosen direction and unresolved trade-offs are explicit, and the selection rule was not changed after seeing the result.

### 6 — Construct the minimum faithful prototype

Choose the **minimum fidelity that can test the current uncertainty**. Do not increase fidelity as a substitute for resolving a relationship.

Representation may be:
- relation diagram / storyboard / sequence;
- SVG / editable board;
- wireframe / HTML state prototype;
- physical mockup / dieline;
- section / massing / CAD/Blender model;
- data/map/interactive artifact.

Use the **Prototype Fidelity Matrix**:

`UNKNOWN TYPE → MINIMUM VALID TEST MEDIUM → CLAIM LIMIT`

Typical routing:
- hierarchy / proportion / composition → editable SVG/layout at target reading size;
- adjacency / path / threshold / section relation → plan + section and, when needed, simple 3D;
- interaction / state / Return / interruption → executable interaction prototype or real browser/runtime;
- motion timing → runtime motion, not keyframe screenshots alone;
- material / texture / grip / tactile behavior → real sample or physical mockup;
- assembly / disassembly / repair access → physical/CAD assembly with dependency sequence;
- packaging opening / fold / lock → dieline + physical mockup where the behavior matters;
- print color / small type / finishing → controlled proof at intended process/scale;
- field / structural / engineering / safety truth → specialist evidence; a design prototype is insufficient.

A representation is invalid for the current test when its medium cannot expose the claimed failure mode. Do not use high visual fidelity to compensate for the wrong test medium.

Rules:
- use Required Native Output First;
- preserve editable master identity;
- representative fidelity must match the claim being tested;
- if the question is relation/topology, do not hide it under presentation polish;
- if the question is material/ergonomic/engineering/field reality, emit specialist validation rather than simulating certainty.

**Phase exit:** a real artifact exists that can falsify or strengthen the design hypothesis.

### 7 — Attack, actual-readback and design crit

Actual Readback is mandatory. Inspect the artifact/model/page/runtime itself.

Attack at the correct layer:
- deletion / label-off / color-off / style-off;
- grayscale / distance / thumbnail;
- adverse load / simultaneous use / error / interruption;
- sequence reversal / missing state / edge case;
- alternate actor / maintenance / accessibility / service route;
- cross-view consistency: plan↔section, state↔interface, model↔drawing;
- reference fidelity when the task is explicitly reconstruction.

Use two orthogonal readback sweeps when applicable:

`WHOLE → REGION → OBJECT → DETAIL`

and

`FIRST READ → SECOND READ → NEAR READ → USE READ`

A Whole-level PASS does not excuse a broken detail, and a polished detail does not repair a weak whole. Static first-read quality does not prove real use sequence.

Separate:
- Machine QA;
- Visual QA;
- Project QA;
- triggered specialist validation.

Design Crit asks:
- does it answer the Decision Question;
- does the form/space/system still carry the intended relation without explanatory decoration;
- is the first read correct;
- is hierarchy and proportion professionally resolved;
- is any false grouping, false affordance, false structural cue or unsupported claim introduced;
- is the artifact stronger than the current mature design, not merely more systematic.

**Phase exit:** concrete failure/root cause is identified, or the design survives the attacks relevant to this round.

### 8 — Repair at root cause, not at the surface

Classify the failure:

`Parameter / Relation / Geometry / Topology / Architecture / Evidence`

Do not respond to a Relation/Topology failure with more resolution, nicer materials or typography.

Preserve a compact repair record:

`FAILURE → ROOT CAUSE → CHANGED VARIABLE → LOCKED VARIABLES PRESERVED → NEW READBACK → RESULT`

After two repeated REVISE cycles on the same Decision Question, use the Control Plane repeated-revise breaker and reclassify the root cause before another iteration.

**Phase exit:** the artifact is re-read after the actual repair, not just re-exported.

### 9 — Validation handoff and return loop

When technical proof is needed, hand off:
- Object ID and Current editable master;
- expected behavior / relation to preserve;
- Required Native Output;
- units / scale / axis / canvas / CRS where relevant;
- dimension / geometry authority;
- exchange format;
- assumptions / unknowns;
- exact test variable / acceptance evidence;
- change authority;
- residual HOLD boundary.

Validation may return `PASS / REVISE / HOLD`, but may not silently edit DESIGN-owned invariants.

If validation proposes a change:

`REQUIREMENT / FINDING → CHANGE REQUEST → DESIGN DISPOSITION → REVISED MASTER OR HOLD → RETEST`

The returned result must feed the same object. Floating validation evidence is not closure.

**Phase exit:** technical findings are either absorbed into the master, explicitly rejected with authority, or retained as HOLD.

### 10 — Presentation handoff without design-state collapse

DESIGN does not own final presentation quality.

When a design candidate is ready for PRESENTATION, hand off:
- page/object claim hierarchy;
- Current assets and source/provenance;
- locked spatial/product/system relations;
- permitted crop/layout/image/text freedoms;
- evidence labels that must remain;
- unresolved HOLDs;
- target medium / reading distance / viewport / sequence;
- what presentation must not imply.

Also issue a compact **Design Continuity Contract** for the relations that must survive presentation:

`PRIMARY RELATIONSHIP → DOMINANT HIERARCHY → KEY PROPORTION / GEOMETRY → SPATIAL OR INTERACTION SEQUENCE → EVIDENCE HIERARCHY → MATERIAL/CMF ROLE WHEN MATERIAL → ALLOWED PRESENTATION DELTA`

PRESENTATION may improve crop, grid, pacing, typography, image treatment and media-specific expression inside the allowed delta. It must not silently re-author locked geometry, route topology, interaction priority, evidence order or product/spatial relation simply to fit a layout.

Route to the minimum specialist owner set:
`oleander-visual-design / oleander-image-art-direction / oleander-story-and-board / oleander-web-ui / oleander-motion / oleander-data-viz`.

Presentation may expose a design weakness. If so, return to the correct design layer instead of forcing the layout to hide it.

**Phase exit:** presentation has a clean contract and cannot silently rewrite design truth.

### 11 — Release, persistence and post-use readback

Release/QC remains downstream. Persist only when triggered by the Control Plane.

Before a design decision becomes durable, preserve a compact **Design Decision Record**:

`DECISION → WHY → SUPPORTING EVIDENCE → REJECTED ALTERNATIVES → LOCKED VARIABLES → REMAINING UNKNOWN → REOPEN TRIGGER → EDITABLE MASTER`

This is not a second governance receipt. It prevents a later revision from unknowingly reopening or reversing a consequential design decision.

For any material change, run **Change Propagation** before declaring the repair local:

`CHANGE → AFFECTED OBJECTS / VIEWS / STATES → AUTHORITY IMPACT → REQUIRED RETEST → DERIVATIVES TO REGENERATE → STATUS`

Check, as applicable, model/drawing, plan/section, UI states, route, board, web, video, package, evidence captions and validation receipts. A local edit is not closed if dependent artifacts still communicate the previous decision.

Before a design decision becomes durable, also record:
- chosen option and rejected alternatives;
- Locked / Open variables;
- rationale and supporting evidence;
- known uncertainty;
- specialist PASS/HOLD;
- reopen trigger;
- editable master identity.

After implementation/use when evidence exists, compare:
`PREDICTED RELATION / OUTCOME → OBSERVED RESULT → FAILURE / SIDE EFFECT → DECISION / PRINCIPLE / METHOD REVISION`

Do not treat launch, render, build, CI, print export or file existence as outcome proof.

### 12 — Knowledge return

Only after real artifact creation, readback and repair should a reusable method/rule become Practice/Candidate evidence.

Return:
`CONTEXT → GAP → EXISTING OWNER → ARTIFACT → TEST/ATTACK → FAILURE → ROOT CAUSE → REPAIR/RETEST → TRANSFER RULE → BOUNDARY → MATURITY → HANDOFF TO CURRENT OWNER`

Cross-context evidence should strengthen an existing owner when possible. Do not create a new Skill merely because a project produced an interesting move.

## Smallest falsifiable loop

Default to the shortest loop that can change the decision:

`DECISION QUESTION → KEY UNKNOWN → 2+ MATERIAL ALTERNATIVES OR ONE CONSTRAINED HYPOTHESIS → MINIMUM FAITHFUL ARTIFACT → ATTACK → READBACK → DECIDE / REOPEN`

This is the main efficiency rule. More process is not automatically better process.

## Open / locked variable discipline

At every substantial round:
- Lock what is already authoritative or sufficiently proven;
- Open only the variables required by the Decision Question;
- record any intentional re-opening and why;
- do not change several unrelated variables if the result cannot be attributed.

A/B/C comparison should keep fixed conditions explicit.

## Process health detectors

These are anomaly signals, not performance KPIs and not promotion scores. Use them to decide when the process itself needs repair:

- repeated REVISE on the same Decision Question;
- too many simultaneously Open unrelated variable families;
- unverified assumptions that survive into high fidelity;
- decisions repeatedly reopened without a new trigger/evidence;
- artifact exists but Actual Readback is missing;
- validation finding has no Design Disposition;
- presentation changes a locked relation or geometry;
- downstream derivative remains stale after an upstream design change;
- option set contains several cosmetic variants but only one concept family.

A detector firing does not automatically reject the design. It requires the correct owner to inspect the cause.

## Reference decomposition gate

When a user/project supplies a concrete reference, adopted version or mature example, separate **relation** from **style** before generating options. Record:
- hierarchy and dominant alignment;
- density and whitespace rhythm;
- object/media scale and crop behavior;
- section/sequence order;
- interaction/state relationship;
- repeated visual/spatial grammar;
- motion ownership where temporal behavior matters.

Then translate those relationships into the project's own authority, content and constraints.

Use:
`REFERENCE → STRUCTURAL RELATIONS → PROJECT CONSEQUENCES → OPTIONS → ACTUAL ARTIFACT DELTA REVIEW`

Do not reproduce third-party identity or irrelevant surface decoration unless the task is explicitly a governed reconstruction exercise.

## Evidence-density gate

Do not equate more modules with more design depth.

`LOW EVIDENCE DENSITY → FEWER STRONGER OBJECTS`

Missing proof remains missing proof even when a composition would benefit from more density.

## Rules

1. Start from a real project Decision Question or genuine capability gap.
2. Existing Skill First and Current Knowledge First where applicable.
3. Keep evidence, inference, assumption and decision separate.
4. Frame actor/context/outcome/guardrail before committing to form.
5. Expose the key unknown that can still change the decision.
6. Every substantial design round creates an editable or native inspectable artifact.
7. Alternatives must be materially different when the decision genuinely has alternatives; cosmetic variants do not count.
8. Actual Readback is mandatory after construction and after repair.
9. Design Quality is independent from evidence correctness and technical validity.
10. Existing Mature Design First: do not regress a stronger Current artifact merely because a new process is cleaner.
11. Use the minimum prototype fidelity needed to answer the current question.
12. When dimensions/engineering/human/field truth are unresolved, preserve uncertainty and route validation.
13. A design artifact cannot certify browser behavior, CAD roundtrip, engineering approval, field truth, human safety or manufacturing readiness.
14. A visual reference is not a template license; extract relevant relations unless strict reconstruction is explicitly requested.
15. Do not fill missing evidence with decoration or synthetic content.
16. For physical/product/spatial form, do not let decorative cues silently imply function, ventilation, grip, fastening, movement, structure, access or serviceability.
17. Presentation polish cannot override a weak design relation; route back to DESIGN.
18. Validation findings cannot silently overwrite the design master; use controlled return/disposition.
19. Preserve rejected alternatives and reopen triggers for consequential decisions.
20. Use a Variable Budget so unrelated simultaneous changes do not masquerade as causal evidence.
21. Treat options in the same concept family as variants, not independent concept-space coverage.
22. Match prototype medium to the unknown being tested; wrong-medium fidelity is not proof.
23. Preserve the Design Continuity Contract across presentation handoff.
24. Propagate material changes through dependent objects and retest affected views/states before closure.
25. `PROCESS PASS ≠ DESIGN PASS ≠ VALIDATION PASS ≠ PRESENTATION PASS ≠ FIELD PASS`.

## Semantic-dimension-to-form gate

When one project claim contains multiple relation types:

1. Split `DISCRETE / CONTINUOUS / DIRECTIONAL / RELATIONAL / HIERARCHICAL / TEMPORAL`.
2. Assign different form roles when dimensions differ.
3. Generate at least two mappings if the relationship is not locked.
4. Remove labels, numbering, arrows and decorative color.
5. Reject literal counting decoration when it reproduces only the number, not the relation.
6. If structural/ergonomic/safety/manufacturing geometry is introduced, hand off validation.

Promotion test:

`REMOVE LABELS + DECORATIVE COLOR → DOES THE FORM STILL PRESERVE THE RELATION TYPE?`

## Execution boundary

This skill is an installed OLEANDER execution owner for DESIGN reasoning and design-state progression. Installation does not grant artifact KEEP, specialist technical authority, field truth or release authority.

It cannot:
- self-KEEP;
- replace specialist technical validation;
- grant final presentation KEEP;
- claim field/manufacturing/engineering/human-test truth;
- convert project or training evidence into Current Knowledge without the Knowledge lifecycle.

Activation closure: project-use and cross-context Practice evidence exist; maintained Golden Cases remain in `evals/golden/skills.jsonl`; AIG-01/AIG-02/AIG-03 regression checks passed on PR #449; the user explicitly authorized continuation to default activation on 2026-08-29. Independent artifact design verdicts remain governed separately by `OLEANDER_INDEPENDENT_DESIGN_VERDICT_POLICY_v1.0.md`.