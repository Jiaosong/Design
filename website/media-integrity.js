(() => {
  'use strict';

  const boardImages = [...document.querySelectorAll('.daylily-detail figure img, .reno-detail figure img, .expression-encounter figure img')];
  if (!boardImages.length) return;

  const viewer = document.createElement('div');
  viewer.className = 'work-viewer';
  viewer.hidden = true;
  viewer.setAttribute('role', 'dialog');
  viewer.setAttribute('aria-modal', 'true');
  viewer.setAttribute('aria-labelledby', 'work-viewer-title');
  viewer.innerHTML = `
    <h2 id="work-viewer-title" class="visually-hidden">作品大图查看</h2>
    <div class="work-viewer__bar">
      <button class="work-viewer__close" type="button" aria-label="关闭作品大图">关闭 / ESC</button>
    </div>
    <div class="work-viewer__stage">
      <img alt="" />
    </div>
    <p class="work-viewer__caption"></p>`;
  document.body.appendChild(viewer);

  const closeButton = viewer.querySelector('.work-viewer__close');
  const viewerImage = viewer.querySelector('.work-viewer__stage img');
  const viewerCaption = viewer.querySelector('.work-viewer__caption');
  let returnFocus = null;

  const closeViewer = () => {
    if (viewer.hidden) return;
    viewer.hidden = true;
    viewerImage.removeAttribute('src');
    document.body.classList.remove('is-viewing-work');
    returnFocus?.focus?.();
  };

  const openViewer = (source) => {
    returnFocus = source;
    viewerImage.src = source.currentSrc || source.src;
    viewerImage.alt = source.alt || '作品大图';
    const figure = source.closest('figure');
    const caption = figure?.querySelector('figcaption')?.textContent?.trim();
    viewerCaption.textContent = caption || source.alt || '';
    viewer.hidden = false;
    document.body.classList.add('is-viewing-work');
    closeButton.focus();
  };

  boardImages.forEach((image) => {
    image.classList.add('work-board-image');
    image.closest('figure')?.classList.add('work-board');
    image.setAttribute('tabindex', '0');
    image.setAttribute('role', 'button');
    image.setAttribute('aria-label', `${image.alt || '作品图'}。打开大图查看。`);
    image.draggable = false;

    image.addEventListener('click', () => openViewer(image));
    image.addEventListener('keydown', (event) => {
      if (event.key !== 'Enter' && event.key !== ' ') return;
      event.preventDefault();
      openViewer(image);
    });
  });

  closeButton.addEventListener('click', closeViewer);
  viewer.addEventListener('click', (event) => {
    if (event.target === viewer) closeViewer();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !viewer.hidden) {
      event.preventDefault();
      closeViewer();
    }
  });
})();