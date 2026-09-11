export type RetrievalSpace = "CURRENT" | "SUPPORT" | "PROVENANCE";
export type ExplicitRetrievalSpace = RetrievalSpace | "EXCLUDED" | null;
export type SearchEligibility = "DEFAULT" | "SCOPED" | "HISTORY_ONLY" | "BLOCKED" | null;

export interface Env {
  MANIFEST: D1Database;
  AI: Ai;
  KNOWLEDGE_INDEX: VectorizeIndex;
  INGEST_QUEUE: Queue<IngestMessage>;
  INGEST_DLQ: Queue<IngestMessage>;
  NOTION_TOKEN: string;
  NOTION_WEBHOOK_VERIFICATION_TOKEN: string;
  OLEANDER_API_TOKEN: string;
  NOTION_VERSION: string;
  NOTION_ROOT_PAGE_ID: string;
  NOTION_NOTES_DATA_SOURCE_ID: string;
  EMBEDDING_MODEL: string;
  EMBEDDING_DIMENSIONS: string;
  API_DEFAULT_TOP_K: string;
}

export interface IngestMessage {
  kind: "notion-page-sync";
  page_id: string;
  cause_id: string;
  cause_type: "webhook" | "reconcile" | "manual";
  event_type?: string;
  event_timestamp?: string;
}

export interface NotionWebhookEvent {
  id?: string;
  type?: string;
  timestamp?: string;
  entity?: { id?: string; type?: string };
  data?: Record<string, unknown>;
  verification_token?: string;
}

export interface NotionPage {
  object: "page";
  id: string;
  url?: string;
  in_trash?: boolean;
  last_edited_time?: string;
  parent?: Record<string, unknown>;
  properties?: Record<string, NotionProperty>;
}

export type NotionProperty = Record<string, unknown> & { type?: string };

export interface PageMarkdown {
  object: "page_markdown";
  id: string;
  markdown: string;
  truncated: boolean;
  unknown_block_ids: string[];
}

export interface NormalizedPage {
  pageId: string;
  canonicalId: string | null;
  title: string;
  url: string | null;
  lastEditedTime: string | null;
  inTrash: boolean;
  parentDataSourceId: string | null;
  retrievalSpace: ExplicitRetrievalSpace;
  searchEligibility: SearchEligibility;
  trustState: string | null;
  governanceState: string | null;
  relationState: string | null;
  contentLevel: string | null;
  knowledgeRole: string | null;
  primaryDomainIds: string[];
  relatedDomainIds: string[];
  sourceRelationIds: string[];
  methodRelationIds: string[];
  replacementIds: string[];
  replacedDocumentIds: string[];
}

export interface AuthorityDecision {
  index: boolean;
  effectiveSpace: RetrievalSpace | null;
  reason: string;
  conflict: boolean;
}

export interface KnowledgeChunk {
  ordinal: number;
  headingPath: string[];
  text: string;
  tokenEstimate: number;
  textHash?: string;
  vectorId?: string;
}

export interface ManifestChunkRow {
  vector_id: string;
  page_id: string;
  ordinal: number;
  namespace: RetrievalSpace;
  heading_path: string;
  token_estimate: number;
  text_hash: string;
  content_hash: string;
  chunk_text: string;
  metadata_json: string;
  active: number;
}

export interface SearchRequest {
  query: string;
  top_k?: number;
  include_support?: boolean;
  include_provenance?: boolean;
  include_scoped?: boolean;
  canonical_id?: string;
}

export interface KnowledgeHit {
  vector_id: string;
  score: number;
  namespace: RetrievalSpace;
  page_id: string;
  canonical_id: string | null;
  title: string;
  heading_path: string;
  text: string;
  content_hash: string;
  knowledge_role: string | null;
  content_level: string | null;
  trust_state: string | null;
}
