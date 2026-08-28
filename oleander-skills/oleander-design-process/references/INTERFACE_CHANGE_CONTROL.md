# Interface Change Control — Candidate Reference

Status: `CANDIDATE REFERENCE / PRACTICE_EVIDENCE / NOT CURRENT RULE`

Purpose: extend the existing `oleander-design-process` Validation Handoff only when downstream evidence proposes a change to a DESIGN-owned invariant.

## Existing-first comparison

The current handoff already resolves object/master, expected behavior, assumptions, authority, expected validation and return status. This reference adds only the missing **change-control loop**.

## Candidate sequence

`REQUIREMENT / EXPECTATION → DESIGN INVARIANT → VALIDATION FINDING → CHANGE REQUEST → IMPACTED INVARIANT → CHANGE AUTHORITY → DISPOSITION → REVISED MASTER / HOLD`

### Minimum change request fields

- `OBJECT_ID`
- `CURRENT_NATIVE_MASTER`
- `UPSTREAM_REQUIREMENT_OR_EXPECTATION`
- `AFFECTED_DESIGN_INVARIANT`
- `VALIDATION_FINDING_ID`
- `PROPOSED_CHANGE`
- `EVIDENCE_OWNER`
- `IMPACT_ON_OTHER_INVARIANTS`
- `CHANGE_AUTHORITY`
- `DISPOSITION = ACCEPT / REJECT / ALTERNATIVE / HOLD`
- `REVISED_MASTER_OR_HOLD`
- `RESIDUAL_HOLD`

## Candidate attacks

- `SILENT EDIT`: validator changes master directly → REJECT.
- `FROZEN DESIGN`: owner refuses all evidence-based change proposals → REVISE/HOLD.
- `PARTIAL PASS`: return must identify the exact invariant affected.
- `TRACE DELETION`: removing requirement/invariant trace must break promotion.
- `AUTHORITY`: proposal ownership and change authority must remain separate.

## External source calibration

NASA Requirements Management, Interface Management and Design Solution Definition were reviewed on 2026-08-28:
- https://www.nasa.gov/reference/6-2-requirements-management/
- https://www.nasa.gov/reference/6-3-interface-management/
- https://www.nasa.gov/reference/4-4-design-solution-definition/

Transferred:
- bidirectional traceability;
- controlled interface changes;
- explicit responsibility/change authority;
- distinction between design-solution verification and later product verification.

Rejected / not adopted as OLEANDER defaults:
- aerospace WBS/lifecycle structure;
- Interface Working Group governance;
- unanimous approval;
- NASA interface-document templates/names;
- mission-specific technical thresholds.

Rights boundary:
NASA public technical references are used for process calibration. No NASA branding, diagrams, proprietary template wording, fixed technical values or project-specific content is copied.

## Promotion boundary

This reference remains Candidate-only until materially different project usage demonstrates:
1. a real validation finding that would change an upstream design invariant;
2. an actual change request/disposition;
3. same-object master update/readback;
4. residual technical HOLD;
5. applicable independent review.

CI, a synthetic A/B, or producer readback cannot promote it.
