# OLEANDER Notion Canonical Knowledge Runtime Receipt v0.1

Status: **IMPLEMENTATION CANDIDATE**

Promotion: **NOT REQUESTED / NOT GRANTED**

Date: 2026-09-11

## Scope

Created an isolated Cloudflare runtime skeleton for:

`Notion Canonical Knowledge → Webhook → Worker → Queue/Dedupe → Fetch Latest → Normalize/Chunk → D1 + Workers AI → Vectorize namespaces → Authority API → Knowledge Pack`.

## Upstream authority preserved

- Notion root: `9150e089-9a7d-4b29-b026-175fca3a41b3`
- Notes data source: `4668fc63-45a6-496e-a2cc-f9542928b9e8`
- `Retrieval Space｜检索空间` is consumed as an existing Notion field; no parallel taxonomy is created.
- CURRENT is explicit-only; missing/conflicting authority cannot auto-promote.

## Validation result

**PASS — local/runtime skeleton closure**

- `npm run typecheck`: PASS, 0 TypeScript errors.
- `vitest run`: PASS, 3 test files / 11 tests.
- authority tests: explicit-only CURRENT, legacy/history downgrade, blocked exclusion, missing-space fail-closed.
- chunker tests: heading-path preservation, CJK-aware sizing, 320-token bound, signed-URL hash normalization.
- webhook security tests: raw-body HMAC-SHA256 verification and AES-GCM setup-token storage roundtrip.
- `wrangler deploy --dry-run`: PASS; Worker bundle and AI / D1 / Queue / Vectorize bindings resolve.
- D1 local migrations: PASS; `0001_manifest.sql` (14 commands) + `0002_history_and_setup_state.sql` (4 commands).
- local Worker HTTP: `/health` 200; unauthenticated search 401; Notion handshake 200 without token echo.
- encrypted webhook setup flow: handshake 200 → bearer-protected setup-token read 200 → clear 200.
- provisioning script without `-Apply`: PASS; prints plan only and creates no Cloudflare resources.

## Known boundary

Workers AI and Vectorize cannot be fully exercised in Wrangler local mode. Their binding/configuration shape passes Wrangler dry-run, but the actual embedding + Vectorize write/query path remains **REMOTE VALIDATION PENDING** until the Cloudflare D1 / Queue / Vectorize resources are explicitly provisioned and the Worker is deployed.

Cloudflare account resources and Notion webhook subscription were intentionally **not** created by this receipt because those are external/account mutations. The provisioning script requires an explicit `-Apply` flag.
