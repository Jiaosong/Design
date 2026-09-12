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
  cause_type: "webhook" | "reconcile" | "manual" | "incremental";
  event_type?: string;
  event_timestamp?: string;
  // Ephemeral execution hint. Durable scheduler rows intentionally do not
  // persist it; the D1 drain derives force=true only for explicit reconciles.
  force?: boolean;
}

export type SyncTaskStatus = "PENDING" | "PROCESSING" | "RETRY" | "PROCESSED" | "BLOCKED";

export interface SyncTaskRow {
  cause_id: string;
  run_id: string | null;
  page_id: string;
  cause_type: IngestMessage["cause_type"];
  event_type: string | null;
  status: SyncTaskStatus;
  attempts: number;
  error: string | null;
  next_attempt_at: string | null;
  created_at: string | null;
  updated_at: string;
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
  canonicalParentIds: string[];
  canonicalChildrenIds: string[];
  methodFamilies: string[];
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

export interface KnowledgeReaderSnapshot {
  title: string;
  subtitle?: string;
  generatedAt: string;
  metrics: Array<{ key: string; label: string; value: string | number; note?: string }>;
  migration: { done: number; total: number; next?: string };
  roleDistribution: Array<{ name: string; value: number }>;
  evidenceDistribution: Array<{ name: string; value: number }>;
  levelDistribution: Array<{ name: string; value: number }>;
  items: Array<{
    id: string;
    title: string;
    summary?: string;
    canonicalId?: string;
    role?: string;
    level?: string;
    retrievalSpace?: string;
    searchEligibility?: string;
    trustState?: string;
    governanceState?: string;
    relationState?: string;
    indexState?: string;
    authorityReason?: string;
    notionLastEditedTime?: string;
    indexedAt?: string;
    group: "current" | "methods" | "evidence" | "practice" | "history";
    url?: string;
    tags?: string[];
    evidence?: string[];
    limitations?: string[];
  }>;
  defaultSelectedId?: string;
  source: {
    authority: string;
    derivative: string;
    activeDocuments: number;
    indexedDocuments: number;
    explicitCurrent: number;
    support: number;
    provenance: number;
  };
}

export interface KnowledgeReaderDetailSection {
  key: string;
  headingPath: string[];
  text: string;
  chunkOrdinals: number[];
  tokenEstimate: number;
}

export interface KnowledgeReaderDetailRelation {
  direction: "outgoing" | "incoming";
  relationType: string;
  pageId: string;
  canonicalId?: string;
  title?: string;
  role?: string;
  level?: string;
  retrievalSpace?: string;
  governanceState?: string;
  relationState?: string;
}

export interface KnowledgeReaderFrameworkObjectRef {
  registry: "notes" | "domains";
  pageId: string;
  title?: string;
  canonicalId?: string;
  role?: string;
  level?: string;
  retrievalSpace?: string;
  governanceState?: string;
  relationState?: string;
  lastEditedTime?: string;
  inTrash?: boolean;
  domainLevel?: string;
  frameworkPath?: string;
}

export interface KnowledgeReaderFrameworkReadback {
  source: {
    authority: "Notion";
    state: "HYDRATED" | "UNAVAILABLE";
    derivativeRevision?: string;
    liveRevision?: string;
    revisionMatches?: boolean;
    error?: string;
  };
  domains: {
    primaryDeclaredIds: string[];
    relatedDeclaredIds: string[];
    primary: KnowledgeReaderFrameworkObjectRef[];
    related: KnowledgeReaderFrameworkObjectRef[];
    primaryRelationComplete: boolean;
    relatedRelationComplete: boolean;
    unresolvedPageIds: string[];
  };
  canonicalHierarchy: {
    declaredParentIds: string[];
    declaredChildrenIds: string[];
    parent: KnowledgeReaderFrameworkObjectRef | null;
    parents: KnowledgeReaderFrameworkObjectRef[];
    parentAmbiguous: boolean;
    children: KnowledgeReaderFrameworkObjectRef[];
    parentRelationComplete: boolean;
    childrenRelationComplete: boolean;
    unresolvedPageIds: string[];
  };
  routingInputs: {
    knowledgeRole?: string;
    methodFamily: string[];
    requiredNativeOutput: {
      state: "EXECUTION_CONTEXT_REQUIRED";
      source: "CURRENT_EXECUTION_CONTEXT_NOT_BOUND";
    };
    unresolvedInputs: string[];
  };
  executionOwner: {
    state: "NOT_HYDRATED";
    localProjectionUsed: false;
    reason: "AUTHORITATIVE_RESOLVER_READBACK_NOT_BOUND";
    blockingInputs: string[];
  };
}

export interface KnowledgeReaderDetail {
  version: "oleander-knowledge-reader-detail/v1";
  generatedAt: string;
  id: string;
  title: string;
  canonicalId?: string;
  url?: string;
  role?: string;
  level?: string;
  retrievalSpace?: string;
  searchEligibility?: string;
  trustState?: string;
  governanceState?: string;
  relationState?: string;
  indexState?: string;
  authorityReason?: string;
  notionLastEditedTime?: string;
  indexedAt?: string;
  primaryDomainIds: string[];
  relatedDomainIds: string[];
  frameworkReadback?: KnowledgeReaderFrameworkReadback;
  review: {
    contentComplete: boolean;
    markdownTruncated: boolean;
    chunkCount: number;
    tokenEstimate: number;
    unknownBlockIds: string[];
    relationReadback: {
      declared: {
        primaryDomain: number;
        relatedDomain: number;
        source: number;
        method: number;
        replacement: number;
        replacedDocument: number;
      };
      indexedOutgoing: {
        source: number;
        method: number;
        replacement: number;
        replacedDocument: number;
      };
      unresolvedTargets: Array<{ relationType: string; pageId: string }>;
      missingManifestEdges: Array<{ relationType: string; pageId: string }>;
    };
  };
  sections: KnowledgeReaderDetailSection[];
  relations: KnowledgeReaderDetailRelation[];
}
