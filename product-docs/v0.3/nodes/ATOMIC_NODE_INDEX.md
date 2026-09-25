# OLEANDER Atomic Product Node Index v0.3.1

[← Product Node Graph](README.md) · [Node Registry](NODE_REGISTRY.md) · [Visual Maps](../maps/README.md)

> v0.3.1 把 first-class product node 继续拆到可单独定义、验收、追踪和变更的原子能力。每个原子节点只有一份 primary document。

## Node Depth

```mermaid
flowchart LR
    S[Strategy / Master PRD] --> P[Primary Product Node]
    P --> A[Atomic Product Node]
    A --> R[Requirement IDs]
    R --> AC[Acceptance / Failure]
    AC --> E[Eval / Metric]
```

**Primary node docs:** 23
**Atomic node docs:** 69
**Total product node docs:** 92

## N01｜HOME

Parent: [N01 HOME](N01_HOME.md)

| Node | Atomic capability | Priority | Primary metric |
|---|---|---|---|
| N01A | [RESUME SNAPSHOT](atomic/N01A_RESUME_SNAPSHOT.md) | P0 | Resume Accuracy / Resume Correction |
| N01B | [FRONTIER](atomic/N01B_FRONTIER.md) | P0 | Frontier Correction Rate |
| N01C | [CRITICAL OPEN](atomic/N01C_CRITICAL_OPEN.md) | P0 | Critical-open Resolution Rate |
| N01D | [ACTIVE ARTIFACT](atomic/N01D_ACTIVE_ARTIFACT.md) | P0 | Active Artifact Correction Rate |
| N01E | [NEXT ACTION](atomic/N01E_NEXT_ACTION.md) | P0 | Next-action Acceptance / Correction |

## N02｜FOCUS

Parent: [N02 FOCUS](N02_FOCUS.md)

| Node | Atomic capability | Priority | Primary metric |
|---|---|---|---|
| N02A | [PROBLEM STATEMENT](atomic/N02A_PROBLEM_STATEMENT.md) | P0 | Problem Reframe Rate |
| N02B | [CURRENT DESIGN QUESTION](atomic/N02B_CURRENT_DESIGN_QUESTION.md) | P0 | Question Clarity / Correction |
| N02C | [DESIGN VALUE / INTENT](atomic/N02C_DESIGN_VALUE_INTENT.md) | P0 | Intent Drift Detection / Human Correction |
| N02D | [CONSTRAINT / ASSUMPTION](atomic/N02D_CONSTRAINT_ASSUMPTION.md) | P0 | Stale Assumption Detection |
| N02E | [SUCCESS CONDITION](atomic/N02E_SUCCESS_CONDITION.md) | P1 | Success-condition Rework |
| N02F | [REFRAME](atomic/N02F_REFRAME.md) | P0 | Reframe-to-Recovery Time |

## N03A｜EXPLORE

Parent: [N03A EXPLORE](N03A_EXPLORE.md)

| Node | Atomic capability | Priority | Primary metric |
|---|---|---|---|
| N03A1 | [DESIGN DIRECTION](atomic/N03A1_DESIGN_DIRECTION.md) | P0 | Direction Usefulness |
| N03A2 | [ALTERNATIVE SET](atomic/N03A2_ALTERNATIVE_SET.md) | P0 | Comparable Set Quality |
| N03A3 | [MATERIAL DISTINCTNESS](atomic/N03A3_MATERIAL_DISTINCTNESS.md) | P0 | Material Divergence / Cosmetic Duplicate |
| N03A4 | [BASELINE / OFF](atomic/N03A4_BASELINE_OFF.md) | P1 | Baseline Consideration Rate |
| N03A5 | [REFERENCE TRANSFORMATION](atomic/N03A5_REFERENCE_TRANSFORMATION.md) | P1 | Precedent Transfer Correction |

## N03B｜DEVELOP

Parent: [N03B DEVELOP](N03B_DEVELOP.md)

| Node | Atomic capability | Priority | Primary metric |
|---|---|---|---|
| N03B1 | [MATURITY GAP](atomic/N03B1_MATURITY_GAP.md) | P1 | Maturity-gap Correction |
| N03B2 | [DEVELOPMENT FRONTIER](atomic/N03B2_DEVELOPMENT_FRONTIER.md) | P0 | Development Frontier Correction |
| N03B3 | [DOMAIN ADAPTER](atomic/N03B3_DOMAIN_ADAPTER.md) | P0 | Cross-domain Transfer Success |
| N03B4 | [INTENT CHECK](atomic/N03B4_INTENT_CHECK.md) | P1 | Intent Drift Detection |

## N03C｜SYNTHESIZE

Parent: [N03C SYNTHESIZE](N03C_SYNTHESIZE.md)

| Node | Atomic capability | Priority | Primary metric |
|---|---|---|---|
| N03C1 | [COMPLEXITY REVIEW](atomic/N03C1_COMPLEXITY_REVIEW.md) | P1 | Accepted Simplification |
| N03C2 | [SIMPLIFICATION / LOSS CHECK](atomic/N03C2_SIMPLIFICATION_LOSS_CHECK.md) | P0 | Simplification Loss Rejection |

## N04｜COMPARE

Parent: [N04 COMPARE](N04_COMPARE.md)

| Node | Atomic capability | Priority | Primary metric |
|---|---|---|---|
| N04A | [COMPARISON WORLD](atomic/N04A_COMPARISON_WORLD.md) | P0 | Comparison Validity |
| N04B | [TRADE-OFF](atomic/N04B_TRADEOFF.md) | P0 | Decision Usefulness |
| N04C | [DECISION RATIONALE](atomic/N04C_DECISION_RATIONALE.md) | P0 | Rationale Coverage |
| N04D | [REOPEN CONDITION](atomic/N04D_REOPEN_CONDITION.md) | P1 | Appropriate Reopen Rate |

## N05｜MAP

Parent: [N05 MAP](N05_MAP.md)

| Node | Atomic capability | Priority | Primary metric |
|---|---|---|---|
| N05A | [DESIGN RELATION](atomic/N05A_DESIGN_RELATION.md) | P0 | Relation Usefulness / Maintenance Burden |
| N05B | [CHANGE IMPACT](atomic/N05B_CHANGE_IMPACT.md) | P0 | Change Impact Precision |
| N05C | [REVISION SCOPE](atomic/N05C_REVISION_SCOPE.md) | P0 | Full-reset Avoidance / Preserved-valid-work |
| N05D | [PROFESSIONAL BINDING](atomic/N05D_PROFESSIONAL_BINDING.md) | P1 | Cross-domain Conflict Detection |

## N06｜ARTIFACTS

Parent: [N06 ARTIFACTS](N06_ARTIFACTS.md)

| Node | Atomic capability | Priority | Primary metric |
|---|---|---|---|
| N06A | [ARTIFACT IDENTITY](atomic/N06A_ARTIFACT_IDENTITY.md) | P0 | Artifact Identity Correction |
| N06B | [ARTIFACT ROLE](atomic/N06B_ARTIFACT_ROLE.md) | P0 | Role Misclassification Rate |
| N06C | [REVISION IDENTITY](atomic/N06C_REVISION_IDENTITY.md) | P0 | Revision Mismatch Rate |
| N06D | [READBACK](atomic/N06D_READBACK.md) | P0 | Readback Completion / Revision Integrity |
| N06E | [FIDELITY / CLAIM CEILING](atomic/N06E_FIDELITY_CLAIM_CEILING.md) | P0 | Claim-ceiling Violation Rate |
| N06F | [DEGRADED SUBSTITUTE](atomic/N06F_DEGRADED_SUBSTITUTE.md) | P1 | Degraded-workflow Success |

## N07｜REVIEW

Parent: [N07 REVIEW](N07_REVIEW.md)

| Node | Atomic capability | Priority | Primary metric |
|---|---|---|---|
| N07A | [REVIEW TARGET](atomic/N07A_REVIEW_TARGET.md) | P0 | Wrong-target Review Rate |
| N07B | [FINDING](atomic/N07B_FINDING.md) | P0 | Finding-to-Action Conversion |
| N07C | [ROOT-CAUSE HYPOTHESIS](atomic/N07C_ROOTCAUSE_HYPOTHESIS.md) | P0 | Repair Hypothesis Accuracy |
| N07D | [VERIFICATION](atomic/N07D_VERIFICATION.md) | P0 | Verification Claim Integrity |
| N07E | [VALIDATION](atomic/N07E_VALIDATION.md) | P0 | Validation Task/Outcome Success |
| N07F | [INDEPENDENT REVIEW](atomic/N07F_INDEPENDENT_REVIEW.md) | P1 | Independent Review Integrity |
| N07G | [RECHECK / RE-READBACK](atomic/N07G_RECHECK_REREADBACK.md) | P0 | Revision Re-readback Rate |

## N08｜KNOWLEDGE

Parent: [N08 KNOWLEDGE](N08_KNOWLEDGE.md)

| Node | Atomic capability | Priority | Primary metric |
|---|---|---|---|
| N08A | [KNOWLEDGE NEED](atomic/N08A_KNOWLEDGE_NEED.md) | P0 | Research-to-Design Conversion |
| N08B | [SOURCE / EVIDENCE](atomic/N08B_SOURCE_EVIDENCE.md) | P0 | Evidence Provenance Completeness |
| N08C | [APPLICABILITY / LIMITATION](atomic/N08C_APPLICABILITY_LIMITATION.md) | P0 | Applicability Correction Rate |
| N08D | [EVIDENCE CONTRADICTION](atomic/N08D_EVIDENCE_CONTRADICTION.md) | P1 | Contradiction Resolution Quality |
| N08E | [CLAIM CEILING](atomic/N08E_CLAIM_CEILING.md) | P0 | Overclaim Rate |

## N09｜HISTORY

Parent: [N09 HISTORY](N09_HISTORY.md)

| Node | Atomic capability | Priority | Primary metric |
|---|---|---|---|
| N09A | [DECISION HISTORY](atomic/N09A_DECISION_HISTORY.md) | P0 | Decision Trace Completeness |
| N09B | [REJECTED DIRECTION MEMORY](atomic/N09B_REJECTED_DIRECTION_MEMORY.md) | P1 | Rejected Branch Recoverability |
| N09C | [RESUME POINT](atomic/N09C_RESUME_POINT.md) | P0 | Resume-point Success |
| N09D | [HANDOFF PACK](atomic/N09D_HANDOFF_PACK.md) | P1 | Handoff Correction Rate |
| N09E | [PROJECT LEARNING CANDIDATE](atomic/N09E_PROJECT_LEARNING_CANDIDATE.md) | P2 | Transfer Correction / Reuse Value |

## N10｜SESSION KERNEL

Parent: [N10 SESSION KERNEL](N10_SESSION_KERNEL.md)

| Node | Atomic capability | Priority | Primary metric |
|---|---|---|---|
| N10F | [WORK INTENT](atomic/N10F_WORK_INTENT.md) | P0 | Intent Correction Rate |
| N10G | [MUTATION DIRECTIVE](atomic/N10G_MUTATION_DIRECTIVE.md) | P0 | Directive Violation Rate |
| N10H | [SUPPORT MODE](atomic/N10H_SUPPORT_MODE.md) | P1 | Explanation Interruption Rate |
| N10I | [HUMAN ACTION LEVEL](atomic/N10I_HUMAN_ACTION_LEVEL.md) | P0 | Action-level Collapse Rate |

## N11｜PEOPLE / AUTHORITY

Parent: [N11 PEOPLE / AUTHORITY](N11_PEOPLE_AUTHORITY.md)

| Node | Atomic capability | Priority | Primary metric |
|---|---|---|---|
| N11A | [ACTOR ROLE](atomic/N11A_ACTOR_ROLE.md) | P1 | Role Resolution Correction |
| N11B | [SCOPED RIGHTS](atomic/N11B_SCOPED_RIGHTS.md) | P0 | Unauthorized Override Rate |
| N11C | [CONFLICT HOLD](atomic/N11C_CONFLICT_HOLD.md) | P1 | Conflict Containment Rate |

## N12｜INTEGRATIONS

Parent: [N12 INTEGRATIONS](N12_INTEGRATIONS.md)

| Node | Atomic capability | Priority | Primary metric |
|---|---|---|---|
| N12A | [INTEGRATION CONTRACT](atomic/N12A_INTEGRATION_CONTRACT.md) | P1 | Integration Success / Misroute |
| N12B | [EXTERNAL WRITE](atomic/N12B_EXTERNAL_WRITE.md) | P0 | Unauthorized External Write |
| N12C | [DEGRADED INTEGRATION](atomic/N12C_DEGRADED_INTEGRATION.md) | P1 | Degraded Route Success |

## N13｜SETTINGS

Parent: [N13 SETTINGS](N13_SETTINGS.md)

| Node | Atomic capability | Priority | Primary metric |
|---|---|---|---|
| N13A | [DATA / PRIVACY SETTINGS](atomic/N13A_DATA_PRIVACY_SETTINGS.md) | P2 | Privacy Setting Comprehension |
| N13B | [CONNECTOR PERMISSIONS](atomic/N13B_CONNECTOR_PERMISSIONS.md) | P2 | Overbroad Permission Rate |
| N13C | [ACCESSIBILITY SETTINGS](atomic/N13C_ACCESSIBILITY_SETTINGS.md) | P2 | Accessibility Task Success |

## N14｜SYSTEM HEALTH

Parent: [N14 SYSTEM HEALTH](N14_SYSTEM_HEALTH.md)

| Node | Atomic capability | Priority | Primary metric |
|---|---|---|---|
| N14A | [HEALTH SIGNAL](atomic/N14A_HEALTH_SIGNAL.md) | P1 | Health Signal Accuracy |
| N14B | [DEGRADED ROUTE](atomic/N14B_DEGRADED_ROUTE.md) | P1 | Truthful Degradation Rate |
| N14C | [INCIDENT / RECOVERY](atomic/N14C_INCIDENT_RECOVERY.md) | P1 | Recovery Time / Data-loss Incidents |
