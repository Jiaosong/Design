# OLEANDER AIG-01｜AI Evaluation & Regression v0.1

Status: ACTIVE governance protocol when present on `main` / E1 static corpus gate required / not evidence of model reliability
Canonical method source: Notion `AIG-01｜AI Evaluation & Regression Protocol v0.1｜评估与回归`

## Namespace rule
`AIG-01` is the current AI-governance identifier. `P0` is reserved by the project axis for `Portfolio` and must not be reused for AI governance. Historical records that already contain `P0` remain immutable audit evidence only.

## Retrieval alias / authority routing
Canonical query: **What happens when a model, prompt, skill, tool or retrieval policy changes?**
Search aliases: `model change`, `prompt change`, `skill update`, `tool change`, `retrieval policy change`, `AI change control`, `regression gate`, `rollback`.
Authority rule: a model, prompt, skill, tool, retrieval policy, parser, canonical source, rendering path, or automation change is a governed candidate change. It must be evaluated against the approved baseline, cannot silently replace the current default, and must retain a rollback point.

## Purpose
AIG-01 prevents AI from becoming an unexamined default. It adds four controls before and around all AI-assisted design work:
1. AI Necessity Gate
2. AI Eval Harness
3. Retrieval & Context QA
4. AI Change / Regression Gate

AI may help execute these checks, but cannot close an AIG-01 gate on itself.

## AIG-01.1 | AI Necessity Gate
Run before assigning a task to AI.

Required questions:
- Task / object / version
- Why is AI needed for this task?
- Can a deterministic rule, normal software, script, expert review, or physical test answer it more reliably?
- What value does AI add: retrieval, comparison, clustering, bounded divergence, interpretation, translation, or automation?
- What is the cost if AI is wrong?
- What evidence must remain outside AI?
- What is the human fallback?
- What condition forces AI to stop or escalate?

Decision:
- `NO-AI`
- `AI-ASSIST`
- `AI-EXECUTE-BOUNDED`
- `HOLD`

Hard rule: AI is never justified only because it is faster, available, visually impressive, or able to generate many options.

## AIG-01.2 | AI Eval Harness
Every reusable OLEANDER skill, prompt family, or model-dependent workflow must be tested against task-specific cases.

Eval layers:
1. `L1 Contract`
2. `L2 Evidence`
3. `L3 Task`
4. `L4 Safety / Rights`
5. `L5 Regression`

Eval status: `PASS / PASS-WITH-WARNINGS / FAIL / HOLD-HUMAN-REVIEW`.

Core metrics include unsupported-claim rate, wrong-authority-source rate, stale-source acceptance rate, required-field omission rate, human override rate, task success rate, regression count and blocker escape rate. Scores never replace failure analysis.

## AIG-01.3 | Retrieval & Context QA
Retrieval is a separate system to test. A fluent answer with the wrong source version is a failure.

Golden query record:
- Query ID
- User intent
- Expected canonical source(s)
- Allowed supporting source(s)
- Forbidden / legacy source(s)
- Required version / date / status
- Required truth state
- Required conflict warning
- Expected answer constraints

Context packs explicitly separate Canonical rules, Current object/version, Approved evidence, Legacy/rejected material, Unknowns, Locked variables, Allowed variables, Current gate and Required output.

## AIG-01.4 | AI Change & Regression Gate
Any change to model, prompt, skill, tool, retrieval policy, canonical source, parser, rendering path, or automation is a governed system change.

Change record:
- Change ID
- Current approved version
- Candidate version
- Reason for change
- Affected skills / workflows / projects
- Golden set used
- Baseline result
- Candidate result
- New failures
- Resolved failures
- Human review
- Decision
- Rollback point

Decisions: `PROMOTE / PROMOTE-WITH-LIMITS / HOLD / ROLLBACK`.

A candidate cannot be promoted when it introduces unsupported factual claims, worse source-authority selection, loss of truth-state separation, safety/rights/regulatory overreach, broken reconstructability or regression on a previously passing blocker case.

## Execution sequence
`Necessity → Context Pack → Eval / Retrieval QA → Work → Human Gate → Regression Record → Promote or Rollback`

## Repository implementation
- `evals/golden/`
- `evals/retrieval/`
- `evals/change-control/`
- `evals/scripts/`
- `.github/workflows/ai-governance-evals.yml`

## Relationship to AIG-02 and AIG-03
After AIG-01 authorizes AI use, `OLEANDER_AIG-02_Failure_Trust_Provenance_v0.1.md` governs runtime failure/escalation, human-AI trust calibration and asset-level provenance. `OLEANDER_AIG-03_Runtime_Evidence_v0.1.md` measures real operational evidence. AIG-02 failures may force AIG-01 `HOLD` or `ROLLBACK`; AIG-03 evidence may change future AIG-01 permissions and regression coverage.

## Relationship to existing OLEANDER governance
Truth states remain defined by AI Design Reasoning Protocol v0.2. E0–E4 remain defined by Validation Protocol. Simulation uses Simulation Protocol v0.2. Human authority, rights, regulation, physical testing and professional sign-off are not replaced by eval scores.
