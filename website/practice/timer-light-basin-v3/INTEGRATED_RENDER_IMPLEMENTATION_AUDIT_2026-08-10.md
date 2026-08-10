# v3.3 Integrated Render Implementation Audit｜2026-08-10

**Result:** `IMPLEMENTATION_MATCH_PASS`

Formal Hero and CMF both bind the canonical `timer_100_pbr.glb`; locked material, grazing-light, metal-knob, contact-shadow and color/post parameters are present in the production modules. This is source/runtime-binding evidence, not full-browser visual-regression evidence.

## Checks
- canonical_glb_sha_match: **PASS**
- hero_and_cmf_bind_canonical: **PASS**
- housing_roughness_0_55: **PASS**
- diffuser_profile_roughness_0_42: **PASS**
- diffuser_profile_transmission_0_30: **PASS**
- diffuser_profile_ior_1_49: **PASS**
- knob_metalness_1_roughness_0_27: **PASS**
- hero_shadow_0_22_blur_5_2: **PASS**
- top_grazing_key_locked: **PASS**
- knob_focus_locked: **PASS**
- linear_hdr_no_renderer_tonemap: **PASS**
- agx_last_stage: **PASS**
- halffloat_post_and_shadow: **PASS**
- viewer_geometry_not_mutated: **PASS**
- orientation_scale_only: **PASS**
- deps_exact: **PASS**
- local_refs_exist: **PASS**

## Canonical binding
- canonical GLB: `assets/pbr/timer_100_pbr.glb`
- SHA-256: `900e02510ab6b2b5176aa3723dba7981700dc79b5f217dbe481844a534ed7c66`
- Hero and CMF both bind this canonical model.
- `PhotographyViewer.js` changes orientation / display scale / ground normalization only; no geometry mutation was found.

## Integrated browser gate
`BLOCKED_IN_CURRENT_RUNTIME_POLICY`: local Chromium itself establishes WebGL under Xvfb/SwiftShader, but navigation to local HTTP is replaced by `chrome-error://chromewebdata/`; CDP `setDocumentContent` does not execute the page module graph. Therefore the complete-page visual QA is not reported as PASS.

This blocker is separate from the already locked four-gate photography calibration. It is a deployment/integration execution limitation, not evidence that the locked render profile failed.

## Boundary
Photography render lock remains visualization-only; engineering validation stays NOT RUN.
