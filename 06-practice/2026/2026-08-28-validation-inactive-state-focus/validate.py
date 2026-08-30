import asyncio,json, pathlib
from playwright.async_api import async_playwright
BASE=pathlib.Path('/mnt/data/oleander_validation_state_focus')
VIEWPORTS=[{'width':1280,'height':720},{'width':390,'height':844}]
async def run_one(browser,name,vp):
    page=await browser.new_page(viewport=vp)
    await page.set_content((BASE/name).read_text(),wait_until='load')
    await page.click('#tab-b')
    await page.wait_for_timeout(120)
    await page.evaluate('document.activeElement && document.activeElement.blur()')
    seq=[]
    for _ in range(6):
        await page.keyboard.press('Tab')
        seq.append(await page.evaluate('document.activeElement && document.activeElement.id'))
    axon=await page.locator('#panel-a').evaluate("e=>({hidden:e.hidden,aria:e.getAttribute('aria-hidden'),inert:e.inert,display:getComputedStyle(e).display,opacity:getComputedStyle(e).opacity,left:getComputedStyle(e).left})")
    section=await page.locator('#panel-b').evaluate("e=>({hidden:e.hidden,aria:e.getAttribute('aria-hidden'),inert:e.inert,display:getComputedStyle(e).display})")
    await page.close()
    return {'fixture':name,'viewport':vp,'settled_state':'SECTION','focus_sequence':seq,'inactive_axon':axon,'active_section':section,'ghost_focus_present':'a-hotspot' in seq}
async def main():
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
        out=[]
        for vp in VIEWPORTS:
            out.append(await run_one(browser,'fixture_a.html',vp))
            out.append(await run_one(browser,'fixture_b.html',vp))
        await browser.close()
    pathlib.Path(BASE/'results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
    bad=[x for x in out if x['fixture']=='fixture_a.html']
    good=[x for x in out if x['fixture']=='fixture_b.html']
    assert all(x['ghost_focus_present'] for x in bad), bad
    assert all(not x['ghost_focus_present'] for x in good), good
    assert all(x['inactive_axon']['hidden'] and x['inactive_axon']['inert'] for x in good), good
asyncio.run(main())
