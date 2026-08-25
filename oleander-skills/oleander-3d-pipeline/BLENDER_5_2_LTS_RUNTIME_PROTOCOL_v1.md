# OLEANDER Blender 5.2 LTS Runtime Protocol v1

Status: **CANDIDATE TRAINING DELTA / NOT SILENTLY CURRENT**

Purpose: bind Blender execution to a versioned, recoverable runtime and prevent a valid `.blend`, render, procedural result, or export from being treated as evidence for a claim the runtime did not actually test.

This protocol extends the installed `oleander-3d-pipeline` owner. It does not create a second 3D Skill and does not replace project Source Authority, the Modeling Worker, Surface System, Artifact Review, or project-specific design judgment.

## Official runtime baseline｜2026-08-19

- Blender **5.2 LTS** was released 2026-07-14 and is supported until July 2028. It is the preferred default for new OLEANDER Blender production unless a project dependency requires another verified version.
- Blender 4.5 LTS remains maintained, so long-lived work may legitimately stay on 4.5 when add-on, interchange, or project compatibility requires it. Version choice must be explicit; recency alone does not rewrite a production environment.
- Blender 5.0 introduced major color-management changes including wide-gamut/HDR support and ACES-oriented workflows. A render comparison without a recorded color pipeline is therefore incomplete evidence.
- Blender 5.2 adds remote Asset Libraries and experimental node-based cloth/hair physics. Network availability or a visually convincing simulation does not create durable dependency proof or physical/engineering truth.

Official sources:
- https://www.blender.org/releases/5-2/
- https://www.blender.org/download/lts/
- https://www.blender.org/download/releases/5-0/
- https://docs.blender.org/manual/en/5.2/files/blend/packed_data.html
- https://docs.blender.org/manual/en/5.2/files/asset_libraries/introduction.html

---

## 1｜Runtime Identity Gate

Every execution that produces retained evidence records:

`BLENDER VERSION → BUILD / PLATFORM → DEVICE / BACKEND → EXTENSIONS → COLOR CONFIG → PROJECT FILE`

Required receipt fields:

- application name and exact Blender version;
- build hash when available, otherwise explicit `UNKNOWN_NOT_CAPTURED`;
- OS/platform;
- render/compute backend actually used (`CPU / CUDA / OPTIX / HIP / METAL / ONEAPI / OTHER` as observed);
- required extensions/add-ons with version/source when they affect the result;
- project `.blend` identity and Source/Derived classification;
- Python script/operator version when automation is part of the evidence.

### Fail closed when

- the scene requires an add-on/operator that is not present;
- the recorded version differs from the version that produced the retained artifact and the difference is not assessed;
- a tool path is assumed from documentation but not available in the actual runtime.

Fail codes:
`HOLD_BLENDER_RUNTIME_UNVERIFIED`, `FAIL_REQUIRED_EXTENSION_MISSING`, `FAIL_RUNTIME_RECEIPT_ARTIFACT_MISMATCH`.

---

## 2｜Version / Compatibility Gate

A `.blend` opening successfully in another Blender version proves only that opening succeeded.

Rules:

1. Lock an authoring version family for each production asset.
2. Before migration, make a recoverable copy of the last-known-good authoring file.
3. Reopen after migration and check geometry, modifiers, node groups, libraries, materials, color management, cameras, render engine, simulations/caches, and output settings.
4. Data-block names, packed/linked data, node/API behavior, render defaults, and I/O behavior are version-sensitive and must not be assumed identical across 4.5/5.x boundaries.
5. A compatibility conversion may create a new Derived/Working revision; it does not silently overwrite the prior Source authority.

Fail codes:
`FAIL_VERSION_MIGRATION_UNREADBACK`, `FAIL_VERSION_SEMANTIC_DRIFT`, `FAIL_OLD_SOURCE_OVERWRITTEN_BY_MIGRATION`.

---

## 3｜Color Pipeline Gate

For any render used in CMF comparison, product review, visual approval, lifecycle comparison, or cross-application handoff record:

- working color space;
- display device;
- view transform;
- look;
- exposure;
- output file color space / encoding;
- HDR or SDR intent;
- OCIO configuration identity when non-default/external;
- compositor/display conversion path when applicable.

Controlled A/B comparisons keep these fixed unless color management itself is the test variable.

### Hard boundaries

- changing AgX / ACES / Filmic / display transform can change appearance without changing geometry or material parameters;
- an ACES-looking result does not prove a physically measured material;
- EXR/HDR output does not prove correct viewing downstream unless the receiving color pipeline is also defined;
- exposure is not a repair for invalid roughness, geometry, normals, or lighting logic.

Fail codes:
`FAIL_COLOR_PIPELINE_UNRECORDED`, `FAIL_COMPARISON_COLOR_PIPELINE_DRIFT`, `FAIL_DISPLAY_TRANSFORM_USED_AS_MATERIAL_REPAIR`.

---

## 4｜Asset / Dependency Recoverability Gate

Blender 5.2 remote Asset Libraries and Blender Packed Data are useful production mechanisms but must preserve OLEANDER recoverability.

Rules:

1. Classify each external dependency: `PACKED / RELATIVE_EXTERNAL / LINKED_LIBRARY / REMOTE_ASSET / CACHE / VIDEO_AUDIO / FONT / OTHER`.
2. If a remote asset is required for a retained deliverable, record its library/source identity and materialize a recoverable local/packed copy when licensing and file semantics allow.
3. Do not make a network-only asset the sole dependency of a CURRENT production file.
4. `Pack Resources` is not assumed to include every external file; maintain an external dependency manifest and reopen test.
5. Linked libraries may be packed, but packed linked data remains linked/read-only semantics; packing is not ownership transfer.
6. Large media/caches that cannot be packed must have stable relative paths or a durable package location.

Fail codes:
`FAIL_NETWORK_ONLY_REQUIRED_DEPENDENCY`, `FAIL_DEPENDENCY_MANIFEST_INCOMPLETE`, `FAIL_PACKED_DATA_ASSUMED_COMPLETE`, `FAIL_LINKED_ASSET_OWNER_TRANSFER`.

---

## 5｜Geometry Nodes / Procedural / Simulation Gate

Procedural convenience does not collapse Source and evaluated geometry.

For Geometry Nodes or procedural modifiers record:

- authoritative input geometry;
- node-group identity/version;
- exposed parameters and deterministic seeds;
- generated/evaluated carrier identity;
- whether instances are preserved or realized and why;
- attribute/material-ID requirements;
- simulation zone/state/cache identity when used;
- dependency on external objects/collections/images/assets.

### 5.2 physics boundary

Node-based cloth/hair physics in Blender 5.2 is an **experimental procedural capability**. OLEANDER may use it for form exploration, animation, contact/behavior visualization, or bounded comparison, but it is not engineering validation, certified cloth behavior, structural proof, ergonomic proof, or manufacturing truth.

If simulation evidence is retained, pin runtime, inputs, solver parameters, frame range, cache/state identity, and output carrier. If repeatability is required, rerun from a cleared/known state.

Fail codes:
`FAIL_PROCEDURAL_SOURCE_EVALUATED_COLLAPSE`, `FAIL_NONDETERMINISTIC_SEED_UNRECORDED`, `FAIL_SIMULATION_STATE_UNBOUND`, `FAIL_VISUAL_SIMULATION_PROMOTED_TO_PHYSICAL_TRUTH`.

---

## 6｜Render Engine / Device Gate

Choose engine by the claim and delivery context, not by habit.

### Cycles
Use when path-traced reflection/transmission/volume behavior or high-quality offline lighting evidence is required. Record samples, adaptive sampling, light paths as relevant, denoise policy, device/backend, and render pass set.

### EEVEE
Use for realtime/interactive previews, fast iteration, or delivery whose intended renderer is EEVEE-class raster/realtime. Record screen/ray-tracing/light-probe settings that materially affect the result.

### Hard boundaries

- `Cycles PASS ≠ physical material measurement`;
- `EEVEE MATCH ≠ Cycles equivalence`;
- changing engine/device/denoise inside an A/B material or surface comparison invalidates comparison lock unless it is the tested variable;
- denoise, compositor effects, glare, depth-of-field, motion blur, or bloom-like treatments may not hide the defect being judged.

Fail codes:
`FAIL_RENDER_ENGINE_CLAIM_MISMATCH`, `FAIL_RENDER_COMPARISON_ENGINE_DRIFT`, `FAIL_POSTPROCESS_CONCEALS_REVIEW_DEFECT`.

---

## 7｜I/O Capability Gate

Do not infer format support from a generic 3D pipeline list.

For each requested import/export route record:

`FORMAT → ACTUAL OPERATOR / EXTENSION → VERSION → OPTIONS → REPRESENTATIVE ROUNDTRIP → LOSS`

Rules:

1. Verify the operator/extension in the executing Blender version before promising delivery.
2. Treat USD, glTF/GLB, FBX, OBJ, Alembic and other routes according to actual runtime capability and consumer needs.
3. If STEP/IGES/CAD-solid interchange is requested, verify the concrete installed bridge/add-on or route through an actual CAD tool; do not imply native Blender support merely because the format is useful elsewhere in the OLEANDER pipeline.
4. Collada/DAE was removed from Blender 5.0; legacy DAE workflows require a verified alternative runtime/extension and explicit loss statement.
5. Round-trip a representative asset for units, axis/origin, hierarchy/instances, normals, materials/textures, cameras/animation, attributes and naming.

Fail codes:
`HOLD_IO_OPERATOR_UNAVAILABLE`, `FAIL_IO_SUPPORT_ASSUMED_NOT_VERIFIED`, `FAIL_ROUNDTRIP_SEMANTIC_LOSS_UNDECLARED`.

---

## 8｜Automation / Background Execution Gate

For scripted or headless Blender work retain:

- exact command/script entry point;
- Blender version/build;
- Python script revision/hash;
- input identities;
- deterministic seeds when applicable;
- stdout/stderr or Blender log;
- exit status;
- produced file list and hashes;
- reopen/readback result.

A process exit code of zero proves execution only. It does not prove the image, model, exchange, or design result.

Fail codes:
`FAIL_AUTOMATION_RECEIPT_MISSING`, `FAIL_OUTPUT_NOT_READBACK`, `FAIL_ZERO_EXIT_PROMOTED_TO_DESIGN_PASS`.

---

## 9｜Minimum Blender Runtime Receipt

A reusable Blender run should be expressible as:

```text
TASK / CLAIM
→ SOURCE + STATE CLASS
→ BLENDER VERSION / BUILD / PLATFORM
→ EXTENSIONS + DEPENDENCIES
→ UNITS / AXES / SCALE
→ PROCEDURAL / SIMULATION STATE
→ COLOR PIPELINE
→ ENGINE / DEVICE / RIG
→ I/O CAPABILITIES USED
→ OUTPUT + HASH + READBACK
→ MACHINE VERDICT
→ EVIDENCE VERDICT
→ DESIGN REVIEW STATUS
→ DOES-NOT-PROVE
```

Machine and evidence gates may pass while Design Quality remains `REVISE / REJECT / HOLD`.

---

## Promotion boundary

This protocol may be promoted into the installed 3D Skill only after:

1. validator/tests pass;
2. representative Blender 5.2 execution demonstrates the receipt can be produced without mutating Source;
3. at least one CMF/render case and one procedural/exchange case exercise the contract;
4. OLEANDER Artifact Review checks the actual outputs where outputs are produced;
5. cross-system CURRENT pointers are updated only after promotion decision.

Does not prove: field truth, engineering approval, physical material properties, manufacturing readiness, reference fidelity, Design KEEP, MAIN KEEP.
