(() => {
  'use strict';

  function keyMarkup(type) {
    const columns = type === 'environment'
      ? ['Neutral Studio', 'Soft Interior', 'Wet-zone']
      : ['Day 0', 'Dirty-wiped', 'PU Aged'];
    return `
      <div class="pro04-evidence-map" data-evidence-map="${type}" aria-label="Evidence matrix mapping">
        <div class="pro04-evidence-map__rows"><span>ROWS</span><b>D02 / TOP</b><b>D03 / BOTTOM</b></div>
        <div class="pro04-evidence-map__columns"><span>COLUMNS</span>${columns.map((label) => `<b>${label}</b>`).join('')}</div>
      </div>`;
  }

  function enhance(sectionId, type) {
    const section = document.querySelector(sectionId);
    if (!section || section.querySelector(`[data-evidence-map="${type}"]`)) return;
    const stage = section.querySelector('.pro04-evidence-visual-stage');
    if (!stage) return;
    stage.insertAdjacentHTML('beforebegin', keyMarkup(type));
  }

  function apply() {
    if (document.documentElement.dataset.pro04 !== 'ready') return false;
    enhance('#p04', 'environment');
    enhance('#p05', 'lifecycle');
    return true;
  }

  if (!apply()) {
    const observer = new MutationObserver(() => {
      if (apply()) observer.disconnect();
    });
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-pro04'], childList: true, subtree: true });
  }
})();