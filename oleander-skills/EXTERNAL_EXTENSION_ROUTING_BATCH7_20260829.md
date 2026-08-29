# OLEANDER External-Digestion Routing — Batch 7 — 2026-08-29

Status: `CANDIDATE ROUTING ADDENDUM / EXISTING-FIRST / NO CORE-SKILL PROMOTION`

Purpose: route the first `GAP-ENG-01` digestion from `NEXT_CAPABILITY_GAP_SOURCE_MAP_20260829.md` back into existing owners without creating Manufacturing Engineering, GD&T, Metrology or Product Release as new Core Skills.

## Current-first result

The broad gap:

`DFM / DFA / GD&T-GPS / TOLERANCE / METROLOGY / PRODUCT RELEASE`

was **not** accepted as one new Skill. Current owners already cover large parts:

- Design Process: physical-product reasoning, serviceability, material/reliability/system reasoning;
- 3D Pipeline: native CAD, units, datums/joints, assembly geometry, STEP/open-native exchange;
- Research: measurement model, calibration, traceability and uncertainty;
- Technical Drawing: PR #172 Candidate drawing-carrier lineage;
- Delivery QC: package/file/release-artifact integrity;
- Governance: version/current/lifecycle integrity.

The material residual is split into two Candidate extensions.

## Routing table

| Trigger / Required Native Output | Existing owner | Candidate extension | External study provenance |
|---|---|---|---|
| A physical design must be checked against a named manufacturing/assembly process, workholding/tooling, measurement-system fitness and repeatable process evidence before design/tooling/release closure | `oleander-design-process` + 3D / Research / Delivery / VALIDATION as needed | `oleander-design-process/DFM_DFA_PROCESS_CAPABILITY_EXTENSION.md` | `wonsukchoi/domain-experts/roles/manufacturing-engineer/SKILL.md` (MIT) + existing OLEANDER assembly/serviceability rules |
| Functional fit/location/orientation/profile/runout or tolerance accumulation must survive CAD→PMI/drawing→inspection/metrology handoff with datum, control, method, uncertainty and revision semantics intact | `oleander-3d-pipeline` + Research + Technical Drawing PR #172 + VALIDATION | `oleander-3d-pipeline/FUNCTIONAL_TOLERANCE_GDNT_METROLOGY_HANDOFF_EXTENSION.md` | `K-Dense-AI/scientific-agents/precision-engineering-specialist/AGENTS.md` (MIT) |

## Required routing order

When both apply, prefer:

`FUNCTION / FAILURE CONSEQUENCE`
`→ PRODUCT / ASSEMBLY RELATION`
`→ NATIVE CAD + FUNCTIONAL DATUM / INTERFACE`
`→ FUNCTIONAL TOLERANCE / VARIATION CONTRACT`
`→ CANDIDATE MANUFACTURING PROCESS`
`→ DRAWING / PMI CARRIER`
`→ MEASUREMENT PLAN + DATUM SIMULATION`
`→ MEASUREMENT UNCERTAINTY / DECISION RULE`
`→ PROCESS / INSPECTION EVIDENCE`
`→ DESIGN OR PROCESS RETURN`
`→ RELEASE PACKAGE / EXTERNAL APPROVAL HOLD`

Do not collapse this into one owner.

## Ownership boundaries

### Design Process
Owns:
- when manufacturability changes the design;
- named candidate process and critical feature/process questions;
- DFM/DFA consequence and design/process reopen;
- containment vs corrective-action distinction.

Does not own:
- signed manufacturing release;
- supplier capability certification;
- GD&T standard interpretation by itself;
- metrology accreditation.

### 3D Pipeline
Owns:
- source geometry, units, datums/interfaces and assembly relation;
- tolerance/PMI semantic handoff from functional geometry;
- exchange/readback identity when supported.

Does not own:
- drawing-carrier Current promotion;
- process capability;
- laboratory measurement authority;
- engineering signoff.

### Research / Measurement Uncertainty
Owns:
- measurand/method/instrument/calibration/traceability/uncertainty meaning;
- decision-impact boundary.

Does not own:
- design datum strategy;
- process capability or supplier release.

### Technical Drawing PR #172
Remains the only Candidate Technical Drawing implementation lineage.

`BATCH7 EXTENSION ≠ PARALLEL TECHNICAL-DRAWING SKILL`.

This batch intentionally creates no `oleander-skills/oleander-technical-drawing/` directory on main.

## NO-DELTA / rejected new identities

No new Core Skill for:
- Manufacturing Engineering;
- GD&T;
- Metrology;
- Tolerance Stack;
- DFA;
- PPAP / APQP / FAI;
- CMM programming.

These are routed as bounded professional concerns through existing owners until real project evidence proves an unresolved ownership gap.

## Universal-rule firewall

The following remain context/authority dependent and must not become global defaults:
- Cpk/Ppk targets;
- GR&R thresholds;
- RSS vs worst-case selection;
- sample/subgroup size;
- datum schemes or 3-2-1 fixturing recipes;
- MMC/LMC/virtual-condition examples;
- guard-band percentages;
- CMM point density, stylus, filter or temperature recipes;
- ASME Y14.5 / ISO GPS / AIAG / AS9102 / PPAP edition or workflow;
- named CAD/CMM/quality software;
- one “DFM checklist” detached from the actual process and function.

## Claim boundaries

`CAD VALID ≠ MANUFACTURABLE`

`DRAWING COMPLETE ≠ PROCESS CAPABLE`

`MEASURED ≠ TRACEABLE / DECISION-CAPABLE`

`INSPECTION PASS ≠ PROCESS CONTROL`

`PROCESS CAPABILITY ≠ ENGINEERING / CUSTOMER RELEASE`

`CI PASS ≠ MANUFACTURING / METROLOGY PASS`

## Maturity

Both entries remain:

`DOCUMENTED CANDIDATE EXTENSION / SOURCE DIGESTED / NO PRACTICE / NO CROSS-CONTEXT / NO PROJECT USAGE / NO PROMOTION`.

Next maturity step is a controlled practice with actual geometry, datum/tolerance choices, simulated or bounded measurement evidence and explicit failures—not another generic source-search batch for the same capability.