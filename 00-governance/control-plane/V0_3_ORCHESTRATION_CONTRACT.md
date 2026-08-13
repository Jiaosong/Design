# OLEANDER Control Plane v0.3｜Orchestration Contract

Status: `REVIEW / ORCHESTRATION CANDIDATE`

This contract extends the merged v0.2 executable core. It does not replace `OLEANDER Current Authority v1.1.0` or any existing specialist gate.

## O1｜Provider Receipt Chain

Canonical order:

`Current Authority / Registry -> GitHub -> Drive -> File Library -> Runtime Materialization`

Rules:
- every provider receipt explicitly records `attempted`, `status` and `hits`;
- a valid hit may stop the chain after every higher-priority provider has been resolved;
- a lower-priority hit is blocked when any higher-priority provider is missing, unavailable, blocked or errored;
- `UNLOCATED / E0` may be declared only after all five providers were attempted and all returned `NOT_FOUND`;
- external connector results are receipts/snapshots, not a new source of authority.

## O2｜Promotion Orchestrator

The orchestrator compiles:

`Control Card -> Machine QA -> Visual QA -> Project QA -> triggered specialist gates -> Persistence when triggered`

All compiled prerequisites must PASS before the machine state can become:

`READY_FOR_HUMAN_DECISION`

The executable layer never emits an automatic `PROMOTED` decision. Candidate retention, Canonical promotion and Release remain human-owned design/governance decisions.

For `FULL_SYNC`, the post-promotion action list includes:
- Artifact Register;
- Notion / GitHub / Drive full sync;
- Contradiction Scan.

## O3｜Contradiction Scan

The scan compares three system snapshots against **one explicit expected canonical state**. This avoids treating Notion, GitHub and Drive as competing truth sources.

Required systems:
- Notion;
- GitHub;
- Drive.

Fail-closed conditions:
- missing system;
- system status not `FOUND`;
- missing expected field;
- field value contradicts expected canonical state.

The scan reports contradictions only. It does not silently repair external state.

## O4｜Automation Boundary

Repository runtime may validate and orchestrate receipts, but authenticated external-system calls remain outside GitHub Actions. An agent/connector may gather external receipts and feed them into v0.3. Credentials are never inferred or embedded into repository governance code.

## O5｜Evidence Boundary

`Provider FOUND != Evidence PASS`.

`Cross-system consistent != Physical / Field / Human / Rights / Engineering validated`.

`Promotion machine prerequisites PASS != human promotion decision`.
