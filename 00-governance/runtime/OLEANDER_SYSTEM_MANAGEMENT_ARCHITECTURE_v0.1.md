# OLEANDER System Management Refactor v0.1

**Status:** CANDIDATE / NON-AUTHORITY / IMPLEMENTED FOR SYSTEM-ENTRY VALIDATION

This refactor does not create another OLEANDER architecture. It introduces one machine-readable management entrypoint over the existing Current architecture:

    1 Current OLEANDER System Architecture
            ↓
    1 Complex Project Master Runtime
            ↓
    11 Runtime Layers R-A ... R-K
            ↓
    existing owner-native contracts / registries / processes

The refactor exists to stop Chat, CoS, plugins, local software inventories and provider sessions from gradually becoming accidental parallel state systems.

## 1 | Management domains

The system management view covers Authority / Identity, Project State, Knowledge / Evidence, Design Intelligence, Design Development, Professional Process, Cross-disciplinary Interfaces, Capability / Skill / Tool Runtime, Native Artifacts, Readback / Review, Persistence / Promotion / Sync, Knowledge Return / Evolution, and Environment / Execution Surfaces.

These are management views over the existing architecture. They are not new Runtime Layers.

## 2 | Canonical system entry

The machine-readable entry is OLEANDER_SYSTEM_MANIFEST_v0.1.json.

The runtime entry is oleander_system_gateway.py with five operations:

- manifest;
- context;
- environment;
- preflight;
- self-test.

The gateway returns an oleander.system-context-envelope.v0.1 projection. The projection is disposable execution context and has no authority to change Current, Project State, Knowledge, Design Decision, Artifact Current or Promotion.

## 3 | CoS role after refactor

Chat On Steroids becomes an explicit Execution Harness:

    Human / Chat
            ↓
    OLEANDER System Gateway
            ↓
    Current owner-native Project / Knowledge / Authority context
            ↓
    existing Resolver / Action Guard
            ↓
    CoS Harness
      session / workers / tools / plugins / browser / desktop
            ↓
    actual execution
            ↓
    readback
            ↓
    owner-native transition if justified

Hard separation:

    CoS Session ≠ Project State
    CoS Compact & Resume ≠ Project Resume authority
    CoS Tool Call ≠ Artifact completion
    CoS Plugin Registry ≠ OLEANDER capability authority
    CoS Goal Loop ≠ Design completion authority

OLEANDER_COS_HARNESS_ADAPTER_v0.1.json owns this mapping.

## 4 | Knowledge management

The refactor keeps the existing knowledge architecture: L0 ... L7, independent Knowledge Role, typed relations, Content Remediation, KI0 ... KI5 and task/claim OE0 ... OE3.

No runtime framework memory, vector database, chat transcript, local plugin state or provider event log becomes canonical knowledge.

The System Context Envelope carries only canonical refs and task-scoped mount records needed by the current action.

## 5 | Project management

Project State remains owner-native. The gateway may carry project_id, project_state_ref, current_task_ref, decision_object_id, source_authority_ref and authority_fingerprint.

Missing values remain unresolved. The gateway must not manufacture them from folder names, chat history, CoS sessions or filenames.

## 6 | Interface management

System-wide typed interfaces remain owned by the existing Runtime Layer Interface, Skill Capability, Tool Adapter, Native Artifact, Execution Receipt, Runtime Provider and Cross-platform Sync contracts.

The System Context Envelope is only the top-level composition envelope used to pass those owner-native refs to execution.

## 7 | Environment and applications

The environment is resolved from two different truths:

    Canonical static surface registry
            +
    live machine / account capability observation
            =
    Current execution view

A stale .mcp-runtime snapshot is reported as stale runtime evidence. It cannot override the canonical static registry and it cannot change project authority.

All apps and plugins are modeled as execution surfaces. Selection is by required capability, native output, permission, side-effect and readback, never merely by installed vendor name.

## 8 | Runtime-provider boundary

DeepSeek Harness, Microsoft Agent Framework, PydanticAI + Temporal and native CoS remain provider candidates below the OLEANDER product semantics.

The provider layer may own runtime session, tool execution, approval, sandbox, durable execution, worker orchestration and execution trace.

It may not own Project State, Knowledge Authority, Design Decision, Artifact Current, Design KEEP, Professional PASS or Promotion.

## 9 | Migration strategy

Phase 1 implemented by this refactor:

1. create System Manifest;
2. create System Context Envelope;
3. create CoS Harness Adapter contract;
4. create executable System Gateway;
5. reduce CoS prompt binding to the Gateway and immutable authority boundaries;
6. validate existing refs and fail closed.

Later phases may move additional provider-specific code below the Runtime Provider Contract, but only after the same conformance tests pass and no owner-native state migrates into provider sessions.

## 10 | Does not prove

This candidate refactor does not prove all Current OLEANDER runtime code has migrated to the gateway, any provider is promoted, external project/user validation, professional correctness, Design KEEP or Promotion.

It establishes the management seam required to perform those migrations without creating another system.
