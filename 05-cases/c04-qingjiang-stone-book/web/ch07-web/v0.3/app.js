(() => {
  const surfaces = [...document.querySelectorAll('.surface')];
  const update = () => {
    const y = window.scrollY + window.innerHeight * .35;
    let active = surfaces[0];
    for (const s of surfaces) if (s.offsetTop <= y) active = s;
    document.documentElement.dataset.activeSurface = active?.dataset.surface || '';
  };
  addEventListener('scroll', update, {passive:true}); update();
})();
