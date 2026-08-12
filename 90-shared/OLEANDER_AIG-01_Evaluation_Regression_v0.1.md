# OLEANDER AIG-01｜AI Evaluation & Regression v0.1

Status: ACTIVE governance protocol when present on `main` / E1 static corpus gate required / not evidence of model reliability
Canonical method source: Notion `AIG-01｜AI Evaluation & Regression Protocol v0.1｜评估与回归`

## Namespace rule
`AIG-01` is the current AI-governance identifier. `P0` is reserved by the project axis for `Portfolio` and must not be reused for AI governance. Historical records that already contain AI `P0` remain immutable audit evidence only.

`L0–L7` is reserved for Knowledge Architecture. AIG evaluation depth therefore uses the explicit `EVAL-*` namespace rather than bare `L*` labels.

## Retrieval alias / authority routing
Canonical query: **What happens when a model, prompt, skill, tool or retrieval policy changes?**

Search aliases: `model change`, `prompt change`, `skill update`, `tool change`, `retrieval policy change`, `AI change control`, `regression gate`, `rollback`.

Authority rule: a model, prompt, skill, tool, retrieval policy, parser, canonical source, rendering path, or automation change is a governed candidate change. It must be evaluated against the approved baseline, cannot silently replace the current default, and must retain a rollback point. The full canonical method remains Notion `AIG-01｜AI Evaluation & Regression Protocol v0.1｜评估与回归`; this file is the GitHub execution contract.

## Purpose
AIG-01 prevents AI from becoming an unexamined default. It adds four controls before and around all AI-assisted design work:

1. AI Necessity Gate
2. AI Eval Harness
3. Retrieval & Context QA
4. AI Change / Regression Gate

AI may help execute these checks, but cannot close an AIG-01 gate on itself.

---

## AIG-01.1 | AI Necessity Gate
Run before assigning a task to AI.

### Required questions
- Task / object / version
- Why is AI needed for this task?
- Can a deterministic rule, normal software, script, expert review, or physical test answer it more reliably?
- What value does AI add: retrieval, comparison, clustering, bounded divergence, interpretation, translation, or automation?
- What is the cost if AI is wrong?
- What evidence must remain outside AI?
- What is the human fallback?
- What condition forces AI to stop or escalate?

### Decision
- `NO-AI`: deterministic / professional / physical route is better.
- `AI-ASSIST`: AI may retrieve, compare, structure, generate bounded variants, or analyze.
- `AI-EXECUTE-BOUNDED`: AI may execute a deterministic or reconstructable task inside locked inputs.
- `HOLD`: task is blocked by missing evidence, rights, safety, regulation, or responsibility.

### Hard rule
AI is never justified only because it is faster, available, visually impressive, or able to generate many options.

---

## AIG-01.2 | AI Eval Harness
Every reusable OLEANDER skill, prompt family, or model-dependent workflow must be tested against task-specific cases.

### Eval layers
1. `EVAL-1 Contract`: required fields, truth states, locked variables, output format.
2. `EVAL-2 Evidence`: source accuracy, unsupported claims, stale-source rejection, authority selection.
3. `EVAL-3 Task`: whether the task-specific output is correct and useful.
4. `EVAL-4 Safety / Rights`: whether the run incorrectly closes safety, legal, cultural, rights, privacy, or professional gates.
5. `EVAL-5 Regression`: whether a new model / prompt / skill version performs worse than the approved baseline.

These are AI evaluation dimensions, not Knowledge Architecture levels.

### Eval status
- `PASS`
- `PASS-WITH-WARNINGS`
- `FAIL`
- `HOLD-HUMAN-REVIEW`

### Core metrics
- unsupported-claim rate
- wrong-authority-source rate
- stale-source acceptance rate
- required-field omission rate
- human override rate
- task success rate
- regression count
- blocker escape rate

Scores never replace failure analysis. One blocker may fail a release even if the average score is high.

---

## AIG-01.3 | Retrieval & Context QA
Retrieval is a separate system to test. A fluent answer with the wrong source version is a failure.

### Golden query record
- Query ID
- User intent
- Expected canonical source(s)
- Allowed supporting source(s)
- Forbidden / legacy source(s)
- Required version / date / status
- Required truth state
- Required conflict warning
- Expected answer constraints

### Retrieval metrics
- canonical-source recall
- source-authority accuracy
- stale-source rate
- legacy-source contamination rate
- conflict-detection rate
- missing-evidence honesty rate

### Context pack rule
Every serious AI handoff must explicitly separate:
- Canonical rules
- Current object / version
- Approved evidence
- Legacy / rejected material
- Unknowns
- Locked variables
- Allowed variables
- Current gate
- Required output

Do not dump the full archive into context when a scoped pack can preserve authority more reliably.

---

## AIG-01.4 | AI Change & Regression Gate
Any change to model, prompt, skill, tool, retrieval policy, canonical source, parser, rendering path, or automation must be treated as a governed system change.

### Change record
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

### Decisions
- `PROMOTE`
- `PROMOTE-WITH-LIMITS`
- `HOLD`
- `ROLLBACK`

### Release gate
A candidate cannot be promoted when it introduces:
- unsupported factual claims
- worse source-authority selection
- loss of truth-state separation
- safety / rights / regulatory overreach
- broken reconstructability
- regression on a previously passing blocker case

Model / skill version changes are analogous to changing a measuring instrument: rerun the benchmark set before using the new version as the default.

---

## AIG-01 execution sequence
`Necessity → Context Pack → Eval / Retrieval QA → Work → Human Gate → Regression Record → Promote or Rollback`

## Repository implementation
- `evals/golden/` — task-specific benchmark cases
- `evals/retrieval/` — canonical-source retrieval QA cases
- `evals/change-control/` — promotion and rollback records
- `evals/scripts/` — deterministic validators
- `.github/workflows/ai-governance-evals.yml` — CI gate

## Relationship to AIG-02 runtime governance and AIG-03 evidence
After AIG-01 authorizes AI use, `90-shared/OLEANDER_AIG-02_Failure_Trust_Provenance_v0.1.md` governs runtime failure/escalation, human-AI trust calibration and asset-level provenance. `90-shared/OLEANDER_AIG-03_Runtime_Evidence_v0.1.md` measures real operational evidence. An AIG-02 failure may force AIG-01 `HOLD` or `ROLLBACK`; repeated blockers must be added to regression coverage. AIG-03 evidence may narrow permissions or change future regression cases.

## Relationship to existing OLEANDER governance
- Truth states remain defined by AI Design Reasoning Protocol v0.2.
- E0–E4 remain defined by Validation Protocol.
- Simulation uses Simulation Protocol v0.2.
- Human authority, rights, regulation, physical testing and professional sign-off are not replaced by eval scores.
