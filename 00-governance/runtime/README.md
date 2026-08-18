# OLEANDER Runtime Contracts

This directory contains cross-project runtime and capability-routing contracts. It does not replace Notion Current Authority or Project State.

## Current default capability resolution

Use:

- `OLEANDER_DEFAULT_SKILL_RESOLVER_v1.1.md`
- `OLEANDER_DEFAULT_SKILL_RESOLVER_v1.1.json`
- `OLEANDER_NOTION_CURRENT_ARCHITECTURE_BINDING_v1.0.md`
- `OLEANDER_NOTION_CURRENT_ARCHITECTURE_BINDING_v1.0.json`
- `OLEANDER_NOTION_TO_GITHUB_EXECUTION_OWNER_MAP_v1.0.md`
- `OLEANDER_NOTION_TO_GITHUB_EXECUTION_OWNER_MAP_v1.0.json`

Canonical default:

`CURRENT NOTION ROOT AUTHORITY → LIVE REGISTRY → CURRENT DOMAIN / L0–L7 / ROLE / CANONICAL ID → CURRENT METHOD / THEORY / SOURCE / CASE / EVIDENCE / TOOL / PRACTICE → REQUIRED NATIVE OUTPUT → GITHUB EXECUTION OWNER MAP → EXISTING MATURE DESIGN / EXECUTION SKILL → CAPABILITY PROBE → REAL EXECUTION → ACTUAL READBACK → EVIDENCE GATE + INDEPENDENT DESIGN QUALITY GATE`

The GitHub installed-skill list is the formal reusable **execution** registry, not the complete OLEANDER design-intelligence inventory. GitHub Skill names are execution identifiers and must not be copied into Notion as a parallel taxonomy.

The execution-owner map is a routing layer only. `NO_DEDICATED_OWNER` is a valid result and does not authorize automatic creation of a new Skill. Candidate specialist status must remain explicit.

For any execution owner that produces or materially judges visual output, check the local `VISUAL_LAYER_BINDING.md` when present. These files are **binding-only**: they point back to existing Current Notion knowledge, existing Skill submodules, training cases and Artifact Review rules. They do not create a new visual taxonomy, style bible or effect methodology. If the local binding conflicts with Current Project Authority or a more specific Current design source, Current Authority wins.

Current Notion structural routing must use the live Registry and `Canonical Parent｜层级上位 / Canonical Children｜层级子级`; historical navigation ancestry and legacy `上位笔记 / 子级笔记` are not current routing authority.

`OLEANDER_DEFAULT_SKILL_RESOLVER_v1.0.md/.json` remains as superseded implementation provenance in Git history/repository history and is not the current pointer after v1.1 promotion.

## Candidate executable contract layer v0.1

The following files strengthen the interface between Current Notion knowledge objects and GitHub execution implementation without creating new Skills or Notion taxonomy:

- `OLEANDER_SKILL_CAPABILITY_CONTRACT_v0.1.md/.json` — per-owner capability, lifecycle, authority, tools, fallback, gates and handoff declaration.
- `OLEANDER_MULTI_SKILL_EXECUTION_DAG_CONTRACT_v0.1.md/.json` — PRIMARY/SUPPORT/READ-ONLY/VALIDATOR/REVIEWER DAG, minimum sufficient owner set and typed handoffs.
- `OLEANDER_TOOL_ADAPTER_CONTRACT_v0.1.md/.json` — Notion TOOL → GitHub adapter boundary, effect/operator selection, version binding and static-vs-temporal ownership.
- `OLEANDER_NATIVE_ARTIFACT_CONTRACT_v0.1.md/.json` — typed native artifact handoff, editability, semantic layers, dependencies, hashes and shared provenance vocabulary.
- `OLEANDER_EXECUTION_REGRESSION_CONTRACT_v0.1.md/.json` — STRUCTURAL + SEMANTIC + VISUAL_ROI + RUNTIME regression.
- `OLEANDER_NOTION_GITHUB_DRIFT_CHECK_v0.1.md/.json` — Current/STALE/MISSING/DIVERGED/ORPHANED cross-platform mapping contract with static vs live-check separation.

Validation entrypoint:

`python 00-governance/runtime/validate_execution_contracts.py`

While these files are `CANDIDATE_FOR_CURRENT`, the Current default resolver remains v1.1 and the Current Owner Map remains v1.0. Promotion requires CI/readback and a status update; file existence alone is not promotion.

## Existing active runtime contracts

- `OLEANDER_UNIVERSAL_PRODUCTION_ENVIRONMENT_v1.0.md/.json` — tool-agnostic capability and production routing.
- `OLEANDER_BLENDER_RUNTIME_v1.0.md/.json` — shared Blender runtime.
- `OLEANDER_REFERENCE_MATERIALIZATION_GATE_v1.0.md/.json` — source-byte and pixel-level reconstruction preflight.

The default skill resolver **supplements** the Universal Production Environment by defining the knowledge-to-execution ordering. It does not create a parallel tool environment.

## Hard boundary

`Artifact existence ≠ Design quality`  
`Traceability ≠ Professional finish`  
`Evidence correctness ≠ Visual excellence`  
`Process PASS ≠ MAIN KEEP`

`NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS`
