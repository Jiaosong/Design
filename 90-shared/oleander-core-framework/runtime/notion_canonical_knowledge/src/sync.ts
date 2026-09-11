import { resolveAuthority } from "./authority";
import { chunkMarkdown, normalizeMarkdownForHash } from "./chunker";
import { embedTexts } from "./embedding";
import { sha256Hex, stableStringify } from "./hash";
import { deactivatePage, getActiveVectorIds, saveDocumentAndChunks } from "./manifest";
import { fetchCompleteMarkdown, fetchPage, NotionHttpError } from "./notion";
import { belongsToDataSource, normalizePage } from "./normalize";
import type { Env, IngestMessage, ManifestChunkRow, RetrievalSpace } from "./types";

function embeddingText(input: {
  title: string;
  canonicalId: string | null;
  knowledgeRole: string | null;
  contentLevel: string | null;
  headingPath: string[];
  text: string;
}): string {
  return [
    input.title ? `Title: ${input.title}` : "",
    input.canonicalId ? `Canonical ID: ${input.canonicalId}` : "",
    input.knowledgeRole ? `Role: ${input.knowledgeRole}` : "",
    input.contentLevel ? `Level: ${input.contentLevel}` : "",
    input.headingPath.length ? `Path: ${input.headingPath.join(" > ")}` : "",
    input.text,
  ]
    .filter(Boolean)
    .join("\n");
}

async function deleteVectors(env: Env, ids: string[]): Promise<void> {
  for (let i = 0; i < ids.length; i += 1000) {
    const batch = ids.slice(i, i + 1000);
    if (batch.length) await env.KNOWLEDGE_INDEX.deleteByIds(batch);
  }
}

async function makeVectorId(pageId: string, namespace: RetrievalSpace, ordinal: number, textHash: string): Promise<string> {
  // SHA-256 hex is exactly 64 chars, within Vectorize's vector-id limit.
  return sha256Hex(`${pageId}:${namespace}:${ordinal}:${textHash}`);
}

export async function syncPage(env: Env, message: IngestMessage): Promise<{ status: string; page_id: string; chunks?: number }> {
  let rawPage;
  try {
    rawPage = await fetchPage(env, message.page_id);
  } catch (error) {
    if (error instanceof NotionHttpError && error.status === 404) {
      const ids = await deactivatePage(env.MANIFEST, message.page_id, "NOTION_NOT_FOUND_OR_NO_LONGER_SHARED");
      await deleteVectors(env, ids);
      return { status: "DEACTIVATED_NOT_FOUND", page_id: message.page_id };
    }
    throw error;
  }

  if (!belongsToDataSource(rawPage, env.NOTION_NOTES_DATA_SOURCE_ID)) {
    const ids = await deactivatePage(env.MANIFEST, message.page_id, "OUTSIDE_NOTES_DATA_SOURCE");
    await deleteVectors(env, ids);
    return { status: "DEACTIVATED_OUTSIDE_NOTES", page_id: message.page_id };
  }

  const page = normalizePage(rawPage);
  const authority = resolveAuthority(page);
  if (!authority.index || !authority.effectiveSpace) {
    const ids = await deactivatePage(env.MANIFEST, page.pageId, authority.reason);
    await deleteVectors(env, ids);
    return { status: "EXCLUDED", page_id: page.pageId };
  }

  const markdownResult = await fetchCompleteMarkdown(env, page.pageId);
  const markdown = normalizeMarkdownForHash(markdownResult.markdown);
  const structureForHash = markdown
    .split(/\r?\n/)
    .filter((line) => /^#{1,6}\s+/.test(line))
    .join("\n");
  const contentHash = await sha256Hex(
    stableStringify({
      page_id: page.pageId,
      canonical_id: page.canonicalId,
      authority: authority.effectiveSpace,
      metadata: {
        search_eligibility: page.searchEligibility,
        trust_state: page.trustState,
        governance_state: page.governanceState,
        relation_state: page.relationState,
        content_level: page.contentLevel,
        knowledge_role: page.knowledgeRole,
        primary_domains: page.primaryDomainIds,
        related_domains: page.relatedDomainIds,
        source_relations: page.sourceRelationIds,
        method_relations: page.methodRelationIds,
        replacements: page.replacementIds,
        replaced_documents: page.replacedDocumentIds,
      },
      markdown,
    }),
  );
  const structureHash = await sha256Hex(structureForHash);

  const chunks = chunkMarkdown(markdown);
  const texts = chunks.map((chunk) =>
    embeddingText({
      title: page.title,
      canonicalId: page.canonicalId,
      knowledgeRole: page.knowledgeRole,
      contentLevel: page.contentLevel,
      headingPath: chunk.headingPath,
      text: chunk.text,
    }),
  );
  const vectors = await embedTexts(env, texts);
  const namespace = authority.effectiveSpace;
  const manifestRows: ManifestChunkRow[] = [];
  const vectorRecords: VectorizeVector[] = [];

  for (let i = 0; i < chunks.length; i += 1) {
    const chunk = chunks[i];
    const values = vectors[i];
    if (!chunk || !values) throw new Error(`Chunk/vector mismatch at ${i}`);
    const textHash = await sha256Hex(chunk.text);
    const vectorId = await makeVectorId(page.pageId, namespace, chunk.ordinal, textHash);
    const metadata = {
      page_id: page.pageId,
      canonical_id: page.canonicalId ?? "",
      title: page.title.slice(0, 300),
      heading: chunk.headingPath.join(" > ").slice(0, 500),
      knowledge_role: page.knowledgeRole ?? "",
      content_level: page.contentLevel ?? "",
      trust_state: page.trustState ?? "",
      content_hash: contentHash,
    };
    vectorRecords.push({ id: vectorId, namespace, values, metadata });
    manifestRows.push({
      vector_id: vectorId,
      page_id: page.pageId,
      ordinal: chunk.ordinal,
      namespace,
      heading_path: chunk.headingPath.join(" > "),
      token_estimate: chunk.tokenEstimate,
      text_hash: textHash,
      content_hash: contentHash,
      chunk_text: chunk.text,
      metadata_json: JSON.stringify(metadata),
      active: 1,
    });
  }

  const oldIds = await getActiveVectorIds(env.MANIFEST, page.pageId);
  for (let i = 0; i < vectorRecords.length; i += 1000) {
    await env.KNOWLEDGE_INDEX.upsert(vectorRecords.slice(i, i + 1000));
  }

  await saveDocumentAndChunks(env.MANIFEST, {
    page,
    authority,
    contentHash,
    structureHash,
    truncated: markdownResult.truncated,
    unknownBlockIds: markdownResult.unknown_block_ids,
    chunks: manifestRows,
  });

  const newIds = new Set(manifestRows.map((row) => row.vector_id));
  const staleIds = oldIds.filter((id) => !newIds.has(id));
  await deleteVectors(env, staleIds);
  return { status: authority.conflict ? "INDEXED_FAIL_CLOSED" : "INDEXED", page_id: page.pageId, chunks: chunks.length };
}
