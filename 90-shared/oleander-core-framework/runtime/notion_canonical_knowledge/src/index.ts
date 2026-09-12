import {
  FIELDS,
  SCHEDULED_SYNC_BATCH_SIZE,
  SCHEDULED_SYNC_MAX_ATTEMPTS,
  SCHEDULED_SYNC_STALE_PROCESSING_MS,
} from "./config";
import { sha256Hex } from "./hash";
import {
  beginSyncRun,
  claimDueSyncTasks,
  completeSyncRun,
  deleteRuntimeState,
  failSyncRun,
  getRuntimeState,
  markWebhookFallbackFailure,
  markWebhookFallbackScheduled,
  markWebhookProcessed,
  markWebhookQueued,
  markWebhookQueueError,
  putRuntimeState,
  recordSyncMessageReceipt,
  recordWebhookReceived,
  refreshSyncRunStatus,
  requeueStaleSyncTasks,
  schedulerTaskCounts,
  stageSyncMessages,
  syncRunReadback,
} from "./manifest";
import {
  createAcademicPage,
  createDashboardWidgetView,
  createLinkedNotesView,
  createReaderPage,
  createViewOnDatabase,
  fetchCompleteMarkdown,
  fetchPage,
  listNotesPages,
  listDatabaseViews,
  replaceReaderIntroMarkdown,
  retrieveNotesDataSource,
  retrieveView,
  updatePageGovernanceFields,
  updatePageMarkdownContent,
  updateView,
} from "./notion";
import { normalizePage } from "./normalize";
import { decryptSetupSecret, encryptSetupSecret, isAuthorized, verifyNotionSignature } from "./security";
import { knowledgePackByCanonicalId, knowledgeSearch } from "./search";
import { buildKnowledgeReaderSnapshot } from "./reader";
import { syncPage } from "./sync";
import type { Env, IngestMessage, NotionWebhookEvent, SearchRequest } from "./types";

function json(data: unknown, status = 200): Response {
  return Response.json(data, { status, headers: { "Cache-Control": "no-store" } });
}

function errorJson(error: unknown, status = 500): Response {
  const message = error instanceof Error ? error.message : String(error);
  return json({ ok: false, error: message }, status);
}

async function handleWebhook(request: Request, env: Env): Promise<Response> {
  const rawBody = await request.text();
  let payload: NotionWebhookEvent;
  try {
    payload = JSON.parse(rawBody) as NotionWebhookEvent;
  } catch {
    return json({ ok: false, error: "invalid_json" }, 400);
  }

  // One-time subscription handshake. The token is intentionally never echoed back.
  if (payload.verification_token) {
    if (env.OLEANDER_API_TOKEN) {
      const encrypted = await encryptSetupSecret(payload.verification_token, env.OLEANDER_API_TOKEN);
      await putRuntimeState(env.MANIFEST, "pending_notion_webhook_verification_token", encrypted);
    }
    return json({
      ok: true,
      verification_received: true,
      instruction: "Retrieve the pending token through the bearer-protected /v1/webhook-setup-token endpoint, store it as NOTION_WEBHOOK_VERIFICATION_TOKEN, then DELETE that endpoint state.",
    });
  }

  const valid = await verifyNotionSignature(
    rawBody,
    env.NOTION_WEBHOOK_VERIFICATION_TOKEN,
    request.headers.get("X-Notion-Signature"),
  );
  if (!valid) return json({ ok: false, error: "invalid_signature" }, 401);

  const eventId = payload.id;
  const eventType = payload.type;
  const entityId = payload.entity?.id;
  if (!eventId || !eventType) return json({ ok: false, error: "missing_event_identity" }, 400);

  const record = await recordWebhookReceived(env.MANIFEST, {
    id: eventId,
    type: eventType,
    entityId: entityId ?? null,
    timestamp: payload.timestamp ?? null,
  });
  if (!entityId || !eventType.startsWith("page.")) {
    return json({ ok: true, ignored: true, reason: "non_page_event_or_missing_entity", event_id: eventId });
  }
  if (!record.inserted && record.status !== "QUEUE_ERROR" && record.status !== "RECEIVED") {
    return json({ ok: true, duplicate: true, event_id: eventId });
  }

  const message: IngestMessage = {
    kind: "notion-page-sync",
    page_id: entityId,
    cause_id: eventId,
    cause_type: "webhook",
    event_type: eventType,
    ...(payload.timestamp ? { event_timestamp: payload.timestamp } : {}),
  };
  try {
    await env.INGEST_QUEUE.send(message, { contentType: "json" });
    await markWebhookQueued(env.MANIFEST, eventId);
    return json({ ok: true, queued: true, event_id: eventId }, 202);
  } catch (error) {
    const queueError = error instanceof Error ? error.message : String(error);
    try {
      await stageSyncMessages(env.MANIFEST, [message]);
      await markWebhookFallbackScheduled(env.MANIFEST, eventId, queueError);
      return json({ ok: true, queued: false, fallback_scheduled: true, event_id: eventId }, 202);
    } catch (fallbackError) {
      await markWebhookQueueError(
        env.MANIFEST,
        eventId,
        `queue=${queueError}; fallback=${fallbackError instanceof Error ? fallbackError.message : String(fallbackError)}`,
      );
      return errorJson(fallbackError, 503);
    }
  }
}

async function handleReconcile(request: Request, env: Env): Promise<Response> {
  if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
  const body = (await request.json().catch(() => ({}))) as { page_id?: string; limit?: number };
  const limit = Number.isFinite(body.limit) ? Math.max(1, Math.min(1000, Math.floor(body.limit as number))) : undefined;
  const runId = crypto.randomUUID();
  const mode = body.page_id ? "MANUAL_PAGE" : limit ? "BOUNDED_NOTES_RECONCILE" : "FULL_NOTES_RECONCILE";
  await beginSyncRun(env.MANIFEST, runId, mode);
  let count = 0;
  try {
    if (body.page_id) {
      const cause = `reconcile:${runId}:${body.page_id}`;
      await stageSyncMessages(env.MANIFEST, [
        { kind: "notion-page-sync", page_id: body.page_id, cause_id: cause, cause_type: "manual" },
      ]);
      count = 1;
    } else {
      const messages: IngestMessage[] = [];
      for await (const pageId of listNotesPages(env)) {
        messages.push({ kind: "notion-page-sync", page_id: pageId, cause_id: `reconcile:${runId}:${pageId}`, cause_type: "reconcile" });
        if (limit && count + messages.length >= limit) break;
        if (messages.length >= 100) {
          await stageSyncMessages(env.MANIFEST, messages);
          count += messages.length;
          messages.length = 0;
        }
      }
      if (messages.length) {
        await stageSyncMessages(env.MANIFEST, messages);
        count += messages.length;
      }
    }
    await completeSyncRun(env.MANIFEST, runId, count);
    return json({ ok: true, run_id: runId, mode, limit: limit ?? null, pages_scheduled: count, scheduler: "D1_CRON" }, 202);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    await failSyncRun(env.MANIFEST, runId, count, message);
    throw error;
  }
}

interface ReaderLayerState {
  page_id: string;
  url: string | null;
  core_view_id: string;
  methods_view_id: string;
  evidence_view_id: string;
  practice_view_id: string;
  history_view_id: string;
}

interface ReaderCounts {
  core: number;
  methods: number;
  evidence: number;
  practice: number;
  history: number;
}

interface AcademicSourceRow {
  page_id: string;
  title: string;
  governance_state: string | null;
  replacement_ids_json: string;
}

interface ReaderLink {
  title: string;
  url: string;
}

function safeJsonIds(raw: string | null | undefined): string[] {
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw) as unknown;
    return Array.isArray(parsed) ? parsed.filter((value): value is string => typeof value === "string") : [];
  } catch {
    return [];
  }
}

async function ensureReaderView(
  env: Env,
  baseViewId: string,
  input: {
    name: string;
    type: "gallery" | "chart";
    configuration: Record<string, unknown>;
    position?: Record<string, unknown>;
  },
) {
  const base = await retrieveView(env, baseViewId);
  const databaseId = base.parent?.database_id;
  const dataSourceId = base.data_source_id;
  if (!databaseId || !dataSourceId) throw new Error(`Reader base view ${baseViewId} is missing database/data-source identity`);
  const views = await listDatabaseViews(env, databaseId);
  const existing = views.find((view) => view.name === input.name && view.type === input.type);
  const visual = existing ?? await createViewOnDatabase(env, {
    database_id: databaseId,
    data_source_id: dataSourceId,
    name: input.name,
    type: input.type,
    ...(base.filter ? { filter: base.filter } : {}),
    ...(base.sorts?.length ? { sorts: base.sorts } : {}),
    configuration: input.configuration,
    position: input.position ?? { type: "start" },
  });
  return { base, visual };
}

async function ensureReaderDashboard(
  env: Env,
  baseViewId: string,
  input: {
    rolePropertyId: string;
    galleryProperties: Array<Record<string, unknown>>;
  },
) {
  const base = await retrieveView(env, baseViewId);
  const databaseId = base.parent?.database_id;
  const dataSourceId = base.data_source_id;
  if (!databaseId || !dataSourceId) throw new Error(`Reader base view ${baseViewId} is missing database/data-source identity`);

  const topViews = await listDatabaseViews(env, databaseId);
  let dashboard = topViews.find((view) => view.name === "00｜Dashboard｜知识总览" && view.type === "dashboard")
    ?? await createViewOnDatabase(env, {
      database_id: databaseId,
      data_source_id: dataSourceId,
      name: "00｜Dashboard｜知识总览",
      type: "dashboard",
      position: { type: "start" },
    });
  dashboard = await retrieveView(env, dashboard.id);
  const rows = Array.isArray(dashboard.configuration?.rows)
    ? dashboard.configuration.rows as Array<{ widgets?: Array<{ view_id?: string }> }>
    : [];
  const widgetIds = rows.flatMap((row) => row.widgets ?? []).map((widget) => widget.view_id).filter((id): id is string => typeof id === "string");
  const existingWidgets = [] as Awaited<ReturnType<typeof retrieveView>>[];
  for (const widgetId of widgetIds) existingWidgets.push(await retrieveView(env, widgetId));
  const ensureWidget = async (widget: {
    name: string;
    type: "list" | "gallery" | "chart";
    filter?: Record<string, unknown>;
    sorts?: Array<Record<string, unknown>>;
    configuration?: Record<string, unknown>;
    placement: { type: "new_row"; row_index?: number } | { type: "existing_row"; row_index: number };
  }) => {
    const existing = existingWidgets.find((view) => view.name === widget.name && view.type === widget.type);
    if (existing) return existing;
    const created = await createDashboardWidgetView(env, {
      dashboard_view_id: dashboard.id,
      data_source_id: dataSourceId,
      name: widget.name,
      type: widget.type,
      ...(widget.filter ? { filter: widget.filter } : {}),
      ...(widget.sorts?.length ? { sorts: widget.sorts } : {}),
      ...(widget.configuration ? { configuration: widget.configuration } : {}),
      placement: widget.placement,
    });
    existingWidgets.push(created);
    return created;
  };

  const coreFilter = {
    and: [
      {
        or: [
          { property: FIELDS.contentLevel, select: { equals: "L4｜Framework" } },
          { property: FIELDS.contentLevel, select: { equals: "L5｜Knowledge Object" } },
        ],
      },
      { property: FIELDS.governanceState, select: { equals: "ACTIVE" } },
      { property: FIELDS.relationState, select: { equals: "VALID" } },
    ],
  };
  const evidenceFilter = {
    and: [
      { property: FIELDS.contentLevel, select: { equals: "L6｜Evidence / Case" } },
      { property: FIELDS.governanceState, select: { equals: "ACTIVE" } },
      { property: FIELDS.relationState, select: { equals: "VALID" } },
    ],
  };
  const methodFilter = {
    and: [
      { property: FIELDS.knowledgeRole, select: { equals: "METHOD" } },
      { property: FIELDS.governanceState, select: { equals: "ACTIVE" } },
      { property: FIELDS.relationState, select: { equals: "VALID" } },
    ],
  };
  const practiceFilter = {
    and: [
      { property: FIELDS.contentLevel, select: { equals: "L7｜Practice / Output" } },
      { property: FIELDS.governanceState, select: { equals: "ACTIVE" } },
    ],
  };
  const currentFilter = {
    and: [
      { property: FIELDS.retrievalSpace, select: { equals: "CURRENT" } },
      { property: FIELDS.searchEligibility, select: { equals: "DEFAULT" } },
      { property: FIELDS.governanceState, select: { equals: "ACTIVE" } },
      { property: FIELDS.relationState, select: { equals: "VALID" } },
    ],
  };
  const chartConfiguration = (caption: string) => ({
    type: "chart",
    chart_type: "donut",
    x_axis: { type: "select", property_id: input.rolePropertyId, sort: { type: "manual" }, hide_empty_groups: true },
    y_axis: { aggregator: "count" },
    color_theme: "auto",
    height: "small",
    legend_position: "side",
    show_data_labels: true,
    donut_labels: "name_and_value",
    caption,
  });
  const galleryConfiguration = {
    type: "gallery",
    properties: input.galleryProperties,
    cover: null,
    card_layout: "compact",
  };

  const coreChart = await ensureWidget({
    name: "Core｜知识角色",
    type: "chart",
    filter: coreFilter,
    configuration: chartConfiguration("Core Knowledge by role"),
    placement: { type: "new_row", row_index: 0 },
  });
  const evidenceChart = await ensureWidget({
    name: "Evidence｜证据结构",
    type: "chart",
    filter: evidenceFilter,
    configuration: chartConfiguration("Evidence / Case by role"),
    placement: { type: "existing_row", row_index: 0 },
  });
  const currentGallery = await ensureWidget({
    name: "Current｜当前知识",
    type: "gallery",
    filter: currentFilter,
    sorts: [{ property: FIELDS.knowledgeRole, direction: "ascending" }, { property: FIELDS.title, direction: "ascending" }],
    configuration: galleryConfiguration,
    placement: { type: "new_row", row_index: 1 },
  });
  const methodsGallery = await ensureWidget({
    name: "Methods｜方法",
    type: "gallery",
    filter: methodFilter,
    sorts: [{ property: FIELDS.title, direction: "ascending" }],
    configuration: galleryConfiguration,
    placement: { type: "new_row", row_index: 2 },
  });
  const practiceGallery = await ensureWidget({
    name: "Practice｜实践",
    type: "gallery",
    filter: practiceFilter,
    sorts: [{ property: FIELDS.title, direction: "ascending" }],
    configuration: galleryConfiguration,
    placement: { type: "existing_row", row_index: 2 },
  });

  return { dashboard, coreChart, evidenceChart, currentGallery, methodsGallery, practiceGallery };
}

function readerCard(icon: string, color: string, title: string, count: number, detail: string, url: string): string {
  return [
    `\t<column>`,
    `\t\t<callout icon="${icon}" color="${color}">`,
    `\t\t\t**${title}** · **${count}**<br>${detail}<br>[进入视图 →](${url})`,
    `\t\t</callout>`,
    `\t</column>`,
  ].join("\n");
}

async function buildReaderVisualization(
  env: Env,
  reader: ReaderLayerState,
  views: {
    dashboard: ReaderLink;
    core: ReaderLink;
    methods: ReaderLink;
    evidence: ReaderLink;
    practice: ReaderLink;
    history: ReaderLink;
  },
): Promise<{ markdown: string; counts: ReaderCounts; academic_done: number; academic_total: number; academic_next: string | null }> {
  const counts = await env.MANIFEST.prepare(
    `SELECT
      SUM(CASE WHEN active=1 AND governance_state='ACTIVE' AND relation_state='VALID' AND content_level IN ('L4｜Framework','L5｜Knowledge Object') THEN 1 ELSE 0 END) AS core,
      SUM(CASE WHEN active=1 AND governance_state='ACTIVE' AND relation_state='VALID' AND knowledge_role='METHOD' THEN 1 ELSE 0 END) AS methods,
      SUM(CASE WHEN active=1 AND governance_state='ACTIVE' AND relation_state='VALID' AND content_level='L6｜Evidence / Case' THEN 1 ELSE 0 END) AS evidence,
      SUM(CASE WHEN active=1 AND governance_state='ACTIVE' AND content_level='L7｜Practice / Output' THEN 1 ELSE 0 END) AS practice,
      SUM(CASE WHEN active=1 AND (effective_space='PROVENANCE' OR governance_state IN ('LEGACY','ARCHIVED','HOLD')) THEN 1 ELSE 0 END) AS history
     FROM documents`,
  ).first<ReaderCounts>() ?? { core: 0, methods: 0, evidence: 0, practice: 0, history: 0 };

  const academicOrder = [
    "D01｜城市更新与社区营造",
    "D04｜数字设计、BIM与智能建造",
    "D06｜公共建筑、社会基础设施与公共性",
    "D07｜居住研究、住房与日常生活",
    "D03｜气候低碳与韧性设计",
    "D05｜建筑经济、开发策划与全生命周期价值",
    "D02｜乡村建筑与地方营造",
  ];
  const sourceRows = await env.MANIFEST.prepare(
    `SELECT page_id,title,governance_state,replacement_ids_json
     FROM documents
     WHERE active=1 AND title IN (${academicOrder.map(() => "?").join(",")})`,
  ).bind(...academicOrder).all<AcademicSourceRow>();
  const sourceByTitle = new Map(sourceRows.results.map((row) => [row.title, row]));
  const academicLines: string[] = [];
  let academicDone = 0;
  let academicNext: string | null = null;

  for (const title of academicOrder) {
    const row = sourceByTitle.get(title);
    const replacements = safeJsonIds(row?.replacement_ids_json);
    const done = row?.governance_state === "LEGACY" && replacements.length > 0;
    if (done) {
      academicDone += 1;
      const target = await env.MANIFEST.prepare(
        "SELECT title,notion_url FROM documents WHERE page_id=? AND active=1 LIMIT 1",
      ).bind(replacements[0]).first<{ title: string; notion_url: string | null }>();
      academicLines.push(target?.notion_url
        ? `✅ [${target.title}](${target.notion_url})`
        : `✅ ${title}`);
    } else {
      if (!academicNext) academicNext = title;
      academicLines.push(`${academicNext === title ? "◐" : "○"} ${title}`);
    }
  }

  const methodIds = ["MTH-KNOWLEDGE-ACADEMIC-NOTE-001", "MTH-ARCH-RESEARCH-001", "MTH-ARCH-EVIDENCE-GOV-001"];
  const methodRows = await env.MANIFEST.prepare(
    `SELECT canonical_id,title,notion_url FROM documents
     WHERE active=1 AND canonical_id IN (?,?,?) ORDER BY title`,
  ).bind(...methodIds).all<{ canonical_id: string; title: string; notion_url: string | null }>();
  const methodLines = methodRows.results.map((row) => row.notion_url ? `- [${row.title}](${row.notion_url})` : `- ${row.title}`);

  const filled = "●".repeat(academicDone);
  const open = "○".repeat(Math.max(0, academicOrder.length - academicDone));
  const today = new Date().toISOString().slice(0, 10);
  const intro = [
    `<callout icon="🧭" color="blue_bg">`,
    `\t**READ CURRENT FIRST｜先读当前知识，再追溯证据。**<br>这里是人的阅读首页，不是治理后台。默认先打开 **Dashboard** 看全局，再按 **Core → Methods → Evidence → Practice** 深入；History 只在需要追溯来源、旧版本或迁移关系时打开。<br>[打开知识仪表盘 →](${views.dashboard.url})`,
    `</callout>`,
    ``,
    `## 阅读地图`,
    ``,
    `<columns>`,
    readerCard("📘", "blue_bg", "Core Knowledge｜核心知识", Number(counts.core ?? 0), "L4/L5 · ACTIVE · VALID；先读论点与框架", views.core.url),
    readerCard("🧪", "purple_bg", "Methods｜方法", Number(counts.methods ?? 0), "研究、证据治理与专业方法；回答“怎么做”", views.methods.url),
    readerCard("🔎", "yellow_bg", "Evidence｜证据", Number(counts.evidence ?? 0), "L6 Source / Evidence / Case；需要核验时进入", views.evidence.url),
    `</columns>`,
    ``,
    `<columns>`,
    readerCard("🛠️", "green_bg", "Practice｜实践", Number(counts.practice ?? 0), "L7 Practice / Output；看真实执行与 readback", views.practice.url),
    readerCard("🗂️", "gray_bg", "History｜历史与治理", Number(counts.history ?? 0), "Legacy / Provenance / Hold；默认不占第一阅读层", views.history.url),
    [
      `\t<column>`,
      `\t\t<callout icon="◒" color="orange_bg">`,
      `\t\t\t**Academic Migration｜专题论文级迁移** · **${academicDone}/${academicOrder.length}**<br><span color="green">${filled}</span><span color="gray">${open}</span><br>${academicNext ? `下一项：**${academicNext}**` : "专题队列已完成"}`,
      `\t\t</callout>`,
      `\t</column>`,
    ].join("\n"),
    `</columns>`,
    ``,
    `## 当前知识主线`,
    ``,
    `<columns>`,
    `\t<column>`,
    `\t\t<callout icon="📚" color="blue_bg">`,
    `\t\t\t**专题 Current**<br>${academicLines.join("<br>")}`,
    `\t\t</callout>`,
    `\t</column>`,
    `\t<column>`,
    `\t\t<callout icon="⚙️" color="purple_bg">`,
    `\t\t\t**方法 Owner**<br>${methodLines.join("<br>") || "方法 owner 尚未索引"}`,
    `\t\t</callout>`,
    `\t</column>`,
    `</columns>`,
    ``,
    `## 阅读方式`,
    ``,
    `<callout icon="→" color="gray_bg">`,
    `\t**Core** 形成理解 → **Methods** 决定怎么研究/执行 → **Evidence** 负责核验 → **Practice** 看真实结果。<br>遇到版本冲突、旧口径或替代关系时再进入 **History**。机器 ID、PR、receipt、migration log 不承担第一层阅读任务。`,
    `</callout>`,
    ``,
    `> Reader snapshot refreshed **${today}**. Core 数量包含其中的 Method 对象，五个数字不是互斥分区，也不应相加为 corpus 总量。`,
    ``,
    `---`,
    ``,
    `## Live Views｜实时知识视图`,
    ``,
    `下方仍连接同一 Notes 数据源：**Dashboard** 是第一入口，**Cards / Map** 用于浏览，**List** 用于完整检索；没有复制第二套知识库。`,
    ``,
  ].join("\n");

  return { markdown: intro, counts, academic_done: academicDone, academic_total: academicOrder.length, academic_next: academicNext };
}

async function visualizeReaderLayer(env: Env): Promise<Record<string, unknown>> {
  const stored = await env.MANIFEST.prepare("SELECT state_value FROM runtime_state WHERE state_key='reader_layer_v1' LIMIT 1")
    .first<{ state_value: string }>();
  if (!stored?.state_value) throw new Error("reader_layer_v1 is not initialized");
  const reader = JSON.parse(stored.state_value) as ReaderLayerState;
  const notes = await retrieveNotesDataSource(env);
  const roleProperty = notes.properties?.[FIELDS.knowledgeRole];
  const rolePropertyId = typeof roleProperty?.id === "string" ? roleProperty.id : FIELDS.knowledgeRole;
  const galleryProperties = [
    { property_id: FIELDS.knowledgeRole, visible: true, card_property_width_mode: "inline" },
    { property_id: FIELDS.contentLevel, visible: true, card_property_width_mode: "inline" },
  ];

  const dashboard = await ensureReaderDashboard(env, reader.core_view_id, {
    rolePropertyId,
    galleryProperties,
  });

  const coreGallery = await ensureReaderView(env, reader.core_view_id, {
    name: "01｜Cards｜核心知识",
    type: "gallery",
    configuration: { type: "gallery", properties: galleryProperties, cover: null, card_layout: "compact" },
    position: { type: "start" },
  });
  const coreMap = await ensureReaderView(env, reader.core_view_id, {
    name: "Map｜知识角色分布",
    type: "chart",
    configuration: {
      type: "chart",
      chart_type: "donut",
      x_axis: { type: "select", property_id: rolePropertyId, sort: { type: "manual" }, hide_empty_groups: true },
      y_axis: { aggregator: "count" },
      color_theme: "auto",
      height: "small",
      legend_position: "side",
      show_data_labels: true,
      donut_labels: "name_and_value",
      caption: "Core Knowledge by knowledge role",
    },
    position: { type: "after_view", view_id: coreGallery.visual.id },
  });
  const methodsGallery = await ensureReaderView(env, reader.methods_view_id, {
    name: "02｜Cards｜方法",
    type: "gallery",
    configuration: { type: "gallery", properties: galleryProperties, cover: null, card_layout: "compact" },
    position: { type: "start" },
  });
  const evidenceMap = await ensureReaderView(env, reader.evidence_view_id, {
    name: "03｜Map｜证据分布",
    type: "chart",
    configuration: {
      type: "chart",
      chart_type: "donut",
      x_axis: { type: "select", property_id: rolePropertyId, sort: { type: "manual" }, hide_empty_groups: true },
      y_axis: { aggregator: "count" },
      color_theme: "auto",
      height: "small",
      legend_position: "side",
      show_data_labels: true,
      donut_labels: "name_and_value",
      caption: "L6 evidence objects by knowledge role",
    },
    position: { type: "start" },
  });
  const practiceGallery = await ensureReaderView(env, reader.practice_view_id, {
    name: "04｜Cards｜实践",
    type: "gallery",
    configuration: { type: "gallery", properties: galleryProperties, cover: null, card_layout: "compact" },
    position: { type: "start" },
  });

  await updateView(env, reader.core_view_id, { name: "List｜核心完整目录" });
  await updateView(env, reader.methods_view_id, { name: "List｜方法完整目录" });
  await updateView(env, reader.evidence_view_id, { name: "List｜证据完整索引" });
  await updateView(env, reader.practice_view_id, { name: "List｜实践完整目录" });
  const historyView = await updateView(env, reader.history_view_id, { name: "99｜Trace｜历史与治理" });

  const visual = await buildReaderVisualization(env, reader, {
    dashboard: { title: dashboard.dashboard.name ?? "Dashboard", url: dashboard.dashboard.url ?? reader.url ?? "" },
    core: { title: coreGallery.visual.name ?? "Core Knowledge", url: coreGallery.visual.url ?? reader.url ?? "" },
    methods: { title: methodsGallery.visual.name ?? "Methods", url: methodsGallery.visual.url ?? reader.url ?? "" },
    evidence: { title: evidenceMap.visual.name ?? "Evidence", url: evidenceMap.visual.url ?? reader.url ?? "" },
    practice: { title: practiceGallery.visual.name ?? "Practice", url: practiceGallery.visual.url ?? reader.url ?? "" },
    history: { title: historyView.name ?? "History", url: historyView.url ?? reader.url ?? "" },
  });
  await replaceReaderIntroMarkdown(env, reader.page_id, visual.markdown);
  const readback = await fetchCompleteMarkdown(env, reader.page_id);
  const state = {
    reader_page_id: reader.page_id,
    reader_url: reader.url,
    dashboard_view_id: dashboard.dashboard.id,
    dashboard_core_chart_view_id: dashboard.coreChart.id,
    dashboard_evidence_chart_view_id: dashboard.evidenceChart.id,
    dashboard_current_gallery_view_id: dashboard.currentGallery.id,
    dashboard_methods_gallery_view_id: dashboard.methodsGallery.id,
    dashboard_practice_gallery_view_id: dashboard.practiceGallery.id,
    core_gallery_view_id: coreGallery.visual.id,
    core_map_view_id: coreMap.visual.id,
    methods_gallery_view_id: methodsGallery.visual.id,
    evidence_map_view_id: evidenceMap.visual.id,
    practice_gallery_view_id: practiceGallery.visual.id,
    counts: visual.counts,
    academic_done: visual.academic_done,
    academic_total: visual.academic_total,
    academic_next: visual.academic_next,
    markdown_length: readback.markdown.length,
    markdown_truncated: readback.truncated,
    unknown_block_ids: readback.unknown_block_ids,
  };
  await env.MANIFEST.prepare(
    "INSERT INTO runtime_state(state_key,state_value,updated_at) VALUES('reader_visual_v1',?,?) ON CONFLICT(state_key) DO UPDATE SET state_value=excluded.state_value,updated_at=excluded.updated_at",
  ).bind(JSON.stringify(state), new Date().toISOString()).run();
  return state;
}

async function handleRequest(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  if (request.method === "GET" && url.pathname === "/health") {
    return json({ ok: true, service: "oleander-notion-canonical-knowledge", version: "0.1.0" });
  }
  if (request.method === "POST" && url.pathname === "/webhooks/notion") return handleWebhook(request, env);
  if (request.method === "POST" && url.pathname === "/v1/reconcile") return handleReconcile(request, env);

  if (url.pathname === "/v1/governance-page") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    if (request.method === "GET") {
      const pageId = url.searchParams.get("page_id");
      if (!pageId) return json({ ok: false, error: "page_id_required" }, 400);
      const [page, markdown] = await Promise.all([fetchPage(env, pageId), fetchCompleteMarkdown(env, pageId)]);
      return json({
        ok: true,
        page: normalizePage(page),
        markdown: markdown.markdown,
        markdown_truncated: markdown.truncated,
        unknown_block_ids: markdown.unknown_block_ids,
      });
    }
    if (request.method === "POST") {
      const body = (await request.json().catch(() => ({}))) as {
        page_id?: string;
        updates?: {
          canonical_id?: string | null;
          retrieval_space?: string | null;
          search_eligibility?: string | null;
          governance_state?: string | null;
          relation_state?: string | null;
        };
      };
      if (!body.page_id) return json({ ok: false, error: "page_id_required" }, 400);
      if (!body.updates || typeof body.updates !== "object") return json({ ok: false, error: "updates_required" }, 400);
      const before = normalizePage(await fetchPage(env, body.page_id));
      await updatePageGovernanceFields(env, body.page_id, body.updates);
      const syncResult = await syncPage(env, {
        kind: "notion-page-sync",
        page_id: body.page_id,
        cause_id: `governance:${crypto.randomUUID()}`,
        cause_type: "manual",
      });
      const after = normalizePage(await fetchPage(env, body.page_id));
      return json({ ok: true, before, after, sync: syncResult });
    }
  }

  if (request.method === "POST" && url.pathname === "/v1/academic-page") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    const body = (await request.json().catch(() => ({}))) as {
      title?: string;
      canonical_id?: string;
      markdown?: string;
      source_page_ids?: string[];
      replaced_page_ids?: string[];
      retrieval_space?: string;
      search_eligibility?: string;
      trust_state?: string;
      governance_state?: string;
      relation_state?: string;
      content_level?: string;
      knowledge_role?: string;
    };
    if (!body.title || !body.canonical_id || !body.markdown) return json({ ok: false, error: "title_canonical_id_markdown_required" }, 400);
    if (!/^[A-Z0-9][A-Z0-9-]{4,}$/.test(body.canonical_id)) return json({ ok: false, error: "invalid_canonical_id" }, 400);
    const allowedRetrieval = new Set(["CURRENT", "SUPPORT", "PROVENANCE"]);
    const allowedEligibility = new Set(["DEFAULT", "SCOPED", "HISTORY_ONLY", "BLOCKED"]);
    const allowedTrust = new Set(["UNKNOWN", "UNVERIFIED", "VERIFIED"]);
    const allowedGovernance = new Set(["ACTIVE", "ARCHIVED", "HOLD", "LEGACY", "REVIEW"]);
    const allowedRelation = new Set(["REVIEW", "VALID"]);
    const allowedLevels = new Set(["L4｜Framework", "L5｜Knowledge Object", "L6｜Evidence / Case", "L7｜Practice / Output"]);
    const allowedRoles = new Set(["INDEX", "THEORY", "METHOD", "EVIDENCE", "SOURCE", "CASE", "PRACTICE", "TOOL"]);
    if (body.retrieval_space && !allowedRetrieval.has(body.retrieval_space)) return json({ ok: false, error: "invalid_retrieval_space" }, 400);
    if (body.search_eligibility && !allowedEligibility.has(body.search_eligibility)) return json({ ok: false, error: "invalid_search_eligibility" }, 400);
    if (body.trust_state && !allowedTrust.has(body.trust_state)) return json({ ok: false, error: "invalid_trust_state" }, 400);
    if (body.governance_state && !allowedGovernance.has(body.governance_state)) return json({ ok: false, error: "invalid_governance_state" }, 400);
    if (body.relation_state && !allowedRelation.has(body.relation_state)) return json({ ok: false, error: "invalid_relation_state" }, 400);
    if (body.content_level && !allowedLevels.has(body.content_level)) return json({ ok: false, error: "invalid_content_level" }, 400);
    if (body.knowledge_role && !allowedRoles.has(body.knowledge_role)) return json({ ok: false, error: "invalid_knowledge_role" }, 400);
    const duplicate = await env.MANIFEST.prepare(
      "SELECT page_id, title FROM documents WHERE active=1 AND canonical_id=? LIMIT 1",
    ).bind(body.canonical_id).first<{ page_id: string; title: string }>();
    if (duplicate) return json({ ok: false, error: "canonical_id_exists", duplicate }, 409);

    const page = await createAcademicPage(env, {
      title: body.title,
      canonical_id: body.canonical_id,
      markdown: body.markdown,
      source_page_ids: body.source_page_ids ?? [],
      replaced_page_ids: body.replaced_page_ids ?? [],
      ...(body.retrieval_space ? { retrieval_space: body.retrieval_space } : {}),
      ...(body.search_eligibility ? { search_eligibility: body.search_eligibility } : {}),
      ...(body.trust_state ? { trust_state: body.trust_state } : {}),
      ...(body.governance_state ? { governance_state: body.governance_state } : {}),
      ...(body.relation_state ? { relation_state: body.relation_state } : {}),
      ...(body.content_level ? { content_level: body.content_level } : {}),
      ...(body.knowledge_role ? { knowledge_role: body.knowledge_role } : {}),
    });
    const sync = await syncPage(env, {
      kind: "notion-page-sync",
      page_id: page.id,
      cause_id: `academic:${crypto.randomUUID()}`,
      cause_type: "manual",
    });
    return json({ ok: true, page: normalizePage(await fetchPage(env, page.id)), sync });
  }

  if (request.method === "POST" && url.pathname === "/v1/academic-page/content") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    const body = (await request.json().catch(() => ({}))) as {
      page_id?: string;
      old_str?: string;
      new_str?: string;
    };
    if (!body.page_id || !body.old_str || !body.new_str) {
      return json({ ok: false, error: "page_id_old_str_new_str_required" }, 400);
    }
    if (body.old_str === body.new_str) return json({ ok: false, error: "content_patch_noop" }, 400);
    if (body.old_str.length > 20_000 || body.new_str.length > 20_000) {
      return json({ ok: false, error: "content_patch_too_large" }, 413);
    }

    const beforePage = normalizePage(await fetchPage(env, body.page_id));
    if (beforePage.parentDataSourceId !== env.NOTION_NOTES_DATA_SOURCE_ID) {
      return json({ ok: false, error: "academic_page_not_in_notes_data_source" }, 409);
    }
    if (!beforePage.canonicalId || beforePage.retrievalSpace !== "CURRENT" || beforePage.governanceState !== "ACTIVE") {
      return json({
        ok: false,
        error: "academic_content_patch_requires_active_current_canonical_page",
        canonical_id: beforePage.canonicalId,
        retrieval_space: beforePage.retrievalSpace,
        governance_state: beforePage.governanceState,
      }, 409);
    }
    if (beforePage.relationState !== "REVIEW") {
      return json({ ok: false, error: "academic_content_patch_requires_review_state", relation_state: beforePage.relationState }, 409);
    }

    const beforeMarkdown = await fetchCompleteMarkdown(env, body.page_id);
    if (beforeMarkdown.truncated || beforeMarkdown.unknown_block_ids.length > 0) {
      return json({ ok: false, error: "academic_content_patch_requires_complete_readback" }, 409);
    }
    const occurrences = beforeMarkdown.markdown.split(body.old_str).length - 1;
    if (occurrences !== 1) {
      return json({ ok: false, error: "content_patch_old_str_must_match_once", occurrences }, 409);
    }

    await updatePageMarkdownContent(env, body.page_id, body.old_str, body.new_str);
    const afterMarkdown = await fetchCompleteMarkdown(env, body.page_id);
    if (afterMarkdown.truncated || afterMarkdown.unknown_block_ids.length > 0) {
      return json({ ok: false, error: "content_patch_post_readback_incomplete" }, 502);
    }
    if (!afterMarkdown.markdown.includes(body.new_str) || afterMarkdown.markdown.includes(body.old_str)) {
      return json({ ok: false, error: "content_patch_readback_failed" }, 502);
    }
    const sync = await syncPage(env, {
      kind: "notion-page-sync",
      page_id: body.page_id,
      cause_id: `academic-content:${crypto.randomUUID()}`,
      cause_type: "manual",
    });
    return json({
      ok: true,
      page: normalizePage(await fetchPage(env, body.page_id)),
      before_markdown_length: beforeMarkdown.markdown.length,
      after_markdown_length: afterMarkdown.markdown.length,
      markdown_truncated: afterMarkdown.truncated,
      unknown_block_ids: afterMarkdown.unknown_block_ids,
      sync,
    });
  }

  if (request.method === "POST" && url.pathname === "/v1/reader-layer") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    const existing = await env.MANIFEST.prepare("SELECT state_value FROM runtime_state WHERE state_key='reader_layer_v1' LIMIT 1")
      .first<{ state_value: string }>();
    if (existing?.state_value) return json({ ok: true, existing: true, reader: JSON.parse(existing.state_value) });

    const page = await createReaderPage(env);
    const current = await createLinkedNotesView(env, page.id, {
      name: "01｜Core Knowledge｜核心知识",
      type: "list",
      filter: {
        and: [
          {
            or: [
              { property: "内容层级", select: { equals: "L4｜Framework" } },
              { property: "内容层级", select: { equals: "L5｜Knowledge Object" } },
            ],
          },
          { property: "治理状态", select: { equals: "ACTIVE" } },
          { property: "关系状态", select: { equals: "VALID" } },
        ],
      },
      sorts: [{ property: "知识角色", direction: "ascending" }, { property: "Name", direction: "ascending" }],
    });
    const support = await createLinkedNotesView(env, page.id, {
      name: "02｜Methods｜方法",
      type: "list",
      filter: {
        and: [
          { property: "知识角色", select: { equals: "METHOD" } },
          { property: "治理状态", select: { equals: "ACTIVE" } },
          { property: "关系状态", select: { equals: "VALID" } },
        ],
      },
      sorts: [{ property: "Name", direction: "ascending" }],
    });
    const evidence = await createLinkedNotesView(env, page.id, {
      name: "03｜Evidence｜证据",
      type: "list",
      filter: {
        and: [
          { property: "内容层级", select: { equals: "L6｜Evidence / Case" } },
          { property: "治理状态", select: { equals: "ACTIVE" } },
          { property: "关系状态", select: { equals: "VALID" } },
        ],
      },
      sorts: [{ property: "Name", direction: "ascending" }],
    });
    const practice = await createLinkedNotesView(env, page.id, {
      name: "04｜Practice｜实践",
      type: "list",
      filter: {
        and: [
          { property: "内容层级", select: { equals: "L7｜Practice / Output" } },
          { property: "治理状态", select: { equals: "ACTIVE" } },
        ],
      },
      sorts: [{ property: "Name", direction: "ascending" }],
    });
    const history = await createLinkedNotesView(env, page.id, {
      name: "99｜History｜历史与治理",
      type: "list",
      filter: {
        or: [
          { property: "Retrieval Space｜检索空间", select: { equals: "PROVENANCE" } },
          { property: "治理状态", select: { equals: "LEGACY" } },
          { property: "治理状态", select: { equals: "ARCHIVED" } },
          { property: "治理状态", select: { equals: "HOLD" } },
        ],
      },
      sorts: [{ property: "Name", direction: "ascending" }],
    });
    const reader = {
      page_id: page.id,
      url: page.url ?? null,
      core_view_id: current.id,
      methods_view_id: support.id,
      evidence_view_id: evidence.id,
      practice_view_id: practice.id,
      history_view_id: history.id,
    };
    await env.MANIFEST.prepare(
      "INSERT INTO runtime_state(state_key,state_value,updated_at) VALUES('reader_layer_v1',?,?) ON CONFLICT(state_key) DO UPDATE SET state_value=excluded.state_value,updated_at=excluded.updated_at",
    ).bind(JSON.stringify(reader), new Date().toISOString()).run();
    return json({ ok: true, existing: false, reader });
  }

  if (request.method === "POST" && url.pathname === "/v1/reader-layer/visualize") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    try {
      const state = await visualizeReaderLayer(env);
      return json({ ok: true, visualized: true, state });
    } catch (error) {
      return errorJson(error);
    }
  }

  if (request.method === "POST" && url.pathname === "/v1/drain-once") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    await drainScheduledSync(env);
    return json({ ok: true, drained: true, batch_size: SCHEDULED_SYNC_BATCH_SIZE });
  }

  if (request.method === "GET" && url.pathname === "/v1/reconcile-status") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    const runId = url.searchParams.get("run_id");
    if (!runId) return json({ ok: false, error: "run_id_required" }, 400);
    const readback = await syncRunReadback(env.MANIFEST, runId);
    return readback ? json({ ok: true, run: readback }) : json({ ok: false, error: "not_found" }, 404);
  }

  if (request.method === "GET" && url.pathname === "/v1/scheduler-status") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    const [lastSeen, lastResult, taskCounts] = await Promise.all([
      getRuntimeState(env.MANIFEST, "scheduled_cron_last_seen"),
      getRuntimeState(env.MANIFEST, "scheduled_cron_last_result"),
      schedulerTaskCounts(env.MANIFEST),
    ]);
    let lastSeenAt: string | null = null;
    if (lastSeen?.value) {
      try {
        const parsed = JSON.parse(lastSeen.value) as { started_at?: string };
        lastSeenAt = parsed.started_at ?? lastSeen.updated_at;
      } catch {
        lastSeenAt = lastSeen.updated_at;
      }
    }
    const lastSeenMs = lastSeenAt ? Date.parse(lastSeenAt) : Number.NaN;
    const cronStale = !Number.isFinite(lastSeenMs) || Date.now() - lastSeenMs > 3 * 60 * 1000;
    const openTasks =
      (taskCounts.PENDING ?? 0) +
      (taskCounts.RETRY ?? 0) +
      (taskCounts.PROCESSING ?? 0);
    return json({
      ok: true,
      cron_stale: cronStale,
      fallback_required: cronStale && openTasks > 0,
      open_tasks: openTasks,
      task_counts: taskCounts,
      scheduled_cron_last_seen: lastSeen,
      scheduled_cron_last_result: lastResult,
    });
  }

  if (request.method === "GET" && url.pathname === "/v1/queue-metrics") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    const [ingest, dlq] = await Promise.all([env.INGEST_QUEUE.metrics(), env.INGEST_DLQ.metrics()]);
    return json({
      ok: true,
      ingest: {
        queue: "oleander-notion-ingest",
        backlog_count: ingest.backlogCount,
        backlog_bytes: ingest.backlogBytes,
        oldest_message_timestamp: ingest.oldestMessageTimestamp?.toISOString() ?? null,
      },
      dlq: {
        queue: "oleander-notion-ingest-dlq",
        backlog_count: dlq.backlogCount,
        backlog_bytes: dlq.backlogBytes,
        oldest_message_timestamp: dlq.oldestMessageTimestamp?.toISOString() ?? null,
      },
    });
  }

  if (url.pathname === "/v1/webhook-setup-token") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    if (request.method === "GET") {
      const pending = await getRuntimeState(env.MANIFEST, "pending_notion_webhook_verification_token");
      if (!pending) return json({ ok: false, error: "not_found" }, 404);
      return json({
        ok: true,
        verification_token: await decryptSetupSecret(pending.value, env.OLEANDER_API_TOKEN),
        captured_at: pending.updated_at,
        instruction: "Set this value as NOTION_WEBHOOK_VERIFICATION_TOKEN, then DELETE /v1/webhook-setup-token.",
      });
    }
    if (request.method === "DELETE") {
      await deleteRuntimeState(env.MANIFEST, "pending_notion_webhook_verification_token");
      return json({ ok: true, cleared: true });
    }
  }

  if (request.method === "GET" && url.pathname === "/v1/reader-snapshot") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    return json(await buildKnowledgeReaderSnapshot(env.MANIFEST));
  }

  if (request.method === "POST" && url.pathname === "/v1/search") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    try {
      const body = (await request.json()) as SearchRequest;
      return json(await knowledgeSearch(env, body));
    } catch (error) {
      return errorJson(error, 400);
    }
  }

  const canonicalMatch = /^\/v1\/knowledge-pack\/([^/]+)$/.exec(url.pathname);
  if (request.method === "GET" && canonicalMatch) {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    const canonicalId = decodeURIComponent(canonicalMatch[1] ?? "");
    const pack = await knowledgePackByCanonicalId(env, canonicalId);
    return pack ? json(pack) : json({ ok: false, error: "not_found" }, 404);
  }
  return json({ ok: false, error: "not_found" }, 404);
}

function retryDelaySeconds(attempts: number): number {
  return Math.min(3600, 60 * 2 ** Math.max(0, attempts - 1));
}

async function seedOperatorRequestedReconcile(env: Env): Promise<boolean> {
  const request = await getRuntimeState(env.MANIFEST, "scheduled_reconcile_request");
  if (!request || !request.value.startsWith("REQUESTED")) return false;

  const [, requestedLimit] = request.value.split(":", 2);
  const parsedLimit = requestedLimit ? Number.parseInt(requestedLimit, 10) : Number.NaN;
  const limit = Number.isFinite(parsedLimit) ? Math.max(1, Math.min(1000, parsedLimit)) : undefined;
  const runId = crypto.randomUUID();
  const mode = limit ? "OPERATOR_BOUNDED_RECONCILE" : "OPERATOR_FULL_RECONCILE";
  await putRuntimeState(env.MANIFEST, "scheduled_reconcile_request", `CLAIMED:${runId}`);
  await beginSyncRun(env.MANIFEST, runId, mode);

  let count = 0;
  try {
    const messages: IngestMessage[] = [];
    for await (const pageId of listNotesPages(env)) {
      messages.push({ kind: "notion-page-sync", page_id: pageId, cause_id: `reconcile:${runId}:${pageId}`, cause_type: "reconcile" });
      if (limit && count + messages.length >= limit) break;
      if (messages.length >= 100) {
        await stageSyncMessages(env.MANIFEST, messages);
        count += messages.length;
        messages.length = 0;
      }
    }
    if (messages.length) {
      await stageSyncMessages(env.MANIFEST, messages);
      count += messages.length;
    }
    await completeSyncRun(env.MANIFEST, runId, count);
    await putRuntimeState(
      env.MANIFEST,
      "scheduled_reconcile_last_run",
      JSON.stringify({ run_id: runId, mode, pages_scheduled: count, scheduled_at: new Date().toISOString() }),
    );
    await deleteRuntimeState(env.MANIFEST, "scheduled_reconcile_request");
    return true;
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    await failSyncRun(env.MANIFEST, runId, count, message);
    await putRuntimeState(env.MANIFEST, "scheduled_reconcile_request", `ERROR:${runId}:${message.slice(0, 1000)}`);
    throw error;
  }
}

async function drainScheduledSync(env: Env): Promise<void> {
  // Seeding a full reconcile can enumerate >1k Notion rows and persist >1k D1
  // tasks. Do not also process a page in that same Free-plan Cron invocation.
  if (await seedOperatorRequestedReconcile(env)) return;
  const staleBefore = new Date(Date.now() - SCHEDULED_SYNC_STALE_PROCESSING_MS).toISOString();
  await requeueStaleSyncTasks(env.MANIFEST, staleBefore);
  const tasks = await claimDueSyncTasks(env.MANIFEST, SCHEDULED_SYNC_BATCH_SIZE);
  const touchedRuns = new Set<string>();

  for (const task of tasks) {
    const message: IngestMessage = {
      kind: "notion-page-sync",
      page_id: task.page_id,
      cause_id: task.cause_id,
      cause_type: task.cause_type,
      ...(task.event_type ? { event_type: task.event_type } : {}),
    };
    if (task.run_id) touchedRuns.add(task.run_id);
    try {
      await syncPage(env, message);
      await recordSyncMessageReceipt(env.MANIFEST, {
        causeId: task.cause_id,
        pageId: task.page_id,
        causeType: task.cause_type,
        eventType: task.event_type,
        status: "PROCESSED",
        attempts: task.attempts,
      });
      if (task.cause_type === "webhook") await markWebhookProcessed(env.MANIFEST, task.cause_id);
    } catch (error) {
      const messageText = error instanceof Error ? error.message : String(error);
      const blocked = task.attempts >= SCHEDULED_SYNC_MAX_ATTEMPTS;
      const nextAttemptAt = blocked
        ? null
        : new Date(Date.now() + retryDelaySeconds(task.attempts) * 1000).toISOString();
      await recordSyncMessageReceipt(env.MANIFEST, {
        causeId: task.cause_id,
        pageId: task.page_id,
        causeType: task.cause_type,
        eventType: task.event_type,
        status: blocked ? "BLOCKED" : "RETRY",
        attempts: task.attempts,
        error: messageText,
        nextAttemptAt,
      });
      if (task.cause_type === "webhook") {
        await markWebhookFallbackFailure(env.MANIFEST, task.cause_id, messageText, blocked);
      }
      console.error("scheduled_knowledge_ingest_failed", {
        cause_id: task.cause_id,
        page_id: task.page_id,
        attempts: task.attempts,
        blocked,
        next_attempt_at: nextAttemptAt,
        error: messageText,
        fingerprint: await sha256Hex(`${task.page_id}:${task.cause_id}`),
      });
    }
  }

  for (const runId of touchedRuns) await refreshSyncRunStatus(env.MANIFEST, runId);
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    try {
      return await handleRequest(request, env);
    } catch (error) {
      return errorJson(error);
    }
  },

  async queue(batch: MessageBatch<IngestMessage>, env: Env): Promise<void> {
    for (const message of batch.messages) {
      try {
        if (message.body.kind !== "notion-page-sync") {
          message.ack();
          continue;
        }
        await syncPage(env, message.body);
        if (message.body.cause_id.startsWith("reconcile:")) {
          await recordSyncMessageReceipt(env.MANIFEST, {
            causeId: message.body.cause_id,
            pageId: message.body.page_id,
            causeType: message.body.cause_type,
            eventType: message.body.event_type ?? null,
            status: "PROCESSED",
            attempts: message.attempts,
          });
        }
        if (message.body.cause_type === "webhook") await markWebhookProcessed(env.MANIFEST, message.body.cause_id);
        message.ack();
      } catch (error) {
        if (message.body.cause_id.startsWith("reconcile:")) {
          await recordSyncMessageReceipt(env.MANIFEST, {
            causeId: message.body.cause_id,
            pageId: message.body.page_id,
            causeType: message.body.cause_type,
            eventType: message.body.event_type ?? null,
            status: "RETRY",
            attempts: message.attempts,
            error: error instanceof Error ? error.message : String(error),
          });
        }
        console.error("knowledge_ingest_failed", {
          queue_message_id: message.id,
          cause_id: message.body.cause_id,
          page_id: message.body.page_id,
          attempts: message.attempts,
          error: error instanceof Error ? error.message : String(error),
          fingerprint: await sha256Hex(`${message.body.page_id}:${message.body.cause_id}`),
        });
        message.retry({ delaySeconds: Math.min(900, 2 ** Math.min(message.attempts, 9)) });
      }
    }
  },

  async scheduled(controller: ScheduledController, env: Env, _ctx: ExecutionContext): Promise<void> {
    const startedAt = new Date().toISOString();
    await putRuntimeState(
      env.MANIFEST,
      "scheduled_cron_last_seen",
      JSON.stringify({
        started_at: startedAt,
        scheduled_time: new Date(controller.scheduledTime).toISOString(),
        cron: controller.cron,
      }),
    );
    try {
      await drainScheduledSync(env);
      await putRuntimeState(
        env.MANIFEST,
        "scheduled_cron_last_result",
        JSON.stringify({ ok: true, started_at: startedAt, completed_at: new Date().toISOString() }),
      );
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      await putRuntimeState(
        env.MANIFEST,
        "scheduled_cron_last_result",
        JSON.stringify({ ok: false, started_at: startedAt, failed_at: new Date().toISOString(), error: message.slice(0, 1000) }),
      );
      throw error;
    }
  },
} satisfies ExportedHandler<Env, IngestMessage>;
