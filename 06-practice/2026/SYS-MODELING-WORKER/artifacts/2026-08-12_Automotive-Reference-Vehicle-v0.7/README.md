# SYS-MODELING-WORKER-VAL-01｜Automotive Reference Vehicle v0.7｜F1 Modeling Benchmark

**Project:** P2 `SYS-MODELING-WORKER` → P3 `SYS-MODELING-WORKER-WS-01｜Automotive Reference Benchmark`  
**Node ownership:** `IP03` primary with Business / Spatial support; node codes are not project IDs.  
**Status:** `F1 DESIGN VALIDATION PASS / CANDIDATE_AUTHORITY / REVIEW`

## Decision
Use one generic unbranded automobile as the comprehensive modeling benchmark for OLEANDER Modeling Worker development.

v0.7 is promoted because it closes the major Product-QA failures found in v0.1–v0.6: greenhouse/glazing separation, wheel-face hierarchy, front surfacing pinching, and roof-canopy overhang.

## Runtime evidence
- Blender 5.2.0 LTS / Cycles CPU
- Run `31553008820`
- Job `93979529010`
- Artifact `9124975690`
- Artifact SHA-256 `e8e459bfde3af4d03d41a839d5673404875ab79e7ade7b088155d4fd770508d6`
- final render step: 73 s
- 720 × 720 / 8 samples / 8 views
- Machine QA: PASS
- Product / Visual QA: PASS at F1 benchmark scope

## Benchmark coverage
- exterior loft/surfacing
- body / windshield / side glass / rear glass / A-B-C pillar hierarchy
- repeated and mirrored wheel assemblies
- tire / rim / spoke / brake-disc / caliper layering
- transparent and emissive parts
- visible interior blockout
- panel seam / trim / lamp / mirror details
- Hero / side / rear / top / front ortho / wheel detail / cabin detail / clay surfacing
- independent Machine QA and Product QA

## Authority
`WORKING_SOURCE → CANDIDATE_AUTHORITY`

Not Canonical/Frozen Authority.

## Known limitations
- not Class-A surfacing;
- simplified bumper/lamp/weatherstrip/flush-glass transitions;
- interior blockout only;
- no suspension/steering kinematics, underbody, crash, aero, package, homologation or production validation;
- styling is generic/stylized and is not an OLEANDER automotive design exemplar.

## Revision audit
v0.1 REJECT → v0.2 Machine PASS/Product REJECT → v0.3 REJECT → v0.4 surfacing REJECT → v0.5 Product REVISE → v0.6 Product REVISE → v0.7 F1 PASS.

Promotion-only rule: only v0.7 enters current candidate persistence; earlier versions remain audit/history only.
