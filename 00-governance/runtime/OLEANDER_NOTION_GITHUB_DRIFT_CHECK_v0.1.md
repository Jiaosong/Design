# OLEANDER Notion ↔ GitHub Drift Check v0.1

Status: **ACTIVE_CURRENT**  
Decision date: **2026-08-18**  
Scope: **cross-platform knowledge-to-execution implementation drift**

## 0｜Purpose

Detect drift between Current Notion knowledge identity and GitHub execution implementation without making GitHub the owner of Notion naming/taxonomy.

Canonical comparison key:

`NOTION CANONICAL ID → GITHUB IMPLEMENTATION PATH / EXECUTION OWNER → IMPLEMENTED REVISION → IMPLEMENTATION COMMIT → LAST VERIFIED → DRIFT STATE`.

## 1｜Drift states

- `CURRENT` — implementation explicitly targets the Current Notion object/revision and required files exist.
- `STALE` — implementation exists but its declared Notion revision/verification date is older than the Current known revision or pointer.
- `MISSING` — Current Notion object requires an implementation but no mapped GitHub implementation exists.
- `DIVERGED` — both sides exist but declared semantics/owner/boundary conflict.
- `ORPHANED_IMPLEMENTATION` — GitHub implementation points to a missing/Legacy/non-Current Notion object without an allowed compatibility reason.
- `NOT_REQUIRED` — Current Notion object is knowledge-only and does not require GitHub implementation.
- `UNKNOWN` — live cross-platform evidence is insufficient; do not guess.

## 2｜Required mapping record

`mapping_id / notion_canonical_id / notion_object_id / knowledge_role / notion_governance_state / notion_last_verified / github_owner / github_paths / implemented_revision / implementation_commit / runtime_or_validator / last_verified / drift_state / drift_reason / next_action / does_not_prove`.

## 3｜Check order

1. Resolve Notion Current Root Authority and live Registry.
2. Resolve the Current Notion object by Canonical ID, not historical page ancestry.
3. Read governance state, knowledge role, relations and last-verified/current revision signal.
4. Resolve GitHub through Current Execution Owner Map.
5. Verify mapped files/owners exist on `main` and their status/lifecycle labels are compatible.
6. Compare `implemented_revision / implementation_commit / last_verified`.
7. Emit one drift state; never auto-create a Skill or silently rewrite Notion.

## 4｜Current seed mappings

### Resolver
- Notion: `KN-METHOD-OLEANDER-SKILL-RESOLVER-001`.
- GitHub: `00-governance/runtime/OLEANDER_DEFAULT_SKILL_RESOLVER_v1.1.md/.json`.
- Supporting map: `OLEANDER_NOTION_TO_GITHUB_EXECUTION_OWNER_MAP_v1.0.md/.json`.

### Image Processing TOOL
- Notion: `T-VISUAL-IMAGE-OPS-001` / page `3c0b86be-5c47-8142-bab6-e6cac9306bd2`.
- GitHub execution binding: 11 `VISUAL_LAYER_BINDING.md` consumers merged through PR #246 / merge commit `767402f55a2bad308b111eee85f30e93d9f2c86f`.
- TOOL remains Notion operator authority; GitHub files are adapters/bindings, not duplicate Canonical TOOLs.

## 5｜Automation boundary

GitHub CI can validate repository paths, machine-readable schemas, implementation revisions and internal consistency. It cannot claim a live Notion object is CURRENT unless a trusted Notion snapshot/API read was provided for that run.

Therefore the drift checker supports two modes:

- `GITHUB_STATIC_CHECK` — repository-side completeness and mapping consistency only.
- `LIVE_CROSS_PLATFORM_CHECK` — requires live Notion readback and records the Notion object ID/revision/verification time consumed.

Do not report `CURRENT` from a repository-only check when the Notion side was not read.

## 6｜Repair actions

Allowed actions:
- `UPDATE_GITHUB_IMPLEMENTATION`;
- `UPDATE_GITHUB_POINTER`;
- `UPDATE_NOTION_POINTER_OR_RELATION` when the Notion Current object is wrong and authority allows write;
- `MARK_DEPRECATED_OR_LEGACY`;
- `REVIEW_REQUIRED`;
- `NO_ACTION`.

Forbidden automatic action: creating a new Skill merely because a mapping is MISSING.

## 7｜Does not prove

Drift status proves cross-platform pointer/implementation consistency only. It does not prove method quality, design quality, field truth, user validation, runtime correctness beyond the checked scope or project promotion.
