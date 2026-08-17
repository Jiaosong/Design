# C04 R06 Drawing v1.4｜AR-G + AR-S01 Producer Self-Check

Project: `PRJ-C04-QINGJIANG-SHISHU`  
Object: `C23-R06-GA-SECTION-DETAIL`  
Artifact: `C04_R06_GA_SECTION_DETAIL_v1_4_CANDIDATE.svg`  
Producer status: **`EXECUTED / SELF-CHECKED / REVIEW PENDING`**  
Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`

> This is a producer self-check, not an independent design verdict. Under `OLEANDER_INDEPENDENT_DESIGN_VERDICT_POLICY_v1.0`, this file does not assign `PIXEL KEEP`, `MAIN KEEP` or `PROFESSIONAL FINISH PASS`.

## Existing-Mature benchmark used

Compared against PR #133 source candidate:
`R06_SKILL_DRIVEN_v1_3/02_R06_GA_SECTION_DETAIL_v1_3.svg`  
Source PR head: `d63386d7b6b00f93cbc82a0e7f81622d4989fc53`  
Source blob: `5481e1deeb71b8920ff97923a8c7b34ffc533a04`

Latest PR #133 independent review remains authoritative for candidate disposition:
- GA / section / detail = `KEEP / SUPPORT TECHNICAL`;
- overall R06 v1.3 = `NOT MAIN KEEP YET`;
- v1.7 may currentize explicit component geometry where conflicting;
- no Field / Engineering / Promotion inference.

## Material drawing delta

v1.4 changes **representation and drawing semantics only**:

1. Removes card-wall / presentation-panel framing and uses one continuous technical sheet.
2. Registers plan, elevation and section under a common datum / centerline system.
3. Adds explicit A–A section cut in plan and stable IDs: `C23-R06-S01`, `C23-R06-AX01`, `C23-R06-D01`.
4. Separates cut / outline / detail / annotation / center / dimension line hierarchies.
5. Converts potentially misleading `LOCKED` dimension wording into `[C] = CONCEPT INTERFACE DIMENSION`.
6. Keeps `1200 / 160 / 840 c-c / 975 / 220×180×12 / 150×110 / 4×M16 / RHS 60×40×4` only from the reviewed v1.7 lineage; no new numeric geometry added.
7. Makes the 1700 reference person visible in elevation and the lean/contact/view relation visible in section.
8. Makes the use boundary explicit: interpret / lean / read / short recovery; **not sole fall-protection / guard authority**.
9. Makes the verified-RC-only condition explicit at the post-base detail and blocks anchor issue when substrate evidence is absent.
10. Adds professional title block / status / scale / units / truth boundary without implying plotted scale or construction issue.

## AR-G01–G10 self-check

- `AR-G01 Identity & Naming`: self-check PASS — project, object, sheet IDs and revision visible.
- `AR-G02 Version & Status`: self-check PASS — `v1.4 CAND / REVIEW PENDING / NO PROMOTION` visible.
- `AR-G03 Completeness`: self-check PASS for this single-sheet delta — plan, elevation, section, exploded hierarchy, RC-condition detail, general notes, title block.
- `AR-G04 Internal Consistency`: self-check PASS — repeated interface dimensions and component names agree across views.
- `AR-G05 Cross-file Consistency`: self-check PASS against PR #133 reviewed v1.7 explicit geometry lineage; no generic `SEC-A = R06` shorthand used.
- `AR-G06 Evidence & Truth`: self-check PASS — `[C]`, FIELD OPEN, engineer-open, verified-RC-only and NTS boundaries are explicit.
- `AR-G07 Open & Integrity`: self-check PASS — XML parsed; Inkscape reopened and rendered the final SVG at `1684×1191`.
- `AR-G08 Reproduction`: self-check PASS for deterministic SVG reopen/export in the current runtime; this does not prove cross-runtime font equivalence.
- `AR-G09 Change Traceability`: self-check PASS — Owner Receipt and source lineage recorded before repository artifact write.
- `AR-G10 Final Artifact Review`: producer readback completed at full-sheet and near-read scale; **independent review still pending**.

## AR-S01 Drawing self-check

### Geometry ↔ Dimension
No self-detected mismatch among the inherited concept interfaces. `[C]` marks concept dimensions rather than field measurements.

### View appropriateness
- Plan owns length / width / post c-c / section cut.
- Elevation owns overall height / body scale / datum.
- Section owns body contact / assembly depth / below-datum condition boundary.
- Exploded axon owns layer order only; it carries no authoritative dimensions beyond references repeated from orthographic views.
- D01 owns the verified-RC conditional post-base relationship.

### Occlusion / Clearance
Final local preview was reopened after layout repair. No critical annotation crosses the principal object geometry; lower exploded/detail content no longer collides with the title block.

### Cross-view consistency
Plan/elevation post spacing, overall envelope and section component stack are visually registered to the same v1.7 interface logic.

### Construction / Functional Logic
The sheet does not select an anchor embedment, substrate or final foundation. Unknown substrate remains a HOLD interface. The R06 object is explicitly not treated as sole fall-protection authority.

### Scale / Proportion
Drawing is `NTS`. A 1700 reference person is included only as a body-scale reference. No graphic scale is claimed.

## Remaining producer-observed weakness

`C23-R06-D01` note density is still high at whole-sheet viewing distance. It is acceptable only as near-read **technical support** until an independent reviewer decides whether to split the connection detail onto a dedicated sheet. Do not promote this sheet to MAIN on the basis of this self-check.

## Local execution evidence

- SVG SHA-256: `8fc1f08c7082936307fdd270193e460bd8515c08822b697b798191ba1907c73a`
- local review PNG SHA-256: `3545dce721ebd1e14002f70ea1a9607f429272c591b82409894ca4fe89fe4934`
- remote SVG blob readback: `7395af373264468572a5b8a9156cd3ec9750e809`

Local PNG is review evidence only and is not claimed as a durable production copy. The editable SVG in GitHub is the governed source artifact for this delta.

## Current verdict allowed to producer

**`EXECUTED / SELF-CHECKED / REVIEW PENDING`**

Independent Design Verdict required before any `PIXEL KEEP / MAIN KEEP / PROFESSIONAL FINISH PASS` claim.
