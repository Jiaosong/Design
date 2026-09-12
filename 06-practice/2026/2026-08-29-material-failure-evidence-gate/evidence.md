# Material Failure Evidence-Gate Practice

Status: PRACTICE_EVIDENCE / TRAINING ONLY / NO PROJECT CLAIM

## GAP
New Candidate material-selection/failure-analysis extension has no Practice/Cross-context/Project evidence. Validate its fail-closed boundary: incomplete material/process evidence must not be promoted to a proven root cause.

## SOURCE
- HSE Safety Alert ED 2-2015, issue 2015-09-18: Catastrophic failure of a pipework clamp connector.
- Current URL checked 2026-08-29: https://www.hse.gov.uk/safetybulletins/catastrophic-failure-of-a-techlok-clamp.htm
- Scope: incident-specific evidence only; not a universal material/design standard.

## TEST
A_INCOMPLETE_FAILURE_CLAIM intentionally asserts ROOT_CAUSE_PROVEN while omitting material/process/hardness/heat-treatment evidence. Generic static-stress-pass wording is EXERCISE ASSUMPTION only.

B_SOURCE_GROUNDED_INCIDENT_REPRODUCTION records only HSE-published incident facts and explicitly limits the claim to source-bounded reproduction.

Both JSON artifacts were written, reopened from disk, parsed independently, hashed, and evaluated.

## READBACK / VERDICT
PROVEN_CANDIDATE_FAIL_CLOSED_ON_INCOMPLETE_EVIDENCE__HOLD_PHYSICAL_AND_PROJECT_PROOF

PROVEN:
- A overclaim is rejected by the evidence gate.
- B can reproduce incident-specific source facts without turning them into universal rules.

NOT PROVEN / HOLD:
- actual root cause for any new or project failure;
- universal hardness/material threshold;
- simulation adequacy;
- physical retest;
- engineering/fabrication safety;
- project fabrication PASS or FIELD truth.

## TRANSFER BOUNDARY
Material/failure validation must preserve the chain: actual object/material/process identity -> authoritative source/test evidence -> failure observation -> causal claim -> physical/specialist confirmation where required. Missing links remain HOLD. A source-bounded historical incident can train the evidence gate but cannot stand in for a project test.
