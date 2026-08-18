#!/usr/bin/env python3
"""Build a standalone native HTML demo from motion handoff instances.

The generated demo uses CSS/WAAPI/normal scroll only. It is a regression/runtime
smoke artifact and does not prove AR-S10, accessibility or Design KEEP.
"""
from __future__ import annotations
import html
import json
import random
import sys
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def by_recipe(instances, rid):
    return next((i for i in instances if i.get("recipe_id") == rid), None)


def main():
    if len(sys.argv) != 3:
        print("usage: build_motion_recipe_demo.py REGISTER OUTPUT.html")
        raise SystemExit(2)
    reg = load(Path(sys.argv[1]))
    out = Path(sys.argv[2])
    motions = [i for i in reg.get("effect_instances", []) if i.get("kind") == "MOTION_HANDOFF"]
    path = by_recipe(motions, "TD-MR01-PATH-TRACE")
    handoff = by_recipe(motions, "TD-MR04-SHARED-CONTAINER-HANDOFF")
    scroll = by_recipe(motions, "TD-MR07-SCROLL-PROGRESS")
    particles = by_recipe(motions, "TD-MR12-PARTICLE-FIELD")
    path_duration = int((path or {}).get("parameters", {}).get("duration_ms", 760))
    handoff_duration = int((handoff or {}).get("parameters", {}).get("duration_ms", 360))

    rng = random.Random(17)
    particle_html = []
    for n in range(28):
        x = rng.uniform(4, 96); y = rng.uniform(10, 90); dx = rng.uniform(28, 95); dy = rng.uniform(-18, 18); delay = rng.uniform(-4.0, 0.0); dur = rng.uniform(3.5, 7.0)
        particle_html.append(
            f'<i class="particle" style="--x:{x:.2f}%;--y:{y:.2f}%;--dx:{dx:.2f}px;--dy:{dy:.2f}px;--delay:{delay:.2f}s;--dur:{dur:.2f}s"></i>'
        )

    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OLEANDER Motion Recipe Smoke Demo</title>
<style>
:root{{--paper:#f3f0e8;--ink:#17231f;--muted:#68716c;--teal:#4d8d92;--rust:#a95a4e}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--paper);color:var(--ink);font-family:system-ui,sans-serif}}
main{{max-width:1100px;margin:auto;padding:36px}} h1{{font-size:28px;margin:0 0 8px}} p{{color:var(--muted);line-height:1.55}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px;margin-top:28px}} article{{min-height:270px;background:#faf8f2;border:1px solid #c9c5b8;border-radius:16px;padding:18px;overflow:hidden}}
.k{{font:700 11px/1.2 ui-monospace,monospace;letter-spacing:.08em;color:var(--muted)}} .demo{{height:190px;margin-top:14px;border-top:1px solid #ddd8cc;position:relative;overflow:hidden}}
.path-trace{{fill:none;stroke:var(--teal);stroke-width:7;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;animation:pathTrace {path_duration}ms linear 300ms both}}
@keyframes pathTrace{{to{{stroke-dashoffset:0}}}}
.handoff-stage{{position:relative;height:100%}} .anchor{{position:absolute;width:76px;height:76px;border:2px solid var(--ink);border-radius:12px;display:grid;place-items:center;background:var(--paper);transition:transform {handoff_duration}ms cubic-bezier(.65,0,.35,1),width {handoff_duration}ms cubic-bezier(.65,0,.35,1),height {handoff_duration}ms cubic-bezier(.65,0,.35,1)}}
.anchor.a{{left:18px;top:52px}} .anchor.b{{left:250px;top:30px;width:170px;height:120px}} .handoff-stage[data-state="b"] .anchor.a{{transform:translate(232px,-22px);width:170px;height:120px}} .handoff-stage[data-state="b"] .anchor.b{{opacity:.08}} button{{border:1px solid #9d9b92;background:#fff;padding:7px 10px;border-radius:9px;cursor:pointer}}
.scroll-track{{height:1250px;position:relative;background:linear-gradient(#faf8f2,#ede7db)}} .progress{{position:sticky;top:0;height:8px;background:#d8d5ca}} .progress>span{{display:block;height:100%;width:0;background:var(--teal)}} .scroll-note{{position:sticky;top:28px;padding:18px;color:var(--muted)}}
.field{{position:relative;height:100%;background:linear-gradient(90deg,rgba(77,141,146,.08),rgba(77,141,146,.01))}} .particle{{position:absolute;left:var(--x);top:var(--y);width:4px;height:4px;border-radius:50%;background:var(--teal);opacity:.55;animation:flow var(--dur) linear var(--delay) infinite}} @keyframes flow{{to{{transform:translate(var(--dx),var(--dy));opacity:.12}}}}
@media(max-width:760px){{.grid{{grid-template-columns:1fr}}}}
@media(prefers-reduced-motion:reduce){{.path-trace{{animation:none;stroke-dashoffset:0}} .anchor{{transition:none}} .particle{{animation:none}}}}
</style></head><body><main>
<div class="k">OLEANDER / TECHNICAL DRAWING × MOTION / NATIVE SMOKE DEMO</div><h1>Motion handoff recipes</h1><p>No library dependency. Motion is optional; static endpoints and normal scrolling remain available. Runtime review is still pending.</p>
<section class="grid">
<article data-recipe="TD-MR01-PATH-TRACE"><div class="k">TD-MR01 / EF-03</div><strong>Path trace</strong><div class="demo"><svg viewBox="0 0 480 190" width="100%" height="100%"><path class="path-trace" pathLength="1" d="M30 145 C105 120 125 55 205 80 S315 150 445 44"/><circle cx="30" cy="145" r="7" fill="#17231f"/><circle cx="445" cy="44" r="7" fill="#a95a4e"/></svg></div></article>
<article data-recipe="TD-MR04-SHARED-CONTAINER-HANDOFF"><div class="k">TD-MR04 / EF-01</div><strong>Shared container continuity</strong> <button id="toggle">toggle state</button><div class="demo handoff-stage" id="handoff" data-state="a"><div class="anchor a">R06</div><div class="anchor b">DETAIL</div></div></article>
<article data-recipe="TD-MR07-SCROLL-PROGRESS"><div class="k">TD-MR07 / EF-06</div><strong>Native scroll progress</strong><div class="demo" style="overflow:auto"><div class="scroll-track" id="scrollTrack"><div class="progress"><span id="bar"></span></div><div class="scroll-note">Normal scroll remains the baseline. Progress is bound to actual scroll extent; no pinning or scroll-jacking.</div></div></div></article>
<article data-recipe="TD-MR12-PARTICLE-FIELD"><div class="k">TD-MR12 / EF-16</div><strong>Modelled particle / flow field</strong><div class="demo field">{''.join(particle_html)}<div style="position:absolute;left:12px;bottom:10px;font-size:11px;color:#68716c">MODELLED / NOT FIELD OBSERVED</div></div></article>
</section>
<p class="k" style="margin-top:24px">Regression demo only · reduced motion supported · no Design KEEP / AR-S10 PASS claimed</p>
</main><script>
const stage=document.getElementById('handoff'); document.getElementById('toggle').addEventListener('click',()=>stage.dataset.state=stage.dataset.state==='a'?'b':'a');
const scroller=document.querySelector('[data-recipe="TD-MR07-SCROLL-PROGRESS"] .demo'); const bar=document.getElementById('bar');
function updateProgress(){{const max=Math.max(1,scroller.scrollHeight-scroller.clientHeight); const p=Math.max(0,Math.min(1,scroller.scrollTop/max)); bar.style.width=(p*100).toFixed(2)+'%';}}
scroller.addEventListener('scroll',updateProgress,{{passive:true}}); updateProgress();
</script></body></html>'''
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    required = ["prefers-reduced-motion", "TD-MR01-PATH-TRACE", "TD-MR04-SHARED-CONTAINER-HANDOFF", "TD-MR07-SCROLL-PROGRESS", "TD-MR12-PARTICLE-FIELD"]
    missing = [s for s in required if s not in doc]
    if missing:
        raise SystemExit(f"FAIL: generated demo missing {missing}")
    print(f"PASS: generated native motion demo {out}; recipes={len(motions)}; reduced-motion marker present")


if __name__ == "__main__":
    main()
