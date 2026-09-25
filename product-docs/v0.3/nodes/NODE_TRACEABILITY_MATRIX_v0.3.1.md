# OLEANDER Node Traceability Matrix v0.3.1

[← Node Graph](README.md) · [Atomic Node Index](ATOMIC_NODE_INDEX.md)

> 这一层回答 Node → Requirement → Metric。详细 User Need / Requirement Family / Verification Method 继续由 v0.2 traceability baseline 承担。

```mermaid
flowchart LR
    U[User Need] --> N[Product Node]
    N --> R[Requirement ID]
    R --> A[Acceptance]
    A --> M[Metric / Eval]
```

| Atomic Node | Parent | Requirement IDs | Priority | Primary metric |
|---|---|---|---|---|
| [N01A RESUME SNAPSHOT](atomic/N01A_RESUME_SNAPSHOT.md) | N01 HOME | HOME-F01<br>HOME-F07<br>INT-F25 | P0 | Resume Accuracy / Resume Correction |
| [N01B FRONTIER](atomic/N01B_FRONTIER.md) | N01 HOME | HOME-F02<br>FOCUS-F09<br>DEV-F02 | P0 | Frontier Correction Rate |
| [N01C CRITICAL OPEN](atomic/N01C_CRITICAL_OPEN.md) | N01 HOME | HOME-F03<br>UN-P28<br>UN-P35 | P0 | Critical-open Resolution Rate |
| [N01D ACTIVE ARTIFACT](atomic/N01D_ACTIVE_ARTIFACT.md) | N01 HOME | HOME-F04<br>ART-F01<br>ART-F02<br>ART-F03 | P0 | Active Artifact Correction Rate |
| [N01E NEXT ACTION](atomic/N01E_NEXT_ACTION.md) | N01 HOME | HOME-F06<br>UN-P03<br>INT-F16 | P0 | Next-action Acceptance / Correction |
| [N02A PROBLEM STATEMENT](atomic/N02A_PROBLEM_STATEMENT.md) | N02 FOCUS | FOCUS-F01<br>SR-PF | P0 | Problem Reframe Rate |
| [N02B CURRENT DESIGN QUESTION](atomic/N02B_CURRENT_DESIGN_QUESTION.md) | N02 FOCUS | FOCUS-F02<br>UN-P02 | P0 | Question Clarity / Correction |
| [N02C DESIGN VALUE / INTENT](atomic/N02C_DESIGN_VALUE_INTENT.md) | N02 FOCUS | FOCUS-F03<br>UN-P07<br>SR-DV | P0 | Intent Drift Detection / Human Correction |
| [N02D CONSTRAINT / ASSUMPTION](atomic/N02D_CONSTRAINT_ASSUMPTION.md) | N02 FOCUS | FOCUS-F05<br>UN-P08<br>UN-P27 | P0 | Stale Assumption Detection |
| [N02E SUCCESS CONDITION](atomic/N02E_SUCCESS_CONDITION.md) | N02 FOCUS | FOCUS-F06 | P1 | Success-condition Rework |
| [N02F REFRAME](atomic/N02F_REFRAME.md) | N02 FOCUS | FOCUS-F07<br>FOCUS-F08<br>UN-P36 | P0 | Reframe-to-Recovery Time |
| [N03A1 DESIGN DIRECTION](atomic/N03A1_DESIGN_DIRECTION.md) | N03A EXPLORE | EXP-F01<br>EXP-F02 | P0 | Direction Usefulness |
| [N03A2 ALTERNATIVE SET](atomic/N03A2_ALTERNATIVE_SET.md) | N03A EXPLORE | EXP-F04<br>CMP-F09 | P0 | Comparable Set Quality |
| [N03A3 MATERIAL DISTINCTNESS](atomic/N03A3_MATERIAL_DISTINCTNESS.md) | N03A EXPLORE | EXP-F03<br>EXP-F09 | P0 | Material Divergence / Cosmetic Duplicate |
| [N03A4 BASELINE / OFF](atomic/N03A4_BASELINE_OFF.md) | N03A EXPLORE | EXP-F08 | P1 | Baseline Consideration Rate |
| [N03A5 REFERENCE TRANSFORMATION](atomic/N03A5_REFERENCE_TRANSFORMATION.md) | N03A EXPLORE | EXP-F06<br>KNW-F08 | P1 | Precedent Transfer Correction |
| [N03B1 MATURITY GAP](atomic/N03B1_MATURITY_GAP.md) | N03B DEVELOP | DEV-F01 | P1 | Maturity-gap Correction |
| [N03B2 DEVELOPMENT FRONTIER](atomic/N03B2_DEVELOPMENT_FRONTIER.md) | N03B DEVELOP | DEV-F02<br>DEV-F07 | P0 | Development Frontier Correction |
| [N03B3 DOMAIN ADAPTER](atomic/N03B3_DOMAIN_ADAPTER.md) | N03B DEVELOP | DEV-F08<br>INT-F28 | P0 | Cross-domain Transfer Success |
| [N03B4 INTENT CHECK](atomic/N03B4_INTENT_CHECK.md) | N03B DEVELOP | DEV-F05 | P1 | Intent Drift Detection |
| [N03C1 COMPLEXITY REVIEW](atomic/N03C1_COMPLEXITY_REVIEW.md) | N03C SYNTHESIZE | SYN-F01<br>SYN-F02<br>SYN-F03 | P1 | Accepted Simplification |
| [N03C2 SIMPLIFICATION / LOSS CHECK](atomic/N03C2_SIMPLIFICATION_LOSS_CHECK.md) | N03C SYNTHESIZE | SYN-F06<br>SYN-F07 | P0 | Simplification Loss Rejection |
| [N04A COMPARISON WORLD](atomic/N04A_COMPARISON_WORLD.md) | N04 COMPARE | CMP-F01<br>CMP-F09<br>CMP-F10 | P0 | Comparison Validity |
| [N04B TRADE-OFF](atomic/N04B_TRADEOFF.md) | N04 COMPARE | CMP-F02<br>CMP-F03<br>CMP-F04<br>CMP-F05 | P0 | Decision Usefulness |
| [N04C DECISION RATIONALE](atomic/N04C_DECISION_RATIONALE.md) | N04 COMPARE | CMP-F06<br>HIS-F02 | P0 | Rationale Coverage |
| [N04D REOPEN CONDITION](atomic/N04D_REOPEN_CONDITION.md) | N04 COMPARE | CMP-F07<br>HIS-F02 | P1 | Appropriate Reopen Rate |
| [N05A DESIGN RELATION](atomic/N05A_DESIGN_RELATION.md) | N05 MAP | MAP-F01<br>MAP-F02<br>MAP-F03<br>MAP-F04 | P0 | Relation Usefulness / Maintenance Burden |
| [N05B CHANGE IMPACT](atomic/N05B_CHANGE_IMPACT.md) | N05 MAP | MAP-F05<br>MAP-F10<br>UN-P20<br>UN-P36 | P0 | Change Impact Precision |
| [N05C REVISION SCOPE](atomic/N05C_REVISION_SCOPE.md) | N05 MAP | MAP-F11<br>REV-F07<br>UN-P36 | P0 | Full-reset Avoidance / Preserved-valid-work |
| [N05D PROFESSIONAL BINDING](atomic/N05D_PROFESSIONAL_BINDING.md) | N05 MAP | MAP-F09<br>DEV-F08<br>PEO-F02 | P1 | Cross-domain Conflict Detection |
| [N06A ARTIFACT IDENTITY](atomic/N06A_ARTIFACT_IDENTITY.md) | N06 ARTIFACTS | ART-F01<br>ART-F03 | P0 | Artifact Identity Correction |
| [N06B ARTIFACT ROLE](atomic/N06B_ARTIFACT_ROLE.md) | N06 ARTIFACTS | ART-F02 | P0 | Role Misclassification Rate |
| [N06C REVISION IDENTITY](atomic/N06C_REVISION_IDENTITY.md) | N06 ARTIFACTS | ART-F04<br>ART-F10 | P0 | Revision Mismatch Rate |
| [N06D READBACK](atomic/N06D_READBACK.md) | N06 ARTIFACTS | ART-F07<br>REV-F13<br>INT-F21 | P0 | Readback Completion / Revision Integrity |
| [N06E FIDELITY / CLAIM CEILING](atomic/N06E_FIDELITY_CLAIM_CEILING.md) | N06 ARTIFACTS | ART-F09<br>KNW-F11<br>REV-F12 | P0 | Claim-ceiling Violation Rate |
| [N06F DEGRADED SUBSTITUTE](atomic/N06F_DEGRADED_SUBSTITUTE.md) | N06 ARTIFACTS | ART-F12<br>NFR-10 | P1 | Degraded-workflow Success |
| [N07A REVIEW TARGET](atomic/N07A_REVIEW_TARGET.md) | N07 REVIEW | REV-F01 | P0 | Wrong-target Review Rate |
| [N07B FINDING](atomic/N07B_FINDING.md) | N07 REVIEW | REV-F02<br>REV-F03<br>REV-F04<br>REV-F05 | P0 | Finding-to-Action Conversion |
| [N07C ROOT-CAUSE HYPOTHESIS](atomic/N07C_ROOTCAUSE_HYPOTHESIS.md) | N07 REVIEW | REV-F06 | P0 | Repair Hypothesis Accuracy |
| [N07D VERIFICATION](atomic/N07D_VERIFICATION.md) | N07 REVIEW | REV-F11<br>SR-VF | P0 | Verification Claim Integrity |
| [N07E VALIDATION](atomic/N07E_VALIDATION.md) | N07 REVIEW | REV-F10<br>SR-VA | P0 | Validation Task/Outcome Success |
| [N07F INDEPENDENT REVIEW](atomic/N07F_INDEPENDENT_REVIEW.md) | N07 REVIEW | REV-F09<br>UN-P33 | P1 | Independent Review Integrity |
| [N07G RECHECK / RE-READBACK](atomic/N07G_RECHECK_REREADBACK.md) | N07 REVIEW | REV-F08<br>REV-F13 | P0 | Revision Re-readback Rate |
| [N08A KNOWLEDGE NEED](atomic/N08A_KNOWLEDGE_NEED.md) | N08 KNOWLEDGE | KNW-F01 | P0 | Research-to-Design Conversion |
| [N08B SOURCE / EVIDENCE](atomic/N08B_SOURCE_EVIDENCE.md) | N08 KNOWLEDGE | KNW-F02<br>KNW-F03 | P0 | Evidence Provenance Completeness |
| [N08C APPLICABILITY / LIMITATION](atomic/N08C_APPLICABILITY_LIMITATION.md) | N08 KNOWLEDGE | KNW-F04<br>KNW-F05<br>KNW-F06 | P0 | Applicability Correction Rate |
| [N08D EVIDENCE CONTRADICTION](atomic/N08D_EVIDENCE_CONTRADICTION.md) | N08 KNOWLEDGE | KNW-F07 | P1 | Contradiction Resolution Quality |
| [N08E CLAIM CEILING](atomic/N08E_CLAIM_CEILING.md) | N08 KNOWLEDGE | KNW-F11<br>REV-F12<br>ART-F09 | P0 | Overclaim Rate |
| [N09A DECISION HISTORY](atomic/N09A_DECISION_HISTORY.md) | N09 HISTORY | HIS-F02<br>CMP-F06<br>CMP-F07 | P0 | Decision Trace Completeness |
| [N09B REJECTED DIRECTION MEMORY](atomic/N09B_REJECTED_DIRECTION_MEMORY.md) | N09 HISTORY | HIS-F03<br>EXP-F07 | P1 | Rejected Branch Recoverability |
| [N09C RESUME POINT](atomic/N09C_RESUME_POINT.md) | N09 HISTORY | HIS-F06<br>INT-F25<br>INT-F26 | P0 | Resume-point Success |
| [N09D HANDOFF PACK](atomic/N09D_HANDOFF_PACK.md) | N09 HISTORY | HIS-F07<br>SR-IF | P1 | Handoff Correction Rate |
| [N09E PROJECT LEARNING CANDIDATE](atomic/N09E_PROJECT_LEARNING_CANDIDATE.md) | N09 HISTORY | HIS-F09<br>SR-PL | P2 | Transfer Correction / Reuse Value |
| [N10F WORK INTENT](atomic/N10F_WORK_INTENT.md) | N10 SESSION KERNEL | INT-F01 | P0 | Intent Correction Rate |
| [N10G MUTATION DIRECTIVE](atomic/N10G_MUTATION_DIRECTIVE.md) | N10 SESSION KERNEL | INT-F02<br>INT-F20 | P0 | Directive Violation Rate |
| [N10H SUPPORT MODE](atomic/N10H_SUPPORT_MODE.md) | N10 SESSION KERNEL | INT-F03<br>INT-F23<br>INT-F24 | P1 | Explanation Interruption Rate |
| [N10I HUMAN ACTION LEVEL](atomic/N10I_HUMAN_ACTION_LEVEL.md) | N10 SESSION KERNEL | INT-F04<br>INT-F05 | P0 | Action-level Collapse Rate |
| [N11A ACTOR ROLE](atomic/N11A_ACTOR_ROLE.md) | N11 PEOPLE / AUTHORITY | PEO-F01 | P1 | Role Resolution Correction |
| [N11B SCOPED RIGHTS](atomic/N11B_SCOPED_RIGHTS.md) | N11 PEOPLE / AUTHORITY | PEO-F02 | P0 | Unauthorized Override Rate |
| [N11C CONFLICT HOLD](atomic/N11C_CONFLICT_HOLD.md) | N11 PEOPLE / AUTHORITY | PEO-F03 | P1 | Conflict Containment Rate |
| [N12A INTEGRATION CONTRACT](atomic/N12A_INTEGRATION_CONTRACT.md) | N12 INTEGRATIONS | SR-IF<br>NFR-10 | P1 | Integration Success / Misroute |
| [N12B EXTERNAL WRITE](atomic/N12B_EXTERNAL_WRITE.md) | N12 INTEGRATIONS | INT-F16<br>INT-F17<br>PEO-F02 | P0 | Unauthorized External Write |
| [N12C DEGRADED INTEGRATION](atomic/N12C_DEGRADED_INTEGRATION.md) | N12 INTEGRATIONS | ART-F12<br>NFR-10 | P1 | Degraded Route Success |
| [N13A DATA / PRIVACY SETTINGS](atomic/N13A_DATA_PRIVACY_SETTINGS.md) | N13 SETTINGS | NFR-12 | P2 | Privacy Setting Comprehension |
| [N13B CONNECTOR PERMISSIONS](atomic/N13B_CONNECTOR_PERMISSIONS.md) | N13 SETTINGS | NFR-05<br>N12A | P2 | Overbroad Permission Rate |
| [N13C ACCESSIBILITY SETTINGS](atomic/N13C_ACCESSIBILITY_SETTINGS.md) | N13 SETTINGS | NFR-07 | P2 | Accessibility Task Success |
| [N14A HEALTH SIGNAL](atomic/N14A_HEALTH_SIGNAL.md) | N14 SYSTEM HEALTH | NFR-03<br>NFR-06 | P1 | Health Signal Accuracy |
| [N14B DEGRADED ROUTE](atomic/N14B_DEGRADED_ROUTE.md) | N14 SYSTEM HEALTH | NFR-10<br>N12C | P1 | Truthful Degradation Rate |
| [N14C INCIDENT / RECOVERY](atomic/N14C_INCIDENT_RECOVERY.md) | N14 SYSTEM HEALTH | NFR-02<br>NFR-06<br>Launch Readiness | P1 | Recovery Time / Data-loss Incidents |
