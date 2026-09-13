# OLEANDER Core Framework — Retrieval Adapter

This directory binds the OLEANDER Authority-aware RAG implementation into the existing core framework as a **derived retrieval adapter**.

It does not create a new framework, runtime authority, project state, skill, method, or knowledge authority.

Canonical implementation contract:

- `00-governance/OLEANDER_AUTHORITY_AWARE_RAG_CONTRACT_v0.1.md`

Runtime policy implementation:

- `00-governance/runtime/oleander_rag_policy.py`

Cloudflare derived retrieval worker:

- `00-governance/runtime/oleander-rag-worker/`

## Existing-first integration rule

The adapter consumes the existing OLEANDER authority and lifecycle fields and returns a typed Knowledge Pack. It must obey existing Source → Permission → Derived Result semantics and must not mutate canonical authority from a retrieval result.

Default execution:

`Current Task → existing Resolver → Retrieval Adapter → Authority Gate → legal candidates → Knowledge Pack → existing Skill/Project execution`

When a source must be verified or written back:

`Knowledge Pack locator → canonical source fetch (Notion/GitHub adapter) → existing authority/readback gate → authorized mutation`

## Fail-closed boundaries

- no canonical locator → HOLD
- UNKNOWN trust/authority in default Current retrieval → HOLD
- CURRENT/PROVENANCE mixed default ranking → HOLD
- canonical collision → HOLD
- derived result attempting authority promotion → HOLD
- stale source hash presented as fresh → HOLD

This adapter is optional at runtime until Golden Set and production shadow-read acceptance gates close.
