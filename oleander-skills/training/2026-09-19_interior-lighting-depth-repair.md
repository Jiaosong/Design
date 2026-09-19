# 2026-09-19｜Interior + Lighting Candidate Practitioner-Depth Repair

Status: `STRICT CONTENT REVIEW / EXISTING CANDIDATES PRESERVED / SIX MATERIAL DELTAS / NO NEW PROCESS / NO CURRENT PROMOTION`

## Existing-first correction

Initial search correctly found that Interior Design and Lighting Design remain `DOMAIN PROCESS OPEN` in the Current Architecture Map, but a later read of the latest main revealed that both already have validated **Candidate professional-process definitions**:

- `00-governance/interior-design-process-v1.0-CANDIDATE.md`
- `00-governance/schemas/interior-design-process.v1.candidate.json`
- `00-governance/lighting-design-process-v1.0-CANDIDATE.md`
- `00-governance/schemas/lighting-design-process.v1.candidate.json`

Latest main also contains:
- an open-domain adoption frontier;
- synthetic Lighting practice reapplication;
- explicit usage-empty / synthetic-practice / bounded-project-adoption distinctions.

Therefore no new readiness layer or parallel Candidate process is appropriate.

The repair target changed to:

> strict practitioner-depth audit of the existing Interior / Lighting Candidate definitions.

---

# Interior audit

Existing Interior Candidate already covers:
- existing conditions / base-building authority;
- brief / user / operations;
- code / life safety / accessibility;
- space planning / clearances;
- partitions / doors / hardware / glazing;
- RCP / lighting / MEP / acoustics;
- finishes / substrates / transitions;
- joinery / millwork;
- FF&E / procurement / logistics;
- details / specifications / schedules / QA-QC;
- submittals / samples / mockups / substitutions;
- construction administration / site observation / change;
- closeout / O&M / warranties / asset data;
- post-occupancy / maintenance / adaptation.

Existing release chains are already strong:
- RCP / ceiling-service;
- joinery / millwork;
- door / hardware;
- finish;
- FF&E;
- submittal / substitution;
- closeout.

## Interior material gap

The machine carrier did not expose one unified professional-object contract for:

`STABLE ID → REVISION/CONFIGURATION → NATIVE SOURCE → PRODUCT/MATERIAL/FABRICATION IDENTITY → OWNER → INTERFACE → RELEASE STATE → ACTUAL READBACK → REOPEN`.

The information existed in fragments, but was not explicit as a single machine-readable execution-depth object.

### Delta I-01

Add:

`Professional Object Identity / Revision / Release Register`.

Applies to:
- room / zone;
- RCP zone;
- door/opening/hardware set;
- finish;
- joinery/millwork;
- FF&E/equipment;
- detail;
- submittal/mockup/sample;
- installed/closeout item.

Rules:
- tag alone is insufficient where document/product/field revisions can diverge;
- `CURRENT` means resolved owner-native revision/configuration, not “latest file seen”;
- release binds owner + exact claim boundary;
- actual readback binds the same object identity/configuration or records deviation;
- substitution creates a successor configuration;
- owner/source/revision/configuration/installed-identity/interface change reopens consumers.

This deepens the existing professional process; it does not create a new state registry.

---

# Lighting audit

Existing Lighting Candidate already covers:
- brief / visual tasks / operating states;
- daylight / luminous concept;
- photometric / brightness / glare / color-quality;
- luminaire / optics / source / architectural integration;
- controls / scenes / daylight response / user interaction;
- exterior / landscape / façade / night;
- mockup / sample / calculation verification;
- specification / procurement / substitution;
- commissioning / aiming / measurement / night readback;
- maintenance / replacement / POE / tuning.

Existing synthetic practice correctly remains:
`project_exercise_counted = false`.

## Professional-source refresh

Current public IES material reviewed in 2026 confirms:
- LP-6-25 expands lighting-control design/documentation and system-level control considerations, including interoperability/cybersecurity-related controls context;
- LP-8-20 treats commissioning as QA across design/construction/occupancy;
- LP-42-26 updates control method designations;
- LP-4-20(R2026) remains current for electric-light-source selection/specification.

No universal metric threshold was imported.

---

# Lighting material gaps

## Delta L-01｜Temporal-light quality as an explicit object

Existing prose mentioned:
- low-end dimming;
- temporal output;
- dropout/pop-on/stepping/hunting;
- camera/display banding.

Gap:
the process did not expose a stable object carrying:
- material user/task/camera/display condition;
- governing criterion/source;
- exact driver/control/dimming/output configuration;
- measurement/observation method;
- limitation.

Added:

`Temporal Light Quality / Driver-Control State Record`.

No universal PstLM/SVM threshold is introduced. Specific metrics apply only when a mounted source/project requirement makes them material.

## Delta L-02｜Networked-controls interoperability / cybersecurity owner boundary

Existing Candidate covered protocol/groups/addressing but not a dedicated network-controls professional handoff.

Added:

`Control Network / Interoperability / Cybersecurity Handoff Record`.

Minimum content where material:
- protocol/topology;
- gateway;
- remote access;
- firmware/configuration identity;
- interoperability dependency;
- failure/degraded state;
- Controls / IT / Cybersecurity owner.

Lighting owns luminous/control intent and interaction consequences within appointment; it does not self-certify cybersecurity/IT approval.

## Delta L-03｜Measurement identity / calibration / uncertainty

Existing LGT-08 required measurement context but did not expose a dedicated field object.

Added:

`Measurement Instrument / Method / Calibration / Uncertainty Record`.

Carrier:
- instrument ID;
- calibration/status;
- method;
- location/plane/view;
- time/state/configuration;
- sampling/repeatability;
- uncertainty/method limits;
- raw/derived result refs.

## Delta L-04｜Commissioned baseline / final configuration

Existing LGT-09 already required comparison to commissioned behavior, but LGT-08 did not expose a dedicated baseline manifest.

Added:

`Commissioned Baseline / Final Configuration Manifest`.

Carrier:
- final luminaire;
- optic;
- driver;
- control/address;
- firmware/configuration where material;
- scene;
- aim;
- sensor;
- accepted deviations;
- final settings;
- reviewer/date;
- baseline ref/digest.

LGT-09 now consumes this baseline explicitly.

---

# Regression additions

## FAIL-052
Interior professional object released without stable identity/revision/configuration/owner/release/readback/reopen chain.

## FAIL-053
Temporal-light quality claim based on generic “flicker-free” or unbound metric without condition/source/configuration/method.

## FAIL-054
Networked lighting controls treated as interoperable/secure merely because devices communicate.

## FAIL-055
Lighting field measurement reported without instrument/method/calibration/state/uncertainty context.

## FAIL-056
Post-occupancy drift/tuning/replacement compared to memory/generic intent rather than commissioned baseline.

---

# Explicit non-delta

This repair does not:
- create new Interior stages;
- create new Lighting stages;
- promote either Candidate to Current;
- create a new cybersecurity process;
- create a new commissioning process;
- make Lighting owner of IT/cyber approval;
- introduce universal flicker, illuminance, glare or color thresholds;
- promote synthetic Lighting practice to real project exercise;
- change the Current Architecture Map OPEN state.

---

# Maturity

`INTERIOR CANDIDATE = EXISTING PROFESSIONAL DEPTH + OBJECT IDENTITY/REVISION/RELEASE CONTRACT DEEPENED`.

`LIGHTING CANDIDATE = EXISTING PROFESSIONAL DEPTH + TEMPORAL / NETWORK-CONTROL / MEASUREMENT / COMMISSIONED-BASELINE OBJECTS DEEPENED`.

Next evidence need remains unchanged:
- Interior still lacks real project adoption evidence;
- Lighting still lacks real project adoption/installed commissioning evidence;
- both remain `DOMAIN PROCESS OPEN` until authorized promotion.
