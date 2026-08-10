# Failure & Escalation Playbook

Use when an AI-assisted OLEANDER task produces an error, conflict, unsafe overreach, unknown tool state or evidence/provenance failure.

## Failure record
- Failure ID:
- Task / project / object version:
- Model / tool / skill version:
- Trigger:
- Category: `F-SOURCE|F-STALE|F-TRUTH|F-RIGHTS|F-SAFETY|F-DATA|F-GEOMETRY|F-TOOL|F-CONFLICT|F-PROVENANCE`
- Evidence:
- Affected outputs:
- Potential impact:

## Escalation
Choose one:
- [ ] `F0 SELF-CORRECT`
- [ ] `F1 HUMAN-REVIEW`
- [ ] `F2 DOMAIN-EXPERT`
- [ ] `F3 STOP-HOLD`

## Containment
- What has been frozen?
- What must not be published / executed / reused?
- Is rollback required?
- Is the tool state known?

## Owner
- Escalation owner:
- Required expert / rights holder / decision owner:
- Deadline or next review point:

## Recovery
- Root cause:
- Correction:
- Re-test:
- Regression case to add/update:
- Final state: `RESOLVED|LIMITED|HOLD|ROLLBACK`
- Residue / lessons:

## Mandatory rules
- Repeat of the same blocker twice -> at least F1.
- D4 cultural-rights or D5 safety-critical issue -> at least F2.
- Unknown irreversible tool state -> F3.
- Rights unknown before public release -> F3.
- Recovery is incomplete until a re-test or explicit hold is recorded.