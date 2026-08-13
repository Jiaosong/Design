# Control Plane v0.2 Status

Branch: `agent/project-control-plane-v0-2`
Status: `EXECUTABLE CANDIDATE / REVIEW`
Authority: subordinate to `00-governance/README.md` and `OLEANDER Current Authority v1.1.0`.

Implemented in v0.2:
- Project Control Card v0.2 schema;
- fail-closed card validation;
- Context / namespace resolver;
- EXPLORE / CANDIDATE / AUTHORITY gate-profile resolver;
- CB-01 repeated-revise breaker;
- deterministic registry/filesystem asset locator primitive;
- unit tests and GitHub Actions CI.

Not implemented yet:
- authenticated Drive/File Library provider adapters inside repository runtime;
- promotion orchestrator;
- Notion × GitHub × Drive contradiction scan;
- automatic mutation of external project registries.

Those remain separate v0.3+ orchestration work and must not be implied by v0.2 PASS.
