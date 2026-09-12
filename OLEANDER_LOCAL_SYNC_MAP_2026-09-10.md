# OLEANDER LOCAL SYNC MAP｜CURRENT 2026-09-12

> Filename is retained to avoid creating a parallel checkpoint. This page supersedes its 2026-09-10 contents.

## Workspace Authority
- Local workspace: D:\\Desgin
- Repository: Jiaosong/Design
- Execution layer: Chat On Steroids Core

## Active Worktrees

### Blender Runtime
- Path: D:\\Desgin
- Branch: agent/blender-surface-system-v1-21-source-context
- Runtime code baseline before this checkpoint-only map update: bf324158502c9b8896aa9a1a8914c0f276497b00
- Remote: origin/agent/blender-surface-system-v1-21-source-context
- Upstream delta: 0 ahead / 0 behind
- Status: SYNCED TO OWN REMOTE

### C04 Web Presentation
- Path: D:\\Desgin\\.oleander-presentation-c04
- Branch: agent/c04-web-v1-12-currentize-20260830
- HEAD: 35648ae297ead58fbd4ca43c7b5e1c710663abec
- Remote: origin/agent/c04-web-v1-12-currentize-20260830
- Upstream remote HEAD: c9cf475c
- Upstream delta: 0 ahead / 1 behind
- Status: ISOLATED WORKTREE / REMOTE ADVANCED BY 1 / local browser-readback remains untracked; do not fast-forward until the untracked browser evidence is reviewed

### Notion Canonical Knowledge Runtime + Post-Sync Governance
- Path: D:\\Desgin\\.worktrees\\notion-canonical-knowledge-v01
- Branch: agent/oleander-notion-d04-academic-20260912
- HEAD: 808c46af75528f10a424295593cfd2edb9f28eaf
- Remote: origin/agent/oleander-notion-d04-academic-20260912
- Runtime PR: #521 MERGED -> `ec6bd93aceacb1303aa2729f22c9fe964463f702`
- Receipt closure PR: #522 MERGED -> `45cadb2fdbf2e9c70152ed363b0d03b2d462840e`
- Scheduler resilience PR: #523 MERGED -> `1156086864df4bd5b34898a341f892f6c1484099`
- Large-page embedding hardening PR: #524 MERGED -> `abd4bee0428b5dcc904aa464f89134496ff12211`
- Final corpus closure PR: #525 MERGED -> `f5f35b9929beb1d9c4b1297050a06586423527b9`
- Post-sync governance PR: #526 MERGED -> `0a58055f9539ea05387f80ad6cd4742cee94595e`
- Reader + Academic migration PR: #527 MERGED -> `1f699762978515a89d6dafd8e75de9e042126f11`
- D04 academic migration PR: #528 MERGED -> `5dfb458ae70d45d015ab34ee0ef519cb5c4715eb`
- Upstream delta: 0 ahead / 0 behind
- CI: AI Governance PASS / Anti-Pollution PASS / Vercel PASS
- Cloudflare Worker: `5fe7321c-5503-45ca-9dd2-7779f8f4e7b2`
- Runtime policy: webhook = Queue fast path with D1 fallback; bulk reconcile = D1 durable scheduler; primary scheduler = one-page-per-minute Cloudflare Cron; `scheduled_cron_last_seen` / `scheduled_cron_last_result` provide durable heartbeat readback; `scheduler-status` exposes staleness + open task counts; protected `drain-once` uses the same atomic D1 claim; embedding requests use conservative batching plus adaptive recursive split on provider context overflow; post-sync governance uses a bearer-protected, field-allowlisted live Notion read/write path with immediate `syncPage` readback; Reader Layer uses linked views over the same Notes data source; Academic migration creates additive Current carriers and preserves superseded pages NO LOSS; DLQ = containment only, no auto replay
- Scheduler state: Cloudflare Cron recovered; latest durable heartbeat reports `ok=true` for `* * * * *`.
- Cross-provider fallback: GitHub Actions fallback remains gated STANDBY and is not a second authority or second task store.
- Current full reconcile: `9b40de03-96d5-40b1-be84-0f137e7d248e` / `COMPLETE` / 1,184 durable tasks
- Full-sync readback remains closed: `1,184 PROCESSED / 0 PENDING / 0 PROCESSING / 0 RETRY / 0 BLOCKED`; both formerly oversized RETRY pages closed as `PROCESSED` on attempt `3` with `error=NULL`.
- Historical full-reconcile closure remains **SYNCED / 1184 OF 1184** for run `9b40de03-96d5-40b1-be84-0f137e7d248e`. Phase 2 intentionally adds new Current carriers without deleting the superseded pages, so current Notes/D1 row count is now larger than the historical run size.
- Governance Phase 1: **ACTIVE / Batch 01–02 APPLIED + READ BACK / NO PERMANENT DELETE**. Canonical collision groups reduced `3 -> 0`; two historical duplicate carriers were re-identified as Legacy, and the distinct External Skill Round 2 evidence received its own Canonical ID.
- Empty-body containment: ten relation-bearing evidence shells are now `HOLD / PROVENANCE / HISTORY_ONLY`; two fully orphan body-empty pages are retained in Notion as `HOLD / PROVENANCE / BLOCKED` and excluded only from the derivative retrieval plane. `PRAC-BJ-XJ01-20260812-01` remains unchanged pending index-owner/relation review.
- Reader Layer: `知识阅读台｜Knowledge Reader` is live under the root, backed by the existing Notes data source rather than a duplicate DB. Views: `Core Knowledge = L4/L5 + ACTIVE + VALID`; `Methods = METHOD + ACTIVE + VALID`; `Evidence = L6 + ACTIVE + VALID`; `Practice = L7 + ACTIVE`; `History = PROVENANCE or LEGACY/ARCHIVED/HOLD`.
- Academic quality owner: `MTH-KNOWLEDGE-ACADEMIC-NOTE-001｜论文级知识页：论点、证据、反例与适用边界` is `CURRENT / DEFAULT / ACTIVE / VALID`. L4/L5 must use thesis + claim-level evidence + rival/counterevidence + method where relevant + independent Limitations; L6/L7 retain role-specific concise formats.
- First academic THEORY migration: `KN-ARCH-URBAN-REGEN-001｜城市更新：空间改善、产权治理与反置换机制` is `CURRENT / DEFAULT / ACTIVE / VALID`; old `D01｜城市更新与社区营造` is preserved as `LEGACY-KN-ARCH-URBAN-REGEN-D01-20260807 / PROVENANCE / HISTORY_ONLY` with reciprocal replacement relation.
- Research METHOD owner: `MTH-ARCH-RESEARCH-001｜建筑研究方法：问题、证据、有效性与伦理` is `CURRENT / DEFAULT / ACTIVE / VALID`; old D08 preserved as `LEGACY-MTH-ARCH-RESEARCH-D08-20260730 / PROVENANCE / HISTORY_ONLY`.
- Evidence-governance METHOD owner: `MTH-ARCH-EVIDENCE-GOV-001｜建筑证据治理协议：权威、适用性、版本与冲突` is `CURRENT / DEFAULT / ACTIVE / VALID`; old K03 preserved as `LEGACY-MTH-ARCH-EVIDENCE-GOV-K03-20260824 / PROVENANCE / HISTORY_ONLY`. Stable protocol is now separated from dated standards/product/supplier/price update logs.
- D04 academic THEORY migration: `KN-ARCH-DIGITAL-INFO-001｜BIM 与数字建造：信息需求、开放交换与可验证工作流` is `CURRENT / DEFAULT / ACTIVE / VALID`, with live-Notion review of testable thesis, claim-level sources, rival/counterevidence, method boundary and independent Limitations before promotion. Old `D04｜数字设计、BIM与智能建造` is fully retained as `LEGACY-KN-ARCH-DIGITAL-INFO-D04-20260807 / PROVENANCE / HISTORY_ONLY / LEGACY / VALID`, linked reciprocally to the Current replacement.
- Current D1 readback after additive D04 migration: `1,189 document rows / 1,187 active / 2 excluded`; duplicate non-empty Canonical ID groups remain `0`. New D04 Current is `INDEXED / 38 chunks / not truncated`; old D04 remains `INDEXED / 57 chunks / not truncated`. The two excluded rows are the previously contained orphan empty pages and remain in Notion.
- Remaining rewrite queue: `D06 -> D07 -> D03 -> D05 -> D02`; `K05` is navigation/IA cleanup only, not a paper. Each migration remains additive and readback-gated.

## Baseline
- origin/main: 5dfb458ae70d45d015ab34ee0ef519cb5c4715eb
- Blender execution branch vs origin/main: 173 commits unique locally / 1569 commits on origin/main
- Policy: origin/main is not automatically merged into active execution branches; reconcile through Source Authority / project state first.
- Policy: do not merge into active branches without authority review

## Authority Split
- Notion: canonical knowledge authority and lifecycle state
- GitHub: runtime / artifact version authority and CI receipts
- D1 + Vectorize: derivative, rebuildable retrieval plane; never a second Current authority
- Local worktrees: execution state only; worktree existence does not prove remote or knowledge sync

## Sync Rule
MASTER PROTOCOL -> PROJECT STATE -> SOURCE AUTHORITY -> CURRENT TASK -> Execution Branch

Write success != Sync success. Only canonical target readback may be marked SYNCED.
