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
- Upstream delta: 0 ahead / 0 behind
- Status: ISOLATED WORKTREE / REMOTE SYNCED / local browser-readback remains untracked

### Notion Canonical Knowledge Runtime
- Path: D:\\Desgin\\.worktrees\\notion-canonical-knowledge-v01
- Branch: agent/oleander-notion-canonical-knowledge-v01-20260911
- HEAD: dd42eee0a61b8c233861b55f7bea84515084083c
- Remote: origin/agent/oleander-notion-canonical-knowledge-v01-20260911
- PR: #521
- Upstream delta: 0 ahead / 0 behind
- CI: AI Governance PASS / Anti-Pollution PASS / Vercel PASS
- Cloudflare Worker: b5f7ad57-36db-4c02-94f6-2c0cb24d7591
- Runtime policy: webhook = Queue fast path with D1 fallback; bulk reconcile = D1 durable scheduler + Cron drain; DLQ = containment only, no auto replay
- Knowledge corpus state: PARTIAL / READBACK PENDING; prior snapshot 194 indexed documents vs 1,184 enumerated Notes objects. Do not label NOTION SYNCED until reconcile task readback closes.

## Baseline
- origin/main: c40381da06933fbfe9c77e7a75f248b52c63d6c2
- Blender execution branch vs origin/main: 163 commits unique locally / 1533 commits on origin/main
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
