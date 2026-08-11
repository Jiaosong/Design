# 2026-08-11｜Blender｜Technique Pattern → Node Group → Real Workflow

## Status

`BLENDER 5.2 VERIFIED / NODE GROUP REUSABLE / REAL-WORKFLOW VALIDATION COMPLETE WITH W01 PRESET NOT PROMOTED`

This record promotes the diagnostic-pass C Track patterns C01 / C03 / C04 / C05 / C06 / C07 / C08 / C09 into reusable parameterized Shader Node Groups, then tests those groups in eight workflow contexts.

## Runtime authority

- Blender: `5.2.0 LTS`
- build: `fbe6228777e7`
- renderer: Cycles
- official Linux archive SHA-256, verified before execution: `96f6c181a30f4950607839dc84d42a354b250d8a0231b098b59b7bc69c351c48`
- promoted evidence run: GitHub Actions `31467648234`
- job: `93703798641`
- artifact: `9092213075`
- artifact digest: `sha256:2a8e408ef4f83216cba3e514efb02a85974ca59bf3d7d4860faaad0a71b55c34`

## Reusable node groups

1. `OL_SHD_C01_ShapeControl_v1`
2. `OL_SHD_C03_RepetitionCells_v1`
3. `OL_SHD_C04_WhiteNoiseCell_v1`
4. `OL_SHD_C05_ComposeFields_v1`
5. `OL_SHD_C06_SpaceManipulation_v1`
6. `OL_SHD_C07_WaveField_v1`
7. `OL_SHD_C08_VoronoiField_v1`
8. `OL_SHD_C09_GaborField_v1`

Interface rule: semantic inputs, defaults, UI ranges, explicit internal constraints where mathematically required. UI Min/Max is not treated as a clamp. Gabor texture anisotropy remains distinct from Principled BSDF anisotropy.

## Workflow review

| Workflow | Pattern chain | Decision |
|---|---|---|
| W01 Wall | C01 + C08 + C05 | `INTEGRATION PASS / PRESET NOT PROMOTED` — Blender wiring and response are valid, but the wall preset remains visually too weak to promote. |
| W02 Wood | C06 + C07 + C09 + C05 | `PASS` |
| W03 Stone | C08 + Noise + C05 | `PASS AFTER REVISION` — increased topology / roughness / bump readability; procedural study only, not physical stone calibration. |
| W04 Textile | C09 + C07 + C05 | `PASS` |
| W05 Facade | C03 + C04 + C05 | `PASS` — mullion/transom geometry is context only, not constructability validation. |
| W06 Landscape | C06 + C08 + C03 + C04 + C05 | `PASS AFTER GEOMETRY-CONTEXT REVISION` — first run ground occluded low terrain and created floating islands; corrected in review 2. |
| W07 Brand | C03 + C04 + C01 + C05 | `PASS AFTER COMPOSITION REVISION` — replaced uncontrolled random blocks with sparse deterministic dots + central ring. |
| W08 Motion | C07 Phase | `PASS` — F001/F013/F025 show real temporal change; review-2 frame differences change about 70.6–71.0% of pixels by >5 levels. |

## Failure chain retained

- Run `31466376857`: build/render succeeded; Post-Review rejected initial W01 / W03 / W06 / W07 presets.
- Run `31467398406`: payload reconstruction failed before Blender; not visual evidence.
- Run `31467648234`: corrected review-2 builder; all builds/renders/artifact upload succeeded. This is the promoted binary evidence.
- Run `31468294571`: later wall-strengthening payload reconstruction failed before Blender; not visual evidence and does not supersede the promoted review-2 artifact.

## Evidence boundary

This PASS proves only:

- Blender 5.2 node/API compatibility;
- reusable Node Group interface behavior;
- procedural signal-role separation;
- cross-workflow visual/structural migration;
- controlled Post-Review and revision history.

It does **not** prove measured CMF, real wood/stone/textile material properties, manufacturing, facade construction, structural performance, ecological/GIS truth, field performance, or user validation.

## Archive

- Notion master record: `2026-08-11｜Blender｜Technique Pattern → Node Group → Real Workflow`
  - https://app.notion.com/p/3b9b86be5c4781dfb014e904e06fd1af
- Google Drive folder:
  - https://drive.google.com/drive/folders/11uxrdZdg0v3J5xD0_vl388CEXM_4J6e9
- Raw Blender evidence ZIP ID: `1S1pqzD51LqEE3ncNKr9uU5aNN52WW0wJ`
- Final package ZIP ID: `1E2-ZkIFafpXVZYZ5qFwvSxkAbzSc86OO`
- Reusable binary inside evidence package: `OLEANDER_Procedural_NodeGroups_v1.0.blend`
- Draft PR: https://github.com/Jiaosong/Design/pull/47 — mergeable, intentionally not auto-merged.

## Next gate

`Validated Node Groups → Asset Catalog / Naming / Debug Contract → real evidence-backed material/project calls → Role / PBR / Geometry / Reality Gate`
