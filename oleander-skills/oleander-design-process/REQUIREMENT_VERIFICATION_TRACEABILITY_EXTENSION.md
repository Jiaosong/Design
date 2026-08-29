# Requirement → Verification Traceability Extension

Status: `CANDIDATE EXTENSION / SUPPORT ONLY / NO CURRENT L5 PROMOTION`

Owner: `oleander-design-process`

Use when a project contains material obligations that must survive design iteration and be proven individually: performance requirements, safety constraints, accessibility obligations, interaction states, dimensions, service conditions, asset/content obligations or contractual acceptance criteria.

This extension complements Current `Design Goal Contract` and the existing requirement/evidence coverage map. Goals define desired outcomes; this extension turns material obligations into traceable, testable objects and controls what happens when they change.

## Core contract

`STAKEHOLDER / SOURCE → NEED / GOAL → ATOMIC REQUIREMENT OR CONSTRAINT → RATIONALE + PRIORITY → ACCEPTANCE / FAILURE CONDITION → DESIGN OBJECT / INTERFACE → VERIFICATION METHOD → EVIDENCE ID + CONFIGURATION → STATUS → CHANGE IMPACT → REVERIFY / HOLD`

## Requirement rules

1. **Requirement ≠ aspiration.** A material requirement must be precise enough that evidence can support PASS/FAIL/BOUNDED/HOLD. If it cannot be tested, keep it as a goal/hypothesis rather than disguising it as a requirement.
2. **One obligation per traceable object where material.** Avoid compound statements whose parts can pass/fail independently.
3. **Source and rationale stay attached.** A requirement without a parent need/source risks becoming gold-plating; a parent need without downstream proof risks becoming decoration.
4. **Acceptance is defined before proof is interpreted.** Do not move the threshold after seeing the result unless the change is explicitly governed and impact-assessed.
5. **Verification method follows the claim.** Inspection, analysis, demonstration, test, browser/runtime proof, physical measurement or human task evidence are distinct proof classes.
6. **Proof is configuration-bound.** Evidence must identify the relevant model/build/revision/runtime/test article when that configuration can change the result.
7. **Derived implementation detail is not automatically a requirement.** Keep WHAT/WHY separate from a chosen HOW unless the implementation constraint is itself authoritative.
8. **Change propagates both directions.** A changed requirement reopens affected design/evidence; a design/interface change must identify which requirements/evidence become stale.
9. **Waiver/exception is not deletion.** Record scope, authority, rationale and residual consequence.

## Required output

- `source_need_goal`;
- `atomic_requirement_or_constraint`;
- `rationale_priority`;
- `acceptance_failure_condition`;
- `allocated_design_object_or_interface`;
- `verification_method_and_proof_class`;
- `evidence_id_configuration_revision`;
- `status_and_open_unknowns`;
- `change_impact_links`;
- `reverify_or_waiver_state`.

## Failure attacks

Reject or revise when:

- a vague goal such as “easy / robust / premium / safe” is marked verified without an operational definition;
- several independent obligations are bundled into one PASS;
- a requirement has no source/rationale and survives only because a team member added it;
- evidence exists but is for the wrong revision/configuration;
- a screenshot proves visual appearance but is used to claim runtime behavior, accessibility or physical performance;
- an implementation choice becomes permanent authority without source;
- acceptance criteria are adjusted after a failed test without change control;
- a requirement changes but dependent drawings/models/tests remain marked Current/PASS;
- one domain's `shall` syntax, V-model phase or requirements tool becomes mandatory OLEANDER process.

## Transfer boundary

External professional source study:
- `K-Dense-AI/scientific-agents/scientific-agents/systems-engineer/AGENTS.md` — MIT repository; requirements/traceability/V&V mechanisms only.
- Current OLEANDER NASA stakeholder-goal source and Design Goal Contract remain internal authority for outcome framing.

Accepted: bidirectional traceability, atomic/verifiable obligations, source/rationale linkage, requirement-to-proof mapping, verification vs validation separation, configuration-bound evidence, change-impact reopening.

Rejected as universal OLEANDER truth: mandatory `shall` grammar, one V-model lifecycle, DOORS/Jama/Polarion/Cameo tooling, SRR/PDR/CDR review sequence, fixed T/A/I/D labels where another proof taxonomy is more appropriate, or aerospace standards detached from project authority.

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / EXTERNAL-SOURCE-DIGESTED / PRACTICE NOT YET RUN / NO PROJECT USAGE / NO PROMOTION`.