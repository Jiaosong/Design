# OLEANDER Artifact Review System v1.0

Status: ACTIVE
Date: 2026-08-11
Scope: All design, technical, data, code, GIS, visual, documentation, presentation and release outputs.

## Core structure

All reviews are split into two layers:

- **A｜Common Review**: AR-G01—AR-G10, mandatory for every file.
- **B｜Specific Review**: AR-S01—AR-S09, triggered by file/object type.

A file may be marked `POST-REVIEW PASS` only after **Common PASS + all triggered Specific PASS**. A package may be marked `PACKAGE RELEASE PASS` only after every file-level gate passes and AR-S09 passes.

Historical results not rerun under v1.0 remain **LEGACY REVIEW RESULT** and do not automatically inherit v1.0 PASS.

## A｜Common Review

| ID | Gate | Required check |
|---|---|---|
| AR-G01 | Identity & Naming | project ID, filename, case ID, version, date, naming system |
| AR-G02 | Version & Status | CURRENT / REVIEW / PENDING / VOID / SUPERSEDED |
| AR-G03 | Completeness | files, pages, fields, dependencies, references, attachments |
| AR-G04 | Internal Consistency | names, numbers, units, status and conclusions agree internally |
| AR-G05 | Cross-file Consistency | parameters, IDs, versions and status agree across the package |
| AR-G06 | Evidence & Truth | FACT / INFERENCE / HYPOTHESIS / PENDING / UNKNOWN are separated |
| AR-G07 | Open & Integrity | artifact can actually be opened, parsed and exported |
| AR-G08 | Reproduction | rerun/re-export produces an explainably consistent result |
| AR-G09 | Change Traceability | reason, change, superseded state and re-review are recorded |
| AR-G10 | Final Artifact Review | after automatic QA, reopen the final artifact and review it |

### AR-G10 must review these independently

- Visual hierarchy
- Boundary
- **Occlusion / 遮挡**
- Clearance
- Geometry ↔ Dimension
- **Scale / Proportion: technical scale + component/construction proportion**
- View Appropriateness
- Cross-view Consistency
- Construction / Functional Logic
- Evidence / PENDING
- Export / Reproduction

`AUTO QA = 0 error` is never equivalent to final artifact PASS.

Hard FAIL conditions cannot be averaged away by a score: critical occlusion, scale error, geometry-dimension mismatch, wrong view, cross-view conflict, construction/functional logic error, false evidence claim, or unreadable/corrupt artifact.

## B｜Specific Review

### AR-S01｜Drawing Review
SVG, DXF, CAD exports, technical PDF/PNG. Review hierarchy, text/graphic boundaries, occlusion, clearance, geometry-dimension consistency, true scale, construction proportion, view appropriateness, cross-view consistency, drafting semantics, construction logic, constructability and export integrity.

### AR-S02｜Model Review
OBJ, STL, GLB and native 3D models. Review units, origin/axis, geometry integrity, topology, normals, non-manifold/self-intersection, hierarchy, collision/clearance, assembly, parameter consistency, 2D consistency, export fidelity, reopen and reproduction.

### AR-S03｜Data Review
JSON, CSV, XLSX, parameter matrices and QA data. Review schema, type, unit, range, missing, duplicate, formula, dependency, outlier, evidence status and artifact consistency. Data-to-artifact mismatch is FAIL.

### AR-S04｜Code / Parametric Review
Python, Grasshopper, generators, QA scripts and rule engines. Review input/output contract, units, dependencies, boundary conditions, invalid input, error handling, determinism, parameter traceability, version dependency and reproduction. **Code PASS ≠ Generated Artifact PASS.**

### AR-S05｜GIS Review
SHP, GeoJSON, GPKG, QGIS/ArcGIS and GIS outputs. Review CRS/EPSG, projection/datum, source/date, geometry validity, joins, buffer/distance units, NoData, classification, legend, scale bar, north arrow, spatial accuracy and evidence boundary.

### AR-S06｜Visual / CMF Review
PNG/JPG, KV, posters, product/brand visuals and CMF boards. Review composition, hierarchy, alignment, occlusion, proportion, product form, Color × Material × Finish × Texture × Process, manufacturability, brand continuity, typography and export.

### AR-S07｜Documentation Review
Markdown, README, REVIEW, REVISION, Notion and DOCX. Review naming, version, taxonomy, terminology, fact/method/inference/hypothesis/unknown, evidence, source, links, legacy mapping, file references and status. Include **Claim Audit**: DONE/PASS/synced/verified claims require actual evidence.

### AR-S08｜Presentation Review
PPTX and presentation PDF. Review page grid, hierarchy, typography, crop, occlusion, density and alignment; Story/Argument/Evidence/Decision; and cross-page consistency of parameters, figure IDs, scale, color, legend and conclusions.

### AR-S09｜Release Package Review
ZIP, MANIFEST, GitHub branch, Drive folder and final directory. Review completeness, structure, naming, CURRENT version, VOID/SUPERSEDED, manifest/SHA256, dependencies, unzip/open test, reproduction and Notion/GitHub/Drive status consistency.

For any release package containing native binaries, canonical models, render/CAD scenes or other non-trivial production binaries, **AR-S09 additionally requires `PAP-G0—PAP-G6 PASS` under `production-asset-persistence-gate-v1.0.md`.** A checksum, preview, File Library metadata record, temporary `/mnt/data` path or expiring workflow artifact is not a durable binary copy.

## Production Asset Persistence dependency

Canonical gate: [`production-asset-persistence-gate-v1.0.md`](production-asset-persistence-gate-v1.0.md)

The production persistence chain is:

`package → hash → durable upload → independent retrieval → SHA/open verification → PERSISTENCE PASS → AR-S09 PASS → Promotion / Archive`

Required production quartet when applicable:

- native source / authoring binary;
- canonical model / interchange authority;
- production ZIP;
- checksum records.

At least one **real, independently retrievable binary copy** of every required asset must exist in a qualified durable store. Notion/GitHub text, filenames, hashes, previews, local runtime files and expiring workflow artifacts are evidence records only and cannot satisfy persistence by themselves.

## Status flow

`REVIEW PENDING → NEEDS REVISION / FAIL → correction → rerun QA → reopen final artifact → POST-REVIEW PASS`

For packages with triggered production binaries:

`POST-REVIEW PASS → PERSISTENCE PENDING / FAIL → PAP-G0—PAP-G6 PASS → AR-S09 PASS → PACKAGE RELEASE PASS`

Only after all triggered gates pass may a package become `PACKAGE RELEASE PASS`.
