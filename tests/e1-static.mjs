import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const html = await readFile(new URL('../website/index.html', import.meta.url), 'utf8');
const css = await readFile(new URL('../website/styles.css', import.meta.url), 'utf8');

const ids = [...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]);
const duplicateIds = ids.filter((id, index) => ids.indexOf(id) !== index);
assert.deepEqual([...new Set(duplicateIds)], [], `Duplicate IDs: ${duplicateIds.join(', ')}`);

const idSet = new Set(ids);
for (const attribute of ['aria-controls', 'aria-labelledby', 'aria-describedby']) {
  for (const match of html.matchAll(new RegExp(`\\s${attribute}="([^"]+)"`, 'g'))) {
    for (const id of match[1].split(/\s+/)) {
      assert(idSet.has(id), `${attribute} references missing ID: ${id}`);
    }
  }
}

for (const match of html.matchAll(/<img\b([^>]*)>/g)) {
  assert(/\salt="[^"]*"/.test(match[1]), `Image is missing alt text: ${match[0].slice(0, 120)}`);
}

for (const match of html.matchAll(/\shref="#([^"]*)"/g)) {
  assert(match[1] && idSet.has(match[1]), `Anchor references missing ID: #${match[1]}`);
}

assert(/@font-face/.test(css), 'Local font-face declarations are required.');
assert(/scroll-margin-top/.test(css), 'Fixed-header anchor offset is required.');
assert(/prefers-reduced-motion:\s*reduce/.test(css), 'Reduced-motion styles are required.');

console.log(`E1 static checks passed: ${ids.length} IDs, resolved ARIA references, image alternatives, anchors, fonts, offsets, and reduced motion.`);
