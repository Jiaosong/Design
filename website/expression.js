(() => {
  'use strict';

  const $ = (selector, root = document) => root.querySelector(selector);

  // Public identity authority: keep the wordmark; hide the provisional symbol.
  const brandMark = $('.brand-mark');
  if (brandMark) brandMark.setAttribute('aria-hidden', 'true');

  // First read is portfolio/research, not governance state.
  const hero = $('#home');
  const coordinate = hero?.querySelector('.section-coordinate');
  if (coordinate) coordinate.textContent = 'PORTFOLIO / RESEARCH INTERFACE / 2026';

  const heroSystem = $('.hero-system');
  if (heroSystem) {
    heroSystem.setAttribute('aria-label', 'OLEANDER 阅读原则');
    heroSystem.innerHTML = [
      '<span><b>READ</b> 大图先建立感知，内容关系随后展开</span>',
      '<span><b>VERIFY</b> 图表、表格与文字只在需要解释和核验时出现</span>'
    ].join('');
  }

  // Replace the decorative weave listener with a semantic 3-state reading.
  const field = $('[data-weave-field]');
  const oldToggle = $('[data-weave-toggle]');
  let toggle = oldToggle;
  if (oldToggle?.parentNode) {
    toggle = oldToggle.cloneNode(true);
    oldToggle.parentNode.replaceChild(toggle, oldToggle);
  }
  const controls = field?.querySelector('.hero-field__controls');
  const meta = toggle?.querySelector('span');
  const label = toggle?.querySelector('strong');
  const note = document.createElement('div');
  note.className = 'field-reading-note';
  note.setAttribute('aria-live', 'polite');
  controls?.appendChild(note);

  const states = [
    ['context', 'FIELD / 01', '阅读断点', '语境先于对象：关系仍然连续，意义来自使用、来源与共同经验。'],
    ['break', 'BREAK / 02', '查看重连', '对象仍可被识别，但来源、动作与真实生活之间出现断裂。'],
    ['reconnect', 'INTERVENTION / 03', '返回语境', '介入不是增加装饰，而是重新建立可进入、可理解、可继续的关系条件。']
  ];
  let stateIndex = 0;
  const renderFieldState = () => {
    const [key, code, next, text] = states[stateIndex];
    if (field) field.dataset.expressionState = key;
    if (meta) meta.textContent = 'RELATIONSHIP READING';
    if (label) label.textContent = next;
    note.innerHTML = `<span>${code}</span><p>${text}</p>`;
    toggle?.setAttribute('aria-pressed', String(key === 'reconnect'));
    toggle?.setAttribute('aria-label', `${code}。${text}。点击进入下一阅读状态。`);
  };
  renderFieldState();
  toggle?.addEventListener('click', () => {
    stateIndex = (stateIndex + 1) % states.length;
    renderFieldState();
  });

  // Visual hierarchy rule: BIG IMAGE > SMALL IMAGE > DIAGRAM > TABLE > TEXT.
  // The first encounter therefore enters immediately after the hero.
  if (hero && $('#question') && !$('.expression-encounter')) {
    const encounter = document.createElement('section');
    encounter.className = 'expression-encounter';
    encounter.setAttribute('aria-labelledby', 'encounter-title');
    encounter.innerHTML = `
      <header class="expression-encounter__head">
        <div>
          <span class="eyebrow">SELECTED WORK / FIRST ENCOUNTER</span>
          <p>先感知作品，再解释关系；先看结果，再进入证据。</p>
        </div>
        <h2 id="encounter-title">作品先发生。<br>解释随后进入。</h2>
      </header>
      <figure class="encounter-hero">
        <img src="assets/daylily/hero.jpg" alt="忘也 Daylily 项目主视觉" loading="eager" decoding="async">
        <figcaption><span>C02</span><strong>忘也 Daylily</strong><small>PROTOTYPED / TEST PLANNED</small></figcaption>
      </figure>
      <div class="encounter-secondary">
        <figure>
          <img src="assets/reno-cmf/cover.jpg" alt="The Light Collection CMF 项目视觉" loading="lazy" decoding="async">
          <figcaption><span>C03</span><strong>The Light Collection</strong><small>VISUALIZED / SAMPLE TEST PENDING</small></figcaption>
        </figure>
        <figure>
          <img src="assets/daylily/material.jpg" alt="Daylily 项目材料研究图" loading="lazy" decoding="async">
          <figcaption><span>MATERIAL</span><strong>材料与感知证据</strong><small>SECONDARY VISUAL</small></figcaption>
        </figure>
      </div>`;
    hero.insertAdjacentElement('afterend', encounter);
  }

  // Engineering grid appears only while the reader is actually reading structure.
  if ('IntersectionObserver' in window) {
    const targets = ['relations', 'practice'].map((id) => document.getElementById(id)).filter(Boolean);
    const visibility = new Map(targets.map((target) => [target, false]));
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => visibility.set(entry.target, entry.isIntersecting));
      document.body.classList.toggle('is-reading-structure', [...visibility.values()].some(Boolean));
    }, { threshold: 0.08, rootMargin: '-12% 0px -12% 0px' });
    targets.forEach((target) => observer.observe(target));
  }
})();
