# OLEANDER 3D Runtime Evidence Matrix

Status: **CANDIDATE / BOUNDED RUNTIME EVIDENCE / NO SILENT PROMOTION**

Purpose: record native and target-runtime facts proven by executable L7 witnesses on PR #468. This matrix is narrower than the Notion knowledge objects and narrower than `3D_PRODUCTION_KNOWLEDGE_ROUTING.md`: every row states exactly what the tested carrier proves and what remains HOLD.

General rule:

`WORKFLOW GREEN ≠ UNIVERSAL ENGINE RULE ≠ DESIGN KEEP ≠ MANUFACTURING / PHYSICAL TRUTH`

Unless a row says otherwise, current target-runtime witnesses use Blender 5.2.0 LTS source artifacts and Chromium through Playwright 1.55.0 with Three r179 / WebGL2 software carrier. Absolute SwiftShader timing is sensitivity evidence only, not a hardware production budget.

## E01 — Numeric tangent frame + embedded normal texture pixel

- Witness: `06-practice/2026/SYS-MODELING-WORKER/2026-08-30-gltf-tbn-reconstruction-witness/`
- Workflow: `OLEANDER 3D glTF Numeric TBN Reconstruction`
- Confirmed run: `33317869372` — SUCCESS after the v3 workflow Gate was corrected.
- Evidence class: `TARGET_RUNTIME_NUMERIC_TBN_PLUS_EMBEDDED_NORMAL_PIXEL`.
- Proven in this carrier:
  - Blender source tangent XYZ and normal XYZ survive glTF node transform into the tested target direction Gate;
  - `TANGENT.w` preserves the standard-vs-mirrored UV handedness witness;
  - `B = w * cross(N,T)` reconstructs the expected bitangent for positive-determinant transforms;
  - the GLB-embedded normal-map image is actually read through Three `normalMap.image`, not replaced by a source constant;
  - expected RGBA8 `[173,189,230,255]` and target sampled RGBA8 `[173,189,230,255]` match exactly in the observed run;
  - actual sampled pixel decoding drives a target perturbed-normal direction that passes the `0.005 deg + 5e-5 component` direction Gate;
  - standard-vs-mirrored perturbed-normal separation remains discriminative: about `42.20 deg` from source q and `41.68 deg` from the actual sampled pixel.
- Production consequence:
  - `NORMAL MAP FILE EXISTS` is insufficient evidence; retained normal-map claims require texture-carrier readback when interchange is material.
  - tangent XYZ, normal XYZ, handedness and texture pixel should be treated as one dependent shading contract, not isolated export checkboxes.
- Fragment-stage cross-reference:
  - E07 closes a diagnostic WebGL fragment-framebuffer stage for the same standard/mirrored witness, but only for its tested ShaderMaterial/WebGL2 software carrier.
- HOLD:
  - full production PBR/material-shader parity;
  - hardware GPU/driver parity;
  - mip/filter/anisotropy behavior;
  - skinning/animation tangent frames;
  - other engines/importers;
  - Design KEEP.

## E02 — Negative determinant changes effective tangent handedness

- Witness: `06-practice/2026/SYS-MODELING-WORKER/2026-08-30-gltf-negative-scale-tbn-witness/`
- Workflow: `OLEANDER 3D glTF Negative Scale TBN Witness`
- Confirmed fragment-stage run: `33460924293` — SUCCESS.
- Previous numeric-only run `33317869448` remains provenance.
- Evidence class: `TARGET_RUNTIME_NEGATIVE_SCALE_TBN_PLUS_FRAGMENT_OUTPUT`.
- Retained provenance: the first raw reconstruction run failed intentionally and showed the failure mechanism.
- Observed raw failure:
  - source and target object transform determinant `-1`;
  - exported tangent `w = +1`;
  - tangent and normal directions remained correct;
  - raw `B = w * cross(N,T)` produced an approximately `179.99958 deg` bitangent reversal;
  - perturbed-normal error was approximately `57.37063 deg`.
- Corrected tested contract:
  - `effective_w = tangent.w * sign(det(M_world))`;
  - reconstruct world bitangent from `effective_w * cross(N_world,T_world)`.
- Actual fragment/framebuffer closure in the same carrier:
  - source GLB SHA-256 = `666090d558f1dd2488d8b591708634bf9f670ff858a94b63b5ec90b9eefbf400`;
  - imported normal texel = `[173,189,230,255]`;
  - positive determinant expected/observed framebuffer RGBA8 = `[134,130,0,255]` / `[134,130,0,255]`, max channel delta `0`;
  - negative determinant expected/observed framebuffer RGBA8 = `[121,130,0,255]` / `[121,130,0,255]`, max channel delta `0`;
  - decoded-direction error is approximately `0.19450 deg` in both controlled cases;
  - expected positive-vs-negative fragment separation ≈ `5.59804 deg`;
  - observed separation ≈ `5.83575 deg`;
  - separation drift ≈ `0.23771 deg`, within the unchanged `<=0.5 deg` discriminator Gate;
  - output is read from the actual WebGL render target/framebuffer rather than reconstructed only in JavaScript numerics.
- Production consequence:
  - a negative-scale mirror is not treated as an ordinary tangent-safe transform after tangent-space baking;
  - determinant sign belongs in the target-runtime tangent-frame validation contract;
  - stored mesh `TANGENT.w` alone is insufficient for an odd-reflection world transform when fragment output is material to the claim.
- HOLD:
  - non-uniform negative scale;
  - nested negative transforms;
  - applied/baked mirror vs object-space negative scale;
  - skinning/animation/morph targets;
  - topology/triangulation mutation;
  - full Three `MeshStandardMaterial` / production PBR formula parity;
  - hardware GPU/driver parity;
  - other engines/importers;
  - Design KEEP.

## E03 — Geometry Nodes Instance Component is not a static Mesh Component

- Witness: `06-practice/2026/SYS-MODELING-WORKER/2026-08-30-gn-instance-realize-sensitivity/` and the existing Geometry Nodes native benchmark.
- Workflow: `OLEANDER 3D GN Instance vs Realize Sensitivity`.
- Confirmed latest-head run: `33317869414` — SUCCESS.
- Retained provenance: the initial Gate wrongly required Instance and Realize static GLB outputs to converge; that assumption failed and was removed.
- Proven in this Blender 5.2 carrier:
  - an unresolved Geometry Nodes Instance Component on the tested `to_mesh()` / static-mesh path is not equivalent to a Mesh Component;
  - Realize Instances materializes explicit mesh geometry and therefore changes representation semantics and downstream export behavior;
  - instance/realize state must be an explicit handoff decision rather than an incidental node choice.
- Production consequence:
  - `INSTANCE COMPONENT ≠ MESH COMPONENT ≠ STATIC EXPORT`;
  - retain instance/realize policy, instance count, explicit mesh count and target export strategy in handoff evidence.
- HOLD:
  - arbitrary GN graphs;
  - all exporters;
  - `EXT_mesh_gpu_instancing` parity;
  - production-scene performance;
  - Design KEEP.

## E04 — Runtime instance carrier: draw calls vs explicit geometry storage

- Witness: `06-practice/2026/SYS-MODELING-WORKER/2026-08-30-three-instance-carrier-benchmark/`.
- Workflow: `OLEANDER 3D Three Instance Carrier Benchmark`.
- Confirmed run on the candidate branch: SUCCESS; same-population screenshots received Artifact Review.
- Controlled populations: `225 / 900 / 3600` identical cubes.
- Observed representation facts:
  - Naive Mesh objects: `225 / 900 / 3600` draw calls;
  - `InstancedMesh`: `1 / 1 / 1` draw call;
  - one Flattened Mesh: `1 / 1 / 1` draw call;
  - explicit carrier-byte ratio Flattened / Instanced: approximately `5.31x / 5.54x / 6.73x` for those populations.
- Production consequence:
  - draw-call reduction and geometry-storage duplication are separate axes;
  - `1 DRAW CALL ≠ LOW MEMORY ≠ HIGH FPS`;
  - choose instance, flattened, or separate-object carrier from mutability/culling/material/LOD/runtime requirements, not draw-call count alone.
- HOLD:
  - physical GPU allocation;
  - hardware frame budget;
  - occlusion/frustum behavior;
  - multiple materials;
  - LOD/HLOD;
  - production scene complexity;
  - Design KEEP.

## E05 — Normal vs displacement depends on view and required cue

- Witness: `06-practice/2026/SYS-MODELING-WORKER/2026-08-30-normal-vs-displacement-by-view/`.
- Workflow: `OLEANDER 3D Normal vs Displacement by View`.
- Confirmed latest-head run `33317869389` — SUCCESS.
- Observed controlled silhouette evidence:
  - `TOP_FAR`: low + normal silhouette IoU approximately `0.99651` relative to high reference;
  - `GRAZE_CLOSE`: low + normal falls to approximately `0.86342`;
  - displaced/geometry carrier at `GRAZE_CLOSE` approximately `0.99631`;
  - grazing-view silhouette advantage of displacement/geometry approximately `+0.13289`.
- Production consequence:
  - detail representation is selected by `frequency × view × required cue`, not frequency alone;
  - normal/bump may represent a cue only while silhouette, parallax, self-occlusion or physical relief are not required at the target view.
- HOLD:
  - arbitrary assets/materials;
  - production displacement tessellation budgets;
  - physical manufacturing truth;
  - Design KEEP.

## E06 — Triangulation changes tangent-space shading

- Witness: `06-practice/2026/SYS-MODELING-WORKER/2026-08-30-gltf-triangulation-tbn-witness/`.
- Workflow: `OLEANDER 3D glTF Triangulation TBN Witness`.
- Confirmed run: `33318087835` — SUCCESS.
- Evidence class: `TARGET_RUNTIME_TRIANGULATION_SENSITIVITY_WITH_RESOLVED_UV_CONVENTION`.
- Retained provenance:
  - v1 failed because six Blender face-corner samples were incorrectly averaged against four indexed target vertices;
  - v2 exposed raw UV-coordinate convention mismatch and a separate exact-basis precision diagnostic;
  - neither failure was deleted or converted to PASS by widening the original direction/component Gate.
- Proven in this carrier:
  - source→target UV convention resolves consistently as `V_FLIP`; all matched corners have mapped UV delta `0`;
  - two alternate triangulations of the same four source positions and same source UV assignment produce large, repeatable tangent-space shading changes;
  - source per-vertex alternate-triangulation perturbed-normal differences: approximately `12.084506 / 10.817926 / 10.952708 / 9.196483 deg`;
  - target readback: approximately `12.084158 / 10.815838 / 10.950281 / 9.197082 deg`;
  - maximum source→target sensitivity drift: approximately `0.002427 deg`;
  - every matched corner passes handedness + final perturbed-normal direction semantics;
  - every per-source-vertex aggregate perturbed normal passes the unchanged `0.005 deg + 5e-5 component` Gate.
- Independent precision HOLD retained:
  - `exactBasisCornerParity = false` because a few individual T/N/B components exceed the `5e-5` component diagnostic by only a few `1e-6` even though their angular errors remain below `0.005 deg` and the final perturbed-normal Gate passes.
- Production consequence:
  - `TRIANGULATION CHANGE ≠ SHADING-NEUTRAL CHANGE` for tangent-space baked assets;
  - lock final triangulation before tangent-space bake/export, or recompute/rebake tangents and maps after topology/triangulation changes;
  - compare source and target UVs under the actual carrier convention rather than assuming raw numeric UV identity.
- HOLD:
  - exact per-corner T/N/B component parity at `5e-5`;
  - triangulation-specific fragment-shader output parity;
  - production retopo mesh;
  - cross-DCC MikkTSpace parity;
  - a downstream importer that recomputes tangents after post-bake triangulation mutation;
  - Design KEEP.

## E07 — Diagnostic WebGL fragment normal output reaches the framebuffer

- Witness: `06-practice/2026/SYS-MODELING-WORKER/2026-08-30-fragment-normal-output-witness/`.
- Workflow: `OLEANDER 3D WebGL Fragment Normal Output`.
- Confirmed run: `33319029908` — SUCCESS.
- Evidence class: `TARGET_RUNTIME_WEBGL_FRAGMENT_TBN_NORMAL_OUTPUT`.
- Retained failure provenance:
  - first execution timed out before the viewer exposed a ready/error state;
  - after runtime diagnostics were added, Three r179 exposed `outputColorSpaceConfig` failure caused by setting `WebGLRenderer.outputColorSpace = NoColorSpace`;
  - the fix retained a valid renderer output configuration while keeping the offscreen diagnostic render target as the raw carrier; TBN math and framebuffer pixel Gates were not relaxed.
- Proven in this carrier:
  - source GLB SHA-256 = `a12bdf28512e672fce762c99aeb09c2405be3689fd4fbb5b75f55b7bc97a0020`;
  - GLB embedded normal sample remains `[173,189,230,255]`;
  - `TBN_STANDARD` expected framebuffer RGBA8 `[134,130,0,255]`, observed `[134,130,0,255]`, max channel delta `0`, decoded-direction error approximately `0.194495 deg`;
  - `TBN_MIRRORED` expected framebuffer RGBA8 `[67,74,28,255]`, observed `[67,74,28,255]`, max channel delta `0`, decoded-direction error approximately `0.140551 deg`;
  - expected standard-vs-mirrored separation approximately `41.677975 deg`;
  - observed framebuffer separation approximately `42.006839 deg`;
  - separation drift approximately `0.328865 deg`;
  - browser output was read back from the actual WebGL render target/framebuffer path rather than reconstructed only in JavaScript numerics.
- Cross-reference:
  - E02 now independently closes the previously open negative-determinant diagnostic fragment/framebuffer path for its exact tested carrier and keeps non-uniform/nested/applied-mirror/PBR/hardware cases HOLD.
- Production consequence:
  - `NORMAL MAP FILE EXISTS ≠ TARGET TEXTURE PIXEL PRESERVED ≠ FRAGMENT OUTPUT VERIFIED`;
  - when fragment output is material to an interchange claim, a numeric accessor/texture check can be supplemented by a deliberately bounded shader/framebuffer witness.
- HOLD:
  - hardware GPU and driver parity; current CI carrier is WebGL2 software/SwiftShader-class execution;
  - full Three `MeshStandardMaterial` / production PBR formula parity;
  - mip/filter/anisotropy behavior;
  - triangulation-specific fragment parity;
  - other engines/importers;
  - Design KEEP.

## E08 — Material-node data semantics + diagnostic lighting are evidence-bearing state

- Witness: `06-practice/2026/SYS-MODELING-WORKER/2026-08-30-material-nodes-lighting-diagnostic/`.
- Workflow: `OLEANDER 3D Material Nodes Lighting Diagnostic`.
- Confirmed current-head run: `33320392696` — SUCCESS; execute, contract validation, hashing and artifact upload all passed.
- Runtime: Blender `5.2.0 LTS / fbe6228777e7`, Cycles CPU, `256×256`, 16 samples, AgX, locked camera/geometry.
- Current artifact: `9734724592`; ZIP digest `sha256:514e213dbf44225a46bea0bdc71e2cd6ac7294d647a7462e41578aa563d157c0`.
- Native master: `MATERIAL_NODES_LIGHTING_DIAGNOSTIC.blend`, 102,924 bytes, SHA-256 `bf2e3ed1b070533bd44c8efad7dd78204211f0af64106e1f331826a204f907a1`.
- Shared scalar roughness source: `ROUGHNESS_DATA_SOURCE.png`, 10,987 bytes, SHA-256 `1c57f40b3698f776c063f96b1d518fd8ecda0a8bfc30f582e9d97db9aa75a2b2`.
- Controlled materials:
  - `CONTROL_CONSTANT` — Principled roughness constant;
  - `ROUGHNESS_NONCOLOR` — the shared PNG explicitly interpreted as `Non-Color` data;
  - `ROUGHNESS_SRGB_WRONG` — the exact same PNG bytes intentionally interpreted as `sRGB`.
- Controlled rigs:
  - `BROAD` — large frontal area / whole-surface response;
  - `STRIP` — narrow oblique strip / highlight-width and continuity pressure;
  - `GRAZING` — low-angle strip / roughness and surface-response pressure.
- Confirmed output facts:
  - all nine Cycles RGBA PNG renders exist and each retains 23,756 visible object pixels under the locked frame;
  - control-rig metric distances: Broad↔Strip `0.245901`, Broad↔Grazing `1.126830`, Strip↔Grazing `0.911735`; unchanged Gate required maximum `> 0.05`;
  - same-PNG color-space interpretation distances: Broad `0.030657`, Strip `0.032803`, Grazing `0.030273`; unchanged Gate required maximum `> 0.03`;
  - maximum final written-output near-saturation fraction (`>= 0.99`) = `0.0`, Gate `< 0.08`;
  - actual nine-frame Artifact Review = **KEEP SUPPORT / DIAGNOSTIC EVIDENCE**: Broad/Strip/Grazing are visibly distinct, the Non-Color vs sRGB roughness change is subtle but visually/measurably present, framing/geometry are locked, and the set is not treated as hero rendering or physical CMF approval.
- Measurement-carrier provenance:
  - run `33319859082` failed before rendering because `read_factory_settings(use_empty=True)` left `scene.world = None`; explicit diagnostic World was created without altering material/rig Gates;
  - run `33320024059` rendered a valid Broad PNG but in-memory `Render Result` alpha reported zero visible pixels while the written RGBA PNG was correct;
  - run `33320229312` showed the same background-runtime boundary more strongly: written PNG was `256×256`, while in-memory `Render Result.size` was `(0,0)` after `write_still`;
  - v2 therefore measures the actual written RGBA PNG; radiometric/HDR `>1` clipping is not silently reconstructed and remains HOLD rather than lowering an unrelated Gate.
- Reproducibility readback across run 4 and run 5:
  - experimental metrics repeat to a maximum observed metric drift of approximately `3.54e-8`;
  - four decoded RGBA outputs are pixel-identical;
  - the other five differ by only one channel value at one pixel, maximum `1 LSB`;
  - PNG file SHA values differ, therefore this is **numeric/pixel stability within 1 LSB**, not byte-deterministic rendering.
- Production consequence:
  - `SAME TEXTURE BYTES ≠ SAME SHADER INPUT SEMANTICS`; scalar data maps require explicit data/color-space interpretation;
  - `DIAGNOSTIC RIG NAME ≠ DIAGNOSTIC SEPARATION`; a Broad/Strip/Grazing matrix earns authority only when actual output demonstrates distinct diagnostic pressure;
  - `WRITTEN ARTIFACT ≠ IN-MEMORY BUFFER`; if a runtime readback carrier is demonstrated unreliable, retain the failure provenance, measure the applicable delivered carrier, and leave unsupported claims HOLD instead of changing thresholds.
- HOLD:
  - radiometric/HDR clipping measurement for this CI route;
  - XJ01 historical authority exact-byte identity;
  - physical PP/roughness measurement;
  - texture-source photography/scan truth;
  - normal/displacement map semantics outside the separate E01/E05 witnesses;
  - spectral/material metrology;
  - hero-lighting quality;
  - Physical CMF Approval;
  - Design KEEP.

## E09 — Same source controls do not collapse B-Spline/NURBS and Catmull-Clark into one surface

- Witness: `06-practice/2026/SYS-MODELING-WORKER/2026-08-31-nurbs-subd-same-source-benchmark/`.
- Workflow: `OLEANDER 3D NURBS vs SubD Same-Source Benchmark`.
- Confirmed run: `33376553806` — SUCCESS; FreeCAD build/reopen, Blender build/reopen, evaluated comparison, bounded contract and artifact upload all passed.
- Artifact: `9752141736`; ZIP digest `sha256:d233c9911715b452bd455edd9d087a69923053fab4c72f26d58ac1aa8a0a5733`.
- Shared source: `source_controls.json`, SHA-256 `b4a64dd70d0e91b9f019ea01de56ead0c80bcd13f84b74a265624c8c1965ae09`.
- Worker A:
  - FreeCAD `1.1.3` / OpenCASCADE;
  - degree-3 non-rational B-Spline profile from the nine shared poles, revolved 360 degrees into a valid B-Rep Face;
  - native FCStd reopen valid; STEP derivative retained; evaluated mesh 2,510 vertices / 5,016 raw faces.
- Worker B:
  - Blender `5.2.0 LTS`;
  - polygon radial cage from the same rings → unapplied Catmull-Clark Subdivision modifier;
  - native `.blend` reopen valid;
  - L2 evaluated 1,442 vertices / 1,440 polygons; L4 evaluated 23,042 vertices / 23,040 polygons.
- Measured representation result:
  - FreeCAD B-Spline/NURBS vs SubD L4 profile RMSE = `1.790459 mm`;
  - SubD L2 vs L4 profile RMSE = `0.093447 mm`;
  - FreeCAD vs SubD profile-curvature RMSE = `0.000688071 /mm`;
  - FreeCAD evaluated profile vs source control-radius RMS delta = `1.868059 mm`;
  - SubD L4 evaluated profile vs source control-radius RMS delta = `3.304436 mm`;
  - FreeCAD bbox ≈ `240.000 × 109.016 × 109.016 mm`;
  - SubD L4 bbox ≈ `229.843 × 104.158 × 104.158 mm`;
  - length relative delta ≈ `4.232%`; diameter relative delta ≈ `4.456%`;
  - max cross-section noncircularity ≈ `0.293%`.
- Retained failure provenance:
  - run `33376286912` built/saved/exported the B-Spline successfully but failed an invalid reopen assumption: FCStd build→reopen retained B-Rep area exactly while Y/Z BoundBox changed by `0.015727886 mm`;
  - the former `1e-8 mm` bbox Gate was rejected as an over-precise proxy for geometry identity;
  - v2 keeps validity/type/topology/area as exact invariants and bbox as a bounded diagnostic (`<0.05 mm`, relative `<0.0005`). Representation construction and cross-representation thresholds were not relaxed.
- Artifact Review:
  - same-camera renders visibly support the measured relation: FreeCAD B-Spline/NURBS is longer/more voluminous, while Catmull-Clark is globally contracted but preserves the same streamlined first-read;
  - lighting is too dark for Zebra/highlight-flow/Class-A approval, so the images are **KEEP SUPPORT / REPRESENTATION EVIDENCE**, not professional surface-quality PASS.
- Production consequence:
  - `SAME CONTROL ARCHITECTURE ≠ SAME EVALUATED / LIMIT SURFACE`;
  - `CONTROL POLE / RING ≠ REQUIRED SURFACE INTERPOLATION POINT` unless interpolation is explicitly part of the representation contract;
  - `HIGHER SUBD EVALUATION LEVEL ≠ NURBS CONVERSION`: here L2→L4 sampling change (`0.093 mm` profile RMSE) is far smaller than the NURBS↔SubD representation delta (`1.790 mm`);
  - compare cross-representation claims on evaluated sections/curvature/silhouette and native reopen, not on similar UI vocabulary such as control points or smooth surfaces.
- HOLD:
  - Rhino 8 native `.3dm` NURBS/SubD parity;
  - Rhino Zebra/EMap/CurvatureGraph/MatchSrf and G2/G3 Class-A qualification;
  - Houdini procedural parity;
  - aerodynamic/CFD performance;
  - manufacturing/engineering truth;
  - Design KEEP.

## E10 — Operator success requires semantic postconditions, not only kernel/API validity

- Witness: `06-practice/2026/SYS-MODELING-WORKER/2026-08-31-operator-failure-anatomy/`.
- Notion practice: `PRAC-20260831-3D-12｜Operator Failure Anatomy｜FreeCAD B-Rep × Blender Modifier Parameter Sweep`.
- Workflow: `OLEANDER 3D Operator Failure Anatomy`.
- Confirmed latest visual-fix run: `33389249392` — workflow SUCCESS.
- Artifact: `9756862659`; ZIP digest `sha256:70687957293ce4765119058a8b2bf6f943b237f4076748a66e343a8c64b6c26c`.
- Source commit: `cde1de96a0c5ac76071b7cd5f5006adc336cde68`.
- Runtimes:
  - FreeCAD `1.1.3` / OpenCASCADE B-Rep worker;
  - Blender `5.2.0 LTS` modifier worker.
- Proven in the tested FreeCAD carrier:
  - Fillet `5.9 mm` is the last semantic success; `6.0 mm` raises a kernel exception; `6.1 mm` returns an invalid shape with geometry/bbox explosion;
  - Thickness `11.9 mm` is the last semantic success; `12.0 mm` raises a kernel exception; `12.1 mm` and `14.0 mm` return `isValid=true` Solids that are the original `40×24×12 mm`, 6-face / 12-edge / 8-vertex / 11520 mm³ box — a `VALID_SEMANTIC_NOOP`;
  - a 10 mm-radius sphere shell remains regular at inward offset `-9.9 mm` and hits the zero-radius failure boundary at `-10.0 mm`.
- Proven in the tested Blender carrier:
  - Bevel with Clamp ON realizes the same measured corner clearance `4.701062 mm` at requested widths `6.1 mm` and `8.0 mm`, while Clamp OFF at `8.0 mm` realizes `5.760580 mm`; policy can therefore saturate realized geometry;
  - Solidify requested `2.0 mm` realizes `1.0 mm` world thickness under unapplied object scale `[2,1,0.5]`, and `2.0 mm` after the same scale is baked into geometry.
- Refined semantic contract:
  - `RESULT = OPERATOR(INPUT, PARAMETERS, REFERENCES, TOLERANCE, POLICY, TRANSFORM_STATE, CONTEXT)`;
  - `SEMANTIC_SUCCESS = VALIDATE(RESULT, DECLARED_POSTCONDITIONS / INVARIANTS)`.
- Production consequence:
  - `KERNEL RETURN / NOT-NULL / IsValid ≠ OPERATOR SEMANTIC SUCCESS`;
  - requested parameter value is not guaranteed realized geometry;
  - kernel exception, invalid returned shape, valid semantic no-op, policy-clamped result and transform-dependent realized value are distinct failure/readback states;
  - operator validation should use parameter/failure sweeps and postcondition readback, not one successful call.
- Artifact Review boundary:
  - native numeric/semantic receipts and reopen evidence PASS;
  - latest Bevel/Solidify closeups remain too dark for reliable direct visual discrimination, especially the `1 mm` vs `2 mm` Solidify difference;
  - therefore **ARTIFACT REVIEW = POST-REVIEW FAIL / TRAINING NOT CLOSED**. Workflow SUCCESS must not be described as a final visual-evidence PASS.
- HOLD:
  - repaired readable visual carrier with explicit section/thickness gauge;
  - Rhino native OffsetSrf/FilletSrf/Shell parity;
  - arbitrary topology and general self-intersection repair;
  - manufacturing wall-thickness approval;
  - all B-Rep kernels / modifier implementations;
  - Design KEEP.

## Routing rules promoted only within tested bounds

1. `INSTANCE COMPONENT ≠ MESH COMPONENT ≠ STATIC EXPORT`.
2. `1 DRAW CALL ≠ LOW MEMORY ≠ HIGH FPS`.
3. For the tested negative-determinant carrier, tangent-frame reconstruction and its diagnostic fragment output must include transform determinant sign: `effective_w = tangent.w * sign(det(M_world))`; E02 closes this only for its exact tested software carrier.
4. `NORMAL MAP FILE EXISTS ≠ TARGET TEXTURE PIXEL PRESERVED ≠ FRAGMENT OUTPUT VERIFIED`; E07 closes the standard/mirrored final stage and E02 closes the negative-determinant final stage only for their bounded diagnostic WebGL carriers.
5. Surface-detail carrier selection uses `frequency × view × required cue`.
6. For tangent-space baked assets in the tested carrier, `TRIANGULATION CHANGE ≠ SHADING-NEUTRAL CHANGE`; lock triangulation before bake/export or recompute/rebake after topology changes.
7. `RAW SOURCE UV VALUES ≠ TARGET UV VALUES` when the exchange carrier defines a convention transform; validate the resolved convention explicitly.
8. `SAME TEXTURE BYTES ≠ SAME SHADER INPUT SEMANTICS`; scalar data maps such as roughness must preserve their intended data/color-space interpretation.
9. `DIAGNOSTIC RIG NAME ≠ DIAGNOSTIC SEPARATION`; Broad/Strip/Grazing labels are not evidence unless the actual outputs demonstrate distinct diagnostic pressure.
10. `WRITTEN ARTIFACT ≠ IN-MEMORY BUFFER`; when a runtime proves one carrier unreliable, retain the failure and move only the supported measurement to the applicable carrier instead of silently relaxing thresholds.
11. `REPEATABLE METRICS ≠ BYTE-DETERMINISTIC RENDER`; report the observed reproducibility level explicitly.
12. `SAME CONTROL ARCHITECTURE ≠ SAME EVALUATED SURFACE`; when comparing NURBS/B-Spline, SubD or other representation families, separate source controls, evaluator, sampling density and evaluated geometry, and never treat subdivision level as representation conversion.
13. `KERNEL RETURN / NOT-NULL / IsValid ≠ OPERATOR SEMANTIC SUCCESS`; operator claims require declared postconditions/invariants, failure sweeps and realized-geometry readback. Policy and transform state are part of the tested operator contract when they alter the result.

## Maturity boundary

These rows are executable L7 evidence on the candidate PR, but they do not silently promote the entire parent framework or Skill to universal truth. Explicit parent maturity changes still require applicable scope to be declared, artifact readback retained, unresolved HOLDs excluded, and promotion boundaries preserved.
