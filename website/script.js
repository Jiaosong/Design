const grid=document.createElement('style');
grid.textContent='@media (min-width:1180px){.daylily-opening,.reno-opening{grid-template-columns:repeat(12,minmax(0,1fr))!important;gap:clamp(18px,1.65vw,24px)!important}}#home>.section-coordinate{opacity:1!important;color:#5f625d!important}#break>.chapter-coordinate{color:#b8b5ad!important;opacity:1!important}';
document.head.appendChild(grid);

['visual-hierarchy.css','visual-contrast.css','visual-encounter-title.css','visual-encounter-image.css','visual-opening-frame.css','visual-opening-grid.css','visual-opening-image.css','media-integrity.css'].forEach((href)=>{
  const link=document.createElement('link');
  link.rel='stylesheet';
  link.href=href;
  document.head.appendChild(link);
});

const base=document.createElement('script');
base.src='script-base.js';
base.onload=()=>{
  const expression=document.createElement('script');
  expression.src='expression.js';
  expression.onload=()=>{
    const media=document.createElement('script');
    media.src='media-integrity.js';
    media.onload=()=>document.documentElement.setAttribute('data-oleander-ready','true');
    document.body.appendChild(media);
  };
  document.body.appendChild(expression);
};
document.body.appendChild(base);
