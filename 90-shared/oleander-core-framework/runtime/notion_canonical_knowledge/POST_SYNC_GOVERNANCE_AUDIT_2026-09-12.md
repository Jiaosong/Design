# OLEANDER Notion Post-Sync Governance Audit — 2026-09-12

Status: **PHASE 1 ACTIVE / SHADOW PLAN / NO PERMANENT DELETE**

This audit starts after the `1,184 / 1,184` corpus reconcile closed. It does not create a new knowledge authority. Notion remains canonical; D1/Vectorize are derivative readback surfaces.

## Rules

- Read actual page content before identity, naming, path, duplicate, or lifecycle decisions.
- No bulk rename, move, delete, merge, or dedupe from metadata alone.
- Decision set: `KEEP / MERGE / SUPERSEDE / ARCHIVE / HOLD`.
- First pass is reversible: identity/property corrections and retrieval containment only; no permanent deletion.
- After every Notion mutation: live Notion readback -> normal `syncPage` -> D1/Vectorize readback -> audit receipt.

## Corpus Triage Snapshot

Verified against production D1 after full sync:

- Active documents: `1,184`
- Missing Canonical ID: `40`
- Blank title: `0`
- Missing governance state: `71`
- Missing relation state: `63`
- Duplicate non-empty Canonical IDs: `3 groups`
- Duplicate exact titles: `0 groups`

These are candidate counts only. They are not equivalent to defects until the corresponding page content and role are reviewed.

## Batch 01 — Canonical Collision Review

### A. `MTH-DESIGN-DOUBLE-DIAMOND-001`

Current carrier:

- Page `390b86be-5c47-8121-8748-cb089a5674c3`
- Title: `MTH-DESIGN-DOUBLE-DIAMOND-001｜双钻发散—收敛方法｜Double Diamond`
- `SUPPORT / SCOPED / METHOD / L5`
- Body explicitly defines the Current method boundary and points to the official source carrier.
- Decision: **KEEP canonical identity**.

Historical carrier:

- Page `3c6b86be-5c47-8116-9606-d59a7588bd71`
- Title: `PROVENANCE｜MTH-DESIGN-DOUBLE-DIAMOND-001｜2026-08-24 Duplicate Carrier → Current Canonical`
- `PROVENANCE / HISTORY_ONLY`
- Body explicitly states: “This duplicate carrier no longer owns `MTH-DESIGN-DOUBLE-DIAMOND-001`.”
- Defect: property-level Canonical ID still collides with the Current carrier.
- Shadow decision: **SUPERSEDE identity only; preserve body NO LOSS**.
- Proposed reversible Canonical ID: `LEGACY-MTH-DESIGN-DOUBLE-DIAMOND-001-DUP-20260824`.

### B. `SRC-KANO-1984-001`

Current carrier:

- Page `3c0b86be-5c47-8137-b063-c980aec07e35`
- Title: `SRC-KANO-1984-001｜Kano et al. 1984｜Attractive Quality and Must-Be Quality`
- `CURRENT / DEFAULT / SOURCE / L6`
- Body is the compact current source boundary with DOI/J-STAGE evidence and explicit non-supported claims.
- Decision: **KEEP canonical identity**.

Historical carrier:

- Page `3adb86be-5c47-8164-a89e-f7db5e372ade`
- Title: `A06｜Kano et al. 1984《Attractive Quality and Must-Be Quality》｜原始论文`
- `PROVENANCE / HISTORY_ONLY / SOURCE / L6`
- Body is an earlier evidence carrier with overlapping source facts and old-note corrections.
- Defect: it still owns the same Canonical ID as the Current source page.
- Shadow decision: **SUPERSEDE identity only; preserve evidence/history**.
- Proposed reversible Canonical ID: `LEGACY-SRC-KANO-1984-001-A06`.

### C. `EVD-SKILL-EXTERNAL-BATCH2-DIGEST-20260828`

Carrier 1:

- Page `3cab86be-5c47-8104-a6d9-e8c9660ff21c`
- Title: `...｜Typography + Iconography + IA + Layout + A11y + Wayfinding + Brand Rules`
- Body calls itself `External Skill Digestion Evidence｜Batch 2｜2026-08-28` and records PR #424 / merge `471b4454...`.
- Decision: **KEEP existing Batch2 Canonical ID**.

Carrier 2:

- Page `3cab86be-5c47-8172-897f-d3361f5dcbda`
- Title: `...｜Curation + Product Form + UI Tokens + OpenSCAD + Design Language`
- Body calls itself `External Skill Digestion Evidence｜Round 2｜2026-08-28` and records PR #427 / merge `a5d58f27...`.
- Defect: distinct evidence run incorrectly reuses Batch2 Canonical ID.
- Shadow decision: **KEEP page/content; correct identity only**.
- Proposed reversible Canonical ID: `EVD-SKILL-EXTERNAL-ROUND2-DIGEST-20260828`.

All three groups are already fail-closed outside accidental Current retrieval, so identity correction can be performed without deleting or merging content.

## Batch 02 Queue — Zero-Body Candidates

D1 readback found `13` active pages with zero indexed body chunks. `unknown_block_ids=[]` and `markdown_truncated=0`, but zero body is not automatically “delete/blank”: index carriers and relation-only records can be legitimate.

Priority review classes:

- Two orphan design-history titles with no Canonical ID or governance metadata: `北欧设计：有机现代主义与人文温度`; `意大利设计：从理性主义到孟菲斯的造型革命` -> **HOLD for live-role/parent review**.
- Ten evidence/case carriers across `EVD-HERITAGE-*` and `EVD-STATEEXHIBITION-*` -> **HOLD for source/content completeness review; no false-completion promotion**.
- `PRAC-BJ-XJ01-20260812-01｜XJ01 CMF Foundation｜Business Practice` -> role is `INDEX`; **HOLD judgment until relation graph is read**.

No Batch 02 mutation is authorized by this audit yet.

## Next Queue

1. Apply and read back the three Batch 01 identity corrections.
2. Re-query canonical collisions; expected count after Batch 01: `0` for these reviewed groups.
3. Read Batch 02 relation/parent context before any lifecycle change.
4. Then process missing Canonical ID / governance / relation candidates in small content-read batches, not bulk mutation.
