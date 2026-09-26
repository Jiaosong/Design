# OLEANDER Runtime Provider Contract v0.1

**Status:** `CANDIDATE_NON_AUTHORITY`

This contract is the executable seam introduced by the v0.3.3 Execution Fabric architecture. It is deliberately below OLEANDER Project/Design semantics.

```text
OLEANDER Project / Design / Authority Semantics
                ↓
        Runtime Provider Contract
                ↓
 native/COS | DeepSeek Harness | Microsoft Agent Framework | PydanticAI+Temporal
                ↓
       tools / models / sandbox / jobs
```

## Hard boundary

```text
Provider Session ≠ Project State
Provider Replay ≠ Project Truth
Provider Approval ≠ Human Design Decision
Provider Permission ≠ OLEANDER Action Guard
Provider Event Log ≠ Current
Provider Completion ≠ Artifact / Design Completion
```

OLEANDER Action Guard is evaluated first. A provider-native approval may further restrict execution but may never widen a denied action.

## Execution Ledger

Provider events are normalized into an append-only **Execution Ledger projection**. The projection is runtime evidence only. Authority-bearing keys such as `project_current`, `design_decision`, `design_keep`, `professional_pass`, and `promotion` are stripped/rejected from normalized provider events.

## Candidate providers

- `native_cos` — current local/COS reference path.
- `deepseek_harness` — CLI/profile composition smoke plus contract shim.
- `microsoft_agent_framework` — AgentSession/framework surface smoke plus contract shim.
- `pydantic_ai_temporal` — deterministic TestModel + Temporal durability/test-environment smoke plus contract shim.

The same conformance fixtures run against every provider. Provider-specific native smoke is reported separately from contract conformance so an import or CLI launch cannot masquerade as full integration.

## Promotion boundary

Passing this candidate benchmark does **not** make a provider Current. Adoption requires an explicit system-alignment review, actual native execution integration, readback, provider-removal test, and the existing OLEANDER authority/promotion path.
