# OLEANDER Building Acoustics Professional Process v1.0

**Status:** CONTROLLED EVOLUTION CANDIDATE — NOT CURRENT / NOT PROFESSIONAL PASS  
**Evolution ID:** `EV-PROF-ACOUSTICS-20260916`  
**Authority baseline:** `OLEANDER_CURRENT_ARCHITECTURE_MAP_v2.1` + `professional-domain-process-contract-v1.0.md`  
**Knowledge position:** consumes existing OLEANDER Specialty/Acoustics, Human-space, Material-System and product/system Knowledge owners; does not create a second acoustic Knowledge authority.  
**Integration position:** all cross-domain interface truth remains owned by Current R-F Cross-Disciplinary Integration.  

---

## 1｜Purpose

This candidate defines a domain-native professional process for **Building Acoustics / Acoustic Design**. It does not convert generic reverberation, sound-insulation, absorption or noise values into project targets, and it does not treat one product rating, laboratory result, model output or field sample as proof of complete occupied-building acoustic performance.

The process carries acoustic work through:

`USE / ACTIVITY / SOURCE-RECEIVER CONTEXT → CRITERIA / MEASUREMENT BASIS → ROOM ACOUSTICS → SEPARATION / FLANKING → BUILDING-SERVICES NOISE / VIBRATION → DETAIL / INTERFACE → TEST / COMMISSIONING → DELIVERY / FIELD READBACK → IN-USE RESPONSE / CHANGE`

It preserves the distinction between **acoustic design intent**, **prediction**, **laboratory element/system evidence**, **field measurement**, and **experienced/operational outcome**.

---

## 2｜Professional basis and source boundary

Current source context used by this candidate includes:

- **ISO 3382-2:2008** — current confirmed method context for reverberation-time measurement in ordinary rooms;
- **ISO 16283-1:2014 + applicable amendment** — current confirmed field-measurement context for airborne sound insulation between rooms;
- **ISO 717-1:2020** — current confirmed rating method context for airborne sound insulation from frequency-dependent measurements;
- other project-applicable ISO/national/local standards for impact sound, façade sound insulation, equipment noise, room acoustics, educational/healthcare/residential or specialist spaces only after exact applicability review;
- **Institute of Acoustics Building Acoustics Group** as current professional context spanning room acoustics, sound insulation, HVAC acoustic design and vibration isolation;
- project jurisdiction, client brief, specialist appointment, building type, room task, operational state, source spectrum, background conditions and responsible professional/statutory authority remain controlling.

These references do **not** establish one universal `RT`, `Rw`, `DnT,w`, `LnT,w`, `NR/NC`, dBA, absorption coefficient, background-noise or vibration target for every project. Metrics, targets, frequency range, averaging, correction, uncertainty and acceptance route must be project/source/method specific.

---

## 3｜Scope

### In scope

- acoustic appointment, project/use/task/source-receiver basis and claim ceiling;
- acoustic criteria and measurement/verification basis;
- room acoustics for speech, music, learning, healthcare, work, rest, privacy or other project tasks where triggered;
- airborne and impact sound separation and flanking-path control;
- façade/environmental noise interface where part of the acoustic appointment;
- building-services noise and vibration criteria/interfaces with MEP and structure;
- partitions, ceilings, floors, doors, glazing, junctions, penetrations, seals and absorptive/diffusive systems at acoustic interfaces;
- electroacoustic/sound-system interface only to the extent necessary to coordinate room/building acoustics; system design authority stays with its actual owner;
- acoustic modelling/prediction where appropriate and explicitly bounded;
- laboratory/system evidence and project-specific mock-up/field testing where required;
- construction/submittal/site QA affecting acoustic performance;
- commissioning/field measurement, defects/complaints and in-use return.

### Outside this process authority

- universal room-acoustic or sound-insulation target values;
- Architecture Design KEEP or spatial/aesthetic authority;
- MEP equipment/system engineering approval;
- Structural Engineering approval of vibration-supporting structure;
- product procurement approval merely because acoustic data exists;
- electroacoustic/sound-system design approval outside appointment;
- statutory approval, code compliance or licensed sign-off outside actual authority;
- R-F Integration PASS;
- field truth inferred from simulation, laboratory ratings or a single measurement;
- Project Promotion.

---

## 4｜Native professional carriers

`ACO-BASIS → ACO-ROOM → ACO-SEPARATION → ACO-NOISEVIB → ACO-DETAIL → ACO-TEST → ACO-DELIVERY → ACO-INUSE`

These are OLEANDER carriers for this candidate. They are not Architecture `ADD-*` aliases and are not claimed as ISO/IOA stage numbering.

---

## 5｜ACO-BASIS — Use / Source-Receiver / Criteria / Verification Basis

**Question:** What acoustic outcome is actually in scope for which users/tasks, sources, receiving spaces and operating states, under which source/measurement/verification basis?

Required native outputs:

- `ACOUSTIC_SCOPE_AUTHORITY_REGISTER`
- `SOURCE_RECEIVER_TASK_MATRIX`
- `ACOUSTIC_CRITERIA_METHOD_REGISTER`
- `ACOUSTIC_VERIFICATION_PLAN`
- `OPEN_ASSUMPTION_SOURCE_REGISTER`

Must establish:

- project/building/room use and time-state assumptions;
- speech, music, privacy, rest, concentration, healthcare, recording, industrial or other task needs where relevant;
- internal/external source types and spectral/time characteristics where consequential;
- receiver sensitivity and occupancy/operational state;
- applicable metric, method, frequency range and acceptance context for each claim;
- distinction between client aspiration, code/minimum requirement, specialist design target and test/acceptance criterion;
- existing-condition baseline where material;
- measurement/prediction uncertainty and open source assumptions where relevant.

**Exit ceiling:** `ACOUSTIC_BASIS_RESOLVED`.

Does not prove a room, partition, service system or completed building meets any target.

---

## 6｜ACO-ROOM — Room Acoustics / Speech / Music / Spatial Sound Field

**Question:** Does the room acoustic strategy support the declared task at the current evidence ceiling without reducing the design to one reverberation number or one absorption coefficient?

Native outputs:

- `ROOM_ACOUSTIC_STRATEGY`
- `SOURCE_RECEIVER_POSITION_MAP`
- `SURFACE_ACOUSTIC_ROLE_MAP`
- `ROOM_ACOUSTIC_MODEL_REGISTER`
- `CRITICAL_ROOM_ACOUSTIC_READBACK`

Where in claim, assess the relation among:

- room volume, geometry and coupled/connected spaces;
- source and receiver positions/states;
- reverberation/decay behavior and frequency dependence;
- speech intelligibility/clarity or musical-support requirements where relevant;
- early/late reflection behavior where method/space requires it;
- absorptive, reflective, diffusive and variable acoustic elements;
- seating/furniture/occupancy assumptions where consequential;
- HVAC/background noise and sound-system interfaces;
- large openings, operable partitions, doors and changing room states.

A material `αw`, NRC or laboratory absorption value is an **input**, not a room-result claim. A single reverberation-time figure cannot automatically close speech, privacy, noise, spatial variation or specialist performance.

**Exit ceiling:** `ROOM_ACOUSTIC_STRATEGY_COORDINATED`.

---

## 7｜ACO-SEPARATION — Airborne / Impact / Façade Separation / Flanking

**Question:** Is the required source-to-receiver sound-separation strategy resolved as a complete project assembly and junction system rather than as isolated wall/floor/door ratings?

Native outputs:

- `ACOUSTIC_SEPARATION_REQUIREMENT_MATRIX`
- `AIRBORNE_IMPACT_ASSEMBLY_REGISTER`
- `FLANKING_PATH_MAP`
- `FACADE_NOISE_INTERFACE_REGISTER`
- `OPENING_DOOR_GLAZING_PENETRATION_REGISTER`

Must distinguish:

- laboratory element/system rating from project field performance;
- direct transmission from flanking transmission;
- wall/floor/ceiling/door/glazing/roof/façade paths;
- junction and perimeter continuity;
- service penetrations, back-to-back devices, ducts, transfer paths and leakage paths;
- door undercuts/seals and operational requirements;
- raised floor, suspended ceiling, façade mullion and structural junction effects where applicable;
- impact source and floor/ceiling system conditions where impact sound is in scope;
- external noise source and façade configuration where façade acoustic performance is in claim.

`Rw / STC / laboratory rating ≠ project field isolation` unless the applicable method and complete project configuration support that transfer.

**Exit ceiling:** `ACOUSTIC_SEPARATION_COORDINATED`.

---

## 8｜ACO-NOISEVIB — Building Services Noise / Vibration / Structure-borne Interfaces

**Question:** Are mechanical/electrical/plumbing and other equipment noise/vibration sources coordinated with acoustic criteria through traceable airborne and structure-borne paths?

Native outputs:

- `MEP_ACOUSTIC_SOURCE_REGISTER`
- `NOISE_PATH_CONTROL_DIAGRAM`
- `VIBRATION_ISOLATION_INTERFACE_REGISTER`
- `DUCT_PIPE_PENETRATION_ACOUSTIC_REGISTER`
- `BACKGROUND_NOISE_PREDICTION_READBACK`

Where relevant, distinguish:

- source sound power/pressure data and its actual operating condition;
- room/background target from equipment or terminal contribution limits;
- airborne path, duct-borne path, breakout, regenerated noise and structure-borne vibration;
- plant-room construction, bases/inertia, isolators, flexible connections and penetrations;
- duct/pipe/terminal attenuation and pressure/flow consequences with MEP owner;
- control sequences, part-load/full-load/standby/emergency modes;
- lift, transformer, generator, pump, fan, drainage, AV/IT and other triggered sources;
- transient/intermittent/tonal/low-frequency conditions where material.

Acoustic coordination may define source/path/receiver criteria and interface requirements but does not self-award MEP or Structural Engineering PASS.

**Exit ceiling:** `ACOUSTIC_NOISE_VIBRATION_COORDINATED`.

---

## 9｜ACO-DETAIL — Junction / Product-System / Penetration / Installation Detail

**Question:** Do representative critical details preserve the acoustic function through complete assemblies, junctions, penetrations, seals and buildability constraints?

Native outputs:

- `CRITICAL_ACOUSTIC_DETAIL_SET`
- `ACOUSTIC_PRODUCT_SYSTEM_CONFIG_REGISTER`
- `PENETRATION_SEAL_CONTINUITY_REGISTER`
- `ACOUSTIC_TOLERANCE_INSTALLATION_REGISTER`
- `INSPECTION_ACCESS_REGISTER`

Typical critical conditions include project-relevant combinations of:

- partition head/base/end/junction;
- façade-to-partition and structure-to-partition junctions;
- wall/ceiling/floor continuity;
- doors, frames, seals, thresholds and glazing;
- operable/folding partitions;
- service penetrations and access panels;
- ducts and transfer paths;
- resilient layers, floating floors, isolators and support interfaces;
- absorptive ceilings/walls interrupted by lights, sprinklers, diffusers and access hatches;
- acoustic lining/enclosure around noisy plant or ducts;
- installation tolerances, gaps, workmanship, sequencing and inspectability.

A generic manufacturer detail or isolated product certificate cannot substitute for a project-specific complete acoustic path when configuration/material interfaces differ.

**Exit ceiling:** `ACOUSTIC_CRITICAL_DETAILS_COORDINATED`.

---

## 10｜ACO-TEST — Model / Mock-up / Field Measurement / Commissioning

**Question:** Does the verification evidence actually test or measure the declared acoustic claim under a traceable method, state and configuration?

Native outputs:

- `ACOUSTIC_TEST_MEASUREMENT_PLAN`
- `MODEL_METHOD_INPUT_REGISTER`
- `SPECIMEN_ROOM_CONFIGURATION_IDENTITY`
- `MEASUREMENT_RESULT_REGISTER`
- `FAILURE_REPAIR_RETEST_LOG`
- `UNCERTAINTY_TRANSFER_LIMIT_REGISTER`

Potential evidence, only where relevant to the claim:

- predictive room/building acoustic models;
- laboratory element/system test evidence;
- mock-up/sample testing;
- reverberation-time/room-parameter field measurement;
- airborne/impact sound-insulation field measurement;
- background-noise and equipment-noise measurement;
- vibration measurement;
- specialist functional acoustic tests.

Every result must retain method/edition, instruments/calibration where required, source/receiver positions, room/equipment state, occupancy/furnishing state where relevant, frequency treatment, corrections/averaging, sample/configuration identity, uncertainty/limitations and deviations.

A prediction is not a measurement. A laboratory rating is not field performance. A sample/one-room PASS is not a whole-building PASS.

**Exit ceiling:** `ACOUSTIC_VERIFICATION_EVIDENCE_BOUNDED`.

---

## 11｜ACO-DELIVERY — Submittal / Construction QA / Field Readback

**Question:** Does construction preserve the acoustic assemblies and paths that were actually designed and reviewed?

Native outputs:

- `ACOUSTIC_SUBMITTAL_CONFIG_REGISTER`
- `ACOUSTIC_SITE_QA_INSPECTION_REGISTER`
- `CONCEALED_ACOUSTIC_WORK_READBACK`
- `DEFECT_REPAIR_RETEST_REGISTER`
- `SUBSTITUTION_DEVIATION_REGISTER`

Track, where consequential:

- exact partition/floor/ceiling/door/glazing/lining/system build-up;
- manufacturer/product/system identity and compatible accessories;
- perimeter seals and concealed continuity;
- penetrations, boxes, access panels and late service changes;
- resilient channels/layers, isolators and bridge risks;
- plant bases, flexible connections and vibration paths;
- ceiling/absorber continuity after MEP/lighting/sprinkler coordination;
- workmanship gaps and tolerance deviations;
- substitutions/value engineering;
- pre-close inspection opportunities;
- field test failures, repair and retest.

Inspection or sample testing only supports the actually observed/tested scope.

**Exit ceiling:** `ACOUSTIC_DELIVERY_READBACK_COMPLETE` for bounded evidence obtained.

---

## 12｜ACO-INUSE — Occupied Performance / Complaints / Operational Change

**Question:** What acoustic condition is supportable in real use, and what observations require diagnosis, repair or reopen rather than immediate causal claims?

Native outputs:

- `ACOUSTIC_INUSE_STATE_REGISTER`
- `COMPLAINT_SOURCE_RECEIVER_LOG`
- `OPERATING_STATE_ACOUSTIC_READBACK`
- `ACOUSTIC_DIAGNOSTIC_HYPOTHESIS_REGISTER`
- `ACOUSTIC_CHANGE_REOPEN_LOG`

Separate:

- observed complaint/symptom;
- measured condition;
- operational state;
- candidate transmission/source cause;
- diagnostic intervention;
- repair/change;
- post-intervention verification.

Changes in occupancy, room use, partitions, doors, finishes, furniture, ceiling, floor, MEP equipment/settings, duct/pipe routing, sound systems or operating hours can invalidate previous acoustic assumptions and must reopen affected scope.

One complaint does not prove a cause; one quiet measurement does not prove universal occupied performance; one project's outcome does not become universal Knowledge without the existing R-K/G9 route.

**Exit ceiling:** `ACOUSTIC_INUSE_STATE_BOUNDED`.

---

## 13｜Cross-disciplinary interface contract

R-F remains the single integration authority.

Key interfaces include:

- **Architecture:** room geometry/volume, adjacency, openings, circulation, spatial thresholds and material intent;
- **Interior:** partitions, finishes, ceilings, doors, furniture, operable elements and use states;
- **MEP:** plant/source data, duct/pipe paths, terminals, pressure/flow constraints, vibration isolation and controls;
- **Structural:** slabs/walls/supports, structure-borne paths, bases and vibration-sensitive interfaces;
- **Facade / Envelope:** external-noise path, glazing/façade assembly and perimeter/junction interfaces;
- **FLS:** fire-rated partitions/doors/penetrations and life-safety devices, without acoustic treatment invalidating fire function;
- **Lighting / AV / Digital:** ceiling/wall penetrations, loudspeakers, sound systems and operational interfaces;
- **Accessibility / HCD:** hearing/accessibility/communication consequences where applicable, without reducing them to acoustics alone;
- **FM:** operating state, maintenance, replacement, complaints and post-occupancy readback;
- **Cost/Procurement:** acoustic option and product cost without converting commercial acceptance into technical approval.

`ACOUSTIC COORDINATION ≠ R-F INTEGRATION PASS`.

---

## 14｜Knowledge binding

Consequential acoustic Knowledge must enter through existing task/claim-scoped Operational Mount. Existing owners include, without being replaced:

- `IDX-ARCH-SPECIALTY-008` — specialty-system routing with an Acoustics track;
- existing acoustic ceiling, acoustic door and other system/product objects;
- Human-space and Building-physics Knowledge owners where task/experience/environment is involved;
- current standards/evidence-governance owners;
- project models, measurements and commissioning/site evidence.

The L4 Index remains routing Knowledge and does not become the professional process authority.

---

## 15｜Evidence ladder / fail-closed transfer

Keep separate:

`MATERIAL/PRODUCT PROPERTY → LAB ELEMENT/SYSTEM TEST → PROJECT ASSEMBLY/JUNCTION → MODEL/PREDICTION → FIELD SAMPLE/ROOM MEASUREMENT → OCCUPIED/OPERATING CONDITION`

No step automatically proves the next.

Examples:

`ABSORPTION COEFFICIENT ≠ ROOM ACOUSTIC PASS`  
`LAB RATING ≠ FIELD ISOLATION`  
`PARTITION RATING ≠ ROOM-TO-ROOM PRIVACY`  
`MODEL PASS ≠ FIELD MEASUREMENT PASS`  
`ONE ROOM PASS ≠ WHOLE BUILDING PASS`  
`MEASURED SYMPTOM ≠ CAUSE CONFIRMED`  

---

## 16｜AI boundary

AI may support:

- source/version comparison;
- source-path-receiver graphs;
- room/assembly option comparison;
- model-input and detail consistency checking;
- flanking/penetration failure seeking;
- test-plan generation;
- measured-result organization and configuration reconciliation.

AI must not:

- invent project acoustic targets or fixed values;
- invent measured acoustic results;
- infer room performance from material/product headline data;
- infer field isolation from laboratory rating alone;
- infer causal diagnosis from a complaint or one measurement;
- award acoustic, MEP, structural, FLS, statutory or field PASS;
- replace project-native editable drawings/models/calculations and actual measurement records with generated imagery.

---

## 17｜Reopen contract

Material reopen triggers include:

- use/task/occupancy/operating-state change;
- criteria, standard/method/version or acceptance-route change;
- room geometry/volume, adjacency or opening change;
- partition/floor/ceiling/door/glazing/façade build-up change;
- MEP plant/source level, routing, terminal, duct/pipe or control-state change;
- structural support/base/vibration path change;
- penetration, seal, access panel or late service change;
- absorptive/diffusive surface amount/location or furnishing state change where consequential;
- product/substitution/workmanship/configuration change;
- failed measurement/test or material complaint/defect;
- repair/operational change that invalidates prior assumptions.

Reopen affected scope and propagated dependencies only; preserve unrelated valid predecessor evidence.

---

## 18｜Completion / Promotion firewall

A process instance may close only at its declared claim ceiling when:

1. required native outputs exist;
2. consequential Knowledge mounts are valid for exact claims;
3. critical interfaces meet required R-F maturity or are explicitly outside claim;
4. relevant model/test/measurement evidence is method/configuration/state bound;
5. material open items do not contradict the claim;
6. professional review is complete for the bounded scope;
7. Independent Review is complete where adoption/promotion requires it;
8. truthful professional receipt exists.

Even then:

`ACOUSTIC PROCESS PASS ≠ ARCHITECTURE DESIGN KEEP`  
`ACOUSTIC PROCESS PASS ≠ MEP / STRUCTURAL / FLS PASS`  
`ACOUSTIC PROCESS PASS ≠ R-F INTEGRATION PASS`  
`ACOUSTIC PROCESS PASS ≠ STATUTORY APPROVAL`  
`ACOUSTIC PROCESS PASS ≠ WHOLE-BUILDING / IN-USE TRUTH`  
`ACOUSTIC PROCESS PASS ≠ CURRENT ADOPTION / PROMOTION`

---

## 19｜Current candidate state

`EV-PROF-ACOUSTICS-20260916` may enter **EV2_EVAL_READY** only after its machine definition, workflow validation hook and immutable EV2 receipt exist on the isolated branch.

Until eligible Independent Review and authorized owner-native adoption close:

**Building Acoustics remains `DOMAIN PROCESS OPEN`.**
