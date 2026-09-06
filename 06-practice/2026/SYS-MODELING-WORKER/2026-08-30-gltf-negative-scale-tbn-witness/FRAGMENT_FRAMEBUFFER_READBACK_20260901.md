# Negative-Determinant TBN → Fragment Framebuffer Readback

Status: **PRACTICE EVIDENCE / BOUNDED PROVEN / NO PROMOTION**

Owner: existing `oleander-3d-pipeline` computer-graphics quality Candidate lineage, PR #468.

## Gap attacked

Previous E02/E07 evidence had already proved numeric tangent-basis reconstruction and a standard/mirrored WebGL fragment witness, but retained this explicit gap:

`negative-determinant-specific fragment parity = HOLD`

This run extends the existing negative-scale witness rather than creating a parallel validator or Skill.

## Artifact / runtime

- Workflow: `OLEANDER 3D glTF Negative Scale TBN Witness`
- Confirmed run: `33460924293` — SUCCESS
- Source carrier: Blender 5.2.0 LTS generated GLB
- Source GLB SHA-256: `666090d558f1dd2488d8b591708634bf9f670ff858a94b63b5ec90b9eefbf400`
- Browser carrier: Chromium / Playwright + Three r179 / WebGL software carrier
- Imported embedded normal texel: `[173,189,230,255]`
- Evidence artifact ID: `9783156980`
- Artifact ZIP digest: `fb1987c87e2b73eb63612c6fbfc0c8aaf9ae9140bcfc39311b2c282326fa99ea`

## Failure discriminator retained

For the negative-determinant object:

- source/target world determinant = `-1`;
- exported `TANGENT.w = +1`;
- raw `B = w * cross(N,T)` remains intentionally wrong;
- raw bitangent error ≈ `179.99958 deg`;
- raw perturbed-normal error ≈ `57.37063 deg`.

The correction remains:

`effective_w = exported_TANGENT.w * sign(det(M_world))`

`B_world = effective_w * normalize(cross(N_world,T_world))`

The effective handedness is therefore `-1` for this witness and the transform-aware numeric TBN path passes without widening the established direction Gates.

## Actual fragment/framebuffer evidence

The viewer now consumes the GLB's imported normal-map texture through an actual diagnostic WebGL fragment shader, renders to a `WebGLRenderTarget`, and reads the target framebuffer with `readRenderTargetPixels`.

### Positive determinant

- expected RGBA8: `[134,130,0,255]`
- observed RGBA8: `[134,130,0,255]`
- max channel delta: `0`
- decoded-direction error ≈ `0.19450 deg`

### Negative determinant

- expected RGBA8: `[121,130,0,255]`
- observed RGBA8: `[121,130,0,255]`
- max channel delta: `0`
- decoded-direction error ≈ `0.19450 deg`

### Discrimination

- expected positive-vs-negative fragment separation ≈ `5.59804 deg`
- observed framebuffer separation ≈ `5.83575 deg`
- separation drift ≈ `0.23771 deg` (`<= 0.5 deg` Gate)

Result:

- `numericTransformAwarePass = true`
- `fragmentFramebufferPass = true`
- `negativeScaleFragmentOutputPasses = true`
- evidence class = `TARGET_RUNTIME_NEGATIVE_SCALE_TBN_PLUS_FRAGMENT_OUTPUT`

## What this proves

Within the tested carrier, stored mesh `TANGENT.w` alone is insufficient under an odd-reflection world transform. Target-runtime validation must account for the transform determinant, and the determinant-aware handedness survives through the tested imported-texture → fragment-shader → render-target → framebuffer chain.

## What this does not prove

Still HOLD:

- non-uniform negative scale;
- nested negative transforms;
- applied/baked mirror vs object-space mirror;
- skinning / animation / morph targets;
- topology or triangulation mutation;
- full Three `MeshStandardMaterial` / production PBR parity;
- hardware GPU / driver parity;
- other engines/importers;
- Design KEEP, physical material truth, engineering/manufacturing approval.

`WORKFLOW SUCCESS ≠ UNIVERSAL ENGINE RULE ≠ DESIGN KEEP`.
