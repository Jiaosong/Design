# OLEANDER AI Governance P0 v0.1

Status: DRAFT for review / intended to extend `OLEANDER_AI_Design_Reasoning_Protocol_v0.2.md`
Canonical method source: Notion `01B｜OLEANDER AI 协同设计方法｜读取、反馈与验证`

## Purpose
P0 prevents AI from becoming an unexamined default. It adds four controls before and around all AI-assisted design work:

1. AI Necessity Gate
2. AI Eval Harness
3. Retrieval & Context QA
4. AI Change / Regression Gate

AI may help execute these checks, but cannot close a P0 gate on itself.

---

## P0-1 | AI Necessity Gate

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

## P0-2 | AI Eval Harness

Every reusable OLEANDER skill, prompt family, or model-dependent workflow must be tested against task-specific cases.

### Eval layers
1. `L1 Contract`: required fields, truth states, locked variables, output format.
2. `L2 Evidence`: source accuracy, unsupported claims, stale-source rejection, authority selection.
3. `L3 Task`: whether the task-specific output is correct and useful.
4. `L4 Safety / Rights`: whether the run incorrectly closes safety, legal, cultural, rights, privacy, or professional gates.
5. `L5 Regression`: whether a new model / prompt / skill version performs worse than the approved baseline.

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

## P0-3 | Retrieval & Context QA

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

## P0-4 | AI Change & Regression Gate

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

## P0 execution sequence

`Necessity → Context Pack → Eval / Retrieval QA → Work → Human Gate → Regression Record → Promote or Rollback`

## Repository implementation

- `evals/golden/` — task-specific benchmark cases
- `evals/retrieval/` — canonical-source retrieval QA cases
- `evals/schemas/` — machine-readable case schemas
- `evals/scripts/` — deterministic validators
- `.github/workflows/ai-governance-evals.yml` — CI gate

## Relationship to existing OLEANDER governance

- Truth states remain defined by AI Design Reasoning Protocol v0.2.
- E0–E4 remain defined by Validation Protocol.
- Simulation uses Simulation Protocol v0.2.
- Human authority, rights, regulation, physical testing and professional sign-off are not replaced by eval scores.
