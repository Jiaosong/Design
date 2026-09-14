# Built-asset High-Fidelity Acceptance Extension

Status: `CURRENT CONDITIONAL WORKFLOW GATE / NO FIELD-ENGINEERING-CODE PROMOTION`

Owner: `oleander-3d-pipeline`

Use when a task asks for a **complete / realistic / high-fidelity building, spatial or infrastructure model**, when close construction inspection is part of the deliverable, or when the artifact is described as construction-aware, near-as-built or digital-twin-ready.

This extension does not create a second 3D Skill, BIM authority, engineering checker or as-built certification route. It turns “high detail” into a bounded OLEANDER acceptance contract that sits inside the existing 3D pipeline and still passes through independent Artifact Review / Professional Design Crit.

## Core separation

`VISUAL REALISM ≠ BUILT-ASSET COMPLETENESS ≠ FIELD / AS-BUILT TRUTH ≠ ENGINEERING / CODE APPROVAL`

`BIM LOD / LOI LABEL ≠ OLEANDER BUILT-ASSET ACCEPTANCE`

`OBJECT / POLYGON / MODIFIER COUNT ≠ CONSTRUCTIVE DEPTH`

`VISIBLE FASTENER ≠ STRUCTURAL CAPACITY`

`RANDOM CRACK TEXTURE ≠ OBSERVED PATHOLOGY`

External BIM LOD/LOI definitions may be mapped when the active project requires them, but they do not self-pass this gate. OLEANDER separately checks system coverage, physical relations, representation carrier, truth state and actual readback at the target inspection distance.

## BA maturity ladder

Declare one requested target before tertiary detail work:

- `BA0_MASSING` — primary volumes, voids, orientation and approximate spatial relation.
- `BA1_DESIGN` — major architectural/structural elements, openings, primary interfaces and design-scale dimensions.
- `BA2_COORDINATED_ASSEMBLY` — architecture + structure + in-scope MEP are coordinated enough for spatial, interface and clash review.
- `BA3_HIGH_FIDELITY_CONSTRUCTIVE` — decision-critical assemblies expose support, connection, fastening, edge/closure, penetration, drainage, service and maintenance logic at the required inspection distance.
- `BA4_NEAR_AS_BUILT_CANDIDATE` — BA3 plus evidence-bounded installed-condition variation, defects/aging and component/system identity sufficient for a near-as-built / digital-twin candidate review.

`BA4` is an OLEANDER review descriptor. It does **not** itself prove field verification, contractual as-built status, commissioning, code compliance, structural capacity, fabrication approval or engineering sign-off.

Detail depth is allocated by decision relevance, camera/inspection distance, system criticality and downstream use. Equal geometric density everywhere is not a quality requirement.

## System coverage matrix

Every system expected by the active task must be recorded as one of:

`MODELED / REPRESENTED / OPEN / OUT_OF_SCOPE`

and carry the applicable source/truth state. At minimum review the systems that are materially in scope:

1. **Primary structure / foundation** — columns, beams, slabs, walls, frames, foundations, bearings and transfers relevant to the claim.
2. **Envelope / roof** — wall build-up, curtain wall, subframe, joints, sealants, flashing, waterproofing, roof edges, gutters and water-shedding routes.
3. **Interior build-up** — partitions, ceilings, floors, framing/substructure, trims, reveals, access panels and junctions.
4. **Doors / windows / hardware** — frames, sills, heads/jambs, seals, hinges, locks, rails, closers and mounting relations where visible or decision-critical.
5. **Fasteners / connection hardware** — bolts, nuts, washers, screws, anchors, rivets, clips, brackets, plates, pins, clamps, hangers and equivalent parts where they explain the joint.
6. **Water supply** — mains/branches, hot/cold routes, valves, meters, pumps, fixtures, insulation, supports, sleeves and equipment interfaces as relevant.
7. **Drainage** — sanitary/waste/rainwater routes, stacks, vents, traps, drains, cleanouts, roof drainage, slope/direction, supports and discharge continuity as relevant.
8. **Electrical / low voltage** — conduit, tray, trunking, boxes, panels, switches/outlets, luminaires, equipment feeds, grounding/bonding and penetrations as relevant.
9. **HVAC / mechanical** — ducts, hydronic/refrigerant/condensate routes, terminals, dampers, equipment, flex/isolators, insulation, supports and access as relevant.
10. **Fire / life safety** — sprinkler, hydrant, detection/alarm, emergency systems, fire stopping and smoke-control elements when in scope.
11. **Site / utility interfaces** — incoming/outgoing services, drainage interfaces, external equipment and structure/site transitions when in scope.
12. **Maintenance / serviceability** — access panels, valve/panel access, filter removal, equipment replacement, door swing and maintenance routes.
13. **Defect / wear / aging** — cracks, corrosion, leakage marks, efflorescence, staining, chipped edges, sealant aging, wear, patching and installation variation when existing-condition realism is claimed.

An expected in-scope system that silently disappears is a blocker. Use `OPEN` or `OUT_OF_SCOPE` with a reason instead of hiding the omission.

## Critical-detail representation carrier

For every decision-critical detail declare the carrier:

- `GEOMETRY` — silhouette-changing parts, contact-shadow-producing parts, real supports/connections, clearances, service routes, penetrations and inspection-critical hardware.
- `DISPLACEMENT` — meso relief that changes local depth but does not own a required physical joint.
- `NORMAL_BUMP` — micro surface relief below geometric decision relevance.
- `DECAL` — labels, staining, fine surface cracking, localized wear or markings when they do not replace required physical geometry.
- `METADATA_OR_OPEN` — semantic/engineering information that matters but is not yet authoritative geometry.

Do not use a shader, normal map, decal or AI-generated image to replace a required joint, support, penetration, service route, fastener group, clearance or other physical relation.

## Connection / support continuity

At `BA3` / `BA4`, representative decision-critical assemblies must make these relations inspectable:

- what supports what;
- how parts transfer across the interface at the representational level;
- what fastens, welds, clips, seals or seats the connection;
- whether washers/nuts/gaskets/spacers/isolators/bushings are present where materially required to explain the joint;
- how repeated seams, trims, rails and service supports terminate at real edges/openings;
- how penetrations receive sleeves, closure, sealing or fire-stopping representation when applicable;
- whether pipes, ducts, trays, cables and equipment have plausible supports rather than floating;
- whether equipment/panels have plausible mounting and service interfaces.

Fastener size, spacing, grade, weld specification, anchor embedment or connection capacity may be represented only to the authority level actually available. A visible bolt is not engineering proof.

## MEP continuity / coordination / serviceability

For each in-scope routed system:

1. endpoints connect to the intended fixture, equipment or system rather than stopping in air;
2. routes do not pass through structure or another system without an explicit penetration/coordination state;
3. supports/hangers are plausible at the review level and connect to a host rather than float;
4. drainage follows a plausible gravity direction/slope and includes service/cleanout logic where the claim requires it;
5. valves, panels, filters, pumps, fan coils, access panels and equivalent service items remain reachable;
6. doors/removable panels/replacement routes do not collide with fixed equipment in the checked state;
7. required clearances are modeled, dimensioned, source-governed or explicitly `OPEN`.

`ROUTE EXISTS ≠ SYSTEM CONTINUITY PASS`.

## Material build-up / interface depth

Where the camera or decision exposes construction, do not stop at a single infinitely thin shell. Check the relevant:

- layer / thickness state;
- cavity / secondary frame / substrate;
- waterproofing / seal / gasket;
- trim / reveal / flashing / closure;
- interface gap / overlap / bearing;
- support relation and termination.

A plausible PBR shader is appearance evidence only. It does not prove wall/roof build-up, physical material specification, moisture performance or constructability.

## Defect / crack / aging truth state

Any shown crack, corrosion, stain, water mark, efflorescence, chipped edge, sealant aging, wear, patch or installation variation must use one of:

- `FIELD_OBSERVED`
- `FIELD_MEASURED`
- `SOURCE_GROUNDED`
- `INFERRED`
- `SIMULATED_CONDITION`
- `OPEN`

Rules:

- random crack/noise textures may be `SIMULATED_CONDITION` for visual/scenario realism but are never field findings by default;
- structural vs non-structural crack interpretation remains `OPEN` unless appropriate evidence / professional review supports it;
- defect location, width, severity, cause and progression must not be invented as measured facts;
- visual weathering may not hide wrong geometry, wrong scale, missing joints or procedural repetition artifacts.

## Reality without CG perfection

High-fidelity models may include bounded installation tolerance, light misalignment, joint variation, color variation, wear and repair traces. Those variations must be intentional and physically plausible.

Random transform/noise is not a substitute for evidence-bounded construction variation and cannot be used to disguise:

- wrong dimensions or scale;
- missing interfaces;
- unsupported parts;
- repetitive procedural errors;
- weak primary/secondary geometry.

## Multi-distance readback

`BA3` / `BA4` requires actual readback at three distances where the task permits:

1. `OVERALL_CONTEXT` — mass, spatial/system hierarchy and gross clashes;
2. `WORKING_HUMAN` — openings, interfaces, hardware, services, material scale and maintenance relation;
3. `INSPECTION_REPRESENTATIVE_JOINT` — fasteners, seals, terminations, penetrations, support logic, defects and service access relevant to the target.

Hidden engineering-relevant content may use reduced display LOD for performance, but it must remain modeled/semantically represented or explicitly `OPEN`. “Not visible in the hero camera” is not permission to silently omit a required system.

Readback is a repair loop:

`MODEL → OVERALL / WORKING / INSPECTION READBACK → BLOCKER / WARNING → ROOT CAUSE → SOURCE / RELATION REPAIR → RETEST`

## BA3 / BA4 hard failures

Reject the claimed level when any applicable blocker remains:

- shell + decorative detail presented as complete construction;
- floating hardware, dangling cable/pipe/rod, unsupported equipment or unexplained termination;
- seams/trims/services overrun real openings or host boundaries;
- impossible interpenetration/clash left unresolved where coordination is part of the claim;
- critical joint represented only by texture/decal while its physical relation is required;
- drainage route contradicts gravity, slope or service logic at the claimed level;
- expected in-scope architecture/structure/MEP system silently absent;
- maintenance/service access contradicted by geometry and not marked `OPEN`;
- crack/defect/aging presented as field fact without truth-state support;
- invented dimensions, grades, fastener sizes, slopes, capacities or tolerances presented as authoritative;
- beauty render, BIM/LOD label, object count, polygon count, modifier count or texture resolution used to waive any failed relation above.

## Required receipt

When this gate triggers, return a `BUILT_ASSET_FIDELITY_ACCEPTANCE_RECEIPT` with at least:

- `trigger_reason`;
- `requested_ba_target`;
- `achieved_ba_target`;
- `system_coverage_matrix`;
- `explicit_omissions_and_out_of_scope`;
- `critical_detail_carrier_matrix`;
- `connection_support_termination_checks`;
- `representative_joint_readbacks`;
- `penetration_and_service_route_readbacks_if_applicable`;
- `mep_continuity_checks_if_applicable`;
- `drainage_logic_checks_if_applicable`;
- `clash_and_clearance_checks_if_applicable`;
- `maintenance_and_service_access_checks_if_applicable`;
- `material_build_up_and_interface_checks_if_applicable`;
- `defect_aging_truth_state_ledger_if_applicable`;
- `overall_context_preview`;
- `working_human_distance_preview`;
- `inspection_distance_preview`;
- `blockers`;
- `warnings`;
- `repair_retest_record_if_needed`;
- `engineering_code_manufacturing_field_open_items`;
- `does_not_prove`.

For `BA3` / `BA4`, any unresolved hard blocker caps the achieved target below that claimed level and prevents AR-S02 Model PASS for that claim.

## Failure codes

- `FAIL_BUILT_ASSET_SYSTEM_COVERAGE`
- `FAIL_BUILT_ASSET_CONNECTION_CONTINUITY`
- `FAIL_BUILT_ASSET_MEP_CONTINUITY`
- `FAIL_BUILT_ASSET_DRAINAGE_LOGIC`
- `FAIL_BUILT_ASSET_SUPPORT_OR_CLEARANCE`
- `FAIL_BUILT_ASSET_DETAIL_CARRIER`
- `FAIL_BUILT_ASSET_DEFECT_TRUTH_STATE`
- `REVISE_BUILT_ASSET_INSPECTION_DEPTH`
- `HOLD_BUILT_ASSET_AUTHORITY_OPEN`

## Cross-owner routing

- Native geometry / Blender execution / model identity / render derivative → `oleander-3d-pipeline`.
- IFC semantic exchange → `IFC_SEMANTIC_EXCHANGE_HANDOFF_EXTENSION.md` when IFC is actually in the task.
- Functional tolerances / GD&T-GPS / metrology handoff → `FUNCTIONAL_TOLERANCE_GDNT_METROLOGY_HANDOFF_EXTENSION.md` when fit/tolerance claims require it.
- Design decision, options and project-level assumptions → `oleander-design-process`.
- Technical drawing carrier / dimensions / annotations → Technical Drawing owner/candidate route where applicable.
- Release package integrity → `oleander-delivery-qc`.
- Structural, MEP, fire, code, commissioning, survey/as-built, fabrication and field approval remain with the applicable external/project professional authority.

## Professional-source boundary

This gate may use project-selected BIM information requirements, BIMForum LOD specifications, ISO 19650 information-management requirements, buildingSMART IFC/IDS definitions, discipline codes, manufacturer data and engineering standards as sources when they actually govern the project.

OLEANDER `BA0–BA4` does not replace those external standards. It is a cross-medium acceptance descriptor used to prevent visual/detail density from being mistaken for construction/system/field truth.

## Maturity

`CURRENT CONDITIONAL WORKFLOW GATE / USER-REQUESTED OLEANDER INTEGRATION / REUSABLE REVIEW CONTRACT / ENGINEERING-CODE-MANUFACTURING-FIELD APPROVAL REMAINS EXTERNAL`.
