# Governance v1.0.1

Status: ACTIVE
Evidence: E2
Owner: 刘旋 / OLEANDER／织作

## Layers
- Business: B01 Positioning & Value; B02 Model & Offering; B03 Operation & Partnership; B04 Metrics & Governance.
- Culture: CU01 Source & Context; CU02 Knowledge & Interpretation; CU03 Participation & Rights; CU04 Continuity & Renewal.
- IP: IP01 Identity & Naming; IP02 Narrative & Content; IP03 Visual & Verbal System; IP04 Application & Licensing.
- Spatial: SP01 Site & Evidence; SP02 Program & Relations; SP03 Space & Experience; SP04 Construction & Operation.

## Cases
- C01: 一脉广渡. Legacy: CASE/GD, old 03 and P00 pages. Primary: Culture + Spatial. Status: RESEARCH + PROPOSAL / EVIDENCE REVIEW.
- C02: 忘也 Daylily. Legacy: CASE/DY, old 03C. Primary: Business + IP + Spatial. Status: INDEPENDENT PORTFOLIO / PROTOTYPED / TEST PLANNED / NOT RUN.
- C03: The Light Collection / Reno CMF independent concept proposal. Legacy: CASE/LC, old 03D. Primary: IP. Status: PORTFOLIO CONCEPT / VISUALIZED / SAMPLE TEST PENDING. Do not imply OPPO commission, adoption, production, or endorsement.

## Identity
- IP-NM-001 v1.0.0 ACTIVE E2
- IP-IA-001 OPEN E1; the recovered v0.4 source is LEGACY / READ-ONLY evidence only.
- IP-WM-001 OPEN E0; Wordmark v0.8.1 is DEPRECATED / LINK_ONLY and does not define the current object.
- IP-SM-001 OPEN E0; rejected v0.5 remains excluded.
- IP-LK-001 OPEN E0; R4C-G2 is DEPRECATED / LINK_ONLY and must not be reconstructed from previews.
- v0.7 and v0.7-R1 remain LEGACY comparison inputs.

## Migration v1.0.1
- Migration-level HOLD: 0.
- Located and hashed legacy v0.4 and rejected v0.5 sources.
- Decoupled missing legacy aliases from current-object creation.
- Current-object design, recognition, physical reproduction and E4 rights/release gates remain open.
- See `00-governance/migration/`.

## Status Codes
OPEN / WIP / PROTO / CAND / REVIEW / ACTIVE / APPROVED / RELEASED / HOLD / REJECTED / DEPRECATED / LEGACY / ARCHIVED

## Evidence Codes
E0 unlocated; E1 source located; E2 internal validation; E3 real-world validation; E4 approved release with rights, hash, and rollback record.

## Mandatory Post-Generation Review Gate

Canonical rule: [`post-generation-review-gate.md`](post-generation-review-gate.md)

所有设计与技术输出必须在生成/导出/自动 QA 后，再执行一次独立成品审查。未执行时状态为 `REVIEW PENDING`；发现问题为 `POST-REVIEW FAIL / NEEDS REVISION`；只有修正并重审达到 `POST-REVIEW PASS`，才允许升级为 DONE / PASS / Candidate。

自动 QA、脚本 PASS、bbox=0、文件存在或可复现运行，都不能替代最终成品审查。成品审查必须覆盖实际视觉、图文边界、几何—标注一致性、比例/尺度、构造逻辑、证据状态和最终文件复现。
