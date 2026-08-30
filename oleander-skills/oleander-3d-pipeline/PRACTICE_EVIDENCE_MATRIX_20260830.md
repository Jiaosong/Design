# OLEANDER 3D Production Practice Evidence Matrix — 2026-08-30

Status: **CANDIDATE EVIDENCE INDEX / NO MATURITY BY ASSOCIATION**

Purpose: prevent tutorial/documentation knowledge, static practice, historical runtime evidence and current native-runtime evidence from collapsing into one maturity label. This index does not replace the canonical Notion objects.

## Evidence classes

- `DOC_TRANSLATED` — official/tutorial/documentation knowledge translated; no native artifact practice.
- `STATIC_PRACTICE` — a real reasoning/data/contract exercise exists but the named DCC/runtime was not actually executed.
- `HISTORICAL_NATIVE` — native DCC/runtime was executed and receipts/hashes survive, but current binary artifact is not re-openable/recovered in this review.
- `RECOVERED_NATIVE` — native artifact bytes were recovered/re-opened in this review and actual preview/readback is available.
- `TARGET_RUNTIME` — exchange artifact has been imported/opened in its actual downstream runtime with semantic/visual/profiling readback.

These are evidence classes, not quality scores.

`RECOVERED_NATIVE ≠ DESIGN PASS` and `DOC_TRANSLATED ≠ UNIMPORTANT`.

## Current matrix

| Route | Canonical knowledge | Best current practice evidence | Native runtime state | Current maturity interpretation | Next discriminator |
|---|---|---|---|---|---|
| Blender polygon/SubD / surface control | Modeling Essence + SubD + Differential Geometry + Representation Bandwidth | `PRAC-20260830-3D-01` / Porsche 992 V49–V64 | `RECOVERED_NATIVE` Blender 5.2; V58/V59 `.blend` + renders recovered | M6 only for the seven bounded practiced propositions; Porsche design remains REJECT | same-source Rhino/NURBS comparison; aperture-architecture repair |
| Blender/Cycles material–reflection | Lighting/Radiometry + BSDF + Color + Render Production | `PRAC-20260830-3D-02` / XJ01-06B | `HISTORICAL_NATIVE`; artifact `9109574737` expired | M6 only for controlled-comparison/diagnostic-lighting propositions; Physical CMF HOLD | current 9-frame rerun or physical-sample correspondence |
| Blender Geometry Nodes | Blender Production + `EVD-DCC-BLENDER-GEOMETRY-NODES-5_2-001` | no native repository artifact located in 2026-08-30 search | `DOC_TRANSLATED` | M4/M5 only; no M6 promotion | real `.blend` with field/attribute/domain/instance contract, output counts/bounds and export readback |
| Rhino NURBS/SubD | Rhino Surface Modeling + Rhino 8 tools + Surface Continuity | no recovered `.3dm` benchmark | `DOC_TRANSLATED` | M4/M5 only | same-source product surface with CV/span/continuity/zebra and STEP/reopen evidence |
| Grasshopper | Grasshopper Parametric + `PRAC-20260809-01` | static Data Tree handoff; page explicitly says Rhino/GH runtime not executed | `STATIC_PRACTICE / RUNTIME HOLD` | existing M6 property must not be interpreted as native-runtime M6; CP2/CP4 OPEN | actual `.gh/.3dm` run, tree readback, bake identity and reopen |
| Houdini | Houdini Procedural + Houdini 21 evidence | no recovered `.hip` runtime artifact | `DOC_TRANSLATED` | M4/M5 only | SOP/attribute/VEX/HDA native practice with seed/schema/output/cache/USD readback |
| Maya | Maya 2027 evidence + DCC Polygon/SubD | no recovered `.ma/.mb` runtime artifact | `DOC_TRANSLATED` | M4 only | Quad Draw/retopo or SubD task with native reopen and held-out render |
| 3ds Max | 3ds Max 2027 evidence + DCC Polygon/SubD | no recovered `.max` runtime artifact | `DOC_TRANSLATED` | M4 only | modifier/retopo/array task with native stack readback |
| SketchUp | SketchUp Spatial + 2026 native evidence | no recovered `.skp` runtime artifact | `DOC_TRANSLATED` | M4 only | components/solids/section or spatial massing task with native reopen/export |
| Autodesk Fusion | Modeling Essence + Parametric Design + Fusion evidence | no recovered Fusion native model | `DOC_TRANSLATED` | M4 only | named-parameter feature/assembly change sweep + STEP/native reopen |
| FreeCAD | Modeling Essence + Parametric Design + FreeCAD evidence | no recovered FreeCAD native model | `DOC_TRANSLATED` | M4 only | Body/Sketch/Datum/Feature recompute + reference-change sweep + STEP reopen |
| Surface detail / texture / bake | Surface Detail + Shading/Texturing + Substance pipeline | XJ01 optical practice does not cover high→low bake correctness | `DOC_TRANSLATED / PARTIAL HISTORICAL` | do not infer bake M6 from material render | actual high/low + cage + normal/tangent/UV bake + target render readback |
| Interchange / Technical Art | glTF PBR Interchange + Runtime TA | Qingjiang model references exist in project history, but no canonical GLB/FBX artifact was located by repo/Notes search in this pass | `HOLD / SOURCE RECOVERY` | no M6 promotion | recover exact GLB/FBX identity/hash, exporter/importer settings and browser/engine readback |
| Bio–Math computational form | 18 L6 Bio–Math objects | theory/evals only; Porsche supports only surface-control subset | `DOC_TRANSLATED + PARTIAL PRACTICE` | parent remains M5; no blanket M6 | controlled GN/Houdini/Rhino experiments for topology/field/TPMS/L-system/spectral claims |

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

## Governance rule

Do not upgrade a parent theory because one child practice passed. Promotion is proposition-scoped and evidence-scoped.

Do not downgrade a useful static practice merely because native runtime is absent; instead preserve its actual claim boundary. Conversely, a database property reading `M6 PRACTICED` must never be read as proof of native DCC execution when the practice body explicitly says runtime was not executed.

`MATURITY LABEL < ACTUAL EVIDENCE CONTRACT` whenever the two disagree.
