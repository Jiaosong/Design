# Structure-to-Form Protocol v1

Status: CANDIDATE SPECIALIST EXTENSION.

Architecture binding: this protocol is an OLEANDER 3D / Modeling Contract specialization executed inside **K3 Execution Router**. It does not create a new OLEANDER Project Flow, P-level, Workstream, Validation object, system Gate or promotion state. Project mode, Decision Question, Authority, Locked/Open Variables and promotion remain owned by the existing Control Plane and Canonical Project Flow.

Use when no existing product/reference object governs the exterior, or when the task is original product development. The product must grow from functional and structural causality rather than arbitrary exterior styling.

## Specialist execution order
`S0 Intent → S1 Functional Decomposition → S2 Component Graph → S3 Interface / Motion Graph → S4 Package & Clearance → S5 Structural Topology → S6 Form Envelope → S7 Primary Surface → S8 Assembly / Manufacturing → S9 Secondary / CMF → Existing K4 Review Router`

**S0–S9 are internal specialist stage IDs only. They are not OLEANDER P0–P4 project levels, G0–G9 Gates, or project lifecycle states.** A project may iterate these stages inside either Exploration or Canonical Production as allowed by the current Project Control Card.

## Evidence classes
Every requirement or value must be classified as one of:
- `HARD_CONSTRAINT` — known dimension, interface, safety, human factor, selected component or manufacturing condition;
- `FUNCTIONAL_DECISION` — architecture chosen to make the product work;
- `DESIGN_DECISION` — proportion, curvature, visual balance, surface language;
- `ASSUMPTION` — unresolved component, supplier value, package range or engineering hypothesis.

Do not describe assumptions as engineering truth.

## S0 Product Intent
### MUST CHECK
- user/job to be done;
- operating environment;
- user/body interaction if any;
- target size/weight/cost/manufacturing class when known;
- service life / replaceability / maintenance intent;
- required deliverable level.
### EVIDENCE
`PRODUCT_INTENT_RECEIPT`.

## S1 Functional Decomposition
Break the product into verbs/functions before parts: support, contain, move, pump, sense, illuminate, cool, seal, grip, display, connect, charge, protect, etc.

### MUST CHECK
- primary function;
- support functions;
- input/output of energy, material, information and user action;
- failure-sensitive functions.
### EVIDENCE
`FUNCTION_TREE.json`.

## S2 Component Graph
Map functions to physical modules or placeholder volumes.

Each node records:
- component/module id;
- role;
- known or assumed dimensions/range;
- mass or mass range when relevant;
- heat/noise/vibration/liquid/optical concerns when relevant;
- source/confidence;
- may-move? / may-service?.

Each edge records:
- mechanical connection;
- electrical/data connection;
- airflow/fluid path;
- optical path;
- load transfer;
- user/service dependency.

### EVIDENCE
`COMPONENT_GRAPH.json`.

## S3 Interface / Motion Graph
Define relations that cannot be discovered safely after exterior surfacing:
- rotation/translation axes;
- insertion/removal vectors;
- connectors;
- human reach/touch zones;
- mating planes;
- sealing boundaries;
- vents/air paths;
- cable bends;
- access/tool corridors.

### EVIDENCE
`INTERFACE_MOTION_GRAPH.json`.

## S4 Package & Clearance
Create simplified package geometry before styling.

### MUST CHECK
- component envelopes;
- service/removal envelopes;
- tolerance/clearance assumptions;
- wall/insulation/air gaps when applicable;
- center of gravity / support polygon when relevant;
- ergonomic envelope when human-contact product;
- keep-out regions.

### FORBIDDEN
- shrinking unknown internals merely to preserve a preferred exterior;
- zero-clearance packaging without evidence;
- treating placeholder dimensions as selected production components.

### EVIDENCE
`PACKAGE_MODEL` + `PACKAGE_CLEARANCE_RECEIPT.json`.

## S5 Structural Topology
Define how the product physically stands and transfers forces before exterior finish.

Possible owners:
- monocoque shell;
- internal frame;
- base/chassis + cover;
- plate/beam/frame assembly;
- hinge/linkage;
- soft structural envelope;
- mixed topology.

### MUST CHECK
- primary load paths qualitatively or quantitatively as task requires;
- mounting references;
- joint locations;
- support/contact points;
- assembly directions;
- structural vs cosmetic parts.

### EVIDENCE
`STRUCTURAL_TOPOLOGY_RECEIPT.json`.

## S6 Form Envelope
Generate the first exterior envelope from package + structural + use constraints.

The envelope is not styling detail. It records:
- occupied volume;
- required clearances;
- access openings;
- grasp/interaction zones;
- visual/physical center of gravity;
- major silhouette and primary-volume alternatives.

Generate multiple structural layouts when there is a material design choice, e.g. vertical stack / horizontal layout / central core / distributed modules. Compare consequences before surfacing using the existing Comparison-First logic.

### EVIDENCE
`FORM_ENVELOPE_OPTIONS` + selection receipt.

## S7 Primary Surface
Only after S0–S6 are coherent, construct Source using the selected representation family.

For reflective continuous products prefer:
`feature curves / sections / boundary rails → structured cage or CAD/NURBS patches → evaluated surface`.

For rigid manufacturing-dominant products prefer datum/features/solids. For rotational products prefer profile/revolve. For mechanism products prefer skeleton/sections. For soft goods use material-behavior route.

### MUST CHECK
- primary form reads correctly without logo, detail or CMF;
- Source controls are sparse and causal;
- apertures/interfaces are integrated into topology when structurally meaningful;
- Broad / Strip / Grazing / Zebra as applicable;
- no secondary detail is used to conceal primary-form weakness.

### EVIDENCE
`PRIMARY_SURFACE_SOURCE` + diagnostics.

## S8 Assembly / Manufacturing
Translate concept geometry into an explicit construction hypothesis appropriate to the intended process.

Examples:
- injection molding: part split, wall-thickness hypothesis, draft direction, bosses/ribs/snaps, assembly vector;
- CNC: stock/access, tool-radius constraints, wall thickness, fastening;
- sheet metal: thickness, bend radius, flange/seam, unfold logic;
- cast/formed parts: draft/parting/tool access as appropriate;
- soft goods: pattern/seam/foam/textile construction.

### IMPORTANT
A visual concept may remain `DESIGN_PROPOSAL / ENGINEERING_OPEN`; do not invent production feasibility.

## S9 Secondary / CMF
Buttons, seams, lenses, fasteners, trim, graphics, micro-detail and CMF only enter after primary form and interface architecture are coherent.

## Original-design specialist review criteria
This protocol does not add a new Design Quality Gate. These criteria feed the existing **Visual QA + Project QA / Professional Design** decision in K4:
- functional legibility;
- package efficiency;
- ergonomics/interaction;
- proportion and primary hierarchy;
- structural/form coherence;
- surface continuity;
- assembly credibility;
- CMF/form relation;
- professional finish.

## Specialist FAIL / HOLD outputs
These do not bypass the Control Plane; route them through K4/K5 as applicable:
- `HOLD_FUNCTION_ARCHITECTURE_UNRESOLVED`
- `HOLD_COMPONENT_PACKAGE_UNRESOLVED`
- `FAIL_INTERFACE_CONFLICT`
- `FAIL_CLEARANCE_CONFLICT`
- `REVISE_STRUCTURAL_TOPOLOGY`
- `REVISE_PRIMARY_FORM_GENERIC`
- `STOP_DETAIL_PRIMARY_FORM_NOT_READY`
- `HOLD_ENGINEERING_PROOF_OPEN`

## Does not prove
Without corresponding engineering evidence this protocol does not prove structural safety, thermal performance, electrical safety, sealing, tooling, manufacturability, certification, cost or production readiness.
