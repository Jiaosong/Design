from pathlib import Path
import hashlib, shutil, subprocess
root=Path(__file__).resolve().parent
base=root.parent/'app-v1.28-ch14-route03-successor-candidate'
if not base.exists(): base=root.parent/'C04_QINGJIANG_APP_v1_28_CH14_ROUTE03_SUCCESSOR_CANDIDATE'
# Reassemble exact v1.28 base when repository chunks are present; local handoff may already contain full source.
if (base/'REASSEMBLE.py').exists():
    subprocess.run(['python',str(base/'REASSEMBLE.py')],check=True)
    base_src=base/'reassembled'
else:
    base_src=base
out=root/'reassembled'
out.mkdir(exist_ok=True)
index=(base_src/'index.html').read_text(encoding='utf-8')
css=(base_src/'app.css').read_text(encoding='utf-8')
js=(base_src/'app.js').read_text(encoding='utf-8')
index=index.replace('<title>清江石书 App v1.28 Candidate｜CH14 × ROUTE-03</title>','<title>清江石书 App v1.29 Candidate｜CH14 × ROUTE-03</title>')
needle='  <div class="status-line" id="statusLine"><span id="statusName">UNKNOWN</span><i></i><span id="digitalName">FULL</span><i></i><span>NTS / NOT GPS</span></div>\n'
index=index.replace(needle,needle+'  <div class="explore-cue" id="exploreCue" aria-hidden="true"><span>EXPLORE</span><i></i><b id="exploreState">INTENT</b></div>\n',1)
css=css+'\n\n'+(root/'GAME_TEXTURE_PATCH_v1_29.css').read_text(encoding='utf-8')
js=js.replace("c04.qingjiang.app.v128.framework","c04.qingjiang.app.v129.framework")
old="function setBehavior(state){clearTimeout(resetTimer);app.dataset.behavior=state;const el=document.getElementById('behaviorReadout');if(el)el.textContent=state.toUpperCase()}"
new="function setBehavior(state){clearTimeout(resetTimer);app.dataset.behavior=state;const el=document.getElementById('behaviorReadout');if(el)el.textContent=state.toUpperCase();const cue=document.getElementById('exploreState');if(cue)cue.textContent=state.toUpperCase()}"
js=js.replace(old,new,1)
for name,data in [('index.html',index.encode()),('app.css',css.encode()),('app.js',js.encode())]:
    (out/name).write_bytes(data)
expected={'index.html':'3f228c90122c8b546ca71a1092ef5c5cc2320ef6','app.css':'4b1c1407c5487a57aa3d1d44d06c9349e960b515','app.js':'9a4b61f8cad07f4878d7707016fc4d9ab997bfc1'}
for name,sha in expected.items():
    data=(out/name).read_bytes(); got=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
    if got!=sha: raise SystemExit(f'{name}: {got} != {sha}')
    print(name,got,'EXACT')
