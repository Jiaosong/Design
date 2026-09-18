# 2026-09-18｜Lighting Design Professional Process Digestion

Status: `CANDIDATE R-E PROFESSIONAL PROCESS / TWO HISTORICAL GENERATIONS DIGESTED / CURRENT CONTRACT ALIGNED / 2025–2026 IES SOURCE REFRESH / PRACTITIONER RELEASE OBJECTS + INTERFACE BINDINGS DEEPENED / PROJECT EXERCISE NOT YET CLAIMED / NO PROMOTION`

## Existing-first sources

Two historical remote branches were reviewed.

### Generation A — v21 evolution

Branch:
`agent/v21-lighting-domain-process-evolution-20260915`

Files:
- `00-governance/lighting-design-process-v1.0.md`
- `00-governance/schemas/lighting-design-process.v1.json`

Unique useful content:
- Lighting Basis / responsibility;
- visual-task / experience / time-state matrix;
- daylight-electric integration;
- luminaire/product/optic register;
- controls/scene register;
- mockup/aiming benchmark;
- production/submittal/equivalent support;
- commissioning/aiming/measurement/handover;
- maintenance/post-occupancy.

Its evolution/promotion state was **not** adopted.

### Generation B — professional-depth Stage11

Branch:
`candidate/professional-depth-stage11-20260916`

Files:
- `00-governance/lighting-design-development-process-v1.0.md`
- `00-governance/schemas/lighting-design-process.v1.json`

This is the professional-depth mother because it contains the richer decision body for:
- visual task / adaptation;
- daylight as geometry/time/material;
- luminous hierarchy / brightness;
- photometric assumptions and uncertainty;
- glare/reflection mechanism;
- color/spectral/material appearance;
- luminaire/optic integration;
- controls / scenes / daylight response;
- exterior/night;
- mockup / model correlation;
- specification/substitution;
- commissioning/night readback;
- maintenance / post-occupancy.

Material deficit found:
- machine `interface_bindings[]` were effectively empty;
- practitioner release objects for tag→electrical/control mapping, submittal release and commissioning acceptance were not explicit enough.

Current Candidate therefore uses Stage11 as mother and absorbs unique v21 execution objects without creating a parallel framework.

---

# Current professional-source refresh｜2026-09-18

Current IES public Lighting Library / standards listings were reviewed.

## IES Lighting Practice scope

Current Lighting Library includes practice standards for:
- people/buildings;
- outdoor environments;
- daylight;
- electric light sources;
- controls;
- design/construction process;
- commissioning;
- maintenance/upgrades;
- environmental/outdoor impacts.

## ANSI/IES LP-6-25

Current 2025 Lighting Controls practice evidence explicitly covers:
- control-system design factors;
- documentation for design, construction, commissioning and functional testing;
- control strategies/equipment;
- emergency-lighting control interfaces;
- physical implementation;
- interoperability/protocol concerns.

Accepted transfer:
`CONTROL INTENT → DOCUMENTED GROUPS/SEQUENCES/INTERFACES → ACCEPTANCE TEST → ACTUAL COMMISSIONING READBACK`.

## ANSI/IES LP-8-20

Current IES commissioning evidence states that design intent must be monitored through construction/final installation and correct luminaires, sources, drivers/ballasts and controls must be installed and perform against owner/designer criteria.

Accepted transfer:
`POWERED ON ≠ COMMISSIONED`.

## ANSI/IES LP-16-22

Accepted transfer:
control narrative / sequence-of-operation documentation is an implementation/commissioning carrier, not a replacement for design.

## ANSI/IES TM-30-24 + LP-30-26

Accepted transfer:
- color rendition is not reducible to a single generic CRI/CCT claim;
- project-specific color goals/criteria need a bounded reason;
- phase-specific specification / procurement / CA consequences matter.

No universal TM-30 number is introduced by OLEANDER.

## ANSI/IES LP-42-26

Accepted transfer:
dimming/control method identity and protocol information belong in luminaire/control scheduling and implementation evidence.

## ANSI/IES LP-4-20(R2026)

Accepted transfer:
source properties/selection/specification are material professional objects.

---

# Current Candidate

Prose:
`00-governance/lighting-design-process-v1.0-CANDIDATE.md`

Machine definition:
`00-governance/schemas/lighting-design-process.v1.candidate.json`

Current Architecture remains:
`Lighting Design = CONTRACT_ENVELOPE_AVAILABLE / DOMAIN PROCESS OPEN`.

---

# Stage structure preserved from professional-depth mother

- LGT-00 Lighting Brief / Tasks / States
- LGT-01 Daylight + Luminous Concept
- LGT-02 Photometric / Brightness / Glare / Color
- LGT-03 Luminaire / Optics / Source / Integration
- LGT-04 Controls / Scenes / Daylight Response / User Interaction
- LGT-05 Exterior / Landscape / Façade / Night
- LGT-06 Mockup / Sample / Calculation / Verification
- LGT-07 Specification / Procurement / Substitution / Construction Coordination
- LGT-08 Commissioning / Aiming / Measurement / Actual Night Readback
- LGT-09 Maintenance / Replacement / POE Tuning / Learning

These are OLEANDER Lighting candidate stages.

They are not copied IES project stages.

---

# New practitioner control objects

## 1. Lighting Basis / Responsibility Matrix

`AREA/SPACE → USER/TASK → TIME/STATE → LIGHTING ROLE → OWNER → ELECTRICAL/CONTROLS/FIRE/DAYLIGHT/MAINTENANCE RESPONSIBILITY → CRITERION SOURCE → VALIDATION → OPEN ITEM`.

## 2. Daylight Model Configuration Record

Binds weather/sky, geometry, glazing, reflectance, shade, sensor/view, engine/version and sensitivity variables.

## 3. Photometric Model Configuration Record

`MODEL → GEOMETRY REV → PHOTOMETRIC FILE REV → OUTPUT FACTOR → MOUNTING/AIMING → SURFACES → CALCULATION/VIEW PLANES → SCENE → MAINTENANCE BASIS → ENGINE/VERSION → RESULT`.

## 4. Luminaire / Optical / Product Register

Binds tag, optic/distribution, output/power, driver, color, control method, mounting/aiming, shielding, environment, access, photometric file and substitution-critical attributes.

## 5. Luminaire tag → electrical / control mapping

`TAG → DRIVER → CIRCUIT/FEED → GROUP/ADDRESS → METHOD/PROTOCOL → SCENE → SENSOR/TRIGGER → EMERGENCY RELATION → OWNER → TEST POINT`.

Lighting does not assume Electrical circuit-protection authority or Controls programming approval.

## 6. Control Intent / Sequence Register

`SCENE → TRIGGER → GROUPS → COMMAND → CURVE/FADE/SEQUENCE → DAYLIGHT RESPONSE → OVERRIDE → FAILSAFE/DEGRADED → INTERFACE → TEST → READBACK`.

## 7. Luminaire Submittal / Substitution Release Register

`SUBMITTAL → GOVERNING CURRENT → PRODUCT/OPTIC/DRIVER/CONTROL → DEVIATIONS → PHOTOMETRIC/COLOR/GLARE/DIMENSION/THERMAL/MAINTENANCE/CONTROL IMPACT → RECALC/REMOCKUP → INTERFACE IMPACT → DISPOSITION → CURRENT UPDATE`.

## 8. Aiming / Focusing Record

Captures installed tag/location/target/final setting/beam/accessory/output/scene/conflict/reviewer/date.

## 9. Commissioning Criterion / Result / Compliance Matrix

`CRITERION → SOURCE → OPERATING STATE → TEST → EXPECTED → ACTUAL → RESULT → DEFECT/ACTION → RETEST → FINAL CONFIGURATION`.

## 10. Maintenance / Replacement Equivalence Register

A replacement must retain the required luminous, color, control, detail, thermal/access and aiming relationships—not merely fit physically.

---

# Continuous technical threads

- LGT-T01 Scope / visual task / responsibility
- LGT-T02 Daylight / temporal state
- LGT-T03 Luminous hierarchy / brightness / glare
- LGT-T04 Photometric model / assumptions
- LGT-T05 Color quality / spectral / material appearance
- LGT-T06 Luminaire / optic / source / driver
- LGT-T07 Mounting / integration / access
- LGT-T08 Electrical/control mapping / sequences
- LGT-T09 Exterior/night/ecology/spill
- LGT-T10 Mockup / benchmark / verification
- LGT-T11 Specification / submittal / substitution
- LGT-T12 Construction coordination / field
- LGT-T13 Aiming / commissioning / measurement
- LGT-T14 Handover / O&M / maintenance / replacement
- LGT-T15 Post-occupancy tuning / learning
- LGT-T16 Cross-disciplinary interfaces / responsibility

---

# Machine interface deepening

The Stage11 machine definition had deep stage content but no meaningful per-stage interface bindings.

The Candidate now binds 27 interfaces across:
- Architecture;
- Interior;
- Electrical Engineering;
- Structural Engineering;
- Controls/BMS;
- Digital Product/HCD;
- Landscape Architecture;
- Ecology;
- Façade;
- Procurement/Supplier;
- Fire/Life Safety;
- Facilities Management / Operations.

R-F Cross-Disciplinary Integration remains the only interface-maturity/disposition owner.

Lighting declares stage-side requirements only.

---

# AIG-02 regression

Added:
- FAIL-031 — photometric result from wrong configuration;
- FAIL-032 — lighting metric used outside its actual task/view question;
- FAIL-033 — shallow lumens/watts/CCT/beam substitution equivalence;
- FAIL-034 — scene names without real control sequence;
- FAIL-035 — luminaire tags not mapped to electrical/control implementation;
- FAIL-036 — protocol label treated as commissioned behavior;
- FAIL-037 — mockup generalized beyond tested configuration;
- FAIL-038 — commissioning without criterion/result/retest matrix;
- FAIL-039 — field aiming/tuning not captured in final configuration;
- FAIL-040 — physical-fit replacement treated as performance equivalence.

---

# Explicit non-delta

This batch does not:
- make Lighting Current;
- restore old evolution/adoption state;
- create universal lighting thresholds;
- make IES standards project criteria without applicability/authority;
- grant Electrical / Fire / Accessibility / Energy / Ecology / Health approval;
- create a Lighting-specific interface maturity system;
- create a Core Skill;
- claim a project Lighting PASS without project exercise.

---

# Bounded practice reapplication｜SP03-R02

Historical practice branch:

`practice/2026-08-11-sp03-r02-light-performance-interface@95c4543db17dc0e98459c967a4e36a5bb4cd92e3`

was reapplied to the Candidate without copying its synthetic result into project truth.

Source evidence includes:
- exact synthetic test-cell input contract;
- real Radiance 6.0a runs;
- evalglare 3.06;
- pyradiance 1.2.4;
- 8 workplane simulations;
- 16 HDR glare views;
- 16 evalglare evaluations;
- failure/reopen history;
- numerically-stable-not-byte-identical reproduction evidence.

Candidate coverage:

- `LGT-00` — PARTIAL practice support;
- `LGT-01` — practice support;
- `LGT-02` — practice support;
- `LGT-06` — practice support;
- `LGT-03/04/05/07/08/09` — explicitly NOT_EXERCISED.

The exercise proves:
- model configuration must be bound to a result;
- one preferred render/sky cannot prove robustness;
- runtime PASS is not artifact/professional PASS;
- schema/parser defects can invalidate evidence interpretation;
- simulation can expose tradeoffs without selecting a universal winner.

It does **not** prove:
- real project geometry/material/weather/time;
- project lighting criteria;
- real product/optic/driver selection;
- controls implementation;
- production/submittal;
- installed aiming/commissioning;
- maintenance/post-occupancy;
- project Lighting professional PASS.

Machine reapplication:
`06-practice/2026/2026-09-18-lighting-process-reapplication/LGT_SP03_R02_CANDIDATE_REAPPLICATION_v0.1.json`

Receipt:
`06-practice/2026/2026-09-18-lighting-process-reapplication/LGT_SP03_R02_CANDIDATE_REAPPLICATION_RECEIPT_v0.1.json`

This raises method-use evidence without closing the Project Reality gate.

---

# Maturity

Current ceiling:

`CANDIDATE PROCESS / STAGE11 PROFESSIONAL-DEPTH MOTHER / UNIQUE v21 EXECUTION OBJECTS ABSORBED / CURRENT CONTRACT MACHINE DEFINITION / 2025–2026 IES SOURCE REFRESH / 27 INTERFACE BINDINGS / PRACTITIONER RELEASE OBJECTS / AIG FAILURE REGRESSION / SP03-R02 SYNTHETIC PRACTICE REAPPLICATION / PROJECT EXERCISE NOT CLAIMED / INDEPENDENT LIGHTING PROFESSIONAL REVIEW NOT_RUN / NO CURRENT PROMOTION`.

The remaining Lighting gap is now:
**real project exercise + independent Lighting professional review**.

It is no longer missing process granularity.

`LIGHTING PROCESS DETAIL EXISTS ≠ INSTALLED PERFORMANCE`.

`COMMISSIONING RECORD EXISTS ≠ DESIGN KEEP`.
