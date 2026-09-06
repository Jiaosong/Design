from pathlib import Path
from playwright.sync_api import sync_playwright
import json, sys, importlib.metadata, subprocess
root=Path(__file__).parent
results={"tool":{"playwright_python":importlib.metadata.version('playwright'),"chromium":subprocess.check_output(['/usr/bin/chromium','--version'],text=True).strip()},"cases":[]}
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    for fname in ['A_animationend_dependency.html','B_reduced_motion_state_equivalent.html']:
        for pref in ['no-preference','reduce']:
            page=browser.new_page(viewport={"width":800,"height":600},reduced_motion=pref)
            page.set_content((root/fname).read_text(encoding='utf-8'), wait_until='load')
            media=page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches")
            page.click('#go')
            page.wait_for_timeout(450)
            status=page.locator('#status').inner_text()
            transform=page.locator('#panel').evaluate("e=>getComputedStyle(e).transform")
            results['cases'].append({"fixture":fname,"preference":pref,"media_matches":media,"status_after_450ms":status,"transform":transform})
            page.close()
    browser.close()
A=[x for x in results['cases'] if x['fixture'].startswith('A_')]
B=[x for x in results['cases'] if x['fixture'].startswith('B_')]
results['assertions']={
 "A_no_preference_ready": next(x for x in A if x['preference']=='no-preference')['status_after_450ms']=='ready',
 "A_reduce_fails_state_equivalence": next(x for x in A if x['preference']=='reduce')['status_after_450ms']!='ready',
 "B_no_preference_ready": next(x for x in B if x['preference']=='no-preference')['status_after_450ms']=='ready',
 "B_reduce_ready": next(x for x in B if x['preference']=='reduce')['status_after_450ms']=='ready',
}
results['verdict']='PASS_FOR_BOUNDED_REDUCED_MOTION_STATE_EQUIVALENCE' if all(results['assertions'].values()) else 'REVISE'
(root/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
sys.exit(0 if results['verdict'].startswith('PASS') else 2)
