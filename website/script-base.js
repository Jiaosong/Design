(() => {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const header = document.querySelector('[data-header]');
  const menuToggle = document.querySelector('.menu-toggle');
  const siteNav = document.querySelector('.site-nav');

  const onScroll = () => header?.classList.toggle('is-scrolled', window.scrollY > 24);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  const setMenuOpen = (open, restoreFocus = false) => {
    menuToggle?.setAttribute('aria-expanded', String(open));
    siteNav?.classList.toggle('is-open', open);
    if (open) {
      window.requestAnimationFrame(() => siteNav?.querySelector('a')?.focus());
    } else if (restoreFocus) {
      menuToggle?.focus();
    }
  };

  menuToggle?.addEventListener('click', () => {
    const open = menuToggle.getAttribute('aria-expanded') === 'true';
    setMenuOpen(!open);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menuToggle?.getAttribute('aria-expanded') === 'true') {
      event.preventDefault();
      setMenuOpen(false, true);
    }
  });

  siteNav?.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      setMenuOpen(false);
    });
  });

  const revealItems = document.querySelectorAll('.reveal');
  if (prefersReducedMotion || !('IntersectionObserver' in window)) {
    revealItems.forEach((item) => item.classList.add('is-visible'));
  } else {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    revealItems.forEach((item) => revealObserver.observe(item));
  }

  const sectionLinks = [...document.querySelectorAll('.site-nav a')];
  const observedSections = sectionLinks
    .map((link) => document.querySelector(link.getAttribute('href')))
    .filter(Boolean);
  if ('IntersectionObserver' in window) {
    const navObserver = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      sectionLinks.forEach((link) => {
        const current = link.getAttribute('href') === `#${visible.target.id}`;
        link.classList.toggle('is-current', current);
        if (current) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }, { threshold: [0.16, 0.32, 0.52], rootMargin: '-18% 0px -58% 0px' });
    observedSections.forEach((section) => navObserver.observe(section));
  }

  const bindTabKeyboard = (tabs, activate) => {
    const items = [...tabs];
    items.forEach((tab, index) => {
      tab.addEventListener('keydown', (event) => {
        let nextIndex = index;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') nextIndex = (index + 1) % items.length;
        else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') nextIndex = (index - 1 + items.length) % items.length;
        else if (event.key === 'Home') nextIndex = 0;
        else if (event.key === 'End') nextIndex = items.length - 1;
        else return;
        event.preventDefault();
        items[nextIndex].focus();
        activate(items[nextIndex]);
      });
    });
  };

  const relationData = {
    culture: {
      number: 'RELATION / 01', count: '2 PROJECTS', source: 'CULTURE', target: 'EXPERIENCE',
      question: '文化如何从被识别，逐渐走向被理解、使用与参与？',
      description: '关注品牌、信息、材料与空间如何共同组织公众进入文化内容的路径。',
      projects: [['C01', '一脉广渡', '#project-weaving'], ['Research', '文化参与中的所有权', '#projects']]
    },
    memory: {
      number: 'RELATION / 02', count: '1 PROJECT', source: 'MEMORY', target: 'PLACE',
      question: '场所如何承载没有被正式记录、却持续影响日常的记忆？',
      description: '关注材料痕迹、行动路径与地方叙事如何共同形成空间理解。',
      projects: [['C02', '地方记忆空间叙事', '#projects']]
    },
    symbol: {
      number: 'RELATION / 03', count: '1 EXPERIMENT', source: 'SYMBOL', target: 'BEHAVIOR',
      question: '一个公共符号如何通过方向、位置与反馈影响人的选择？',
      description: '关注视觉信息不是如何被观看，而是如何进入移动、停留与行动。',
      projects: [['C03', '公共符号与行为实验', '#projects']]
    },
    local: {
      number: 'RELATION / 04', count: '2 RECORDS', source: 'LOCAL', target: 'PUBLIC',
      question: '地方经验如何进入公共叙事，同时保留来源、差异与解释权？',
      description: '关注文化贡献者、运营者与公众之间如何共享内容、决策和长期维护。',
      projects: [['Research', '公共文化参与中的所有权问题', '#projects'], ['C01', '一脉广渡', '#project-weaving']]
    },
    tradition: {
      number: 'RELATION / 05', count: '1 CORE PROJECT', source: 'TRADITION', target: 'CONTEMPORARY LIFE',
      question: '传统如何进入当代生活，而不被压缩成一种表面风格？',
      description: '关注制作结构、真实使用与当代体验之间的新连接条件。',
      projects: [['C01', '一脉广渡', '#project-weaving']]
    }
  };

  const relationButtons = document.querySelectorAll('.relation-option');
  const relationEls = {
    number: document.querySelector('#relation-number'),
    count: document.querySelector('#relation-count'),
    source: document.querySelector('#relation-source'),
    target: document.querySelector('#relation-target'),
    question: document.querySelector('#relation-question'),
    description: document.querySelector('#relation-description'),
    projects: document.querySelector('#relation-projects')
  };

  relationButtons.forEach((button) => {
    button.addEventListener('click', () => {
      relationButtons.forEach((item) => {
        const active = item === button;
        item.classList.toggle('is-active', active);
        item.setAttribute('aria-pressed', String(active));
      });
      const data = relationData[button.dataset.relation];
      if (!data) return;
      Object.entries(relationEls).forEach(([key, element]) => {
        if (!element || key === 'projects') return;
        element.textContent = data[key];
      });
      relationEls.projects.innerHTML = data.projects.map(([type, title, href]) => `<a href="${href}"><span>${type}</span>${title}</a>`).join('');
    });
  });

  const modeButtons = document.querySelectorAll('[data-project-mode]');
  const modePanels = document.querySelectorAll('[data-mode-panel]');
  const setProjectMode = (button) => {
    const mode = button.dataset.projectMode;
    modeButtons.forEach((item) => {
      const active = item === button;
      item.classList.toggle('is-active', active);
      item.setAttribute('aria-selected', String(active));
      item.tabIndex = active ? 0 : -1;
    });
    modePanels.forEach((panel) => {
      const active = panel.dataset.modePanel === mode;
      panel.hidden = !active;
      panel.classList.toggle('is-active', active);
    });
  };
  modeButtons.forEach((button) => {
    button.addEventListener('click', () => setProjectMode(button));
  });
  bindTabKeyboard(modeButtons, setProjectMode);

  const practiceData = {
    read: { code: '01 / READ', title: '关系阅读', question: '设计对象原本处于怎样的关系中？', description: '从场景、材料、行为与相关者开始，理解对象如何形成、被使用和进入共同记忆。', methods: '现场观察 / 相关者访谈 / 材料分析 / 使用路径记录', outputs: '语境地图 / 关系地图 / 来源记录 / 研究边界', evidence: '<a href="#context">织造项目：材料、制作、使用与记忆链</a>' },
    frame: { code: '02 / FRAME', title: '问题定义', question: '哪一段关系真正需要设计介入？', description: '从表面需求继续追问：什么仍然存在、什么改变了、谁受到影响，以及设计能改变什么。', methods: '断点图 / 相关者地图 / 命题写作 / 设计介入范围', outputs: '核心命题 / 主要断点 / 成功标准 / 不解决事项', evidence: '<a href="#break">织造项目：对象仍在，关系先断裂</a>' },
    translate: { code: '03 / TRANSLATE', title: '结构转译', question: '如何保留来源逻辑，而不复制表面形式？', description: '从表面进入结构、动作和关系，再把研究发现转化为可以跨媒介工作的规则。', methods: '来源分层 / 结构提取 / 转译矩阵 / 文化边界检查', outputs: '转译原则 / 设计规则 / 视觉与空间语法 / 被拒绝方向', evidence: '<a href="#translation">织造项目：交错、重复与张力</a>' },
    form: { code: '04 / FORM', title: '体验生成', question: '规则如何进入真实触点和行为？', description: '不按媒介罗列成果，而按看见、理解、使用、参与和延续组织体验路径。', methods: '体验地图 / 触点生态 / 叙事序列 / 原型', outputs: '识别系统 / 空间叙事 / 互动序列 / 延续机制', evidence: '<a href="#experience">织造项目：从识别到延续</a>' },
    test: { code: '05 / TEST', title: '证据检查', question: '新的关系是否真的发生？', description: '检查理解、行为、参与和运营，不把完成形式或满意度自动视为关系变化。', methods: '任务测试 / 理解访谈 / 行为观察 / 相关者评审', outputs: '结果记录 / 失败记录 / 迭代决定 / 未来验证', evidence: '<a href="#change">织造项目：测试计划、推断与未知</a>' },
    continue: { code: '06 / CONTINUE', title: '系统延续', question: '谁能在项目结束后继续使用、维护和修正它？', description: '定义内容如何进入、谁拥有修改权、系统如何扩展，以及错误与贡献如何被处理。', methods: '治理地图 / 模板设计 / 维护计划 / 版本记录', outputs: '设计指南 / 内容模板 / 运营规则 / ODL Change Log', evidence: '<a href="#reflection">织造项目：责任、边界与下一问题</a>' }
  };
  const practiceSteps = document.querySelectorAll('.practice-step');
  const practiceEls = {
    code: document.querySelector('#practice-code'), title: document.querySelector('#practice-title'), question: document.querySelector('#practice-question'), description: document.querySelector('#practice-description'), data: document.querySelector('#practice-data')
  };
  const practicePanel = document.querySelector('#practice-panel');
  const setPracticeStep = (step) => {
    practiceSteps.forEach((item) => {
      const active = item === step;
      item.classList.toggle('is-active', active);
      item.setAttribute('aria-selected', String(active));
      item.tabIndex = active ? 0 : -1;
    });
    practicePanel?.setAttribute('aria-labelledby', step.id);
    const data = practiceData[step.dataset.practiceStep];
    practiceEls.code.textContent = data.code;
    practiceEls.title.textContent = data.title;
    practiceEls.question.textContent = data.question;
    practiceEls.description.textContent = data.description;
    practiceEls.data.innerHTML = `<div><dt>Methods</dt><dd>${data.methods}</dd></div><div><dt>Outputs</dt><dd>${data.outputs}</dd></div><div><dt>Project Evidence</dt><dd>${data.evidence}</dd></div>`;
  };
  practiceSteps.forEach((step) => {
    step.addEventListener('click', () => setPracticeStep(step));
  });
  bindTabKeyboard(practiceSteps, setPracticeStep);

  const form = document.querySelector('#relationship-form');
  if (!form) return;
  const steps = [...form.querySelectorAll('[data-form-step]')];
  const navItems = [...document.querySelectorAll('[data-contact-nav]')];
  const summary = form.querySelector('[data-contact-summary]');
  const success = form.querySelector('[data-form-success]');
  let currentStep = 1;
  const draftKey = 'oleanderRelationshipDraft';

  const setStep = (number) => {
    currentStep = Math.max(1, Math.min(5, number));
    steps.forEach((step) => {
      const active = Number(step.dataset.formStep) === currentStep;
      step.hidden = !active;
      step.classList.toggle('is-active', active);
    });
    navItems.forEach((item) => {
      const stepNumber = Number(item.dataset.contactNav);
      item.classList.toggle('is-active', stepNumber === currentStep);
      item.classList.toggle('is-complete', stepNumber < currentStep);
    });
    const activeHeading = steps[currentStep - 1]?.querySelector('h3');
    if (activeHeading && !prefersReducedMotion) activeHeading.scrollIntoView({ behavior: 'smooth', block: 'center' });
    updateSummary();
  };

  const getValue = (name) => {
    const field = form.elements[name];
    if (!field) return '';
    if (field instanceof RadioNodeList) return field.value || '';
    return field.value || '';
  };

  const setFieldError = (name, invalid) => {
    const error = form.querySelector(`[data-error-for="${name}"]`);
    if (error) error.hidden = !invalid;
    form.querySelectorAll(`[name="${CSS.escape(name)}"]`).forEach((control) => {
      if (invalid) control.setAttribute('aria-invalid', 'true');
      else control.removeAttribute('aria-invalid');
    });
  };

  const validateStep = (number) => {
    let valid = true;
    if (number === 1) {
      valid = Boolean(getValue('purpose'));
      setFieldError('purpose', !valid);
    }
    if (number === 2) {
      valid = getValue('object').trim().length >= 8;
      setFieldError('object', !valid);
    }
    if (number === 5) {
      const nameValid = getValue('name').trim().length > 1;
      const email = getValue('email').trim();
      const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
      setFieldError('name', !nameValid);
      setFieldError('email', !emailValid);
      valid = nameValid && emailValid;
    }
    return valid;
  };

  const focusFirstInvalid = () => {
    form.querySelector('[aria-invalid="true"]')?.focus();
  };

  const getCheckedValues = (name) => [...form.querySelectorAll(`input[name="${name}"]:checked`)].map((input) => input.value);

  const updateSummary = () => {
    if (!summary) return;
    const purpose = getValue('purpose') || '尚未选择';
    const object = getValue('object').trim() || '尚未填写';
    const relations = getCheckedValues('relations').join('、') || getValue('break').trim() || '尚未说明';
    const stage = getValue('stage') || '尚不确定';
    summary.innerHTML = `<span>YOUR RELATION NOTE</span><dl><div><dt>Purpose</dt><dd>${escapeHtml(purpose)}</dd></div><div><dt>Object</dt><dd>${escapeHtml(object)}</dd></div><div><dt>Relation</dt><dd>${escapeHtml(relations)}</dd></div><div><dt>Stage</dt><dd>${escapeHtml(stage)}</dd></div></dl>`;
  };

  const serializeForm = () => {
    const data = {};
    new FormData(form).forEach((value, key) => {
      if (data[key]) data[key] = [].concat(data[key], value);
      else data[key] = value;
    });
    return data;
  };

  const saveDraft = () => {
    try { localStorage.setItem(draftKey, JSON.stringify(serializeForm())); } catch (_) { /* localStorage unavailable */ }
  };

  const restoreDraft = () => {
    try {
      const saved = JSON.parse(localStorage.getItem(draftKey) || 'null');
      if (!saved) return;
      Object.entries(saved).forEach(([name, value]) => {
        const values = Array.isArray(value) ? value : [value];
        const controls = [...form.querySelectorAll(`[name="${CSS.escape(name)}"]`)];
        controls.forEach((control) => {
          if (control.type === 'radio' || control.type === 'checkbox') control.checked = values.includes(control.value);
          else control.value = values[0] || '';
        });
      });
      updateSummary();
    } catch (_) { /* ignore invalid draft */ }
  };

  const escapeHtml = (value) => String(value).replace(/[&<>'"]/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[char]));

  const clearResolvedError = (target) => {
    if (!target?.name) return;
    if (target.name === 'purpose' && getValue('purpose')) setFieldError('purpose', false);
    if (target.name === 'object' && getValue('object').trim().length >= 8) setFieldError('object', false);
    if (target.name === 'name' && getValue('name').trim().length > 1) setFieldError('name', false);
    if (target.name === 'email' && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(getValue('email').trim())) setFieldError('email', false);
  };

  form.addEventListener('input', (event) => { clearResolvedError(event.target); updateSummary(); saveDraft(); });
  form.addEventListener('change', (event) => { clearResolvedError(event.target); updateSummary(); saveDraft(); });

  form.querySelectorAll('[data-next-step]').forEach((button) => button.addEventListener('click', () => {
    if (validateStep(currentStep)) setStep(currentStep + 1);
    else focusFirstInvalid();
  }));
  form.querySelectorAll('[data-prev-step]').forEach((button) => button.addEventListener('click', () => setStep(currentStep - 1)));

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!validateStep(5)) {
      focusFirstInvalid();
      return;
    }
    steps.forEach((step) => { step.hidden = true; });
    success.hidden = false;
    try { localStorage.removeItem(draftKey); } catch (_) { /* ignore */ }
    success.focus();
  });

  form.querySelector('[data-reset-form]')?.addEventListener('click', () => {
    form.reset();
    form.querySelectorAll('[aria-invalid="true"]').forEach((control) => control.removeAttribute('aria-invalid'));
    form.querySelectorAll('[data-error-for]').forEach((error) => { error.hidden = true; });
    success.hidden = true;
    steps[0].hidden = false;
    try { localStorage.removeItem(draftKey); } catch (_) { /* ignore */ }
    setStep(1);
  });

  restoreDraft();
  updateSummary();
})();

(() => {
  'use strict';

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(pointer: fine)').matches;

  // A moving highlight makes the paper respond to the reader without replacing the native cursor.
  if (!reduced && finePointer) {
    let frame = 0;
    window.addEventListener('pointermove', (event) => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        document.documentElement.style.setProperty('--pointer-x', `${event.clientX}px`);
        document.documentElement.style.setProperty('--pointer-y', `${event.clientY}px`);
      });
    }, { passive: true });
  }

  const bindTilt = (element, strength = 3.2) => {
    if (!element || reduced || !finePointer) return;
    element.addEventListener('pointermove', (event) => {
      const rect = element.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - 0.5;
      const y = (event.clientY - rect.top) / rect.height - 0.5;
      element.style.setProperty('--paper-tilt-x', `${x * strength}deg`);
      element.style.setProperty('--paper-tilt-y', `${y * -strength}deg`);
    });
    element.addEventListener('pointerleave', () => {
      element.style.setProperty('--paper-tilt-x', '0deg');
      element.style.setProperty('--paper-tilt-y', '0deg');
    });
  };

  const weaveField = document.querySelector('[data-weave-field]');
  const weaveToggle = document.querySelector('[data-weave-toggle]');
  const densityInput = document.querySelector('[data-weave-density]');
  const densityOutput = document.querySelector('[data-weave-density-output]');
  bindTilt(weaveField, 2.2);

  const setDensity = (value) => {
    const numericValue = Math.max(20, Math.min(100, Number(value)));
    const normalized = numericValue / 100;
    weaveField?.style.setProperty('--weave-density', normalized.toFixed(2));
    if (densityOutput) densityOutput.textContent = `${numericValue}%`;
    densityInput?.setAttribute('aria-valuetext', `关系织场密度 ${numericValue}%`);
  };
  if (densityInput) {
    setDensity(densityInput.value);
    densityInput.addEventListener('input', () => setDensity(densityInput.value));
  }
  weaveToggle?.addEventListener('click', () => {
    const woven = !weaveField.classList.contains('is-woven');
    weaveField.classList.toggle('is-woven', woven);
    weaveToggle.setAttribute('aria-pressed', String(woven));
    const strong = weaveToggle.querySelector('strong');
    if (strong) strong.textContent = woven ? '松开织场' : '连接织场';
  });

  // Relationship Reading: Original / Current / Intended states share one stable geometry.
  const readingStates = {
    original: {
      source: '织物', sourceNote: '制作与日常使用', action: '进入', target: '家庭记忆', targetNote: '地方身份与共同经验',
      status: 'ACTIVE / PAST', context: '长期制作、日常使用与家庭生活', evidence: '材料记录 + 制作者陈述',
      implication: '文化意义由持续使用和共同记忆生成。',
      detail: '织物磨损、修补与长期保存痕迹表明，它曾作为生活对象而非展示符号进入家庭。', confidence: 'EVIDENCE / MATERIAL / SOURCE REVIEW', tension: 42
    },
    current: {
      source: '传统纹样', sourceNote: '仍然可以被识别', action: '脱离', target: '制作语境', targetNote: '使用、动作与地方记忆',
      status: 'WEAKENED / CURRENT', context: '文旅传播、完成品展示与快速视觉消费', evidence: '现场观察 + 对照分析',
      implication: '对象仍在，形成对象的关系过程却退到背景。',
      detail: '观察中，访客主要停留在成品与拍照区域；流程说明、工具和使用历史没有形成连续阅读入口。', confidence: 'EVIDENCE / OBSERVED / SOURCE REVIEW', tension: 78
    },
    intended: {
      source: '公众', sourceNote: '观看者与潜在参与者', action: '重新进入', target: '制作关系', targetNote: '材料、动作、使用与共同结果',
      status: 'EMERGING / PROPOSED', context: '品牌、包装、空间与参与式触点', evidence: '测试计划 + 设计假设',
      implication: '设计建立进入过程的条件，而不是声称已经完成文化延续。',
      detail: '计划通过展开、连接和共同生成测试理解路径；测试尚未执行，长期理解与公共参与仍为未知。', confidence: 'EVIDENCE / TEST PLANNED / NOT RUN', tension: 58
    }
  };

  const lab = document.querySelector('[data-reading-lab]');
  const canvas = document.querySelector('[data-reading-canvas]');
  const stateButtons = [...document.querySelectorAll('[data-reading-state]')];
  const tension = document.querySelector('[data-reading-tension]');
  const tensionOutput = document.querySelector('[data-reading-tension-output]');
  const reset = document.querySelector('[data-reading-reset]');
  const evidenceToggle = document.querySelector('[data-reading-evidence-toggle]');
  const evidencePanel = document.querySelector('[data-reading-evidence-panel]');
  let currentReadingState = 'original';

  const readingElements = {
    source: document.querySelector('[data-reading-source]'),
    sourceNote: document.querySelector('[data-reading-source-note]'),
    action: document.querySelector('[data-reading-action]'),
    target: document.querySelector('[data-reading-target]'),
    targetNote: document.querySelector('[data-reading-target-note]'),
    status: document.querySelector('[data-reading-status]'),
    context: document.querySelector('[data-reading-context]'),
    evidence: document.querySelector('[data-reading-evidence]'),
    implication: document.querySelector('[data-reading-implication]'),
    detail: document.querySelector('[data-reading-evidence-detail]'),
    confidence: document.querySelector('[data-reading-confidence]')
  };

  const setTension = (value) => {
    const numericValue = Math.max(0, Math.min(100, Number(value)));
    const normalized = numericValue / 100;
    const shift = Math.round(normalized * 24);
    lab?.style.setProperty('--relation-tension', normalized.toFixed(2));
    lab?.style.setProperty('--source-shift', `${-shift}px`);
    lab?.style.setProperty('--target-shift', `${shift}px`);
    if (tensionOutput) tensionOutput.textContent = `${numericValue}%`;
    tension?.setAttribute('aria-valuetext', `关系张力 ${numericValue}%`);
  };

  const setReadingState = (key, announce = true) => {
    const data = readingStates[key];
    if (!data || !canvas) return;
    currentReadingState = key;
    canvas.dataset.state = key;
    Object.entries(readingElements).forEach(([name, node]) => {
      if (node && data[name] !== undefined) node.textContent = data[name];
    });
    stateButtons.forEach((button) => {
      const active = button.dataset.readingState === key;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-selected', String(active));
      button.tabIndex = active ? 0 : -1;
      if (active) canvas.setAttribute('aria-labelledby', button.id);
    });
    if (tension) tension.value = String(data.tension);
    setTension(data.tension);
    if (announce) {
      canvas.setAttribute('aria-label', `${data.source}通过“${data.action}”连接${data.target}。当前状态：${data.status}。${data.implication}`);
    }
  };

  const activateReadingTab = (button) => setReadingState(button.dataset.readingState);
  stateButtons.forEach((button, index) => {
    button.addEventListener('click', () => activateReadingTab(button));
    button.addEventListener('keydown', (event) => {
      let nextIndex = index;
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') nextIndex = (index + 1) % stateButtons.length;
      else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') nextIndex = (index - 1 + stateButtons.length) % stateButtons.length;
      else if (event.key === 'Home') nextIndex = 0;
      else if (event.key === 'End') nextIndex = stateButtons.length - 1;
      else return;
      event.preventDefault();
      stateButtons[nextIndex].focus();
      activateReadingTab(stateButtons[nextIndex]);
    });
  });
  tension?.addEventListener('input', () => setTension(tension.value));
  reset?.addEventListener('click', () => setReadingState(currentReadingState));
  evidenceToggle?.addEventListener('click', () => {
    const expanded = evidenceToggle.getAttribute('aria-expanded') === 'true';
    evidenceToggle.setAttribute('aria-expanded', String(!expanded));
    evidencePanel.hidden = expanded;
    evidenceToggle.firstChild.textContent = expanded ? '展开证据层 ' : '收起证据层 ';
  });
  document.querySelectorAll('[data-paper-tilt]').forEach((item) => bindTilt(item, 3));
  setReadingState('original', false);

  // Evidence becomes a readable layer instead of a static card.
  const evidenceDetails = [
    {
      label: 'SOURCE TRACE',
      text: '材料表面存在不均匀密度、边缘磨损与修补痕迹；这些信息支持“形式由制作和使用共同生成”的判断。'
    },
    {
      label: 'OBSERVATION LIMIT',
      text: '观察发生在单一展示场景，能够支持入口问题判断，但不能代表所有公众或长期行为。'
    },
    {
      label: 'REVISION LOG',
      text: '判断从“缺少兴趣”修正为“缺少进入过程的路径”，下一轮需要在低解释条件下重新测试。'
    }
  ];
  document.querySelectorAll('.evidence-grid > .evidence-record').forEach((card, index) => {
    if (card.querySelector('.evidence-toggle')) return;
    const detail = evidenceDetails[index];
    if (!detail) return;
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'evidence-toggle';
    button.setAttribute('aria-expanded', 'false');
    button.textContent = '展开证据层 ＋';
    const panel = document.createElement('div');
    panel.className = 'evidence-layer';
    panel.hidden = true;
    panel.innerHTML = `<span class="record-code">${detail.label}</span><p>${detail.text}</p>`;
    button.addEventListener('click', () => {
      const expanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', String(!expanded));
      button.textContent = expanded ? '展开证据层 ＋' : '收起证据层 ×';
      panel.hidden = expanded;
    });
    card.append(button, panel);
  });

  // Translation applications reveal the rule behind the surface.
  const ruleDetails = [
    'RULE / 两个独立方向必须共同完成识别，任一方向都不能单独成为完整标志。',
    'RULE / 打开与折叠必须改变信息关系，而不只是展示隐藏内容。',
    'RULE / 不同路径承担不同理解任务，并在关键位置发生真实交汇。',
    'RULE / 参与者的动作必须改变可见的共同结果，并显示自己的贡献去向。'
  ];
  document.querySelectorAll('.rule-applications article').forEach((card, index) => {
    card.tabIndex = 0;
    card.setAttribute('role', 'button');
    card.setAttribute('aria-pressed', 'false');
    const reveal = document.createElement('div');
    reveal.className = 'rule-reveal';
    reveal.innerHTML = `<div><p>${ruleDetails[index]}</p></div>`;
    card.appendChild(reveal);
    const toggle = () => {
      const active = !card.classList.contains('is-active');
      document.querySelectorAll('.rule-applications article').forEach((other) => {
        other.classList.toggle('is-active', other === card && active);
        other.setAttribute('aria-pressed', String(other === card && active));
      });
    };
    card.addEventListener('click', toggle);
    card.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        toggle();
      }
    });
  });

  // Experience stages show a role transition and touchpoint contract.
  const experienceData = [
    ['STAGE / 01', 'Observer → Reader', '入口不立即给出完整纹样，而以开放交错结构建立继续阅读的动机。', 'TOUCHPOINT / IDENTITY + ENTRANCE'],
    ['STAGE / 02', 'Reader → Interpreter', '材料、动作和来源证据被分层呈现，让图形从风格对象转为生成过程。', 'TOUCHPOINT / INFORMATION + MATERIAL ARCHIVE'],
    ['STAGE / 03', 'Interpreter → User', '包装展开和空间路径让结构进入手部操作与身体移动，而不只停留在说明文字。', 'TOUCHPOINT / PACKAGING + WAYFINDING'],
    ['STAGE / 04', 'User → Participant', '个人选择改变可见结果，系统同时说明这项改变如何进入共同结构。', 'TOUCHPOINT / INTERACTION + WORKSHOP'],
    ['STAGE / 05', 'Participant → Carrier', '可复用物件、内容档案和后续入口把体验带出现场，形成继续阅读的条件。', 'TOUCHPOINT / ARCHIVE + REUSABLE OBJECT']
  ];
  const experienceItems = [...document.querySelectorAll('.experience-path button')];
  const experienceNodes = {
    code: document.querySelector('[data-experience-code]'),
    role: document.querySelector('[data-experience-role]'),
    description: document.querySelector('[data-experience-description]'),
    touchpoint: document.querySelector('[data-experience-touchpoint]')
  };
  const activateExperience = (index) => {
    const data = experienceData[index];
    if (!data) return;
    experienceItems.forEach((item, itemIndex) => {
      const active = itemIndex === index;
      item.classList.toggle('is-active', active);
      item.setAttribute('aria-pressed', String(active));
    });
    experienceNodes.code.textContent = data[0];
    experienceNodes.role.textContent = data[1];
    experienceNodes.description.textContent = data[2];
    experienceNodes.touchpoint.textContent = data[3];
  };
  experienceItems.forEach((item, index) => {
    item.setAttribute('aria-pressed', String(index === 0));
    item.addEventListener('click', () => activateExperience(index));
    item.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        activateExperience(index);
      }
    });
  });
  activateExperience(0);

  // Preserve the existing practice tabs while giving the paper a visible state change.
  const practiceDetail = document.querySelector('.practice-detail');
  document.querySelectorAll('.practice-step').forEach((step) => {
    step.addEventListener('click', () => {
      if (!practiceDetail || reduced) return;
      practiceDetail.classList.remove('is-changing');
      void practiceDetail.offsetWidth;
      practiceDetail.classList.add('is-changing');
    });
  });
})();
