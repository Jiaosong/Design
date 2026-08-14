(() => {
  'use strict';
  const $ = (selector, root = document) => root.querySelector(selector);

  document.body.classList.add('portfolio-framework-v2');

  if (!document.querySelector('link[data-portfolio-crops]')) {
    const cropStyles = document.createElement('link');
    cropStyles.rel = 'stylesheet';
    cropStyles.href = 'portfolio-crops.css';
    cropStyles.dataset.portfolioCrops = '';
    cropStyles.onload = () => document.documentElement.setAttribute('data-portfolio-crops', 'ready');
    document.head.appendChild(cropStyles);
  }

  const main = $('#main');
  const hero = $('#home');
  const encounter = $('.expression-encounter');
  const projects = $('#projects');
  const c02 = $('#project-daylily');
  const c03 = $('#project-reno-cmf');
  const c01 = $('#project-weaving');
  const question = $('#question');
  const relations = $('#relations');
  const evidence = $('#evidence');
  const practice = $('#practice');
  const about = $('#about');
  const contact = $('#contact');

  if (encounter && !encounter.id) encounter.id = 'selected-work';
  c02?.setAttribute('data-case-role', 'visual-case');
  c03?.setAttribute('data-case-role', 'visual-case');
  c01?.setAttribute('data-case-role', 'research-case');

  const encounterHead = encounter?.querySelector('.expression-encounter__head');
  if (encounterHead) {
    const eyebrow = encounterHead.querySelector('.eyebrow');
    const copy = encounterHead.querySelector('p');
    if (eyebrow) eyebrow.textContent = 'SELECTED WORKS / 01';
    if (copy) copy.textContent = '先由作品建立判断，再进入过程、证据与完整作品板。';
  }

  [
    ['.encounter-work--daylily', '#project-daylily', '进入 Daylily 完整案例'],
    ['.encounter-work--reno', '#project-reno-cmf', '进入 The Light Collection 完整案例']
  ].forEach(([selector, href, label]) => {
    const figure = $(selector, encounter || document);
    const caption = figure?.querySelector('figcaption');
    if (caption && !caption.querySelector('.encounter-case-link')) {
      const link = document.createElement('a');
      link.className = 'encounter-case-link';
      link.href = href;
      link.textContent = `${label} →`;
      caption.appendChild(link);
    }
  });

  const projectHeading = projects?.querySelector('.section-heading');
  if (projectHeading) {
    const eyebrow = projectHeading.querySelector('.eyebrow');
    const title = projectHeading.querySelector('h2');
    const intro = projectHeading.querySelector('.section-intro');
    if (eyebrow) eyebrow.textContent = 'PROJECT INDEX / ARCHIVE';
    if (title) title.innerHTML = '完整案例之后，<br>再回看项目索引。';
    if (intro) intro.textContent = '这里用于按关系、实践与开放档案重新定位项目；它不承担作品集的第一阅读。';
  }

  const projectCoordinate = projects?.querySelector(':scope > .section-coordinate');
  if (projectCoordinate) projectCoordinate.textContent = 'PROJECT INDEX / AFTER WORK';
  const questionCoordinate = question?.querySelector(':scope > .section-coordinate');
  if (questionCoordinate) questionCoordinate.textContent = 'RESEARCH QUESTION / 02';
  const relationCoordinate = relations?.querySelector(':scope > .section-coordinate');
  if (relationCoordinate) relationCoordinate.textContent = 'RELATION READING / 03';
  const evidenceCoordinate = evidence?.querySelector(':scope > .section-coordinate');
  if (evidenceCoordinate) evidenceCoordinate.textContent = 'EVIDENCE / 04';

  const relationPanel = $('#project-panel-relation');
  const modeSwitcher = projects?.querySelector('.mode-switcher');
  if (relationPanel && modeSwitcher) relationPanel.insertAdjacentElement('afterend', modeSwitcher);

  const openingLabels = [
    [c02, 'PROJECT / C02 / BRAND + SPACE'],
    [c03, 'PROJECT / C03 / CMF'],
    [c01, 'RESEARCH CASE / C01']
  ];
  openingLabels.forEach(([caseNode, text]) => {
    const openingCoordinate = caseNode?.querySelector(':scope > header .section-coordinate');
    if (openingCoordinate) openingCoordinate.textContent = text;
  });

  const daylilyLabels = ['01 / CONTEXT', '02 / POSITION', '03 / IDENTITY', '04 / CMF + TOUCHPOINTS', '05 / SPACE + EXPERIENCE'];
  [...(c02?.querySelectorAll('.daylily-chapter') || [])].forEach((chapter, index) => {
    const label = chapter.querySelector('.chapter-coordinate');
    if (label && daylilyLabels[index]) label.textContent = daylilyLabels[index];
  });

  const renoLabels = ['01 / CONTEXT', '02 / CONCEPT', '03 / COLOR', '04 / MATERIAL + FINISH', '05 / SERIES'];
  [...(c03?.querySelectorAll('.reno-chapter') || [])].forEach((chapter, index) => {
    const label = chapter.querySelector('.chapter-coordinate');
    if (label && renoLabels[index]) label.textContent = renoLabels[index];
  });

  if (main && question && !$('.portfolio-research-divider')) {
    const divider = document.createElement('section');
    divider.className = 'portfolio-research-divider section';
    divider.setAttribute('aria-labelledby', 'research-divider-title');
    divider.innerHTML = `
      <div class="section-coordinate">RESEARCH / APPROACH</div>
      <div class="portfolio-research-divider__inner reveal">
        <p class="eyebrow">AFTER THE WORK</p>
        <h2 id="research-divider-title">从结果返回问题、<br>关系与证据。</h2>
        <p>作品先承担判断；研究部分解释这些判断如何形成、被修订，以及哪些结论仍需验证。</p>
      </div>`;
    question.insertAdjacentElement('beforebegin', divider);
  }

  const divider = $('.portfolio-research-divider');
  if (main) {
    [hero, encounter, c02, c03, c01, projects, divider, question, relations, evidence, practice, about, contact]
      .filter(Boolean)
      .forEach((node) => main.appendChild(node));
  }

  const nav = $('#site-nav');
  if (nav) {
    nav.innerHTML = `
      <a href="#selected-work">项目</a>
      <a href="#question">研究</a>
      <a href="#practice">方法</a>
      <a href="#about">关于</a>
      <a href="#contact">联系</a>`;
  }

  const scrollCue = hero?.querySelector('.scroll-cue');
  if (scrollCue) {
    scrollCue.href = '#selected-work';
    scrollCue.innerHTML = '查看作品 <span aria-hidden="true">↓</span>';
  }
})();