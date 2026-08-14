(() => {
  'use strict';
  const $ = (selector, root = document) => root.querySelector(selector);

  document.body.classList.add('portfolio-framework-v2');

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

  const projectHeading = projects?.querySelector('.section-heading');
  if (projectHeading) {
    const eyebrow = projectHeading.querySelector('.eyebrow');
    const title = projectHeading.querySelector('h2');
    const intro = projectHeading.querySelector('.section-intro');
    if (eyebrow) eyebrow.textContent = 'SELECTED WORKS';
    if (title) title.innerHTML = '先看作品。<br>判断与证据随后进入。';
    if (intro) intro.textContent = '品牌、空间与 CMF 项目先以真实成果建立第一判断；研究、方法与证据在作品之后展开。';
  }

  const projectCoordinate = projects?.querySelector(':scope > .section-coordinate');
  if (projectCoordinate) projectCoordinate.textContent = 'SELECTED WORKS / 01';
  const questionCoordinate = question?.querySelector(':scope > .section-coordinate');
  if (questionCoordinate) questionCoordinate.textContent = 'RESEARCH QUESTION / 02';
  const relationCoordinate = relations?.querySelector(':scope > .section-coordinate');
  if (relationCoordinate) relationCoordinate.textContent = 'RELATION READING / 03';
  const evidenceCoordinate = evidence?.querySelector(':scope > .section-coordinate');
  if (evidenceCoordinate) evidenceCoordinate.textContent = 'EVIDENCE / 04';

  const relationPanel = $('#project-panel-relation');
  const modeSwitcher = projects?.querySelector('.mode-switcher');
  if (relationPanel && modeSwitcher) relationPanel.insertAdjacentElement('afterend', modeSwitcher);

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
    [hero, encounter, projects, c02, c03, c01, divider, question, relations, evidence, practice, about, contact]
      .filter(Boolean)
      .forEach((node) => main.appendChild(node));
  }

  const nav = $('#site-nav');
  if (nav) {
    nav.innerHTML = `
      <a href="#projects">项目</a>
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