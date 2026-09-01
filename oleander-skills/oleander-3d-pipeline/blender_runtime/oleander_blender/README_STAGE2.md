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
- direct metric dimension operator;
- deterministic linear duplicate operator.

## Authority boundary

These features do not create a B-Rep/NURBS kernel, solver-backed sketch constraints, Class-A surface certification, IFC round-trip certification, engineering analysis, manufacturing release, or design approval.

A stored parameter/constraint entry is design intent metadata until a deterministic geometry solver is bound and verified. A geometry diff is change evidence, not a quality verdict. A stale flag is dependency-governance state, not proof that a downstream artifact is incorrect.

## Required runtime validation

Before promotion beyond `PROPOSED_UNVERIFIED_RUNTIME`:

1. install the extension in the declared Blender target build;
2. register all classes without exceptions;
3. create two objects with unique OLE IDs;
4. assign one as an upstream dependency of the other;
5. mark the upstream changed and verify downstream stale propagation;
6. store a geometry baseline, alter a dimension, and verify a CHANGED diff;
7. run dependency audit and verify missing/cycle cases fail;
8. set FIELD/ENGINEERING/MANUFACTURING states independently and verify review summary does not collapse them into geometry PASS;
9. test scene Unit Scale values other than 1.0 for millimetre operators;
10. save, reopen, and verify OLE metadata, baseline, dependency and review data persist.
