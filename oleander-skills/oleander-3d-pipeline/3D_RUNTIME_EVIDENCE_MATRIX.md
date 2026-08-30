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
- HOLD:
  - actual GPU fragment-shader output parity;
  - mip/filter/anisotropy behavior;
  - skinning/animation tangent frames;
  - other engines/importers;
  - Design KEEP.

## E02 — Negative determinant changes effective tangent handedness

- Witness: `06-practice/2026/SYS-MODELING-WORKER/2026-08-30-gltf-negative-scale-tbn-witness/`
- Workflow: `OLEANDER 3D glTF Negative Scale TBN Witness`
- Confirmed latest-head run: `33317869448` — SUCCESS.
- Retained provenance: the first raw reconstruction run failed intentionally and showed the failure mechanism.
- Observed raw failure:
  - source and target object transform determinant `-1`;
  - exported tangent `w = +1`;
  - tangent and normal directions remained correct;
  - raw `B = w * cross(N,T)` produced an approximately `180 deg` bitangent reversal;
  - perturbed-normal error was approximately `57.37 deg`.
- Corrected tested contract:
  - `effective_w = tangent.w * sign(det(M_world))`;
  - reconstruct world bitangent from `effective_w * cross(N_world,T_world)`.
- Production consequence:
  - a negative-scale mirror is not treated as an ordinary tangent-safe transform after tangent-space baking;
  - determinant sign belongs in the target-runtime tangent-frame validation contract.
- HOLD:
  - non-uniform negative scale;
  - nested negative transforms;
  - skinning/animation;
  - fragment-shader output parity;
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
  - actual fragment-shader output parity;
  - production retopo mesh;
  - cross-DCC MikkTSpace parity;
  - a downstream importer that recomputes tangents after post-bake triangulation mutation;
  - Design KEEP.

## Routing rules promoted only within tested bounds

1. `INSTANCE COMPONENT ≠ MESH COMPONENT ≠ STATIC EXPORT`.
2. `1 DRAW CALL ≠ LOW MEMORY ≠ HIGH FPS`.
3. For the tested negative-determinant carrier, tangent-frame reconstruction must include transform determinant sign: `effective_w = tangent.w * sign(det(M_world))`.
4. `NORMAL MAP FILE EXISTS ≠ TARGET TEXTURE PIXEL PRESERVED ≠ FRAGMENT-SHADER OUTPUT PARITY`.
5. Surface-detail carrier selection uses `frequency × view × required cue`.
6. For tangent-space baked assets in the tested carrier, `TRIANGULATION CHANGE ≠ SHADING-NEUTRAL CHANGE`; lock triangulation before bake/export or recompute/rebake after topology changes.
7. `RAW SOURCE UV VALUES ≠ TARGET UV VALUES` when the exchange carrier defines a convention transform; validate the resolved convention explicitly.

## Maturity boundary

These rows are executable L7 evidence on the candidate PR, but they do not silently promote the entire parent framework, Skill, or Notion objects to universal M6. Promotion requires the applicable project/worker scope to be declared, artifact readback retained, and unresolved HOLDs excluded from the claim.
