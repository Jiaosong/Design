# Control Plane v0.3 Status

Branch: `agent/project-control-plane-v0-3-live-final`
Status: `HARDENED ORCHESTRATION CANDIDATE / REVIEW`
Authority: subordinate to `00-governance/README.md` and `OLEANDER Current Authority v1.1.0`.

## v0.2 baseline

PR #88 is merged to `main` as executable core.

## v0.3 repair scope — exactly five items

1. **Rebase latest main** — clean branch created from current main instead of rebasing the 181-commit-stale PR #89 branch.
2. **Schema Enforcement** — checked-in Control Card and orchestration schemas are now executed by dependency-free runtime validation.
3. **Authority-bound Provider/Gate Receipts** — provider hits and Gate PASS receipts must bind to exact object/source/authority/hash evidence; discovery is not authority.
4. **Explicit Promotion Transition** — Promotion declares and validates `from_authority_state -> target_authority_state / target_design_state`; machine output stops at `READY_FOR_HUMAN_DECISION`.
5. **Semantic/Freshness Contradiction Scan + PR #85 replay** — snapshots bind object/revision/payload hash/time plus semantic assertions; Automotive v0.11 PR #85 is the immutable integration replay.

## Validation completed before PR

- isolated unit/regression tests: `24/24 PASS`;
- PR #85 promotion replay: `READY_FOR_HUMAN_DECISION`;
- PR #85 post-promotion Notion/GitHub/Drive replay: `CONTRADICTION_SCAN_PASS / findings=[]`;
- GitHub canonical receipt readback confirms v0.11 `PROMOTED / CANONICAL_AUTHORITY / M5–M10 CLOSED / PAP PASS`;
- Notion Canonical Authority receipt readback confirms the same core state;
- Drive Canonical Authority receipt readback confirms the same core state and is bound to its real Google Docs revision ID.

## Explicitly still human-owned

- Candidate retention;
- final root-cause reclassification;
- Locked Variable reopening;
- substantive Rights / Reality / Engineering / Human Test judgment;
- Candidate -> Canonical / Release decision.

No sixth repair item or new system Gate is introduced in this patch.
