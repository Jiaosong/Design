# DFM / DFA / Process Capability Extension

Status: `CANDIDATE EXTENSION / SUPPORT ONLY / NO CURRENT L5 PROMOTION`

Owner: `oleander-design-process`

Use when a physical product, mechanism, fixture, assembly, spatial element or fabricated component must move from design intent toward a repeatable manufacturing process. This extension closes the gap between `valid geometry` and `manufacturing evidence` without creating a manufacturing-approval authority inside OLEANDER.

It does **not** replace:
- `oleander-3d-pipeline/PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION.md` for native geometry, datums, joints and deterministic CAD checks;
- Current FMEA for failure-mode analysis;
- `oleander-research/MEASUREMENT_UNCERTAINTY_EXTENSION.md` for measurement meaning and uncertainty;
- Technical Drawing PR #172 for drawing-carrier execution;
- supplier / manufacturing / quality authority for production approval.

## Core contract

`FUNCTION / ASSEMBLY REQUIREMENT → CANDIDATE PROCESS + MATERIAL / SECTION → FUNCTIONAL FEATURE + DATUM / INTERFACE → PROCESS-FEATURE CAPABILITY QUESTION → WORKHOLDING / TOOLING / SEQUENCE → MEASUREMENT-SYSTEM FITNESS → PROCESS EVIDENCE → DFM / DFA CONSEQUENCE → DESIGN OR PROCESS REVISION → RETEST / FIRST-ARTICLE OR BOUNDED RELEASE EVIDENCE → CLAIM CEILING`

## Core separations

`CAD VALID ≠ MANUFACTURABLE`

`DRAWING TOLERANCE ≠ PROCESS CAPABILITY`

`INSPECTION ≠ PROCESS CONTROL`

`100% SORT ≠ ROOT-CAUSE CORRECTION`

`Cpk / Ppk NUMBER ≠ CAPABLE PROCESS WITHOUT STABILITY + MEASUREMENT FITNESS + CONTEXT`

`ASSEMBLES ONCE ≠ DFA / REPEATABLE ASSEMBLY`

## DFM / DFA reasoning rules

1. **Start from function and assembly, not the preferred machine.** Identify what the feature must locate, seal, rotate, slide, clamp, align, protect, transfer or service before choosing manufacturing concessions.
2. **Name the candidate process.** Machining, forming, molding, casting, additive, sheet fabrication, bonding, fastening, printing, coating and hybrid routes impose different feature and tolerance realities. Generic “DFM-friendly” advice without a process is not material evidence.
3. **Separate geometry possibility from repeatable capability.** A process may physically make one good part yet fail to hold the feature distribution, surface, alignment or assembly result repeatedly.
4. **Tie tolerance pressure to a functional characteristic.** If a tolerance or finish cannot be linked to fit, function, safety, appearance, downstream process or service need, treat tightening as an unresolved cost/authority question rather than a default quality improvement.
5. **Workholding must preserve functional reference logic.** Clamping convenience must not silently replace the datum/interface relations used by the product in assembly or service.
6. **Measurement-system fitness precedes process-capability interpretation.** A capability result derived from an unsuitable, unstable or poorly matched measurement method cannot diagnose the process cleanly.
7. **Capability is contextual.** Population, machine/tool/fixture state, material lot, program/process revision, sampling structure and environmental conditions remain attached to the result.
8. **Containment is not correction.** Sorting, reinspection or operator vigilance may protect a short-term shipment but do not prove the underlying manufacturing process became capable.
9. **DFA includes error-proofed assembly relations.** Part count alone is not the goal. Access, orientation, locating, fastening, sequence, poka-yoke/error direction, rework, service and disassembly can materially change the design.
10. **Manufacturing feedback returns upstream.** If a required feature cannot be achieved repeatably or economically under the chosen route, the process or design must reopen before tooling/release is treated as fixed.

## Required output

- `function_assembly_requirement`;
- `candidate_process_material_section`;
- `critical_feature_interface_and_datum_relation`;
- `process_feature_capability_question`;
- `tooling_workholding_sequence_state`;
- `measurement_system_fitness_state`;
- `process_evidence_and_population`;
- `dfm_dfa_findings`;
- `design_or_process_revision`;
- `retest_first_article_or_release_evidence`;
- `supplier_quality_manufacturing_holds`;
- `claim_ceiling`.

## Failure attacks

Reject or revise when:

- a STEP/DXF/CAD export is called manufacturable because it opens correctly;
- a process is not named but fixed wall/radius/tolerance rules are imposed as universal DFM truth;
- a tolerance is tightened because “precision is better” with no functional consequence;
- a fixture locates from convenient surfaces while the product function depends on another datum/interface relation;
- process capability is claimed from a single first article or a few cherry-picked conforming parts;
- a Cpk/Ppk value is reported without confirming the process/data state and measurement fitness required by the decision;
- a weak measurement system is treated as proof of process variation;
- 100% inspection or sorting is presented as permanent corrective action;
- a process/tolerance mismatch is discovered after tooling but the drawing is left unchanged because “production will learn it”;
- part-count reduction destroys serviceability, assembly access, error prevention or functional robustness;
- PPAP/APQP/FAI/control-plan vocabulary is used as a release certificate without the actual required authority and evidence.

## Transfer boundary

External source study:
- `wonsukchoi/domain-experts/roles/manufacturing-engineer/SKILL.md` — repository MIT.

Accepted material delta:
- manufacturing as translation from released design intent to a repeatable process;
- datum/workholding alignment as a functional contract;
- process/tolerance mismatch must return to design before tooling is treated as closed;
- measurement-system capability must precede process-capability interpretation;
- capability evidence must remain attached to process/configuration/population;
- containment vs corrective-action separation;
- DFA as repeatable assembly/error-proofing/service reasoning, not only part-count minimization.

Rejected as universal OLEANDER truth:
- fixed Cpk/Ppk release thresholds;
- fixed GR&R percentage gates;
- automatic RSS over worst-case or vice versa;
- fixed subgroup/sample sizes;
- one PFMEA/RPN/action-priority rule;
- one PPAP/APQP/NPI release sequence;
- fixed OEE targets;
- shop-specific locator clearance, process capability or fixture recipes;
- ASME/AIAG/OEM standards detached from Current project/jurisdiction/customer authority.

## Co-routing boundary

- Native CAD, datum/joint/source geometry → `oleander-3d-pipeline`.
- Functional tolerance / GD&T-GPS / feature-level inspection handoff → `oleander-3d-pipeline/FUNCTIONAL_TOLERANCE_GDNT_METROLOGY_HANDOFF_EXTENSION.md`.
- Measurement model, calibration, traceability, uncertainty → `oleander-research/MEASUREMENT_UNCERTAINTY_EXTENSION.md`.
- Drawing carrier / callout execution → Technical Drawing PR #172 Candidate lineage; do not create a parallel main Technical Drawing Skill.
- Release package/file integrity → `oleander-delivery-qc`.
- Production acceptance, signed engineering, supplier approval and legal/compliance authority remain external professional/project owners.

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / EXTERNAL-SOURCE-DIGESTED / PRACTICE NOT YET RUN / NO PROJECT USAGE / NO PROMOTION`.