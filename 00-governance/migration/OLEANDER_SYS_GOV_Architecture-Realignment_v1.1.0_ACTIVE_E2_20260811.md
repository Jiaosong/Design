# OLEANDER System Governance｜Architecture Realignment v1.1.0

**Date:** 2026-08-11  
**Status:** ACTIVE / E2  
**Decision owner:** 刘旋 / OLEANDER／织作  
**Authority:** Notion `00｜OLEANDER Knowledge Architecture｜知识架构与关系治理` + `00A｜Multi-Level Framework｜多级知识与项目框架` + `00｜OLEANDER／织作｜命名与四层架构迁移基线`

## 1｜Why this change exists
OLEANDER now separates knowledge structure, project structure, application layers, reusable assets and validation rather than allowing one numbering scheme to carry several meanings.

Current structure:
- Knowledge architecture: `00 / 01 / 02 / 10 / 20 / 30 / 90 / 99`.
- Knowledge axis: `L0 → L7`.
- Project axis: `P0 Portfolio → P1 Program → P2 Project → P3 Workstream → P4 Validation`.
- Application mapping: `Business / Culture / IP / Spatial`.
- Cases: `C01 / C02 / C03...`.
- IP assets: `IP-[Role]-[NNN]`.

## 2｜No-loss / no-pollution rule
This migration does **not** delete evidence history and does **not** keep two current systems alive.

- Historical commits, PR titles, evidence event IDs and source filenames remain immutable audit evidence.
- Legacy material may be retained in `99-archive`, Git history or migration records, but it cannot remain a second current authority.
- Current navigation, current templates, current schema defaults, retrieval expected sources and new IDs must use the current architecture only.
- Do not duplicate a page merely to move it into the new architecture; prefer in-place identity/property/relationship repair.
- A historical identifier may appear in a migration note only when needed to map or verify provenance.

## 3｜AI governance namespace repair
The former AI-governance labels `P0 / P1 / P2` collided with the current project axis. Current AI governance therefore uses:

| Current | Meaning | Former current label | History handling |
| --- | --- | --- | --- |
| `AIG-01` | AI Evaluation & Regression | AI `P0` | old wording only in immutable history |
| `AIG-02` | Failure, Trust & Provenance | AI `P1` | old wording only in immutable history |
| `AIG-03` | Runtime Evidence | AI `P2` | old wording only in immutable history |

Historical runtime IDs such as `P2-E011`, `P2-E012`, `P2-E013` are **not renumbered** because they are evidence identities. New events use `AIG3-E...`.

## 4｜GitHub current-authority changes
Current contracts created:
- `90-shared/OLEANDER_AIG-01_Evaluation_Regression_v0.1.md`
- `90-shared/OLEANDER_AIG-02_Failure_Trust_Provenance_v0.1.md`
- `90-shared/OLEANDER_AIG-03_Runtime_Evidence_v0.1.md`

Former current files removed from `90-shared` on the migration branch:
- `OLEANDER_AI_Governance_P0_v0.1.md`
- `OLEANDER_AI_Governance_P1_v0.1.md`
- `OLEANDER_AI_Runtime_Evidence_P2_v0.1.md`

Execution layer aligned:
- `evals/scripts/validate_evals.py`
- `.github/workflows/ai-governance-evals.yml`
- `evals/retrieval/golden_queries.jsonl`
- `evals/runtime/RUNTIME_EVENT_TEMPLATE.json`
- `evals/runtime/BASELINE_2026-08-10.md`
- `90-shared/README.md`

Historical event rows and evidence URLs were not rewritten.

## 5｜Notion in-place changes
Canonical pages renamed in place:
- `AIG-01｜AI Evaluation & Regression Protocol v0.1｜评估与回归`
- `AIG-02｜AI Failure, Trust & Provenance Protocol v0.1｜失败、信任与来源`
- `AIG-03｜AI Runtime Evidence Protocol v0.1｜真实运行证据`

Index objects were repaired in place:
- `MTH-AI-GOV-AIG01-001`
- `MTH-AI-GOV-AIG02-001`
- `MTH-AI-GOV-AIG03-001`

Runtime database renamed in place:
- `AIG-03｜AI Runtime Evidence Log｜真实运行证据`

Existing `P2-*` event IDs remain historical evidence IDs. New records use `AIG3-*`.

`04C｜Media Assets & Rights` current first-reading asset groups were changed from CASE/GD/DY/LC labels to C01/C02/C03; historical linked source pages remain available as provenance.

## 6｜Authority boundaries after migration
- `P0–P4` = project axis only.
- `AIG-01–03` = AI governance only.
- `C01+` = case roots only.
- `CLM-*` = claim IDs only.
- `IP-*` = IP asset IDs only.
- `L0–L7` = knowledge depth only.

A current page or machine template that violates these namespaces is a governance defect and must not be promoted.

## 7｜Intentionally retained history
Retained without current-authority status:
- historical PR #20/#21 titles;
- historical `P2-E...` evidence events and `P2-AUD...` audit IDs;
- Legacy CASE/P01 source filenames and migration mappings;
- old rejected/superseded identity assets used for provenance or comparison.

Their presence is not permission to reuse their naming in new current objects.

## 8｜Still outside this migration
This record does not claim that every historical Notion ancestor path has been physically moved. Current authority is controlled by Canonical ID, governance status, relations and current navigation; physical relocation should occur only where it can be done without duplicating content or breaking evidence links.

This record also does not upgrade any evidence status, project stage, rights state, Motion Practice state or release gate.

## 9｜Acceptance gate
Architecture realignment is complete only when:
1. current AI governance retrieval resolves to AIG-01/02/03;
2. current templates generate AIG3 event IDs, not new P2-E IDs;
3. the governance CI validates the new contracts;
4. former P0/P1/P2 AI files are absent from current `90-shared` authority;
5. historical IDs remain traceable;
6. no project-axis P0/P1/P2 object is confused with AI governance.
