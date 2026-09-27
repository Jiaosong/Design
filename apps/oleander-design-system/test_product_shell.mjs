import fs from 'node:fs'
import path from 'node:path'
import assert from 'node:assert/strict'

const root = path.dirname(new URL(import.meta.url).pathname.replace(/^\/(?:[A-Za-z]:)/, match => match.slice(1)))
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8')
const js = fs.readFileSync(path.join(root, 'app.js'), 'utf8')
const css = fs.readFileSync(path.join(root, 'styles.css'), 'utf8')

for (const view of ['Home', 'Projects', 'Design', 'Knowledge', 'Sources', 'Browser', 'Integrations', 'Review', 'System']) {
  assert.match(js, new RegExp(`['\"]${view}['\"]`), `missing navigation view ${view}`)
}

for (const stage of ['R1', 'R2', 'R3', 'R4', 'R5']) {
  assert.match(js, new RegExp(`['\"]${stage}['\"]`), `missing reliability stage ${stage}`)
}

assert.match(js, /STAGED_LOCAL_ONLY/)
assert.match(js, /api\/source\/init/)
assert.match(js, /api\/source\/chunk/)
assert.match(js, /api\/source\/commit/)
assert.match(js, /KNOWLEDGE_DRAFT_READY/)
assert.match(js, /External Knowledge Surfaces/)
assert.match(js, /Linked source\/view ≠ OLEANDER Knowledge Current/)
assert.match(js, /Git branch ≠ Design Direction/)
assert.match(js, /Imported ≠ Knowledge Current/)
assert.match(js, /PAGE_LOADED ≠ SOURCE_CAPTURED/)
assert.doesNotMatch(js, /state\.reliability\.R[1-4]\s*=\s*['\"]PASS['\"]/, 'UI must not fabricate Surface Reliability PASS states')
assert.match(js, /api\/surface-views/)
assert.match(js, /api\/hosts/)
assert.match(html, /Host Runtime 未绑定/)
assert.match(css, /\.app-shell/)

console.log('PASS OLEANDER Design System product shell static contract')
