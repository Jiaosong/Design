import { describe, expect, it } from "vitest";
import { deriveReaderKnowledgeSyncState } from "../src/live-status";

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
});
