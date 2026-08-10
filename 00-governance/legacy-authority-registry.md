# Legacy / Duplicate Authority Registry

Status: ACTIVE governance registry
Date: 2026-08-11

Purpose: prevent duplicate File Library uploads, historical working notes, and superseded machine files from being re-selected as current authority by search ranking or filename recency.

## Authority rule

1. Immutable historical bytes remain evidence and are never silently rewritten.
2. `CURRENT AUTHORITY` is assigned only to the canonical Notion/GitHub source listed here.
3. `SUPERSEDED`, `LEGACY`, `RESOLVED`, and `HISTORICAL ERROR` files may be retrieved for provenance, but must not drive new generated content without explicit historical intent.
4. Duplicate filenames have no authority by themselves.

## Registry

| Legacy / duplicate source | State | Current authority | Required handling |
|---|---|---|---|
| `OLEANDER品牌设计进展.txt` (all duplicate uploads / earlier working states) | SUPERSEDED WORKING NOTES | Notion `01｜OLEANDER 品牌与设计语言`; Notion `00｜OLEANDER／织作｜命名与四层架构迁移基线`; Notion `05H｜Identity Candidate & Asset Audit` | Historical comparison only; do not restore CASE/GD or rejected symbol routes as current. |
| `修复文字问题.txt` copies claiming the connector cannot write/create PRs | HISTORICAL ERROR / SUPERSEDED TOOL CAPABILITY NOTE | Current connected GitHub tool behavior + repository audit trail | Do not use as a current capability constraint. Preserve as an error record. |
| `文件未找到处理请求.txt` about `拆解专项赛资料 (1).zip` | RESOLVED HISTORICAL FAILURE | Current project/file state | Do not use as current file-availability evidence. |
| `P01_evidence_manifest.v0.2.schema.json` | SUPERSEDED MACHINE SCHEMA | `00-governance/schemas/c01-evidence-manifest.v1.schema.json` | Never validate new C01 data against P01 IDs. |
| `P01_evidence_manifest.v0.2.template.json` and earlier P01 evidence templates | SUPERSEDED TEMPLATE | C01 schema + future C01 template generated under the canonical namespace | Keep original bytes; do not generate new P01-* evidence slots. |
| `CASE_GD_Public_Claim_Matrix.csv` | LEGACY CLAIM REGISTER | Claim namespace in `00-governance/naming-status.md` + C01 Claim Register | Map legacy C01–C05 claims to CLM-C01-001–005; never reuse bare Cnn as Claim ID. |
| `OLEANDER_Verified_Content_v0.1.json` | LEGACY CONTENT SNAPSHOT | Current Notion brand / case map / naming baseline | Preserve for provenance; old P01 + CASE/GD architecture is not current. |
| old `index.html`, `oleander-components.js`, `portfolio.content.json` using P01 and LIU/JIAOSONG | LEGACY / TEST FIXTURE unless explicitly promoted by current release gate | Current website source and release gate | Do not infer current authorship or case naming from old test fixtures. |

## Claim migration map

| Legacy Claim ID | Canonical Claim ID | Historical statement |
|---|---|---|
| C01 | CLM-C01-001 | 刘旋主导一脉广渡整体项目 |
| C02 | CLM-C01-002 | 项目已在广渡村实施 |
| C03 | CLM-C01-003 | 村民参与并认可方案 |
| C04 | CLM-C01-004 | 项目改善了文化传承或地方收益 |
| C05 | CLM-C01-005 | 手狮课程由传承人认可 |

The historical verification states are not upgraded by this mapping. ID migration changes namespace only, not truth state or evidence level.
