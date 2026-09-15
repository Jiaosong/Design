# OLEANDER High-Fidelity Built-Environment Model Acceptance Gate v1.0

Status: ACTIVE
Date: 2026-09-14
Scope: Spatial / architecture / built-environment 3D models when the requested claim includes complete realistic building representation, close constructive inspection, high-fidelity realism, near-as-built, digital-twin-ready representation, or equivalent system-completeness language.

## 1｜Position in OLEANDER

This is a **specialized acceptance Gate**, not a replacement for `AR-S02｜Model Review`, `oleander-3d-pipeline`, engineering review, field verification or code approval.

**Owner boundary:** this governance file owns the cross-project acceptance meaning and claim ceiling. `oleander-skills/oleander-3d-pipeline/BUILT_ASSET_HIGH_FIDELITY_ACCEPTANCE_EXTENSION.md` is the 3D Skill execution / receipt binding for that Gate. Neither may widen the other into field, engineering, code or as-built authority.

When triggered, the canonical validation path is:

`Machine QA → Visual QA → Project QA → Built-asset High-Fidelity Gate → other applicable specialized gates → PAP when triggered → Promotion / Release`

The Built-asset High-Fidelity Gate must run before a built-environment model is described as high-fidelity complete, near-as-built or digital-twin-ready. A beauty render, high polygon count, high object count, PBR material, successful export, CI PASS or reopen PASS cannot substitute for it.

`BA3/BA4 ACCEPTANCE ≠ FIELD VERIFIED ≠ ENGINEERING APPROVED ≠ CODE COMPLIANT ≠ AS-BUILT CERTIFIED`

## 2｜Trigger

Trigger this Gate when one or more are true:

- the user/client asks for a **complete realistic building model** rather than massing or presentation shell;
- the required inspection distance exposes screws, bolts, brackets, joints, seals, pipe supports, penetrations or service interfaces;
- the model is expected to represent water supply, drainage, electrical, HVAC, fire protection or other building services as a coordinated system;
- the claim uses `BA3_HIGH_FIDELITY_CONSTRUCTIVE`, `NEAR_AS_BUILT`, `DIGITAL_TWIN_READY`, construction-detail-complete or equivalent language;
- defects, cracks, wear, corrosion, leakage traces or other existing-condition states are represented as meaningful information;
- hidden construction/service relationships are part of the decision even when they are not visible in the hero camera.

Do not trigger it merely because a simple spatial massing model is rendered attractively.

## 3｜BA maturity namespace

BA is the OLEANDER built-asset representation maturity namespace. It is independent from project-flow `FID0–FID3`, BIM LOD labels, engineering approval and field status.

| Level | Name | Minimum meaning |
|---|---|---|
| BA0 | `BA0_MASSING` | site / envelope / major volumes; no claim of construction or service completeness |
| BA1 | `BA1_DESIGN` | principal architectural components, spatial interfaces and major coordination volumes are explicit |
| BA2 | `BA2_COORDINATED_ASSEMBLY` | major build-ups, supports, interfaces, penetrations and principal service routes are represented for design review |
| BA3 | `BA3_HIGH_FIDELITY_CONSTRUCTIVE` | close-review constructive detail plus coordinated building systems, material assemblies, serviceability and bounded reality/defect layer are represented to the declared scope |
| BA4 | `BA4_NEAR_AS_BUILT_CANDIDATE` | BA3 plus source-traceable existing-condition/system identity and sufficiently explicit asset/interface state for near-as-built or digital-twin workflows; field/engineering/code claims still require their own authority |

These levels are OLEANDER review descriptors. They do **not** certify external BIM LOD, fabrication readiness, structural capacity, commissioning, regulatory compliance or field measurement.

`FID` answers how much execution/render fidelity is being spent. `BA` answers what built-environment information and constructive/system depth the underlying model actually contains. `FID3` never upgrades a model to BA3/BA4.

## 4｜Mandatory discipline matrix for BA3 / BA4

For a whole-building BA3/BA4 claim, the acceptance matrix must explicitly resolve every applicable discipline below. `N/A` is allowed only with a reason showing that the system is genuinely outside the declared building scope.

1. **Structure** — foundations, columns, beams, slabs, walls, frames, trusses and load-transfer interfaces relevant to the modeled scope.
2. **Envelope** — wall/roof build-ups, curtain wall or cladding supports, openings, flashing, waterproofing, seals, drips, terminations and weather-shedding paths.
3. **Interior build-up** — partitions, linings, ceilings, subframes, floor build-ups, trims, reveals, access panels and junctions.
4. **Fasteners / hardware / interfaces** — bolts, nuts, washers, anchors, screws, rivets, clips, brackets, cleats, plates, hangers, hinges, rails, gaskets and equivalent joining elements where they explain the assembly.
5. **Water supply** — cold/hot water mains and branches, valves, meters, pumps/filters when in scope, supports, insulation, sleeves and equipment/fixture connections.
6. **Drainage** — sanitary/waste/rain/vent systems, traps, drains, cleanouts, risers, horizontal branches, outlets, support and **gravity/slope/flow logic**.
7. **Electrical** — power and low-voltage routes, trays/conduits, panels, boxes, switches/outlets/fixtures, grounding/equipotential where relevant, equipment feeds and penetration/firestop relationships.
8. **HVAC / mechanical** — ducts, pipes/refrigerant/condensate routes, equipment, valves/dampers, terminals, supports, insulation, flexible connections and maintenance clearance where in scope.
9. **Fire protection / life-safety interfaces** — sprinkler/fire-water, detection/alarm interfaces, fire doors/curtains where modeled, smoke/exhaust interfaces, emergency systems and fire stopping at relevant penetrations.
10. **Material assemblies** — real layer order, thickness state, cavities, insulation, waterproofing, finishes, coatings/process states, joints and closure logic appropriate to the claim.
11. **Defect / aging / reality layer** — cracks, wear, impact, corrosion, staining, water marks, efflorescence, coating failure, concrete voids, sealant aging, timber/color variation or construction tolerance when the model claims existing-condition realism.
12. **Maintenance / access** — inspection panels, accessible valves/panels, equipment replacement/removal routes, tool clearance, door swing, service space, safe access and guarding when applicable.

## 5｜HFB-A01 Scope & fidelity contract

Before detailed modeling or acceptance, record:

- target `BA0–BA4`;
- whole-building vs bounded-zone scope;
- discipline matrix and explicit exclusions;
- camera / inspection distances and technical views required;
- field status;
- engineering / manufacturer / code authority status;
- what the model is allowed to prove and what it is not allowed to prove.

If the requested phrase implies BA3/BA4 but the actual scope only supports BA0–BA2, the result is `FAIL_BUILT_ASSET_SYSTEM_COVERAGE` or a downward reclassification, not a marketing-language upgrade.

## 6｜HFB-A02 Evidence and truth

Every dimension, system route, component, defect or condition that materially affects the claim must be classified as:

- `EVIDENCE` — supported by a traceable source appropriate to the claim;
- `INFERENCE` — derived from evidence by an explicit method;
- `ASSUMPTION` — reversible placeholder or bounded estimate;
- `DECISION` — design/simulation choice rather than observed fact.

Project-specific spatial evidence classes such as `FIELD_MEASURED / OFFICIAL_OR_SOURCE_GROUNDED / INFERRED / ASSUMED / DESIGN_PROPOSAL` remain valid and may be carried in parallel. The built-asset truth ledger must not widen them.

No `INFERENCE`, `ASSUMPTION` or `DECISION` may be relabeled `FIELD_OBSERVED`, `FIELD_MEASURED` or `VERIFIED` merely because the modeled result looks plausible.

For cracks and defects, distinguish at minimum:

- structural or engineering-significant crack/defect when such a classification is actually supported;
- non-structural/service/finish crack when supported;
- generic visual surface variation;
- simulated/design defect representation.

Random crack textures or procedural dirt may be used as a **visual simulation** only when labeled accordingly. They cannot serve as existing-condition evidence.

## 7｜HFB-A03 Geometry vs material / displacement / decal

Represent as **geometry** when the element materially changes any of:

- silhouette or section;
- contact / occlusion relation;
- actual component connection;
- clearance, interference or access;
- service continuity / support / penetration;
- construction joint width/depth that must be inspected;
- technical drawing or section meaning.

Normal/bump/displacement may carry micro-scale roughness, pores, machining/finish texture or other surface relief when it does not replace the required constructive relationship.

Decals may carry local staining, labels, markings and appropriately classified fine defects. A decal cannot replace a required bracket, sleeve, joint, pipe, support, penetration, seal or other physical relationship.

## 8｜HFB-A04 Constructive interface and fastener gate

Where an interface is in scope, inspect more than object presence:

- component ownership and actual contact/offset relation;
- fastener type/diameter class when known or bounded status when unknown;
- quantity and spacing logic;
- orientation and accessible installation direction;
- washer/nut/bearing/anchor/insert relation when relevant;
- embedment / penetration state when the claim depends on it;
- bracket/plate/cleat attachment to both supported and supporting elements;
- no floating hardware, disconnected rods or decorative fasteners with no assembly role;
- seams, trims, gaskets and repeated details terminate at real openings and boundaries.

Visible screws/bolts prove **assembly representation only**. They do not prove structural capacity, manufacturer compliance or fabrication approval.

## 9｜HFB-A05 Building-service continuity gate

### Water supply

Trace each required route from source/distribution to branch and terminal/equipment connection. Check valves, supports, sleeves, insulation and service access where applicable. Unsupported or floating endpoints are not complete-system evidence.

### Drainage

Trace gravity flow through the required sanitary/waste/rain/vent network. Check connection, direction, slope logic, traps/cleanouts/access and outlet/stack relationships. A visually convenient route with reverse fall, impossible gravity behavior or inaccessible maintenance is a FAIL.

### Electrical

Trace required power/low-voltage distribution to modeled loads/terminals. Check tray/conduit support, panel/box relationship, penetration/firestop relation and clashes with structure/services. Decorative cables ending in space do not pass.

### HVAC / mechanical

Trace required equipment, duct/pipe/refrigerant/condensate routes and terminals. Check supports, insulation where relevant, flexible/vibration interfaces and maintenance/replacement clearances.

### Fire protection

Trace the modeled fire/life-safety system only to the supported scope. Check service continuity and penetration/firestop relationships. Visual presence never substitutes for hydraulic, alarm, smoke-control or code engineering validation.

## 10｜HFB-A06 Coordination, clash and penetration gate

At minimum inspect:

- structure ↔ architecture;
- MEP ↔ structure;
- MEP ↔ ceiling/interior build-up;
- service ↔ service;
- door/access swing ↔ equipment/service zone;
- pipe/duct/tray support ↔ real supporting element;
- penetration ↔ sleeve / waterproofing / firestop / closure as applicable;
- drainage ↔ gravity route and clearance;
- equipment ↔ maintenance/removal envelope;
- repeated components ↔ host boundaries and openings.

Hard clashes, unsupported penetrations, impossible support relations and unmaintainable critical equipment are not averaged away by visual quality.

## 11｜HFB-A07 Material assembly and process gate

PBR appearance and physical assembly are separate states. For the claimed inspection depth, resolve:

- material identity or bounded generic class;
- layer order and thickness state;
- support/subframe relation;
- coating/finish/process state where visually or technically relevant;
- seal, gasket, flashing, waterproofing, insulation and closure logic;
- weathering/service exposure assumptions;
- mapping scale / UV / texture repetition appropriate to the camera distance.

`PBR PASS ≠ MATERIAL SPECIFICATION PASS ≠ CONSTRUCTION PASS`.

## 12｜HFB-A08 Reality / defect layer gate

Perfect CG cleanliness is not a requirement for BA3/BA4; **bounded physical irregularity** is. However, reality cannot be faked by random noise.

Review, as applicable:

- installation tolerances and slight alignment variation;
- joint-width variation within the stated evidence/assumption boundary;
- wear/contact patterns;
- corrosion/oxidation;
- stains, water traces and efflorescence;
- paint/coating damage;
- concrete pores/voids;
- aged sealant;
- material color variation;
- floor/tread wear;
- cracks with explicit evidence class.

Every defect family must state whether it is observed/sourced, inferred, assumed or intentionally simulated.

## 13｜HFB-A09 Maintenance and serviceability gate

Where systems are modeled as complete, verify the model also represents the access needed to operate them:

- valves, meters, panels and cleanouts can be reached;
- access panels correspond to the service behind them;
- filters/components can be removed where that claim matters;
- equipment has declared service/replacement clearance;
- doors/hatches can open without impossible clashes;
- maintenance paths, ladders/platforms/guarding are represented where required by the scope.

If the model intentionally omits maintenance geometry, the corresponding service-completeness claim must be lowered or kept OPEN.

## 14｜HFB-A10 Geometry and scene reality gate

Machine and visual review must identify, where applicable:

- floating components;
- disconnected service endpoints;
- unsupported fixtures/services;
- unintended mesh/solid intersections;
- coplanar z-fighting;
- zero-thickness construction where thickness is physically required;
- impossible infinitely sharp exposed edges at the target review distance;
- missing elbows/fittings/transitions;
- doors/windows not actually coordinated with host openings;
- missing sleeves/closures at penetrations;
- wrong units / implausible object scale / unintended unapplied scale;
- normals/non-manifold/topology defects that affect the deliverable;
- missing or invalid UV/material assignments;
- obvious texture scale/tiling failure;
- duplicated geometry or repeated detail escaping host bounds.

Where deterministic checking is possible, use Blender/Python/BIM/IFC or equivalent machine checks. Machine PASS remains only the machine gate.

## 15｜Camera-distance and hidden-system rule

Render fidelity may be camera-dependent; information completeness may not be.

- Hero / inspection zones may require explicit fasteners, seals, terminations and defects.
- Mid-range zones may use governed instancing/procedural detail.
- Background-only zones may use lower visual LOD when the lower detail cannot affect the stated claim.
- Hidden but engineering-/coordination-relevant systems must remain in the model/technical evidence when they are part of the requested completeness claim; they cannot disappear merely because the hero camera cannot see them.

## 16｜Required acceptance receipt

When this Gate is triggered, emit `BUILT_ASSET_FIDELITY_ACCEPTANCE_RECEIPT` containing at minimum:

- `trigger_reason`, `requested_ba_target`, `achieved_ba_target`;
- `system_coverage_matrix` with evidence state and explicit `OPEN / OUT_OF_SCOPE` reasons;
- `explicit_omissions_and_out_of_scope`;
- `critical_detail_carrier_matrix` with `GEOMETRY / DISPLACEMENT / NORMAL_BUMP / DECAL / METADATA_OR_OPEN`;
- connection/support/termination and representative-joint readbacks;
- penetration/interface, MEP continuity, drainage, clash/clearance, maintenance/service-access and material-build-up checks as applicable;
- defect/aging truth-state ledger when applicable;
- overall / working-human / inspection-distance previews;
- blockers, warnings and repair/retest record;
- engineering / code / manufacturing / field OPEN items;
- failure codes;
- `PASS / REVISE / HOLD / FAIL`;
- explicit `does_not_prove` boundary.

The canonical machine schema and fail-closed validator are `oleander-skills/oleander-3d-pipeline/contracts/BLENDER_3D_RECEIPT_SCHEMAS_v1.json` and `oleander-skills/oleander-3d-pipeline/tools/validate_receipt.py --section 07A_built_asset_fidelity`.

## 17｜Hard FAIL

The following cannot be averaged away by model complexity, render quality or documentation volume:

- required whole-building discipline/system absent under a BA3/BA4 completeness claim;
- floating or disconnected critical connection/service endpoint;
- drainage route with impossible gravity/slope logic;
- unresolved hard coordination clash that invalidates the represented assembly/system;
- critical fixture/service shown without plausible support/host relation;
- required penetration missing its applicable sleeve/closure/fire/waterproofing relation;
- inaccessible critical maintenance item when serviceability is part of the claim;
- evidence-class violation such as simulated/random crack represented as field-observed fact;
- unit/scale error or geometry-to-dimension contradiction;
- material/decal/lighting used to conceal missing required physical geometry;
- hidden required systems omitted solely because they are not visible in the final camera;
- BA3/BA4 label applied to a model whose represented depth is materially lower.

## 18｜Gate result and promotion rule

- `PASS` — the declared BA representation scope passes this Gate; external engineering/field/code states remain only as separately proven.
- `REVISE` — representation is materially incomplete or inconsistent but can be corrected without changing the declared evidence authority.
- `HOLD` — a requested claim depends on missing field/engineering/manufacturer/code authority that cannot be truthfully resolved inside the current task.
- `FAIL` — hard failure, evidence violation or declared BA mismatch.

Promotion requires this Gate only when triggered. Passing it never suppresses `AR-G01—AR-G10`, `AR-S02`, independent design review, field/engineering/code gates, or PAP when a production binary is retained.

## 19｜Canonical invariants

`HIGH OBJECT COUNT ≠ BUILDING COMPLETENESS`
`VISIBLE FASTENERS ≠ ENGINEERING CAPACITY`
`PBR REALISM ≠ MATERIAL / ASSEMBLY TRUTH`
`BEAUTY RENDER ≠ SYSTEM CONTINUITY`
`SIMULATED CRACK ≠ OBSERVED DEFECT`
`BA3/BA4 ACCEPTANCE ≠ FIELD / ENGINEERING / CODE PASS`
