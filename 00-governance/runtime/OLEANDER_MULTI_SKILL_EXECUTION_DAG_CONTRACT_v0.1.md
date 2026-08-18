# OLEANDER Multi-Skill Execution DAG Contract v0.1

Status: **CANDIDATE_FOR_CURRENT**  
Decision date: **2026-08-18**  
Scope: **multi-owner execution and handoff**

## 0｜Purpose

Convert multi-Skill routing into an explicit directed acyclic execution graph. This contract does not create an orchestration Skill.

Canonical order:

`CURRENT KNOWLEDGE / PROJECT AUTHORITY → REQUIRED NATIVE OUTPUT → MINIMUM SUFFICIENT OWNER SET → PRIMARY_OWNER → SUPPORT / READ-ONLY NODES → TYPED ARTIFACT HANDOFFS → REAL EXECUTION → READBACK → INDEPENDENT REVIEW`.

## 1｜Required DAG fields

Each graph declares:

`dag_id / task_id / required_native_output / primary_owner / nodes / edges / artifact_contracts / conflict_precedence / reviewer_node / completion_condition / does_not_prove`.

Each node declares:

`owner_id / role / lifecycle_state / read_permissions / write_permissions / inputs / outputs / gates / can_promote`.

Valid node roles:

- `PRIMARY_OWNER` — owns completion of the requested native output.
- `SUPPORTING_OWNER` — produces a bounded intermediate artifact.
- `READ_ONLY_CONSUMER` — may inspect but not mutate upstream artifacts.
- `VALIDATOR` — machine/runtime/compliance validation only.
- `INDEPENDENT_REVIEWER` — issues the review verdict; cannot be the producer of the reviewed artifact when independence is required.

## 2｜Minimum sufficient owner set

`NO COMPRESSION / NO LOSS` protects information, not process length.

Before adding any node, ask whether the requested native output can be produced and validated without it. If yes, omit it.

A task must not automatically expand to Research → DataViz → Technical Drawing → Motion → Delivery QC. Only owners that contribute a required artifact, gate or review are included.

## 3｜Artifact ownership and permissions

Every edge carries a Native Artifact Contract.

Default handoff permission is `READ_ONLY`.

A downstream owner may mutate upstream content only when the edge explicitly grants:
- `DERIVE` — create a new derivative without changing upstream master;
- `MUTATE_PRESENTATION_ONLY` — change crop/layout/style while preserving semantic/source authority;
- `MUTATE_AUTHORIZED_SOURCE` — change the authoritative object only when Current Authority grants it.

No downstream owner may silently overwrite the upstream master.

## 4｜Conflict precedence

When owners conflict:

1. Current Project / Source / Design Authority;
2. authoritative native-source owner for the disputed semantic object;
3. PRIMARY_OWNER for output assembly decisions that do not alter upstream authority;
4. supporting owner within its declared capability boundary;
5. validator/reviewer may block promotion but may not silently rewrite the producer artifact.

## 5｜Example bounded DAG

A complex communication deliverable may legitimately be:

`oleander-research (evidence matrix) → oleander-data-viz (analytical SVG) → OLEANDER Technical Drawing candidate body (technical SVG) → oleander-story-and-board (board assembly) → oleander-delivery-qc (release inspection)`.

`oleander-motion` is added only if temporal behavior/video is actually required.

The board owner may compose the analytical/technical artifacts but cannot change their authoritative values or geometry without a routed upstream revision.

## 6｜Independent review identity

Where independent review is required, record:

`producer_id / reviewer_id / review_input_artifact_id / review_input_hash / reviewer_independence_state / review_verdict / promotion_authority`.

`reviewer_independence_state` values:

`INDEPENDENT / PARTIALLY_INDEPENDENT / NOT_INDEPENDENT`.

A producer self-check may accompany the artifact but must not be treated as the independent verdict.

## 7｜Completion

A DAG is complete only when:
- every required output exists as a Native Artifact Contract;
- every required edge handoff is satisfied;
- blockers are resolved or explicitly HOLD;
- actual runtime/readback gates are complete where required;
- independent review state is recorded where required.

## 8｜Does not prove

A valid DAG proves orchestration clarity only. It does not prove the artifacts are correct, beautiful, field-valid, user-validated or release-ready.
