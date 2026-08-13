# OLEANDER Project Control Plane v0.3

Status: `v0.2 EXECUTABLE CORE / MERGED` + `v0.3 ORCHESTRATION CANDIDATE / REVIEW`

This directory is subordinate to `00-governance/README.md` and existing canonical specialist systems. It compiles and orchestrates existing rules; it does **not** create a second source of governance truth and does not autonomously make design, evidence, rights or release decisions.

## Architecture

`v0.2 compiler/router -> v0.3 orchestration -> existing specialist gates / external systems`

### v0.2 executable core

- Project Control Card validation;
- Context / namespace resolution;
- EXPLORE / CANDIDATE / AUTHORITY gate-profile selection;
- CB-01 Repeated Revise Breaker;
- deterministic registry/filesystem asset locator primitive.

### v0.3 orchestration

1. **CB-03 External Provider Chain**
   - canonical order: `Current Authority / Registry -> GitHub -> Drive -> File Library -> runtime materialization`;
   - a lower-priority hit is blocked if any higher-priority provider is missing, unavailable, blocked or errored;
   - the chain may stop after a valid hit once all higher-priority providers are resolved;
   - `UNLOCATED / E0` is eligible only after all five providers were attempted and all returned `NOT_FOUND`.
2. **Promotion Orchestrator**
   - compiles Machine / Visual / Project QA plus all specialist gates selected by v0.2;
   - no selected gate may be `NOT_RUN / BLOCKED / FAIL`;
   - machine completion returns only `READY_FOR_HUMAN_DECISION`;
   - human judgment retains Candidate -> Canonical / Release authority.
3. **Cross-system Contradiction Scan**
   - compares Notion / GitHub / Drive snapshots against one explicit expected canonical state;
   - missing systems, missing expected fields or conflicting values fail closed;
   - a contradiction scan does not create or repair external state by itself.

## Non-negotiable boundaries

- `Machine PASS != Design PASS`.
- `Executed != Validated`.
- Digital evidence cannot substitute for Physical / Field / Human / Rights / Engineering evidence.
- Derived artifacts cannot replace Source Authority.
- External provider adapters produce **receipts/snapshots**; repository runtime does not invent connector credentials.
- Promotion orchestration compiles prerequisites; it does not perform the final human promotion decision.
- No new system Gate is created here; existing Artifact Review, Post-Generation Review, Rights, Reality, Engineering, Human Test and PAP systems remain canonical specialist modules.

## Commands

### v0.2 core

```bash
python 00-governance/control-plane/control_plane.py validate CARD.json
python 00-governance/control-plane/control_plane.py resolve CARD.json
python 00-governance/control-plane/control_plane.py gates CARD.json
python 00-governance/control-plane/control_plane.py breaker CARD.json
python 00-governance/control-plane/control_plane.py check CARD.json
python 00-governance/control-plane/control_plane.py locate NAME --root PATH [--registry REGISTRY.json]
```

### v0.3 orchestration

```bash
python 00-governance/control-plane/orchestrator.py providers PROVIDER_RECEIPTS.json
python 00-governance/control-plane/orchestrator.py promotion CARD.json GATE_RESULTS.json
python 00-governance/control-plane/orchestrator.py contradictions CONTRADICTION_MANIFEST.json
```

## Problem-layer ladder

`Parameter -> Relation -> Geometry -> Topology -> Architecture -> Evidence`

When CB-01 trips, the executable layer blocks same-layer tuning and requires `ROOT_CAUSE_RECLASSIFICATION`; it does not choose the new problem layer automatically.

## Promotion sequence

`Control Card PASS -> required QA PASS -> triggered specialist gates PASS -> persistence PASS when triggered -> READY_FOR_HUMAN_DECISION -> human Promote/Reject -> Artifact Register -> promotion-focused sync -> contradiction scan`

A contradiction scan occurs after canonical synchronization when `FULL_SYNC` is requested. It is not used to retroactively justify a promotion whose prerequisite gates were open.

## External provider contract

The repository orchestration layer accepts provider receipts. ChatGPT/agent connectors may query Drive, File Library, Notion or GitHub and feed their results into those receipts, but CI itself does not hold or infer those credentials.

A `FOUND` result may stop the search chain after all higher-priority providers are resolved. By contrast, an `UNLOCATED / E0` declaration requires a complete five-provider `NOT_FOUND` chain.

## Tests

```bash
python -m unittest discover -s 00-governance/control-plane/tests -p 'test_*.py' -v
python 00-governance/control-plane/control_plane.py check 00-governance/control-plane/examples/example-explore.json
python 00-governance/control-plane/orchestrator.py providers 00-governance/control-plane/examples/v0.3-provider-found.json
python 00-governance/control-plane/orchestrator.py promotion 00-governance/control-plane/examples/v0.3-authority-card.json 00-governance/control-plane/examples/v0.3-gates-pass.json
python 00-governance/control-plane/orchestrator.py contradictions 00-governance/control-plane/examples/v0.3-contradiction-pass.json
```
