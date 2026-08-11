# OLEANDER AIG-02｜AI Failure, Trust & Provenance v0.1

Status: ACTIVE runtime-governance protocol when present on `main` / not evidence of automatic failure detection
Canonical method source: Notion `AIG-02｜AI Failure, Trust & Provenance Protocol v0.1｜失败、信任与来源`

## Namespace rule
`AIG-02` is the current AI runtime-governance identifier. `P1` is reserved by the project axis for `Program`. Historical records that already contain `P1` remain immutable audit evidence only.

## Purpose
AIG-01 governs whether AI should be used and whether a changed configuration may be promoted. AIG-02 governs runtime failure, human trust calibration and file-level provenance.

AIG-02 has three controls:
1. Failure & Escalation
2. Human-AI Trust Calibration
3. Asset-level Provenance

AI cannot close F2/F3 escalation gates on itself.

## AIG-02.1 | Failure & Escalation
Failure taxonomy:
- `F-SOURCE`
- `F-STALE`
- `F-TRUTH`
- `F-RIGHTS`
- `F-SAFETY`
- `F-DATA`
- `F-GEOMETRY`
- `F-TOOL`
- `F-CONFLICT`
- `F-PROVENANCE`

Escalation levels:
- `F0 SELF-CORRECT`
- `F1 HUMAN-REVIEW`
- `F2 DOMAIN-EXPERT`
- `F3 STOP-HOLD`

Mandatory escalation includes repeated blockers, unresolved conflict with canonical authority, D4/D5 high-risk data, unknown rights, repeated fabrication of unknowns and irreversible actions under unknown tool state.

For F1–F3 record: `failure_id`, task, object/version, trigger, category, evidence, containment, escalation owner, recovery action, re-test, final state and residue.

## AIG-02.2 | Human-AI Trust Calibration
The goal is calibrated reliance, not more trust.

AI Recommendation Card exposes:
- Recommendation
- Evidence Basis
- Truth State
- Assumptions
- Unknowns / Conflicts
- Alternatives
- Failure Modes
- What Would Falsify This
- Human Action Required
- Next Test

Hard rules:
- model self-reported confidence is not evidence strength;
- fluency, realism, chain length or multi-agent agreement do not increase evidence level;
- deterministic questions go to deterministic checks; reality questions go to reality tests;
- reversible execution requires preview/diff/scope/rollback/owner;
- human overrides remain evidence and are not discarded as noise.

## AIG-02.3 | Asset-level Provenance
Media rights remain governed by the current Media Assets & Rights canonical object. AIG-02 adds a portable file-level manifest.

Minimum fields:
- Asset ID / project / object version
- Original source / creator / rights holder
- Rights status / publish permission
- Input asset IDs / ingredients
- Creation method
- AI model/tool/version
- Prompt/instruction/workflow version
- Action history
- Human edits / responsibility
- Evidence status / known unknowns
- Generation/edit date
- File hash / manifest version
- Withdrawal/delete/replace path

A final asset cannot become the start of its own provenance chain. Composed assets retain traceable ingredients.

### C2PA compatibility direction
OLEANDER manifests are governance records, not cryptographic authenticity claims. Future C2PA support may map ingredients, actions, assertions, content binding and active manifest where available. C2PA never replaces copyright, cultural authorization or design responsibility.

## Execution sequence
`AIG-01 Necessity/Permission → Context Pack → AI Work → Recommendation Card / Provenance Record → Failure Detection → F0/F1/F2/F3 → Human/Expert/Rights Holder/Reality Test → Recovery + Re-test + Residue → AIG-01 Regression/Promote/Hold/Rollback`

## Repository implementation
- `evals/failure/FAILURE_ESCALATION_PLAYBOOK.md`
- `evals/failure/failure_cases.jsonl`
- `evals/trust/AI_RECOMMENDATION_CARD.md`
- `evals/provenance/ASSET_PROVENANCE_MANIFEST_TEMPLATE.json`
- `evals/scripts/validate_evals.py`

## Evidence boundary
Static CI proves the protocol corpus is structurally present and internally consistent. It does not prove failures are automatically detected, trust is calibrated in practice, or assets carry cryptographically verifiable Content Credentials.
