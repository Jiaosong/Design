# Existing Project Repair Extension

Status: OWNER-LOCAL EXTENSION / CANDIDATE FOR PROJECT-USAGE READBACK
Owner: `oleander-design-process`
Lifecycle: DESIGN primary; PRESENTATION / VALIDATION / GOVERNANCE through existing handoff contracts
Scope: repair and optimization of an already-active OLEANDER project/object whose Current authority, mature baseline, source assets, production frontier or review findings already exist.
Non-goal: this is not a second project process, not a new Core Skill, not a replacement for the Work Coordination Contract, and not a reason to interrupt the independent KNOWLEDGE frontier.

## 1. Why this extension exists

The base Design Process is intentionally broad: it can frame a new design question, diverge, construct, attack, repair and hand off. Existing projects need an additional constraint because the main risk is often not lack of ideas but accidental regression, duplicated Current objects, source substitution, owner collision, or repeated process work that does not improve the actual artifact.

Use this extension when the task is equivalent to:

- optimize / fix / repair / continue an existing project;
- improve a Current web, board, model, drawing, package, interaction or production artifact;
- consume newly matured OLEANDER knowledge/skills without restarting the project;
- close an existing review blocker or HOLD;
- recover a project whose process is more mature than its final output.

Do not use it merely because a project exists. If the actual design question has materially changed, return to the base Design Process and re-frame the object honestly.

## 2. Parallel-lane rule: project repair must not consume the knowledge frontier

OLEANDER may continue knowledge development and project repair in parallel.

Default separation:

`KNOWLEDGE LANE = discover / structure / deepen / distill / route reusable knowledge`

`PROJECT REPAIR LANE = consume Current authority + existing Skills → repair the active Work Object → readback → handoff`

Project repair may:
- read Current Knowledge and mature Evidence;
- use installed/Candidate specialist Skills according to their real routing state;
- create project-specific evidence and a later Knowledge Return package.

Project repair must not:
- change the KNOWLEDGE runner schedule or cadence;
- replace its selected Current object or Depth Gap;
- force a project patch into Current Knowledge before the normal knowledge lifecycle;
- duplicate an existing Method/Skill simply to make project execution faster;
- treat an unfinished project result as a new Current Rule.

If a repair exposes a reusable method gap, complete the project repair first where possible and return only:

`CONTEXT → FAILURE → ROOT CAUSE → REPAIR → RETEST → TRANSFER RULE → BOUNDARY → EVIDENCE`

KNOWLEDGE may absorb that later without blocking project production.

## 3. Repair preflight

Before editing, resolve the same Work Object already governed by the Work Coordination Contract:

`PROJECT_ID → OBJECT_ID → CURRENT_OWNER → CURRENT AUTHORITY → CURRENT NATIVE MASTER → CURRENT PR/WRITE FRONTIER → BEST MATURE BASELINE → OPEN REVIEW GAP → LOCKED VARIABLES → SOURCE/ASSET AUTHORITY → REQUIRED NATIVE OUTPUT → REQUIRED READBACK`

Mandatory checks:

1. **Same-object check** — do not invent a new Object ID for the repair.
2. **Best-existing check** — identify the strongest current/mature artifact before changing it.
3. **Frontier check** — continue the current production branch/PR/frontier unless Governance explicitly changes it.
4. **Authority check** — do not bind Legacy, weak thumbnail, context image, render or model substitute as authority when stronger source identity exists.
5. **Variable check** — identify exactly what may change and what must remain locked.
6. **Owner check** — only the current owner edits the production object; other owners receive explicit handoff.
7. **Readback check** — decide how the actual result will be inspected before beginning the edit.

If any of 1–4 is unresolved and the repair would overwrite project truth, HOLD the write and route the exact blocker.

## 4. Repair triage: classify before acting

Do not send every defect back to DESIGN.

Classify the primary failure:

| Failure class | Typical symptom | Primary owner/action |
| --- | --- | --- |
| `AUTHORITY / IDENTITY` | dual Current, wrong source, wrong object, stale frontier | GOVERNANCE resolves before production continues |
| `SOURCE / ASSET INTEGRITY` | requested image/model/file exists but exact bytes/crop/child identity not bound | current production owner binds only authority-ready source; unresolved source remains HOLD |
| `DESIGN LOGIC` | route, hierarchy, topology, function, relation, object definition is wrong | DESIGN reopens the minimum correct layer |
| `PRESENTATION` | correct design reads weakly because of crop, grid, type, pacing, image role, hierarchy | PRESENTATION repairs without rewriting locked design truth |
| `RUNTIME / TECHNICAL` | browser state, interaction, export, roundtrip, units, performance, fallback or file semantics fail | VALIDATION tests and returns PASS / REVISE / HOLD |
| `KNOWLEDGE GAP` | repair depends on genuinely missing reusable evidence/method | record bounded evidence request; do not silently repurpose the independent Knowledge frontier |

When several classes coexist, fix the earliest authority-breaking class first. Do not beautify a source-integrity failure or run validation on a knowingly wrong master.

## 5. Existing Mature Design First

Repair is comparative, not absolute.

Use:

`BEST EXISTING → TARGETED DELTA → ACTUAL READBACK → REGRESSION CHECK → KEEP / REVISE / ROLLBACK`

A newer artifact loses if it is weaker than the best existing artifact in the dimension that matters, even when:
- its file structure is cleaner;
- it uses a newer Skill;
- it has more components;
- CI passes;
- it is more systematic;
- it contains more documentation.

Before replacing a mature artifact, record:

`WHAT IS STRONGER NOW → WHAT IS PRESERVED → WHAT IS INTENTIONALLY CHANGED → WHAT COULD REGRESS`

If the repair cannot state a material benefit, prefer no change.

## 6. Minimum Repair Delta

For an existing project, default to the smallest root-cause change that can close the current gap.

`GAP → ROOT CAUSE → MINIMUM OWNER → MINIMUM VARIABLE SET → EDITABLE/NATIVE DELTA → READBACK`

Examples:
- missing exact project images → bind the three resolved source derivatives; do not redesign the page around placeholders;
- weak hierarchy with correct content → change crop/scale/type/pacing; do not rewrite project logic;
- Return blocked by animation → fix state/interruptibility; do not add a second navigation model;
- one model module missing → restore its asset binding; do not promote the model to project Hero if the project authority says otherwise;
- wrong route geometry → return to authoritative geometry; do not stretch the route to satisfy a presentation grid.

A large redesign is permitted only when the failure class is actually Architecture/Topology/Design Logic and the current artifact cannot be repaired locally.

## 7. Artifact Delta Gate

A project Work Object may advance owner/state only when a **material production delta** exists.

Minimum production evidence:

1. an actual editable/native artifact or authoritative binding changed;
2. the changed artifact was reopened/rendered/run in the relevant medium;
3. the intended repair is visible/inspectable in that readback;
4. locked relations/source identity/truth state were checked for regression;
5. residual HOLD is explicit;
6. the receiver can identify the same `PROJECT_ID / OBJECT_ID` and current native master.

The following are not sufficient on their own:

`document created / manifest updated / receipt written / hash recorded / commit exists / PR opened / CI green / file exists / screenshot exists`

Use:

`ARTIFACT EXISTENCE ≠ MATERIAL DELTA ≠ DESIGN QUALITY ≠ VALIDATION PASS`

If there is no real artifact delta, remain `HOLD / COOLDOWN / SAME OWNER` rather than manufacturing progress in governance text.

## 8. Repair-loop handoff

The normal loop is:

`CURRENT OWNER → REPAIR → READBACK → HANDOFF_READY → NEXT OWNER → TEST/CRIT → PASS or RETURN SAME OBJECT`

Typical project-production route:

`DESIGN (only if design logic is open) → PRESENTATION → VALIDATION → return to PRESENTATION or DESIGN by failure class → VALIDATION RETEST → project Current / release handoff`

Rules:
- PRESENTATION may not silently fix design logic by changing locked relations.
- VALIDATION may not silently edit the design/presentation master.
- DESIGN should not reclaim an object for a purely visual or technical defect.
- GOVERNANCE changes owner/frontier only after readback of the real state.
- A return uses the same Object ID; it is not a new project iteration identity.

Compact repair handoff:

`PROJECT_ID / OBJECT_ID → FROM / TO → CURRENT MASTER → FAILURE CLASS → WHAT CHANGED → LOCKED VARIABLES → READBACK EVIDENCE → WHAT MUST BE TESTED NEXT → RESIDUAL HOLD → CURRENT FRONTIER`

## 9. Presentation-to-validation closure for Web / interactive work

When the active object is a web or interaction artifact, PRESENTATION first closes source/visual integrity that it owns. VALIDATION then proves the runtime.

PRESENTATION should deliver, where applicable:
- exact-authority asset binding;
- source/derivative identity;
- approved copy/state hierarchy;
- desktop/mobile visual source-level readback;
- motion/no-motion design intent;
- unresolved asset HOLDs.

VALIDATION should then test the same object, where applicable:
- real desktop browser;
- real mobile viewport;
- keyboard/focus/Return;
- state equivalence including degraded/closed/unknown states;
- Reduced Motion;
- no-enhancement / no-WebGL fallback when enhancement exists;
- asset 404/load failure behavior;
- layout stability / overflow;
- console/runtime errors;
- performance-risk states;
- renderer/context/dispose/mobile downgrade for shader/WebGL paths.

`STATIC OR SOURCE READBACK ≠ BROWSER PASS`.

## 10. Source and asset integrity rule

For existing projects, source recovery is part of repair quality.

Use only assets whose role is established enough for the current claim:

`SOURCE IDENTITY → EXACT FILE/BYTES → DERIVATIVE/CROP IDENTITY → TARGET ROLE → BINDING → READBACK`

Unresolved source/crop/child identity remains `HOLD`. Do not fill a source gap by:
- AI generation;
- redraw presented as original source;
- a model substituted for a real landscape/product/image authority;
- a low-resolution thumbnail promoted to Hero;
- a visually similar file whose identity is unknown.

A constrained placeholder may remain only when the project explicitly permits it and it cannot be mistaken for final/authoritative content.

## 11. No-loss and stale-derivative check

Repair must obey NO COMPRESSION / NO LOSS.

After a material upstream change, run:

`CHANGE → DEPENDENT ARTIFACTS → STALE DERIVATIVES → REQUIRED REGENERATION / RETEST → STATUS`

Do not delete older evidence just because a repair is stronger. Preserve provenance and supersession, while keeping one discoverable Current production state.

## 12. Closure criteria

The repair round is closed only when:

- same Work Object identity is preserved;
- Current authority/frontier is known;
- real artifact delta exists;
- root-cause layer was changed rather than cosmetically masked;
- actual readback was performed after the last change;
- no stronger mature artifact was silently regressed;
- required specialist handoff/retest is complete or explicitly HOLD;
- dependent derivatives are updated or explicitly stale/HOLD;
- project Current/queue state reflects the real owner and next action;
- reusable learning, if any, is returned as bounded evidence without interrupting or self-promoting into Current Knowledge.

Compact closure record:

`OBJECT → GAP → FAILURE CLASS → ROOT CAUSE → ACTUAL REPAIR → READBACK → REGRESSION CHECK → VERDICT → RESIDUAL HOLD → NEXT OWNER/ACTION → KNOWLEDGE RETURN IF MATERIAL`

## 13. Golden repair scenario

Scenario: an existing project website has a mature structure and a live production PR. Three requested real assets have now been resolved to exact authority-ready derivatives; several other requested assets still lack exact source/crop/child identity. The page also needs browser validation.

Correct process:

1. preserve the current `PROJECT_ID / OBJECT_ID / PR frontier`;
2. current PRESENTATION owner binds only the three authority-ready derivatives;
3. do not redesign the mature page merely to hide unresolved asset gaps;
4. keep unresolved assets HOLD and do not substitute AI/redraw/model/weak thumbnail;
5. perform final source-level desktop/mobile visual readback;
6. hand the same object to VALIDATION;
7. VALIDATION performs real browser/state/fallback checks;
8. visual failures return PRESENTATION; design-logic failures return DESIGN; runtime-only failures remain VALIDATION until a repair handoff is required;
9. only real artifact delta + readback changes queue/owner state;
10. reusable repair knowledge is returned later to KNOWLEDGE without pausing or redirecting its independent frontier.

Blockers:
- new Object ID for the same repair;
- parallel production PR opened without Governance authority;
- unresolved asset substituted by generated or identity-unknown content;
- CI/receipt/manifest used as the only evidence of progress;
- Validation starts before the presentation/source master is stable enough to test;
- Knowledge runner is repurposed or slowed to service the repair;
- newer but weaker artifact replaces the best mature result.

Pass condition:

The existing project becomes materially stronger while preserving authority, object identity, mature design value, independent knowledge progress and a verifiable owner-by-owner repair trail.
