# 2026-08-10 | SP04 | Revit Parametric Wall Opening

Status: TRAINING PROTOTYPE / REVIT EXECUTION PENDING.

## Objective
Build a wall-hosted rectangular opening family from a reference-plane skeleton, with Width, Height and Sill Height as explicit parameters. The exercise trains constraint order, flex testing, host cutting and reproducible family QA rather than decorative modeling.

## Exercise-only hypothetical parameters
- Width types: 900 / 1200 / 1500 mm
- Height types: 2100 / 2400 mm
- Sill Height checks: 0 / 450 / 900 mm
- Minimum edge clearance check: 150 mm (training assumption only; not a code requirement)

## Revit workflow — NOT RUN in this runtime
1. Start from an appropriate wall-hosted / face-based family template.
2. Create and name reference planes: Left, Right, Bottom, Top, Center-LR.
3. Dimension reference planes first; label Width, Height and Sill Height.
4. Flex the skeleton before creating geometry.
5. Create the opening/void and lock its profile to the reference framework.
6. Enable the appropriate void-cut behavior where the chosen family category/template requires it.
7. Load into a sandbox project, place in at least two wall types, flex all parameter combinations and inspect plan/elevation/section.
8. Save the `.rfa` only after all flex tests pass; export QA screenshots and type matrix.

## QA contract
Pass requires: no unconstrained geometry, no failed constraints, opening remains hosted, dimensions update from parameters, all type combinations flex, and cut behavior is verified in a test project.

## Evidence boundary
Autodesk documents that reference planes should drive constrained family geometry and recommends flexing the family after constraints are established. Autodesk also documents wall openings and the `Cut with Voids When Loaded` family behavior. No `.rfa` or Revit viewport evidence is claimed here because Revit was not available in this runtime.

## Candidate gate
A score above 90 is necessary but not sufficient. Candidate status requires a real `.rfa`, sandbox `.rvt`, flex-test evidence, parameter/type table, and verified host-cut behavior.
