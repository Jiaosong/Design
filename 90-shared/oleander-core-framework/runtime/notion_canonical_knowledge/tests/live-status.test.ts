import { describe, expect, it } from "vitest";
import { deriveReaderKnowledgeSyncState } from "../src/live-status";
import { bindKnowledgeReaderExecutionContext } from "../src/reader";
import type { ExecutionLiveStatusProjection } from "../src/manifest";
import type { KnowledgeReaderDetail, KnowledgeReaderFrameworkReadback } from "../src/types";

function frameworkFixture(): KnowledgeReaderFrameworkReadback {
  return {
    source: {
      authority: "Notion",
      state: "HYDRATED",
      derivativeRevision: "2026-09-13T00:00:00.000Z",
      readbackStartedRevision: "2026-09-13T00:00:00.000Z",
      liveRevision: "2026-09-13T00:00:00.000Z",
      readbackRevisionCoherent: true,
      revisionMatches: true,
    },
    domains: {
      primaryDeclaredIds: [],
      relatedDeclaredIds: [],
      primary: [],
      related: [],
      primaryRelationComplete: true,
      relatedRelationComplete: true,
      registryInventoryComplete: true,
      unresolvedPageIds: [],
    },
    canonicalHierarchy: {
      declaredParentIds: [],
      declaredChildrenIds: [],
      parent: null,
      parents: [],
      parentAmbiguous: false,
      children: [],
      parentRelationComplete: true,
      childrenRelationComplete: true,
      unresolvedPageIds: [],
    },
    routingInputs: {
      knowledgeRole: "METHOD",
      methodFamily: ["分析建模"],
      methodFamilyComplete: true,
      primaryDomainRoutingReady: false,
      primaryDomainRoutingIssues: ["primary_domain_cardinality_0"],
      requiredNativeOutput: {
        state: "EXECUTION_CONTEXT_REQUIRED",
        source: "CURRENT_EXECUTION_CONTEXT_NOT_BOUND",
      },
      unresolvedInputs: [
        "required_native_output_or_execution_medium",
        "current_task_or_project_runtime_context",
        "primary_current_l2_domain",
      ],
    },
    executionOwner: {
      state: "NOT_HYDRATED",
      localProjectionUsed: false,
      reason: "AUTHORITATIVE_RESOLVER_READBACK_NOT_BOUND",
      blockingInputs: [
        "required_native_output_or_execution_medium",
        "current_task_or_project_runtime_context",
        "authoritative_execution_owner_resolver_runtime_readback",
        "primary_current_l2_domain",
      ],
    },
  };
}

function detailFixture(canonicalId = "KN-METHOD-TEST-001"): KnowledgeReaderDetail {
  return {
    version: "oleander-knowledge-reader-detail/v1",
    generatedAt: "2026-09-13T00:00:00.000Z",
    id: "page-1",
    title: "Method test",
    canonicalId,
    primaryDomainIds: [],
    relatedDomainIds: [],
    review: {
      contentComplete: true,
      markdownTruncated: false,
      chunkCount: 0,
      tokenEstimate: 0,
      unknownBlockIds: [],
      relationReadback: {
        declared: {
          primaryDomain: 0,
          relatedDomain: 0,
          source: 0,
          method: 0,
          replacement: 0,
          replacedDocument: 0,
        },
        indexedOutgoing: {
          source: 0,
          method: 0,
          replacement: 0,
          replacedDocument: 0,
        },
        unresolvedTargets: [],
        missingManifestEdges: [],
      },
    },
    sections: [],
    relations: [],
  };
}

function projectionFixture(overrides: Partial<ExecutionLiveStatusProjection> = {}): ExecutionLiveStatusProjection {
  return {
    version: "oleander-execution-live-status/v1",
    task_id: "TASK-1",
    executor_id: "EXEC-1",
    checkpoint_sequence: 4,
    status: "WORKING",
    receipt_id: "EXR-1",
    execution_context: {
      source: "OLEANDER_EXECUTION_RECEIPT_V1",
      receipt_id: "EXR-1",
      canonical_ids: ["KN-METHOD-TEST-001"],
      checkpoint_state: "RESUMABLE",
      authority_fingerprint: "AUTH-1",
      stale_reasons: [],
      required_native_output: {
        artifact_class: "parametric_model",
        native_format: "Grasshopper GH",
        editable_required: true,
        target_runtime: "Rhino + Grasshopper",
        derived_formats: ["3dm"],
      },
      owner_set: {
        minimum_sufficient_owner_set: true,
        primary_owner: "oleander-3d-pipeline",
        nodes: [{ owner_id: "oleander-3d-pipeline", role: "PRIMARY_OWNER" }],
        omitted_owner_reasoning: "One installed geometry owner is sufficient.",
      },
      flow_completion: {
        completion_gate: "HOLD",
        completion_claim_allowed: false,
        incomplete_required_phases: ["REAL_EXECUTION"],
      },
    },
    ...overrides,
  };
}

describe("Reader live status", () => {
  it("stays idle when no durable sync work is open", () => {
    expect(deriveReaderKnowledgeSyncState({ PROCESSED: 1184 })).toBe("IDLE");
  });

  it("reports active durable work as syncing", () => {
    expect(deriveReaderKnowledgeSyncState({ PROCESSING: 1, PENDING: 3 })).toBe("SYNCING");
  });

  it("reports retries as degraded instead of completed", () => {
    expect(deriveReaderKnowledgeSyncState({ RETRY: 1, PROCESSING: 1 })).toBe("DEGRADED");
  });

  it("fails closed when only blocked tasks remain", () => {
    expect(deriveReaderKnowledgeSyncState({ BLOCKED: 2, PROCESSED: 10 })).toBe("BLOCKED");
  });

  it("hydrates task-scoped owner/output only from an exact receipt canonical match", () => {
    const result = bindKnowledgeReaderExecutionContext(
      detailFixture(),
      frameworkFixture(),
      "TASK-1",
      [projectionFixture()],
    );
    expect(result.executionOwner.state).toBe("HYDRATED");
    if (result.executionOwner.state !== "HYDRATED") throw new Error("expected hydrated owner");
    expect(result.executionOwner.primaryOwner).toBe("oleander-3d-pipeline");
    expect(result.executionOwner.receiptId).toBe("EXR-1");
    expect(result.executionOwner.localProjectionUsed).toBe(false);
    expect(result.routingInputs.requiredNativeOutput.state).toBe("HYDRATED_FROM_EXECUTION_RECEIPT");
    expect(result.routingInputs.unresolvedInputs).toEqual(["primary_current_l2_domain"]);
  });

  it("keeps owner unresolved when task or canonical identity does not match", () => {
    const mismatch = bindKnowledgeReaderExecutionContext(
      detailFixture("KN-OTHER-001"),
      frameworkFixture(),
      "TASK-1",
      [projectionFixture()],
    );
    expect(mismatch.executionOwner).toMatchObject({
      state: "NOT_HYDRATED",
      localProjectionUsed: false,
      requestedTaskId: "TASK-1",
      contextMatchState: "NO_MATCH",
    });
    expect(mismatch.routingInputs.requiredNativeOutput.state).toBe("EXECUTION_CONTEXT_REQUIRED");
  });

  it("fails closed on stale receipt context", () => {
    const stale = projectionFixture({
      execution_context: {
        ...projectionFixture().execution_context!,
        stale_reasons: ["SOURCE_AUTHORITY_CHANGED"],
      },
    });
    const result = bindKnowledgeReaderExecutionContext(detailFixture(), frameworkFixture(), "TASK-1", [stale]);
    expect(result.executionOwner).toMatchObject({ state: "NOT_HYDRATED", contextMatchState: "STALE" });
  });

  it("treats malformed legacy D1 execution context as no authoritative match", () => {
    const malformed = {
      ...projectionFixture(),
      execution_context: {
        source: "OLEANDER_EXECUTION_RECEIPT_V1",
        receipt_id: "EXR-1",
        canonical_ids: "KN-METHOD-TEST-001",
      },
    } as unknown as ExecutionLiveStatusProjection;
    expect(() => bindKnowledgeReaderExecutionContext(detailFixture(), frameworkFixture(), "TASK-1", [malformed])).not.toThrow();
    const result = bindKnowledgeReaderExecutionContext(detailFixture(), frameworkFixture(), "TASK-1", [malformed]);
    expect(result.executionOwner).toMatchObject({ state: "NOT_HYDRATED", contextMatchState: "NO_MATCH" });
  });

  it("rejects malformed legacy owner-set semantics instead of trusting D1 shape", () => {
    const malformed = projectionFixture({
      execution_context: {
        ...projectionFixture().execution_context!,
        owner_set: {
          ...projectionFixture().execution_context!.owner_set,
          nodes: [
            { owner_id: "oleander-3d-pipeline", role: "PRIMARY_OWNER" },
            { owner_id: "oleander-research", role: "PRIMARY_OWNER" },
          ],
        },
      },
    });
    const result = bindKnowledgeReaderExecutionContext(detailFixture(), frameworkFixture(), "TASK-1", [malformed]);
    expect(result.executionOwner).toMatchObject({ state: "NOT_HYDRATED", contextMatchState: "NO_MATCH" });
  });

  it("selects the highest checkpoint sequence and fails closed on conflicting same-sequence contexts", () => {
    const old = projectionFixture({ checkpoint_sequence: 3, receipt_id: "EXR-OLD", execution_context: {
      ...projectionFixture().execution_context!,
      receipt_id: "EXR-OLD",
      owner_set: {
        ...projectionFixture().execution_context!.owner_set,
        primary_owner: "oleander-research",
        nodes: [{ owner_id: "oleander-research", role: "PRIMARY_OWNER" }],
      },
    } });
    const current = projectionFixture({ checkpoint_sequence: 4 });
    const selected = bindKnowledgeReaderExecutionContext(detailFixture(), frameworkFixture(), "TASK-1", [old, current]);
    expect(selected.executionOwner.state === "HYDRATED" && selected.executionOwner.primaryOwner).toBe("oleander-3d-pipeline");

    const conflict = projectionFixture({
      executor_id: "EXEC-2",
      execution_context: {
        ...projectionFixture().execution_context!,
        receipt_id: "EXR-2",
        owner_set: {
          ...projectionFixture().execution_context!.owner_set,
          primary_owner: "oleander-research",
          nodes: [{ owner_id: "oleander-research", role: "PRIMARY_OWNER" }],
        },
      },
      receipt_id: "EXR-2",
    });
    const ambiguous = bindKnowledgeReaderExecutionContext(detailFixture(), frameworkFixture(), "TASK-1", [current, conflict]);
    expect(ambiguous.executionOwner).toMatchObject({ state: "NOT_HYDRATED", contextMatchState: "AMBIGUOUS" });
  });

  it("does not fall back to an older owner context when the task has newer direct telemetry", () => {
    const receiptProjection = projectionFixture({ checkpoint_sequence: 4 });
    const { receipt_id: _receiptId, execution_context: _executionContext, ...newerDirect } = projectionFixture({
      checkpoint_sequence: 5,
      executor_id: "EXEC-2",
    });
    const result = bindKnowledgeReaderExecutionContext(
      detailFixture(),
      frameworkFixture(),
      "TASK-1",
      [receiptProjection, newerDirect],
    );
    expect(result.executionOwner).toMatchObject({ state: "NOT_HYDRATED", contextMatchState: "NO_MATCH" });
    expect(result.routingInputs.requiredNativeOutput.state).toBe("EXECUTION_CONTEXT_REQUIRED");
  });

  it("fails closed when same-sequence projections disagree on execution status", () => {
    const working = projectionFixture({ executor_id: "EXEC-1", status: "WORKING" });
    const hold = projectionFixture({ executor_id: "EXEC-2", status: "HOLD" });
    const result = bindKnowledgeReaderExecutionContext(detailFixture(), frameworkFixture(), "TASK-1", [working, hold]);
    expect(result.executionOwner).toMatchObject({ state: "NOT_HYDRATED", contextMatchState: "AMBIGUOUS" });
  });
});
