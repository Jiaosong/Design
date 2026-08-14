(() => {
  'use strict';

  const root = document.querySelector('#project-display');
  const params = new URLSearchParams(location.search);
  const projectId = params.get('project') || 'xj01';
  const registry = {
    xj01: 'data/projects/xj01.json'
  };

  const escapeHTML = (value = '') => String(value).replace(/[&<>"']/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
  }[char]));

  const statusTone = (value = '') => {
    const text = String(value).toUpperCase();
    if (/(PASS|READY|RETAIN|CLOSED)/.test(text) && !/(NOT|OPEN|INCOMPLETE)/.test(text)) return 'positive';
    if (/(OPEN|PENDING|NOT_|INCOMPLETE|DRAFT|REBUILD|READY_NOT_EXECUTED)/.test(text)) return 'open';
    if (/(REJECT|FAIL|BLOCK)/.test(text)) return 'negative';
    return 'neutral';
  };

  const badge = (value, label = value) =>
    `<span class="project-status project-status--${statusTone(value)}">${escapeHTML(label)}</span>`;

  const artifactsFor = (data, capabilityId) =>
    data.artifacts.filter((artifact) => {
      const caps = Array.isArray(artifact.capability) ? artifact.capability : [artifact.capability].filter(Boolean);
      return caps.includes(capabilityId) && artifact.web_available;
    });

  const artifactFigure = (artifact, options = {}) => {
    const tier = artifact.presentation_tier || artifact.role || 'review';
    const diagnostic = /diagnostic|archive/.test(tier) || artifact.default_visibility === 'hidden';
    const classes = ['project-artifact', `project-artifact--${escapeHTML(tier)}`];
    if (options.large) classes.push('project-artifact--large');
    const figure = `
      <figure class="${classes.join(' ')}" data-artifact-id="${escapeHTML(artifact.id)}" data-artifact-role="${escapeHTML(artifact.role)}">
        <img src="${escapeHTML(artifact.src)}" alt="${escapeHTML(options.alt || `${artifact.direction || 'XJ01'} ${artifact.role}`)}" loading="${options.eager ? 'eager' : 'lazy'}" decoding="async">
        <figcaption>
          <span>${escapeHTML(artifact.direction || artifact.evidence_level || 'XJ01')}</span>
          <strong>${escapeHTML(options.label || artifact.id)}</strong>
          ${artifact.status ? badge(artifact.status, artifact.status) : ''}
        </figcaption>
      </figure>`;
    return diagnostic
      ? `<details class="project-diagnostic"><summary>诊断 / 历史证据：${escapeHTML(options.label || artifact.id)}</summary>${figure}</details>`
      : figure;
  };

  const sectionShell = (cap, body, extra = '') => `
    <section class="project-capability project-capability--${escapeHTML(cap.type)} ${extra}" id="cap-${escapeHTML(cap.id)}" data-capability="${escapeHTML(cap.id)}">
      <div class="project-capability__meta">
        <span>${escapeHTML(cap.type.toUpperCase())}</span>
        ${badge(cap.status, cap.status)}
      </div>
      ${body}
    </section>`;

  const renderOpening = (data, cap) => {
    const d02 = data.directions.find((d) => d.id === 'D02');
    const d03 = data.directions.find((d) => d.id === 'D03');
    const whole = data.artifacts.filter((a) => /^A1-WHOLE-/.test(a.id));
    return sectionShell(cap, `
      <div class="project-opening-copy">
        <p class="eyebrow">INTERNAL REVIEW / ${escapeHTML(data.project.current_stage)}</p>
        <h1>${escapeHTML(data.project.title)}</h1>
        <p class="project-opening-question">${escapeHTML(data.project.design_question)}</p>
        <div class="project-opening-status">
          ${badge(data.status.project, `PROJECT / ${data.status.project}`)}
          ${badge(data.status.visual_evidence, `VISUAL / ${data.status.visual_evidence}`)}
          ${badge(data.status.physical_cmf, `PHYSICAL / ${data.status.physical_cmf}`)}
        </div>
      </div>
      <div class="project-opening-pair">
        ${whole.map((a, index) => artifactFigure(a, {large:true, eager:index === 0, label:`${a.direction} / Whole Product`})).join('')}
      </div>
      <div class="project-direction-strip">
        <div><span>D02</span><strong>${escapeHTML(d02?.name || '')}</strong><small>${escapeHTML(d02?.open_risks?.[0] || '')}</small></div>
        <div><span>D03</span><strong>${escapeHTML(d03?.name || '')}</strong><small>${escapeHTML(d03?.open_risks?.[0] || '')}</small></div>
      </div>
    `, 'project-capability--opening');
  };

  const renderQuestion = (data, cap) => sectionShell(cap, `
    <div class="project-statement">
      <p class="eyebrow">DESIGN QUESTION</p>
      <h2>${escapeHTML(data.project.design_question)}</h2>
      <div class="project-tension-list">
        ${data.project.core_tensions.map((item) => `<span>${escapeHTML(item)}</span>`).join('')}
      </div>
    </div>
  `);

  const renderDirections = (data, cap) => {
    const candidates = data.directions.filter((d) => ['D02','D03'].includes(d.id));
    const whole = data.artifacts.filter((a) => /^A1-WHOLE-/.test(a.id));
    return sectionShell(cap, `
      <header class="project-section-heading"><span>PRIMARY CANDIDATES</span><h2>方向必须在同一问题、同一观察条件下竞争。</h2></header>
      <div class="project-comparison-grid">
        ${candidates.map((direction) => {
          const art = whole.find((a) => a.direction === direction.id);
          return `<article class="project-direction-card">
            ${art ? artifactFigure(art, {label:`${direction.id} / ${direction.name}`}) : ''}
            <div class="project-direction-card__copy">
              <div><strong>${escapeHTML(direction.id)}</strong><span>${escapeHTML(direction.name)}</span></div>
              <p>${escapeHTML(direction.material_grammar?.pp || '')}</p>
              <ul>${direction.open_risks.map((risk) => `<li>${escapeHTML(risk)}</li>`).join('')}</ul>
            </div>
          </article>`;
        }).join('')}
      </div>
      <p class="project-boundary">NO WINNER / 当前综合色为 D2 数字候选，不是实体综合色批准。</p>
    `);
  };

  const renderMaterials = (data, cap) => {
    const mids = data.artifacts.filter((a) => /^A1-MID-/.test(a.id));
    return sectionShell(cap, `
      <header class="project-section-heading"><span>MATERIAL HIERARCHY</span><h2>材料真实性必须服务整机关系，而不是让单个材质“显得复杂”。</h2></header>
      <div class="project-comparison-grid">${mids.map((a) => artifactFigure(a, {label:`${a.direction} / Material Hierarchy`})).join('')}</div>
      <div class="project-material-grid">
        ${data.materials.map((m) => `<article>
          <span>${escapeHTML(m.id)}</span>
          <h3>${escapeHTML(m.name)}</h3>
          <p>${escapeHTML(m.role || '')}</p>
          <small>${escapeHTML(m.surface_intent || '')}</small>
          <div>${badge(m.truth_state || 'U', `TRUTH / ${m.truth_state || 'U'}`)} ${badge(m.process_status || 'UNKNOWN', `PROCESS / ${m.process_status || 'UNKNOWN'}`)}</div>
        </article>`).join('')}
      </div>
    `);
  };

  const renderDetail = (data, cap) => sectionShell(cap, `
    <header class="project-section-heading"><span>INTERFACES</span><h2>接口必须说明材料、结构与操作为什么这样相遇。</h2></header>
    <div class="project-interface-list">
      ${data.interfaces.map((i) => `<article><span>${escapeHTML(i.id)}</span><strong>${escapeHTML(i.name)}</strong>${badge(i.status, i.status)}</article>`).join('')}
    </div>
  `);

  const renderInteraction = (data, cap) => {
    const arts = artifactsFor(data, 'interaction').filter((a) => !/diagnostic/.test(a.presentation_tier || ''));
    return sectionShell(cap, `
      <header class="project-section-heading"><span>INTERACTION REALITY GATE</span><h2>数字可读性已经形成判断；真实湿手、力反馈和换头成功率仍未关闭。</h2></header>
      ${arts.map((a) => artifactFigure(a, {large:true, label:'Operation Context / Digital Evidence'})).join('')}
      <div class="project-decision-list">${data.interaction.decisions.map((d) => `<div><strong>${escapeHTML(d.target)}</strong><span>${escapeHTML(d.decision)}</span></div>`).join('')}</div>
      <div class="project-open-gate"><strong>P1 READY_NOT_EXECUTED</strong><ul>${data.interaction.physical_open.map((v) => `<li>${escapeHTML(v)}</li>`).join('')}</ul></div>
    `);
  };

  const renderEnvironment = (data, cap) => sectionShell(cap, `
    <header class="project-section-heading"><span>VE06 / ENVIRONMENT ADAPTATION</span><h2>缺失的环境证据直接显示为 OPEN；不使用氛围图代替验证。</h2></header>
    <div class="project-state-grid">
      ${data.environment.contexts.map((ctx) => `<article>
        <span>${escapeHTML(ctx.id)}</span><h3>${escapeHTML(ctx.name)}</h3><p>${escapeHTML(ctx.purpose)}</p>${badge(ctx.status, ctx.status)}
      </article>`).join('')}
    </div>
  `);

  const renderLifecycle = (data, cap) => {
    const proxies = artifactsFor(data, 'lifecycle');
    return sectionShell(cap, `
      <header class="project-section-heading"><span>VE07 / LIFECYCLE REALISM</span><h2>研究攻击逻辑保留，但旧程序化图像不能冒充专业最终视觉。</h2></header>
      <div class="project-state-grid">
        <article><span>D02</span><h3>${escapeHTML(data.lifecycle.direction_cautions.D02)}</h3><p>需通过真实 PU 邻接与老化样板关闭。</p></article>
        <article><span>D03</span><h3>${escapeHTML(data.lifecycle.direction_cautions.D03)}</h3><p>需通过 wet / dirty-wiped 实体与更真实数字状态关闭。</p></article>
      </div>
      ${proxies.map((a) => artifactFigure(a, {label:'06D / Research Proxy'})).join('')}
    `);
  };

  const renderEvidence = (data, cap) => sectionShell(cap, `
    <header class="project-section-heading"><span>TRUTH / EVIDENCE REGISTER</span><h2>展示层必须保留事实、观察、判断、假设与未知之间的边界。</h2></header>
    <div class="project-evidence-list">
      ${data.evidence.map((e) => `<article>
        <div>${badge(e.truth_state, e.truth_state)} ${e.level ? badge(e.level, e.level) : ''}</div>
        <h3>${escapeHTML(e.subject)}</h3><p>${escapeHTML(e.statement)}</p><small>${escapeHTML(e.status)}</small>
      </article>`).join('')}
    </div>
  `);

  const renderSpecification = (data, cap) => sectionShell(cap, `
    <header class="project-section-heading"><span>SPEC / HANDOFF</span><h2>综合色、finish 和 sample plan 已有设计级结构，但还不能称为工程批准。</h2></header>
    <div class="project-spec-grid">
      <article><span>D02</span><h3>${escapeHTML(data.directions.find((d) => d.id === 'D02')?.name || '')}</h3>
        <p>${escapeHTML(data.specifications.D02.finish)}</p><small>${escapeHTML(data.specifications.D02.main_physical_risk)}</small></article>
      <article><span>D03</span><h3>${escapeHTML(data.directions.find((d) => d.id === 'D03')?.name || '')}</h3>
        <p>${escapeHTML(data.specifications.D03.finish)}</p><small>${escapeHTML(data.specifications.D03.main_physical_risk)}</small></article>
    </div>
    <div class="project-promotion-gate">
      <strong>Promotion blockers</strong>
      <ul>${data.status.promotion_blockers.map((v) => `<li>${escapeHTML(v)}</li>`).join('')}</ul>
    </div>
  `);

  const renderFallback = (data, cap) => sectionShell(cap, `
    <header class="project-section-heading"><span>${escapeHTML(cap.type)}</span><h2>${escapeHTML(cap.id)}</h2></header>
    <p>${escapeHTML((cap.questions || []).join(' / '))}</p>
  `);

  const renderers = {
    identity: renderOpening,
    question: renderQuestion,
    direction: renderDirections,
    material: renderMaterials,
    detail: renderDetail,
    interaction: renderInteraction,
    context: renderEnvironment,
    lifecycle: renderLifecycle,
    evidence: renderEvidence,
    specification: renderSpecification
  };

  function validateCapabilities(data) {
    const have = new Set(data.capabilities.map((cap) => cap.id));
    const minimum = data.display.minimum_capabilities || [];
    const missing = minimum.filter((id) => !have.has(id));
    return { minimum, missing };
  }

  function buildPlan(data) {
    const byId = new Map(data.capabilities.map((cap) => [cap.id, cap]));
    const planned = [...(data.display.plan || [])]
      .sort((a, b) => (b.priority || 0) - (a.priority || 0))
      .map((entry) => byId.get(entry.capability_id))
      .filter(Boolean);

    const used = new Set(planned.map((cap) => cap.id));
    const requiredExtras = data.capabilities.filter((cap) =>
      !used.has(cap.id) &&
      (cap.priority === 'required' || cap.priority === 'required_for_professional_handoff')
    );
    return [...planned, ...requiredExtras];
  }

  async function init() {
    const source = registry[projectId];
    if (!source) throw new Error(`Unknown project: ${projectId}`);
    const response = await fetch(source, { cache: 'no-store' });
    if (!response.ok) throw new Error(`Project data failed: ${response.status}`);
    const data = await response.json();

    document.title = `OLEANDER｜${data.project.title}`;
    document.documentElement.dataset.projectDisplay = 'loading';

    const validation = validateCapabilities(data);
    const plan = buildPlan(data);
    root.innerHTML = `
      ${validation.missing.length ? `<div class="project-schema-warning">Missing minimum capabilities: ${validation.missing.map(escapeHTML).join(', ')}</div>` : ''}
      <div class="project-release-boundary">${badge(data.release_state, data.release_state)} <span>此实例用于内部设计评审；未关闭的证据不会被视觉包装成完成项。</span></div>
      ${plan.map((cap) => {
        const renderer = renderers[cap.type] || renderFallback;
        return renderer(data, cap);
      }).join('')}
    `;

    document.documentElement.dataset.projectDisplay = 'ready';
    root.focus({ preventScroll: true });
  }

  init().catch((error) => {
    console.error(error);
    root.innerHTML = `<div class="project-schema-warning"><strong>Project display failed.</strong><p>${escapeHTML(error.message)}</p></div>`;
    document.documentElement.dataset.projectDisplay = 'error';
  });
})();