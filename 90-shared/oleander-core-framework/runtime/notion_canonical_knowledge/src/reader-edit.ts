export type ReaderContentPatchInput = {
  pageId: string;
  oldStr: string;
  newStr: string;
};

export type ReaderContentPatchValidation =
  | { ok: true; input: ReaderContentPatchInput }
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
