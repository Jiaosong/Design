# OLEANDER PRD Traceability Matrix v0.2.0

[← Master PRD](OLEANDER_DESIGN_COLLABORATION_PRD_v0.2.0.md)

**Purpose:** 把产品 Feature 反向追踪到用户需求、体验主题、Functional Architecture / System Requirement family 和验证方式。  
**Boundary:** 本表是 Product trace，不替代 v1.7.0 System Requirements 的正式逐条 trace。

Verification codes：
- INSP — Inspection
- ANAL — Analysis
- DEMO — Demonstration
- TEST — Test
- REVIEW — Expert / Design Review
- USER — User Evaluation
- PROJ — Real Project Exercise
- TRACE — Traceability Review

---

# 1｜HOME / FOCUS

| Feature | User Need | Upstream design activity | System requirement family | Verification | Priority |
|---|---|---|---|---|---|
| HOME-F01 Resume Snapshot | UN-P01–06 | CONTINUITY / RESUME | SR-CT / SR-IM / SR-DG | TEST + PROJ + USER | P0 |
| HOME-F02 Frontier Card | UN-P02/03/17 | FRAME / DEVELOP | SR-PF / SR-DD / SR-CV | USER + PROJ | P0 |
| HOME-F03 Critical Open | UN-P03/28/35 | CONVERGE / RECOVER | SR-CV / SR-RR | TEST + USER | P0 |
| HOME-F04 Active Artifact | UN-P22–25 | MATERIALIZE / READBACK | SR-DR / SR-RB | INSP + TEST | P0 |
| HOME-F05 Recent Design Moves | UN-P05/15/16 | CONTINUITY | SR-CT | INSP + PROJ | P1 |
| HOME-F06 Next Design Actions | UN-P03/17 | FRAME / DEVELOP | SR-PF / SR-DD | USER + PROJ | P0 |
| HOME-F07 Source Basis | UN-P04/27/28 | CONTINUITY / EVIDENCE | SR-IM / SR-CT | INSP + TEST | P1 |
| HOME-F08 Session Delta | UN-P05/06 | CONTINUITY | SR-CT | TEST + PROJ | P1 |
| FOCUS-F01 Problem Statement | UN-P02/08 | DISCOVER / FRAME | SR-PF | DEMO + REVIEW | P0 |
| FOCUS-F02 Current Question | UN-P02 | FRAME | SR-PF | DEMO + REVIEW | P0 |
| FOCUS-F03 Design Value | UN-P07/30 | FRAME / VALUE | SR-DV / SR-HA | REVIEW + USER | P0 |
| FOCUS-F04 Scope / Scale | UN-P02/20 | FRAME | SR-PF / SR-IN | DEMO | P1 |
| FOCUS-F05 Constraints / Assumptions | UN-P08/27/28 | INTERPRET / FRAME | SR-PF / SR-IM | INSP + TEST | P0 |
| FOCUS-F06 Success Condition | UN-P02/17 | FRAME | SR-PF / SR-CV | REVIEW + USER | P1 |
| FOCUS-F07 Reframe | UN-P02/35/36 | REFRAME | SR-PF / SR-RR | TEST + PROJ | P0 |
| FOCUS-F08 Reframe Impact | UN-P19/20/36 | REFRAME / INTEGRATE | SR-IN / SR-RR | ANAL + TEST | P0 |
| FOCUS-F09 Frontier | UN-P03/17 | DEVELOP | SR-DD / SR-CV | USER + PROJ | P0 |

---

# 2｜STUDIO / COMPARE

| Feature | User Need | Upstream activity | Requirement family | Verification | Priority |
|---|---|---|---|---|---|
| EXP-F01 Direction | UN-P12 | GENERATE | SR-EX | DEMO + REVIEW | P0 |
| EXP-F02 Strategy Statement | UN-P12/14 | GENERATE | SR-EX / SR-DJ | REVIEW | P0 |
| EXP-F03 Relation Difference | UN-P12 | GENERATE / JUDGE | SR-EX / SR-DJ | DEMO | P0 |
| EXP-F04 Alternative Set | UN-P12/14 | GENERATE / COMPARE | SR-EX / SR-DJ | TEST + USER | P0 |
| EXP-F05 Search-space Gap | UN-P12/13 | GENERATE | SR-EX | USER + PROJ | P1 |
| EXP-F06 Reference Transform | UN-P27/28 | INTERPRET / GENERATE | SR-PF / SR-EX / SR-IM | REVIEW + PROJ | P1 |
| EXP-F07 Hold/Continue/Retire | UN-P15/16/30 | CHOOSE | SR-DJ / SR-HA | TEST + USER | P0 |
| EXP-F08 Baseline/OFF | UN-P13 | GENERATE | SR-EX | DEMO + REVIEW | P1 |
| EXP-F09 Distinctness | UN-P12 | GENERATE | SR-EX | TEST + USER | P0 |
| DEV-F01 Maturity Gap | UN-P17 | DEVELOP | SR-DD | USER + REVIEW | P1 |
| DEV-F02 Next Frontier | UN-P17/18 | DEVELOP | SR-DD / SR-CV | USER + PROJ | P0 |
| DEV-F03 Resolution Ladder | UN-P18 | DEVELOP | SR-DD | DEMO | P1 |
| DEV-F04 Professional Depth | UN-P18/20 | DEVELOP | SR-DD / SR-IN | REVIEW + PROJ | P0 |
| DEV-F05 Intent Check | UN-P07/19 | DEVELOP / JUDGE | SR-DV / SR-DD | USER + REVIEW | P1 |
| DEV-F06 Low-resolution Warning | UN-P17/18 | DEVELOP | SR-DD | USER + PROJ | P1 |
| DEV-F07 Development Action | UN-P03/18 | DEVELOP / MATERIALIZE | SR-DD / SR-DR | DEMO + PROJ | P0 |
| DEV-F08 Domain Adapter | UN-P20/30 | DEVELOP / INTEGRATE | SR-CTX / SR-DD / SR-IN | ANAL + DEMO | P0 |
| DEV-F09 Whole Check | UN-P19/20 | INTEGRATE / JUDGE | SR-IN / SR-DJ | REVIEW | P1 |
| SYN-F01 Complexity Review | UN-P21 | SYNTHESIZE | SR-SY | USER + REVIEW | P1 |
| SYN-F02 Merge Opportunity | UN-P21 | SYNTHESIZE | SR-SY | DEMO + USER | P1 |
| SYN-F03 Design Economy | UN-P21 | SYNTHESIZE | SR-SY | ANAL + USER | P2 |
| SYN-F04 Grammar Consistency | UN-P19/21 | SYNTHESIZE | SR-SY / SR-DV | REVIEW | P1 |
| SYN-F05 Hierarchy Reinforcement | UN-P21 | SYNTHESIZE | SR-SY | REVIEW | P1 |
| SYN-F06 Simplification Test | UN-P21 | SYNTHESIZE / COMPARE | SR-SY / SR-DJ | DEMO + USER | P1 |
| SYN-F07 Loss Check | UN-P19/21 | SYNTHESIZE | SR-SY / SR-RR | TEST + REVIEW | P0 |
| CMP-F01 Side-by-side | UN-P14 | JUDGE | SR-DJ | DEMO + USER | P0 |
| CMP-F02 Relation Difference | UN-P12/14 | JUDGE | SR-DJ | DEMO | P0 |
| CMP-F03 Consequence Difference | UN-P14/20 | JUDGE | SR-DJ / SR-IN | ANAL + DEMO | P0 |
| CMP-F04 Trade-off | UN-P14/15 | JUDGE / CHOOSE | SR-DJ | USER + REVIEW | P0 |
| CMP-F05 Uncertainty | UN-P14/27 | JUDGE | SR-DJ / SR-IM | INSP + USER | P0 |
| CMP-F06 Rationale | UN-P15 | CHOOSE | SR-DJ / SR-CT | INSP + USER | P0 |
| CMP-F07 Reopen Condition | UN-P15/16 | CHOOSE / REVISE | SR-DJ / SR-RR | TEST | P1 |
| CMP-F08 Retained Alternative | UN-P16 | CHOOSE / CONTINUITY | SR-EX / SR-CT | TEST | P1 |
| CMP-F09 Same Comparison World | UN-P12/14 | JUDGE | SR-DJ / SR-IM | TEST | P0 |
| CMP-F10 Revision Binding | UN-P22–25 | JUDGE / REALITY | SR-DR / SR-RB / SR-IM | TEST | P0 |
| CMP-F11 Human Steer | UN-P29–32 | CHOOSE | SR-HA / SR-DJ | TEST + USER | P0 |

---

# 3｜MAP / ARTIFACTS

| Feature | User Need | Activity | Requirement family | Verification | Priority |
|---|---|---|---|---|---|
| MAP-F01 Relation Create | UN-P07/20 | FRAME / INTEGRATE | SR-DV / SR-IN / SR-IM | INSP + DEMO | P0 |
| MAP-F02 Relation Link | UN-P20 | INTEGRATE | SR-IN | INSP + ANAL | P0 |
| MAP-F03 Importance | UN-P17/20 | JUDGE | SR-DJ / SR-IN | USER | P1 |
| MAP-F04 Stability | UN-P15/17 | CHOOSE / DEVELOP | SR-DJ / SR-DD | INSP + USER | P1 |
| MAP-F05 Change Impact | UN-P20/36 | INTEGRATE / REVISE | SR-IN / SR-RR | ANAL + TEST | P0 |
| MAP-F06 Whole/Local | UN-P11/19 | JUDGE / INTEGRATE | SR-DJ / SR-IN | DEMO + USER | P1 |
| MAP-F07 Artifact Binding | UN-P22/25 | MATERIALIZE | SR-DR / SR-IM | INSP | P0 |
| MAP-F08 Finding Binding | UN-P09/10 | JUDGE | SR-DJ | INSP + DEMO | P0 |
| MAP-F09 Professional Binding | UN-P20/33 | INTEGRATE | SR-IN / SR-HA | ANAL + REVIEW | P1 |
| MAP-F10 Dependency Traversal | UN-P20/36 | INTEGRATE | SR-IN / SR-RR | ANAL + TEST | P1 |
| MAP-F11 Preserve Scope | UN-P19/36 | REVISE | SR-RR | TEST + PROJ | P0 |
| ART-F01 Artifact Register | UN-P22 | MATERIALIZE | SR-DR / SR-IM | INSP | P0 |
| ART-F02 Artifact Role | UN-P23/24 | MATERIALIZE | SR-DR / SR-IM | TEST | P0 |
| ART-F03 Native Link | UN-P22/23 | MATERIALIZE | SR-DR | DEMO + PROJ | P0 |
| ART-F04 Revision | UN-P22/25 | MATERIALIZE / REVISE | SR-DR / SR-RR | TEST | P0 |
| ART-F05 Relation Binding | UN-P07/22 | MATERIALIZE | SR-DR / SR-IM | INSP | P0 |
| ART-F06 Question Binding | UN-P02/22 | MATERIALIZE | SR-DR / SR-IM | INSP | P1 |
| ART-F07 Readback | UN-P24/25 | READBACK | SR-RB | TEST + DEMO | P0 |
| ART-F08 Version Compare | UN-P11/25 | READBACK / JUDGE | SR-RB / SR-DJ | DEMO | P1 |
| ART-F09 Fidelity | UN-P25/28 | VERIFY | SR-VF / SR-IM | INSP + REVIEW | P0 |
| ART-F10 Content Binding | UN-P22/25 | READBACK | SR-RB / SR-IM | TEST | P0 |
| ART-F11 Stale Warning | UN-P04/37 | CONTINUITY | SR-CT / SR-DG | TEST | P0 |
| ART-F12 Degraded Substitute | UN-P22/28/35 | DEGRADED OP | SR-DG / SR-DR | DEMO + TEST | P1 |

---

# 4｜REVIEW / KNOWLEDGE / HISTORY

| Feature | User Need | Activity | Requirement family | Verification | Priority |
|---|---|---|---|---|---|
| REV-F01 Review Target | UN-P25 | READBACK / JUDGE | SR-RB / SR-DJ | INSP + TEST | P0 |
| REV-F02 Finding | UN-P09/10 | JUDGE | SR-DJ | REVIEW + DEMO | P0 |
| REV-F03 Finding Type | UN-P10 | JUDGE | SR-DJ | TEST | P0 |
| REV-F04 Severity/Impact | UN-P10 | JUDGE | SR-DJ | USER + REVIEW | P1 |
| REV-F05 Affected Relation | UN-P09/20 | JUDGE | SR-DJ / SR-IN | INSP | P0 |
| REV-F06 Root Cause | UN-P09/35 | JUDGE / REVISE | SR-DJ / SR-RR | REVIEW + PROJ | P0 |
| REV-F07 Design Action | UN-P03/35 | REVISE | SR-RR / SR-DD | DEMO | P0 |
| REV-F08 Recheck | UN-P25/35 | READBACK / REVISE | SR-RB / SR-RR | TEST | P0 |
| REV-F09 Independent Review | UN-P10/30/33 | REVIEW | SR-DJ / SR-HA | REVIEW + INSP | P1 |
| REV-F10 Validation Scenario | UN-P26 | VALIDATE | SR-VA | USER + PROJ | P0 |
| REV-F11 Verification Claim | UN-P25/26/27 | VERIFY | SR-VF / SR-IM | TEST + TRACE | P0 |
| REV-F12 Does-not-prove | UN-P27/28 | VERIFY | SR-VF / SR-IM | INSP + REVIEW | P0 |
| REV-F13 Re-readback | UN-P25/35 | REVISE / READBACK | SR-RR / SR-RB | TEST | P0 |
| KNW-F01 Knowledge Need | UN-P27/28 | DISCOVER | SR-PF / SR-IM | DEMO | P0 |
| KNW-F02 Source | UN-P27 | DISCOVER | SR-IM | INSP | P0 |
| KNW-F03 Evidence Strength | UN-P27/28 | INTERPRET | SR-IM | INSP + REVIEW | P0 |
| KNW-F04 Applicability | UN-P27/28 | INTERPRET | SR-IM | REVIEW | P0 |
| KNW-F05 Design Meaning | UN-P27/28 | INTERPRET | SR-PF | DEMO + PROJ | P0 |
| KNW-F06 Limitation | UN-P27/28 | INTERPRET | SR-IM | INSP | P0 |
| KNW-F07 Contradiction | UN-P27 | INTERPRET | SR-IM | TEST + REVIEW | P1 |
| KNW-F08 Precedent | UN-P27/28 | INTERPRET | SR-PF / SR-EX | REVIEW + PROJ | P1 |
| KNW-F09 Return to Design | UN-P02/27 | INTERPRET | SR-PF / SR-IM | TRACE + PROJ | P0 |
| KNW-F10 Freshness | UN-P04/27 | CONTINUITY | SR-CT / SR-IM | TEST | P1 |
| KNW-F11 Claim Ceiling | UN-P28 | VERIFY | SR-VF / SR-IM | TEST + REVIEW | P0 |
| HIS-F01 Timeline | UN-P05 | CONTINUITY | SR-CT | INSP + PROJ | P1 |
| HIS-F02 Decision History | UN-P15 | CONTINUITY | SR-CT / SR-DJ | INSP | P0 |
| HIS-F03 Rejected Memory | UN-P16 | CONTINUITY | SR-CT / SR-EX | TEST | P1 |
| HIS-F04 Reframe History | UN-P05/36 | CONTINUITY | SR-CT / SR-PF | TEST | P1 |
| HIS-F05 Frontier History | UN-P01/17 | CONTINUITY | SR-CT / SR-CV | USER | P2 |
| HIS-F06 Resume Point | UN-P01–06 | CONTINUITY | SR-CT / SR-DG | TEST + PROJ | P0 |
| HIS-F07 Handoff | UN-P05/33 | CONTINUITY / INTERFACE | SR-CT / SR-IF | DEMO + PROJ | P1 |
| HIS-F08 Steer Lineage | UN-P15/16/29 | CONTINUITY | SR-CT / SR-HA | TEST | P0 |
| HIS-F09 Learning Candidate | UN-P38 | LEARN | SR-PL | REVIEW + TRACE | P2 |

---

# 5｜SESSION / PEOPLE

| Feature | User Need | Activity | Requirement family | Verification | Priority |
|---|---|---|---|---|---|
| INT-F01 Work Intent | UN-P29 | INTERACTION | SR-HA / SR-IF | TEST | P0 |
| INT-F02 Mutation Directive | UN-P29–31 | INTERACTION | SR-HA / SR-DG | TEST | P0 |
| INT-F03 Support Mode | UN-P34 | LEARN | SR-PL / SR-HA | USER + TEST | P1 |
| INT-F04 Action Level | UN-P29/30 | INTERACTION | SR-HA | TEST | P0 |
| INT-F05 Affective Feedback | UN-P09/34 | JUDGE | SR-DJ / SR-PL | USER + TEST | P0 |
| INT-F06 Steer Actions | UN-P29–32 | CHOOSE | SR-HA / SR-DJ | TEST | P0 |
| INT-F07 Referent Binding | UN-P32 | CHOOSE | SR-IM / SR-HA | TEST | P0 |
| INT-F08 Ambiguity | UN-P32 | CHOOSE | SR-HA / SR-DG | TEST + USER | P0 |
| INT-F09 Alias Collision | UN-P32 | INTERACTION | SR-IM | TEST | P0 |
| INT-F10 Compound Actions | UN-P29/32 | CHOOSE | SR-HA / SR-IM | TEST | P0 |
| INT-F11 Conflict Clarify | UN-P32 | CHOOSE | SR-HA | TEST | P0 |
| INT-F12 Parent Preservation | UN-P16 | CONTINUITY | SR-CT / SR-IM | TEST | P0 |
| INT-F13 Reject Preservation | UN-P16 | CONTINUITY | SR-CT | TEST | P0 |
| INT-F14 Defer | UN-P16/31 | CHOOSE | SR-HA / SR-RR | TEST | P0 |
| INT-F15 Reopen | UN-P16 | REVISE | SR-RR | TEST | P1 |
| INT-F16 Auto-advance | UN-P31 | EXECUTE | SR-HA / SR-DG | TEST + USER | P0 |
| INT-F17 Human Stop | UN-P30–33 | INTERACTION | SR-HA / SR-DG | TEST | P0 |
| INT-F18 Pre-write Freshness | UN-P37 | EXECUTE | SR-IM / SR-DG | TEST | P0 |
| INT-F19 Stale Block | UN-P37 | RECOVER | SR-RR / SR-DG | TEST | P0 |
| INT-F20 READ_ONLY | UN-P30 | INTERACTION | SR-HA | TEST | P0 |
| INT-F21 Second-round Proof | UN-P25/29 | MAKE / READBACK | SR-DR / SR-RB / SR-HA | TEST + PROJ | P0 |
| INT-F22 Invariants | UN-P19/25 | READBACK | SR-DV / SR-RB | TEST | P0 |
| PEO-F01 Actor Role | UN-P33 | AUTHORITY | SR-HA / SR-IF | INSP | P1 |
| PEO-F02 Scoped Rights | UN-P30/33 | AUTHORITY | SR-HA | TEST + REVIEW | P0 |
| PEO-F03 Conflict Hold | UN-P33/35 | AUTHORITY / RECOVER | SR-HA / SR-DG | TEST | P1 |
| INT-F23 Support Insert | UN-P34 | LEARN | SR-PL | USER | P1 |
| INT-F24 Support Fade | UN-P34 | LEARN | SR-PL / SR-HA | TEST + USER | P1 |
| INT-F25 Resume Precedence | UN-P01–06 | CONTINUITY | SR-CT / SR-IM | TEST + PROJ | P0 |
| INT-F26 Ephemeral Session | UN-P05/38 | CONTINUITY | SR-CT / SR-DG | TEST | P0 |
| INT-F27 Plugin-off | UN-P38 | CONTINUITY | SR-CT / SR-DG | TEST + PROJ | P1 |
| INT-F28 Domain Adapter | UN-P20/30 | PROFESSIONAL | SR-CTX / SR-IN / SR-HA | ANAL + DEMO | P0 |
| INT-F29 Closure | UN-P24–30 | REPORT | SR-IM / SR-HA | TEST + INSP | P0 |

---

# 6｜Coverage Rules

1. Feature 被实现，不等于对应 System Requirement 已完全验证。
2. Product acceptance 可以验证 UX / behaviour，但不能自动替代 professional validation。
3. 一条 Feature 可以覆盖多个 requirement families。
4. 一条 System Requirement 也可以跨多个 product surfaces 实现。
5. 未来 Logical / Physical Architecture 必须从正式 System Requirements 继续分配，不能把本 PRD 的界面结构直接当 software architecture。
