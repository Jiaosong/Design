# OLEANDER Parametric CAD Geometry Validation Extension

Status: `CANDIDATE EXTENSION / 3D-PIPELINE + TECHNICAL-DRAWING + DELIVERY-QC`

Use when the Required Native Output includes parametric mechanical/product CAD, STEP/STP exchange, assemblies, mating interfaces, datum-driven positioning, purchased components or geometry claims that must survive deterministic inspection.

## Core separation

`DESIGN INTENT → PARAMETRIC SOURCE → DATUM / JOINT RELATION → CAD ARTIFACT → DETERMINISTIC GEOMETRY CHECK → DIAGNOSTIC VISUAL READBACK → REPAIR`.

A rendered view, browser viewer, manually dragged placement or aesthetically plausible model is not geometry proof.

## Native-output rule

Choose the professional native/open-native CAD artifact required by the project. When STEP/STP is the governing exchange format, preserve the editable parametric source as the Current authoring authority and treat STEP as an inspectable exchange/validation artifact unless Current authority explicitly promotes it.

Mesh outputs such as STL/3MF/GLB are downstream derivatives for fabrication preview, real-time viewing or mesh-specific checks. A mesh derivative must not silently replace an editable parametric source when parametric continuation is required.

## Parametric source contract

For geometry that affects fit, assembly or later technical drawing:

- expose meaningful dimensions and offsets as named parameters;
- record unit system, local origin, primary planes/axes and dimension authority;
- give important parts/features stable semantic labels where the execution surface supports them;
- keep generated geometry reconstructable from source and parameters;
- do not patch an exported exchange file when an authoritative source exists; repair the source and regenerate;
- separate verified dimensions, governed estimates and unresolved FIELD/manufacturing values.

## Datum and assembly contract

Do not author assembly placement as unexplained visual transforms when a functional relation exists.

Use this reasoning order:

`ROOT / FIXED COMPONENT → PART-LOCAL FRAME → FUNCTIONAL DATUM → MATE / JOINT INTENT → PARAMETERIZED PLACEMENT → GENERATED ASSEMBLY → ALIGNMENT / FRAME / MEASUREMENT CHECK`.

Functional datums may include mounting faces, bolt axes, hinge axes, slider axes, gasket seats, locating tabs, bearing axes, center planes or other project-specific interfaces.

Every material numeric transform should correspond to a stated datum, offset, clearance, contact condition or deliberate presentation-only exploded-view operation.

## Purchased-component gate

When a design names an off-the-shelf component whose real envelope or interface matters, search an authoritative manufacturer/catalog/source model before drawing a simplified proxy.

Record:

- exact model/part identifier and aliases searched;
- source and license/usage boundary;
- source geometry checksum or version when material;
- whether the model is authoritative, supplier-provided, community-derived or only an envelope;
- the fallback envelope and uncertainty when no trustworthy model is available.

`NAMED REAL PART AVAILABLE → GENERIC PLACEHOLDER` is a regression unless the simplification is intentional and documented.

## Geometry validation ladder

For every material generated/modified CAD object, scale checks to the actual specification:

1. **Identity / units / bounds** — file/object identity, units, bounding box, body/solid count.
2. **Topology / solidity** — closed/valid solids where required; open surfaces only when explicitly intended.
3. **Spec dimensions** — measure every user/project-specified dimension, clearance or offset that is part of the claim.
4. **Assembly relations** — inspect mating deltas, center/axis alignment, occurrence frames and orientation where relevant.
5. **Change isolation** — when modifying geometry, compare before/after and verify unrelated locked geometry did not drift.
6. **Visual diagnostic** — review one or more deterministic CAD snapshots/views suitable for the geometry complexity.
7. **Convert visual suspicion back to geometry** — a visual concern becomes a validation claim only after a corresponding dimension/frame/topology/contact check.

## Diagnostic snapshot rule

A visibly changed primary CAD object needs an actual visual readback when a faithful renderer/viewer is available. Use a small view packet only when complexity justifies it; do not render endless variants after deterministic checks are already conclusive.

Typical diagnostic views:

- opposed isometric views for hidden-face coverage;
- top/front orthographic views for symmetry/profile;
- section view for cavities, shell thickness, bores or blind features;
- transparent/hidden-edge/wireframe only when they answer a specific overlap/contact question.

Visual review is diagnostic, not dimensional authority.

## Manufacturing boundary

Geometry validity does not prove manufacturability, tolerance capability, structural safety or certification. If DfM/DfAM is required, route measured geometry to the relevant process limits, supplier/manufacturer data or specialist validation owner. Do not estimate wall thickness, support angle, tolerance or process feasibility from a render when it can be measured.

## Required handoff

Return:

- Current parametric/native source identity;
- exchange/STEP identity when used;
- units/origin/axis and geometry/dimension authority;
- named parameters and locked dimensions;
- datum/joint/mating intent;
- purchased-component provenance or documented envelope fallback;
- deterministic checks actually executed;
- diagnostic visual readback and follow-up geometry checks;
- source repair/retest record;
- downstream technical drawing / manufacturing / QC HOLD boundaries.

## Candidate boundary

This extension strengthens CAD reasoning and validation but does not create an OLEANDER engineering-certification owner. `VALID CAD GEOMETRY ≠ MANUFACTURABLE ≠ STRUCTURALLY SAFE ≠ FIELD VERIFIED`.