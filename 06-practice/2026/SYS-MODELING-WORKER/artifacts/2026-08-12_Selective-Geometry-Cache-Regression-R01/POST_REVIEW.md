# SYS-MODELING-WORKER-VAL-02｜R01 Selective Geometry × Cache Regression｜Post-Review

**Project:** P2 `SYS-MODELING-WORKER` → P3 `SYS-MODELING-WORKER-WS-01｜Automotive Reference Benchmark`  
**Validation:** P4 `SYS-MODELING-WORKER-VAL-02` / workflow code `MODELING-R01`  
**Node ownership:** `IP03` primary + Business support; node codes are not project IDs.  
**Historical executed result:** `WORKER METHOD PASS / DESIGN VARIANT REJECT / SOURCE AUTHORITY UNCHANGED`  
**Current clean-path state:** `ROUTING REPAIRED / SOURCE CLEAN-PATH RERUN PENDING`

## Historical runtime evidence
- GitHub Run `31553669263`
- Job `93981513179`
- Artifact `9125183502`
- Artifact SHA-256 `a180b68309728c945b4afc8e742bde8dff119bcec9d5e530f2a0efaf95fa3d11`
- selective Blender execution: `19 s`

The historical run remains valid evidence provenance. It consumed the executed v0.7 source from Run `31553008820` / Artifact `9124975690`. After project-path repair, promotion of this validation as current clean-path evidence requires a rerun against the clean #74 source artifact when that artifact exists.

## Method result
- exactly 40 wheel-spoke mesh objects changed;
- locked mesh objects changed: 0;
- only `WHEEL_DETAIL` and `HERO_FRONT_3Q` rerendered;
- first content-addressed resolution: `MISS`;
- identical second resolution: `HIT` and Blender execution skipped.

Cache scope is **job-local proof only**. Cross-run persistent cache is not validated.

## Design judgment
The geometry variant (`spoke_chord_scale = 0.90`) is **REJECTED**. Wheel Detail loses spoke-to-rim connection strength and the local gaps become more apparent; Hero change is too small to justify the local coherence loss.

The source `OLEANDER_Automotive_Reference_Vehicle_v0.7` remains unchanged and keeps `CANDIDATE_AUTHORITY` at the benchmark scope established by VAL-01.

## Promotion boundary
Retain the execution method at the current validation scope, not the wheel variant:

`Modeling Contract → target selector → locked-geometry hash gate → selective geometry revision → affected-view render → job-local content-addressed cache resolution`

Do not claim generalized Modeling Worker capability until at least:
1. clean-path rerun against the current VAL-01 artifact;
2. cross-run persistent cache validation if that capability is desired;
3. a second geometry family demonstrates the same dependency-control behavior.

Not Class-A, engineering CAD, vehicle-package, manufacturing or production validation.
