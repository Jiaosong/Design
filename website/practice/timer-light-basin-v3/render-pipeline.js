import { PhotographyViewer } from './render/PhotographyViewer.js';

const viewers={};
document.querySelectorAll('[data-photo-viewer]').forEach((element)=>{
  viewers[element.id]=new PhotographyViewer(element);
});

document.querySelectorAll('[data-material-view]').forEach((button)=>{
  button.addEventListener('click',()=>{
    document.querySelectorAll('[data-material-view]').forEach((candidate)=>{
      const active=candidate===button;
      candidate.classList.toggle('is-active',active);
      candidate.setAttribute('aria-pressed',String(active));
    });
    viewers.materialStudio?.focus(button.dataset.materialView);
  });
});
