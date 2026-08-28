# OLEANDER Physical Product Phase Gates Extension

Status: `CANDIDATE EXTENSION / DESIGN-PROCESS`

Use when developing a physical product whose visual form depends on internal payload, ergonomics, mechanisms, assembly interfaces, manufacturing logic or CMF. This is a conditional product-design route, not a mandatory linear sequence for every object.

## Core principle

`VISUAL FINISH MUST NOT OUTRUN FUNCTIONAL RESOLUTION`.

High-fidelity rendering can make an unresolved object look falsely complete. Increase visual fidelity only when the design questions appropriate to that fidelity have been answered or explicitly held open.

## Adaptive phase model

Resolve only the phases required by the actual product:

`BRIEF / SOURCE AUTHORITY → FUNCTION + ENVELOPE → DIVERGENT FORM OPTIONS → PROPORTION / ORTHOGRAPHIC CHECK → PAYLOAD / CAVITY / HUMAN INTERFACE → MECHANISM / ASSEMBLY INTERFACE WHEN APPLICABLE → NEUTRAL FORM READBACK → CMF → CONTEXT / HERO PRESENTATION → VALIDATION HANDOFF`.

A simple solid object may not need a cavity or mechanism phase. A powered, wearable, opening, folding, dispensing, docking or transformable product usually does.

## Gate 0 — brief / decision authority

Record:

- problem and user/context;
- primary function and required interactions;
- hard envelope or spatial constraints;
- known payload/components;
- target use environment;
- manufacturing/price/service/lifecycle constraints when known;
- source references and what relation each reference is meant to inform;
- success criteria and unresolved assumptions.

Style/CMF preferences may be recorded early, but they must not silently determine geometry before functional constraints are understood.

## Gate 1 — divergence before premature lock

Generate genuinely different form relations when the design problem is still open. Diversity should attack meaningful variables such as:

- stance / footprint / orientation;
- volume distribution;
- symmetry/asymmetry;
- opening/interaction direction;
- support/contact relation;
- component/payload organization;
- silhouette and visual mass.

Do not satisfy divergence by changing only color, fillet radius, decorative seams or camera angle.

Use the minimum number of options needed to expose the real trade-off. A fixed sketch quota is not an OLEANDER rule.

## Gate 2 — proportion and neutral-form check

Before CMF or context render carries the judgment, inspect form in a representation that exposes proportion and geometry rather than hiding it with material/lighting.

Possible evidence:

- orthographic/front/side/top views;
- clean linework;
- clay/neutral material model;
- silhouette/thumbnail comparison;
- section or measured block model.

A form that only works in one flattering 3/4 hero camera is not sufficiently resolved.

## Gate 3 — payload / cavity / human interface

When the product contains, supports, receives or positions another object/body part, answer where that payload actually goes before visual lock.

Record as applicable:

- payload/envelope dimensions and authority;
- cavity/clearance relation;
- access/insertion/removal path;
- hand/body/eye/reach/contact zones;
- control visibility and affordance;
- cable/fluid/light/air/material path;
- maintenance/service access;
- collision/clearance and tolerance assumptions.

Use verified anthropometric/product/component sources or governed estimates. A hand silhouette or AI render is not dimensional authority.

If the payload or human interface does not fit, return upstream to the form/envelope instead of hiding the conflict in presentation.

## Gate 4 — mechanism / assembly interface

Activate only when parts move, latch, hinge, slide, rotate, flex, dispense, transform, attach, seal or otherwise depend on a functional relation.

Before a persuasive motion/render, state:

- what moves relative to what;
- pivot/axis/path/contact relation;
- what constrains and stops motion;
- restoring/holding/locking force or state when relevant;
- payload behavior through the motion;
- assembly order / access;
- likely failure/interference modes;
- which claims are concept assumptions versus technically validated.

Route fit-critical geometry to `oleander-3d-pipeline/PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION.md` when appropriate.

`MECHANISM DESCRIPTION / CAD MOTION ≠ ENGINEERING VALIDATION`.

## Gate 5 — form lock is conditional

A form may be designated as the Current selected design only after the relevant upstream functional questions have been addressed enough for the project's current maturity.

Record:

- what is locked;
- what remains adjustable;
- what proof supports the lock;
- what later evidence would force reopening;
- unresolved manufacturing/engineering/FIELD boundaries.

`LOCKED FOR DESIGN DEVELOPMENT ≠ FROZEN FOR TOOLING`.

## Gate 6 — CMF on governed geometry

CMF must be evaluated on the same Current form unless a deliberate geometry revision is declared.

For each CMF direction connect material/finish to actual requirements such as:

- structural/tactile/thermal behavior;
- grip/cleanability/weathering;
- durability and repair;
- manufacturing process;
- optical/translucent behavior;
- brand/perception role;
- lifecycle/environmental considerations.

Do not regenerate or redraw the form in a way that silently changes geometry while pretending to compare only materials.

## Gate 7 — hero/context presentation

Hero renders and lifestyle scenes are downstream presentation evidence. They may prove:

- intended visual character;
- object/context relationship;
- scale reading when bound to verified geometry;
- selected CMF/camera/lighting presentation.

They do not prove hidden cavity, mechanism feasibility, ergonomics, manufacturability, safety, tolerances or field performance.

If presentation reveals a real upstream design defect, return to the appropriate gate; do not retouch it away.

## Phase regression rule

A later phase may reopen an earlier decision when new evidence arrives. Record the causal change rather than pretending the earlier phase never existed.

Examples:

- CMF material requires wall/part split change → return to geometry/technical validation;
- mechanism interference changes envelope → return to form/payload;
- ergonomic test changes control position → return to human-interface/form;
- manufacturing process invalidates a surface or undercut → return through validation handoff.

## Required output

For a material physical-product round, return or persist:

- Current brief/source authority;
- option set and meaningful changed variables;
- selected form/proportion evidence;
- payload/cavity/human-interface evidence when applicable;
- mechanism/assembly relation and validation boundary when applicable;
- lock/open-variable record;
- CMF relation to the governed form;
- hero/context derivative identity;
- actual readback at each material phase used;
- upstream reopen decisions;
- technical/manufacturing/field HOLDs.

## Candidate boundary

This extension enforces design sequencing and visible proof. It does not provide universal ergonomic dimensions, DFM rules or engineering approval. Those require current authoritative sources and appropriate validation owners.