#!/usr/bin/env python3
import base64, asyncio, hashlib, json, pathlib, subprocess
from PIL import Image, ImageChops
from playwright.async_api import async_playwright

FONT = pathlib.Path('/usr/share/fonts/opentype/cantarell/Cantarell-VF.otf')
OUT = pathlib.Path('out'); OUT.mkdir(exist_ok=True)
TEXT = 'OLEANDER Variable 700'

async def main():
    raw = FONT.read_bytes(); b64 = base64.b64encode(raw).decode()
    rec = {'font_sha256': hashlib.sha256(raw).hexdigest(), 'source_font': str(FONT)}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        page = await browser.new_page(viewport={'width':800,'height':300})
        for w in (400,700):
            html = f'''<!doctype html><meta charset="utf-8"><style>@font-face{{font-family:CantVF;src:url(data:font/otf;base64,{b64}) format("opentype");font-weight:100 800}}body{{margin:0;width:800px;height:300px;display:flex;align-items:center;justify-content:center}}#t{{font-family:CantVF,sans-serif;font-size:72px;font-variation-settings:"wght" {w}}}</style><div id="t">{TEXT}</div>'''
            await page.set_content(html, wait_until='load'); await page.evaluate('document.fonts.ready')
            rec[str(w)] = {
                'fontFamily': await page.eval_on_selector('#t','e=>getComputedStyle(e).fontFamily'),
                'fontVariationSettings': await page.eval_on_selector('#t','e=>getComputedStyle(e).fontVariationSettings'),
                'bbox': await page.eval_on_selector('#t','e=>e.getBoundingClientRect().toJSON()')}
            await page.pdf(path=str(OUT/f'w{w}.pdf'), width='800px', height='300px', print_background=True)
        await browser.close()
    for w in (400,700):
        subprocess.run(['pdftoppm','-png','-singlefile','-r','96',str(OUT/f'w{w}.pdf'),str(OUT/f'pdf_w{w}')],check=True,stdout=subprocess.DEVNULL)
        rec[str(w)]['pdffonts'] = subprocess.check_output(['pdffonts',str(OUT/f'w{w}.pdf')],text=True)
        rec[str(w)]['pdftotext'] = subprocess.check_output(['pdftotext',str(OUT/f'w{w}.pdf'),'-'],text=True).strip()
    a=Image.open(OUT/'pdf_w400.png').convert('L'); b=Image.open(OUT/'pdf_w700.png').convert('L'); d=ImageChops.difference(a,b)
    rec['pdf_raster_diff']={'bbox':d.getbbox(),'extrema':d.getextrema(),'nonzero_pixels':sum(1 for p in d.getdata() if p!=0)}
    for p in ('w400.pdf','w700.pdf','pdf_w400.png','pdf_w700.png'):
        rec.setdefault('sha256',{})[p]=hashlib.sha256((OUT/p).read_bytes()).hexdigest()
    pathlib.Path('validation_results.json').write_text(json.dumps(rec,indent=2),encoding='utf-8')
    assert rec['400']['fontVariationSettings'] == '"wght" 400'
    assert rec['700']['fontVariationSettings'] == '"wght" 700'
    assert rec['pdf_raster_diff']['nonzero_pixels'] > 0
    assert 'yes yes yes' in rec['400']['pdffonts'] and 'yes yes yes' in rec['700']['pdffonts']

asyncio.run(main())
