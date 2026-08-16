# Control Plane v0.3 Status

Status: `CURRENT EXECUTION CONTRACT / HARDENED ORCHESTRATION / NO-LOSS v0.3 DEEPENING`
Authority: subordinate to `00-governance/README.md`, current OLEANDER governance, and `00-governance/OLEANDER_NO_COMPRESSION_NO_LOSS_POLICY_v1.0.md`.

## Historical baseline

- PR #88 merged the executable Control Plane core.
- PR #90 hardened orchestration, authority-bound receipts, Promotion transitions, semantic/freshness contradiction scanning and immutable PR #85 replay.
- PR #131 compiled the global NO COMPRESSION / NO LOSS rule into Control Plane validation.
- PR #134 closed the stored-card compatibility audit with no stock Architecture-card migration required at that time.
- PR #135 added repository-wide Current Control Card discovery by content signature.

These are historical execution facts, not Design PASS or project Promotion claims.

## Current no-loss execution contract

Control Card v0.3 is the Current stored-card schema. v0.2 remains readable for immutable replay/backward compatibility only in explicit provenance/replay zones.

v0.3 separates:

- `problem_layer` — what kind of design/research problem is being worked on; from
- `change_scope` — whether the operation is a restructure and which project/delivery surfaces it affects.

This closes the previous gap where Narrative/Web/Board/PDF/Film/App/Integration/Final-Edit restructuring could avoid no-loss merely because `problem_layer != Architecture`.

For `change_scope.kind=RESTRUCTURE`:

1. affected surfaces must be explicit;
2. established objects must be listed in `established_object_baseline` and bound to `baseline_source`, unless the work is explicitly greenfield;
3. `preservation_review.decisions` must cover that baseline exactly — no missing, duplicate or outside-baseline decisions;
4. `concept_state / presentation_state / truth_evidence_state` remain separate;
5. `SPLIT / GROUP / MERGE / REMAP` require traceable target object IDs;
6. every non-CUT action preserves identity/retrievability;
7. CUT requires `concept_state=DROP` and `identity_preserved=false`;
8. material reduction actions require a substantive structured reason code; compression/page count/minimalism/shorter delivery are not valid reason codes;
9. `global_fixed_chapter_count_applied=false` remains mandatory, so C04's 12-layer structure is not a global template.

## Repository enforcement

`scan_control_cards.py` runs through the existing AI Governance workflow on every PR and every push to `main`.

It discovers Control Cards by content signature rather than filename. Current cards outside excluded provenance/replay zones must use schema v0.3 and pass the existing Control Plane validator.

The scanner does not create a second registry or Gate.

## Historical replay boundary

Automotive v0.11 PR #85 remains immutable replay evidence. Current generic Gate labels absent from historical source stay `REPLAY_MAPPING`; historical files are not rewritten to satisfy newer Current-card contracts.

## Explicitly still human-owned

- Candidate retention;
- final root-cause reclassification;
- Locked Variable reopening;
- substantive Design / MAIN judgment;
- Rights / Reality / Engineering / Human Test judgment;
- Candidate -> Canonical / Release decision.

`Machine PASS != Design PASS` and `Process PASS != MAIN KEEP` remain non-negotiable.
