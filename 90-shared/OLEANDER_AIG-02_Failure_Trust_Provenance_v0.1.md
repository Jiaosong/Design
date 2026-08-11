# OLEANDER AIG-02｜AI Failure, Trust & Provenance v0.1

Status: ACTIVE runtime-governance protocol when present on `main` / not evidence of automatic failure detection
Canonical method source: Notion `AIG-02｜AI Failure, Trust & Provenance Protocol v0.1｜失败、信任与来源`

## Namespace rule
`AIG-02` is the current AI runtime-governance identifier. `P1` is reserved by the project axis for `Program`. Historical records that already contain AI `P1` remain immutable audit evidence only.

## Purpose
AIG-01 governs whether AI should be used and whether a changed AI configuration may be promoted. AIG-02 governs runtime failure, human trust calibration and file-level provenance.

AIG-02 has three controls:
1. Failure & Escalation
2. Human-AI Trust Calibration
3. Asset-level Provenance

AI cannot close F2/F3 escalation gates on itself.

## AIG-02.1 | Failure & Escalation

### Failure taxonomy
- `F-SOURCE`: invented or non-traceable source; wrong authority source.
- `F-STALE`: legacy/rejected/superseded guidance treated as current.
- `F-TRUTH`: inference, hypothesis, unknown or simulation promoted to fact/observed result.
- `F-RIGHTS`: rights, privacy or cultural authorization unresolved.
- `F-SAFETY`: safety, regulation or professional authority overreach.
- `F-DATA`: wrong unit, denominator, field, version or missing-data handling.
- `F-GEOMETRY`: unit, axis, tolerance, locked-variable or reconstructability failure.
- `F-TOOL`: tool/MCP/API/parser/renderer failed, returned partial output or has unknown state.
- `F-CONFLICT`: agents/sources/simulations conflict without a defensible resolution.
- `F-PROVENANCE`: asset ingredients, action history or model/tool version cannot be traced.

### Escalation levels
- `F0 SELF-CORRECT`: low-risk, local and directly verifiable; correct and record.
- `F1 HUMAN-REVIEW`: affects design judgment; pause automatic progression and submit evidence/diff.
- `F2 DOMAIN-EXPERT`: safety, regulation, professional or cultural-rights issue; freeze conclusion.
- `F3 STOP-HOLD`: authority, rights, responsibility or tool state is unresolved; stop AI/publication path.

### Mandatory escalation
- Same blocker repeats twice: at least F1.
- AI conflicts with a canonical source and cannot explain the conflict: F1.
- D4 cultural/rights or D5 safety-critical data: at least F2.
- Unauthorised personal/client data, unknown publication rights, or repeated fabrication of unknowns: F3.
- Tool state is unknown and the action may be irreversible: F3.

### Recovery record
For F1–F3 record: `failure_id`, task, object/version, trigger, category, evidence, containment, escalation owner, recovery action, re-test, final state and residue.

## AIG-02.2 | Human-AI Trust Calibration
The goal is not to increase trust. The goal is calibrated reliance: the human should know when AI is useful, when it must be checked, and how to override it.

### AI Recommendation Card
Important AI recommendations must expose:
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

### Hard rules
- Do not use model self-reported confidence percentages as evidence strength.
- Fluency, visual realism, chain length or multi-agent agreement do not increase evidence level.
- Deterministic questions go to deterministic checks; reality questions go to reality tests.
- A2/A3 suggestions or reversible execution require preview, diff, affected scope, rollback path and owner.
- Human overrides remain part of the archive; they are not deleted as noise.

## AIG-02.3 | Asset-level Provenance
Media rights remain governed by Notion `04C｜Media Assets & Rights｜媒介资产与权利`. AIG-02 adds a portable file-level manifest.

### Minimum fields
- Asset ID / project / object version
- Original source / creator / rights holder
- Rights status / publish permission
- Input asset IDs / ingredients
- Creation method: HUMAN / AI-ASSISTED / AI-GENERATED / HYBRID / UNKNOWN
- AI model/tool/version
- Prompt/instruction/workflow version
- Action history
- Human edits / human responsibility
- Evidence status / known unknowns
- Generation/edit date
- File hash / manifest version
- Withdrawal/delete/replace path

A final asset cannot become the start of its own provenance chain. Composed assets must retain traceable ingredients.

### C2PA compatibility direction
OLEANDER manifests are governance records, not cryptographic authenticity claims. Future C2PA support should map ingredients, actions, assertions, content binding and active manifest where available. C2PA never replaces copyright, cultural authorization or design responsibility.

## AIG-02 execution sequence
`AIG-01 Necessity/Permission → Context Pack → AI Work → Recommendation Card / Provenance Record → Failure Detection → F0/F1/F2/F3 → Human/Expert/Rights Holder/Reality Test → Recovery + Re-test + Residue → AIG-01 Regression/Promote/Hold/Rollback`

## Repository implementation
- `evals/failure/FAILURE_ESCALATION_PLAYBOOK.md`
- `evals/failure/failure_cases.jsonl`
- `evals/trust/AI_RECOMMENDATION_CARD.md`
- `evals/provenance/ASSET_PROVENANCE_MANIFEST_TEMPLATE.json`
- `evals/scripts/validate_evals.py` validates AIG-01 + AIG-02 + AIG-03 governance corpus.

## Evidence boundary
Static CI proves the protocol corpus is structurally present and internally consistent. It does not prove that AI failures are automatically detected, that human trust is calibrated in practice, or that assets carry cryptographically verifiable Content Credentials.
