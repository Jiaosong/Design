const NAV = [
  ['01', 'Home'],
  ['02', 'Projects'],
  ['03', 'Design'],
  ['04', 'Knowledge'],
  ['05', 'Sources'],
  ['06', 'Browser'],
  ['07', 'Integrations'],
  ['08', 'Review'],
  ['09', 'System'],
]

const RELIABILITY = [
  ['R1', 'Admission'],
  ['R2', 'Identity'],
  ['R3', 'Capability'],
  ['R4', 'Execution'],
  ['R5', 'Result'],
]

const state = {
  view: 'Home',
  sourceInbox: [],
  projects: [],
  executionSurfaces: [],
  surfaceViews: [],
  browserProfile: null,
  hostRuntimes: [],
  knowledgeBody: null,
  hostBound: false,
  hostHealth: null,
  reliability: Object.fromEntries(RELIABILITY.map(([id]) => [id, 'UNKNOWN'])),
}

const workspace = document.querySelector('#workspace')
const nav = document.querySelector('#primaryNav')
const commandDialog = document.querySelector('#commandDialog')
const commandInput = document.querySelector('#commandInput')
const commandResults = document.querySelector('#commandResults')
const commandButton = document.querySelector('#commandButton')
const compactReliability = document.querySelector('#compactReliability')
const hostStatus = document.querySelector('#hostStatus')

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')
}

function renderNav() {
  nav.innerHTML = NAV.map(([code, label]) => `
    <button class="nav-button ${state.view === label ? 'active' : ''}" type="button" data-view="${label}">
      <span class="nav-code">${code}</span><span>${label}</span>
    </button>
  `).join('')
  nav.querySelectorAll('[data-view]').forEach(button => {
    button.addEventListener('click', () => setView(button.dataset.view))
  })
}

function reliabilityMarkup(compact = false) {
  if (compact) {
    return RELIABILITY.map(([id, name]) => `
      <div class="mini-stage"><strong>${id}</strong><span>${name}</span><span class="state-label unknown">${state.reliability[id]}</span></div>
    `).join('')
  }
  return `<div class="reliability-grid">${RELIABILITY.map(([id, name]) => `
    <div class="reliability-stage">
      <div class="stage-id">${id}</div>
      <div class="stage-name">${name}</div>
      <div class="stage-state"><span class="state-label unknown">${state.reliability[id]}</span></div>
    </div>
  `).join('')}</div>`
}

function surfaceReliabilityVector(surface) {
  const vector = Object.fromEntries(RELIABILITY.map(([id]) => [id, 'UNKNOWN']))
  if (!surface) return vector
  const stages = surface.reliability_preflight?.stages || {}
  const stageMap = {
    R1: 'R1_ADMISSION',
    R2: 'R2_IDENTITY',
    R3: 'R3_CAPABILITY',
    R4: 'R4_EXECUTION',
  }
  for (const [shortId, stageId] of Object.entries(stageMap)) {
    const stage = stages[stageId]
    if (stage?.state) vector[shortId] = String(stage.state).toUpperCase()
  }
  vector.R5 = 'NOT_RUN'
  return vector
}

function compactSurfaceVector(surface) {
  const vector = surfaceReliabilityVector(surface)
  return RELIABILITY.map(([id]) => `${id} ${vector[id]}`).join(' · ')
}

function header(title, lede, eyebrow = 'OLEANDER DESIGN SYSTEM') {
  return `<header class="workspace-header"><div><div class="eyebrow">${eyebrow}</div><h1>${title}</h1><p class="lede">${lede}</p></div></header>`
}

function homeView() {
  return `${header('工作台', '从项目状态、设计对象、知识与真实执行面进入工作。Chat 只是操作方式之一。')}
    <div class="grid">
      <section class="card span-4"><h2>Projects</h2><div class="metric">${state.projects.length}</div><div class="metric-label">发现的 project candidate</div><p>${state.hostBound ? '发现 ≠ 已绑定 Project。仍需 owner-native Project State / authority binding。' : 'Host 未绑定；不会从当前目录猜测 Project。'}</p></section>
      <section class="card span-4"><h2>Open Decisions</h2><div class="metric">—</div><div class="metric-label">等待 Project Context</div><p>Decision / KEEP / Promotion 仍由 Authority Kernel 与现有 owner-native contracts 管理。</p></section>
      <section class="card span-4"><h2>Source Inbox</h2><div class="metric">${state.sourceInbox.length}</div><div class="metric-label">本地 staged source</div><p>Staged ≠ ingested ≠ Knowledge Current。</p></section>
      <section class="card span-8"><h2>Current frontier</h2><div class="object-list"><div class="object-row"><div><div class="object-title">尚未解析 Project Context</div><div class="object-meta">Host Runtime / Project State 未绑定；产品壳不会从当前目录猜测 Current。</div></div><span class="state-label unknown">UNRESOLVED</span></div></div></section>
      <section class="card span-4"><h2>Surface Reliability</h2><div class="reliability-mini">${reliabilityMarkup(true)}</div></section>
    </div>`
}

function projectsView() {
  const rows = state.projects.length ? state.projects.map(project => `
    <div class="object-row">
      <div>
        <div class="object-title">${escapeHtml(project.directory_name)}</div>
        <div class="object-meta">${escapeHtml(project.state)} · ${project.local_repository_branch ? `branch ${escapeHtml(project.local_repository_branch)} · ` : ''}${project.local_repository_revision ? `${escapeHtml(project.local_repository_revision.slice(0, 12))} · ` : ''}target repo: ${escapeHtml(project.target_repository_candidate)}<br>migration: ${escapeHtml(project.migration_state || 'NOT_SPLIT')}${project.migration_split_commit ? ` · ${escapeHtml(project.migration_split_commit.slice(0, 12))}` : ''}${project.legacy_source_retained ? ' · legacy copy retained' : ''}</div>
      </div>
      <span class="state-label ${project.local_repository_ready ? 'pass' : 'staged'}">${escapeHtml(project.local_repository_ready ? 'LOCAL REPO READY' : project.migration_state === 'SPLIT_BRANCH_READY' ? 'SPLIT READY' : 'DISCOVERED')}</span>
    </div>
  `).join('') : '<div class="object-row"><div><div class="object-title">没有已发现项目</div><div class="object-meta">Host Runtime 未绑定或 05-cases 为空。</div></div><span class="state-label unknown">EMPTY</span></div>'
  return `${header('Projects', '一个 OLEANDER Project 可以绑定 primary repository、satellite repositories、多个 runtime workspaces、artifact stores 与 knowledge mounts。', 'PROJECT KERNEL')}
    <div class="grid">
      <section class="card span-12">
        <h2>Project Registry</h2>
        <div class="object-list">${rows}</div>
      </section>
      <section class="card span-6"><h2>Git boundary</h2><p>Git commit ≠ Project Current<br>Git branch ≠ Design Direction<br>Git merge ≠ Design KEEP<br>Git clean ≠ Design Valid</p></section>
      <section class="card span-6"><h2>Workspace boundary</h2><p>Runtime Workspace 是 materialization。它可以对应 main、design direction、presentation、research 或 temporary runtime，但不拥有 Project State。</p></section>
    </div>`
}

function designView() {
  return `${header('Design', '设计对象、方向比较、修改、混合、综合、读回与 Review 的主工作区。Provider mechanics 保持在后台。', 'DESIGN KERNEL')}
    <div class="grid">
      <section class="card span-8"><h2>Canvas / Native Surface</h2><div class="drop-zone"><strong>尚未绑定 Native Design Surface</strong><span>Rhino / AutoCAD / Revit / Blender / Figma 等将通过 SurfaceView 打开，不直接绕过 ActionRuntime。</span><br><button class="button" disabled>Open Surface</button></div></section>
      <section class="card span-4"><h2>Design Actions</h2><div class="object-list">${['Explore','Compare','Critique','Develop','Modify','Mix','Synthesize','Readback','Review'].map(x => `<div class="object-row"><div class="object-title">${x}</div><span class="state-label unknown">HOST_NOT_BOUND</span></div>`).join('')}</div></section>
    </div>`
}

function knowledgeView() {
  const drafts = state.sourceInbox.filter(item => item.status === 'KNOWLEDGE_DRAFT_READY')
  const surfaceById = new Map(state.surfaceViews.map(surface => [surface.surface_definition_id, surface]))
  const knowledgeSurfaces = [
    ['Notion', 'notion_connector'],
    ['Google Drive', 'google_drive_connector'],
    ['Baidu', 'baidu_storage'],
  ].map(([name, id]) => {
    const surface = surfaceById.get(id)
    return {
      name,
      status: surface ? String(surface.availability || 'UNKNOWN').toUpperCase() : 'UNREGISTERED',
      source: surface?.observation_source || 'NO_CURRENT_SURFACE',
    }
  })
  const draftRows = drafts.length ? drafts.map(item => `
    <div class="object-row">
      <div>
        <div class="object-title">${escapeHtml(item.name)}</div>
        <div class="object-meta">${escapeHtml(item.source_id || item.id)} · ${item.bodySectionCount || item.extraction?.section_count || '?'} sections · Review OPEN · KI UNGRADED · OE UNGRADED</div>
      </div>
      <button class="button" type="button" data-open-knowledge="${escapeHtml(item.source_id || '')}">打开正文</button>
    </div>
  `).join('') : '<div class="object-row"><div><div class="object-title">暂无 Knowledge Draft</div><div class="object-meta">先从 Sources 导入可提取的文档；Imported 仍不等于 Knowledge Current。</div></div><span class="state-label unknown">EMPTY</span></div>'
  const body = state.knowledgeBody?.body
  const draft = state.knowledgeBody?.knowledge_draft
  const bodyMarkup = body ? `
    <section class="card span-12">
      <div class="knowledge-body-head">
        <div><h2>Structured Body</h2><div class="object-meta">${escapeHtml(body.body_id)} · source revision ${escapeHtml(String(body.source_revision).slice(0, 28))}…</div></div>
        <div class="knowledge-state-line"><span class="state-label staged">Review ${escapeHtml(draft?.review_state || 'OPEN')}</span><span class="state-label unknown">KI ${escapeHtml(draft?.ki_state || 'UNGRADED')}</span><span class="state-label unknown">OE ${escapeHtml(draft?.oe_state || 'UNGRADED')}</span></div>
      </div>
      <div class="structured-sections">${(body.sections || []).map(section => `<article class="structured-section"><div class="section-citation">${escapeHtml(section.citation?.kind || 'SOURCE')} ${escapeHtml(section.citation?.page || section.citation?.slide || section.citation?.paragraph || '')}</div>${section.heading ? `<h3>${escapeHtml(section.heading)}</h3>` : ''}<div class="section-text">${escapeHtml(section.text || '')}</div></article>`).join('')}</div>
    </section>` : ''
  return `${header('Knowledge', 'Source、Structured Body、Provenance、KI、OE、Knowledge Mount 分离管理；Vector index 只是检索层。', 'KNOWLEDGE KERNEL')}
    <div class="grid">
      <section class="card span-4"><h2>Knowledge Drafts</h2><div class="metric">${drafts.length}</div><div class="metric-label">尚未进入 Knowledge Current</div></section>
      <section class="card span-4"><h2>Mounts</h2><div class="metric">—</div><div class="metric-label">Task-specific projection</div></section>
      <section class="card span-4"><h2>Review queue</h2><div class="metric">${state.sourceInbox.length}</div><div class="metric-label">仅 staged，不代表待 KI/OE</div></section>
      <section class="card span-12"><h2>Draft Library</h2><div class="object-list">${draftRows}</div></section>
      <section class="card span-12"><h2>External Knowledge Surfaces</h2><div class="integration-grid">${knowledgeSurfaces.map(surface => `<div class="integration-card"><div class="integration-head"><span class="integration-name">${escapeHtml(surface.name)}</span><span class="state-label ${surface.status === 'AVAILABLE' ? 'pass' : 'unknown'}">${escapeHtml(surface.status)}</span></div><div class="integration-meta">Observation: ${escapeHtml(surface.source)}<br>Linked source/view ≠ OLEANDER Knowledge Current</div></div>`).join('')}</div></section>
      ${bodyMarkup}
      <section class="card span-12"><h2>Knowledge boundary</h2><p>Original Source ≠ Extracted Body · Extracted ≠ Validated · Imported ≠ Knowledge Current · Vector Index ≠ Knowledge</p></section>
    </div>`
}

async function openKnowledgeBody(sourceId) {
  if (!sourceId || !state.hostBound) return
  try {
    state.knowledgeBody = await apiJson(`/api/source/${encodeURIComponent(sourceId)}/body`)
  } catch (error) {
    state.knowledgeBody = { error: error.message }
  }
  render()
}

function bindKnowledge() {
  document.querySelectorAll('[data-open-knowledge]').forEach(button => {
    button.addEventListener('click', () => openKnowledgeBody(button.dataset.openKnowledge))
  })
}

async function digestFile(file) {
  const buffer = await file.arrayBuffer()
  const hash = await crypto.subtle.digest('SHA-256', buffer)
  return 'sha256:' + [...new Uint8Array(hash)].map(v => v.toString(16).padStart(2, '0')).join('')
}

function mapHostSource(source) {
  return {
    id: source.source_id,
    source_id: source.source_id,
    name: source.name || source.source_id,
    size: Number(source.size || 0),
    type: source.content_type || source.source_kind || 'application/octet-stream',
    fingerprint: source.fingerprint || 'unknown',
    status: source.ingestion_state || 'ORIGINAL_PRESERVED',
    extraction: source.extraction || null,
    persisted: true,
    bodyPreview: source.body_preview || '',
    bodySectionCount: source.body_section_count || 0,
  }
}

async function apiJson(url, options = {}) {
  const response = await fetch(url, {
    cache: 'no-store',
    ...options,
    headers: {
      ...(options.body instanceof Blob ? {} : { 'Content-Type': 'application/json' }),
      ...(options.headers || {}),
    },
  })
  const payload = await response.json().catch(() => ({ status: 'FAIL', error: `HTTP_${response.status}` }))
  if (!response.ok) throw new Error(payload.error || `HTTP_${response.status}`)
  return payload
}

async function uploadFileToHost(file) {
  const init = await apiJson('/api/source/init', {
    method: 'POST',
    body: JSON.stringify({ name: file.name, size: file.size, type: file.type }),
  })
  const upload = init.upload
  const chunkSize = Number(upload.chunk_size || 4 * 1024 * 1024)
  const chunkCount = Math.ceil(file.size / chunkSize)
  const temporary = {
    id: `upload-${upload.upload_id}`,
    name: file.name,
    size: file.size,
    type: file.type || 'application/octet-stream',
    fingerprint: 'server-calculating',
    status: 'UPLOADING',
    persisted: false,
  }
  state.sourceInbox.unshift(temporary)
  render()
  for (let index = 0; index < chunkCount; index += 1) {
    const start = index * chunkSize
    const end = Math.min(file.size, start + chunkSize)
    await apiJson(`/api/source/chunk?upload_id=${encodeURIComponent(upload.upload_id)}&index=${index}`, {
      method: 'PUT',
      body: file.slice(start, end),
      headers: { 'Content-Type': 'application/octet-stream' },
    })
    temporary.status = `UPLOADING ${Math.round(((index + 1) / Math.max(1, chunkCount)) * 100)}%`
    render()
  }
  const committed = await apiJson('/api/source/commit', {
    method: 'POST',
    body: JSON.stringify({ upload_id: upload.upload_id, chunk_count: chunkCount }),
  })
  const mapped = mapHostSource(committed.source)
  mapped.extraction = committed.extraction || mapped.extraction
  if (committed.extraction?.preview) mapped.bodyPreview = committed.extraction.preview
  if (committed.extraction?.section_count) mapped.bodySectionCount = committed.extraction.section_count
  const position = state.sourceInbox.findIndex(item => item.id === temporary.id)
  if (position >= 0) state.sourceInbox.splice(position, 1, mapped)
  else state.sourceInbox.unshift(mapped)
}

async function stageFiles(files) {
  for (const file of files) {
    if (state.hostBound) {
      try {
        await uploadFileToHost(file)
      } catch (error) {
        state.sourceInbox.unshift({
          id: crypto.randomUUID(),
          name: file.name,
          size: file.size,
          type: file.type || 'application/octet-stream',
          fingerprint: 'upload-failed',
          status: `HOST_UPLOAD_FAILED: ${error.message}`,
        })
      }
      continue
    }
    const digest = await digestFile(file)
    state.sourceInbox.push({
      id: crypto.randomUUID(),
      name: file.name,
      size: file.size,
      type: file.type || 'application/octet-stream',
      fingerprint: digest,
      status: 'STAGED_LOCAL_ONLY',
    })
  }
  render()
}

function sourcesView() {
  const rows = state.sourceInbox.length ? state.sourceInbox.map(item => {
    const statusClass = item.status === 'KNOWLEDGE_DRAFT_READY' ? 'pass' : 'staged'
    const extraction = item.extraction?.status ? ` · extraction: ${item.extraction.status}` : ''
    const body = item.bodySectionCount ? ` · body ${item.bodySectionCount} sections` : ''
    return `<div class="object-row"><div><div class="object-title">${escapeHtml(item.name)}</div><div class="object-meta">${escapeHtml(item.type)} · ${item.size.toLocaleString()} bytes · ${escapeHtml(item.fingerprint.slice(0, 24))}…${escapeHtml(extraction)}${escapeHtml(body)}</div>${item.bodyPreview ? `<div class="source-preview">${escapeHtml(item.bodyPreview)}</div>` : ''}</div><span class="state-label ${statusClass}">${escapeHtml(item.status)}</span></div>`
  }).join('') : '<div class="object-row"><div><div class="object-title">暂无 Source</div><div class="object-meta">Host 绑定时会持久化原件并生成 server-side fingerprint；无 Host 时只做浏览器本地 staged。</div></div><span class="state-label unknown">EMPTY</span></div>'
  return `${header('Sources', '把文档、视频、音频、图片或网页先作为 Source 保留原件与指纹，再进入结构化正文、引用绑定、Review、KI/OE。', 'SOURCE INBOX')}
    <div class="grid">
      <section class="card span-12">
        <div id="sourceDrop" class="drop-zone">
          <strong>拖入文件到 Source Inbox</strong>
          <span>PDF · DOCX · PPTX · XLSX · MP4 · MOV · MP3 · WAV · Images · CAD/BIM/GIS packages</span><br>
          <button id="pickSource" class="button primary" type="button">选择文件</button>
          <input id="sourcePicker" type="file" multiple>
        </div>
      </section>
      <section class="card span-12"><h2>${state.hostBound ? 'Source Inbox' : 'Staged Sources'}</h2><div class="object-list">${rows}</div></section>
    </div>`
}

function browserView() {
  const browserViews = state.surfaceViews.filter(view => view.view_kind === 'BROWSER')
  const profile = state.browserProfile
  const browserRows = browserViews.length ? browserViews.map(view => `
    <div class="object-row">
      <div><div class="object-title">${escapeHtml(view.display_name)}</div><div class="object-meta">${escapeHtml(compactSurfaceVector(view))}<br>${escapeHtml(view.observation_source || 'NO_CURRENT_SURFACE_OBSERVATION')}</div></div>
      <span class="state-label ${view.availability === 'AVAILABLE' ? 'pass' : view.availability === 'DEGRADED' ? 'staged' : 'unknown'}">${escapeHtml(view.availability)}</span>
    </div>
  `).join('') : '<div class="object-row"><div><div class="object-title">没有 Browser SurfaceView</div></div><span class="state-label unknown">EMPTY</span></div>'
  return `${header('Browser', '项目级 Design Browser：Browse / Research / Compare / Capture / Clip / Ingest。Persistent capture 必须进入 Source Inbox。', 'BROWSER SURFACE')}
    <div class="grid">
      <section class="card span-8"><h2>Browser SurfaceViews</h2><div class="object-list">${browserRows}</div></section>
      <section class="card span-4"><h2>Browser Profile</h2><div class="object-list"><div class="object-row"><div><div class="object-title">${escapeHtml(profile?.browser_profile_id || 'UNRESOLVED')}</div><div class="object-meta">Scope: ${escapeHtml(profile?.scope || 'UNKNOWN')}<br>Downloads → ${escapeHtml(profile?.download_target || 'UNKNOWN')}<br>Captures → ${escapeHtml(profile?.capture_target || 'UNKNOWN')}</div></div><span class="state-label unknown">${escapeHtml(profile?.status || 'NOT_BOUND')}</span></div></div></section>
      <section class="card span-4"><h2>Capture semantics</h2><p>PAGE_LOADED ≠ SOURCE_CAPTURED<br>SOURCE_CAPTURED ≠ KNOWLEDGE_INGESTED<br>KNOWLEDGE_INGESTED ≠ KNOWLEDGE_CURRENT</p></section>
    </div>`
}

function integrationsView() {
  const names = state.surfaceViews
  return `${header('Integrations', 'SurfaceDefinition 保持可见；是否能执行由 SurfaceInstance / Identity / CapabilityCatalog / Reliability 决定。', 'SURFACE KERNEL')}
    <div class="grid">
      <section class="card span-12"><h2>Surface Registry</h2><div class="integration-grid">${names.map(surface => {
        const statusClass = surface.availability === 'AVAILABLE' ? 'pass' : surface.availability === 'DEGRADED' ? 'staged' : 'unknown'
        return `<div class="integration-card"><div class="integration-head"><span class="integration-name">${escapeHtml(surface.display_name)}</span><span class="state-label ${statusClass}">${escapeHtml(surface.availability)}</span></div><div class="integration-meta">${escapeHtml(surface.view_kind)} · Reliability: ${escapeHtml(surface.reliability_preflight?.status || 'UNKNOWN')}<br>${escapeHtml(compactSurfaceVector(surface))}<br>Observation: ${escapeHtml(surface.observation_source || 'NO_CURRENT_SURFACE_OBSERVATION')}<br>Authority ceiling: UI projection only</div></div>`
      }).join('') || '<div class="object-meta">SurfaceView projection unavailable.</div>'}</div></section>
      <section class="card span-12"><h2>Surface Reliability Boundary</h2>${reliabilityMarkup(false)}</section>
    </div>`
}

function reviewView() {
  return `${header('Review', 'Human decision、Knowledge Review、Design KEEP、专业 Review 与 Promotion gate 在这里汇总，但不由 UI 自己产生 authority。', 'AUTHORITY / REVIEW')}
    <div class="grid"><section class="card span-12"><h2>Review Queue</h2><div class="object-row"><div><div class="object-title">无 owner-native review objects</div><div class="object-meta">需要 Host Runtime + Project Context 才能加载真实 Review。</div></div><span class="state-label unknown">EMPTY</span></div></section></div>`
}

function systemView() {
  const hostRows = state.hostRuntimes.length ? state.hostRuntimes.map(host => {
    const statusClass = host.availability === 'AVAILABLE' ? 'pass' : host.status === 'STALE' || host.availability === 'DEGRADED' ? 'staged' : 'unknown'
    const detail = [
      host.host_class,
      host.version ? `version ${host.version}` : null,
      host.reason || null,
      host.snapshot_at ? `snapshot ${host.snapshot_at}` : null,
    ].filter(Boolean).join(' · ')
    return `<div class="object-row"><div><div class="object-title">${escapeHtml(host.host_runtime_id)}</div><div class="object-meta">${escapeHtml(detail)}</div></div><span class="state-label ${statusClass}">${escapeHtml(host.status || host.availability || 'UNKNOWN')}</span></div>`
  }).join('') : '<div class="object-row"><div><div class="object-title">Host Runtime view unavailable</div></div><span class="state-label unknown">UNKNOWN</span></div>'
  return `${header('System', 'Runtime、Host、Surface、Recovery 与 advanced execution diagnostics。普通设计操作不需要暴露 worker/task/checkpoint。', 'SYSTEM / ADVANCED')}
    <div class="grid">
      <section class="card span-6"><h2>Host Runtime</h2><div class="object-list">${hostRows}</div></section>
      <section class="card span-6"><h2>Execution Kernel</h2><p>ExecutionLedger<br>ActionRuntime<br>DurableJob</p></section>
      <section class="card span-12"><h2>Reliability Console</h2>${reliabilityMarkup(false)}</section>
    </div>`
}

function renderWorkspace() {
  const views = {
    Home: homeView,
    Projects: projectsView,
    Design: designView,
    Knowledge: knowledgeView,
    Sources: sourcesView,
    Browser: browserView,
    Integrations: integrationsView,
    Review: reviewView,
    System: systemView,
  }
  workspace.innerHTML = (views[state.view] || homeView)()
  if (state.view === 'Sources') bindSourceInbox()
  if (state.view === 'Knowledge') bindKnowledge()
  compactReliability.innerHTML = reliabilityMarkup(true)
}

function bindSourceInbox() {
  const drop = document.querySelector('#sourceDrop')
  const picker = document.querySelector('#sourcePicker')
  const pick = document.querySelector('#pickSource')
  pick.addEventListener('click', () => picker.click())
  picker.addEventListener('change', () => stageFiles([...picker.files]))
  ;['dragenter', 'dragover'].forEach(type => drop.addEventListener(type, event => {
    event.preventDefault()
    drop.classList.add('dragover')
  }))
  ;['dragleave', 'drop'].forEach(type => drop.addEventListener(type, event => {
    event.preventDefault()
    drop.classList.remove('dragover')
  }))
  drop.addEventListener('drop', event => stageFiles([...event.dataTransfer.files]))
}

function setView(view) {
  if (!NAV.some(([, label]) => label === view)) return
  state.view = view
  render()
  workspace.focus()
}

const commands = [
  ...NAV.map(([, label]) => ({ label: `打开 ${label}`, detail: 'Navigate', run: () => setView(label) })),
  { label: '导入 Source', detail: 'Sources · local staging only', run: () => setView('Sources') },
  { label: '查看 Surface Reliability', detail: 'System · R1–R5', run: () => setView('System') },
  { label: '查看 Integrations', detail: 'Surface registry', run: () => setView('Integrations') },
]

function renderCommands(query = '') {
  const needle = query.trim().toLowerCase()
  const rows = commands.filter(item => !needle || `${item.label} ${item.detail}`.toLowerCase().includes(needle))
  commandResults.innerHTML = rows.map((item, index) => `<button class="command-item" type="button" data-command="${index}"><strong>${escapeHtml(item.label)}</strong><span>${escapeHtml(item.detail)}</span></button>`).join('') || '<div class="object-meta" style="padding:12px">没有匹配命令</div>'
  commandResults.querySelectorAll('[data-command]').forEach((button, index) => {
    button.addEventListener('click', () => {
      rows[index].run()
      commandDialog.close()
    })
  })
}

function openCommand() {
  renderCommands('')
  commandInput.value = ''
  commandDialog.showModal()
  requestAnimationFrame(() => commandInput.focus())
}

commandButton.addEventListener('click', openCommand)
commandInput.addEventListener('input', () => renderCommands(commandInput.value))
document.addEventListener('keydown', event => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault()
    openCommand()
  }
})

function render() {
  renderNav()
  renderWorkspace()
  renderHostStatus()
}

function renderHostStatus() {
  if (state.hostBound) {
    hostStatus.innerHTML = '<span class="status-dot pass"></span><span>Design System Local Host · READY</span>'
  } else {
    hostStatus.innerHTML = '<span class="status-dot unknown"></span><span>Host Runtime 未绑定</span>'
  }
}

async function bootstrapHost() {
  try {
    const health = await apiJson('/api/health')
    if (health.status !== 'PASS') throw new Error('HOST_HEALTH_FAILED')
    state.hostBound = true
    state.hostHealth = health
    const [projects, sources, system, surfaceViews, browserProfile, hostRuntimes] = await Promise.all([
      apiJson('/api/projects'),
      apiJson('/api/sources'),
      apiJson('/api/system'),
      apiJson('/api/surface-views'),
      apiJson('/api/browser/profile'),
      apiJson('/api/hosts'),
    ])
    state.projects = Array.isArray(projects.projects) ? projects.projects : []
    state.sourceInbox = Array.isArray(sources.sources) ? sources.sources.map(mapHostSource) : []
    state.executionSurfaces = Array.isArray(system.view?.surfaces) ? system.view.surfaces : []
    state.surfaceViews = Array.isArray(surfaceViews.surface_views) ? surfaceViews.surface_views : []
    state.browserProfile = browserProfile || null
    state.hostRuntimes = Array.isArray(hostRuntimes.hosts) ? hostRuntimes.hosts : []
    const localHostSurface = state.executionSurfaces.find(surface => surface.surface_id === 'design_system_local_host')
    state.reliability = surfaceReliabilityVector(localHostSurface)
  } catch {
    state.hostBound = false
    state.reliability = Object.fromEntries(RELIABILITY.map(([id]) => [id, 'UNKNOWN']))
  }
  render()
}

render()
bootstrapHost()
