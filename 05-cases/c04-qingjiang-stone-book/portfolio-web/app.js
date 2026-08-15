(() => {
  const loadStyle = (href, authority) => {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = href;
    if (authority) link.dataset.authority = authority;
    document.head.appendChild(link);
  };
  loadStyle('authority-tokens.css', 'QJ-D-DUAL-QUALITY-GATE-2026-08-15');
  loadStyle('drawing-gallery.css', 'QJ-C22-SPATIAL-DRAWING-v3.0');
  loadStyle('offline-media.css', 'C04-OFFLINE-PRESENTATION-MEDIA-v0.1');

  const data = window.C04_DATA;
  if (!data) return;

  const byId = (id) => document.getElementById(id);
  const routeById = new Map(data.route.map(item => [item.id, item]));
  const navLinks = [...document.querySelectorAll('.site-nav a')];

  const mapImg = document.querySelector('.map-shell img');
  if (mapImg) {
    mapImg.src = 'assets/drawings/01_Macro_Network_Masterplan.svg';
    mapImg.alt = 'QJ-C22 宏观网络总平面：由第一方官方导览关系转译的可编辑远程研究图纸，非测绘';
    mapImg.loading = 'eager';
  }
  const heroMedia = document.querySelector('.hero-media');
  if (heroMedia) heroMedia.setAttribute('aria-label', 'QJ-C22 source-grounded Qingjiang spatial relation field; presentation drawing, not field photograph');
  const heroSource = document.querySelector('.hero-source');
  if (heroSource) heroSource.innerHTML = 'DRAWING · QJ-C22 SOURCE-GROUNDED SPATIAL FIELD<br>Derived from current macro relation authority · not field photography / not survey';

  function setRoute(id) {
    const item = routeById.get(id);
    if (!item) return;
    document.querySelectorAll('[data-route]').forEach(el => el.classList.toggle('active', el.dataset.route === id));
    const idEl = byId('route-id');
    if (!idEl) return;
    idEl.textContent = `${item.id} · ${item.name}`;
    byId('route-title').textContent = item.zh;
    byId('route-note').textContent = item.note;
    byId('route-state').textContent = item.state;
    byId('route-responsibility').textContent = item.responsibility;
    byId('route-evidence').textContent = item.reality;
  }

  document.querySelectorAll('[data-route]').forEach(el => {
    el.addEventListener('mouseenter', () => setRoute(el.dataset.route));
    el.addEventListener('focus', () => setRoute(el.dataset.route));
    el.addEventListener('click', () => setRoute(el.dataset.route));
  });

  const drawingItems = [
    { id:'01', title:'Macro Network Masterplan', zh:'宏观网络总平面', src:'assets/drawings/01_Macro_Network_Masterplan.svg', note:'北岸到达 / 跨江索道 / 南岸多分支网络。关系级总平面，非测绘、非地理定位。' },
    { id:'05', title:'Typical Sections A/B/C', zh:'典型关系剖面', src:'assets/drawings/05_Typical_Sections_A_B_C.svg', note:'SEC-A 跨江交通与观看；SEC-B 坡地步道与恢复边缘；SEC-C 自然收束。除官方索道参数外，不读取非测绘地图尺寸。' }
  ];

  const linkedSection = byId('linked');
  const librarySection = byId('library');
  if (linkedSection && librarySection) {
    const section = document.createElement('section');
    section.className = 'frame drawing-gallery';
    section.id = 'drawings';
    section.innerHTML = `
      <div class="frame-index">02B / CURRENT DRAWING SET</div>
      <header class="section-head">
        <div><div class="eyebrow">QJ-C22 · SOURCE DRAWING LAYER</div><h2>图纸不是<br>后台附件</h2></div>
        <div><p class="lead">当前空间线已经形成可编辑的远程研究图纸包。网页不再重复画一套“更漂亮但更弱”的示意图，而是把<strong>当前 C22 SVG 原图</strong>直接作为作品证据层，与上面的交互关系图互相校验。</p><div class="meta"><span class="meta-tag">SOURCE-GROUNDED</span><span class="meta-tag">PROVISIONAL</span><span class="meta-tag">SCALE NTS</span><span class="meta-tag">FIELD OPEN</span></div></div>
      </header>
      <div class="drawing-stage">
        <figure class="drawing-view" style="margin:0"><img id="drawing-main" src="${drawingItems[0].src}" alt="${drawingItems[0].zh}" loading="lazy"></figure>
        <aside class="drawing-menu" id="drawing-menu">
          ${drawingItems.map((item,i)=>`<button class="drawing-btn${i===0?' active':''}" data-drawing="${i}"><span class="num">${item.id}</span><span><b>${item.zh}</b><span>${item.title}</span></span></button>`).join('')}
          <div class="drawing-caption"><strong id="drawing-caption-title">${drawingItems[0].zh}</strong><span id="drawing-caption-text">${drawingItems[0].note}</span><br><a class="drawing-link" id="drawing-open" href="${drawingItems[0].src}" target="_blank" rel="noopener">OPEN EDITABLE SVG ↗</a></div>
        </aside>
      </div>`;
    librarySection.parentNode.insertBefore(section, librarySection);

    const main = byId('drawing-main');
    const capTitle = byId('drawing-caption-title');
    const capText = byId('drawing-caption-text');
    const open = byId('drawing-open');
    byId('drawing-menu').querySelectorAll('.drawing-btn').forEach(button => {
      button.addEventListener('click', () => {
        const item = drawingItems[Number(button.dataset.drawing)];
        main.src = item.src;
        main.alt = item.zh;
        capTitle.textContent = item.zh;
        capText.textContent = item.note;
        open.href = item.src;
        byId('drawing-menu').querySelectorAll('.drawing-btn').forEach(b => b.classList.toggle('active', b === button));
      });
    });
  }

  const nodeGrid = byId('node-grid');
  let currentFilter = 'all';
  let currentNode = data.nodes[0];
  function nodeMatches(node) {
    if (currentFilter === 'featured') return node.featured;
    if (currentFilter === 'open') return node.level === 'open' || node.level === 'hold';
    return true;
  }
  function showNode(node) {
    currentNode = node;
    byId('node-num').textContent = node.id.replace('R', '');
    byId('node-title').textContent = node.title;
    byId('node-alt').textContent = node.alt || '';
    byId('node-status').textContent = node.status;
    byId('node-role').innerHTML = `<strong>${node.role}</strong>`;
    byId('node-evidence').textContent = node.evidence;
    nodeGrid.querySelectorAll('.node-card').forEach(card => card.classList.toggle('active', card.dataset.id === node.id));
  }
  function renderNodes() {
    nodeGrid.innerHTML = '';
    data.nodes.filter(nodeMatches).forEach(node => {
      const button = document.createElement('button');
      button.className = `node-card${node.featured ? ' featured' : ''}`;
      button.dataset.id = node.id;
      button.innerHTML = `<b>${node.id} · ${node.title}</b><span>${node.status}</span>`;
      button.addEventListener('click', () => showNode(node));
      nodeGrid.appendChild(button);
    });
    const visible = data.nodes.filter(nodeMatches);
    if (!visible.includes(currentNode)) showNode(visible[0] || data.nodes[0]); else showNode(currentNode);
  }
  document.querySelectorAll('.filter-btn').forEach(button => {
    button.addEventListener('click', () => {
      currentFilter = button.dataset.filter;
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.toggle('active', b === button));
      renderNodes();
    });
  });
  renderNodes();

  const blockerBoard = byId('blocker-board');
  data.blockers.forEach((item, index) => {
    const card = document.createElement('article');
    card.className = 'blocker-card';
    card.innerHTML = `<div><div class="blocker-id">${item.id}</div><h4>${item.title}</h4><p>${item.detail}</p></div><div class="blocker-foot">${index === 0 ? 'PRIMARY FIELD BLOCKER' : 'OPEN · NO PROMOTION'}</div>`;
    blockerBoard.appendChild(card);
  });

  const sourceGrid = byId('source-grid');
  data.sources.forEach(source => {
    const card = document.createElement('article');
    card.className = 'source-card';
    card.innerHTML = `<div><div class="source-kind">${source.kind}</div><div class="source-date">${source.date}</div></div><div><h3>${source.title}</h3><p>${source.use}</p><a href="${source.url}" target="_blank" rel="noopener noreferrer">OPEN SOURCE ↗</a></div>`;
    sourceGrid.appendChild(card);
  });

  const motionScreen = byId('motion-screen');
  const motionPlay = byId('motion-play');
  motionPlay.addEventListener('click', () => {
    const playing = motionScreen.classList.toggle('playing');
    motionPlay.textContent = playing ? 'RESET STUDY' : 'PLAY STUDY';
  });

  if ('IntersectionObserver' in window) {
    const sections = [...document.querySelectorAll('[data-nav]')];
    const observer = new IntersectionObserver(entries => {
      const visible = entries.filter(e => e.isIntersecting).sort((a,b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      const index = Number(visible.target.dataset.nav);
      navLinks.forEach((link, i) => link.classList.toggle('active', i === index));
    }, { threshold:[0.35,0.55,0.75] });
    sections.forEach(section => observer.observe(section));
  }

  document.documentElement.dataset.fieldObserved = String(data.meta.fieldObserved);
  document.documentElement.dataset.fieldMeasured = String(data.meta.fieldMeasured);
  document.documentElement.dataset.g1f = data.meta.g1f;
  document.documentElement.dataset.promotion = data.meta.promotion;

  // Export-only mode: isolate the requested section as the only first viewport.
  // This avoids relying on Chrome CLI's long-page scroll position and does not affect normal browsing.
  const captureId = new URLSearchParams(location.search).get('capture');
  if (captureId) {
    document.documentElement.style.scrollBehavior = 'auto';
    document.body.style.overflow = 'hidden';
    const target = byId(captureId);
    if (target) {
      document.querySelectorAll('main > section, main > aside').forEach(el => {
        if (el !== target) el.style.display = 'none';
      });
      target.style.minHeight = '100vh';
      target.style.height = '100vh';
      target.style.overflow = 'hidden';
      target.style.margin = '0';
      window.scrollTo(0, 0);
      document.documentElement.dataset.capture = captureId;
    }
  }
})();