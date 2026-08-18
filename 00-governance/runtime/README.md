# OLEANDER Runtime Contracts

This directory contains cross-project runtime and capability-routing contracts. It does not replace Notion Current Authority or Project State.

## Current default capability resolution

Use:

- `OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.md`
- `OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json` — Current implementation revision `1.2.1`
- `OLEANDER_NOTION_CURRENT_ARCHITECTURE_BINDING_v1.0.md/.json`
- `OLEANDER_NOTION_TO_GITHUB_EXECUTION_OWNER_MAP_v1.0.md/.json`
- `OLEANDER_EXECUTION_RECEIPT_v1.0.md/.json` — Current policy revision `1.1`

Canonical default:

`CURRENT NOTION ROOT AUTHORITY → CURRENT TASK / SOURCE AUTHORITY → STICKY CONSTRAINT LOCK → LIVE REGISTRY → CURRENT DOMAIN / L0–L7 / ROLE / CANONICAL ID → CURRENT METHOD / THEORY / SOURCE / CASE / EVIDENCE / TOOL / PRACTICE → ACTUAL EXISTING METHOD / SKILL READBACK → REQUIRED NATIVE OUTPUT → FLOW COMPLETION CHECKLIST → GITHUB EXECUTION OWNER MAP → SKILL CAPABILITY CONTRACT → MINIMUM SUFFICIENT OWNER SET / DAG → ALLOWED TOOL ADAPTER WHEN REQUIRED → REAL NATIVE ARTIFACT → TYPED HANDOFF → STRUCTURAL + SEMANTIC + VISUAL_ROI + RUNTIME REGRESSION → ACTUAL READBACK → EVIDENCE GATE + INDEPENDENT DESIGN QUALITY GATE → FLOW COMPLETION GATE → EXECUTION RECEIPT → DRIFT CHECK WHEN CROSS-PLATFORM POINTERS CHANGE`

### Sticky execution constraints

Explicit negative user constraints are resolved **before** owner/tool selection and remain active through ordinary follow-ups until explicitly revoked. Current normalized rules include:

- `NO_IMAGE_GENERATION`
- `NO_NEW_SKILL`
- `NO_NEW_METHOD`
- `NO_NEW_FRAMEWORK`
- `USE_EXISTING_OLEANDER_METHODS_AND_SKILLS`
- `FULL_OLEANDER_FLOW_REQUIRED`
- `NO_PRODUCER_SELF_PROMOTION`

“继续 / 优化 / 再做 / 修一下” does not revoke an active constraint. An available capability does not override a deny lock. If no compliant fallback can produce the required native output, return the affected step as `HOLD` rather than violating the constraint.

### Full-flow completion

`FULL_OLEANDER_FLOW_REQUIRED` means **all applicable phases must close**, not “run every Skill”. The Minimum Sufficient Owner Set remains mandatory.

Plan, method explanation, artifact existence, export, PR, CI green, self-check, render PASS or regression PASS are intermediate states. A full-flow task cannot be reported `CLOSED / 完成 / 已闭环` until the Current Execution Receipt `flow_completion.completion_gate = PASS` and no required applicable phase remains incomplete.

The GitHub installed-skill list is the formal reusable execution registry, not the complete OLEANDER design-intelligence inventory. GitHub Skill names are execution identifiers and must not be copied into Notion as a parallel taxonomy.

The execution-owner map is routing only. `NO_DEDICATED_OWNER` is valid and does not authorize automatic creation of a new Skill. An active creation deny is stronger still: it blocks gap-driven creation and requires existing-owner composition, fallback or HOLD.

For execution owners that produce or materially judge visual output, check local `VISUAL_LAYER_BINDING.md` when present. These files are binding-only and do not create a new visual taxonomy, style bible or effect methodology.

Current Notion structural routing uses the live Registry and `Canonical Parent｜层级上位 / Canonical Children｜层级子级`; historical navigation ancestry and legacy hierarchy fields are not Current routing authority.

`OLEANDER_DEFAULT_SKILL_RESOLVER_v1.1.md/.json` is superseded implementation provenance. Current execution uses v1.2 implementation revision 1.2.1.

## Current executable contract layer v0.1

- `OLEANDER_SKILL_CAPABILITY_CONTRACT_v0.1.md/.json`
- `OLEANDER_MULTI_SKILL_EXECUTION_DAG_CONTRACT_v0.1.md/.json`
- `OLEANDER_TOOL_ADAPTER_CONTRACT_v0.1.md/.json`
- `OLEANDER_NATIVE_ARTIFACT_CONTRACT_v0.1.md/.json`
- `OLEANDER_EXECUTION_REGRESSION_CONTRACT_v0.1.md/.json`
- `OLEANDER_NOTION_GITHUB_DRIFT_CHECK_v0.1.md/.json`

Instance carrier:

- `OLEANDER_EXECUTION_RECEIPT_v1.0.md/.json` — policy revision 1.1; all new receipts record `constraint_lock` + `flow_completion`.
- `receipts/` — execution receipts. Only the explicitly allowlisted pre-policy receipts may omit policy-1.1 fields.
- `regression-baselines/` — typed four-layer regression baselines.

Validation entrypoints:

- `python 00-governance/runtime/validate_execution_contracts.py`
- `python 00-governance/runtime/validate_execution_locks.py`

Runtime regression corpus:

- `evals/runtime/sticky_constraints_and_flow.jsonl`

These contracts and validators do not promote candidate Skills or Notion objects.

## Existing active runtime contracts

- `OLEANDER_UNIVERSAL_PRODUCTION_ENVIRONMENT_v1.0.md/.json` — Current implementation revision 1.0.1; constraint preflight now precedes capability routing and tool selection.
- `OLEANDER_BLENDER_RUNTIME_v1.0.md/.json`
- `OLEANDER_REFERENCE_MATERIALIZATION_GATE_v1.0.md/.json`

The Default Skill Resolver supplements the Universal Production Environment; it does not create a parallel tool environment.

## Hard boundary

`Artifact existence ≠ Design quality`  
`Traceability ≠ Professional finish`  
`Evidence correctness ≠ Visual excellence`  
`Process PASS ≠ MAIN KEEP`  
`Regression PASS ≠ Design KEEP`  
`PR / CI PASS ≠ FULL FLOW COMPLETE`

`NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS`

`NO LOSS` protects information; it does not require running every Skill.
