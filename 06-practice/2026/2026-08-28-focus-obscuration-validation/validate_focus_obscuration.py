from pathlib import Path
from playwright.sync_api import sync_playwright
import json, hashlib
ROOT=Path(__file__).parent
viewports=[('desktop',1280,720),('mobile',390,844)]
results=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for fixture in ['a_obscured.html','b_repaired.html']:
        for name,w,h in viewports:
            page=browser.new_page(viewport={'width':w,'height':h})
            page.set_content((ROOT/fixture).read_text(encoding='utf-8'), wait_until='load')
            page.keyboard.press('Tab')
            active=page.evaluate('document.activeElement && document.activeElement.id')
            geom=page.evaluate('''() => { const t=document.activeElement.getBoundingClientRect(); const h=document.querySelector('#sticky').getBoundingClientRect(); const s=getComputedStyle(document.activeElement); return {target:{x:t.x,y:t.y,w:t.width,h:t.height,bottom:t.bottom},header:{bottom:h.bottom},outline:s.outlineStyle,outlineWidth:s.outlineWidth}; }''')
            fully_hidden=geom['target']['bottom'] <= geom['header']['bottom']
            screenshot=ROOT/f"{fixture[:-5]}_{name}.png"
            page.screenshot(path=str(screenshot), full_page=False)
            results.append({'fixture':fixture,'viewport':name,'active':active,'fully_hidden_by_sticky_header':fully_hidden,'geometry':geom,'screenshot_sha256':hashlib.sha256(screenshot.read_bytes()).hexdigest()})
            page.close()
    browser.close()
(ROOT/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
assert all(r['active']=='target' for r in results)
assert all(r['fully_hidden_by_sticky_header'] for r in results if r['fixture']=='a_obscured.html')
assert all(not r['fully_hidden_by_sticky_header'] for r in results if r['fixture']=='b_repaired.html')
