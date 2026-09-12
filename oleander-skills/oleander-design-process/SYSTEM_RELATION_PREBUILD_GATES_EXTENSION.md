# OLEANDER Design Process｜System Relation Prebuild Gates Extension

Status: `OWNER-LOCAL EXTENSION / ACTIVE WITH oleander-design-process / CURRENT KNOWLEDGE FIRST / NO NEW SKILL`

Purpose: prevent high-fidelity geometry, constructive detail, CMF or presentation polish from advancing before the system relations that make the design usable and coherent have been made explicit and tested. This extension governs **design relation eligibility**; it does not replace engineering, code, ergonomics, manufacturing or field authority.

## 0｜Trigger

Use this extension when a design contains one or more materially coupled physical or system relations, including circulation/entry/exit, stairs/platforms/headroom, body/path/object relation, host/attached-part relation, support/fastening/sealing/drainage/service relation, moving envelopes, host-driven procedural geometry, or multiple subsystems whose local geometry can look plausible while the combined relation can still fail.

Do **not** use this extension to invent specialist numeric requirements. Resolve Current Knowledge / Project Source Authority / specialist authority first. Unknown technical values remain `OPEN / HOLD` and are not replaced by generic external numbers.

## 1｜Canonical order

For triggered work:

`AUTHORITY → HARD CONSTRAINTS → SYSTEM TOPOLOGY → CLEARANCE / ENVELOPE → INTERFACE GRAPH → GEOMETRY → CONSTRUCTIVE DETAIL → MATERIAL / CMF → READBACK`

Not:

`GEOMETRY → DETAIL → MATERIAL → READBACK → DISCOVER TOPOLOGY / CLEARANCE / INTERFACE FAILURE`.

High fidelity cannot compensate for an unresolved upstream relation.

## 2｜System Topology Gate

Before detail-bearing geometry, record:

`ACTOR / USE SEQUENCE / SYSTEM NODES / REQUIRED CONNECTIONS / ENTRY / EXIT / RETURN / FORBIDDEN COLLISIONS / OPEN INTERFACES`.

Answer who/what acts on the system, what sequence must remain possible, which objects must connect, which topology relations are invariant, and which collisions/dead ends/blocked egresses/disconnected states are forbidden.

Gate result:

- `PASS` — topology is explicit enough to test the selected direction;
- `REVISE` — topology is contradictory or the selected form breaks it;
- `HOLD` — required authority is unavailable and guessing would corrupt the design.

`TOPOLOGY REVISE/HOLD → DETAIL LOCKED`.

## 3｜Spatial Clearance / Envelope Gate

Before repetitive or high-cost detail generation, identify and read back all clearances/envelopes that can invalidate the system, as applicable: circulation/egress, headroom, reach/operation, maintenance/replacement access, open/close swept envelope, body/path/structure collision, stair/platform/guard/roof relation, assembly/disassembly path and service/tool access.

Use current project/specialist authority for numeric acceptance values. When numeric authority is unavailable, preserve the relation and test direction without fabricating a threshold.

Required readback:

`REQUIREMENT / AUTHORITY → TEST LOCATION OR ENVELOPE → ACTUAL OBSERVATION / MEASUREMENT → PASS / REVISE / HOLD → DESIGN CONSEQUENCE`.

Hard rule:

`CLEARANCE UNKNOWN, REVISE OR HOLD → DOWNSTREAM DETAIL THAT DEPENDS ON THAT CLEARANCE IS NOT ELIGIBLE`.

## 4｜Interface Graph Gate

Every material object/subsystem that depends on another object must answer:

`THIS OBJECT → CONNECTS TO WHAT → THROUGH WHAT INTERFACE → SUPPORTED / LOCATED / SEALED / DRAINED / SERVICED HOW`.

The graph/ledger must expose host/dependent object, interface type, support/location logic, sealing/drainage when applicable, operation/service/removal relation, authority state, unresolved specialist hold and dependency direction.

Direct `REVISE` signals include floating elements, terminals ending in air, fasteners/brackets without a valid host, platforms blocking their own egress, clamps/fixings penetrating the wrong host relation, drainage elements without a target, or details driven by an obsolete/approximate host when authoritative host geometry exists.

The interface diagram itself is not PASS. The actual design artifact must be read back against it.

## 5｜Detail Eligibility Gate

Before generating or polishing repetitive/detail-scale elements such as bolts, washers, pins, trim, flashing, seals, seams, secondary rails, cleats, micro-material, texture, repeated brackets/balusters/supports, record:

`SYSTEM TOPOLOGY STATE / CLEARANCE STATE / INTERFACE STATE / SOURCE AUTHORITY STATE / ROUTE STATE → DETAIL_ELIGIBILITY`.

Allowed states:

- `ELIGIBLE` — all upstream design relations required by this detail are `PASS`;
- `PARTIAL` — bounded detail proceeds only in explicitly isolated passed zones;
- `LOCKED` — any required upstream relation is `REVISE / HOLD / STALE / UNKNOWN`.

Canonical rule:

`SYSTEM RELATION PASS → DETAIL ELIGIBLE`.

Never use `MORE DETAIL → LOOKS PROFESSIONAL` as a substitute for relation proof.

## 6｜Constructive Representation Gate

Representation type must follow constructive role strongly enough to avoid false physical cues. Distinguish, when relevant, round tube/rod/cable, flat bar, folded sheet, standing seam, gutter/channel, flashing, curb, gasket/seal, plate, bracket/cleat and rail.

DESIGN proves role and relation. Section sizing, grade, fastener capacity, structural adequacy, manufacturing tolerance and code compliance remain with Current Knowledge / specialist authority.

`CONVINCING SHAPE ≠ CONSTRUCTIVE ROLE TRUTH ≠ ENGINEERING VALIDATION`.

## 7｜Source Change Dependency Invalidation Gate

When an upstream source changes materially, dependent details cannot silently remain Current. Triggers include authoritative host surface, topology/route, opening/boundary, stair/platform/circulation relation, geometry master, interface location/ownership, or a source dimension/datum that drives dependent geometry.

Classify dependents as:

`CURRENT / STALE / REGEN_REQUIRED / RETEST_REQUIRED / SUPERSEDED`.

Then record:

`SOURCE CHANGE → DEPENDENT OBJECTS → INVALIDATION STATE → REGEN / REBIND ACTION → ACTUAL READBACK → RESULT`.

A downstream object that still renders is not evidence that its dependency remains valid.

## 8｜PREBUILD_SYSTEM_RELATION_GATE output

When triggered, preserve one human/machine-readable gate record with at least:

- `decision_object`
- `locked_variables`
- `open_variables`
- `system_topology_state`
- `system_nodes_and_required_connections`
- `clearance_requirements`
- `clearance_readback`
- `interface_graph`
- `support_service_relations`
- `source_authority_state`
- `detail_eligibility`
- `unresolved_specialist_holds`
- `dependent_artifacts`
- `invalidation_triggers`
- `result = PASS / REVISE / HOLD`

This is a design gate, not a construction approval record.

## 9｜Repair routing

Reopen the earliest causal layer:

- hard constraint failure → requirement/authority;
- topology failure → system topology/route;
- clearance failure → spatial relation/geometry layout;
- interface failure → host/dependency/interface graph;
- dependency failure → source/invalidation/regeneration;
- representation failure → constructive role mapping;
- specialist numeric/physical validity failure → specialist Validation owner.

Do not repair an upstream relation failure by adding local detail.

## 10｜Boundary

This extension does not prove code compliance, engineering capacity/structural safety, universal ergonomic dimensions, field measurement truth, manufacturing readiness, construction issue status, or Design KEEP merely because the prebuild gate passed.

It exists to ensure the selected design is **eligible to become detailed** before detail generation consumes time and hides upstream failure.
