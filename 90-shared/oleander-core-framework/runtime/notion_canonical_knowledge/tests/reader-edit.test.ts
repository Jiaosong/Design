import { describe, expect, it } from "vitest";
import { validateReaderBeginContentReviewInput, validateReaderContentPatchInput } from "../src/reader-edit";

describe("private Reader content patch contract", () => {
  it("accepts one bounded exact replacement", () => {
    expect(validateReaderContentPatchInput(" page-12345678 ", "before", "after")).toEqual({
      ok: true,
      input: { pageId: "page-12345678", oldStr: "before", newStr: "after" },
    });
  });

  it("rejects missing, oversized and no-op patches", () => {
    expect(validateReaderContentPatchInput("", "before", "after")).toMatchObject({ ok: false, status: 400 });
    expect(validateReaderContentPatchInput("page-12345678", "same", "same")).toEqual({
      ok: false,
      status: 400,
      error: "content_patch_noop",
    });
    expect(validateReaderContentPatchInput("page-12345678", "a".repeat(20_001), "after")).toEqual({
      ok: false,
      status: 413,
      error: "content_patch_too_large",
    });
  });

  it("rejects page identifiers beyond the service-boundary limit", () => {
    expect(validateReaderContentPatchInput("p".repeat(129), "before", "after")).toMatchObject({ ok: false, status: 400 });
  });

  it("requires exact identity and revision before entering content REVIEW", () => {
    expect(validateReaderBeginContentReviewInput(" page-12345678 ", " KN-METHOD-TEST-001 ", " 2026-09-13T10:00:00.000Z ")).toEqual({
      ok: true,
      input: {
        pageId: "page-12345678",
        expectedCanonicalId: "KN-METHOD-TEST-001",
        expectedNotionLastEditedTime: "2026-09-13T10:00:00.000Z",
      },
    });
    expect(validateReaderBeginContentReviewInput("page-12345678", "", "2026-09-13T10:00:00.000Z")).toMatchObject({ ok: false, status: 400 });
    expect(validateReaderBeginContentReviewInput("page-12345678", "KN-METHOD-TEST-001", "")).toMatchObject({ ok: false, status: 400 });
  });
});
