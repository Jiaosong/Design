# OLEANDER Next Capability Gap / Source Map — 2026-08-29

Status: `DISCOVERY / SUPPORT EVIDENCE / NO CORE-SKILL INSTALL / NO PROJECT USAGE / NO PROMOTION`

Purpose: extend the Current coverage-gap scan beyond Batch-4 visual/content candidates. This file is a controlled discovery/evidence map only. It does not install an external Skill, create a new Core Skill, change Current L5 authority, or claim technical/professional validation.

## Existing-first baseline

Current OLEANDER has eleven core reusable identities. The strongest recent coverage is visual design, Web/UI, motion, image art direction, story/board, research, data visualization, CAD/3D source/derivative discipline, delivery QC, design reasoning and emerging technical drawing. The residual gaps below are mostly engineering translation / physical evidence / information-model / field-evidence gaps, not reasons to duplicate those owners.

`CAPABILITY GAP ≠ NEW CORE SKILL REQUIRED`.

## P0 — highest-value residual gaps

### GAP-ENG-01 — DFM / DFA / GD&T-GPS / Tolerance / Metrology / Product Release
Current coverage: design-process handles physical-product reasoning; 3D handles CAD/STEP/datum/assembly geometry truth; technical-drawing handles drawing semantics; shared runtime already exposes CAD/DXF/STEP. None of these prove manufacturability or released process capability.

Residual chain:
`FUNCTIONAL REQUIREMENT → DATUM STRATEGY → FIT → TOLERANCE STACK → GD&T/GPS → PROCESS CAPABILITY → MEASUREMENT PLAN → DFM/DFA → INSPECTION → BOM/REVISION → RELEASE EVIDENCE`.

Sources:
- `wonsukchoi/domain-experts/roles/manufacturing-engineer/SKILL.md` — MIT. Useful mechanisms: datum reference frame as functional contract; manufacturability tied to candidate process; measurement-system capability before capability claim; process/tolerance mismatch must return to design before tooling.
- `K-Dense-AI/scientific-agents/precision-engineering-specialist` — MIT. Useful for GD&T/CMM/metrology/measurement uncertainty/error-budget reasoning.
- `beiming183-cloud/AutoCAD-skills/mechanical-drafting-gbt` — comparison only against existing OLEANDER Technical Drawing; do not create a parallel drafting owner before license/current comparison.

Reject as universal: fixed Cpk/Ppk/GR&R thresholds, automatic RSS-vs-worst-case rules, one PPAP/APQP release sequence, one jurisdiction/standard edition as global truth, drawing/CMM report as manufacturing approval.

Route: `oleander-design-process → oleander-3d-pipeline / oleander-technical-drawing → oleander-delivery-qc / VALIDATION`.

### GAP-HUM-01 — Human Factors / Ergonomics / Anthropometry
Residual chain:
`USER POPULATION → TASK → POSTURE → REACH / CLEARANCE → GRIP / FORCE → VISUAL FIELD → REPETITION / FATIGUE → VARIABILITY / IMPAIRMENT → DESIGN CONSEQUENCE → PHYSICAL TEST`.

Sources:
- NASA Human Integration Design Handbook + Human Integration Design Processes — official human-system design reference.
- CDC/NIOSH Anthropometry — official evidence that population/body-size variability matters to tools, workspaces and PPE.
- `getburo/buro-free/industrial-designer` — All Rights Reserved; only high-level independently reformulated concepts may be retained.

Reject as universal: automatic `5th–95th percentile` coverage, one grip/reach table, render-pose ergonomics, digital-human fit as physical proof, population data used without demographic/task fit.

Route: `oleander-design-process`, co-route technical-drawing/VALIDATION when dimensions become claims.

### GAP-VAL-01 — Physical Prototype / Test Planning / Verification-Validation Matrix
Residual chain:
`DESIGN CLAIM → TESTABLE REQUIREMENT → TEST ARTICLE PEDIGREE/FIDELITY → METHOD (ANALYSIS / INSPECTION / DEMONSTRATION / TEST) → FIXTURE/SETUP → VARIABLES/MEASUREMENTS → ACCEPTANCE / FAILURE → RUN → FAILURE EVIDENCE → SOURCE REPAIR → RETEST`.

Source:
- NASA Systems Engineering Handbook V&V planning / validation requirements matrix — official source distinguishing physical models, simulations, fit-checks, procedure dry-runs and controlled final units.

Retained candidate delta: `PROTOTYPE FIDELITY MUST MATCH THE CLAIM BEING TESTED` and `TEST ARTICLE PEDIGREE MUST BE RECORDED`.

Reject as universal: NASA lifecycle vocabulary as OLEANDER lifecycle, prototype pass as final validation, one mandatory test method for all claims.

Route: `oleander-design-process → oleander-delivery-qc / VALIDATION`.

### GAP-FIELD-01 — Field Survey / Reality Capture / Photogrammetry
Residual chain:
`SURVEY QUESTION → CONTROL / SCALE / COORDINATE AUTHORITY → CAPTURE PLAN → PHOTO/VIDEO/MEASUREMENT/GNSS/POINT CLOUD → METADATA → REGISTRATION → ERROR/UNCERTAINTY → DERIVED GEOMETRY → FIELD EVIDENCE → DESIGN CONSEQUENCE`.

Sources:
- USGS 2026 Structure-from-Motion aided photogrammetry technical manual — current official source stressing control, tie/control/scale measurements and error estimates.
- Autodesk Reality Capture sample — implementation reference only, not evidence authority.

Reject as universal: one RMSE threshold, one Metashape/RealityCapture tuning value, point-cloud/mesh as field truth without control/uncertainty, photogrammetry replacing required licensed survey.

Route: `oleander-research + oleander-data-viz + oleander-3d-pipeline`.

### GAP-BIM-01 — OpenBIM / IFC Information Requirements / Coordination
Residual chain:
`INFORMATION REQUIREMENT → MODEL BREAKDOWN → CLASSIFICATION → OBJECT / PROPERTY REQUIREMENT → IFC/IDS/bSDD → DISCIPLINE MODEL → COORDINATION / ISSUE → BCF / REVISION → MODEL QA → EXCHANGE READBACK`.

Sources:
- buildingSMART IFC 4.3 official material;
- buildingSMART IDS 1.0 information-requirement/checking ecosystem;
- buildingSMART bSDD class/property dictionary references;
- buildingSMART implementation listings, whose self-reported-support warning is itself a useful evidence-trust boundary.

Reject as universal: `IFC export succeeded = coordinated BIM`, self-reported software support as certification, one LOD/LOI numbering system, RVT-native capability without actual runtime.

Route: `oleander-3d-pipeline + oleander-technical-drawing + delivery/validation`; no software-specific Revit Skill by default.

### GAP-BLDG-01 — Building Performance Analysis / Simulation
Residual chain:
`DESIGN QUESTION → CLIMATE / PROGRAM / MODEL ASSUMPTIONS → GEOMETRY / ENVELOPE / SYSTEM → METRIC → SIMULATION ENGINE → SENSITIVITY → RESULT → DESIGN CONSEQUENCE → RETEST`.

Sources:
- Ladybug Tools / Honeybee — open energy/daylight model ecosystem with explicit geometry/sensor/model assumptions;
- EnergyPlus / Radiance should be selected by the question, not treated as universal design authority.

Retained candidate delta: `SIMULATION INPUT AUTHORITY + MODEL ASSUMPTION + METRIC FITNESS MUST BE EXPLICIT BEFORE RESULT IS ALLOWED TO CHANGE DESIGN`.

Reject as universal: tool defaults as design criteria, simulation output as code/comfort/field approval, one engine for daylight/thermal/airflow/energy.

Route: `oleander-design-process + oleander-data-viz + VALIDATION`.

## P1 — additional engineering-evidence gaps

### GAP-REL-01 — Reliability / Durability / Accelerated-Life Evidence
Residual chain:
`DUTY CYCLE / ENVIRONMENT → FAILURE MODE → RELIABILITY REQUIREMENT → TEST/ANALYSIS → FAILURE DATA → ROOT CAUSE → CORRECTIVE ACTION → RETEST → REVISION TRACE`.

Source: `K-Dense-AI/scientific-agents/reliability-engineer` — MIT; useful concepts include FRACAS, FMECA/DFMEA/PFMEA, accelerated-life/testing vocabulary and revision trace. Reject domain-specific release thresholds and profiles as universal.

### GAP-SAFE-01 — Hazard / Safety / Risk Analysis
Residual chain:
`HAZARD → HARM / SEVERITY CONTEXT → CAUSAL PATH → CONTROL HIERARCHY → REQUIREMENT → VERIFICATION → RESIDUAL RISK → CHANGE TRACE`.

Candidate frameworks: FMEA/FMECA, FTA, STPA, HAZOP selected by domain/problem. Reject one global risk matrix, one severity scale, one RPN threshold, or AI safety sign-off.

### GAP-MAT-01 — Material Selection / Process / Failure Analysis
Source: `wonsukchoi/domain-experts/materials-engineer` — MIT.

Residual chain:
`LOAD / ENVIRONMENT / LIFE → FAILURE MODE → MATERIAL PROPERTY SOURCE → PROCESS / SECTION / FINISH EFFECT → CANDIDATES → TRADEOFF → SAMPLE / TEST → FAILURE / AGING → DESIGN REVISION`.

Retained delta: coupon/datasheet property ≠ real-part behavior; failure mode and environment govern material/process selection. Reject handbook constants/alloy rankings/heat-treatment recipes without current material/process evidence.

### GAP-MET-01 — Measurement / Metrology / Uncertainty
Residual chain:
`MEASURAND → METHOD / INSTRUMENT → CALIBRATION / TRACEABILITY → RESOLUTION / REPEATABILITY → UNCERTAINTY → DECISION RULE → RESULT → CLAIM BOUNDARY`.

Source group: K-Dense precision/metrology profile (MIT) plus GUM/ISO/NIST primary sources when quantitative use is required.

Candidate hard rule: `MEASURED NUMBER WITHOUT METHOD + UNCERTAINTY + TRACEABILITY IS NOT DIMENSIONAL AUTHORITY`.

### GAP-REQ-01 — Requirements Engineering / Traceability / Change Impact
Residual chain:
`STAKEHOLDER / SOURCE → ATOMIC REQUIREMENT → RATIONALE / PRIORITY → ACCEPTANCE / VERIFICATION METHOD → DESIGN OBJECT → TEST/EVIDENCE → CHANGE IMPACT → STATUS`.

Source:
- `jdm4pku/RE-Skills` — broad RE Skill set, including elicitation/acceptance/management/validation. No root LICENSE was observed in the inspected repository tree; treat as `LICENSE-UNCLEAR / HIGH-LEVEL COMPARISON ONLY` unless clarified.
- NASA V&V planning is a stronger primary-source cross-check for requirement-to-verification binding.

Reject software-only user-story/Gherkin conventions as universal physical/architectural requirements practice.

### GAP-CONF-01 — BOM / Configuration / Specification / Release Control
Residual chain:
`OBJECT / PART → SPEC → MATERIAL/PROCESS → DRAWING/MODEL → BOM → REVISION → CHANGE EFFECTIVITY → SUPPLIER / BUILD RECORD → AS-BUILT / AS-MADE EVIDENCE`.

This is distinct from repository version control. Route to `technical-drawing + delivery-qc + governance`, co-routed with material/procurement knowledge.

## P2 — known but still thin execution layers

- Acoustic design & measurement: system/product knowledge exists, unified requirement→model/measurement→space consequence method remains thin.
- LCA / embodied carbon evidence: sustainability/circular-design knowledge exists; functional-unit/system-boundary/EPD/scenario evidence remains thin.
- Cost / quantity / value engineering: pricing/procurement knowledge exists; option-QTO/cost-source/freshness/risk/value loop remains thin.
- Physical accessibility / inclusive design: digital accessibility is stronger than physical/body/environment accessibility.
- Mechanism / kinematics / load-path reasoning: no consolidated input→joint→motion→constraint→load/stop/failure→validation contract.
- Photography capture / evidence photography: Claim-bound Camera + art direction exist; repeatable capture/scale/metadata/light/evidence discipline remains thin.

## Source / rights ledger

- `wonsukchoi/domain-experts` — MIT confirmed 2026-08-29.
- `K-Dense-AI/scientific-agents` — MIT confirmed 2026-08-29.
- `jdm4pku/RE-Skills` — no root LICENSE observed in inspected tree; high-level comparison only.
- NASA HIDH/HIDP and Systems Engineering Handbook — official professional references; do not import NASA lifecycle/identity as defaults.
- CDC/NIOSH Anthropometry — official evidence reference.
- USGS SfM photogrammetry technical manual — official evidence reference; numeric/tuning details remain context-specific.
- buildingSMART IFC/IDS/bSDD — official openBIM references; tool support listings are self-reported unless certified separately.
- Ladybug Tools/Honeybee — open-source simulation workflow reference; tool defaults are not universal design criteria.

## Recommended next discovery/digestion order

1. `DFM / GD&T / METROLOGY / RELEASE`
2. `HUMAN FACTORS / ERGONOMICS`
3. `PHYSICAL PROTOTYPE / TEST PLANNING`
4. `FIELD SURVEY / REALITY CAPTURE`
5. `OPENBIM / IFC / IDS / BCF`
6. `BUILDING PERFORMANCE SIMULATION`
7. `RELIABILITY / DURABILITY`
8. `MATERIAL SELECTION / FAILURE ANALYSIS`
9. `REQUIREMENTS / TRACEABILITY`
10. `HAZARD / SAFETY / RISK`
11. `CONFIGURATION / BOM / SPECIFICATION RELEASE`
12. remaining P2 execution gaps.

## Promotion firewall

This map authorizes search/comparison only.

`SOURCE FOUND ≠ SKILL DIGESTED`

`SKILL DIGESTED ≠ EXTENSION INSTALLED`

`EXTENSION DOCUMENTED ≠ CURRENT L5`

`CI PASS ≠ ENGINEERING / FIELD / MANUFACTURING / SAFETY PASS`

`CROSS-CONTEXT PRACTICE ≠ PROJECT USAGE ≠ VALIDATED CANDIDATE ≠ ACTIVE`

Before any extension is written: re-run Current + SUPPORT + METHOD-RECOVERY comparison for that exact gap; read license/rights and core references; isolate Material Delta; reject fixed heuristics; design an adversarial eval; preserve independent professional authority and physical/field HOLDs.