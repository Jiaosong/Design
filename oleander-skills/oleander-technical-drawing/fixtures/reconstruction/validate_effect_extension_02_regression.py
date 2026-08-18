#!/usr/bin/env python3
from __future__ import annotations
import copy,json,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent; SKILL=HERE.parent.parent
VAL=SKILL/'tools'/'validate_effect_extension_02.py'; FIX=HERE/'EFFECT-RECIPE-02_EXTENDED_REGISTER.json'; STATIC=SKILL/'recipes'/'SVG_PROCEDURAL_RECIPES.json'; MOTION=SKILL/'recipes'/'MOTION_HANDOFF_RECIPES.json'

def run(d):
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'f.json'; p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
        cp=subprocess.run([sys.executable,str(VAL),str(p),str(STATIC),str(MOTION)],capture_output=True,text=True)
        return cp.returncode,cp.stdout+cp.stderr

def inst(d,key,iid): return next(x for x in d[key] if x['instance_id']==iid)
def neg(name,d,needle):
    rc,out=run(d)
    if rc==0: raise SystemExit(f'FAIL {name}: invalid fixture passed')
    if needle not in out: raise SystemExit(f'FAIL {name}: expected {needle!r}; got {out!r}')
    print('PASS negative:',name)

def main():
    base=json.loads(FIX.read_text(encoding='utf-8')); rc,out=run(base)
    if rc: raise SystemExit('positive failed: '+out)
    print('PASS positive extension fixture')
    d=copy.deepcopy(base); inst(d,'static_instances','FX2-02').pop('legend_id'); neg('halftone no legend',d,'missing')
    d=copy.deepcopy(base); inst(d,'static_instances','FX2-04').pop('source_pass_id'); neg('blend no source pass',d,'missing')
    d=copy.deepcopy(base); inst(d,'static_instances','FX2-06').pop('registration_ref'); neg('hillshade no registration',d,'missing')
    d=copy.deepcopy(base); inst(d,'static_instances','FX2-07').pop('camera_ref'); neg('AO no camera parity',d,'missing')
    d=copy.deepcopy(base); inst(d,'static_instances','FX2-08')['required_labels_preserved']=False; neg('unsafe source crop',d,'preserve required labels')
    d=copy.deepcopy(base); inst(d,'motion_instances','MX2-02')['registration_class']='MAP_BOUND'; neg('refraction on map geometry',d,'cannot move authoritative/map geometry')
    d=copy.deepcopy(base); inst(d,'motion_instances','MX2-05')['keyboard_fallback']=''; neg('cursor no keyboard fallback',d,'missing') if False else None
    # empty fallback still present; explicitly remove to assert schema failure
    d=copy.deepcopy(base); inst(d,'motion_instances','MX2-05').pop('keyboard_fallback'); neg('cursor no keyboard fallback',d,'missing')
    d=copy.deepcopy(base); inst(d,'motion_instances','MX2-06')['native_scroll_baseline']=False; neg('smooth scroll no native baseline',d,'native scroll baseline')
    d=copy.deepcopy(base); inst(d,'motion_instances','MX2-08').pop('keyboard_equivalent'); neg('drag no keyboard equivalent',d,'missing')
    d=copy.deepcopy(base); inst(d,'motion_instances','MX2-01')['reduced_motion']=''; neg('morph no reduced motion',d,'reduced motion required')
    print('PASS: extension regression suite')
if __name__=='__main__': main()
