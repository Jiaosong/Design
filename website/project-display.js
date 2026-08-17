(() => {
  'use strict';

  const root = document.querySelector('#project-display');
  const params = new URLSearchParams(location.search);
  const registry = { xj01: 'data/projects/xj01.json' };
  const projectId = params.get('project') || 'xj01';

  const esc = (value = '') => String(value).replace(/[&<>"']/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
  }[char]));

  const art = (data, id) => data.artifacts.find((item) => item.id === id);
  const direction = (data, id) => data.directions.find((item) => item.id === id);
  const image = (artifact, alt, className = '') => artifact ? `
    <figure class="pro04-image ${className}" data-artifact-id="${esc(artifact.id)}">
      <img src="${esc(artifact.src)}" alt="${esc(alt)}" loading="lazy" decoding="async">
    </figure>` : '';
  const section = (id, eyebrow, title, body, className = '') => `
    <section id="${id}" class="pro04-section ${className}" data-pro04-section="${id}">
      <header class="pro04-section__header"><span>${esc(eyebrow)}</span><h2>${esc(title)}</h2></header>${body}
    </section>`;
  const swatch = (dir, label) => `
    <div class="pro04-swatch" style="--swatch:${esc(dir.colour.hex)}">
      <span>${esc(dir.id)}</span><strong>${esc(label)}</strong>
      <small>${esc(dir.colour.hex)} · L*${esc(dir.colour.lch_approx?.[0])} · C*${esc(dir.colour.lch_approx?.[1])} · h°${esc(dir.colour.lch_approx?.[2])}</small>
    </div>`;

  function renderHero(data) {
    const d02 = direction(data, 'D02'), d03 = direction(data, 'D03');
    return `<section id="p00" class="pro04-hero" data-pro04-section="p00">
      <div class="pro04-hero__copy">
        <p class="pro04-kicker">XJ01 / CMF DIRECTION STUDY</p>
        <h1>Continuous<br>Material Hierarchy</h1>
        <p class="pro04-hero__lead">Two retained territories. One product architecture. Digital CMF design review — no physical approval claimed.</p>
        <div class="pro04-hero__status"><span>PRO-04.2</span><span>DESIGN REVIEW READY</span><span>NO WINNER</span></div>
      </div>
      <div class="pro04-hero__visuals" style="min-height:0;align-self:center">
        <figure class="pro04-image" data-artifact-id="PRO04-PRESENTATION-HERO" data-evidence-level="D1" style="background:#eceae3">
          <img src="assets/xj01/pro04-hero-directions.jpg" alt="D02 Cool Mineral Air and D03 Quiet Green Mineral presentation comparison" loading="eager" decoding="async" style="width:100%;height:auto;object-fit:contain">
        </figure>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px">
          <div style="border-top:6px solid ${esc(d02.colour.hex)};padding-top:12px"><b style="font:700 .68rem var(--mono)">D02</b><strong style="display:block;margin-top:5px;font:1.05rem var(--serif)">Cool Mineral Air</strong><small style="color:var(--trace);font:.62rem var(--mono)">Lightweight structural cleanliness</small></div>
          <div style="border-top:6px solid ${esc(d03.colour.hex)};padding-top:12px"><b style="font:700 .68rem var(--mono)">D03</b><strong style="display:block;margin-top:5px;font:1.05rem var(--serif)">Quiet Green Mineral</strong><small style="color:var(--trace);font:.62rem var(--mono)">Soft domestic care</small></div>
        </div>
      </div>
      <p class="pro04-boundary">Presentation stimulus / D1 exact-geometry broad preflight. D2 black-field renders remain review evidence and are not promoted to Hero.</p>
    </section>`;
  }

  function renderDirectionDNA(data) {
    const copy = {
      D02:{promise:'Lightweight Structural Cleanliness',perception:'Airy / precise / hygienic',behaviour:'PP stays visually light; Iron reads as structure; PU remains neutral and subordinate.'},
      D03:{promise:'Soft Domestic Care',perception:'Calm / domestic / gentle',behaviour:'PP carries a softer domestic reading; Iron recedes; PU defines the contact terminal.'}
    };
    return section('p01','01 / CMF TERRITORIES','Direction DNA',`
      <p class="pro04-intro">The two directions differ by perception, material behaviour and risk — not hue alone.</p>
      <div class="pro04-territories">${['D02','D03'].map((id)=>{const dir=direction(data,id),c=copy[id];return `<article class="pro04-territory" style="--territory:${esc(dir.colour.hex)}">
        <div class="pro04-territory__visual">${image(art(data,`A1-WHOLE-${id}`),`${id} whole product`,'pro04-image--territory')}</div>
        <div class="pro04-territory__copy"><span>${esc(id)}</span><h3>${esc(dir.name)}</h3><h4>${esc(c.promise)}</h4><dl>
          <div><dt>Perception</dt><dd>${esc(c.perception)}</dd></div>
          <div><dt>Material behaviour</dt><dd>${esc(c.behaviour)}</dd></div>
          <div><dt>Primary risk</dt><dd>${esc(dir.open_risks?.[0]||'')}</dd></div>
        </dl></div></article>`;}).join('')}</div>
      <p class="pro04-decision">D02 + D03 retained. No winner selected in digital review.</p>`,'pro04-section--territories');
  }

  function renderCMFSystem(data) {
    const d02=direction(data,'D02'), d03=direction(data,'D03');
    return section('p02','02 / CMF SYSTEM','Colour × Material × Geometry',`
      <p class="pro04-intro">Colour is evaluated on the real material role and product geometry — never as a detached swatch.</p>
      <div class="pro04-swatches">${swatch(d02,'Cool Mineral Air')}${swatch(d03,'Quiet Green Mineral')}</div>
      <div class="pro04-cmf-visuals"><div>${image(art(data,'A1-MID-D02'),'D02 material hierarchy')}</div><div>${image(art(data,'A1-MID-D03'),'D03 material hierarchy')}</div></div>
      <div class="pro04-material-roles">${data.materials.map((m)=>`<article><span>${esc(m.known_material_class||m.id)}</span><h3>${esc(m.name)}</h3><p>${esc(m.role)}</p><small>${esc(m.surface_intent)}</small></article>`).join('')}</div>
      <p class="pro04-boundary">Colour corridors are digital design targets, not measured production specifications.</p>`);
  }

  function renderInterfaces(data) {
    return section('p03','03 / OPERATION + INTERFACES','Where materials meet',`
      <p class="pro04-intro">Interfaces carry more CMF meaning than isolated surface macros.</p>
      <div class="pro04-interface-layout">
        <div class="pro04-interface-layout__primary">${image(art(data,'06C-OPERATION'),'Operation context digital evidence','pro04-image--operation')}<span>Operation context / D2 digital evidence</span></div>
        <div class="pro04-interface-layout__secondary">${image(art(data,'A1-MID-D02'),'Material interface context')}<p>I01 Iron × PP and I03 PP × PU remain the two critical material readings. The image keeps product context instead of presenting anonymous macro texture.</p></div>
      </div>
      <div class="pro04-interface-list">${data.interfaces.map((i)=>`<article><span>${esc(i.id)}</span><strong>${esc(i.name)}</strong><small>${esc(i.status)}</small></article>`).join('')}</div>`);
  }

  function renderEnvironment(data) {
    const d02=direction(data,'D02'), d03=direction(data,'D03');
    return section('p04','04 / ENVIRONMENT RESPONSE','Reflection Environment Adaptation',`
      <p class="pro04-intro">This is a controlled light-field test, not a claim of full spatial-context validation.</p>
      <div class="pro04-environment-grid">${data.environment.contexts.map((ctx,index)=>`<article class="pro04-env-card pro04-env-card--${index+1}"><span>${esc(ctx.id)}</span><h3>${esc(ctx.name)}</h3><p>${esc(ctx.purpose)}</p><div class="pro04-env-pair"><i style="--chip:${esc(d02.colour.hex)}">D02</i><i style="--chip:${esc(d03.colour.hex)}">D03</i></div><small>${esc(ctx.status)}</small></article>`).join('')}</div>
      <div class="pro04-result"><b>Result</b><p>${esc(data.environment.decision)}</p><small>${esc(data.environment.boundary)}</small></div>`,'pro04-section--environment');
  }

  function renderLifecycle(data) {
    const d02=direction(data,'D02'), d03=direction(data,'D03');
    const rows=[
      {label:'USE',d02:'Stable baseline',d03:'Stable baseline'},
      {label:'WIPE',d02:'Residue kept local',d03:'Clarity risk after dirty-wiped stress'},
      {label:'LONG-TERM',d02:'PU adjacency contrast caution',d03:'PU remains secondary; wet sensitivity remains a caution'}
    ];
    return section('p05','05 / LIFECYCLE','Use → Wipe → Long-term Appearance',`
      <p class="pro04-intro">Lifecycle is shown as a material-risk story, not a dramatic failure simulation.</p>
      <div class="pro04-lifecycle-head"><span></span><b>D02 / ${esc(d02.name)}</b><b>D03 / ${esc(d03.name)}</b></div>
      <div class="pro04-lifecycle-table">${rows.map((r)=>`<div class="pro04-lifecycle-row"><strong>${r.label}</strong><p style="--territory:${esc(d02.colour.hex)}">${esc(r.d02)}</p><p style="--territory:${esc(d03.colour.hex)}">${esc(r.d03)}</p></div>`).join('')}</div>
      <p class="pro04-boundary">Wet, dirty-wiped and ageing states remain D2/H-D2 relative risk evidence. They do not predict real material ageing.</p>
      <details class="pro04-diagnostic"><summary>Show diagnostic lifecycle history</summary>${image(art(data,'06D-LIFECYCLE-PROXY'),'Historical lifecycle diagnostic proxy')}</details>`,'pro04-section--lifecycle');
  }

  function renderAppendix(data) {
    return section('p06','APPENDIX / EVIDENCE BOUNDARY','What this digital CMF study proves',`
      <div class="pro04-proof-summary">
        <article><strong>SUPPORTED</strong><p>Exact geometry, controlled D2 comparisons, direction hierarchy and digital environment/lifecycle risk review.</p></article>
        <article><strong>NOT CLAIMED</strong><p>Measured production colour, supplier/process feasibility, physical ageing, real interaction validation or engineering approval.</p></article>
        <article><strong>CURRENT SCOPE</strong><p>Digital CMF design review + professional presentation. Physical sample route is out of scope by project decision.</p></article>
      </div>
      <details class="pro04-appendix-details"><summary>Evidence register / design-spec boundary</summary><div class="pro04-evidence-list">${data.evidence.map((e)=>`<article><span>${esc(e.truth_state)}${e.level?` · ${esc(e.level)}`:''}</span><h3>${esc(e.subject)}</h3><p>${esc(e.statement)}</p><small>${esc(e.status)}</small></article>`).join('')}</div></details>
      <div class="pro04-hard-boundary">Digital appearance ≠ measured colour ≠ process feasibility ≠ physical ageing ≠ engineering approval.</div>`,'pro04-section--appendix');
  }

  const renderPresentation=(data)=>[renderHero(data),renderDirectionDNA(data),renderCMFSystem(data),renderInterfaces(data),renderEnvironment(data),renderLifecycle(data),renderAppendix(data)].join('');

  async function init(){
    const source=registry[projectId]; if(!source) throw new Error(`Unknown project: ${projectId}`);
    const response=await fetch(source,{cache:'no-store'}); if(!response.ok) throw new Error(`Project data failed: ${response.status}`);
    const data=await response.json(); document.title=`OLEANDER｜${data.project.title}`;
    document.documentElement.dataset.projectDisplay='loading'; document.documentElement.dataset.pro04='loading';
    root.innerHTML=`<div class="project-release-boundary"><span>INTERNAL REVIEW</span><span>${esc(data.project.current_stage)}</span><span>PHYSICAL / OUT OF SCOPE</span></div>${renderPresentation(data)}`;
    document.documentElement.dataset.projectDisplay='ready'; document.documentElement.dataset.pro04='ready'; root.focus({preventScroll:true});
  }

  init().catch((error)=>{console.error(error);root.innerHTML=`<div class="project-schema-warning"><strong>Project display failed.</strong><p>${esc(error.message)}</p></div>`;document.documentElement.dataset.projectDisplay='error';document.documentElement.dataset.pro04='error';});
})();