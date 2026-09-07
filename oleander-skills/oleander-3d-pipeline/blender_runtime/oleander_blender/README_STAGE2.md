# OLEANDER Blender Runtime — Stage 2

Stage 2 adds deterministic workbench primitives that do not depend on an external CAD/BIM/CAE/CAM runtime.

## Added

- dependency graph from stable OLE IDs;
- downstream stale propagation;
- missing dependency and cycle audit;
- deterministic geometry baseline and diff;
- parameter and constraint metadata contracts;
- separated review-state summarization;
- semantic object snapshot;
- direct metric dimension operator with Scene Unit Scale conversion;
- deterministic linear duplicate operator;
- OLE-ID configuration capture/restore for normal, exploded, transport, installation or other governed presentation/assembly states;
- governed BOM/quantity grouping using Part Number or a semantic+dimension fallback;
- same-Part-Number conflict detection for dimension, material, fabrication process and semantic-class inconsistencies;
- scene manifest v0.2 containing semantics, dependencies, parameters/constraints, geometry diff, review state and configuration index;
- dependency-free repository static check;
- Blender headless runtime validation script.

## Configuration boundary

A configuration stores transform, visibility and parameter metadata state by OLE ID. It does not duplicate or promote a new geometry master. It can represent normal/exploded/transport/installation presentation states, but it is not a solver-backed mechanical configuration, feature-suppression system or engineering-approved assembly state.

## BOM boundary

The BOM includes only objects that explicitly declare at least one of Part Number, Semantic Class, Object Class, Material Spec or Fabrication Process. Cameras, lights and undeclared temporary objects are skipped. A shared Part Number with inconsistent dimensions/material/process/semantic class is reported as a conflict rather than silently merged.

The BOM is a governed model-derived quantity view. It does not create procurement, manufacturing or engineering approval.

## Authority boundary

These features do not create a B-Rep/NURBS kernel, solver-backed sketch constraints, Class-A surface certification, IFC round-trip certification, engineering analysis, manufacturing release, or design approval.

A stored parameter/constraint entry is design intent metadata until a deterministic geometry solver is bound and verified. A geometry diff is change evidence, not a quality verdict. A stale flag is dependency-governance state, not proof that a downstream artifact is incorrect.

## Validation layers

### Repository static validation

Run:

```bash
python oleander-skills/oleander-3d-pipeline/blender_runtime/tests/static_check.py
```

This checks Python syntax, runtime-version agreement, manifest schema and lifecycle-state discipline without importing Blender. Static PASS is not Blender runtime PASS.

### Blender runtime validation

From Blender 5.1+:

```bash
blender --background --factory-startup --python \
  oleander-skills/oleander-3d-pipeline/blender_runtime/tests/validate_stage2.py
```

Before promotion beyond `PROPOSED_UNVERIFIED_RUNTIME`, verify:

1. extension registration without exceptions;
2. OLE metadata persistence;
3. object dependency resolution, missing-dependency detection and cycle handling;
4. downstream stale propagation;
5. geometry baseline and CHANGED diff;
6. configuration capture and restoration by OLE ID;
7. BOM grouping and same-Part-Number conflict detection;
8. FIELD/ENGINEERING/MANUFACTURING/DESIGN state separation;
9. Scene Unit Scale conversion for millimetre operators;
10. audit v0.2 and manifest v0.2 generation;
11. save/reopen persistence of OLE metadata, baseline, dependency, configuration and review data.

Until those runtime checks are executed with readback evidence, the runtime remains `PROPOSED_UNVERIFIED_RUNTIME`.
