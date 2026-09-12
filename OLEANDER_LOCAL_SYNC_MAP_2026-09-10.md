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

### Notion Canonical Knowledge Runtime
- Path: D:\\Desgin\\.worktrees\\notion-canonical-knowledge-v01
- Branch: agent/oleander-notion-canonical-knowledge-v01-20260911
- HEAD: 3fce0601aa7bb0be291a85c374270a8d8cc68449
- Remote: origin/agent/oleander-notion-canonical-knowledge-v01-20260911
- Runtime PR: #521 MERGED -> `ec6bd93aceacb1303aa2729f22c9fe964463f702`
- Receipt closure PR: #522 MERGED -> `45cadb2fdbf2e9c70152ed363b0d03b2d462840e`
- Scheduler resilience PR: #523 MERGED -> `1156086864df4bd5b34898a341f892f6c1484099`
- Large-page embedding hardening PR: #524 MERGED -> `abd4bee0428b5dcc904aa464f89134496ff12211`
- Final corpus closure PR: #525 MERGED -> `f5f35b9929beb1d9c4b1297050a06586423527b9`
- Upstream delta: 0 ahead / 0 behind
- CI: AI Governance PASS / Anti-Pollution PASS / Vercel PASS
- Cloudflare Worker: `a893e972-5ae5-425c-9298-2315dc05f417`
- Runtime policy: webhook = Queue fast path with D1 fallback; bulk reconcile = D1 durable scheduler; primary scheduler = one-page-per-minute Cloudflare Cron; `scheduled_cron_last_seen` / `scheduled_cron_last_result` provide durable heartbeat readback; `scheduler-status` exposes staleness + open task counts; protected `drain-once` uses the same atomic D1 claim; embedding requests use conservative batching plus adaptive recursive split on provider context overflow; DLQ = containment only, no auto replay
- Scheduler state: Cloudflare Cron recovered; latest durable heartbeat reports `ok=true` for `* * * * *`.
- Cross-provider fallback: GitHub Actions fallback remains gated STANDBY and is not a second authority or second task store.
- Current full reconcile: `9b40de03-96d5-40b1-be84-0f137e7d248e` / `COMPLETE` / 1,184 durable tasks
- Production readback: `1,184 PROCESSED / 0 PENDING / 0 PROCESSING / 0 RETRY / 0 BLOCKED`; D1 documents `1,184 total / 1,184 active`; both formerly oversized RETRY pages closed as `PROCESSED` on attempt `3` with `error=NULL`.
- Knowledge corpus state: **SYNCED / 1184 OF 1184**.

## Baseline
- origin/main: f5f35b9929beb1d9c4b1297050a06586423527b9
- Blender execution branch vs origin/main: 169 commits unique locally / 1559 commits on origin/main
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
