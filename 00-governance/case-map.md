# Case Map

| Canonical Case | Current P2 Project ID | Legacy / historical aliases | Application Mapping emphasis | Current Status |
|---|---|---|---|---|
| C01 / 一脉广渡 | `PRJ-C01-YIMAI-GUANGDU` | CASE/GD; old 03; P00 | Culture + Spatial = PRIMARY; Business + IP = SUPPORTING | RESEARCH + PROPOSAL / EVIDENCE REVIEW |
| C02 / 忘也 Daylily | `PRJ-C02-DAYLILY` | CASE/DY; old 03C | Business + IP + Spatial = PRIMARY; Culture = CONDITIONAL | PROTOTYPED / TEST PLANNED / NOT RUN |
| C03 / The Light Collection | `PRJ-C03-LIGHT-COLLECTION` | CASE/LC; old 03D | IP = PRIMARY; Business = SUPPORTING | VISUALIZED / SAMPLE TEST PENDING |
| C04 / 清江石书｜红花峰林十三印 | `PRJ-C04-QINGJIANG-SHISHU` | 清江十三印 / 清江三十印; historical QJ13 / C04-WS-* / C04-VAL-* references | Culture + Spatial = PRIMARY; IP + Business = SUPPORTING / CONDITIONAL | RESEARCH + PROPOSAL / WEB EVIDENCE REVIEW / FIELD NOT RUN |

## Namespace authority

- `C01/C02/C03/C04` are **Case Axis root IDs only**. A bare `Cnn` does not substitute for a P2 Project ID.
- The writable Project Registry now separates `Project ID｜项目ID` from `Case ID｜案例ID`. Current Project Axis routing resolves the explicit Project ID plus `P0–P4` project level first; Case ID is an independent context/filter axis.
- Legacy `项目编号`, workflow codes, titles, paths, filenames, and historical aliases may still contain bare `Cnn`; they are compatibility/provenance only and are not Current Project ID authority.
- Application Mapping describes where case knowledge/design work is applied; it does not define Knowledge Architecture ownership. Knowledge Objects must be located separately through `Domain / exact L0–L7 level`.
- New case-scoped claims use `CLM-C01-NNN`, `CLM-C02-NNN`, `CLM-C03-NNN`, `CLM-C04-NNN`.
- Historical `CASE_GD_Public_Claim_Matrix.csv` IDs `C01–C05` are Legacy Claim IDs and map to `CLM-C01-001–005`.
- Historical case-prefixed project IDs such as `C04-WS-* / C04-VAL-*` are migration residues. Preserve immutable references, but repair writable project-registry identities in place rather than creating duplicate projects.
- Legacy labels never become current authority through search ranking, filename recency, or copy duplication.

## C04 Project Axis migration status

Current explicit identities already recovered in the writable Project Registry:

- P2: `PRJ-C04-QINGJIANG-SHISHU`
- P3 Governance / Site: `PRJ-C04-GOV-SITE`
- P3 Experience / Spatial: `PRJ-C04-EXPERIENCE-SPATIAL`
- P3 Digital / Interaction: `PRJ-C04-DIGITAL-INTERACTION`
- P4 Runtime / Responsive validation: `PRJ-C04-RUNTIME-RESPONSIVE`

The P3 Visual Reading row retains Case ID `C04`, but its new explicit Project ID is still **HOLD** at the current registry-write checkpoint; historical `C04-WS-04` therefore remains workflow/legacy compatibility only and must not be treated as a repaired Project ID until the registry write succeeds.
