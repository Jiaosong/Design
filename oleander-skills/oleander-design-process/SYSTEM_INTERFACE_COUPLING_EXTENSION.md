# System Interface / Coupling Extension

Status: `CANDIDATE EXTENSION / SUPPORT ONLY / NO CURRENT L5 PROMOTION`

Owner: `oleander-design-process`

Use when a design succeeds or fails through relations between components, subsystems, services, teams, carriers or states rather than through one object in isolation. This extension exists to prevent local component PASS from being mistaken for integrated-system PASS.

It does not replace Current Trade Study, FMEA, Design Goal Contract, technical drawing, CAD, runtime validation or project governance. It exposes the interface and coupling structure those owners must consume.

## Core contract

`SYSTEM PURPOSE / BOUNDARY → FUNCTIONS / COMPONENTS → INTERFACES → EXCHANGED THINGS + UNITS / TIMING / OWNERSHIP → COUPLING / DEPENDENCY → INTEGRATION ORDER → FAILURE-SPLIT → VERIFICATION OBJECT → DESIGN CONSEQUENCE / HANDOFF`

## Interface ledger

For every material interface, record only fields relevant to the task, such as:

- upstream/downstream or peer object IDs;
- physical / spatial / information / electrical / service / human / organizational interface class;
- what crosses the boundary: geometry, load, material, signal, data, state, person, service, permission, heat, fluid, content or responsibility;
- directionality and allowed states;
- units/scale/coordinate frame/protocol/format where relevant;
- timing/order/latency/delay when state or sequence matters;
- ownership and Source Authority on each side;
- assumptions and known losses;
- verification method and evidence location.

An interface record describes the boundary contract; it must not silently redefine the internal design of either subsystem.

## Coupling rules

1. **Component PASS ≠ integration PASS.** A set of individually valid objects can still fail through mismatched units, timing, geometry, state, ownership or assumptions.
2. **Boundary before detail.** When unexpected system behavior appears, inspect interfaces and coupling before redesigning every component.
3. **Trace both directions.** A requirement/claim should trace upward to the system need and downward to the object/interface/evidence that satisfies it when such traceability is material.
4. **Separate interface failure hypotheses.** Distinguish at least: interface mismatch, component out-of-spec, wrong environmental assumption, configuration drift, requirement ambiguity and test/procedure defect.
5. **Expose iteration.** If tasks/components are mutually dependent, do not hide the coupling inside a fake linear schedule. Record the coupled block and its required iteration/verification.
6. **Units/timing/coordinates are design information.** They are not implementation trivia when crossing an interface can change behavior.
7. **Emergent behavior gets a system-level test.** Do not infer whole-system behavior only by summing subsystem test results.

## Optional structural carriers

Use only when they help answer the decision:

- interface/contract table;
- N²-style relation matrix;
- dependency graph;
- Design Structure Matrix or equivalent coupling matrix;
- state/interface sequence;
- system-boundary diagram;
- requirement → interface/object → verification trace.

The diagram/matrix is not itself insight. It must identify the consequential coupling, failure mode, integration order or design change.

## Required output

- `system_purpose_boundary`;
- `function_component_map`;
- `material_interface_ledger`;
- `coupling_dependency_map`;
- `integration_or_iteration_order`;
- `rival_failure_explanations`;
- `verification_objects`;
- `design_consequence`;
- `handoff_to_actual_technical_owner`;
- `residual_HOLD`.

## Failure attacks

Reject or revise when:

- every subsystem passes but no interface has been tested;
- a connector/file/API/route exists and is called an interface PASS without units, state, timing or ownership where relevant;
- a dependency diagram is produced with no integration consequence;
- a linear plan hides a mutually coupled block;
- a local optimization damages system-level goal/return/safety/service behavior;
- interface mismatch is "fixed" by arbitrary conversion/offset without source authority;
- SysML/DSM/N²/software tooling is adopted as the method rather than as a carrier;
- one aerospace lifecycle, V-model, review phase or software stack is installed as universal OLEANDER process.

## Transfer boundary

External professional source study:
- `K-Dense-AI/scientific-agents/systems-engineer/AGENTS.md` — MIT repository.
- `d-wwei/systems-thinking/SKILL.md` was reviewed only as high-level comparison; no repository license was found in the inspected tree, so no source prose/framework package is transferred from it.

Accepted from the MIT systems-engineering source: explicit system boundary, bidirectional traceability, interface contracts, coupling/integration sequencing, separation of verification and validation, and rival explanations for integration failure.

Rejected as universal: ISO/IEC/IEEE 15288 lifecycle adoption, V-model as mandatory project structure, DOORS/Jama/Cameo tooling, PDR/CDR/ORR review sequence, fixed weight-perturbation percentages, generic risk matrices and domain-specific safety standards detached from the actual project.

## Candidate claim

`LOCAL OBJECT CORRECTNESS CANNOT ESTABLISH SYSTEM CORRECTNESS WHEN MATERIAL BEHAVIOR CROSSES AN UNVERIFIED INTERFACE.`

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / EXTERNAL-SOURCE-DIGESTED / PRACTICE NOT YET RUN / NO PROJECT USAGE / NO PROMOTION`.