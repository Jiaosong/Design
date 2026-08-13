(() => {
  const figures = [...document.querySelectorAll('.encounter-work, .daylily-detail figure, .reno-detail figure')].filter((item) => item.querySelector('img'));
  if (!figures.length) return;
  const dialog = document.createElement('dialog');
  dialog.className = 'image-focus-dialog';
  const image = document.createElement('img');
  const caption = document.createElement('p');
  const close = document.createElement('button');
  close.type = 'button';
  close.textContent = '关闭 / ESC';
  dialog.append(image, caption, close);
  document.body.appendChild(dialog);
  const show = (figure) => {
    const source = figure.querySelector('img');
    image.src = source.currentSrc || source.src;
    image.alt = source.alt || '';
    caption.textContent = figure.querySelector('figcaption')?.textContent?.trim() || source.alt || '';
    dialog.showModal();
  };
  close.addEventListener('click', () => dialog.close());
  figures.forEach((figure) => {
    figure.classList.add('image-focusable');
    figure.tabIndex = 0;
    figure.addEventListener('click', (event) => { if (!event.target.closest('a,button')) show(figure); });
    figure.addEventListener('keydown', (event) => { if (event.key === 'Enter') show(figure); });
  });
})();