# OLEANDER 3D Production Practice Evidence Matrix — 2026-08-30

Status: **CANDIDATE EVIDENCE INDEX / NO MATURITY BY ASSOCIATION**

Purpose: prevent tutorial/documentation knowledge, static practice, historical runtime evidence, current native-runtime evidence and downstream target-runtime evidence from collapsing into one maturity label. This index does not replace the canonical Notion objects.

## Evidence classes

- `DOC_TRANSLATED` — official/tutorial/documentation knowledge translated; no native artifact practice.
- `STATIC_PRACTICE` — a real reasoning/data/contract exercise exists but the named DCC/runtime was not actually executed.
- `HISTORICAL_NATIVE` — native DCC/runtime was executed and receipts/hashes survive, but current binary artifact is not re-openable/recovered in this review.
- `RECOVERED_NATIVE` — native artifact bytes were recovered/re-opened in this review and actual preview/readback is available.
- `TARGET_RUNTIME` — exchange artifact has been imported/opened in its actual downstream runtime with semantic/visual/profiling readback.

These are evidence classes, not quality scores.

`RECOVERED_NATIVE ≠ DESIGN PASS`, `TARGET_RUNTIME ≠ PERFORMANCE PASS`, and `DOC_TRANSLATED ≠ UNIMPORTANT`.

## Current matrix

| Route | Canonical knowledge | Best current practice evidence | Native/runtime state | Current maturity interpretation | Next discriminator |
|---|---|---|---|---|---|
| Blender polygon/SubD / surface control | Modeling Essence + SubD + Differential Geometry + Representation Bandwidth | `PRAC-20260830-3D-01` / Porsche 992 V49–V64 | `RECOVERED_NATIVE` Blender 5.2; V58/V59 `.blend` + renders recovered | M6 only for the seven bounded practiced propositions; Porsche design remains REJECT | same-source Rhino/NURBS comparison; aperture-architecture repair |
| Blender/Cycles material–reflection | Lighting/Radiometry + BSDF + Color + Render Production | `PRAC-20260830-3D-02` / XJ01-06B | `HISTORICAL_NATIVE`; artifact `9109574737` expired | M6 only for controlled-comparison/diagnostic-lighting propositions; Physical CMF HOLD | current 9-frame rerun or physical-sample correspondence |
| Blender Geometry Nodes | Blender Production + `EVD-DCC-BLENDER-GEOMETRY-NODES-5_2-001` | `PRAC-20260830-3D-03`; Preserve/Realize A/B `.blend`, PNG, GLB and receipts; run `33306247098` | `RECOVERED_NATIVE` Blender 5.2; native reopen + explicit evaluated-mesh GLB bake/roundtrip | M6 only for fields, named-attribute domain/type, instance policy, native reopen and export-bake/graph-loss propositions | performance sensitivity sweep; production generator with non-synthetic source |
| Rhino NURBS/SubD | Rhino Surface Modeling + Rhino 8 tools + Surface Continuity | no recovered `.3dm` benchmark | `DOC_TRANSLATED / NATIVE RUNTIME HOLD` | M4/M5 only | same-source product surface with CV/span/continuity/zebra and STEP/reopen evidence |
| Grasshopper | Grasshopper Parametric + `PRAC-20260809-01` | static Data Tree handoff; page explicitly says Rhino/GH runtime not executed | `STATIC_PRACTICE / RUNTIME HOLD` | existing M6 property must not be interpreted as native-runtime M6; CP2/CP4 OPEN | actual `.gh/.3dm` run, tree readback, bake identity and reopen |
| Houdini | Houdini Procedural + Houdini 21 evidence | no recovered `.hip` runtime artifact | `DOC_TRANSLATED / NATIVE RUNTIME HOLD` | M4/M5 only | SOP/attribute/VEX/HDA native practice with seed/schema/output/cache/USD readback |
| Maya | Maya 2027 evidence + DCC Polygon/SubD | no recovered `.ma/.mb` runtime artifact | `DOC_TRANSLATED / NATIVE RUNTIME HOLD` | M4 only | Quad Draw/retopo or SubD task with native reopen and held-out render |
| 3ds Max | 3ds Max 2027 evidence + DCC Polygon/SubD | no recovered `.max` runtime artifact | `DOC_TRANSLATED / NATIVE RUNTIME HOLD` | M4 only | modifier/retopo/array task with native stack readback |
| SketchUp | SketchUp Spatial + 2026 native evidence | no recovered `.skp` runtime artifact | `DOC_TRANSLATED / NATIVE RUNTIME HOLD` | M4 only | components/solids/section or spatial massing task with native reopen/export |
| Autodesk Fusion | Modeling Essence + Parametric Design + Fusion evidence | no recovered Fusion native model | `DOC_TRANSLATED / PROPRIETARY RUNTIME HOLD` | M4 only; FreeCAD native practice does not establish Fusion parity | named-parameter feature/assembly change sweep + native Fusion reopen + STEP comparison |
| FreeCAD parametric CAD | Modeling Essence + Parametric Design + `EVD-CAD-FREECAD-1_1-20260830-001` | `PRAC-20260830-3D-04`; FreeCAD 1.1.3 `.FCStd`, STEP, parameter sweep and reopen receipts | `RECOVERED_NATIVE` FreeCAD 1.1.3 + STEP roundtrip | M6 only for named-parameter/expression dependency, recompute sweep, native reopen and STEP geometry-vs-history-loss propositions | datum/reference-change robustness, Sketcher constraints, assembly/fit; Fusion remains separate HOLD |
| High→low tangent normal mechanics | Surface Detail + Texture Map Processing + Shading/Texturing | `PRAC-20260830-3D-06`; run `33306786418` | `RECOVERED_NATIVE` Blender 5.2; selected-to-active tangent bake + `.blend`/external texture reopen | M6 for bake mechanics, UV carrier, Non-Color data semantics and tangent Normal Map wiring only. Artifact Review rejects reading this as macro-shape equivalence | correct spatial-frequency representation; cross-runtime tangent semantics |
| Surface-detail representation bandwidth | Texture Map Processing + Surface Detail | `PRAC-20260830-3D-08`; run `33308580990` | `RECOVERED_NATIVE`; macro geometry + meso tangent bake, native reopen, actual preview comparison | M6 for bounded macro/meso representation choice: silhouette IoU `0.9998729`; baked RGB MAE `0.0010110` vs plain `0.0020522` (~50.7% reduction) | cross-engine tangent basis; mirrored UV; displacement/parallax A/B; production texel-density budget |
| Blender→GLB→browser target runtime | glTF PBR Interchange + Runtime TA | `PRAC-20260830-3D-05`; run `33306786373` | `TARGET_RUNTIME` Chromium + WebGL2 + Three r179; 1 mesh / 1 material / 3980 triangles | M6 for exact baked-GLB identity, real browser load/readback, material existence and axis-extent mapping; not a performance or Design PASS | signed coordinate mapping, tangent/normal semantics, runtime profiling/device matrix |
| Signed coordinate / handedness exchange | glTF PBR Interchange + Runtime TA | `PRAC-20260830-3D-07`; run `33308581065` | `TARGET_RUNTIME`; four asymmetric named witnesses | M6 for Blender `(x,y,z) → glTF/Three (x,z,-y)` signed static transform and determinant `+1` handedness preservation in declared exporter/runtime pair | tangent/normal orientation; negative scale/mirror; animation/camera/light transforms |
| glTF tangent basis / mirrored UV | glTF PBR Interchange + Shading/Texturing | native/browser witness currently executing from branch head `22d5caa453f4a7622e158f25accb1f856c461d92` | `EXECUTING / NO PROMOTION YET` | no M6 until Blender bitangent-sign → GLB `TANGENT.w` → Three tangent attribute is read back per named object | finish `UV_STANDARD` / `UV_MIRRORED` semantic witness and inspect actual target artifact |
| Bio–Math computational form | 18 L6 Bio–Math objects | theory/evals + Porsche surface-control subset + GN sinusoidal field/instance subset | `DOC_TRANSLATED + PARTIAL PRACTICE` | parent remains M5; no blanket M6 | controlled GN/Houdini/Rhino experiments for topology/TPMS/L-system/spectral claims |

## Required promotion contract

Before any row moves to native-practice evidence, capture:

`SOURCE ID → SOFTWARE/VERSION → NATIVE MASTER → INPUT/REFERENCE → PRIMARY VARIABLE → LOCKED VARIABLES → FAILURE/SENSITIVITY SWEEP → ACTUAL OUTPUT → REOPEN/ROUNDTRIP → VISUAL/SEMANTIC READBACK → ARTIFACT REVIEW → HASH/COMMIT → HOLDS`.

For procedural systems additionally record:

`PARAMETER SCHEMA → SEED → ATTRIBUTE/DATA DOMAIN → INSTANCE/REALIZE POLICY → OUTPUT COUNTS/BOUNDS → CACHE/EXPORT STATE`.

For NURBS additionally record:

`DEGREE → CV/SPAN/KNOT STRUCTURE → BOUNDARY MATCH → G0/G1/G2/G3 CLAIM → ZEBRA/CURVATURE → TRIM STATE → TESSELLATION/STEP REOPEN`.

For parametric CAD additionally record:

`DATUM/REFERENCE → NAMED PARAMETERS → CONSTRAINT GRAPH → FEATURE DEPENDENCY → RECOMPUTE → CHANGE SWEEP → SOLID VALIDITY → EXCHANGE/REOPEN`.

For cross-runtime Technical Art additionally record:

`DCC MASTER → EXPORTER VERSION/SETTINGS → EXCHANGE HASH → TARGET IMPORT SETTINGS → UNITS/AXIS → NORMAL/TANGENT/UV/MATERIAL → RUNTIME PROFILE → SCREENSHOT/CAPTURE → KNOWN LOSS`.

For normal/detail representation additionally record:

`SPATIAL FREQUENCY → SILHOUETTE/PARALLAX REQUIREMENT → GEOMETRY/DISPLACEMENT/NORMAL/BUMP CHOICE → UV/TANGENT BASIS → BAKE CAGE → TARGET PIXELS → VISUAL DELTA → CROSS-RUNTIME READBACK`.

## Governance rule

Do not upgrade a parent theory because one child practice passed. Promotion is proposition-scoped and evidence-scoped.

Do not downgrade a useful static practice merely because native runtime is absent; instead preserve its actual claim boundary. Conversely, a database property reading `M6 PRACTICED` must never be read as proof of native DCC execution when the practice body explicitly says runtime was not executed.

A green workflow is execution evidence, not automatic professional/design approval.

`MATURITY LABEL < ACTUAL EVIDENCE CONTRACT` whenever the two disagree.
