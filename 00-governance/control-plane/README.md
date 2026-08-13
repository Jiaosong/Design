# OLEANDER Project Control Plane v0.2

Status: REVIEW / EXECUTABLE CANDIDATE

This directory turns the v0.1 operational compression layer into a small executable compiler/router. It is subordinate to `00-governance/README.md` and existing canonical specialist systems. It does **not** create a second source of governance truth.

## What v0.2 executes

1. **Project Control Card validation** — a single machine-readable card for one active Decision Question.
2. **Context / namespace resolution** — keeps Knowledge, Application Mapping, Project Axis, Case Axis and Priority separate.
3. **Gate profile selection** — attaches existing specialist gates only when their triggers apply.
4. **CB-01 Repeated Revise Breaker** — two consecutive same-question, same-layer Visual/Project `REVISE` results block a third same-layer tuning loop and require `ROOT_CAUSE_RECLASSIFICATION`.
5. **Asset locator primitive** — deterministic registry + filesystem lookup. Drive/File Library providers must materialize or feed registry entries; CI does not invent connector credentials.

## Non-negotiable boundaries

- Machine PASS != Design PASS.
- Executed != Validated.
- Digital evidence cannot substitute for Physical / Field / Human / Rights / Engineering evidence.
- Derived artifacts cannot replace Source Authority.
- Human judgment owns Candidate retention, Locked Variable reopening, root-cause confirmation and Canonical/Release decisions.
- No new system Gate is created here; existing Artifact Review, Post-Generation Review, Rights, Reality, Engineering, Human Test and PAP systems are only routed.

## Commands

```bash
python 00-governance/control-plane/control_plane.py validate CARD.json
python 00-governance/control-plane/control_plane.py resolve CARD.json
python 00-governance/control-plane/control_plane.py gates CARD.json
python 00-governance/control-plane/control_plane.py breaker CARD.json
python 00-governance/control-plane/control_plane.py check CARD.json
python 00-governance/control-plane/control_plane.py locate NAME --root PATH [--registry REGISTRY.json]
```

`check` is the fail-closed entry point for CI. It returns non-zero when the card is invalid or CB-01 is tripped.

## Problem-layer ladder

`Parameter -> Relation -> Geometry -> Topology -> Architecture -> Evidence`

When CB-01 trips, the tool does not decide the new layer. It blocks same-layer tuning and requires human/root-cause reclassification.

## Gate routing

- `EXPLORE`: Authority Check + Preflight + Visual QA.
- `CANDIDATE`: Machine + Visual + Project QA.
- `AUTHORITY`: Machine + Visual + Project QA + existing Artifact/Post-Generation review; specialist gates attach from artifact/claim/persistence triggers.
- PAP is triggered by production binaries, release packages, or explicit `PAP/FULL_SYNC` persistence triggers.
- AR-S09 is triggered only for Authority release-package/release/full-sync contexts.

## Asset locator boundary

The locator searches supplied registry entries and materialized filesystem roots. It intentionally cannot call ChatGPT-only Drive/File Library connectors from GitHub Actions. The external orchestrator should query providers in the canonical order and pass durable/materialized results into the executable layer:

`Current Authority / Registry -> GitHub -> Drive -> File Library -> runtime materialization`

Only after the external provider chain and this locator both fail should an object be declared `UNLOCATED / E0`.

## Tests

```bash
python -m unittest discover -s 00-governance/control-plane/tests -p 'test_*.py' -v
python 00-governance/control-plane/control_plane.py check 00-governance/control-plane/examples/example-explore.json
```
