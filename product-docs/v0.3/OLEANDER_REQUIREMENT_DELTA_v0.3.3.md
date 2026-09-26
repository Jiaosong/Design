# OLEANDER Requirement Delta v0.3.3

[← v0.3.2 Delta](OLEANDER_REQUIREMENT_DELTA_v0.3.2.md) · [← Execution Fabric Architecture](OLEANDER_EXECUTION_FABRIC_ARCHITECTURE_v0.3.3.md)

**State:** `WORKING CONTENT DELTA / NON-AUTHORITY / SYSTEM ALIGNMENT OPEN`

v0.3.3 extends v0.3.2 with a provider-neutral execution architecture.

---

# New / Changed Requirements

| ID | Priority | Requirement | Primary node |
|---|---|---|---|
| HAR-F01 | P0 | OLEANDER runtime capabilities must be exposed through a provider-neutral Harness Adapter contract | N12D |
| HAR-F02 | P0 | Harness Session / Event Log must remain distinct from Project State / Current | N12D |
| HAR-F03 | P0 | Provider-native approval/sandbox cannot bypass or replace OLEANDER Action Guard | N12D / N10D |
| HAR-F04 | P0 | Provider execution events must normalize into an Execution Ledger that supports readback/audit without becoming project truth | N12D / N14 |
| HAR-F05 | P1 | OLEANDER should be able to switch compliant runtime providers without changing product semantics or authority | N12D |
| HAR-F06 | P1 | Workflow platforms such as Dify may execute bounded subflows but cannot own Project State, Design Decision or Artifact Current | N12D |

---

# System Alignment Additions

| Alignment ID | Required proof | Status |
|---|---|---|
| SA-14 | define Runtime Contract against current COS/native execution before adding external harness | `CANDIDATE_CONTRACT_PASS / NO_PROMOTION` |
| SA-15 | provider session/event stream survives reload/replay while Project State remains separately owner-native | `OPEN_SYSTEM_ALIGNMENT` |
| SA-16 | DeepSeek Harness narrow adapter spike passes session/tool/approval/sandbox/trace conformance | `OPEN_SYSTEM_ALIGNMENT` |
| SA-17 | provider-native approval cannot execute an action denied by OLEANDER Action Guard | `CONTRACT_ORDERING_PASS / REAL_PROVIDER_PATH_OPEN` |
| SA-18 | provider switch preserves design decision / artifact / project identities | `SYNTHETIC_IDENTITY_PASS / REAL_SWITCH_OPEN` |
| SA-19 | one bounded Dify workflow can round-trip typed input/result without acquiring project authority | `OPTIONAL_AFTER_CORE_PARITY` |

Candidate evidence for SA-14 / SA-17 / SA-18: [Runtime Provider Benchmark — 2026-09-26](../../00-governance/runtime/runtime_provider_spikes/results/OLEANDER_RUNTIME_PROVIDER_BENCHMARK_20260926.md).
This evidence does not close SA-15 / SA-16 / SA-18 real-switch semantics and does not promote a provider.

---

# Closure rule

No provider is considered adopted because its demo runs.

Adoption requires:
1. Runtime Contract implemented；
2. conformance suite passes；
3. authority/state separation remains intact；
4. degraded behaviour is truthful；
5. readback proves actual execution；
6. provider removal does not make Project State unrecoverable。
