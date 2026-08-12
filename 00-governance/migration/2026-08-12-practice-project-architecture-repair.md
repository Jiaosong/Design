# 2026-08-12｜Practice / Project Architecture Repair

Status: **CURRENT-AUTHORITY REPAIR / HISTORY PRESERVED**

## Scope

This migration continues the architecture realignment accepted in PR #66 and the clean Spatial Practice repair merged in PR #68.

It audits three collision classes:
1. four-layer node codes (`B/CU/IP/SP`) being treated as project IDs;
2. `P0/P1/P2/P3` being reused as delivery priority labels;
3. old AI `P0/P1/P2` namespace being read as current authority.

## Current rules

- Project axis only: `P0 Portfolio → P1 Program → P2 Project → P3 Workstream → P4 Validation`.
- Four-layer nodes only: `B01–B04 / CU01–CU04 / IP01–IP04 / SP01–SP04`.
- Delivery priority only: `Priority-0 / Priority-1 / Priority-2 / Priority-3`.
- Current AI namespace only: `AIG-01 / AIG-02 / AIG-03`.
- Historical branch names, event IDs, PR titles, run IDs and source filenames remain immutable provenance.

## Practice project maps

- P2 `PRAC-BUSINESS-2026`
  - P3 `PRAC-BUSINESS-2026-WS-01` Timer Light Basin
- P2 `PRAC-CULTURE-2026`
  - P3 `PRAC-CULTURE-2026-WS-01` CU01 Material Transformation
- P2 `PRAC-IP-2026`
  - P3 `PRAC-IP-2026-WS-01` Product Form & Interface
  - P3 `PRAC-IP-2026-WS-02` Wayfinding
  - P3 `PRAC-IP-2026-WS-03` Motion Hierarchy
- P2 `PRAC-SPATIAL-2026`
  - existing P3/P4 mapping retained from PR #68

Culture was initially left empty to avoid symmetry-driven project creation. During the same audit, a new 2026-08-12 CU01 Material Transformation Practice was discovered in both Notion and canonical Drive. It contains a concrete source-translation question, official-source verification, A/B design judgement, non-transferable form/rights boundaries and editable artifacts. It therefore legitimately triggers the first Culture P2/P3. No Culture P4 is created because real material/manufacturing/safety validation remains open.

## Shared-system exception

`SYS-BLENDER-SURFACE` is a P2 shared-system project under `PG-10｜Knowledge & Governance`.

Its primary knowledge node may be `IP03`, but `IP03` is not its project ID and does not make it a child of annual `PRAC-IP-2026`. Version directories under `06-practice/2026` remain execution/practice evidence; current reusable authority remains under `90-shared/toolchains/blender-surface-system/`.

## Notion repair record

Current Notion project database priority options were migrated from the colliding legacy labels:
- `P0 紧急` → `Priority-0｜紧急`
- `P1 重要` → `Priority-1｜重要`
- `P2 一般` → `Priority-2｜一般`
- `P3 低` → `Priority-3｜低`

After row migration, the old P0–P3 priority options were removed from the current schema.

Additional legacy/orphan project rows were assigned current project-axis identities without duplicating their bodies:
- `SYS-KNOWLEDGE-BASE`
- `RES-CMF-TRENDS-2026`
- `SYS-USER-RESEARCH-METHODS`
- `PRJ-ZTS-PLANNING-2026`
- `BJ-RESEARCH-2026`
- P3 `BJ-RESEARCH-2026-WS-01` / workflow code `XJ01-WS-01`

Practice project relations added/repaired:
- `PRAC-BUSINESS-2026` + Timer P3 + L7
- `PRAC-CULTURE-2026` + CU01 Material Transformation P3 + L7
- `PRAC-IP-2026` + Product Form / Wayfinding / Motion P3 + L7
- existing `PRAC-SPATIAL-2026` P2/P3/P4 retained
- shared `SYS-BLENDER-SURFACE` moved conceptually out of annual IP Practice and attached to PG-10 without relocating historical evidence.

The AIG-03 Runtime Evidence Log now explicitly treats `P2-E001—P2-E013` and `P2-AUD-*` as Legacy Event IDs only. New runtime events remain `AIG3-E...`.

## Evidence boundary

Architecture repair does not upgrade Reality, rights, engineering, user, manufacturing, project-specific material, or release evidence. P4 is not created merely to make a hierarchy look complete.