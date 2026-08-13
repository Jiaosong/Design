# Control Plane v0.3 Status

Branch: `agent/project-control-plane-v0-3-live-final`
Status: `HARDENED ORCHESTRATION CANDIDATE / REVIEW`
Authority: subordinate to `00-governance/README.md` and `OLEANDER Current Authority v1.1.0`.

## v0.2 baseline

PR #88 is merged to `main` as executable core.

## v0.3 repair scope — exactly five items

1. **Rebase latest main** — clean branch created from current main instead of rebasing the 181-commit-stale PR #89 branch.
2. **Schema Enforcement** — checked-in Control Card and orchestration schemas are executed by dependency-free runtime validation.
3. **Authority-bound Provider/Gate Receipts** — provider hits and Gate PASS receipts bind distinct authority `object_id` and exact `source_id`, authority state/hash and evidence receipt metadata. LIVE accepts DIRECT evidence only; REPLAY mappings cannot enter live Promotion.
4. **Explicit Promotion Transition** — Promotion declares and validates `from_authority_state -> target_authority_state / target_design_state`; machine output stops at `READY_FOR_HUMAN_DECISION`.
5. **Semantic/Freshness Contradiction Scan + PR #85 replay** — snapshots bind object/revision/payload hash/time plus semantic assertions; Automotive v0.11 PR #85 is the immutable integration replay.

## Validation on PR #90

- hardened unit/regression set: `27/27 PASS`;
- v0.2 fixture Control Card check: PASS;
- PR #85 compatibility replay: `PROMOTION_REPLAY_PREREQUISITES_PASS / replay_only=true`;
- replay exposes historical-to-current Gate mappings explicitly and has `post_promotion_actions=[]`;
- PR #85 post-promotion Notion/GitHub/Drive replay: `CONTRADICTION_SCAN_PASS / findings=[]`;
- compile check: PASS;
- GitHub Actions `OLEANDER Control Plane v0.3`: SUCCESS;
- GitHub Actions `AI Governance Evals`: SUCCESS.

## PR #85 evidence boundary

Historical source text directly supports M5–M10 PASS/CLOSED, PAP-G0—G6 PASS, Formal Promote Review PASS and Candidate-to-Promotion Execution. Current generic Gate labels absent from the historical source are recorded only as `REPLAY_MAPPING`; they are not promoted to historical DIRECT evidence.

## Explicitly still human-owned

- Candidate retention;
- final root-cause reclassification;
- Locked Variable reopening;
- substantive Rights / Reality / Engineering / Human Test judgment;
- Candidate -> Canonical / Release decision.

No sixth repair item or new system Gate is introduced in this patch.
