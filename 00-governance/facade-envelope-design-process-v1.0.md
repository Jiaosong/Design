# OLEANDER Facade / Building Envelope Engineering Process v1.0

**Status:** CONTROLLED EVOLUTION CANDIDATE — NOT CURRENT / NOT PROFESSIONAL PASS  
**Evolution ID:** `EV-PROF-ENVELOPE-20260916`  
**Authority baseline:** `OLEANDER_CURRENT_ARCHITECTURE_MAP_v2.1` + `professional-domain-process-contract-v1.0.md`  
**Knowledge position:** consumes existing OLEANDER Material–System–Interface and façade/envelope Knowledge owners; does not create a second Knowledge authority.  
**Integration position:** all cross-domain interface truth remains owned by Current R-F Cross-Disciplinary Integration.  

---

## 1｜Purpose

This candidate defines a domain-native professional process for **Facade / Building Envelope Engineering** without renaming Architecture `ADD-*`, without turning material/product pages into engineering authority, and without treating one calculation, mock-up, test report or manufacturer system page as proof of the complete installed envelope.

The process carries the envelope from performance basis through system definition, building-physics and movement engineering, fire interfaces, detailed junctions/tolerances, representative mock-up/testing, fabrication/site quality readback and in-use return.

The governing professional relation is:

`PROJECT / EXPOSURE / AUTHORITY → PERFORMANCE BRIEF → SYSTEM / ZONE STRATEGY → PHYSICS + LOAD / MOVEMENT + FIRE → DETAIL / INTERFACE / TOLERANCE → MOCK-UP / TEST → FABRICATION / INSTALLATION / QA → HANDOVER / MAINTENANCE / IN-USE → CHANGE / REOPEN`

This is **not** a universal procurement sequence and does not imply that every project uses the same façade type, responsibility split or testing regime.

---

## 2｜Professional basis and bounded transfer

Current external professional context used by this candidate includes:

- **ISO/TR 5863:2025 — Integrative design of the building envelope — General principles**: integrative envelope design across thermal performance, daylight/visual environment, ventilation, airtightness, watertightness, moisture, sound and sustainability/technical-system integration.
- **ISO 12631:2017 — Thermal performance of curtain walling — Calculation of thermal transmittance**: current confirmed calculation context for curtain-wall thermal transmittance; its stated exclusions remain exclusions and cannot be silently filled by the model.
- **ISO 24084:2022 — Curtain walling — Inter-storey displacement resistance — Test method**: movement-resistance test context where inter-storey displacement is a design requirement.
- **Society of Façade Engineering / CIBSE**: façade engineering is a specialist multidisciplinary field linking architects, façade engineers, building-services engineers, structural engineers, contractors and other actors across design, supply, installation, testing and operation.
- applicable project jurisdiction, fire/building regulations, structural/loading basis, energy/thermal/moisture requirements, product/system standards, manufacturer data and project-specific tests remain controlling only within their actual applicability.

These sources do **not** create universal project values. Wind pressure, movement, U-value, condensation criteria, air/water pressure, glass build-up, anchor capacity, sealant bite, cavity/fire performance, panel dimensions, test pressure and sampling frequency remain project/source/configuration dependent.

---

## 3｜Scope

### In scope

- façade/envelope appointment, authority, exposure and claim ceiling;
- performance brief and acceptance matrix;
- façade/envelope system zoning and typology selection;
- curtain wall, window wall, windows/doors, rainscreen/cladding and opaque wall interfaces where included in appointment;
- thermal, solar/daylight interface, airtightness, water management, moisture/condensation and acoustic interfaces;
- wind/self-weight/seismic/movement load path and structural support/anchor interfaces;
- perimeter fire, cavity/barrier, spandrel/backpan and opening/penetration fire interfaces where triggered;
- joints, drainage, membranes, sealants, gaskets, insulation continuity, thermal bridges, transitions and tolerances;
- maintainability, access, replacement and cleaning consequences;
- representative mock-up, laboratory/site performance testing where required;
- fabrication/submittal/production/installation QA and field readback;
- handover, inspection/maintenance and in-use defect/change return.

### Outside this process authority

- Architecture Design KEEP or aesthetic authority;
- Structural Engineering member/global-structure approval;
- Fire / Life Safety statutory or professional approval;
- MEP/HVAC design approval;
- detailed acoustic professional approval outside envelope interface scope;
- statutory approval, AHJ acceptance or licensed sign-off outside appointment;
- procurement/commercial approval merely because a product or system is technically described;
- R-F Integration PASS;
- field truth inferred from models, product pages or a single successful mock-up;
- project Promotion.

---

## 4｜Native professional carriers

The candidate preserves domain-native carriers:

`ENV-BASIS → ENV-CONCEPT → ENV-PHYSICS → ENV-MOVEMENT → ENV-FIRE → ENV-DETAIL → ENV-MOCKUP → ENV-DELIVERY → ENV-INUSE`

These are OLEANDER carriers for this candidate, not ISO/CWCT/SFE stage numbers and not Architecture stage aliases.

---

## 5｜ENV-BASIS — Authority / Exposure / Performance Basis

**Question:** What envelope claim is in scope, under which project/jurisdiction/appointment basis, against which environmental exposures and performance objectives?

Required native outputs:

- `ENVELOPE_AUTHORITY_SCOPE_REGISTER`
- `EXPOSURE_DESIGN_BASIS`
- `ENVELOPE_PERFORMANCE_BRIEF`
- `OPEN_SOURCE_ASSUMPTION_REGISTER`

Must establish at minimum:

- climate/exposure and orientation basis;
- applicable codes/standards/source editions and project-specific requirements;
- façade/envelope responsibility split and design-assist/delegated-design boundaries where relevant;
- architectural geometry/aesthetic intent as an input, not an engineering conclusion;
- structural support/movement basis status;
- thermal/moisture/air/water/acoustic/fire/maintenance performance categories actually in claim;
- required calculations, mock-ups, tests, reviews and authority routes at the current claim ceiling.

**Exit ceiling:** `ENVELOPE_BASIS_RESOLVED`.

Does not prove performance, product suitability, constructability or statutory approval.

---

## 6｜ENV-CONCEPT — System zoning / typology / load-and-water-path concept

**Question:** Which envelope system families and zones can credibly satisfy the performance brief and project geometry without hiding incompatible interfaces?

Native outputs:

- `ENVELOPE_ZONE_SYSTEM_MAP`
- `SYSTEM_OPTION_COMPARISON`
- `PRIMARY_LOAD_WATER_AIR_THERMAL_PATH_DIAGRAM`
- `CRITICAL_TRANSITION_REGISTER`

The concept must distinguish, where applicable:

- unitized / stick / window-wall / punched-window / rainscreen / opaque-wall / lightweight-special-system logic;
- drained/ventilated cavities versus sealed/barrier approaches;
- primary/secondary water management and pressure-equalization assumptions;
- operable versus fixed elements;
- glazing / opaque / spandrel / backpan / insulation / membrane / support layers;
- building corners, bases, parapets, roofs, terraces, entrances and other transitions;
- maintainability and replacement implications.

A preferred architectural appearance does not close the engineering option comparison.

**Exit ceiling:** `ENVELOPE_SYSTEM_CONCEPT_DEFINED`.

---

## 7｜ENV-PHYSICS — Thermal / air / water / moisture / daylight-acoustic interfaces

**Question:** Are the envelope's declared building-physics functions translated into an internally consistent system with traceable assumptions and failure paths?

Native outputs:

- `ENVELOPE_PHYSICS_MODEL_REGISTER`
- `THERMAL_BRIDGE_CONTINUITY_MAP`
- `AIR_WATER_MOISTURE_CONTROL_LAYER_MAP`
- `CONDENSATION_RISK_REGISTER`
- `DAYLIGHT_SOLAR_ACOUSTIC_INTERFACE_REGISTER`

Required checks include, where in claim:

- centre-of-system and junction thermal effects;
- frame/panel/glazing interfaces and thermal breaks;
- air-barrier continuity;
- external and internal water paths, drainage, weeps and recoverability;
- vapour/moisture migration and condensation risk at actual layer sequence;
- solar/daylight and visual consequences where envelope configuration controls them;
- acoustic source/receiver and flanking implications where envelope performance is material;
- HVAC/natural-ventilation interface assumptions where openings or façade controls participate.

`ISO 12631`-type thermal calculation does not close solar, leakage, condensation, corners/edges or structure-fixing effects that are outside that method's scope.

**Exit ceiling:** `ENVELOPE_PHYSICS_COORDINATED`.

---

## 8｜ENV-MOVEMENT — Loads / support / anchors / movement accommodation

**Question:** Can the envelope transfer declared loads and accommodate building, component and joint movement through a traceable support path without hidden incompatibility?

Native outputs:

- `ENVELOPE_LOAD_MOVEMENT_BASIS`
- `SUPPORT_ANCHOR_INTERFACE_REGISTER`
- `MOVEMENT_ACCOMMODATION_DIAGRAM`
- `CRITICAL_GLASS_PANEL_SUPPORT_CHECK_REGISTER`

Must separate:

- project wind/seismic/self-weight/maintenance loads from generic product ratings;
- global structural movements from local façade movements;
- inter-storey drift, slab edge movement, thermal expansion, creep/shrinkage and construction tolerance where applicable;
- bracket/anchor/subframe capacity responsibility from main-structure responsibility;
- glass/panel edge/support assumptions from final engineering verification;
- movement capability of sealants, gaskets, joints and firestops from nominal joint geometry.

`ISO 24084`-type repeated movement testing is evidence for the tested configuration and imposed displacement regime, not automatic proof of every project detail.

**Exit ceiling:** `ENVELOPE_MOVEMENT_COORDINATED`.

---

## 9｜ENV-FIRE — Fire / cavity / perimeter / opening interfaces

**Question:** Are triggered façade fire functions and interfaces represented as complete configuration-specific assemblies rather than material-property shortcuts?

Native outputs:

- `ENVELOPE_FIRE_INTERFACE_REGISTER`
- `PERIMETER_CAVITY_BARRIER_MAP`
- `SPANDREL_BACKPAN_FIRE_CONTINUITY_DETAIL_SET`
- `FIRE_EVIDENCE_CONFIGURATION_MATRIX`

Must distinguish:

- material reaction-to-fire evidence;
- assembly/system fire-resistance or propagation evidence;
- perimeter firestop/cavity barrier configuration;
- slab edge / curtain-wall / backpan / insulation / membrane / fixing relation;
- openings, penetrations, louvers and interfaces with MEP/FLS;
- tested/assessed configuration versus project variation;
- design-stage engineering coordination versus installed inspection/acceptance.

FLS retains life-safety/statutory authority. A façade professional process may coordinate and specify envelope interfaces but may not award FLS PASS.

**Exit ceiling:** `ENVELOPE_FIRE_INTERFACES_COORDINATED`.

---

## 10｜ENV-DETAIL — Junction / tolerance / fabrication / maintenance detail

**Question:** Do representative critical details preserve all required control layers and movement/installation/maintenance logic simultaneously?

Native outputs:

- `CRITICAL_ENVELOPE_DETAIL_SET`
- `JOINT_SEALANT_GASKET_REGISTER`
- `TOLERANCE_STACK_REGISTER`
- `INSTALLATION_SEQUENCE_READBACK`
- `MAINTENANCE_REPLACEMENT_ACCESS_MAP`

Critical details include project-relevant combinations of:

- base / sill / head / jamb / corner;
- slab edge / spandrel / backpan;
- parapet / roof / terrace transition;
- entrance / canopy / louver / service penetration;
- opaque-to-glazed and system-to-system transitions;
- drainage paths and compartmented cavities;
- membranes, flashings, terminations, sealants and gaskets;
- brackets/anchors/subframes and tolerance adjustment;
- access for inspection, cleaning, repair and replacement.

A rendered section or generic manufacturer detail is not sufficient when the project geometry/configuration is materially different.

**Exit ceiling:** `ENVELOPE_CRITICAL_DETAILS_COORDINATED`.

---

## 11｜ENV-MOCKUP — Representative prototype / performance testing / failure readback

**Question:** Has the project used a representative test/prototype strategy where the claim requires physical proof, and has failure been converted into bounded design change rather than hidden?

Native outputs:

- `ENVELOPE_MOCKUP_TEST_PLAN`
- `SPECIMEN_CONFIGURATION_IDENTITY`
- `TEST_SEQUENCE_AND_ACCEPTANCE_REGISTER`
- `FAILURE_REPAIR_RETEST_LOG`
- `TRANSFER_LIMIT_REGISTER`

Possible evidence includes, only when required by project/authority/appointment:

- visual/design mock-up;
- laboratory performance mock-up;
- air/water/structural/movement testing;
- field water/air tests;
- adhesion/compatibility tests;
- thermal/acoustic/fire testing or assessment by the relevant authority route.

Every physical result must record specimen identity, geometry, products, interfaces, installation method, test method/version, preconditioning, sequence, modifications and transfer limits.

`MOCKUP PASS ≠ PRODUCTION PASS ≠ INSTALLED BUILDING PASS`.

**Exit ceiling:** `ENVELOPE_TEST_EVIDENCE_BOUNDED`.

---

## 12｜ENV-DELIVERY — Submittal / fabrication / installation / QA / field readback

**Question:** Does the delivered envelope preserve the approved design configuration through fabrication and installation, with deviations and substitutions explicitly controlled?

Native outputs:

- `ENVELOPE_SUBMITTAL_CONFIG_REGISTER`
- `FABRICATION_QA_REGISTER`
- `INSTALLATION_INSPECTION_REGISTER`
- `FIELD_TEST_READBACK`
- `DEVIATION_SUBSTITUTION_REGISTER`

Must track:

- shop/fabrication drawing responsibility and revision;
- exact product/system/plant/batch where consequential;
- glass/panel/unit identification where required;
- sealant/gasket/adhesive compatibility and process controls;
- anchorage/fixing installation and substrate condition;
- membranes/flashings/drainage/firestop continuity;
- protection, storage, transport and installation sequence;
- site tolerance and adjustment;
- field tests, defects, repair and retest;
- substitutions and value-engineering consequences.

A shop drawing approval stamp does not automatically prove engineering adequacy, fabrication conformity, installation quality or field performance.

**Exit ceiling:** `ENVELOPE_DELIVERY_READBACK_COMPLETE` for the bounded evidence actually obtained.

---

## 13｜ENV-INUSE — Handover / maintenance / defects / adaptation

**Question:** What envelope condition is actually supportable after handover, and what in-use evidence reopens the design or knowledge route?

Native outputs:

- `ENVELOPE_HANDOVER_ASBUILT_REGISTER`
- `MAINTENANCE_INSPECTION_PLAN`
- `DEFECT_WATER_AIR_THERMAL_RETURN_LOG`
- `REPLACEMENT_COMPATIBILITY_REGISTER`
- `ENVELOPE_CHANGE_REOPEN_LOG`

Track at minimum:

- as-built configuration identity where available;
- access/inspection/cleaning/repair strategy;
- sealant/gasket/coating and drainage maintenance dependencies;
- glass/panel/unit replacement constraints;
- leakage, condensation, thermal discomfort, noise, movement, breakage, corrosion, delamination, fire-interface and other observed defects;
- changes in adjacent systems or building operation that affect envelope assumptions.

Observed performance can reopen project design and bounded R-K/G9 knowledge candidates, but one project's success/failure does not become universal rule without the existing Knowledge authority route.

**Exit ceiling:** `ENVELOPE_INUSE_STATE_BOUNDED`.

---

## 14｜Cross-disciplinary interface contract

R-F remains the single integration authority. This process may originate or consume façade/envelope interface records but cannot self-award closure of another profession.

Key interfaces include:

- **Architecture:** geometry, appearance, openings, spatial thresholds, maintainability consequences;
- **Structural Engineering:** support points, slab edges, movement, anchors, load transfer, tolerances;
- **MEP:** louvers, ventilation, penetrations, condensate/drainage, controls, plant/access;
- **Fire / Life Safety:** perimeter fire, cavity barriers, spandrels, opening/protection interfaces;
- **Accessibility:** thresholds, doors, controls, visibility and safe approach/use;
- **Lighting / Daylight:** glazing/shading/visual performance and façade-mounted equipment;
- **Acoustics:** external noise insulation and flanking paths;
- **Interior:** perimeter conditions, blinds, finishes and access;
- **Landscape/Site/Civil:** ground interfaces, splash/drainage/exposure and entrance transitions;
- **FM:** cleaning, inspection, replacement, BMU/access and defects;
- **Cost/Procurement:** option cost and supply route, without converting cost approval into technical approval.

`ENVELOPE COORDINATION ≠ R-F INTEGRATION PASS`.

---

## 15｜Knowledge binding

Consequential envelope knowledge must enter through the existing task/claim-scoped Operational Mount. Existing owners include, without being replaced:

- `FW-ARCH-MATERIAL-SYSTEM-001` — Material–System–Interface framework;
- existing façade/curtain-wall, glazing, insulation, firestop, sealant and special-envelope system objects;
- current code/evidence-governance owners;
- project-specific test, product, fabrication and site evidence.

No material/system object becomes professional process authority because it is referenced here.

---

## 16｜Evidence ladder and reality boundary

Keep separate:

- analytical/model evidence;
- product/component evidence;
- assembly/system evidence;
- representative mock-up/test evidence;
- production/fabrication evidence;
- installed/site evidence;
- in-use observed evidence.

The process must never silently promote evidence upward across these levels.

Examples:

`PRODUCT TDS ≠ ASSEMBLY PASS`  
`ASSEMBLY TEST ≠ PROJECT CONFIGURATION PASS`  
`PROJECT MOCKUP PASS ≠ ALL PRODUCTION UNITS PASS`  
`FIELD SAMPLE PASS ≠ COMPLETE BUILDING PASS`  
`MODEL PASS ≠ FIELD TRUTH`  

---

## 17｜AI boundary

AI may support:

- source/version comparison;
- layer/interface graphs;
- option comparisons;
- thermal/junction/test-variable checking;
- FMEA and failure-seeking;
- document/configuration comparison;
- submittal/test/site-readback reconciliation.

AI must not:

- invent wind, thermal, fire, anchor, glass, joint or test values;
- infer project approval from a manufacturer page;
- infer full-system performance from one component;
- infer as-built condition from design intent;
- declare façade engineering, FLS, structural, statutory or field PASS without the required professional evidence/authority;
- replace exact native editable drawings/models/calculations/test records with generated imagery.

---

## 18｜Reopen contract

Material reopen triggers include:

- project/jurisdiction/source change;
- geometry, orientation, exposure or use change;
- façade system/zone change;
- support, movement or tolerance change;
- glazing/panel/insulation/membrane/sealant/gasket/anchor/firestop substitution;
- opening/louver/penetration/control change;
- test specimen/configuration or acceptance change;
- failed mock-up/field test;
- fabrication/installation deviation;
- in-use leakage, condensation, breakage, movement, fire-interface or maintenance failure;
- adjacent structural/MEP/FLS/Architecture change that alters the interface contract.

Reopen only the affected scope plus propagated dependencies; do not erase valid unrelated work.

---

## 19｜Completion / promotion firewall

A candidate process instance may only close at its declared claim ceiling when:

1. required native outputs exist;
2. consequential Knowledge mounts are valid for the exact claim;
3. critical interfaces have the required R-F maturity/disposition;
4. declared analyses/tests/readbacks exist at the required evidence level;
5. material unresolved items do not contradict the claim;
6. professional review is complete for the bounded scope;
7. Independent Review requirements are satisfied where promotion/adoption requires them;
8. a truthful professional receipt exists.

Even then:

`PROCESS PASS ≠ ARCHITECTURE DESIGN KEEP`  
`PROCESS PASS ≠ R-F INTEGRATION PASS`  
`PROCESS PASS ≠ STATUTORY APPROVAL`  
`PROCESS PASS ≠ FIELD / IN-USE TRUTH`  
`PROCESS PASS ≠ CURRENT ADOPTION / PROMOTION`

---

## 20｜Current candidate state

`EV-PROF-ENVELOPE-20260916` begins at **EV2_EVAL_READY** only after its machine definition, workflow validation hook and EV2 receipt exist and are read back under the frozen Current authority baseline.

Until eligible Independent Review and authorized owner-native adoption close:

**Facade / Building Envelope Engineering remains `DOMAIN PROCESS OPEN`.**

---

## 2026-09-19｜Execution Binding Contract｜Facade / Building Envelope professional-depth parity

**Candidate boundary:** additive parity repair only. v001 Independent Review remains bound to the earlier EV3 professional input and does not review this later head.

### Knowledge / owner routing
- Existing material/envelope framework + exact system/product/source objects remain knowledge owners.
- `oleander-research` supports source/product/test evidence; `oleander-design-process` supports system options, interface/change reasoning.
- `oleander-3d-pipeline` may support geometry/exchange; `oleander-technical-drawing` remains candidate-only; `oleander-delivery-qc` is package integrity only.
- Facade engineer, building-physics specialist, structural/FLS domain owners, laboratory/mockup/test provider and site QA authority are `PROJECT_SPECIALIST_REQUIRED` where the claim requires them.

### Required native carriers
Exposure/performance basis；system zoning/typology；control-layer continuity；opening/junction/transition details；support/anchor/movement；thermal/air/water/moisture analysis；submittal/substitution；mockup/test；fabrication/site QA；maintenance/defect/in-use return。

### Object-level invocation matrix
#### A｜Basis / exposure / system zoning
Tool: project climate/exposure + system register. Readback: orientation/exposure/performance target and exact system zone. Reopen: climate/exposure/geometry/performance/system change.
#### B｜Control layers / junctions / drainage
Tool: editable detail/control-layer carrier. Readback: wall-window-roof-base air/water/thermal/moisture continuity, drainage/weep path and transition logic. Reopen: opening/detail/membrane/seal/gasket/insulation/firestop change.
#### C｜Support / movement / tolerance
Tool: structural interface + anchor/joint/tolerance carrier. Readback: load path, movement accommodation, install tolerance and adjacent-system compatibility. Reopen: structure/anchor/panel/module/movement/tolerance change.
#### D｜Analysis / mockup / testing
Tool: project-authorized thermal/moisture/daylight/air-water analysis and mockup/test records. Readback: method/version/input/specimen/configuration + failure mode + repair/retest. Reopen: model/input/specimen/system/test failure change.
#### E｜Fabrication / installation / in-use
Tool: shop/fabrication/site QA + field-test + maintenance/defect records. Readback: exact installed configuration and site deviation. Reopen: substitution/fabrication/site deviation/leak/condensation/maintenance defect.

### Boundary
`COMPONENT EVIDENCE ≠ ASSEMBLY PASS`；`ASSEMBLY TEST ≠ PROJECT CONFIGURATION PASS`；`MOCKUP PASS ≠ PRODUCTION PASS`；`MODEL PASS ≠ FIELD TRUTH`；Envelope coordination ≠ R-F Integration PASS.
