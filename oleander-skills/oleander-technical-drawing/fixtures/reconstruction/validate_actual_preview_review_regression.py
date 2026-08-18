#!/usr/bin/env python3
import copy, json, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
VALIDATOR=ROOT/'tools'/'validate_actual_preview_review.py'
FIXTURE=Path(__file__).with_name('PREVIEW-REVIEW-01_REGISTER.json')

def run(data,should_pass,label):
    with tempfile.NamedTemporaryFile('w',suffix='.json',delete=False,encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2); p=Path(f.name)
    cp=subprocess.run([sys.executable,str(VALIDATOR),str(p)],capture_output=True,text=True)
    p.unlink(missing_ok=True)
    if (cp.returncode==0)!=should_pass:
        print(cp.stdout,cp.stderr); raise SystemExit('regression failed: '+label)
    print('PASS regression:',label)

def main():
    base=json.loads(FIXTURE.read_text(encoding='utf-8'))
    run(base,True,'positive preview receipt')
    bad=copy.deepcopy(base); bad['views']=[v for v in bad['views'] if v['mode']!='NEAR_READ']
    run(bad,False,'near-read is mandatory')
    bad=copy.deepcopy(base); bad['views']=[v for v in bad['views'] if v['mode']!='GRAYSCALE']
    run(bad,False,'color-dependent artifact requires grayscale readback')
    bad=copy.deepcopy(base); bad['review_result']='KEEP'
    run(bad,False,'machine receipt cannot award KEEP')
    bad=copy.deepcopy(base); bad['views'][0]['opened']=False
    run(bad,False,'preview must be explicitly opened')
    bad=copy.deepcopy(base); bad['review_result']='ISSUE_FOUND'; bad.pop('root_cause',None)
    run(bad,False,'issue result requires root cause')

if __name__=='__main__': main()
