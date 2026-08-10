# OLEANDER AI Eval Harness v0.1

This directory evaluates OLEANDER AI workflows as systems, not as generic language models.

## Scope

- `golden/skills.jsonl`: task-specific cases for reusable OLEANDER skills.
- `retrieval/golden_queries.jsonl`: canonical-source and context-authority cases.
- `scripts/validate_evals.py`: deterministic schema and governance checks.
- CI: `.github/workflows/ai-governance-evals.yml`.

## Evaluation philosophy

1. Evaluate real OLEANDER tasks, not abstract benchmarks.
2. A blocker failure overrides a high average score.
3. Evidence authority, truth state, version and scope matter as much as fluency.
4. A polished output that invents evidence is a failure.
5. Model, prompt, skill, retrieval, parser or tool changes require regression comparison.
6. Human review remains mandatory for safety, regulation, rights, cultural authority and final design decisions.

## Golden case result contract

A run record should include:

```json
{
  "case_id": "SK-RES-001",
  "system_version": "...",
  "model_tool_version": "...",
  "input_version": "...",
  "result": "PASS|PASS-WITH-WARNINGS|FAIL|HOLD-HUMAN-REVIEW",
  "checks": [],
  "blockers": [],
  "human_review": "...",
  "evidence_links": []
}
```

## Promotion rule

Candidate AI configuration may become default only when:

- all blocker cases pass;
- no new unsupported-claim or source-authority regression appears;
- truth-state separation is retained;
- all required fields remain present;
- human reviewer approves any changed behavior affecting design authority.

## Current limitation

The first implementation validates the governance corpus and case completeness in CI. Model execution remains explicit because OLEANDER may use multiple AI providers/tools; every actual model run must store the model/tool/version and a result record before promotion.
