export type ReaderContentPatchInput = {
  pageId: string;
  oldStr: string;
  newStr: string;
};

export type ReaderContentPatchValidation =
  | { ok: true; input: ReaderContentPatchInput }
  | { ok: false; status: 400 | 413; error: string };

export type ReaderBeginContentReviewInput = {
  pageId: string;
  expectedCanonicalId: string;
  expectedNotionLastEditedTime: string;
};

export type ReaderBeginContentReviewValidation =
  | { ok: true; input: ReaderBeginContentReviewInput }
  | { ok: false; status: 400; error: string };

export type ReaderSupportContentPatchInput = ReaderContentPatchInput & {
  expectedCanonicalId: string;
  expectedNotionLastEditedTime: string;
};

export type ReaderSupportContentPatchValidation =
  | { ok: true; input: ReaderSupportContentPatchInput }
  | { ok: false; status: 400 | 413; error: string };

export function validateReaderContentPatchInput(
  pageIdInput: unknown,
  oldStrInput: unknown,
  newStrInput: unknown,
): ReaderContentPatchValidation {
  const pageId = typeof pageIdInput === "string" ? pageIdInput.trim() : "";
  const oldStr = typeof oldStrInput === "string" ? oldStrInput : "";
  const newStr = typeof newStrInput === "string" ? newStrInput : "";
  if (!pageId || pageId.length > 128 || !oldStr || !newStr) {
    return { ok: false, status: 400, error: "page_id_old_str_new_str_required" };
  }
  if (oldStr === newStr) return { ok: false, status: 400, error: "content_patch_noop" };
  if (oldStr.length > 20_000 || newStr.length > 20_000) {
    return { ok: false, status: 413, error: "content_patch_too_large" };
  }
  return { ok: true, input: { pageId, oldStr, newStr } };
}

export function validateReaderSupportContentPatchInput(
  pageIdInput: unknown,
  expectedCanonicalIdInput: unknown,
  expectedNotionLastEditedTimeInput: unknown,
  oldStrInput: unknown,
  newStrInput: unknown,
): ReaderSupportContentPatchValidation {
  const content = validateReaderContentPatchInput(pageIdInput, oldStrInput, newStrInput);
  if (!content.ok) return content;
  const expectedCanonicalId = typeof expectedCanonicalIdInput === "string" ? expectedCanonicalIdInput.trim() : "";
  const expectedNotionLastEditedTime = typeof expectedNotionLastEditedTimeInput === "string"
    ? expectedNotionLastEditedTimeInput.trim()
    : "";
  if (!expectedCanonicalId || expectedCanonicalId.length > 256 || !expectedNotionLastEditedTime || expectedNotionLastEditedTime.length > 128) {
    return { ok: false, status: 400, error: "support_content_patch_requires_expected_identity_and_revision" };
  }
  return {
    ok: true,
    input: {
      ...content.input,
      expectedCanonicalId,
      expectedNotionLastEditedTime,
    },
  };
}

export function validateReaderBeginContentReviewInput(
  pageIdInput: unknown,
  expectedCanonicalIdInput: unknown,
  expectedNotionLastEditedTimeInput: unknown,
): ReaderBeginContentReviewValidation {
  const pageId = typeof pageIdInput === "string" ? pageIdInput.trim() : "";
  const expectedCanonicalId = typeof expectedCanonicalIdInput === "string" ? expectedCanonicalIdInput.trim() : "";
  const expectedNotionLastEditedTime = typeof expectedNotionLastEditedTimeInput === "string"
    ? expectedNotionLastEditedTimeInput.trim()
    : "";
  if (!pageId || pageId.length > 128 || !expectedCanonicalId || expectedCanonicalId.length > 256 || !expectedNotionLastEditedTime || expectedNotionLastEditedTime.length > 128) {
    return { ok: false, status: 400, error: "content_review_requires_expected_identity_and_revision" };
  }
  return { ok: true, input: { pageId, expectedCanonicalId, expectedNotionLastEditedTime } };
}
