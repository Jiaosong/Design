# OLEANDER OpenSCAD Parametric Fabrication Extension

Status: `CANDIDATE EXTENSION / 3D-PIPELINE`

Use when the Required Native Output is an editable `.scad` model intended for parameter-driven fabrication, especially 3D-printed utility parts, fixtures, holders, brackets, enclosures or fit studies.

This extension complements `PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION.md`. OpenSCAD is a valid parametric authoring route when it matches the required output; it does not replace a richer CAD assembly/tooling workflow when that is required.

## Core principle

`DESIGN INTENT → NAMED USER PARAMETERS → STABLE REFERENCE FRAMES / ANCHORS → DERIVED GEOMETRY → DETERMINISTIC CHECK → PROCESS / ORIENTATION DECISION → MESH/3MF DERIVATIVE → FABRICATION READBACK`.

The `.scad` source remains the editable parametric authority when it is the selected native authoring format. STL/3MF/render previews are derivatives unless Current authority explicitly says otherwise.

## Native-source contract

For material OpenSCAD work:

- keep dimensions, clearances and configurable counts as named parameters when they are intended to change;
- separate user-facing parameters from derived/internal values;
- keep units explicit;
- use stable reference points/planes/axes or anchor-style relations rather than unexplained transform chains;
- group repeated/meaningful geometry into modules/functions;
- make derived dimensions inspectable through assertions, echoes/reports or deterministic measurement where the runtime permits;
- repair the `.scad` source and regenerate derivatives rather than patching an STL/3MF when parametric continuation matters.

Project source conventions remain authoritative. OLEANDER does not require BOSL2 or any specific helper library.

## Parameter surface gate

Expose only parameters that correspond to real design decisions or controlled fabrication variations.

For each public parameter record:

- semantic meaning;
- units;
- valid or currently tested range if authoritative;
- dependent dimensions/features;
- collision/fit/manufacturing sensitivities;
- whether changing it requires downstream retest.

Do not expose every internal constant merely because OpenSCAD Customizer can display it. A large parameter panel with hidden coupling is not a robust parametric model.

## Reference-frame / anchor discipline

When dimensions change, relative placement should remain stable because it is defined from meaningful geometry relations.

Prefer relations such as:

- base/top/center plane;
- mating face;
- hole/shaft axis;
- enclosure wall datum;
- payload envelope boundary;
- symmetric centerline;
- mounting origin.

Every material translation/rotation should be explainable by a declared relation, design offset or presentation-only transformation.

## Boolean robustness

Constructive geometry can fail when coincident/coplanar boundaries create ambiguous subtraction/intersection results.

When the model uses boolean cuts/unions/intersections:

- avoid relying on visually coincident faces as a validation strategy;
- use bounded numerical clearance/overcut techniques only when they are justified by the modeling kernel/process and do not alter intended dimensions materially;
- inspect resulting bodies/meshes for missing faces, non-manifold geometry or unintended slivers when the export route exposes those checks;
- keep modeling-kernel workarounds separate from actual manufacturing clearance.

A boolean epsilon/workaround is not a fit tolerance.

## Fabrication orientation as a design decision

For FDM or another direction-dependent process, print/build orientation may change strength, support need, surface quality, tolerance and visible layering.

Choose orientation from the actual part requirements:

- primary load directions and likely failure mode;
- supported/unsupported surfaces;
- critical fit/contact faces;
- surface-finish priority;
- dimensional accuracy sensitivity;
- build volume and process capability;
- assembly/contact access after print.

Do not import fixed orientation angles, overhang rules, wall counts, infill percentages or material defaults as universal OLEANDER values. Use current printer/material/process data and project evidence.

`PRINTS FLAT ≠ CORRECT ORIENTATION`.

## Printer / process profile boundary

Treat printer, nozzle, material, slicer and process settings as a versioned fabrication context, not as geometry truth.

Record when material:

- printer/process identity;
- nozzle/tooling identity;
- material and batch/spec source when relevant;
- slicer/profile identity;
- layer/process settings that interact with model features;
- environmental/enclosure requirements;
- assumptions still unverified.

If the actual printer/process is unknown, keep process-specific settings open rather than designing around guessed capability.

## Export / derivative contract

Prefer the downstream format that preserves the information the fabrication workflow actually needs.

For mesh/fabrication derivatives record:

- source `.scad` identity/version;
- export format and units;
- mesh resolution/tessellation policy where material;
- object/body count;
- any color/material metadata;
- slicer/project metadata when included;
- reopen/import result in the target fabrication tool when available.

3MF may be preferable to STL when the actual toolchain benefits from preserved units/metadata, but it is not an OLEANDER universal requirement.

## Validation ladder

Scale checks to the claim:

1. source parses/renders;
2. parameter changes regenerate intended geometry;
3. bounds/units/body count are plausible;
4. specified dimensions/clearances are checked deterministically where possible;
5. boolean/export mesh integrity is checked where relevant;
6. print orientation/process assumptions are recorded;
7. derivative reopens in the target tool when available;
8. physical fit/strength/finish remains separate until real fabrication evidence exists.

For fit-critical assemblies or purchased components, co-route to `PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION.md` and current component/manufacturer evidence.

## Required output

Return:

- `.scad` Current source identity;
- user-parameter contract and derived dimensions;
- reference-frame/anchor logic;
- libraries/dependencies and license boundary;
- deterministic geometry checks;
- process/orientation rationale;
- export/3MF/STL derivative identities as used;
- target-tool reopen/readback when available;
- physical fabrication/fit/strength HOLD boundary.

## Candidate boundary

OpenSCAD source validity and mesh export do not prove manufacturability, strength, tolerance, safety or physical fit.

External study provenance: `swh/openscad-skill` / `openscad-bosl2`. No repository-level license file was found in the reviewed state, so OLEANDER retains only independently synthesized high-level mechanisms. BOSL2 house style, fixed numeric baselines, printer/material tables, slicer recipes, helper tools and code templates are excluded.