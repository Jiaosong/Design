import { describe, expect, it } from "vitest";

const namespaceFor = (space: string, historyIntent = false): string | null => {
  if (space === "CURRENT") return "prod-current";
  if (space === "SUPPORT") return "prod-support";
  if (space === "PROVENANCE" && historyIntent) return "prod-provenance";
  return null;
};

describe("OLEANDER retrieval namespace boundaries", () => {
  it("keeps current and provenance in separate pools", () => {
    expect(namespaceFor("CURRENT")).toBe("prod-current");
    expect(namespaceFor("PROVENANCE")).toBeNull();
    expect(namespaceFor("PROVENANCE", true)).toBe("prod-provenance");
  });

  it("does not make excluded content queryable", () => {
    expect(namespaceFor("EXCLUDED")).toBeNull();
    expect(namespaceFor("UNKNOWN")).toBeNull();
  });
});
