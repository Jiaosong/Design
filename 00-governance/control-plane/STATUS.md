# Control Plane v0.3 Status

Branch: `agent/project-control-plane-v0-3-orchestration`
Status: `ORCHESTRATION CANDIDATE / REVIEW`
Authority: subordinate to `00-governance/README.md` and `OLEANDER Current Authority v1.1.0`.

## v0.2 merged baseline

PR #88 was reviewed CI-green and squash-merged to `main` as commit `eb310049a509d7c48a6bb55d3d1284566aec2908`.

Merged capabilities:
- Project Control Card v0.2 schema;
- fail-closed card validation;
- Context / namespace resolver;
- EXPLORE / CANDIDATE / AUTHORITY gate-profile resolver;
- CB-01 repeated-revise breaker;
- deterministic registry/filesystem asset locator primitive;
- tests and immutable-SHA-pinned GitHub Actions CI.

## v0.3 candidate

Implemented on this branch:
- canonical external provider receipt chain;
- CB-03 higher-authority-gap protection;
- fail-closed `UNLOCATED / E0` eligibility;
- Promotion Orchestrator that compiles all selected QA/gates and stops at `READY_FOR_HUMAN_DECISION`;
- Notion / GitHub / Drive contradiction scan against explicit expected canonical state;
- orchestration schema, examples, tests and v0.3 CI.

## Explicitly not automated

- connector authentication or credential storage inside GitHub Actions;
- autonomous Candidate -> Canonical / Release decisions;
- autonomous mutation of Notion / Drive / File Library / project registries;
- automatic repair of contradictions;
- replacement of Physical / Field / Human / Rights / Engineering evidence with digital execution evidence.

## Acceptance boundary

v0.3 may be promoted only after:
- all v0.2 + v0.3 unit/integration checks pass;
- existing AI Governance Evals pass;
- external provider ordering remains fail-closed;
- Promotion output remains human-decision-gated;
- contradiction scan remains compare-only and fail-closed.
