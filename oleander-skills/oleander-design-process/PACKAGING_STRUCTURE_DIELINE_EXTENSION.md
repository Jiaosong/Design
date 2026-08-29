# OLEANDER Packaging Structure + Dieline Extension

Status: `CANDIDATE EXTENSION / DESIGN-PROCESS`

Use when packaging form, opening, protection, assembly or panel geometry materially affects the product experience and must remain traceable into an editable dieline/production handoff. This is not a print-preflight replacement and does not certify manufacturing, transport, regulatory or supplier feasibility.

## Core contract

`PAYLOAD / PRODUCT → DISTRIBUTION + USE CONTEXT → PRODUCTION METHOD / STRUCTURE FAMILY → PANEL / CUT / CREASE / GLUE / LOCK RELATIONS → INSERT / PROTECTION / OPENING → GRAPHIC FACE ROLES → EDITABLE DIELINE → PROTOTYPE / ASSEMBLY READBACK → PRODUCTION HANDOFF`.

Packaging graphics must adapt to structural truth. A clean front panel is not allowed to erase fold, seam, opening, closure, barcode/regulatory or protection requirements that actually govern the object.

## Structural-intent gate

Before drawing a dieline, resolve:
- product/payload dimensions and which dimensions are authoritative;
- orientation, fragility, mass, contact/protection and access needs;
- distribution/storage context that materially changes structure;
- intended opening/reclosing/reuse behavior;
- production method and supplier constraints if known;
- structure family or precedent source and what is being modified.

If material thickness, clearance, board behavior, converting method or supplier limits are unknown, keep them as explicit HOLD/TEST inputs rather than importing generic external numbers.

## Dieline relation model

Represent structural semantics explicitly, with stable IDs where useful:
- panels/faces;
- trim/cut geometry;
- crease/score/fold geometry;
- glue/adhesive zones;
- lock/tuck/slot/tab relations;
- perforation/tear/opening paths;
- windows/handles/hangers where applicable;
- inserts/dividers/cradles and payload contact zones;
- seam and wrap continuity;
- production-only marks/layers separated from consumer artwork.

A line style is not enough if the semantic role is ambiguous. Preserve layer/entity identity in the editable master and in downstream exchange where the target workflow supports it.

## Structure-family use

Industry code libraries such as FEFCO may provide a shared vocabulary and starting topology for corrugated structures. They do not remove the need to verify product fit, material/process assumptions, supplier capability, assembly behavior or local regulatory requirements.

Use:
`REFERENCE STRUCTURE → VERIFIED RELATIONS → PROJECT MODIFICATION → DIFFERENCE LOG → PROTOTYPE`.

Do not redraw a coded/reference structure from memory and still claim it as that structure.

## Opening and unboxing sequence

When opening sequence matters, map:
`SEALED → FIRST CONTACT → OPENING ACTION → INTERMEDIATE REVEAL → PRODUCT ACCESS → REMOVAL → RECLOSE / DISPOSAL / REUSE`.

For each step, identify which flap, tab, tear, friction fit, insert or orientation relation enables the action. Do not add layers merely for a premium reveal if they conflict with access, damage protection, material efficiency, accessibility or production constraints.

## Graphic-face ownership

Before final artwork, classify each physical face/panel by role:
- primary identification/selection;
- product/variant differentiation;
- instruction/use;
- regulatory/mandatory information;
- secondary story/evidence;
- opening/handling cue;
- production-only area.

The roles are project-specific and can change after structure testing. Do not assume one universal “front/back/side” hierarchy for every pack format.

## Prototype and readback

At candidate stage, test at the highest fidelity available:
- flat dieline relation check;
- folded/assembled paperboard proxy or 3D fold simulation where suitable;
- payload insertion/removal path;
- closure/opening sequence;
- seam and graphic crossover behavior;
- face hierarchy in realistic orientation;
- obvious interference/collision or inaccessible glue/lock relations.

A valid PDF/SVG/DXF export is not assembly proof. A folded paper mock-up is not transport, compression, drop, seal or production proof.

## Cross-owner routing

- visual hierarchy across faces → `oleander-visual-design`;
- press/PDF/X/bleed/output-intent/preflight/proof → `oleander-delivery-qc/PRINT_PRODUCTION_PREFLIGHT_EXTENSION.md`;
- fit-critical 3D geometry or inserts → `oleander-3d-pipeline` and VALIDATION as needed;
- product affordance/serviceability → `PRODUCT_FORM_AFFORDANCE_SERVICEABILITY_EXTENSION.md` when the opening/handling relation extends beyond package structure;
- legal/regulatory/barcode/nutrition requirements → current jurisdiction/source authority, never this extension alone.

## Rejected external defaults

Do **not** promote as universal OLEANDER rules:
- fixed bleed, safety or fold offsets;
- fixed barcode quiet-zone values;
- fixed minimum type sizes;
- one rich-black build, trapping value, DPI, TAC or Delta-E tolerance;
- “always Pantone” or any single print method as default;
- fixed shelf distance/seconds or cost-per-unit claims;
- social-shareability as a packaging quality metric.

All numeric production values must come from the current printer/supplier/standard/jurisdiction or an explicit bounded test assumption.

## Required output

Return payload/context authority, structure-family/reference source, editable dieline identity, panel/cut/crease/glue/lock ledger, opening/protection sequence, graphic-face role map, prototype/readback evidence, production handoff, rejected defaults and unresolved supplier/material/regulatory/physical holds.

## Candidate boundary

This extension is independently reformulated from MIT-licensed `prone-dc302/AlterLab-FC-Skills` packaging study and cross-checked against the official FEFCO design-style code concept. It retains structural relation logic, not the source skill's fixed measurements, templates, brand language or claimed performance metrics. Real supplier/physical validation is still required.