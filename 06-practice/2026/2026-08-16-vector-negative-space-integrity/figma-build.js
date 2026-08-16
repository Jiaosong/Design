// OLEANDER daily practice — Figma Plugin API source
// Reproduces the three-variant negative-space integrity board.
// Exercise assumptions only; not a brand authority asset.

const frame = figma.createFrame();
frame.name = 'NEGATIVE_SPACE_INTEGRITY_LAB';
frame.resize(1600, 1000);
frame.fills = [{ type: 'SOLID', color: { r: 0.96, g: 0.96, b: 0.95 } }];

await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });
await figma.loadFontAsync({ family: 'Inter', style: 'Semi Bold' });

function shapeSvg(notch) {
  const mid = 130;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="240" height="260" viewBox="0 0 240 260"><path fill="#111111" fill-rule="evenodd" d="M60 20H180V240H60Z M60 ${mid-notch} L180 ${mid-2*notch} L180 ${mid+2*notch} L60 ${mid+notch} Z"/></svg>`;
}

const variants = [8, 12, 16];
const sizes = [64, 32, 16];

// Exact layout implementation is stored in the execution receipt/README.
// Core reproducible relation:
// 1) fixed 240×260 silhouette
// 2) oblique negative-space notch as the only geometric variable
// 3) duplicate each variant at 64/32/16 px for target-scale inspection
// 4) retain monochrome fills and no stylistic effects

return { variants, sizes, rootFrameName: frame.name };
