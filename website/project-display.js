(() => {
  'use strict';

  const root = document.querySelector('#project-display');
  const params = new URLSearchParams(location.search);
  const registry = { xj01: 'data/projects/xj01.json' };
  const projectId = params.get('project') || 'xj01';

  const esc = (value = '') => String(value).replace(/[&<>"']/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
  }[char]));

  const statusTone = (value = '') => {
    const text = String(value).toUpperCase();
    if (/OUT_OF_SCOPE/.test(text)) return 'neutral';
    if (/(PASS|READY|RETAIN|CLOSED|EXECUTED)/.test(text) && !/(NOT|OPEN|INCOMPLETE)/.test(text)) return 'positive';
    if (/(OPEN|PENDING|NOT_|INCOMPLETE|DRAFT|REBUILD)/.test(text)) return 'open';
    if (/(REJECT|FAIL|BLOCK)/.test(text)) return 'negative';
    return 'neutral';
  };

  const badge = (value, label = value) =>
    `<span class="project-status project-status--${statusTone(value)}">${esc(label)}</span>`;

  const artifactsFor = (data, capabilityId) =>
    data.artifacts.filter((artifact) => {
      const caps = Array.isArray(artifact.capability) ? artifact.capability : [artifact.capability].filter(Boolean);
      return caps.includes(capabilityId) && artifact.web_available;
    });

  const artifactFigure = (artifact, options = {}) => {
    const tier = artifact.presentation_tier || artifact.role || 'review';
    const diagnostic = /diagnostic|archive/.test(tier) || artifact.default_visibility === 'hidden';
    const classes = ['project-artifact', `project-artifact--${esc(tier)}`];
    if (options.large) classes.push('project-artifact--large');
    const figure = `
      <figure class="${classes.join(' ')}" data-artifact-id="${esc(artifact.id)}" data-artifact-role="${esc(artifact.role)}">
        <img src="${esc(artifact.src)}" alt="${esc(options.alt || `${artifact.direction || 'XJ01'} ${artifact.role}`)}"
          loading="${options.eager ? 'eager' : 'lazy'}" decoding="async">
        <figcaption>
          <span>${esc(artifact.direction || artifact.evidence_level || 'XJ01')}</span>
          <strong>${esc(options.label || artifact.id)}</strong>
          ${artifact.status ? badge(artifact.status) : ''}
        </figcaption>
      </figure>`;
    return diagnostic
      ? `<details class="project-diagnostic"><summary>诊断 / 历史证据：${esc(options.label || artifact.id)}</summary>${figure}</details>`
      : figure;
  };

  const shell = (cap, body, extra = '') => `
    <section class="project-capability project-capability--${esc(cap.type)} ${extra}"
      id="cap-${esc(cap.id)}" data-capability="${esc(cap.id)}">
      <div class="project-capability__meta">
        <span>${esc(cap.type.toUpperCase())}</span>${badge(cap.status)}
      </div>
      ${body}
    </section>`;

  const renderOpening = (data, cap) => {
    const whole = data.artifacts.filter((a) => /^A1-WHOLE-/.test(a.id));
    return shell(cap, `
      <div class="project-opening-copy">
        <p class="eyebrow">INTERNAL REVIEW / ${esc(data.project.current_stage)}</p>
        <h1>${esc(data.project.title)}</h1>
        <p class="project-opening-question">${esc(data.project.design_question)}</p>
        <div class="project-opening-status">
          ${badge(data.status.project, `PROJECT / ${data.status.project}`)}
          ${badge(data.status.visual_evidence, `VISUAL / ${data.status.visual_evidence}`)}
          ${badge(data.status.physical_cmf, `PHYSICAL / ${data.status.physical_cmf}`)}
        </div>
      </div>
      <div class="project-opening-pair">
        ${whole.map((a, i) => artifactFigure(a, { large: true, eager: i === 0, label: `${a.direction} / Whole Product` })).join('')}
      </div>
      <p class="project-boundary">D02 + D03 retained / no winner. Digital CMF review only; production colour and process are not claimed.</p>
    `, 'project-capability--opening');
  };

  const renderQuestion = (data, cap) => shell(cap, `
    <div class="project-statement">
      <p class="eyebrow">DESIGN QUESTION</p>
      <h2>${esc(data.project.design_question)}</h2>
      <div class="project-tension-list">${data.project.core_tensions.map((item) => `<span>${esc(item)}</span>`).join('')}</div>
    </div>`);

  const renderDirections = (data, cap) => {
    const candidates = data.directions.filter((d) => ['D02', 'D03'].includes(d.id));
    const whole = data.artifacts.filter((a) => /^A1-WHOLE-/.test(a.id));
    return shell(cap, `
      <header class="project-section-heading"><span>PRIMARY CANDIDATES</span><h2>同一观察条件下比较综合色与材料层级，不用效果补偿方向。</h2></header>
      <div class="project-comparison-grid">
        ${candidates.map((direction) => {
          const art = whole.find((a) => a.direction === direction.id);
          return `<article class="project-direction-card">
            ${art ? artifactFigure(art, { label: `${direction.id} / ${direction.name}` }) : ''}
            <div class="project-direction-card__copy">
              <div><strong>${esc(direction.id)}</strong><span>${esc(direction.name)}</span></div>
              <p>${esc(direction.material_grammar?.pp || '')}</p>
              <ul>${(direction.open_risks || []).map((risk) => `<li>${esc(risk)}</li>`).join('')}</ul>
            </div>
          </article>`;
        }).join('')}
      </div>
      <p class="project-boundary">NO WINNER / D02 与 D03 均为数字设计候选，不是生产综合色批准。</p>
    `);
  };

  const renderMaterials = (data, cap) => {
    const mids = data.artifacts.filter((a) => /^A1-MID-/.test(a.id));
    return shell(cap, `
      <header class="project-section-heading"><span>MATERIAL HIERARCHY</span><h2>PP 建立主体综合色，Iron 提供结构证据，PU 形成接触终端。</h2></header>
      <div class="project-comparison-grid">${mids.map((a) => artifactFigure(a, { label: `${a.direction} / Material Hierarchy` })).join('')}</div>
      <div class="project-material-grid">
        ${data.materials.map((m) => `<article>
          <span>${esc(m.id)}</span><h3>${esc(m.name)}</h3><p>${esc(m.role)}</p>
          <small>${esc(m.surface_intent)}</small>
          <div>${badge(m.truth_state, `TRUTH / ${m.truth_state}`)} ${badge(m.process_status, `PROCESS / ${m.process_status}`)}</div>
        </article>`).join('')}
      </div>`);
  };

  const renderDetail = (data, cap) => shell(cap, `
    <header class="project-section-heading"><span>INTERFACES</span><h2>接口用于验证材料关系与操作层级，不把局部细节做成装饰。</h2></header>
    <div class="project-interface-list">
      ${data.interfaces.map((i) => `<article><span>${esc(i.id)}</span><strong>${esc(i.name)}</strong>${badge(i.status)}</article>`).join('')}
    </div>`);

  const renderInteraction = (data, cap) => {
    const arts = artifactsFor(data, 'interaction').filter((a) => !/diagnostic/.test(a.presentation_tier || ''));
    const physicalOut = data.status.interaction_06c_p1 === 'OUT_OF_SCOPE';
    return shell(cap, `
      <header class="project-section-heading">
        <span>06C / INTERACTION</span>
        <h2>${physicalOut ? '数字 CMF 操作判断已关闭；实体交互已从当前项目范围移除。' : '数字可读性已经形成判断；实体交互仍待验证。'}</h2>
      </header>
      ${arts.map((a) => artifactFigure(a, { large: true, label: 'Operation Context / Digital Evidence' })).join('')}
      <div class="project-decision-list">
        ${data.interaction.decisions.map((d) => `<div><strong>${esc(d.target)}</strong><span>${esc(d.decision)}</span></div>`).join('')}
      </div>
      <div class="project-open-gate">
        <strong>${physicalOut ? 'PHYSICAL INTERACTION / OUT OF SCOPE' : 'PHYSICAL INTERACTION / OPEN'}</strong>
        <p>${esc(data.interaction.scope_note || 'Digital evidence does not equal physical interaction validation.')}</p>
      </div>`);
  };

  const renderEnvironment = (data, cap) => shell(cap, `
    <header class="project-section-heading"><span>VE06 / ENVIRONMENT ADAPTATION</span>
      <h2>三种受控数字环境用于攻击综合色与材料关系；不是氛围图替代验证。</h2>
    </header>
    <div class="project-state-grid">
      ${data.environment.contexts.map((ctx) => `<article>
        <span>${esc(ctx.id)}</span><h3>${esc(ctx.name)}</h3><p>${esc(ctx.purpose)}</p>${badge(ctx.status)}
      </article>`).join('')}
    </div>
    <p class="project-boundary">${esc(data.environment.decision)} ${esc(data.environment.boundary)}</p>`);

  const renderLifecycle = (data, cap) => {
    const proxies = artifactsFor(data, 'lifecycle');
    return shell(cap, `
      <header class="project-section-heading"><span>VE07 / LIFECYCLE STRESS</span>
        <h2>Wet、Dirty-wiped、PU Aged 只作为 H/D2 相对风险构造，不作为材料预测。</h2>
      </header>
      <div class="project-state-grid">
        <article><span>D02</span><h3>${esc(data.lifecycle.direction_cautions.D02)}</h3><p>Retained as relative digital risk evidence.</p></article>
        <article><span>D03</span><h3>${esc(data.lifecycle.direction_cautions.D03)}</h3><p>Retained as relative digital risk evidence.</p></article>
      </div>
      ${proxies.map((a) => artifactFigure(a, { label: 'Lifecycle / Diagnostic History' })).join('')}
      <p class="project-boundary">${esc(data.lifecycle.front_end_policy)}</p>`);
  };

  const renderEvidence = (data, cap) => shell(cap, `
    <header class="project-section-heading"><span>TRUTH / EVIDENCE REGISTER</span><h2>事实、数字观察、判断、假设与范围决定保持分层。</h2></header>
    <div class="project-evidence-list">
      ${data.evidence.map((e) => `<article>
        <div>${badge(e.truth_state)} ${e.level ? badge(e.level) : ''}</div>
        <h3>${esc(e.subject)}</h3><p>${esc(e.statement)}</p><small>${esc(e.status)}</small>
      </article>`).join('')}
    </div>`);

  const renderSpecification = (data, cap) => shell(cap, `
    <header class="project-section-heading"><span>DESIGN SPEC</span>
      <h2>综合色与 finish 记录为数字设计意图；工程、供应商与量产批准不在当前范围。</h2>
    </header>
    <div class="project-spec-grid">
      <article><span>D02</span><h3>${esc(data.directions.find((d) => d.id === 'D02')?.name || '')}</h3>
        <p>${esc(data.specifications.D02.finish)}</p><small>${esc(data.specifications.D02.main_risk)}</small></article>
      <article><span>D03</span><h3>${esc(data.directions.find((d) => d.id === 'D03')?.name || '')}</h3>
        <p>${esc(data.specifications.D03.finish)}</p><small>${esc(data.specifications.D03.main_risk)}</small></article>
    </div>
    <div class="project-promotion-gate">
      <strong>Presentation completion items</strong>
      <ul>${data.status.promotion_blockers.map((v) => `<li>${esc(v)}</li>`).join('')}</ul>
    </div>`);

  const renderFallback = (data, cap) => shell(cap, `
    <header class="project-section-heading"><span>${esc(cap.type)}</span><h2>${esc(cap.id)}</h2></header>
    <p>${esc((cap.questions || []).join(' / '))}</p>`);

  const renderers = {
    identity: renderOpening, question: renderQuestion, direction: renderDirections,
    material: renderMaterials, detail: renderDetail, interaction: renderInteraction,
    context: renderEnvironment, lifecycle: renderLifecycle, evidence: renderEvidence,
    specification: renderSpecification
  };

  function buildPlan(data) {
    const byId = new Map(data.capabilities.map((cap) => [cap.id, cap]));
    const planned = [...(data.display.plan || [])]
      .sort((a, b) => (b.priority || 0) - (a.priority || 0))
      .map((entry) => byId.get(entry.capability_id)).filter(Boolean);
    const used = new Set(planned.map((cap) => cap.id));
    const required = data.capabilities.filter((cap) => !used.has(cap.id) && cap.priority === 'required');
    return [...planned, ...required];
  }

  async function init() {
    const source = registry[projectId];
    if (!source) throw new Error(`Unknown project: ${projectId}`);
    const response = await fetch(source, { cache: 'no-store' });
    if (!response.ok) throw new Error(`Project data failed: ${response.status}`);
    const data = await response.json();

    document.title = `OLEANDER｜${data.project.title}`;
    document.documentElement.dataset.projectDisplay = 'loading';
    const plan = buildPlan(data);
    root.innerHTML = `
      <div class="project-release-boundary">${badge(data.release_state)}
        <span>数字设计评审与展示实例；实体、量产与工程验证不在当前范围。</span>
      </div>
      ${plan.map((cap) => (renderers[cap.type] || renderFallback)(data, cap)).join('')}
    `;
    document.documentElement.dataset.projectDisplay = 'ready';
    root.focus({ preventScroll: true });
  }

  init().catch((error) => {
    console.error(error);
    root.innerHTML = `<div class="project-schema-warning"><strong>Project display failed.</strong><p>${esc(error.message)}</p></div>`;
    document.documentElement.dataset.projectDisplay = 'error';
  });
})();