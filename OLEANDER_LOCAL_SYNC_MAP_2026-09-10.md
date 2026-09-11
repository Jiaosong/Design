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
- HEAD: 15041c82177499e28e5e73019faa5a6578088e0c
- Remote: origin/agent/oleander-notion-canonical-knowledge-v01-20260911
- Runtime PR: #521 MERGED -> `ec6bd93aceacb1303aa2729f22c9fe964463f702`
- Receipt closure PR: #522 MERGED -> `45cadb2fdbf2e9c70152ed363b0d03b2d462840e`
- Upstream delta: 0 ahead / 0 behind
- CI: AI Governance PASS / Anti-Pollution PASS / Vercel PASS
- Cloudflare Worker: 64ebe2ee-7dd8-417b-9197-04c687b2051e
- Runtime policy: webhook = Queue fast path with D1 fallback; bulk reconcile = D1 durable scheduler + one-page-per-Cron drain; protected `drain-once` calls the same durable consumer for explicit operator verification/recovery; DLQ = containment only, no auto replay
- Current full reconcile: `9b40de03-96d5-40b1-be84-0f137e7d248e` / `DRAINING` / 1,184 durable tasks
- Production readback: all 7 historical fallback webhooks processed; current full-reconcile tasks have entered `PROCESSED`; total durable receipts `18 PROCESSED / 1,173 PENDING`; indexed documents `201` (pre-hardening snapshot `194`)
- Knowledge corpus state: PARTIAL / DRAINING. Automatic Cron continuation is still awaiting independent readback; do not label NOTION SYNCED until all current-run tasks close.

## Baseline
- origin/main: 45cadb2fdbf2e9c70152ed363b0d03b2d462840e
- Blender execution branch vs origin/main: 167 commits unique locally / 1547 commits on origin/main
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
