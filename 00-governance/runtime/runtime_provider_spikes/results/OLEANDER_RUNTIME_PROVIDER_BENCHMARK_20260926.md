# OLEANDER Runtime Provider Benchmark — 2026-09-26

**State:** `PASS_CANDIDATE_SPIKE`
**Authority ceiling:** `EXECUTION_CAPABILITY_AND_OBSERVABILITY_ONLY`
**Machine receipt:** [OLEANDER_RUNTIME_PROVIDER_BENCHMARK_20260926.json](OLEANDER_RUNTIME_PROVIDER_BENCHMARK_20260926.json)
**Contract:** [OLEANDER_RUNTIME_PROVIDER_CONTRACT_v0.1.json](../../OLEANDER_RUNTIME_PROVIDER_CONTRACT_v0.1.json)

This is the first executable provider-neutral runtime spike. It is **not** a provider-selection verdict and does not promote a new Current runtime.

This benchmark intentionally lives outside untime/receipts/ because it is candidate benchmark evidence, **not** an OLEANDER Execution Receipt.

## Environment

| Item | Observed |
|---|---|
| OS | Windows 11 |
| Node | `v24.18.0` |
| npm | `11.16.0` |
| Benchmark Python | Python 3.13 isolated venv |
| Shared conformance fixtures | 9 |

The optional Python provider packages were installed into a dedicated local benchmark venv and are not repository/runtime dependencies.

## Results

| Provider | Pinned / observed version | Shared contract | Native smoke | What actually ran |
|---|---|---|---|---|
| COS / Native | current repository | `9/9 PASS` | `PASS` | existing `oleander_chat_runtime_bridge.py --self-test`, including resolver/observability authority boundaries |
| DeepSeek Harness | `0.1.5-rc.3` | `9/9 PASS` | `PASS` | actual `dsh --version` + shipped `headless` profile composition via `--dump-default-config`; no model credential |
| Microsoft Agent Framework | `1.19.0` | `9/9 PASS` | `PASS` | actual package import, `AgentSession` instantiation, and `WorkflowBuilder` / `create_harness_agent` API seam verification; no model call |
| PydanticAI + Temporal | `2.51.0` + `1.33.0` | `9/9 PASS` | `PASS` | deterministic PydanticAI `TestModel` agent run + `TemporalDurability` capability + actual Temporal ephemeral test server start/shutdown |

Contract-shim identity stability check: `PASS` — the same synthetic project/decision/artifact identity fingerprints remained unchanged across all four contract shims. This is **not** yet an actual provider-switch/resume test.

## Shared contract cases

1. `CONTINUE` remains `CONTINUE` rather than being reinterpreted as `RESUME`.
2. `RESUME` opens runtime/session context without becoming Project State.
3. `RECOVER` preserves `PARTIAL` as partial rather than manufacturing completion.
4. the candidate Action Guard ordering projection blocks provider invocation when the envelope carries an OLEANDER denial, even when provider approval is `true`.
5. `READ_ONLY` does not authorize sensitive external disclosure.
6. material cost / blast-radius escalation is blocked without scoped authorization.
7. provider failure stays scoped and does not mutate Project State.
8. provider-supplied project-authority fields are stripped from the Execution Ledger while benign provider evidence is preserved.
9. provider-native approval may narrow an OLEANDER `ALLOW`, but cannot widen an OLEANDER denial.

## Interpretation

The result supports one architectural conclusion:

> A provider-neutral execution seam is viable without moving OLEANDER Project State, Current, Design Decision, Artifact authority or Promotion semantics into the provider.

It does **not** yet support a framework winner. Native-smoke depth is intentionally different:

- COS/native has the deepest pre-existing OLEANDER integration.
- DeepSeek Harness currently proves CLI/profile composition at the pinned preview version, not real OLEANDER tool/action execution.
- Microsoft Agent Framework currently proves session/workflow/harness API availability, not a real OLEANDER artifact mutation.
- PydanticAI+Temporal currently has the deepest isolated durability smoke because a deterministic agent run and Temporal ephemeral test environment were both executed, but it still has no OLEANDER real-artifact path.

The Action Guard checks in this round are **contract-level ordering tests**, not a replacement for the existing Current resolver/tool-authority path. SA-17 therefore remains open for a real provider-native approval integration.

## Not proven

- production readiness;
- framework superiority;
- real model quality;
- real CAD / Figma / Blender / browser artifact authoring parity;
- long-running provider durability under actual interruption;
- provider removal + later OLEANDER resume;
- real provider-native approval integrated with OLEANDER Action Guard;
- latency/cost/implementation-complexity comparison;
- external-user value;
- Design KEEP, professional PASS, or Promotion.

## Next evidence

The next benchmark round should use one identical bounded **real native artifact action** per provider adapter and measure:

```text
OLEANDER action
→ Action Guard
→ provider approval/sandbox
→ real tool/native mutation
→ actual delta
→ readback
→ interrupt
→ recover
→ provider removal/switch
→ OLEANDER resume
```

Only after that round should a Runtime Provider ADR compare adoption candidates.
