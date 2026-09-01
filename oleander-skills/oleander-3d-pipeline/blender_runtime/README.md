# OLEANDER Blender Runtime — v0.1 Scaffold

This directory contains the first executable layer of the OLEANDER Blender Workbench.

## Current scope

Implemented without external sidecars:

- persistent `OLE ID` stored on Blender objects;
- governed metadata for object class, master type and master locator;
- geometry/material authority state;
- FIELD / ENGINEERING / MANUFACTURING state separation;
- LOD and assembly identity;
- stale-output marker;
- baseline scene audit;
- duplicate OLE ID detection;
- missing texture-path detection;
- non-manifold/non-finite mesh review checks;
- scene manifest generation to an editable Blender Text datablock.

Not implemented or claimed yet:

- B-Rep CAD kernel;
- NURBS/Class-A certification;
- sketch constraint solver;
- CAD assembly/mates;
- IFC semantic round-trip;
- vector technical drawing engine;
- CAE solver integration;
- CAM toolpath/postprocessor integration;
- automatic geometry-deviation round trip;
- full dependency graph/stale propagation;
- natural-language deterministic operator router.

These remain specialist sidecars or later workbench modules under `BLENDER_RUNTIME_WORKBENCH_EXTENSION.md`.

## Blender target

The add-on metadata currently targets Blender 5.1+ and uses standard `bpy.types.PropertyGroup`, `bpy.props`, Operators, Panels, Text datablocks and `bmesh`. Keep the implementation version-tolerant where practical and re-probe against the actual production Blender version before promotion.

## Install for development

Zip the `oleander_blender` package directory or place it in a Blender scripts/addons location, then enable **OLEANDER Blender Runtime** in Blender extensions/add-ons according to the active Blender installation policy.

After enabling, open:

`3D Viewport -> Sidebar -> OLEANDER`

## First validation sequence

1. Create three ordinary mesh objects.
2. Select them and run `Assign / Repair ID`.
3. Rename the Blender objects and verify `ole_id` remains unchanged.
4. Duplicate one object and run Audit; the copied identity should be reported as a collision until repaired.
5. Set one object to `CAD_NATIVE` without a master locator and confirm Audit flags the missing master locator.
6. Set geometry authority to `FIELD_OPEN` and confirm this remains distinct from mesh geometry status.
7. Create a deliberately open mesh and confirm the geometry review reports non-manifold edges.
8. Break an external image path and confirm dependency review reports it.
9. Build `OLEANDER_MANIFEST.json` in Blender's Text Editor and inspect object identity/authority/state.
10. Confirm the audit summary never claims engineering, constructability or design approval.

## Promotion gate

Do not label this runtime `ACTIVE` until it has been opened in the target Blender build and the validation sequence above has readback evidence.

Future specialist sidecars must also pass the parent 3D Skill's unit/axis, authority, reopen and round-trip requirements before their capabilities are advertised as active.
